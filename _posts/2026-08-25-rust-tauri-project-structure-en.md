---
layout: single
title: "Rust 16. Reading the Tauri project structure"
description: "Explains how to read a Tauri project through the frontend area, src-tauri, Cargo.toml, tauri.conf.json, lib.rs, and capabilities."
date: 2026-08-25 09:00:00 +09:00
lang: en
translation_key: rust-tauri-project-structure
section: development
topic_key: rust
categories: Rust
tags: [rust, tauri, desktop-app, webview, app-development]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/rust/rust-tauri-project-structure/
---

## Summary

A Tauri project is commonly split into a frontend project and a Rust project under `src-tauri/`. Reading that structure helps you know where UI changes, Rust commands, app configuration, and permissions belong.

At first, do not memorize every file. Learn the roles: top-level frontend, `src-tauri` Rust backend, `tauri.conf.json` app configuration, and `capabilities` as the permission boundary.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: tutorial | analysis
- Test environment: No local execution. This post is based on the Tauri v2 Project Structure documentation.
- Tested versions: Tauri v2 documentation checked on 2026-04-29. Actual generated files can vary by template and Tauri CLI version.
- Evidence level: official documentation, original project documentation

## Verified Facts

- Tauri documentation says a project is usually made of a Rust project and an optional JavaScript project.
- The official example shows `package.json`, `index.html`, `src/`, and `src-tauri/`.
- `src-tauri/` contains files such as `Cargo.toml`, `Cargo.lock`, `build.rs`, `tauri.conf.json`, `src/main.rs`, `src/lib.rs`, `icons/`, and `capabilities/`.
- Tauri documentation describes `tauri.conf.json` as the main configuration file, containing settings from application identifier to dev server URL and acting as a marker for the Tauri CLI to find the Rust project.
- Tauri documentation describes `capabilities/` as the default folder where Tauri reads capability files; commands must be allowed there to be used from JavaScript.
- The verification date for this post is 2026-04-29.

## Overall Structure

A representative structure looks like this:

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

## File Roles

| Location | Role |
| --- | --- |
| `package.json` | Frontend scripts, dependencies, dev command |
| `src/` | UI code, UI state, frontend `invoke` calls |
| `src-tauri/Cargo.toml` | Rust crate dependencies and build metadata |
| `src-tauri/build.rs` | Tauri build-system hook |
| `src-tauri/tauri.conf.json` | App identifier, window, build, bundle, and security settings |
| `src-tauri/src/main.rs` | Desktop entry point; usually not where most changes go |
| `src-tauri/src/lib.rs` | Main place for Rust commands, builder setup, and plugin registration |
| `src-tauri/capabilities/` | Window/WebView permission definitions |
| `src-tauri/icons/` | App icon assets |

## Where to Change Things

Change UI text, buttons, and frontend state in the frontend `src/` directory. If a button needs to read a local file or run Rust logic, define a command in `src-tauri/src/lib.rs`.

For app name, identifier, window settings, and dev server connection, inspect `tauri.conf.json`. If a command or plugin API is blocked from the frontend, inspect `capabilities/default.json` or the related capability file.

## Reading Order

1. Read `package.json` to see the dev commands.
2. Read `src-tauri/tauri.conf.json` to understand frontend dev server and bundle settings.
3. Read `src-tauri/src/lib.rs` to find registered commands and plugins.
4. Search frontend `src/` for `invoke` to see which commands the UI calls.
5. Check `src-tauri/capabilities/` to confirm the command or plugin permission is allowed.

## Common Misunderstandings

- `src-tauri` is not just a config folder. It is a Rust Cargo project.
- Tauri v2 examples do not put all app code in `main.rs`; `lib.rs` is the main place for app logic.
- Importing a frontend API does not automatically grant OS access. Capabilities and permissions still matter.
- Frontend structure can vary by template, but the role of `src-tauri` stays recognizable.

## Limitations

- Actual file names vary by frontend framework, package manager, and Tauri version.
- Rust-only frontends and workspace layouts may have a different top-level shape.
- Mobile targets add entry point and build configuration concerns.

## References

- [Tauri: Project Structure](https://v2.tauri.app/start/project-structure/)
- [Tauri: Configuration Files](https://v2.tauri.app/develop/configuration-files/)
- [Tauri: Capabilities](https://v2.tauri.app/security/capabilities/)
- [Tauri: Calling Rust from the Frontend](https://v2.tauri.app/develop/calling-rust/)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added project structure, file roles, reading order, and common misunderstandings.
