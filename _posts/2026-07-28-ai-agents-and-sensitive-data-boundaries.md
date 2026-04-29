---
layout: single
title: "AI agent와 개인정보/민감정보 경계"
description: "AI agent가 다루는 prompt, tool call, trace, MCP, memory, output에서 개인정보와 민감정보 경계를 설정하는 기준을 정리한다."
date: 2026-07-28 09:00:00 +09:00
lang: ko
translation_key: ai-agents-and-sensitive-data-boundaries
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

AI agent의 민감정보 경계는 모델 입력만의 문제가 아니다. prompt, 첨부 파일, retrieval 결과, tool call 인자와 응답, MCP 연결, trace, memory, 최종 출력까지 모두 데이터 경계에 포함된다.

기본 원칙은 "필요한 데이터만 넣고, 필요한 도구만 열고, 기록에는 민감정보가 들어갈 수 있음을 전제로 보존과 접근을 통제한다"이다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: tutorial | analysis
- 테스트 환경: 로컬 실행 테스트 없음. OpenAI Agents SDK, OpenAI Codex 보안 문서, OWASP LLM Top 10 문서를 기준으로 정리했다.
- 테스트 버전: 공식 문서 2026-04-29 확인. 제품 설정과 보존 정책은 조직 계약과 배포 방식에 따라 달라질 수 있다.
- 출처 성격: 공식 문서, 보안 프로젝트 문서

## 문제 정의

에이전트는 사용자의 한 문장만 처리하지 않는다. 작업을 수행하는 동안 저장소 파일을 읽고, 외부 문서를 요약하고, tool call을 실행하고, 실행 기록을 trace에 남길 수 있다. 그래서 개인정보와 민감정보 경계는 "모델에 보내도 되는가"보다 넓게 설계해야 한다.

경계가 없으면 비밀값이 trace에 남거나, 외부 콘텐츠가 내부 데이터와 섞이거나, 사람이 승인하지 않은 도구가 민감 데이터에 접근할 수 있다.

## 확인한 사실

- OpenAI Agents SDK tracing 문서는 LLM generation, function tool call, handoff, guardrail, custom event 같은 span을 기록하며, generation과 function span이 입력/출력을 저장할 수 있어 민감정보를 포함할 수 있다고 설명한다.
- OpenAI Codex 보안 문서는 prompt, tool arguments, tool outputs를 민감하게 취급하고 telemetry 보존과 접근 통제를 적용하라고 권고한다.
- OWASP LLM02:2025는 LLM 애플리케이션의 민감정보 노출을 주요 위험으로 다루며, tokenization과 redaction 같은 전처리 통제를 언급한다.
- OWASP LLM06:2025는 과도한 agent 권한이 피해 범위를 키울 수 있음을 다룬다.
- 이 글의 검증 기준일은 2026-04-29이다.

## 데이터 분류 기준

| 분류 | 예시 | 기본 처리 |
| --- | --- | --- |
| 공개 데이터 | 공개 문서, 공개 저장소, 공개 이슈 | 출처를 기록하고 외부 입력으로 표시 |
| 내부 데이터 | 비공개 설계 문서, 사내 위키 | 업무 필요 범위에서만 context에 포함 |
| 개인정보 | 이름, 이메일, 전화번호, 계정 식별자 | 최소화, 마스킹, 보존 기간 관리 |
| 민감정보 | API key, token, private key, secret, credential | prompt/tool/trace에 원문 포함 금지 |
| 규제 데이터 | 의료, 금융, 법적 기록 등 | 조직 정책과 계약 기준 없이는 agent 처리 금지 |

## 경계 설정 절차

1. agent 작업을 시작하기 전에 입력 데이터의 출처를 `사용자 제공`, `저장소`, `외부 웹`, `MCP`, `secret store`로 구분한다.
2. secret과 credential은 원문을 prompt에 넣지 않는다. 필요하면 별도 secret manager나 제한된 tool이 간접 사용하도록 한다.
3. 외부 콘텐츠는 내부 지시문과 분리하고, 외부 문서의 명령문을 agent 지시로 취급하지 않는다.
4. tool call 권한은 작업 단위로 제한한다. 읽기, 쓰기, 네트워크, 결제, 배포, 삭제 권한을 분리한다.
5. high-risk action은 사람 승인 없이 실행하지 않는다. 예: prod 데이터 조회, 외부 전송, 배포, 권한 변경, 대량 삭제.
6. trace와 로그에는 prompt, tool arguments, tool outputs가 들어갈 수 있음을 전제로 redaction, retention, 접근 통제를 적용한다.
7. 결과물에는 개인정보나 내부 비밀이 섞이지 않았는지 출력 검증을 둔다.
8. 사고가 의심되면 어떤 입력, 어떤 tool, 어떤 trace, 어떤 승인으로 데이터가 이동했는지 timeline을 복원한다.

## 운영 판단

민감정보를 "모델이 기억하지 않으면 괜찮다"로 판단하면 부족하다. 실무에서는 model input보다 agent harness의 기록, tool output, connector 권한, 운영자 접근 권한이 더 자주 문제가 된다.

가장 안전한 구조는 raw secret을 agent context 밖에 두고, agent는 제한된 capability를 가진 도구만 호출하게 만드는 방식이다. 예를 들어 "배포 토큰을 알려줘"가 아니라 "승인된 배포 도구를 dry-run으로 실행해줘"처럼 권한을 기능 단위로 감싼다.

## 점검 질문

- 이 작업에 원문 개인정보가 꼭 필요한가, 아니면 마스킹된 식별자로 충분한가?
- trace와 로그를 누가 볼 수 있고, 얼마 동안 보존되는가?
- MCP나 외부 도구가 어떤 데이터에 접근할 수 있는가?
- 외부 콘텐츠가 내부 지시문처럼 실행될 가능성이 있는가?
- 사람 승인 없이 외부 전송, 삭제, 권한 변경, 배포가 가능한가?

## 한계와 예외

- 이 글은 법률 자문이나 조직의 개인정보 처리방침을 대체하지 않는다.
- 개인정보 처리 근거, 국외 이전, 보존 기간, 데이터 처리 계약은 조직별로 별도 검토가 필요하다.
- 제품별 데이터 사용 정책은 계약, API, 엔터프라이즈 설정, 지역 설정에 따라 달라질 수 있다.

## 참고자료

- [OpenAI Agents SDK: Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Codex: Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [OWASP LLM02:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
- [OWASP LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: 개인정보/민감정보 분류, trace와 tool call 경계, 운영 점검 질문을 보강.
