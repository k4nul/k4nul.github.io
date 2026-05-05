---
layout: single
title: "Rust Service 20. Kubernetes Deployment와 Service로 배포하기"
description: "Rust API 컨테이너를 Kubernetes Deployment와 Service로 배포하는 최소 manifest 경계를 정리한다."
date: 2027-02-02 09:00:00 +09:00
lang: ko
translation_key: rust-api-kubernetes-deployment-service
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

Kubernetes에 올린다는 말은 컨테이너 하나를 실행한다는 말이 아니라 원하는 replica 상태와 네트워크 접근 지점을 선언한다는 뜻이다.

Deployment는 Pod replica의 desired state와 rollout을 관리하고, Service는 Pod 앞에 안정적인 접근 지점을 만든다. 처음 manifest에서는 이 두 책임을 섞지 않는 것이 중요하다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: SBOM과 image scan 결과 읽기
- 다음 글: ConfigMap, Secret, env 주입 기준 정하기
- 보강 기준: 실제 발행 전 로컬 Kubernetes 환경에서 `kubectl apply`, rollout 확인, Service endpoint 확인, port-forward health check, 실패 event를 기록한다.

## 문서 정보

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial / Kubernetes manifest 경계 설계
- 테스트 환경: 직접 Kubernetes cluster 실행 없음. 이 글은 Deployment와 Service manifest의 최소 경계를 정리한다.
- 확인한 문서: Kubernetes v1.36 문서의 Deployment, Service, port-forward, kubectl reference
- 출처 성격: Kubernetes 공식 문서

## 문제 정의

Docker image를 만들고 scan까지 확인했다면 다음 단계는 Kubernetes에 배포하는 것이다. 하지만 처음부터 Ingress, TLS, ConfigMap, Secret, probes, resource limits, HPA를 모두 붙이면 어떤 문제가 어느 계층에서 생겼는지 보기 어렵다.

이번 글에서는 두 가지 질문만 다룬다.

- Deployment가 원하는 수의 Rust API Pod를 만들고 유지하는가?
- Service가 label selector로 그 Pod들을 안정적으로 가리키는가?

ConfigMap, Secret, probes, resources, Ingress는 뒤 글에서 단계적으로 붙인다.

## 확인한 사실

- Kubernetes Deployment 문서는 Deployment가 Pod와 ReplicaSet에 대한 declarative update를 제공한다고 설명한다.
- Deployment controller는 Deployment를 관찰해 원하는 Pod를 올리기 위한 ReplicaSet을 만든다.
- Kubernetes Deployment 문서는 selector와 Pod template label을 적절히 지정해야 하며, selector가 다른 controller와 겹치면 예기치 않은 동작이 생길 수 있다고 경고한다.
- Kubernetes Service 문서는 Service를 application을 network service로 노출하는 방법으로 설명한다.
- Service는 일반적으로 selector를 사용해 Pod 접근을 추상화한다.
- Kubernetes Service에는 ClusterIP, NodePort, LoadBalancer 같은 type이 있으며, 처음 내부 확인에는 ClusterIP와 `kubectl port-forward`가 단순하다.

## 최소 Manifest

처음 manifest는 의도적으로 작게 둔다. image는 tag보다 digest를 쓰는 편이 재현성에 유리하지만, 예시에서는 읽기 쉽게 tag 형태를 사용한다. 실제 배포 기록에는 digest를 남긴다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rust-api
  labels:
    app: rust-api
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
          image: ghcr.io/org/rust-api:v0.3.0
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 3000
---
apiVersion: v1
kind: Service
metadata:
  name: rust-api
  labels:
    app: rust-api
spec:
  type: ClusterIP
  selector:
    app: rust-api
  ports:
    - name: http
      port: 80
      targetPort: http
