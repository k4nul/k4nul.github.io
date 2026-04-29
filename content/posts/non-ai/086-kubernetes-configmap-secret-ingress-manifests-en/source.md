---
layout: single
title: "K8S 07. Practical Manifests: ConfigMap, Secret, Ingress"
description: "A beginner-friendly guide to separating configuration, sensitive values, and external HTTP entry points in Kubernetes manifests."
date: 2026-07-12 09:00:00 +0900
lang: en
translation_key: kubernetes-configmap-secret-ingress-manifests
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, configmap, secret, ingress, manifest]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/kubernetes-configmap-secret-ingress-manifests/
---

## Summary

After writing a Deployment and Service, the next step is to move application configuration out of the image, keep sensitive values separate from code, and route HTTP traffic into the Service. In Kubernetes, this is commonly expressed with `ConfigMap`, `Secret`, and `Ingress`.

The conclusion of this post is that these objects should be understood as separation boundaries: runtime configuration, sensitive data, and external entry rules.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: tutorial
- Test environment: verified in the author's separate practice environment. OS, node details, and cluster topology are not fixed in this post.
- Test version: Kubernetes official documentation checked on 2026-04-24. The documentation site displayed v1.36 links.
- Source level: Kubernetes official documentation.
- Note: Secret encryption, external Secret management, and TLS automation are separate operational topics.

## Problem Definition

Common early manifest mistakes include:

- Putting environment-specific configuration inside the container image.
- Leaving passwords or tokens in Git as plain text.
- Assuming a Service automatically creates an external HTTP domain.
- Treating an Ingress object and an Ingress controller as the same thing.

## Verified Facts

- According to Kubernetes ConfigMap documentation, a ConfigMap is an API object that stores non-confidential key-value data.
  Evidence: [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- According to Kubernetes Secret documentation, a Secret stores a small amount of sensitive data such as a password, token, or key.
  Evidence: [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- According to Kubernetes Secret documentation, Secrets are similar to ConfigMaps but Kubernetes applies additional protection to Secret objects. Authorization configuration directly affects access to Secret data.
  Evidence: [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- According to Kubernetes Ingress documentation, Ingress manages external HTTP/HTTPS access rules to Services inside the cluster.
  Evidence: [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- According to Kubernetes Ingress documentation, the Kubernetes project recommends Gateway API instead of Ingress, and the Ingress API is frozen with no further feature changes or updates planned.
  Evidence: [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- According to Kubernetes Ingress Controllers documentation, an Ingress controller must be running in the cluster for Ingress to work.
  Evidence: [Ingress Controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)

A simple ConfigMap example:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_MODE: production
  LOG_LEVEL: info
```

Sensitive data should be separated into a Secret, not a ConfigMap.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  DB_PASSWORD: change-me
```

A Deployment can consume both objects as environment variables.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
        - name: app
          image: example/app:1.0.0
          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: app-secret
```

Ingress declares HTTP routing rules from the outside world to a Service.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app
spec:
  ingressClassName: nginx
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-svc
                port:
                  number: 80
```

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow in the author's practice environment.
- Confirmed result: based on official documentation, I separated the roles of ConfigMap, Secret, Ingress, and Ingress controller.
- Directly verified items: `kubectl apply -f`, `kubectl get configmap,secret,ingress`, `kubectl describe ingress`, and Ingress controller events.

## Interpretation / Opinion

In my view, the main difference between ConfigMap and Secret is the type of value. Non-sensitive runtime settings belong in ConfigMap. Passwords, tokens, and private keys belong in Secret.

However, using a Secret does not finish the security work. Secret access permissions, namespace boundaries, audit, encryption at rest, and CI/CD masking all matter. The `stringData` value in the example is only a placeholder.

Ingress is easier to understand as a routing rule object, not the load balancer or reverse proxy itself. The actual traffic handling is done by an Ingress controller. If there is no controller, or if `ingressClassName` does not match, the Ingress object alone will not make traffic arrive.

For new clusters or long-lived platform design, Gateway API should be reviewed alongside Ingress. The Ingress example in this post is a minimal explanation for reading an object that still appears often in existing clusters and beginner material.

## Limits and Exceptions

The basic manifest and Ingress object check flow was verified in the author's practice environment. DNS, TLS, certificate manager, and cloud load balancer integration need separate operational verification. This post also does not cover Secret encryption at rest, external secrets, or sealed secrets.

Controller-specific annotations differ by implementation. Check the relevant controller documentation when using NGINX Ingress, Traefik, HAProxy, or a cloud provider controller.

The Kubernetes Ingress API is stable but frozen. Gateway API may be a better fit for new HTTP traffic routing designs, and this post is not a Gateway API comparison or migration guide.

## References

- Kubernetes Docs, [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- Kubernetes Docs, [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- Kubernetes Docs, [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- Kubernetes Docs, [Ingress Controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)
