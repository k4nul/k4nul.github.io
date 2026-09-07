---
layout: single
title: "Long-Running Agent Workflows with MCP Tasks: Resume, Input, and Cancellation"
description: "Interpreting MCP Tasks' durable task IDs, polling, input_required, and cooperative cancellation as a state contract for long-running tools."
date: 2026-09-23 09:00:00 +09:00
lang: en
translation_key: mcp-tasks-resume-input-cancellation
section: development
topic_key: ai
categories: AI
tags: [ai, agents, mcp, async-jobs, api-design, reliability]
track: agent-interface-engineering
published: false
permalink: /en/development/mcp-tasks-resume-input-cancellation/
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

A CI run, bulk operation, model-training job, or approval wait can outlive an HTTP connection. MCP Tasks is the opt-in, draft `io.modelcontextprotocol/tasks` extension. When a client advertises support on the relevant request and a server elects to task-enable a supported `tools/call`, the server can return a durable `taskId` rather than a final result, letting the client query state again, supply input, or request cancellation.

A task API does not make long-running work automatically successful. Task state, external side effects, cancellation, and outcome verification remain separate contracts.

## Document Info / Environment

- Draft and verification baseline: 2026-09-07
- Document type: specification analysis / operations guide
- Test environment: no direct implementation or execution. This draft analyzes official MCP Tasks documentation.
- Scope: state design for long-running tools, not host-specific support or performance.

## Problem Statement / 문제 정의

Suppose `deploy_service` completes after twenty minutes. If the client disconnects, the server must not lose the job, and the client must not start a duplicate deployment. A workflow also needs to distinguish a missing approval or parameter from failure.

A task API needs evidence for four things:

1. durable task creation;
2. current state and required next input;
3. the state change actually made by an external system;
4. cleanup and final outcome after cancellation or failure.

## Verified Facts / 확인된 사실

- MCP Tasks is an opt-in draft extension for long-running MCP operations. A server can return a durable task handle rather than a final result immediately.
  Evidence: [MCP Tasks overview](https://modelcontextprotocol.io/extensions/tasks/overview)
- The client advertises Tasks support in request metadata, while the server decides per eligible request whether to create a task. A capable client must handle either a normal result or a `CreateTaskResult`.
  Evidence: [MCP Tasks extension specification](https://tasks.extensions.modelcontextprotocol.io/specification/2026-07-28/tasks)
- The server must create a task durably before returning its creation response; that response can include `taskId`, status, `ttlMs`, and `pollIntervalMs`.
  Evidence: [MCP Tasks overview](https://modelcontextprotocol.io/extensions/tasks/overview)
- A client uses `tasks/get` for status and can answer `input_required` requests with `tasks/update`.
  Evidence: [MCP Tasks overview](https://modelcontextprotocol.io/extensions/tasks/overview)
- `tasks/cancel` is cooperative. On success, the server acknowledges cancellation intent with an empty result, and observable state is eventually consistent. If work already finished or cancellation cannot take effect, the final state may be other than `cancelled`. Terminal states are `completed`, `failed`, and `cancelled`.
  Evidence: [MCP Tasks overview](https://modelcontextprotocol.io/extensions/tasks/overview)

## Reproduction Steps / 재현 순서

Draw the state contract before writing a long-running tool.

```text
MCP task statuses:
working ↔ input_required
working | input_required → completed | failed | cancelled

Application-specific facts—such as cancellation requested, provider cleanup,
or an external side effect—belong in a separate audit/workflow record.
```

Then answer these questions.

| Design question | Example |
| --- | --- |
| What binds a task ID? | User, tenant, and original request hash. |
| What remains after TTL? | Because an MCP task may be marked failed or deleted after TTL, retain an audit summary and external job ID under a separate audit-retention policy. |
| What does an input reconfirm? | Approver, target, and change summary. |
| What follows cancellation? | Provider status and cleanup outcome. |
| What prevents retry duplication? | A single deployment start for one intent. |

## Observations / 관찰 결과

Task status is the tool server's view; business outcome is the external system's view. A task can become `cancelled` after a provider already sent an email or started a deployment. Conversely, `completed` does not by itself prove the deployment reached the intended region.

A final result should therefore carry a target ID, external job ID, observation time, and a method for final verification—not just a prose sentence. A failure result should state retry eligibility and known side effects.

## Interpretation / 해석

MCP Tasks is more than replacing a long request with polling. It is a way to make resumable workflow state an API contract.

```text
task identity + owner check + state transition
+ input/approval record + external outcome evidence
+ cancellation and retry policy
```

Without these elements, a task only keeps a UI spinner alive and cannot answer what actually ran after an incident.

## Limitations / 한계

- This is an official-documentation analysis and did not test commercial host support.
- Tasks is a draft extension as of the verification baseline; it requires explicit client and server opt-in, and its wire format or behavior may change.
- Cooperative cancellation does not guarantee rollback or removal of external side effects.
- In MCP Tasks, `failed` denotes a JSON-RPC error during execution. A tool result with `isError: true` may instead appear in a `completed` task result, so product-level failure taxonomy must not be equated with MCP task status.
- A durable task store still needs retention, tenant isolation, and access-control policy.
- Task state alone does not prove that the user's business objective was achieved.

## References / 참고자료

- [MCP Tasks overview](https://modelcontextprotocol.io/extensions/tasks/overview)
- [MCP Tasks extension specification — 2026-07-28 draft](https://tasks.extensions.modelcontextprotocol.io/specification/2026-07-28/tasks)
- [MCP extension negotiation, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/lifecycle)

## Change Log / 변경 이력

- 2026-09-07: Created as an English local draft. `published: false`; no site, external-channel, or actual schedule was changed.
