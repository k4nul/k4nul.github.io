---
layout: single
title: "Rust Service 10. SQLx migration과 쿼리 검증 흐름 만들기"
description: "SQLx migration, query macro, prepare 흐름을 사용해 데이터베이스 변경과 코드 변경을 함께 검증하는 기준을 만든다."
date: 2026-11-24 09:00:00 +09:00
lang: ko
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
---

## 요약

스키마 변경은 코드 변경과 분리된 메모가 아니라 빌드와 테스트에서 함께 확인되어야 하는 계약이다.

SQLx에서는 migration 파일, `query!` 계열 macro, `cargo sqlx prepare` 흐름을 함께 설계해야 한다. 그래야 데이터베이스 변경과 Rust 코드 변경이 서로 어긋나는 일을 CI에서 잡을 수 있다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: SQLite 또는 PostgreSQL 붙이기
- 다음 글: repository/service 계층을 어디까지 나눌지 정하기
- 보강 기준: 실제 발행 전 migration 생성, 적용, query 검증, 실패 사례를 같은 저장소에서 재현한 로그로 보강한다.

## 문서 정보

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial / 검증 흐름 설계
- 테스트 환경: 직접 실행 테스트 없음. 아래 명령은 재현 계획이며, 아직 실행 결과를 포함하지 않는다.
- 확인한 버전: SQLx 0.8.6 문서, SQLx CLI README
- 출처 성격: 공식 문서, 원 프로젝트 문서

## 문제 정의

데이터베이스 스키마는 코드 밖에 있지만, API 동작을 강하게 결정한다. `users.email` 컬럼 이름이 바뀌었는데 Rust query가 그대로라면 컴파일, 테스트, 배포 중 어딘가에서 실패해야 정상이다.

이번 글의 목표는 세 가지를 한 흐름으로 묶는 것이다.

- migration 파일은 스키마 변경의 기록이다.
- query macro는 Rust 코드가 기대하는 스키마를 확인하는 장치다.
- `cargo sqlx prepare --check`는 CI에서 query metadata가 최신인지 확인하는 장치다.

## 확인한 사실

- SQLx 0.8.6의 `migrate!` macro는 migration을 binary에 embed하고 `Migrator` static instance로 확장된다고 문서화되어 있다.
- `sqlx::migrate!()`의 기본 directory는 `./migrations`이며, directory는 `Cargo.toml`이 있는 project root 기준 상대 경로다.
- SQLx 0.8.6의 `query!` macro는 정적으로 검사되는 SQL query를 만든다.
- SQLx `query!` macro 문서는 build time에 `DATABASE_URL`이 스키마 확인 대상 데이터베이스를 가리키거나, workspace root에 `.sqlx`가 있어야 한다고 설명한다.
- SQLx CLI README는 `sqlx migrate add <name>`, `sqlx migrate run`, reversible migration을 위한 `sqlx migrate add -r <name>`, offline mode metadata 생성을 위한 `cargo sqlx prepare`, CI용 `cargo sqlx prepare --check` 흐름을 설명한다.
- SQLx CLI README는 `prepare --check`가 `.sqlx` data가 현재 스키마나 query와 맞지 않으면 nonzero exit status로 종료된다고 설명한다.

## 기본 흐름

SQLite 예시로 흐름을 잡으면 다음 순서가 된다.

```powershell
$env:DATABASE_URL = "sqlite://target/dev.db"
sqlx database create
sqlx migrate add create_users
sqlx migrate run
cargo check
cargo sqlx prepare
cargo sqlx prepare --check
```

`sqlx database create`와 SQLite file URL 동작은 실제 예제 저장소에서 확인해 기록해야 한다. 이 글의 핵심은 명령의 성공 로그가 아니라 검증 순서다.

## Migration 예시

`sqlx migrate add create_users`가 만든 파일에 schema 변경을 적는다.

```sql
create table users (
    id integer primary key,
    email text not null unique,
    display_name text not null,
    created_at text not null
);
```

production에 이미 적용된 migration은 수정하지 않는 것을 기본 원칙으로 둔다. 새 변경은 새 migration으로 추가한다. 이미 공유된 migration을 고치면 개발자별 로컬 DB, CI DB, 운영 DB의 이력이 갈라질 수 있다.

## App Startup Migration

애플리케이션 시작 시 migration을 적용할지, 배포 pipeline에서 별도 job으로 실행할지는 운영 방식에 따라 다르다. 다만 두 방식 모두 실패를 숨기면 안 된다.

```rust
use sqlx::{migrate::Migrator, SqlitePool};

static MIGRATOR: Migrator = sqlx::migrate!();

async fn run_migrations(pool: &SqlitePool) -> Result<(), sqlx::Error> {
    MIGRATOR.run(pool).await
}
```

