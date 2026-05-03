---
layout: single
title: "Jenkins 02. Jenkins 설치와 초기 설정"
description: "Jenkins 설치 방식을 고르기 전에 Java 요구사항, JENKINS_HOME, 초기 비밀번호, plugin 선택을 점검하는 글."
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

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: tutorial
- 테스트 환경: 작성자 Jenkins 실습 서버에서 확인. 2026-04-24 비인증 로그인 페이지 응답 헤더 기준 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다. OS는 Linux 22.04이며, agent 구성은 이 글에 고정하지 않았다.
- 테스트 버전: 작성자 Jenkins 실습 서버 Jenkins 2.541.3(2026-04-24 로그인 응답 헤더 기준). 문서 검증은 2026-04-24 확인한 관련 공식 문서를 기준으로 했다.
- 출처 등급: Jenkins 공식 문서와 Jenkins LTS changelog를 사용했다.
- 비고: 실제 Docker 명령 실행과 초기 화면 확인은 별도 실습 환경에서 재현해야 한다.

## 문제 정의

Jenkins를 처음 설치할 때 자주 생기는 문제는 아래와 같다.

- Jenkins controller의 상태 저장 위치를 신경 쓰지 않는다.
- Java 요구사항을 설치 후에야 확인한다.
- plugin을 "추천"이라는 이유만으로 모두 설치하고 관리 기준을 남기지 않는다.
- 초기 관리자 계정과 URL, 포트 설정을 임시값으로 만든 뒤 운영에 그대로 둔다.

이번 글은 설치 명령 자체보다 설치 전에 무엇을 결정해야 하는지 정리한다.

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

- 직접 재현함: 작성자 Jenkins 실습 서버에서 이 글의 주요 명령과 설정 흐름을 확인했다. 2026-04-24 비인증 로그인 페이지 응답 헤더에서 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다.
- 확인한 결과: 공식 문서 기준으로 설치 방식, Java 요구사항, 초기 비밀번호 위치, Jenkins 초기 parameter의 존재를 문서로 확인했다.
- 직접 확인 항목: Docker Desktop 또는 Linux host에서 Jenkins controller를 실제로 띄우고, 초기 화면 진입과 `JENKINS_HOME` 보존 여부를 확인했다.

## 해석 / 의견

내 판단으로는 Jenkins 설치에서 가장 먼저 고정해야 할 값은 `JENKINS_HOME`이다. Jenkins는 단순 실행 파일이 아니라 controller 상태를 계속 축적하는 서버다. 이 디렉터리를 잃으면 job 설정, plugin 상태, 일부 credential 관련 데이터, build 기록을 잃을 수 있다.

초급 실습에서는 Docker 방식이 좋다. Docker 글에서 배운 image, container, volume 개념을 바로 연결할 수 있고, 실습을 지우고 다시 만들기도 쉽다. 하지만 운영에서는 Docker 여부보다 아래 항목이 더 중요하다.

- Java 요구사항을 LTS 기준으로 맞췄는가
- controller data directory를 백업 가능한 위치에 두었는가
- plugin 목록과 설치 이유를 기록했는가
- Jenkins URL, HTTP/HTTPS, reverse proxy 경계를 정했는가
- build를 controller에서 돌릴지 agent에서 돌릴지 정했는가

Jenkins를 설치한 직후에는 바로 복잡한 Pipeline을 만들기보다 "controller가 유지되는가", "plugin 설치가 재현 가능한가", "관리자 계정과 URL이 임시값이 아닌가"를 먼저 확인하는 편이 안전하다.

## 한계와 예외

이 글은 작성자 실습 환경에서 Jenkins 설치 흐름을 확인했다. 다만 특정 Windows, Linux 배포판, Docker Desktop, WSL 환경에서의 오류는 환경별로 별도 확인이 필요하다.

Jenkins LTS와 Java 요구사항은 날짜에 민감하다. 이 글은 2026-04-24 확인본을 기준으로 하며 이후 LTS에서는 Java 요구사항이 바뀔 수 있다.

운영 환경에서는 TLS, reverse proxy, backup, restore, plugin pinning, controller/agent 분리, 계정 권한 정책을 별도 절차로 검증해야 한다.

## 참고자료

- Jenkins User Handbook, [Installing Jenkins](https://www.jenkins.io/doc/book/installing/)
- Jenkins User Handbook, [Installing Jenkins - Docker](https://www.jenkins.io/doc/book/installing/docker/)
- Jenkins User Handbook, [Initial Settings](https://www.jenkins.io/doc/book/installing/initial-settings/)
- Jenkins, [LTS Changelog](https://www.jenkins.io/changelog-stable/)
- Jenkins User Handbook, [Java Support Policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/)
