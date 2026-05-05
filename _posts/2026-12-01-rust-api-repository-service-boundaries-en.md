---
layout: single
title: "Rust Service 11. Choosing repository and service boundaries"
description: "Decides when to split handlers, services, and repositories in a Rust API, and when that split is too much."
date: 2026-12-01 09:00:00 +09:00
lang: en
translation_key: rust-api-repository-service-boundaries
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
permalink: /en/rust/rust-api-repository-service-boundaries/
---

## Summary

Layers are not there to look sophisticated. They exist to separate reasons for change.

Start with thin handlers and repositories. Add a service layer when multiple handlers share the same business rule or when a transaction boundary appears. If a CRUD endpoint has no repeated rule yet, adding traits, mocks, services, and repositories up front can make the code heavier than the problem.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Building SQLx migrations and query checks
- Next post: Separating unit and integration tests for an API
- Expansion criteria: before publication, record the example repository's module tree, test locations, and one failure case.

## Document Information

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial and design note
- Test environment: no direct execution result is included in this post yet. The structure and code below are boundary examples, not a recorded test log.
- Checked versions: Rust Book, Axum 0.8.9 documentation, SQLx 0.8.6 documentation
- Evidence level: official documentation, original project documentation

## Problem Statement

Rust API projects usually drift in one of two directions:

- They split too late: JSON mapping, validation, SQL, transactions, and error mapping all end up inside handlers.
- They split too early: a rule that has not repeated once is wrapped in traits, services, repositories, and DTO conversion layers.

The goal is not to pick the one correct architecture name. The goal is to decide where each reason for change should live.

## Verified Facts

- The Rust Book says that as programs grow, grouping related functionality and separating distinct features clarifies where implementation lives and where changes should happen.
- The Rust Book describes the module system as a way to control public and private implementation details and scope.
- A Rust package can contain multiple binary crates and optionally one library crate.
- Axum connects HTTP requests to application code through `Router`, routes, extractors, and handlers.
- SQLx query macros can check the relationship between SQL and Rust types, but they do not express business rules for the application.

## Layer Responsibilities

A small starting rule is enough.

| Layer | Responsibility | Avoid |
| --- | --- | --- |
| handler | request extraction, public error mapping, response conversion | SQL detail, multi-step business rules |
| service | repository orchestration, transaction boundaries, business rules | direct dependency on HTTP headers or Axum extractors |
| repository | SQL execution, row and storage-record mapping | HTTP status decisions, public error-body construction |
| domain/model | pure values and rules | database connections, request bodies |

A service layer is not mandatory for every endpoint. If one handler calls one repository function and no separate rule exists, handler plus repository is a reasonable starting point.

## Starting Structure

Do not start with a grand architecture. Start with module names that reveal responsibility.

```text
src/
  main.rs
  lib.rs
  app.rs
  routes/
    mod.rs
    users.rs
  domain/
    mod.rs
    users.rs
  repositories/
    mod.rs
    users.rs
```

Keep `main.rs` as a thin entry point that reads configuration and starts the listener. Expose core app assembly from `lib.rs` or `app.rs` so integration tests can call `build_router`.

## Handler Example

The handler stays at the Axum boundary.

```rust
use axum::{extract::State, http::StatusCode, Json};

pub async fn create_user(
    State(state): State<AppState>,
    Json(request): Json<CreateUserRequest>,
) -> Result<(StatusCode, Json<UserResponse>), ApiError> {
    let input = request.try_into_domain().map_err(ApiError::validation)?;
    let user = services::users::create_user(&state.db, input)
        .await
        .map_err(ApiError::from_service)?;

    Ok((StatusCode::CREATED, Json(UserResponse::from(user))))
}
```

This handler knows request and response DTOs. It does not know SQL strings or transaction details.

## When Service Helps

Add a service layer after repetition or orchestration appears.

```rust
pub async fn create_user(
    db: &sqlx::SqlitePool,
    input: CreateUserInput,
) -> Result<User, CreateUserError> {
    if repositories::users::exists_by_email(db, &input.email).await? {
        return Err(CreateUserError::EmailAlreadyUsed);
    }

    repositories::users::insert(db, input).await
}
```

If this rule is shared by multiple handlers or needs a transaction, a service function is natural. If the endpoint is just a simple read, a service file may only add motion.

## Repository Example

The repository wraps the storage language.

```rust
pub async fn exists_by_email(
    db: &sqlx::SqlitePool,
    email: &str,
) -> Result<bool, sqlx::Error> {
    let row = sqlx::query!(
        r#"
        select exists(select 1 from users where email = ?) as "exists!: bool"
        "#,
        email
    )
    .fetch_one(db)
    .await?;

    Ok(row.exists)
}
```

The repository should not return `StatusCode::CONFLICT`. How an email conflict becomes a public response belongs to error mapping at the HTTP boundary.

## Reproduction Plan

When this is connected to the example repository, record these checks:

```powershell
cargo fmt --check
cargo test
cargo test users
```

Expected checks:

- unit tests verify domain and service rules without HTTP,
- integration tests verify public routes and response shape,
- repository or database integration tests run after migrations,
- handlers do not leak raw SQLx errors into public responses.

## Verification Checklist

- Is the added layer separating a real reason for change?
- Are handlers kept near the HTTP boundary?
- Are services independent from Axum extractors and HTTP status codes?
- Are repositories independent from public API response shapes?
- Was a trait added only when testing or replacement actually needs it?
- Is the transaction boundary placed in a service or another clear application flow?

## Interpretation

For a small Rust API, dependency direction matters more than layer count. The outer HTTP boundary can call inward to business rules and storage details, but inner code should not need to know Axum response shapes.

Layers can be added later. But if every concern starts inside handlers and tests accumulate around that shape, later separation becomes expensive. The useful middle ground is thin structure with visible reasons for change.

## Limitations

- This post assumes a single-service example. Large systems with multiple bounded contexts or crates need additional rules.
- Repository traits are not always necessary. Real-database integration tests can be simpler and more trustworthy.
- When SQLx query macros are used, compile-time query checks and migration state must be designed together.
- The examples are structural and do not include executed output yet.

## References

- [Rust Book: Packages, Crates, and Modules](https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html)
- [Axum 0.8.9 crate documentation](https://docs.rs/axum/0.8.9/axum/)
- [SQLx query macro 0.8.6](https://docs.rs/sqlx/0.8.6/sqlx/macro.query.html)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Added handler/service/repository responsibility boundaries, starting module structure, and reproduction plan based on official documentation.
