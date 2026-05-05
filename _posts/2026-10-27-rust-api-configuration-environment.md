---
layout: single
title: "Rust Service 06. 설정 파일과 환경변수 분리하기"
description: "Rust API의 포트, 로그 레벨, 데이터베이스 URL, 비밀값을 설정 계층으로 분리하는 기준을 세운다."
date: 2026-10-27 09:00:00 +09:00
lang: ko
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
---

## Summary / 요약

설정은 코드의 상수가 아니다. 로컬, CI, 컨테이너, Kubernetes에서 값이 달라지는 항목은 시작 시점에 명시적으로 읽고, 누락되면 빠르게 실패해야 한다.

포트, 로그 레벨, feature flag처럼 비밀이 아닌 값은 설정 문서나 ConfigMap으로 관리할 수 있다. 데이터베이스 URL, 토큰, 인증 키처럼 노출되면 안 되는 값은 일반 설정 파일에 넣지 않고 환경변수 이름, 필수 여부, 주입 위치를 문서화한다.

## Curriculum Position / 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: 에러 응답을 일관되게 만들기
- 다음 글: tracing으로 구조화 로그 남기기
- 보강 기준: 실제 발행 전 예제 저장소, 실행 명령, 사용 버전, 실패 로그를 이 글의 범위에 맞춰 추가한다.

## Document Info / Environment

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial
- 테스트 환경: 직접 실행 테스트 없음. 아래 코드는 발행 전 예제 저장소에서 환경변수 유무에 따른 시작 성공/실패를 확인해야 할 설계안이다.
- 테스트 버전: 실행 버전 미고정. 검증 기준일에 Twelve-Factor App Config, Kubernetes ConfigMap, Kubernetes Secret 문서를 기준으로 확인했다.
- 출처 성격: 공식 문서

## Problem Statement / 문제 정의

서버가 커질수록 `127.0.0.1:3000`, `info`, `postgres://...` 같은 값이 코드 곳곳에 흩어지기 쉽다. 이렇게 되면 로컬에서는 동작하지만 컨테이너나 Kubernetes에서 같은 바이너리를 재사용하기 어렵다.

이번 글의 범위는 설정 파일과 환경변수를 분리하는 기준이다. 목표는 설정을 한 번 읽어 `AppConfig`로 고정하고, 비밀값을 로그나 repository에 남기지 않으며, Kubernetes로 이동할 때 ConfigMap과 Secret의 책임을 구분하는 것이다.

## Verified Facts / 확인한 사실

- Twelve-Factor App의 Config 문서는 deploy마다 달라지는 database handle, 외부 서비스 credential, canonical hostname 같은 값을 config로 보고, config와 code를 엄격히 분리하라고 설명한다. 근거: [Twelve-Factor App: Config](https://12factor.net/config)
- 같은 문서는 config를 환경변수에 저장하는 방식을 언어와 운영체제에 덜 종속적인 표준으로 설명한다. 따라서 Rust 코드에서는 시작 시점에 필요한 환경변수를 읽고 검증하는 계층이 필요하다. 근거: [Twelve-Factor App: Config](https://12factor.net/config)
- Kubernetes ConfigMap 문서는 ConfigMap을 비밀이 아닌 데이터를 key-value 형태로 저장하는 API object로 설명한다. ConfigMap은 1MiB를 넘는 큰 설정 덩어리를 담도록 설계되지 않았다. 근거: [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- Kubernetes Secret 문서는 Secret을 password, token, key 같은 소량의 민감한 데이터를 담는 object로 설명하고, ConfigMap과 비슷하지만 confidential data를 위해 의도된 것이라고 설명한다. 근거: [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- Kubernetes Secret의 base64 값은 숨김 처리일 뿐 유용한 수준의 기밀성을 제공하지 않는다고 문서가 주의한다. 따라서 Secret manifest를 repository에 그대로 넣는 것은 별도 보안 검토가 필요하다. 근거: [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

## Reproduction Steps / 재현 절차

아직 직접 실행 결과는 없다. 발행 전에는 최소 API 예제에 `AppConfig`를 추가하고, 필수 환경변수 누락 시 시작이 실패하는지 확인한다.

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

발행 전 확인 명령은 다음처럼 나눈다.

```powershell
$env:DATABASE_URL="postgres://example"
cargo run
Remove-Item Env:\DATABASE_URL
cargo run
```

| 이름 | 예시 | 필수 | 비밀 여부 | Kubernetes 위치 |
| --- | --- | --- | --- | --- |
| `APP_BIND_ADDR` | `0.0.0.0:3000` | 아니오 | 아니오 | ConfigMap |
| `RUST_LOG` | `info,tower_http=info` | 아니오 | 아니오 | ConfigMap |
| `DATABASE_URL` | `postgres://...` | 예 | 예 | Secret |

## Observations / 관찰 결과

- 현재 문서에는 실제 `cargo run` 출력이 없다.
- 성공 조건은 필수 환경변수가 있을 때 서버가 시작되고, 없을 때 명확한 설정 오류로 실패하는 것이다.
- 실패 조건은 secret 값을 `Debug` 출력, panic 메시지, 로그, Docker image layer, repository 파일에 남기는 경우다.

## Verification Checklist / 검증 체크리스트

- deploy마다 달라지는 값이 코드 상수로 박혀 있지 않은가?
- 필수 환경변수가 누락될 때 시작 시점에 실패하는가?
- 기본값이 있는 설정과 반드시 주입해야 하는 설정이 구분되어 있는가?
- ConfigMap에 비밀값이 들어가지 않는가?
- Secret manifest나 `.env` 실제 값이 repository에 들어가지 않는가?
- 설정 오류 로그가 secret 값을 그대로 출력하지 않는가?

## Interpretation / 해석

설정 계층은 코드 양을 늘리지만 운영 사고를 줄인다. 값이 어디서 들어오는지 한곳에 모이면 Docker, CI, Kubernetes로 이동할 때 "무엇을 주입해야 하는가"가 문서가 된다.

다만 모든 값을 환경변수로만 밀어 넣을 필요는 없다. route 구성처럼 deploy마다 바뀌지 않는 내부 wiring은 코드에 두고, 배포마다 달라지는 값과 비밀값만 설정 계층으로 빼는 편이 읽기 쉽다.

## Limitations / 한계

- 이 글은 아직 실제 명령 실행 결과를 포함하지 않는다.
- 예제는 `std::env` 기반의 작은 설정 로더이며, `config` crate나 cloud secret manager 연동을 다루지 않는다.
- Kubernetes Secret은 민감값을 구분해 다루는 API object이지, 그 자체로 모든 저장/전송/접근 통제 문제를 해결하지 않는다.
- 실제 발행 전에는 예제 저장소, 실행 명령, 버전, 실패 로그를 추가해야 한다.

## References / 참고자료

- [Twelve-Factor App: Config](https://12factor.net/config)
- [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

## Change Log / 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: 설정/비밀값 경계, Kubernetes ConfigMap/Secret 근거, 재현 절차와 한계를 분리해 수정.
