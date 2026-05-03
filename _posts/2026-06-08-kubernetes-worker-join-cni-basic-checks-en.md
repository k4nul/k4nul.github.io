---
layout: single
title: "K8S 05. Worker Join, CNI Setup, and Basic Cluster Checks"
description: "A Kubernetes kubeadm guide for joining worker nodes, checking CNI status, and validating basic cluster readiness."
date: 2026-06-08 09:00:00 +09:00
lang: en
translation_key: kubernetes-worker-join-cni-basic-checks
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, kubeadm, worker-node, cni, kubectl]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/kubernetes-worker-join-cni-basic-checks/
---

## Summary

A control plane alone is not enough to understand normal cluster operations. Joining worker nodes shows how workloads are scheduled across nodes, and CNI is needed for Pod networking and CoreDNS readiness.

The conclusion of this post is that worker join success should be checked through `kubectl get nodes`, system Pods, Pod network state, and a simple workload scheduling test, not only through the `kubeadm join` exit code.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: tutorial
- Test environment: verified in the author's separate practice environment. OS, node details, and cluster topology are not fixed in this post.
- Test version: Kubernetes kubeadm official documentation checked on 2026-04-24.
- Source level: Kubernetes official documentation.
- Note: Windows worker nodes are outside this post.

## Problem Definition

After worker join, "the node appears" and "the cluster is healthy" are not the same. A node can be `NotReady`, CNI may be missing, and system Pods can be Pending or CrashLooping.

## Verified Facts

- According to kubeadm join documentation, `kubeadm join` initializes a new Kubernetes node and adds it to an existing cluster.
  Evidence: [kubeadm join](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/)
- According to kubeadm cluster creation documentation, `kubeadm init` output includes the `kubeadm join` command to run on worker nodes.
  Evidence: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- According to the same documentation, after installing a Pod network add-on you can check that CoreDNS Pods are `Running`.
  Evidence: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- According to Kubernetes Components documentation, kubelet ensures that Pods and containers are running on a node.
  Evidence: [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)

Check flow:

```bash
# on worker node
sudo kubeadm join <control-plane-host>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>

# on control plane
kubectl get nodes -o wide
kubectl get pods -A
kubectl describe node <worker-node-name>
```

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow in the author's practice environment.
- Documentation check result: official documentation was used to verify the purpose of join and CoreDNS checks after CNI.
- Needs reproduction: record node state before and after worker join, CoreDNS state before and after CNI, and sample Deployment scheduling results.

## Interpretation / Opinion

My judgment is that worker join issues are easier to debug in three layers. First, did the node register with the API server? Second, can kubelet and the container runtime run Pods? Third, does CNI provide Pod networking?

`NotReady` is a symptom, not a root cause. Check `describe node`, kubelet logs, and CNI Pod state together.

## Limits and Exceptions

This post assumes Linux worker nodes. Windows workers, multi-architecture nodes, GPU nodes, and taint/toleration-dedicated nodes require separate verification.

CNI installation manifests, Pod CIDR requirements, and NetworkPolicy support vary by CNI.

## References

- Kubernetes Docs, [kubeadm join](https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-join/)
- Kubernetes Docs, [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- Kubernetes Docs, [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
