---
layout: single
title: "Rust Service 16. .dockerignore, build cache, 이미지 크기 줄이기"
description: "Rust API 이미지 빌드에서 build context, .dockerignore, cache invalidation, 이미지 크기 확인 기준을 정리한다."
date: 2027-01-05 09:00:00 +09:00
lang: ko
translation_key: rust-api-dockerignore-cache-image-size
section: development
topic_key: rust
featured: false
track: rust
repo:
demo:
references:
categories: Rust
tags: [rust, axum, api, production, devops]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Docker 이미지가 느리게 빌드되거나 예상보다 커지는 문제는 대개 application code보다 build context와 layer 순서에서 먼저 생긴다.

`target/`, 로컬 산출물, 비밀 파일은 build context에서 제외하고, dependency layer와 source layer는 분리한다. 이미지 크기는 감으로 판단하지 말고 build context 전송량, image size, layer history를 함께 확인한다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: Docker multi-stage build로 Rust API 이미지 만들기
- 다음 글: GitHub Actions로 fmt, clippy, test, build 자동화하기
- 보강 기준: 실제 발행 전 예제 저장소에서 `.dockerignore` 적용 전후의 context 전송량, build 시간, image size, layer history를 기록한다.

## 문서 정보

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial / Docker build 운영 점검
- 테스트 환경: 직접 Docker build 실행 없음. 이 글은 Docker build context와 cache 설계 기준을 정리한다.
- 테스트 버전: Docker CLI/Engine 버전 미기록, BuildKit 버전 미기록, Rust toolchain 버전 미기록. 발행 전 실제 실행 환경을 기록해야 한다.
- 출처 성격: Docker 공식 문서

## 문제 정의

multi-stage build를 적용해도 build context가 크거나 layer 순서가 나쁘면 CI 시간이 길어지고, image에 불필요한 파일이 들어갈 가능성이 커진다.

확인해야 할 질문은 다음과 같다.

- `docker build .`에서 builder가 볼 수 있는 파일 집합은 무엇인가?
- `target/`, `.env`, local dump, test output이 context에 포함되는가?
- source file 하나를 바꿀 때 dependency build layer까지 매번 깨지는가?
- image size를 어느 명령으로 확인하고 기록할 것인가?
- layer history에서 secret이나 불필요한 copy가 보이지 않는가?

이번 글의 목적은 "빌드가 빠르다"가 아니라 "어떤 파일이 빌드에 들어가고, 어떤 변경이 cache를 깨는지 설명할 수 있다"에 있다.

## 확인한 사실

- Docker build context 문서는 build context를 build가 접근할 수 있는 파일 집합으로 설명한다.
- Docker 문서에 따르면 local directory를 build context로 쓰면 `COPY`와 `ADD` 같은 build instruction이 context 안의 파일과 directory를 참조할 수 있다.
- Docker build context 문서는 local directory context가 recursive하게 처리되며, current directory를 context로 쓰면 builder가 build에 필요한 파일을 context에서 읽는다고 설명한다.
- Docker cache 최적화 문서는 layer 순서, 작은 build context, bind mount, cache mount, external cache를 cache 활용 방법으로 제시한다.
- Docker cache mount 문서는 일반 layer cache가 instruction과 관련 파일의 exact match에 의존하고, cache mount는 package cache를 여러 build에 걸쳐 재사용할 수 있게 한다고 설명한다.
- Docker image tag는 편리한 이름이지만 움직일 수 있고, digest는 특정 image content를 가리키는 immutable identifier로 다뤄진다.

## .dockerignore 기준

`.dockerignore`는 image size를 줄이는 파일이 아니라 build context를 줄이는 파일이다. context에 들어간 파일은 Dockerfile에서 실수로 복사할 수 있고, remote builder나 CI에서는 전송 비용도 만든다.

Rust API의 시작점은 아래 정도로 잡을 수 있다.

```dockerignore
# Rust build output
target/

# Local environment and secrets
.env
.env.*
*.pem
*.key
*.p12

# Git and editor noise
.git/
.github/
.idea/
.vscode/

# Local data and generated output
*.db
*.sqlite
coverage/
tmp/
dist/

# Docker artifacts
docker-compose.override.yml
```

주의할 점은 `.github/`를 제외하면 Dockerfile 안에서 workflow 파일을 참조할 수 없다는 것이다. 대부분의 API image에는 필요 없지만, build metadata를 image label로 넣는 정책이 있다면 제외 규칙을 다시 검토한다.

## Cache 친화적인 Dockerfile 순서

source 전체를 먼저 복사하면 작은 코드 변경도 dependency build cache를 깨기 쉽다. 먼저 dependency 판단에 필요한 파일을 복사하고, dependency build와 source build를 분리한다.

아래 예시는 구조 설명용이다. 실제 dependency cache를 더 정교하게 쓰려면 `cargo-chef` 같은 도구를 검토할 수 있다.

