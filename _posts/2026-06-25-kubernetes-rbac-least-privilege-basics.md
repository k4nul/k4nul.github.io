---
layout: single
title: "Kubernetes RBAC 최소 권한 입문"
description: "Kubernetes RBAC 최소 권한 입문에 대해 공식 문서와 운영 관점으로 확인할 기준, 점검 순서, 한계를 정리한 글."
date: 2026-06-25 09:00:00 +09:00
lang: ko
translation_key: kubernetes-rbac-least-privilege-basics
section: security
topic_key: security-engineering
categories: Security
tags: [security, devsecops, supply-chain-security, cloud-security]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Kubernetes RBAC의 최소 권한은 "필요한 subject에게 필요한 resource와 verb만 binding한다"는 뜻이다. 입문 단계에서는 Role과 ClusterRole, RoleBinding과 ClusterRoleBinding, `apiGroups/resources/verbs`, service account, subresource를 구분하는 것부터 시작하면 된다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: tutorial | analysis
- 테스트 환경: 실행 테스트 없음. Kubernetes RBAC 공식 문서 기준으로 개념과 점검 순서 정리.
- 테스트 버전: Kubernetes 공식 문서 2026-04-29 확인본. 클러스터와 kubectl 로컬 버전은 고정하지 않음.
- 출처 등급: 공식 문서

## 문제 정의

RBAC를 처음 설정할 때 가장 흔한 실수는 `cluster-admin`, `*` resource, `*` verb, ClusterRoleBinding을 편의상 먼저 쓰는 것이다. 이런 설정은 동작은 빨리 만들지만, 새 resource나 subresource가 생겼을 때 의도하지 않은 권한까지 열 수 있다.

이 글은 Kubernetes RBAC를 최소 권한 관점에서 읽는 기준을 정리한다.

## 확인된 사실

- Kubernetes RBAC는 `rbac.authorization.k8s.io` API group을 사용해 권한 결정을 구성한다.
  근거: [Kubernetes RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- Role은 namespace 안의 권한을 정의하고, ClusterRole은 cluster-scoped 권한 또는 여러 namespace에 재사용할 권한을 정의한다.
  근거: [Kubernetes Role and ClusterRole](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-and-clusterrole)
- RBAC 권한은 additive 방식이며 deny rule이 없다.
  근거: [Kubernetes RBAC API objects](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#api-objects)
- 공식 문서는 wildcard resource/verb가 과권한을 만들 수 있으므로 필요한 resource와 verb만 쓰라고 경고한다.
  근거: [Kubernetes RBAC wildcard caution](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#referring-to-resources)
- Pod log는 `pods/log` subresource로 표현한다.
  근거: [Kubernetes RBAC subresource example](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#referring-to-resources)

## 직접 재현한 결과

- 직접 재현 없음: 이 글은 실제 클러스터에 RBAC manifest를 적용한 실험 보고서가 아니다.
- 직접 확인한 범위: 2026-04-29 기준 Kubernetes 공식 문서의 RBAC object와 예시.

## 재현 순서

최소 권한 Role을 만들 때는 아래 순서로 좁힌다.

1. subject를 정한다: user, group, service account 중 누구에게 줄 권한인지 먼저 정한다.
2. namespace 범위를 정한다: 특정 namespace면 Role과 RoleBinding을 우선 검토한다.
3. resource를 정한다: 예를 들어 `pods`, `pods/log`, `configmaps`, `deployments`.
4. verb를 정한다: `get`, `list`, `watch`, `create`, `update`, `patch`, `delete` 중 실제 필요한 것만 둔다.
5. `*`를 피한다: 처음부터 `resources: ["*"]`, `verbs: ["*"]`를 쓰지 않는다.
6. binding한다: Role은 권한 정의이고, RoleBinding은 그 권한을 subject에게 부여하는 객체다.
7. 검증한다: `kubectl auth can-i`로 허용/거부 결과를 확인한다.

예를 들어 애플리케이션 service account가 같은 namespace 안에서 Pod 목록과 Pod 로그만 읽어야 한다면 이렇게 시작할 수 있다.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-log-reader
  namespace: app
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-pod-log-reader
  namespace: app
subjects:
  - kind: ServiceAccount
    name: app-reader
    namespace: app
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: pod-log-reader
```

검증 예시는 다음과 같다.

```bash
kubectl auth can-i get pods --as=system:serviceaccount:app:app-reader -n app
kubectl auth can-i get pods/log --as=system:serviceaccount:app:app-reader -n app
kubectl auth can-i delete pods --as=system:serviceaccount:app:app-reader -n app
```

마지막 명령은 위 Role 기준으로 `no`가 나와야 한다.

## 관찰 결과

- Role/ClusterRole은 "무엇을 할 수 있는가"를 정의하고, RoleBinding/ClusterRoleBinding은 "누가 그 권한을 받는가"를 정의한다.
- ClusterRoleBinding은 권한을 cluster 전체에 부여할 수 있으므로 입문 단계에서는 RoleBinding보다 더 조심해서 써야 한다.
- `pods`를 읽을 수 있다고 항상 `pods/log`를 읽을 수 있는 것은 아니다. subresource는 별도로 생각해야 한다.

## 해석 / 의견

내 판단으로는 RBAC 최소 권한의 출발점은 "읽기 전용 view 권한"이 아니라 "실제 작업에 필요한 API 요청 목록"이다. 같은 읽기 작업이라도 `get pods`, `list pods`, `get pods/log`, `watch deployments`는 서로 다른 권한이다.

의견: 처음에는 namespace Role로 좁게 만들고, 여러 namespace에서 같은 권한이 반복될 때 ClusterRole 재사용을 검토하는 편이 안전하다.

## 한계와 예외

- 실제 권한 평가는 authentication, admission controller, aggregation, API server 설정과 함께 봐야 한다.
- managed Kubernetes는 기본 ClusterRole, service account token, workload identity 동작이 배포 환경별로 다를 수 있다.
- 이 글은 RBAC 입문이며 Pod Security, NetworkPolicy, cloud IAM, secret rotation을 다루지 않는다.

## 참고자료

- [Kubernetes RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Kubernetes RBAC Role and ClusterRole](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-and-clusterrole)
- [Kubernetes RBAC Referring to resources](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#referring-to-resources)
- [Kubernetes Authorization overview](https://kubernetes.io/docs/reference/access-authn-authz/authorization/)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: RBAC 핵심 object, 최소 권한 manifest, 검증 명령, 공식 문서 근거 보강.
