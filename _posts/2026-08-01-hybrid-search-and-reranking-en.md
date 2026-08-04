---
layout: single
title: "Why vector search alone can be insufficient: keywords, hybrid search, reranking"
description: "Compares lexical, vector, hybrid retrieval, and reranking through recall, ranking, cost, and latency."
date: 2026-08-01 09:00:00 +09:00
lang: en
translation_key: hybrid-search-and-reranking
section: development
topic_key: ai
categories: AI
tags: [ai, rag, retrieval, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
permalink: /en/development/hybrid-search-and-reranking/
sidebar:
  nav: "sections"

search: true
---

## Summary / 요약

Semantic similarity can handle wording variation, while product codes, abbreviations, versions, and amounts often require lexical signals. Hybrid retrieval and reranking separate candidate recall from ranking quality.

## Document Info / Environment

- Written and verified: 2026-08-01
- Type: conceptual and design guide
- Direct experiment: none. Concepts were reviewed against cited research and official documentation.
- Provider capabilities and defaults can change; verify linked documentation before publication.

## Problem Statement / 문제 정의

Why vector search alone can be insufficient: keywords, hybrid search, and rerankingcannot be answered as one model capability. Inspect source documents, retrieval candidates, user authorization, and the generation contract as separate layers.

## Verified Facts / 확인된 사실

- BEIR provides a benchmark that compares dense, sparse, and reranking approaches across retrieval tasks. [Thakur et al.](https://arxiv.org/abs/2104.08663)
- DPR presents dense question–passage candidate retrieval. [Karpukhin et al.](https://arxiv.org/abs/2004.04906)

- Lexical retrieval can be strong for exact terms, IDs, and rare abbreviations; vector retrieval can recover related wording.
- Hybrid retrieval combines candidate sets or scores. Its combination rule is itself an evaluation target.
- A reranker reorders an initial candidate set using a more detailed query–document comparison. It cannot recover a document that never became a candidate.

## Reproduction Steps / 재현 순서

1. Label questions containing exact strings, paraphrases, abbreviations, and numeric constraints.
2. Compare Recall@k for lexical-only, vector-only, and hybrid retrieval.
3. At the same candidate count, record MRR or nDCG and latency before and after reranking.
4. Separate candidate misses from cases where the right candidate was present but ranked too low.

## Observations / 관찰 결과

Evaluation records should retain candidate documents, selected context, citations, and authorization conditions alongside the answer. That evidence identifies whether a recurrence belongs to document stewardship, retrieval, generation, or access control.

## Interpretation / 해석

My interpretation: hybrid retrieval is not “always better”; it is a testable response to the signals required by a question distribution. Reranking should state its accuracy, cost, and latency trade-off.

## Limitations / 한계

- Score normalization and candidate counts vary by implementation.
- This article does not recommend a specific search engine or reranker.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Karpukhin et al., Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: 제목별 핵심 개념, 비교·평가 절차, 근거 연결을 보강한 내부 검토용 개정본. `published: false`; 발행 일정은 정하지 않았다.
