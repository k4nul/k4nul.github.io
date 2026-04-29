---
layout: single
title: "Kubernetes troubleshooting with describe, events, and logs"
description: "Explains Kubernetes troubleshooting with describe, events, and logs with official documentation, operational checks, and limitations."
date: 2026-06-18 09:00:00 +09:00
lang: en
translation_key: kubernetes-troubleshooting-describe-events-logs
section: development
topic_key: devops
categories: DevOps
tags: [devops, kubernetes, troubleshooting, operations]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/kubernetes-troubleshooting-describe-events-logs/
---

## Summary

In Kubernetes troubleshooting, `describe`, `events`, and `logs` answer different questions. `describe` shows the object's current state and recent events, `events` shows control-plane and kubelet decisions over time, and `logs` shows what the containerized application wrote after it started.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: tutorial | analysis
- Test environment: No live execution. This post is based on Kubernetes official documentation and kubectl reference pages.
- Test version: Kubernetes documentation checked on 2026-04-29. No local cluster or kubectl version is fixed.
- Evidence level: official documentation

## Problem Statement

Jumping straight to `kubectl logs` can miss failures that happen before the container starts, such as scheduling or image pull failures. Looking only at events can miss application exceptions that happen inside a running container.

This post gives a first-response order for Pod or Deployment failures using `describe`, `events`, and `logs`.

## Verified Facts

- Kubernetes debug documentation separates application state, events, and logs as troubleshooting inputs.
  Evidence: [Kubernetes Debug Applications](https://kubernetes.io/docs/tasks/debug/debug-application/)
- Kubernetes documentation demonstrates using `kubectl describe pod` to inspect events for a Pending Pod.
  Evidence: [Kubernetes Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)
- Official documentation shows `kubectl logs ${POD_NAME} -c ${CONTAINER_NAME}` for current logs and `--previous` for a previously crashed container.
  Evidence: [Kubernetes Examining pod logs](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#examining-pod-logs)
- `kubectl events` can show namespace-wide events, all-namespace events, or events filtered to a specific resource.
  Evidence: [kubectl events](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_events/)

## Reproduction Steps

The first goal is to identify where the workload stopped.

1. Find the affected workload.

```bash
kubectl get pods -n <namespace>
kubectl get deploy,rs,pod -n <namespace>
```

2. Inspect the Pod description.

```bash
kubectl describe pod <pod-name> -n <namespace>
```

Check these fields first:

- `Status`, `Conditions`: `PodScheduled`, `Initialized`, `Ready`, `ContainersReady`
- `Containers`: image, command, args, ports, env, mounts
- `State`, `Last State`, `Restart Count`
- `Events`: scheduler, kubelet, image pull, and probe messages

3. Re-read events in time order.

```bash
kubectl events -n <namespace> --for pod/<pod-name>
kubectl events -n <namespace> --types=Warning
kubectl events --all-namespaces --types=Warning
```

When many Pods fail together, namespace-level or cluster-level events can be faster than per-Pod `describe`.

4. Read container logs.

```bash
kubectl logs <pod-name> -n <namespace> -c <container-name>
kubectl logs <pod-name> -n <namespace> -c <container-name> --previous
```

`--previous` matters for cases such as `CrashLoopBackOff`, where the current container may have already restarted.

5. Classify likely causes by status.

- `Pending` + `FailedScheduling`: node selector, taint/toleration, resource request, or PVC binding
- `ImagePullBackOff` or `ErrImagePull`: image name, tag, registry auth, network, or pull policy
- `CrashLoopBackOff`: `Last State`, exit code, `--previous` logs, or probe configuration
- `Running` but `Ready=False`: readiness probe, dependency, or service endpoint
- Normal events but application failure: app log, config, secret mount, or environment variable

## Observations

- `describe` is a compact view of one object's current state plus recent events.
- `events` is better for the timeline of scheduler, controller, and kubelet decisions.
- `logs` only helps after the container has emitted output. If the Pod fails before startup, logs may be empty.

## Interpretation

In my view, the useful default order is: use `describe` to narrow the layer, use `events` to understand the control-plane timeline, then use `logs` to inspect application behavior inside the container.

Opinion: incident notes should keep namespace, pod, container, commands run, key event reason, exit code, restart count, and whether `--previous` was used. That is usually more useful than pasting the entire raw log.

## Limitations

- Kubernetes events are not a long-term incident archive. Long-running investigations need separate logging and observability.
- Managed Kubernetes, CNI, CSI, registry, and node OS differences can change the exact messages and likely causes.
- This post covers first response for Pod/Deployment issues, not the full space of control-plane, DNS, storage, or network-policy failures.

## References

- [Kubernetes Debug Applications](https://kubernetes.io/docs/tasks/debug/debug-application/)
- [Kubernetes Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)
- [kubectl describe](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe)
- [kubectl logs](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#logs)
- [kubectl events](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_events/)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added `describe`, `events`, and `logs` troubleshooting order with status-based interpretation.
