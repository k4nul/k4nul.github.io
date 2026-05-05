---
layout: single
title: "Rust Service 15. Building a Rust API image with Docker multi-stage builds"
description: "Builds a smaller Rust API container image by separating builder and runtime stages."
date: 2026-12-29 09:00:00 +09:00
lang: en
translation_key: rust-api-docker-multistage-build
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
permalink: /en/rust/rust-api-docker-multistage-build/
---

## Summary

The runtime image does not need the Rust compiler, Cargo registry cache, or the full source tree. It needs the executable and the runtime files required by that executable.

A Docker multi-stage build compiles in a builder stage and copies only the build artifact into a runtime stage. This is not only an image-size technique; it is a way to define what belongs in the production image.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Choosing defaults for CORS, rate limits, and request size
- Next post: Using .dockerignore, build cache, and image-size checks
- Expansion criteria: before publication, add the example repository's binary name, Docker version, build log, image size, and container run result.

## Document Information

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial / container build design
- Test environment: No direct Docker build execution. This post documents Dockerfile structure and verification criteria.
- Tested versions: Docker CLI/Engine version not recorded, Rust toolchain version not recorded. Actual environment must be recorded before publication.
- Evidence level: Docker official documentation, Dockerfile guidance, Rust official image conventions

## Problem Statement

Running a Rust API from a `FROM rust` image is convenient, but the production image becomes larger and includes tools the runtime path does not need.

The runtime image should answer these questions:

- Does the runtime image still include the compiler and source code?
- Does the built binary name match the `COPY` path in the Dockerfile?
- Are base image tags pinned enough for reproducible builds?
- Are runtime files such as TLS certificates or timezone data included when needed?
- Does the service run as a non-root user?
- Can secrets leak through build layers or image history?

This post focuses on stage boundaries before build-cache optimization. Cache and image-size measurement are handled in the next post.

## Verified Facts

- Docker's multi-stage build documentation explains that one Dockerfile can contain multiple `FROM` instructions and that artifacts can be selectively copied from one stage to another.
- Docker multi-stage builds can name stages with `AS` and copy files from them with `COPY --from=<stage>`.
- Dockerfile best-practice guidance notes that image tags can change over time, so digest pinning should be considered when reproducible builds matter.
- Docker build-secrets documentation provides secret mounts instead of putting build secrets into ordinary `ARG`, `ENV`, or `COPY` layers.
- If a Rust API depends on dynamically linked libraries or TLS certificates, the runtime stage must contain those runtime files. Choosing `scratch`, distroless, or Debian slim depends on binary linking and operational requirements.

## Dockerfile Example

This is a starting point for the stage structure. `rust-api` is an example binary name; match it to the real package or bin name in `Cargo.toml`.

```dockerfile
# syntax=docker/dockerfile:1

FROM rust:1-slim-bookworm AS builder
WORKDIR /app

COPY Cargo.toml Cargo.lock ./
COPY src ./src
RUN cargo build --release --locked

FROM debian:bookworm-slim AS runtime
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/target/release/rust-api /usr/local/bin/rust-api

ENV RUST_LOG=info
EXPOSE 3000
USER 65532:65532
ENTRYPOINT ["rust-api"]
```

The example is intentionally simple. Better dependency caching might use `cargo-chef` or workspace-aware layering, but that belongs in the next post.

## Stage Boundary Check

The core question is which files remain in the runtime image.

| Location | Include | Exclude |
| --- | --- | --- |
| Builder stage | Rust toolchain, source, Cargo registry/cache, build dependencies | Production runtime secrets |
| Runtime stage | Release binary, CA certificates, required runtime files | Compiler, Cargo cache, full source tree |
| Build context | Dockerfile, source, lock file | `.env`, local database dumps, test output, target directory |

`Cargo.lock` is the baseline for reproducible application builds. `cargo build --release --locked` fails when the lock file and dependency resolution disagree, which makes the problem visible in CI.

## Base Image Pinning

The example uses `rust:1-slim-bookworm` and `debian:bookworm-slim` for readability. For production, decide whether tags are enough. Docker's guidance notes that tags can point to different images over time, so digest pinning is stronger when reproducibility matters.

```dockerfile
FROM rust:1-slim-bookworm AS builder
FROM debian:bookworm-slim AS runtime
```

Stricter policies can add digest pinning, image signing, SBOM generation, and vulnerability scanning. This series covers release tags and scanning in later posts.

## Security Defaults

- Do not put secrets into image layers through `ARG`, `ENV`, or `COPY`.
- If private dependency credentials are required, evaluate Docker BuildKit secret mounts.
- Run the runtime stage as a non-root user.
- If the application needs to write files, create writable directories and set ownership before `USER`.
- Document the container port and the Axum listener port.
- Check image history for sensitive values.

## Reproduction Steps

In the real example repository, record these commands and results.

1. Record the Docker version.

```powershell
docker version
```

2. Build the image.

```powershell
docker build --pull -t rust-api:local .
```

3. Run the container.

```powershell
docker run --rm -p 3000:3000 -e RUST_LOG=info rust-api:local
```

4. In another terminal, check the health endpoint.

```powershell
curl.exe -i http://127.0.0.1:3000/health
```

5. Inspect image size and layer history.

```powershell
docker images rust-api:local
docker history rust-api:local
```

## Observation Status

This post does not yet include direct execution output. Before publication, add:

- `docker version` output
- The last lines of a successful `docker build --pull -t rust-api:local .`
- The address and port logged by the running API
- `/health` response status
- Image size from `docker images rust-api:local`
- Confirmation from `docker history rust-api:local` that secrets and source-copy mistakes are absent

## Verification Checklist

- Are builder and runtime stages separated?
- Does the runtime stage exclude the compiler, Cargo cache, and full source tree?
- Does the `COPY --from=builder` binary path match the actual binary name?
- Does the build use `cargo build --release --locked` against the lock file?
- Does the runtime stage include required files such as CA certificates?
- Does the container run as a non-root user?
- Are secrets absent from build layers and image history?
- Are build, run, health check, image-size, and history commands recorded?

## Interpretation

Understanding multi-stage builds only as "making the image smaller" misses half the value. The stronger benefit is narrowing the production image boundary. If source code and compilers are not in the runtime image, the attack surface and review scope are smaller.

Splitting stages does not automatically make an image safe. Secrets can still enter the build context, the wrong files can still be copied into the runtime stage, and the process can still run as root. That is why the Dockerfile should be checked together with `docker history`, image size, runtime user, and health-check behavior.

## Limitations

- This is a design post and does not run `docker build` directly.
- `scratch` and distroless runtime images require separate checks for binary linking, DNS, TLS certificates, and timezone data.
- Runtime dependencies can differ depending on whether crates use OpenSSL or rustls.
- Multi-architecture builds, SBOM generation, image scanning, and registry push are handled later in the series.

## References

- [Docker: Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker: Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker: Build secrets](https://docs.docker.com/build/building/secrets/)
- [Docker Hub: rust official image](https://hub.docker.com/_/rust)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Expanded stage boundaries, base image pinning, secret handling, non-root runtime, and verification commands using Docker official documentation.
