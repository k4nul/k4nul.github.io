---
layout: single
title: "Rust Service 17. GitHub Actions로 fmt, clippy, test, build 자동화하기"
description: "Rust API 저장소에서 GitHub Actions로 fmt, clippy, test, Docker build 검증을 자동화하는 기본 흐름을 만든다."
date: 2027-01-12 09:00:00 +09:00
lang: ko
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
---

## 요약

CI는 배포 장식이 아니라 main branch에 들어오는 변경의 최소 품질선을 고정하는 장치다.

첫 workflow는 작게 시작한다. `fmt`, `clippy`, `test`, release build, Docker build를 분리하고, `permissions`를 명시하며, 어떤 실패가 merge를 막는지 문서화한다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: .dockerignore, build cache, 이미지 크기 줄이기
- 다음 글: release tag와 Docker image tag 연결하기
- 보강 기준: 실제 발행 전 예제 저장소에서 성공 run, fmt 실패, clippy 실패, test 실패, Docker build 실패 로그를 각각 추가한다.

## 문서 정보

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial / CI 품질선 설계
- 테스트 환경: 직접 GitHub Actions 실행 없음. 이 글은 workflow 구조와 검증 기준을 정리한다.
- 확인한 버전: GitHub Actions workflow syntax 문서, GitHub Actions Rust guide, Dependency caching reference, Secure use reference
- 출처 성격: GitHub 공식 문서, Docker 공식 문서

## 문제 정의

로컬에서 `cargo test`가 통과해도 main branch 품질이 보장되지는 않는다. 사람마다 toolchain, 환경 변수, Docker 버전, feature flag가 다를 수 있기 때문이다.

처음 CI가 답해야 할 질문은 다음과 같다.

- pull request와 main push에서 같은 최소 검증이 도는가?
- format, lint, test, build 실패가 서로 구분되는가?
- `GITHUB_TOKEN` 권한이 필요한 만큼만 열려 있는가?
- dependency cache가 secret이나 민감 파일을 저장하지 않는가?
- Dockerfile이 CI에서도 build되는가?
- 실패 로그를 보고 어떤 merge 기준이 깨졌는지 바로 알 수 있는가?

이번 글은 image push나 release 자동화를 다루지 않는다. 지금 단계의 목표는 "main에 들어가기 전에 깨져야 할 변경은 깨지게 만드는 것"이다.

## 확인한 사실

- GitHub Actions workflow syntax 문서는 workflow와 job 수준에서 `permissions`를 설정할 수 있다고 설명한다.
- GitHub Actions `defaults.run`은 `run` step의 기본 shell과 working directory를 설정할 수 있다.
- GitHub Actions Rust guide는 Rust 프로젝트를 build/test하는 CI workflow를 만들 수 있고, GitHub-hosted runner에 Rust 관련 software가 포함되어 있다고 설명한다.
- GitHub Actions Rust guide는 `actions/cache`로 Cargo registry, Cargo git cache, `target` 등을 cache하는 예시를 제공한다.
- GitHub dependency caching reference는 cache miss가 발생하면 job이 성공했을 때 새 cache가 만들어진다고 설명한다.
- 같은 caching reference는 cache path에 access token이나 login credential 같은 민감 정보를 저장하지 말라고 경고한다.
- GitHub secure use reference는 workflow credential에 least privilege를 적용해야 한다고 설명한다.
- GitHub secure use reference는 보안 강화를 위해 action을 full-length commit SHA로 pinning하는 방식을 설명한다.

## 최소 Workflow 예시

아래 예시는 push와 pull request에서 품질선을 확인하는 출발점이다. 실제 저장소가 `master`를 기본 branch로 쓴다면 `main` 대신 `master`로 바꾼다.

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

version tag로 action을 쓰는 예시는 읽기 쉽다. 다만 보안 수준이 높은 저장소에서는 GitHub 보안 가이드에 맞춰 `actions/checkout@v6` 같은 tag 대신 검토한 full-length commit SHA로 pinning하는 정책을 검토한다.

## Job 분리 기준

처음에는 하나의 job으로 충분하다. 다만 실패 원인을 더 빨리 보려면 아래처럼 나눌 수 있다.

