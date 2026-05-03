---
layout: single
title: "Rust 19. Tauri 첫 로컬 도구 만들기"
description: "Tauri에서 파일·네트워크 권한 없이 시작하는 첫 로컬 text stats 도구를 만들며 frontend, Rust command, 검증 경계를 연결한다."
date: 2026-09-15 09:00:00 +09:00
lang: ko
translation_key: rust-tauri-first-local-tool
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

Tauri 첫 로컬 도구는 파일 읽기, shell 실행, 네트워크 요청부터 시작하지 않는 편이 좋다. 처음에는 frontend가 문자열을 보내고 Rust command가 계산 결과를 돌려주는 작은 도구가 가장 안전하다.

이 글의 예시는 text stats 도구다. 사용자가 textarea에 글을 넣으면 Rust command가 line, word, character 수를 계산해 반환한다. 이 예시는 OS 권한이 거의 필요 없어서 Tauri의 기본 흐름을 배우기에 좋다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: tutorial | analysis
- 테스트 환경: 로컬 실행 테스트 없음. Tauri v2 project structure, command, capability 문서를 기준으로 예제를 구성했다.
- 테스트 버전: Tauri v2 문서 2026-04-29 확인. 실제 실행 시에는 `tauri`, `@tauri-apps/api`, Rust toolchain, frontend package manager 버전을 기록해야 한다.
- 출처 성격: 공식 문서, 원 프로젝트 문서

## 확인한 사실

- Tauri project structure 문서는 일반적인 Tauri project가 top-level JavaScript project와 `src-tauri/` Rust project로 나뉜다고 설명한다.
- Tauri command 문서는 `#[tauri::command]`로 Rust command를 만들고 `invoke_handler`에 등록한 뒤 frontend에서 `invoke`로 호출하는 흐름을 설명한다.
- Tauri command 문서는 command가 인자, 반환값, 에러, async를 다룰 수 있다고 설명한다.
- Tauri capability 문서는 등록된 custom command가 기본적으로 모든 window와 WebView에서 허용된다고 설명한다. 더 좁은 제한이 필요하면 `AppManifest::commands`와 capability 설계를 검토해야 한다.
- 이 글의 검증 기준일은 2026-04-29이다.

## 만들 도구

기능은 일부러 작게 잡는다.

- 입력: 사용자가 입력한 text
- 처리: line 수, word 수, character 수 계산
- 출력: JSON으로 직렬화 가능한 구조체
- 권한: 파일, shell, 네트워크, plugin permission 없음
- 실패 조건: 입력이 너무 크거나 비어 있는 경우

이렇게 시작하면 Tauri의 세 가지 핵심을 한 번에 볼 수 있다.

1. frontend 입력
2. Rust command
3. frontend 결과 표시

## Rust command

`src-tauri/src/lib.rs`에 반환 구조체와 command를 둔다.

```rust
use serde::Serialize;

#[derive(Serialize)]
struct TextStats {
    lines: usize,
    words: usize,
    chars: usize,
}

#[tauri::command]
fn analyze_text(input: String) -> Result<TextStats, String> {
    let text = input.trim();

    if text.is_empty() {
        return Err("text is required".to_string());
    }

    if text.len() > 100_000 {
        return Err("text is too large".to_string());
    }

    Ok(TextStats {
        lines: text.lines().count(),
        words: text.split_whitespace().count(),
        chars: text.chars().count(),
    })
}
```

그리고 builder에 등록한다.

```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![analyze_text])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Frontend 호출

frontend에서는 raw `invoke`를 작은 wrapper로 감싼다.

```ts
import { invoke } from "@tauri-apps/api/core";

type TextStats = {
  lines: number;
  words: number;
  chars: number;
};

export async function analyzeText(input: string): Promise<TextStats> {
  return await invoke<TextStats>("analyze_text", { input });
}
```

UI 이벤트에서는 성공과 실패를 모두 처리한다.

```ts
try {
  const stats = await analyzeText(textarea.value);
  result.textContent = `${stats.lines} lines, ${stats.words} words, ${stats.chars} chars`;
} catch (error) {
  result.textContent = String(error);
}
```

## 검증할 것

| 입력 | 기대 결과 |
| --- | --- |
| 빈 문자열 | `text is required` 에러 |
| `hello world` | words 2 |
| 여러 줄 입력 | lines가 줄 수와 일치 |
| 한글 입력 | chars가 byte 수가 아니라 문자 수 기준 |
| 매우 긴 입력 | 크기 제한 에러 |

이 도구는 파일을 읽지 않기 때문에 filesystem plugin permission이 필요 없다. shell도 실행하지 않고 network도 쓰지 않는다. 첫 도구에서 이 점이 중요하다. 로컬 앱이라고 해서 곧바로 로컬 전체 권한을 열 필요는 없다.

## 다음에 붙일 수 있는 기능

기본 흐름이 확인되면 기능을 조금씩 넓힌다.

- 결과 복사 버튼
- 최근 입력을 local storage나 store plugin에 저장
- 파일 열기 기능
- markdown 분석
- export 기능

다만 파일 열기, 저장, 외부 command 실행을 붙이는 순간 capability와 permission 설계가 다시 필요하다. 기능이 늘 때마다 "어떤 window가 어떤 command를 왜 호출해야 하는가"를 다시 적는다.

## 한계와 예외

- 이 글은 실제 실행 로그가 아니라 첫 도구 설계 예제다.
- production 앱에서는 입력 크기, Unicode 처리, frontend state, error UX, 테스트를 더 정교하게 다뤄야 한다.
- 파일 접근, shell 실행, 외부 binary embedding은 다음 단계의 별도 주제로 보는 것이 안전하다.

## 참고자료

- [Tauri: Project Structure](https://v2.tauri.app/start/project-structure/)
- [Tauri: Calling Rust from the Frontend](https://v2.tauri.app/develop/calling-rust/)
- [Tauri: Capabilities](https://v2.tauri.app/security/capabilities/)
- [Tauri: Permissions](https://v2.tauri.app/security/permissions/)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: 첫 로컬 text stats 도구 예제, Rust command, frontend invoke, 검증 기준을 보강.
