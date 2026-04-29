---
layout: single
title: "AI agents and sensitive data boundaries"
description: "Defines sensitive data boundaries across prompts, tool calls, traces, MCP connections, memory, and outputs in AI agent systems."
date: 2026-07-28 09:00:00 +09:00
lang: en
translation_key: ai-agents-and-sensitive-data-boundaries
section: development
topic_key: ai
categories: AI
tags: [ai, llm, agents, ai-security, ai-agent-operations]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/ai/ai-agents-and-sensitive-data-boundaries/
---

## Summary

Sensitive data boundaries for AI agents are broader than model input. Prompts, attachments, retrieval results, tool call arguments and outputs, MCP connections, traces, memory, and final answers all belong in the data boundary.

The baseline is to include only the data needed for the task, expose only the tools needed for the task, and treat traces and logs as places where sensitive data may appear unless deliberately redacted.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: tutorial | analysis
- Test environment: No local execution. This post is based on OpenAI Agents SDK, OpenAI Codex security documentation, and OWASP LLM Top 10 guidance.
- Tested versions: Official documentation checked on 2026-04-29. Retention and product settings can vary by deployment and contract.
- Evidence level: official documentation, security project documentation

## Problem Statement

An agent does not process only one user sentence. During a task it may read repository files, summarize external documents, run tools, and record traces. So the sensitive data boundary must be wider than "is this safe to send to the model?"

Without that boundary, secrets can land in traces, external content can be mixed with internal data, or a tool can access sensitive data without an explicit approval point.

## Verified Facts

- OpenAI Agents SDK tracing records spans such as LLM generations, function tool calls, handoffs, guardrails, and custom events. The SDK documentation states that generation and function spans can store inputs and outputs, which may contain sensitive data.
- OpenAI Codex security documentation advises treating prompts, tool arguments, and tool outputs as sensitive and applying telemetry retention and access controls.
- OWASP LLM02:2025 covers sensitive information disclosure in LLM applications and mentions controls such as tokenization and redaction.
- OWASP LLM06:2025 covers excessive agency, where unnecessary authority can increase damage.
- The verification date for this post is 2026-04-29.

## Data Classification

| Class | Examples | Default Handling |
| --- | --- | --- |
| Public data | Public docs, public repositories, public issues | Record source and mark as external input |
| Internal data | Private design docs, internal wiki pages | Include only when needed for the task |
| Personal data | Names, emails, phone numbers, account identifiers | Minimize, mask, and manage retention |
| Sensitive data | API keys, tokens, private keys, secrets, credentials | Do not include raw values in prompts, tools, or traces |
| Regulated data | Health, financial, legal, or similarly regulated records | Do not process without policy and contract review |

## Boundary Procedure

1. Before starting an agent task, classify input origin as user-provided, repository, external web, MCP, or secret store.
2. Do not place raw secrets or credentials in prompts. If they are needed, let a constrained tool use them indirectly through a secret manager.
3. Keep external content separate from internal instructions. Do not treat instructions inside external documents as agent instructions.
4. Scope tool permissions per task. Separate read, write, network, payment, deployment, permission-change, and deletion authority.
5. Require human approval for high-risk actions such as production data access, external transfer, deployment, permission changes, and bulk deletion.
6. Assume traces and logs may contain prompts, tool arguments, and tool outputs; apply redaction, retention limits, and access control.
7. Validate output before release to catch personal data, internal secrets, or unintended disclosure.
8. If an incident is suspected, reconstruct which input, tool, trace, and approval moved data across the boundary.

## Operational Judgment

It is not enough to say "the model will not remember it." In practice, the larger risks are often in the harness: trace retention, tool outputs, connector permissions, and operator access.

The safer pattern is to keep raw secrets outside the agent context and expose only constrained capabilities. For example, prefer "run the approved deployment tool in dry-run mode" over "show the deployment token."

## Review Questions

- Does this task need raw personal data, or would masked identifiers be enough?
- Who can read traces and logs, and how long are they retained?
- What data can MCP servers or external tools access?
- Could external content be interpreted as internal instructions?
- Can the agent transfer data, delete resources, change permissions, or deploy without human approval?

## Limitations

- This post is not legal advice and does not replace an organization's privacy policy.
- Legal basis, cross-border transfer, retention, and data processing agreements require separate review.
- Product data-use behavior can vary by contract, API, enterprise setting, and region.

## References

- [OpenAI Agents SDK: Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Codex: Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added data classes, trace and tool-call boundaries, and operational review questions.
