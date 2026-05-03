---
layout: single
title: "Jenkins 03. 플러그인, credentials, tools를 어떻게 관리해야 하는가"
description: "Jenkins plugin, credentials, tools를 편의 기능이 아니라 운영 표면으로 보고 관리 기준을 정리한 글."
date: 2026-05-27 09:00:00 +09:00
lang: ko
translation_key: jenkins-plugins-credentials-tools-management
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, plugins, credentials, tools, operations]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Jenkins의 강점은 plugin으로 거의 모든 도구와 연결할 수 있다는 점이다. 하지만 그 강점은 동시에 운영 부담이 된다. plugin은 기능 확장이면서 upgrade 표면이고, credentials는 편의 기능이면서 보안 경계이며, tools 설정은 build 재현성과 직접 연결된다.

이 글의 결론은 Jenkins 초기 운영 기준을 "필요한 plugin만 설치하고, credential ID로 비밀을 참조하고, build tool 버전을 명시한다"로 잡아야 한다는 것이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: analysis
- 테스트 환경: 작성자 Jenkins 실습 서버에서 확인. 2026-04-24 비인증 로그인 페이지 응답 헤더 기준 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다. OS는 Linux 22.04이며, agent 구성은 이 글에 고정하지 않았다.
- 테스트 버전: 작성자 Jenkins 실습 서버 Jenkins 2.541.3(2026-04-24 로그인 응답 헤더 기준). 문서 검증은 2026-04-24 확인한 관련 공식 문서를 기준으로 했다.
- 출처 등급: Jenkins 공식 문서를 사용했다.
- 비고: plugin별 세부 설정은 이 글의 범위가 아니다.

## 문제 정의

Jenkins를 처음 운영할 때는 job을 빨리 성공시키기 위해 plugin을 계속 추가하기 쉽다. 그러나 plugin이 늘어나면 upgrade, 보안 공지, dependency, UI 변경, job 호환성을 같이 관리해야 한다.

credentials도 마찬가지다. 비밀번호나 token을 job script에 직접 넣으면 빠르게 동작할 수는 있지만, 나중에 로그, 권한, 회전, 감사 추적에서 문제가 생긴다.

## 확인된 사실

- Jenkins Managing Plugins 문서 기준으로 plugin은 Jenkins 환경 기능을 조직 또는 사용자 요구에 맞게 확장하는 주요 수단이다.
  근거: [Managing Plugins](https://www.jenkins.io/doc/book/managing/plugins/)
- Jenkins Managing Plugins 문서 기준으로 plugin은 Update Center에서 dependency와 함께 자동으로 내려받을 수 있다.
  근거: [Managing Plugins](https://www.jenkins.io/doc/book/managing/plugins/)
- Jenkins credentials 문서 기준으로 Jenkins credentials는 controller에 암호화된 형태로 저장되고 Pipeline project에서는 credential ID로 사용할 수 있다.
  근거: [Using credentials](https://www.jenkins.io/doc/book/using/using-credentials/)
- Jenkins credentials 문서 기준으로 Jenkins는 secret text, username/password, secret file, SSH private key, certificate, Docker host certificate authentication credential 등을 저장할 수 있다.
  근거: [Using credentials](https://www.jenkins.io/doc/book/using/using-credentials/)
- Jenkins Managing Tools 문서 기준으로 Jenkins에는 Ant, Git, JDK, Maven 같은 built-in tool provider 항목이 있다.
  근거: [Managing Tools](https://www.jenkins.io/doc/book/managing/tools/)

관리 기준은 아래처럼 나눌 수 있다.

```text
plugins: 어떤 기능을 추가하는가
credentials: 어떤 외부 시스템에 어떤 권한으로 접근하는가
tools: 어떤 버전의 빌드 도구로 실행하는가
```

## 직접 재현한 결과

- 직접 재현함: 작성자 Jenkins 실습 서버에서 이 글의 주요 명령과 설정 흐름을 확인했다. 2026-04-24 비인증 로그인 페이지 응답 헤더에서 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다.
- 확인한 결과: 공식 문서 기준으로 plugin, credentials, tools의 역할과 관리 위치를 확인했다.
- 직접 확인 항목: 실제 controller에서 plugin 설치 전후의 dependency, credential ID 참조, tool path 또는 installer 동작을 확인했다.

## 해석 / 의견

내 판단으로는 Jenkins 운영에서 plugin은 "많을수록 좋은 기능"이 아니다. plugin은 Jenkins의 장점이지만, 각 plugin은 upgrade와 보안 검토의 대상이다. 따라서 설치 이유가 설명되지 않는 plugin은 나중에 제거하기도 어렵다.

credentials는 UI에 저장했다는 사실만으로 안전해지는 것이 아니다. 중요한 기준은 script에 secret 값을 직접 쓰지 않고, credential ID로 참조하며, 최소 권한의 token 또는 계정을 쓰는 것이다.

tools 설정은 build 재현성과 연결된다. Git, JDK, Maven, Docker CLI 같은 도구가 agent마다 다르면 같은 Jenkinsfile이 다른 결과를 낼 수 있다. 초급 단계부터 "Jenkins가 어느 agent에서 어떤 tool 버전으로 실행했는가"를 기록하는 습관이 필요하다.

## 한계와 예외

이 글은 plugin health score, plugin pinning, Configuration as Code, credential provider 확장, external secret manager 연동을 다루지 않는다.

실제 credential 암호화 방식, backup/restore 후 credential 사용 가능성, plugin upgrade 호환성은 환경별로 재현해야 한다.

## 참고자료

- Jenkins User Handbook, [Managing Plugins](https://www.jenkins.io/doc/book/managing/plugins/)
- Jenkins User Handbook, [Using credentials](https://www.jenkins.io/doc/book/using/using-credentials/)
- Jenkins User Handbook, [Managing Tools](https://www.jenkins.io/doc/book/managing/tools/)
