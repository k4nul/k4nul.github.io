---
layout: single
title: "Rust Service 08. Handling validation and bad requests"
description: "Separates JSON parse failures, field validation failures, and size-limit failures into clear 4xx API responses."
date: 2026-11-10 09:00:00 +09:00
lang: en
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
permalink: /en/rust/rust-api-input-validation-bad-requests/
---

## Summary

Validation is not a pile of temporary `if` statements inside handlers. It is the first boundary that protects the public API contract.

For an Axum API, it helps to separate four failure classes: request body size, JSON syntax, DTO deserialization, and field or business-rule validation. They are all client-side failures, but they are not the same failure.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Writing structured logs with tracing
- Next post: Adding SQLite or PostgreSQL storage
- Expansion criteria: before publication, connect this example to the repository, record executed command output, and pin the exact crate versions used in the final sample.

## Document Information

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial and boundary design note
- Test environment: no direct execution result is included in this post yet. The code below is a reviewable flow example, not a recorded benchmark or test log.
- Checked versions: Axum 0.8.9 documentation, OWASP Input Validation Cheat Sheet as available on the verification date.
- Evidence level: official documentation, original project documentation

## Problem Statement

When validation is handled ad hoc, the API starts returning different shapes for similar mistakes. One malformed JSON body might return an Axum default body, another missing field might return a custom error object, and a too-large request might look like an internal failure.

The goal of this post is to define a repeatable boundary:

- parsing failures are mapped before business logic runs,
- field validation is explicit and predictable,
- public responses are stable,
- logs can keep diagnostic detail without leaking request bodies or personal data.

## Verified Facts

- Axum's `Json` extractor deserializes request bodies into types that implement `DeserializeOwned`.
- Axum documents that `Json` can fail because the content type is not JSON, the body is not syntactically valid JSON, the body cannot be deserialized into the target type, or buffering the body fails.
- Because JSON parsing consumes the request body, Axum documents that `Json` must be the last extractor when a handler has multiple extractors.
- Axum exposes `JsonRejection` variants such as `MissingJsonContentType`, `JsonSyntaxError`, `JsonDataError`, and `BytesRejection`. The enum is non-exhaustive, so matching code needs a fallback arm.
- Axum's `DefaultBodyLimit` applies a default 2 MB limit to `Bytes` and extractors built on it, including `String`, `Json`, and `Form`. `DefaultBodyLimit::max` can change that limit for a route or router.
- OWASP recommends validating input as early as possible, applying both syntactic and semantic validation, and preferring allowlist validation over denylist validation.

## Boundary Design

Use separate names for separate failures:

| Failure class | Public code | HTTP status | Example |
| --- | --- | --- | --- |
| Request body too large | `payload_too_large` | `413 Payload Too Large` | JSON body exceeds the configured body limit. |
| Missing or wrong content type | `unsupported_media_type` | `415 Unsupported Media Type` | `Content-Type` is not compatible with JSON. |
| Invalid JSON syntax | `invalid_json` | `400 Bad Request` | Body is `{ "email":` and cannot be parsed. |
| JSON does not fit the DTO | `invalid_request` | `400 Bad Request` | Required field is missing or has the wrong type. |
| Field or business-rule validation failed | `validation_failed` | `422 Unprocessable Entity` | `displayName` is empty after trimming. |

This split is intentionally boring. The client can react to stable codes, and the server can still log more specific internal detail.

## DTO Example

