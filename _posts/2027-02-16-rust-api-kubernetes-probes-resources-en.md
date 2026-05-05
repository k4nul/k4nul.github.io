---
layout: single
title: "Rust Service 22. Setting probes and resource limits"
description: "Defines readiness, liveness, startup probes, and Kubernetes CPU/memory requests and limits for a Rust API."
date: 2027-02-16 09:00:00 +09:00
lang: en
translation_key: rust-api-kubernetes-probes-resources
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
permalink: /en/rust/rust-api-kubernetes-probes-resources/
---

## Summary

A Kubernetes probe is not just a decorative health URL. Readiness decides whether a Pod should receive traffic. Liveness decides whether the container should be restarted. Startup probes protect slower-starting processes from being killed by liveness too early.

Resource requests and limits are also operational signals. Requests influence scheduling. Limits constrain runtime usage. Even if a Rust API starts quickly and uses little memory in a local test, unverified limits can hide a problem or create a new one.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Choosing ConfigMap, Secret, and env injection rules
- Next post: Opening external access with Ingress and TLS boundaries
- Scope: deciding whether a Pod can receive traffic, whether it should be restarted, and how much CPU and memory it should request

## Document Information

- Written date: 2026-05-05
- Verification date: 2026-05-05
- Document type: tutorial | analysis
- Test environment: No live-cluster execution test. The procedure is based on Kubernetes official documentation and generic manifest examples.
- Tested versions: Kubernetes documentation baseline. `kubectl`, metrics-server, and cluster versions are left unspecified because no live cluster was executed for this post.
- Evidence level: official documentation

## Problem Statement

The previous Deployment only proved that a Pod could be started. Operations need more than that.

A service may need a database connection before it can safely accept traffic. A process may be running but unable to serve requests because the runtime loop is stuck. A Pod may also use too much node memory, or fail during normal traffic because the memory limit was guessed too low.

The goal of this post is to connect Rust API health endpoints to Kubernetes signals and to treat resource requests and limits as observable operating assumptions rather than pretty defaults.

## Verified Facts

- Kubernetes documentation describes liveness probes as a way to decide whether a container should be restarted, and readiness probes as a way to decide whether a Pod is ready to accept traffic.
  Evidence: [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- Kubernetes documentation states that startup probes, when configured, delay liveness and readiness checks until the startup probe succeeds.
  Evidence: [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- Kubernetes documentation allows CPU and memory requests and limits to be set per container. Requests describe what a container needs, while limits describe the maximum allowed usage.
  Evidence: [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- Kubernetes documentation describes memory limits as enforceable by container termination when exceeded, while CPU limits constrain CPU usage.
  Evidence: [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

## Practice Baseline

Use at least two health endpoints in the Rust API.

- `/live`: confirms that the process and request loop can respond. Do not put database checks here.
- `/ready`: confirms that the service can safely receive traffic. This can include database connectivity, required configuration, migration readiness, or other request-path dependencies, all with short timeouts.

An Axum router might separate them like this:

```rust
use axum::{routing::get, Json, Router};
use serde_json::json;

async fn live() -> Json<serde_json::Value> {
    Json(json!({ "status": "ok" }))
}

async fn ready() -> Json<serde_json::Value> {
    // In a real service, check dependencies with a short timeout.
    Json(json!({ "status": "ready" }))
}

pub fn router() -> Router {
    Router::new()
        .route("/live", get(live))
        .route("/ready", get(ready))
}
```

The Deployment manifest should keep probe meanings separate.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rust-api
  namespace: rust-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: rust-api
  template:
    metadata:
      labels:
        app: rust-api
    spec:
      containers:
        - name: rust-api
          image: ghcr.io/example/rust-api:2027.02.16
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            periodSeconds: 10
            timeoutSeconds: 2
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /live
              port: 8080
            periodSeconds: 20
            timeoutSeconds: 2
            failureThreshold: 3
          startupProbe:
            httpGet:
              path: /live
              port: 8080
            periodSeconds: 5
            failureThreshold: 12
          resources:
            requests:
              cpu: 50m
              memory: 64Mi
            limits:
              cpu: 500m
              memory: 256Mi
```

The resource values above are examples, not benchmark results. They show a starting shape for a small API. Real values should be adjusted using traffic volume, response size, database pool size, JSON payload size, TLS or compression placement, logging volume, allocator behavior, and concurrency settings.

After applying the manifest, inspect rollout state, Pod state, and events together.

```bash
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/rust-api -n rust-api
kubectl get pods -n rust-api
kubectl describe pod -l app=rust-api -n rust-api
kubectl get endpointslice -n rust-api -l kubernetes.io/service-name=rust-api
```

If metrics-server is installed, also check actual resource usage.

```bash
kubectl top pod -n rust-api
```

## Observations

No live-cluster output is included in this post. During verification, record these outcomes separately:

| Situation | Expected observation |
| --- | --- |
| `/ready` fails | The Pod may be Running but not Ready, and can be removed from Service endpoints |
| `/live` fails repeatedly | kubelet restarts the container and restart count increases |
| startup probe fails | The container restarts if `/live` does not succeed within the startup window |
| memory limit is exceeded | The container may terminate and show OOMKilled or related events |
| CPU limit is reached | Latency and throttling are more likely than immediate restarts |
| requests exceed available node capacity | The Pod may stay Pending with scheduling events |

## Interpretation

Using the same endpoint for readiness and liveness is convenient, but it blurs the operating meaning. If a slow database makes liveness fail and Kubernetes repeatedly restarts the API Pod, the restart loop amplifies the incident instead of recovering it. Put external dependencies in readiness. Keep liveness close to unrecoverable process failure.

Resource limits are not proof of production readiness by themselves. A memory limit can kill the process, and a CPU limit can damage latency. Start with a conservative baseline only if you will continue tuning it with load tests and production metrics.

Rust services may use less memory than some equivalent dynamic-runtime services, but that should not be written as a universal fact. Actual memory depends on payload size, database pools, caches, compression, logging, allocator behavior, and concurrency settings.

## Limitations

- This post focuses on HTTP probes. It does not cover the detailed tradeoffs of gRPC probes, exec probes, or TCP socket probes.
- The resource values are not benchmark-backed recommendations.
- `kubectl top` requires metrics-server or a compatible metrics pipeline.
- Health endpoints are poor signals if they are blocked by authentication middleware, rate limiting, or external APIs.

## References

- [Liveness, Readiness, and Startup Probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/)
- [Resource Management for Pods and Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Assign Memory Resources to Containers and Pods](https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/)
- [Assign CPU Resources to Containers and Pods](https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/)

## Change Log

- 2026-05-05: Rewrote the probe and resource guidance using Kubernetes official documentation, with separate observation points.
