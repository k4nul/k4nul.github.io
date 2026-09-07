---
layout: single
title: "GenAI Observability Has Shared Conventions—But Do Not Freeze Your Trace Schema Yet"
description: "Using OpenTelemetry GenAI Semantic Conventions to design agent/model/tool traces, schema migration, token-usage and latency observation, and sensitive-content redaction."
date: 2026-10-14 09:00:00 +09:00
lang: en
translation_key: genai-observability-schema-migration-redaction
section: development
topic_key: ai
categories: AI
tags: [ai, observability, opentelemetry, tracing, privacy, security]
track: agent-interface-engineering
published: false
permalink: /en/development/genai-observability-schema-migration-redaction/
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

When an LLM application is slow, it is guesswork unless you can see where time went across model calls, tool invocations, retries, and token handling. OpenTelemetry’s GenAI Semantic Conventions provide common names for model/provider metadata and token-usage attributes; an OTel span supplies operation duration. For failures and generation termination, use span status and `error.type` where applicable, and `gen_ai.response.finish_reasons` for inference responses. Business outcome remains application-defined.

Shared conventions do not mean an application should freeze its trace schema forever. At the verification baseline, the GenAI conventions are marked **Development**; the dedicated repository has no published releases or schema URL, so its main-branch documents are an evolving specification rather than a stable versioned contract. Capturing full prompts, tool arguments, and tool results is as sensitive as it is useful. Good design achieves **meaningful observation and minimal collection together**.

## Document Info / Environment

- Draft and verification baseline: 2026-09-07
- Document type: observability design guide
- Test environment: no OTel collector or agent SDK was run. This draft analyzes official OpenTelemetry guidance and release notes.
- Scope: instrumentation and data-governance design; it does not guarantee support by a specific backend or coding assistant.

## Problem Statement / 문제 정의

“An LLM is slow” is not diagnosable. It breaks into at least these questions:

- How long did the entire agent request take?
- Was the bottleneck model time or tool execution?
- What were input/output token counts and finish reason?
- How much latency came from retry? Token usage supports cost estimation, not an authoritative bill; any estimate needs a versioned pricing source and explicit model, region, cache, modality, and billing assumptions.
- May a trace retain prompts, schemas, tool arguments, and tool results?

Ignoring the final question turns observability from a debugging system into a secret store.

## Verified Facts / 확인된 사실

