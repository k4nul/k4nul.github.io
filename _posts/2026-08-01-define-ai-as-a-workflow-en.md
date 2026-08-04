---
layout: single
title: "Define AI as a Workflow, Not a Feature"
description: "A practical way to define an AI capability through its inputs, decisions, outputs, and accountable handoffs."
date: 2026-08-01
lang: en
translation_key: define-ai-as-a-workflow
section: development
topic_key: ai
categories: AI
tags: [ai, workflow, risk-management, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/development/define-ai-as-a-workflow/
---

## Summary / 요약

An AI capability is easier to design responsibly when it is described as a workflow rather than as a chat box or a model call. The workflow includes the source and scope of inputs, context selection, model processing, presentation of the output, and the person or system that acts next. Value and failure can emerge at any of those points.

## Document Info / Environment

This is a conceptual draft dated 2026-08-01. It reports no implementation, production observation, or direct test. It is written for product, engineering, and operations readers who need a shared description of an AI-assisted flow.

## Problem Statement / 문제 정의

“Build an AI summarizer” does not say which documents are allowed, whether the result is advisory, or whether it can trigger an action. The same model can support low-impact reading or influence a consequential decision. A vague feature definition therefore produces vague evaluation and failure-handling criteria.

## Verified Facts / 확인된 사실

NIST AI RMF 1.0 organizes risk-management activity around GOVERN, MAP, MEASURE, and MANAGE; MAP includes identifying context and intended purpose. NIST AI 600-1 treats generative-AI risks as sociotechnical, involving data, people, and deployment context. These sources support documenting the system around the model, not just naming the model.

## Reproduction Steps / 재현 순서

Write the user goal in one sentence. Then record the input source and permitted scope, context sent to the model, output format, and receiving actor. For every handoff, record ownership and what should stop or be communicated on failure. Include routes for missing evidence, ambiguous requests, and unusable input.

## Observations / 관찰 결과

This map turns “the AI answers” into visible decisions: whether to answer without evidence, show citations, or pass output automatically to another system. Evaluation can then cover input fitness, evidence linkage, and safety of the next action as well as fluency.

## Interpretation / 해석

A workflow definition is not a promise to eliminate risk. It is a small design record that exposes assumptions and dependencies for discussion. Separating provider, application operator, and user roles also makes it less tempting to assign every failure to one component.

## Limitations / 한계

A diagram does not replace access controls, security design, legal review, or use-case-specific judgment. NIST guidance is voluntary risk-management guidance, not a compliance certification. Documentation alone cannot guarantee that a model output is correct or appropriate.

## References / 참고자료

- [NIST AI RMF 1.0 (NIST AI 100-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

2026-08-01: Internal review draft created. No publication schedule or availability status is implied.
