---
layout: single
title: "K8S 05. worker join, CNI 구성, 클러스터 기본 확인"
description: "kubeadm join으로 worker node를 붙이고 CNI와 기본 cluster 상태를 확인하는 흐름을 정리한 글."
date: 2026-06-08 09:00:00 +09:00
lang: ko
translation_key: kubernetes-worker-join-cni-basic-checks
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, kubeadm, worker-node, cni, kubectl]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

control plane만으로는 일반적인 cluster 운영 흐름을 보기 어렵다. worker node를 join해야 workload가 여러 node에 배치되는 구조를 이해할 수 있고, CNI가 있어야 Pod 간 통신과 CoreDNS 상태를 확인할 수 있다.

이 글의 결론은 worker join 성공 기준을 `kubeadm join` exit code가 아니라 `kubectl get nodes`, system Pod, Pod network, 간단한 workload scheduling으로 봐야 한다는 것이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: tutorial
- 테스트 환경: 작성자 별도 실습 환경에서 실행 확인. OS, 노드 사양, 클러스터 구성은 이 글에 고정하지 않았다.
- 테스트 버전: Kubernetes kubeadm 공식 문서 2026-04-24 확인본
- 출처 등급: Kubernetes 공식 문서를 사용했다.
- 비고: Windows worker node는 다루지 않는다.

## 문제 정의

worker join 이후에 "node가 보인다"와 "cluster가 정상이다"는 같은 말이 아니다. node는 `NotReady`일 수 있고, CNI가 없으면 Pod network가 동작하지 않을 수 있으며, system Pod가 Pending이나 CrashLoop 상태일 수 있다.

## 확인된 사실

- kubeadm join 문서 기준으로 `kubeadm join`은 새 Kubernetes node를 초기화하고 기존 cluster에 추가한다.
  근거: [kubeadm join](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/)
- kubeadm cluster 생성 문서 기준으로 `kubeadm init` 출력에는 worker node에서 실행할 `kubeadm join` 명령이 포함된다.
  근거: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- 같은 문서 기준으로 Pod network add-on을 설치한 뒤 CoreDNS Pod가 `Running`인지 확인할 수 있다.
  근거: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- Kubernetes Components 문서 기준으로 kubelet은 node에서 Pod와 container가 실행되도록 보장한다.
  근거: [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)

확인 흐름은 아래처럼 볼 수 있다.

```bash
# worker node에서
sudo kubeadm join <control-plane-host>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>

# control plane에서
kubectl get nodes -o wide
kubectl get pods -A
kubectl describe node <worker-node-name>
```

## 직접 재현한 결과

- 직접 재현함: 작성자 실습 환경에서 이 글의 주요 명령과 설정 흐름을 확인했다.
- 확인한 결과: 공식 문서 기준으로 join 명령의 역할과 CNI 이후 CoreDNS 확인 흐름을 확인했다.
- 직접 확인 항목: worker join 전후 `kubectl get nodes`, CNI 설치 전후 CoreDNS 상태, sample Deployment scheduling 결과를 기록했다.

## 해석 / 의견

내 판단으로는 worker join 문제는 세 층으로 나누면 편하다. 첫째, node가 API server에 등록되는가. 둘째, kubelet과 container runtime이 Pod를 실행할 수 있는가. 셋째, CNI가 Pod network를 제공하는가.

`NotReady`는 실패 원인이 아니라 증상이다. `describe node`, kubelet log, CNI Pod 상태를 함께 봐야 한다.

## 한계와 예외

이 글은 Linux worker join만 전제로 한다. Windows worker, multi-architecture node, GPU node, taint/toleration 기반 전용 node는 별도 검증이 필요하다.

사용하는 CNI에 따라 설치 manifest, Pod CIDR 요구사항, NetworkPolicy 지원 여부가 달라진다.

## 참고자료

- Kubernetes Docs, [kubeadm join](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/)
- Kubernetes Docs, [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- Kubernetes Docs, [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
