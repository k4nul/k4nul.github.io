---
layout: single
title: "Rust Service 28. Running non-root containers with least privilege"
description: "Sets least-privilege runtime criteria for a Rust API container using non-root users, read-only root filesystems, and dropped capabilities."
date: 2027-03-30 09:00:00 +09:00
lang: en
translation_key: rust-api-non-root-container-security
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
permalink: /en/rust/rust-api-non-root-container-security/
---

## Summary

A small Rust API binary normally does not need root privileges. If the container can bind to an unprivileged port, write only to explicitly mounted paths, and read configuration from environment variables, running it as root is unnecessary risk.

This post turns that idea into a deployable baseline: set a non-root user in the image, repeat the intent in Kubernetes `securityContext`, drop Linux capabilities, keep the root filesystem read-only, and make every writable directory explicit.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Debugging intentional failures with describe, events, and logs
- Next post: Reading Kubernetes RBAC from a service operations view

## Document Information

- Written date: 2026-05-05
- Verification date: 2026-05-05
- Document type: tutorial | analysis
- Test environment: Document review only. The commands below are verification commands to run against the example repository and cluster used for publication.
- Tested versions: Environment-specific in this post. Recheck Rust, Docker, and Kubernetes versions in the target environment before publishing execution results.
- Evidence level: official Docker documentation, official Kubernetes documentation, operational interpretation

## Problem Statement

The service built in this series is a single Rust API process. It accepts HTTP traffic, talks to its configured dependencies, and exposes health or metrics endpoints. None of those jobs require UID 0.

The production boundary is therefore simple: the image and the Pod manifest should both say "this process is not root." Relying on only one layer is weaker than making the intent visible in both places.

## Verified Facts

- Dockerfile has a `USER` instruction that sets the user or UID used for subsequent `RUN`, `CMD`, and `ENTRYPOINT` instructions.
- Kubernetes security context fields can set process identity and container restrictions such as `runAsUser`, `runAsGroup`, `runAsNonRoot`, capabilities, read-only root filesystem, and seccomp profile.
- Kubernetes Pod Security Standards include restrictions around privileged containers, privilege escalation, capabilities, and seccomp profiles.
- These facts were checked against official Docker and Kubernetes documentation on 2026-05-05.

## Image Baseline

The runtime image should not depend on a root shell to start the API. A typical Dockerfile sets ownership at copy time and switches to a numeric user before the final command:

```dockerfile
FROM gcr.io/distroless/cc-debian12:nonroot

WORKDIR /app
COPY --chown=65532:65532 target/release/rust-api /app/rust-api

USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/app/rust-api"]
```

The important part is not this exact base image. The important part is that the final image has a known non-root identity and the binary can start without writing into the image filesystem.

For an Axum service, avoid port `80` inside the container unless there is a specific reason. Listening on `8080` avoids the old need for privileged low ports, while Kubernetes `Service` and `Ingress` can still expose normal public ports outside the Pod.

## Kubernetes Baseline

The Pod manifest should express the same runtime intent:

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
      app.kubernetes.io/name: rust-api
  template:
    metadata:
      labels:
        app.kubernetes.io/name: rust-api
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 65532
        runAsGroup: 65532
        fsGroup: 65532
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: api
          image: ghcr.io/example/rust-api:1.0.0
          ports:
            - containerPort: 8080
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
```

This manifest separates two ideas.

First, the Pod-level `securityContext` defines the expected identity for processes and mounted volumes. Second, the container-level `securityContext` removes privileges the process should not need.

`readOnlyRootFilesystem: true` is useful only when writable paths are planned. If the Rust service, TLS library, logging setup, or temporary file handling writes to `/tmp`, mount `/tmp` explicitly. The manifest above does that with `emptyDir`.

## Verification Commands

Before deployment, inspect the image identity:

{% raw %}
```bash
docker image inspect ghcr.io/example/rust-api:1.0.0 \
  --format '{{.Config.User}}'
```
{% endraw %}

After deployment, confirm the Pod accepted the security context:

```bash
kubectl get pod -n rust-api -l app.kubernetes.io/name=rust-api \
  -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.spec.securityContext.runAsNonRoot}{"\n"}{end}'
```

Then verify that the application still starts and serves traffic:

```bash
kubectl rollout status deployment/rust-api -n rust-api
kubectl logs deployment/rust-api -n rust-api --tail=50
kubectl port-forward service/rust-api 8080:80 -n rust-api
curl -fsS http://127.0.0.1:8080/healthz
```

The success condition is not "the YAML applied." The success condition is "the API runs with the restricted identity and still passes its health checks."

## Failure Modes

If the container fails with a permission error, do not remove all security settings at once. Identify the path or privilege that failed.

Common fixes are narrow:

- Mount a writable `emptyDir` for `/tmp` or another explicit cache directory.
- Change file ownership at image build time instead of running the container as root.
- Keep `readOnlyRootFilesystem` enabled and move mutable state out of the image layer.
- Add one specific capability only when a measured dependency proves it is required.

For a normal HTTP API, adding `privileged: true`, mounting the host filesystem, or granting broad Linux capabilities is a sign that the service boundary has been lost.

## Operational Rule

The runtime contract for this series is:

1. The image declares a non-root user.
2. The Pod declares `runAsNonRoot: true`.
3. The container drops all capabilities by default.
4. The root filesystem is read-only.
5. Writable paths are listed as volumes.
6. Any exception is recorded with a reason, owner, and removal condition.

That final exception log matters. Security settings often decay through small emergency changes. Recording the reason keeps the exception visible after the incident is over.

## Limitations

- This post does not prove that every base image is secure. It covers runtime privilege boundaries for the API container.
- Distroless images may not include a shell, so debugging commands that require `sh` should be planned through logs, ephemeral containers, or a separate debug image.
- `fsGroup` behavior can vary with storage drivers and volume types; verify mounted volume ownership in the target cluster.
- Sidecars and init containers need their own security contexts. A safe API container does not automatically make the whole Pod safe.

## References

- [Dockerfile reference: USER](https://docs.docker.com/reference/dockerfile/#user)
- [Kubernetes: Configure a Security Context for a Pod or Container](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
- [Kubernetes: Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Kubernetes: Linux kernel security constraints for Pods and containers](https://kubernetes.io/docs/concepts/security/linux-kernel-security-constraints/)

## Change Log

- 2026-05-05: Replaced scaffold draft with a reviewed non-root container baseline, Kubernetes security context example, verification commands, and limitations.
