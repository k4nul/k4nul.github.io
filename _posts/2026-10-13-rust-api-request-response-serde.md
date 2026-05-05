---
layout: single
title: "Rust Service 04. 요청/응답 타입 설계와 serde 사용 기준"
description: "Rust API에서 요청 DTO, 응답 DTO, 내부 도메인 타입을 분리하고 serde 적용 범위를 정한다."
date: 2026-10-13 09:00:00 +09:00
lang: ko
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
---

## Summary / 요약

API 타입은 외부 계약이다. 내부 구조체를 그대로 JSON으로 내보내면 필드 이름, optional 여부, enum 표현, 숨겨야 할 내부 값이 구현 변경과 함께 흔들린다.

요청 타입은 `Deserialize`, 응답 타입은 `Serialize` 중심으로 설계하고, domain 타입에는 가능한 한 HTTP/JSON 표현을 묻히지 않는다. 단순 CRUD 초반에는 request, response, domain을 분리하되 변환 코드를 짧게 유지한다.

## Curriculum Position / 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: Rust API 프로젝트 구조 잡기
- 다음 글: 에러 응답을 일관되게 만들기
- 보강 기준: 실제 발행 전 예제 저장소, 실행 명령, 사용 버전, 실패 로그를 이 글의 범위에 맞춰 추가한다.

## Document Info / Environment

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial
- 테스트 환경: 직접 실행 테스트 없음. 아래 코드는 발행 전 예제 저장소에서 `cargo test`와 HTTP 요청으로 확인해야 할 설계안이다.
- 테스트 버전: 실행 버전 미고정. 검증 기준일에 Serde 공식 문서와 Axum `0.8.9`의 `Json` 문서를 기준으로 확인했다.
- 출처 성격: 공식 문서, 원 프로젝트 문서

## Problem Statement / 문제 정의

최소 API 서버가 JSON을 주고받기 시작하면 곧 타입 경계 문제가 생긴다. 클라이언트가 보내는 payload, 서버가 저장하거나 계산하는 내부 모델, 클라이언트에게 돌려주는 응답은 비슷해 보여도 같은 책임이 아니다.

이번 글의 범위는 요청/응답 타입 설계와 serde 사용 기준이다. 목표는 `serde`를 모든 구조체에 습관적으로 붙이는 것이 아니라, 외부 JSON 계약이 필요한 타입에만 명확하게 붙이는 것이다.

## Verified Facts / 확인한 사실

- Serde 공식 문서는 `#[derive(Serialize, Deserialize)]`가 crate 안의 data structure에 대해 `Serialize`와 `Deserialize` 구현을 생성한다고 설명한다. 근거: [Serde: Using derive](https://serde.rs/derive.html)
- Serde container attributes 문서는 `rename_all`로 struct field 또는 enum variant의 case convention을 바꿀 수 있다고 설명한다. JSON 계약을 camelCase로 고정하려면 DTO에 명시하는 편이 안전하다. 근거: [Serde: Container attributes](https://serde.rs/container-attrs.html)
- Serde container attributes 문서는 `deny_unknown_fields`가 알 수 없는 field를 만났을 때 deserialization error를 내게 한다고 설명한다. 다만 이 선택은 forward compatibility를 줄일 수 있으므로 public API에서는 의도적으로 결정해야 한다. 근거: [Serde: Container attributes](https://serde.rs/container-attrs.html)
- Axum `Json` 문서는 extractor로 사용할 때 request body를 `DeserializeOwned` 타입으로 역직렬화하고, response로 사용할 때 값을 JSON 응답으로 만든다고 설명한다. 또한 JSON extractor는 body를 소비하므로 여러 extractor가 있을 때 마지막에 두어야 한다. 근거: [Axum Json](https://docs.rs/axum/0.8.9/axum/struct.Json.html)
- 이 글의 `Request`, `Response`, `Domain` 분리는 공식 표준이 아니라 API 계약을 안정적으로 관리하기 위한 이 시리즈의 설계 기준이다.

## Reproduction Steps / 재현 절차

아직 직접 실행 결과는 없다. 발행 전에는 최소 API 예제에 request/response/domain 타입을 추가하고 `cargo test`와 HTTP 요청 결과를 기록한다.

```powershell
cargo add serde --features derive
cargo add serde_json
```

타입은 다음처럼 역할을 나눈다.

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

handler에서는 JSON 계약 타입만 받거나 내보낸다.

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

## Observations / 관찰 결과

- 현재 문서에는 실제 `cargo test`, `cargo run`, `curl.exe` 출력이 없다.
- 성공 조건은 response JSON에 `passwordHash` 또는 `password_hash` 같은 내부 field가 나오지 않는 것이다.
- 실패 조건은 unknown field 거부 여부, 필수 field 누락, JSON syntax error, domain field 노출을 구분해서 기록한다.

## Verification Checklist / 검증 체크리스트

- request DTO에는 외부 입력으로 받을 field만 있는가?
- response DTO에는 클라이언트에게 공개할 field만 있는가?
- domain 타입이 serde attribute와 HTTP 표현에 과하게 묶이지 않았는가?
- `rename_all` 같은 JSON naming 정책이 DTO에 명시되어 있는가?
- `deny_unknown_fields`를 사용할 경우 compatibility tradeoff를 본문에 설명했는가?
- 실제 `cargo test`와 HTTP 요청/응답 결과를 기록했는가?

## Interpretation / 해석

요청/응답 타입을 나누는 일은 코드 양을 조금 늘린다. 하지만 API를 운영하기 시작하면 이 작은 중복이 훨씬 싼 보험이 된다. 내부 field를 바꿔도 응답 계약을 유지할 수 있고, 민감한 값이 실수로 JSON에 섞일 가능성도 줄어든다.

다만 모든 타입을 기계적으로 세 벌씩 만들 필요는 없다. 외부 계약이 없거나 테스트 내부에서만 쓰는 값은 단순하게 두고, HTTP boundary에 닿는 타입부터 분리하는 편이 읽기 쉽다.

## Limitations / 한계

- 이 글은 아직 실제 명령 실행 결과를 포함하지 않는다.
- DTO 분리는 작은 예제에서는 장황해 보일 수 있다.
- `deny_unknown_fields`는 엄격한 입력 검증에 도움이 되지만, 일부 클라이언트 확장 시나리오에서는 호환성을 낮출 수 있다.
- 날짜, 시간, decimal, enum 표현은 별도 설계가 필요하며 이 글에서는 깊게 다루지 않는다.
- 실제 발행 전에는 예제 저장소, 실행 명령, 버전, 실패 로그를 추가해야 한다.

## References / 참고자료

- [Serde documentation](https://serde.rs/)
- [Serde: Using derive](https://serde.rs/derive.html)
- [Serde: Container attributes](https://serde.rs/container-attrs.html)
- [Axum Json extractor and response](https://docs.rs/axum/0.8.9/axum/struct.Json.html)

## Change Log / 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: Serde derive, JSON DTO 경계, 재현 절차, compatibility 한계를 분리해 수정.
