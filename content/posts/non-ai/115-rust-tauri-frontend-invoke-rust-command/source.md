---
layout: single
title: "Rust 17. Frontend에서 Rust command 호출하기"
description: "Tauri frontend에서 Rust command를 invoke로 호출하는 기본 흐름, 인자 전달, 반환값, 에러 처리, 보안 경계를 정리한다."
date: 2026-09-01 09:00:00 +09:00
lang: ko
translation_key: rust-tauri-frontend-invoke-rust-command
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

Tauri에서 frontend가 Rust를 호출하는 기본 통로는 command와 `invoke`다. Rust 쪽 함수에 `#[tauri::command]`를 붙이고 builder에 등록한 뒤, frontend에서 `@tauri-apps/api/core`의 `invoke`로 이름을 호출한다.

중요한 점은 "호출된다"가 끝이 아니라는 것이다. command 이름, 인자 직렬화, 반환 타입, 에러 타입, 입력 검증, capability와 permission 경계를 함께 봐야 안전한 앱 구조가 된다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: tutorial | analysis
- 테스트 환경: 로컬 실행 테스트 없음. Tauri v2 Calling Rust from the Frontend 공식 문서를 기준으로 정리했다.
- 테스트 버전: Tauri v2 문서 2026-04-29 확인. 실제 코드는 사용하는 Tauri crate와 `@tauri-apps/api` 버전에 맞춰 확인해야 한다.
- 출처 성격: 공식 문서, 원 프로젝트 문서

## 확인한 사실

- Tauri 공식 문서는 frontend에서 Rust code와 통신하는 방법으로 command primitive와 event system을 설명한다.
- command는 인자를 받을 수 있고 값을 반환할 수 있으며, 에러를 반환하거나 async로 만들 수 있다.
- command는 `#[tauri::command]`로 정의하고 `tauri::generate_handler!`를 통해 builder의 `invoke_handler`에 등록한다.
- frontend에서는 `@tauri-apps/api/core`에서 `invoke`를 import해 command 이름으로 호출한다.
- command 인자는 camelCase JSON object로 전달하며, Rust 쪽 인자는 `serde::Deserialize`를 구현해야 한다.
- 반환값은 `serde::Serialize`를 구현해야 하며, 실패 가능한 command는 `Result`를 반환할 수 있다.
- 이 글의 검증 기준일은 2026-04-29이다.

## Rust command 만들기

`src-tauri/src/lib.rs`에 command를 하나 만든다.

```rust
#[tauri::command]
fn greet(name: String) -> Result<String, String> {
    let trimmed = name.trim();

    if trimmed.is_empty() {
        return Err("name is required".to_string());
    }

    Ok(format!("Hello, {trimmed}!"))
}
```

그리고 builder에 등록한다.

```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

command가 많아지면 별도 module로 빼도 된다. 다만 command 이름은 module namespace로 자동 분리되지 않으므로 앱 전체에서 고유하게 관리해야 한다.

## Frontend에서 호출하기

frontend에서는 `invoke`를 import하고 command 이름과 인자를 넘긴다.

```ts
import { invoke } from "@tauri-apps/api/core";

export async function greetFromRust(name: string): Promise<string> {
  return await invoke<string>("greet", { name });
}
```

버튼에서 호출한다면 실패도 처리해야 한다.

```ts
try {
  const message = await greetFromRust(input.value);
  result.textContent = message;
} catch (error) {
  result.textContent = String(error);
}
```

## 인자와 반환값 규칙

| 항목 | 기준 |
| --- | --- |
| command 이름 | frontend에서 문자열로 호출하므로 변경 시 호출부도 같이 수정 |
| 인자 | JSON object로 전달. 기본은 camelCase |
| Rust 입력 타입 | `serde::Deserialize` 가능해야 함 |
| Rust 반환 타입 | `serde::Serialize` 가능해야 함 |
| 실패 처리 | `Result<T, E>`로 표현하고 frontend promise rejection 처리 |
| 큰 바이너리 | JSON serialization 비용을 고려해 별도 방식 검토 |

## 보안 경계

frontend에서 넘어온 값은 사용자가 입력한 값과 같게 취급해야 한다. local app이라도 frontend 입력은 신뢰 경계 밖에서 온 것으로 보고 Rust에서 다시 검증한다.

특히 다음 command는 조심해야 한다.

- 파일 경로를 받아 읽기/쓰기
- shell command 실행
- 외부 URL 요청
- secret 또는 token 접근
- project directory 밖의 파일 변경
- 대량 삭제, 배포, 업데이트 실행

이런 command는 입력 검증, 경로 제한, scope 제한, capability/permission 검토, 사용자 확인 UI를 함께 둔다.

## 디버깅 기준

| 증상 | 확인할 것 |
| --- | --- |
| command not found | `generate_handler!`에 등록했는지, 이름이 같은지 |
| argument missing | frontend 인자 key가 camelCase인지 |
| deserialize error | Rust 입력 타입과 JSON shape가 맞는지 |
| promise rejected | Rust command가 `Err`를 반환했는지 |
| permission error | capability, plugin permission, window 설정 |

## 한계와 예외

- 이 글은 event system, channel, state management를 깊게 다루지 않는다.
- 실제 앱에서는 typed wrapper를 만들어 frontend 전체에 raw `invoke` 문자열이 퍼지지 않게 하는 편이 좋다.
- 인증, 파일 접근, shell 실행 같은 고위험 기능은 별도 글에서 더 좁은 permission 설계와 함께 다뤄야 한다.

## 참고자료

- [Tauri: Calling Rust from the Frontend](https://v2.tauri.app/develop/calling-rust/)
- [Tauri: Project Structure](https://v2.tauri.app/start/project-structure/)
- [Tauri: Capabilities](https://v2.tauri.app/security/capabilities/)
- [Tauri: Permissions](https://v2.tauri.app/security/permissions/)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: command 정의, `invoke` 호출, 인자/반환값 규칙, 에러 처리, 보안 경계를 보강.
