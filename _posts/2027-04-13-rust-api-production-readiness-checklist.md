---
layout: single
title: "Rust Service 30. 운영 체크리스트: 배포 전 무엇을 확인해야 하는가"
description: "Rust API를 운영 환경에 올리기 전 기능, 설정, 보안, 관측성, 롤백 기준을 하나의 체크리스트로 묶는다."
date: 2027-04-13 09:00:00 +09:00
lang: ko
translation_key: rust-api-production-readiness-checklist
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

이 시리즈의 마지막 글은 새 기능을 추가하지 않는다. 대신 지금까지 만든 Rust API가 배포 가능한 운영 단위인지 확인한다.

좋은 체크리스트는 "열심히 확인했다"가 아니라 "배포를 멈출 조건이 무엇인지"를 알려 준다. 그래서 이 글은 코드, 설정, 이미지, Kubernetes manifest, 관측성, 보안, 롤백을 하나의 배포 전 표로 묶는다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: Kubernetes RBAC를 서비스 운영 관점에서 다시 보기
- 다음 글: 없음. 이 글이 30주제 커리큘럼의 마무리다.

## 문서 정보

- 작성일: 2026-05-05
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial | analysis
- 테스트 환경: 문서 검토 기준. 실제 발행 전 예제 저장소, CI 실행 결과, 이미지 digest, Kubernetes 배포 결과를 함께 기록해야 한다.
- 테스트 버전: 이 글에서는 특정 버전을 고정하지 않는다. 발행 전 Rust, Docker, GitHub Actions, Kubernetes, 관측성 도구 버전을 기록한다.
- 출처 성격: Kubernetes 공식 문서, Docker 공식 문서, GitHub Actions 공식 문서, 운영 해석

## 문제 정의

운영 준비는 느낌으로 판단하면 흔들린다. 테스트가 통과했지만 Secret이 로그에 찍힐 수 있고, 이미지가 빌드됐지만 non-root 실행이 깨질 수 있으며, Deployment가 적용됐지만 롤백 명령이 준비되지 않았을 수 있다.

이 체크리스트는 완벽한 보안 감사를 대신하지 않는다. 다만 작은 Rust API를 운영 환경에 올리기 전에 반드시 확인해야 할 최소 기준을 한 장으로 고정한다.

## 확인한 사실

- Kubernetes 공식 문서는 production environment 구성을 별도의 주제로 다룬다.
- Kubernetes 보안 문서는 Pod Security Standards, Security Context, ServiceAccount, RBAC, Secret 관리, 보안 체크리스트를 별도 항목으로 제공한다.
- Docker Build 문서는 이미지 빌드, 캐시, 빌드 컨텍스트, 멀티 플랫폼 빌드 등 운영 이미지 제작 기준을 제공한다.
- GitHub Actions 보안 문서는 workflow 권한, secret 취급, third-party action 사용 등 CI 보안 고려사항을 다룬다.
- 위 사실은 2026-05-05 기준 공식 문서로 확인했다.

## 배포 전 체크리스트

| 영역 | 확인할 것 | 멈출 조건 |
| --- | --- | --- |
| 코드 품질 | `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`가 CI에서 통과한다. | 경고를 무시하거나 로컬에서만 통과했다. |
| API 계약 | 요청/응답 schema, 오류 응답, validation 실패 응답이 문서와 맞다. | 클라이언트가 의존하는 필드가 설명 없이 바뀌었다. |
| 설정 | 필수 환경 변수가 문서화되어 있고 기본값과 운영값이 분리되어 있다. | 운영 Secret이나 URL이 코드, 이미지, 로그에 들어간다. |
| 데이터베이스 | migration 적용 순서와 롤백 가능성이 기록되어 있다. | 배포 후 되돌릴 수 없는 schema 변경인데 승인 기록이 없다. |
| 이미지 | 멀티스테이지 빌드, `.dockerignore`, non-root `USER`, image digest, SBOM 또는 scan 결과가 확인된다. | `latest`만 배포하거나 root 실행이 남아 있다. |
| Kubernetes manifest | Deployment, Service, ConfigMap, Secret 참조, probe, resource request/limit, securityContext가 함께 검토된다. | probe나 resource 기준 없이 replica만 늘린다. |
| 네트워크 | Ingress, TLS, CORS, request size, rate limit 기준이 명시되어 있다. | 외부 노출 경로가 문서와 다르다. |
| 관측성 | 구조화 로그, metric, trace, dashboard, alert가 같은 route/service label을 공유한다. | 실패해도 어느 신호를 볼지 정해져 있지 않다. |
| 보안 권한 | 런타임 ServiceAccount, CI 배포 권한, 운영자 조회 권한이 분리되어 있다. | 런타임 Pod에 불필요한 API 토큰이나 `cluster-admin` 성격 권한이 있다. |
| 롤아웃 | `kubectl rollout status` 확인 기준과 실패 시 중단 조건이 있다. | 배포 완료를 HTTP 헬스 체크 없이 적용 성공만으로 판단한다. |
| 롤백 | 직전 image digest, migration 영향, `kubectl rollout undo` 가능 여부가 기록되어 있다. | 되돌릴 버전과 명령이 배포 전에 없다. |

