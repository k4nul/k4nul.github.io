---
layout: single
title: "Rust Service 25. Connecting logs, metrics, and traces with OpenTelemetry"
description: "Defines the signal boundaries and minimum OpenTelemetry setup for connecting logs, metrics, and traces for a Rust API on Kubernetes."
date: 2027-03-09 09:00:00 +09:00
lang: en
translation_key: rust-api-opentelemetry-logs-metrics-traces
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
permalink: /en/rust/rust-api-opentelemetry-logs-metrics-traces/
---

## Summary

Observability is not about producing more logs. It is signal design: logs, metrics, and traces should point to the same request and the same deployed version so operators can narrow symptoms toward causes.

This post uses a baseline where the Rust API exports traces and metrics through OpenTelemetry Protocol (OTLP), and logs include trace id and request id fields. In Kubernetes, the OpenTelemetry Collector becomes the handoff point between the application and telemetry backends.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Writing rollout, rollback, and incident runbooks
- Next post: Choosing Prometheus metrics for a Rust API
- Scope: the minimum observability boundary between a Rust API, Kubernetes Pods, and the OpenTelemetry Collector

## Document Information

- Written date: 2026-05-05
- Verification date: 2026-05-05
- Document type: tutorial | analysis
- Test environment: No direct execution test. The structure is based on OpenTelemetry, Kubernetes, and standards documentation.
- Tested versions: OpenTelemetry Rust documentation baseline. On the verification date, OpenTelemetry Rust lists traces, metrics, and logs as Beta, so crate versions and signal status must be rechecked before publication.
- Evidence level: official documentation, standards documentation

## Problem Statement

The previous runbook described what to look at during a bad rollout. Now the service has to emit the signals that the runbook depends on.

During an incident, one signal is rarely enough.

- Logs show which event or error happened.
- Metrics show how often and how badly it happened.
- Traces show which internal steps and external dependencies one request crossed.

If those signals are not connected, operators have to manually match log entries, dashboard points, and trace samples. The goal of this post is to define common fields first: `service.name`, `service.version`, `trace_id`, `request_id`, and HTTP route.

## Verified Facts

