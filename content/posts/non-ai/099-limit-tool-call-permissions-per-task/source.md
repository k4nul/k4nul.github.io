---
layout: single
title: "tool call 권한을 task 단위로 제한하기"
description: "tool call 권한을 task 단위로 제한하기에 대해 공식 문서와 운영 관점으로 확인할 기준, 점검 순서, 한계를 정리한 글."
date: 2026-07-07 09:00:00 +09:00
lang: ko
translation_key: limit-tool-call-permissions-per-task
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

agent에게 모든 tool을 항상 열어두면 작업 범위보다 권한이 커진다. task 단위 권한 제한은 "이번 작업에 필요한 tool만, 필요한 인자 범위로, 필요한 시간 동안" 허용하는 운영 방식이다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: analysis | tutorial
- 테스트 환경: 실행 테스트 없음. OpenAI Agents SDK, Codex 보안 문서, OWASP LLM06 기준으로 정리.
- 테스트 버전: 관련 공식 문서 2026-04-29 확인본. 로컬 agent runtime 버전은 고정하지 않음.
- 출처 등급: 공식 문서, 보안 프로젝트 문서

## 문제 정의

LLM agent의 위험은 모델 출력 자체보다 tool 권한에서 커진다. 문서 요약 작업에 shell, 파일 삭제, 배포, 외부 전송 tool까지 열려 있으면 prompt injection이나 잘못된 추론이 실제 변경으로 이어질 수 있다. 따라서 권한은 agent 전역이 아니라 task 범위로 줄여야 한다.

## 확인된 사실

- OpenAI Agents SDK 문서는 agent가 tool, guardrail, handoff를 조합해 동작한다고 설명한다.
  근거: [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- Agents SDK guardrail 문서는 function tool 호출 전후에 tool guardrail을 둘 수 있다고 설명한다.
  근거: [OpenAI Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- Codex 보안 문서는 sandbox와 approval을 통해 workspace 밖 파일 수정, 네트워크 접근, side effect가 있는 connector/tool call을 통제한다고 설명한다.
  근거: [Codex agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- OWASP LLM06 Excessive Agency는 과도한 기능, 권한, 자율성이 LLM application의 위험을 키운다고 설명한다.
  근거: [OWASP LLM06 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

## 직접 재현한 결과

- 직접 재현 없음: 이 글은 특정 agent framework에서 tool registry를 구현한 실험 보고서가 아니다.
- 직접 확인한 범위: 2026-04-29 기준 OpenAI와 OWASP 문서의 tool/guardrail/approval/permission 설명.

## 재현 순서

task 단위 tool 권한을 설계할 때는 작업을 먼저 분류한다.

| task 유형 | 기본 허용 tool | 기본 차단 tool | 승인 후보 |
| --- | --- | --- | --- |
| 문서 요약 | read, search | write, shell, network send | 민감 문서 열람 |
| 코드 리뷰 | read, diff, test readout | apply patch, deploy | 대량 파일 읽기 |
| 코드 수정 | read, apply patch, test | deploy, secret read | shell command |
| 배포 준비 | read, build, artifact inspect | production deploy | deploy, cloud write |
| 사고 조사 | read logs, search, trace | delete, rotate, external send | secret access, account disable |

실제 하네스 정책은 아래 순서로 만든다.

1. task intent를 선언한다: `summarize`, `review`, `edit`, `test`, `deploy`, `incident`.
2. tool allowlist를 만든다: task별 tool 이름과 인자 schema를 제한한다.
3. resource 범위를 제한한다: repository path, namespace, cloud project, ticket project, time window.
4. write와 side effect를 분리한다: read tool과 write/deploy/send tool을 같은 기본 권한에 넣지 않는다.
5. high-risk tool은 approval 뒤에 둔다: shell, network, secret, deployment, delete, payment, IAM 변경.
6. tool guardrail을 둔다: 경로 traversal, 외부 URL, secret-like 값, destructive command를 검사한다.
7. trace를 남긴다: 허용된 tool, 거절된 tool, 승인 요청, 실제 실행 결과를 기록한다.

예시는 다음과 같다.

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

## 관찰 결과

- 같은 agent라도 task가 다르면 필요한 tool 권한이 다르다.
- tool 이름만 제한하면 부족하다. `read_file`도 경로 범위가 넓으면 민감 파일을 읽을 수 있고, `http_request`도 destination 제한이 없으면 데이터 유출 경로가 될 수 있다.
- approval은 모든 tool call에 붙이는 것보다 high-risk boundary에 붙일 때 효과가 좋다.

## 해석 / 의견

내 판단으로는 "agent 권한"보다 "task 권한"이 운영 단위로 더 적절하다. 사용자가 요청한 작업이 문서 요약이면 요약 권한만, 코드 수정이면 수정 권한만 열어야 한다.

의견: task가 끝나면 tool 권한도 만료되어야 한다. 장기 session에 이전 task 권한이 남아 있으면 다음 작업에서 불필요한 권한이 재사용될 수 있다.

## 한계와 예외

- OpenAI Agents SDK, Codex, MCP host, 자체 orchestrator마다 tool 권한 모델이 다르다.
- hosted tool이나 built-in execution tool은 custom function tool과 guardrail 적용 지점이 다를 수 있다.
- 이 글은 설계 기준이며 실제 구현에서는 policy engine, audit log, identity provider, secret manager와 연동해야 한다.

## 참고자료

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [OWASP LLM06 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: task별 tool allowlist, resource scope, approval boundary, trace 기준 보강.
