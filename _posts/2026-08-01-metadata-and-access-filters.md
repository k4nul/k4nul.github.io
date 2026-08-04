---
layout: single
title: "Metadata filtering과 권한 필터: 검색되면 안 되는 문서"
description: "RAG 검색 이전에 권한·테넌트·문서 상태를 필터링해야 하는 이유와 검증 절차를 정리한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: metadata-and-access-filters
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

검색 품질은 관련 문서를 찾는 것뿐 아니라 사용자가 볼 수 없는 문서를 후보에 넣지 않는 것까지 포함한다. 권한 필터는 생성 이후 마스킹이 아니라 검색 이전의 경계여야 한다.

## Document Info / Environment

- 작성일·검증 기준일: 2026-08-01
- 문서 성격: 개념·설계 가이드
- 직접 실행 테스트: 없음. 인용한 연구와 공식 문서로 개념을 검토했다.
- 공급자 기능·기본값은 변경될 수 있으므로 링크는 발행 전 다시 확인한다.

## Problem Statement / 문제 정의

Metadata filtering과 권한 필터: 검색되면 안 되는 문서라는 질문은 모델 하나의 기능으로 답할 수 없다. 문서 원본, 검색 후보, 사용자 권한, 생성 계약을 분리해 관찰해야 한다.

## Verified Facts / 확인된 사실

- NIST AI 600-1은 생성형 AI의 data privacy와 information integrity 위험을 다루며, 상황별 위험 관리가 필요하다고 설명한다. [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- OWASP LLM Top 10은 민감정보 노출을 LLM 애플리케이션의 주요 위험으로 분류한다. [OWASP](https://genai.owasp.org/llm-top-10/)

- metadata에는 문서 소유자, 테넌트, 역할, 분류, 상태, 버전, 유효 기간처럼 검색 범위를 결정하는 속성이 들어갈 수 있다.
- 질의 시점의 사용자·조직·역할을 신뢰할 수 있는 인가 시스템에서 계산하고, 그 결과를 retrieval filter에 적용해야 한다.
- 모델에게 “비밀을 말하지 말라”고 지시하는 것은 인가를 대체하지 못한다. 권한 밖 청크가 문맥에 들어가면 생성 단계에서 이미 노출 위험이 생긴다.

## Reproduction Steps / 재현 순서

1. 테넌트·역할·문서 상태가 다른 테스트 계정을 준비한다.
2. 같은 질문을 각 계정으로 실행해 후보 목록, 선택 문맥, 인용이 허용 범위 안인지 확인한다.
3. allow case뿐 아니라 deny case와 권한 변경 직후의 동기화 사례를 테스트한다.
4. 필터 누락은 보안 사건 후보로 기록하고 답변 품질 지표와 분리한다.

## Observations / 관찰 결과

평가 결과는 답변 문장만이 아니라 후보 문서, 선택 문맥, 인용, 권한 조건과 함께 남겨야 한다. 그래야 같은 오류를 문서·검색·생성·권한의 어느 층에서 고칠지 판단할 수 있다.

## Interpretation / 해석

내 해석으로 접근 제어는 검색 기능의 옵션이 아니라 지식 원본에서 답변까지 이어지는 보안 계약이다. 기본값은 넓게 검색한 뒤 숨기는 것이 아니라, 허용된 범위만 검색하는 것이다.

## Limitations / 한계

- ACL 모델과 색인 갱신 방식은 조직마다 다르다.
- 법적 보존·감사 요구는 관할과 데이터 유형에 따라 별도 검토가 필요하다.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Karpukhin et al., Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: 제목별 핵심 개념, 비교·평가 절차, 근거 연결을 보강한 내부 검토용 개정본. `published: false`; 발행 일정은 정하지 않았다.
