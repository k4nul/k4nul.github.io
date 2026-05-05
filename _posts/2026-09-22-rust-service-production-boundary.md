---
layout: single
title: "Rust Service 01. Rust 웹 서비스에서 Rust가 책임질 영역 정하기"
description: "Rust 웹 서비스에서 언어, 프레임워크, 인프라, 운영 도구가 각각 맡아야 할 책임을 나누는 기준을 정리한다."
date: 2026-09-22 09:00:00 +09:00
lang: ko
translation_key: rust-service-production-boundary
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

Rust 서비스 운영 커리큘럼의 첫 단계는 코드를 쓰기 전에 책임 경계를 정하는 것이다. Rust와 Axum은 요청을 handler로 연결하고, 타입 경계와 에러 응답을 코드로 표현하며, 실행 가능한 바이너리를 만드는 영역을 맡는다.

반대로 TLS 종료, 프로세스 재시작 정책, 이미지 빌드, 배포 선언, 비밀 주입, 로그 보관은 애플리케이션 코드만으로 보장하기 어렵다. 이 글은 앞으로의 예제에서 Rust 코드, 컨테이너 이미지, CI, Kubernetes, 관측성, 보안 기준을 어디서 나눌지 정하는 기준표 역할을 한다.

## Curriculum Position / 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: 없음. Tauri 후속 블록 다음에 시작하는 새 운영 커리큘럼의 첫 글이다.
- 다음 글: Axum으로 최소 API 서버 만들기
- 보강 기준: 실제 발행 전 예제 저장소, 실행 명령, 사용 버전, 실패 로그를 이 글의 범위에 맞춰 추가한다.

## Document Info / Environment

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: analysis
- 테스트 환경: 직접 실행 테스트 없음. 이 글은 책임 경계 기준을 정리하는 분석 글이며, 특정 예제 서버의 실행 성공을 증명하지 않는다.
- 테스트 버전: 실행 버전 미고정. 검증 기준일에 docs.rs의 Axum latest 페이지는 `0.8.9`로 표시되었고, Docker Build와 Kubernetes Concepts는 공식 문서 기준으로 확인했다.
- 출처 성격: 공식 문서, 원 프로젝트 문서

## Problem Statement / 문제 정의

이 커리큘럼의 목표는 Rust로 API 하나를 만드는 데서 끝나지 않고, 그 API를 빌드하고 배포하고 관측하고 되돌릴 수 있는 운영 단위로 만드는 것이다.

이번 글의 범위는 Rust 웹 서비스에서 Rust가 책임질 영역을 정하는 것이다. 여기서 정한 기준은 뒤의 Docker, CI/CD, Kubernetes, 관측성, 보안 글에서 반복해서 참조한다.

## Verified Facts / 확인한 사실

- Axum 공식 문서는 Axum을 HTTP 라우팅과 요청 처리 라이브러리로 설명하며, 주요 항목으로 routing, handlers, extractors, responses, error handling, middleware, state sharing을 둔다. 따라서 HTTP 요청을 handler로 연결하고 응답 타입으로 바꾸는 경계는 Axum 애플리케이션 코드의 책임으로 볼 수 있다. 근거: [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- Axum 공식 문서는 Axum이 Tokio와 Hyper와 함께 동작하도록 설계되었다고 설명한다. 따라서 비동기 런타임 선택과 TCP listener 구동 방식은 Rust 코드 안에서 명시해야 하는 실행 전제다. 근거: [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- Docker Build 공식 문서는 애플리케이션을 이미지로 포장하고 배포 가능한 산출물로 만드는 역할을 Docker Build의 범위로 설명한다. 따라서 바이너리를 어떤 이미지 layer에 넣고 어떤 base image를 사용할지는 Rust 코드가 아니라 이미지 빌드 책임이다. 근거: [Docker Build documentation](https://docs.docker.com/build/)
- Kubernetes Concepts 문서는 Kubernetes를 컨테이너화된 workload와 service를 선언적 설정과 자동화로 관리하는 플랫폼으로 설명한다. 따라서 replica 수, rollout, service discovery, Pod 설정은 애플리케이션 코드와 분리된 배포 책임이다. 근거: [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)
- 이 글은 특정 cloud provider의 registry, managed Kubernetes, secret manager 동작을 일반 사실로 확장하지 않는다.

## Reproduction Steps / 재현 절차

이 글은 실행 절차를 제공하는 글이 아니라 책임 경계 점검표를 제공하는 글이다. 직접 재현 결과가 필요한 항목은 이후 글에서 별도 명령과 출력으로 기록한다.

발행 전 각 주제는 다음 순서로 확인한다.

1. 이 변경이 Rust 코드, Cargo 설정, Dockerfile, CI workflow, Kubernetes manifest, 운영 runbook 중 어디에 속하는지 적는다.
2. 로컬에서 확인할 명령과 CI에서 반복할 명령을 분리한다.
3. 성공 조건과 실패 조건을 각각 한 줄로 쓴다.
4. 실패했을 때 남아야 할 HTTP 응답, 로그, metric, Kubernetes event를 정한다.
5. secret, token, 개인정보가 로그나 이미지 layer에 남지 않는지 확인한다.

## Observations / 관찰 결과

- 현재 글에는 직접 실행 출력이 없다.
- 검증 가능한 사실은 공식 문서가 설명하는 도구의 책임 범위로 제한했다.
- 이후 글에서 실제 명령을 추가할 때는 `cargo run`, `curl`, `docker build`, `kubectl` 출력처럼 재현 가능한 관찰값을 별도로 기록해야 한다.

## Verification Checklist / 검증 체크리스트

- 코드 변경이 필요한가, 아니면 설정 또는 manifest 변경인가?
- 실패했을 때 HTTP 응답, 로그, metric, Kubernetes event 중 어디에 흔적이 남는가?
- 비밀값, 토큰, 개인정보가 로그나 이미지 layer에 남지 않는가?
- 로컬에서 재현한 명령과 결과를 본문에 기록했는가?
- 공식 문서의 옵션 이름과 예제가 검증 기준일 기준으로 아직 맞는가?

## Interpretation / 해석

Rust API 운영 글은 언어 기능 설명만으로는 부족하다. 실제 운영에서 문제는 대개 코드와 코드 바깥 경계 사이에서 생긴다.

따라서 이번 커리큘럼은 Axum 코드, Docker 이미지, GitHub Actions, Kubernetes manifest, 관측성 신호, 보안 기준을 한 서비스 흐름 안에서 연결한다. 작은 서비스 하나를 끝까지 밀어 보는 편이 개별 도구를 따로 외우는 것보다 운영 판단에 더 도움이 된다.

## Limitations / 한계

- 이 글은 책임 경계 분석 글이며 실제 명령 실행 결과를 포함하지 않는다.
- 특정 cloud provider의 managed Kubernetes, registry, secret manager 동작은 범위 밖이다.
- 실제 발행 전에는 예제 저장소, 실행 명령, 버전, 실패 로그를 추가해야 한다.
- 보안 관련 기준은 조직 정책과 위협 모델에 따라 달라질 수 있다.

## References / 참고자료

- [Axum crate documentation](https://docs.rs/axum/0.8.9/axum/)
- [Docker Build documentation](https://docs.docker.com/build/)
- [Kubernetes Concepts](https://kubernetes.io/docs/concepts/)

## Change Log / 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: 책임 경계, 공식 문서 근거, 재현 여부, 한계를 분리해 수정.
