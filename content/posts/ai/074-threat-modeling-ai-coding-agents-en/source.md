---
layout: single
title: "Threat modeling AI coding agents"
description: "Explains Threat modeling AI coding agents with official documentation, operational checks, and limitations."
date: 2026-07-21 09:00:00 +09:00
lang: en
translation_key: threat-modeling-ai-coding-agents
section: development
topic_key: ai
categories: AI
tags: [ai, llm, agents, ai-security, ai-agent-operations]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/ai/threat-modeling-ai-coding-agents/
---

## Summary

Threat modeling an AI coding agent is not only about hallucinated code. The attack surface includes repository input, external content, tool authority, secrets, sandboxing, approvals, traces, and deployment boundaries.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: analysis | tutorial
- Test environment: No live execution. This post is based on OpenAI Codex/Agents SDK documentation and OWASP LLM risk categories.
- Test version: Related official documentation checked on 2026-04-29. No specific agent runtime version is fixed.
- Evidence level: official documentation, security project documentation, NIST documentation

## Problem Statement

A coding agent can read code, create patches, run tests, execute shell commands, interact with issues and pull requests, call MCP connectors, and prepare deployments. A web-application style threat model that only lists network endpoints is not enough. You need to model the boundary between data the agent reads and tools it can execute.

## Verified Facts

- Codex security documentation describes sandboxed task execution and approval boundaries for file-system, network, and side-effecting actions.
  Evidence: [OpenAI Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- OpenAI Agents SDK tracing documentation describes traces for LLM generations, tool calls, handoffs, and guardrails.
  Evidence: [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)
- OWASP LLM01 describes prompt injection as a risk that can alter model behavior or output in unintended ways.
  Evidence: [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- OWASP LLM02 addresses sensitive information disclosure through LLM outputs or related systems.
  Evidence: [OWASP LLM02 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
- OWASP LLM06 describes excessive functionality, permissions, or autonomy leading to damaging actions.
  Evidence: [OWASP LLM06 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- NIST AI RMF Generative AI Profile provides risk management guidance organized around govern, map, measure, and manage activities.
  Evidence: [NIST AI RMF Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)

## Reproduction Steps

Start by listing assets and boundaries.

| Area | Question | Example risk |
| --- | --- | --- |
| Input | Can the agent trust what it reads? | prompt injection, poisoned issue, malicious README |
| Authority | Which tools and credentials are available? | excessive agency, secret access, destructive command |
| Execution | Where do commands and tests run? | sandbox escape, persistence, network egress |
| Changes | Which files and branches can be modified? | unauthorized patch, workflow tampering |
| External connections | Does it reach GitHub, cloud, MCP, or package registries? | data exfiltration, connector side effect |
| Records | What is stored in traces and logs? | missing audit trail, sensitive trace storage |

An initial threat modeling pass can follow this order.

1. Split task types: Q&A, code review, code edit, test execution, deployment preparation, incident response.
2. Classify input origins: user request, repository files, issue/PR comments, web results, MCP resources, memory.
3. Limit tool authority per task: read, write, shell, network, secret, and deploy are separate permissions.
4. Put high-risk actions behind approval: writes outside the workspace, external sends, deploys, secret access, IAM changes.
5. Set sandbox and network defaults: deny by default, approve when needed, allowlist where possible.
6. Define trace fields: input source, tool call, approval, guardrail, verification, failure.
7. Test abuse cases: malicious README, PR title injection, compromised dependency, secret exfiltration, test command manipulation.

## Observations

- Coding agent security depends more on operational boundaries than on model quality alone.
- The same prompt injection has different impact on a read-only agent and an agent with deployment authority.
- Threat models become actionable when they describe what this task may do, not what the agent can do in theory.

## Interpretation

In my view, the main threat appears when natural-language input can drive execution authority. Prompt, tool, sandbox, approval, and trace should be designed as one harness boundary.

Opinion: the first threat model does not need a perfect diagram. Five concrete abuse cases mapped to current controls are more useful.

## Limitations

- Agent products differ in sandbox, approval, network, and MCP behavior.
- This is an introductory threat model and does not measure exploitability of specific vulnerabilities.
- Organization-specific legal, privacy, and security requirements must be added separately.

## References

- [OpenAI Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OWASP LLM02 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
- [OWASP LLM06 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- [NIST AI RMF Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added AI coding agent assets, trust boundaries, abuse cases, and official evidence.
