---
layout: single
title: "Rust Service 03. Structuring a Rust Axum API project"
description: "Sets boundaries between main, router, state, and handler modules in an Axum API project."
date: 2026-10-06 09:00:00 +09:00
lang: en
translation_key: rust-axum-project-structure
section: development
topic_key: rust
featured: false
track: rust
repo:
demo:
references:
categories: Rust
tags: [rust, axum, api, production, devops]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/rust/rust-axum-project-structure/
---

## Summary

A toy Axum example can live in `main.rs`. A service that will be operated needs separate startup code, routing code, state definitions, and handlers so changes stay visible.

There is no need to start with deep architecture. This post starts with a shallow `main.rs`, `router.rs`, `state.rs`, and `handlers/` shape, then adds repository or service layers only when a database or external API creates a real boundary.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Building a minimal API server with Axum
- Next post: Designing request and response types with serde
- Expansion criteria: before publication, add the example repository, commands, tool versions, and failure logs that fit this post's scope.

## Document Info / Environment

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial
- Test environment: No direct execution test. The structure below is a design target to verify in the example repository with file movement, `cargo test`, and `cargo run`.
- Tested versions: No runtime versions pinned. On the verification date, this was checked against the Rust Book package/crate rules and Axum `0.8.9` documentation on docs.rs.
- Evidence level: official documentation, original project documentation

## Problem Statement

A one-file minimal server raises the next question: how far should the project be split? If everything stays in one file for too long, routes, state, and handlers become tangled. If too many layers appear too early, the post teaches folder names before the reader sees why they are needed.

This post covers structuring a Rust Axum API project. The rule is simple: keep the entry point small, assemble routes in one place, make shared state explicit, and keep handlers focused on turning HTTP input into responses.

## Verified Facts

- The Rust Book describes a crate as the smallest amount of code the compiler considers at a time, and a package as one or more crates plus `Cargo.toml`. Evidence: [Rust Book: Packages and Crates](https://doc.rust-lang.org/book/ch07-01-packages-and-crates.html)
- The Rust Book describes Cargo's convention that `src/main.rs` is the crate root of a binary crate and `src/lib.rs` is the crate root of a library crate. Keeping `main.rs` as a small runtime entry point fits that convention. Evidence: [Rust Book: Packages and Crates](https://doc.rust-lang.org/book/ch07-01-packages-and-crates.html)
- Axum documentation describes `Router` as the type that connects paths to services or handlers. Separating `router.rs` and `handlers/` maps that framework boundary into the project layout. Evidence: [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- Axum documentation describes shared state through `State` extraction and `.with_state(...)`. A visible `state.rs` type is easier to review than hidden global handler dependencies. Evidence: [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- `main.rs`, `router.rs`, `state.rs`, and `handlers/` are a local design choice for this series, not an official Rust or Axum standard.

## Reproduction Steps

There is no direct execution result yet. Before publication, move the minimal server into this shape and record `cargo test` and `cargo run` results.

```text
src/
  main.rs
  router.rs
  state.rs
  handlers/
    mod.rs
    health.rs
```

Limit each file's job.

1. `main.rs` reads configuration, opens the listener, and calls `build_router`.
2. `router.rs` assembles route lists, common layers, and state wiring.
3. `state.rs` defines dependency types shared by handlers.
4. `handlers/` contains functions that turn HTTP input into response types.
5. Do not add repository or service layers until a database, queue, or external API makes that boundary useful.

Before publication, use these checks.

```powershell
cargo test
cargo run
```

## Observations

- This document currently contains no actual `cargo test` or `cargo run` output.
- The success condition is that `/health` and the JSON echo endpoint keep the same behavior after the file split.
- Failure notes should separate module path errors, visibility errors, state type mismatches, and missing routes.

## Verification Checklist

- Does `main.rs` avoid detailed handler logic?
- Can the route list be found in one file?
- Is shared state explicit, without hidden global dependencies in handlers?
- Does each new layer reduce real complexity instead of only adding names?
- Are actual `cargo test` and `cargo run` outputs recorded after the file move?

## Interpretation

Project structure is more like a tool for lowering change cost than a universal answer sheet. Starting with `domain`, `application`, `infrastructure`, and `adapter` folders can make the reader memorize names before the need exists.

This series starts shallow and adds layers only when SQLx storage, authentication, or external service calls create a reason. That way the reader learns "this much split is enough for this complexity," not just "copy this folder tree."

## Limitations

- This post does not yet include actual file movement and execution output.
- The proposed shape is for the small API example in this series, not a standard layout for every Rust web service.
- Workspaces, multi-crate APIs, plugin architectures, and monorepo operations are outside the scope.
- Before publication, add an example repository, commands, versions, and failure logs.

## References

- [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- [Rust Book: Packages and Crates](https://doc.rust-lang.org/book/ch07-01-packages-and-crates.html)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Separated Rust package/crate evidence, Axum structure criteria, and pre-execution verification steps.