| Job | 명령 | merge 차단 기준 |
| --- | --- | --- |
| `fmt` | `cargo fmt --all -- --check` | formatting이 맞지 않으면 실패 |
| `lint` | `cargo clippy --all-targets --all-features -- -D warnings` | warning을 허용하지 않으면 실패 |
| `test` | `cargo test --locked` | unit/integration test 실패 |
| `build` | `cargo build --release --locked` | release profile build 실패 |
| `docker` | `docker build -t rust-api:ci .` | Dockerfile 또는 build context 문제 |

job을 너무 빨리 쪼개면 cache와 중복 setup이 늘 수 있다. 반대로 하나의 job이 너무 길어지면 실패 위치를 찾기 어려워진다. 첫 기준은 "실패 로그를 보고 무엇을 고쳐야 하는지 바로 보이는가"다.

## Permissions와 Secret 경계

CI 검증만 하는 workflow에는 대개 package write, release write, deployment 권한이 필요 없다.

```yaml
permissions:
  contents: read
```

나중에 image push를 추가하면 `packages: write` 같은 권한이 필요해질 수 있다. 그때도 전체 workflow에 넓게 열기보다 push job에만 필요한 권한을 부여한다.

cache에도 secret을 넣지 않는다. Cargo registry cache와 `target`은 build 속도를 높이는 용도이지, token 저장소가 아니다. private registry token이 필요하면 GitHub secrets, OIDC, package manager 설정을 별도 경계로 다룬다.

## 로컬과 CI 명령 맞추기

CI에서만 쓰는 마법 명령을 만들지 않는다. 개발자가 로컬에서도 같은 기준을 실행할 수 있어야 한다.

```powershell
cargo fmt --all -- --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --locked
cargo build --release --locked
docker build -t rust-api:ci .
```

로컬에서 이 명령이 통과하는데 CI에서만 실패한다면 toolchain, OS package, environment variable, Docker build context 차이를 의심한다.

## 관찰 상태

이 글에는 아직 실제 GitHub Actions 실행 결과가 없다. 발행 전에는 다음 run을 기록해야 한다.

- 모든 step이 통과한 workflow run URL
- formatting 오류가 있을 때 `Format` step이 실패하는 로그
- clippy warning이 있을 때 `Clippy` step이 실패하는 로그
- test failure가 `Test` step에서 보이는 로그
- Dockerfile 문제가 `Docker build` step에서 보이는 로그
- cache hit/miss가 로그에 어떻게 나타나는지

## 검증 체크리스트

- workflow trigger가 pull request와 기본 branch push를 모두 다루는가?
- `permissions`가 명시되어 있고 최소 권한에서 시작하는가?
- `fmt`, `clippy`, `test`, release build, Docker build 실패가 구분되는가?
- `Cargo.lock`을 기준으로 `--locked` 검증을 수행하는가?
- cache key가 dependency 변경과 연결되어 있는가?
- cache path에 secret이나 credential이 들어가지 않는가?
- action pinning 정책을 문서화했는가?
- 실패한 check가 branch protection이나 merge 기준과 연결되어 있는가?

## 해석 / 의견

CI는 "나중에 배포할 때 돌리는 것"이 아니라 개발 흐름의 품질선을 앞쪽에 두는 일이다. 특히 Rust API에서는 format, lint, test, Docker build가 서로 다른 문제를 잡는다. 하나만 통과한다고 나머지가 안전하다고 볼 수 없다.

처음부터 복잡한 matrix나 release 자동화를 넣기보다, 실패가 명확한 작은 workflow를 먼저 두는 편이 좋다. 그 다음 image push, release, SBOM, scan을 추가하면 어느 단계에서 위험이 늘어나는지 보인다.

## 한계와 예외

- 이 글은 GitHub Actions를 직접 실행하지 않은 설계 글이다.
- self-hosted runner는 hosted runner와 보안/캐시/도구 설치 경계가 다르다.
- private dependency, database integration test, service container가 필요하면 secrets와 network 경계를 별도로 설계해야 한다.
- image push, registry login, release 생성은 다음 글의 범위다.

## 참고자료

- [GitHub Actions: Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [GitHub Actions: Building and testing Rust](https://docs.github.com/en/actions/tutorials/build-and-test-code/rust)
- [GitHub Actions: Dependency caching reference](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching)
- [GitHub Actions: Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Docker: Build with GitHub Actions](https://docs.docker.com/build/ci/github-actions/)

## 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: GitHub Actions workflow 구조, Rust check 명령, cache, permissions, action pinning, 실패 로그 기준을 공식 문서 기반으로 보강.
