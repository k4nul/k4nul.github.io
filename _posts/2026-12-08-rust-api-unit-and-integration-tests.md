---
layout: single
title: "Rust Service 12. API 테스트에서 unit test와 integration test 분리하기"
description: "Rust API의 순수 로직 테스트, handler 테스트, 데이터베이스 포함 통합 테스트를 분리하는 기준을 정리한다."
date: 2026-12-08 09:00:00 +09:00
lang: ko
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
---

## 요약

모든 테스트가 서버 전체를 띄우면 느리고, 모든 테스트가 순수 함수만 보면 실제 경계가 빠진다.

순수 로직은 unit test, route와 response contract는 integration test, DB 흐름은 migration과 fixture가 포함된 별도 테스트로 나눈다. 중요한 것은 테스트 이름이 아니라 실패했을 때 어떤 경계가 깨졌는지 바로 보이게 만드는 것이다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: repository/service 계층을 어디까지 나눌지 정하기
- 다음 글: 인증을 붙이기 전에 세션과 JWT 경계 이해하기
- 보강 기준: 실제 발행 전 예제 저장소에서 `cargo test`, handler test, DB integration test의 실행 결과를 기록한다.

## 문서 정보

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial / 테스트 전략
- 테스트 환경: 직접 실행 테스트 없음. 아래 코드는 테스트 구조 설명용이며, 실제 실행 로그가 아니다.
- 확인한 버전: Rust Book, Cargo Book, Tokio 1.48.0 문서, Tower 0.5.3 문서, Axum 0.8.9 문서
- 출처 성격: 공식 문서, 원 프로젝트 문서

## 문제 정의

API 테스트를 모두 “통합 테스트”라고 부르면 테스트 suite가 금방 둔해진다. 반대로 unit test만 많으면 JSON, route, status code, database migration 같은 실제 경계가 검증되지 않는다.

이번 글의 목표는 테스트를 세 층으로 나누는 것이다.

- 순수 규칙이 깨졌는가?
- HTTP contract가 깨졌는가?
- database와 migration을 포함한 흐름이 깨졌는가?

## 확인한 사실

- Rust Book은 unit test를 작은 범위에서 한 module을 isolation으로 테스트하는 것으로 설명하고, integration test를 library 외부에서 public interface를 사용해 여러 module을 함께 테스트하는 것으로 설명한다.
- Rust Book은 unit test를 `src` 안 코드 옆에 두고 `#[cfg(test)]` module을 쓰는 관례를 설명한다.
- Rust Book은 top-level `tests` directory의 각 파일을 별도 crate로 컴파일하는 integration test 흐름을 설명한다.
- Cargo Book은 기본 `cargo test`가 unit test, integration test, doc test 등을 빌드하고 실행하는 target selection 흐름을 설명한다.
- Tokio 1.48.0의 `#[tokio::test]` macro는 async test를 runtime에서 실행하도록 표시하며, 기본 test runtime은 single-thread current-thread runtime이라고 설명한다.
- Tower `ServiceExt`는 `oneshot` method를 제공하며, Axum router를 HTTP server 없이 request/response 단위로 테스트할 때 자주 쓰는 방식이다.

## 테스트 구분표

| 테스트 종류 | 위치 | 검증 대상 | 외부 의존성 |
| --- | --- | --- | --- |
| unit test | `src/**`의 `#[cfg(test)]` module | domain/service 순수 규칙 | 없음 또는 최소 |
| handler/route integration test | `tests/*.rs` | route, status, JSON response contract | test state |
| DB integration test | `tests/*.rs` 또는 별도 feature | migration, SQLx query, transaction | test DB |

처음에는 빠른 unit test와 HTTP contract test를 기본값으로 두고, DB test는 fixture 관리가 준비된 뒤 추가한다.

## Unit Test 예시

순수 validation이나 service rule은 HTTP를 몰라도 테스트할 수 있어야 한다.

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

이 테스트가 실패하면 HTTP가 아니라 domain rule이 깨진 것이다.

## Handler Test 예시

route와 response shape는 server socket을 열지 않고도 확인할 수 있다. 핵심은 `build_router`를 test에서 호출할 수 있게 `lib.rs` 쪽에 공개하는 것이다.

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

