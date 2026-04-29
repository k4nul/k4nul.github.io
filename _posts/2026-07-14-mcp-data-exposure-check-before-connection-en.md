---
layout: single
title: "Check data exposure before connecting MCP"
description: "Explains Check data exposure before connecting MCP with official documentation, operational checks, and limitations."
date: 2026-07-14 09:00:00 +09:00
lang: en
translation_key: mcp-data-exposure-check-before-connection
section: development
topic_key: ai
categories: AI
tags: [ai, llm, agents, ai-security, ai-agent-operations]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/ai/mcp-data-exposure-check-before-connection/
---

## Summary

Before connecting an MCP server, review the data exposure path, not only the tools it offers. Resources, prompts, tools, OAuth scopes, redirects, network egress, and trace/log destinations all affect what data can leave the original system boundary.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: analysis | tutorial
- Test environment: No live execution. This post is based on MCP official security guidance and OpenAI Agents SDK MCP documentation.
- Test version: MCP 2025-06-18 security best practices and OpenAI Agents SDK MCP documentation checked on 2026-04-29.
- Evidence level: official documentation, specification documentation

## Problem Statement

MCP is commonly used as a standard interface between agents and external tools or data. Once a server is connected, its tools, resources, prompts, and authentication flow become part of the agent execution boundary. Without a data exposure review, internal documents, tickets, emails, repositories, or cloud credentials may be exposed more broadly than intended.

## Verified Facts

- OpenAI Agents SDK documentation states that MCP can expose filesystem, HTTP, or connector-backed tools to an agent.
  Evidence: [OpenAI Agents SDK MCP](https://openai.github.io/openai-agents-python/mcp/)
- MCP security best practices require per-client consent, displayed scopes, redirect URI validation, and CSRF protection.
  Evidence: [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- MCP security best practices recommend a progressive, least-privilege scope model and list wildcard or omnibus scopes as common mistakes.
  Evidence: [MCP scope minimization guidance](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices#mitigation-3)
- MCP security best practices warn about SSRF risks in server-side MCP clients that fetch OAuth-related URLs and recommend HTTPS, private IP blocking, redirect validation, and egress proxies.
  Evidence: [MCP SSRF mitigation guidance](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices#mitigation-1)
- The MCP schema reference says clients should not make tool-use decisions based only on `ToolAnnotations` from untrusted servers.
  Evidence: [MCP schema reference](https://modelcontextprotocol.io/specification/draft/schema)

## Reproduction Steps

Review an MCP connection in this order.

1. Define the server trust boundary.

- Check operator, source repository, deployment location, update process, and package version pinning.
- Distinguish local stdio servers from remote HTTP servers.

2. List the exposed surface.

```text
server: github-mcp
transport: stdio | streamable-http | hosted
tools: [list_issues, create_issue, read_file, write_file]
resources: [repo files, issues, pull requests]
prompts: [triage_prompt]
auth: OAuth | API key | local credential
logs: local file | hosted trace | vendor backend
```

3. Classify tools by impact.

- Read: lookup, search, list
- Write: comment, create issue, edit file
- Side effect: deploy, payment, permission change, external send

4. Review scopes and consent.

- Do not request `all`, `full-access`, or `*` scopes at first connection.
- The user should see which client requests which third-party scopes.
- Redirect URIs should be validated by exact match.

5. Review data paths.

- Check whether resource contents are stored in the model provider, trace backend, MCP server logs, or third-party API logs.
- Look for secrets, personal data, customer data, and internal documents moving into prompts or tool outputs.

6. Review network egress and SSRF.

- Check whether the remote MCP server or server-side client can reach internal IPs, cloud metadata, or private services.
- Do not blindly follow redirects into internal addresses.

7. Define post-connection monitoring.

- Trace executed tools, requested scopes, approvals, failed calls, blocked URLs, and redaction results.

## Observations

- MCP is not just "one more tool." It creates a new trust boundary between the agent and external systems.
- Tool descriptions and annotations from the server are not enough to prove safety.
- Broad scopes and unclear resource boundaries can turn prompt injection or mistaken tool calls into data exposure.

## Interpretation

In my view, the first review unit for MCP is data flow, not tool name. You should be able to explain which data passes through which server into model context and trace storage.

Opinion: start with read-only scopes and limited resources. Open write or side-effect tools only after approval and audit logging are ready.

## Limitations

- MCP specifications and SDK implementations are moving quickly, so confirm the exact version and host policy at connection time.
- This is a pre-connection review checklist. It does not certify any specific MCP server as safe.
- Organization-specific data classification, DLP, legal hold, and retention policies still apply.

## References

- [OpenAI Agents SDK MCP](https://openai.github.io/openai-agents-python/mcp/)
- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- [MCP Authorization](https://modelcontextprotocol.io/specification/draft/basic/authorization)
- [MCP Schema Reference](https://modelcontextprotocol.io/specification/draft/schema)
- [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added MCP data surface, scope, consent, SSRF, and logging checks.