```

이 manifest는 운영 완성본이 아니다. probes, resources, securityContext, config, secret, ingress는 빠져 있다. 먼저 Deployment와 Service의 기본 연결만 검증한다.

## 필드 경계

처음에는 각 필드가 어느 책임을 갖는지 설명할 수 있어야 한다.

| 필드 | 위치 | 의미 |
| --- | --- | --- |
| `spec.replicas` | Deployment | 유지하려는 Pod 수 |
| `spec.selector.matchLabels` | Deployment | Deployment가 관리할 Pod label |
| `template.metadata.labels` | Deployment Pod template | 새 Pod에 붙을 label |
| `containers.image` | Pod template | 실행할 image |
| `containerPort` | Pod template | container가 listen하는 port 문서화 |
| `spec.selector` | Service | Service가 traffic을 보낼 Pod label |
| `ports.port` | Service | Service가 노출하는 port |
| `ports.targetPort` | Service | Pod container port 또는 named port |

Deployment selector와 Pod template label이 맞지 않으면 Deployment가 Pod를 제대로 관리하지 못한다. Service selector와 Pod label이 맞지 않으면 Service endpoint가 비어 있을 수 있다.

## 재현 순서

발행 전에는 실제 cluster에서 아래 결과를 기록한다. namespace는 예시로 `rust-api`를 사용한다.

1. namespace를 만들고 manifest를 적용한다.

```powershell
kubectl create namespace rust-api
kubectl apply -n rust-api -f k8s/deployment-service.yaml
```

2. Deployment rollout을 확인한다.

```powershell
kubectl rollout status deployment/rust-api -n rust-api
kubectl get deploy,rs,pods -n rust-api -l app=rust-api
```

3. Service와 endpoint를 확인한다.

```powershell
kubectl get service rust-api -n rust-api
kubectl get endpointslice -n rust-api -l kubernetes.io/service-name=rust-api
```

4. port-forward로 cluster 내부 Service를 로컬에서 확인한다.

```powershell
kubectl port-forward service/rust-api 8080:80 -n rust-api
curl.exe -i http://127.0.0.1:8080/health
```

5. 문제가 있으면 event와 로그를 확인한다.

```powershell
kubectl describe deployment rust-api -n rust-api
kubectl describe pod -n rust-api -l app=rust-api
kubectl logs -n rust-api -l app=rust-api --tail=100
```

## 실패를 읽는 기준

Kubernetes 실패는 한 줄로 끝나지 않는다.

| 증상 | 먼저 볼 곳 | 흔한 원인 |
| --- | --- | --- |
| Pod가 안 만들어짐 | `kubectl describe deployment` | selector/template label 불일치, quota, admission 거부 |
| Pod가 `ImagePullBackOff` | `kubectl describe pod` | image 이름, tag/digest, registry auth 문제 |
| Pod가 반복 재시작 | `kubectl logs`, `describe pod` | app bind address, env 누락, runtime crash |
| Service 접속 실패 | `get endpointslice`, Service selector | Service selector와 Pod label 불일치 |
| port-forward 실패 | Service selector, Pod readiness, API server 권한 | endpoint 없음, selector 없는 Service |

이번 글에서는 readiness probe를 아직 붙이지 않지만, Service가 실제 traffic을 보내도 되는 Pod를 고르는 기준은 다음 단계에서 꼭 다룬다.

## 관찰 상태

이 글에는 아직 실제 cluster 실행 결과가 없다. 발행 전에는 다음 값을 추가해야 한다.

- Kubernetes server version과 kubectl version
- 사용한 namespace
- `kubectl apply` 결과
- `kubectl rollout status` 결과
- Deployment, ReplicaSet, Pod 목록
- Service와 EndpointSlice 상태
- port-forward 후 `/health` 응답
- 실패 event 예시 하나

## 검증 체크리스트

- Deployment와 Service가 한 파일 안에 있더라도 책임이 분리되어 있는가?
- Deployment selector와 Pod template label이 일치하는가?
- Service selector와 Pod label이 일치하는가?
- container가 실제로 `0.0.0.0:3000` 같은 cluster 접근 가능한 주소에서 listen하는가?
- image tag/digest와 release 기록이 연결되어 있는가?
- `kubectl rollout status`와 Service endpoint 확인을 모두 기록했는가?
- port-forward health check로 application 응답까지 확인했는가?
- 아직 다루지 않은 probes/resources/config/secret/ingress 범위를 명시했는가?

## 해석 / 의견

Deployment와 Service는 Kubernetes 배포의 가장 작은 운영 단위다. Deployment만 있으면 Pod는 뜰 수 있지만 안정적인 접근 지점이 없고, Service만 있으면 traffic을 보낼 Pod가 없다.

처음부터 모든 운영 옵션을 붙이면 YAML은 그럴듯해지지만 실패 원인을 읽기 어려워진다. Deployment가 Pod를 만들고, Service가 그 Pod를 가리키고, `/health`가 응답하는 것까지 확인한 뒤 다음 설정을 붙이는 편이 안전하다.

## 한계와 예외

- 이 글은 실제 cluster에서 실행하지 않은 manifest 설계 글이다.
- probes, resources, ConfigMap, Secret, Ingress, TLS, NetworkPolicy는 뒤 글의 범위다.
- LoadBalancer Service 동작은 cloud provider 또는 bare-metal load balancer 구성에 따라 달라진다.
- private registry image pull은 imagePullSecret과 registry 권한 설정이 필요하며 이 글에서는 다루지 않는다.

## 참고자료

- [Kubernetes: Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes: Service](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Kubernetes: Use port forwarding to access applications](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)
- [Kubernetes: kubectl reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands)

## 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: Deployment/Service 책임 경계, 최소 manifest, label/selector 검증, rollout/endpoint/port-forward 재현 절차를 Kubernetes 공식 문서 기준으로 보강.
