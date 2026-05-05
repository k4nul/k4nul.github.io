---
layout: single
title: "Rust Service 24. rollout, rollback, 장애 대응 runbook 만들기"
description: "Rust API 배포에서 Kubernetes rollout 확인, rollback 판단, 장애 대응 runbook을 하나의 운영 절차로 묶는다."
date: 2027-03-02 09:00:00 +09:00
lang: ko
translation_key: rust-api-rollout-rollback-runbook
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

배포 자동화가 있어도 사람은 언제 멈추고 언제 되돌릴지 알아야 한다. `kubectl rollout status`가 성공했다는 사실은 Deployment 관점의 진행 상태를 말해줄 뿐, 서비스 품질이 정상이라는 뜻은 아니다.

이 글에서는 배포 전 확인, 배포 중 관찰, 실패 조건, rollback 명령, 사후 기록 항목을 하나의 runbook으로 묶는다. 목표는 "명령을 외우는 것"이 아니라 장애 중에도 같은 순서로 판단할 수 있게 만드는 것이다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: Ingress로 외부 접근 열고 TLS 경계 이해하기
- 다음 글: OpenTelemetry로 logs, metrics, traces 연결하기
- 이번 글의 범위: Deployment rollout을 관찰하고, 실패 기준에 따라 rollback 또는 중단 결정을 내리는 최소 운영 문서

## 문서 정보

- 작성일: 2026-05-05
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial | analysis
- 테스트 환경: 직접 클러스터 실행 테스트 없음. Kubernetes 공식 문서와 일반 runbook 예시를 기준으로 절차를 정리했다.
- 테스트 버전: Kubernetes 문서 기준. `kubectl`과 클러스터 버전은 고정하지 않았다.
- 출처 성격: 공식 문서

## 문제 정의

앞 글까지 Rust API를 이미지로 만들고, Kubernetes Deployment/Service/Ingress로 배포하는 경계를 만들었다. 이제 남는 문제는 "배포가 잘못되었을 때 무엇을 할 것인가"다.

실패는 여러 모양으로 나타난다.

- 새 ReplicaSet이 뜨지 않는다.
- Pod는 Running이지만 readiness가 실패한다.
- HTTP 5xx 비율이 올라간다.
- latency가 기준을 넘는다.
- 특정 고객 또는 특정 endpoint만 실패한다.
- 새 버전은 정상인데 외부 의존성이 동시에 흔들린다.

이 상황에서 runbook이 없으면 사람마다 다른 명령을 치고, 서로 다른 기준으로 "조금 더 보자"와 "되돌리자"를 판단한다. 운영 문서의 가치는 평상시보다 장애 중에 더 크게 드러난다.

## 확인한 사실

