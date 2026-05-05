---
layout: single
title: "Rust Service 29. Kubernetes RBAC를 서비스 운영 관점에서 다시 보기"
description: "Rust API 운영에서 ServiceAccount, Role, RoleBinding, 배포 권한을 최소 권한 관점으로 다시 정리한다."
date: 2027-04-06 09:00:00 +09:00
lang: ko
translation_key: rust-api-kubernetes-rbac-service-operations
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

Rust API가 Kubernetes API를 직접 호출하지 않는다면, 런타임 Pod에는 Kubernetes 리소스를 읽고 바꾸는 권한이 필요하지 않다.

운영 관점에서 RBAC를 읽을 때 핵심은 `ServiceAccount`, `Role`, `RoleBinding` 이름을 외우는 것이 아니다. 런타임 권한, CI 배포 권한, 운영자 조회 권한을 서로 다른 주체로 나누고, 각 주체가 실제로 해야 하는 동작만 허용하는 것이다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: non-root container와 최소 권한 실행 기준
- 다음 글: 운영 체크리스트: 배포 전 무엇을 확인해야 하는가

## 문서 정보

- 작성일: 2026-05-05
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial | analysis
- 테스트 환경: 문서 검토 기준. 아래 명령은 실제 예제 클러스터에서 재현해야 하는 검증 명령이다.
- 테스트 버전: 이 글에서는 특정 Kubernetes 버전을 고정하지 않는다. 발행 전 대상 클러스터의 Kubernetes와 `kubectl` 버전을 함께 기록한다.
- 출처 성격: Kubernetes 공식 문서, 운영 해석

## 문제 정의

Kubernetes에서 권한은 자주 "일단 붙여 보고 되면 유지"되는 식으로 커진다. 하지만 API 서버에 접근할 수 있는 권한은 장애 대응과 보안 사고의 반경을 동시에 키운다.

이 글의 기준 서비스는 일반적인 Axum 기반 Rust API다. 이 서비스는 HTTP 요청을 처리하고 데이터베이스나 외부 API에 접근하지만, Kubernetes Deployment나 Secret을 직접 읽을 필요는 없다. 그렇다면 런타임 ServiceAccount는 Kubernetes API 토큰을 자동으로 받을 이유도 작다.

## 확인한 사실

- Kubernetes RBAC는 `Role`, `ClusterRole`, `RoleBinding`, `ClusterRoleBinding`을 사용해 API 권한을 부여한다.
- RBAC 권한은 허용 규칙을 더하는 방식이다. 거부 규칙을 별도로 작성해 권한을 빼는 모델이 아니다.
- `Role`은 특정 namespace 안의 리소스 권한을 정의한다. `ClusterRole`은 cluster 범위 리소스에 쓸 수 있고, `RoleBinding`이 참조하면 특정 namespace 안에서만 권한을 줄 수 있다.
- ServiceAccount는 Pod 같은 워크로드가 Kubernetes API에 인증할 때 사용하는 Kubernetes 내부 계정이다.
- `kubectl auth can-i`는 특정 주체가 특정 동작을 할 수 있는지 확인하는 데 사용할 수 있다.
- 위 사실은 2026-05-05 기준 Kubernetes 공식 문서로 확인했다.

## 권한을 세 주체로 나눈다

운영에서 먼저 나눌 주체는 세 가지다.

| 주체 | 예시 이름 | 해야 하는 일 | 하지 말아야 할 일 |
| --- | --- | --- | --- |
| 런타임 Pod | `rust-api-runtime` | Rust API 프로세스 실행 | Secret 조회, Deployment 수정, Pod 목록 조회 |
| CI/CD 배포자 | `rust-api-deployer` | 정해진 namespace의 Deployment 갱신 | cluster 전체 권한, Secret 전체 조회 |
| 운영자 조회 계정 | `rust-api-reader` | Pod, Event, 로그 조회 | 리소스 수정, Secret 값 조회 |

이 분리는 귀찮아 보이지만 사고 범위를 줄인다. API 컨테이너가 침해되어도 배포 권한이 바로 노출되지 않고, CI 권한이 잘못 설정되어도 운영자 조회 권한과 섞이지 않는다.

## 런타임 ServiceAccount

서비스가 Kubernetes API를 호출하지 않는다면 런타임 ServiceAccount는 권한을 갖지 않아도 된다. 더 나아가 Pod에 ServiceAccount 토큰이 자동으로 마운트되지 않도록 명시한다.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rust-api-runtime
  namespace: rust-api
automountServiceAccountToken: false
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rust-api
  namespace: rust-api
spec:
  template:
    spec:
      serviceAccountName: rust-api-runtime
      automountServiceAccountToken: false
      containers:
        - name: api
          image: ghcr.io/example/rust-api:1.0.0
