---
layout: single
title: "Rust Service 25. OpenTelemetry로 logs, metrics, traces 연결하기"
description: "Rust API와 Kubernetes 운영에서 OpenTelemetry로 logs, metrics, traces를 연결할 때의 신호 경계와 최소 설정을 정리한다."
date: 2027-03-09 09:00:00 +09:00
lang: ko
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
---

## 요약

관측성은 로그를 많이 남기는 일이 아니다. 장애 증상을 원인 후보로 좁혀 가기 위해 logs, metrics, traces가 같은 요청과 같은 배포 버전을 가리키도록 신호를 설계하는 일이다.

이 글에서는 Rust API가 OpenTelemetry Protocol(OTLP)로 traces와 metrics를 내보내고, logs에는 trace id와 request id를 포함시키는 구조를 기본값으로 잡는다. Kubernetes에서는 OpenTelemetry Collector가 신호를 받아 backend로 보내는 중간 지점이 된다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: rollout, rollback, 장애 대응 runbook 만들기
- 다음 글: Prometheus 기준으로 어떤 metric을 남길지 정하기
- 이번 글의 범위: Rust API, Kubernetes Pod, OpenTelemetry Collector 사이의 최소 관측성 경계

## 문서 정보

- 작성일: 2026-05-05
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial | analysis
- 테스트 환경: 직접 실행 테스트 없음. OpenTelemetry, Kubernetes 공식 문서와 일반 설정 예시를 기준으로 정리했다.
- 테스트 버전: OpenTelemetry Rust 문서 기준. 검증 기준일 현재 OpenTelemetry Rust의 traces, metrics, logs status는 Beta로 안내되어 있어, 실제 발행 전 crate 버전과 기능 상태를 다시 확인해야 한다.
- 출처 성격: 공식 문서, 표준 문서

## 문제 정의

앞 글의 runbook은 "배포가 이상하면 무엇을 볼 것인가"를 정했다. 이제 그 runbook이 볼 수 있는 신호를 서비스가 실제로 내보내야 한다.

장애 중에는 한 가지 신호만으로 충분하지 않은 경우가 많다.

- 로그는 어떤 에러가 발생했는지 보여준다.
- metric은 얼마나 자주, 얼마나 크게 문제가 발생했는지 보여준다.
- trace는 한 요청이 어떤 내부 단계와 외부 의존성을 거쳤는지 보여준다.

이 세 신호가 서로 연결되어 있지 않으면 운영자는 로그 탭, 대시보드, trace UI를 오가며 같은 요청을 손으로 맞춰야 한다. 이 글의 목표는 `service.name`, `service.version`, `trace_id`, `request_id`, HTTP route 같은 공통 필드를 먼저 정하는 것이다.

## 확인한 사실

