---
layout: single
title: "GenAI 관측성에는 공통 convention이 생기고 있지만 trace schema를 고정하면 안 되는 이유"
description: "OpenTelemetry GenAI Semantic Conventions를 이용해 agent/model/tool trace, schema migration, token usage·latency 관찰, 민감 콘텐츠 redaction을 설계한다."
date: 2026-10-14 09:00:00 +09:00
lang: ko
translation_key: genai-observability-schema-migration-redaction
section: development
topic_key: ai
categories: AI
tags: [ai, observability, opentelemetry, tracing, privacy, security]
track: agent-interface-engineering
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

LLM application의 느린 응답은 model 호출, tool 실행, retry, token 처리 중 어디에서 시간이 쓰였는지 보지 않으면 추측이 된다. OpenTelemetry의 GenAI Semantic Conventions는 model/provider metadata와 token usage attribute의 공통 이름을 제공하고, 작업 duration은 OTel span의 시작·종료 시각으로 측정한다. 실패와 생성 종료는 상황에 따라 span status·`error.type`, inference response의 `gen_ai.response.finish_reasons`로 기록하며, 업무 outcome은 애플리케이션이 별도로 정의해야 한다.

공통 convention이 생겼다고 trace schema를 애플리케이션 내부에 영구 고정하면 안 된다. 검증 기준일 현재 GenAI convention은 **Development** 안정성 단계이고 전용 repository에는 published release와 schema URL이 없으므로 main branch 문서는 안정된 버전 계약이 아니라 변하는 명세로 취급해야 한다. full prompt·tool argument·tool result capture는 유용한 만큼 민감하고 크다. 좋은 설계는 **의미 있는 관찰과 최소 수집을 함께** 달성한다.

## Document Info / Environment

- 작성일·검증 기준일: 2026-09-07
- 문서 성격: observability design guide
- 테스트 환경: OTel collector나 agent SDK를 직접 실행하지 않았다. OpenTelemetry 공식 가이드·release note를 분석했다.
- 범위: instrumentation·데이터 거버넌스 설계. 특정 backend 또는 coding assistant의 지원을 보장하지 않는다.

## Problem Statement / 문제 정의

"LLM이 느리다"는 진단 가능한 statement가 아니다. 최소한 다음 질문으로 나뉜다.

- agent의 전체 요청은 얼마나 걸렸는가?
- model call과 tool execution 중 어느 구간이 병목인가?
- input/output token과 종료 이유는 무엇인가?
- retry가 latency를 얼마나 만들었는가? token usage는 비용 추정의 재료일 뿐 확정 청구 금액이 아니다. 비용을 보고한다면 versioned pricing source와 model·region·cache·modality·billing 가정을 명시해야 한다.
- trace에 prompt, schema, tool argument, tool result를 남겨도 되는가?

마지막 질문을 무시하면 observability가 디버깅 장비이면서 동시에 비밀정보 저장소가 된다.

## Verified Facts / 확인된 사실

