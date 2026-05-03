---
layout: single
title: "Rust 19. Building a first local tool with Tauri"
description: "Builds a first Tauri local text stats tool without file or network permissions, connecting frontend input, Rust commands, and validation boundaries."
date: 2026-09-15 09:00:00 +09:00
lang: en
translation_key: rust-tauri-first-local-tool
section: development
topic_key: rust
categories: Rust
tags: [rust, tauri, desktop-app, webview, app-development]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/rust/rust-tauri-first-local-tool/
---

## Summary

A first Tauri local tool should not start with file access, shell execution, or network calls. Start with a small tool where the frontend sends text and a Rust command returns a computed result.

This example is a text stats tool. The user types text into a textarea, and a Rust command returns line, word, and character counts. It needs almost no operating-system authority, which makes it a good first Tauri boundary exercise.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: tutorial | analysis
- Test environment: No local execution. The example is based on Tauri v2 project structure, command, and capability documentation.
- Tested versions: Tauri v2 documentation checked on 2026-04-29. For a real run, record `tauri`, `@tauri-apps/api`, Rust toolchain, and frontend package manager versions.
- Evidence level: official documentation, original project documentation

## Verified Facts

- Tauri project structure documentation describes a typical Tauri project as a top-level JavaScript project plus a Rust project under `src-tauri/`.
- Tauri command documentation shows the flow of defining a Rust command with `#[tauri::command]`, registering it in `invoke_handler`, and calling it from the frontend with `invoke`.
- Tauri command documentation says commands can accept arguments, return values, return errors, and be async.
- Tauri capability documentation says registered custom commands are allowed by all windows and WebViews by default. For tighter limits, review `AppManifest::commands` and capability design.
- The verification date for this post is 2026-04-29.

## Tool Scope

Keep the feature deliberately small.

- Input: text entered by the user
- Processing: count lines, words, and characters
- Output: a JSON-serializable struct
- Permissions: no filesystem, shell, network, or plugin permission
- Failure cases: empty input or oversized input

This shows the three core pieces:

1. frontend input
2. Rust command
3. frontend result display

## Rust Command

Place the return struct and command in `src-tauri/src/lib.rs`.

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

Register it in the builder.

```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![analyze_text])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Frontend Call

Wrap raw `invoke` in a small typed function.

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

Handle both success and failure in UI code.

```ts
try {
  const stats = await analyzeText(textarea.value);
  result.textContent = `${stats.lines} lines, ${stats.words} words, ${stats.chars} chars`;
} catch (error) {
  result.textContent = String(error);
}
```

## Verification Cases

| Input | Expected Result |
| --- | --- |
| empty string | `text is required` error |
| `hello world` | words 2 |
| multiline text | line count matches input |
| Korean text | chars count characters, not bytes |
| very large input | size-limit error |

This tool does not read files, so it does not need filesystem plugin permissions. It does not run shell commands or use the network. That is the lesson: a local app does not need broad local authority just because it is local.

## Next Features

After the basic flow works, expand slowly.

- copy result button
- save recent input with local storage or the store plugin
- open file
- markdown analysis
- export result

As soon as you add file access, saving, or external command execution, revisit capabilities and permissions. For every new feature, write down which window should call which command and why.

## Limitations

- This post is a first-tool design example, not a local execution transcript.
- Production apps need more careful input limits, Unicode behavior, frontend state, error UX, and tests.
- Filesystem access, shell execution, and external binary embedding should be treated as separate next-step topics.

## References

- [Tauri: Project Structure](https://v2.tauri.app/start/project-structure/)
- [Tauri: Calling Rust from the Frontend](https://v2.tauri.app/develop/calling-rust/)
- [Tauri: Capabilities](https://v2.tauri.app/security/capabilities/)
- [Tauri: Permissions](https://v2.tauri.app/security/permissions/)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added a first local text stats tool example, Rust command, frontend invoke wrapper, and verification cases.