```dockerfile
# syntax=docker/dockerfile:1

FROM rust:1-slim-bookworm AS builder
WORKDIR /app

COPY Cargo.toml Cargo.lock ./
COPY src ./src

RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release --locked

FROM debian:bookworm-slim AS runtime
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/target/release/rust-api /usr/local/bin/rust-api

USER 65532:65532
ENTRYPOINT ["rust-api"]
```

BuildKit cache mount를 쓰면 package cache를 build 사이에 재사용할 수 있다. 다만 cache mount는 image에 들어가는 파일과 다르다. build가 빨라졌다고 runtime image가 자동으로 작아지는 것은 아니다.

## 이미지 크기 확인 기준

image size는 하나의 숫자만 보지 않는다.

| 확인 대상 | 명령 | 보는 이유 |
| --- | --- | --- |
| build context 전송량 | `docker build --progress=plain -t rust-api:cache-check .` | `transferring context`가 과하게 크지 않은지 확인 |
| 최종 image size | `docker images rust-api:cache-check` | 이전 build와 비교할 기준값 |
| layer history | `docker history rust-api:cache-check` | secret, source copy, package cache가 남지 않았는지 확인 |
| container 동작 | `docker run --rm -p 3000:3000 rust-api:cache-check` | 작게 만든 image가 실제로 실행되는지 확인 |

작은 image가 항상 좋은 image는 아니다. TLS certificate, timezone data, 진단용 최소 파일이 필요한 서비스라면 그 파일은 포함해야 한다. 목표는 "무조건 작게"가 아니라 "필요한 파일만 설명 가능하게"다.

## 재현 순서

발행 전 예제 저장소에서는 아래 절차를 기록한다.

1. Docker version을 기록한다.

```powershell
docker version
```

2. `.dockerignore` 적용 전 build context 전송량과 image size를 기록한다.

```powershell
docker build --progress=plain -t rust-api:before-ignore .
docker images rust-api:before-ignore
docker history rust-api:before-ignore
```

3. `.dockerignore` 적용 후 같은 값을 기록한다.

```powershell
docker build --progress=plain -t rust-api:after-ignore .
docker images rust-api:after-ignore
docker history rust-api:after-ignore
```

4. source file 하나만 수정한 뒤 어느 layer부터 cache가 깨지는지 확인한다.

```powershell
docker build --progress=plain -t rust-api:cache-check .
```

5. 최종 image가 실행되는지 확인한다.

```powershell
docker run --rm -p 3000:3000 rust-api:after-ignore
curl.exe -i http://127.0.0.1:3000/health
```

## 관찰 상태

이 글에는 아직 직접 실행 결과가 없다. 발행 전에는 다음 값을 추가해야 한다.

- Docker CLI/Engine version
- `.dockerignore` 적용 전후 `transferring context` 크기
- `.dockerignore` 적용 전후 image size
- source 변경 후 cache hit/miss가 발생한 layer
- `docker history`에서 secret과 local artifact가 보이지 않는다는 확인
- `/health` 응답 status

## 검증 체크리스트

- `target/`, `.env`, local dump, test output이 build context에서 제외되는가?
- `.dockerignore`가 Dockerfile에서 필요한 파일까지 제외하지 않는가?
- dependency 판단 파일과 source file copy 순서가 분리되어 있는가?
- BuildKit cache mount를 쓰는 경우 image 내용과 cache 내용을 혼동하지 않는가?
- image size와 layer history를 함께 기록했는가?
- secret이 build context, image layer, image history에 남지 않는가?
- 작아진 image가 실제 health check를 통과하는가?

## 해석 / 의견

Docker build 최적화는 "명령을 더 복잡하게 만드는 일"이 아니다. build에 들어가는 파일과 cache가 깨지는 이유를 줄이는 일이다. Rust 프로젝트에서는 `target/` 하나만 context에 들어가도 전송량과 실수 가능성이 크게 늘 수 있다.

또한 build cache와 image size는 다른 문제다. cache는 build 시간을 줄이고, `.dockerignore`는 context와 실수 표면을 줄이며, multi-stage build는 runtime image의 파일 경계를 줄인다. 세 가지를 분리해서 보면 원인을 찾기 쉽다.

## 한계와 예외

- 이 글은 Docker build를 직접 실행하지 않은 설계 글이다.
- workspace 구조, private dependency, native library 사용 여부에 따라 cache 전략이 달라질 수 있다.
- `cargo-chef`, `sccache`, registry cache, GitHub Actions cache는 다음 CI 단계에서 더 구체적으로 다룰 수 있다.
- image size를 줄이는 과정에서 TLS certificate나 필요한 runtime file을 제거하면 런타임 장애가 생길 수 있다.

## 참고자료

- [Docker: Build context](https://docs.docker.com/build/concepts/context/)
- [Docker: Optimize cache usage in builds](https://docs.docker.com/build/cache/optimize/)
- [Docker: Build cache](https://docs.docker.com/build/cache/)
- [Docker: Pull an image by digest](https://docs.docker.com/reference/cli/docker/image/pull/)

## 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: `.dockerignore`, build context, cache mount, image size, layer history 검증 기준을 Docker 공식 문서 기준으로 보강.
