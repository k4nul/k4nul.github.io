---
layout: single
title: "Rust 17. Calling Rust commands from the frontend"
description: "Explains the Tauri flow for calling Rust commands with invoke, including arguments, return values, errors, and security boundaries."
date: 2026-09-01 09:00:00 +09:00
lang: en
translation_key: rust-tauri-frontend-invoke-rust-command
section: development
topic_key: rust
categories: Rust
tags: [rust, tauri, desktop-app, webview, app-development]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/rust/rust-tauri-frontend-invoke-rust-command/
---

## Summary

In Tauri, the basic path from frontend to Rust is a command plus `invoke`. You annotate a Rust function with `#[tauri::command]`, register it in the builder, and call it from the frontend with `invoke` from `@tauri-apps/api/core`.

The important part is not only that the call works. You also need to understand command names, argument serialization, return types, error handling, input validation, and the capability/permission boundary.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: tutorial | analysis
- Test environment: No local execution. This post is based on the official Tauri v2 Calling Rust from the Frontend documentation.
- Tested versions: Tauri v2 documentation checked on 2026-04-29. Real code should be checked against the installed Tauri crate and `@tauri-apps/api` versions.
- Evidence level: official documentation, original project documentation

## Verified Facts

- Tauri documentation describes the command primitive and event system as ways for the frontend to communicate with Rust code.
- Commands can accept arguments, return values, return errors, and be async.
- Commands are defined with `#[tauri::command]` and registered through `tauri::generate_handler!` in the builder's `invoke_handler`.
- The frontend can import `invoke` from `@tauri-apps/api/core` and call a command by name.
- Command arguments are passed as a JSON object using camelCase keys by default, and Rust argument types must implement `serde::Deserialize`.
- Returned values must implement `serde::Serialize`, and fallible commands can return `Result`.
- The verification date for this post is 2026-04-29.

## Define a Rust Command

Add a command in `src-tauri/src/lib.rs`.

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

Register it in the builder.

```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

If the app has many commands, move them into separate modules. Command names still need to be unique across the app; module names do not create a frontend namespace.

## Call It from the Frontend

Import `invoke` and pass the command name plus arguments.

```ts
import { invoke } from "@tauri-apps/api/core";

export async function greetFromRust(name: string): Promise<string> {
  return await invoke<string>("greet", { name });
}
```

When using it from UI code, handle failure too.

```ts
try {
  const message = await greetFromRust(input.value);
  result.textContent = message;
} catch (error) {
  result.textContent = String(error);
}
```

## Argument and Return Rules

| Item | Rule |
| --- | --- |
| Command name | Called as a string from the frontend; update callers when renaming |
| Arguments | Passed as a JSON object; camelCase by default |
| Rust input type | Must be deserializable with `serde::Deserialize` |
| Rust return type | Must be serializable with `serde::Serialize` |
| Failure handling | Use `Result<T, E>` and handle promise rejection in the frontend |
| Large binary data | Consider serialization cost instead of blindly returning JSON |

## Security Boundary

Treat frontend values as user-controlled input. Even in a local app, frontend input crosses a trust boundary and should be validated again in Rust.

Be especially careful with commands that:

- read or write paths supplied by the frontend
- run shell commands
- request external URLs
- access secrets or tokens
- change files outside the project directory
- perform bulk deletion, deployment, update, or other side effects

For these commands, combine input validation, path restrictions, scope limits, capability/permission review, and user confirmation.

## Debugging Guide

| Symptom | Check |
| --- | --- |
| command not found | Is it registered in `generate_handler!` and is the name correct? |
| argument missing | Does the frontend use the expected camelCase key? |
| deserialize error | Does the Rust input type match the JSON shape? |
| promise rejected | Did the Rust command return `Err`? |
| permission error | Check capability, plugin permission, and window configuration |

## Limitations

- This post does not deeply cover the event system, channels, or state management.
- In real apps, prefer typed frontend wrappers so raw `invoke` strings do not spread everywhere.
- High-risk features such as authentication, filesystem access, and shell execution need narrower permission design in separate posts.

## References

- [Tauri: Calling Rust from the Frontend](https://v2.tauri.app/develop/calling-rust/)
- [Tauri: Project Structure](https://v2.tauri.app/start/project-structure/)
- [Tauri: Capabilities](https://v2.tauri.app/security/capabilities/)
- [Tauri: Permissions](https://v2.tauri.app/security/permissions/)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added command definition, `invoke` usage, argument and return rules, error handling, and security boundaries.
