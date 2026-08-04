---
layout: single
title: "AI 기능을 평가하는 방법"
description: "데모의 인상 대신 과업, 근거, 실패 비용, 사람 검토를 기준으로 AI 기능을 평가하는 방법을 정리한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: evaluating-ai-features
section: development
topic_key: ai
categories: AI
tags: [ai, llm, evaluation, risk-management, quality]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

AI 기능 평가는 “답이 좋아 보이는가”만으로 끝나면 재현성과 책임을 잃는다. 평가는 실제 사용자 과업, 정답 또는 근거, 허용 가능한 실패, 검토·에스컬레이션 경로를 함께 정의해야 한다. 특히 생성형 기능은 자연스러운 문장 품질과 사실성, 형식 준수, 안전, 운영 비용을 분리해 봐야 한다.

## Document Info / Environment

- 작성일: 2026-08-01
- 검증 기준: NIST 지침과 공식 문서
- 문서 성격: concept analysis
- 테스트 환경: 직접 실행 실험 없음.
- 모델별 점수·가격·성능을 비교하지 않는다.

## Problem Statement / 문제 정의

데모에서 한두 질문이 잘 답됐다는 사실은 실제 업무 분포를 대표하지 않는다. 반대로 자동화율 하나도 오류의 영향, 사람이 고친 시간, 근거 누락, 권한 문제를 숨긴다. 평가 대상은 모델 자체가 아니라 입력 수집, 검색, 지시, 도구, 검증, 사용자 경험을 포함한 기능 전체여야 한다.

## Verified Facts / 확인된 사실

NIST AI RMF와 생성형 AI 프로파일은 위험을 맥락에 맞게 관리하고, 거버넌스·측정·관리 활동을 연결하는 프레임워크를 제공한다([NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)). OpenAI의 평가 가이드는 평가를 정의하고 데이터셋으로 측정하는 반복적 접근을 설명한다([Evaluation guide](https://developers.openai.com/api/docs/guides/evals)). 이는 단일 인상 평가보다 과업별 기준과 기록이 필요함을 뒷받침한다.

## Reproduction Steps / 재현 순서

직접 모델 실험 대신 평가 계획을 만든다. 실제 업무에서 익명화·권한 검토된 사례를 모으고, 정상·경계·실패 사례를 포함한다. 각 사례에 기대 결과, 허용 가능한 대안 표현, 원본 근거, 심각도, 사람 검토 필요 여부를 붙인다. 검색 품질, 생성 품질, 구조 검증, 사용자 완료율을 따로 기록하고 변경 전후 같은 집합으로 비교한다.

## Observations / 관찰 결과

한 점수는 원인을 감춘다. 검색이 실패했는데 생성 품질만 낮다고 기록하거나, 형식은 맞지만 사실이 틀린 결과를 성공으로 셀 수 있다. 오류를 근거 부재, 검색 누락, 해석 오류, 스키마 실패, 권한·안전 문제로 나누면 우선순위가 명확해진다. 사용자 피드백도 근거와 재현 가능한 사례에 연결해야 한다.

## Interpretation / 해석

내 해석으로 좋은 평가는 모델 순위를 만드는 작업보다 제품의 의사결정 기준을 만드는 일이다. 어떤 실패는 초안 단계에서 허용되지만, 어떤 실패는 사용자에게 노출되기 전 차단되어야 한다. 따라서 출시 기준에는 품질뿐 아니라 중단 기준, 롤백, 사람에게 넘기는 경로가 포함되어야 한다.

## Limitations / 한계

평가 데이터셋도 편향되거나 오래될 수 있고, 점수는 실제 사용자 경험을 완전히 대변하지 않는다. 고위험 영역은 독립 검토와 분야별 의무가 필요하다. 이 글은 직접 실험이나 특정 제품 비교를 제공하지 않는다.

## References / 참고자료

- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [OpenAI, Evaluation guide](https://developers.openai.com/api/docs/guides/evals)

## Change Log / 변경 이력

- 2026-08-01: 내부 검토용 초안 작성. 게시 일정과 공개 상태는 변경하지 않았다.
