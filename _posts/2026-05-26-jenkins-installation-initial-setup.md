---
layout: single
title: "Jenkins 02. Jenkins 설치와 초기 설정"
description: "Docker로 Jenkins를 실행하고 초기 비밀번호, 플러그인 선택, 관리자 계정, Jenkins URL, 오류 대응까지 확인하는 설치 절차."
date: 2026-05-26 09:00:00 +09:00
lang: ko
translation_key: jenkins-installation-initial-setup
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, installation, initial-setup, java, docker]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Jenkins 설치는 "어떤 버튼을 누르느냐"보다 "어디에 controller 상태를 보관하고, 어떤 Java로 실행하고, 어떤 plugin을 처음부터 넣을 것인가"를 먼저 정하는 작업이다. 특히 Jenkins는 UI 설정, job 설정, credential, plugin 상태가 `JENKINS_HOME`에 쌓이므로 이 경로를 임시 공간처럼 다루면 안 된다.

이 글의 결론은 초급 실습에서는 Docker 설치가 흐름을 이해하기 쉽지만, 운영 설치에서는 Java 버전, 저장소, 백업, 네트워크 포트, plugin 목록을 설치 전 체크리스트로 분리해야 한다는 것이다.

## 이 글에서 할 수 있는 것

- Docker named volume에 `/var/jenkins_home`을 보존하면서 Jenkins controller를 실행한다.
- 초기 관리자 비밀번호를 container log 또는 `/var/jenkins_home/secrets/initialAdminPassword`에서 확인한다.
- `http://localhost:8080`에서 초기 화면에 접근하고 setup wizard를 끝낸다.
- 추천 플러그인 설치와 선택 설치의 차이를 이해하고, 첫 관리자 계정과 Jenkins URL을 설정한다.
- 재시작 후 설정이 유지되는지 확인하고, 실습 환경을 안전하게 정리한다.
- 포트 충돌, volume 권한, Java 버전, plugin 설치 실패, 초기 비밀번호 파일 문제를 어디서 확인할지 안다.

## 사전 준비

- 실행 위치: Docker가 설치된 로컬 Linux, macOS, Windows WSL 또는 Docker Desktop 환경
- shell: Bash 계열 예시
- 권한: 현재 사용자가 `docker` 명령을 실행할 수 있어야 한다. Linux에서 권한이 없으면 `sudo docker ...` 형태로 바꿔 실행한다.
- 포트: host의 `8080` 포트가 비어 있어야 한다. 이미 사용 중이면 아래 예시에서 `8080:8080`을 `18080:8080`처럼 바꾼다.
- 실습 범위: 이 절차는 로컬 실습용이다. 운영 환경에서는 이 글 뒤의 "운영으로 가져갈 때 주의할 점"을 별도로 확인해야 한다.

## 최종 결과

실습이 끝나면 아래 상태가 되어야 한다.

- `jenkins` container가 실행 중이다.
- `jenkins_home` Docker volume이 `/var/jenkins_home`에 연결되어 있다.
- 브라우저에서 `http://localhost:8080`에 접속할 수 있다.
- 초기 관리자 계정과 Jenkins URL 설정이 끝난다.
- container를 재시작해도 Jenkins 설정이 유지된다.

## 빠른 실행 절차

```bash
docker volume create jenkins_home
```

```bash
docker run \
  --name jenkins \
  --detach \
  --publish 8080:8080 \
  --publish 50000:50000 \
  --volume jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

Jenkins가 올라오는 동안 로그를 확인한다.

```bash
docker logs -f jenkins
```

초기 관리자 비밀번호는 아래 명령으로 확인한다.

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

또는 `docker logs jenkins` 출력에서 `Please use the following password to proceed to installation` 주변의 값을 확인한다.

브라우저에서 아래 주소로 접속한다.

```text
http://localhost:8080
```

초기 화면에서는 다음 순서로 진행한다.

1. `Unlock Jenkins` 화면에서 초기 관리자 비밀번호를 붙여 넣는다.
2. `Customize Jenkins` 화면에서 초급 실습은 `Install suggested plugins`를 선택한다.
3. 운영 설치 준비라면 `Select plugins to install`를 선택하고 필요한 plugin 이름과 이유를 따로 기록한다.
4. `Create First Admin User` 화면에서 임시 계정이 아니라 계속 사용할 관리자 계정을 만든다.
5. `Instance Configuration` 화면에서 실습은 `http://localhost:8080/`을 사용한다. 운영에서는 실제 외부 접근 URL과 reverse proxy 경계를 먼저 정한다.

