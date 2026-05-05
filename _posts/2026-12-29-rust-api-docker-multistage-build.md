---
layout: single
title: "Rust Service 15. Docker multi-stage build로 Rust API 이미지 만들기"
description: "Rust API를 builder stage와 runtime stage로 나누어 더 작은 컨테이너 이미지로 만드는 흐름을 정리한다."
date: 2026-12-29 09:00:00 +09:00
lang: ko
translation_key: rust-api-docker-multistage-build
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

운영 이미지에는 Rust compiler, cargo registry cache, 전체 source tree가 필요하지 않다. 필요한 것은 실행 파일과 런타임 의존 파일뿐이다.

Docker multi-stage build는 builder stage에서 컴파일하고 runtime stage에는 빌드 산출물만 복사하는 방식이다. 이미지 크기만 줄이는 기법이 아니라, 운영 이미지에 들어가는 파일의 경계를 명확히 하는 방법이다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: CORS, rate limit, request size limit 기본값 정하기
- 다음 글: .dockerignore, build cache, 이미지 크기 줄이기
- 보강 기준: 실제 발행 전 예제 저장소의 binary 이름, Docker 버전, build 로그, image size, container 실행 결과를 추가한다.

## 문서 정보

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial / container build 설계
- 테스트 환경: 직접 Docker build 실행 없음. 이 글은 Dockerfile 구조와 검증 기준을 정리한다.
- 테스트 버전: Docker CLI/Engine 버전 미기록, Rust toolchain 버전 미기록. 발행 전 실제 실행 환경을 기록해야 한다.
- 출처 성격: Docker 공식 문서, Dockerfile 작성 가이드, Rust 공식 이미지 관례

## 문제 정의

Rust API를 컨테이너로 배포할 때 단순히 `FROM rust` 이미지에서 실행하면 편하지만 운영 이미지가 커지고 불필요한 도구가 함께 들어간다.

운영 이미지에서 확인해야 할 질문은 다음과 같다.

- runtime image에 compiler와 source code가 남아 있는가?
- 빌드 결과 binary 이름이 Dockerfile의 `COPY` 경로와 일치하는가?
- base image tag가 재현 가능하게 고정되어 있는가?
- TLS 인증서나 timezone data처럼 런타임에 필요한 파일은 포함되어 있는가?
- root가 아닌 사용자로 실행해도 동작하는가?
- secret이 build layer나 image history에 남지 않는가?

이번 글에서는 build cache 최적화보다 stage 경계를 먼저 다룬다. cache와 image size 측정은 다음 글에서 별도로 정리한다.

## 확인한 사실

- Docker 공식 multi-stage 문서는 하나의 Dockerfile 안에서 여러 `FROM` instruction을 사용할 수 있고, 앞 stage의 산출물을 뒤 stage로 선택적으로 복사할 수 있다고 설명한다.
- Docker multi-stage build에서는 `AS`로 stage에 이름을 붙이고, `COPY --from=<stage>`로 특정 stage의 파일을 복사할 수 있다.
- Dockerfile best practices 문서는 base image tag가 변경될 수 있으므로 재현 가능한 build가 필요하면 digest pinning을 고려해야 한다고 설명한다.
- Docker build secrets 문서는 build secret을 Dockerfile의 `ARG`나 일반 `COPY` 대신 secret mount로 다루는 방식을 제공한다.
- Rust API가 동적 링크된 library나 TLS 인증서를 필요로 하는 경우, runtime stage에 해당 런타임 파일이 있어야 한다. `scratch`, distroless, Debian slim 중 무엇을 쓸지는 binary 링크 방식과 운영 요구에 따라 달라진다.

## Dockerfile 예시

아래 예시는 기본 구조를 보여 주기 위한 출발점이다. `rust-api`는 예시 binary 이름이므로 실제 `Cargo.toml`의 package 또는 bin 이름과 맞춰야 한다.

```dockerfile
# syntax=docker/dockerfile:1

FROM rust:1-slim-bookworm AS builder
WORKDIR /app

COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo build --release --locked

FROM debian:bookworm-slim AS runtime
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/target/release/rust-api /usr/local/bin/rust-api

ENV RUST_LOG=info
EXPOSE 3000
USER 65532:65532
ENTRYPOINT ["rust-api"]
```

이 예시는 일부러 단순하다. dependency cache를 더 잘 쓰려면 `cargo-chef`나 workspace 분리 전략을 검토할 수 있지만, 그 주제는 다음 글에서 다룬다.

## Stage 경계 체크

multi-stage build의 핵심은 "어떤 파일이 runtime image에 남는가"다.

| 위치 | 포함할 것 | 제외할 것 |
| --- | --- | --- |
| builder stage | Rust toolchain, source, Cargo registry/cache, build dependency | 운영 실행용 secret |
| runtime stage | release binary, CA certificates, 필요한 runtime file | compiler, cargo cache, 전체 source tree |
| build context | Dockerfile, source, lock file | `.env`, local database dump, test output, target directory |

