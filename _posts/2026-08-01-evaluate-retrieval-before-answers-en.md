---
layout: single
title: "Evaluate retrieval before evaluating answers in RAG"
description: "Explains how to separate retrieval and answer evaluation in RAG using Recall@k, ranking, and evidence faithfulness."
date: 2026-08-01 09:00:00 +09:00
lang: en
translation_key: evaluate-retrieval-before-answers
section: development
topic_key: ai
categories: AI
tags: [ai, rag, retrieval, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
permalink: /en/development/evaluate-retrieval-before-answers/
sidebar:
  nav: "sections"

search: true
---

## Summary / 요약

If the authoritative evidence never appears among candidates, changing the generator cannot fix the primary cause. Retrieval and generation evaluation measure different failures.

## Document Info / Environment

- Written and verified: 2026-08-01
- Type: conceptual and design guide
- Direct experiment: none. Concepts were reviewed against cited research and official documentation.
- Provider capabilities and defaults can change; verify linked documentation before publication.

## Problem Statement / 문제 정의

Evaluate retrieval before evaluating answers in RAGcannot be answered as one model capability. Inspect source documents, retrieval candidates, user authorization, and the generation contract as separate layers.

## Verified Facts / 확인된 사실

- BEIR evaluates retrieval with relevance judgments and ranking metrics. [Thakur et al.](https://arxiv.org/abs/2104.08663)
- RAG combines retrieved external documents with generation. [Lewis et al.](https://arxiv.org/abs/2005.11401)

- Retrieval evaluation asks whether expected evidence is in top-k candidates (for example Recall@k) and how highly it is ranked (MRR or nDCG).
- Answer evaluation examines faithfulness, correctness, completeness, citation quality, and no-answer behavior.
- The same final answer accuracy can conceal good retrieval with bad generation, or poor retrieval with a lucky answer from model priors.

## Reproduction Steps / 재현 순서

1. Label an authoritative passage and allowed document IDs for each question.
2. After authorization filtering, record Recall@k and ranking metrics for the top-k candidates.
3. With selected context fixed, evaluate claim-to-source consistency and no-answer behavior.
4. Classify misses as absent documents, ranking errors, context assembly errors, unsupported generation, or authorization errors.

## Observations / 관찰 결과

Evaluation records should retain candidate documents, selected context, citations, and authorization conditions alongside the answer. That evidence identifies whether a recurrence belongs to document stewardship, retrieval, generation, or access control.

## Interpretation / 해석

My interpretation: “evaluate retrieval first” does not abandon answer evaluation. It narrows causes from observable upstream stages so prompt edits do not hide corpus or search failures.

## Limitations / 한계

- Evidence labeling is costly and more than one passage may be valid.
- Metrics alone do not establish suitability for high-risk use.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Karpukhin et al., Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: 제목별 핵심 개념, 비교·평가 절차, 근거 연결을 보강한 내부 검토용 개정본. `published: false`; 발행 일정은 정하지 않았다.
