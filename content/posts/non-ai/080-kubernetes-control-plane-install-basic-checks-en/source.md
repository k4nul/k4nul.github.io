---
layout: single
title: "K8S 04. Control Plane Installation and Basic Checks"
description: "A kubeadm control plane checklist covering kubeconfig, Pod network installation, and basic control plane verification."
date: 2026-06-13 09:00:00 +0900
lang: en
translation_key: kubernetes-control-plane-install-basic-checks
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, kubeadm, control-plane, kubectl, cni]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/kubernetes-control-plane-install-basic-checks/
---

## Summary

Control plane installation does not end with `kubeadm init`. After init, you need to configure kubeconfig, install a Pod network add-on, and check system Pods and node state.

The conclusion of this post is that success should mean more than "the command finished." You should be able to access the API server with kubectl and inspect CoreDNS plus control plane Pod state.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: tutorial
- Test environment: verified in the author's separate practice environment. OS, node details, and cluster topology are not fixed in this post.
- Test version: Kubernetes kubeadm official documentation checked on 2026-04-24.
- Source level: Kubernetes official documentation.
- Note: HA control plane and external etcd are outside this post.

## Problem Definition

Beginners often assume the cluster is complete when `kubeadm init` finishes. In practice, kubeconfig setup, CNI installation, system Pod checks, and node status checks still follow.

This post defines the basic verification order for a single control plane learning environment.

## Verified Facts

- According to kubeadm cluster creation documentation, `kubeadm init` runs prechecks and then downloads and installs control plane components.
  Evidence: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- According to the same documentation, after init, a regular user should copy `/etc/kubernetes/admin.conf` to `$HOME/.kube/config` and change ownership.
  Evidence: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- According to the same documentation, you should deploy a Pod network after init, and after installing a Pod network you can check whether CoreDNS Pods are `Running`.
  Evidence: [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- According to Kubernetes Components documentation, the control plane includes kube-apiserver, etcd, kube-scheduler, and kube-controller-manager.
  Evidence: [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)

Basic check flow:

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

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow in the author's practice environment.
- Documentation check result: official documentation was used to verify kubeconfig setup and Pod network installation after `kubeadm init`.
- Needs reproduction: record init output, node state, CoreDNS state, and the before/after effect of CNI installation on a real control plane node.

## Interpretation / Opinion

My judgment is that the first control plane check is whether kubectl can reach the API server. The next checks are whether the node becomes Ready and CoreDNS becomes Running.

Without a Pod network, the control plane may initialize but the cluster is not ready to run workloads normally. CNI choice is not an afterthought; it is part of cluster design.

## Limits and Exceptions

The control plane installation and basic check flow were verified in the author's practice environment. Container runtime, swap, firewall, cgroup driver, and OS package repository setup must be verified per environment.

A single control plane is useful for learning but does not meet production high-availability expectations.

## References

- Kubernetes Docs, [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- Kubernetes Docs, [Kubernetes Components](https://kubernetes.io/docs/concepts/overview/components/)
