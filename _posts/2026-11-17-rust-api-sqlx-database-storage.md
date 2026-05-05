---
layout: single
title: "Rust Service 09. SQLite 또는 PostgreSQL 붙이기"
description: "Rust API에 SQLx 기반 데이터 저장소를 붙일 때 pool, transaction, query 위치를 어떻게 잡을지 정리한다."
date: 2026-11-17 09:00:00 +09:00
lang: ko
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
---

## 요약

데이터베이스 연결은 handler마다 새로 만드는 객체가 아니라 애플리케이션 상태로 공유되는 자원이다.

처음에는 SQLx pool을 Axum state에 넣고, handler는 요청/응답 경계에 집중시키며, 데이터베이스 쿼리는 작고 명확한 함수로 분리한다. transaction은 여러 변경을 하나의 원자적 작업으로 묶어야 할 때만 명시적으로 사용한다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: 입력 검증과 잘못된 요청 처리하기
- 다음 글: SQLx migration과 쿼리 검증 흐름 만들기
- 보강 기준: 실제 발행 전 예제 저장소에 SQLite와 PostgreSQL 중 하나를 먼저 고정하고, 실행 결과와 실패 로그를 함께 기록한다.

## 문서 정보

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial / 설계 기준
- 테스트 환경: 직접 실행 테스트 없음. 아래 코드는 저장소 구조를 잡기 위한 예시이며, 실제 실행 로그가 아니다.
- 확인한 버전: SQLx 0.8.6 문서, Axum 0.8.9 문서
- 출처 성격: 공식 문서, 원 프로젝트 문서

## 문제 정의

입력 검증이 끝나면 다음 경계는 저장소다. 이 시점에서 아무 기준 없이 데이터베이스 코드를 붙이면 다음 문제가 빠르게 생긴다.

- handler 안에 SQL 문자열과 응답 조립이 섞인다.
- 요청마다 connection을 새로 만들게 된다.
- 데이터베이스 오류가 그대로 외부 응답으로 새어 나간다.
- transaction이 필요한 흐름과 단일 query 흐름이 구분되지 않는다.

이번 글의 목표는 SQLx를 붙이는 첫 구조를 정하는 것이다. 이 글에서는 migration의 세부 흐름보다 pool, state, query 위치, 오류 매핑을 다룬다.

## 확인한 사실

- SQLx 0.8.6 문서는 SQLx를 Rust용 async SQL toolkit으로 설명한다.
- SQLx 0.8.6은 Tokio와 async-std 런타임을 지원하며, `runtime-tokio`와 `runtime-async-std` feature를 문서화한다.
- SQLx 0.8.6 문서에는 PostgreSQL, MySQL, SQLite driver module과 `PgPool`, `SqlitePool` 같은 pool type alias가 있다.
- SQLx의 `Pool`은 비동기 데이터베이스 connection pool이다.
- Axum 0.8.9의 `State` 문서는 `Router::with_state`로 애플리케이션 상태를 제공하고 handler에서 `State<T>`로 추출하는 흐름을 설명한다. 예시 설명에는 configuration과 database connection pool을 state에 넣을 수 있다고 되어 있다.
- Axum 문서는 `State`가 extractor이므로 body extractor보다 앞에 두라고 설명한다.

## 설계 기준

처음 구조는 작게 시작한다.

| 결정 | 기준 |
| --- | --- |
| pool 생성 위치 | 애플리케이션 시작 시 한 번 생성한다. |
| pool 전달 방식 | `AppState`에 넣고 `Router::with_state`로 공유한다. |
| handler 책임 | 요청 추출, validation 호출, 서비스 또는 저장소 함수 호출, 응답 변환에 집중한다. |
| query 위치 | handler 밖의 저장소 함수로 둔다. |
| transaction | 여러 query가 함께 성공하거나 함께 실패해야 할 때만 명시한다. |
| 외부 오류 응답 | SQLx 내부 오류 문자열을 그대로 노출하지 않는다. |

## 의존성 예시

SQLite로 먼저 흐름을 고정하면 로컬 재현이 쉽다.

