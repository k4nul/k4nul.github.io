---
layout: single
title: "Rust Service 29. Reading Kubernetes RBAC from a service operations view"
description: "Revisits ServiceAccounts, Roles, RoleBindings, and deployment permissions for Rust API operations."
date: 2027-04-06 09:00:00 +09:00
lang: en
translation_key: rust-api-kubernetes-rbac-service-operations
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
permalink: /en/rust/rust-api-kubernetes-rbac-service-operations/
---

## Summary

If a Rust API does not call the Kubernetes API, its runtime Pod should not need permission to read or modify Kubernetes resources.

From a service operations view, RBAC is less about memorizing object names and more about separating identities: runtime permissions, CI deployment permissions, and operator read permissions should not be merged into one broad account.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Running non-root containers with least privilege
- Next post: Production readiness checklist before deployment

## Document Information

- Written date: 2026-05-05
- Verification date: 2026-05-05
- Document type: tutorial | analysis
- Test environment: Document review only. The commands below are verification commands to reproduce against the publication example cluster.
- Tested versions: This post does not pin a Kubernetes version. Record the target Kubernetes and `kubectl` versions before publishing execution results.
- Evidence level: official Kubernetes documentation, operational interpretation

## Problem Statement

Kubernetes permissions often grow through small conveniences: add a permission, unblock the deployment, keep it forever. That habit increases both the debugging surface and the security blast radius.

The service in this series is a normal Axum-based Rust API. It handles HTTP requests and talks to its configured dependencies. It does not need to read Kubernetes Deployments or Secrets. If that is true, the runtime ServiceAccount should also be small, and in many cases the Pod should not receive an API token at all.

## Verified Facts

- Kubernetes RBAC grants API permissions through `Role`, `ClusterRole`, `RoleBinding`, and `ClusterRoleBinding`.
- RBAC permissions are additive. The model grants allowed actions; it does not add separate deny rules to subtract permissions.
- A `Role` defines permissions inside a namespace. A `ClusterRole` can define cluster-scoped permissions, and a `RoleBinding` can reference a `ClusterRole` to grant the permissions only inside one namespace.
- A ServiceAccount is a Kubernetes identity used by workloads such as Pods when they authenticate to the Kubernetes API.
- `kubectl auth can-i` can check whether a subject can perform an action.
- These facts were checked against official Kubernetes documentation on 2026-05-05.

## Split Three Identities

Start with three identities:

| Identity | Example name | Should do | Should not do |
| --- | --- | --- | --- |
| Runtime Pod | `rust-api-runtime` | Run the Rust API process | Read Secrets, modify Deployments, list Pods |
| CI/CD deployer | `rust-api-deployer` | Update the intended Deployment | Hold cluster-wide permissions or broad Secret reads |
| Operator reader | `rust-api-reader` | Read Pods, Events, and logs | Modify resources or read Secret values |

This split reduces the size of mistakes. If the API container is compromised, deployment authority is not automatically exposed. If CI credentials are misconfigured, they are not also the human read-only account.

## Runtime ServiceAccount

If the service does not call the Kubernetes API, the runtime ServiceAccount does not need RBAC bindings. It can also opt out of automatic token mounting.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rust-api-runtime
  namespace: rust-api
automountServiceAccountToken: false
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rust-api
  namespace: rust-api
spec:
  template:
    spec:
      serviceAccountName: rust-api-runtime
      automountServiceAccountToken: false
      containers:
        - name: api
          image: ghcr.io/example/rust-api:1.0.0
```

There is no `RoleBinding` here. That absence is the point. The runtime API should operate without Kubernetes API permissions.

Verify the boundary:

```bash
kubectl auth can-i get pods \
  --as=system:serviceaccount:rust-api:rust-api-runtime \
  -n rust-api
```

The expected answer is `no`. For a service that does not use the Kubernetes API, that is a good result.

## Operator Read Permissions

Operators may need to inspect Pods, Events, and logs during incidents. Read permission should still be scoped. In particular, `get`, `list`, and `watch` on `secrets` should not be added casually.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: rust-api-reader
  namespace: rust-api
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log", "events", "services", "endpoints"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: rust-api-reader
  namespace: rust-api
subjects:
  - kind: ServiceAccount
    name: rust-api-reader
    namespace: rust-api
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: rust-api-reader
```

Read-only access exists for diagnosis. Keep it separate from deployment mutation.

## CI Deployment Permissions

CI should have a narrower job. If the pipeline only updates an image tag or digest for one Deployment, `get`, `patch`, and `update` on that Deployment may be enough.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: rust-api-deployer
  namespace: rust-api
rules:
  - apiGroups: ["apps"]
    resources: ["deployments"]
    resourceNames: ["rust-api"]
    verbs: ["get", "patch", "update"]
  - apiGroups: ["apps"]
    resources: ["replicasets"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: rust-api-deployer
  namespace: rust-api
subjects:
  - kind: ServiceAccount
    name: rust-api-deployer
    namespace: rust-api
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: rust-api-deployer
```

`resourceNames` can narrow the permission to a specific Deployment. It does not fit every operation, so verify the actual API calls made by the deployment command.

Check the expected permission:

```bash
kubectl auth can-i patch deployment/rust-api \
  --as=system:serviceaccount:rust-api:rust-api-deployer \
  -n rust-api
```

This should return `yes`. Secret reads should still return `no`:

```bash
kubectl auth can-i get secrets \
  --as=system:serviceaccount:rust-api:rust-api-deployer \
  -n rust-api
```

## Settings To Avoid

Using `cluster-admin` for service deployment convenience is almost always too broad. Wildcard resources and wildcard verbs are similar warning signs.

Stop and review when you see these patterns:

- The runtime Pod and CI pipeline use the same ServiceAccount.
- The API container mounts a ServiceAccount token without a reason.
- A `ClusterRoleBinding` is used even though only one namespace is needed.
- Log access is bundled with broad Secret read access.
- Temporary incident permissions have no owner, expiration, or removal issue.

RBAC is easier to grow than to shrink. Because rules add permissions, start small and add only what a reproduced operation needs.

## Operations Checklist

- Does the runtime ServiceAccount set `automountServiceAccountToken: false`?
- Does the runtime ServiceAccount avoid unnecessary `RoleBinding` objects?
- Is CI deployment authority scoped to the namespace and resource it updates?
- Are operator read permissions separated from mutation permissions?
- Is every Secret read permission documented with a reason?
- Are `kubectl auth can-i` results captured before deployment?

## Limitations

- Kubernetes Operators and controllers that intentionally call the API server need a different runtime RBAC design.
- Managed Kubernetes IAM, OIDC federation, and external secret manager permission models vary by provider and need separate review.
- `kubectl auth can-i` checks authorization. It does not prove that the workload only sends intended requests.

## References

- [Kubernetes: Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)
- [Kubernetes: Service Accounts](https://kubernetes.io/docs/concepts/security/service-accounts/)
- [Kubernetes: Configure Service Accounts for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)

## Change Log

- 2026-05-05: Replaced scaffold text with runtime, CI, and operator permission separation criteria plus verification commands.
