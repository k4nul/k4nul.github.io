---
layout: single
title: "Rust Service 27. Debugging intentional failures with describe, events, and logs"
description: "Creates intentional image pull, readiness, and missing-configuration failures, then narrows the failing Kubernetes layer with kubectl describe, events, and logs."
date: 2027-03-23 09:00:00 +09:00
lang: en
translation_key: rust-api-kubernetes-failure-debugging
section: development
topic_key: rust
featured: false
track: rust
repo:
demo:
references:
categories: Rust
tags: [rust, axum, api, production, devops]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/rust/rust-api-kubernetes-failure-debugging/
---

## Summary

Failure handling is too expensive to learn for the first time during a real incident. Practice by creating small failures and reading the evidence Kubernetes leaves behind.

This post uses image pull failure, readiness failure, and missing configuration as examples. The goal is to use `kubectl rollout status`, `kubectl describe`, `kubectl events`, and `kubectl logs` in a consistent order so the failing layer becomes smaller.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Choosing Prometheus metrics for a Rust API
- Next post: Running non-root containers with least privilege
- Scope: checking workload state, Pod events, container logs, and Service endpoints when a Rust API Pod fails

## Document Information

- Written date: 2026-05-05
- Verification date: 2026-05-05
- Document type: tutorial | analysis
- Test environment: No live-cluster execution test. The post is based on Kubernetes official documentation and generic failure manifests.
- Tested versions: Kubernetes documentation baseline. `kubectl` and cluster versions are left unspecified.
- Evidence level: official documentation

## Problem Statement

Kubernetes failures do not fit on one screen. The same user-facing symptom, "the service is down," can come from different layers.

- The image name is wrong and the container cannot be pulled.
- The Pod is Running, but readiness fails and the Pod is not used by the Service.
- A Secret or ConfigMap key is missing and the container cannot start.
- The app is healthy, but the Service selector does not match any Pod.
- The Ingress host does not match and requests never reach the backend.

This is not a complete incident response manual. It is a practice article for creating small failures and reading Kubernetes evidence in a fixed order.

## Verified Facts

- Kubernetes Debug Pods documentation recommends checking Pod state and recent events with `kubectl describe pods ${POD_NAME}` as the first debugging step for Pods.
  Evidence: [Kubernetes Debug Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
- The `kubectl events` reference describes listing events for a namespace or filtering events for a specific resource.
  Evidence: [kubectl events](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_events/)
- Kubernetes logging documentation explains that container stdout/stderr streams are handled by kubelet and logging pipelines, and can be accessed through built-in tools such as `kubectl logs`.
  Evidence: [Kubernetes Logging Architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
- Kubernetes Debug Running Pods documentation covers tools such as `kubectl exec` and ephemeral containers. This post intentionally starts with describe/events/logs before shelling into a container.
  Evidence: [Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)

## Practice Baseline

Start from a known-good state.

```bash
kubectl get deployment rust-api -n rust-api
kubectl rollout status deployment/rust-api -n rust-api --timeout=120s
kubectl get pod -n rust-api -l app=rust-api
kubectl get endpointslice -n rust-api -l kubernetes.io/service-name=rust-api
```

When a failure appears, use this order.

```bash
kubectl rollout status deployment/rust-api -n rust-api --timeout=120s
kubectl get pod -n rust-api -l app=rust-api
kubectl describe pod -n rust-api -l app=rust-api
kubectl events -n rust-api --for deployment/rust-api
kubectl logs deployment/rust-api -n rust-api --since=10m
kubectl get endpointslice -n rust-api -l kubernetes.io/service-name=rust-api
```

### Failure 1: Image Pull Failure

Deploy a tag that does not exist.

```bash
kubectl set image deployment/rust-api rust-api=ghcr.io/example/rust-api:not-exist -n rust-api
kubectl rollout status deployment/rust-api -n rust-api --timeout=120s
```

Check:

```bash
kubectl get pod -n rust-api -l app=rust-api
kubectl describe pod -n rust-api -l app=rust-api
kubectl events -n rust-api --types=Warning
```

The expected interpretation is that the failure happens before the application starts. `kubectl logs` may not help because the container has not run.

### Failure 2: Readiness Failure

Point readiness to a wrong path.

```yaml
readinessProbe:
  httpGet:
    path: /not-ready
    port: 8080
  periodSeconds: 10
  timeoutSeconds: 2
  failureThreshold: 3
```

Check:

```bash
kubectl rollout status deployment/rust-api -n rust-api --timeout=120s
kubectl describe pod -n rust-api -l app=rust-api
kubectl get endpointslice -n rust-api -l kubernetes.io/service-name=rust-api
kubectl logs deployment/rust-api -n rust-api --since=10m
```

The expected interpretation is that the container can run but is not Ready, so it may be absent from Service endpoints. Application logs may show probe requests or timeout clues.

### Failure 3: Missing ConfigMap or Secret Key

Make the Deployment reference a missing key.

```yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: rust-api-secret
        key: DATABASE_URL_MISSING
```

Check:

```bash
kubectl describe deployment rust-api -n rust-api
kubectl describe pod -n rust-api -l app=rust-api
kubectl events -n rust-api --for deployment/rust-api
kubectl events -n rust-api --types=Warning
```

The expected interpretation is that Kubernetes could not complete container environment configuration. This is not an application-code error yet.

## Observations

No live-cluster output is included in this post. During verification, record observations like this:

| Failure | Look first | Are logs useful? | Typical interpretation |
| --- | --- | --- | --- |
| image pull failure | Pod event, describe | Usually no | image name, tag, or registry permission |
| readiness failure | describe, endpoint, logs | Yes | app runs but is not ready for traffic |
| missing config key | describe, event | Usually no | ConfigMap or Secret reference problem |
| app panic | logs, restart count | Yes | code or runtime configuration problem |
| Service selector mismatch | Service, EndpointSlice | No | label connection between Pod and Service is wrong |

## Interpretation

`kubectl logs` is familiar, so it is tempting to run it first. For failures where the container never starts, logs can be empty. Image pull, scheduling, secret mount, and env injection failures are usually faster to understand from events and `describe`.

If the container is Running and readiness fails, logs and endpoints matter together. You need to know whether the app received the probe request, whether the route exists, and whether an external dependency timed out.

Debugging is not about a magic command. It is about layer order: Deployment rollout, ReplicaSet, Pod state, event, container log, Service endpoint, and Ingress. A fixed order helps the team talk about the same evidence during an incident.

## Limitations

- This post covers intentional practice failures. Real incidents may require checking node pressure, DNS, CNI, admission webhooks, quota, and cloud load balancers.
- `kubectl events` output and event retention depend on cluster configuration and version.
- Pods with multiple containers require `kubectl logs -c`.
- Practice failures should be created in a sandbox namespace, not in production.

## References

- [Kubernetes Debug Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/)
- [Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)
- [kubectl events](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_events/)
- [Kubernetes Logging Architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
- [Kubernetes Debug Services](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/)

## Change Log

- 2026-05-05: Rewrote the intentional failure practice and describe/events/logs observation order using Kubernetes official documentation.
