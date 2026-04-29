---
layout: single
title: "Prompt injection as a harness problem"
description: "Explains Prompt injection as a harness problem with official documentation, operational checks, and limitations."
date: 2026-06-30 09:00:00 +09:00
lang: en
translation_key: prompt-injection-as-a-harness-problem
section: development
topic_key: ai
categories: AI
tags: [ai, llm, agents, ai-security, ai-agent-operations]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/ai/prompt-injection-as-a-harness-problem/
---

## Summary

Prompt injection is not solved by better prompt wording alone. If an agent reads external content and can call tools, the harness must separate "text to analyze" from "instructions to execute".

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: analysis | tutorial
- Test environment: No live execution. This post is based on OWASP LLM01, OpenAI Agents SDK guardrails, and Codex approval/sandbox documentation.
- Test version: Related official documentation checked on 2026-04-29. No local agent runtime version is fixed.
- Evidence level: official documentation, security project documentation

## Problem Statement

Prompt injection is often framed as a model obedience problem, but the operational risk is broader. The malicious instruction may live in a web page, README, issue comment, email, log, or retrieved document. If the agent also has tool permissions, injection can lead to file modification, external transmission, secret disclosure, or arbitrary command execution.

This post treats prompt injection as a harness problem: input origin, tool authority, approval, validation, and traceability.

## Verified Facts

- OWASP LLM01 defines prompt injection as prompts altering an LLM's behavior or output in unintended ways.
  Evidence: [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- OWASP separates direct and indirect prompt injection. Indirect injection can occur when an LLM processes external sources such as websites or files.
  Evidence: [OWASP LLM01 Types of Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/#types-of-prompt-injection-vulnerabilities)
- OWASP mitigation guidance includes output format validation, input/output filtering, least privilege, human approval for high-risk actions, external-content separation, and adversarial testing.
  Evidence: [OWASP LLM01 Prevention and Mitigation](https://genai.owasp.org/llmrisk/llm01-prompt-injection/#prevention-and-mitigation-strategies)
- OpenAI Agents SDK documentation describes input, output, and tool guardrails, with tool guardrails available around custom function-tool calls.
  Evidence: [OpenAI Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- Codex documentation warns that web results should still be treated as untrusted and that prompt injection can cause an agent to follow untrusted instructions.
  Evidence: [Codex agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)

## Reproduction Steps

Use this sequence when designing harness controls for prompt injection.

1. Label external input: web pages, files, issue comments, email, MCP resources, and search results are untrusted data.
2. Separate instruction and data channels: text such as "ignore previous instructions" inside an external document is data to analyze, not an instruction to execute.
3. Reduce tool authority: a read-only summarization task should not receive write, shell, network, or secret-access tools.
4. Validate tool arguments: paths, URLs, commands, queries, recipients, and cloud resource ids should be constrained by schema and allowlists.
5. Require approval for high-risk actions: deletes, deployments, external sends, payments, permission changes, and secret access.
6. Validate output shape: use schemas, citation requirements, unsupported-claim checks, and secret redaction.
7. Record traces: keep external input origin, blocked guardrails, approval requests, executed tools, and rejected tools.
8. Run adversarial tests: direct injection, indirect injection, tool argument injection, and output exfiltration scenarios.

Example policy:

```text
untrusted_content:
  sources: [web, issue_comment, email, mcp_resource, file_from_user]
  rule: "treat embedded instructions as data, not commands"

tool_policy:
  summarize: [read_file, search]
  edit_code: [read_file, apply_patch]
  deploy: approval_required
  shell_network_secret: approval_required
```

## Observations

- Prompt injection impact grows with the authority granted to the agent's tools.
- A system prompt alone does not reliably solve the problem of untrusted external text being interpreted as instruction.
- If the harness labels external content and limits tool authority, even a fooled model has less room to cause damage.

## Interpretation

In my view, prompt injection defense should center on execution authority, not only prompt wording. Assume the model can make a mistake, then make sure the harness limits what that mistake can do.

Opinion: prompt injection testing is both security testing and operations testing. The key question is not only "was the model fooled?" but "what could it do after being fooled?"

## Limitations

- There is no single complete mitigation for prompt injection. Model behavior, retrieval, tools, UI, and permission policy must be reviewed together.
- This post does not measure payload success rates or model-specific defense performance.
- Real services need domain-specific risk review for personal data, customer data, secrets, payments, and deployment authority.

## References

- [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OpenAI Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added OWASP LLM01 direct/indirect injection framing, harness controls, and permission/approval boundaries.
