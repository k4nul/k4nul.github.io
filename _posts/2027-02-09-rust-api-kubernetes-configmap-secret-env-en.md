---
layout: single
title: "Rust Service 21. Choosing ConfigMap, Secret, and env injection rules"
description: "Defines how a Rust API should separate Kubernetes ConfigMaps, Secrets, and environment-variable injection in production manifests."
date: 2027-02-09 09:00:00 +09:00
lang: en
translation_key: rust-api-kubernetes-configmap-secret-env
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
permalink: /en/rust/rust-api-kubernetes-configmap-secret-env/
---

## Summary

In Kubernetes, ordinary configuration and secret values can both reach a Rust API as environment variables. They should still be managed as different operational objects.

This post uses a simple rule: put ordinary configuration in a ConfigMap, sensitive values in a Secret, and expose the final application interface through explicit environment variables. The important caveat is that using a Secret object does not make the system safe by itself. Creation, access control, encryption at rest, rotation, and rollout behavior still need to be designed.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Deploying with Kubernetes Deployment and Service
- Next post: Setting readiness/liveness probes and resource limits
- Scope: separating runtime configuration from the container image and keeping secret values out of code and image layers

## Document Information

- Written date: 2026-05-05
- Verification date: 2026-05-05
- Document type: tutorial | analysis
- Test environment: No live-cluster execution test. The procedure is based on Kubernetes official documentation and generic manifest examples.
- Tested versions: Kubernetes documentation baseline. `kubectl` and cluster versions are left unspecified because no live cluster was executed for this post.
- Evidence level: official documentation

## Problem Statement

The previous post deployed a Rust API with a Deployment and a Service. The next question is what should be baked into the image and what should be injected from outside the image.

These values may all be needed by the same API, but they do not have the same operational meaning.

- `RUST_LOG`: a log-level setting. This is ordinary configuration.
- `APP_BIND_ADDR`: the address the application binds to. This is ordinary configuration.
- `DATABASE_URL`: may contain database credentials. Treat it as secret.
- `JWT_SIGNING_KEY`: a token signing key. Treat it as secret and define a rotation procedure.

Putting all of these values into Dockerfile `ENV` instructions makes the image less reusable and can mix secret material into image layers or registry access boundaries. Putting every value into a Secret hides ordinary configuration from normal review. The goal of this post is not just to choose an object, but to assign an operational responsibility.

## Verified Facts

