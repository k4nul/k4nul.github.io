---
layout: single
title: "Rust Service 07. Writing structured logs with tracing"
description: "Uses tracing events and spans to shape request-scoped structured logs for a Rust API."
date: 2026-11-03 09:00:00 +09:00
lang: en
translation_key: rust-api-structured-logging-tracing
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
permalink: /en/rust/rust-api-structured-logging-tracing/
---

## Summary

Plain string logs become hard to follow once a request crosses async work. Spans let the service record scope and relationships.

Request logs should keep field names such as `method`, `path`, `status`, `latency`, and `requestId` consistent so they can be searched and aggregated. Headers, tokens, passwords, and full request bodies should be excluded from default log fields.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Separating config files and environment variables
- Next post: Handling validation and bad requests
- Expansion criteria: before publication, add the example repository, commands, tool versions, and failure logs that fit this post's scope.

## Document Info / Environment

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial
- Test environment: No direct execution test. The code below is a design target to verify in the example repository by checking request log fields and sensitive-data exclusion.
- Tested versions: No runtime versions pinned. On the verification date, this was checked against `tracing`, `tracing-subscriber 0.3.23`, and `tower-http 0.6.8` documentation.
- Evidence level: official documentation, original project documentation

## Problem Statement

When an API runs asynchronously, one request can cross several functions and await points. Plain string logs make it hard to connect those events back to one request.

This post covers structured logging with `tracing`. The goal is not prettier log text. The goal is request-scoped fields and spans that can be searched in operation.

## Verified Facts

- `tracing` documentation describes spans as periods of time with a beginning and end that represent execution context. Events represent points in time and may occur inside spans. Evidence: [tracing crate documentation](https://docs.rs/tracing/latest/tracing/)
- `tracing` documentation describes structured fields on spans and events using `field_name = field_value`. That lets the service record `method`, `path`, and `status_code` as fields instead of burying them in strings. Evidence: [tracing crate documentation](https://docs.rs/tracing/latest/tracing/)
- `tracing-subscriber` `fmt` documentation provides a subscriber that records spans and events to stdout, and it supports runtime filtering through `RUST_LOG` with `EnvFilter`. Evidence: [tracing-subscriber fmt](https://docs.rs/tracing-subscriber/latest/tracing_subscriber/fmt/)
- `tracing-subscriber` formatter documentation describes JSON output as newline-delimited JSON logs intended for production systems that consume structured logs as JSON. Evidence: [tracing-subscriber fmt](https://docs.rs/tracing-subscriber/latest/tracing_subscriber/fmt/)
- `tower-http` `TraceLayer` documentation describes middleware that adds high-level tracing to an HTTP service and can record latency and response status in callbacks. Evidence: [tower-http TraceLayer](https://docs.rs/tower-http/latest/tower_http/trace/index.html)

## Reproduction Steps

There is no direct execution result yet. Before publication, add `tracing-subscriber` and `TraceLayer` to the minimal API example and record the fields produced by one request.

```powershell
cargo add tracing
cargo add tracing-subscriber --features env-filter,json
cargo add tower-http --features trace
```

Initialize tracing at startup.

```rust
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};

fn init_tracing() {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info,tower_http=info"));

    tracing_subscriber::registry()
        .with(filter)
        .with(tracing_subscriber::fmt::layer().json())
        .init();
}
```

Attach an HTTP request tracing layer to the router.

```rust
use axum::Router;
use tower_http::trace::TraceLayer;

fn build_router() -> Router {
    Router::new()
        // routes...
        .layer(TraceLayer::new_for_http())
}
```

Before publication, verify with:

```powershell
$env:RUST_LOG="info,tower_http=trace"
cargo run
curl.exe http://127.0.0.1:3000/health
```

## Observations

- This document currently contains no actual log output.
- The success condition is that one request produces searchable fields for method, path, status, and latency.
- Failure conditions include logging `authorization`, `cookie`, `set-cookie`, passwords, tokens, or entire request bodies by default.

## Verification Checklist

- Are log field names consistent across requests?
- Can log verbosity be changed with `RUST_LOG`?
- Can request start and response completion be connected through the same span or matching fields?
- Are status and latency recorded as fields instead of only in a message string?
- Are headers and bodies not logged wholesale?
- Is there a plan to connect request ids or trace ids between error responses and logs?

## Interpretation

Operational logs are both text for people and data for systems. A message like `request finished` is readable, but it is weak for status aggregation or latency search.

Logging every value is risky in the other direction. Headers and bodies may contain secrets or personal data, so default fields should start with the operational minimum: method, path template, status, latency, and request id.

## Limitations

- This post does not yet include actual log output or executed command results.
- The example is the beginning of structured logging; OpenTelemetry trace export and metrics export are handled in later observability posts.
- `TraceLayer::new_for_http()` defaults should not be assumed to satisfy every organization's log schema.
- Header logging is excluded by default and should be added narrowly with an allowlist when needed.
- Before publication, add an example repository, commands, versions, and failure logs.

## References

- [tracing crate documentation](https://docs.rs/tracing/latest/tracing/)
- [tracing-subscriber fmt](https://docs.rs/tracing-subscriber/latest/tracing_subscriber/fmt/)
- [tower-http TraceLayer](https://docs.rs/tower-http/latest/tower_http/trace/index.html)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Separated tracing span/event evidence, JSON formatter, TraceLayer scope, and sensitive logging limitations.
