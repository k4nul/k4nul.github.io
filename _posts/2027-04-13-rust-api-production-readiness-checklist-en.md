---
layout: single
title: "Rust Service 30. Production readiness checklist before deployment"
description: "Combines functionality, configuration, security, observability, and rollback criteria into a pre-deployment checklist for a Rust API."
date: 2027-04-13 09:00:00 +09:00
lang: en
translation_key: rust-api-production-readiness-checklist
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
permalink: /en/rust/rust-api-production-readiness-checklist/
---

## Summary

The final post in this series does not add a new feature. It checks whether the Rust API built so far is ready to behave as an operable service.

A useful checklist does not say "we looked carefully." It says what should stop a deployment. This post ties code, configuration, images, Kubernetes manifests, observability, security, and rollback into one pre-deployment table.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Reading Kubernetes RBAC from a service operations view
- Next post: None. This closes the 30-topic curriculum.

## Document Information

- Written date: 2026-05-05
- Verification date: 2026-05-05
- Document type: tutorial | analysis
- Test environment: Document review only. Before publication, record the example repository, CI results, image digest, and Kubernetes deployment result.
- Tested versions: This post does not pin versions. Record Rust, Docker, GitHub Actions, Kubernetes, and observability tool versions before publishing execution results.
- Evidence level: official Kubernetes documentation, official Docker documentation, official GitHub Actions documentation, operational interpretation

## Problem Statement

Production readiness becomes shaky when it is judged by mood. Tests can pass while Secrets leak into logs. An image can build while non-root execution is broken. A Deployment can apply while no rollback command is ready.

This checklist does not replace a full security review. It defines the minimum checks a small Rust API should satisfy before it is deployed into an operating environment.

## Verified Facts

- Kubernetes documentation treats production environment setup as a separate topic.
- Kubernetes security documentation provides separate guidance for Pod Security Standards, Security Context, ServiceAccounts, RBAC, Secret handling, and security checklists.
- Docker Build documentation covers image builds, cache, build context, and related production image concerns.
- GitHub Actions security documentation covers workflow permissions, secret handling, and third-party action risk.
- These facts were checked against official documentation on 2026-05-05.

## Pre-Deployment Checklist

| Area | Check | Stop condition |
| --- | --- | --- |
| Code quality | `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, and `cargo test` pass in CI. | Warnings are ignored or only local checks passed. |
| API contract | Request and response schemas, error responses, and validation failures match the documentation. | A client-visible field changed without explanation. |
| Configuration | Required environment variables are documented, with defaults separated from production values. | Production Secrets or URLs appear in code, image layers, or logs. |
| Database | Migration order and rollback impact are recorded. | A non-reversible schema change has no approval record. |
| Image | Multi-stage build, `.dockerignore`, non-root `USER`, image digest, and SBOM or scan result are checked. | Only `latest` is deployed or root execution remains. |
| Kubernetes manifests | Deployment, Service, ConfigMap, Secret references, probes, resource requests and limits, and security context are reviewed together. | Replicas are changed without probe or resource criteria. |
| Network | Ingress, TLS, CORS, request size, and rate limit criteria are explicit. | The external exposure path differs from the documented path. |
| Observability | Structured logs, metrics, traces, dashboards, and alerts share route and service labels. | Nobody knows which signal to inspect after failure. |
| Security permissions | Runtime ServiceAccount, CI deployer, and operator reader permissions are separated. | The runtime Pod has an unnecessary API token or cluster-admin-like authority. |
| Rollout | `kubectl rollout status` and failure stop conditions are defined. | Deployment success means only "the YAML applied." |
| Rollback | Previous image digest, migration impact, and `kubectl rollout undo` feasibility are recorded. | There is no known version or command to roll back to. |

## Command Baseline

A checklist is weak if it cannot be repeated. Keep the commands CI and operators should run.

```bash
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```

Record image results by digest, not only by tag.

{% raw %}
```bash
docker build -t ghcr.io/example/rust-api:1.0.0 .
docker image inspect ghcr.io/example/rust-api:1.0.0 --format '{{.Id}} {{.Config.User}}'
```
{% endraw %}

Before deployment, check manifests against the server-side schema.

```bash
kubectl apply --dry-run=server -f k8s/
kubectl diff -f k8s/
```

During deployment, check rollout and health together.

```bash
kubectl rollout status deployment/rust-api -n rust-api
kubectl get pods -n rust-api -l app.kubernetes.io/name=rust-api
kubectl logs deployment/rust-api -n rust-api --tail=100
```

Keep RBAC evidence from the previous post:

```bash
kubectl auth can-i get secrets \
  --as=system:serviceaccount:rust-api:rust-api-runtime \
  -n rust-api
```

For this service, the expected answer is `no`.

## Go / No-Go Decision

| Decision | Meaning |
| --- | --- |
| Go | Code tests, image criteria, manifest checks, observability, and rollback planning are all satisfied. |
| Conditional Go | The risk is small, reversible, and recorded as an exception with an owner and expiration. |
| No-Go | Data loss, Secret exposure, irreversible migration risk, excessive permissions, or unobservable failure risk remains. |

`Conditional Go` is not a shortcut. If an exception has no owner, removal condition, and review date, treat it as `No-Go`.

## Deployment Record

After deployment, store these facts in one place:

- Deployed Git commit SHA
- Deployed image tag and digest
- Applied migrations
- `kubectl rollout status` result
- Health check result
- Dashboard link or screenshot location
- Alerts that fired and how they were handled
- Whether rollback happened, and why

This record makes the next incident easier. It stops the team from relying on memory for what changed.

## Limitations

- This checklist targets a general Rust API. Regulated systems such as payment, healthcare, privacy-sensitive, or financial systems need separate audit and control procedures.
- Managed Kubernetes, registries, secret managers, and observability backends vary by provider.
- Passing the checklist does not guarantee there will be no incidents. It checks whether the service can be observed, operated, and rolled back when something goes wrong.

## References

- [Kubernetes: Production environment](https://kubernetes.io/docs/setup/production-environment/)
- [Kubernetes: Security Checklist](https://kubernetes.io/docs/concepts/security/security-checklist/)
- [Kubernetes: Application Security Checklist](https://kubernetes.io/docs/concepts/security/application-security-checklist/)
- [Docker Build documentation](https://docs.docker.com/build/)
- [GitHub Actions: Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)

## Change Log

- 2026-05-05: Replaced scaffold text with a pre-deployment Go/No-Go checklist, verification commands, and deployment record criteria.
