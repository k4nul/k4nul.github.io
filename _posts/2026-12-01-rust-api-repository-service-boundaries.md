---
layout: single
title: "Rust Service 11. repository/service 계층을 어디까지 나눌지 정하기"
description: "Rust API에서 handler, service, repository 계층을 언제 나누고 언제 과하게 나누지 말아야 하는지 판단한다."
date: 2026-12-01 09:00:00 +09:00
lang: ko
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
---

## 요약

계층은 멋있어 보이기 위해 만드는 것이 아니라 변경 이유를 분리하기 위해 만든다.

처음에는 handler와 repository를 얇게 두고, 여러 handler가 같은 비즈니스 규칙을 공유하거나 transaction 경계가 생길 때 service 계층을 추가한다. 반대로 CRUD 하나뿐인 API에서 trait, mock, service, repository를 모두 먼저 만들면 구조가 설명보다 무거워진다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: SQLx migration과 쿼리 검증 흐름 만들기
- 다음 글: API 테스트에서 unit test와 integration test 분리하기
- 보강 기준: 실제 발행 전 예제 저장소의 module tree, 테스트 위치, 실패 사례를 함께 기록한다.

## 문서 정보

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial / 설계 기준
- 테스트 환경: 직접 실행 테스트 없음. 아래 구조와 코드는 경계 설명용 예시이며, 실행 로그가 아니다.
- 확인한 버전: Rust Book, Axum 0.8.9 문서, SQLx 0.8.6 문서
- 출처 성격: 공식 문서, 원 프로젝트 문서

## 문제 정의

Rust API를 처음 만들 때 가장 흔한 실수는 두 방향이다.

- 너무 늦게 나눈다: handler 안에 JSON 변환, validation, SQL, transaction, error mapping이 모두 들어간다.
- 너무 빨리 나눈다: 아직 한 번도 반복되지 않은 로직을 trait, service, repository, DTO 변환 계층으로 미리 감싼다.

이번 글의 목표는 “어떤 이름의 계층이 정답인가”가 아니라 “어떤 변경 이유를 어디에 둘 것인가”를 정하는 것이다.

## 확인한 사실

- Rust Book은 프로젝트가 커질수록 관련 기능을 묶고 서로 다른 기능을 분리하면 구현 위치와 변경 위치를 명확히 할 수 있다고 설명한다.
- Rust Book은 module system이 공개/비공개 세부 구현과 scope를 제어하는 기능을 제공한다고 설명한다.
- Rust package는 여러 binary crate와 선택적인 library crate를 포함할 수 있다.
- Axum은 `Router`, route, extractor, handler를 중심으로 HTTP 요청을 애플리케이션 코드에 연결한다.
- SQLx query macro는 SQL과 Rust 타입의 관계를 확인하는 도구이지만, 비즈니스 규칙을 대신 표현하지는 않는다.

## 계층 책임

처음 기준은 다음 정도면 충분하다.

| 계층 | 책임 | 피해야 할 일 |
| --- | --- | --- |
| handler | 요청 추출, public error mapping, response 변환 | SQL 세부 구현, 여러 단계 business rule |
| service | 여러 repository 호출 조합, transaction 경계, business rule | HTTP header나 Axum extractor 직접 의존 |
| repository | SQL 실행, row와 저장소 record 변환 | HTTP status 결정, 공개 error body 생성 |
| domain/model | 순수 값과 규칙 | database connection, request body 직접 의존 |

모든 API에 service가 항상 필요한 것은 아니다. 한 handler가 한 repository 함수를 호출하고 별도 규칙이 없다면 handler와 repository만으로 시작해도 된다.

## 시작 구조 예시

처음부터 복잡한 architecture를 만들기보다, module 이름이 책임을 드러내게 둔다.

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

`main.rs`는 설정을 읽고 listener를 띄우는 얇은 진입점으로 둔다. integration test가 `build_router`를 호출할 수 있게 핵심 조립은 `lib.rs`나 `app.rs`에서 공개한다.

## Handler 예시

handler는 Axum 경계에 머문다.

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

이 코드에서 handler는 request DTO와 response DTO를 안다. 하지만 SQL 문자열이나 transaction 세부 구현은 모른다.

## Service가 필요한 순간

service 계층은 반복이 확인되었을 때 추가한다.

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

이 정도 규칙이 여러 handler에서 공유되거나 transaction으로 묶여야 한다면 service가 자연스럽다. 반대로 단순 조회 하나만 있는 endpoint에 service를 만들면 파일만 늘고 변경 이유는 분리되지 않는다.

## Repository 예시

repository는 저장소의 언어를 감싼다.

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

repository는 `StatusCode::CONFLICT`를 반환하지 않는다. 이메일 중복이 외부에서 어떤 HTTP 응답이 될지는 handler 또는 error mapping 계층에서 결정한다.

## 재현 계획

실제 저장소에 반영할 때는 다음을 기록한다.

```powershell
cargo fmt --check
cargo test
cargo test users
```

확인할 결과:

- unit test가 domain/service 규칙을 HTTP 없이 검증하는가?
- integration test가 public route와 response shape를 검증하는가?
- repository test 또는 DB integration test가 migration 적용 후 실행되는가?
- handler가 SQLx error 문자열을 공개 응답에 노출하지 않는가?

## 검증 체크리스트

- 계층을 추가한 이유가 “파일 정리”가 아니라 “변경 이유 분리”인가?
- handler가 HTTP 경계 밖의 일을 너무 많이 하지 않는가?
- service가 Axum extractor나 HTTP status에 직접 의존하지 않는가?
- repository가 공개 API 응답 형식을 모르도록 되어 있는가?
- trait은 테스트나 교체 가능성이 실제로 필요할 때만 추가했는가?
- transaction 경계가 service 또는 명확한 application flow에 있는가?

## 해석 / 의견

작은 Rust API에서는 계층 수보다 의존 방향이 더 중요하다. 바깥쪽 HTTP 경계가 안쪽 business rule과 storage detail을 호출하되, 안쪽 코드가 Axum 응답 형식을 알아야 하는 상황은 피하는 편이 좋다.

계층은 나중에 나눌 수 있다. 하지만 handler 안에 모든 것이 섞인 상태로 테스트가 쌓이면 나중에 분리하기가 훨씬 어려워진다. 그래서 처음 구조는 얇게, 그러나 변경 이유는 보이게 두는 것이 균형점이다.

## 한계와 예외

- 이 글은 단일 서비스 예제 기준이다. 여러 bounded context나 여러 crate가 필요한 대형 시스템은 별도 기준이 필요하다.
- repository trait은 항상 필요한 것이 아니다. 실제 DB를 사용하는 integration test가 더 단순하고 신뢰도 높을 수 있다.
- SQLx query macro를 쓰는 경우 compile-time 검증 흐름과 migration 상태가 함께 맞아야 한다.
- 예제 코드는 구조 설명용이며 실행 결과를 포함하지 않는다.

## 참고자료

- [Rust Book: Packages, Crates, and Modules](https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html)
- [Axum 0.8.9 crate documentation](https://docs.rs/axum/0.8.9/axum/)
- [SQLx query macro 0.8.6](https://docs.rs/sqlx/0.8.6/sqlx/macro.query.html)

## 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: handler/service/repository 책임, 시작 module 구조, 재현 계획을 공식 문서 기준으로 보강.
