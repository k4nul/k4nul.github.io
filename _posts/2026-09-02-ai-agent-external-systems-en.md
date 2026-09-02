---
layout: single
title: "What It Means for an AI Agent to Work with External Systems"
description: "Why AI agents that read data and call external tools need explicit interface contracts, least privilege, approval boundaries, and verifiable outcomes."
date: 2026-09-02 00:00:00 +09:00
lang: en
translation_key: ai-agent-external-systems
section: development
topic_key: ai
categories: AI
tags: [ai, agents, tools, mcp, agent-security, agent-evaluation]
track: agent-interface-engineering
published: false
permalink: /en/development/ai-agent-external-systems/
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

AI agents are no longer limited to producing text in a chat interface. They can read data sources, call tools, continue multi-step work, and in some cases request changes in external systems. The central design problem is therefore not only how naturally a model writes, but **which actions are allowed under which authority and how their outcomes are verified**.

This opening article defines four design axes for agents that work with external systems: tool contracts, authority boundaries, human approval, and verifiable records. It is not an installation guide or a comparison of model performance.

## Document Info / Environment

- Draft date: 2026-09-02
- Verification baseline: 2026-09-02
- Document type: concept analysis / operations guide
- Test environment: no direct execution test. This article compares public statements in primary documentation to establish design boundaries.
- Version baseline: MCP documentation path `2026-07-28`; Chrome WebMCP documentation updated 2026-08-07. Product and browser support can change after this date.
- Source grade: official product documentation, official protocol documentation, and official research.

## Problem Statement / 문제 정의

“Summarize this email” and “read this email and send a reply to the customer” are fundamentally different requests. The latter can read external data, process untrusted content, and take actions that are difficult to reverse.

A common mistake is to treat a tool connection as a simple feature extension. It expands capability, but it also expands data-exposure paths and authority. Rather than attaching security after a connection is made, the interface should answer four questions from the start:

1. What information may the agent read?
2. May it only propose a change, or may it make the change?
3. Who approves the action, and at what point?
4. What evidence proves the outcome, and what record remains if it fails?

## Verified Facts / 확인된 사실

- OpenAI’s Agents SDK describes agents as applications that plan, call tools, collaborate across specialists, and retain enough state for multi-step work. Its documentation also states that an application server can retain control over deployment, tool implementation, state storage, and approval decisions.
  Evidence: [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents)

- The official MCP documentation describes MCP as an open-source standard for connecting AI applications with external systems. Its examples include data sources such as local files and databases, tools such as search engines and calculators, and workflows such as specialized prompts.
  Evidence: [Model Context Protocol: What is MCP?](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro)

- Chrome’s WebMCP documentation describes a **proposed web-platform API** through which a website can register structured, callable tools, so a browser agent need not rely only on DOM inference and simulated clicks or typing (“actuation”). A tool can currently describe its expected input with `inputSchema`. WebMCP does not itself require the browser-to-agent transport to be MCP or guarantee automatic discovery by every agent. As of 2026-09-02, it can be tested in an origin trial beginning with Chrome 149; it must not be presented as a finalized universal web standard, a default feature of every browser, or an automatic guarantee of authentication, authorization, or user approval.
  Evidence: [Chrome for Developers: WebMCP](https://developer.chrome.com/docs/ai/webmcp), [WebMCP Draft Community Group Report](https://webmachinelearning.github.io/webmcp/)

- OpenAI’s agent-safety guide discusses prompt injection, unintended private-data sharing with connected MCPs, tool approvals, structured outputs, evaluations, and trace grading. It explicitly says that mitigations reduce risk rather than making agents perfect.
  Evidence: [OpenAI: Safety in building agents](https://developers.openai.com/api/docs/guides/agent-builder-safety)

- Anthropic explains that browser agents face a large prompt-injection attack surface because they process untrusted webpages, documents, advertisements, and search results while being able to act. Its research explicitly says that no browser agent is immune to prompt injection.
  Evidence: [Anthropic: Mitigating the risk of prompt injections in browser use](https://www.anthropic.com/research/prompt-injection-defenses)

## Reproduction Steps / 재현 순서

This is not a tutorial that connects and runs a particular product. The following is a repeatable design review for a proposed external-system connection.

1. Categorize each proposed action as `read`, `draft`, `change request`, or `irreversible execution`.
2. For each action, document its required input, permitted data scope, authority, approver, and success evidence.
3. Declare that externally retrieved content is not trusted instruction.
4. For changing tools, define failure, retry, duplicate-execution, and cancellation behavior.
5. Before operating the workflow, include normal cases as well as insufficient-authority, invalid-input, suspected-prompt-injection, and rejected-approval cases in the evaluation set.

No direct reproduction was performed: this draft did not connect an MCP server, browser agent, or commercial API. It therefore makes no claim about a tool’s real-world success rate, cost, latency, or security level.

## Observations / 관찰 결과

A comparison of the official documentation shows that a model call is only part of an agent implementation. As an agent connects to more external systems, the application layer needs tool definitions, state handling, approvals, traces, and evaluation.

Browser actuation and structured tool calls are not the same problem. Actuation interprets a human-facing UI and performs multiple steps; a structured tool expresses intended input and action as a contract. WebMCP’s present status is a proposed progressive enhancement for site-defined tasks, not evidence that it immediately replaces UI automation or guarantees correct tool output or a successful business outcome.

## Interpretation / 해석

In my view, the minimum unit of an agent capability is not “prompt + model.” It is this contract:

```text
permitted purpose
+ explicit input
+ least privilege
+ approval condition
+ observable outcome
+ failure, retry, and cancellation rules
```

Without that contract, a successful tool call does not establish a successful business outcome. For example, a `send_email` call can return an HTTP success while still sending to the wrong recipient, sending a duplicate message, or sending unapproved content.

A prudent first step is therefore to separate lower-impact, reviewable actions—such as read-only retrieval and draft generation—from consequential actions. Writes, transmission, deletion, payment, and deployment do not become safe merely because they have a tool name. Their authority scope, user confirmation, audit record, and reversibility must be designed together.

## Limitations / 한계

- This is an analysis of public primary documentation; it does not validate any organization’s authority model, regulatory requirements, or workflow.
- Actual MCP and WebMCP support, SDK behavior, browser capabilities, and product UIs can change.
- A WebMCP input schema can help an agent understand expected input, but it does not replace independent authentication, authorization, server-side input validation, transaction confirmation, or user approval.
- A structured tool contract does not eliminate prompt injection or model mistakes. It must be combined with approvals, least privilege, input validation, traces, and evaluation.
- A release decision needs organization-specific review of privacy, access control, audit retention, payment/deletion/deployment policy, and incident response.

## References / 참고자료

- [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents)
- [OpenAI: Safety in building agents](https://developers.openai.com/api/docs/guides/agent-builder-safety)
- [Model Context Protocol: What is MCP?](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro)
- [Chrome for Developers: WebMCP](https://developer.chrome.com/docs/ai/webmcp)
- [WebMCP Draft Community Group Report](https://webmachinelearning.github.io/webmcp/)
- [Anthropic: Mitigating the risk of prompt injections in browser use](https://www.anthropic.com/research/prompt-injection-defenses)

## Change Log / 변경 이력

- 2026-09-02: Reliability review: clarified WebMCP’s experimental status, its boundary from MCP, and the non-guarantees of input schemas; added the primary draft specification. `published: false`; no publication schedule, public status, or site file was changed.
- 2026-09-02: Created a local draft using primary, authoritative sources only. `published: false`; no publication schedule, public status, or site file was changed.
