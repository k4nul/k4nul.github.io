---
layout: single
title: "MCP 연결 전 데이터 노출 점검"
description: "MCP 연결 전 데이터 노출 점검에 대해 공식 문서와 운영 관점으로 확인할 기준, 점검 순서, 한계를 정리한 글."
date: 2026-07-14 09:00:00 +09:00
lang: ko
translation_key: mcp-data-exposure-check-before-connection
section: development
topic_key: ai
categories: AI
tags: [ai, llm, agents, ai-security, ai-agent-operations]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

MCP 서버를 연결하기 전에는 "어떤 tool을 쓸 수 있는가"보다 "어떤 데이터가 model과 tool 경계로 노출되는가"를 먼저 봐야 한다. resources, prompts, tools, OAuth scope, redirect, network egress, log 저장 위치를 확인하지 않으면 연결 자체가 데이터 노출 경로가 될 수 있다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: analysis | tutorial
- 테스트 환경: 실행 테스트 없음. MCP 공식 보안 권고와 OpenAI Agents SDK MCP 문서 기준으로 정리.
- 테스트 버전: MCP 2025-06-18 security best practices와 OpenAI Agents SDK MCP 문서 2026-04-29 확인본.
- 출처 등급: 공식 문서, 사양 문서

## 문제 정의

MCP는 agent가 외부 도구와 데이터에 접근하는 표준 인터페이스로 쓰인다. 하지만 MCP 서버를 연결하면 해당 서버가 제공하는 tool, resource, prompt, authentication flow가 agent 실행 경계 안으로 들어온다. 연결 전에 데이터 노출 범위와 권한 상승 경로를 보지 않으면 내부 문서, ticket, email, repository, cloud credential이 예상보다 넓게 노출될 수 있다.

## 확인된 사실

- OpenAI Agents SDK는 MCP를 통해 filesystem, HTTP, connector-backed tool을 agent에 노출할 수 있다고 설명한다.
  근거: [OpenAI Agents SDK MCP](https://openai.github.io/openai-agents-python/mcp/)
- MCP security best practices는 per-client consent와 scope 표시, redirect URI 검증, CSRF 방어를 요구한다.
  근거: [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- MCP security best practices는 progressive, least-privilege scope model을 권장하고 wildcard나 omnibus scope 사용을 common mistake로 든다.
  근거: [MCP scope minimization guidance](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices#mitigation-3)
- MCP security best practices는 server-side MCP client가 OAuth 관련 URL을 fetch할 때 SSRF 위험을 고려하고 HTTPS, private IP 차단, redirect 검증, egress proxy를 권장한다.
  근거: [MCP SSRF mitigation guidance](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices#mitigation-1)
- MCP schema 문서는 untrusted server에서 온 `ToolAnnotations`만으로 tool 사용 결정을 내려서는 안 된다고 설명한다.
  근거: [MCP schema reference](https://modelcontextprotocol.io/specification/draft/schema)

## 직접 재현한 결과

- 직접 재현 없음: 이 글은 특정 MCP server를 연결해 실제 데이터 노출을 측정한 보고서가 아니다.
- 직접 확인한 범위: 2026-04-29 기준 MCP 공식 보안 문서와 OpenAI Agents SDK MCP 문서.

## 재현 순서

MCP 연결 전에는 아래 순서로 점검한다.

1. 서버 신뢰 경계를 정한다.

- 서버 운영 주체, source repository, 배포 위치, update 방식, package version pinning 여부를 확인한다.
- local stdio 서버인지 remote HTTP 서버인지 구분한다.

2. 노출되는 surface를 목록화한다.

```text
server: github-mcp
transport: stdio | streamable-http | hosted
tools: [list_issues, create_issue, read_file, write_file]
resources: [repo files, issues, pull requests]
prompts: [triage_prompt]
auth: OAuth | API key | local credential
logs: local file | hosted trace | vendor backend
```

3. tool 권한을 read/write/side effect로 나눈다.

- read: 조회, 검색, 목록
- write: comment, issue 생성, 파일 수정
- side effect: 배포, 결제, 권한 변경, 외부 전송

4. scope와 consent를 확인한다.

- 처음부터 `all`, `full-access`, `*` 같은 scope를 요청하지 않는다.
- 사용자가 어떤 client가 어떤 third-party scope를 요청하는지 볼 수 있어야 한다.
- redirect URI는 exact match로 검증해야 한다.

5. 데이터 경로를 확인한다.

- resource 내용이 model provider, trace backend, MCP server log, third-party API log 중 어디에 남는지 확인한다.
- secret, 개인정보, customer data, 내부 문서가 prompt나 tool output으로 이동하는지 본다.

6. network egress와 SSRF를 확인한다.

- remote MCP server 또는 server-side client가 내부 IP, cloud metadata, private service에 접근할 수 있는지 확인한다.
- redirect를 자동으로 따라가며 내부 주소로 이동하지 않도록 제한한다.

7. 연결 후 모니터링을 정한다.

- 실행된 tool, 요청 scope, 승인 기록, 실패한 호출, 차단된 URL, redaction 결과를 trace에 남긴다.

## 관찰 결과

- MCP는 "도구 하나 추가"가 아니라 agent와 외부 시스템 사이의 새 trust boundary를 만든다.
- 서버가 제공하는 tool 설명이나 annotation만 보고 안전하다고 판단하면 안 된다.
- scope가 넓고 resource 경계가 흐리면 prompt injection이나 잘못된 tool call이 데이터 유출로 이어질 수 있다.

## 해석 / 의견

내 판단으로는 MCP 연결의 첫 리뷰 단위는 tool 이름이 아니라 데이터 흐름이다. 어떤 데이터가 어느 서버를 지나 model context와 trace backend로 들어가는지 설명할 수 있어야 연결을 승인할 수 있다.

의견: 초기 연결은 read-only scope와 제한된 resource에서 시작하고, write 또는 side effect tool은 별도 approval과 audit log가 준비된 뒤 여는 편이 안전하다.

## 한계와 예외

- MCP 사양과 SDK 구현은 빠르게 변할 수 있으므로 실제 연결 시점의 버전과 host 정책을 다시 확인해야 한다.
- 이 글은 사전 점검 기준이며 특정 MCP server의 안전성을 보증하지 않는다.
- 조직별 데이터 분류, DLP, legal hold, retention 정책은 별도로 적용해야 한다.

## 참고자료

- [OpenAI Agents SDK MCP](https://openai.github.io/openai-agents-python/mcp/)
- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- [MCP Authorization](https://modelcontextprotocol.io/specification/draft/basic/authorization)
- [MCP Schema Reference](https://modelcontextprotocol.io/specification/draft/schema)
- [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: MCP 연결 전 데이터 surface, scope, consent, SSRF, logging 점검 기준 보강.