```

여기에는 `RoleBinding`이 없다. 그 자체가 의도다. 런타임 API는 Kubernetes API 권한 없이도 동작해야 한다.

검증은 다음처럼 한다.

```bash
kubectl auth can-i get pods \
  --as=system:serviceaccount:rust-api:rust-api-runtime \
  -n rust-api
```

기대값은 `no`다. 애플리케이션이 Kubernetes API를 사용하지 않는 구조라면 이 결과가 정상이다.

## 운영자 조회 권한

운영자는 장애 대응을 위해 Pod, Event, 로그를 읽어야 할 수 있다. 하지만 읽기 권한도 무제한이면 커진다. 특히 `secrets`의 `get`, `list`, `watch`는 신중해야 한다.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: rust-api-reader
  namespace: rust-api
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log", "events", "services", "endpoints"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: rust-api-reader
  namespace: rust-api
subjects:
  - kind: ServiceAccount
    name: rust-api-reader
    namespace: rust-api
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: rust-api-reader
```

조회 권한은 장애 분석을 위한 권한이다. 배포 수정 권한과 같은 계정에 넣지 않는다.

## CI 배포 권한

CI가 해야 하는 일은 더 좁다. 예를 들어 이미지 태그나 digest를 바꾸는 배포 파이프라인이라면 `Deployment`를 `get`, `patch`, `update`할 수 있으면 충분할 수 있다.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: rust-api-deployer
  namespace: rust-api
rules:
  - apiGroups: ["apps"]
    resources: ["deployments"]
    resourceNames: ["rust-api"]
    verbs: ["get", "patch", "update"]
  - apiGroups: ["apps"]
    resources: ["replicasets"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: rust-api-deployer
  namespace: rust-api
subjects:
  - kind: ServiceAccount
    name: rust-api-deployer
    namespace: rust-api
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: rust-api-deployer
```

`resourceNames`를 사용하면 특정 Deployment로 권한 범위를 더 좁힐 수 있다. 다만 모든 동작에 항상 맞는 것은 아니므로 실제 배포 명령이 어떤 API 호출을 하는지 확인해야 한다.

배포 계정은 다음처럼 검증한다.

```bash
kubectl auth can-i patch deployment/rust-api \
  --as=system:serviceaccount:rust-api:rust-api-deployer \
  -n rust-api
```

이 명령은 `yes`가 나와야 한다. 반대로 Secret 조회는 `no`가 나와야 한다.

```bash
kubectl auth can-i get secrets \
  --as=system:serviceaccount:rust-api:rust-api-deployer \
  -n rust-api
```

## 피해야 할 설정

`cluster-admin`을 서비스 배포 편의용으로 붙이는 것은 거의 항상 과하다. `*` 리소스와 `*` verb도 마찬가지다.

특히 다음 패턴은 리뷰에서 멈춰야 한다.

- 런타임 Pod와 CI가 같은 ServiceAccount를 사용한다.
- API 컨테이너가 이유 없이 ServiceAccount 토큰을 마운트한다.
- namespace 하나만 필요한데 `ClusterRoleBinding`을 사용한다.
- 로그 조회를 위해 Secret 전체 조회 권한까지 부여한다.
- 임시 장애 대응 권한에 만료 조건이나 제거 이슈가 없다.

RBAC는 나중에 "빼는" 방식으로 정리하기 어렵다. 허용 규칙이 쌓이는 구조라서 처음부터 작게 시작하는 편이 낫다.

## 운영 체크리스트

- 런타임 ServiceAccount에 `automountServiceAccountToken: false`가 설정되어 있는가?
- 런타임 ServiceAccount에 불필요한 `RoleBinding`이 없는가?
- CI 배포 권한은 대상 namespace와 대상 리소스로 제한되어 있는가?
- 운영자 조회 권한은 수정 권한과 분리되어 있는가?
- `secrets` 조회 권한이 필요한 이유가 문서화되어 있는가?
- `kubectl auth can-i` 결과가 배포 전 증거로 남아 있는가?

## 한계와 예외

- Kubernetes Operator처럼 API 서버를 직접 호출하는 프로그램은 이 글의 런타임 기준과 다르게 설계해야 한다.
- Managed Kubernetes의 클라우드 IAM 연동, OIDC federation, external secret manager 권한 모델은 제품마다 다르므로 별도 검토가 필요하다.
- `kubectl auth can-i`는 권한 판단을 확인하는 도구이지, 실제 워크로드가 의도한 요청만 한다는 증명은 아니다.

## 참고자료

- [Kubernetes: Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Kubernetes: Service Accounts](https://kubernetes.io/docs/concepts/security/service-accounts/)
- [Kubernetes: Configure Service Accounts for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)

## 변경 이력

- 2026-05-05: 기본 틀을 정리하고 런타임, CI, 운영자 권한 분리 기준과 검증 명령을 추가했다.
