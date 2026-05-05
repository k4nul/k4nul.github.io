---
layout: single
title: "Rust Service 06. Separating config files and environment variables"
description: "Defines how to separate ports, log levels, database URLs, and secrets into a configuration layer."
date: 2026-10-27 09:00:00 +09:00
lang: en
translation_key: rust-api-configuration-environment
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
permalink: /en/rust/rust-api-configuration-environment/
---

## Summary

Configuration is not a code constant. Values that differ across local runs, CI, containers, and Kubernetes should be read explicitly at startup and fail fast when required values are missing.

Non-secret values such as ports, log levels, and feature flags can live in documented config or ConfigMaps. Sensitive values such as database URLs, tokens, and signing keys should not be put in ordinary config files; document the environment variable name, whether it is required, and where it is injected.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Making API error responses consistent
- Next post: Writing structured logs with tracing
- Expansion criteria: before publication, add the example repository, commands, tool versions, and failure logs that fit this post's scope.

## Document Info / Environment

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial
- Test environment: No direct execution test. The code below is a design target to verify in the example repository by starting with and without required environment variables.
- Tested versions: No runtime versions pinned. On the verification date, this was checked against Twelve-Factor App Config, Kubernetes ConfigMap, and Kubernetes Secret documentation.
- Evidence level: official documentation

## Problem Statement

As the server grows, values such as `127.0.0.1:3000`, `info`, and `postgres://...` can spread through the code. That works locally, but it makes the same binary harder to reuse in containers and Kubernetes.

This post covers separating config files and environment variables. The goal is to read configuration once into `AppConfig`, keep secrets out of logs and repositories, and make the ConfigMap/Secret boundary visible before the service moves into Kubernetes.

## Verified Facts

- Twelve-Factor App Config describes config as values that vary between deploys, including database handles, external service credentials, and canonical hostnames, and requires strict separation between config and code. Evidence: [Twelve-Factor App: Config](https://12factor.net/config)
- The same document describes environment variables as a language- and OS-agnostic way to store config. A Rust service therefore needs a startup layer that reads and validates required environment variables. Evidence: [Twelve-Factor App: Config](https://12factor.net/config)
- Kubernetes ConfigMap documentation describes a ConfigMap as an API object for storing non-confidential key-value data. It is not designed for large settings blobs; ConfigMap data cannot exceed 1MiB. Evidence: [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- Kubernetes Secret documentation describes a Secret as an object for a small amount of sensitive data such as passwords, tokens, or keys, and says Secrets are similar to ConfigMaps but intended for confidential data. Evidence: [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- Kubernetes Secret documentation warns that base64 values are obscured but do not provide a useful level of confidentiality. Secret manifests still need separate repository and access-control review. Evidence: [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

## Reproduction Steps

There is no direct execution result yet. Before publication, add `AppConfig` to the minimal API example and verify that startup succeeds when required variables exist and fails when they are missing.

```rust
use std::{env, net::SocketAddr};

#[derive(Debug, Clone)]
struct AppConfig {
    bind_addr: SocketAddr,
    log_level: String,
    database_url: String,
}

#[derive(Debug)]
enum ConfigError {
    Missing(&'static str),
    Invalid(&'static str),
}

impl AppConfig {
    fn from_env() -> Result<Self, ConfigError> {
        let bind_addr = env::var("APP_BIND_ADDR")
            .unwrap_or_else(|_| "127.0.0.1:3000".to_string())
            .parse()
            .map_err(|_| ConfigError::Invalid("APP_BIND_ADDR"))?;

        let log_level = env::var("RUST_LOG").unwrap_or_else(|_| "info".to_string());
        let database_url = env::var("DATABASE_URL")
            .map_err(|_| ConfigError::Missing("DATABASE_URL"))?;

        Ok(Self {
            bind_addr,
            log_level,
            database_url,
        })
    }
}
```

Before publication, verify both paths.

```powershell
$env:DATABASE_URL="postgres://example"
cargo run
Remove-Item Env:\DATABASE_URL
cargo run
```

| Name | Example | Required | Secret | Kubernetes location |
| --- | --- | --- | --- | --- |
| `APP_BIND_ADDR` | `0.0.0.0:3000` | No | No | ConfigMap |
| `RUST_LOG` | `info,tower_http=info` | No | No | ConfigMap |
| `DATABASE_URL` | `postgres://...` | Yes | Yes | Secret |

## Observations

- This document currently contains no actual `cargo run` output.
- The success condition is that the server starts when required environment variables exist and fails with a clear config error when they are missing.
- Failure conditions include writing secret values to `Debug` output, panic messages, logs, Docker image layers, or repository files.

## Verification Checklist

- Are values that vary between deploys removed from code constants?
- Does startup fail when a required environment variable is missing?
- Are optional defaults and required injected values documented separately?
- Are secrets excluded from ConfigMaps?
- Are real Secret manifests or `.env` values excluded from the repository?
- Do config error logs avoid printing secret values?

## Interpretation

A configuration layer adds a little code, but it reduces operational surprises. When all externally supplied values are read in one place, Docker, CI, and Kubernetes setup can answer a plain question: what must be injected?

That does not mean every value must become an environment variable. Internal wiring that does not vary between deploys can stay in code. Pull out deploy-specific values and secrets first.

## Limitations

- This post does not yet include executed command output.
- The example uses a small `std::env` loader and does not cover the `config` crate or cloud secret-manager integration.
- A Kubernetes Secret is an API object for separating sensitive data. It does not by itself solve every storage, transport, and access-control concern.
- Before publication, add an example repository, commands, versions, and failure logs.

## References

- [Twelve-Factor App: Config](https://12factor.net/config)
- [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Separated config/secret boundaries, Kubernetes ConfigMap/Secret evidence, reproduction steps, and limitations.
