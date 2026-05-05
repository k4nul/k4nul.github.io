---
layout: single
title: "Rust Service 05. 에러 응답을 일관되게 만들기"
description: "Rust API에서 내부 에러, 사용자 입력 에러, HTTP 상태 코드, JSON 에러 응답의 경계를 분리한다."
date: 2026-10-20 09:00:00 +09:00
lang: ko
translation_key: rust-api-consistent-error-response
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

운영되는 API에서 에러는 디버그 메시지가 아니라 사용자와 운영자가 함께 보는 계약이다.

내부 에러 원인은 로그에 남기고, 응답에는 안정적인 `code`, `message`, `requestId` 또는 RFC 9457의 Problem Details 형태처럼 문서화된 field만 내보낸다. 이번 글의 핵심은 Rust error type을 그대로 JSON에 노출하지 않고, HTTP 상태 코드와 응답 body를 한곳에서 매핑하는 것이다.

## Curriculum Position / 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: 요청/응답 타입 설계와 serde 사용 기준
- 다음 글: 설정 파일과 환경변수 분리하기
- 보강 기준: 실제 발행 전 예제 저장소, 실행 명령, 사용 버전, 실패 로그를 이 글의 범위에 맞춰 추가한다.

## Document Info / Environment

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial
- 테스트 환경: 직접 실행 테스트 없음. 아래 코드는 발행 전 예제 저장소에서 정상 응답, 400 응답, 500 응답을 나눠 확인해야 할 설계안이다.
- 테스트 버전: 실행 버전 미고정. 검증 기준일에 Axum `0.8.9`의 `IntoResponse`, RFC 9457, OWASP Error Handling Cheat Sheet를 기준으로 확인했다.
- 출처 성격: 공식 문서, 표준 문서, 보안 가이드

## Problem Statement / 문제 정의

handler가 `Result<T, E>`를 반환하기 시작하면 에러 표현을 어디서 통일할지 정해야 한다. 각 handler가 임의의 문자열과 상태 코드를 직접 만들면 같은 실패도 endpoint마다 다른 JSON 모양으로 나간다.

이번 글의 범위는 에러 응답을 일관되게 만드는 것이다. 목표는 내부 에러 타입, HTTP 상태 코드, 공개 JSON body, 로그 field를 분리해서 운영 중에도 검색하고 추적하기 쉬운 응답 계약을 만드는 것이다.

## Verified Facts / 확인한 사실

