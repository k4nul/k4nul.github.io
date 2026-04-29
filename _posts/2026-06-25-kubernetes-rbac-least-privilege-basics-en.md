---
layout: single
title: "Kubernetes RBAC least privilege basics"
description: "Explains Kubernetes RBAC least privilege basics with official documentation, operational checks, and limitations."
date: 2026-06-25 09:00:00 +09:00
lang: en
translation_key: kubernetes-rbac-least-privilege-basics
section: security
topic_key: security-engineering
categories: Security
tags: [security, devsecops, supply-chain-security, cloud-security]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/security/kubernetes-rbac-least-privilege-basics/
---

## Summary

Kubernetes RBAC least privilege means binding only the required resources and verbs to the required subject. Start by separating Role from ClusterRole, RoleBinding from ClusterRoleBinding, and `apiGroups/resources/verbs` from the users or service accounts that receive them.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: tutorial | analysis
- Test environment: No live execution. This post summarizes concepts and checks from Kubernetes RBAC official documentation.
- Test version: Kubernetes documentation checked on 2026-04-29. No local cluster or kubectl version is fixed.
- Evidence level: official documentation

## Problem Statement

The common beginner mistake is to use `cluster-admin`, wildcard resources, wildcard verbs, or ClusterRoleBinding for convenience. That may make the first workload run, but it can grant access to current and future resources that the workload does not need.

This post explains how to read Kubernetes RBAC from a least-privilege perspective.

## Verified Facts

- Kubernetes RBAC uses the `rbac.authorization.k8s.io` API group to configure authorization decisions.
  Evidence: [Kubernetes RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- A Role defines permissions inside a namespace, while a ClusterRole defines cluster-scoped permissions or reusable permissions.
  Evidence: [Kubernetes Role and ClusterRole](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-and-clusterrole)
- RBAC permissions are additive and do not include deny rules.
  Evidence: [Kubernetes RBAC API objects](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#api-objects)
- Kubernetes documentation warns that wildcard resources or verbs can grant overly permissive access.
  Evidence: [Kubernetes RBAC wildcard caution](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#referring-to-resources)
- Pod logs are represented as the `pods/log` subresource.
  Evidence: [Kubernetes RBAC subresource example](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#referring-to-resources)

## Reproduction Steps

Use this order when designing a least-privilege Role.

1. Choose the subject: user, group, or service account.
2. Choose the namespace scope: if the access is namespace-specific, prefer Role and RoleBinding first.
3. Choose resources: for example `pods`, `pods/log`, `configmaps`, or `deployments`.
4. Choose verbs: only the required subset of `get`, `list`, `watch`, `create`, `update`, `patch`, and `delete`.
5. Avoid `*`: do not start with `resources: ["*"]` or `verbs: ["*"]`.
6. Bind the role: the Role defines permissions, and the RoleBinding grants them to a subject.
7. Verify with `kubectl auth can-i`.

For example, if an application service account only needs to list Pods and read Pod logs in one namespace:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-log-reader
  namespace: app
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-pod-log-reader
  namespace: app
subjects:
  - kind: ServiceAccount
    name: app-reader
    namespace: app
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: pod-log-reader
```

Verification examples:

```bash
kubectl auth can-i get pods --as=system:serviceaccount:app:app-reader -n app
kubectl auth can-i get pods/log --as=system:serviceaccount:app:app-reader -n app
kubectl auth can-i delete pods --as=system:serviceaccount:app:app-reader -n app
```

The last command should return `no` for the Role above.

## Observations

- Role and ClusterRole define what can be done. RoleBinding and ClusterRoleBinding define who receives that permission.
- ClusterRoleBinding can grant access across the cluster, so it deserves more caution than a namespace RoleBinding.
- Access to `pods` does not automatically mean access to `pods/log`. Subresources should be reviewed explicitly.

## Interpretation

In my view, least privilege starts from the actual API requests a workload needs, not from a broad "read-only" label. `get pods`, `list pods`, `get pods/log`, and `watch deployments` are different permissions.

Opinion: start narrowly with a namespace Role, then consider reusable ClusterRoles only when the same permission set is needed across namespaces.

## Limitations

- Real authorization also depends on authentication, admission controllers, aggregation, and API server settings.
- Managed Kubernetes environments can differ in default ClusterRoles, service account token behavior, and workload identity integration.
- This is an RBAC introduction. It does not cover Pod Security, NetworkPolicy, cloud IAM, or secret rotation.

## References

- [Kubernetes RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Kubernetes RBAC Role and ClusterRole](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-and-clusterrole)
- [Kubernetes RBAC Referring to resources](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#referring-to-resources)
- [Kubernetes Authorization overview](https://kubernetes.io/docs/reference/access-authn-authz/authorization/)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added core RBAC objects, least-privilege manifest, verification commands, and official-documentation evidence.
