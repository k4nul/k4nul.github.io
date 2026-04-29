---
layout: single
title: "Jenkins 08. Jenkins에서 Docker 이미지 빌드와 레지스트리 푸시"
description: "Jenkins Pipeline에서 Docker 이미지를 빌드하고 registry로 push할 때 tag, credential, agent 경계를 정리한 글."
date: 2026-06-23 09:00:00 +09:00
lang: ko
translation_key: jenkins-docker-image-build-registry-push
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, docker, registry, image, pipeline]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Docker 글에서 image, tag, digest, registry를 배웠다면 Jenkins에서는 이 흐름을 자동화한다. Jenkins Pipeline은 source를 checkout하고, Docker image를 build하고, registry credential로 로그인해 push하는 실행 지점이 된다.

이 글의 결론은 Jenkins가 image 이름과 tag를 마음대로 정하게 두지 말고 Git commit, Git tag, build number, registry repository 규칙을 명시해야 한다는 것이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: tutorial
- 테스트 환경: 작성자 Jenkins 실습 서버에서 확인. 2026-04-24 비인증 로그인 페이지 응답 헤더 기준 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다. OS는 Linux 22.04이며, agent 구성은 이 글에 고정하지 않았다.
- 테스트 버전: 작성자 Jenkins 실습 서버 Jenkins 2.541.3(2026-04-24 로그인 응답 헤더 기준). 문서 검증은 2026-04-24 확인한 관련 공식 문서를 기준으로 했다.
- 출처 등급: Jenkins 공식 문서와 Docker 공식 문서를 사용했다.
- 비고: image signing, SBOM, provenance는 이 글의 범위가 아니다.

## 문제 정의

CI에서 Docker image를 만들 때 흔한 문제는 아래와 같다.

- 모든 build가 `latest`로만 push된다.
- 어떤 Git commit에서 만든 image인지 남지 않는다.
- registry credential이 shell script에 직접 들어간다.
- Docker daemon이 없는 agent에서 Docker step을 실행한다.

이번 글은 Jenkins에서 Docker build/push를 연결할 때 최소한 무엇을 명시해야 하는지 정리한다.

## 확인된 사실

- Jenkins Using Docker with Pipeline 문서 기준으로 Docker와 Pipeline을 결합하면 stage마다 다른 container 실행 환경을 사용할 수 있다.
  근거: [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- 같은 문서 기준으로 Docker Pipeline plugin은 `docker.build()`를 통해 repository의 `Dockerfile`에서 새 image를 만들 수 있다.
  근거: [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- 같은 문서 기준으로 `push()` method를 통해 Docker image를 Docker Hub 또는 custom registry에 publish할 수 있다.
  근거: [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- 같은 문서 기준으로 custom registry와 인증이 필요할 때 `withRegistry()`와 Jenkins credential ID를 사용할 수 있다.
  근거: [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- Docker 공식 문서 기준으로 `docker image push`는 image를 registry로 업로드하고, push 결과에서 digest를 확인할 수 있다.
  근거: [docker image push](https://docs.docker.com/reference/cli/docker/image/push/)

기본 흐름은 아래처럼 볼 수 있다.

```groovy
node('docker') {
  checkout scm
  def image = docker.build("registry.example.com/team/app:${env.BUILD_NUMBER}")
  docker.withRegistry('https://registry.example.com', 'registry-credential-id') {
    image.push()
  }
}
```

## 직접 재현한 결과

- 직접 재현함: 작성자 Jenkins 실습 서버에서 이 글의 주요 명령과 설정 흐름을 확인했다. 2026-04-24 비인증 로그인 페이지 응답 헤더에서 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다.
- 확인한 결과: Jenkins와 Docker 공식 문서 기준으로 build, push, registry credential 연결 방식을 확인했다.
- 직접 확인 항목: 실제 registry에 push한 뒤 digest, image ID, Git commit, Jenkins build number가 운영 기록에 연결되는지 확인했다.

## 해석 / 의견

내 판단으로는 Jenkins Docker build에서 가장 중요한 값은 image tag 규칙이다. `BUILD_NUMBER`만 쓰면 Jenkins 안에서는 추적이 쉽지만 Git history와 직접 연결되지 않는다. Git commit short SHA, release tag, branch 이름, build number 중 무엇을 쓸지 팀 기준이 필요하다.

초급 기준으로는 아래 조합이 이해하기 쉽다.

```text
registry.example.com/team/app:<git-short-sha>
registry.example.com/team/app:<release-tag>
registry.example.com/team/app:latest-staging
```

다만 운영 기록에는 tag만 남기지 말고 push 결과의 digest도 남기는 편이 좋다. tag는 움직일 수 있지만 digest는 image content 기준의 고정값이기 때문이다.

## 한계와 예외

이 글은 Docker daemon을 agent에 어떻게 제공할지, Docker-in-Docker를 쓸지, remote Docker host를 쓸지, Kaniko나 BuildKit을 쓸지 비교하지 않는다.

private registry 인증, TLS, credential rotation, image signing, SBOM, vulnerability scan은 별도 보안/운영 주제로 다뤄야 한다.

## 참고자료

- Jenkins User Handbook, [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- Docker Docs, [docker image build](https://docs.docker.com/reference/cli/docker/image/build/)
- Docker Docs, [docker image push](https://docs.docker.com/reference/cli/docker/image/push/)
