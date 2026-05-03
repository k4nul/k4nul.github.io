---
layout: single
title: "Rust 15. Tauri 개발 환경과 첫 앱 실행"
description: "Tauri 첫 앱을 만들기 전에 필요한 Rust, 시스템 의존성, Node.js, create-tauri-app 흐름과 실행 확인 기준을 정리한다."
date: 2026-08-18 09:00:00 +09:00
lang: ko
translation_key: rust-tauri-development-environment-first-app
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

Tauri 첫 앱 실행에서 중요한 것은 명령어 하나를 외우는 것이 아니라 개발 환경의 층을 구분하는 것이다. Tauri는 Rust project와 JavaScript project가 함께 움직이는 경우가 많으므로 Rust toolchain, OS별 system dependency, Node.js 또는 package manager, Tauri CLI 역할을 나눠 이해해야 한다.

이 글은 실제 실행 로그를 제공하는 글이 아니라, 공식 문서 기준으로 첫 앱을 만들 때 확인해야 할 순서를 정리한 글이다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: tutorial | analysis
- 테스트 환경: 로컬 실행 테스트 없음. Tauri v2 prerequisites와 create project 공식 문서를 기준으로 절차를 정리했다.
- 테스트 버전: Tauri v2 문서 2026-04-29 확인. 실제 실행 시에는 `rustc --version`, `cargo --version`, `node --version`, package manager 버전을 기록해야 한다.
- 출처 성격: 공식 문서, 원 프로젝트 문서

## 확인한 사실

- Tauri prerequisites 문서는 시작 전에 system dependencies, Rust, mobile target을 쓰는 경우의 추가 설정이 필요하다고 설명한다.
- Tauri 문서는 Linux, macOS, Windows별 system dependency가 다르다고 설명한다.
- Tauri create project 문서는 `create-tauri-app`이 공식 유지 템플릿으로 새 프로젝트 생성을 돕는다고 설명한다.
- Tauri create project 문서는 Bash, PowerShell, npm, yarn, pnpm, deno, bun, Cargo 방식의 생성 명령을 제시한다.
- 이 글의 검증 기준일은 2026-04-29이다.

## 설치 전 확인

| 층 | 확인할 것 | 이유 |
| --- | --- | --- |
| OS dependency | Linux/macOS/Windows별 WebView/build 의존성 | Tauri가 시스템 WebView와 native build 도구를 사용하기 때문 |
| Rust | `rustc`, `cargo`, rustup toolchain | `src-tauri`가 Cargo project이기 때문 |
| Node.js/package manager | npm, pnpm, yarn, bun 등 | frontend scaffold와 dev server 실행에 필요 |
| Tauri CLI | npm package 또는 Cargo 기반 CLI | dev/build 명령을 실행 |
| mobile target | Android/iOS 설정 | desktop만 만들면 처음에는 생략 가능 |

## 첫 프로젝트 생성 흐름

Windows PowerShell 기준 예시는 다음과 같다.

```powershell
irm https://create.tauri.app/ps | iex
```

npm을 이미 쓰고 있다면 다음처럼 시작할 수 있다.

```powershell
npm create tauri-app@latest
```

프로젝트 생성 중에는 대체로 다음을 고른다.

- project name
- bundle identifier
- frontend language
- package manager
- UI template
- TypeScript 또는 JavaScript flavor

처음이라면 공식 문서의 권장처럼 Vanilla + TypeScript 조합으로 시작하면 구조가 단순하다.

## 첫 실행 확인

생성 후 실제 실행 명령은 선택한 package manager에 따라 다르다. 예를 들어 `pnpm`을 골랐다면 보통 다음 흐름이 된다.

```powershell
cd my-tauri-app
pnpm install
pnpm tauri dev
```

첫 실행에서 확인할 것은 화면이 뜨는지만이 아니다.

1. dev server가 실행되는가?
2. Rust build가 진행되는가?
3. Tauri window가 열리는가?
4. frontend 수정이 반영되는가?
5. `src-tauri` 쪽 Rust 수정 후 재빌드가 되는가?
6. 에러가 나면 OS dependency, Rust, Node/package manager 중 어느 층에서 실패했는지 구분되는가?

## 실패 해석

| 증상 | 먼저 볼 곳 |
| --- | --- |
| Rust compile error | `src-tauri/Cargo.toml`, Rust toolchain, crate version |
| dev server 실패 | `package.json`, package manager install 상태 |
| window가 열리지 않음 | system WebView, Tauri CLI, OS dependency |
| command not found | PATH, rustup, Node.js, package manager |
| 권한 관련 에러 | capability, permission, plugin 설정 |

에러 메시지를 그대로 복사하기보다 "어느 층에서 실패했는지"를 먼저 표시하면 나중에 재현과 도움 요청이 쉬워진다.

## 다음 단계

첫 앱이 실행되면 바로 기능을 많이 붙이기보다 프로젝트 구조를 읽어야 한다. 특히 `src-tauri/`, `tauri.conf.json`, `src-tauri/src/lib.rs`, `src-tauri/capabilities/default.json`이 어떤 역할을 하는지 이해하면 이후 command와 permission을 다룰 때 덜 흔들린다.

## 한계와 예외

- 이 글은 실제 로컬 설치 결과를 검증한 로그가 아니다.
- OS별 설치 명령은 공식 prerequisites 문서를 우선 확인해야 한다.
- corporate device, WSL, proxy, antivirus, old WebView 환경에서는 추가 문제가 생길 수 있다.

## 참고자료

- [Tauri: Prerequisites](https://v2.tauri.app/start/prerequisites/)
- [Tauri: Create a Project](https://v2.tauri.app/start/create-project/)
- [Tauri: Project Structure](https://v2.tauri.app/start/project-structure/)
- [Rust installation](https://www.rust-lang.org/tools/install)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: Tauri 개발 환경 구성 요소, 첫 프로젝트 생성 흐름, 실패 해석 기준을 보강.
