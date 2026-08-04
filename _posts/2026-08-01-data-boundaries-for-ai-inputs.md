---
layout: single
title: "AI 입력을 위한 데이터 경계 설정"
description: "AI에 전달할 데이터와 전달하지 않을 데이터를 출처, 목적, 권한, 보관 경계로 구분하는 방법을 다룬다."
date: 2026-08-01
lang: ko
translation_key: data-boundaries-for-ai-inputs
section: development
topic_key: ai
categories: AI
tags: [ai, data-governance, privacy, security]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

AI 입력 경계는 ‘민감한 데이터는 조심한다’는 문구보다 구체적이어야 한다. 어떤 데이터가 어떤 목적에 필요한지, 누가 접근할 수 있는지, 모델 호출에 실제로 어떤 부분이 전달되는지 정해야 한다. 최소한의 필요한 문맥만 전달하고, 전달할 수 없는 데이터와 예외 처리 경로를 명시하면 설계와 검토의 기준이 생긴다.

## Document Info / Environment

이 문서는 2026-08-01 기준의 일반 데이터 경계 설계 초안이다. 특정 데이터셋, 계정, 저장소, 고객 정보를 열람하거나 시험하지 않았다. 법률 자문이나 개인정보 처리 적합성 판단도 제공하지 않는다.

## Problem Statement / 문제 정의

AI 기능은 사용자의 질문, 첨부 문서, 검색 결과, 대화 이력을 한 입력으로 묶기 쉽다. 하지만 데이터마다 소유자, 목적, 보관 기간, 접근 권한이 다를 수 있다. 입력 경계가 없으면 필요한 정보보다 넓은 범위를 전달하거나, 권한이 다른 문서를 같은 답변 문맥에 섞을 위험이 생긴다.

## Verified Facts / 확인된 사실

NIST AI RMF 1.0은 MAP에서 AI 시스템의 맥락, 데이터, 이해관계자와 영향을 식별하도록 제시한다. NIST AI 600-1은 생성형 AI의 데이터 출처, 품질, 프라이버시 관련 위험을 맥락에 맞게 문서화하고 관리할 것을 제안한다. OWASP Top 10 for LLM Applications는 민감 정보 노출을 LLM 애플리케이션의 위험 범주로 다룬다.

## Reproduction Steps / 재현 순서

입력 후보마다 출처, 소유자, 사용 목적, 분류, 접근 조건, 허용 기간을 기록한다. 이어서 기능별로 반드시 필요한 필드만 선택하고, 원문 대신 요약·식별자·권한 필터 결과로 충분한지 검토한다. 사용자 입력과 검색 문서는 신뢰 수준이 다르므로 분리하여 처리하고, 경계 밖 데이터가 필요하다는 요청에는 중단 또는 별도 승인 경로를 둔다.

## Observations / 관찰 결과

이 기록을 만들면 ‘모든 문서를 AI에 연결한다’는 요구가 데이터 흐름 단위의 질문으로 바뀐다. 어떤 문서는 검색 대상이 될 수 있어도 모델 문맥에는 들어가지 않을 수 있고, 어떤 결과는 사용자에게 표시되기 전에 권한 필터를 통과해야 한다. 경계는 모델 호출 전과 출력 후 모두에 필요하다.

## Interpretation / 해석

데이터 최소화는 기능을 약하게 만드는 규칙이 아니라 목적에 맞는 입력을 선택하는 설계 방법이다. 모델이 더 많은 문맥을 받는다고 항상 더 좋은 결과를 내는 것은 아니며, 관련 없는 정보는 오류와 노출 범위도 넓힐 수 있다. 명시적 경계는 데이터 소유자와 제품팀이 가정을 함께 검토하게 한다.

## Limitations / 한계

분류표만으로 모든 민감성이나 재식별 위험을 판단할 수는 없다. 국가, 산업, 계약, 조직 정책에 따른 요구는 별도로 확인해야 한다. 이 글은 어떤 처리 방식의 법적 적합성이나 보안성을 보장하지 않으며, 실제 설계에는 보안·프라이버시 담당자의 검토가 필요하다.

## References / 참고자료

- [NIST AI RMF 1.0 (NIST AI 100-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
## Change Log / 변경 이력

2026-08-01: 내부 검토용 초안 작성. 게시 일정과 제공 상태는 확정하지 않았다.
