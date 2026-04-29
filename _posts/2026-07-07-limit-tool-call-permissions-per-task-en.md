---
layout: single
title: "Limit tool-call permissions per task"
description: "Explains Limit tool-call permissions per task with official documentation, operational checks, and limitations."
date: 2026-07-07 09:00:00 +09:00
lang: en
translation_key: limit-tool-call-permissions-per-task
section: development
topic_key: ai
categories: AI
tags: [ai, llm, agents, ai-security, ai-agent-operations]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/ai/limit-tool-call-permissions-per-task/
---

## Summary

If every tool is always available to an agent, the agent's authority can exceed the task. Per-task tool permissions mean enabling only the tools, argument ranges, resources, and duration needed for the current task.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: analysis | tutorial
- Test environment: No live execution. This post is based on OpenAI Agents SDK, Codex security documentation, and OWASP LLM06.
- Test version: Related official documentation checked on 2026-04-29. No local agent runtime version is fixed.
- Evidence level: official documentation, security project documentation

## Problem Statement

The risk in LLM agents often grows at the tool boundary. A summarization task should not have shell, delete, deploy, external-send, or secret-read tools available by default. If it does, prompt injection or model error can become real system change.

## Verified Facts

- OpenAI Agents SDK documentation describes agents as composed of instructions, tools, guardrails, handoffs, and related behavior.
  Evidence: [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- Agents SDK guardrail documentation describes tool guardrails around function-tool calls.
  Evidence: [OpenAI Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- Codex security documentation describes sandbox and approval controls for actions such as edits outside the workspace, network access, and connector/tool calls with side effects.
  Evidence: [Codex agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- OWASP LLM06 Excessive Agency describes excessive functionality, permissions, and autonomy as risks in LLM applications.
  Evidence: [OWASP LLM06 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

## Reproduction Steps

Classify the task before granting tools.

| Task type | Default allowed tools | Default blocked tools | Approval candidates |
| --- | --- | --- | --- |
| Document summary | read, search | write, shell, network send | sensitive document access |
| Code review | read, diff, test readout | apply patch, deploy | broad file reads |
| Code edit | read, apply patch, test | deploy, secret read | shell command |
| Deployment prep | read, build, artifact inspect | production deploy | deploy, cloud write |
| Incident review | read logs, search, trace | delete, rotate, external send | secret access, account disable |

Build the harness policy in this order.

1. Declare task intent: `summarize`, `review`, `edit`, `test`, `deploy`, or `incident`.
2. Create a tool allowlist: limit tool names and argument schemas per task.
3. Limit resource scope: repository paths, namespaces, cloud projects, ticket projects, or time windows.
4. Separate write and side effects: do not put read tools and write/deploy/send tools in the same default permission set.
5. Put high-risk tools behind approval: shell, network, secret, deployment, delete, payment, and IAM changes.
6. Add tool guardrails: check path traversal, external URLs, secret-like values, and destructive commands.
7. Record traces: allowed tools, denied tools, approval requests, and actual execution results.

Example:

```yaml
task: code_review
tools:
  allow:
    - read_file
    - list_files
    - git_diff
  deny:
    - apply_patch
    - shell
    - deploy
resources:
  paths:
    - src/**
    - tests/**
approval_required:
  - shell
  - external_network
  - secret_read
```

## Observations

- The same agent needs different tools for different tasks.
- Tool names are not enough. `read_file` still needs path scope, and `http_request` still needs destination scope.
- Approval is most useful at high-risk boundaries, not on every single tool call.

## Interpretation

In my view, "task permissions" are a better operating unit than "agent permissions." If the request is summarization, grant summarization authority. If the request is code editing, grant editing authority.

Opinion: tool permissions should expire with the task. Long-lived sessions should not carry powerful permissions from a previous task into the next one.

## Limitations

- OpenAI Agents SDK, Codex, MCP hosts, and custom orchestrators have different tool permission models.
- Hosted tools or built-in execution tools may not use the same guardrail points as custom function tools.
- Real implementations need integration with policy engines, audit logs, identity providers, and secret managers.

## References

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [OWASP LLM06 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added task-specific tool allowlists, resource scopes, approval boundaries, and trace criteria.