- OpenTelemetry 공식 문서는 traces, metrics, logs, baggage를 현재 지원 신호로 설명한다. traces는 요청 경로, metrics는 런타임 측정값, logs는 이벤트 기록이다.
  근거: [OpenTelemetry Signals](https://opentelemetry.io/docs/concepts/signals/)
- OpenTelemetry Rust 문서는 검증 기준일 현재 traces, metrics, logs를 Beta 상태로 안내한다. Rust 적용 글은 사용 crate와 기능 상태를 고정해서 다시 확인해야 한다.
  근거: [OpenTelemetry Rust](https://opentelemetry.io/docs/languages/rust/)
- Kubernetes 공식 문서는 observability를 metrics, logs, traces를 수집하고 분석해 클러스터와 애플리케이션 상태를 이해하는 과정으로 설명한다.
  근거: [Kubernetes Observability](https://kubernetes.io/docs/concepts/cluster-administration/observability/)
- W3C Trace Context는 `traceparent`와 `tracestate` HTTP header로 분산 trace context를 전파하는 표준을 정의한다.
  근거: [W3C Trace Context](https://www.w3.org/TR/trace-context/)
- OpenTelemetry semantic conventions에는 `service.name`, `service.namespace`, `service.version`, `service.instance.id` 같은 service resource attribute가 정의되어 있다.
  근거: [OpenTelemetry service attributes](https://opentelemetry.io/docs/specs/semconv/registry/attributes/service/)

## 실습 기준

이번 글의 기본 구조는 아래와 같다.

```text
Rust API
  -> OTLP traces/metrics
  -> OpenTelemetry Collector Service
  -> tracing/metrics backend

Rust API stdout/stderr logs
  -> node or log collector
  -> log backend
```

처음부터 모든 backend를 붙이지 않는다. 먼저 서비스가 같은 이름과 버전, 같은 trace context를 쓰는지 확인한다.

### Resource attributes

Pod manifest에는 최소한 service 식별 정보를 넣는다.

```yaml
env:
  - name: OTEL_SERVICE_NAME
    value: rust-api
  - name: OTEL_RESOURCE_ATTRIBUTES
    value: service.namespace=k4nul,service.version=2027.03.09,deployment.environment.name=production
  - name: OTEL_EXPORTER_OTLP_ENDPOINT
    value: http://otel-collector.observability.svc.cluster.local:4317
```

`service.version`에는 사람이 읽기 쉬운 release version이나 Git SHA를 넣는다. image tag만으로 충분하지 않다면 image digest도 release note에 남긴다.

### Trace context

HTTP 요청 경계에서는 `traceparent`를 받고 다음 outbound 요청에도 전파해야 한다. Ingress나 gateway가 trace header를 새로 만들 수 있지만, 애플리케이션이 그 값을 로그와 span에 연결하지 않으면 운영자는 correlation을 잃는다.

로그 필드는 아래처럼 맞춘다.

| 필드 | 목적 |
| --- | --- |
| `trace_id` | trace UI로 이동하기 위한 공통 키 |
| `span_id` | 특정 작업 단계를 찾기 위한 키 |
| `request_id` | 외부 클라이언트 또는 gateway 기준 요청 키 |
| `http.method` | 요청 방법 |
| `http.route` | cardinality를 낮춘 route 패턴 |
| `status_code` | HTTP 응답 코드 |
| `error.kind` | 에러 분류 |
| `service.version` | 배포 버전 구분 |

주의할 점은 URL 전체나 사용자 입력값을 metric label로 넣지 않는 것이다. `/users/123`, `/users/456`을 label로 남기면 cardinality가 커진다. metric에는 `/users/{id}` 같은 route pattern을 쓴다.

### Collector 경계

Collector는 애플리케이션과 vendor backend 사이의 완충 지점이다. 처음에는 OTLP receiver, batch processor, logging/debug 또는 실제 exporter만 둔다.

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

운영에서는 `debug` exporter 대신 사용하는 backend exporter를 둔다. 중요한 것은 Rust API가 backend vendor SDK에 직접 강하게 묶이지 않도록 OTLP와 Collector 경계를 먼저 잡는 것이다.

## 관찰 결과

직접 실행 결과는 포함하지 않았다. 실제 검증 시 아래 관찰 지점을 기록한다.

| 확인 항목 | 기대 결과 |
| --- | --- |
| collector endpoint | Pod에서 `otel-collector` Service DNS를 해석할 수 있다 |
| trace export | 샘플 요청 하나가 backend 또는 debug exporter에 trace로 보인다 |
| metric export | 요청 수와 latency metric이 service/version 기준으로 보인다 |
| log correlation | error log에 `trace_id` 또는 `request_id`가 포함된다 |
| version 구분 | 배포 전후 신호가 `service.version`으로 나뉜다 |
| 민감 정보 | Authorization, cookie, token, 개인정보가 span/log attribute에 남지 않는다 |

## 해석 / 의견

OpenTelemetry를 도입할 때 가장 흔한 실수는 exporter부터 고르는 것이다. 먼저 정해야 할 것은 "장애 중 어떤 질문에 답할 것인가"다.

예를 들어 "배포 후 checkout latency가 왜 늘었나"라는 질문에는 latency metric, 특정 route의 trace sample, 같은 trace id를 가진 error log가 필요하다. "Pod가 죽었나"라는 질문에는 Kubernetes event와 restart count가 먼저 필요할 수 있다. 신호마다 답하는 질문이 다르므로, logs/metrics/traces를 같은 형태로 만들 필요는 없다. 대신 같은 요청과 같은 배포 버전을 가리키는 공통 키는 맞춰야 한다.

Rust 생태계에서는 `tracing` crate 기반 instrumentation을 OpenTelemetry와 연결하는 구성이 자주 쓰인다. 하지만 이 글은 crate 조합을 고정하지 않는다. OpenTelemetry Rust 상태와 crate API는 변할 수 있으므로 실제 예제 저장소에서는 `Cargo.lock`, exporter 설정, Collector manifest를 함께 고정해야 한다.

## 한계와 예외

- 이 글은 구조 설계 글이다. 실제 Rust 코드 실행 결과, trace backend 화면, metric query 결과는 포함하지 않는다.
- OpenTelemetry Rust 기능 상태는 검증 기준일에 Beta로 확인했다. 발행 시점의 crate version과 signal 안정성을 다시 확인해야 한다.
- 로그 수집은 stdout/stderr 기반 Kubernetes logging pipeline과 OpenTelemetry logs pipeline 중 어느 쪽을 쓸지 조직마다 다르다.
- sampling, tail sampling, PII redaction, multi-tenant attribute 정책은 별도 운영 주제다.

## 참고자료

- [OpenTelemetry Signals](https://opentelemetry.io/docs/concepts/signals/)
- [OpenTelemetry Rust](https://opentelemetry.io/docs/languages/rust/)
- [OpenTelemetry Collector and Kubernetes](https://opentelemetry.io/docs/platforms/kubernetes/collector/)
- [OpenTelemetry Protocol](https://opentelemetry.io/docs/specs/otel/protocol/)
- [OpenTelemetry service attributes](https://opentelemetry.io/docs/specs/semconv/registry/attributes/service/)
- [Kubernetes Observability](https://kubernetes.io/docs/concepts/cluster-administration/observability/)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)

## 변경 이력

- 2026-05-05: OpenTelemetry 신호 경계, Rust 상태 주의점, Collector 최소 구조를 공식 문서 기준으로 재작성.
