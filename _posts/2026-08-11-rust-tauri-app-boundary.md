---
layout: single
title: "Rust 14. Tauri는 Rust GUI 프레임워크가 아니라 앱 경계다"
description: "Tauri를 Rust GUI 프레임워크가 아니라 WebView frontend와 Rust backend를 연결하는 앱 경계로 이해해야 하는 이유를 정리한다."
date: 2026-08-11 09:00:00 +09:00
lang: ko
translation_key: rust-tauri-app-boundary
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

Tauri를 "Rust로 버튼과 레이아웃을 그리는 GUI 프레임워크"로 이해하면 금방 헷갈린다. Tauri의 기본 모델은 HTML, CSS, JavaScript로 UI를 만들고, Rust는 OS 기능, 파일, 프로세스, 네이티브 API, 보안 경계를 맡는 구조다.

그래서 Tauri를 배울 때 핵심은 widget API가 아니라 app boundary다. frontend가 무엇을 요청할 수 있고, Rust 쪽이 무엇을 허용하며, capability와 permission이 어떤 창 또는 WebView에 적용되는지를 보는 것이 중요하다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: analysis | tutorial
- 테스트 환경: 로컬 실행 테스트 없음. Tauri v2 공식 문서를 기준으로 개념을 정리했다.
- 테스트 버전: Tauri v2 문서 2026-04-29 확인. 실제 프로젝트에서는 `tauri`, `tauri-cli`, Rust toolchain, frontend package manager 버전을 따로 기록해야 한다.
- 출처 성격: 공식 문서, 원 프로젝트 문서

## 확인한 사실

- Tauri 공식 문서는 Tauri를 desktop과 mobile 플랫폼용 앱을 빌드하는 프레임워크로 설명하며, HTML/JavaScript/CSS로 컴파일되는 frontend framework를 사용할 수 있다고 설명한다.
- Tauri 앱은 시스템의 native WebView를 활용하므로 앱마다 브라우저 엔진을 번들하지 않는 구조다.
- Tauri 문서는 JavaScript와 Rust 사이의 binding으로 `invoke`를 언급하고, TAO가 window 생성, WRY가 webview rendering을 담당한다고 설명한다.
- Tauri v2 문서는 capabilities가 frontend WebView에 노출되는 core 기능과 plugin 기능을 제한하는 시스템이라고 설명한다.
- 이 글의 검증 기준일은 2026-04-29이다.

## Tauri를 앱 경계로 보는 이유

웹 앱에서는 브라우저 sandbox가 OS 접근을 강하게 제한한다. 데스크톱 앱에서는 사용자가 로컬 파일, 시스템 알림, shell, window, updater, filesystem 같은 기능을 기대한다. Tauri는 그 사이에 경계를 만든다.

| 영역 | 역할 |
| --- | --- |
| Frontend | 화면, 사용자 입력, 상태 표시, UI 상호작용 |
| WebView | frontend를 렌더링하는 OS 제공 웹 런타임 |
| Rust backend | OS 기능 호출, 로컬 데이터 처리, 무거운 작업, 안전한 API 제공 |
| IPC / command | frontend가 Rust 기능을 요청하는 통로 |
| Capability / permission | 어떤 창이 어떤 command와 plugin 기능을 쓸 수 있는지 정하는 경계 |

이 구조에서는 frontend 코드를 "신뢰된 로컬 코드"로 과대평가하면 안 된다. frontend는 사용자의 입력, 외부 파일, 로컬 HTML, 네트워크 응답 같은 영향을 받을 수 있다. 민감한 결정은 Rust 쪽 command에서 검증해야 한다.

## Rust GUI 프레임워크와 다른 점

Rust GUI 프레임워크는 보통 Rust 코드가 UI tree, widget, event, layout을 직접 다룬다. Tauri에서는 UI 대부분이 웹 기술이다. Rust는 UI를 직접 그리기보다 시스템 기능을 작고 명확한 command로 노출한다.

따라서 Tauri에서 좋은 Rust 코드는 "화면을 그리는 코드"보다 "경계가 명확한 로컬 API"에 가깝다.

예:

- 좋음: `read_config`, `save_settings`, `list_recent_projects`
- 위험함: `run_shell_any_command`, `read_any_file`, `write_to_path_without_validation`

## 설계 기준

1. frontend는 UX와 표시를 맡긴다.
2. Rust command는 한 가지 일을 하도록 작게 만든다.
3. command 입력은 Rust에서 다시 검증한다.
4. 파일 경로, URL, shell 인자, 외부 데이터는 신뢰하지 않는다.
5. capability에는 필요한 permission만 추가한다.
6. plugin을 추가할 때는 frontend에서 실제로 필요한 command만 열었는지 확인한다.
7. 창이 여러 개라면 창별 capability가 합쳐질 때 권한 경계가 넓어지지 않는지 확인한다.

## 초보자가 잡아야 할 감각

Tauri를 배우는 순서는 "Rust 문법을 깊게 파기"보다 "frontend와 Rust 사이의 계약을 작게 만들기"가 먼저다.

- UI에서 버튼을 누른다.
- `invoke`로 이름 있는 command를 호출한다.
- Rust command가 입력을 검증하고 결과를 반환한다.
- capability가 그 command 접근을 허용한다.
- 실패하면 frontend는 에러를 표시한다.

이 흐름이 이해되면 Tauri의 보안 모델과 프로젝트 구조가 훨씬 자연스럽게 보인다.

## 한계와 예외

- 이 글은 Tauri 내부 구현 전체나 WRY/TAO 직접 사용법을 다루지 않는다.
- Rust-only frontend 선택지인 Yew, Leptos, Sycamore도 가능하지만, 이 글은 일반적인 WebView + Rust backend 구조를 기준으로 한다.
- mobile target, updater, code signing, store 배포는 별도 주제다.

## 참고자료

- [Tauri: What is Tauri?](https://v2.tauri.app/start/)
- [Tauri: Architecture](https://v2.tauri.app/concept/architecture/)
- [Tauri: Calling Rust from the Frontend](https://v2.tauri.app/develop/calling-rust/)
- [Tauri: Capabilities](https://v2.tauri.app/security/capabilities/)
- [Tauri: Permissions](https://v2.tauri.app/security/permissions/)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: Tauri를 GUI 프레임워크가 아니라 WebView와 Rust backend 사이의 앱 경계로 설명하도록 본문 보강.
