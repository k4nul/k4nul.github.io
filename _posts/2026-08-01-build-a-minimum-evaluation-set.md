---
layout: single
title: "최소 AI 평가 세트 만들기"
description: "실제 사용 사례와 실패 사례를 포함한 작은 평가 세트로 AI 기능의 변화를 비교하는 방법을 설명한다."
date: 2026-08-01
lang: ko
translation_key: build-a-minimum-evaluation-set
section: development
topic_key: ai
categories: AI
tags: [ai, evaluation, testing, risk-management]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

AI 평가 세트는 거대한 벤치마크가 시작점일 필요가 없다. 실제 사용자가 하는 질문, 반드시 지켜야 할 제약, 답하지 말아야 할 요청을 소수라도 명시하면 변경 전후를 비교할 수 있다. 최소 세트의 목적은 모델의 절대적 능력을 선언하는 것이 아니라, 기능의 의도와 위험에 맞는 반복 가능한 검토 기준을 만드는 데 있다.

## Document Info / Environment

이 문서는 2026-08-01 기준의 평가 설계 초안이다. 특정 모델이나 데이터셋을 실행·채점하지 않았으며, 여기의 예시는 성능 수치나 제품 결과를 주장하지 않는다.

## Problem Statement / 문제 정의

프롬프트, 검색, 모델, 도구를 바꾸면 답변이 ‘더 좋아 보일’ 수 있지만 무엇이 좋아졌는지 알기 어렵다. 정상 질문만 모으면 근거 부족, 애매한 요청, 권한 밖 정보 같은 중요한 실패를 놓친다. 평가 기준이 없으면 릴리스 뒤의 불만이 사실상 첫 번째 테스트가 된다.

## Verified Facts / 확인된 사실

NIST AI RMF 1.0은 MAP에서 식별된 중요한 위험부터 측정 방법과 지표를 선택하고, 측정하지 못하는 특성도 문서화하도록 제시한다. 또한 배포 환경과 유사한 조건에서 성능 또는 보증 기준을 측정하도록 설명한다. NIST AI 600-1은 생성형 AI의 평가와 지속적 모니터링을 위험 관리의 맥락에서 다룬다.

## Reproduction Steps / 재현 순서

먼저 기능 목적을 대표하는 실제 질문을 모으고, 각 질문에 허용되는 근거와 기대 행동을 적는다. 그 다음 사실상 답이 없는 질문, 상충하는 문서, 모호한 표현, 거절 또는 사람 연결이 필요한 요청을 추가한다. 각 항목에는 통과 기준, 검토자, 결과 기록 형식을 붙이고, 변경할 때 같은 세트를 다시 실행해 차이를 검토한다.

## Observations / 관찰 결과

작은 세트도 문제를 분리하는 데 도움이 된다. 검색 근거가 없는데 답하면 검색·정책 문제이고, 근거가 있는데 왜곡하면 생성·표시 문제일 수 있다. 단일 점수보다 항목별 실패 이유를 기록하면 다음 개선의 우선순위를 정하기 쉽다.

## Interpretation / 해석

평가는 한 번의 출시에 붙는 인증 도장이 아니라 제품 가정을 계속 확인하는 루프다. 최소 세트는 완전한 현실을 대표하지 않지만, 팀이 어떤 실패를 중요하게 보며 어떤 한계를 수용하지 않는지 드러낸다. 표본과 기준은 사용 사례 변화에 맞춰 갱신되어야 한다.

## Limitations / 한계

작은 세트는 드문 사례, 장기적 영향, 다양한 사용자 경험을 포괄하지 못한다. 사람이 작성한 기대 답도 오류나 편향을 가질 수 있다. 평가 결과는 특정 조건의 증거일 뿐 일반적 안전성, 정확성, 법적 적합성을 보장하지 않는다.

## References / 참고자료

- [NIST AI RMF 1.0 (NIST AI 100-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

2026-08-01: 내부 검토용 초안 작성. 게시 일정과 제공 상태는 확정하지 않았다.
