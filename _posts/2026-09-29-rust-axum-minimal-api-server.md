---
layout: single
title: "Rust Service 02. Axum으로 최소 API 서버 만들기"
description: "Axum의 Router, route, handler, Json 응답을 사용해 가장 작은 Rust API 서버의 형태를 잡는다."
date: 2026-09-29 09:00:00 +09:00
lang: ko
translation_key: rust-axum-minimal-api-server
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

## Summary / 요약

최소 서버의 목적은 기능을 많이 넣는 것이 아니라 서버가 어디서 시작되고, 라우터가 어디서 조립되며, handler가 어떤 타입을 주고받는지 확인하는 것이다. 이번 단계에서는 `/health`와 작은 JSON echo endpoint만 둔다.

상태 공유, 데이터베이스 연결, 인증, tracing, graceful shutdown은 다음 글로 미룬다. 그래야 첫 예제가 Axum의 Router, route, handler, Json 응답이라는 가장 작은 경계를 흐리지 않는다.

## Curriculum Position / 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: Rust 웹 서비스에서 Rust가 책임질 영역 정하기
- 다음 글: Rust API 프로젝트 구조 잡기
- 보강 기준: 실제 발행 전 예제 저장소, 실행 명령, 사용 버전, 실패 로그를 이 글의 범위에 맞춰 추가한다.

## Document Info / Environment

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial
- 테스트 환경: 직접 실행 테스트 없음. 아래 코드는 발행 전 로컬에서 재현해야 할 최소 예제 방향이며, 아직 성공 출력으로 기록하지 않는다.
- 테스트 버전: 실행 버전 미고정. 검증 기준일에 docs.rs의 Axum latest 페이지는 `0.8.9`로 표시되었고, Tokio는 공식 프로젝트 문서 기준으로 확인했다.
- 출처 성격: 공식 문서, 원 프로젝트 문서

## Problem Statement / 문제 정의

이 커리큘럼의 목표는 Rust로 API 하나를 만드는 데서 끝나지 않고, 그 API를 빌드하고 배포하고 관측하고 되돌릴 수 있는 운영 단위로 만드는 것이다.

이번 글의 범위는 Axum으로 최소 API 서버를 만드는 것이다. 이 단계에서 확인할 것은 "서버가 뜬다"가 아니라 "라우터와 handler의 타입 경계가 보인다"는 점이다.

## Verified Facts / 확인한 사실

- Axum 공식 문서는 `Router`가 어떤 path를 어떤 service나 handler로 보낼지 설정하는 타입이라고 설명한다. 따라서 최소 서버의 첫 확인 대상은 route 목록이다. 근거: [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- Axum 공식 문서는 handler를 extractor를 인자로 받고 response로 변환 가능한 값을 반환하는 async function으로 설명한다. 따라서 handler의 입력과 출력 타입을 작게 유지하는 것이 첫 예제의 핵심이다. 근거: [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- Axum 공식 문서는 `Json` 응답이 `serde::Serialize`를 구현한 값을 JSON 응답으로 만들 수 있다고 설명한다. JSON echo 예제는 이 경계를 확인하기에 충분하다. 근거: [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- Tokio 공식 프로젝트 문서는 Tokio를 Rust 비동기 런타임으로 설명하며, 네트워크 애플리케이션 작성에 필요한 기반 요소를 제공한다고 설명한다. 따라서 `#[tokio::main]`과 TCP listener 구동은 이 예제의 실행 전제다. 근거: [Tokio project](https://tokio.rs/)

## Reproduction Steps / 재현 절차

아직 직접 실행한 결과는 없다. 실제 발행 전에는 아래 절차를 로컬에서 실행하고 성공 출력과 실패 조건을 함께 기록한다.

```powershell
cargo new rust-api-minimal
cd rust-api-minimal
cargo add axum@0.8.9
cargo add tokio@1 --features macros,rt-multi-thread
cargo add serde --features derive
cargo add serde_json
```

`src/main.rs`의 검증 대상 예시는 다음처럼 작게 둔다.

```rust
use axum::{routing::{get, post}, Json, Router};
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
struct Health {
    status: &'static str,
}

#[derive(Deserialize, Serialize)]
struct EchoRequest {
    message: String,
}

async fn health() -> Json<Health> {
    Json(Health { status: "ok" })
}

async fn echo(Json(payload): Json<EchoRequest>) -> Json<EchoRequest> {
    Json(payload)
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/health", get(health))
        .route("/echo", post(echo));

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await
        .expect("bind listener");

    axum::serve(listener, app).await.expect("run server");
}
```

발행 전 확인 명령은 다음 두 요청으로 충분하다.

```powershell
cargo run
curl.exe http://127.0.0.1:3000/health
curl.exe -X POST http://127.0.0.1:3000/echo -H "content-type: application/json" -d '{"message":"hello"}'
```

## Observations / 관찰 결과

- 현재 문서에는 실제 `cargo run` 또는 `curl` 출력이 없다.
- 발행 전 성공 조건은 `/health`가 200 JSON 응답을 반환하고, `/echo`가 받은 JSON payload를 그대로 JSON으로 돌려주는 것이다.
- 실패 조건은 서버 bind 실패, dependency version 불일치, JSON body 파싱 실패, route 오타를 구분해서 기록한다.

## Verification Checklist / 검증 체크리스트

- `Router`에 등록된 route가 글에서 설명한 endpoint와 일치하는가?
- handler 입력 타입과 출력 타입이 본문에서 보이는가?
- 실행 명령과 HTTP 확인 명령의 실제 출력이 기록되어 있는가?
- 실패했을 때 route 없음, JSON 파싱 실패, listener bind 실패를 구분할 수 있는가?
- 공식 문서의 예제 API가 검증 기준일 기준으로 아직 맞는가?

## Interpretation / 해석

Rust API 운영 글은 언어 기능 설명만으로는 부족하다. 실제 운영에서 문제는 대개 코드와 코드 바깥 경계 사이에서 생긴다.

첫 서버는 작을수록 좋다. 이 단계에서 database pool, configuration loader, error enum, tracing layer를 모두 넣으면 route와 handler의 기본 경계를 확인하기 어렵다. 운영 준비는 뒤에서 붙이되, 첫 실행 단위는 읽는 사람이 한 화면에서 이해할 수 있어야 한다.

## Limitations / 한계

- 이 글은 아직 실제 명령 실행 결과를 포함하지 않는다.
- 이 예제는 TLS, authentication, authorization, rate limiting, request size limit, graceful shutdown을 다루지 않는다.
- JSON echo는 타입 경계 확인용 예제이며 비즈니스 API 설계 예시는 아니다.
- 실제 발행 전에는 예제 저장소, 실행 명령, 버전, 실패 로그를 추가해야 한다.

## References / 참고자료

- [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- [Tokio project](https://tokio.rs/)

## Change Log / 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: 최소 Axum 서버의 근거, 재현 절차, 성공 조건, 한계를 분리해 수정.