- Kubernetes documentation describes ConfigMaps as API objects for storing non-confidential data in key-value pairs. A ConfigMap can decouple environment-specific configuration from container images.
  Evidence: [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- Kubernetes documentation describes Secrets as objects for sensitive data such as passwords, tokens, or keys. The same documentation warns that Secrets are, by default, stored unencrypted in the API server's underlying data store, so RBAC and encryption at rest are part of the real security boundary.
  Evidence: [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- A ConfigMap can be consumed as environment variables, command arguments, or mounted files. ConfigMaps consumed as environment variables are not updated automatically for already-running containers.
  Evidence: [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- Kubernetes supports `env`, `envFrom`, `configMapKeyRef`, and `secretKeyRef` patterns for container environment variables.
  Evidence: [Define Environment Variables for a Container](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/)

## Practice Baseline

This post assumes the application reads final values through `std::env` or a configuration loader. Earlier posts covered Rust-side configuration parsing. Here, the boundary is the Kubernetes manifest.

Use this operating table:

| Value | Object | Injection | Operational rule |
| --- | --- | --- | --- |
| `RUST_LOG` | ConfigMap | explicit `env` | Restart the Deployment after changing it |
| `APP_BIND_ADDR` | ConfigMap | explicit `env` | Manifest value overrides image defaults |
| `APP_ENV` | ConfigMap | explicit `env` | Store only environment names such as `production` or `staging` |
| `DATABASE_URL` | Secret | explicit `env` | Never log it, and restart Pods during rotation |
| `JWT_SIGNING_KEY` | Secret | explicit `env` | Document rotation and the old-key grace period |

`envFrom` is convenient, but it hides name collisions. For core service configuration, explicit mappings are easier to review.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: rust-api-config
  namespace: rust-api
data:
  RUST_LOG: info
  APP_BIND_ADDR: 0.0.0.0:8080
  APP_ENV: production
---
apiVersion: v1
kind: Secret
metadata:
  name: rust-api-secret
  namespace: rust-api
type: Opaque
stringData:
  DATABASE_URL: postgres://app:change-me@example-postgres:5432/app
  JWT_SIGNING_KEY: replace-with-a-real-rotated-key
```

This example is only for shape. Do not commit real secret values to Git. In production, use a dedicated secret-management flow such as Sealed Secrets, External Secrets, a cloud secret manager, or encrypted GitOps storage.

The Deployment should make the source of each value explicit.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rust-api
  namespace: rust-api
spec:
  template:
    spec:
      containers:
        - name: rust-api
          image: ghcr.io/example/rust-api:2027.02.09
          ports:
            - containerPort: 8080
          env:
            - name: RUST_LOG
              valueFrom:
                configMapKeyRef:
                  name: rust-api-config
                  key: RUST_LOG
            - name: APP_BIND_ADDR
              valueFrom:
                configMapKeyRef:
                  name: rust-api-config
                  key: APP_BIND_ADDR
            - name: APP_ENV
              valueFrom:
                configMapKeyRef:
                  name: rust-api-config
                  key: APP_ENV
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: rust-api-secret
                  key: DATABASE_URL
            - name: JWT_SIGNING_KEY
              valueFrom:
                secretKeyRef:
                  name: rust-api-secret
                  key: JWT_SIGNING_KEY
```

Apply and inspect the objects separately from application behavior.

```bash
kubectl apply -f k8s/config.yaml
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/rust-api -n rust-api
kubectl describe deployment/rust-api -n rust-api
```

When a ConfigMap or Secret value is injected through environment variables, include a rollout restart in the change procedure.

```bash
kubectl apply -f k8s/config.yaml
kubectl rollout restart deployment/rust-api -n rust-api
kubectl rollout status deployment/rust-api -n rust-api
```

Be careful with Secret inspection commands. The routine runbook should not print secret data.

```bash
kubectl get secret rust-api-secret -n rust-api
kubectl describe secret rust-api-secret -n rust-api
```

## Observations

No live-cluster output is included in this post. During verification, check these observable outcomes:

- A wrong ConfigMap or Secret name should leave evidence in Pod events or container startup state.
- A missing required key should either prevent container start or fail the application startup validation.
- ConfigMap values injected as environment variables should be treated as restart-bound values.
- Secret values must not appear in logs, panic output, tracing fields, or configuration dumps.

## Interpretation

The practical difference between ConfigMap and Secret is larger than the Kubernetes object name. A ConfigMap change can usually go through normal configuration review. A Secret change should track who generated the value, where it is stored, how it rotates, and when the old value is retired.

From the Rust API's point of view, both can become environment variables. That means application validation should be based on meaning, not source. For example, an empty `DATABASE_URL` should fail startup, while an empty `RUST_LOG` may fall back to a default.

`envFrom` is useful for demos and low-risk groups of values. For production-facing service settings, explicit `env` entries are clearer because they prevent hidden key exposure and make review easier.

## Limitations

- This post stays within built-in Kubernetes objects. Cloud secret managers, Vault, External Secrets Operator, and Sealed Secrets are outside the detailed scope.
- A Secret object is not enough without RBAC, encryption at rest, audit policy, and a rotation process.
- Mounted ConfigMap and Secret volumes have different update behavior from environment-variable injection. This post's default examples use environment variables.
- The manifest examples are structural. They are not a recommendation to store real secret values in Git.

## References

- [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Define Environment Variables for a Container](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/)
- [Distribute Credentials Securely Using Secrets](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/)

## Change Log

- 2026-05-05: Rewrote the ConfigMap, Secret, and environment-variable injection guidance using Kubernetes official documentation.
