---
layout: single
title: "Rust Service 16. Using .dockerignore, build cache, and image-size checks"
description: "Explains build context, .dockerignore, cache invalidation, and image-size checks for Rust API images."
date: 2027-01-05 09:00:00 +09:00
lang: en
translation_key: rust-api-dockerignore-cache-image-size
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
permalink: /en/rust/rust-api-dockerignore-cache-image-size/
---

## Summary

Slow Docker builds and unexpectedly large images often start with build context and layer order, not with application code.

Exclude `target/`, local artifacts, and secret files from the build context, then separate dependency layers from source layers. Check build context transfer size, image size, and layer history instead of judging the image by feel.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Building a Rust API image with Docker multi-stage builds
- Next post: Automating fmt, clippy, test, and build with GitHub Actions
- Expansion criteria: before publication, record build-context transfer size, build time, image size, and layer history before and after `.dockerignore` in the example repository.

## Document Information

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial / Docker build operations check
- Test environment: No direct Docker build execution. This post documents Docker build context and cache design criteria.
- Tested versions: Docker CLI/Engine version not recorded, BuildKit version not recorded, Rust toolchain version not recorded. Actual environment must be recorded before publication.
- Evidence level: Docker official documentation

## Problem Statement

Even after adopting multi-stage builds, CI can stay slow and images can remain risky if the build context is large or layer order causes unnecessary cache invalidation.

The review questions are:

- What file set can the builder access when running `docker build .`?
- Are `target/`, `.env`, local dumps, and test output included in the context?
- Does a single source-file change rebuild dependency layers every time?
- Which command records image size?
- Does layer history show secrets or unnecessary copies?

The goal is not only "fast builds." The goal is to explain which files enter the build and which changes invalidate cache.

## Verified Facts

- Docker build context documentation describes build context as the set of files that the build can access.
- Docker documentation says that when a local directory is used as the build context, build instructions such as `COPY` and `ADD` can refer to files and directories in that context.
- Docker build context documentation says local directory contexts are processed recursively and that using the current directory as context makes its files available to the builder.
- Docker cache optimization documentation lists layer ordering, small build contexts, bind mounts, cache mounts, and external cache as ways to improve cache usage.
- Docker cache mount documentation explains that normal layer cache depends on an exact match for the instruction and relevant files, while cache mounts can reuse package cache across builds.
- Docker image tags are convenient names that can move, while image digests identify specific image content.

## .dockerignore Criteria

`.dockerignore` reduces build context. Once a file is in the context, the Dockerfile can accidentally copy it, and remote builders or CI systems may pay the transfer cost.

A Rust API can start with a file like this:

```dockerignore
# Rust build output
target/

# Local environment and secrets
.env
.env.*
*.pem
*.key
*.p12

# Git and editor noise
.git/
.github/
.idea/
.vscode/

# Local data and generated output
*.db
*.sqlite
coverage/
tmp/
dist/

# Docker artifacts
docker-compose.override.yml
```

Be careful with `.github/`: excluding it means Dockerfile instructions cannot use workflow files. Most API runtime images do not need them, but image-label or build-metadata policies may require a different rule.

## Cache-Friendly Dockerfile Order

If the whole source tree is copied first, small code changes can invalidate dependency build cache. Copy dependency decision files first, then copy source.

This example is a structural starting point. More advanced dependency caching can use tools such as `cargo-chef`, but that should be introduced intentionally.

```dockerfile
# syntax=docker/dockerfile:1

FROM rust:1-slim-bookworm AS builder
WORKDIR /app

COPY Cargo.toml Cargo.lock ./
COPY src ./src

RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release --locked

FROM debian:bookworm-slim AS runtime
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/target/release/rust-api /usr/local/bin/rust-api

USER 65532:65532
ENTRYPOINT ["rust-api"]
```

BuildKit cache mounts can reuse package cache across builds. They are not the same as files included in the final image. A faster build does not automatically mean a smaller runtime image.

## Image-Size Checks

Do not rely on one number.

| Check | Command | Reason |
| --- | --- | --- |
| Build context transfer | `docker build --progress=plain -t rust-api:cache-check .` | Check whether `transferring context` is unexpectedly large |
| Final image size | `docker images rust-api:cache-check` | Record a comparison baseline |
| Layer history | `docker history rust-api:cache-check` | Look for secrets, source copies, or package cache leftovers |
| Container behavior | `docker run --rm -p 3000:3000 rust-api:cache-check` | Confirm the smaller image still runs |

A smaller image is not always a better image. If the service needs TLS certificates, timezone data, or minimal runtime diagnostics, keep those files. The target is not "small at any cost"; it is "only necessary files, explainably included."

## Reproduction Steps

In the example repository, record this flow before publication.

1. Record the Docker version.

```powershell
docker version
```

2. Record build context transfer size and image size before `.dockerignore`.

```powershell
docker build --progress=plain -t rust-api:before-ignore .
docker images rust-api:before-ignore
docker history rust-api:before-ignore
```

3. Apply `.dockerignore` and record the same values.

```powershell
docker build --progress=plain -t rust-api:after-ignore .
docker images rust-api:after-ignore
docker history rust-api:after-ignore
```

4. Change one source file and check where the cache starts missing.

```powershell
docker build --progress=plain -t rust-api:cache-check .
```

5. Confirm the final image runs.

```powershell
docker run --rm -p 3000:3000 rust-api:after-ignore
curl.exe -i http://127.0.0.1:3000/health
```

## Observation Status

This post does not yet include direct execution output. Before publication, add:

- Docker CLI/Engine version
- `transferring context` size before and after `.dockerignore`
- Image size before and after `.dockerignore`
- First layer that misses cache after a source-file change
- Confirmation from `docker history` that secrets and local artifacts are absent
- `/health` response status

## Verification Checklist

- Are `target/`, `.env`, local dumps, and test output excluded from the build context?
- Does `.dockerignore` avoid excluding files the Dockerfile needs?
- Are dependency decision files copied separately from source files?
- If BuildKit cache mounts are used, are cache contents not confused with image contents?
- Are image size and layer history both recorded?
- Are secrets absent from build context, image layers, and image history?
- Does the smaller image still pass a health check?

## Interpretation

Docker build optimization is not about making the Dockerfile clever. It is about reducing the files that enter the build and the reasons cache gets invalidated. In Rust projects, accidentally sending `target/` into the context can increase transfer size and mistake surface quickly.

Build cache and image size are separate problems. Cache reduces build time, `.dockerignore` reduces context and accidental exposure, and multi-stage builds reduce the runtime image boundary. Keeping those separate makes failures easier to diagnose.

## Limitations

- This post does not execute Docker builds directly.
- Workspace layout, private dependencies, and native libraries can change the cache strategy.
- `cargo-chef`, `sccache`, registry cache, and GitHub Actions cache can be handled more concretely in the CI stage.
- Removing TLS certificates or required runtime files while reducing size can create runtime failures.

## References

- [Docker: Build context](https://docs.docker.com/build/concepts/context/)
- [Docker: Optimize cache usage in builds](https://docs.docker.com/build/cache/optimize/)
- [Docker: Build cache](https://docs.docker.com/build/cache/)
- [Docker: Pull an image by digest](https://docs.docker.com/reference/cli/docker/image/pull/)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Expanded `.dockerignore`, build context, cache mount, image-size, and layer-history verification criteria using Docker official documentation.
