---
layout: single
title: "K8S 08. requests, limits, probe를 왜 같이 봐야 하는가"
description: "Kubernetes에서 resource requests, limits, liveness/readiness/startup probe를 함께 이해해야 하는 이유를 정리한 글."
date: 2026-07-13 09:00:00 +0900
lang: ko
translation_key: kubernetes-requests-limits-probes
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, resources, requests, limits, probes]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Kubernetes에서 `requests`와 `limits`는 Pod가 node 위에 배치되고 실행될 때의 resource 경계를 만든다. probe는 container가 traffic을 받아도 되는지, 재시작해야 하는지, startup을 기다려야 하는지를 판단하는 신호다.

이 글의 결론은 resource 설정과 probe를 따로 보지 말아야 한다는 것이다. request가 낮으면 배치가 과하게 낙관적일 수 있고, limit가 빡빡하면 application이 느려지거나 죽을 수 있으며, probe가 공격적으로 잡히면 그 현상이 재시작 폭주처럼 보일 수 있다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: analysis
- 테스트 환경: 작성자 별도 실습 환경에서 실행 확인. OS, 노드 사양, 클러스터 구성은 이 글에 고정하지 않았다.
- 테스트 버전: Kubernetes 공식 문서 2026-04-24 확인본. 문서 사이트는 v1.36 링크를 표시했다.
- 출처 등급: Kubernetes 공식 문서를 사용했다.
- 비고: production 값 산정은 application profile과 실제 metric을 기반으로 해야 한다.

## 문제 정의

초기 manifest에서는 아래 문제가 자주 섞여 나타난다.

- `resources`를 비워 둔 채 Pod를 배포한다.
- `requests`와 `limits`를 같은 의미로 생각한다.
- readiness probe와 liveness probe를 같은 endpoint로 둔다.
- startup이 느린 application에 liveness probe를 너무 빨리 실행한다.
- restart가 발생하면 application bug, resource 부족, probe 설정 오류를 구분하지 못한다.

## 확인된 사실

- Kubernetes Resource Management 문서 기준으로 container resource에는 request와 limit을 지정할 수 있다.
  근거: [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- 같은 문서 기준으로 scheduler는 Pod를 배치할 node를 선택할 때 resource request를 사용한다.
  근거: [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- Kubernetes Pod QoS 문서 기준으로 Pod는 resource 설정에 따라 Guaranteed, Burstable, BestEffort QoS class로 분류된다.
  근거: [Pod Quality of Service Classes](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/)
- Kubernetes Probe 문서 기준으로 kubelet은 probe를 통해 container 상태를 주기적으로 진단할 수 있다.
  근거: [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- 같은 문서 기준으로 startup probe가 설정되면 startup probe가 성공하기 전까지 liveness/readiness probe가 실행되지 않는다.
  근거: [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- 같은 문서 기준으로 readiness probe 실패 시 해당 Pod IP는 matching Service의 EndpointSlice에서 ready endpoint로 취급되지 않는다.
  근거: [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)

기본 예시는 아래와 같다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
        - name: app
          image: example/app:1.0.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
          startupProbe:
            httpGet:
              path: /healthz
              port: 8080
            failureThreshold: 30
            periodSeconds: 2
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            periodSeconds: 10
            failureThreshold: 3
```

## 직접 재현한 결과

- 직접 재현함: 작성자 실습 환경에서 이 글의 주요 명령과 설정 흐름을 확인했다.
- 확인한 결과: 공식 문서 기준으로 request, limit, QoS class, startup/readiness/liveness probe의 역할을 확인했다.
- 직접 확인 항목: `kubectl describe pod`, `kubectl get events`, metric 수집, 제한 초과 시 container 상태 변화, readiness 실패 시 endpoint 제외 여부를 확인했다.

## 해석 / 의견

내가 운영 기준으로 먼저 보는 값은 request다. request는 scheduler가 node를 고를 때 보는 신호이므로, 너무 낮게 잡으면 cluster가 실제보다 여유 있다고 판단할 수 있다. 반대로 너무 높으면 배치 가능한 node가 줄어들고 Pending이 늘 수 있다.

limit은 안전장치이지만 성능 설정이기도 하다. memory limit은 application이 예상보다 메모리를 많이 쓸 때 종료로 이어질 수 있고, CPU limit은 처리량과 latency에 영향을 줄 수 있다. 따라서 limit을 "무조건 낮게 잡는 값"으로 보면 안 된다.

probe는 application의 생존 신호를 Kubernetes가 해석할 수 있게 만드는 계약이다. readiness는 traffic 수신 가능 여부, liveness는 재시작 필요 여부, startup은 느린 초기화를 기다리는 용도로 분리해서 보는 편이 안전하다. 특히 liveness probe를 너무 공격적으로 두면 일시적인 지연이 재시작으로 번지고, 재시작이 다시 지연을 만드는 나쁜 순환이 생길 수 있다.

## 한계와 예외

작성자 실습 환경에서 기본 resource와 probe 흐름을 확인했다. 다만 예시의 CPU와 memory 값은 권장값이 아니라 구조를 설명하기 위한 자리표시자다. 실제 값은 metric, peak traffic, startup 시간, GC 특성, 외부 dependency 지연을 보고 정해야 한다.

batch job, queue worker, database, JVM application, Go service, Node.js service는 적절한 request/limit과 probe 전략이 다를 수 있다.

## 참고자료

- Kubernetes Docs, [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- Kubernetes Docs, [Pod Quality of Service Classes](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/)
- Kubernetes Docs, [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
