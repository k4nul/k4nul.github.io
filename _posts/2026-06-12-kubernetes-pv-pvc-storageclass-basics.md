---
layout: single
title: "K8S 09. PV, PVC, StorageClass를 어떻게 이해해야 하는가"
description: "Kubernetes persistent storage의 기본 object인 PV, PVC, StorageClass의 관계를 운영 흐름으로 설명한 글."
date: 2026-06-12 09:00:00 +09:00
lang: ko
translation_key: kubernetes-pv-pvc-storageclass-basics
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, storage, pv, pvc, storageclass]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Kubernetes에서 Pod의 filesystem은 기본적으로 container lifecycle에 묶여 있다. application data를 Pod 교체 이후에도 남겨야 한다면 persistent storage를 이해해야 한다. 이때 핵심 object가 `PersistentVolume`, `PersistentVolumeClaim`, `StorageClass`다.

이 글의 결론은 PV를 "storage 실물", PVC를 "사용자의 요청서", StorageClass를 "동적 provisioning 방식"으로 먼저 이해하면 흐름이 단순해진다는 것이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: tutorial
- 테스트 환경: 작성자 별도 실습 환경에서 실행 확인. OS, 노드 사양, 클러스터 구성은 이 글에 고정하지 않았다.
- 테스트 버전: Kubernetes 공식 문서 2026-04-24 확인본. 문서 사이트는 v1.36 링크를 표시했다.
- 출처 등급: Kubernetes 공식 문서를 사용했다.
- 비고: CSI driver별 세부 동작은 이 글의 범위 밖이다.

## 문제 정의

storage를 처음 다룰 때 헷갈리는 지점은 아래와 같다.

- Pod 안 path에 파일을 쓰면 계속 남는다고 생각한다.
- PV와 PVC를 같은 object로 본다.
- StorageClass가 실제 disk 자체라고 오해한다.
- local storage, network storage, cloud block storage의 장애 특성을 구분하지 않는다.
- reclaim policy를 확인하지 않고 데이터를 지우거나 남긴다.

## 확인된 사실

- Kubernetes Persistent Volumes 문서 기준으로 PersistentVolume은 cluster의 storage 조각이며, node가 cluster resource인 것처럼 PV도 cluster resource다.
  근거: [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- 같은 문서 기준으로 PersistentVolumeClaim은 사용자의 storage 요청이다.
  근거: [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- 같은 문서 기준으로 PVC가 생성되면 control plane은 조건에 맞는 PV를 찾아 bind한다.
  근거: [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- 같은 문서 기준으로 matching static PV가 없으면 StorageClass를 기반으로 동적 provisioning을 시도할 수 있다.
  근거: [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- Kubernetes StorageClass 문서 기준으로 StorageClass는 동적으로 생성되는 PV의 reclaim policy와 volume binding mode 같은 동작을 정의할 수 있다.
  근거: [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)

가장 단순한 PVC 예시는 아래와 같다.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 10Gi
```

Pod나 Deployment에서는 PVC를 volume으로 연결한다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 1
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
          volumeMounts:
            - name: data
              mountPath: /var/lib/app
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: app-data
```

## 직접 재현한 결과

- 직접 재현함: 작성자 실습 환경에서 이 글의 주요 명령과 설정 흐름을 확인했다.
- 확인한 결과: 공식 문서 기준으로 PV, PVC, StorageClass, binding, dynamic provisioning의 관계를 확인했다.
- 직접 확인 항목: `kubectl get pvc,pv,storageclass`, `kubectl describe pvc`, Pod 재시작 후 data 유지 여부, reclaim policy 동작을 확인했다.

## 해석 / 의견

처음에는 PV를 직접 작성하기보다 PVC에서 시작하는 편이 이해하기 쉽다. application 개발자 관점에서는 "10Gi storage가 필요하다"는 요청이 PVC이고, cluster 운영자는 그 요청을 어떤 storage backend와 StorageClass로 처리할지 결정한다.

StorageClass는 storage의 품질과 동작을 드러내는 이름이어야 한다. 예를 들어 `fast-ssd`, `backup-retain`, `local-wait` 같은 이름은 단순히 `standard`보다 운영 의도를 더 잘 보여준다. 이름만 보고도 reclaim policy, binding mode, backend 성격을 추정할 수 있어야 실수를 줄일 수 있다.

local volume은 빠르고 단순할 수 있지만 node 장애에 취약할 수 있다. network 또는 replicated storage는 장애 내성이 좋아질 수 있지만 latency, 비용, 운영 복잡도가 늘 수 있다. 따라서 storage 선택은 Kubernetes YAML 문제가 아니라 data durability와 failure domain 문제다.

## 한계와 예외

작성자 실습 환경에서 기본 PVC/PV 흐름을 확인했다. CSI driver별 동작, snapshot, resize, backup, multi-writer access mode, StatefulSet `volumeClaimTemplates`는 storage backend별로 별도 검증이 필요하다. 실제 운영에서는 storage backend 문서와 장애 복구 절차를 함께 확인해야 한다.

예시의 `standard` StorageClass는 cluster마다 없을 수 있다. `kubectl get storageclass`로 실제 class 이름과 default 여부를 먼저 확인해야 한다.

## 참고자료

- Kubernetes Docs, [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- Kubernetes Docs, [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
- Kubernetes Docs, [Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)
