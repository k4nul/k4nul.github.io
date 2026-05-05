---
layout: single
title: "Rust Service 27. 장애를 일부러 만들고 describe, events, logs로 추적하기"
description: "Rust API 배포에서 image pull 실패, readiness 실패, 설정 누락을 일부러 만들고 kubectl describe, events, logs로 계층별 원인을 좁힌다."
date: 2027-03-23 09:00:00 +09:00
lang: ko
translation_key: rust-api-kubernetes-failure-debugging
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

장애 대응은 실제 장애가 난 뒤 처음 배우기에는 너무 비싸다. 작은 실패를 일부러 만들고, Kubernetes가 어떤 흔적을 남기는지 읽는 연습이 필요하다.

이 글에서는 image pull 실패, readiness 실패, 설정 누락을 예시로 삼아 `kubectl rollout status`, `kubectl describe`, `kubectl events`, `kubectl logs`를 어떤 순서로 볼지 정리한다. 핵심은 명령을 많이 치는 것이 아니라 실패 계층을 좁히는 것이다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: Prometheus 기준으로 어떤 metric을 남길지 정하기
- 다음 글: non-root container와 최소 권한 실행 기준
- 이번 글의 범위: Kubernetes에서 Rust API Pod가 실패할 때 workload, Pod event, container log, Service endpoint를 순서대로 확인하는 연습

## 문서 정보

- 작성일: 2026-05-05
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial | analysis
- 테스트 환경: 직접 클러스터 실행 테스트 없음. Kubernetes 공식 문서와 일반적인 실패 재현 manifest를 기준으로 정리했다.
- 테스트 버전: Kubernetes 문서 기준. `kubectl`과 클러스터 버전은 고정하지 않았다.
- 출처 성격: 공식 문서

## 문제 정의

Kubernetes 장애는 한 화면에서 끝나지 않는다. 같은 "서비스가 안 된다"라는 증상도 원인은 다를 수 있다.

- image 이름이 틀려서 컨테이너를 pull하지 못한다.
- Pod는 Running이지만 readiness probe가 실패해 Service endpoint에서 빠진다.
- Secret이나 ConfigMap key가 없어 컨테이너 시작이 실패한다.
- 앱은 정상인데 Service selector가 틀려 endpoint가 비어 있다.
- Ingress host가 맞지 않아 backend로 요청이 가지 않는다.

이번 글은 완전한 장애 대응 매뉴얼이 아니다. 작은 실패를 의도적으로 만들고, Kubernetes가 남긴 증거를 같은 순서로 읽는 연습이다.

## 확인한 사실

