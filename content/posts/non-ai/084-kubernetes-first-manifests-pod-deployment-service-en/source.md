---
layout: single
title: "K8S 06. Writing First Manifests: Pod, Deployment, Service"
description: "A beginner Kubernetes manifest guide covering basic fields and first Pod, Deployment, and Service examples."
date: 2026-07-10 09:00:00 +0900
lang: en
translation_key: kubernetes-first-manifests-pod-deployment-service
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, manifest, pod, deployment, service]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/kubernetes-first-manifests-pod-deployment-service/
---

## Summary

A Kubernetes manifest is YAML that tells the cluster the desired state. Instead of memorizing everything at once, first read `apiVersion`, `kind`, `metadata`, and `spec`, then move from Pod to Deployment and from Deployment to Service.

The conclusion of this post is that normal application deployment should start with a Deployment and Service combination, not a standalone Pod.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: tutorial
- Test environment: verified in the author's separate practice environment. OS, node details, and cluster topology are not fixed in this post.
- Test version: Kubernetes official documentation checked on 2026-04-24.
- Source level: Kubernetes official documentation.
- Note: namespace, ConfigMap, Secret, and Ingress are handled in the next post.

## Problem Definition

Beginner manifest mistakes include:

- Assuming every `kind` has the same structure.
- Missing the label and selector relationship.
- Creating Pods directly and expecting scale or rollout behavior.
- Confusing Service `port` and `targetPort`.

## Verified Facts

- According to Kubernetes Objects documentation, almost every Kubernetes object includes `spec` for desired state and `status` for current state.
  Evidence: [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- According to the same documentation, creating an object requires fields such as `apiVersion`, `kind`, `metadata`, and `spec`.
  Evidence: [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- According to Pods documentation, a Pod is the smallest deployable unit in Kubernetes.
  Evidence: [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- According to Deployment documentation, a Deployment provides declarative updates for Pods and ReplicaSets.
  Evidence: [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- According to Service documentation, a Service can expose a selected set of Pods as a network endpoint.
  Evidence: [Service](https://kubernetes.io/docs/concepts/services-networking/service/)

First manifest example:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-nginx
  template:
    metadata:
      labels:
        app: hello-nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
          ports:
            - containerPort: 80
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-nginx
spec:
  selector:
    app: hello-nginx
  ports:
    - port: 80
      targetPort: 80
```

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow in the author's practice environment.
- Documentation check result: official documentation was used to verify object fields and the roles of Deployment and Service.
- Needs reproduction: run `kubectl apply -f`, `kubectl get deploy,pod,svc`, and `kubectl describe svc` to verify selector and endpoint connection.

## Interpretation / Opinion

My judgment is that the most important first-manifest lines are labels and selectors, not the image. If the Deployment Pod template labels and Service selector do not match, Pods may run but Service has no traffic target.

Pod manifests are useful for learning, but Deployment should be the default for application operation. That path makes replica, rollout, and rollback easier to learn next.

## Limits and Exceptions

The manifest application flow was checked in the author's practice environment. Image pull availability for `nginx:1.27`, Service endpoint creation, and Pod scheduling can vary by registry state and cluster environment.

Production manifests usually also need resource requests/limits, probes, securityContext, namespace, imagePullPolicy, and rollout strategy.

## References

- Kubernetes Docs, [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- Kubernetes Docs, [Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
- Kubernetes Docs, [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- Kubernetes Docs, [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