`Cargo.lock`은 애플리케이션 binary를 재현 가능하게 빌드하기 위한 기준이 된다. `cargo build --release --locked`는 lock file과 dependency 해석이 어긋날 때 실패하게 하므로 CI에서 드러나기 쉽다.

## Base Image 고정

예시에서는 읽기 쉽게 `rust:1-slim-bookworm`과 `debian:bookworm-slim`을 사용했다. 실제 운영에서는 tag만으로 충분한지 확인해야 한다. Docker 문서 기준으로 tag는 시간이 지나며 다른 image를 가리킬 수 있으므로, 재현 가능성이 중요하면 digest까지 고정한다.

```dockerfile
FROM rust:1-slim-bookworm AS builder
FROM debian:bookworm-slim AS runtime
```

운영 정책이 더 엄격하면 다음 단계에서 digest pinning, image signing, SBOM, vulnerability scan을 함께 붙인다. 이 시리즈에서는 release와 scan을 뒤쪽 글에서 따로 다룬다.

## 보안 기본값

- secret을 `ARG`, `ENV`, `COPY`로 image layer에 남기지 않는다.
- private dependency token이 필요하면 Docker BuildKit secret mount 같은 별도 방식을 검토한다.
- runtime stage에서 root가 아닌 사용자로 실행한다.
- application이 파일을 써야 한다면 `USER` 전 단계에서 write directory를 만들고 소유권을 맞춘다.
- container 안의 default port와 Axum listener port를 문서화한다.
- image history에 민감한 값이 남지 않는지 확인한다.

## 재현 순서

실제 예제 저장소에서는 다음 명령과 결과를 기록한다.

1. Docker version을 기록한다.

```powershell
docker version
```

2. image를 build한다.

```powershell
docker build --pull -t rust-api:local .
```

3. container를 실행한다.

```powershell
docker run --rm -p 3000:3000 -e RUST_LOG=info rust-api:local
```

4. 다른 terminal에서 health endpoint를 확인한다.

```powershell
curl.exe -i http://127.0.0.1:3000/health
```

5. image 크기와 layer history를 확인한다.

```powershell
docker images rust-api:local
docker history rust-api:local
```

## 관찰 상태

이 글에는 아직 직접 실행 결과가 없다. 발행 전에는 다음 값을 추가해야 한다.

- `docker version` 출력
- `docker build --pull -t rust-api:local .` 성공 로그의 마지막 부분
- `docker run` 실행 후 API가 listen한 주소와 port
- `/health` 응답 status
- `docker images rust-api:local`의 image size
- `docker history rust-api:local`에서 secret이나 source copy가 보이지 않는다는 확인

## 검증 체크리스트

- builder stage와 runtime stage가 분리되어 있는가?
- runtime stage에 compiler, cargo cache, 전체 source tree가 들어가지 않는가?
- `COPY --from=builder`의 binary 경로가 실제 binary 이름과 맞는가?
- `cargo build --release --locked`가 lock file 기준으로 실행되는가?
- runtime stage에 필요한 CA certificate 같은 파일이 포함되어 있는가?
- root가 아닌 사용자로 실행하는가?
- image build 과정에서 secret이 layer나 history에 남지 않는가?
- build, run, health check, image size, history 확인 명령이 기록되어 있는가?

## 해석 / 의견

multi-stage build는 "이미지를 작게 만드는 방법"으로만 이해하면 절반만 보는 것이다. 더 중요한 효과는 운영 image의 파일 경계를 작게 만드는 데 있다. source와 compiler가 runtime에 없으면 공격 표면과 검토 범위가 줄어든다.

다만 stage를 나누었다고 자동으로 안전해지는 것은 아니다. build context에 secret이 들어가거나, runtime stage에 잘못 복사하거나, root 사용자로 실행하면 같은 문제가 남는다. 그래서 Dockerfile만 보지 말고 `docker history`, image size, 실행 사용자, health check까지 함께 확인해야 한다.

## 한계와 예외

- 이 글은 Docker build를 직접 실행하지 않은 설계 글이다.
- `scratch`나 distroless runtime image는 binary 링크 방식, DNS, TLS 인증서, timezone data 요구에 따라 별도 검증이 필요하다.
- OpenSSL 기반 crate를 쓰는지, rustls 기반 crate를 쓰는지에 따라 runtime 의존 파일이 달라질 수 있다.
- multi-architecture build, SBOM 생성, image scan, registry push는 뒤쪽 글에서 다룬다.

## 참고자료

- [Docker: Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker: Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker: Build secrets](https://docs.docker.com/build/building/secrets/)
- [Docker Hub: rust official image](https://hub.docker.com/_/rust)

## 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: Docker multi-stage build의 stage 경계, base image 고정, secret 처리, non-root 실행, 검증 명령을 공식 문서 기준으로 보강.
