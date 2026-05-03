---
layout: single
title: "Jenkins 01. Jenkins는 무엇이고 왜 아직도 많이 쓰이는가"
description: "Jenkins를 Git, Docker 이후의 CI/CD 자동화 도구로 이해하고 controller, agent, plugin, Pipeline의 역할을 정리한 글."
date: 2026-05-25 09:00:00 +09:00
lang: ko
translation_key: jenkins-what-and-why-still-used
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, ci, cd, automation, pipeline]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Git 글에서는 변경 이력, branch, tag, PR/MR을 다뤘고 Docker 글에서는 image와 registry를 다뤘다. Jenkins는 이 둘 사이를 자동화해서 "코드를 가져오고, 빌드하고, 테스트하고, 산출물을 남기는 흐름"을 반복 가능하게 만드는 도구로 이해하면 쉽다.

이 글의 결론은 Jenkins를 단순한 "배포 버튼"이 아니라 self-hosted 자동화 서버로 봐야 한다는 것이다. Jenkins가 여전히 선택되는 이유는 가장 새롭기 때문이 아니라, plugin, agent, Pipeline, Jenkinsfile을 조합해 조직 내부 환경에 맞는 CI/CD 흐름을 만들 수 있기 때문이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: analysis
- 테스트 환경: 작성자 Jenkins 실습 서버에서 확인. 2026-04-24 비인증 로그인 페이지 응답 헤더 기준 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다. OS는 Linux 22.04이며, agent 구성은 이 글에 고정하지 않았다.
- 테스트 버전: 작성자 Jenkins 실습 서버 Jenkins 2.541.3(2026-04-24 로그인 응답 헤더 기준). 문서 검증은 2026-04-24 확인한 관련 공식 문서를 기준으로 했다.
- 출처 등급: Jenkins 공식 문서, Jenkins LTS changelog, Jenkins Java Support Policy를 사용했다.
- 비고: 이 글은 Jenkins와 GitHub Actions, GitLab CI, Tekton의 장단점 비교가 아니라 Jenkins 입문 전 개념 정리에 집중한다.

## 문제 정의

Git을 배운 뒤에는 "변경을 어디에서 자동으로 검사할 것인가"라는 질문이 생긴다. PR/MR에서 사람이 diff를 보고 리뷰할 수는 있지만, 빌드, 테스트, 이미지 생성, registry push 같은 반복 작업을 매번 사람이 손으로 실행하기는 어렵다.

Jenkins를 처음 볼 때 흔한 오해는 아래와 같다.

- Jenkins를 Git 대신 쓰는 도구라고 생각한다.
- Jenkins를 단순히 배포 버튼이 있는 웹 화면으로만 본다.
- plugin을 많이 설치할수록 좋은 Jenkins라고 생각한다.
- Pipeline을 UI에 직접 넣어도 충분하다고 생각한다.
- controller와 agent를 구분하지 않고 한 서버에서 모든 빌드를 실행한다.

이번 글은 Jenkins가 어떤 문제를 해결하는지, 그리고 왜 Git과 Docker 다음에 배워야 하는지를 정리한다. 설치, 초기 비밀번호, plugin 선택, 첫 job 생성은 다음 글의 범위로 남긴다.

## 확인된 사실

