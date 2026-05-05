---
layout: single
title: "Rust Service 02. Building a minimal API server with Axum"
description: "Builds the smallest useful Rust API server shape with Axum Router, routes, handlers, and JSON responses."
date: 2026-09-29 09:00:00 +09:00
lang: en
translation_key: rust-axum-minimal-api-server
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
permalink: /en/rust/rust-axum-minimal-api-server/
---

## Summary

The goal of a minimal server is not feature count. It is to see where the server starts, where the router is assembled, and what handler input and output types look like. This step keeps only `/health` and a small JSON echo endpoint.

Shared state, database wiring, authentication, tracing, and graceful shutdown stay out of this first example. That keeps the smallest useful Axum boundary visible: `Router`, routes, handlers, and JSON responses.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Defining what Rust owns in a web service
- Next post: Structuring a Rust Axum API project
- Expansion criteria: before publication, add the example repository, commands, tool versions, and failure logs that fit this post's scope.

## Document Info / Environment

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial
- Test environment: No direct execution test. The code below is the minimal example direction to reproduce before publication; it is not yet recorded as successful output.
- Tested versions: No runtime versions pinned. On the verification date, the docs.rs latest Axum page showed `0.8.9`; Tokio was checked against the official project documentation.
- Evidence level: official documentation, original project documentation

## Problem Statement

The goal of this curriculum is not just to build a Rust API. The goal is to turn that API into an operable unit that can be built, deployed, observed, and rolled back.

This post covers building a minimal API server with Axum. The important point is not merely that the server starts. The important point is that the route and handler type boundaries are easy to see.

## Verified Facts

- The Axum official documentation describes `Router` as the type used to set up which paths go to which services. The first thing to verify in a minimal server is therefore the route list. Evidence: [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- The Axum documentation describes handlers as async functions that take extractors as arguments and return something convertible into a response. Keeping handler input and output types small is the core of this first example. Evidence: [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- The Axum documentation describes `Json` responses as working with values that implement `serde::Serialize`. A JSON echo endpoint is enough to verify that boundary. Evidence: [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- The Tokio project describes Tokio as an asynchronous Rust runtime that provides building blocks for network applications. `#[tokio::main]` and a TCP listener are therefore runtime assumptions in this example. Evidence: [Tokio project](https://tokio.rs/)

## Reproduction Steps

There is no direct execution result yet. Before publication, run the following steps locally and record both the successful output and the failure conditions.

```powershell
cargo new rust-api-minimal
cd rust-api-minimal
cargo add axum@0.8.9
cargo add tokio@1 --features macros,rt-multi-thread
cargo add serde --features derive
cargo add serde_json
```

Keep the `src/main.rs` verification target small.

```rust
use axum::{routing::{get, post}, Json, Router};
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
struct Health {
    status: &'static str,
}

#[derive(Deserialize, Serialize)]
struct EchoRequest {
    message: String,
}

async fn health() -> Json<Health> {
    Json(Health { status: "ok" })
}

async fn echo(Json(payload): Json<EchoRequest>) -> Json<EchoRequest> {
    Json(payload)
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/health", get(health))
        .route("/echo", post(echo));

    let listener = tokio::net::TcpListener::bind("127.0.0.1:3000")
        .await
        .expect("bind listener");

    axum::serve(listener, app).await.expect("run server");
}
```

Before publication, these two HTTP checks are enough for this scope.

```powershell
cargo run
curl.exe http://127.0.0.1:3000/health
curl.exe -X POST http://127.0.0.1:3000/echo -H "content-type: application/json" -d '{"message":"hello"}'
```

## Observations

- This document currently contains no actual `cargo run` or `curl` output.
- The success condition before publication is that `/health` returns a 200 JSON response and `/echo` returns the JSON payload it received.
- Failure notes should separate listener bind failure, dependency version mismatch, JSON body parsing failure, and route typos.

## Verification Checklist

- Do the routes registered in `Router` match the endpoints described in the post?
- Are handler input and output types visible in the post?
- Are actual command outputs for the server and HTTP checks recorded?
- Can route-not-found, JSON parsing failure, and listener bind failure be distinguished?
- Are the official example APIs still correct on the verification date?

## Interpretation

A Rust API operations series needs more than language syntax. Real problems often appear at the boundary between code and the systems around it.

The first server should stay small. If a database pool, configuration loader, error enum, and tracing layer all arrive at once, the reader can no longer see the basic route and handler boundary. Operational concerns should be added later, but the first executable unit should fit in one screen.

## Limitations

- This post does not yet include executed command output.
- This example does not cover TLS, authentication, authorization, rate limiting, request size limits, or graceful shutdown.
- The JSON echo endpoint is only a type-boundary example, not a business API design example.
- Before publication, add an example repository, commands, versions, and failure logs.

## References

- [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- [Tokio project](https://tokio.rs/)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Separated minimal Axum evidence, reproduction steps, success conditions, and limitations.
