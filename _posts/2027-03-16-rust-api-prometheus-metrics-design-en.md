---
layout: single
title: "Rust Service 26. Choosing Prometheus metrics for a Rust API"
description: "Designs request count, latency, error, and saturation metrics for a Rust API using Prometheus naming and label-cardinality rules."
date: 2027-03-16 09:00:00 +09:00
lang: en
translation_key: rust-api-prometheus-metrics-design
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
permalink: /en/rust/rust-api-prometheus-metrics-design/
---

## Summary

A metric is not a number for filling a dashboard. It should answer an operational question: continue the rollout, roll back, or narrow the cause of an incident.

For a Rust API, start with HTTP request count, latency distribution, error rate, in-flight load, and external dependency health. In Prometheus terms, the important rules are to expose units and metric type in the name, and to keep labels bounded by using route patterns instead of raw URLs.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Connecting logs, metrics, and traces with OpenTelemetry
- Next post: Debugging intentional failures with describe, events, and logs
- Scope: the minimum metric design that makes a Rust API readable in Prometheus or Prometheus-compatible backends

## Document Information

- Written date: 2026-05-05
- Verification date: 2026-05-05
- Document type: tutorial | analysis
- Test environment: No direct execution test. The post is based on Prometheus official documentation and generic HTTP API metric design.
- Tested versions: Prometheus documentation baseline. Rust metric crate, OpenTelemetry Collector, and Prometheus server versions are left unspecified.
- Evidence level: official documentation

## Problem Statement

The previous post connected logs, metrics, and traces with OpenTelemetry. Now the metrics themselves need names and labels.

Bad metric design quietly creates cost and confusion.

- If a full URL is used as a label, `/users/1` and `/users/2` become separate time series.
- If `latency_ms` and `latency_seconds` are mixed, PromQL queries become error-prone.
- If a counter is used for the current number of connections, decreases cannot be represented correctly.
- If p99 is viewed without request count, low-volume endpoints can be overinterpreted.

The goal of this post is to choose a small first set of metrics and make sure each one answers a real operating question.

## Verified Facts

- Prometheus documentation describes counter, gauge, histogram, and summary as core metric types. A counter is cumulative and only increases until reset, while a gauge can go up and down.
  Evidence: [Prometheus metric types](https://prometheus.io/docs/concepts/metric_types/)
- Prometheus naming guidance recommends that a metric name refer to one unit and one measured quantity, use base units, and include unit suffixes.
  Evidence: [Prometheus metric and label naming](https://prometheus.io/docs/practices/naming/)
- Prometheus label guidance warns that every unique label key-value combination creates a new time series, and warns against high-cardinality labels such as user IDs and email addresses.
  Evidence: [Prometheus metric and label naming](https://prometheus.io/docs/practices/naming/)
- Prometheus histogram guidance explains histogram and summary tradeoffs for distributions such as latency, and recommends native histograms where available. The real choice still depends on instrumentation library and backend support.
  Evidence: [Prometheus histograms and summaries](https://prometheus.io/docs/practices/histograms/)

## Practice Baseline

Start with these metric families.

| Question | Metric example | Type | Labels |
| --- | --- | --- | --- |
| How many requests arrive? | `rust_api_http_requests_total` | counter | `method`, `route`, `status_class` |
| How slow are requests? | `rust_api_http_request_duration_seconds` | histogram | `method`, `route`, `status_class` |
| How many requests are in progress? | `rust_api_http_in_flight_requests` | gauge | none, or a restricted `route` |
| Which build is running? | `rust_api_build_info` | gauge/info style | `version`, `commit` |
| Is the DB pool saturated? | `rust_api_db_pool_in_use` | gauge | `pool` |
| Are DB operations failing? | `rust_api_db_errors_total` | counter | `operation`, `error_kind` |

The `route` label should use the router's pattern, not the raw URL.

| Actual request | Metric label |
| --- | --- |
| `/users/123` | `/users/{id}` |
| `/users/456` | `/users/{id}` |
| `/orders/2027-03-16/items` | `/orders/{order_id}/items` |

Do not use these values as labels:

- user id
- email
- IP address
- raw URL
- request body value
- token, session id, authorization header
- raw error message

## Example Exposition

The following Prometheus exposition text is a design example, not live output.

```text
# HELP rust_api_http_requests_total Total HTTP requests handled by rust-api.
# TYPE rust_api_http_requests_total counter
rust_api_http_requests_total{method="GET",route="/health",status_class="2xx"} 1200
rust_api_http_requests_total{method="POST",route="/users",status_class="5xx"} 3

# HELP rust_api_http_request_duration_seconds HTTP request latency in seconds.
# TYPE rust_api_http_request_duration_seconds histogram
rust_api_http_request_duration_seconds_bucket{method="GET",route="/users/{id}",status_class="2xx",le="0.05"} 180
rust_api_http_request_duration_seconds_bucket{method="GET",route="/users/{id}",status_class="2xx",le="0.1"} 240
rust_api_http_request_duration_seconds_bucket{method="GET",route="/users/{id}",status_class="2xx",le="+Inf"} 250
rust_api_http_request_duration_seconds_sum{method="GET",route="/users/{id}",status_class="2xx"} 12.4
rust_api_http_request_duration_seconds_count{method="GET",route="/users/{id}",status_class="2xx"} 250
```

Start PromQL checks with these shapes.

```promql
sum(rate(rust_api_http_requests_total[5m])) by (route, status_class)
```

```promql
histogram_quantile(
  0.95,
  sum(rate(rust_api_http_request_duration_seconds_bucket[5m])) by (le, route)
)
```

```promql
sum(rate(rust_api_http_requests_total{status_class="5xx"}[5m]))
/
sum(rate(rust_api_http_requests_total[5m]))
```

## Observations

No direct execution output is included in this post. During verification, check these points:

| Check | Expected result |
| --- | --- |
| `/metrics` response | HELP/TYPE lines and samples are present |
| route label | route pattern is used instead of raw URL |
| status label | `2xx`, `4xx`, `5xx` grouping is used unless exact status is needed |
| duration unit | seconds are used consistently |
| cardinality | no user id, email, token, or unbounded value appears in labels |
| deployment version | version can be separated through a metric or resource attribute |

## Interpretation

Metric design should begin with judgment, not visibility. If the rollout runbook watches 5xx rate and p95 latency, those values need reliable metrics.

It is better to begin with HTTP boundaries and external dependencies than to add many business, cache, and queue metrics at once. The common questions are simple: did traffic increase, did latency increase, did errors increase, which route changed, and did it start with the new version?

A Rust API can expose `/metrics` directly through a Prometheus client crate, or emit OpenTelemetry metrics through a Collector into a Prometheus-compatible backend. Either way, naming, units, and label cardinality still need to be designed deliberately.

## Limitations

- This post covers metric design. The concrete Rust crate and middleware implementation should be pinned in an example repository.
- Native histogram use depends on the instrumentation library, Collector, and Prometheus-compatible backend.
- Services with many route groups may need different bucket boundaries for different workloads.
- Metric labels are not a safe place for personal data or security tokens. Metrics are often retained and replicated widely.

## References

- [Prometheus metric types](https://prometheus.io/docs/concepts/metric_types/)
- [Prometheus metric and label naming](https://prometheus.io/docs/practices/naming/)
- [Prometheus instrumentation best practices](https://prometheus.io/docs/practices/instrumentation/)
- [Prometheus histograms and summaries](https://prometheus.io/docs/practices/histograms/)

## Change Log

- 2026-05-05: Rewrote the Prometheus naming, label cardinality, and histogram guidance using official documentation.
