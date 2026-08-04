---
layout: single
title: "A Context Window Is Not Memory"
description: "Separate request context, application state, and retrieved documents when designing long-running AI features."
date: 2026-08-01 09:00:00 +09:00
lang: en
translation_key: context-window-is-not-memory
section: development
topic_key: ai
categories: AI
tags: [ai, llm, context-window, memory, rag, agents]
track: ai-knowledge-foundations
published: false
author_profile: false
permalink: /en/development/context-window-is-not-memory/
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

“Memory” can refer to three different things: text the model can consider in this request, durable state an application stores for later requests, and documents retrieved when needed. All can influence an answer, but they differ in location, lifetime, update rules, and authorization. A long context window does not itself create durable, governed memory.

## Document Info / Environment

- Written: 2026-08-01
- Verification basis: official documentation and a primary research paper
- Document type: concept analysis
- Experiment environment: no direct experiment was performed.
- Scope: product-specific context sizes and memory behavior are not compared.

## Problem Statement / 문제 정의

When a model refers to an earlier message, it is tempting to infer that it stored the information permanently. Conversely, data stored in an application is unavailable to a model unless the application reads it and includes it in a request or exposes it through an authorized tool. Conflating these mechanisms creates oversized prompts, lost state between sessions, and unsafe mixing of documents with different permissions.

## Verified Facts / 확인된 사실

Anthropic defines a context window as the information a model can reference when generating a response and distinguishes it from training data; its documentation lists prompts, messages, tool results, documents, and output as context contributors ([official documentation](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)). OpenAI similarly describes context-window limits and adding retrieved material to generation requests ([prompt guide](https://developers.openai.com/api/docs/guides/prompt-engineering)). The RAG paper distinguishes a generator’s parametric memory from a non-parametric document index ([Lewis et al.](https://arxiv.org/abs/2005.11401)).

## Reproduction Steps / 재현 순서

No direct product test is claimed. Classify information in one workflow: put the current task and immediate tool result in request context; retain durable decisions, ownership, and completion state in an application-controlled store; retrieve policies and manuals only when relevant and authorized. For every durable item, record its source, update owner, and timestamp. Then inject only the subset necessary for the current task.

## Observations / 관찰 결과

This division narrows diagnosis. If an assistant seems to forget, verify whether prior material was actually included and whether summarization omitted it. If it contradicts an earlier decision, inspect the durable source of truth and its retrieval path. If it exposes an unrelated document, inspect tenant, user, and role filters before generation. More context is not automatically better context.

## Interpretation / 해석

My interpretation is that long-running AI “memory” is mainly an application-state design problem. The model can reason over supplied information, while the application must decide what persists, who may change it, and who may retrieve it. Larger input capacity can help process more material at once, but it does not solve provenance, ownership, or access control.

## Limitations / 한계

This does not compare vendor memory features or guarantee their retention policies. Actual context capacity and billing can change. A production design also needs auditing, deletion, backups, and data-classification controls. The analysis is conceptual and reports no direct experiment.

## References / 참고자료

- [Anthropic, Context windows](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)
- [OpenAI, Prompt engineering guide](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)

## Change Log / 변경 이력

- 2026-08-01: Internal-review English mirror created; publication status and schedule were not changed.