```toml
[dependencies]
axum = "0.8"
serde = { version = "1", features = ["derive"] }
sqlx = { version = "0.8", features = ["runtime-tokio", "sqlite"] }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

PostgreSQL로 전환할 때는 `sqlite` 대신 `postgres`를 켜고, 네트워크 TLS가 필요한 환경에서는 SQLx 문서의 `tls-rustls` 또는 `tls-native-tls` feature 선택을 별도로 확인한다.

## AppState 예시

아래 예시는 pool을 state로 전달하는 구조만 보여준다. 실제 애플리케이션에서는 설정 로딩, migration 실행, 에러 응답 구현을 함께 연결해야 한다.

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

여기서 `ApiError::database`는 이전 오류 응답 글에서 만든 공개 오류 형식으로 변환하는 함수라고 가정한다. 내부 로그에는 SQLx 오류를 남기더라도, 외부 응답에는 `database_unavailable` 같은 안정적인 코드만 내보내는 편이 운영에 적합하다.

## 저장소 함수 예시

handler가 SQL을 직접 많이 들고 있으면 응답 경계와 저장소 경계가 섞인다. 처음에는 trait 추상화까지 만들 필요 없이, pool을 받는 작은 함수부터 시작해도 충분하다.

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

이 예시는 다음 글의 `query!` / `query_as!` 검증 흐름과 이어진다. SQLx query macro는 빌드 시점에 데이터베이스 스키마 또는 `.sqlx` metadata가 필요하므로, migration과 CI 흐름을 함께 설계해야 한다.

## 로컬 재현 계획

아직 이 글에서는 실행 결과를 기록하지 않았다. 실제 발행 전에는 다음 순서로 결과를 남긴다.

```powershell
$env:DATABASE_URL = "sqlite::memory:"
cargo check
cargo test
cargo run
curl.exe -i http://127.0.0.1:3000/health/db
```

확인할 결과:

- 애플리케이션 시작 시 pool 생성 실패가 즉시 드러나는가?
- `/health/db`가 실제 query 실패를 감지하는가?
- SQLx 오류가 공개 응답에 그대로 노출되지 않는가?
- 연결 수, timeout, database URL이 환경별 설정으로 분리되어 있는가?

## 검증 체크리스트

- branch가 `master`인지 확인했는가?
- `DATABASE_URL`은 설정 또는 secret으로 분리되어 있는가?
- handler가 요청/응답 경계와 SQL 세부 구현을 동시에 들고 있지 않은가?
- pool은 요청마다 생성되지 않는가?
- database 오류가 공개 응답에 그대로 노출되지 않는가?
- query macro를 쓴다면 migration과 `.sqlx` 또는 `DATABASE_URL` 기반 검증 흐름이 있는가?

## 해석 / 의견

데이터베이스를 붙이는 순간 API는 단순한 프로세스가 아니라 외부 상태를 가진 서비스가 된다. 그래서 이 글의 핵심은 SQL 문법보다 소유권 경계다.

pool은 애플리케이션이 소유하고, handler는 필요한 state를 빌려 쓰며, 저장소 함수는 데이터 접근을 작게 감싼다. 이 정도 구조만 있어도 뒤의 migration, 테스트, Docker, Kubernetes 설정을 훨씬 덜 흔들면서 붙일 수 있다.

## 한계와 예외

- 이 글은 SQLite 예시를 중심으로 구조를 설명한다. PostgreSQL에서는 연결 URL, TLS, 계정 권한, migration 환경이 달라진다.
- SQLx feature 조합은 선택한 데이터베이스와 런타임에 따라 달라진다.
- query macro가 실제로 통과하는지는 migration이 적용된 데이터베이스 또는 `.sqlx` metadata가 있어야 확인할 수 있다.
- pool 크기와 timeout 값은 예시이며, 실제 운영값은 DB 서버 제한과 트래픽 특성을 기준으로 잡아야 한다.

## 참고자료

- [SQLx crate documentation 0.8.6](https://docs.rs/sqlx/0.8.6/sqlx/)
- [SQLx Pool](https://docs.rs/sqlx/0.8.6/sqlx/struct.Pool.html)
- [SQLx query macro](https://docs.rs/sqlx/0.8.6/sqlx/macro.query.html)
- [Axum State extractor](https://docs.rs/axum/0.8.9/axum/extract/struct.State.html)

## 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: SQLx pool, Axum state, 저장소 함수, 로컬 재현 계획을 분리하고 공식 문서 기준으로 검증 사실을 보강.
