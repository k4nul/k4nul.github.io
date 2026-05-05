---
layout: single
title: "Rust Service 07. tracing으로 구조화 로그 남기기"
description: "Rust tracing의 event와 span을 사용해 요청 단위로 추적 가능한 로그 구조를 만든다."
date: 2026-11-03 09:00:00 +09:00
lang: ko
translation_key: rust-api-structured-logging-tracing
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

문자열 로그만 남기면 요청 하나가 여러 비동기 작업으로 나뉘는 순간 따라가기 어렵다. span은 작업의 범위와 관계를 남기는 도구다.

요청 단위 로그는 `method`, `path`, `status`, `latency`, `requestId` 같은 field 이름을 고정해야 검색과 집계가 쉬워진다. header, token, password, request body 전체처럼 민감할 수 있는 값은 기본 로그 field에서 제외한다.

## Curriculum Position / 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: 설정 파일과 환경변수 분리하기
- 다음 글: 입력 검증과 잘못된 요청 처리하기
- 보강 기준: 실제 발행 전 예제 저장소, 실행 명령, 사용 버전, 실패 로그를 이 글의 범위에 맞춰 추가한다.

## Document Info / Environment

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial
- 테스트 환경: 직접 실행 테스트 없음. 아래 코드는 발행 전 예제 저장소에서 요청 로그 field와 민감값 미노출 여부를 확인해야 할 설계안이다.
- 테스트 버전: 실행 버전 미고정. 검증 기준일에 `tracing`, `tracing-subscriber 0.3.23`, `tower-http 0.6.8` 문서를 기준으로 확인했다.
- 출처 성격: 공식 문서, 원 프로젝트 문서

## Problem Statement / 문제 정의

API가 비동기로 동작하면 하나의 요청이 여러 함수와 await 지점으로 흩어진다. 단순 문자열 로그는 어떤 요청의 어떤 단계에서 생긴 일인지 연결하기 어렵다.

이번 글의 범위는 `tracing`으로 구조화 로그를 남기는 것이다. 목표는 로그 메시지를 예쁘게 만드는 것이 아니라, 요청 단위로 검색 가능한 field와 span을 남기는 것이다.

## Verified Facts / 확인한 사실

- `tracing` 문서는 span을 시작과 끝이 있는 기간을 나타내며, 프로그램 실행 흐름의 맥락을 표현하는 구조로 설명한다. event는 특정 시점에 발생한 일을 나타내고 span 안에서 발생할 수 있다. 근거: [tracing crate documentation](https://docs.rs/tracing/latest/tracing/)
- `tracing` 문서는 span과 event의 structured field를 `field_name = field_value` 형태로 기록할 수 있다고 설명한다. 따라서 `method`, `path`, `status_code` 같은 field를 문자열 안에 묻지 않고 별도 field로 남길 수 있다. 근거: [tracing crate documentation](https://docs.rs/tracing/latest/tracing/)
- `tracing-subscriber`의 `fmt` 문서는 span과 event를 stdout에 기록하는 subscriber를 제공하며, `EnvFilter`를 통해 `RUST_LOG` 환경변수로 runtime filtering을 할 수 있다고 설명한다. 근거: [tracing-subscriber fmt](https://docs.rs/tracing-subscriber/latest/tracing_subscriber/fmt/)
- `tracing-subscriber`의 formatter 문서는 JSON formatter가 newline-delimited JSON logs를 출력하며, 이는 production에서 structured log 소비 도구가 JSON을 읽는 경우를 위한 형식이라고 설명한다. 근거: [tracing-subscriber fmt](https://docs.rs/tracing-subscriber/latest/tracing_subscriber/fmt/)
- `tower-http`의 `TraceLayer` 문서는 HTTP service에 high-level tracing을 추가하는 middleware이며, `on_response` callback에서 latency와 response status를 기록할 수 있다고 설명한다. 근거: [tower-http TraceLayer](https://docs.rs/tower-http/latest/tower_http/trace/index.html)

## Reproduction Steps / 재현 절차

아직 직접 실행 결과는 없다. 발행 전에는 최소 API 예제에 `tracing-subscriber`와 `TraceLayer`를 추가하고, 요청 1개가 어떤 log field를 남기는지 기록한다.

```powershell
cargo add tracing
cargo add tracing-subscriber --features env-filter,json
cargo add tower-http --features trace
```

초기화 코드는 시작 지점에 둔다.

```rust
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};

fn init_tracing() {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info,tower_http=info"));

    tracing_subscriber::registry()
        .with(filter)
        .with(tracing_subscriber::fmt::layer().json())
        .init();
}
```

라우터에는 HTTP 요청 단위 tracing layer를 붙인다.

```rust
use axum::Router;
use tower_http::trace::TraceLayer;

fn build_router() -> Router {
    Router::new()
        // routes...
        .layer(TraceLayer::new_for_http())
}
```

발행 전 확인 명령은 다음처럼 둔다.

```powershell
$env:RUST_LOG="info,tower_http=trace"
cargo run
curl.exe http://127.0.0.1:3000/health
```

## Observations / 관찰 결과

- 현재 문서에는 실제 로그 출력이 없다.
- 성공 조건은 요청 1개에 대해 method, path, status, latency를 검색 가능한 field로 확인할 수 있는 것이다.
- 실패 조건은 `authorization`, `cookie`, `set-cookie`, password, token, request body 전체가 기본 로그에 포함되는 경우다.

## Verification Checklist / 검증 체크리스트

- 로그 field 이름이 요청마다 일관적인가?
- `RUST_LOG`로 로그 레벨을 바꿀 수 있는가?
- HTTP 요청 시작과 응답 완료를 같은 span 또는 연결 가능한 field로 추적할 수 있는가?
- status와 latency가 문자열 메시지 안이 아니라 field로 남는가?
- header와 body를 통째로 로그에 남기지 않는가?
- request id 또는 trace id를 에러 응답과 로그에 연결할 계획이 있는가?

## Interpretation / 해석

운영 로그는 사람이 읽는 문장인 동시에 시스템이 검색하는 데이터다. `request finished`라는 문자열만 있으면 눈으로는 읽히지만, status별 집계나 latency 검색에는 약하다.

반대로 모든 값을 field로 남기는 것도 위험하다. header나 body에는 secret과 개인정보가 섞일 수 있으므로, 기본 field는 method, path template, status, latency, request id처럼 운영에 필요한 최소값으로 시작하는 편이 안전하다.

## Limitations / 한계

- 이 글은 아직 실제 로그 출력과 실행 결과를 포함하지 않는다.
- 예제는 structured logging의 시작점이며 OpenTelemetry trace export나 metrics export는 뒤의 관측성 글에서 다룬다.
- `TraceLayer::new_for_http()`의 기본 출력만으로 조직의 log schema를 모두 만족한다고 가정하지 않는다.
- header logging은 기본적으로 제외하고, 필요할 때 allowlist 방식으로 좁게 추가해야 한다.
- 실제 발행 전에는 예제 저장소, 실행 명령, 버전, 실패 로그를 추가해야 한다.

## References / 참고자료

- [tracing crate documentation](https://docs.rs/tracing/latest/tracing/)
- [tracing-subscriber fmt](https://docs.rs/tracing-subscriber/latest/tracing_subscriber/fmt/)
- [tower-http TraceLayer](https://docs.rs/tower-http/latest/tower_http/trace/index.html)

## Change Log / 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: tracing span/event 근거, JSON formatter, TraceLayer 사용 범위, 민감정보 로그 한계를 분리해 수정.
