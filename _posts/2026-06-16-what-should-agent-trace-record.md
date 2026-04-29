---
layout: single
title: "에이전트 trace에는 무엇을 남겨야 하는가"
description: "에이전트 trace에는 무엇을 남겨야 하는가에 대해 공식 문서와 운영 관점으로 확인할 기준, 점검 순서, 한계를 정리한 글."
date: 2026-06-16 09:00:00 +09:00
lang: ko
translation_key: what-should-agent-trace-record
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

agent trace는 대화 전문을 그대로 저장하는 공간이 아니라, 나중에 "무엇을 근거로 어떤 권한을 사용했는가"를 확인하기 위한 운영 기록이다. 최소한 실행 단위, 모델 호출, tool call, handoff, guardrail 결과, 승인 여부, 오류와 검증 결과를 연결해서 남겨야 한다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: analysis | tutorial
- 테스트 환경: 실행 테스트 없음. OpenAI Agents SDK와 Codex 보안 문서를 기준으로 trace 설계 항목을 정리.
- 테스트 버전: OpenAI Agents SDK 문서와 Codex 문서 2026-04-29 확인본. 로컬 SDK 버전은 고정하지 않음.
- 출처 등급: 공식 문서, 보안 프로젝트 문서

## 문제 정의

agent trace를 "로그를 많이 남기는 것"으로만 이해하면 두 가지 문제가 생긴다. 첫째, 사고 분석에 필요한 decision path는 빠지고 원문 prompt와 출력만 과하게 남을 수 있다. 둘째, 민감정보가 trace backend로 이동하면서 새로운 노출면이 생길 수 있다.

이 글은 agent trace에 남겨야 할 최소 항목과 남기면 위험한 항목을 분리한다.

## 확인된 사실

- OpenAI Agents SDK tracing 문서는 agent run 중 LLM generation, tool call, handoff, guardrail, custom event를 기록 대상으로 설명한다.
  근거: [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)
- 같은 문서는 trace가 workflow 단위이고, span에는 시작/종료 시각, trace id, parent id, span data가 포함된다고 설명한다.
  근거: [OpenAI Agents SDK Traces and spans](https://openai.github.io/openai-agents-python/tracing/#traces-and-spans)
- tracing은 LLM generation과 function call의 입력/출력을 포함할 수 있으므로 민감정보 포함 여부를 설정해야 한다.
  근거: [OpenAI Agents SDK Sensitive data](https://openai.github.io/openai-agents-python/tracing/#sensitive-data)
- Codex 문서는 sandbox와 approval을 분리해 설명하며, workspace 밖 파일 수정, 네트워크 접근, side effect가 있는 connector/tool call은 승인 경계가 될 수 있다고 설명한다.
  근거: [Codex agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)

## 직접 재현한 결과

- 직접 재현 없음: 이 글은 특정 agent runtime을 실행해 trace payload를 수집한 실험 보고서가 아니다.
- 직접 확인한 범위: 2026-04-29 기준 공식 문서에서 trace와 approval이 어떤 운영 항목을 제공하는지 확인했다.

## 재현 순서

trace schema를 설계할 때는 아래 순서로 점검한다.

1. 실행 단위를 정한다: `trace_id`, `workflow_name`, `group_id`, 요청자, 저장소/프로젝트, 작업 id.
2. 입력 출처를 기록한다: 사용자 입력, 파일, 웹 검색, MCP/resource, 이전 memory 중 어디서 온 데이터인지 구분한다.
3. 모델 호출을 기록한다: model 이름, generation span, token/usage가 필요한 경우의 집계값, 실패한 호출과 재시도 여부.
4. tool call을 기록한다: tool 이름, 인자 요약, 대상 리소스, 권한 범위, 실행 전 승인 필요 여부, 결과 요약.
5. handoff를 기록한다: 넘긴 agent, 넘긴 이유, 전달된 context 범위, 제거한 context가 있으면 그 이유.
6. guardrail 결과를 기록한다: input/output/tool guardrail 이름, 통과/차단/tripwire 여부, 차단 사유.
7. approval을 기록한다: 승인 요청 사유, 승인자 또는 승인 정책, 승인/거절/timeout 결과, 승인 후 실제 실행 여부.
8. 검증 결과를 기록한다: 실행한 테스트, 실패한 검증, 사람이 확인해야 할 남은 위험.
9. 민감정보 정책을 기록한다: 원문 저장 여부, redaction 방식, trace 보존 기간, 외부 trace processor 전송 여부.

민감한 값은 원문보다 분류와 해시, 길이, 리소스 id처럼 재현에 필요한 최소값으로 남긴다.

```text
trace_id: trace_...
workflow_name: "repository maintenance"
input_source: user_request | file | web | mcp | memory
tool_call: { name, target, permission_scope, approved, result_summary }
guardrail: { name, stage, outcome, reason }
verification: { ran, failed, not_run, reason }
sensitive_data: { raw_input_saved: false, redaction: "token/value redacted" }
```

## 관찰 결과

- trace에 원문 prompt와 출력만 남기면 "왜 그 tool을 실행했는가"를 나중에 설명하기 어렵다.
- 반대로 모든 원문 입력과 tool output을 저장하면 debugging은 쉬워지지만 개인정보, secret, 내부 문서가 trace 저장소로 옮겨갈 수 있다.
- 운영에 필요한 trace는 결과보다 경계가 중요하다. 어떤 권한이 있었고, 어떤 guardrail이 작동했고, 어떤 승인이 있었는지가 사고 분석의 핵심 단서가 된다.

## 해석 / 의견

내 판단으로는 agent trace의 목적은 "모델의 생각을 보관"하는 것이 아니라 "운영 가능한 책임 사슬을 남기는 것"이다. 따라서 trace에는 자연어 대화보다 실행 단위, 권한, tool call, guardrail, approval, 검증 결과가 더 안정적으로 남아야 한다.

의견: 기본값은 원문 최소 저장이어야 한다. 문제가 생긴 뒤 원문이 필요하다는 이유로 모든 입력을 항상 저장하면 trace가 새로운 데이터 유출 경로가 된다.

## 한계와 예외

- 조직의 감사 요구사항, 개인정보 처리 방침, 보존 기간 정책은 이 글의 범위를 벗어난다.
- OpenAI Agents SDK와 Codex의 tracing/approval 동작은 버전에 따라 달라질 수 있다.
- 실제 trace backend, SIEM, APM, DLP 연동은 제품별 데이터 모델을 따로 확인해야 한다.

## 참고자료

- [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [OpenAI Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: trace 기록 항목, 민감정보 경계, 공식 문서 근거 보강.
