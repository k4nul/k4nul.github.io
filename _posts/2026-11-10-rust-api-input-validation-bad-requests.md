---
layout: single
title: "Rust Service 08. 입력 검증과 잘못된 요청 처리하기"
description: "Rust API에서 JSON 파싱 실패, 필드 검증 실패, 크기 제한 실패를 구분해 400 계열 응답으로 정리한다."
date: 2026-11-10 09:00:00 +09:00
lang: ko
translation_key: rust-api-input-validation-bad-requests
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

입력 검증은 handler 안쪽의 임시 if문 모음이 아니다. 외부 계약을 보호하는 첫 번째 경계다.

JSON 파싱 실패, DTO 역직렬화 실패, field 검증 실패, body size 제한 실패는 원인과 응답 메시지가 다르다. 각 실패가 어떤 공개 error code와 HTTP 상태 코드로 나가는지 표로 고정해야 클라이언트와 운영 로그가 흔들리지 않는다.

## Curriculum Position / 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: tracing으로 구조화 로그 남기기
- 다음 글: SQLite 또는 PostgreSQL 붙이기
- 보강 기준: 실제 발행 전 예제 저장소, 실행 명령, 사용 버전, 실패 로그를 이 글의 범위에 맞춰 추가한다.

## Document Info / Environment

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial
- 테스트 환경: 직접 실행 테스트 없음. 아래 코드는 발행 전 예제 저장소에서 malformed JSON, schema mismatch, field validation failure, body size limit을 나눠 확인해야 할 설계안이다.
- 테스트 버전: 실행 버전 미고정. 검증 기준일에 Axum `0.8.9` extractor 문서와 OWASP Input Validation Cheat Sheet를 기준으로 확인했다.
- 출처 성격: 공식 문서, 보안 가이드

## Problem Statement / 문제 정의

요청 body가 JSON이 아니거나, JSON은 맞지만 DTO 타입과 맞지 않거나, 타입은 맞지만 값이 정책을 어길 수 있다. 이 실패들을 모두 "bad request" 문자열 하나로 처리하면 클라이언트가 고칠 수 있는 문제인지 판단하기 어렵다.

이번 글의 범위는 입력 검증과 잘못된 요청 처리다. 목표는 parsing, syntactic validation, semantic validation, size limit을 분리하고, 공개 응답은 일관되게 작게 유지하는 것이다.

## Verified Facts / 확인한 사실

