---
layout: single
title: "AI coding agent 보안 위협 모델 입문"
description: "AI coding agent 보안 위협 모델 입문에 대해 공식 문서와 운영 관점으로 확인할 기준, 점검 순서, 한계를 정리한 글."
date: 2026-07-21 09:00:00 +09:00
lang: ko
translation_key: threat-modeling-ai-coding-agents
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

AI coding agent의 위협 모델은 "모델이 틀린 코드를 만들 수 있다"에서 끝나지 않는다. 저장소 입력, 외부 콘텐츠, tool 권한, secret, sandbox, approval, trace, 배포 경계가 함께 봐야 할 공격면이다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: analysis | tutorial
- 테스트 환경: 실행 테스트 없음. OpenAI Codex/Agents SDK 문서와 OWASP LLM 위험 분류 기준으로 구조 정리.
- 테스트 버전: 관련 공식 문서 2026-04-29 확인본. 특정 agent runtime 버전은 고정하지 않음.
- 출처 등급: 공식 문서, 보안 프로젝트 문서, NIST 문서

## 문제 정의

coding agent는 코드 읽기, 패치 생성, 테스트 실행, shell command, issue/PR 작업, MCP connector, 배포 준비까지 수행할 수 있다. 그래서 전통적인 웹 앱 위협 모델처럼 네트워크 endpoint만 보는 방식으로는 부족하다. agent가 읽는 데이터와 실행할 수 있는 tool 사이에서 권한과 신뢰 경계를 다시 그려야 한다.

## 확인된 사실

- Codex 보안 문서는 task가 sandbox에서 실행되며, approval과 network/file-system 경계가 보안 통제의 일부라고 설명한다.
  근거: [OpenAI Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- OpenAI Agents SDK tracing 문서는 LLM generation, tool call, handoff, guardrail 같은 agent 실행 단위를 trace로 남길 수 있다고 설명한다.
  근거: [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)
- OWASP LLM01은 prompt injection이 모델의 동작이나 출력을 의도치 않게 바꾸는 위험이라고 설명한다.
  근거: [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- OWASP LLM02는 민감정보가 LLM 출력이나 관련 시스템을 통해 노출될 수 있는 위험을 다룬다.
  근거: [OWASP LLM02 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
- OWASP LLM06은 과도한 기능, 권한, 자율성이 damaging action으로 이어질 수 있다고 설명한다.
  근거: [OWASP LLM06 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- NIST AI RMF Generative AI Profile은 생성형 AI 위험을 govern, map, measure, manage 활동으로 다루는 기준을 제공한다.
  근거: [NIST AI RMF Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)

## 직접 재현한 결과

- 직접 재현 없음: 이 글은 특정 coding agent를 공격한 penetration test 보고서가 아니다.
- 직접 확인한 범위: 2026-04-29 기준 OpenAI, OWASP, NIST 공식 자료의 통제 항목.

## 재현 순서

coding agent 위협 모델은 아래 자산과 경계를 먼저 적는다.

| 영역 | 질문 | 대표 위험 |
| --- | --- | --- |
| 입력 | agent가 읽는 데이터는 신뢰할 수 있는가 | prompt injection, poisoned issue, malicious README |
| 권한 | 어떤 tool과 credential을 쓸 수 있는가 | excessive agency, secret access, destructive command |
| 실행 | 어디서 command와 test가 실행되는가 | sandbox escape, persistence, network egress |
| 변경 | 어떤 파일과 branch를 수정할 수 있는가 | unauthorized patch, workflow tampering |
| 외부 연결 | GitHub, cloud, MCP, package registry에 연결되는가 | data exfiltration, connector side effect |
| 기록 | 무엇을 trace와 log로 남기는가 | missing audit trail, sensitive trace storage |

초기 threat modeling 절차는 다음과 같다.

1. task 유형을 나눈다: 질문 답변, 코드 리뷰, 코드 수정, 테스트 실행, 배포 준비, 사고 대응.
2. 입력 출처를 분류한다: 사용자 요청, 저장소 파일, issue/PR comment, web result, MCP resource, memory.
3. tool 권한을 task별로 제한한다: 읽기, 쓰기, shell, network, secret, deploy를 분리한다.
4. high-risk action을 approval 뒤에 둔다: workspace 밖 쓰기, 외부 전송, 배포, secret 접근, IAM 변경.
5. sandbox와 network 기본값을 정한다: 기본 차단, 필요 시 승인, allowlist 기반 허용.
6. trace 필드를 정한다: input source, tool call, approval, guardrail, verification, failure.
7. abuse case를 테스트한다: malicious README, PR title injection, compromised dependency, secret exfiltration, test command manipulation.

## 관찰 결과

- coding agent 보안은 모델 품질보다 운영 경계에 더 크게 의존한다.
- 같은 prompt injection이라도 읽기 전용 agent와 배포 권한 agent의 피해 범위는 다르다.
- 위협 모델은 "agent가 무엇을 할 수 있는가"보다 "이번 task에서 무엇을 할 수 있어야 하는가"로 좁혀야 실무에 맞다.

## 해석 / 의견

내 판단으로는 AI coding agent의 핵심 위협은 자연어 입력이 실행 권한으로 이어지는 순간에 생긴다. 그래서 prompt, tool, sandbox, approval, trace를 별개 항목이 아니라 하나의 harness 경계로 설계해야 한다.

의견: 첫 위협 모델은 완벽한 diagram보다 작은 abuse case 5개를 실제 운영 정책에 매핑하는 방식이 더 유용하다.

## 한계와 예외

- agent 제품별 sandbox, approval, network, MCP 동작은 다르므로 실제 사용 제품 문서를 다시 확인해야 한다.
- 이 글은 위협 모델 입문이며 특정 취약점 exploitability를 측정하지 않았다.
- 조직별 법무, 개인정보, 내부 보안 정책은 별도 요구사항으로 추가해야 한다.

## 참고자료

- [OpenAI Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Agents SDK Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [OWASP LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OWASP LLM02 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/)
- [OWASP LLM06 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)
- [NIST AI RMF Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: AI coding agent 자산, 신뢰 경계, abuse case, 공식 근거 보강.
