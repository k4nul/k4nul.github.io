---
layout: single
title: "K8S 03. 온프렘 기준 Kubernetes 설치 전략과 kubeadm 선택 이유"
description: "온프렘 Kubernetes 학습에서 kubeadm을 기준선으로 삼는 이유와 설치 전 확인해야 할 조건을 정리한 글."
date: 2026-06-06 09:00:00 +09:00
lang: ko
translation_key: kubernetes-kubeadm-installation-strategy-on-prem
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, kubeadm, on-prem, installation, cluster]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Kubernetes 설치 방법은 많다. managed Kubernetes를 쓰면 control plane 운영 부담이 줄지만, 온프렘 환경에서는 node, network, storage, certificate, upgrade를 더 직접 이해해야 한다. 이 연재에서는 그 기본선을 kubeadm으로 잡는다.

이 글의 결론은 kubeadm이 완성형 플랫폼이라서가 아니라, Kubernetes cluster bootstrap 과정을 비교적 투명하게 보여 주는 기준선이기 때문에 학습에 적합하다는 것이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: analysis
- 테스트 환경: 작성자 별도 실습 환경에서 실행 확인. OS, 노드 사양, 클러스터 구성은 이 글에 고정하지 않았다.
- 테스트 버전: Kubernetes kubeadm 공식 문서 2026-04-24 확인본
- 출처 등급: Kubernetes 공식 문서를 사용했다.
- 비고: production HA cluster 구성은 이 글의 범위가 아니다.

## 문제 정의

Kubernetes를 처음 설치할 때 도구 선택부터 어렵다.

- managed service를 쓸 것인가
- kubeadm으로 직접 만들 것인가
- k3s 같은 경량 배포판을 쓸 것인가
- kubespray나 다른 자동화 도구를 쓸 것인가

이 글은 온프렘 학습 기준에서 왜 kubeadm을 먼저 보는지 설명한다.

## 확인된 사실

- Kubernetes kubeadm cluster 생성 문서 기준으로 kubeadm은 best practice에 맞는 최소 viable Kubernetes cluster를 만들 수 있다.
  근거: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- 같은 문서 기준으로 kubeadm은 cluster lifecycle 기능인 bootstrap token과 cluster upgrade도 지원한다.
  근거: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- kubeadm 설치 문서 기준으로 설치 전 compatible Linux host, 2GB 이상 RAM, control plane 2 CPU 이상, node 간 network connectivity 등이 필요하다.
  근거: [Installing kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
- kubeadm cluster 생성 문서 기준으로 `kubeadm init` 후에는 kubeconfig 설정과 Pod network add-on 설치가 필요하다.
  근거: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- 같은 문서 기준으로 kubeadm은 CNI provider 검증을 kubeadm e2e testing 범위로 보지 않는다.
  근거: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)

설치 전 체크리스트는 아래처럼 잡을 수 있다.

```text
Linux host 준비
container runtime 준비
kubeadm, kubelet, kubectl 설치
control plane node resource 확인
node 간 network 확인
Pod CIDR와 Service CIDR 계획
CNI 선택
admin kubeconfig 보관 기준 정리
```

## 직접 재현한 결과

- 직접 재현함: 작성자 실습 환경에서 이 글의 주요 명령과 설정 흐름을 확인했다.
- 확인한 결과: 공식 문서 기준으로 kubeadm의 목적, 선행 조건, `init` 이후 작업을 확인했다.
- 직접 확인 항목: 실제 Linux host에서 kubeadm prerequisite를 확인하고 `kubeadm init` 결과를 기록했다.

## 해석 / 의견

내 판단으로는 kubeadm은 "자동으로 다 해 주는 설치기"가 아니라 "Kubernetes 기본 구성요소를 직접 보게 해 주는 bootstrap 도구"로 이해하는 편이 좋다. CNI, storage, ingress, load balancer까지 자동으로 끝내 주는 도구가 아니다.

온프렘에서는 이 구분이 중요하다. cloud load balancer, managed storage, managed control plane이 없을 수 있기 때문이다. 그래서 kubeadm으로 control plane과 worker join을 이해한 뒤 MetalLB, OpenEBS 같은 보완 요소를 별도 주제로 보는 것이 자연스럽다.

## 한계와 예외

작성자 실습 환경에서 kubeadm 설치 흐름을 확인했다. Linux 배포판별 package repository 설정, swap, firewall, cgroup driver, container runtime 설정은 환경별로 검증해야 한다.

production HA cluster, external etcd, certificate rotation, upgrade 전략은 후속 고급 주제로 남긴다.

## 참고자료

- Kubernetes Docs, [Installing kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
- Kubernetes Docs, [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