## 명령 기준

체크리스트는 말로 끝나면 약하다. CI와 운영자가 반복할 명령을 남긴다.

```bash
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```

이미지는 tag보다 digest를 기준으로 배포 결과를 남긴다.

{% raw %}
```bash
docker build -t ghcr.io/example/rust-api:1.0.0 .
docker image inspect ghcr.io/example/rust-api:1.0.0 --format '{{.Id}} {{.Config.User}}'
```
{% endraw %}

Kubernetes 배포 전에는 manifest가 서버 기준 schema에 맞는지 확인한다.

```bash
kubectl apply --dry-run=server -f k8s/
kubectl diff -f k8s/
```

배포 중에는 rollout과 health check를 같이 본다.

```bash
kubectl rollout status deployment/rust-api -n rust-api
kubectl get pods -n rust-api -l app.kubernetes.io/name=rust-api
kubectl logs deployment/rust-api -n rust-api --tail=100
```

권한은 RBAC 글에서 다룬 것처럼 `can-i` 결과를 남긴다.

```bash
kubectl auth can-i get secrets \
  --as=system:serviceaccount:rust-api:rust-api-runtime \
  -n rust-api
```

이 서비스 기준에서 기대값은 `no`다.

## Go / No-Go 판정

| 판정 | 의미 |
| --- | --- |
| Go | 코드 테스트, 이미지 기준, manifest 검증, 관측성, 롤백 계획이 모두 충족됐다. |
| Conditional Go | 위험이 작고 되돌릴 수 있으며, 소유자와 만료 시간이 있는 예외로 기록됐다. |
| No-Go | 데이터 손실, Secret 노출, 복구 불가 migration, 권한 과다, 관측 불가 장애 가능성이 남아 있다. |

`Conditional Go`는 편의 문구가 아니다. 예외에 소유자, 제거 조건, 확인 날짜가 없으면 사실상 `No-Go`로 다루는 편이 안전하다.

## 배포 기록에 남길 것

배포가 끝나면 다음 정보를 한곳에 남긴다.

- 배포한 Git commit SHA
- 배포한 image tag와 digest
- 실행한 migration 목록
- `kubectl rollout status` 결과
- health check 결과
- 주요 dashboard 링크 또는 screenshot 위치
- 발생한 alert와 대응 기록
- 롤백 여부와 이유

이 기록은 다음 장애 대응에서 시간을 줄인다. "그때 무엇을 배포했는가"를 기억에 맡기지 않게 해 준다.

## 한계와 예외

- 이 체크리스트는 일반적인 Rust API 운영 기준이다. 결제, 의료, 개인정보, 금융처럼 규제 요구가 있는 시스템은 별도의 감사와 통제 절차가 필요하다.
- Managed Kubernetes, registry, secret manager, observability backend의 세부 기능은 공급자마다 다르다.
- 체크리스트 통과는 장애가 없다는 보장이 아니다. 다만 장애를 탐지하고 되돌릴 준비가 되어 있는지 확인한다.

## 참고자료

- [Kubernetes: Production environment](https://kubernetes.io/docs/setup/production-environment/)
- [Kubernetes: Security Checklist](https://kubernetes.io/docs/concepts/security/security-checklist/)
- [Kubernetes: Application Security Checklist](https://kubernetes.io/docs/concepts/security/application-security-checklist/)
- [Docker Build documentation](https://docs.docker.com/build/)
- [GitHub Actions: Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)

## 변경 이력

- 2026-05-05: 기본 틀을 정리하고 배포 전 Go/No-Go 체크리스트, 검증 명령, 배포 기록 기준을 추가했다.