- OpenTelemetry documentation lists traces, metrics, logs, and baggage as supported signals. It describes traces as the path of a request, metrics as runtime measurements, and logs as event records.
  Evidence: [OpenTelemetry Signals](https://opentelemetry.io/docs/concepts/signals/)
- OpenTelemetry Rust documentation lists traces, metrics, and logs as Beta on the verification date. Rust examples should pin crate versions and recheck signal support before publication.
  Evidence: [OpenTelemetry Rust](https://opentelemetry.io/docs/languages/rust/)
- Kubernetes documentation describes observability as collecting and analyzing metrics, logs, and traces to understand cluster and application state.
  Evidence: [Kubernetes Observability](https://kubernetes.io/docs/concepts/cluster-administration/observability/)
- W3C Trace Context defines `traceparent` and `tracestate` HTTP headers for propagating distributed trace context.
  Evidence: [W3C Trace Context](https://www.w3.org/TR/trace-context/)
- OpenTelemetry semantic conventions define service resource attributes such as `service.name`, `service.namespace`, `service.version`, and `service.instance.id`.
  Evidence: [OpenTelemetry service attributes](https://opentelemetry.io/docs/specs/semconv/registry/attributes/service/)

## Practice Baseline

Use this first shape:

```text
Rust API
  -> OTLP traces/metrics
  -> OpenTelemetry Collector Service
  -> tracing/metrics backend

Rust API stdout/stderr logs
  -> node or log collector
  -> log backend
```

Do not start by attaching every possible backend. First, verify that the service emits consistent identity, version, and trace context.

### Resource Attributes

Add minimum service identity to the Pod manifest.

```yaml
env:
  - name: OTEL_SERVICE_NAME
    value: rust-api
  - name: OTEL_RESOURCE_ATTRIBUTES
    value: service.namespace=k4nul,service.version=2027.03.09,deployment.environment.name=production
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: http://otel-collector.observability.svc.cluster.local:4317
```

Use a release version or Git SHA for `service.version`. If an image tag is not enough for audit, record the image digest in the release note too.

### Trace Context

At the HTTP boundary, the service should receive `traceparent` and propagate it to outbound requests. An Ingress or gateway may create trace headers, but operators lose correlation if the application does not connect them to logs and spans.

Align log fields like this:

| Field | Purpose |
| --- | --- |
| `trace_id` | Common key for jumping into trace UI |
| `span_id` | Key for a specific operation within the trace |
| `request_id` | Request key from the external client or gateway |
| `http.method` | HTTP method |
| `http.route` | Low-cardinality route pattern |
| `status_code` | HTTP response code |
| `error.kind` | Error classification |
| `service.version` | Deployed version boundary |

Do not put full URLs or user input into metric labels. `/users/123` and `/users/456` should be represented as a route pattern such as `/users/{id}` for metrics.

### Collector Boundary

The Collector is the buffer between application instrumentation and vendor backends. Start with an OTLP receiver, batch processor, and debug exporter or one real backend exporter.

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch: {}

exporters:
  debug: {}

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [debug]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [debug]
```

In production, replace `debug` with the exporter for the backend you use. The point is to keep the Rust API connected through OTLP and a Collector boundary instead of coupling it directly to one vendor SDK.

## Observations

No direct execution output is included in this post. During verification, record these checks:

| Check | Expected result |
| --- | --- |
| collector endpoint | The Pod can resolve the `otel-collector` Service DNS name |
| trace export | One sample request appears as a trace in the backend or debug exporter |
| metric export | request count and latency metrics appear with service/version identity |
| log correlation | error logs include `trace_id` or `request_id` |
| version boundary | pre-deploy and post-deploy signals split by `service.version` |
| sensitive data | Authorization, cookie, token, and personal data are absent from span/log attributes |

## Interpretation

The common mistake with OpenTelemetry is choosing an exporter first. The first question should be: what incident question do we need to answer?

For example, "why did checkout latency increase after deployment?" needs a latency metric, a trace sample for the route, and an error log with the same trace id. "did the Pod die?" may need Kubernetes events and restart count before a distributed trace. Each signal answers a different kind of question. They do not need to look identical, but they do need shared keys for request and version correlation.

In Rust services, `tracing`-based instrumentation is often connected to OpenTelemetry. This post does not pin a crate combination. OpenTelemetry Rust status and crate APIs can change, so the real example repository should pin `Cargo.lock`, exporter configuration, and Collector manifests together.

## Limitations

- This is a structure article. It does not include executed Rust output, trace backend screenshots, or metric query results.
- OpenTelemetry Rust signal status was checked as Beta on the verification date. Recheck crate versions and signal stability at publication time.
- Organizations differ on whether logs should flow through Kubernetes stdout/stderr logging pipelines or OpenTelemetry logs pipelines.
- Sampling, tail sampling, PII redaction, and multi-tenant attribute policy are separate operations topics.

## References

- [OpenTelemetry Signals](https://opentelemetry.io/docs/concepts/signals/)
- [OpenTelemetry Rust](https://opentelemetry.io/docs/languages/rust/)
- [OpenTelemetry Collector and Kubernetes](https://opentelemetry.io/docs/platforms/kubernetes/collector/)
- [OpenTelemetry Protocol](https://opentelemetry.io/docs/specs/otel/protocol/)
- [OpenTelemetry service attributes](https://opentelemetry.io/docs/specs/semconv/registry/attributes/service/)
- [Kubernetes Observability](https://kubernetes.io/docs/concepts/cluster-administration/observability/)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)

## Change Log

- 2026-05-05: Rewrote the OpenTelemetry signal boundary, Rust status caveats, and minimum Collector structure using official documentation.
