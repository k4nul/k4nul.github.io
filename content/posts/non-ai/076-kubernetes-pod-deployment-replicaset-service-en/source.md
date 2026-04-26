---
layout: single
title: "K8S 02. Understanding Pod, Deployment, ReplicaSet, and Service as an Operations Flow"
description: "A Kubernetes guide that connects Pod, Deployment, ReplicaSet, and Service as one operating flow instead of isolated definitions."
date: 2026-06-09 09:00:00 +0900
lang: en
translation_key: kubernetes-pod-deployment-replicaset-service
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, pod, deployment, replicaset, service]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/kubernetes-pod-deployment-replicaset-service/
---

## Summary

Pod, Deployment, ReplicaSet, and Service are confusing when memorized separately. As an operations flow: Deployment declares the desired application state, ReplicaSet keeps the Pod count, Pods run containers, and Service provides a stable access point behind changing Pods.

The conclusion of this post is that beginners should understand Deployment and Service relationships before directly creating Pods.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: analysis
- Test environment: verified in the author's separate practice environment. OS, node details, and cluster topology are not fixed in this post.
- Test version: Kubernetes official documentation checked on 2026-04-24.
- Source level: Kubernetes official documentation.
- Note: StatefulSet, DaemonSet, and Job are outside this post.

## Problem Definition

The common beginner question is: why does Kubernetes use objects such as Pod, Deployment, and Service instead of running containers directly?

This post connects four objects through these questions:

- What actually runs containers?
- What maintains the Pod count?
- What manages rollout?
- What provides a stable network endpoint?

## Verified Facts

- According to Kubernetes Pods documentation, a Pod is the smallest deployable computing unit that Kubernetes can create and manage.
  Evidence: [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- According to the same documentation, Pods are generally not created directly and are created using workload resources.
  Evidence: [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- According to Kubernetes Deployment documentation, a Deployment manages Pods for an application workload and provides declarative updates for Pods and ReplicaSets.
  Evidence: [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- According to Kubernetes ReplicaSet documentation, a ReplicaSet maintains a stable set of replica Pods at any given time, and usually a Deployment manages ReplicaSets automatically.
  Evidence: [ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
- According to Kubernetes Service documentation, a Service exposes a network application running as one or more Pods inside the cluster.
  Evidence: [Service](https://kubernetes.io/docs/concepts/services-networking/service/)

Operational flow:

```text
Deployment manifest apply
Deployment controller creates or updates ReplicaSet
ReplicaSet maintains desired Pod count
Pods run containers
Service selects Pods and provides stable endpoint
```

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow in the author's practice environment.
- Documentation check result: official documentation was used to verify the roles and recommended usage flow for the four objects.
- Needs reproduction: create an nginx Deployment and Service, then observe ReplicaSet and Pod names.

## Interpretation / Opinion

My judgment is that beginners should stop thinking of a Pod as a server. Pods are ephemeral and replaceable. That is why Service and Deployment matter.

Deployment makes rollout and rollback easier to understand. When the image tag changes, the Deployment Pod template changes, a new ReplicaSet appears, and Pods are replaced gradually.

Service prevents applications from tracking changing Pod IPs directly. It is an abstraction over the currently selected backing Pods.

## Limits and Exceptions

The basic object creation flow was checked in the author's practice environment.

There are special cases where managing ReplicaSets directly can make sense, but normal application deployment should start with Deployment.

## References

- Kubernetes Docs, [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- Kubernetes Docs, [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- Kubernetes Docs, [ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
- Kubernetes Docs, [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
