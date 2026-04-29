---
layout: single
title: "K8S 01. What Kubernetes Solves and What It Does Not"
description: "An introductory Kubernetes guide that frames Kubernetes as a cluster desired-state system rather than just a container runner."
date: 2026-06-30 09:00:00 +0900
lang: en
translation_key: kubernetes-what-it-solves-and-does-not
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, k8s, cluster, containers, devops]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/kubernetes-what-it-solves-and-does-not/
---

## Summary

Docker teaches the basic feel of building and running container images. Jenkins automates build and push. Kubernetes comes next: it declares and maintains how containerized workloads should run inside a cluster.

The conclusion of this post is that Kubernetes should not be treated as a collection of container run commands. Kubernetes handles deployment, replication, service discovery, and rollout problems, but it does not automatically fix bad images, poor application design, storage limits, or network constraints.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: analysis
- Test environment: verified in the author's separate practice environment. OS, node details, and cluster topology are not fixed in this post.
- Test version: Kubernetes official documentation checked on 2026-04-24. The documentation site showed v1.36 links.
- Source level: Kubernetes official documentation.
- Note: managed Kubernetes and on-prem Kubernetes comparisons are separate operations topics.

## Problem Definition

When first learning Kubernetes, `kubectl run`, `kubectl apply`, YAML, Pod, Deployment, and Service appear together. Without separating what Kubernetes solves from what it does not solve, it is easy to assume Kubernetes automatically handles every operations problem.

This post frames Kubernetes as a desired-state system for clusters, not simply as a tool for running many containers.

## Verified Facts

- According to Kubernetes Components documentation, a Kubernetes cluster consists of a control plane and one or more worker nodes.
  Evidence: [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
- According to the same documentation, kube-apiserver, etcd, kube-scheduler, and kube-controller-manager are control plane components.
  Evidence: [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
- According to the same documentation, kubelet ensures that Pods and containers are running on a node.
  Evidence: [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
- According to Kubernetes Objects documentation, Kubernetes objects are persistent entities that represent cluster state, and creating an object tells Kubernetes the desired state.
  Evidence: [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- According to Kubernetes Workloads documentation, workloads run inside sets of Pods, and workload resources usually manage Pods on your behalf.
  Evidence: [Workloads](https://kubernetes.io/docs/concepts/workloads/)

Kubernetes mainly handles:

```text
declaring desired state
Pod scheduling
maintaining replicas
rollout and rollback
stable endpoints through Service
connecting runtime configuration through ConfigMap, Secret, and volumes
```

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow in the author's practice environment.
- Documentation check result: official documentation was used to verify cluster components, object desired state, and workload resources.
- Needs reproduction: apply a Deployment with `kubectl apply` and observe Pods being created.

## Interpretation / Opinion

My judgment is that the first Kubernetes sentence should be "it keeps desired state" rather than "it runs containers." This makes it easier to understand why Deployments create Pods and why Services provide stable endpoints behind changing Pod IPs.

Kubernetes also has boundaries. A bad Dockerfile, slow application startup, wrong health check, poor resource requests, unstable storage, or broken network design does not become good just because it runs on Kubernetes.

Kubernetes is not a replacement for operations. It is closer to a platform where you express operational intent as API objects and let the control plane continuously reconcile toward that state.

## Limits and Exceptions

The basic cluster flow was checked in the author's practice environment. Detailed scheduler decisions, controller reconciliation internals, and every variation of Pod creation events were outside the observation scope.

Kubernetes deployment methods differ across managed services, kubeadm, kops, kubespray, and lightweight distributions. This series continues with kubeadm because the focus is on on-prem fundamentals.

## References

- Kubernetes Docs, [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
- Kubernetes Docs, [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- Kubernetes Docs, [Workloads](https://kubernetes.io/docs/concepts/workloads/)
