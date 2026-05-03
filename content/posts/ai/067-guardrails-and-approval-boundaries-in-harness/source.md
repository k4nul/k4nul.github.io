---
layout: single
title: "하네스 관점의 guardrail과 approval 경계"
description: "하네스 관점의 guardrail과 approval 경계에 대해 공식 문서와 운영 관점으로 확인할 기준, 점검 순서, 한계를 정리한 글."
date: 2026-06-23 09:00:00 +09:00
lang: ko
translation_key: guardrails-and-approval-boundaries-in-harness
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

하네스 관점에서 guardrail과 approval은 같은 통제가 아니다. guardrail은 입력, 출력, tool call을 자동으로 검사해 허용·거절·차단하는 규칙이고, approval은 권한이 큰 작업을 실행하기 전에 사람이나 정책이 실행 여부를 결정하는 경계다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: analysis | tutorial
- 테스트 환경: 실행 테스트 없음. OpenAI Agents SDK guardrails 문서와 Codex approval/sandbox 문서 기준으로 정리.
- 테스트 버전: OpenAI Agents SDK와 Codex 문서 2026-04-29 확인본. 로컬 runtime 버전은 고정하지 않음.
- 출처 등급: 공식 문서, 보안 프로젝트 문서

## 문제 정의

"guardrail이 있으니 approval은 필요 없다" 또는 "approval을 받으니 guardrail은 없어도 된다"는 식의 설계는 위험하다. guardrail은 반복적이고 기계적인 검사를 잘하지만, 조직의 책임과 권한 위임을 대신하지 않는다. approval은 고위험 작업의 책임 경계를 만들지만, 모든 입력과 출력의 안전성을 자동으로 검증하지 않는다.

이 글은 agent harness에서 두 경계를 어디에 놓을지 정리한다.

## 확인된 사실

- OpenAI Agents SDK 문서는 input guardrail, output guardrail, tool guardrail을 별도 실행 지점으로 설명한다.
  근거: [OpenAI Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- Agents SDK 문서 기준으로 tool guardrail은 custom function tool 호출 전후에 실행되며, handoff나 hosted/built-in tool에는 같은 방식으로 적용되지 않는다.
  근거: [OpenAI Agents SDK Tool guardrails](https://openai.github.io/openai-agents-python/guardrails/#tool-guardrails)
- Codex 문서는 workspace 밖 파일 수정, 네트워크 접근, side effect가 있는 app/connector tool call을 approval 경계로 설명한다.
  근거: [Codex agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- OWASP LLM01은 prompt injection 완화책으로 최소 권한, human approval, 외부 콘텐츠 분리, 입력/출력 필터링을 함께 제시한다.
  근거: [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

## 직접 재현한 결과

- 직접 재현 없음: 이 글은 특정 agent framework의 guardrail 함수를 실행한 테스트가 아니다.
- 직접 확인한 범위: 2026-04-29 기준 공식 문서의 guardrail, approval, sandbox 설명.

## 재현 순서

하네스 정책을 설계할 때는 작업을 먼저 네 가지로 분류한다.

1. 읽기 작업: 파일 읽기, 검색, issue 조회, 로그 조회
2. 쓰기 작업: 파일 수정, config 변경, PR comment, ticket 상태 변경
3. 실행 작업: shell command, build/test, code execution, migration
4. 외부 영향 작업: network call, 배포, secret 접근, cloud/IAM 변경, destructive operation

그다음 guardrail과 approval을 다른 위치에 둔다.

| 단계 | guardrail 예시 | approval 예시 |
| --- | --- | --- |
| 입력 전 | secret, 개인정보, 외부 prompt injection 패턴 감지 | 고위험 작업 요청인지 사람이 확인 |
| tool 실행 전 | tool 인자 schema, 허용 resource, 경로 allowlist 검사 | workspace 밖 쓰기, network, 배포 승인 |
| tool 실행 후 | 출력 redaction, secret 포함 여부 검사 | 예상보다 큰 변경량이면 추가 승인 |
| 최종 출력 전 | 근거 없는 단정, 민감정보 노출 검사 | 사고 보고서, 정책 변경안 최종 승인 |

예시 정책은 이렇게 쓸 수 있다.

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

## 관찰 결과

- guardrail은 자동화된 판정이므로 빠르고 반복 가능하지만, 잘못 설계하면 false positive와 false negative가 생긴다.
- approval은 책임과 맥락을 확인할 수 있지만, 모든 작업을 approval로 돌리면 운영이 느려지고 사용자가 습관적으로 승인할 수 있다.
- 좋은 하네스는 guardrail로 명백한 위험을 줄이고, approval로 권한과 책임이 큰 작업을 멈춰 세운다.

## 해석 / 의견

내 판단으로는 guardrail은 "이 입력이나 tool call이 정책에 맞는가"를 묻고, approval은 "이 권한을 지금 사용해도 되는가"를 묻는다. 두 질문을 분리해야 사고가 났을 때 자동 차단 실패인지, 승인 판단 실패인지, 권한 설계 실패인지 구분할 수 있다.

의견: 기본 정책은 낮은 위험의 반복 작업은 guardrail 중심으로 처리하고, irreversible change와 외부 영향 작업은 approval을 요구하는 방식이 적절하다.

## 한계와 예외

- 제품별 guardrail과 approval 구현은 다르다. 특히 hosted tool, built-in execution tool, MCP connector는 framework별 제한을 확인해야 한다.
- approval은 보안 통제가 아니라 운영 통제에 가깝다. 승인자가 내용을 이해하지 못하면 통제 효과가 낮다.
- 이 글은 일반 harness 설계 기준이며 특정 조직의 법무, 개인정보, 감사 요구사항을 대신하지 않는다.

## 참고자료

- [OpenAI Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: guardrail과 approval의 실행 지점, 차이, 정책 예시 보강.
