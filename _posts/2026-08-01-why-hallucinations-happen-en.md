---
layout: single
title: "Why AI Hallucinations Happen"
description: "Separate fluent generation from factual evidence and design AI features to reduce unsupported claims."
date: 2026-08-01 09:00:00 +09:00
lang: en
translation_key: why-hallucinations-happen
section: development
topic_key: ai
categories: AI
tags: [ai, llm, hallucination, rag, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
permalink: /en/development/why-hallucinations-happen/
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

Fluent AI text is not automatically verified fact. A generative model continues text conditioned on its input, so an ambiguous or unsupported question can still receive a complete-sounding response. This article treats unsupported output as an evidence, retrieval, and validation-design issue rather than attributing intent or deception to a model.

## Document Info / Environment

- Written: 2026-08-01
- Verification basis: primary research, official documentation, and NIST guidance
- Document type: concept analysis
- Experiment environment: no direct experiment was performed.
- No product-specific error rate or performance claim is made.

## Problem Statement / 문제 정의

“Hallucination” can combine wrong citations, stale information, retrieval failures, document misreading, and uncertain inference. Their remedies differ. An order amount needs a source-of-record query; a policy explanation needs a dated document and citation; an uncertain judgment needs abstention and review. Separating the failure mode avoids overstated automation.

## Verified Facts / 확인된 사실

The Transformer paper presents attention-based processing of input and generated tokens ([Vaswani et al.](https://arxiv.org/abs/1706.03762)). RAG research describes coupling generation with an external document index ([Lewis et al.](https://arxiv.org/abs/2005.11401)). NIST’s Generative AI Profile discusses confabulation among generative-AI risks ([NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)). None of these sources equates fluent wording with verified provenance.

## Reproduction Steps / 재현 순서

No live experiment is reproduced. Classify real questions as record-backed, document-backed, or interpretive drafting. Compare record-backed answers with tool or database results; connect document-backed claims to retrieved source passages; and give interpretive output an explicit reviewer and approval rule. When evidence is absent, return the missing information and a verification path instead of an invented answer.

## Observations / 관찰 결과

“Model error” alone is not actionable. Log whether the correct document was retrieved, whether the supplied context conflicted, whether a claim exceeded its evidence, and whether the citation link was valid. A displayed citation matters only when it connects the claim to the actual source material.

## Interpretation / 해석

My interpretation is that mitigation is not an instruction to “never be wrong.” It is the careful placement of source access, relevance selection, citation, output validation, and human approval where evidence matters. Generation can explain a fact; it should not replace the fact’s original source.

## Limitations / 한계

Retrieval and citations do not guarantee truth; source documents can be stale or wrong. This article reports no benchmark or direct experiment. Medical, legal, financial, and other high-impact decisions need additional domain-specific controls.

## References / 참고자료

- [Vaswani et al., Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-01: Internal-review draft created; publication status and schedule were not changed.