이 테스트는 handler, route, extractor rejection mapping, public status code를 본다. 하지만 실제 DB migration을 검증하지는 않는다.

## DB Integration Test 기준

DB test는 느릴 수 있으므로 실행 조건을 명확히 둔다.

```text
tests/
  users_http.rs
  users_db.rs
  common/
    mod.rs
```

DB test fixture는 다음 중 하나를 택한다.

| 방식 | 장점 | 주의점 |
| --- | --- | --- |
| SQLite temporary database | 빠르고 로컬 재현 쉬움 | PostgreSQL 전용 SQL과 차이가 날 수 있음 |
| PostgreSQL test container | 운영 DB와 가까움 | CI 시간이 늘고 환경 구성이 필요함 |
| transaction rollback | 테스트 간 격리 쉬움 | 애플리케이션 코드의 transaction과 충돌하지 않게 설계 필요 |

SQLx query macro를 쓰는 프로젝트라면 DB test 이전에 migration 적용과 `cargo sqlx prepare --check` 흐름도 함께 둔다.

## 실행 계획

실제 발행 전에는 다음 명령과 결과를 기록한다.

```powershell
cargo fmt --check
cargo test
cargo test --test users_http
cargo test --test users_db
cargo sqlx prepare --check
```

CI에서는 빠른 테스트와 DB 테스트를 분리해도 된다. 예를 들어 pull request마다 unit/handler test를 돌리고, DB integration은 migration 변경이나 nightly job에서 더 무겁게 돌리는 방식이 가능하다.

## 관찰 상태

아직 이 글에는 실제 실행 결과가 없다. 발행 전에는 다음 실패 사례 중 하나를 기록한다.

- validation rule 변경으로 unit test가 실패하는 사례
- error response shape 변경으로 handler test가 실패하는 사례
- migration 누락으로 DB integration test 또는 SQLx prepare check가 실패하는 사례

## 검증 체크리스트

- pure rule test가 HTTP 없이 실행되는가?
- public route와 response shape를 integration test로 확인하는가?
- DB test가 migration 적용 후 실행되는가?
- `tests/common/mod.rs`처럼 helper가 별도 test crate로 잘못 잡히지 않게 구성했는가?
- async test가 필요한 곳에만 `#[tokio::test]`를 쓰는가?
- CI에서 빠른 test와 느린 DB test의 실행 조건이 명확한가?

## 해석 / 의견

테스트는 많을수록 좋은 것이 아니라 실패 위치가 선명할수록 좋다. validation 실패를 확인하려고 매번 실제 DB와 HTTP server를 띄우면 suite는 느려지고, 느린 suite는 결국 덜 돌게 된다.

반대로 모든 테스트가 순수 함수만 보면 API contract가 깨져도 모른다. 그래서 빠른 unit test, HTTP contract test, DB integration test가 서로 다른 위험을 맡도록 나누는 편이 오래 간다.

## 한계와 예외

- 이 글은 테스트 framework 자체를 비교하지 않는다. Rust 기본 test harness, Tokio async test, Tower/Axum service 호출 흐름을 기준으로 한다.
- DB fixture 전략은 SQLite와 PostgreSQL 사이에서 달라질 수 있다.
- mock을 만들지 실제 DB를 쓸지는 테스트 목적과 비용에 따라 결정해야 한다.
- 예제 코드는 실행 결과를 포함하지 않는다.

## 참고자료

- [Rust Book: Writing Automated Tests](https://doc.rust-lang.org/book/ch11-00-testing.html)
- [Rust Book: Test Organization](https://doc.rust-lang.org/book/ch11-03-test-organization.html)
- [Cargo Book: cargo test](https://doc.rust-lang.org/cargo/commands/cargo-test.html)
- [Tokio 1.48.0 test macro](https://docs.rs/tokio/1.48.0/tokio/attr.test.html)
- [Tower ServiceExt 0.5.3](https://docs.rs/tower/0.5.3/tower/trait.ServiceExt.html)
- [Axum 0.8.9 documentation](https://docs.rs/axum/0.8.9/axum/)

## 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: unit/handler/DB integration test 경계, 실행 계획, 실패 관찰 기준을 공식 문서 기반으로 보강.
