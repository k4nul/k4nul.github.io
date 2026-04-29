---
layout: single
title: "K8S 06. 첫 manifest 작성 Pod, Deployment, Service"
description: "Kubernetes manifest의 기본 필드와 Pod, Deployment, Service 예제를 처음 쓰는 순서로 정리한 글."
date: 2026-07-09 09:00:00 +09:00
lang: ko
translation_key: kubernetes-first-manifests-pod-deployment-service
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, manifest, pod, deployment, service]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Kubernetes manifest는 cluster에 원하는 상태를 전달하는 YAML이다. 모든 manifest를 한 번에 외우기보다 `apiVersion`, `kind`, `metadata`, `spec`을 먼저 보고, Pod에서 Deployment로, Deployment에서 Service로 확장하는 편이 이해하기 쉽다.

이 글의 결론은 실제 application 배포의 기본 단위를 Pod 단독이 아니라 Deployment와 Service 조합으로 봐야 한다는 것이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: tutorial
- 테스트 환경: 작성자 별도 실습 환경에서 실행 확인. OS, 노드 사양, 클러스터 구성은 이 글에 고정하지 않았다.
- 테스트 버전: Kubernetes 공식 문서 2026-04-24 확인본
- 출처 등급: Kubernetes 공식 문서를 사용했다.
- 비고: namespace, ConfigMap, Secret, Ingress는 다음 글에서 다룬다.

## 문제 정의

초급자가 manifest를 작성할 때 자주 겪는 문제는 아래와 같다.

- `kind`만 바꾸면 같은 구조라고 생각한다.
- label과 selector의 연결을 놓친다.
- Pod를 직접 만들고 scale이나 rollout을 기대한다.
- Service `port`와 `targetPort`를 헷갈린다.

## 확인된 사실

- Kubernetes Objects 문서 기준으로 거의 모든 Kubernetes object에는 원하는 상태를 설명하는 `spec`과 현재 상태를 설명하는 `status`가 있다.
  근거: [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- 같은 문서 기준으로 object 생성 시 `apiVersion`, `kind`, `metadata`, `spec` 같은 필드가 필요하다.
  근거: [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- Pods 문서 기준으로 Pod는 Kubernetes의 가장 작은 deployable unit이다.
  근거: [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- Deployment 문서 기준으로 Deployment는 Pod와 ReplicaSet에 대한 declarative update를 제공한다.
  근거: [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- Service 문서 기준으로 Service는 selector로 선택한 Pod 집합을 network endpoint로 노출할 수 있다.
  근거: [Service](https://kubernetes.io/docs/concepts/services-networking/service/)

첫 manifest는 아래 순서로 읽는다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-nginx
  template:
    metadata:
      labels:
        app: hello-nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
          ports:
            - containerPort: 80
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-nginx
spec:
  selector:
    app: hello-nginx
  ports:
    - port: 80
      targetPort: 80
```

## 직접 재현한 결과

- 직접 재현함: 작성자 실습 환경에서 이 글의 주요 명령과 설정 흐름을 확인했다.
- 확인한 결과: 공식 문서 기준으로 object 필드, Deployment, Service의 역할을 확인했다.
- 직접 확인 항목: `kubectl apply -f`, `kubectl get deploy,pod,svc`, `kubectl describe svc`로 selector와 endpoint 연결을 확인했다.

## 해석 / 의견

내 판단으로는 첫 manifest에서 가장 중요한 줄은 image보다 label과 selector다. Deployment의 Pod template label과 Service selector가 맞지 않으면 Pod는 떠 있어도 Service가 traffic을 보낼 대상이 없다.

Pod manifest는 학습에는 좋지만 application 운영의 기본값은 Deployment로 보는 편이 좋다. 그래야 replica, rollout, rollback 같은 Kubernetes의 장점을 이어서 배울 수 있다.

## 한계와 예외

작성자 실습 환경에서 manifest 적용 흐름을 확인했다. 다만 `nginx:1.27` image pull 가능 여부, Service endpoint 생성, Pod scheduling은 registry 상태와 cluster 환경에 따라 달라질 수 있다.

production manifest에는 resource request/limit, probe, securityContext, namespace, imagePullPolicy, rollout strategy 같은 요소가 추가로 필요하다.

## 참고자료

- Kubernetes Docs, [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- Kubernetes Docs, [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- Kubernetes Docs, [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- Kubernetes Docs, [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
