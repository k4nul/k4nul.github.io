---
layout: single
title: "Jenkins 09. Jenkins 운영에서 자주 만나는 장애와 원인 분리"
description: "Jenkins 장애를 controller, agent, queue, credential, plugin, Pipeline 코드 관점으로 나눠 보는 글."
date: 2026-06-25 09:00:00 +0900
lang: ko
translation_key: jenkins-common-failures-troubleshooting
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, troubleshooting, agents, pipeline, operations]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Jenkins 장애는 "빌드가 실패했다" 한 문장으로 묶으면 해결이 늦어진다. 먼저 queue에 머무는지, agent가 offline인지, credential이 실패했는지, plugin이나 Pipeline 문법 문제인지 분리해야 한다.

이 글의 결론은 Jenkins 장애 대응의 첫 단계가 재실행이 아니라 분류라는 것이다. 실패 위치를 controller, agent, workspace, registry, credential, Pipeline 코드 중 어디인지 좁혀야 한다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: analysis
- 테스트 환경: 작성자 Jenkins 실습 서버에서 확인. 2026-04-24 비인증 로그인 페이지 응답 헤더 기준 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다. OS는 Linux 22.04이며, agent 구성은 이 글에 고정하지 않았다.
- 테스트 버전: 작성자 Jenkins 실습 서버 Jenkins 2.541.3(2026-04-24 로그인 응답 헤더 기준). 문서 검증은 2026-04-24 확인한 관련 공식 문서를 기준으로 했다.
- 출처 등급: Jenkins 공식 문서를 사용했다.
- 비고: 특정 plugin 장애나 보안 취약점 대응 절차는 다루지 않는다.

## 문제 정의

Jenkins에서 자주 만나는 증상은 비슷해 보인다.

- job이 queue에 머문다.
- agent가 offline이다.
- Docker build가 agent에서만 실패한다.
- credential ID를 찾지 못한다.
- plugin upgrade 후 job이 깨진다.
- Pipeline이 느리거나 log가 지나치게 크다.

이 증상을 하나로 묶으면 원인을 찾기 어렵다.

## 확인된 사실

- Jenkins Executor Starvation 문서 기준으로 build queue의 clock icon은 job이 불필요하게 queue에 머무는 신호일 수 있으며, common symptom에는 agent offline, executor 부족, label에 해당하는 executor 부족이 포함된다.
  근거: [Executor Starvation](https://www.jenkins.io/doc/book/using/executor-starvation/)
- Jenkins Using Jenkins agents 문서 기준으로 agent는 controller 요청을 수행하는 executor를 제공하며, Pipeline step과 freestyle job 등을 실행할 수 있다.
  근거: [Using Jenkins agents](https://www.jenkins.io/doc/book/using/using-agents/)
- Jenkins Controller Isolation 문서 기준으로 build는 장기적으로 built-in node가 아니라 agent에서 실행하는 것이 권장된다.
  근거: [Controller Isolation](https://www.jenkins.io/doc/book/security/controller-isolation/)
- Jenkins Scaling Pipelines 문서 기준으로 Pipeline은 예기치 않은 restart나 crash에 대비하기 위해 transient data를 disk에 자주 기록하며, 이것이 병목이 될 수 있다.
  근거: [Scaling Pipelines](https://www.jenkins.io/doc/book/pipeline/scaling-pipeline/)
- Jenkins Securing Jenkins 문서 기준으로 Jenkins는 환경과 위협 모델에 따라 여러 보안 설정과 trade-off를 제공한다.
  근거: [Securing Jenkins](https://www.jenkins.io/doc/book/security/)

원인 분리 순서는 아래처럼 잡을 수 있다.

```text
queue 상태 확인
agent online 여부 확인
label과 executor 수 확인
workspace와 tool 버전 확인
credential ID와 권한 확인
registry 또는 외부 서비스 응답 확인
Pipeline 문법과 plugin 변경 확인
```

## 직접 재현한 결과

- 직접 재현함: 작성자 Jenkins 실습 서버에서 이 글의 주요 명령과 설정 흐름을 확인했다. 2026-04-24 비인증 로그인 페이지 응답 헤더에서 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다.
- 확인한 결과: 공식 문서 기준으로 queue, agent, controller isolation, Pipeline scaling 관련 원인 분리 기준을 확인했다.
- 직접 확인 항목: 작은 Jenkins 실습 환경에서 label mismatch, offline agent, 잘못된 credential ID를 각각 만들어 증상 차이를 기록했다.

## 해석 / 의견

내 판단으로는 Jenkins 장애에서 가장 흔한 실수는 console log만 보는 것이다. console log는 실행된 뒤의 정보다. 애초에 실행되지 않았다면 queue, executor, label, agent 상태를 먼저 봐야 한다.

Docker build 실패는 Dockerfile 문제일 수도 있지만 agent 문제일 수도 있다. 같은 Jenkinsfile이 어떤 agent에서는 성공하고 어떤 agent에서는 실패한다면 Docker daemon 접근, workspace mount, tool version, credential 범위를 먼저 봐야 한다.

plugin upgrade 후 장애는 "코드가 변하지 않았는데 실패한다"는 형태로 나타날 수 있다. 따라서 plugin 변경 이력과 Jenkins core upgrade 이력도 운영 기록에 남겨야 한다.

## 한계와 예외

작성자 실습 환경에서 대표 증상 흐름을 확인했지만, 이 글은 error message별 해결책 목록을 제공하지 않는다.

Jenkins 장애는 plugin, agent OS, network, registry, Git server, credential provider에 따라 증상이 크게 달라질 수 있다.

## 참고자료

- Jenkins User Handbook, [Executor Starvation](https://www.jenkins.io/doc/book/using/executor-starvation/)
- Jenkins User Handbook, [Using Jenkins agents](https://www.jenkins.io/doc/book/using/using-agents/)
- Jenkins User Handbook, [Controller Isolation](https://www.jenkins.io/doc/book/security/controller-isolation/)
- Jenkins User Handbook, [Scaling Pipelines](https://www.jenkins.io/doc/book/pipeline/scaling-pipeline/)
- Jenkins User Handbook, [Securing Jenkins](https://www.jenkins.io/doc/book/security/)