- OpenTelemetry의 2026 GenAI observability 가이드는 model identity와 input/output token count를 설명한다. span timing은 duration을 기록하고, span status와 `error.type`은 error를, `gen_ai.response.finish_reasons`는 inference response의 종료 사유를 다룬다. 업무 outcome은 애플리케이션 정의 값이다.
  근거: [OpenTelemetry guide](https://opentelemetry.io/blog/2026/genai-observability/)
- OTel blog의 VS Code Copilot 예시는 `invoke_agent` span 아래에 `chat`, `execute_tool` child span을 표시한다. GenAI 명세는 이를 해당하는 경우의 operation-name 값으로 정의하지만, 모든 GenAI trace에 이 계층을 강제하지는 않는다.
  근거: [OpenTelemetry guide](https://opentelemetry.io/blog/2026/genai-observability/)
- 인용한 VS Code Copilot walkthrough에서는 full prompt/completion과 tool schema·argument·result가 기본 수집되지 않으며 content capture를 켜야 한다. 이는 해당 integration의 기본값이지 모든 OTel runtime에 대한 보장은 아니다. GenAI convention은 상세 inference-content capture를 opt-in으로 다룬다.
  근거: [OpenTelemetry guide](https://opentelemetry.io/blog/2026/genai-observability/)
- Core semantic-conventions v1.42.0은 core repository에 있던 GenAI 정의를 deprecated하고 dedicated GenAI repository로 stewardship를 옮겼다. 이는 successor convention을 Stable로 만들거나 released schema URL을 제공한 것은 아니다.
  근거: [v1.42.0 release](https://github.com/open-telemetry/semantic-conventions/releases/tag/v1.42.0)

## Reproduction Steps / 재현 순서

세 계층의 애플리케이션 이벤트 계약을 먼저 정의한다. 아래 field name은 명시적으로 `gen_ai.*` 또는 core OTel attribute로 표시하지 않는 한 제품 정의 값이다.

| 계층 | 기본 수집 | 제한된 진단 수집 |
| --- | --- | --- |
| agent | 제품 정의 request ID/outcome, span duration | redacted goal summary |
| model | `gen_ai.operation.name`, `gen_ai.provider.name`, `gen_ai.request.model`, span duration, 제공될 때의 `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens`, 해당할 때의 `gen_ai.response.finish_reasons`, error 시 span status와 `error.type` | sampled/redacted messages |
| tool | `gen_ai.operation.name`, tool name, span duration, error 시 span status와 `error.type` | approved fields only, no raw secret |

`retry_count`, 업무 outcome, authorization decision, diagnostic summary는 애플리케이션 정의 값이다. 자동 retry는 논리 작업 하나를 하나의 span으로 유지하고, retry 세부 정보가 필요할 때만 문서화한 custom field 또는 의도적으로 설계한 attempt telemetry로 보완한다.

Instrumentation boundary에 adapter를 둔다. 안정된 domain event를 선택한 SDK/instrumentation과 backend가 지원하는 정확한 GenAI convention revision으로 map하고, revision 및 schema URL이 공개되면 이를 배포·telemetry metadata에 기록한다. repository의 변하는 `main` branch에 무조건 map하지 않는다. adapter는 migration 작업을 국소화할 뿐 exporter·backend 호환성을 보장하지는 않는다.

content capture는 다음 순서로 gate한다.

1. 애플리케이션/instrumentation 기본값을 metadata-only로 정하고, 활성화한 각 auto-instrumentation·agent integration의 실제 기본 capture 설정을 확인한다.
2. 필요할 때만 sampling·tenant/환경 분리·보존 기간을 정한다.
3. 가능하면 instrumentation source에서 raw content가 span/event에 기록되지 않게 한다. 진단 capture가 승인된 경우에는 span/event 생성 전에 allowlist와 field-level 최소화를 적용하고, 모든 외부 exporter 앞에서는 Collector processor를 defense-in-depth 통제로 사용한다.
4. trace, log/event, retry, queue, debug output, backend copy 등 활성화된 모든 경로를 검증하고 access log와 incident 절차를 둔다.

## Observations / 관찰 결과

trace 하나에 모든 내용을 넣으면 debugging은 빨라질 수 있지만, tool argument와 result가 고객 데이터·access token·내부 URL·소스 일부를 품을 수 있다. 큰 attribute는 비용·query 성능·retention에도 영향을 준다.

반대로 content를 전혀 남기지 않으면 실패 원인을 재현하기 어렵다. 해답은 "전부 또는 전무"가 아니라, 기본 metadata와 제한된 진단 capture를 분리하고 후자를 명시적 정책으로 관리하는 것이다.

## Interpretation / 해석

GenAI observability의 최소 제품은 예쁜 trace 화면이 아니다.

```text
causal spans
+ stable domain events
+ versioned convention adapter
+ minimal-by-default content policy
+ redaction, retention, access audit
```

이 구조는 convention migration 작업을 국소화하고 prompt content가 로그로 장기간 퍼질 위험을 줄인다. tool call 성공은 업무 성공의 증거가 아니므로 outcome evidence는 별도 제품 정의 field 또는 verification 단계에 남긴다. correlation identifier, tenant ID, `gen_ai.conversation.id`, hash도 연결 가능성 때문에 민감할 수 있으므로 retention/access 검토가 필요하다.

## Limitations / 한계

- 이 글은 공식 문서 분석이며 실제 exporter/backend의 schema 호환성을 테스트하지 않았다.
- redaction은 모든 secret을 찾아냈거나 earlier in-process·receiver·queue·debug·backend copy가 없었다는 증거가 아니다. source-side non-collection을 우선하고 representative adversarial·실제 형식 payload로 redaction rule을 테스트해야 한다.
- token·latency 지표만으로 품질, 안전성, 사용자 업무 성공을 평가할 수 없다.

## References / 참고자료

- [Inside the LLM Call: GenAI Observability with OpenTelemetry](https://opentelemetry.io/blog/2026/genai-observability/)
- [OpenTelemetry semantic-conventions v1.42.0](https://github.com/open-telemetry/semantic-conventions/releases/tag/v1.42.0)
- [GenAI semantic-conventions repository (공개 직전 revision 확인)](https://github.com/open-telemetry/semantic-conventions-genai)
- [GenAI spans specification](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md)
- [GenAI agent spans specification](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md)
- [GenAI events specification](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-events.md)
- [OpenTelemetry guidance for handling sensitive data](https://opentelemetry.io/docs/security/handling-sensitive-data/)

## Change Log / 변경 이력

- 2026-09-07: KR local draft 작성. `published: false`; telemetry·backend·외부 채널 설정은 변경하지 않았다.
