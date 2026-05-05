---
layout: single
title: "Rust Service 03. Rust API 프로젝트 구조 잡기"
description: "Axum API 프로젝트에서 main, router, state, handler 모듈을 어떻게 나눌지 기준을 세운다."
date: 2026-10-06 09:00:00 +09:00
lang: ko
translation_key: rust-axum-project-structure
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

작은 Axum 예제는 `main.rs` 하나로도 충분하다. 그러나 운영 대상 서비스는 시작 코드, 라우팅 코드, 상태 정의, handler를 분리해야 변경 범위가 보인다.

처음부터 깊은 계층을 만들 필요는 없다. 이 글은 `main.rs`, `router.rs`, `state.rs`, `handlers/` 정도의 얕은 구조로 시작하고, database나 외부 API가 들어올 때 repository/service 계층을 추가하는 기준을 잡는다.

## Curriculum Position / 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: Axum으로 최소 API 서버 만들기
- 다음 글: 요청/응답 타입 설계와 serde 사용 기준
- 보강 기준: 실제 발행 전 예제 저장소, 실행 명령, 사용 버전, 실패 로그를 이 글의 범위에 맞춰 추가한다.

## Document Info / Environment

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial
- 테스트 환경: 직접 실행 테스트 없음. 아래 구조는 발행 전 예제 저장소에서 파일 이동, `cargo test`, `cargo run`으로 확인해야 할 설계안이다.
- 테스트 버전: 실행 버전 미고정. 검증 기준일에 Rust Book의 package/crate 규칙과 docs.rs의 Axum `0.8.9` 문서를 기준으로 확인했다.
- 출처 성격: 공식 문서, 원 프로젝트 문서

## Problem Statement / 문제 정의

최소 서버가 한 파일에서 동작하면 다음 문제는 "어디까지 쪼갤 것인가"다. 너무 오래 한 파일에 두면 route, state, handler 변경이 서로 섞인다. 반대로 처음부터 계층을 많이 만들면 작은 예제가 프레임워크보다 폴더 구조를 설명하는 글이 된다.

이번 글의 범위는 Rust API 프로젝트 구조 잡기이다. 기준은 단순하다. 실행 진입점은 작게, 라우터는 한곳에서, 공유 상태는 명시적으로, handler는 요청을 응답으로 바꾸는 일에 집중하게 둔다.

## Verified Facts / 확인한 사실

- Rust Book은 crate를 컴파일러가 한 번에 고려하는 가장 작은 코드 단위로 설명하고, package는 `Cargo.toml`을 포함하며 하나 이상의 crate를 묶는 단위라고 설명한다. 근거: [Rust Book: Packages and Crates](https://doc.rust-lang.org/book/ch07-01-packages-and-crates.html)
- Rust Book은 Cargo가 `src/main.rs`를 binary crate의 crate root로, `src/lib.rs`를 library crate의 crate root로 인식하는 관례를 설명한다. 따라서 `main.rs`를 실행 진입점으로 작게 유지하는 것은 Cargo 관례와 잘 맞는다. 근거: [Rust Book: Packages and Crates](https://doc.rust-lang.org/book/ch07-01-packages-and-crates.html)
- Axum 공식 문서는 `Router`로 path와 handler를 연결하고, handler가 extractor를 받아 response로 변환 가능한 값을 반환한다고 설명한다. 따라서 `router.rs`와 `handlers/`를 분리하는 것은 Axum의 개념 경계를 코드 구조에 반영하는 선택이다. 근거: [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- Axum 공식 문서는 handler 사이에 상태를 공유하는 방법 중 하나로 `State` extractor와 `.with_state(...)`를 설명한다. 따라서 공유 의존성은 handler 내부 전역값보다 `state.rs` 같은 명시적 타입으로 모으는 편이 검토하기 쉽다. 근거: [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- `main.rs`, `router.rs`, `state.rs`, `handlers/` 구조는 공식 표준이 아니라 이 시리즈의 로컬 설계 선택이다.

## Reproduction Steps / 재현 절차

아직 직접 실행 결과는 없다. 발행 전 최소 서버 예제를 다음 구조로 이동한 뒤 `cargo test`와 `cargo run` 결과를 기록한다.

```text
src/
  main.rs
  router.rs
  state.rs
  handlers/
    mod.rs
    health.rs
```

역할은 다음처럼 제한한다.

1. `main.rs`는 설정을 읽고 listener를 열고 `build_router`를 실행하는 진입점으로 둔다.
2. `router.rs`는 route 목록과 공통 layer, state 연결만 조립한다.
3. `state.rs`는 handler가 공유하는 의존성 타입을 정의한다.
4. `handlers/`는 HTTP 입력을 받아 응답 타입으로 바꾸는 함수만 둔다.
5. database, queue, 외부 API가 들어오기 전까지 repository/service 계층은 만들지 않는다.

발행 전 확인 명령은 다음처럼 둔다.

```powershell
cargo test
cargo run
```

## Observations / 관찰 결과

- 현재 문서에는 실제 `cargo test` 또는 `cargo run` 출력이 없다.
- 성공 조건은 파일 이동 후에도 기존 `/health`와 JSON echo endpoint가 같은 응답을 내는 것이다.
- 실패 조건은 module 경로 오류, 공개 범위 오류, state type 불일치, route 누락을 구분해서 기록한다.

## Verification Checklist / 검증 체크리스트

- `main.rs`가 실행 진입점 외의 세부 handler 로직을 갖고 있지 않은가?
- route 목록을 한 파일에서 찾을 수 있는가?
- 공유 상태 타입이 명시적이고 handler가 몰래 전역값에 의존하지 않는가?
- 새 계층이 실제 복잡도를 줄이는가, 아니면 이름만 늘리는가?
- 파일 이동 후 실제 `cargo test`와 `cargo run` 출력이 기록되어 있는가?

## Interpretation / 해석

프로젝트 구조는 정답표보다 변경 비용을 줄이는 도구에 가깝다. 처음부터 `domain`, `application`, `infrastructure`, `adapter` 같은 이름을 모두 만들면 독자는 왜 필요한지 알기 전에 구조부터 외우게 된다.

이 시리즈에서는 얕은 구조로 시작하고, SQLx 저장소나 인증 서비스처럼 실제 변경 이유가 생길 때만 계층을 추가한다. 그렇게 해야 독자가 "폴더를 이렇게 나누라"가 아니라 "이 복잡도에서는 여기까지 나누면 충분하다"를 배울 수 있다.

## Limitations / 한계

- 이 글은 아직 실제 파일 이동과 실행 결과를 포함하지 않는다.
- 제안 구조는 이 시리즈의 작은 API 예제 기준이며, 모든 Rust 웹 서비스의 표준 구조가 아니다.
- workspace, multi-crate, plugin architecture, monorepo 운영은 범위 밖이다.
- 실제 발행 전에는 예제 저장소, 실행 명령, 버전, 실패 로그를 추가해야 한다.

## References / 참고자료

- [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- [Rust Book: Packages and Crates](https://doc.rust-lang.org/book/ch07-01-packages-and-crates.html)

## Change Log / 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: Rust package/crate 근거와 Axum 구조 기준을 분리하고, 실행 전 검증 절차를 보강.