SQLx 문서는 stable Rust에서 migration directory 변경을 build가 감지하게 하려면 build script로 `cargo:rerun-if-changed=migrations`를 출력하는 방법을 설명한다. migration을 binary에 embed하는 방식을 쓰면 이 점도 CI에서 확인해야 한다.

```rust
fn main() {
    println!("cargo:rerun-if-changed=migrations");
}
```

## Query Macro 예시

`query_as!`는 SQL 문자열과 Rust 출력 타입 사이의 기대를 build 단계에서 확인하게 해준다. 이 검증은 migration이 적용된 DB 또는 `.sqlx` metadata와 함께 작동한다.

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

만약 `display_name` 컬럼을 migration에서 삭제했는데 Rust query가 그대로라면, query macro 검증 단계에서 실패해야 한다. 이 실패를 CI가 잡는 것이 이 글의 목적이다.

## CI 검증 기준

CI에서는 둘 중 하나의 전략을 택한다.

| 전략 | 기준 |
| --- | --- |
| 실제 DB 기반 검증 | CI에서 DB를 띄우고 migration을 적용한 뒤 `cargo check`를 실행한다. |
| offline metadata 기반 검증 | 개발자가 `cargo sqlx prepare`로 `.sqlx`를 갱신하고, CI에서 `cargo sqlx prepare --check`로 최신성을 확인한다. |

두 전략을 섞을 수는 있지만, 어느 경로가 실패를 책임지는지 문서화해야 한다. `.sqlx`를 사용한다면 query 변경과 migration 변경이 있을 때 `.sqlx`도 함께 갱신되어야 한다.

## Rollback 기준

rollback은 `sqlx migrate revert` 명령 하나로 끝나는 운영 절차가 아니다. 다음을 미리 정해야 한다.

- 해당 migration이 reversible migration으로 생성되었는가?
- down migration이 데이터 손실 없이 가능한가?
- 이미 배포된 애플리케이션 버전이 이전 schema와 호환되는가?
- backup 또는 point-in-time recovery 전략이 있는가?
- rollback 실패 시 어떤 로그와 runbook으로 확인할 것인가?

특히 컬럼 삭제, 데이터 타입 축소, 데이터 변환 migration은 되돌리기 어렵다. 이런 변경은 expand-contract 방식처럼 단계적으로 배포하는 편이 안전하다.

## 관찰 상태

아직 이 글에는 실제 실행 결과가 없다. 발행 전에는 다음 실패 사례 중 하나를 의도적으로 만들고 로그를 기록한다.

- migration을 적용하지 않고 `cargo check`를 실행했을 때 query macro가 실패하는 사례
- query를 바꾼 뒤 `.sqlx`를 갱신하지 않아 `cargo sqlx prepare --check`가 실패하는 사례
- reversible migration의 `down.sql`이 실제로 복구 가능한지 확인한 사례

## 검증 체크리스트

- migration 파일이 version control에 포함되어 있는가?
- 이미 공유된 migration을 수정하지 않고 새 migration을 추가했는가?
- query macro를 쓰는 코드가 migration 적용 후 검증되는가?
- CI가 `cargo sqlx prepare --check` 또는 실제 DB 기반 `cargo check` 중 하나를 수행하는가?
- `.sqlx`를 사용하는 경우 query 변경과 함께 갱신했는가?
- rollback이 명령어가 아니라 데이터 복구 기준까지 포함하는가?

## 해석 / 의견

SQLx의 강점은 SQL을 숨기는 데 있지 않다. SQL을 명시적으로 쓰되, Rust 코드와 데이터베이스 schema가 어긋나는 순간을 더 일찍 발견하게 만드는 데 있다.

그래서 migration 글은 데이터베이스 작업 문서이면서 동시에 CI 설계 문서다. schema 변경을 사람이 기억하는 일로 두지 말고, 명령과 실패 조건으로 남겨야 한다.

## 한계와 예외

- 이 글은 SQLx CLI가 설치되어 있다고 가정한다. 설치 feature는 사용하는 DB와 TLS 정책에 따라 달라진다.
- SQLite와 PostgreSQL은 placeholder, type mapping, migration 운영 방식에서 차이가 있다.
- `migrate!`로 startup migration을 실행하는 방식과 배포 job으로 migration을 실행하는 방식은 각각 장단점이 있다.
- rollback 가능성은 도구가 아니라 migration 내용과 데이터 복구 전략에 의해 결정된다.

## 참고자료

- [SQLx migrate macro 0.8.6](https://docs.rs/sqlx/0.8.6/sqlx/macro.migrate.html)
- [SQLx query macro 0.8.6](https://docs.rs/sqlx/0.8.6/sqlx/macro.query.html)
- [SQLx CLI README](https://github.com/launchbadge/sqlx/blob/main/sqlx-cli/README.md)
- [Cargo build scripts](https://doc.rust-lang.org/cargo/reference/build-scripts.html)

## 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: SQLx migration, query macro, prepare/check, rollback 기준을 공식 문서 기반으로 보강.