## 정상 동작 확인

container가 실행 중인지 확인한다.

```bash
docker ps --filter name=jenkins
```

HTTP 응답이 오는지 확인한다.

```bash
curl -I http://localhost:8080/login
```

Docker volume이 연결되어 있는지 확인한다.

{% raw %}
```bash
docker inspect jenkins --format '{{ range .Mounts }}{{ .Name }} -> {{ .Destination }}{{ println }}{{ end }}'
```
{% endraw %}

재시작 후 설정 유지 여부를 확인한다.

```bash
docker restart jenkins
docker exec jenkins test -f /var/jenkins_home/config.xml && echo "JENKINS_HOME persisted"
```

위 명령이 `JENKINS_HOME persisted`를 출력하면 Jenkins home directory가 volume에 보존되고 있다는 뜻이다.

## 예시: 첫 Jenkinsfile로 빌드 성공 확인

이 예시는 설치가 끝난 뒤 Pipeline job을 하나 만들어 Jenkins가 실제로 job을 실행할 수 있는지 확인하는 최소 예시다. 운영용 pipeline이 아니라 controller 동작 확인용 실습이다.

저장소 루트에 `Jenkinsfile`을 둔다.

```groovy
pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                echo 'Hello, Jenkins'
            }
        }
    }
}
```

UI에서 `New Item` -> `Pipeline`을 선택하고, Pipeline definition을 `Pipeline script from SCM` 또는 실습용 `Pipeline script`로 지정한다. 빌드 후 `Console Output`에서 아래와 비슷한 줄을 확인한다.

정상 결과 예시:

```text
[Pipeline] echo
Hello, Jenkins
Finished: SUCCESS
```

`Finished: SUCCESS`가 보이면 Jenkins controller가 job을 받고, pipeline 문법을 해석하고, stage를 실행한 것이다. 운영에서는 controller에서 직접 build를 많이 돌리지 말고 agent 분리와 credential 범위를 별도로 설계해야 한다.

## 삭제와 정리

container만 지우면 volume은 남는다.

```bash
docker stop jenkins
docker rm jenkins
```

실습 데이터를 완전히 삭제할 때만 volume을 지운다. 운영 또는 재사용할 실습 환경에서는 이 명령을 실행하지 않는다.

```bash
docker volume rm jenkins_home
```

## 자주 나는 오류

### 8080 포트 충돌

증상: `Bind for 0.0.0.0:8080 failed` 또는 브라우저에서 다른 서비스가 열린다.

대표 에러 메시지 예시:

```text
Bind for 0.0.0.0:8080 failed: port is already allocated
```

확인:

{% raw %}
```bash
docker ps --format 'table {{.Names}}\t{{.Ports}}'
```
{% endraw %}

Linux/macOS에서는 host에서 8080을 쓰는 process도 확인한다.

```bash
lsof -i :8080
```

해결: host 포트를 바꿔 실행한다.

```bash
docker run \
  --name jenkins \
  --detach \
  --publish 18080:8080 \
  --publish 50000:50000 \
  --volume jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

이 경우 접속 주소는 `http://localhost:18080`이다.

### volume 권한 문제

증상: Jenkins가 시작되지 않거나 `/var/jenkins_home`에 쓸 수 없다는 로그가 나온다.

확인:

```bash
docker logs jenkins
```

해결: 초급 실습에서는 host bind mount보다 named volume을 우선 사용한다. host directory를 직접 연결해야 한다면 운영 정책에 맞게 소유자와 권한을 조정하고, 임시 해결로 `chmod 777`을 적용하지 않는다.

### Java 버전 문제

증상: Docker가 아닌 설치에서 Jenkins가 Java 요구사항 때문에 시작하지 않는다.

확인:

```bash
java -version
```

해결: 설치하려는 Jenkins LTS의 Java Support Policy를 먼저 확인한다. 공식 `jenkins/jenkins:lts` Docker image를 쓰는 실습에서는 image 안에 Jenkins 실행용 Java가 포함되므로 host의 Java 버전과 분리해서 생각한다.

### 플러그인 설치 실패

증상: setup wizard에서 plugin 다운로드가 실패하거나 오래 멈춘다.

확인:

```bash
docker logs jenkins
```

해결: 네트워크, proxy, DNS, update center 접근 가능 여부를 확인한다. 운영 환경에서는 처음부터 모든 추천 plugin을 무조건 설치하지 말고 필요한 plugin 목록을 기록한 뒤 재현 가능한 방식으로 관리한다.

### 초기 비밀번호 파일을 찾지 못함

