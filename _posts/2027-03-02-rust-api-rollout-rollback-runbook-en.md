---
layout: single
title: "Rust Service 24. Writing rollout, rollback, and incident runbooks"
description: "Combines Kubernetes rollout checks, rollback decisions, and incident response runbooks for a Rust API deployment."
date: 2027-03-02 09:00:00 +09:00
lang: en
translation_key: rust-api-rollout-rollback-runbook
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
permalink: /en/rust/rust-api-rollout-rollback-runbook/
---

## Summary

Even with deployment automation, people need to know when to stop and when to roll back. A successful `kubectl rollout status` only says that the Deployment rollout progressed from Kubernetes' point of view. It does not prove that service quality is healthy.

This post combines pre-deploy checks, rollout observations, failure criteria, rollback commands, and post-incident notes into one runbook. The goal is not to memorize commands, but to preserve the same decision order during an incident.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Opening external access with Ingress and TLS boundaries
- Next post: Connecting logs, metrics, and traces with OpenTelemetry
- Scope: observing a Deployment rollout and deciding whether to continue, stop, or roll back

## Document Information

- Written date: 2026-05-05
- Verification date: 2026-05-05
- Document type: tutorial | analysis
- Test environment: No live-cluster execution test. The procedure is based on Kubernetes official documentation and a generic runbook example.
- Tested versions: Kubernetes documentation baseline. `kubectl` and cluster versions are left unspecified because no live cluster was executed for this post.
- Evidence level: official documentation

## Problem Statement

Previous posts turned the Rust API into an image and exposed it through Kubernetes Deployment, Service, and Ingress boundaries. The next question is what to do when a deployment is wrong.

Failure can appear in several forms:

- The new ReplicaSet does not become available.
- Pods are Running but readiness fails.
- HTTP 5xx rate increases.
- Latency exceeds the release threshold.
- Only a specific customer path or endpoint fails.
- The new version is fine, but an external dependency degrades at the same time.

Without a runbook, each operator runs different commands and uses a different threshold for "wait a little longer" versus "roll back now." The value of operations documentation is highest during a messy rollout.

## Verified Facts

