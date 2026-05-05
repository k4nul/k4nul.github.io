---
layout: single
title: "Rust Service 05. Making API error responses consistent"
description: "Separates internal errors, user input errors, HTTP status codes, and JSON error responses in a Rust API."
date: 2026-10-20 09:00:00 +09:00
lang: en
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
permalink: /en/rust/rust-api-consistent-error-response/
---

## Summary

In an operated API, errors are not debug strings. They are contracts seen by users and operators.

Log internal causes, and return only documented fields such as `code`, `message`, `requestId`, or an RFC 9457 Problem Details shape. The core rule is to avoid exposing Rust error values directly as JSON and to map internal errors, HTTP status codes, and public response bodies in one place.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Designing request and response types with serde
- Next post: Separating config files and environment variables
- Expansion criteria: before publication, add the example repository, commands, tool versions, and failure logs that fit this post's scope.

## Document Info / Environment

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial
- Test environment: No direct execution test. The code below is a design target to verify in the example repository with success, 400, and 500 responses before publication.
- Tested versions: No runtime versions pinned. On the verification date, this was checked against Axum `0.8.9` `IntoResponse`, RFC 9457, and the OWASP Error Handling Cheat Sheet.
- Evidence level: official documentation, standards document, security guide

## Problem Statement

Once handlers return `Result<T, E>`, the service needs a single place to define error representation. If each handler invents its own status code and JSON string, the same failure can look different across endpoints.

This post covers making API error responses consistent. The goal is to separate internal error types, HTTP status codes, public JSON bodies, and log fields so the API remains searchable and traceable in operation.

## Verified Facts

- Axum `IntoResponse` documentation describes the trait used to create responses from handler return values and notes that it can be implemented for custom error types. That supports collecting HTTP status and JSON body mapping on a type such as `ApiError`. Evidence: [Axum IntoResponse](https://docs.rs/axum/0.8.9/axum/response/trait.IntoResponse.html)
- Axum's `IntoResponse` implementations include `(StatusCode, R)`. That makes `(status, Json(body)).into_response()` a supported way to return both status code and JSON body. Evidence: [Axum IntoResponse](https://docs.rs/axum/0.8.9/axum/response/trait.IntoResponse.html)
- RFC 9457 defines Problem Details fields for HTTP APIs, including `type`, `title`, `status`, `detail`, and `instance`. If an API claims `application/problem+json`, it should follow those field meanings; a custom `code/message` response should not be described as RFC 9457 compliant without that mapping. Evidence: [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html)
- The OWASP Error Handling Cheat Sheet explains that unhandled errors can expose stack, version, path, and query information useful for attacker reconnaissance. Unexpected error details should be logged server-side while users receive a generic response. Evidence: [OWASP Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)

## Reproduction Steps

There is no direct execution result yet. Before publication, add a custom error type to the minimal API example and verify a successful response, a bad request, and an internal error separately.

This series uses a small custom format. If you choose RFC 9457 instead, replace `code/message/requestId` with Problem Details fields and the corresponding `application/problem+json` semantics.

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

Handlers return the same error type.

```rust
async fn handler() -> Result<Json<&'static str>, ApiError> {
    Err(ApiError::BadRequest("invalid request body"))
}
```

Before publication, verify this with:

```powershell
cargo test
cargo run
curl.exe -i http://127.0.0.1:3000/example-that-fails
```

## Observations

- This document currently contains no actual `cargo test`, `cargo run`, or `curl.exe` output.
- The success condition is that the same error type consistently produces HTTP status, JSON `code`, and public `message`.
- Failure conditions include leaking debug strings, stack traces, SQL queries, filesystem paths, or secrets into the response body.

## Verification Checklist

- Do all handlers use the same public error response structure?
- Do 4xx and 5xx responses follow the same JSON field naming policy?
- Are internal error causes recorded in logs instead of the public response?
- Does the public `message` avoid implementation details, paths, queries, secrets, and dependency versions?
- Can a request id or trace id connect the response to logs?
- If the API claims RFC 9457 support, do `type`, `title`, `status`, `detail`, `instance`, and content type match that claim?

## Interpretation

Error responses can look minor during development, but in production they become searchable contracts. If every failure says only `internal server error`, users have no next step and operators struggle to connect a response to logs.

Returning raw internal error strings feels convenient while debugging, but it creates security and compatibility cost. Keep public responses small and stable, then use structured logs plus request ids for the details.

## Limitations

- This post does not yet include executed command output.
- The example uses a small `code/message/requestId` format, not a full RFC 9457 Problem Details implementation.
- Field-level validation error details are handled later in the input validation post.
- Request id generation and tracing linkage are handled later in the structured logging post.
- Before publication, add an example repository, commands, versions, and failure logs.

## References

- [Axum IntoResponse](https://docs.rs/axum/0.8.9/axum/response/trait.IntoResponse.html)
- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html)
- [OWASP Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Added Axum error mapping, RFC 9457 distinction, OWASP information exposure criteria, and reproduction steps.
