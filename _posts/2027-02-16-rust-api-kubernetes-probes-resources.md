---
layout: single
title: "Rust Service 22. readiness/liveness probe와 resource limit 잡기"
description: "Rust API의 readiness, liveness, startup probe와 Kubernetes CPU/memory requests, limits를 운영 신호 기준으로 정리한다."
date: 2027-02-16 09:00:00 +09:00
lang: ko
translation_key: rust-api-kubernetes-probes-resources
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

Kubernetes probe는 "헬스 체크 URL을 하나 만들었다"로 끝나는 기능이 아니다. readiness는 트래픽을 받아도 되는지 판단하고, liveness는 컨테이너를 재시작해야 하는지 판단한다. startup probe는 느리게 뜨는 프로세스가 liveness에 너무 일찍 죽지 않도록 보호한다.

resource requests와 limits도 단순한 숫자가 아니다. requests는 스케줄링의 기준이고, limits는 실행 중 제약이다. Rust API가 빠르게 뜨고 적은 메모리로 동작하더라도, 근거 없는 limit은 장애를 숨기거나 새 장애를 만들 수 있다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: ConfigMap, Secret, env 주입 기준 정하기
- 다음 글: Ingress로 외부 접근 열고 TLS 경계 이해하기
- 이번 글의 범위: Pod가 트래픽을 받을 수 있는 상태인지, 재시작해야 하는 상태인지, 어느 정도 자원을 요청해야 하는지 정하는 최소 기준

## 문서 정보

- 작성일: 2026-05-05
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial | analysis
- 테스트 환경: 직접 클러스터 실행 테스트 없음. Kubernetes 공식 문서와 일반 manifest 예시를 기준으로 절차를 정리했다.
- 테스트 버전: Kubernetes 문서 기준. `kubectl`, metrics-server, 클러스터 버전은 고정하지 않았다.
- 출처 성격: 공식 문서

## 문제 정의

앞 글까지의 Deployment는 "Pod가 떠 있다"는 수준의 배포였다. 운영에서는 이 상태만으로 부족하다.

서비스가 트래픽을 받기 전에 데이터베이스 연결을 준비해야 할 수 있다. 시작은 되었지만 내부 데드락이나 이벤트 루프 정지로 더 이상 요청을 처리하지 못할 수도 있다. 또는 CPU와 메모리 설정이 없어 한 Pod가 노드 자원을 과하게 쓰거나, 반대로 너무 작은 limit 때문에 정상 요청 중에 OOM으로 죽을 수 있다.

이 글의 목표는 Rust API의 health endpoint를 Kubernetes 신호로 연결하고, resource requests/limits를 "예쁜 기본값"이 아니라 관찰 가능한 운영 가정으로 다루는 것이다.

## 확인한 사실