- Kubernetes Deployments provide declarative updates for Pods and ReplicaSets. A new rollout is triggered when the Deployment Pod template changes.
  Evidence: [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- Kubernetes provides `kubectl rollout` subcommands such as `status`, `history`, `undo`, `pause`, `resume`, and `restart`.
  Evidence: [kubectl rollout](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/)
- Kubernetes documentation shows rollback to the previous revision with `kubectl rollout undo deployment/<name>` and rollback to a specific revision with `--to-revision`.
  Evidence: [Rolling Back to a Previous Revision](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-to-a-previous-revision)
- Kubernetes documentation notes that the old `--record` flag is deprecated and may be removed. Change cause should be recorded through annotations, Git commits, CI runs, release notes, or another release record.
  Evidence: [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

## Practice Baseline

Split the runbook into pre-deploy checks, rollout observation, failure decisions, rollback, and post-incident notes.

### Pre-deploy Checks

Before applying the manifest, confirm both the target and the rollback context.

```bash
kubectl config current-context
kubectl get deployment rust-api -n rust-api
kubectl rollout history deployment/rust-api -n rust-api
kubectl diff -f k8s/deployment.yaml
```

The runbook should include these fields.

| Field | Example |
| --- | --- |
| Target | `deployment/rust-api` in namespace `rust-api` |
| New image | `ghcr.io/example/rust-api:2027.03.02` |
| Previous image | Confirm from the current Deployment or release note |
| Success criteria | rollout success, `/ready` success, 5xx/latency/error logs below thresholds |
| Failure criteria | rollout timeout, sustained readiness failure, 5xx spike, key endpoint failure |
| Decision owner | deploy operator and rollback approver |

### Deploy and Observe

```bash
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/rust-api -n rust-api --timeout=180s
kubectl get deployment,replicaset,pod -n rust-api -l app=rust-api
kubectl describe deployment rust-api -n rust-api
```

Do not stop at `rollout status`. Check Service endpoints and application behavior too.

```bash
kubectl get endpointslice -n rust-api -l kubernetes.io/service-name=rust-api
kubectl logs deployment/rust-api -n rust-api --since=10m
curl -fsS https://api.example.com/ready
```

If observability is available, watch at least these signals.

| Signal | Question |
| --- | --- |
| Ready Pod count | Are new Pods actually ready for traffic? |
| HTTP 5xx rate | Did errors increase after the deployment? |
| p95/p99 latency | Did successful requests become slow? |
| Error logs | Is the same error code or panic repeated? |
| DB pool / dependency health | Is this an app change or dependency incident? |

### Rollback Decision

Rollback should be tied to predefined failure criteria.

Example criteria:

- Rollout does not finish within `180s`.
- New Pods fail readiness for more than 5 minutes.
- HTTP 5xx rate stays more than 3 times the normal baseline for 5 minutes after deployment.
- A key user path fails and cannot be mitigated with a feature flag or configuration change.
- The error strongly correlates with the new image or manifest change.

Check revision history before rolling back.

```bash
kubectl rollout history deployment/rust-api -n rust-api
kubectl rollout history deployment/rust-api -n rust-api --revision=7
```

Roll back to the previous revision.

```bash
kubectl rollout undo deployment/rust-api -n rust-api
kubectl rollout status deployment/rust-api -n rust-api --timeout=180s
```

Roll back to a specific revision when the target is known.

```bash
kubectl rollout undo deployment/rust-api -n rust-api --to-revision=7
kubectl rollout status deployment/rust-api -n rust-api --timeout=180s
```

## Observations

No live-cluster output is included in this post. During verification, record the following:

| Stage | Record |
| --- | --- |
| Before deploy | Previous image, new image, Git commit, CI run, change summary |
| During rollout | `rollout status`, ReplicaSet, Pod state, events |
| Service check | `/ready`, representative API endpoint, Ingress response |
| Observability check | 5xx, latency, error logs, trace sample |
| Rollback execution | command, target revision, operator, timestamp |
| After rollback | recovery time, remaining impact, follow-up |

A short post-incident record is enough if it captures the operating facts.

```text
Incident: 2027-03-02 rust-api deployment rollback
Start:
End:
New image:
Rolled back to:
Trigger:
Customer impact:
Commands used:
What changed:
What worked:
What failed:
Follow-up:
```

## Interpretation

Kubernetes provides rollout and rollback commands, but it does not decide when rollback is the right business or reliability decision. That decision depends on service SLOs, customer impact, data-change risk, feature flag options, and dependency status.

Even a fast-starting Rust API can be hard to roll back when migrations, database schema, message queues, cache keys, or external API contracts changed with the release. The runbook should explicitly mark changes that are not safely reversible by image rollback alone.

Do not rely only on Kubernetes rollout history for release memory. Deployment revision history records Kubernetes object changes. Operators also need Git commit, image digest, CI run, release note, approver, and change reason.

## Limitations

- This post focuses on Deployments. StatefulSet, Job, database migration, and message schema rollback require separate procedures.
- `kubectl rollout undo` depends on Deployment revision history. Check `revisionHistoryLimit` and old ReplicaSet cleanup behavior.
- A configuration change that does not change the Pod template may not create the revision you expect.
- Rollback is not always the safest response. Configuration revert, feature flag disablement, traffic draining, or a hotfix may be better.

## References

- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [kubectl rollout](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/)
- [Rolling Back to a Previous Revision](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-to-a-previous-revision)
- [kubectl rollout undo](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_undo/)

## Change Log

- 2026-05-05: Rewrote the rollout observation, rollback decision, and incident runbook guidance using Kubernetes official documentation.