- Axum `IntoResponse` 문서는 handler에서 반환할 수 있는 응답을 만드는 trait이며, custom error type에 직접 구현할 수 있다고 설명한다. 따라서 `ApiError` 같은 타입에 HTTP status와 JSON body 매핑을 모으는 방식은 Axum의 응답 모델과 맞다. 근거: [Axum IntoResponse](https://docs.rs/axum/0.8.9/axum/response/trait.IntoResponse.html)
- Axum `IntoResponse` 구현 목록에는 `(StatusCode, R)` 조합이 포함된다. 따라서 `(status, Json(body)).into_response()` 형태로 상태 코드와 JSON body를 함께 반환할 수 있다. 근거: [Axum IntoResponse](https://docs.rs/axum/0.8.9/axum/response/trait.IntoResponse.html)
- RFC 9457은 HTTP API용 Problem Details 객체의 field로 `type`, `title`, `status`, `detail`, `instance`를 정의한다. `application/problem+json`을 표방한다면 이 field 의미를 따라야 하며, 임의의 `code/message` 구조를 RFC 9457 호환이라고 부르면 안 된다. 근거: [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html)
- OWASP Error Handling Cheat Sheet는 처리되지 않은 에러가 기술 스택, 버전, 경로, 쿼리 같은 정보를 노출해 공격자 정찰에 도움을 줄 수 있다고 설명한다. 예기치 않은 에러 세부 내용은 서버 측에 기록하고 사용자에게는 일반화된 응답을 반환하는 방향을 권장한다. 근거: [OWASP Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)

## Reproduction Steps / 재현 절차

아직 직접 실행 결과는 없다. 발행 전에는 최소 API 예제에 custom error type을 추가하고 정상 응답, 잘못된 입력, 내부 에러를 각각 확인한다.

이 시리즈의 단순 포맷은 다음처럼 둔다. RFC 9457을 사용하려면 `code/message/requestId` 대신 Problem Details field와 `application/problem+json` 의미를 별도로 맞춘다.

```rust
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde::Serialize;

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct ErrorResponse {
    code: &'static str,
    message: &'static str,
    request_id: Option<String>,
}

enum ApiError {
    BadRequest(&'static str),
    Internal,
}

impl ApiError {
    fn status_code(&self) -> StatusCode {
        match self {
            Self::BadRequest(_) => StatusCode::BAD_REQUEST,
            Self::Internal => StatusCode::INTERNAL_SERVER_ERROR,
        }
    }

    fn code(&self) -> &'static str {
        match self {
            Self::BadRequest(_) => "bad_request",
            Self::Internal => "internal_error",
        }
    }

    fn public_message(&self) -> &'static str {
        match self {
            Self::BadRequest(message) => message,
            Self::Internal => "unexpected server error",
        }
    }
}

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let status = self.status_code();
        let body = ErrorResponse {
            code: self.code(),
            message: self.public_message(),
            request_id: None,
        };

        (status, Json(body)).into_response()
    }
}
```

handler는 같은 error type을 반환한다.

```rust
async fn handler() -> Result<Json<&'static str>, ApiError> {
    Err(ApiError::BadRequest("invalid request body"))
}
```

발행 전 확인 항목은 다음과 같다.

```powershell
cargo test
cargo run
curl.exe -i http://127.0.0.1:3000/example-that-fails
```

## Observations / 관찰 결과

- 현재 문서에는 실제 `cargo test`, `cargo run`, `curl.exe` 출력이 없다.
- 성공 조건은 같은 에러 타입에서 HTTP status, JSON `code`, public `message`가 일관되게 나오는 것이다.
- 실패 조건은 내부 에러의 debug 문자열, stack trace, SQL query, 파일 경로, secret이 응답 body에 섞이는 경우다.

## Verification Checklist / 검증 체크리스트

- 모든 handler가 같은 공개 에러 응답 구조를 사용하는가?
- 4xx와 5xx가 같은 JSON field naming 정책을 따르는가?
- 내부 에러 원인이 응답이 아니라 로그에 남는가?
- 공개 `message`가 구현 detail, path, query, secret, dependency version을 노출하지 않는가?
- request id 또는 trace id가 응답과 로그를 연결할 수 있는가?
- RFC 9457을 표방한다면 `type`, `title`, `status`, `detail`, `instance` 의미와 content type을 맞췄는가?

## Interpretation / 해석

에러 응답은 개발 중에는 사소해 보이지만 운영에서는 검색 가능한 계약이 된다. `internal server error` 하나만 있으면 사용자는 할 수 있는 일이 없고, 운영자는 로그와 응답을 연결하기 어렵다.

반대로 내부 에러 문자열을 그대로 응답에 넣으면 디버깅은 편해 보여도 보안과 호환성 비용이 커진다. 공개 응답은 안정적으로 작게 유지하고, 자세한 원인은 구조화 로그와 request id로 찾는 편이 운영에 맞다.

## Limitations / 한계

- 이 글은 아직 실제 명령 실행 결과를 포함하지 않는다.
- 예제는 단순한 `code/message/requestId` 포맷이며 RFC 9457 Problem Details 전체 구현이 아니다.
- validation error의 field별 상세 표현은 다음 입력 검증 글에서 더 다룬다.
- request id 생성과 tracing 연결은 구조화 로깅 글에서 별도로 다룬다.
- 실제 발행 전에는 예제 저장소, 실행 명령, 버전, 실패 로그를 추가해야 한다.

## References / 참고자료

- [Axum IntoResponse](https://docs.rs/axum/0.8.9/axum/response/trait.IntoResponse.html)
- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html)
- [OWASP Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)

## Change Log / 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: Axum error mapping, RFC 9457 구분, OWASP 정보 노출 기준, 재현 절차를 보강.
