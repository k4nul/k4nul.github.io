---
layout: single
title: "Jenkins 07. Jenkinsfile 실전 environment, parameters, when"
description: "Jenkinsfile에서 환경 변수, 사용자 입력값, 조건부 stage 실행을 다루는 기본 기준을 정리한 글."
date: 2026-06-21 09:00:00 +0900
lang: ko
translation_key: jenkinsfile-environment-parameters-when
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, jenkinsfile, environment, parameters, when]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

기본 Pipeline 구조를 익혔다면 다음은 값을 어떻게 넣고, 어떤 조건에서 stage를 건너뛸지 정해야 한다. Declarative Pipeline에서는 `environment`, `parameters`, `when`이 이 역할을 맡는다.

이 글의 결론은 배포 환경, debug 여부, branch 조건처럼 바뀌는 값은 Jenkinsfile 안에 고정하지 말고 명시적인 변수와 조건으로 드러내야 한다는 것이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: tutorial
- 테스트 환경: 작성자 Jenkins 실습 서버에서 확인. 2026-04-24 비인증 로그인 페이지 응답 헤더 기준 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다. OS는 Linux 22.04이며, agent 구성은 이 글에 고정하지 않았다.
- 테스트 버전: 작성자 Jenkins 실습 서버 Jenkins 2.541.3(2026-04-24 로그인 응답 헤더 기준). 문서 검증은 2026-04-24 확인한 관련 공식 문서를 기준으로 했다.
- 출처 등급: Jenkins 공식 문서를 사용했다.
- 비고: credential binding의 보안 세부사항은 별도 보안 글에서 더 다뤄야 한다.

## 문제 정의

Pipeline이 단순할 때는 Build, Test만 있으면 된다. 하지만 실무에 가까워질수록 아래 질문이 생긴다.

- staging과 production을 어떻게 구분할 것인가
- 수동 실행 때 어떤 값을 입력받을 것인가
- 특정 branch나 tag에서만 deploy할 것인가
- 불필요한 agent 할당을 피할 수 있는가

## 확인된 사실

- Jenkins Pipeline Syntax 문서 기준으로 `environment` directive는 Pipeline 전체 또는 stage 내부 step에 적용될 key-value 환경 변수를 정의한다.
  근거: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- 같은 문서 기준으로 `environment` directive는 Jenkins 환경에 미리 정의된 credential을 identifier로 접근하기 위한 `credentials()` helper를 지원한다.
  근거: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- 같은 문서 기준으로 `parameters` directive는 Pipeline trigger 시 사용자가 제공할 parameter 목록을 정의하고, 값은 `params` object와 환경 변수로 사용할 수 있다.
  근거: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- 같은 문서 기준으로 `when` directive는 조건에 따라 stage를 실행할지 결정한다.
  근거: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- 같은 문서 기준으로 `beforeAgent true`를 사용하면 stage agent에 들어가기 전에 `when` 조건을 먼저 평가할 수 있다.
  근거: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)

예시는 아래처럼 볼 수 있다.

```groovy
pipeline {
  agent any
  parameters {
    choice(name: 'DEPLOY_ENV', choices: ['staging', 'production'], description: '')
  }
  environment {
    IMAGE_NAME = 'registry.example.com/team/app'
  }
  stages {
    stage('Deploy') {
      when {
        branch 'main'
      }
      steps {
        echo "deploy to ${params.DEPLOY_ENV}"
      }
    }
  }
}
```

## 직접 재현한 결과

- 직접 재현함: 작성자 Jenkins 실습 서버에서 이 글의 주요 명령과 설정 흐름을 확인했다. 2026-04-24 비인증 로그인 페이지 응답 헤더에서 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다.
- 확인한 결과: 공식 문서 기준으로 `environment`, `parameters`, `when`, `beforeAgent`의 역할을 확인했다.
- 직접 확인 항목: Multibranch Pipeline에서 branch 조건이 실제로 stage 실행을 제어하는지 확인했다.

## 해석 / 의견

내 판단으로는 `parameters`는 편리하지만 남용하면 Pipeline이 수동 배포 버튼으로 변한다. 자동 검증에 필요한 값과 사람이 승인해야 하는 값을 분리해야 한다.

`environment`에는 반복되는 이름과 외부 system 주소를 넣기 좋다. 다만 secret 값을 plain text로 넣는 것은 피하고 credential ID를 통해 참조해야 한다.

`when`은 비용 절감에도 영향을 준다. 배포 대상 branch가 아니라면 deploy agent를 잡지 않아도 된다. 특히 Docker build agent나 배포 agent가 제한된 환경에서는 조건 평가 위치도 중요하다.

## 한계와 예외

작성자 실습 환경에서 기본 조건 분기와 parameter 흐름을 확인했다. 실제 Multibranch Pipeline, credential binding, protected branch 정책은 저장소와 권한 모델에 따라 별도 확인이 필요하다.

`branch` 조건은 Multibranch Pipeline에서의 동작과 일반 Pipeline에서의 동작 조건이 다를 수 있다. 실제 job 유형에서 확인해야 한다.

## 참고자료

- Jenkins User Handbook, [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- Jenkins User Handbook, [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
