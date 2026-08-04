---
layout: single
title: "Embedding은 ‘의미를 이해한다’는 말과 어떻게 다른가"
description: "임베딩 유사도가 표현하는 것과 사실성·정확한 조건 일치가 다른 이유를 평가 방법과 함께 설명한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: what-embeddings-represent
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

Embedding은 텍스트를 숫자 벡터로 바꿔 근접도를 비교하게 하지만, 그 근접도가 사실성·권한·정확한 조건 일치를 보장하지는 않는다.

## Document Info / Environment

- 작성일·검증 기준일: 2026-08-01
- 문서 성격: 개념·설계 가이드
- 직접 실행 테스트: 없음. 인용한 연구와 공식 문서로 개념을 검토했다.
- 공급자 기능·기본값은 변경될 수 있으므로 링크는 발행 전 다시 확인한다.

## Problem Statement / 문제 정의

Embedding은 ‘의미를 이해한다’는 말과 어떻게 다른가라는 질문은 모델 하나의 기능으로 답할 수 없다. 문서 원본, 검색 후보, 사용자 권한, 생성 계약을 분리해 관찰해야 한다.

## Verified Facts / 확인된 사실

- Sentence-BERT는 문장 임베딩을 유사도 비교에 사용할 수 있도록 설계했다. [Reimers & Gurevych](https://arxiv.org/abs/1908.10084)
- DPR은 질문과 문서를 dense vector로 인코딩해 내적 기반 검색에 사용한다. [Karpukhin et al.](https://arxiv.org/abs/2004.04906)

- 벡터가 가깝다는 것은 해당 모델·거리 함수에서 표현이 유사하다는 뜻이지, 두 문장이 같은 사실이라는 뜻은 아니다.
- 고유명사, 숫자, 날짜, 부정문, 예외 조항은 의미상 비슷해 보여도 정확한 일치가 중요할 수 있다.
- 임베딩은 검색 후보 생성의 신호이며, 원문·키워드·권한 필터·reranking과 함께 검증해야 한다.

## Reproduction Steps / 재현 순서

1. 동의어 질문, 숫자 하나만 다른 질문, 부정문, 약어를 포함한 평가 세트를 만든다.
2. 각 질문의 상위 k개 문서와 유사도 점수, 정답 근거 포함 여부를 기록한다.
3. 벡터 검색만 쓴 결과와 키워드/하이브리드 결과를 비교한다.
4. 점수가 높아도 틀린 문서를 별도 실패 유형으로 저장한다.

## Observations / 관찰 결과

평가 결과는 답변 문장만이 아니라 후보 문서, 선택 문맥, 인용, 권한 조건과 함께 남겨야 한다. 그래야 같은 오류를 문서·검색·생성·권한의 어느 층에서 고칠지 판단할 수 있다.

## Interpretation / 해석

내 해석으로 embedding은 ‘의미를 이해하는 증명’보다 검색 공간에서 후보를 정렬하기 위한 학습된 표현이다. 따라서 높은 유사도는 검토 우선순위를 줄 뿐, 답변의 근거가 되지는 않는다.

## Limitations / 한계

- 모델·언어·도메인에 따라 임베딩 공간의 성질은 달라진다.
- 이 글은 특정 임베딩 모델의 벤치마크 우열을 주장하지 않는다.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Karpukhin et al., Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: 제목별 핵심 개념, 비교·평가 절차, 근거 연결을 보강한 내부 검토용 개정본. `published: false`; 발행 일정은 정하지 않았다.