- Kubernetes 공식 문서는 liveness probe를 컨테이너 재시작 여부 판단에 사용하고, readiness probe를 Pod가 요청을 받을 준비가 되었는지 판단하는 데 사용한다고 설명한다.
  근거: [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- Kubernetes 공식 문서는 startup probe가 있으면 성공하기 전까지 liveness와 readiness probe를 지연시킨다고 설명한다.
  근거: [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- Kubernetes 공식 문서는 컨테이너별로 CPU와 memory requests/limits를 지정할 수 있으며, requests는 필요한 자원량, limits는 사용할 수 있는 최대량으로 다룬다.
  근거: [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- Kubernetes 문서는 메모리 limit을 넘으면 컨테이너가 종료될 수 있고, CPU limit은 CPU 사용을 제한하는 방식으로 동작한다고 설명한다.
  근거: [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

## 실습 기준

Rust API에는 최소 두 종류의 health endpoint를 둔다.

- `/live`: 프로세스가 살아 있고 요청 처리 루프가 응답 가능한지 확인한다. 데이터베이스 같은 외부 의존성은 넣지 않는다.
- `/ready`: 트래픽을 받아도 되는지 확인한다. 데이터베이스 연결, migration 상태, 필수 설정 로드 여부처럼 요청 처리에 필요한 조건을 제한된 timeout 안에서 확인한다.

예를 들어 Axum 라우터는 아래처럼 역할을 나눌 수 있다.

```rust
use axum::{routing::get, Json, Router};
use serde_json::json;

async fn live() -> Json<serde_json::Value> {
    Json(json!({ "status": "ok" }))
}

async fn ready() -> Json<serde_json::Value> {
    // In a real service, check dependencies with a short timeout.
    Json(json!({ "status": "ready" }))
}

pub fn router() -> Router {
    Router::new()
        .route("/live", get(live))
        .route("/ready", get(ready))
}
```

Deployment manifest에서는 probe 의미를 섞지 않는다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rust-api
  namespace: rust-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: rust-api
  template:
    metadata:
      labels:
        app: rust-api
    spec:
      containers:
        - name: rust-api
          image: ghcr.io/example/rust-api:2027.02.16
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            periodSeconds: 10
            timeoutSeconds: 2
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /live
              port: 8080
            periodSeconds: 20
            timeoutSeconds: 2
            failureThreshold: 3
          startupProbe:
            httpGet:
              path: /live
              port: 8080
            periodSeconds: 5
            failureThreshold: 12
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 500m
              memory: 256Mi
```

위 resource 값은 예시다. 이 값은 벤치마크 결과가 아니라 "작은 API의 출발점"을 보여주기 위한 숫자다. 실제 값은 요청량, 응답 크기, DB pool 크기, JSON payload 크기, TLS/압축 위치, 로그량, allocator 동작을 보고 조정해야 한다.

적용 후에는 rollout, Pod 상태, 이벤트를 함께 본다.

```bash
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/rust-api -n rust-api
kubectl get pods -n rust-api
kubectl describe pod -l app=rust-api -n rust-api
kubectl get endpointslice -n rust-api -l kubernetes.io/service-name=rust-api
```

metrics-server가 있는 클러스터라면 실제 사용량도 확인한다.

```bash
kubectl top pod -n rust-api
```

## 관찰 결과

직접 실행 결과는 포함하지 않았다. 실제 검증 시에는 아래 현상을 구분해서 기록한다.

| 상황 | 기대되는 관찰 |
| --- | --- |
| `/ready` 실패 | Pod는 Running이어도 Ready가 아니며 Service endpoint에서 빠질 수 있다 |
| `/live` 반복 실패 | kubelet이 컨테이너를 재시작하고 restart count가 증가한다 |
| startup probe 실패 | 시작 시간 안에 `/live`가 성공하지 못하면 컨테이너가 재시작된다 |
| memory limit 초과 | 컨테이너 종료, OOMKilled 상태 또는 관련 이벤트가 나타날 수 있다 |
| CPU limit 도달 | 재시작보다는 처리 지연, latency 증가, throttling 관찰이 먼저 나타날 수 있다 |
| requests가 노드 여유보다 큼 | Pod가 Pending 상태로 남고 스케줄링 이벤트가 기록될 수 있다 |

## 해석 / 의견

readiness와 liveness를 같은 endpoint로 묶는 것은 편하지만 운영 의미를 흐린다. 데이터베이스가 잠깐 느릴 때 liveness가 실패해서 API Pod를 계속 재시작하면, 회복이 아니라 장애 증폭이 된다. 외부 의존성은 readiness에 두고, liveness는 프로세스 자체가 회복 불가능한 상태인지에 가깝게 좁히는 편이 안전하다.

resource limit도 "넣으면 운영답다"가 아니다. memory limit은 프로세스를 죽일 수 있고, CPU limit은 latency를 망가뜨릴 수 있다. 그래서 처음에는 작은 기준값을 두더라도, 부하 테스트와 운영 관측으로 계속 조정해야 한다.

Rust API는 같은 기능의 동적 런타임 서비스보다 메모리 사용량이 낮을 수 있지만, 그 문장을 일반 사실처럼 쓰면 안 된다. 실제 서비스의 메모리는 payload 크기, DB pool, 캐시, 압축, 로깅, allocator, 동시성 설정에 따라 달라진다.

## 한계와 예외

- 이 글은 HTTP probe 기준이다. gRPC probe, exec probe, TCP socket probe의 세부 선택 기준은 다루지 않는다.
- resource 예시는 벤치마크 결과가 아니다. 실제 운영값은 부하 테스트와 운영 metric으로 다시 잡아야 한다.
- metrics-server가 없는 클러스터에서는 `kubectl top`이 동작하지 않을 수 있다.
- probe endpoint가 인증 미들웨어, rate limit, 외부 API 호출에 막히면 health signal로 부적절할 수 있다.

## 참고자료

- [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Assign Memory Resources to Containers and Pods](https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/)
- [Assign CPU Resources to Containers and Pods](https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/)

## 변경 이력

- 2026-05-05: probe 의미 분리, resource requests/limits 기준, 검증 관찰 지점을 공식 문서 기준으로 재작성.
