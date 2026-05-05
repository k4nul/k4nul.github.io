---
layout: single
title: "Rust Service 10. Building SQLx migrations and query checks"
description: "Uses SQLx migrations, query macros, and prepare flow to validate database and code changes together."
date: 2026-11-24 09:00:00 +09:00
lang: en
translation_key: rust-api-sqlx-migrations-query-checks
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
permalink: /en/rust/rust-api-sqlx-migrations-query-checks/
---

## Summary

Schema change is not a note separate from code. It is a contract that should be checked in build and test flow.

With SQLx, migrations, `query!` family macros, and `cargo sqlx prepare` should be designed together. That gives CI a clear way to detect when database schema and Rust code drift apart.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Adding SQLite or PostgreSQL storage
- Next post: Choosing repository and service boundaries
- Expansion criteria: before publication, record one successful migration/query-check flow and one intentional failure from the same example repository.

## Document Information

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial and verification-flow design
- Test environment: no direct execution result is included in this post yet. Commands below are a reproduction plan, not a recorded test log.
- Checked versions: SQLx 0.8.6 documentation, SQLx CLI README
- Evidence level: official documentation, original project documentation

## Problem Statement

The database schema lives outside Rust source files, but it strongly determines API behavior. If `users.email` is renamed while Rust queries still expect it, the project should fail somewhere before production.

This post connects three things:

- migration files record schema changes,
- query macros check what Rust code expects from the schema,
- `cargo sqlx prepare --check` gives CI a way to detect stale query metadata.

## Verified Facts

- SQLx 0.8.6 documents `migrate!` as a macro that embeds migrations into the binary and expands to a static `Migrator`.
- `sqlx::migrate!()` defaults to `./migrations`, and the directory is relative to the project root that contains `Cargo.toml`.
- SQLx 0.8.6 documents `query!` as a statically checked SQL query macro.
- SQLx `query!` documentation says `DATABASE_URL` must be set at build time to point to a database with the schema being checked, or `.sqlx` must exist at the workspace root.
- The SQLx CLI README documents `sqlx migrate add <name>`, `sqlx migrate run`, `sqlx migrate add -r <name>` for reversible migrations, `cargo sqlx prepare` for offline metadata, and `cargo sqlx prepare --check` for CI.
- The SQLx CLI README states that `prepare --check` exits nonzero when `.sqlx` data is out of date with the current schema or project queries.

## Basic Flow

With SQLite as the local example path, the flow looks like this:

```powershell
$env:DATABASE_URL = "sqlite://target/dev.db"
sqlx database create
sqlx migrate add create_users
sqlx migrate run
cargo check
cargo sqlx prepare
cargo sqlx prepare --check
```

The exact SQLite file URL behavior should be confirmed in the example repository before publication. The important point in this draft is the verification order.

## Migration Example

`sqlx migrate add create_users` creates a migration file. Put the schema change there.

```sql
create table users (
    id integer primary key,
    email text not null unique,
    display_name text not null,
    created_at text not null
);
```

Treat migrations that have already been applied in a shared environment as immutable by default. Add a new migration for a new change. Editing shared migration history can split local, CI, and production database states.

## App Startup Migration

Whether migrations run during app startup or as a separate deployment job is an operational decision. Either way, migration failure must be visible.

```rust
use sqlx::{migrate::Migrator, SqlitePool};

static MIGRATOR: Migrator = sqlx::migrate!();

async fn run_migrations(pool: &SqlitePool) -> Result<(), sqlx::Error> {
    MIGRATOR.run(pool).await
}
```

SQLx documents that stable Rust projects may need a build script to make Cargo rerun when the migrations directory changes and migrations are embedded into the binary.

```rust
fn main() {
    println!("cargo:rerun-if-changed=migrations");
}
```

## Query Macro Example

`query_as!` lets the build check the relationship between SQL text and Rust output types. That check depends on a migrated database or saved `.sqlx` metadata.

```rust
use sqlx::SqlitePool;

struct UserRecord {
    id: i64,
    email: String,
    display_name: String,
}

async fn find_user_by_email(
    pool: &SqlitePool,
    email: &str,
) -> Result<Option<UserRecord>, sqlx::Error> {
    sqlx::query_as!(
        UserRecord,
        r#"
        select id, email, display_name
        from users
        where email = ?
        "#,
        email
    )
    .fetch_optional(pool)
    .await
}
```

If a migration removes `display_name` while Rust still selects it, the query macro check should fail before deployment. That is the practical purpose of this flow.

## CI Verification Rule

Pick one primary strategy.

| Strategy | Rule |
| --- | --- |
| Live database check | Start a database in CI, apply migrations, then run `cargo check`. |
| Offline metadata check | Developers refresh `.sqlx` with `cargo sqlx prepare`, and CI runs `cargo sqlx prepare --check`. |

The strategies can be combined, but the failure owner should be documented. If `.sqlx` is used, query changes and migration changes must update `.sqlx` together.

## Rollback Rule

Rollback is not just a `sqlx migrate revert` command. Decide these points before production:

- Was the migration created as reversible?
- Can the down migration run without losing required data?
- Is the previously deployed application version compatible with the previous schema?
- Is there a backup or point-in-time recovery strategy?
- Which log or runbook confirms rollback success or failure?

Column deletion, type narrowing, and data rewrite migrations are often difficult to reverse. For those, use a staged expand-contract approach where possible.

## Observation Status

No executed output is included yet. Before publication, record at least one intentional failure:

- query macro failure when migrations are not applied,
- `cargo sqlx prepare --check` failure when `.sqlx` is stale,
- a reversible migration whose down path is actually tested.

## Verification Checklist

- Are migration files committed to version control?
- Did the change add a new migration instead of editing shared migration history?
- Are query macros checked after migrations are applied?
- Does CI run either `cargo sqlx prepare --check` or a live-database `cargo check` path?
- If `.sqlx` is used, was it refreshed with the query change?
- Does the rollback plan cover data recovery, not only a command name?

## Interpretation

SQLx's value is not hiding SQL. Its value is letting the project keep explicit SQL while finding schema drift earlier.

That makes a migration post a CI design post as well. A schema change should not live only in someone's memory. It should be represented by files, commands, and failure conditions.

## Limitations

- This post assumes the SQLx CLI is installed. Installation features depend on the selected database and TLS policy.
- SQLite and PostgreSQL differ in placeholders, type mapping, connection configuration, and migration operations.
- Startup migrations and deployment-job migrations have different operational tradeoffs.
- Rollback safety is determined by migration content and data recovery strategy, not the tool alone.

## References

- [SQLx migrate macro 0.8.6](https://docs.rs/sqlx/0.8.6/sqlx/macro.migrate.html)
- [SQLx query macro 0.8.6](https://docs.rs/sqlx/0.8.6/sqlx/macro.query.html)
- [SQLx CLI README](https://github.com/launchbadge/sqlx/blob/main/sqlx-cli/README.md)
- [Cargo build scripts](https://doc.rust-lang.org/cargo/reference/build-scripts.html)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Added SQLx migration, query macro, prepare/check, and rollback criteria based on official documentation.
