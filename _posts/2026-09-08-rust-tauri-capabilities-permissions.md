---
layout: single
title: "Rust 18. Tauri capability와 permission 기초"
description: "Tauri v2의 capability, permission, scope, runtime authority가 frontend와 Rust command 사이의 권한 경계를 어떻게 만드는지 정리한다."
date: 2026-09-08 09:00:00 +09:00
lang: ko
translation_key: rust-tauri-capabilities-permissions
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

Tauri v2의 capability와 permission은 frontend가 로컬 시스템 기능을 어디까지 호출할 수 있는지 정하는 경계다. capability는 "어떤 window 또는 WebView에 어떤 permission을 붙일 것인가"이고, permission은 "어떤 command 또는 plugin 기능을 허용하거나 거부할 것인가"에 가깝다.

초보자에게 중요한 감각은 단순하다. frontend에서 import가 된다고 OS 기능이 열리는 것이 아니다. command, permission, scope, capability, window label이 맞아야 호출이 허용된다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: tutorial | analysis
- 테스트 환경: 로컬 실행 테스트 없음. Tauri v2 security 문서와 ACL 문서를 기준으로 정리했다.
- 테스트 버전: Tauri v2 문서 2026-04-29 확인. 실제 permission identifier는 사용하는 Tauri/plugin 버전에 맞춰 확인해야 한다.
- 출처 성격: 공식 문서, 원 프로젝트 문서

## 확인한 사실

- Tauri capability 문서는 capability가 window 또는 WebView에 어떤 permission을 grant 또는 deny할지 정의한다고 설명한다.
- capability 파일은 `src-tauri/capabilities` 안에 JSON 또는 TOML로 둘 수 있다.
- Tauri permission 문서는 permission을 command의 명시적 privilege 설명으로 정의하며, command allow/deny와 scope를 결합할 수 있다고 설명한다.
- Tauri command scope 문서는 scope가 command 동작의 세부 allow/deny 범위를 나타내며, deny가 allow보다 우선한다고 설명한다.
- Tauri runtime authority 문서는 runtime에서 permission, capability, scope를 보유하고, WebView invoke 요청이 허용된 origin/window에서 온 것인지 확인한 뒤 command로 넘긴다고 설명한다.
- Tauri capability 문서는 app에 등록한 custom command가 기본적으로 모든 window와 WebView에서 허용되며, 이를 바꾸려면 `AppManifest::commands`를 고려하라고 설명한다.
- 이 글의 검증 기준일은 2026-04-29이다.

## 개념 구분

| 개념 | 질문 | 예시 |
| --- | --- | --- |
| command | frontend가 Rust 또는 plugin 기능을 호출하는 단위 | `set_title`, `read_file`, `greet` |
| permission | 어떤 command를 허용/거부할지 설명하는 권한 | `core:window:allow-set-title` |
| scope | 허용된 command가 다룰 수 있는 대상 범위 | `$HOME/*` 허용, `$HOME/secret` 거부 |
| capability | 어떤 window/WebView에 어떤 permission을 붙일지 정함 | `windows: ["main"]`, `permissions: [...]` |
| runtime authority | invoke 요청을 실제로 허용/거부하는 runtime 경계 | 허용되지 않은 origin이면 command 호출 전 차단 |

## capability 예시

`src-tauri/capabilities/default.json`은 보통 이런 형태로 읽는다.

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:path:default",
    "core:event:default",
    "core:window:allow-set-title"
  ]
}
```

이 예시는 `main` window에 path 기본 기능, event 기본 기능, window title 변경 기능을 허용한다. 모든 window에 같은 권한을 주고 싶어서 `windows: ["*"]`를 쓰기 전에 정말 필요한지 먼저 확인해야 한다.

## permission과 scope

permission은 "read 기능을 열 것인가"를 다루고, scope는 "어디까지 읽게 할 것인가"를 다룬다. 예를 들어 filesystem plugin에서 read command를 허용하더라도 scope가 좁으면 특정 directory만 읽을 수 있다.

중요한 점은 scope가 자동으로 안전을 보장하지 않는다는 것이다. 공식 문서도 command 구현자가 scope 우회를 막아야 한다고 경고한다. 특히 직접 만든 command에 scope 개념을 넣는다면 Rust 코드에서 직접 검증해야 한다.

## custom command와 plugin command

앱 안에서 직접 만든 command는 `tauri::Builder::invoke_handler`에 등록한다. Tauri 문서 기준으로 등록된 custom command는 기본적으로 앱의 모든 window와 WebView에서 사용할 수 있다. 창별로 더 좁게 제한하고 싶다면 build 단계의 `AppManifest::commands`와 capability 설계를 함께 봐야 한다.

plugin command는 보통 plugin이 제공하는 permission identifier를 capability에 추가해 사용한다. 예를 들어 filesystem, shell, global-shortcut 같은 기능은 권한 범위가 넓어질 수 있으므로 default permission을 무심코 추가하지 않는다.

## 점검 순서

1. frontend에서 어떤 기능을 호출하려는지 command 이름을 확인한다.
2. 그 기능이 custom command인지 Tauri core/plugin command인지 구분한다.
3. plugin command라면 필요한 permission identifier를 공식 문서에서 확인한다.
4. 파일, URL, shell, path 같은 대상이 있으면 scope가 필요한지 확인한다.
5. `src-tauri/capabilities/`에서 어떤 window label에 permission이 붙었는지 확인한다.
6. 여러 capability에 같은 window가 포함되어 권한이 합쳐지지 않는지 확인한다.
7. remote URL에 Tauri API를 열어야 한다면 별도 위험 검토를 한다.

## 흔한 실수

- `permissions: ["fs:default"]`처럼 넓은 권한을 먼저 넣고 나중에 줄이려고 한다.
- window title과 window label을 혼동한다. 보안 경계는 label에 의존한다.
- custom command 안에서 파일 경로를 검증하지 않고 frontend 입력을 그대로 사용한다.
- deny scope가 있어도 command 구현이 우회 가능하면 안전하다고 착각한다.
- remote content에 local system access를 열어도 괜찮다고 가정한다.

## 한계와 예외

- capability와 permission은 악성 Rust 코드 자체를 막는 장치가 아니다.
- 너무 넓은 scope, 잘못된 command 구현, supply chain 공격, WebView 취약점까지 자동으로 해결하지 않는다.
- 이 글은 plugin permission 작성법 전체를 다루지 않고, 앱 개발자가 읽어야 할 기본 경계를 다룬다.

## 참고자료

- [Tauri: Capabilities](https://v2.tauri.app/security/capabilities/)
- [Tauri: Permissions](https://v2.tauri.app/security/permissions/)
- [Tauri: Command Scopes](https://v2.tauri.app/security/scope/)
- [Tauri: Runtime Authority](https://v2.tauri.app/security/runtime-authority/)
- [Tauri: Core Permissions](https://v2.tauri.app/reference/acl/core-permissions/)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: capability, permission, scope, runtime authority, custom command 기본 허용 경계를 보강.
