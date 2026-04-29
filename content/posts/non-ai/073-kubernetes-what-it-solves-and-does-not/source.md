---
layout: single
title: "K8S 01. Kubernetes는 무엇을 해결하고 무엇은 해결하지 않는가"
description: "Kubernetes를 컨테이너 실행 도구가 아니라 원하는 상태를 맞추는 cluster 운영 시스템으로 이해하는 글."
date: 2026-06-29 09:00:00 +0900
lang: ko
translation_key: kubernetes-what-it-solves-and-does-not
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, k8s, cluster, containers, devops]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Docker는 container image를 만들고 실행하는 기본 감각을 준다. Jenkins는 build와 push를 자동화한다. Kubernetes는 그 다음 단계에서 "어떤 containerized workload가 cluster 안에서 어떤 상태로 떠 있어야 하는가"를 선언하고 유지하는 시스템이다.

이 글의 결론은 Kubernetes를 단순한 container 실행 명령 모음으로 보면 안 된다는 것이다. Kubernetes는 배포, 복제, service discovery, rollout 같은 문제를 다루지만, 좋은 image, 좋은 application 설계, storage와 network의 물리 제약까지 자동으로 해결하지는 않는다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: analysis
- 테스트 환경: 작성자 별도 실습 환경에서 실행 확인. OS, 노드 사양, 클러스터 구성은 이 글에 고정하지 않았다.
- 테스트 버전: Kubernetes 공식 문서 2026-04-24 확인본. 문서 사이트는 v1.36 링크를 표시했다.
- 출처 등급: Kubernetes 공식 문서를 사용했다.
- 비고: managed Kubernetes와 온프렘 Kubernetes 비교는 별도 운영 주제다.

## 문제 정의

Kubernetes를 처음 배우면 `kubectl run`, `kubectl apply`, YAML, Pod, Deployment, Service가 한꺼번에 나온다. 이때 Kubernetes가 실제로 해결하는 문제와 해결하지 않는 문제를 구분하지 않으면 모든 운영 문제를 Kubernetes가 알아서 처리할 것처럼 오해하기 쉽다.

이번 글은 Kubernetes를 "container를 많이 실행하는 도구"가 아니라 "cluster의 desired state를 맞추는 시스템"으로 이해하는 데 집중한다.

## 확인된 사실

- Kubernetes Components 문서 기준으로 Kubernetes cluster는 control plane과 하나 이상의 worker node로 구성된다.
  근거: [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
- Kubernetes Components 문서 기준으로 kube-apiserver, etcd, kube-scheduler, kube-controller-manager는 control plane 구성요소로 설명된다.
  근거: [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
- Kubernetes Components 문서 기준으로 kubelet은 node에서 Pod와 container가 실행되도록 보장하는 구성요소다.
  근거: [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
- Kubernetes Objects 문서 기준으로 Kubernetes object는 cluster 상태를 나타내는 persistent entity이며, object 생성은 원하는 상태를 Kubernetes에 말하는 행위다.
  근거: [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- Kubernetes Workloads 문서 기준으로 Kubernetes에서는 workload를 Pod 집합 안에서 실행하며, 보통 Pod를 직접 관리하지 않고 workload resource가 Pod 집합을 대신 관리한다.
  근거: [Workloads](https://kubernetes.io/docs/concepts/workloads/)

Kubernetes가 주로 다루는 영역은 아래와 같다.

```text
desired state 선언
Pod scheduling
replica 유지
rollout과 rollback
Service를 통한 stable endpoint 제공
ConfigMap, Secret, volume 같은 실행 환경 연결
```

## 직접 재현한 결과

- 직접 재현함: 작성자 실습 환경에서 이 글의 주요 명령과 설정 흐름을 확인했다.
- 확인한 결과: 공식 문서 기준으로 cluster 구성요소, object desired state, workload resource의 역할을 확인했다.
- 직접 확인 항목: `kubectl apply`로 Deployment를 만들고 Pod가 생성되는 흐름을 직접 관찰했다.

## 해석 / 의견

내 판단으로는 Kubernetes 학습의 첫 문장은 "container를 실행한다"보다 "원하는 상태를 계속 맞춘다"가 되어야 한다. 이 관점이 있어야 왜 Deployment가 Pod를 만들고, Service가 Pod IP 변화 뒤에 안정적인 endpoint를 제공하는지 이해하기 쉽다.

Kubernetes가 해결하지 않는 것도 분명히 해야 한다. 나쁜 Dockerfile, 느린 application startup, 잘못된 health check, 부적절한 resource request, 불안정한 storage, 깨진 network 설계는 Kubernetes가 자동으로 좋게 바꾸지 않는다.

Kubernetes는 운영을 대신해 주는 도구가 아니라 운영 의도를 API object로 표현하고, control plane이 그 상태에 맞춰 계속 조정하게 만드는 플랫폼에 가깝다.

## 한계와 예외

작성자 실습 환경에서 기본 cluster 흐름을 확인했다. 다만 scheduler 내부 판단, controller reconciliation의 세부 과정, Pod 생성 이벤트의 모든 변형은 관찰 범위에 포함하지 않았다.

Kubernetes 배포 방식은 managed service, kubeadm, kops, kubespray, 경량 배포판에 따라 달라질 수 있다. 이 연재는 온프렘 기초 이해를 위해 kubeadm 중심으로 이어 간다.

## 참고자료

- Kubernetes Docs, [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
- Kubernetes Docs, [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- Kubernetes Docs, [Workloads](https://kubernetes.io/docs/concepts/workloads/)
