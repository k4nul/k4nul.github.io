---
layout: single
title: "K8S 10. Bare-metal addendum: when MetalLB and OpenEBS are useful"
description: "An overview of MetalLB and OpenEBS as options for bare-metal Kubernetes load balancer and persistent storage gaps."
date: 2026-07-18 09:00:00 +09:00
lang: en
translation_key: kubernetes-bare-metal-metallb-openebs
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, bare-metal, metallb, openebs, on-prem]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/kubernetes-bare-metal-metallb-openebs/
---

## Summary

In cloud Kubernetes, `Service type: LoadBalancer` and dynamic storage provisioning are often connected to provider features. In on-prem or bare-metal Kubernetes, that connection may not exist automatically. MetalLB and OpenEBS often appear as candidates for filling those gaps.

The conclusion of this post is that MetalLB and OpenEBS should not be treated as mandatory Kubernetes components. They are options for bare-metal environments where network load balancer and storage provisioning capabilities are missing.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: analysis
- Test environment: verified in the author's separate practice environment. OS, node details, and cluster topology are not fixed in this post.
- Test version: Kubernetes official documentation, MetalLB official documentation, and OpenEBS 4.4.x official documentation checked on 2026-04-24.
- Source level: Kubernetes, MetalLB, and OpenEBS official documentation.
- Note: network design, BGP, storage performance, and backup/restore require separate operational validation.

## Problem Definition

In bare-metal Kubernetes, these questions appear quickly:

- Why does a `LoadBalancer` Service not get an external IP?
- Is NodePort enough for production traffic?
- What IP should sit in front of the Ingress controller?
- When a PVC is created, where does the actual disk come from?
- Can local disks satisfy data durability requirements?

## Verified Facts

- According to Kubernetes Service documentation, Service types include ClusterIP, NodePort, and LoadBalancer.
  Evidence: [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
- According to MetalLB documentation, MetalLB is a load balancer implementation for bare-metal Kubernetes clusters using standard routing protocols.
  Evidence: [MetalLB](https://metallb.io/)
- According to MetalLB documentation, Kubernetes does not offer a network load balancer implementation for bare-metal clusters, and LoadBalancers can remain pending when not running on a supported IaaS platform.
  Evidence: [MetalLB](https://metallb.io/)
- According to MetalLB Usage documentation, after MetalLB is installed and configured, creating a Service with `spec.type` set to `LoadBalancer` exposes it externally through MetalLB.
  Evidence: [MetalLB Usage](https://metallb.io/usage/index.html)
- According to Kubernetes Persistent Volumes documentation, PVC/PV binding and StorageClass-based dynamic provisioning are core storage flows.
  Evidence: [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- According to OpenEBS 4.4.x documentation, OpenEBS uses storage available on Kubernetes worker nodes to provide Local or Replicated Persistent Volumes.
  Evidence: [OpenEBS Documentation](https://openebs.io/docs)
- According to OpenEBS Local Storage documentation, Local Storage is accessible from a single node, and if that node becomes unhealthy, the local volume can become inaccessible.
  Evidence: [OpenEBS Local Storage](https://openebs.io/docs/concepts/data-engines/localstorage)

The roles can be simplified like this:

```text
External traffic problem
Service type LoadBalancer -> cloud provider or an implementation such as MetalLB

Persistent storage problem
PVC -> StorageClass -> CSI/provisioner -> actual volume
One on-prem local/replicated storage option: OpenEBS
```

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow in the author's practice environment.
- Confirmed result: based on official documentation, I confirmed the areas MetalLB and OpenEBS are intended to cover.
- Directly verified items: `kubectl get svc`, LoadBalancer external IP assignment, `kubectl describe svc`, `kubectl get storageclass,pvc,pv`, and volume availability after Pod rescheduling.

## Interpretation / Opinion

MetalLB is better understood as a component that helps `LoadBalancer` Services get external IPs in bare-metal clusters, not as a replacement for Ingress. Even when running an Ingress controller, you still need to expose that controller's Service to the outside world. MetalLB can help solve that front-door IP problem.

OpenEBS is not the only answer for Kubernetes storage. If you already have NFS, SAN, Ceph, Longhorn, a cloud CSI driver, or a storage appliance, another option may fit better. OpenEBS is worth considering when you want to manage local or replicated worker-node storage in a Kubernetes-native way.

In on-prem environments, failure domains should be defined before choosing tools. For networking, check IP ranges, routing, ARP/BGP, and failover behavior. For storage, check node failure, disk failure, backup, restore, and data consistency. Installing MetalLB or OpenEBS before answering those questions can produce a cluster that works technically but has no operational standard.

## Limits and Exceptions

The basic role and check flow were verified in the author's practice environment. MetalLB L2 mode, BGP mode, IPAddressPool design, router configuration, and ARP/NDP behavior need separate validation per network environment. OpenEBS Local PV, LVM, ZFS, and Replicated Storage performance and recovery behavior also need separate comparison.

In managed Kubernetes or cloud environments, the provider may already supply LoadBalancer and storage provisioning. In that case, MetalLB or OpenEBS may not be needed.

## References

- Kubernetes Docs, [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
- Kubernetes Docs, [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- Kubernetes Docs, [Storage Classes](https://kubernetes.io/docs/concepts/storage/storage-classes/)
- MetalLB Docs, [MetalLB](https://metallb.io/)
- MetalLB Docs, [Usage](https://metallb.io/usage/index.html)
- OpenEBS Docs, [OpenEBS Documentation](https://openebs.io/docs)
- OpenEBS Docs, [Local Storage](https://openebs.io/docs/concepts/data-engines/localstorage)
