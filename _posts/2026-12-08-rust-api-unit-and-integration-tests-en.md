---
layout: single
title: "Rust Service 12. Separating unit and integration tests for an API"
description: "Separates pure logic tests, handler tests, and database-backed integration tests in a Rust API."
date: 2026-12-08 09:00:00 +09:00
lang: en
translation_key: rust-api-unit-and-integration-tests
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
permalink: /en/rust/rust-api-unit-and-integration-tests/
---

## Summary

If every test boots the whole server, the suite is slow. If every test only checks pure functions, real boundaries disappear.

Use unit tests for pure logic, integration tests for routes and response contracts, and separate database tests for migration-backed flows. The point is not the label. The point is making the broken boundary obvious when a test fails.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Choosing repository and service boundaries
- Next post: Understanding session and JWT boundaries before auth
- Expansion criteria: before publication, record executed output for `cargo test`, handler tests, and database integration tests from the example repository.

## Document Information

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial and test strategy
- Test environment: no direct execution result is included in this post yet. The code below explains test structure, not recorded output.
- Checked versions: Rust Book, Cargo Book, Tokio 1.48.0 documentation, Tower 0.5.3 documentation, Axum 0.8.9 documentation
- Evidence level: official documentation, original project documentation

## Problem Statement

If every API test is called an integration test, the suite gets slow and blurry. If the project only has unit tests, JSON parsing, routing, status codes, and migration-backed SQL can still break.

This post separates tests by the boundary they protect:

- Did a pure rule break?
- Did the HTTP contract break?
- Did a database and migration-backed flow break?

## Verified Facts

- The Rust Book describes unit tests as small, focused tests that exercise one module in isolation, and integration tests as tests external to the library that use its public interface and can exercise multiple modules.
- The Rust Book describes the convention of putting unit tests beside code in `src` with a `#[cfg(test)]` module.
- The Rust Book explains that each file in the top-level `tests` directory is compiled as a separate crate.
- The Cargo Book explains that default `cargo test` target selection builds and runs unit tests, integration tests, and doc tests among other targets.
- Tokio 1.48.0 documents `#[tokio::test]` as a macro for marking async functions to run in a runtime, with a single-thread current-thread runtime by default.
- Tower `ServiceExt` provides `oneshot`, which is commonly used to call an Axum router as a service without opening a server socket.

## Test Matrix

| Test kind | Location | Checks | External dependency |
| --- | --- | --- | --- |
| unit test | `#[cfg(test)]` modules under `src/**` | domain and service rules | none or minimal |
| handler/route integration test | `tests/*.rs` | route, status, JSON response contract | test state |
| DB integration test | `tests/*.rs` or a feature-gated target | migrations, SQLx queries, transactions | test database |

Make fast unit and HTTP contract tests the default. Add database tests once fixture management is explicit.

## Unit Test Example

Pure validation or service rules should be testable without HTTP.

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rejects_empty_display_name() {
        let input = CreateUserInput {
            email: "user@example.com".to_string(),
            display_name: "   ".to_string(),
        };

        let error = validate_create_user(&input).unwrap_err();

        assert!(error.iter().any(|e| e.field == "displayName"));
    }
}
```

If this fails, the domain rule failed. HTTP is not involved.

## Handler Test Example

Routes and response shapes can be checked without opening a server socket. The important design choice is exposing `build_router` from `lib.rs` or `app.rs` so tests can call it.

```rust
use axum::{
    body::Body,
    http::{Request, StatusCode},
};
use tower::ServiceExt;

#[tokio::test]
async fn create_user_rejects_invalid_json() {
    let app = build_router(test_state());

    let response = app
        .oneshot(
            Request::builder()
                .method("POST")
                .uri("/users")
                .header("content-type", "application/json")
                .body(Body::from("{"))
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::BAD_REQUEST);
}
```

This checks the handler, route, extractor rejection mapping, and public status code. It does not prove that migrations work.

## DB Integration Test Rule

Database tests can be slower, so define when they run.

```text
tests/
  users_http.rs
  users_db.rs
  common/
    mod.rs
```

Choose one fixture strategy.

| Strategy | Benefit | Watch point |
| --- | --- | --- |
| SQLite temporary database | fast local reproduction | may differ from PostgreSQL-specific SQL |
| PostgreSQL test container | closer to production DB | slower CI and more setup |
| transaction rollback | good isolation between tests | must not conflict with app-level transactions |

If the project uses SQLx query macros, pair DB tests with migration application and `cargo sqlx prepare --check`.

## Execution Plan

Before publication, record command output for this shape:

```powershell
cargo fmt --check
cargo test
cargo test --test users_http
cargo test --test users_db
cargo sqlx prepare --check
```

CI can separate fast and slow paths. For example, every pull request can run unit and handler tests, while database integration tests run on migration changes or in a scheduled job.

## Observation Status

No executed output is included yet. Before publication, record at least one intentional failure:

- a unit test failure after changing a validation rule,
- a handler test failure after changing the error response shape,
- a DB integration or SQLx prepare failure when a migration is missing.

## Verification Checklist

- Do pure rule tests run without HTTP?
- Do integration tests verify public routes and response shapes?
- Do database tests apply migrations before checking queries?
- Are shared helpers placed under `tests/common/mod.rs` instead of accidentally becoming separate empty test crates?
- Is `#[tokio::test]` used only where async runtime setup is needed?
- Does CI clearly separate fast tests from slower database tests?

## Interpretation

More tests are not automatically better. A useful test suite makes failure location clear. If validation checks always boot a real database and HTTP server, the suite becomes slow, and slow suites get run less often.

But pure tests alone are not enough either. API contracts break at routing and serialization boundaries. A durable test strategy lets unit tests, HTTP contract tests, and database integration tests protect different risks.

## Limitations

- This post does not compare test frameworks. It uses Rust's built-in test harness, Tokio async tests, and Tower/Axum service calls as the baseline.
- Database fixture strategy differs between SQLite and PostgreSQL.
- Whether to mock or use a real database depends on the test purpose and cost.
- The examples do not include executed output yet.

## References

- [Rust Book: Writing Automated Tests](https://doc.rust-lang.org/book/ch11-00-testing.html)
- [Rust Book: Test Organization](https://doc.rust-lang.org/book/ch11-03-test-organization.html)
- [Cargo Book: cargo test](https://doc.rust-lang.org/cargo/commands/cargo-test.html)
- [Tokio 1.48.0 test macro](https://docs.rs/tokio/1.48.0/tokio/attr.test.html)
- [Tower ServiceExt 0.5.3](https://docs.rs/tower/0.5.3/tower/trait.ServiceExt.html)
- [Axum 0.8.9 documentation](https://docs.rs/axum/0.8.9/axum/)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Added unit, handler, and DB integration test boundaries, execution plan, and failure-observation criteria using official documentation.
