---
layout: single
title: "K8S 02. Pod, Deployment, ReplicaSet, Service를 운영 흐름으로 이해하기"
description: "Kubernetes의 Pod, Deployment, ReplicaSet, Service를 개별 암기보다 운영 흐름으로 연결해 설명한 글."
date: 2026-06-05 09:00:00 +09:00
lang: ko
translation_key: kubernetes-pod-deployment-replicaset-service
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, pod, deployment, replicaset, service]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Pod, Deployment, ReplicaSet, Service는 따로 외우면 헷갈린다. 운영 흐름으로 보면 Deployment가 원하는 application 상태를 선언하고, ReplicaSet이 Pod 수를 맞추며, Pod가 container 실행 단위가 되고, Service가 바뀌는 Pod 뒤에 안정적인 접근 지점을 제공한다.

이 글의 결론은 초급자가 Pod를 직접 만드는 것보다 Deployment와 Service의 관계를 먼저 이해해야 한다는 것이다.

## 예시: Deployment와 Service를 한 번에 보기

이 예시는 로컬 실습용이다. 이미 `kubectl`이 클러스터에 연결되어 있고, 실습용 namespace에 리소스를 만들 수 있다고 가정한다. 운영 환경에서는 image tag, resource request/limit, readiness/liveness probe, namespace, label 정책을 별도로 정해야 한다.

`demo-nginx.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-nginx
  labels:
    app.kubernetes.io/name: demo-nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app.kubernetes.io/name: demo-nginx
  template:
    metadata:
      labels:
        app.kubernetes.io/name: demo-nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: demo-nginx
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: demo-nginx
  ports:
    - name: http
      port: 80
      targetPort: 80
```

적용한다.

```bash
kubectl apply -f demo-nginx.yaml
```

정상 상태를 확인한다.

```bash
kubectl get deployment demo-nginx
kubectl get rs -l app.kubernetes.io/name=demo-nginx
kubectl get pods -l app.kubernetes.io/name=demo-nginx
kubectl get service demo-nginx
```

정상 결과 예시:

```text
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
demo-nginx   2/2     2            2           30s

NAME                    READY   STATUS    RESTARTS   AGE
demo-nginx-<hash>-<id>   1/1     Running   0          30s
demo-nginx-<hash>-<id>   1/1     Running   0          30s
```

위 출력에서 Deployment는 원하는 replica 수를 보여 주고, ReplicaSet은 Pod 이름의 중간 hash로 나타나며, Pod는 실제 container 실행 상태를 보여 준다. Service는 Pod IP가 바뀌어도 `demo-nginx`라는 안정적인 접근 지점을 제공한다.

상세 원인을 볼 때는 `describe`와 `logs`를 나눠 쓴다.

```bash
kubectl describe deployment demo-nginx
kubectl describe pod -l app.kubernetes.io/name=demo-nginx
kubectl logs deployment/demo-nginx --all-pods=true --tail=20
```

실패할 경우 대표 상태 예시:

```text
STATUS             의미
ImagePullBackOff   image 이름, tag, registry 인증 문제를 먼저 본다.
CrashLoopBackOff   container process가 시작 후 반복 종료되는지 logs를 본다.
Pending            node resource, taint/toleration, PVC binding 문제를 describe events에서 본다.
```

정리한다.

```bash
kubectl delete -f demo-nginx.yaml
```

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-06-05
- 문서 성격: analysis
- 테스트 환경: 작성자 별도 실습 환경에서 실행 확인. OS, 노드 사양, 클러스터 구성은 이 글에 고정하지 않았다.
- 테스트 버전: Kubernetes 공식 문서 2026-06-05 확인본
- 출처 등급: Kubernetes 공식 문서를 사용했다.
- 비고: StatefulSet, DaemonSet, Job은 이 글의 범위에서 제외한다. 위 출력은 독자 확인용 예시 출력이며, 실제 클러스터의 hash, Pod 이름, AGE는 달라진다.

## 문제 정의

Kubernetes 초급 단계에서 가장 흔한 혼란은 "왜 container를 바로 실행하지 않고 Pod, Deployment, Service 같은 object를 거치는가"이다.

