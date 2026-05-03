---
layout: single
title: "Jenkins 06. Jenkinsfile 기본 문법 agent, stages, steps, post"
description: "Jenkinsfile의 핵심 블록인 agent, stages, steps, post를 초급자 관점에서 정리한 글."
date: 2026-05-30 09:00:00 +09:00
lang: ko
translation_key: jenkinsfile-agent-stages-steps-post
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, jenkinsfile, agent, stages, post]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Jenkinsfile을 읽을 때 가장 먼저 볼 블록은 `agent`, `stages`, `steps`, `post`다. `agent`는 어디서 실행할지, `stages`는 일을 어떤 단계로 나눌지, `steps`는 각 단계에서 무엇을 할지, `post`는 끝난 뒤 어떤 후처리를 할지 정한다.

이 글의 결론은 Jenkinsfile을 처음부터 Groovy 코드처럼 보지 말고 실행 계획표로 읽어야 한다는 것이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: tutorial
- 테스트 환경: 작성자 Jenkins 실습 서버에서 확인. 2026-04-24 비인증 로그인 페이지 응답 헤더 기준 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다. OS는 Linux 22.04이며, agent 구성은 이 글에 고정하지 않았다.
- 테스트 버전: 작성자 Jenkins 실습 서버 Jenkins 2.541.3(2026-04-24 로그인 응답 헤더 기준). 문서 검증은 2026-04-24 확인한 관련 공식 문서를 기준으로 했다.
- 출처 등급: Jenkins 공식 문서를 사용했다.
- 비고: `options`, `tools`, `input`, `parallel`, `matrix`는 이 글의 중심 범위에서 제외한다.

## 문제 정의

Jenkinsfile은 처음 보면 중괄호가 많아서 어렵게 느껴진다. 하지만 초급 단계에서는 모든 문법을 외울 필요가 없다. 먼저 실행 위치, 단계, 단계 내부 명령, 후처리를 구분하면 된다.

## 확인된 사실

- Jenkins Pipeline Syntax 문서 기준으로 `agent` section은 전체 Pipeline 또는 특정 stage가 Jenkins 환경의 어디에서 실행될지 지정한다.
  근거: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- 같은 문서 기준으로 `stages` section은 하나 이상의 `stage` directive를 포함하며, Pipeline 작업의 대부분이 이 안에 위치한다.
  근거: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- 같은 문서 기준으로 `steps` section은 특정 `stage`에서 실행할 하나 이상의 step을 정의한다.
  근거: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- 같은 문서 기준으로 `post` section은 Pipeline 또는 stage 완료 후 실행할 추가 step을 정의하며 `always`, `success`, `failure`, `cleanup` 같은 조건 block을 지원한다.
  근거: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)

기본 구조는 아래처럼 읽을 수 있다.

```groovy
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'make'
      }
    }
    stage('Test') {
      steps {
        sh 'make test'
      }
    }
  }
  post {
    always {
      echo 'finished'
    }
  }
}
```

## 직접 재현한 결과

- 직접 재현함: 작성자 Jenkins 실습 서버에서 이 글의 주요 명령과 설정 흐름을 확인했다. 2026-04-24 비인증 로그인 페이지 응답 헤더에서 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다.
- 확인한 결과: 공식 문서 기준으로 네 블록의 역할과 위치를 확인했다.
- 직접 확인 항목: Linux agent에서는 `sh`, Windows agent에서는 `bat` 또는 `powershell` step을 사용해 같은 구조를 실행했다.

## 해석 / 의견

내 판단으로는 `agent`를 대충 `any`로 두는 습관을 빨리 벗어나는 것이 좋다. Docker build가 필요한 job, Windows build가 필요한 job, 배포 credential이 있는 job은 같은 agent에서 돌면 안 될 수 있다.

`stages`는 사람이 읽는 운영 단위다. Build, Test, Package, Push, Deploy처럼 실패 원인을 분리할 수 있는 이름을 붙이는 편이 좋다.

`post`는 실패했을 때 더 중요하다. 알림, log 정리, 임시 file 정리, test report 수집 같은 작업은 성공 여부와 관계없이 남겨야 할 수 있다.

## 한계와 예외

이 글은 Jenkinsfile 문법의 일부만 다룬다. 실제 운영 Pipeline은 `options`, `environment`, `parameters`, `when`, `tools`, `parallel`을 함께 사용할 수 있다.

Jenkins agent 운영체제에 따라 `sh`, `bat`, `powershell`, `pwsh` step 선택이 달라질 수 있다.

## 참고자료

- Jenkins User Handbook, [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- Jenkins User Handbook, [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
