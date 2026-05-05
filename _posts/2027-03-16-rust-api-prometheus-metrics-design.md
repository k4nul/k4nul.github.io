---
layout: single
title: "Rust Service 26. Prometheus 기준으로 어떤 metric을 남길지 정하기"
description: "Rust API에서 request count, latency, error, saturation 지표를 Prometheus naming과 label cardinality 기준으로 설계한다."
date: 2027-03-16 09:00:00 +09:00
lang: ko
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
---

## 요약

metric은 대시보드를 채우기 위한 숫자가 아니다. 배포를 계속할지, rollback할지, 장애 원인을 좁힐지 판단하는 질문의 답이어야 한다.

Rust API에서는 처음부터 많은 지표를 만들기보다 HTTP 요청 수, latency 분포, error 비율, 동시 처리량과 외부 의존성 상태를 먼저 잡는다. Prometheus 기준에서는 metric 이름에 단위와 타입을 드러내고, label에는 고정된 route pattern만 넣어 cardinality 폭발을 막는 것이 핵심이다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: OpenTelemetry로 logs, metrics, traces 연결하기
- 다음 글: 장애를 일부러 만들고 describe, events, logs로 추적하기
- 이번 글의 범위: Rust API가 Prometheus 또는 Prometheus 호환 backend에서 읽기 좋은 metric을 남기기 위한 최소 설계

## 문서 정보

- 작성일: 2026-05-05
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial | analysis
- 테스트 환경: 직접 실행 테스트 없음. Prometheus 공식 문서와 일반 HTTP API metric 설계 예시를 기준으로 정리했다.
- 테스트 버전: Prometheus 문서 기준. Rust metric crate, OpenTelemetry Collector, Prometheus server 버전은 고정하지 않았다.
- 출처 성격: 공식 문서

## 문제 정의

앞 글에서 OpenTelemetry로 logs, metrics, traces의 연결 구조를 잡았다. 이제 metrics 자체를 어떤 이름과 label로 남길지 정해야 한다.

나쁜 metric 설계는 조용히 비용을 만든다.

- URL 전체를 label로 넣으면 `/users/1`, `/users/2`가 서로 다른 time series가 된다.
- `latency_ms`와 `latency_seconds`가 섞이면 PromQL에서 단위 실수를 만든다.
- counter로 현재 연결 수를 표현하면 값이 내려가는 현상을 설명할 수 없다.
- p99만 보고 count를 보지 않으면 샘플 수가 너무 작은 endpoint를 과대 해석할 수 있다.

이 글의 목표는 Rust API에서 처음 남길 metric을 작게 정하고, 그 metric이 실제 운영 질문에 답하도록 만드는 것이다.

## 확인한 사실

