---
layout: single
title: "Jenkins 04. Freestyle Job과 Pipeline은 무엇이 다른가"
description: "Jenkins Freestyle Job과 Pipeline을 UI 설정과 코드 기반 자동화라는 관점에서 비교한 글."
date: 2026-06-15 09:00:00 +0900
lang: ko
translation_key: jenkins-freestyle-job-vs-pipeline
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, freestyle, pipeline, job, jenkinsfile]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Jenkins에서 job은 일을 실행하는 단위다. Freestyle Job은 UI에서 빠르게 build step을 조립하기 쉽고, Pipeline은 Jenkinsfile로 절차를 코드처럼 남기기 좋다.

이 글의 결론은 초급 실습에서는 Freestyle Job으로 Jenkins의 실행 감각을 잡을 수 있지만, 팀 협업과 PR/MR 검증으로 넘어가면 Pipeline과 Jenkinsfile을 기준으로 삼아야 한다는 것이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: comparison
- 테스트 환경: 작성자 Jenkins 실습 서버에서 확인. 2026-04-24 비인증 로그인 페이지 응답 헤더 기준 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다. OS는 Linux 22.04이며, agent 구성은 이 글에 고정하지 않았다.
- 테스트 버전: 작성자 Jenkins 실습 서버 Jenkins 2.541.3(2026-04-24 로그인 응답 헤더 기준). 문서 검증은 2026-04-24 확인한 관련 공식 문서를 기준으로 했다.
- 출처 등급: Jenkins 공식 문서를 사용했다.
- 비고: Blue Ocean UI 세부 동작은 다루지 않는다.

## 문제 정의

Jenkins를 처음 배우면 Freestyle Job으로도 build, test, deploy step을 만들 수 있다. 그래서 "왜 Jenkinsfile까지 배워야 하는가"라는 질문이 생긴다.

핵심 차이는 자동화 절차가 UI 안에 머무르는가, 아니면 source repository에서 review 가능한 파일로 관리되는가이다.

## 확인된 사실

- Jenkins Working with projects 문서 기준으로 Jenkins는 일을 수행하기 위해 project 또는 job을 사용한다.
  근거: [Working with projects](https://www.jenkins.io/doc/book/using/working-with-projects/)
- 같은 문서 기준으로 Jenkins project 유형에는 Pipeline, Multibranch Pipeline, Organization folders, Freestyle 등이 포함된다.
  근거: [Working with projects](https://www.jenkins.io/doc/book/using/working-with-projects/)
- Jenkins Pipeline 문서 기준으로 Pipeline은 continuous delivery pipeline을 Jenkins 안에 구현하고 통합하기 위한 plugin 묶음이다.
  근거: [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- Jenkins Pipeline 문서 기준으로 Pipeline 정의는 `Jenkinsfile`로 작성해 source control repository에 commit할 수 있으며, source control에 두는 것이 일반적인 best practice로 설명된다.
  근거: [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- Jenkins Getting started with Pipeline 문서 기준으로 Pipeline은 Blue Ocean, classic UI, SCM 방식으로 정의할 수 있지만, `Jenkinsfile`을 source control에 두는 방식이 권장된다.
  근거: [Getting started with Pipeline](https://www.jenkins.io/doc/book/pipeline/getting-started/)

비교 기준은 아래처럼 정리할 수 있다.

```text
Freestyle Job: UI 중심, 빠른 실습, 단순 명령 실행에 편함
Pipeline: Jenkinsfile 중심, review 가능, branch/PR 흐름과 연결하기 좋음
Multibranch Pipeline: branch와 PR/MR 단위 자동 검증에 적합
```

## 직접 재현한 결과

- 직접 재현함: 작성자 Jenkins 실습 서버에서 이 글의 주요 명령과 설정 흐름을 확인했다. 2026-04-24 비인증 로그인 페이지 응답 헤더에서 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다.
- 확인한 결과: 공식 문서 기준으로 job 유형과 Pipeline/Jenkinsfile의 관리 방식을 확인했다.
- 직접 확인 항목: 같은 shell command를 Freestyle Job과 Pipeline에서 각각 실행하고, 설정 변경 이력이 어디에 남는지 비교했다.

## 해석 / 의견

내 판단으로는 Freestyle Job은 Jenkins의 기본 감각을 익히는 데 좋다. "Jenkins가 agent에서 명령을 실행하고 결과를 기록한다"는 구조를 빠르게 볼 수 있기 때문이다.

하지만 팀 작업에서는 Pipeline이 더 적합하다. Jenkinsfile이 저장소에 있으면 Git 글에서 배운 branch, diff, PR/MR review 흐름에 CI/CD 절차도 포함된다. 즉 application code와 automation code를 같은 review 흐름에 넣을 수 있다.

Freestyle Job이 나쁜 것은 아니다. 오래된 job, 단순 운영 task, 임시 점검 job에는 여전히 쓸 수 있다. 다만 새 프로젝트의 기본값은 Pipeline으로 두는 편이 이후 Docker build, registry push, Kubernetes deploy까지 연결하기 쉽다.

## 한계와 예외

이 글은 Freestyle Job과 Pipeline의 모든 plugin 호환성을 비교하지 않는다. 어떤 plugin은 Freestyle에서 더 익숙하게 쓰일 수 있고, 어떤 plugin은 Pipeline step을 제공한다.

작성자 실습 환경에서 기본 UI 흐름은 확인했다. 다만 실제 화면 구성, 저장 파일 차이, job copy/rename/move 동작은 Jenkins 버전과 plugin 구성에 따라 달라질 수 있다.

## 참고자료

- Jenkins User Handbook, [Working with projects](https://www.jenkins.io/doc/book/using/working-with-projects/)
- Jenkins User Handbook, [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- Jenkins User Handbook, [Getting started with Pipeline](https://www.jenkins.io/doc/book/pipeline/getting-started/)