증상: `/var/jenkins_home/secrets/initialAdminPassword` 파일이 없다고 나온다.

확인:

```bash
docker logs jenkins
docker exec jenkins ls -la /var/jenkins_home/secrets
```

해결: container가 아직 초기화 중이면 조금 기다린 뒤 다시 확인한다. 이미 setup wizard를 끝낸 기존 volume을 재사용 중이라면 새 초기 비밀번호 흐름이 다시 나타나지 않을 수 있다. 실습을 처음부터 다시 할 때만 container와 volume을 함께 삭제하고 다시 만든다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-06-05
- 문서 성격: tutorial
- 테스트 환경: 작성자 Jenkins 실습 서버에서 2026-04-24 확인한 로그인 응답 헤더와, 2026-06-05 확인한 Jenkins 공식 Docker 설치 문서를 함께 기준으로 삼았다. OS는 Linux 22.04이며, agent 구성은 이 글에 고정하지 않았다.
- 테스트 버전: 작성자 Jenkins 실습 서버 Jenkins 2.541.3(2026-04-24 로그인 응답 헤더 기준). Java 요구사항과 Docker 설치 절차는 2026-06-05 확인한 Jenkins 공식 문서를 기준으로 했다.
- 출처 등급: Jenkins 공식 문서와 Jenkins LTS changelog를 사용했다.
- 비고: 이 글의 Docker 명령은 로컬 실습용 절차다. 운영 적용 전에는 Jenkins LTS, Java 요구사항, plugin 호환성, 백업/복구 절차를 다시 확인해야 한다.

## 문제 정의

Jenkins를 처음 설치할 때 자주 생기는 문제는 아래와 같다.

- Jenkins controller의 상태 저장 위치를 신경 쓰지 않는다.
- Java 요구사항을 설치 후에야 확인한다.
- plugin을 "추천"이라는 이유만으로 모두 설치하고 관리 기준을 남기지 않는다.
- 초기 관리자 계정과 URL, 포트 설정을 임시값으로 만든 뒤 운영에 그대로 둔다.

이번 글은 Docker 기반 첫 설치 절차를 먼저 제시하고, 그 뒤 설치 전에 무엇을 결정해야 하는지 정리한다.

## 확인된 사실

