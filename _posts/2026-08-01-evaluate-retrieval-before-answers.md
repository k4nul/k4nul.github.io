---
layout: single
title: "RAG 평가는 정답률보다 retrieval부터 봐야 한다"
description: "RAG에서 retrieval과 answer evaluation을 Recall@k, ranking, 근거 충실성으로 분리하는 방법을 설명한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: evaluate-retrieval-before-answers
section: development
topic_key: ai
categories: AI
tags: [ai, rag, retrieval, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

답변이 틀렸을 때 정답 근거가 검색 후보에 없었다면 생성 모델을 바꿔도 원인을 해결하지 못한다. retrieval과 generation 평가는 서로 다른 실패를 측정해야 한다.

## Document Info / Environment

- 작성일·검증 기준일: 2026-08-01
- 문서 성격: 개념·설계 가이드
- 직접 실행 테스트: 없음. 인용한 연구와 공식 문서로 개념을 검토했다.
- 공급자 기능·기본값은 변경될 수 있으므로 링크는 발행 전 다시 확인한다.

## Problem Statement / 문제 정의

RAG 평가는 정답률보다 retrieval부터 봐야 한다라는 질문은 모델 하나의 기능으로 답할 수 없다. 문서 원본, 검색 후보, 사용자 권한, 생성 계약을 분리해 관찰해야 한다.

## Verified Facts / 확인된 사실

- BEIR은 retrieval 성능을 relevance judgment와 ranking metric으로 평가하는 벤치마크를 제공한다. [Thakur et al.](https://arxiv.org/abs/2104.08663)
- RAG는 외부 문서 검색 결과를 생성의 조건으로 결합하는 구조다. [Lewis et al.](https://arxiv.org/abs/2005.11401)

- retrieval 평가는 expected evidence가 top-k 후보에 있는지(예: Recall@k), 그리고 얼마나 위에 있는지(MRR·nDCG)를 본다.
- answer 평가는 근거 충실성, 정확성, 완결성, 인용 품질, no-answer 행동을 본다.
- 같은 최종 정답률이라도 검색은 좋고 생성이 나쁘거나, 검색은 나쁘지만 모델의 사전 지식으로 우연히 맞을 수 있다.

## Reproduction Steps / 재현 순서

1. 질문마다 정답 원문과 허용 문서 ID를 라벨링한다.
2. 권한 필터 적용 뒤 top-k 후보의 Recall@k와 ranking 지표를 기록한다.
3. 선택된 문맥을 고정한 상태에서 답변의 claim-to-source 일치와 no-answer를 평가한다.
4. 문서 누락, 순위 오류, 문맥 조립 오류, 근거 밖 생성, 권한 오류로 분류한다.

## Observations / 관찰 결과

평가 결과는 답변 문장만이 아니라 후보 문서, 선택 문맥, 인용, 권한 조건과 함께 남겨야 한다. 그래야 같은 오류를 문서·검색·생성·권한의 어느 층에서 고칠지 판단할 수 있다.

## Interpretation / 해석

내 해석으로 “retrieval부터”는 답변 평가를 포기하자는 뜻이 아니다. 관측 가능한 앞단부터 원인을 좁혀야 프롬프트 수정이 검색·문서 문제를 가리는 일을 막을 수 있다.

## Limitations / 한계

- 정답 근거 라벨은 비용이 들고 복수 문서가 정답일 수 있다.
- 지표만으로 고위험 답변의 적절성을 보장하지 않는다.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Karpukhin et al., Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: 제목별 핵심 개념, 비교·평가 절차, 근거 연결을 보강한 내부 검토용 개정본. `published: false`; 발행 일정은 정하지 않았다.
