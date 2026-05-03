---
layout: single
title: "Jenkins 05. Declarative Pipeline 입문"
description: "Jenkins Declarative Pipeline을 Scripted Pipeline과 구분하고 초급자가 먼저 익혀야 할 이유를 설명한 글."
date: 2026-05-29 09:00:00 +09:00
lang: ko
translation_key: jenkins-declarative-pipeline-introduction
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, declarative-pipeline, scripted-pipeline, ci]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Jenkins Pipeline에는 Declarative와 Scripted 두 문법이 있다. 초급자는 먼저 Declarative Pipeline으로 `pipeline`, `agent`, `stages`, `steps` 구조를 익히는 편이 좋다.

이 글의 결론은 Declarative Pipeline이 Jenkinsfile의 기본 골격을 읽기 쉽게 만들고, 이후 Docker build나 배포 분기까지 확장하기 좋은 출발점이라는 것이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: tutorial
- 테스트 환경: 작성자 Jenkins 실습 서버에서 확인. 2026-04-24 비인증 로그인 페이지 응답 헤더 기준 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다. OS는 Linux 22.04이며, agent 구성은 이 글에 고정하지 않았다.
- 테스트 버전: 작성자 Jenkins 실습 서버 Jenkins 2.541.3(2026-04-24 로그인 응답 헤더 기준). 문서 검증은 2026-04-24 확인한 관련 공식 문서를 기준으로 했다.
- 출처 등급: Jenkins 공식 문서를 사용했다.
- 비고: Scripted Pipeline의 Groovy 고급 문법은 다루지 않는다.

## 문제 정의

Pipeline을 처음 보면 Groovy, Jenkinsfile, Declarative, Scripted, stage, step 같은 단어가 한꺼번에 나온다. 이때 모든 문법을 동시에 배우면 Jenkins가 실제로 무엇을 실행하는지 흐려진다.

이번 글은 초급자가 먼저 Declarative Pipeline으로 build, test, deploy 단계를 읽는 데 집중한다.

## 확인된 사실

- Jenkins Pipeline 문서 기준으로 Pipeline은 continuous delivery pipeline을 Jenkins에 구현하고 통합하기 위한 plugin 묶음이다.
  근거: [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- Jenkins Pipeline 문서 기준으로 `Jenkinsfile`은 source control repository에 commit할 수 있는 Pipeline 정의 파일이다.
  근거: [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- Jenkins Pipeline 문서 기준으로 Jenkinsfile은 Declarative 또는 Scripted 문법으로 작성할 수 있다.
  근거: [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- Jenkins Pipeline 문서 기준으로 Declarative Pipeline은 Pipeline code를 쓰고 읽기 쉽게 만들도록 설계되었다.
  근거: [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- Jenkins Pipeline Syntax 문서 기준으로 모든 유효한 Declarative Pipeline은 `pipeline` block 안에 들어가야 한다.
  근거: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)

가장 작은 Declarative Pipeline 골격은 아래처럼 볼 수 있다.

```groovy
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'build'
      }
    }
  }
}
```

## 직접 재현한 결과

- 직접 재현함: 작성자 Jenkins 실습 서버에서 이 글의 주요 명령과 설정 흐름을 확인했다. 2026-04-24 비인증 로그인 페이지 응답 헤더에서 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다.
- 확인한 결과: 공식 문서 기준으로 Declarative Pipeline의 기본 구조와 Scripted Pipeline과의 구분을 확인했다.
- 직접 확인 항목: 실제 Jenkins Pipeline job에서 `echo` 단계가 성공하는지 확인했다.

## 해석 / 의견

내 판단으로는 Declarative Pipeline은 초급자에게 "Jenkins가 일을 나눠 실행하는 방식"을 가장 잘 보여준다. `stage` 이름이 UI와 로그에서 기준점이 되기 때문에 build, test, deploy 실패 지점을 분리하기 쉽다.

Scripted Pipeline은 더 유연하지만 초반에는 자유도가 오히려 부담이 될 수 있다. 먼저 Declarative로 공통 구조를 익힌 뒤, 반복과 복잡한 조건이 정말 필요할 때 Scripted 문법이나 shared library를 검토하는 편이 낫다.

좋은 첫 Jenkinsfile은 화려한 자동화가 아니라 아래 세 가지를 보여주면 충분하다.

- 어떤 agent에서 실행되는가
- 어떤 stage 순서로 진행되는가
- 어떤 step이 실패하면 어디에서 멈추는가

## 한계와 예외

작성자 실습 환경에서 Pipeline 실행 흐름을 확인했다. Jenkins UI의 stage 표시, console output, 실패 상태의 세부 화면은 Jenkins 버전과 plugin 구성에 따라 달라질 수 있다.

Declarative Pipeline만으로 모든 복잡한 배포 흐름을 표현해야 한다는 뜻은 아니다. 복잡한 로직은 Scripted block, shared library, 외부 script로 분리하는 편이 나을 수 있다.

## 참고자료

- Jenkins User Handbook, [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- Jenkins User Handbook, [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- Jenkins User Handbook, [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