이 글은 네 object를 아래 질문으로 연결한다.

- 무엇이 실제 container 실행 단위인가
- 누가 Pod 수를 맞추는가
- 누가 rollout을 관리하는가
- 누가 안정적인 network endpoint를 제공하는가

## 확인된 사실

- Kubernetes Pods 문서 기준으로 Pod는 Kubernetes에서 만들고 관리할 수 있는 가장 작은 deployable computing unit이다.
  근거: [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- 같은 문서 기준으로 Pod는 일반적으로 직접 만들지 않고 workload resource를 통해 만들어진다.
  근거: [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- Kubernetes Deployment 문서 기준으로 Deployment는 application workload를 실행할 Pod 집합을 관리하고, Pods와 ReplicaSets에 declarative update를 제공한다.
  근거: [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- Kubernetes ReplicaSet 문서 기준으로 ReplicaSet의 목적은 특정 시점에 안정적인 replica Pod 집합을 유지하는 것이다. 일반적으로 Deployment가 ReplicaSet을 자동 관리하도록 둔다.
  근거: [ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
- Kubernetes Service 문서 기준으로 Service는 cluster 안에서 하나 이상의 Pod로 실행되는 network application을 노출하는 방법이다.
  근거: [Service](https://kubernetes.io/docs/concepts/services-networking/service/)

운영 흐름은 아래처럼 볼 수 있다.

```text
Deployment manifest apply
Deployment controller creates or updates ReplicaSet
ReplicaSet maintains desired Pod count
Pods run containers
Service selects Pods and provides stable endpoint
```

## 직접 재현한 결과

- 직접 재현함: 작성자 실습 환경에서 이 글의 주요 명령과 설정 흐름을 확인했다.
- 확인한 결과: 공식 문서 기준으로 네 object의 역할과 권장 사용 흐름을 확인했다.
- 직접 확인 항목: nginx Deployment와 Service를 만들고 ReplicaSet과 Pod가 어떤 이름으로 생성되는지 관찰했다.

## 해석 / 의견

내 판단으로는 초급자가 가장 먼저 버려야 할 습관은 Pod를 "서버 한 대"처럼 보는 것이다. Pod는 ephemeral하고 교체될 수 있다. 그래서 Service가 필요하고, 그래서 Deployment가 필요하다.

Deployment를 기준으로 보면 rollout과 rollback을 이해하기 쉬워진다. image tag가 바뀌면 Deployment의 Pod template이 바뀌고, 새 ReplicaSet이 생기며, Pod가 점진적으로 교체된다.

Service는 "현재 살아 있는 Pod 목록"을 사람이 추적하지 않게 해 준다. application이 Pod IP를 직접 기억하지 않도록 하는 추상화다.

## 한계와 예외

작성자 실습 환경에서 기본 object 생성 흐름을 확인했다.

ReplicaSet을 직접 다뤄야 하는 특수한 경우가 있을 수 있지만, 일반 application 배포에서는 Deployment를 우선 사용하는 편이 이해와 운영에 유리하다.

운영 환경에서는 이 글의 최소 manifest만으로 충분하지 않다. 최소한 image tag 고정, resource request/limit, probe, namespace 분리, RBAC, NetworkPolicy, 배포/롤백 절차를 추가로 검토해야 한다.

## 함께 읽을 글

- [DevOps 운영 흐름](/devops/)
- [Docker 컨테이너와 VM 차이](/devops/docker-containers-vs-vms/)
- [Dockerfile과 build context 이해하기](/devops/dockerfile-basics-and-build-context/)
- [Jenkins는 무엇이고 왜 아직도 많이 쓰이는가](/devops/jenkins-what-and-why-still-used/)

## 참고자료

- Kubernetes Docs, [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- Kubernetes Docs, [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- Kubernetes Docs, [ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
- Kubernetes Docs, [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
- Kubernetes Docs, [kubectl get](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/)
- Kubernetes Docs, [kubectl describe](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_describe/)
- Kubernetes Docs, [kubectl logs](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/)
