---
layout: single
title: "AI 출력의 변동성을 제어하는 방법"
description: "같은 요청에도 달라질 수 있는 생성 결과를 입력, 제약, 검증, 평가로 관리하는 방법을 정리한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: controlling-output-variance
section: development
topic_key: ai
categories: AI
tags: [ai, llm, prompting, structured-output, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

생성형 AI의 답은 같은 목적을 향해도 표현, 순서, 세부 내용이 달라질 수 있다. 제품에서 중요한 것은 모든 문장을 고정하는 일이 아니라, 허용 가능한 변동과 허용할 수 없는 변동을 구분하는 일이다. 입력을 명확히 하고 출력 계약과 검증을 두면 창의적 문장에는 여지를 남기면서도 데이터 형식과 안전 경계를 관리할 수 있다.

## Document Info / Environment

- 작성일: 2026-08-01
- 검증 기준: 공식 개발자 문서와 NIST 지침
- 문서 성격: concept analysis
- 테스트 환경: 직접 실행 실험 없음.
- 특정 모델의 설정값·성능·가격을 주장하지 않는다.

## Problem Statement / 문제 정의

요약문에는 서로 다른 표현이 허용될 수 있지만, 주문 상태 JSON에서 필드 누락이나 권한 밖 행동은 허용되지 않는다. 이를 같은 “일관성” 문제로 다루면 프롬프트에 과도한 지시를 붙이거나, 반대로 검증해야 할 출력을 자연스러운 문장처럼 받아들이게 된다. 먼저 작업별 실패 기준을 정해야 한다.

## Verified Facts / 확인된 사실

OpenAI는 Structured Outputs가 지정한 JSON Schema를 따르도록 설계된 기능이라고 문서화하며, JSON mode만으로는 특정 스키마 준수를 보장하지 않는다고 구분한다([Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)). NIST AI RMF의 생성형 AI 프로파일은 신뢰성, 측정, 거버넌스 등 위험 관리 활동을 다룬다([NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)). 이는 변동을 모델 설정 하나가 아니라 시스템 통제로 다룰 근거가 된다.

## Reproduction Steps / 재현 순서

직접 실험 대신 대표 작업을 세 부류로 나눈다. 자유로운 초안에는 대상 독자·근거·금지 표현을 제공하고 사람 검토를 둔다. 표준 응답에는 예시와 필수 항목을 제공한다. 시스템 입력에는 스키마, 범위 검사, 재시도와 실패 경로를 둔다. 각 작업에서 무엇이 달라도 되는지와 무엇이 반드시 같아야 하는지를 테스트 케이스로 기록한다.

## Observations / 관찰 결과

변동 원인은 모델만이 아니다. 입력 문서의 차이, 검색 결과의 순위, 도구 응답, 지시 충돌, 출력 파서가 모두 결과에 영향을 준다. 따라서 사건을 볼 때 원문 요청, 선택된 문맥, 구조 검증 결과, 사용자에게 노출된 최종값을 연결해 기록해야 한다. 자연스러운 문장이 같아 보여도 근거가 달라졌다면 별도 문제다.

## Interpretation / 해석

내 해석으로 좋은 제어는 “항상 같은 문장”보다 “계약을 지키는 다양한 문장”을 목표로 한다. 고정해야 하는 것은 필수 필드, 출처, 권한, 금지 행동과 같은 불변 조건이다. 변화를 허용하는 것은 어조, 예시, 설명 순서처럼 사용자 경험을 풍부하게 하는 요소다.

## Limitations / 한계

구조화 출력도 입력 사실의 정확성이나 사업 규칙의 타당성을 보장하지 않는다. 제품별 기능과 제약은 달라질 수 있다. 이 글은 확률 설정별 결과를 측정하지 않았고 직접 실험이 아니다. 고위험 업무에는 독립적인 도메인 검토가 필요하다.

## References / 참고자료

- [OpenAI, Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-01: 내부 검토용 초안 작성. 게시 일정과 공개 상태는 변경하지 않았다.
