---
layout: single
title: "K8S 09. Understanding PV, PVC, and StorageClass"
description: "A practical explanation of Kubernetes persistent storage through PersistentVolume, PersistentVolumeClaim, and StorageClass."
date: 2026-07-16 09:00:00 +09:00
lang: en
translation_key: kubernetes-pv-pvc-storageclass-basics
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, storage, pv, pvc, storageclass]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/kubernetes-pv-pvc-storageclass-basics/
---

## Summary

In Kubernetes, a Pod filesystem is usually tied to the container lifecycle. If application data must survive Pod replacement, you need persistent storage. The core objects are `PersistentVolume`, `PersistentVolumeClaim`, and `StorageClass`.

The conclusion of this post is that the flow becomes simpler when you first think of PV as the storage resource, PVC as the user's request, and StorageClass as the dynamic provisioning policy.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: tutorial
- Test environment: verified in the author's separate practice environment. OS, node details, and cluster topology are not fixed in this post.
- Test version: Kubernetes official documentation checked on 2026-04-24. The documentation site displayed v1.36 links.
- Source level: Kubernetes official documentation.
- Note: CSI driver-specific behavior is outside this post.

## Problem Definition

Kubernetes storage is confusing at first because:

- It is easy to assume files written inside a Pod will remain forever.
- PV and PVC look like the same concept.
- StorageClass can be mistaken for the physical disk itself.
- Local storage, network storage, and cloud block storage have different failure characteristics.
- Reclaim policy can delete or retain data depending on configuration.

## Verified Facts

- According to Kubernetes Persistent Volumes documentation, a PersistentVolume is a piece of storage in the cluster, and PVs are cluster resources just like nodes are cluster resources.
  Evidence: [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- According to the same documentation, a PersistentVolumeClaim is a user's request for storage.
  Evidence: [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- According to the same documentation, after a PVC is created, the control plane looks for a matching PV and binds them.
  Evidence: [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- According to the same documentation, if no matching static PV exists, the cluster can try dynamic provisioning based on StorageClasses.
  Evidence: [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- According to Kubernetes StorageClass documentation, a StorageClass can define behavior such as reclaim policy and volume binding mode for dynamically created PVs.
  Evidence: [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)

A minimal PVC example:

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

A Pod or Deployment mounts the PVC as a volume.

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

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow in the author's practice environment.
- Confirmed result: based on official documentation, I verified the relationship between PV, PVC, StorageClass, binding, and dynamic provisioning.
- Directly verified items: `kubectl get pvc,pv,storageclass`, `kubectl describe pvc`, data persistence after Pod restart, and reclaim policy behavior.

## Interpretation / Opinion

At the beginning, it is easier to start from PVC rather than writing PVs directly. From an application developer's perspective, a PVC says "I need 10Gi of storage." The cluster operator decides which backend and StorageClass should satisfy that request.

StorageClass names should communicate storage quality and behavior. Names such as `fast-ssd`, `backup-retain`, or `local-wait` show operational intent better than a generic `standard`. Ideally, the name should help readers infer reclaim policy, binding mode, and backend characteristics.

Local volumes can be fast and simple, but they can be vulnerable to node failure. Network or replicated storage can improve resilience, but may add latency, cost, and operational complexity. Storage selection is not just a YAML question; it is a data durability and failure domain question.

## Limits and Exceptions

The basic PVC/PV flow was checked in the author's practice environment. CSI driver behavior, snapshots, resizing, backups, multi-writer access modes, and StatefulSet `volumeClaimTemplates` need separate validation per storage backend. In production, check the storage backend documentation and disaster recovery procedure together.

The example `standard` StorageClass may not exist in your cluster. Use `kubectl get storageclass` to check real class names and the default class first.

## References

- Kubernetes Docs, [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- Kubernetes Docs, [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
- Kubernetes Docs, [Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)