- Jenkins 설치 공식 문서 기준으로 Jenkins 설치 절차는 새 설치를 대상으로 하며, Jenkins는 일반적으로 독립 프로세스로 실행된다.
  근거: [Installing Jenkins](https://www.jenkins.io/doc/book/installing/)
- Jenkins LTS changelog와 Java Support Policy 기준으로 2026-04-24 확인한 Jenkins LTS 2.555.1은 Java 21 또는 Java 25가 필요하다.
  근거: [LTS Changelog](https://www.jenkins.io/changelog-stable/), [Java Support Policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/)
- 직접 확인한 작성자 Jenkins 실습 서버는 2026-04-24 로그인 응답 헤더 기준 Jenkins 2.541.3이다. Java 요구사항은 LTS 버전별로 달라질 수 있으므로 설치 전 실제 설치 대상 버전의 Java Support Policy를 확인해야 한다.
  근거: 작성자 Jenkins 실습 서버 로그인 응답 헤더 확인
- Jenkins Docker 설치 문서 기준으로 Docker 방식 설치에서도 `/var/jenkins_home`을 volume으로 연결해 Jenkins home directory를 보존하는 절차가 제시된다.
  근거: [Installing Jenkins - Docker](https://www.jenkins.io/doc/book/installing/docker/)
- Jenkins Docker 설치 문서 기준으로 초기 관리자 비밀번호는 Docker 실행 시 `/var/jenkins_home/secrets/initialAdminPassword`에서 확인할 수 있다.
  근거: [Installing Jenkins - Docker](https://www.jenkins.io/doc/book/installing/docker/)
- Jenkins Initial Settings 문서 기준으로 Jenkins networking 설정은 command line argument로 조정할 수 있고, 기본 HTTP port는 8080이다.
  근거: [Initial Settings](https://www.jenkins.io/doc/book/installing/initial-settings/)

초급 실습의 최소 흐름은 아래처럼 정리할 수 있다.

```text
Java 요구사항 확인
설치 방식 선택
JENKINS_HOME 보존 방식 결정
Jenkins controller 실행
initialAdminPassword 확인
plugin 선택
관리자 계정 생성
Jenkins URL과 기본 보안 설정 확인
```

## 직접 재현한 결과

- 직접 재현함: 작성자 Jenkins 실습 서버에서 2026-04-24 비인증 로그인 페이지 응답 헤더의 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다.
- 공식 문서로 확인한 결과: 2026-06-05 기준 Jenkins Docker 설치 문서에서 `/var/jenkins_home` volume 연결, 초기 관리자 비밀번호 확인, setup wizard 흐름을 확인했다.
- 이번 수정에서 직접 실행하지 않은 항목: 현재 작업 환경에서 새 Docker container를 띄워 setup wizard를 끝까지 재현하지는 않았다. 위 명령은 공식 문서와 이전 실습 흐름을 바탕으로 한 로컬 실습 절차다.

## 해석 / 의견

내 판단으로는 Jenkins 설치에서 가장 먼저 고정해야 할 값은 `JENKINS_HOME`이다. Jenkins는 단순 실행 파일이 아니라 controller 상태를 계속 축적하는 서버다. 이 디렉터리를 잃으면 job 설정, plugin 상태, 일부 credential 관련 데이터, build 기록을 잃을 수 있다.

초급 실습에서는 Docker 방식이 좋다. Docker 글에서 배운 image, container, volume 개념을 바로 연결할 수 있고, 실습을 지우고 다시 만들기도 쉽다. 하지만 운영에서는 Docker 여부보다 아래 항목이 더 중요하다.

- Java 요구사항을 LTS 기준으로 맞췄는가
- controller data directory를 백업 가능한 위치에 두었는가
- plugin 목록과 설치 이유를 기록했는가
- Jenkins URL, HTTP/HTTPS, reverse proxy 경계를 정했는가
- build를 controller에서 돌릴지 agent에서 돌릴지 정했는가

Jenkins를 설치한 직후에는 바로 복잡한 Pipeline을 만들기보다 "controller가 유지되는가", "plugin 설치가 재현 가능한가", "관리자 계정과 URL이 임시값이 아닌가"를 먼저 확인하는 편이 안전하다.

## 운영으로 가져갈 때 주의할 점

로컬 Docker 실습 절차를 운영 설치로 그대로 승격하면 안 된다. 운영에서는 최소한 아래 항목을 별도 작업으로 검증해야 한다.

- TLS와 reverse proxy: Jenkins 자체 HTTP port를 외부에 그대로 노출하지 말고, 조직의 인증/프록시/TLS 경계와 맞춘다.
- backup/restore: `JENKINS_HOME` backup뿐 아니라 복구 리허설까지 확인한다.
- credential 관리: credential 값을 코드, 로그, job description에 남기지 않는다.
- controller와 agent 분리: build를 controller에서 직접 돌리는 구성을 기본값으로 두지 않는다.
- plugin 관리: 설치 이유, 버전, 업데이트 주기, 제거 기준을 기록한다.
- 권한 관리: 첫 관리자 계정으로 계속 운영하지 말고 role 또는 authorization strategy를 별도로 설계한다.
- 업그레이드 전 검증: Jenkins LTS, Java, plugin 호환성은 발행 이후에도 바뀔 수 있으므로 운영 반영 전 다시 확인한다.

## 한계와 예외

이 글은 작성자 실습 환경에서 Jenkins 설치 흐름을 확인했다. 다만 특정 Windows, Linux 배포판, Docker Desktop, WSL 환경에서의 오류는 환경별로 별도 확인이 필요하다.

Jenkins LTS와 Java 요구사항은 날짜에 민감하다. 이 글은 2026-04-24 확인본을 기준으로 하며 이후 LTS에서는 Java 요구사항이 바뀔 수 있다.

운영 환경에서는 TLS, reverse proxy, backup, restore, plugin pinning, controller/agent 분리, 계정 권한 정책을 별도 절차로 검증해야 한다.

## 함께 읽을 글

- [DevOps 운영 흐름](/devops/)
- [Jenkins는 무엇이고 왜 아직도 많이 쓰이는가](/devops/jenkins-what-and-why-still-used/)
- [PR/MR 기반 협업 흐름과 리뷰 기준](/devops/git-pr-mr-collaboration-review/)
- [Docker registry push와 image 관리](/devops/docker-registry-push-and-image-management/)

## 참고자료

- Jenkins User Handbook, [Installing Jenkins](https://www.jenkins.io/doc/book/installing/)
- Jenkins User Handbook, [Installing Jenkins - Docker](https://www.jenkins.io/doc/book/installing/docker/)
- Jenkins User Handbook, [Initial Settings](https://www.jenkins.io/doc/book/installing/initial-settings/)
- Jenkins, [LTS Changelog](https://www.jenkins.io/changelog-stable/)
- Jenkins User Handbook, [Java Support Policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/)
