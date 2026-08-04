---
layout: single
title: "Chunking은 왜 필요한가: 고정 길이·문장 단위·계층형 분할 비교"
description: "고정 길이·문장·계층형 chunking을 문서 구조, 검색 품질, 인용 문맥, 평가 기준으로 비교한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: why-chunking-matters
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

문서를 어떤 단위로 검색할지 정하는 일은 검색 정확도와 인용 가능한 문맥의 경계를 함께 정하는 일이다. 한 가지 크기를 모든 문서에 적용하는 대신, 질문과 문서 구조를 기준으로 비교해야 한다.

## Document Info / Environment

- 작성일·검증 기준일: 2026-08-01
- 문서 성격: 개념·설계 가이드
- 직접 실행 테스트: 없음. 인용한 연구와 공식 문서로 개념을 검토했다.
- 공급자 기능·기본값은 변경될 수 있으므로 링크는 발행 전 다시 확인한다.

## Problem Statement / 문제 정의

Chunking은 왜 필요한가: 고정 길이·문장 단위·계층형 분할 비교라는 질문은 모델 하나의 기능으로 답할 수 없다. 문서 원본, 검색 후보, 사용자 권한, 생성 계약을 분리해 관찰해야 한다.

## Verified Facts / 확인된 사실

- RAG는 질문과 함께 선택된 문서를 생성 모델의 문맥으로 제공하는 구조다. [Lewis et al.](https://arxiv.org/abs/2005.11401)
- Microsoft의 RAG 설계 가이드는 문서 구조와 콘텐츠 유형을 고려해 chunk size와 overlap을 평가하라고 안내한다. [Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)

- 고정 길이: 일정 토큰 수로 자른다. 구현은 단순하지만 제목·예외·표의 경계를 끊을 수 있다.
- 문장/문단 단위: 읽기 경계를 보존하지만, 매우 긴 문단과 짧은 문단의 크기 편차가 커질 수 있다.
- 계층형: 문서→절→청크 관계와 부모 문맥을 보존한다. 검색은 작은 청크로 하고, 답변에는 필요한 상위 문맥을 추가할 수 있지만 색인·평가가 복잡해진다.

## Reproduction Steps / 재현 순서

1. 실제 질문과 정답 근거 문단을 20개 이상 정한다.
2. 동일 문서에 세 분할 방식을 적용하고, 각 질문의 Recall@k와 인용이 조건·예외를 함께 담았는지 기록한다.
3. chunk 크기만 바꾸고 embedding·필터·reranker는 고정한다.
4. 오답을 경계 절단, 과대 문맥, 문서 구조 손실로 분류한다.

## Observations / 관찰 결과

평가 결과는 답변 문장만이 아니라 후보 문서, 선택 문맥, 인용, 권한 조건과 함께 남겨야 한다. 그래야 같은 오류를 문서·검색·생성·권한의 어느 층에서 고칠지 판단할 수 있다.

## Interpretation / 해석

큰 청크가 항상 더 안전하거나 작은 청크가 항상 더 정확한 것은 아니다. 정책처럼 예외와 적용 범위가 중요한 문서는 제목·절·표 관계를 보존하는 설계가 특히 중요하다.

## Limitations / 한계

- 문서 형식과 질문 분포가 달라지면 결과도 달라진다.
- 이 글은 특정 토큰 수나 overlap 비율을 보편적 기본값으로 주장하지 않는다.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Karpukhin et al., Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: 제목별 핵심 개념, 비교·평가 절차, 근거 연결을 보강한 내부 검토용 개정본. `published: false`; 발행 일정은 정하지 않았다.
