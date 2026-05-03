---
layout: single
title: "K8S 08. Why requests, limits, and probes should be reviewed together"
description: "An explanation of Kubernetes resource requests, limits, and liveness/readiness/startup probes as one operational set."
date: 2026-06-11 09:00:00 +09:00
lang: en
translation_key: kubernetes-requests-limits-probes
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, resources, requests, limits, probes]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/kubernetes-requests-limits-probes/
---

## Summary

In Kubernetes, `requests` and `limits` define resource boundaries for scheduling and runtime behavior. Probes tell Kubernetes whether a container can receive traffic, needs to be restarted, or needs more startup time.

The conclusion of this post is that resource settings and probes should not be reviewed separately. A low request can make scheduling too optimistic, a tight limit can slow or kill the application, and an aggressive probe can make the symptom look like a restart loop.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: analysis
- Test environment: verified in the author's separate practice environment. OS, node details, and cluster topology are not fixed in this post.
- Test version: Kubernetes official documentation checked on 2026-04-24. The documentation site displayed v1.36 links.
- Source level: Kubernetes official documentation.
- Note: production sizing should be based on application profiles and real metrics.

## Problem Definition

Early manifests often mix these issues:

- Deploying Pods without `resources`.
- Treating `requests` and `limits` as the same concept.
- Using the same endpoint for readiness and liveness.
- Starting liveness checks too early for slow-starting applications.
- Failing to separate application bugs, resource pressure, and probe misconfiguration when restarts happen.

## Verified Facts

- According to Kubernetes Resource Management documentation, container resources can define requests and limits.
  Evidence: [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- According to the same documentation, the scheduler uses resource requests when choosing a node for a Pod.
  Evidence: [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- According to Kubernetes Pod QoS documentation, Pods are assigned Guaranteed, Burstable, or BestEffort QoS classes based on resource settings.
  Evidence: [Pod Quality of Service Classes](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/)
- According to Kubernetes probe documentation, the kubelet can periodically diagnose container health with probes.
  Evidence: [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- According to the same documentation, when a startup probe is configured, liveness and readiness probes do not run until the startup probe succeeds.
  Evidence: [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- According to the same documentation, when a readiness probe fails, the Pod IP is removed from ready endpoints for matching Services.
  Evidence: [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)

A basic example:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 2
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
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: "100m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
          startupProbe:
            httpGet:
              path: /healthz
              port: 8080
            failureThreshold: 30
            periodSeconds: 2
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            periodSeconds: 10
            failureThreshold: 3
```

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow in the author's practice environment.
- Confirmed result: based on official documentation, I verified the roles of requests, limits, QoS classes, and startup/readiness/liveness probes.
- Directly verified items: `kubectl describe pod`, `kubectl get events`, metrics collection, behavior after exceeding limits, and endpoint removal after readiness failure.

## Interpretation / Opinion

For operations, I usually look at requests first. Requests are the signal the scheduler uses when choosing a node. If they are too low, the cluster can look roomier than it really is. If they are too high, fewer nodes can accept the Pod and Pending Pods can increase.

Limits are guardrails, but they are also performance settings. A memory limit can lead to termination when usage grows beyond expectation. A CPU limit can affect throughput and latency. It is risky to treat limits as values that should simply be as low as possible.

Probes are a contract that lets Kubernetes interpret application health. Readiness means whether traffic should be sent, liveness means whether restart is needed, and startup means whether Kubernetes should wait longer during initialization. An overly aggressive liveness probe can turn temporary delay into restarts, and restarts can create more delay.

## Limits and Exceptions

The basic resource and probe flow was checked in the author's practice environment. The CPU and memory values in the example are placeholders, not recommendations. Real values should be based on metrics, peak traffic, startup time, garbage collection behavior, and external dependency latency.

Batch jobs, queue workers, databases, JVM applications, Go services, and Node.js services can require different request/limit and probe strategies.

## References

- Kubernetes Docs, [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- Kubernetes Docs, [Pod Quality of Service Classes](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/)
- Kubernetes Docs, [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
