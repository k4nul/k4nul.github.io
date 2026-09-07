---
layout: single
title: "Sessionless MCP: Where State, Routing, and Caching Belong Now"
description: "How MCP 2026-07-28's stateless request/response core changes gateway, cache, and long-running workflow-state design."
date: 2026-09-16 09:00:00 +09:00
lang: en
translation_key: sessionless-mcp-state-routing-cache
section: development
topic_key: ai
categories: AI
tags: [ai, agents, mcp, api-design, distributed-systems, caching]
track: agent-interface-engineering
published: false
permalink: /en/development/sessionless-mcp-state-routing-cache/
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

MCP 2026-07-28 removes transport-level sessions and the `initialize`/`initialized` handshake in favor of a stateless request/response core. That does not mean a server has no state. When application state must survive across calls, the server needs to manage it through recoverable storage and explicit request data—such as a workflow handle—rather than a hidden protocol session.

This article examines what becomes simpler behind gateways and multiple instances, and where cache policy, workflow state, and authorization still belong.

## Document Info / Environment

- Draft and verification baseline: 2026-09-07
- Document type: specification analysis / operations guide
- Test environment: no MCP server was deployed. This draft analyzes the official 2026-07-28 release and specification.
- Scope: protocol-state changes and operational design, not a compatibility claim for a particular SDK or client.

## Problem Statement / 문제 정의

A session-oriented connection lets a server remember which connection a request belongs to. Behind a load balancer, a later request may reach another instance and require session affinity or shared session storage. Actual work—an import, deployment, or approval wait—can nevertheless need durable identity across several calls.

Two different forms of state must be separated:

1. **Transport state:** handshake, connection, and protocol session information.
2. **Workflow state:** target, progress, authority scope, external job ID, and outcome evidence owned by the product.

Removing the first does not remove the second. Treating both as disposable makes retries and recovery unable to identify the work.

## Verified Facts / 확인된 사실

- MCP 2026-07-28 moves from a bidirectional, session-based core to a stateless request/response core and removes `initialize`/`initialized` plus `Mcp-Session-Id`.
  Evidence: [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- Streamable HTTP requests include `Mcp-Method` and `Mcp-Name`. The release explains that gateways, WAFs, and rate limiters can apply routing and policy classification from headers rather than parsing JSON bodies.
  Evidence: [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- `tools/list`, `prompts/list`, `resources/list`, and `resources/read` have new cache metadata: `ttlMs` and `cacheScope`.
  Evidence: [MCP specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)
- For state required across calls, the official release proposes returning an explicit handle from one tool and passing it as an argument to the next. This is an application-design pattern, not a universal protocol requirement.
  Evidence: [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)

## Reproduction Steps / 재현 순서

Before implementing a new MCP tool, create a small decision table.

| Question | Example decision |
| --- | --- |
| Does one request finish the work? | A search returns its result immediately. |
| Is identity needed later? | An import returns `import_job_id`. |
| Who owns and validates the handle? | The server binds it to user and tenant. |
| What can be cached? | A tool catalog may use a short TTL only when its declared cache scope permits the intended sharing. |
| What is unsafe to share? | Permission-shaped resource lists and sensitive results. |

Gateways can then apply `Mcp-Method`/`Mcp-Name`-based routing and per-tool rate limits. Those headers are infrastructure metadata, not standalone proof of authorization, so the server must independently authorize the request from its access token and server-side policy.

## Observations / 관찰 결과

Stateless transport simplifies round-robin routing and instance replacement. It also creates new failure modes around cache and workflow handles. A predictable handle reused by another tenant, or a permission-shaped list served from a shared cache, turns transport simplification into a data-boundary failure.

Cache keys therefore need review for tool version, tenant/authority boundary, locale, and any result-shaping condition. A handle should be hard to guess; each call should revalidate its subject, authority, expiry, and current workflow state.

## Interpretation / 해석

In my view, the operational benefit of sessionless MCP is not that a server remembers nothing. It is that hidden transport state becomes an explicit workflow contract.

```text
transport request
+ explicit workflow handle (only when needed)
+ server-side owner/tenant check
+ bounded cache policy
+ tool-specific route and rate limit
```

With this contract, an import or approval flow can survive an instance change. Without it, a model may retain a conversational description but the server cannot recover the precise unit of work to execute.

## Limitations / 한계

- This is a specification analysis; it did not test a particular MCP SDK, proxy, or gateway.
- `ttlMs` and `cacheScope` are server-provided cache lifetime and scope information. Honoring them does not automatically guarantee tenant/authorization isolation or a correct cache key.
- “Stateless” means requests are independent of a protocol session; it does not prohibit request-scoped SSE responses or the long-lived notification stream opened by `subscriptions/listen`.
- An explicit handle is unsafe without separate authorization, expiry, audit, and idempotency controls.
- A stateless protocol does not guarantee rollback or business success for payment, deployment, or deletion.

## References / 참고자료

- [The 2026-07-28 MCP Specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [MCP Streamable HTTP transport, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [MCP tools and cache metadata, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [MCP resources and cache metadata, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)

## Change Log / 변경 이력

- 2026-09-07: Created as an English local draft from the official 2026-07-28 specification. `published: false`; no site, external-channel, or actual schedule was changed.
