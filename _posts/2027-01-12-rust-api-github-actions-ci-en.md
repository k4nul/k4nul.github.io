---
layout: single
title: "Rust Service 17. Automating fmt, clippy, test, and build with GitHub Actions"
description: "Creates a basic GitHub Actions flow for fmt, clippy, tests, and Docker build checks in a Rust API repository."
date: 2027-01-12 09:00:00 +09:00
lang: en
translation_key: rust-api-github-actions-ci
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
permalink: /en/rust/rust-api-github-actions-ci/
---

## Summary

CI is not deployment decoration. It fixes the minimum quality bar for changes entering the main branch.

Keep the first workflow small. Separate `fmt`, `clippy`, `test`, release build, and Docker build checks, set explicit `permissions`, and document which failures block a merge.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Using .dockerignore, build cache, and image-size checks
- Next post: Connecting release tags and Docker image tags
- Expansion criteria: before publication, add one successful run and one example failure log each for fmt, clippy, test, and Docker build in the example repository.

## Document Information

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial / CI quality-gate design
- Test environment: No direct GitHub Actions execution. This post documents workflow structure and verification criteria.
- Checked documents: GitHub Actions workflow syntax, GitHub Actions Rust guide, dependency caching reference, secure use reference
- Evidence level: GitHub official documentation, Docker official documentation

## Problem Statement

A local `cargo test` pass does not guarantee main-branch quality. Developers may have different toolchains, environment variables, Docker versions, and feature flags.

The first CI workflow should answer:

- Do pull requests and main-branch pushes run the same minimum checks?
- Are formatting, linting, tests, and build failures easy to distinguish?
- Does `GITHUB_TOKEN` have only the permissions the workflow needs?
- Does dependency cache avoid storing secrets or sensitive files?
- Does the Dockerfile build in CI?
- Can a failed log tell reviewers which merge rule was broken?

This post does not push images or create releases. The goal is to make changes fail before they enter the main branch when they should fail.

## Verified Facts

- GitHub Actions workflow syntax documents `permissions` at workflow and job levels.
- GitHub Actions `defaults.run` can set default shell and working-directory options for `run` steps.
- GitHub Actions Rust guidance shows how to build and test Rust projects and notes that GitHub-hosted runners include Rust-related software.
- GitHub Actions Rust guidance includes an `actions/cache` example for Cargo registry, Cargo git cache, and `target`.
- GitHub dependency caching reference says a new cache is created on a cache miss if the job completes successfully.
- The same dependency caching reference warns not to store sensitive information such as access tokens or login credentials in the cache path.
- GitHub secure use reference recommends least privilege for workflow credentials.
- GitHub secure use reference describes pinning actions to a full-length commit SHA for stronger security.

## Minimal Workflow Example

This workflow is a starting point for pull requests and pushes. If the repository uses `master` as the default branch, replace `main` with `master`.

{% raw %}
```yaml
name: ci

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  rust:
    name: rust checks
    runs-on: ubuntu-latest
    defaults:
      run:
        shell: bash

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Show toolchain
        run: |
          rustc --version
          cargo --version

      - name: Install Rust components
        run: rustup component add rustfmt clippy

      - name: Cache Cargo
        uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/registry
            ~/.cargo/git
            target
          key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}

      - name: Format
        run: cargo fmt --all -- --check

      - name: Clippy
        run: cargo clippy --all-targets --all-features -- -D warnings

      - name: Test
        run: cargo test --locked

      - name: Release build
        run: cargo build --release --locked

      - name: Docker build
        run: docker build -t rust-api:ci .
```
{% endraw %}

Version tags such as `actions/checkout@v6` make examples readable. For higher-security repositories, apply the GitHub security guidance and consider pinning reviewed actions to full-length commit SHAs instead of mutable tags.

## Job Split Criteria

A single job is enough at first. Split jobs when faster feedback or clearer ownership matters.

| Job | Command | Merge-blocking criterion |
| --- | --- | --- |
| `fmt` | `cargo fmt --all -- --check` | Formatting mismatch |
| `lint` | `cargo clippy --all-targets --all-features -- -D warnings` | Warning or lint failure |
| `test` | `cargo test --locked` | Unit or integration test failure |
| `build` | `cargo build --release --locked` | Release profile build failure |
| `docker` | `docker build -t rust-api:ci .` | Dockerfile or build-context failure |

Splitting too early can increase repeated setup and cache complexity. Keeping everything in one job for too long can make failures harder to locate. The first standard is whether the failure log clearly tells the developer what to fix.

## Permissions And Secret Boundaries

A workflow that only checks CI usually does not need package write, release write, or deployment permissions.

```yaml
permissions:
  contents: read
```

When image push is added later, `packages: write` may be needed. Prefer granting it only to the push job rather than widening the whole workflow.

Do not put secrets in cache paths. Cargo registry cache and `target` are performance tools, not token storage. If private registry credentials are needed, treat GitHub secrets, OIDC, and package-manager configuration as separate boundaries.

## Match Local And CI Commands

Avoid CI-only magic. Developers should be able to run the same quality bar locally.

```powershell
cargo fmt --all -- --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --locked
cargo build --release --locked
docker build -t rust-api:ci .
```

If these pass locally but fail only in CI, inspect toolchain, OS package, environment variable, and Docker build-context differences.

## Observation Status

This post does not yet include a real GitHub Actions run. Before publication, add:

- URL of a successful workflow run
- `Format` step log for a formatting failure
- `Clippy` step log for a lint warning or error
- `Test` step log for a failing test
- `Docker build` step log for a Dockerfile failure
- Log evidence of cache hit or miss

## Verification Checklist

- Does the workflow trigger on pull requests and default-branch pushes?
- Are `permissions` explicit and least-privilege by default?
- Are `fmt`, `clippy`, `test`, release build, and Docker build failures distinguishable?
- Do `cargo` commands use `--locked` where the application repository commits `Cargo.lock`?
- Is the cache key tied to dependency changes?
- Are secrets and credentials excluded from cache paths?
- Is the action pinning policy documented?
- Are failed checks connected to branch protection or merge rules?

## Interpretation

CI is a way to move the quality bar earlier in the development flow, not a thing that only matters at deployment time. For a Rust API, formatting, linting, tests, and Docker builds catch different problems. Passing one does not make the others redundant.

Start with a small workflow whose failures are obvious. Add image push, releases, SBOM, and scanning after the basic quality bar is stable, so the risk added by each stage remains visible.

## Limitations

- This is a design post and does not run GitHub Actions directly.
- Self-hosted runners have different security, caching, and tool-installation boundaries than hosted runners.
- Private dependencies, database integration tests, and service containers require separate secrets and network design.
- Image push, registry login, and release creation are handled in the next post.

## References

- [GitHub Actions: Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [GitHub Actions: Building and testing Rust](https://docs.github.com/en/actions/tutorials/build-and-test-code/rust)
- [GitHub Actions: Dependency caching reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)
- [GitHub Actions: Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Docker: Build with GitHub Actions](https://docs.docker.com/build/ci/github-actions/)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Expanded GitHub Actions workflow structure, Rust check commands, cache, permissions, action pinning, and failure-log criteria using official documentation.
