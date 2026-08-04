---
layout: single
title: "AI 기능 출시 체크리스트: 모델·검색·UX·권한·운영을 한 번에 점검하기"
description: "모델·검색·UX·권한·운영의 증거, 담당자, 보류 조건을 함께 기록하는 AI 기능 출시 전 최소 체크리스트."
date: 2026-08-01
lang: ko
translation_key: ai-feature-release-checklist
section: development
topic_key: ai
categories: AI
tags: [ai, release, checklist, governance, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

이 문서는 “모델이 응답한다”는 사실만으로 AI 기능을 출시하지 않기 위한 최소 체크리스트다. 모델, retrieval, UX, authorization, operations의 각 항목에 증거·담당자·보류 조건을 남긴다. 모든 항목이 체크됐다고 안전성이나 법적 적합성이 보장되는 것은 아니다.

## Document Info / Environment

- 작성일·검증 기준일: 2026-08-02
- 문서 성격: 일반 출시 검토 템플릿. 특정 제품의 배포·성능·보안 감사를 수행하거나 주장하지 않는다.
- 적용 시에는 모델·공급자 문서와 조직 정책을 다시 확인한다.

## Problem Statement / 문제 정의

AI 기능은 모델 호출 하나가 아니라 입력, 검색, UI, 권한, 도구, 운영 대응이 연결된 워크플로다. 한 층만 통과해도 다른 층의 실패가 실제 사용자 피해나 데이터 노출로 이어질 수 있다.

## Verified Facts / 확인된 사실

- NIST AI RMF는 GOVERN, MAP, MEASURE, MANAGE로 위험 관리 활동을 구성하고, 맥락·한계·측정·대응을 문서화하도록 안내한다. [NIST AI RMF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- NIST AI 600-1은 생성형 AI의 정보 무결성, confabulation, 데이터 프라이버시 등 위험을 상황별로 관리할 것을 다룬다. [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- OWASP LLM Top 10은 prompt injection, 민감정보 노출, 과도한 권한을 포함한 LLM 애플리케이션 위험을 제시한다. [OWASP](https://genai.owasp.org/llm-top-10/)

## Reproduction Steps / 재현 순서

출시 책임자와 기능 소유자가 아래 표를 채운다. 각 행은 **증거 링크 또는 기록**, **담당자**, **미해결 시 보류/위험 수용 결정**이 있어야 통과다.

| 영역 | 최소 확인 항목 | 보류 조건 |
| --- | --- | --- |
| Model | 목적·비목적, 모델/버전, 비용·지연 한도, 알려진 실패와 fallback | 평가 범위 밖 고위험 사용 또는 응답 한도 미정 |
| Retrieval | 원본 문서 소유자·버전·폐기 상태, 권한 필터, Recall@k/근거 평가, 인용 검증 | 권한 밖 문서 노출 또는 정답 근거의 반복적 누락 |
| UX | 불확실성 표시, no-answer, 인용/원문 확인, 사용자 다음 행동, 신고 경로 | 근거 없는 단정이 정상 경로이거나 실패 시 사용자 행동이 없음 |
| Authorization | 입력 최소화, 테넌트/역할 필터, tool 최소 권한, 변경 작업 승인 | deny 테스트 실패, 비밀·개인정보가 불필요하게 문맥/로그에 들어감 |
| Operations | 로그 최소화·보존, 모니터링 지표, incident owner, 중단 권한, 롤백/비활성화 | 사건 담당자·중단 방법·재평가 기준이 없음 |

## Observations / 관찰 결과

이 표를 워크플로 단위로 채우면 “출시 준비됨” 대신 검증 가능한 질문이 남는다. 예를 들어 RAG 기능은 답변 자연스러움과 별개로 권한 필터, 근거 회수율, 인용 충실성을 보여야 한다. 실제 변경 tool은 모델의 설명 품질보다 승인·입력 검증·감사 가능성이 먼저다.

## Interpretation / 해석

내 해석으로 체크리스트의 목적은 모든 위험을 없애는 데 있지 않다. 범위, 남은 위험, 소유자, 중단 기준을 같은 기록에 남겨 제한적 출시·보류·명시적 위험 수용 중 어느 결정을 했는지 추적 가능하게 하는 데 있다.

## Limitations / 한계

- 이 체크리스트는 침투 테스트, 접근성 검토, 법률 자문, 분야별 안전 심사를 대체하지 않는다.
- 위험 허용 범위와 의무는 조직·도메인·관할에 따라 다르다.
- 항목 완료 후에도 모델 변화, 문서 변화, 운영 사건이 발생하면 재평가가 필요하다.

## References / 참고자료

- [NIST AI RMF 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)

## Change Log / 변경 이력

- 2026-08-02: Model·Retrieval·UX·Authorization·Operations별 최소 확인 항목과 보류 조건을 갖춘 내부 검토용 체크리스트로 확장. `published: false`.