- Axum extractor 문서는 handler argument로 들어오는 extractor가 request에서 데이터를 추출하며, `Json` extractor가 request body를 소비해 대상 타입으로 역직렬화한다고 설명한다. 근거: [Axum extractors](https://docs.rs/axum/0.8.9/axum/extract/index.html)
- Axum extractor 문서는 body를 소비하는 extractor는 하나만 사용할 수 있고 마지막 argument여야 한다고 설명한다. 따라서 `Json<T>`와 raw body extractor를 동시에 두는 방식으로 검증을 나누면 안 된다. 근거: [Axum extractors](https://docs.rs/axum/0.8.9/axum/extract/index.html)
- Axum extractor 문서는 `JsonRejection`을 통해 missing content type, JSON syntax error, JSON data error, body extraction failure를 구분해서 처리하는 예를 제공한다. 근거: [Axum extractors](https://docs.rs/axum/0.8.9/axum/extract/index.html)
- Axum `DefaultBodyLimit` 문서는 `Bytes`, `String`, `Json`, `Form` 같은 extractor가 내부적으로 사용하는 body 크기 기본 제한이 2MB라고 설명하고, `DefaultBodyLimit::max`로 조정할 수 있다고 설명한다. 근거: [Axum DefaultBodyLimit](https://docs.rs/axum/0.8.9/axum/extract/struct.DefaultBodyLimit.html)
- OWASP Input Validation Cheat Sheet는 입력 검증을 가능한 한 외부 입력을 받은 직후 수행하라고 설명하며, syntactic validation과 semantic validation을 모두 적용하라고 설명한다. denylist는 보조 방어로만 사용하고 allowlist가 더 robust한 접근이라고 설명한다. 근거: [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)

## Reproduction Steps / 재현 절차

아직 직접 실행 결과는 없다. 발행 전에는 최소 API 예제의 create handler에 JSON rejection 처리, field validation, body limit을 추가하고 각 실패 응답을 기록한다.

```rust
use axum::{
    extract::{rejection::JsonRejection, DefaultBodyLimit},
    http::StatusCode,
    routing::post,
    Json, Router,
};
use serde::Deserialize;

#[derive(Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
struct CreateUserRequest {
    email: String,
    display_name: String,
}

#[derive(Debug)]
struct FieldError {
    field: &'static str,
    code: &'static str,
}

enum ApiError {
    BadRequest(&'static str),
    Validation(Vec<FieldError>),
}

fn validate_create_user(input: &CreateUserRequest) -> Result<(), Vec<FieldError>> {
    let mut errors = Vec::new();

    if input.email.trim().is_empty() {
        errors.push(FieldError {
            field: "email",
            code: "required",
        });
    }

    if input.display_name.len() < 2 || input.display_name.len() > 40 {
        errors.push(FieldError {
            field: "displayName",
            code: "length",
        });
    }

    if errors.is_empty() { Ok(()) } else { Err(errors) }
}

fn map_json_rejection(rejection: JsonRejection) -> ApiError {
    match rejection {
        JsonRejection::MissingJsonContentType(_) => {
            ApiError::BadRequest("missing_json_content_type")
        }
        JsonRejection::JsonSyntaxError(_) => ApiError::BadRequest("invalid_json_syntax"),
        JsonRejection::JsonDataError(_) => ApiError::BadRequest("invalid_json_data"),
        JsonRejection::BytesRejection(_) => ApiError::BadRequest("invalid_request_body"),
        _ => ApiError::BadRequest("invalid_request"),
    }
}

async fn create_user(
    payload: Result<Json<CreateUserRequest>, JsonRejection>,
) -> Result<StatusCode, ApiError> {
    let Json(input) = payload.map_err(map_json_rejection)?;
    validate_create_user(&input).map_err(ApiError::Validation)?;
    Ok(StatusCode::CREATED)
}

fn build_router() -> Router {
    Router::new()
        .route("/users", post(create_user))
        .layer(DefaultBodyLimit::max(16 * 1024))
}
```

응답 분류 기준은 먼저 표로 고정한다.

| 실패 종류 | 공개 code | 권장 HTTP 상태 |
| --- | --- | --- |
| `Content-Type` 누락 | `missing_json_content_type` | 400 |
| JSON syntax 오류 | `invalid_json_syntax` | 400 |
| DTO field type/shape 불일치 | `invalid_json_data` | 400 |
| field 검증 실패 | `validation_failed` | 400 또는 422 |
| body size 제한 초과 | `payload_too_large` | 413 |
| business conflict | `conflict` | 409 |

발행 전 확인 요청은 다음처럼 분리한다.

```powershell
curl.exe -i -X POST http://127.0.0.1:3000/users -H "content-type: application/json" -d "{"
curl.exe -i -X POST http://127.0.0.1:3000/users -H "content-type: application/json" -d '{"email":"","displayName":"a"}'
curl.exe -i -X POST http://127.0.0.1:3000/users -H "content-type: text/plain" -d "hello"
```

## Observations / 관찰 결과

- 현재 문서에는 실제 `cargo run` 또는 `curl.exe` 출력이 없다.
- 성공 조건은 parsing 실패, DTO 변환 실패, field 검증 실패가 서로 다른 공개 `code`로 기록되는 것이다.
- 실패 조건은 내부 serde error 전체, panic message, request body 원문, secret field가 응답이나 로그에 그대로 남는 경우다.

## Verification Checklist / 검증 체크리스트

- JSON syntax error와 DTO data error를 같은 메시지로 뭉개지 않았는가?
- field validation 실패가 어떤 field와 code를 반환하는지 문서화되어 있는가?
- body size limit 초과가 413 계열로 확인되었는가?
- validation error가 내부 구현 detail을 노출하지 않는가?
- allowlist 또는 명시적 range/length 검증을 우선 사용했는가?
- 잘못된 요청 샘플과 실제 응답 body가 기록되어 있는가?

## Interpretation / 해석

입력 검증은 보안 기능이면서 API 사용성 기능이다. 클라이언트가 고칠 수 있는 문제를 안정적인 code와 field 목록으로 알려주면, 운영자는 bad request 증가를 원인별로 볼 수 있고 클라이언트는 재시도보다 수정이 필요한 상황을 구분할 수 있다.

다만 validation은 인증, SQL injection 방어, output encoding을 대체하지 않는다. OWASP가 말하듯 입력 검증은 잘못된 데이터가 workflow에 들어오는 것을 줄이는 첫 경계이고, 다른 방어 계층과 함께 써야 한다.

## Limitations / 한계

- 이 글은 아직 실제 명령 실행 결과를 포함하지 않는다.
- 예제의 email 검증은 빈 값 여부만 확인한다. 실제 email syntax와 deliverability 검증은 별도 정책이 필요하다.
- 400과 422 중 어떤 상태를 쓸지는 API 정책에 따라 달라질 수 있으므로 이 시리즈에서는 먼저 일관성을 우선한다.
- validator crate, JSON Schema, OpenAPI schema generation은 별도 선택지이며 이 글에서는 직접 구현 기준만 다룬다.
- 실제 발행 전에는 예제 저장소, 실행 명령, 버전, 실패 로그를 추가해야 한다.

## References / 참고자료

- [Axum extractors](https://docs.rs/axum/0.8.9/axum/extract/index.html)
- [Axum DefaultBodyLimit](https://docs.rs/axum/0.8.9/axum/extract/struct.DefaultBodyLimit.html)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)

## Change Log / 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: Axum rejection 분류, body limit, OWASP syntactic/semantic validation 기준, 재현 절차를 보강.
