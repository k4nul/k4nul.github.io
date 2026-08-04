---
layout: single
title: "Six RAG failure patterns: misses, wrong retrieval, overreach, stale sources"
description: "Presents a diagnostic taxonomy for RAG misses, wrong retrieval, condition misreads, overreach, stale sources, and authorization failures."
date: 2026-08-01 09:00:00 +09:00
lang: en
translation_key: six-rag-failure-patterns
section: development
topic_key: ai
categories: AI
tags: [ai, rag, retrieval, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
permalink: /en/development/six-rag-failure-patterns/
sidebar:
  nav: "sections"

search: true
---

## Summary / 요약

Calling every RAG error a hallucination prevents repair. These six patterns separate document, retrieval, generation, and authorization failures for investigation.

## Document Info / Environment

- Written and verified: 2026-08-01
- Type: conceptual and design guide
- Direct experiment: none. Concepts were reviewed against cited research and official documentation.
- Provider capabilities and defaults can change; verify linked documentation before publication.

## Problem Statement / 문제 정의

Six RAG failure patterns: misses, wrong retrieval, overreach, and stale sourcescannot be answered as one model capability. Inspect source documents, retrieval candidates, user authorization, and the generation contract as separate layers.

## Verified Facts / 확인된 사실

- RAG combines retrieved external documents with generation. [Lewis et al.](https://arxiv.org/abs/2005.11401)
- NIST AI 600-1 emphasizes information integrity, data quality, and context-specific risk management for generative AI. [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

- 1. Miss: the authoritative document is absent from the corpus or top-k candidates.
- 2. Wrong retrieval: irrelevant or merely similar material ranks highly.
- 3. Condition misread: evidence is present but scope, exception, or date is missed.
- 4. Overreach: the answer concludes more than the source states.
- 5. Stale/conflicting source: retired or conflicting material wins.
- 6. Authorization violation: disallowed material appears in candidates, context, or citations.

## Reproduction Steps / 재현 순서

1. Preserve the question, user authorization, corpus version, top-k, selected context, answer, and citations for every incident.
2. Determine whether authoritative evidence reached the corpus, top-k, and selected-context stages.
3. Record one primary pattern and, when needed, contributing patterns.
4. Add the incident to a regression set after remediation.

## Observations / 관찰 결과

Evaluation records should retain candidate documents, selected context, citations, and authorization conditions alongside the answer. That evidence identifies whether a recurrence belongs to document stewardship, retrieval, generation, or access control.

## Interpretation / 해석

My interpretation: the point of a taxonomy is not naming failures. It assigns ownership to document stewardship, retrieval, generation contracts, or authorization controls and makes recurrence measurable.

## Limitations / 한계

- An incident may have more than one cause.
- This taxonomy does not replace domain-specific risk analysis or security incident response.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Karpukhin et al., Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: 제목별 핵심 개념, 비교·평가 절차, 근거 연결을 보강한 내부 검토용 개정본. `published: false`; 발행 일정은 정하지 않았다.