This example keeps transport shape separate from validation logic. `deny_unknown_fields` is a policy choice: it makes the public request contract stricter, so use it only when rejecting unknown fields is acceptable for your API.

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
    UnsupportedMediaType(&'static str),
    PayloadTooLarge(&'static str),
    Validation(Vec<FieldError>),
}

fn validate_create_user(input: &CreateUserRequest) -> Result<(), Vec<FieldError>> {
    let mut errors = Vec::new();

    if !input.email.contains('@') {
        errors.push(FieldError {
            field: "email",
            code: "invalid_email",
        });
    }

    if input.display_name.trim().is_empty() {
        errors.push(FieldError {
            field: "displayName",
            code: "required",
        });
    }

    if errors.is_empty() {
        Ok(())
    } else {
        Err(errors)
    }
}
```

The final application should implement `IntoResponse` for `ApiError` in the same error-response format introduced in the previous post.

## Axum Rejection Mapping

Wrapping the extractor in `Result<Json<T>, JsonRejection>` lets the handler choose a public error code instead of returning Axum's default rejection body.

```rust
fn map_json_rejection(rejection: JsonRejection) -> ApiError {
    match rejection {
        JsonRejection::MissingJsonContentType(_) => {
            ApiError::UnsupportedMediaType("unsupported_media_type")
        }
        JsonRejection::JsonSyntaxError(_) => ApiError::BadRequest("invalid_json"),
        JsonRejection::JsonDataError(_) => ApiError::BadRequest("invalid_request"),
        JsonRejection::BytesRejection(_) => ApiError::PayloadTooLarge("payload_too_large"),
        _ => ApiError::BadRequest("invalid_request"),
    }
}

async fn create_user(
    payload: Result<Json<CreateUserRequest>, JsonRejection>,
) -> Result<StatusCode, ApiError> {
    let Json(payload) = payload.map_err(map_json_rejection)?;

    validate_create_user(&payload).map_err(ApiError::Validation)?;

    Ok(StatusCode::CREATED)
}

fn build_router() -> Router {
    Router::new()
        .route("/users", post(create_user))
        .layer(DefaultBodyLimit::max(16 * 1024))
}
```

The `BytesRejection` branch can represent body buffering failures, not only size-limit failures. In production code, log the internal rejection kind and map the public response conservatively.

## Reproduction Plan

The following commands are the intended local checks once this example is connected to a repository.

```powershell
cargo test
cargo run
```

```powershell
curl.exe -i -X POST http://127.0.0.1:3000/users `
  -H "Content-Type: application/json" `
  --data "{"

curl.exe -i -X POST http://127.0.0.1:3000/users `
  -H "Content-Type: application/json" `
  --data "{\"email\":\"not-an-email\",\"displayName\":\"\"}"

curl.exe -i -X POST http://127.0.0.1:3000/users `
  -H "Content-Type: text/plain" `
  --data "hello"
```

Expected checks:

- malformed JSON returns the `invalid_json` response shape,
- valid JSON with invalid fields returns `validation_failed`,
- wrong content type returns `unsupported_media_type`,
- no raw request body or personal data appears in logs.

## Observation Status

No command output is reproduced here yet. Before publication, this section should include actual `curl.exe -i` responses and a note about the tested Rust, Axum, and Tokio versions.

## Verification Checklist

- Does the public error response shape match the previous error-response post?
- Are parser errors, DTO shape errors, and field validation errors distinguishable?
- Is the body limit explicit for routes that accept request bodies?
- Does every `JsonRejection` match include a wildcard arm for future Axum variants?
- Are request bodies, secrets, and personal data excluded from logs?
- Do tests include malformed JSON, wrong content type, missing fields, unknown fields if denied, and boundary-length cases?

## Interpretation

Validation is easiest to maintain when each layer has a narrow job. Axum extractors can reject malformed transport input. DTO deserialization can enforce basic shape. Validation functions can enforce API-level rules. Service code can enforce rules that require database state or other dependencies.

That separation also improves operations. A spike in `invalid_json` means something different from a spike in `validation_failed`, and neither should be mixed with internal database or dependency failures.

## Limitations

- This post does not prescribe a validation crate. A later implementation may use a crate if it reduces repeated field checks without hiding the public error contract.
- Email validation in the example is intentionally minimal and should not be treated as a complete email-deliverability policy.
- `422 Unprocessable Entity` is a common API choice for semantic validation failures, but an organization may standardize on `400 Bad Request`. The important point is consistency.
- The example is not an executed test log yet.

## References

- [Axum Json extractor](https://docs.rs/axum/0.8.9/axum/struct.Json.html)
- [Axum JsonRejection](https://docs.rs/axum/0.8.9/axum/extract/rejection/enum.JsonRejection.html)
- [Axum DefaultBodyLimit](https://docs.rs/axum/0.8.9/axum/extract/struct.DefaultBodyLimit.html)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Separated parser, DTO, validation, and body-limit failures; pinned checked documentation versions and added reproduction plan.
