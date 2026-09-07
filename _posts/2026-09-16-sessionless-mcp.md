---
layout: single
title: "MCP는 상태를 없앤 것이 아니라, 상태의 위치를 바꿨다"
description: "MCP 2026-07-28의 stateless request/response 전환이 gateway, cache, 장기 업무 상태 설계에 어떤 변화를 주는지 정리한다."
date: 2026-09-16 09:00:00 +09:00
lang: ko
translation_key: sessionless-mcp-state-routing-cache
section: development
topic_key: ai
categories: AI
tags: [ai, agents, mcp, api-design, distributed-systems, caching]
track: agent-interface-engineering
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

MCP 2026-07-28은 전송 계층의 세션과 `initialize`/`initialized` handshake를 없애고 stateless request/response 중심으로 바꿨다. 이는 서버가 상태를 전혀 갖지 않는다는 선언이 아니다. **호출 간 애플리케이션 상태가 필요하면, 서버가 복구 가능한 저장소와 명시적 요청 데이터(예: workflow handle)를 통해 그 상태를 관리해야 한다는 설계 변화**다.

이 글은 MCP server를 여러 인스턴스와 gateway 뒤에 둘 때 무엇이 단순해지고, cache·업무 상태·권한 정책은 어디에 남아야 하는지를 다룬다.

## Document Info / Environment

- 작성일·검증 기준일: 2026-09-07
- 문서 성격: specification analysis / operations guide
- 테스트 환경: 직접 MCP server를 배포하지 않았다. 2026-07-28 공식 릴리스와 사양을 분석했다.
- 범위: protocol-level 상태 변화와 운영 설계. 특정 SDK/client 지원 범위는 주장하지 않는다.

## Problem Statement / 문제 정의

세션 기반 연결은 "이 요청이 어느 연결에서 왔는가"를 서버가 기억하게 한다. load balancer 뒤에서 요청이 다른 인스턴스로 가면 session affinity 또는 공유 session store가 필요해진다. 반면 장기 import, 배포, 승인 대기처럼 실제 업무는 여러 호출에 걸쳐 상태를 보존해야 한다.

여기서 두 가지를 구분해야 한다.

1. **전송 상태:** handshake, 연결, protocol session처럼 transport가 관리하던 정보
2. **업무 상태:** 작업 대상, 진행 단계, 권한 범위, 외부 job ID, 결과 증거처럼 제품이 관리해야 할 정보

첫 번째를 없앤다고 두 번째까지 없애면, 재시도와 장애 복구에서 작업을 식별할 수 없게 된다.

## Verified Facts / 확인된 사실

- MCP 2026-07-28은 bidirectional/session-based core에서 stateless request/response core로 전환하며 `initialize`/`initialized`와 `Mcp-Session-Id`를 제거했다.
  근거: [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- Streamable HTTP 요청에는 `Mcp-Method`, `Mcp-Name` header가 포함된다. 공식 릴리스는 이를 gateway, WAF, rate limiter가 JSON body를 해석하지 않고 route와 정책 분류를 적용할 수 있는 변화로 설명한다.
  근거: [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- `tools/list`, `prompts/list`, `resources/list`, `resources/read` 응답에는 `ttlMs`, `cacheScope` cache metadata가 추가됐다.
  근거: [MCP specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)
- protocol이 stateless여도 cross-call state가 필요한 server는 tool 결과로 명시적 handle을 반환하고 다음 tool argument로 받는 방식을 공식 릴리스가 제안한다. 이는 모든 상태에 대한 프로토콜 의무가 아니라 권고되는 애플리케이션 설계 패턴이다.
  근거: [MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/)

## Reproduction Steps / 재현 순서

새 MCP tool을 설계할 때 다음 표를 먼저 만든다.

| 질문 | 예시 결정 |
| --- | --- |
| 요청 하나로 끝나는가? | 검색은 결과를 즉시 반환 |
| 다음 호출에도 식별자가 필요한가? | import는 `import_job_id` 반환 |
| handle은 누가 소유·검증하는가? | server가 사용자/tenant와 묶어 검증 |
| 무엇을 cache할 수 있는가? | 선언된 cache scope가 의도한 공유를 허용할 때만 tool catalog에 짧은 TTL cache |
| cache가 위험한가? | 권한별 resource 목록과 민감 결과는 공유 cache 금지 |

gateway에는 `Mcp-Method`/`Mcp-Name` 기반 route와 tool별 rate limit을 둘 수 있다. 다만 이 header는 인프라 정책·분류용 metadata이므로, server는 access token과 server-side policy를 기준으로 대상 요청의 authorization을 독립적으로 판정해야 한다.

## Observations / 관찰 결과

stateless transport는 round-robin과 장애 교체를 단순하게 만든다. 하지만 cache와 업무 handle은 새 공격면도 만든다. 다른 tenant가 예측 가능한 handle을 재사용하거나, 권한이 다른 사용자가 공유 cache에서 목록을 받으면 전송 계층의 단순화가 데이터 경계 약화로 바뀐다.

따라서 cache key에는 최소한 tool version, tenant/권한 경계, locale 또는 result-shaping 조건을 검토해야 한다. handle은 추측하기 어려운 값이어야 하며, 서버가 매 호출마다 주체·권한·만료·현재 상태를 확인해야 한다.

## Interpretation / 해석

내 판단으로 sessionless MCP의 실무적 이점은 "서버가 아무것도 기억하지 않아도 된다"가 아니라 **숨은 transport state를 업무 계약으로 승격한다**는 데 있다.

```text
transport request
+ explicit job handle (필요할 때만)
+ server-side owner/tenant check
+ bounded cache policy
+ tool-specific route and rate limit
```

이 계약을 갖추면 인스턴스가 바뀌어도 import나 approval 흐름을 복구할 수 있다. 반대로 handle 없이 대화 문맥에만 상태를 두면, 모델의 설명은 남아도 서버가 실행해야 할 정확한 작업을 다시 찾을 수 없다.

## Limitations / 한계

- 이 글은 사양 분석이며 특정 MCP SDK, proxy, gateway의 실제 호환성을 테스트하지 않았다.
- `ttlMs`와 `cacheScope`는 server가 제공하는 cache lifetime·scope 정보다. 이를 따른다고 tenant·권한 격리나 cache key 정확성이 자동으로 보장되지는 않는다.
- stateless는 요청이 protocol session에 독립적이라는 뜻이다. request-scoped SSE 응답이나 `subscriptions/listen`이 여는 장기 notification stream까지 금지하는 의미는 아니다.
- 명시적 handle도 authorization, TTL, audit, idempotency를 별도로 구현하지 않으면 안전하지 않다.
- stateless protocol은 외부 결제·배포·삭제의 rollback 또는 업무 성공을 보장하지 않는다.

## References / 참고자료

- [The 2026-07-28 MCP Specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [MCP Streamable HTTP transport, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http)
- [MCP tools and cache metadata, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
- [MCP resources and cache metadata, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/server/resources)

## Change Log / 변경 이력

- 2026-09-07: KR local draft 작성. 공식 2026-07-28 사양만 분석했으며 `published: false`이다. 사이트·외부 채널·실제 일정은 변경하지 않았다.
