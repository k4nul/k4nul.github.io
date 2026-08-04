---
layout: single
title: "What embeddings represent—and what “understanding meaning” misses"
description: "Explains what embedding similarity represents, why it differs from factual or exact-condition matching, and how to evaluate it."
date: 2026-08-01 09:00:00 +09:00
lang: en
translation_key: what-embeddings-represent
section: development
topic_key: ai
categories: AI
tags: [ai, rag, retrieval, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
permalink: /en/development/what-embeddings-represent/
sidebar:
  nav: "sections"

search: true
---

## Summary / 요약

Embeddings turn text into numeric vectors for proximity comparisons. Proximity does not guarantee factuality, authorization, or an exact match on conditions.

## Document Info / Environment

- Written and verified: 2026-08-01
- Type: conceptual and design guide
- Direct experiment: none. Concepts were reviewed against cited research and official documentation.
- Provider capabilities and defaults can change; verify linked documentation before publication.

## Problem Statement / 문제 정의

What embeddings represent—and what “understanding meaning” missescannot be answered as one model capability. Inspect source documents, retrieval candidates, user authorization, and the generation contract as separate layers.

## Verified Facts / 확인된 사실

- Sentence-BERT was designed to make sentence embeddings useful for similarity comparison. [Reimers and Gurevych](https://arxiv.org/abs/1908.10084)
- DPR encodes questions and passages as dense vectors for inner-product retrieval. [Karpukhin et al.](https://arxiv.org/abs/2004.04906)

- Close vectors mean the model represents texts as similar under a chosen distance function; they do not mean the statements are equally true.
- Names, numbers, dates, negation, and exception clauses can require exact matching even when wording is semantically similar.
- Embedding is a candidate-generation signal and needs source text, lexical signals, authorization filters, and reranking around it.

## Reproduction Steps / 재현 순서

1. Build an evaluation set with paraphrases, one-number changes, negation, and abbreviations.
2. Record the top-k documents, similarity scores, and whether the authoritative passage is present.
3. Compare vector-only retrieval with lexical or hybrid retrieval.
4. Store high-score wrong documents as their own failure class.

## Observations / 관찰 결과

Evaluation records should retain candidate documents, selected context, citations, and authorization conditions alongside the answer. That evidence identifies whether a recurrence belongs to document stewardship, retrieval, generation, or access control.

## Interpretation / 해석

My interpretation: an embedding is a learned representation for arranging candidates in a search space, not evidence that a system understands or has verified a meaning.

## Limitations / 한계

- Embedding geometry varies by model, language, and domain.
- This article does not rank embedding models by benchmark performance.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Karpukhin et al., Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: 제목별 핵심 개념, 비교·평가 절차, 근거 연결을 보강한 내부 검토용 개정본. `published: false`; 발행 일정은 정하지 않았다.
