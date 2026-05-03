---
layout: single
title: "What should an agent trace record?"
description: "Explains What should an agent trace record? with official documentation, operational checks, and limitations."
date: 2026-06-16 09:00:00 +09:00
lang: en
translation_key: what-should-agent-trace-record
section: development
topic_key: ai
categories: AI
tags: [ai, llm, agents, ai-security, ai-agent-operations]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/ai/what-should-agent-trace-record/
---

## Summary

An agent trace is not a place to store the entire conversation by default. It is an operational record that should explain which input, permission, tool call, guardrail, approval, and verification result led to the next step.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: analysis | tutorial
- Test environment: No live execution. This post summarizes trace design from OpenAI Agents SDK and Codex security documentation.
- Test version: OpenAI Agents SDK and Codex documentation checked on 2026-04-29. No local SDK version is fixed.
- Evidence level: official documentation, security project documentation

## Problem Statement

If an agent trace is treated as "save every log", two failures are likely. The trace may miss the decision path needed for incident review, while still storing too much raw prompt, output, or tool data. That can turn observability into a new sensitive-data exposure path.

This post separates what an agent trace should record from what it should minimize or redact.

## Verified Facts

- The OpenAI Agents SDK tracing documentation describes LLM generations, tool calls, handoffs, guardrails, and custom events as traceable events during an agent run.
  Evidence: [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)
- The same documentation describes traces as workflow-level records and spans as operations with start time, end time, trace id, parent id, and span data.
  Evidence: [OpenAI Agents SDK Traces and spans](https://openai.github.io/openai-agents-python/tracing/#traces-and-spans)
- LLM generation spans and function call spans may capture inputs and outputs, so sensitive-data capture must be configured deliberately.
  Evidence: [OpenAI Agents SDK Sensitive data](https://openai.github.io/openai-agents-python/tracing/#sensitive-data)
- Codex documentation separates sandbox and approval boundaries, including approval for edits outside the workspace, network access, and connector/tool calls with side effects.
  Evidence: [Codex agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)

## Reproduction Steps

Use this checklist when designing a trace schema.

1. Define the execution unit: `trace_id`, `workflow_name`, `group_id`, requester, repository/project, and task id.
2. Record input origin: user request, file, web result, MCP/resource, or memory.
3. Record model calls: model name, generation span, useful usage totals, failed calls, and retries.
4. Record tool calls: tool name, argument summary, target resource, permission scope, approval requirement, and result summary.
5. Record handoffs: receiving agent, reason, forwarded context scope, and filtered context.
6. Record guardrails: input/output/tool guardrail name, allow/block/tripwire result, and reason.
7. Record approvals: approval reason, approver or policy, approved/denied/timed out result, and whether execution actually followed.
8. Record verification: tests that ran, checks that failed, and checks that could not run.
9. Record sensitive-data handling: raw data policy, redaction method, retention, and external trace processor export.

Prefer classifications, hashes, lengths, and resource ids over raw secret values or full document bodies.

```text
trace_id: trace_...
workflow_name: "repository maintenance"
input_source: user_request | file | web | mcp | memory
tool_call: { name, target, permission_scope, approved, result_summary }
guardrail: { name, stage, outcome, reason }
verification: { ran, failed, not_run, reason }
sensitive_data: { raw_input_saved: false, redaction: "token/value redacted" }
```

## Observations

- Raw prompts and final answers alone do not explain why a tool was allowed to run.
- Storing every input and output can make debugging easier while moving secrets, personal data, or internal documents into the trace backend.
- The highest-value trace records are usually boundaries: permissions, tool calls, guardrails, approvals, and verification outcomes.

## Interpretation

In my view, the purpose of an agent trace is not to preserve the model's hidden reasoning. It is to preserve an auditable operational chain: input origin, authority, action, control, result, and verification.

Opinion: the default should be minimal raw-content capture. If every prompt and tool output is always stored, the trace itself becomes a data exposure surface.

## Limitations

- This post does not replace organization-specific audit, privacy, or retention requirements.
- OpenAI Agents SDK and Codex tracing or approval behavior may change by version.
- Real SIEM, APM, DLP, or trace processor integrations require product-specific data modeling.

## References

- [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [OpenAI Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added concrete trace fields, sensitive-data boundary, and official-documentation evidence.
