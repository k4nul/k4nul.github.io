---
layout: single
title: "벡터 검색만으로 부족한 이유: 키워드·하이브리드·reranking"
description: "키워드·벡터·하이브리드 검색과 reranking을 후보 회수율, 순위, 비용, 지연의 관점에서 비교한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: hybrid-search-and-reranking
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

의미 유사도는 자연어 표현 차이에 강할 수 있지만, 제품 코드·약어·버전·금액처럼 정확한 문자열이 중요한 질문에서는 키워드 신호가 필요하다. 하이브리드 검색과 reranking은 후보 누락과 순위 오류를 분리해 다루는 방법이다.

## Document Info / Environment

- 작성일·검증 기준일: 2026-08-01
- 문서 성격: 개념·설계 가이드
- 직접 실행 테스트: 없음. 인용한 연구와 공식 문서로 개념을 검토했다.
- 공급자 기능·기본값은 변경될 수 있으므로 링크는 발행 전 다시 확인한다.

## Problem Statement / 문제 정의

벡터 검색만으로 부족한 이유: 키워드·하이브리드·reranking라는 질문은 모델 하나의 기능으로 답할 수 없다. 문서 원본, 검색 후보, 사용자 권한, 생성 계약을 분리해 관찰해야 한다.

## Verified Facts / 확인된 사실

- BEIR은 다양한 정보 검색 과제에서 dense·sparse·reranking 접근을 비교하는 벤치마크를 제공한다. [Thakur et al.](https://arxiv.org/abs/2104.08663)
- DPR은 dense retrieval의 질문-문서 후보 검색 구조를 제시한다. [Karpukhin et al.](https://arxiv.org/abs/2004.04906)

- 키워드 검색은 정확한 용어·번호·희귀 약어에 강할 수 있고, 벡터 검색은 표현이 달라도 관련 후보를 찾는 데 도움이 될 수 있다.
- 하이브리드 검색은 두 후보 집합이나 점수를 결합한다. 결합 방식 자체도 평가 대상이다.
- reranker는 초기 후보 일부를 더 비싼 모델이나 정교한 질의-문서 비교로 다시 정렬한다. reranking은 후보에 없던 문서를 되살리지는 못한다.

## Reproduction Steps / 재현 순서

1. 질문에 정확 문자열·동의어·약어·숫자 조건을 표시한다.
2. lexical-only, vector-only, hybrid의 Recall@k를 비교한다.
3. 동일 후보 수에서 reranker 전후의 MRR 또는 nDCG와 지연 시간을 기록한다.
4. 후보 누락과 후보는 있었지만 순위가 낮았던 경우를 분리한다.

## Observations / 관찰 결과

평가 결과는 답변 문장만이 아니라 후보 문서, 선택 문맥, 인용, 권한 조건과 함께 남겨야 한다. 그래야 같은 오류를 문서·검색·생성·권한의 어느 층에서 고칠지 판단할 수 있다.

## Interpretation / 해석

내 해석으로 하이브리드는 “둘을 쓰면 항상 더 좋다”가 아니라, 질문 분포가 어떤 신호를 요구하는지 검증하는 설계다. reranking은 정확도와 비용·지연의 교환을 명시해야 한다.

## Limitations / 한계

- 점수 정규화와 후보 수는 구현마다 다르다.
- 이 글은 특정 검색 엔진이나 reranker를 추천하지 않는다.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Karpukhin et al., Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: 제목별 핵심 개념, 비교·평가 절차, 근거 연결을 보강한 내부 검토용 개정본. `published: false`; 발행 일정은 정하지 않았다.
