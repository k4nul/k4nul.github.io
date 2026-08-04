---
layout: single
title: "인용이 있는 답변은 어떻게 만들어지는가"
description: "답변 주장과 원문 passage를 문서 버전·청크 ID·권한까지 포함해 연결하는 RAG 인용 설계를 설명한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: building-citations-in-rag
section: development
topic_key: ai
categories: AI
tags: [ai, rag, retrieval, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

RAG의 인용은 URL 장식이 아니라 답변의 주장과 원문 조각을 연결하는 데이터 구조다. 인용이 있어도 문서가 질문에 답하지 않거나 모델이 문서를 과장하면 신뢰할 수 없다.

## Document Info / Environment

- 작성일·검증 기준일: 2026-08-01
- 문서 성격: 개념·설계 가이드
- 직접 실행 테스트: 없음. 인용한 연구와 공식 문서로 개념을 검토했다.
- 공급자 기능·기본값은 변경될 수 있으므로 링크는 발행 전 다시 확인한다.

## Problem Statement / 문제 정의

인용이 있는 답변은 어떻게 만들어지는가라는 질문은 모델 하나의 기능으로 답할 수 없다. 문서 원본, 검색 후보, 사용자 권한, 생성 계약을 분리해 관찰해야 한다.

## Verified Facts / 확인된 사실

- RAG 연구는 생성에 외부 문서 인덱스를 결합하고 provenance를 중요한 과제로 다룬다. [Lewis et al.](https://arxiv.org/abs/2005.11401)
- NIST AI 600-1은 정보 무결성과 출처 검토를 생성형 AI 위험 관리의 맥락에서 다룬다. [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

- 인용 가능한 레코드는 최소한 document ID, 문서 버전/갱신 시각, chunk ID, 원문 위치, 접근 권한, 검색 점수를 보존해야 한다.
- 생성 단계는 주장 단위로 허용된 청크 ID를 참조하게 하고, 표시 계층은 그 ID에서 제목·링크·문단 위치를 만든다.
- 문서가 삭제·갱신되거나 사용자의 권한이 바뀌면 링크와 표시 가능한 인용도 다시 검증해야 한다.

## Reproduction Steps / 재현 순서

1. 평가 질문마다 정답 주장과 이를 뒷받침하는 허용 passage를 라벨링한다.
2. 답변의 각 핵심 주장에 하나 이상의 passage ID가 연결됐는지 검사한다.
3. 인용의 존재, 인용의 관련성, 주장과 원문의 일치, 링크 접근 가능성을 별도 점수로 기록한다.
4. 근거가 없으면 답변을 축소하거나 “근거를 찾지 못했다” 흐름으로 보낸다.

## Observations / 관찰 결과

평가 결과는 답변 문장만이 아니라 후보 문서, 선택 문맥, 인용, 권한 조건과 함께 남겨야 한다. 그래야 같은 오류를 문서·검색·생성·권한의 어느 층에서 고칠지 판단할 수 있다.

## Interpretation / 해석

내 해석으로 좋은 인용은 답변을 정답으로 만들어 주는 스티커가 아니라, 독자가 원문으로 돌아가 범위·버전·예외를 검토할 수 있게 하는 감사 경로다.

## Limitations / 한계

- 인용 충실성 평가는 사람 검토가 필요할 수 있다.
- 접근 권한에 따라 같은 답변이라도 인용 표시 방식이 달라질 수 있다.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Karpukhin et al., Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: 제목별 핵심 개념, 비교·평가 절차, 근거 연결을 보강한 내부 검토용 개정본. `published: false`; 발행 일정은 정하지 않았다.
