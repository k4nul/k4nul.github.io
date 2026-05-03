---
layout: single
title: "Rust 18. Tauri capabilities and permissions basics"
description: "Explains how Tauri v2 capabilities, permissions, scopes, and runtime authority define the boundary between frontend code and Rust commands."
date: 2026-09-08 09:00:00 +09:00
lang: en
translation_key: rust-tauri-capabilities-permissions
section: development
topic_key: rust
categories: Rust
tags: [rust, tauri, desktop-app, webview, app-development]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/rust/rust-tauri-capabilities-permissions/
---

## Summary

In Tauri v2, capabilities and permissions define how far frontend code can reach into local system functionality. A capability answers "which permissions apply to which window or WebView?" A permission answers "which command or plugin privilege is allowed or denied?"

The beginner rule is simple: importing a frontend API does not automatically open local system access. Command, permission, scope, capability, and window label all matter.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: tutorial | analysis
- Test environment: No local execution. This post is based on Tauri v2 security and ACL documentation.
- Tested versions: Tauri v2 documentation checked on 2026-04-29. Permission identifiers must be checked against the installed Tauri and plugin versions.
- Evidence level: official documentation, original project documentation

## Verified Facts

- Tauri capability documentation says capabilities define which permissions are granted or denied for which windows or WebViews.
- Capability files can be JSON or TOML files inside `src-tauri/capabilities`.
- Tauri permission documentation defines permissions as explicit privileges of commands and says permissions can combine command allow/deny and scopes.
- Tauri command scope documentation says scopes are granular allow/deny behavior for commands, and deny scopes supersede allow scopes.
- Tauri runtime authority documentation says the runtime holds permissions, capabilities, and scopes, checks incoming WebView invoke requests, and denies disallowed calls before the command is invoked.
- Tauri capability documentation says registered custom commands are allowed by all windows and WebViews by default, and points to `AppManifest::commands` for changing that behavior.
- The verification date for this post is 2026-04-29.

## Concept Map

| Concept | Question | Example |
| --- | --- | --- |
| command | What frontend-callable function exists? | `set_title`, `read_file`, `greet` |
| permission | Which command privilege is allowed or denied? | `core:window:allow-set-title` |
| scope | Which target can an allowed command affect? | allow `$HOME/*`, deny `$HOME/secret` |
| capability | Which window/WebView receives which permissions? | `windows: ["main"]`, `permissions: [...]` |
| runtime authority | Who enforces the invoke boundary at runtime? | Disallowed origins are rejected before command execution |

## Capability Example

A typical `src-tauri/capabilities/default.json` can be read like this:

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

This grants the `main` window default path features, default event features, and permission to set the window title. Before using `windows: ["*"]`, verify that every window really needs the same authority.

## Permissions and Scopes

A permission controls whether a command is opened. A scope controls what that command may act on. For example, the filesystem plugin may allow read commands while scopes restrict the readable directories.

Scopes do not automatically make unsafe command implementations safe. The official documentation notes that command developers must prevent scope bypasses. If you design scope-like behavior for your own commands, enforce it in Rust.

## Custom Commands and Plugin Commands

Application commands are registered with `tauri::Builder::invoke_handler`. According to Tauri documentation, registered custom commands are allowed by all app windows and WebViews by default. To restrict them more tightly per window, review build-time `AppManifest::commands` and capability design.

Plugin commands usually require adding plugin-provided permission identifiers to a capability. Be careful with defaults for filesystem, shell, global shortcut, and similar plugins because they can expose broad local authority.

## Review Procedure

1. Identify which command the frontend is trying to call.
2. Decide whether it is a custom command, Tauri core command, or plugin command.
3. For plugin commands, check the required permission identifier in official docs.
4. If the command acts on files, URLs, shell arguments, or paths, check whether a scope is needed.
5. Inspect `src-tauri/capabilities/` to see which window label gets the permission.
6. Check whether multiple capabilities merge on the same window and widen authority.
7. Treat remote URL access to Tauri APIs as a separate risk review.

## Common Mistakes

- Adding broad permissions such as `fs:default` first and hoping to narrow later.
- Confusing window title with window label. Security boundaries depend on labels.
- Accepting frontend-supplied paths in custom commands without Rust-side validation.
- Assuming deny scopes are enough when command implementation can bypass them.
- Granting local system access to remote content without a threat review.

## Limitations

- Capabilities and permissions do not protect against malicious Rust code.
- They do not automatically fix overly broad scopes, incorrect command logic, supply-chain compromise, or WebView vulnerabilities.
- This post covers the application developer's basic reading model, not the full process for authoring plugin permissions.

## References

- [Tauri: Capabilities](https://v2.tauri.app/security/capabilities/)
- [Tauri: Permissions](https://v2.tauri.app/security/permissions/)
- [Tauri: Command Scopes](https://v2.tauri.app/security/scope/)
- [Tauri: Runtime Authority](https://v2.tauri.app/security/runtime-authority/)
- [Tauri: Core Permissions](https://v2.tauri.app/reference/acl/core-permissions/)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added the distinction between capabilities, permissions, scopes, runtime authority, and default custom-command exposure.
