---
layout: single
title: "K8S 10. 온프렘 번외 MetalLB와 OpenEBS는 언제 필요한가"
description: "온프렘 Kubernetes에서 LoadBalancer와 persistent storage 공백을 이해하기 위해 MetalLB와 OpenEBS의 역할을 정리한 글."
date: 2026-07-17 09:00:00 +0900
lang: ko
translation_key: kubernetes-bare-metal-metallb-openebs
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, bare-metal, metallb, openebs, on-prem]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

cloud Kubernetes에서는 `Service type: LoadBalancer`와 동적 storage provisioning이 provider 기능과 자연스럽게 이어지는 경우가 많다. 온프렘 또는 bare metal Kubernetes에서는 그 연결이 자동으로 주어지지 않을 수 있다. 이때 검토 후보로 자주 나오는 도구가 MetalLB와 OpenEBS다.

이 글의 결론은 MetalLB와 OpenEBS를 "Kubernetes 필수 구성요소"가 아니라 온프렘에서 비어 있는 network load balancer와 storage provisioning 영역을 보완하는 선택지로 봐야 한다는 것이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: analysis
- 테스트 환경: 작성자 별도 실습 환경에서 실행 확인. OS, 노드 사양, 클러스터 구성은 이 글에 고정하지 않았다.
- 테스트 버전: Kubernetes 공식 문서, MetalLB 공식 문서, OpenEBS 4.4.x 공식 문서 2026-04-24 확인본.
- 출처 등급: Kubernetes, MetalLB, OpenEBS 공식 문서를 사용했다.
- 비고: network 설계, BGP, storage 성능, backup/restore 검증은 별도 운영 검증이 필요하다.

## 문제 정의

온프렘 Kubernetes에서는 아래 질문이 빠르게 나온다.

- `LoadBalancer` Service를 만들었는데 external IP가 왜 생기지 않는가?
- NodePort만으로 운영 traffic을 받아도 되는가?
- Ingress controller 앞단에는 어떤 IP가 붙어야 하는가?
- PVC를 만들면 실제 disk가 어디서 생기는가?
- local disk를 써도 data durability를 만족할 수 있는가?

## 확인된 사실

- Kubernetes Service 문서 기준으로 Service에는 ClusterIP, NodePort, LoadBalancer 같은 type이 있다.
  근거: [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
- MetalLB 공식 문서 기준으로 MetalLB는 bare metal Kubernetes cluster를 위한 load balancer 구현체이며 표준 routing protocol을 사용한다.
  근거: [MetalLB](https://metallb.io/)
- MetalLB 공식 문서 기준으로 Kubernetes는 bare metal cluster에 대해 network load balancer 구현을 제공하지 않으며, 지원되는 IaaS platform이 아니면 LoadBalancer가 pending 상태로 남을 수 있다.
  근거: [MetalLB](https://metallb.io/)
- MetalLB Usage 문서 기준으로 MetalLB 설치와 설정 후 Service의 `spec.type`을 `LoadBalancer`로 만들면 외부 노출을 처리할 수 있다.
  근거: [MetalLB Usage](https://metallb.io/usage/index.html)
- Kubernetes Persistent Volumes 문서 기준으로 PVC와 PV binding, StorageClass 기반 dynamic provisioning은 storage 운영의 기본 흐름이다.
  근거: [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- OpenEBS 4.4.x 문서 기준으로 OpenEBS는 Kubernetes worker node의 storage를 Local 또는 Replicated Persistent Volume으로 제공한다.
  근거: [OpenEBS Documentation](https://openebs.io/docs)
- OpenEBS Local Storage 문서 기준으로 Local Storage는 single node에만 접근 가능하며, node가 unhealthy해지면 해당 local volume도 접근 불가능해질 수 있다.
  근거: [OpenEBS Local Storage](https://openebs.io/docs/concepts/data-engines/localstorage)

역할을 단순화하면 아래와 같다.

```text
외부 traffic 문제
Service type LoadBalancer -> cloud provider 또는 MetalLB 같은 구현체 필요

persistent storage 문제
PVC -> StorageClass -> CSI/provisioner -> 실제 volume
온프렘 local/replicated storage 후보 중 하나: OpenEBS
```

## 직접 재현한 결과

- 직접 재현함: 작성자 실습 환경에서 이 글의 주요 명령과 설정 흐름을 확인했다.
- 확인한 결과: 공식 문서 기준으로 MetalLB와 OpenEBS가 각각 보완하는 영역을 확인했다.
- 직접 확인 항목: `kubectl get svc`, LoadBalancer external IP 할당, `kubectl describe svc`, `kubectl get storageclass,pvc,pv`, Pod 재스케줄링 시 volume 접근 가능 여부를 확인했다.

## 해석 / 의견

MetalLB는 "Ingress 대체제"라기보다 bare metal cluster에서 `LoadBalancer` type Service가 external IP를 얻도록 돕는 구성요소로 보는 편이 정확하다. Ingress controller를 운영하더라도, 그 controller의 Service를 외부에 안정적으로 노출해야 하므로 MetalLB가 앞단 IP 문제를 풀어 줄 수 있다.

OpenEBS는 "Kubernetes에서 storage를 쓰기 위한 유일한 답"이 아니다. 이미 NFS, SAN, Ceph, Longhorn, cloud CSI, storage appliance가 있다면 다른 선택이 더 맞을 수 있다. OpenEBS는 worker node의 local 또는 replicated storage를 Kubernetes 방식으로 다루고 싶을 때 검토할 수 있는 선택지다.

온프렘에서는 도구 선택보다 먼저 failure domain을 정해야 한다. network는 IP 대역, routing, ARP/BGP, 장애 시 failover를 봐야 하고, storage는 node 장애, disk 장애, backup, restore, data consistency를 봐야 한다. 이 질문에 답하지 않은 채 MetalLB나 OpenEBS부터 설치하면 "동작은 하는데 운영 기준이 없는 cluster"가 되기 쉽다.

## 한계와 예외

작성자 실습 환경에서 기본 역할과 확인 흐름을 검증했다. MetalLB의 L2 mode와 BGP mode 차이, IPAddressPool 설계, router 설정, ARP/NDP 동작은 network 환경별로 별도 검증이 필요하다. OpenEBS도 Local PV, LVM, ZFS, Replicated Storage의 성능과 장애 복구는 별도 비교가 필요하다.

managed Kubernetes나 cloud 환경에서는 provider가 LoadBalancer와 storage provisioning을 이미 제공할 수 있다. 그 경우 MetalLB나 OpenEBS가 필요하지 않을 수 있다.

## 참고자료

- Kubernetes Docs, [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
- Kubernetes Docs, [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- Kubernetes Docs, [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
- MetalLB Docs, [MetalLB](https://metallb.io/)
- MetalLB Docs, [Usage](https://metallb.io/usage/index.html)
- OpenEBS Docs, [OpenEBS Documentation](https://openebs.io/docs)
- OpenEBS Docs, [Local Storage](https://openebs.io/docs/concepts/data-engines/localstorage)
