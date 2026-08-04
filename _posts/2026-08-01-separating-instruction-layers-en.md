---
layout: single
title: "Separating Instruction Layers in AI Systems"
description: "Distinguish system policy, application rules, user requests, and external data when designing AI features."
date: 2026-08-01 09:00:00 +09:00
lang: en
translation_key: separating-instruction-layers
section: development
topic_key: ai
categories: AI
tags: [ai, llm, prompting, security, tool-calling]
track: ai-knowledge-foundations
published: false
author_profile: false
permalink: /en/development/separating-instruction-layers/
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

An AI request can contain text with different authority: product safety policy, workflow rules, a user’s goal, and retrieved content. They must not be treated as equally authoritative. Separating layers lets a product treat “ignore previous instructions” inside a document as data, while preserving boundaries that a user request cannot change.

## Document Info / Environment

- Written: 2026-08-01
- Verification basis: official documentation and NIST guidance
- Document type: concept analysis
- Experiment environment: no direct experiment was performed.
- No provider security feature is claimed to be complete.

## Problem Statement / 문제 정의

Retrieved documents, emails, pages, and tool results can contain untrusted text. If that text shares a layer with operational instructions, policy changes and permission escalation become a contest of strings. Tool calling makes this especially important because generated text can lead to external action; instruction interpretation and approval boundaries must remain separate.

## Verified Facts / 확인된 사실

OpenAI’s prompt guide distinguishes developer and user message roles and provides guidance for delimiting untrusted input ([official guide](https://developers.openai.com/api/docs/guides/prompt-engineering)). Its safety guidance identifies indirect prompt injection as a risk ([Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)). NIST AI 600-1 addresses governance and management of generative-AI risks ([source](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)).

## Reproduction Steps / 재현 순서

No attack test is reproduced. Classify each request into immutable safety and authorization policy, application workflow rules, user intent, and external documents or tool results. Mark external content as data rather than executable instruction. Apply least privilege, argument validation, separate approval for consequential actions, and audit logs to tools.

## Observations / 관찰 결과

Without layers, it is unclear whether a system summarized a document, attempted to follow its embedded instruction, or allowed an unsafe tool call. Preserve the source and layer of each input plus approval outcomes, while avoiding secrets and unnecessary raw content in logs.

## Interpretation / 해석

My interpretation is that instruction layers are an authorization model, not a prompt-writing trick. A system must constrain which text can alter policy and which actions require approval, even when a model can read every string.

## Limitations / 한계

Prompt separation is not a standalone security control. Authentication, authorization, validation, secret handling, and auditing remain necessary. This is conceptual guidance, not penetration-test or direct-experiment evidence.

## References / 참고자료

- [OpenAI, Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [OpenAI, Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-01: Internal-review draft created; publication status and schedule were not changed.
