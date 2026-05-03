---
layout: single
title: "Guardrails and approval boundaries from a harness perspective"
description: "Explains Guardrails and approval boundaries from a harness perspective with official documentation, operational checks, and limitations."
date: 2026-06-23 09:00:00 +09:00
lang: en
translation_key: guardrails-and-approval-boundaries-in-harness
section: development
topic_key: ai
categories: AI
tags: [ai, llm, agents, ai-security, ai-agent-operations]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/ai/guardrails-and-approval-boundaries-in-harness/
---

## Summary

From a harness perspective, guardrails and approvals are different controls. A guardrail automatically validates input, output, or tool calls. An approval boundary stops higher-authority work until a human or policy decision allows it.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: analysis | tutorial
- Test environment: No live execution. This post is based on OpenAI Agents SDK guardrails documentation and Codex approval/sandbox documentation.
- Test version: OpenAI Agents SDK and Codex documentation checked on 2026-04-29. No local runtime version is fixed.
- Evidence level: official documentation, security project documentation

## Problem Statement

Two design mistakes are common: assuming guardrails remove the need for approval, or assuming approval removes the need for guardrails. Guardrails are useful for repeated mechanical checks, but they do not assign organizational responsibility. Approvals create authority boundaries, but they do not automatically validate every input or output.

This post separates where each control belongs in an agent harness.

## Verified Facts

- OpenAI Agents SDK documentation describes input guardrails, output guardrails, and tool guardrails as separate workflow points.
  Evidence: [OpenAI Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- In the Agents SDK documentation, tool guardrails run around custom function tools, while handoffs and hosted/built-in tools do not use the same guardrail pipeline.
  Evidence: [OpenAI Agents SDK Tool guardrails](https://openai.github.io/openai-agents-python/guardrails/#tool-guardrails)
- Codex documentation describes approvals for actions such as edits outside the workspace, network access, and app/connector tool calls with side effects.
  Evidence: [Codex agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- OWASP LLM01 lists least privilege, human approval, external-content separation, and input/output filtering as prompt injection mitigations.
  Evidence: [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

## Reproduction Steps

Start by classifying actions into four groups.

1. Read actions: file reads, searches, issue reads, log reads
2. Write actions: file edits, config changes, PR comments, ticket state changes
3. Execution actions: shell commands, build/test, code execution, migrations
4. External-impact actions: network calls, deploys, secret access, cloud/IAM changes, destructive operations

Then place guardrails and approvals at different points.

| Stage | Guardrail example | Approval example |
| --- | --- | --- |
| Before input | Detect secrets, personal data, or prompt injection patterns | Ask a person to confirm a high-risk request |
| Before tool execution | Validate tool schema, allowed resources, and path allowlists | Approve writes outside workspace, network, or deploys |
| After tool execution | Redact output and detect secret leakage | Ask for extra approval if the change is larger than expected |
| Before final output | Check unsupported claims or sensitive disclosure | Approve incident reports or policy changes |

An example policy can be written like this.

```text
guardrail:
  - block secrets in tool arguments
  - reject writes outside allowed paths
  - redact token-like values in tool output

approval:
  - require approval for network access
  - require approval for deployment or destructive commands
  - require approval for connector calls with side effects
```

## Observations

- Guardrails are fast and repeatable, but can produce false positives and false negatives.
- Approvals add responsibility and context, but too many prompts can make users approve by habit.
- A good harness uses guardrails to reduce obvious risk and approvals to stop actions with larger authority or external impact.

## Interpretation

In my view, a guardrail asks, "Does this input, output, or tool call satisfy policy?" An approval asks, "May this authority be used now?" Keeping those questions separate makes incident review clearer.

Opinion: low-risk repeatable work should lean on guardrails, while irreversible changes and external-impact actions should require approval.

## Limitations

- Guardrail and approval implementations differ by product. Hosted tools, built-in execution tools, and MCP connectors need product-specific review.
- Approval is mainly an operational control. It loses value if the approver cannot understand the requested action.
- This post does not replace legal, privacy, or audit requirements for a specific organization.

## References

- [OpenAI Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added guardrail/approval execution points, differences, and policy examples.
