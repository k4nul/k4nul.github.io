---
layout: single
title: "Rust Service 09. Adding SQLite or PostgreSQL storage"
description: "Explains where SQLx pools, transactions, and queries fit when adding SQLite or PostgreSQL storage."
date: 2026-11-17 09:00:00 +09:00
lang: en
translation_key: rust-api-sqlx-database-storage
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
permalink: /en/rust/rust-api-sqlx-database-storage/
---

## Summary

A database connection is not created fresh in every handler. The pool is shared application state.

Start by placing the SQLx pool in Axum state. Keep handlers focused on request and response boundaries, put database access in small functions, and introduce transactions only when multiple changes must succeed or fail together.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Handling validation and bad requests
- Next post: Building SQLx migrations and query checks
- Expansion criteria: before publication, choose either SQLite or PostgreSQL as the runnable sample path and record command output plus failure logs.

## Document Information

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial and design note
- Test environment: no direct execution result is included in this post yet. The code below is a structure example, not a recorded test log.
- Checked versions: SQLx 0.8.6 documentation, Axum 0.8.9 documentation
- Evidence level: official documentation, original project documentation

## Problem Statement

After input validation, the next boundary is storage. If database code is added without a simple rule, the service quickly drifts:

- handlers start mixing SQL strings with response formatting,
- the app may create connections per request,
- database errors may leak directly into public responses,
- single-query flows and transactional flows become hard to distinguish.

This post defines the first SQLx structure: pool ownership, state extraction, query placement, and error mapping. Migration details are covered in the next post.

## Verified Facts

- SQLx 0.8.6 describes SQLx as an async SQL toolkit for Rust.
- SQLx 0.8.6 documents Tokio and async-std runtime support through features such as `runtime-tokio` and `runtime-async-std`.
- SQLx 0.8.6 exposes PostgreSQL, MySQL, and SQLite driver modules and pool aliases such as `PgPool` and `SqlitePool`.
- SQLx `Pool` is an asynchronous pool of database connections.
- Axum 0.8.9 documents `Router::with_state` for providing application state and `State<T>` for extracting it in handlers. Its state example explicitly mentions configuration and database connection pools as state candidates.
- Axum documents that `State` is an extractor and should be placed before body extractors.

## Design Rule

Keep the first structure small.

| Decision | Rule |
| --- | --- |
| Pool creation | Create it once during application startup. |
| Pool sharing | Put it in `AppState` and provide it with `Router::with_state`. |
| Handler responsibility | Extract request data, call validation and storage functions, convert the result to a response. |
| Query placement | Keep SQL in small storage functions outside the handler. |
| Transactions | Use them only when multiple queries must commit or roll back together. |
| Public errors | Do not expose raw SQLx error strings in API responses. |

## Dependency Example

SQLite is convenient for the first local reproduction path.

```toml
[dependencies]
axum = "0.8"
serde = { version = "1", features = ["derive"] }
sqlx = { version = "0.8", features = ["runtime-tokio", "sqlite"] }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

When switching to PostgreSQL, enable `postgres` instead of `sqlite`. If the database connection needs TLS, check SQLx's documented TLS features such as `tls-rustls` and `tls-native-tls` for the target environment.

## AppState Example

This example only shows the pool-sharing structure. A real application still needs configuration loading, migration execution, and an `ApiError` response implementation.

```rust
use axum::{
    extract::State,
    routing::{get, post},
    Json, Router,
};
use serde::Serialize;
use sqlx::{sqlite::SqlitePoolOptions, SqlitePool};
use std::time::Duration;

#[derive(Clone)]
struct AppState {
    db: SqlitePool,
}

#[derive(Serialize)]
struct HealthResponse {
    status: &'static str,
}

async fn build_state(database_url: &str) -> Result<AppState, sqlx::Error> {
    let db = SqlitePoolOptions::new()
        .max_connections(5)
        .acquire_timeout(Duration::from_secs(3))
        .connect(database_url)
        .await?;

    Ok(AppState { db })
}

fn build_router(state: AppState) -> Router {
    Router::new()
        .route("/health/db", get(db_health))
        .route("/users", post(create_user))
        .with_state(state)
}

async fn db_health(State(state): State<AppState>) -> Result<Json<HealthResponse>, ApiError> {
    sqlx::query("select 1")
        .execute(&state.db)
        .await
        .map_err(ApiError::database)?;

    Ok(Json(HealthResponse { status: "ok" }))
}
```

Here, `ApiError::database` represents the public error mapping introduced in the previous error-response post. Internal logs can keep the SQLx error detail, but the public response should expose a stable code such as `database_unavailable`.

## Storage Function Example

If handlers hold too much SQL, transport logic and storage logic become tangled. Start with small functions that receive a pool reference.

```rust
use sqlx::SqlitePool;

struct UserRecord {
    id: i64,
    email: String,
    display_name: String,
}

async fn find_user_by_id(
    pool: &SqlitePool,
    user_id: i64,
) -> Result<Option<UserRecord>, sqlx::Error> {
    let row = sqlx::query_as!(
        UserRecord,
        r#"
        select id, email, display_name
        from users
        where id = ?
        "#,
        user_id
    )
    .fetch_optional(pool)
    .await?;

    Ok(row)
}
```

This connects directly to the next post. SQLx query macros need a database schema at build time through `DATABASE_URL`, or saved metadata in `.sqlx`, so migrations and CI checks have to be designed together.

## Local Reproduction Plan

This post does not yet include executed output. Before publication, record the result of a run like this:

```powershell
$env:DATABASE_URL = "sqlite::memory:"
cargo check
cargo test
cargo run
curl.exe -i http://127.0.0.1:3000/health/db
```

Expected checks:

- pool creation fails early if the database URL is invalid,
- `/health/db` detects actual query failure,
- SQLx errors are not leaked in public responses,
- connection count, timeout, and database URL are environment-specific configuration.

## Verification Checklist

- Is the branch `master` before editing?
- Is `DATABASE_URL` kept in configuration or secrets?
- Are handlers kept separate from detailed SQL implementation?
- Is the pool created once, not per request?
- Are database errors mapped to stable public API errors?
- If query macros are used, is there a migration plus `.sqlx` or `DATABASE_URL` verification flow?

## Interpretation

Once a database is attached, the API is no longer just a process. It is a service with external state. The main design problem is ownership, not SQL syntax.

Let the application own the pool, let handlers borrow state, and let storage functions wrap data access in small units. That shape makes the later migration, test, Docker, and Kubernetes steps much easier to add without rewriting the service.

## Limitations

- This post uses SQLite examples to explain structure. PostgreSQL changes the connection URL, TLS choice, permissions, and migration environment.
- SQLx feature combinations depend on the selected database and runtime.
- Query macro correctness can only be checked against a migrated database or saved `.sqlx` metadata.
- Pool size and timeout values are examples, not production recommendations.

## References

- [SQLx crate documentation 0.8.6](https://docs.rs/sqlx/0.8.6/sqlx/)
- [SQLx Pool](https://docs.rs/sqlx/0.8.6/sqlx/struct.Pool.html)
- [SQLx query macro](https://docs.rs/sqlx/0.8.6/sqlx/macro.query.html)
- [Axum State extractor](https://docs.rs/axum/0.8.9/axum/extract/struct.State.html)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Added SQLx pool, Axum state, storage function, and reproduction-plan boundaries using checked official documentation.
