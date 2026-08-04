---
layout: single
title: "What is RAG, and how does it differ from an LLM alone"
description: "Explains RAG as retrieved evidence supplied at question time, with boundaries versus an LLM alone, databases, fine-tuning, and tools."
date: 2026-08-01 09:00:00 +09:00
lang: en
translation_key: what-is-rag
section: development
topic_key: ai
categories: AI
tags: [ai, rag, retrieval, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
permalink: /en/development/what-is-rag/
sidebar:
  nav: "sections"

search: true
---

## Summary / 요약

Retrieval-augmented generation (RAG) retrieves selected external passages at question time and supplies them as context for an LLM. It does not automatically update model weights or guarantee that the answer is correct, current, authorized, or well cited.

## Document Info / Environment

- Written and verified: 2026-08-01
- Type: conceptual architecture guide; no direct product benchmark or live deployment was run.
- Provider-specific limits and defaults are intentionally out of scope and must be rechecked before publication.

## Problem Statement / 문제 정의

An LLM alone is not a reliable source for a customer’s current status or an organization’s latest policy. Pasting every document into every request also fails as the corpus grows. RAG creates an explicit retrieval boundary, but that boundary must be evaluated.

## Verified Facts / 확인된 사실

- Lewis et al. describe RAG as combining parametric generation with a non-parametric external memory accessed by retrieval. [Lewis et al.](https://arxiv.org/abs/2005.11401)
- OpenAI’s retrieval documentation describes vector stores and semantic search as retrieval components rather than answers themselves. [OpenAI Retrieval](https://developers.openai.com/api/docs/guides/retrieval)
- NIST AI 600-1 frames generative-AI risk management as context-specific and includes information-integrity and data-quality considerations. [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

A RAG answer therefore has at least five inspectable stages: source document, indexing/chunking, retrieval, context assembly, and generation/citation.

## Reproduction Steps / 재현 순서

1. Classify the requested fact: exact current system value, document-backed explanation, repeated output behavior, or external action.
2. Use a database/API for an exact current record; use RAG for document-backed explanation; consider fine-tuning for repeated behavior; use tools with authorization for external action.
3. For RAG, retain the top candidates, selected passages, document version, user authorization, answer, and citations.
4. Define a no-evidence path rather than letting the model fill a missing source with plausible prose.

## Observations / 관찰 결과

When expected evidence is absent from retrieval candidates, prompt changes address the wrong layer. When evidence is present but the answer is unsupported, inspect context assembly, output constraints, and claim-to-citation linkage.

## Interpretation / 해석

My interpretation is that RAG’s value is not “putting new knowledge into the model.” It makes the candidate evidence corpus governable: documents can be updated, revoked, permission-filtered, and inspected alongside an answer.

## Limitations / 한계

- RAG does not guarantee correctness, authorization, or citation faithfulness.
- Scanned PDFs, tables, images, code, and multilingual documents need their own ingestion evaluation.
- This article does not compare vector databases or managed RAG products.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [OpenAI Retrieval guide](https://developers.openai.com/api/docs/guides/retrieval)
- [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: Expanded the English mirror with system-selection and evaluation boundaries. `published: false`.
