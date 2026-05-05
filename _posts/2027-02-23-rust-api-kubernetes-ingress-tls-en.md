---
layout: single
title: "Rust Service 23. Opening external access with Ingress and TLS boundaries"
description: "Separates host/path routing, Ingress Controllers, and TLS termination boundaries when exposing a Rust API with Kubernetes Ingress."
date: 2027-02-23 09:00:00 +09:00
lang: en
translation_key: rust-api-kubernetes-ingress-tls
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
permalink: /en/rust/rust-api-kubernetes-ingress-tls/
---

## Summary

Ingress is not the Rust application router. It is a Kubernetes API object that connects external HTTP and HTTPS requests to Services inside the cluster.

An Ingress manifest is not enough by itself. A real Ingress Controller must handle traffic, and the runbook should record where TLS terminates, which headers reach backend Pods, and where authentication and health checks run.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Setting readiness/liveness probes and resource limits
- Next post: Writing rollout, rollback, and incident runbooks
- Scope: creating an HTTP external-access boundary in front of a Service and documenting the TLS termination point

## Document Information

- Written date: 2026-05-05
- Verification date: 2026-05-05
- Document type: tutorial | analysis
- Test environment: No live-cluster execution test. The procedure is based on Kubernetes official documentation and generic manifest examples.
- Tested versions: Kubernetes documentation baseline. The Ingress Controller implementation and cluster version are left unspecified because no live cluster was executed for this post.
- Evidence level: official documentation

## Problem Statement

A Service gives a stable network target for a set of Pods inside the cluster. It is not enough when users or external clients need to call `https://api.example.com`.

Ingress expresses that external HTTP boundary. However, the Ingress object is only a declaration. The actual behavior comes from an implementation such as NGINX Ingress Controller, Traefik, HAProxy, or a cloud load balancer controller. This post focuses on the common Kubernetes Ingress shape and TLS boundary; controller-specific annotations belong in a separate operations note.

## Verified Facts

- Kubernetes documentation describes Ingress as an API object that exposes HTTP and HTTPS routes from outside the cluster to Services inside the cluster.
  Evidence: [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- Kubernetes documentation states that an Ingress Controller is required for Ingress to work.
  Evidence: [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- Kubernetes documentation marks Ingress as frozen and points new feature work toward Gateway API. New designs should leave a note about whether Gateway API was considered.
  Evidence: [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- Kubernetes Secret documentation defines the `kubernetes.io/tls` Secret type for TLS certificates and private keys.
  Evidence: [Kubernetes TLS Secrets](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets)

## Practice Baseline

Assume the Rust API already has this ClusterIP Service.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: rust-api
  namespace: rust-api
spec:
  type: ClusterIP
  selector:
    app: rust-api
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

The Ingress object adds HTTP routing in front of that Service.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rust-api
  namespace: rust-api
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
      secretName: rust-api-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: rust-api
                port:
                  number: 80
```

Review three boundaries in this manifest.

| Field | Meaning | Operational check |
| --- | --- | --- |
| `ingressClassName` | Which Ingress Controller should handle it | Confirm that the matching controller exists |
| `rules.host` | Which Host header should route to this backend | Confirm DNS or test-time `--resolve` behavior |
| `tls.secretName` | Which Secret stores the certificate and private key | Confirm certificate hosts, expiry, and key handling |

A test TLS Secret can be created like this. Do not commit production private keys to Git.

```bash
kubectl create secret tls rust-api-tls \
  --cert=./tls.crt \
  --key=./tls.key \
  -n rust-api
```

Inspect the Ingress object, controller behavior, and backend Service separately.

```bash
kubectl apply -f k8s/ingress.yaml
kubectl get ingress -n rust-api
kubectl describe ingress rust-api -n rust-api
kubectl get service rust-api -n rust-api
kubectl get endpointslice -n rust-api -l kubernetes.io/service-name=rust-api
```

If the Ingress address is `203.0.113.10`, test host routing before DNS has propagated with `--resolve`.

```bash
curl --resolve api.example.com:443:203.0.113.10 https://api.example.com/health
```

For a local self-signed certificate, TLS verification may fail. `-k` can be useful during local practice, but it should not become the production verification path.

```bash
curl -k --resolve api.example.com:443:203.0.113.10 https://api.example.com/health
```

## Observations

No live-cluster output is included in this post. During verification, record these conditions separately:

| Situation | Expected observation |
| --- | --- |
| No Ingress Controller | The Ingress object may exist without an external address or working routing |
| Host mismatch | Direct IP access may not route to the expected backend |
| Missing or wrong TLS Secret | Controller events or logs may report certificate errors |
| Wrong Service selector | Ingress exists, but backend endpoints are empty and requests fail |
| Certificate host mismatch | The client reports hostname verification failure |

## Interpretation

If Ingress is treated as "the manifest that opens a URL," incident response becomes fuzzy. A request path usually crosses DNS, a load balancer, an Ingress Controller, an Ingress rule, a Service, EndpointSlices, and then Pods. The runbook should follow that order.

TLS termination is also part of the application boundary. In a common Ingress setup, HTTPS terminates between the client and the Ingress Controller, and traffic from the controller to the Service or Pod may be plain HTTP inside the cluster. In that case, the Rust API is not directly handling TLS. Any use of `X-Forwarded-Proto`, `X-Forwarded-For`, and `Host` needs an explicit trust policy.

Proxy headers are useful, but they need a trust boundary. If the app trusts arbitrary `X-Forwarded-*` headers from external clients, scheme detection, client IP, and redirect generation can be wrong. Only use those headers behind a trusted Ingress Controller and with server or middleware policy that makes that boundary clear.

## Limitations

- Ingress annotations are controller-specific. This post does not generalize NGINX, Traefik, HAProxy, AWS ALB, or GCE Ingress behavior.
- Automatic certificate issuance and renewal may require a component such as cert-manager. This post only covers the Ingress boundary that references a TLS Secret.
- If a design needs newer routing capabilities, Gateway API should be evaluated separately.
- mTLS, end-to-end TLS, WAF rules, rate limiting, and external-dns are separate operations topics.

## References

- [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Kubernetes TLS Secrets](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets)
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Gateway API](https://gateway-api.sigs.k8s.io/)

## Change Log

- 2026-05-05: Rewrote the Ingress Controller, host/path routing, TLS Secret, and TLS termination guidance using official documentation.