- Kubernetes Deployment는 Pod와 ReplicaSet의 선언적 업데이트를 제공한다. Deployment의 Pod template이 바뀌면 새 rollout이 발생한다.
  근거: [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- Kubernetes 공식 문서는 `kubectl rollout status`, `history`, `undo`, `pause`, `resume`, `restart` 같은 하위 명령을 제공한다.
  근거: [kubectl rollout](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/)
- Kubernetes 공식 문서는 이전 revision으로 되돌릴 때 `kubectl rollout undo deployment/<name>` 또는 `--to-revision`을 사용할 수 있다고 설명한다.
  근거: [Rolling Back to a Previous Revision](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-to-a-previous-revision)
- Kubernetes 공식 문서는 `--record` 플래그가 deprecated 되었고 향후 제거될 수 있다고 안내한다. 변경 원인은 annotation, Git commit, CI run, release note 같은 별도 기록으로 남기는 편이 낫다.
  근거: [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

## 실습 기준

runbook은 배포 전, 배포 중, 실패 판단, rollback, 사후 기록으로 나눈다.

### 배포 전 확인

배포 전에 확인할 것은 "클러스터가 manifest를 받을 수 있는가"와 "되돌릴 기준이 있는가"다.

```bash
kubectl config current-context
kubectl get deployment rust-api -n rust-api
kubectl rollout history deployment/rust-api -n rust-api
kubectl diff -f k8s/deployment.yaml
```

운영 runbook에는 아래 값이 있어야 한다.

| 항목 | 예시 |
| --- | --- |
| 배포 대상 | `rust-api` namespace의 `deployment/rust-api` |
| 새 이미지 | `ghcr.io/example/rust-api:2027.03.02` |
| 이전 이미지 | 현재 Deployment 또는 release note에서 확인 |
| 성공 기준 | rollout 성공, `/ready` 성공, 5xx/latency/error log 기준 이하 |
| 실패 기준 | rollout timeout, readiness 실패 지속, 5xx 급증, 주요 endpoint 실패 |
| 결정권자 | 배포 담당자와 rollback 승인자 |

### 배포 실행과 관찰

```bash
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/rust-api -n rust-api --timeout=180s
kubectl get deployment,replicaset,pod -n rust-api -l app=rust-api
kubectl describe deployment rust-api -n rust-api
```

이 단계에서 `rollout status`만 보지 않는다. Service endpoint와 애플리케이션 응답도 같이 본다.

```bash
kubectl get endpointslice -n rust-api -l kubernetes.io/service-name=rust-api
kubectl logs deployment/rust-api -n rust-api --since=10m
curl -fsS https://api.example.com/ready
```

관측 시스템이 있다면 최소한 아래 신호를 본다.

| 신호 | 판단 |
| --- | --- |
| `ready` Pod 수 | 새 ReplicaSet이 실제로 트래픽을 받을 준비가 되었는가 |
| HTTP 5xx 비율 | 배포 후 오류가 증가했는가 |
| p95/p99 latency | 정상 응답이 느려졌는가 |
| error log | 같은 error code 또는 panic이 반복되는가 |
| DB pool / external dependency | 앱 변경인지 의존성 장애인지 구분할 수 있는가 |

### rollback 판단

rollback은 감정적인 버튼이 아니라 미리 정한 실패 기준을 만족할 때 실행하는 절차다.

예시 기준:

- rollout이 `180s` 안에 끝나지 않는다.
- 새 Pod의 readiness 실패가 5분 이상 지속된다.
- 배포 직후 5xx 비율이 평소 기준의 3배 이상으로 5분 이상 유지된다.
- 주요 사용자 경로가 실패하고, feature flag 또는 설정 변경으로 완화할 수 없다.
- 오류 원인이 새 이미지 또는 새 manifest 변경과 강하게 연결된다.

rollback 전에 history를 확인한다.

```bash
kubectl rollout history deployment/rust-api -n rust-api
kubectl rollout history deployment/rust-api -n rust-api --revision=7
```

이전 revision으로 되돌린다.

```bash
kubectl rollout undo deployment/rust-api -n rust-api
kubectl rollout status deployment/rust-api -n rust-api --timeout=180s
```

특정 revision으로 되돌릴 때는 `--to-revision`을 쓴다.

```bash
kubectl rollout undo deployment/rust-api -n rust-api --to-revision=7
kubectl rollout status deployment/rust-api -n rust-api --timeout=180s
```

## 관찰 결과

직접 클러스터 실행 결과는 포함하지 않았다. 실제 검증 시에는 아래처럼 기록한다.

| 단계 | 기록할 내용 |
| --- | --- |
| 배포 전 | 이전 이미지, 새 이미지, Git commit, CI run, 변경 요약 |
| rollout 중 | `rollout status`, ReplicaSet, Pod 상태, event |
| 서비스 확인 | `/ready`, 대표 API endpoint, Ingress 응답 |
| 관측 확인 | 5xx, latency, error log, trace sample |
| rollback 실행 | 실행 명령, 대상 revision, 실행자, 시간 |
| rollback 후 | 정상화 시간, 남은 영향, 후속 조치 |

사후 기록 템플릿은 짧아도 된다.

```text
Incident: 2027-03-02 rust-api deployment rollback
Start:
End:
New image:
Rolled back to:
Trigger:
Customer impact:
Commands used:
What changed:
What worked:
What failed:
Follow-up:
```

## 해석 / 의견

Kubernetes는 rollout과 rollback 명령을 제공하지만, "언제 되돌릴지"는 알려주지 않는다. 그 판단은 서비스의 SLO, 고객 영향, 데이터 변경 여부, feature flag 가능성, 의존성 상태를 함께 보고 내려야 한다.

특히 Rust API처럼 빠르게 시작하는 서비스도 migration, DB schema, message queue, cache key, 외부 API 계약이 함께 바뀌면 단순 image rollback만으로 복구되지 않을 수 있다. runbook에는 "되돌릴 수 없는 변경"을 별도로 표시해야 한다.

배포 기록은 `kubectl` history에만 의존하지 않는 편이 좋다. revision은 Kubernetes 객체 변화의 기록이고, 운영자가 필요한 맥락은 Git commit, image digest, CI run, release note, 승인자, 변경 이유까지 포함한다.

## 한계와 예외

- 이 글은 Deployment 중심이다. StatefulSet, Job, database migration, message schema 변경 rollback은 별도 절차가 필요하다.
- `kubectl rollout undo`는 Deployment revision history가 남아 있어야 유효하다. `revisionHistoryLimit` 설정과 오래된 ReplicaSet 정리를 확인해야 한다.
- Pod template이 바뀌지 않은 설정 변경은 기대한 revision으로 기록되지 않을 수 있다.
- rollback이 항상 최선은 아니다. 설정 revert, feature flag off, traffic drain, hotfix가 더 안전한 경우가 있다.

## 참고자료

- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [kubectl rollout](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/)
- [Rolling Back to a Previous Revision](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-to-a-previous-revision)
- [kubectl rollout undo](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_undo/)

## 변경 이력

- 2026-05-05: rollout 관찰, rollback 판단 기준, 장애 대응 runbook 템플릿을 공식 문서 기준으로 재작성.
