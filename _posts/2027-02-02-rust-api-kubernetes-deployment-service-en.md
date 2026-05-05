---
layout: single
title: "Rust Service 20. Deploying with Kubernetes Deployment and Service"
description: "Defines the minimal Kubernetes Deployment and Service boundary for a containerized Rust API."
date: 2027-02-02 09:00:00 +09:00
lang: en
translation_key: rust-api-kubernetes-deployment-service
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
permalink: /en/rust/rust-api-kubernetes-deployment-service/
---

## Summary

Putting an app on Kubernetes means declaring desired replicas and network access points, not merely running one container.

A Deployment manages the desired state and rollout for Pod replicas. A Service creates a stable access point in front of Pods. The first manifest should keep those responsibilities separate.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Reading SBOMs and image scan results
- Next post: Choosing ConfigMap, Secret, and env injection rules
- Expansion criteria: before publication, record `kubectl apply`, rollout status, Service endpoint status, port-forward health check, and one failure event from a local Kubernetes environment.

## Document Information

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial / Kubernetes manifest boundary design
- Test environment: No direct Kubernetes cluster execution. This post documents the minimum Deployment and Service manifest boundary.
- Checked documents: Kubernetes v1.36 documentation for Deployment, Service, port-forward, and kubectl reference
- Evidence level: Kubernetes official documentation

## Problem Statement

After building and scanning the Docker image, the next step is deploying it to Kubernetes. Adding Ingress, TLS, ConfigMap, Secret, probes, resource limits, and HPA all at once makes failures harder to place.

This post answers only two questions:

- Does the Deployment create and maintain the desired number of Rust API Pods?
- Does the Service select those Pods and provide a stable access point?

ConfigMap, Secret, probes, resources, and Ingress are added in later posts.

## Verified Facts

- Kubernetes Deployment documentation says a Deployment provides declarative updates for Pods and ReplicaSets.
- The Deployment controller observes Deployments and creates ReplicaSets to bring up the desired Pods.
- Kubernetes Deployment documentation says selectors and Pod template labels must be specified appropriately, and overlapping selectors across controllers can create unexpected behavior.
- Kubernetes Service documentation describes Service as a way to expose an application as a network service.
- Services commonly use selectors to abstract access to Kubernetes Pods.
- Kubernetes Service types include ClusterIP, NodePort, and LoadBalancer. For the first internal check, ClusterIP plus `kubectl port-forward` is the simplest path.

## Minimal Manifest

Keep the first manifest intentionally small. A digest is stronger than a tag for reproducibility, but this example uses a tag for readability. The actual deployment record should include the digest.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rust-api
  labels:
    app: rust-api
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
          image: ghcr.io/org/rust-api:v0.3.0
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 3000
---
apiVersion: v1
kind: Service
metadata:
  name: rust-api
  labels:
    app: rust-api
spec:
  type: ClusterIP
  selector:
    app: rust-api
  ports:
    - name: http
      port: 80
      targetPort: http
```

This is not a production-complete manifest. Probes, resources, securityContext, config, secrets, and ingress are missing on purpose. First verify the basic Deployment and Service connection.

## Field Boundaries

Each field should have an explainable responsibility.

| Field | Location | Meaning |
| --- | --- | --- |
| `spec.replicas` | Deployment | Number of Pods to maintain |
| `spec.selector.matchLabels` | Deployment | Pod labels managed by this Deployment |
| `template.metadata.labels` | Deployment Pod template | Labels placed on new Pods |
| `containers.image` | Pod template | Image to run |
| `containerPort` | Pod template | Documents the port the container listens on |
| `spec.selector` | Service | Pod labels that receive Service traffic |
| `ports.port` | Service | Port exposed by the Service |
| `ports.targetPort` | Service | Pod container port or named port |

If the Deployment selector and Pod template labels do not match, the Deployment cannot manage the intended Pods. If the Service selector and Pod labels do not match, the Service may have no endpoints.

## Reproduction Steps

Before publication, run this against an actual cluster. The example namespace is `rust-api`.

1. Create the namespace and apply the manifest.

```powershell
kubectl create namespace rust-api
kubectl apply -n rust-api -f k8s/deployment-service.yaml
```

2. Check the Deployment rollout.

```powershell
kubectl rollout status deployment/rust-api -n rust-api
kubectl get deploy,rs,pods -n rust-api -l app=rust-api
```

3. Check the Service and endpoint state.

```powershell
kubectl get service rust-api -n rust-api
kubectl get endpointslice -n rust-api -l kubernetes.io/service-name=rust-api
```

4. Use port-forward to test the internal Service from the local machine.

```powershell
kubectl port-forward service/rust-api 8080:80 -n rust-api
curl.exe -i http://127.0.0.1:8080/health
```

5. If something fails, inspect events and logs.

```powershell
kubectl describe deployment rust-api -n rust-api
kubectl describe pod -n rust-api -l app=rust-api
kubectl logs -n rust-api -l app=rust-api --tail=100
```

## Reading Failures

Kubernetes failures rarely fit on one line.

| Symptom | First place to check | Common cause |
| --- | --- | --- |
| Pods are not created | `kubectl describe deployment` | Selector/template label mismatch, quota, admission rejection |
| Pod is `ImagePullBackOff` | `kubectl describe pod` | Image name, tag/digest, registry auth |
| Pod restarts repeatedly | `kubectl logs`, `describe pod` | App bind address, missing env, runtime crash |
| Service cannot be reached | `get endpointslice`, Service selector | Service selector and Pod labels do not match |
| port-forward fails | Service selector, Pod readiness, API server permissions | No endpoints, selectorless Service |

This post does not add readiness probes yet, but the next steps must define which Pods are ready for Service traffic.

## Observation Status

This post does not yet include actual cluster output. Before publication, add:

- Kubernetes server version and kubectl version
- Namespace used
- `kubectl apply` output
- `kubectl rollout status` output
- Deployment, ReplicaSet, and Pod list
- Service and EndpointSlice state
- `/health` response through port-forward
- One example failure event

## Verification Checklist

- Are Deployment and Service responsibilities separated even if they are in one file?
- Do the Deployment selector and Pod template labels match?
- Do the Service selector and Pod labels match?
- Does the container actually listen on a cluster-reachable address such as `0.0.0.0:3000`?
- Is the image tag or digest connected to the release record?
- Are both `kubectl rollout status` and Service endpoint checks recorded?
- Does port-forward health check confirm application response?
- Are probes/resources/config/secret/ingress explicitly left for later posts?

## Interpretation

Deployment and Service are the smallest useful operational unit for a Kubernetes deployment. A Deployment can create Pods without giving clients a stable access point. A Service can expose a name without having Pods to send traffic to.

Adding every production option up front makes YAML look mature but makes failures harder to understand. First confirm that the Deployment creates Pods, the Service selects them, and `/health` responds. Then add the next operational boundary.

## Limitations

- This post designs manifests without running them against a real cluster.
- Probes, resources, ConfigMap, Secret, Ingress, TLS, and NetworkPolicy are later topics.
- LoadBalancer Service behavior depends on cloud provider or bare-metal load balancer configuration.
- Pulling from a private registry requires imagePullSecrets and registry permission setup, which this post does not cover.

## References

- [Kubernetes: Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes: Service](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Kubernetes: Use port forwarding to access applications](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)
- [Kubernetes: kubectl reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Expanded Deployment/Service responsibility boundaries, minimal manifest, label/selector verification, rollout, endpoint, and port-forward reproduction steps using Kubernetes official documentation.
