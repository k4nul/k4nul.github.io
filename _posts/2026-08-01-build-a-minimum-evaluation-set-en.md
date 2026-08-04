---
layout: single
title: "Build a Minimum Evaluation Set for AI"
description: "How a small set of real tasks and failure cases can make AI feature changes comparable."
date: 2026-08-01
lang: en
translation_key: build-a-minimum-evaluation-set
section: development
topic_key: ai
categories: AI
tags: [ai, evaluation, testing, risk-management]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/development/build-a-minimum-evaluation-set/
---

## Summary / 요약

An AI evaluation set does not need to begin as a large benchmark. A small collection of real questions, necessary constraints, and requests that should not be answered can make changes comparable. Its purpose is not to declare absolute model capability, but to create repeatable review criteria tied to the feature’s intent and risks.

## Document Info / Environment

This is an evaluation-design draft dated 2026-08-01. It ran and scored no model or dataset; examples make no performance or product-result claim.

## Problem Statement / 문제 정의

After changing a prompt, retrieval method, model, or tool, output may appear better without showing what improved. A set containing only normal questions misses weak evidence, ambiguity, and unauthorized-information cases. Without criteria, post-release complaints become the first meaningful test.

## Verified Facts / 확인된 사실

NIST AI RMF 1.0 calls for selecting measurement methods and metrics beginning with significant mapped risks and documenting characteristics that cannot be measured. It also calls for performance or assurance criteria under conditions similar to deployment. NIST AI 600-1 addresses evaluation and continuous monitoring for generative AI.

## Reproduction Steps / 재현 순서

Collect questions that represent the feature’s purpose, and record acceptable evidence and expected behavior for each. Add no-answer cases, conflicting documents, ambiguous wording, and requests needing refusal or human transfer. Assign pass criteria, reviewer, and result format, then rerun the same set after changes and inspect differences.

## Observations / 관찰 결과

Even a small set helps separate problems. Answering without retrieved support suggests retrieval or policy work; distorting supplied support suggests generation or presentation work. Recording item-level failure reasons is often more actionable than relying on one score.

## Interpretation / 해석

Evaluation is not a release-time certificate. It is a loop for checking product assumptions. A minimum set does not represent all reality, but it makes explicit which failures matter and which limitations are unacceptable. Samples and criteria should change with the use case.

## Limitations / 한계

A small set cannot cover rare cases, long-term effects, or all user experiences. Human-written expected answers can be wrong or biased. Results are evidence under stated conditions, not a guarantee of safety, accuracy, or legal suitability.

## References / 참고자료

- [NIST AI RMF 1.0 (NIST AI 100-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

2026-08-01: Internal review draft created. No publication schedule or availability status is implied.
