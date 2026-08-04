---
layout: single
title: "왜 AI는 그럴듯하지만 틀린 답을 하는가"
description: "생성 텍스트의 유창성과 사실 근거를 구분하고 환각 위험을 줄이는 제품 설계 기준을 정리한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: why-hallucinations-happen
section: development
topic_key: ai
categories: AI
tags: [ai, llm, hallucination, rag, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

AI가 유창한 문장으로 답했다고 해서 그 문장이 검증된 사실이라는 뜻은 아니다. 생성 모델은 입력 문맥을 조건으로 다음 텍스트를 만들며, 근거가 없거나 모호한 질문에도 완전한 답처럼 보이는 문장을 낼 수 있다. 이 글은 이를 모델의 의도나 거짓말로 의인화하지 않고, 근거·검색·검증의 설계 문제로 다룬다.

## Document Info / Environment

- 작성일: 2026-08-01
- 검증 기준: 원 논문, 공식 문서, NIST 지침
- 문서 성격: concept analysis
- 테스트 환경: 직접 실행 실험 없음.
- 특정 모델의 오류율이나 성능을 주장하지 않는다.

## Problem Statement / 문제 정의

“환각”이라는 말은 틀린 인용, 오래된 정보, 검색 실패, 문서 오독, 불확실한 추론을 한 범주로 묶기 쉽다. 그러나 해결책은 다르다. 주문 금액에는 원본 DB 조회가, 정책 설명에는 날짜가 있는 문서와 인용이, 불확실한 판단에는 보류와 사람 검토가 필요하다. 문제의 종류를 분리해야 과장된 자동화를 피할 수 있다.

## Verified Facts / 확인된 사실

Transformer는 입력과 생성된 토큰의 관계를 attention 기반으로 처리하는 구조로 제시되었다([Vaswani et al.](https://arxiv.org/abs/1706.03762)). RAG 논문은 생성기에 외부 문서 인덱스를 결합하는 방법을 다룬다([Lewis et al.](https://arxiv.org/abs/2005.11401)). NIST 생성형 AI 프로파일은 confabulation을 포함한 생성형 AI 위험을 논의한다([NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)). 이 자료들은 유창성이 출처 검증과 동의어가 아님을 뒷받침한다.

## Reproduction Steps / 재현 순서

직접 실험 대신 실제 질문을 원본 레코드형, 문서 근거형, 해석·초안형으로 분류한다. 첫째는 도구나 DB의 반환값과 비교하고, 둘째는 검색된 원문과 인용을 연결하며, 셋째는 검토자와 승인 기준을 둔다. 답을 찾지 못했을 때는 추정 대신 부족한 정보와 다음 확인 경로를 출력하도록 설계한다.

## Observations / 관찰 결과

오류를 “모델이 틀렸다”로 끝내면 개선 지점이 없다. 검색 상위 결과에 정답 문서가 없었는지, 제공된 문맥에 모순이 있었는지, 모델이 근거 밖 주장을 했는지, 인용 연결이 끊겼는지를 나눠 기록해야 한다. 출처 표시는 문서 식별자와 실제 주장 사이의 연결까지 확인할 때 의미가 있다.

## Interpretation / 해석

내 해석으로 환각 완화의 핵심은 모델에게 “절대 틀리지 말라”고 지시하는 것이 아니다. 근거가 필요한 작업에는 원본 접근, 관련성 선택, 인용, 출력 검증, 사람 승인을 적절히 배치하는 일이다. 생성은 설명층이 될 수 있지만 사실의 원본을 대체해서는 안 된다.

## Limitations / 한계

RAG와 인용은 정확성 보증이 아니며, 문서 자체가 오래되거나 틀릴 수 있다. 이 글은 제품별 오류율을 비교하지 않고 직접 실험을 보고하지 않는다. 의료·법률·금융 판단에는 분야별 책임 절차가 추가로 필요하다.

## References / 참고자료

- [Vaswani et al., Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-01: 내부 검토용 초안 작성. 게시 일정과 공개 상태는 변경하지 않았다.