- Prometheus 공식 문서는 counter, gauge, histogram, summary를 core metric type으로 설명한다. Counter는 증가하거나 재시작 때 0으로 reset되는 누적 값이고, gauge는 오르내릴 수 있는 값이다.
  근거: [Prometheus metric types](https://prometheus.io/docs/concepts/metric_types/)
- Prometheus naming 문서는 metric 이름이 단일 단위와 단일 측정 대상을 가리키고, base unit과 unit suffix를 사용하는 것을 권장한다.
  근거: [Prometheus metric and label naming](https://prometheus.io/docs/practices/naming/)
- Prometheus naming 문서는 label의 각 key-value 조합이 새 time series를 만들기 때문에 user id, email, unbounded set 같은 high-cardinality 값을 label에 넣지 말라고 경고한다.
  근거: [Prometheus metric and label naming](https://prometheus.io/docs/practices/naming/)
- Prometheus histogram 문서는 latency 같은 관찰값 분포를 다룰 때 histogram과 summary의 차이를 설명하고, 가능하다면 native histogram을 선호하라고 안내한다. 단, 실제 선택은 사용하는 instrumentation library와 backend 지원을 확인해야 한다.
  근거: [Prometheus histograms and summaries](https://prometheus.io/docs/practices/histograms/)

## 실습 기준

처음에는 아래 metric family만 둔다.

| 질문 | metric 예시 | 타입 | label |
| --- | --- | --- | --- |
| 요청이 얼마나 들어오는가 | `rust_api_http_requests_total` | counter | `method`, `route`, `status_class` |
| 요청이 얼마나 느린가 | `rust_api_http_request_duration_seconds` | histogram | `method`, `route`, `status_class` |
| 동시에 몇 요청을 처리하는가 | `rust_api_http_in_flight_requests` | gauge | 없음 또는 `route` 제한 |
| 빌드/배포 버전은 무엇인가 | `rust_api_build_info` | gauge/info style | `version`, `commit` |
| DB pool이 포화되는가 | `rust_api_db_pool_in_use` | gauge | `pool` |
| DB 요청이 실패하는가 | `rust_api_db_errors_total` | counter | `operation`, `error_kind` |

`route` label은 실제 URL이 아니라 router가 알고 있는 pattern을 사용한다.

| 실제 요청 | metric label |
| --- | --- |
| `/users/123` | `/users/{id}` |
| `/users/456` | `/users/{id}` |
| `/orders/2027-03-16/items` | `/orders/{order_id}/items` |

반대로 아래 값은 label에 넣지 않는다.

- user id
- email
- IP address
- raw URL
- request body value
- token, session id, authorization header
- error message 원문

## 예시 출력

Prometheus exposition 형식의 예시는 아래처럼 읽힌다. 직접 실행 결과가 아니라 설계 예시다.

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

PromQL 예시는 다음처럼 시작한다.

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

## 관찰 결과

직접 실행 결과는 포함하지 않았다. 실제 검증 시에는 아래 항목을 확인한다.

| 확인 항목 | 기대 결과 |
| --- | --- |
| `/metrics` 응답 | HELP/TYPE과 sample이 나온다 |
| route label | raw URL이 아니라 route pattern이다 |
| status label | `200`, `201`, `404`를 모두 펼치기보다 필요한 경우 `2xx`, `4xx`, `5xx`로 묶는다 |
| duration 단위 | seconds 단위로 일관된다 |
| cardinality | user id, email, token 같은 값이 label에 없다 |
| 배포 버전 | metric 또는 resource attribute로 version 구분이 가능하다 |

## 해석 / 의견

metric 설계는 "무엇을 볼 수 있나"보다 "무엇을 판단할 수 있나"에서 출발해야 한다. rollout runbook이 5xx 비율과 p95 latency를 본다면, 그 값을 신뢰할 수 있는 metric이 있어야 한다.

처음부터 business metric, cache metric, queue metric을 많이 넣기보다 HTTP 경계와 외부 의존성부터 시작하는 편이 낫다. 가장 자주 보는 질문은 "요청이 늘었나", "느려졌나", "실패했나", "어느 route인가", "새 버전부터인가"이기 때문이다.

Rust API가 OpenTelemetry metric을 내보내고 Collector를 통해 Prometheus 호환 backend로 보낼 수도 있고, Prometheus client crate로 `/metrics` endpoint를 직접 제공할 수도 있다. 어느 쪽이든 naming, unit, label cardinality 기준은 별도로 지켜야 한다.

## 한계와 예외

- 이 글은 metric 설계 기준이다. 실제 Rust crate 선택과 middleware 구현은 예제 저장소에서 별도로 고정해야 한다.
- native histogram 사용 여부는 instrumentation library, Collector, Prometheus 또는 호환 backend의 지원 상태에 따라 달라진다.
- endpoint 수가 많은 서비스에서는 모든 route에 같은 bucket을 쓰는 것이 적절하지 않을 수 있다.
- metric label은 개인정보와 보안 토큰을 담는 공간이 아니다. 로그보다 오래 보존되고 넓게 복제될 수 있다.

## 참고자료

- [Prometheus metric types](https://prometheus.io/docs/concepts/metric_types/)
- [Prometheus metric and label naming](https://prometheus.io/docs/practices/naming/)
- [Prometheus instrumentation best practices](https://prometheus.io/docs/practices/instrumentation/)
- [Prometheus histograms and summaries](https://prometheus.io/docs/practices/histograms/)

## 변경 이력

- 2026-05-05: Prometheus naming, label cardinality, histogram 기준을 공식 문서 기준으로 재작성.
