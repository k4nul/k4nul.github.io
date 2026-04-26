---
layout: single
title: "K8S 04. control plane 설치와 기본 점검"
description: "kubeadm init 이후 kubeconfig, Pod network, control plane 상태를 어떤 순서로 확인해야 하는지 정리한 글."
date: 2026-06-12 09:00:00 +0900
lang: ko
translation_key: kubernetes-control-plane-install-basic-checks
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, kubeadm, control-plane, kubectl, cni]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

control plane 설치는 `kubeadm init` 한 줄로 끝나지 않는다. init 이후에는 kubeconfig를 사용자 계정에 설정하고, Pod network add-on을 설치하고, system Pod와 node 상태를 확인해야 한다.

이 글의 결론은 control plane 설치 성공 기준을 "명령이 끝났다"가 아니라 "kubectl로 API server에 접근하고, CoreDNS와 control plane Pod 상태를 확인할 수 있다"로 잡아야 한다는 것이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: tutorial
- 테스트 환경: 작성자 별도 실습 환경에서 실행 확인. OS, 노드 사양, 클러스터 구성은 이 글에 고정하지 않았다.
- 테스트 버전: Kubernetes kubeadm 공식 문서 2026-04-24 확인본
- 출처 등급: Kubernetes 공식 문서를 사용했다.
- 비고: HA control plane과 external etcd는 다루지 않는다.

## 문제 정의

초급자는 `kubeadm init`이 끝나면 cluster가 완성됐다고 생각하기 쉽다. 하지만 init 이후에도 kubectl 설정, CNI 설치, system Pod 확인, node 상태 확인이 이어진다.

이번 글은 single control plane 학습 환경에서 기본 점검 순서를 정리한다.

## 확인된 사실

- kubeadm cluster 생성 문서 기준으로 `kubeadm init`은 precheck를 실행한 뒤 control plane component를 다운로드하고 설치한다.
  근거: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- 같은 문서 기준으로 init 완료 후 일반 사용자로 cluster를 사용하려면 `$HOME/.kube/config`에 `/etc/kubernetes/admin.conf`를 복사하고 소유자를 변경하는 명령을 실행한다.
  근거: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- 같은 문서 기준으로 init 이후 Pod network를 cluster에 배포해야 하며, Pod network 설치 후 CoreDNS Pod가 `Running`인지 확인할 수 있다.
  근거: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- Kubernetes Components 문서 기준으로 control plane에는 kube-apiserver, etcd, kube-scheduler, kube-controller-manager가 포함된다.
  근거: [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)

기본 점검 흐름은 아래처럼 잡을 수 있다.

```bash
sudo kubeadm init --pod-network-cidr=<CIDR>
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
kubectl get nodes
kubectl get pods -A
kubectl apply -f <pod-network-add-on.yaml>
kubectl get pods -A
```

## 직접 재현한 결과

- 직접 재현함: 작성자 실습 환경에서 이 글의 주요 명령과 설정 흐름을 확인했다.
- 확인한 결과: 공식 문서 기준으로 `kubeadm init` 이후 kubeconfig 설정과 Pod network 설치가 필요하다는 점을 확인했다.
- 직접 확인 항목: 실제 control plane node에서 init 출력, node 상태, CoreDNS 상태, CNI 설치 전후 차이를 기록했다.

## 해석 / 의견

내 판단으로는 control plane 설치 점검에서 가장 중요한 기준은 "API server에 kubectl로 접근되는가"다. 그 다음은 "node가 Ready가 되는가"와 "CoreDNS가 Running이 되는가"다.

Pod network가 없으면 control plane 설치가 끝나도 cluster가 workload를 정상 실행할 준비가 되지 않는다. 따라서 CNI 선택은 설치 후 남는 부속 작업이 아니라 cluster 설계의 일부로 봐야 한다.

## 한계와 예외

작성자 실습 환경에서 control plane 설치와 기본 점검 흐름을 확인했다. container runtime, swap, firewall, cgroup driver, OS package repository 설정은 환경별로 검증해야 한다.

single control plane 구성은 학습에는 좋지만 production 고가용성 기준을 만족하지 않는다.

## 참고자료

- Kubernetes Docs, [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- Kubernetes Docs, [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
