---
layout: single
title: "Why chunking matters: fixed, sentence, and hierarchical splits"
description: "Compares fixed, sentence, and hierarchical chunking by document structure, retrieval quality, citation context, and evaluation."
date: 2026-08-01 09:00:00 +09:00
lang: en
translation_key: why-chunking-matters
section: development
topic_key: ai
categories: AI
tags: [ai, rag, retrieval, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
permalink: /en/development/why-chunking-matters/
sidebar:
  nav: "sections"

search: true
---

## Summary / 요약

Chunking defines both the unit retrieved and the context that can support a citation. Rather than applying one size everywhere, compare strategies against the corpus structure and real questions.

## Document Info / Environment

- Written and verified: 2026-08-01
- Type: conceptual and design guide
- Direct experiment: none. Concepts were reviewed against cited research and official documentation.
- Provider capabilities and defaults can change; verify linked documentation before publication.

## Problem Statement / 문제 정의

Why chunking matters: fixed, sentence, and hierarchical splitscannot be answered as one model capability. Inspect source documents, retrieval candidates, user authorization, and the generation contract as separate layers.

## Verified Facts / 확인된 사실

- RAG supplies selected documents as context for generation. [Lewis et al.](https://arxiv.org/abs/2005.11401)
- Microsoft’s RAG guidance recommends evaluating chunk size and overlap with document structure and content type in mind. [Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)

- Fixed-size splits use a constant token budget. They are simple, but may cut titles, exceptions, tables, or lists apart.
- Sentence/paragraph splits preserve reading boundaries, but create uneven lengths and may leave very long sections intact.
- Hierarchical splits retain document→section→chunk relationships. A system can retrieve a small child chunk and add parent context, at the cost of more indexing and evaluation work.

## Reproduction Steps / 재현 순서

1. Define at least 20 real questions and the authoritative passage expected for each.
2. Apply all three strategies to the same corpus; record Recall@k and whether citations retain conditions and exceptions.
3. Hold embedding, filters, and reranking constant while changing only segmentation.
4. Classify misses as boundary cuts, oversized context, or lost document structure.

## Observations / 관찰 결과

Evaluation records should retain candidate documents, selected context, citations, and authorization conditions alongside the answer. That evidence identifies whether a recurrence belongs to document stewardship, retrieval, generation, or access control.

## Interpretation / 해석

No chunk size is universally safe. Documents whose rules depend on headings, scope, and exceptions particularly benefit from preserving structural relationships.

## Limitations / 한계

- Results depend on the corpus and question distribution.
- This article does not prescribe a universal token size or overlap ratio.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Karpukhin et al., Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: 제목별 핵심 개념, 비교·평가 절차, 근거 연결을 보강한 내부 검토용 개정본. `published: false`; 발행 일정은 정하지 않았다.