- OpenTelemetry’s GenAI observability guide describes model identity and input/output token counts. Span timing records duration; span status and `error.type` describe errors, while `gen_ai.response.finish_reasons` applies to inference responses. Business outcome is application-defined.
  Evidence: [OpenTelemetry guide](https://opentelemetry.io/blog/2026/genai-observability/)
- The OTel blog’s VS Code Copilot example visualizes an `invoke_agent` span with `chat` and `execute_tool` child spans. The GenAI specification defines these as operation-name values when applicable; it does not require every GenAI trace to use that exact hierarchy.
  Evidence: [OpenTelemetry guide](https://opentelemetry.io/blog/2026/genai-observability/)
- In the cited VS Code Copilot walkthrough, full prompts/completions and tool schemas, arguments, and results are not captured by default and require content capture to be enabled. This is an integration-specific default, not a universal OTel runtime guarantee. The GenAI conventions treat detailed inference-content capture as opt-in.
  Evidence: [OpenTelemetry guide](https://opentelemetry.io/blog/2026/genai-observability/)
- Core semantic-conventions v1.42.0 deprecated GenAI definitions formerly maintained in the core repository and moved stewardship to a dedicated GenAI repository. It did not make successor conventions Stable or provide a released successor schema URL.
  Evidence: [v1.42.0 release](https://github.com/open-telemetry/semantic-conventions/releases/tag/v1.42.0)

## Reproduction Steps / 재현 순서

Define an application event contract in three layers. The field names below are product-defined unless shown as an explicit `gen_ai.*` or core OTel attribute.

| Layer | Default collection | Restricted diagnostic collection |
| --- | --- | --- |
| agent | product-defined request ID/outcome, span duration | redacted goal summary |
| model | `gen_ai.operation.name`, `gen_ai.provider.name`, `gen_ai.request.model`, span duration, `gen_ai.usage.input_tokens` / `gen_ai.usage.output_tokens` when supplied, `gen_ai.response.finish_reasons` when applicable, span status and `error.type` on error | sampled/redacted messages |
| tool | `gen_ai.operation.name`, tool name, span duration, span status and `error.type` on error | approved fields only, never raw secrets |

`retry_count`, business outcome, authorization decision, and diagnostic summaries are application-defined. For automatic retries, retain the logical operation as one span and expose retry details only through a documented custom field or intentionally designed attempt telemetry.

Introduce an adapter at the instrumentation boundary: map stable domain events to the exact GenAI convention revision supported by the selected SDK/instrumentation and backend. Record that revision—and its schema URL when one is published—in deployment and telemetry metadata. Do not map blindly to the repository’s moving `main` branch. The adapter localizes migration work; it does not itself guarantee exporter or backend compatibility.

Gate content capture in this order:

1. set the application/instrumentation default to metadata-only and verify the actual default of every enabled auto-instrumentation or agent integration;
2. define sampling, tenant/environment separation, and retention when needed;
3. prevent raw content from being recorded at the instrumentation source whenever possible; if diagnostic capture is approved, apply an allowlist and field-level minimization before span/event creation, then use Collector processors as defense in depth before every external exporter;
4. validate traces, logs/events, retries, queues, debug output, and backend copies, then add access logging and an incident procedure.

## Observations / 관찰 결과

Putting every detail in a trace can accelerate debugging, yet tool arguments and results can contain customer data, access tokens, internal URLs, or source fragments. Large attributes also affect cost, query performance, and retention.

Capturing no content at all makes failure reproduction difficult. The useful answer is neither “everything” nor “nothing”: separate baseline metadata from restricted diagnostic capture and manage the latter through explicit policy.

## Interpretation / 해석

The minimum viable GenAI observability product is not a pretty trace view.

```text
causal spans
+ stable domain events
+ versioned convention adapter
+ minimal-by-default content policy
+ redaction, retention, access audit
```

This localizes convention-migration work and reduces the risk that prompt content spreads through long-lived logs. A successful tool call is not evidence of successful business work, so record outcome evidence in a separate product-defined field or verification stage. Correlation identifiers, tenant IDs, `gen_ai.conversation.id`, and hashes can themselves be sensitive through linkability and need retention/access review.

## Limitations / 한계

- This is an official-document analysis; it did not test schema compatibility for a particular exporter or backend.
- Redaction is not proof that every secret was detected or that an earlier in-process, receiver, queue, debug, or backend copy did not exist. Prefer source-side non-collection and test redaction rules against representative adversarial and real-format payloads.
- Token and latency metrics alone cannot assess quality, safety, or user business success.

## References / 참고자료

- [Inside the LLM Call: GenAI Observability with OpenTelemetry](https://opentelemetry.io/blog/2026/genai-observability/)
- [OpenTelemetry semantic-conventions v1.42.0](https://github.com/open-telemetry/semantic-conventions/releases/tag/v1.42.0)
- [GenAI semantic-conventions repository (verify revision at publication)](https://github.com/open-telemetry/semantic-conventions-genai)
- [GenAI spans specification](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md)
- [GenAI agent spans specification](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md)
- [GenAI events specification](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-events.md)
- [OpenTelemetry guidance for handling sensitive data](https://opentelemetry.io/docs/security/handling-sensitive-data/)

## Change Log / 변경 이력

- 2026-09-07: Created as an English local draft. `published: false`; no telemetry, backend, or external-channel configuration was changed.