- Kubernetes Debug Pods 문서는 Pod 디버깅의 첫 단계로 Pod 상태와 최근 event를 확인하기 위해 `kubectl describe pods ${POD_NAME}`를 사용하라고 안내한다.
  근거: [Kubernetes Debug Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
- `kubectl events` 공식 reference는 namespace 또는 특정 resource에 대한 event를 표시할 수 있다고 설명한다.
  근거: [kubectl events](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_events/)
- Kubernetes logging 문서는 컨테이너가 stdout/stderr에 쓴 로그를 kubelet과 logging pipeline이 다루며, `kubectl logs` 같은 built-in tool로 확인할 수 있다고 설명한다.
  근거: [Kubernetes Logging Architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
- Kubernetes Debug Running Pods 문서는 실행 중인 Pod를 조사할 때 `kubectl exec`, ephemeral container 같은 방법도 다루지만, 이 글에서는 먼저 describe/events/logs로 좁히는 흐름에 집중한다.
  근거: [Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)

## 실습 기준

먼저 기준 상태를 확인한다.

```bash
kubectl get deployment rust-api -n rust-api
kubectl rollout status deployment/rust-api -n rust-api --timeout=120s
kubectl get pod -n rust-api -l app=rust-api
kubectl get endpointslice -n rust-api -l kubernetes.io/service-name=rust-api
```

실패를 볼 때는 아래 순서를 고정한다.

```bash
kubectl rollout status deployment/rust-api -n rust-api --timeout=120s
kubectl get pod -n rust-api -l app=rust-api
kubectl describe pod -n rust-api -l app=rust-api
kubectl events -n rust-api --for deployment/rust-api
kubectl logs deployment/rust-api -n rust-api --since=10m
kubectl get endpointslice -n rust-api -l kubernetes.io/service-name=rust-api
```

### 실패 1: image pull 실패

일부러 존재하지 않는 tag를 배포한다.

```bash
kubectl set image deployment/rust-api rust-api=ghcr.io/example/rust-api:not-exist -n rust-api
kubectl rollout status deployment/rust-api -n rust-api --timeout=120s
```

확인 지점:

```bash
kubectl get pod -n rust-api -l app=rust-api
kubectl describe pod -n rust-api -l app=rust-api
kubectl events -n rust-api --types=Warning
```

기대되는 해석은 애플리케이션 로그가 아니라 image pull 단계에서 실패했다는 것이다. 이때 `kubectl logs`는 컨테이너가 시작하지 않았기 때문에 유용하지 않을 수 있다.

### 실패 2: readiness 실패

readiness probe path를 틀리게 만든다.

```yaml
readinessProbe:
  httpGet:
    path: /not-ready
    port: 8080
  periodSeconds: 10
  timeoutSeconds: 2
  failureThreshold: 3
```

확인 지점:

```bash
kubectl rollout status deployment/rust-api -n rust-api --timeout=120s
kubectl describe pod -n rust-api -l app=rust-api
kubectl get endpointslice -n rust-api -l kubernetes.io/service-name=rust-api
kubectl logs deployment/rust-api -n rust-api --since=10m
```

기대되는 해석은 컨테이너는 실행되지만 Ready가 아니어서 Service endpoint에서 빠질 수 있다는 것이다. 앱 로그에는 `/not-ready` 요청이나 probe 실패와 연결되는 단서가 남을 수 있다.

### 실패 3: ConfigMap 또는 Secret key 누락

Deployment가 존재하지 않는 key를 참조하게 만든다.

```yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: rust-api-secret
        key: DATABASE_URL_MISSING
```

확인 지점:

```bash
kubectl describe deployment rust-api -n rust-api
kubectl describe pod -n rust-api -l app=rust-api
kubectl events -n rust-api --for deployment/rust-api
kubectl events -n rust-api --types=Warning
```

기대되는 해석은 코드 내부 오류가 아니라 Kubernetes가 컨테이너 환경 구성을 완료하지 못했다는 것이다.

## 관찰 결과

직접 실행 결과는 포함하지 않았다. 실제 검증 시 아래 표처럼 기록한다.

| 실패 | 먼저 볼 곳 | 로그가 유용한가 | 대표 해석 |
| --- | --- | --- | --- |
| image pull 실패 | Pod event, describe | 대개 아님 | 이미지 이름, tag, registry 권한 문제 |
| readiness 실패 | describe, endpoint, logs | 예 | 앱은 실행되지만 트래픽 받을 준비가 안 됨 |
| 설정 key 누락 | describe, event | 대개 아님 | ConfigMap/Secret 참조 문제 |
| 앱 panic | logs, restart count | 예 | 코드 또는 런타임 설정 문제 |
| Service selector 오류 | Service, EndpointSlice | 아님 | Pod와 Service label 연결 문제 |

## 해석 / 의견

`kubectl logs`는 익숙해서 먼저 치기 쉽지만, 컨테이너가 시작하지 못한 장애에서는 빈손일 수 있다. image pull, scheduling, secret mount, env injection 문제는 Pod event와 describe가 더 빠른 길이다.

반대로 컨테이너가 Running이고 readiness만 실패한다면 logs와 endpoint를 같이 봐야 한다. 앱이 실제로 probe 요청을 받았는지, route가 있는지, 외부 의존성 timeout이 있는지 확인해야 하기 때문이다.

장애 디버깅은 "정답 명령"이 아니라 계층 순서다. Deployment rollout, ReplicaSet, Pod state, event, container log, Service endpoint, Ingress 순서로 좁히면 같은 장애라도 팀이 같은 언어로 이야기할 수 있다.

## 한계와 예외

- 이 글은 의도적 실패 연습이다. 실제 장애에서는 node pressure, DNS, CNI, admission webhook, quota, cloud load balancer 같은 계층도 확인해야 한다.
- `kubectl events` 출력과 event retention은 클러스터 설정과 버전에 따라 달라질 수 있다.
- 여러 container가 있는 Pod에서는 `kubectl logs`에 `-c`를 지정해야 한다.
- 운영에서 일부러 실패를 만들 때는 production namespace가 아니라 실습용 namespace를 사용해야 한다.

## 참고자료

- [Kubernetes Debug Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
- [Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)
- [kubectl events](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_events/)
- [Kubernetes Logging Architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
- [Kubernetes Debug Services](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/)

## 변경 이력

- 2026-05-05: 의도적 실패 재현과 describe/events/logs 관찰 순서를 공식 문서 기준으로 재작성.
