---
layout: single
title: "AI agent incident review 템플릿"
description: "AI agent 사고 리뷰에서 timeline, tool call, approval, guardrail, trace, 데이터 노출, 재발 방지 항목을 빠뜨리지 않기 위한 템플릿."
date: 2026-08-04 09:00:00 +09:00
lang: ko
translation_key: ai-agent-incident-review-template
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

AI agent incident review는 일반 장애 리뷰에 agent-specific 증거를 추가해야 한다. 어떤 입력이 들어왔는지, 어떤 모델과 harness 설정으로 실행됐는지, 어떤 tool call이 일어났는지, 어떤 approval과 guardrail이 있었는지, trace에 무엇이 남았는지를 함께 봐야 한다.

아래 템플릿은 책임 추궁보다 재현 가능한 사실 정리와 재발 방지를 목표로 한다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: tutorial | analysis
- 테스트 환경: 로컬 실행 테스트 없음. NIST incident response 문서, CISA playbook, OpenAI agent trace/approval 문서를 기준으로 템플릿을 구성했다.
- 테스트 버전: 공식 문서 2026-04-29 확인. 조직의 사고 등급 체계와 법적 보고 기준은 별도 적용해야 한다.
- 출처 성격: 공식 문서, 보안 프로젝트 문서

## 확인한 사실

- NIST SP 800-61 Rev. 3는 incident response를 cybersecurity risk management 활동과 연결해 준비, 탐지, 대응, 복구의 효과를 높이는 관점으로 설명한다.
- CISA incident and vulnerability response playbooks는 표준화된 운영 절차와 조율된 대응을 강조한다.
- OpenAI Agents SDK tracing 문서는 LLM generation, tool call, handoff, guardrail, custom event가 trace에 포함될 수 있다고 설명한다.
- OpenAI Codex 보안 문서는 prompt, tool arguments, tool outputs를 민감하게 취급하고 보존과 접근 통제를 적용하라고 권고한다.
- 이 글의 검증 기준일은 2026-04-29이다.

## 템플릿

### 1. Incident Summary

- Incident ID:
- 작성일:
- 작성자:
- 심각도:
- 현재 상태: investigating | contained | recovered | closed
- 한 줄 요약:
- 영향 범위:
- 최초 발견 시각:
- 종료 또는 복구 시각:

### 2. Scope and Impact

- 영향을 받은 repository, service, workspace, cloud account, cluster:
- 영향을 받은 사용자 또는 팀:
- 데이터 노출 가능성: 없음 | 가능성 있음 | 확인됨 | 조사 중
- 외부 전송 여부:
- production 변경 여부:
- 비용, 가용성, 보안 영향:

### 3. Agent Task Context

- 사용자 요청 원문 또는 요약:
- task 목적:
- agent/harness 이름:
- model 이름과 버전:
- 실행 위치: local | CI | cloud sandbox | IDE | desktop
- sandbox 모드:
- network access:
- 허용된 tool 목록:
- 연결된 MCP/server/connector:
- 사용된 system/developer instruction 버전:

### 4. Timeline

| 시각 | 이벤트 | 근거 |
| --- | --- | --- |
| HH:MM | 사용자 요청 수신 | chat/session 기록 |
| HH:MM | 첫 tool call 실행 | trace 또는 audit log |
| HH:MM | guardrail/approval 발생 | approval 기록 |
| HH:MM | 이상 징후 탐지 | alert 또는 사용자 신고 |
| HH:MM | containment 조치 | 변경 기록 |
| HH:MM | 복구 확인 | 검증 명령 또는 모니터링 |

타임라인은 추정과 확인을 분리한다. 확인되지 않은 항목에는 `추정` 표시를 붙인다.

### 5. Tool Calls and Side Effects

- 실행된 tool call 목록:
- 읽은 파일과 디렉터리:
- 수정한 파일:
- 실행한 shell command:
- 외부 네트워크 요청:
- cloud/API 호출:
- 배포, 삭제, 권한 변경, 결제 같은 side effect:
- 실패하거나 차단된 tool call:

### 6. Approvals and Guardrails

- 승인 요청이 발생한 시점:
- 승인자:
- 승인 문구와 실제 실행 내용의 차이:
- 자동 승인 또는 사전 승인 정책:
- guardrail tripwire 발생 여부:
- 입력 검증, 출력 검증, tool-call 검증 결과:
- 승인 없이 실행된 high-risk action:

### 7. Trace, Log, and Data Review

- trace ID 또는 session ID:
- trace에 prompt, tool arguments, tool outputs가 포함됐는가:
- 민감정보 또는 개인정보 포함 여부:
- redaction 적용 여부:
- 로그/trace 접근 권한:
- 보존 기간:
- 외부 collector 또는 telemetry endpoint:

### 8. Root Cause and Contributing Factors

- 직접 원인:
- 기여 요인:
- 누락된 guardrail:
- 과도한 tool 권한:
- 불충분한 approval 경계:
- 외부 콘텐츠 또는 prompt injection 가능성:
- 테스트 또는 문서 부족:

### 9. Containment, Recovery, Verification

- containment 조치:
- credential rotation:
- 권한 회수:
- 배포 rollback:
- 데이터 삭제 또는 회수 요청:
- 복구 검증 방법:
- 재발 여부 모니터링:

### 10. Follow-up Actions

| 조치 | 담당자 | 기한 | 상태 |
| --- | --- | --- | --- |
| tool permission 축소 |  |  | open |
| high-risk approval 정책 추가 |  |  | open |
| trace redaction 적용 |  |  | open |
| 재현 테스트 추가 |  |  | open |
| runbook 업데이트 |  |  | open |

## 작성 원칙

사고 리뷰에는 원문 비밀값을 붙이지 않는다. 필요한 경우 redacted hash, secret ID, rotation ticket, trace ID처럼 재확인 가능한 대체 식별자를 쓴다.

"agent가 실수했다"는 결론은 원인 분석이 아니다. 어떤 입력, 권한, guardrail, approval, trace 설계가 그 행동을 가능하게 했는지까지 적어야 다음 설계가 좋아진다.

## 한계와 예외

- 이 템플릿은 법적 보고, 개인정보 침해 신고, 고객 공지 절차를 대체하지 않는다.
- 조직의 incident severity, evidence retention, legal hold 정책이 있으면 그 정책이 우선한다.
- 민감정보가 포함된 trace는 보존보다 격리와 접근 통제가 먼저다.

## 참고자료

- [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
- [CISA Federal Government Cybersecurity Incident and Vulnerability Response Playbooks](https://www.cisa.gov/resources-tools/resources/federal-government-cybersecurity-incident-and-vulnerability-response-playbooks)
- [OpenAI Agents SDK: Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Codex: Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [OWASP GenAI Security Project](https://genai.owasp.org/)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: agent incident review에 필요한 timeline, tool call, approval, guardrail, trace, 데이터 검토 항목을 템플릿으로 보강.