- Jenkins 공식 사용자 문서 기준으로 Jenkins는 build, test, delivery, deploy와 관련된 작업을 자동화하는 self-contained open source automation server다.
  근거: [Jenkins User Documentation - What is Jenkins?](https://www.jenkins.io/doc/)
- Jenkins 공식 사이트 기준으로 Jenkins는 simple CI server로 쓸 수도 있고, project의 continuous delivery hub로 확장할 수도 있다.
  근거: [Jenkins](https://www.jenkins.io/)
- Jenkins 공식 사이트 기준으로 Jenkins는 plugin architecture로 확장되며, Update Center에는 다양한 build tool, cloud provider, analysis tool과 통합하기 위한 plugin이 있다.
  근거: [Jenkins](https://www.jenkins.io/), [Managing Plugins](https://www.jenkins.io/doc/book/managing/plugins/)
- Jenkins Pipeline 공식 문서 기준으로 Pipeline은 continuous delivery pipeline을 Jenkins 안에 구현하고 통합하기 위한 plugin 묶음이다. Pipeline 정의는 `Jenkinsfile`이라는 텍스트 파일로 작성해 source control repository에 commit할 수 있다.
  근거: [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- Jenkins Pipeline 공식 문서 기준으로 `Jenkinsfile`을 source control에 두면 branch와 pull request에 대한 Pipeline build process, Pipeline code review, audit trail, single source of truth 같은 이점을 얻을 수 있다.
  근거: [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- Jenkins agents 공식 문서 기준으로 Jenkins controller는 agent를 관리하고 job scheduling과 monitoring을 조율한다. Agent는 controller가 요청한 일을 수행하는 executor를 제공하며 Pipeline step, freestyle job 등을 실행할 수 있다.
  근거: [Using Jenkins agents](https://www.jenkins.io/doc/book/using/using-agents/)
- Jenkins controller isolation 문서 기준으로 장기 운영에서는 built-in node에서 build를 실행하지 않고 agent에서 실행하는 것이 권장된다. Built-in node에서 실행되는 build는 Jenkins process와 같은 수준으로 controller filesystem에 접근할 수 있기 때문이다.
  근거: [Controller Isolation](https://www.jenkins.io/doc/book/security/controller-isolation/)
- Jenkins credentials 공식 문서 기준으로 Jenkins credentials는 controller에 암호화된 형태로 저장되고 Pipeline에서는 credential ID를 통해 다룰 수 있다.
  근거: [Using credentials](https://www.jenkins.io/doc/book/using/using-credentials/)
- Jenkins LTS changelog와 Java Support Policy 기준으로 2026-04-24에 확인한 Jenkins LTS 2.555.1은 Java 21 또는 Java 25가 필요하며 Java 17은 지원하지 않는다.
  근거: [LTS Changelog](https://www.jenkins.io/changelog-stable/), [Java Support Policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/)
- 직접 확인한 작성자 Jenkins 실습 서버는 2026-04-24 로그인 응답 헤더 기준 Jenkins 2.541.3이다. Java 요구사항은 LTS 버전별로 달라질 수 있으므로, 위 Java 요구사항은 2.555.1 기준으로 읽어야 한다.
  근거: 작성자 Jenkins 실습 서버 로그인 응답 헤더 확인

Git과 Docker 이후 Jenkins 흐름은 아래처럼 볼 수 있다.

```text
Git push or PR/MR
Jenkins job or multibranch Pipeline
checkout source
build and test
create artifact or Docker image
publish result or push image
```

여기서 Jenkins는 source history 자체가 아니고, Docker image 자체도 아니다. Jenkins는 Git에서 source를 가져와 정해진 절차를 실행하고, 그 결과를 사람이 확인할 수 있게 남기는 자동화 실행 지점이다.

## 직접 재현한 결과

- 직접 재현함: 작성자 Jenkins 실습 서버에서 이 글의 주요 명령과 설정 흐름을 확인했다. 2026-04-24 비인증 로그인 페이지 응답 헤더에서 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다.
- 문서 확인 결과: 2026-04-24 기준 Jenkins 공식 문서에서 automation server, plugin, Pipeline, Jenkinsfile, controller/agent, credentials, Java 요구사항을 확인했다.
- 후속 재현 계획: Jenkins 02에서 Docker 또는 로컬 설치 방식으로 Jenkins를 실행하고, 초기 설정과 기본 점검 결과를 별도로 기록한다.

## 해석 / 의견

내 판단으로는 Jenkins를 배울 때 가장 중요한 관점은 "자동화의 실행 위치"다. Git은 변경 이력과 협업 흐름을 제공하고, Docker는 실행 가능한 image와 registry 흐름을 제공한다. Jenkins는 이 재료를 가져와 정해진 순서로 실행한다.

Jenkins가 여전히 선택되는 이유는 아래 조건에서 설명하기 쉽다.

- 내부망, 사내 Git, 사내 registry, 사내 artifact repository처럼 외부 SaaS에 바로 붙이기 어려운 환경이 있다.
- build agent를 Linux, Windows, Docker, 고사양 장비, 특수 tool이 설치된 장비처럼 나눠야 한다.
- CI/CD 흐름을 Jenkinsfile로 저장소에 넣고 code review 대상으로 삼고 싶다.
- plugin이나 shell step을 통해 오래된 배포 스크립트와 새 Pipeline을 점진적으로 연결해야 한다.

다만 이 장점은 운영 부담과 같이 온다. plugin을 무분별하게 늘리거나 credential 관리 기준이 없거나 controller에서 모든 build를 돌리면 Jenkins는 빠르게 불투명해진다. 초급 단계부터 controller, agent, credential, plugin, Jenkinsfile의 책임을 나눠 이해해야 한다.

이 연재에서 Jenkins는 아래 순서로 다루는 편이 자연스럽다.

```text
설치와 초기 설정
plugin, credentials, tools 관리
Freestyle Job과 Pipeline 차이
Declarative Pipeline
Jenkinsfile 기본 문법
Docker image build와 registry push
운영 장애 원인 분리
Kubernetes 배포로 연결할 때의 경계
```

이 순서를 따르면 Git에서 배운 branch, PR/MR, tag가 Jenkins Pipeline의 trigger와 검증 기준으로 연결되고, Docker에서 배운 image tag와 digest가 Jenkins build 산출물 기록으로 연결된다.

## 한계와 예외

이 글의 "왜 아직도 많이 쓰이는가"는 사용량 통계나 시장 점유율 조사에 근거한 결론이 아니다. 공식 문서에서 확인한 Jenkins의 기능적 특성과 일반적인 self-hosted CI/CD 운영 맥락을 바탕으로 한 해석이다.

이 글은 Jenkins 기본 개념 정리에 집중하므로 UI, plugin 설치 화면, 초기 비밀번호 위치, 실제 Pipeline 실행 결과의 세부 절차는 Jenkins 02 이후 글에서 더 자세히 다룬다.

Jenkins LTS와 Java 요구사항은 버전과 날짜에 민감하다. 이 글은 2026-04-24 확인본을 기준으로 하며, 이후 LTS나 weekly release에서는 요구사항이 달라질 수 있다.

GitHub 저장소만 쓰고 GitHub-hosted runner로 충분한 팀, GitLab 안에서 issue, MR, registry, runner를 모두 쓰는 팀, Kubernetes-native pipeline을 우선하는 팀에는 Jenkins가 가장 단순한 선택이 아닐 수 있다.

## 참고자료

- Jenkins, [Jenkins User Documentation](https://www.jenkins.io/doc/)
- Jenkins, [Jenkins](https://www.jenkins.io/)
- Jenkins User Handbook, [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- Jenkins User Handbook, [Managing Plugins](https://www.jenkins.io/doc/book/managing/plugins/)
- Jenkins User Handbook, [Using Jenkins agents](https://www.jenkins.io/doc/book/using/using-agents/)
- Jenkins User Handbook, [Controller Isolation](https://www.jenkins.io/doc/book/security/controller-isolation/)
- Jenkins User Handbook, [Using credentials](https://www.jenkins.io/doc/book/using/using-credentials/)
- Jenkins, [LTS Changelog](https://www.jenkins.io/changelog-stable/)
- Jenkins User Handbook, [Java Support Policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/)
