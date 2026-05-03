---
layout: single
title: "Rust 16. Tauri 프로젝트 구조 읽기"
description: "Tauri 프로젝트의 frontend 영역, src-tauri, Cargo.toml, tauri.conf.json, lib.rs, capabilities 디렉터리의 역할을 읽는 방법."
date: 2026-08-25 09:00:00 +09:00
lang: ko
translation_key: rust-tauri-project-structure
section: development
topic_key: rust
categories: Rust
tags: [rust, tauri, desktop-app, webview, app-development]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Tauri 프로젝트는 보통 frontend project와 `src-tauri/` 안의 Rust project로 나뉜다. 이 구조를 읽을 줄 알아야 "화면 수정", "Rust command 추가", "앱 설정 변경", "권한 부여"가 각각 어디에서 일어나는지 구분할 수 있다.

처음에는 파일을 외우기보다 역할을 나누면 된다. top-level frontend, `src-tauri` Rust backend, `tauri.conf.json` 앱 설정, `capabilities` 권한 경계다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: tutorial | analysis
- 테스트 환경: 로컬 실행 테스트 없음. Tauri v2 Project Structure 공식 문서를 기준으로 정리했다.
- 테스트 버전: Tauri v2 문서 2026-04-29 확인. 실제 생성 구조는 선택한 template와 Tauri CLI 버전에 따라 달라질 수 있다.
- 출처 성격: 공식 문서, 원 프로젝트 문서

## 확인한 사실

- Tauri 공식 문서는 Tauri project가 보통 Rust project와 optional JavaScript project 두 부분으로 구성된다고 설명한다.
- 공식 예시는 `package.json`, `index.html`, `src/`, `src-tauri/` 구조를 보여준다.
- `src-tauri/`는 `Cargo.toml`, `Cargo.lock`, `build.rs`, `tauri.conf.json`, `src/main.rs`, `src/lib.rs`, `icons/`, `capabilities/` 등을 포함한다.
- 공식 문서는 `tauri.conf.json`이 앱 identifier부터 dev server URL까지 담는 주 설정 파일이며, Tauri CLI가 Rust project를 찾는 marker 역할도 한다고 설명한다.
- 공식 문서는 `capabilities/`가 Tauri가 capability file을 읽는 기본 폴더이며, JavaScript에서 command를 쓰려면 여기에서 허용해야 한다고 설명한다.
- 이 글의 검증 기준일은 2026-04-29이다.

## 큰 구조

대표 구조는 다음처럼 읽을 수 있다.

```text
.
├── package.json
├── index.html
├── src/
│   └── main.ts
└── src-tauri/
    ├── Cargo.toml
    ├── Cargo.lock
    ├── build.rs
    ├── tauri.conf.json
    ├── src/
    │   ├── main.rs
    │   └── lib.rs
    ├── icons/
    └── capabilities/
        └── default.json
```

## 파일별 역할

| 위치 | 역할 |
| --- | --- |
| `package.json` | frontend script, dependency, dev command |
| `src/` | 화면 코드, UI 상태, frontend에서 `invoke` 호출하는 코드 |
| `src-tauri/Cargo.toml` | Rust crate dependency와 build metadata |
| `src-tauri/build.rs` | Tauri build system hook |
| `src-tauri/tauri.conf.json` | app identifier, window, build, bundle, security 설정 |
| `src-tauri/src/main.rs` | desktop entry point. 보통 크게 수정하지 않음 |
| `src-tauri/src/lib.rs` | Rust command, builder 설정, plugin 등록의 중심 |
| `src-tauri/capabilities/` | window/WebView별 허용 permission 정의 |
| `src-tauri/icons/` | 앱 아이콘 산출물 |

## 어디를 수정해야 하나

화면 문구나 버튼을 바꾸는 일은 frontend `src/`에서 한다. 버튼을 눌렀을 때 로컬 파일을 읽거나 Rust 로직을 실행해야 한다면 `src-tauri/src/lib.rs`에 command를 만든다.

앱 이름, identifier, window 설정, dev server 연결은 `tauri.conf.json`에서 본다. command나 plugin API가 frontend에서 막힌다면 `capabilities/default.json` 또는 관련 capability file을 확인한다.

## 읽는 순서

1. `package.json`에서 어떤 dev command를 쓰는지 본다.
2. `src-tauri/tauri.conf.json`에서 frontend dev server와 bundle 설정을 본다.
3. `src-tauri/src/lib.rs`에서 등록된 command와 plugin을 찾는다.
4. frontend `src/`에서 `invoke`를 검색해 어떤 command를 호출하는지 본다.
5. `src-tauri/capabilities/`에서 해당 command 또는 plugin permission이 허용되는지 확인한다.

## 흔한 오해

- `src-tauri`는 단순 설정 폴더가 아니다. 별도의 Rust Cargo project다.
- `main.rs`에 모든 코드를 넣는 구조가 아니다. Tauri v2 예시는 `lib.rs`를 중심으로 Rust app logic을 둔다.
- frontend에서 import가 된다고 OS 기능이 자동으로 열리는 것은 아니다. capability와 permission이 필요하다.
- template마다 frontend 구조는 다를 수 있지만 `src-tauri`의 역할은 크게 변하지 않는다.

## 한계와 예외

- 실제 파일명은 선택한 frontend framework, package manager, Tauri 버전에 따라 달라질 수 있다.
- Rust-only frontend나 workspace 구성에서는 top-level 구조가 달라질 수 있다.
- mobile target을 켜면 entry point와 build 설정을 더 신경 써야 한다.

## 참고자료

- [Tauri: Project Structure](https://v2.tauri.app/start/project-structure/)
- [Tauri: Configuration Files](https://v2.tauri.app/develop/configuration-files/)
- [Tauri: Capabilities](https://v2.tauri.app/security/capabilities/)
- [Tauri: Calling Rust from the Frontend](https://v2.tauri.app/develop/calling-rust/)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: 프로젝트 구조, 파일별 역할, 읽는 순서, 흔한 오해를 보강.
