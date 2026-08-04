---
layout: single
title: "When to choose RAG, fine-tuning, tool calling, or agents"
description: "Provides selection criteria for RAG, fine-tuning, tool calling, and agents using evidence, repeated behavior, exact system data, and multi-step work."
date: 2026-08-01 09:00:00 +09:00
lang: en
translation_key: choosing-rag-finetuning-tools-agents
section: development
topic_key: ai
categories: AI
tags: [ai, rag, retrieval, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
permalink: /en/development/choosing-rag-finetuning-tools-agents/
sidebar:
  nav: "sections"

search: true
---

## Summary / 요약

These are not competing product names; they address different problem boundaries. Choose from the source of truth, action risk, repeated behavior, and operating controls—not from a desire to make a model “smarter.”

## Document Info / Environment

- Written and verified: 2026-08-01
- Type: conceptual and design guide
- Direct experiment: none. Concepts were reviewed against cited research and official documentation.
- Provider capabilities and defaults can change; verify linked documentation before publication.

## Problem Statement / 문제 정의

When to choose RAG, fine-tuning, tool calling, or agentscannot be answered as one model capability. Inspect source documents, retrieval candidates, user authorization, and the generation contract as separate layers.

## Verified Facts / 확인된 사실

- RAG combines an external document index with generation. [Lewis et al.](https://arxiv.org/abs/2005.11401)
- OpenAI’s retrieval guide describes vector stores as data structures for search. [OpenAI Retrieval](https://developers.openai.com/api/docs/guides/retrieval)
- OWASP identifies excessive authority and sensitive-information disclosure as material LLM-application risks. [OWASP](https://genai.owasp.org/llm-top-10/)

- RAG: explain changing documents with inspectable evidence; operate sources, authorization, and citations.
- Fine-tuning: learn repeated style, classification, or output behavior; it is not a store for current facts.
- Tool calling: obtain exact system values or perform actions such as calculation or booking; input validation and least privilege are central.
- Agents: coordinate multi-step planning, tool use, and state; each tool needs separate permissions, approvals, and stop conditions.

## Reproduction Steps / 재현 순서

1. Classify whether a request needs current document evidence, an exact system value, repeated behavior, or a multi-step workflow.
2. For each candidate, record source of truth, failure cost, user approval, logging, and evaluation method.
3. Evaluate the smallest viable combination first; for example, validate retrieval and no-answer behavior before adding an agent.
4. For change-making tools, require dry-run, validation, approval, audit records, and stop authority.

## Observations / 관찰 결과

Evaluation records should retain candidate documents, selected context, citations, and authorization conditions alongside the answer. That evidence identifies whether a recurrence belongs to document stewardship, retrieval, generation, or access control.

## Interpretation / 해석

My interpretation: this is rarely an exclusive choice. RAG and tools can be combined, but every added component expands failure boundaries and operating cost.

## Limitations / 한계

- Definitions and product capabilities vary by provider.
- High-risk or regulated domains need additional domain review.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Karpukhin et al., Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: 제목별 핵심 개념, 비교·평가 절차, 근거 연결을 보강한 내부 검토용 개정본. `published: false`; 발행 일정은 정하지 않았다.
