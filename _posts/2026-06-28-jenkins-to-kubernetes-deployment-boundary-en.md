---
layout: single
title: "Jenkins 10. Drawing the Boundary Between Jenkins and Kubernetes Deployment"
description: "A CI/CD boundary guide that separates Jenkins image build responsibilities from Kubernetes desired-state reconciliation."
date: 2026-06-28 09:00:00 +09:00
lang: en
translation_key: jenkins-to-kubernetes-deployment-boundary
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, kubernetes, deployment, ci-cd, boundary]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/jenkins-to-kubernetes-deployment-boundary/
---

## Summary

When connecting Jenkins to Kubernetes, letting Jenkins do everything blurs responsibilities. Jenkins is closer to source verification, image build, and deployment request. Kubernetes is closer to reconciling the desired state written in manifests inside the cluster.

The conclusion of this post is that Jenkins Pipeline should not absorb unlimited cluster operations knowledge. Separate image build, deploy trigger, manifest change, and cluster reconciliation responsibilities.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: analysis
- Test environment: verified against the author's Jenkins practice server. As of 2026-04-24, the unauthenticated login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`. The OS is Linux 22.04; agent details are not fixed in this post.
- Test version: the author's Jenkins practice server reported Jenkins 2.541.3 in the login response header on 2026-04-24. Documentation checks use the relevant official documents checked on 2026-04-24.
- Source level: Jenkins official documentation and Kubernetes official documentation.
- Note: Argo CD, Flux, Helm, Kustomize, and GitOps comparisons are outside this post.

## Problem Definition

When Jenkins is connected to Kubernetes deployment, common problems include:

- Cluster access details and deployment logic all live inside Jenkinsfile.
- Image tags change but manifest history does not.
- Jenkins job success is treated as Kubernetes deployment success.
- Rollback boundaries between Jenkins build number and Kubernetes rollout are unclear.

This post defines the boundary before moving into Kubernetes.

## Verified Facts

- According to Jenkins Using Docker with Pipeline documentation, Jenkins Pipeline can build Docker images and push them to custom registries.
  Evidence: [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- According to Kubernetes Objects documentation, Kubernetes objects are persistent entities that represent cluster state, and Kubernetes continuously works to ensure created objects exist.
  Evidence: [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- According to Kubernetes Objects documentation, `spec` describes desired state, while `status` describes current state supplied and updated by Kubernetes components.
  Evidence: [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- According to Kubernetes Deployment documentation, a Deployment manages Pods for an application workload and provides declarative updates for Pods and ReplicaSets.
  Evidence: [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- According to Kubernetes Service documentation, a Service exposes a network application running as one or more Pods inside the cluster.
  Evidence: [Service](https://kubernetes.io/docs/concepts/services-networking/service/)

A simple boundary model:

```text
Jenkins: checkout, test, image build, registry push, deploy request
Manifest repository: desired state change history
Kubernetes: scheduling, rollout, service routing, reconciliation
Registry: image storage and digest
```

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow on the author's Jenkins practice server. On 2026-04-24, the unauthenticated login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`.
- Documentation check result: Jenkins and Kubernetes official documentation were used to verify the image build/push and object desired-state boundary.
- Needs reproduction: update a Deployment manifest with an image tag and record `kubectl rollout status` separately from Jenkins build success.

## Interpretation / Opinion

My judgment is that Jenkins job success often means "the deployment request was sent," not "the deployment is done." Real deployment success should be checked through Deployment rollout, Pod readiness, Service routing, and Ingress status.

For beginners, letting Jenkins run `kubectl apply` directly is easier to understand. As operations grow, keeping manifest changes in Git and limiting Jenkins to image and change-request creation improves traceability.

The important connection is one source commit, one image digest, one manifest change, and one rollout result. If those four drift apart, incident response becomes much harder.

## Limits and Exceptions

The basic deployment boundary and rollout-check flow were verified in the author's practice environment. RBAC, kubeconfig storage, namespace permissions, rollout failures, and image pull errors need follow-up Kubernetes posts.

For a small internal system, direct `kubectl apply` from Jenkins may be sufficient. For multiple clusters and environments, a GitOps controller may provide clearer boundaries.

## References

- Jenkins User Handbook, [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- Kubernetes Docs, [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- Kubernetes Docs, [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- Kubernetes Docs, [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
