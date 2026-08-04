---
layout: single
title: "Good RAG starts with document quality before retrieval"
description: "Explains why source authority, version, retirement state, structure, ownership, and access scope must be established before RAG indexing."
date: 2026-08-01 09:00:00 +09:00
lang: en
translation_key: document-quality-before-retrieval
section: development
topic_key: ai
categories: AI
tags: [ai, rag, retrieval, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
permalink: /en/development/document-quality-before-retrieval/
sidebar:
  nav: "sections"

search: true
---

## Summary / 요약

Retrieval cannot repair an unclear source corpus. Authority, version, retirement state, structure, ownership, and access scope must be known before indexing; otherwise search can amplify ambiguity rather than resolve it.

## Document Info / Environment

- Written and verified: 2026-08-01
- Type: conceptual and operational design guide; no live corpus test was performed.
- Validate provider documentation and organizational policy again before publication or implementation.

## Problem Statement / 문제 정의

A clean vector index can still retrieve a superseded policy, an unlabeled draft, a document without an accountable owner, or a passage that is inaccessible to the requesting user. These are source-governance failures before they are model failures.

## Verified Facts / 확인된 사실

- RAG combines retrieval from an external document index with generation. [Lewis et al.](https://arxiv.org/abs/2005.11401)
- NIST AI 600-1 identifies data quality, information integrity, and context-specific risk management as relevant to generative-AI systems. [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- Retrieval systems use indexed data structures to return candidate content; the index does not establish that a source is authoritative. [OpenAI Retrieval](https://developers.openai.com/api/docs/guides/retrieval)

A usable source record needs an accountable owner, authoritative status, version or effective date, retirement state, extraction quality, and authorization metadata.

## Reproduction Steps / 재현 순서

1. Inventory candidate sources and mark each as authoritative, supporting, draft, retired, or unknown.
2. Assign an owner, effective date/version, refresh rule, access scope, and retention status before indexing.
3. Test difficult source forms—tables, scanned pages, appendices, duplicate policies, and conflicting versions—against expected passages.
4. Exclude retired and unauthorized material at retrieval time; record the decision and re-evaluate after source changes.

## Observations / 관찰 결과

When a current policy and a retired policy are both searchable without clear metadata, fluent generation can hide the conflict. Retrieval metrics alone will not reveal that the wrong source was treated as authoritative.

## Interpretation / 해석

My interpretation is that document stewardship is part of the product, not a preprocessing chore. A smaller, owned, current corpus is often a better starting point than a larger undifferentiated one.

## Limitations / 한계

- “Authoritative” is an organizational decision, not a vector-search property.
- Source lifecycle and legal retention requirements differ by organization and jurisdiction.
- This article does not prescribe a document-management platform or ingestion pipeline.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [OpenAI Retrieval guide](https://developers.openai.com/api/docs/guides/retrieval)
- [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: Replaced the generic English body with document-quality-specific source-governance guidance. `published: false`.
