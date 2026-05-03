---
layout: single
title: "K8S 03. Kubernetes Installation Strategy for On-Prem and Why kubeadm"
description: "A Kubernetes installation strategy post explaining why kubeadm is a useful baseline for learning on-prem cluster setup."
date: 2026-06-06 09:00:00 +09:00
lang: en
translation_key: kubernetes-kubeadm-installation-strategy-on-prem
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, kubeadm, on-prem, installation, cluster]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/kubernetes-kubeadm-installation-strategy-on-prem/
---

## Summary

There are many ways to install Kubernetes. Managed Kubernetes reduces control plane operations, but on-prem environments require more direct understanding of nodes, network, storage, certificates, and upgrades. This series uses kubeadm as the baseline.

The conclusion of this post is that kubeadm is useful for learning not because it is a complete platform, but because it exposes the cluster bootstrap process relatively clearly.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: analysis
- Test environment: verified in the author's separate practice environment. OS, node details, and cluster topology are not fixed in this post.
- Test version: Kubernetes kubeadm official documentation checked on 2026-04-24.
- Source level: Kubernetes official documentation.
- Note: production HA cluster design is outside this post.

## Problem Definition

Kubernetes installation starts with tool choice:

- Use a managed service?
- Bootstrap directly with kubeadm?
- Use a lightweight distribution such as k3s?
- Use kubespray or another automation tool?

This post explains why kubeadm is the first baseline for on-prem learning.

## Verified Facts

- According to Kubernetes kubeadm cluster creation documentation, kubeadm can create a minimum viable Kubernetes cluster that conforms to best practices.
  Evidence: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- According to the same documentation, kubeadm also supports cluster lifecycle functions such as bootstrap tokens and cluster upgrades.
  Evidence: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- According to kubeadm installation documentation, prerequisites include a compatible Linux host, at least 2GB RAM, at least 2 CPUs for control plane machines, and network connectivity between nodes.
  Evidence: [Installing kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
- According to kubeadm cluster creation documentation, after `kubeadm init`, kubeconfig setup and Pod network add-on installation are needed.
  Evidence: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- According to the same documentation, validating CNI providers is outside kubeadm's current e2e testing scope.
  Evidence: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)

Pre-install checklist:

```text
prepare Linux hosts
prepare container runtime
install kubeadm, kubelet, kubectl
check control plane node resources
check node-to-node networking
plan Pod CIDR and Service CIDR
choose CNI
define admin kubeconfig handling
```

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow in the author's practice environment.
- Documentation check result: official documentation was used to verify kubeadm purpose, prerequisites, and post-init tasks.
- Needs reproduction: run prerequisite checks and record `kubeadm init` output on real Linux hosts.

## Interpretation / Opinion

My judgment is that kubeadm is not an installer that does everything. It is a bootstrap tool that makes core Kubernetes components visible. It does not automatically finish CNI, storage, ingress, or load balancer design.

That distinction matters on-prem. Cloud load balancers, managed storage, and managed control planes may not exist. Understanding control plane bootstrap and worker join through kubeadm makes later MetalLB and OpenEBS topics easier to place.

## Limits and Exceptions

The kubeadm installation flow was checked in the author's practice environment. Linux distribution package repositories, swap, firewall, cgroup driver, and container runtime configuration must be verified per environment.

Production HA clusters, external etcd, certificate rotation, and upgrade strategy are advanced follow-up topics.

## References

- Kubernetes Docs, [Installing kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
- Kubernetes Docs, [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
