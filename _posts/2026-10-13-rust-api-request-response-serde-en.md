---
layout: single
title: "Rust Service 04. Designing request and response types with serde"
description: "Separates request DTOs, response DTOs, and internal domain types while defining where serde belongs."
date: 2026-10-13 09:00:00 +09:00
lang: en
translation_key: rust-api-request-response-serde
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
permalink: /en/rust/rust-api-request-response-serde/
---

## Summary

API types are external contracts. Returning internal structs as JSON couples field names, optionality, enum representation, and hidden internal values to implementation changes.

Design request types around `Deserialize`, response types around `Serialize`, and keep domain types as free from HTTP/JSON representation as practical. Separate request, response, and domain types early, while keeping conversion code small for the first CRUD flows.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Structuring a Rust Axum API project
- Next post: Making API error responses consistent
- Expansion criteria: before publication, add the example repository, commands, tool versions, and failure logs that fit this post's scope.

## Document Info / Environment

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial
- Test environment: No direct execution test. The code below is a design target to verify in the example repository with `cargo test` and HTTP requests before publication.
- Tested versions: No runtime versions pinned. On the verification date, this was checked against the official Serde documentation and Axum `0.8.9` `Json` documentation.
- Evidence level: official documentation, original project documentation

## Problem Statement

Once the minimal API exchanges JSON, the type boundary matters. The payload a client sends, the internal model the server stores or computes, and the response returned to the client may look similar, but they do not have the same responsibility.

This post covers request and response type design with serde. The goal is not to attach serde to every struct by habit. The goal is to attach serialization only where an external JSON contract exists.

## Verified Facts

- Serde documentation says `#[derive(Serialize, Deserialize)]` generates `Serialize` and `Deserialize` implementations for data structures defined in your crate. Evidence: [Serde: Using derive](https://serde.rs/derive.html)
- Serde container attributes document `rename_all` as a way to rename struct fields or enum variants according to a case convention. If the JSON contract is camelCase, it should be explicit on DTOs. Evidence: [Serde: Container attributes](https://serde.rs/container-attrs.html)
- Serde container attributes document `deny_unknown_fields` as an option that errors during deserialization when unknown fields are present. This can reduce forward compatibility, so it should be a deliberate public API decision. Evidence: [Serde: Container attributes](https://serde.rs/container-attrs.html)
- Axum `Json` documentation says that as an extractor it deserializes request bodies into `DeserializeOwned` types, and as a response it creates JSON responses. It also notes that `Json` consumes the request body and must be last when multiple extractors are used. Evidence: [Axum Json](https://docs.rs/axum/0.8.9/axum/struct.Json.html)
- The `Request`, `Response`, and `Domain` split in this post is not an official standard. It is this series' design rule for keeping API contracts stable.

## Reproduction Steps

There is no direct execution result yet. Before publication, add request, response, and domain types to the minimal API example and record `cargo test` plus HTTP request results.

```powershell
cargo add serde --features derive
cargo add serde_json
```

Split types by responsibility.

```rust
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
struct CreateUserRequest {
    email: String,
    display_name: String,
}

struct User {
    id: String,
    email: String,
    display_name: String,
    password_hash: String,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct UserResponse {
    id: String,
    email: String,
    display_name: String,
}

impl From<User> for UserResponse {
    fn from(user: User) -> Self {
        Self {
            id: user.id,
            email: user.email,
            display_name: user.display_name,
        }
    }
}
```

Handlers should receive and return the JSON contract types.

```rust
use axum::Json;

async fn create_user(Json(input): Json<CreateUserRequest>) -> Json<UserResponse> {
    let user = User {
        id: "user_1".to_string(),
        email: input.email,
        display_name: input.display_name,
        password_hash: "not-returned".to_string(),
    };

    Json(UserResponse::from(user))
}
```

## Observations

- This document currently contains no actual `cargo test`, `cargo run`, or `curl.exe` output.
- The success condition is that response JSON does not contain an internal field such as `passwordHash` or `password_hash`.
- Failure notes should separate unknown field handling, missing required fields, JSON syntax errors, and accidental domain field exposure.

## Verification Checklist

- Does the request DTO contain only fields accepted from external input?
- Does the response DTO contain only fields safe to return to clients?
- Is the domain type kept away from unnecessary serde attributes and HTTP representation?
- Is the JSON naming policy, such as `rename_all`, explicit on DTOs?
- If `deny_unknown_fields` is used, is the compatibility tradeoff explained?
- Are actual `cargo test` and HTTP request/response results recorded?

## Interpretation

Separating request and response types adds a little code. In an operated API, that small duplication is cheap insurance. You can change an internal field without breaking the response contract, and you reduce the chance of leaking sensitive values into JSON.

That does not mean every type needs three copies. Values used only in tests or inside the domain can stay simple. Start the split at the HTTP boundary where the contract is visible to clients.

## Limitations

- This post does not yet include executed command output.
- DTO separation can look verbose in very small examples.
- `deny_unknown_fields` can help strict input validation, but it can reduce compatibility in some client extension scenarios.
- Dates, times, decimal values, and enum representations need separate design and are not covered deeply here.
- Before publication, add an example repository, commands, versions, and failure logs.

## References

- [Serde documentation](https://serde.rs/)
- [Serde: Using derive](https://serde.rs/derive.html)
- [Serde: Container attributes](https://serde.rs/container-attrs.html)
- [Axum Json extractor and response](https://docs.rs/axum/0.8.9/axum/struct.Json.html)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Separated Serde derive evidence, JSON DTO boundaries, reproduction steps, and compatibility limitations.
