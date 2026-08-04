---
layout: single
title: "RAG가 틀리는 6가지 패턴: 못 찾음·잘못 찾음·과잉 추론·낡은 문서"
description: "RAG의 문서 누락·오검색·조건 오독·과잉 추론·낡은 문서·권한 위반을 진단하는 분류를 제시한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: six-rag-failure-patterns
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

RAG 오류는 하나의 “환각”으로 뭉뚱그리면 고칠 수 없다. 아래 여섯 패턴은 문서·검색·생성·권한 문제를 분리해 조사하기 위한 분류다.

## Document Info / Environment

- 작성일·검증 기준일: 2026-08-01
- 문서 성격: 개념·설계 가이드
- 직접 실행 테스트: 없음. 인용한 연구와 공식 문서로 개념을 검토했다.
- 공급자 기능·기본값은 변경될 수 있으므로 링크는 발행 전 다시 확인한다.

## Problem Statement / 문제 정의

RAG가 틀리는 6가지 패턴: 못 찾음·잘못 찾음·과잉 추론·낡은 문서라는 질문은 모델 하나의 기능으로 답할 수 없다. 문서 원본, 검색 후보, 사용자 권한, 생성 계약을 분리해 관찰해야 한다.

## Verified Facts / 확인된 사실

- RAG는 검색된 외부 문서를 생성과 결합한다. [Lewis et al.](https://arxiv.org/abs/2005.11401)
- NIST AI 600-1은 생성형 AI에서 정보 무결성, 데이터 품질, 상황별 위험 관리를 강조한다. [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

- 1. 못 찾음: 정답 문서가 corpus 또는 top-k 후보에 없다.
- 2. 잘못 찾음: 무관하거나 비슷한 문서가 상위에 온다.
- 3. 조건 오독: 정답 문서가 있지만 적용 범위·예외·날짜를 놓친다.
- 4. 과잉 추론: 문서가 말하지 않은 결론을 생성한다.
- 5. 낡음/충돌: 폐기 문서나 상충 원본을 우선한다.
- 6. 권한 위반: 허용되지 않은 문서가 후보·문맥·인용에 나타난다.

## Reproduction Steps / 재현 순서

1. 사건마다 질문, 사용자 권한, corpus 버전, top-k, 선택 문맥, 답변, 인용을 보존한다.
2. 정답 원문이 corpus·top-k·selected context 중 어디까지 도달했는지 확인한다.
3. 여섯 패턴 중 하나를 주원인으로, 필요한 경우 보조 원인으로 기록한다.
4. 수정 후 같은 사건을 회귀 세트에 넣고 재실행한다.

## Observations / 관찰 결과

평가 결과는 답변 문장만이 아니라 후보 문서, 선택 문맥, 인용, 권한 조건과 함께 남겨야 한다. 그래야 같은 오류를 문서·검색·생성·권한의 어느 층에서 고칠지 판단할 수 있다.

## Interpretation / 해석

내 해석으로 이 분류의 목적은 실패 이름을 붙이는 데 있지 않다. 소유자를 문서 관리, retrieval, 생성 계약, 권한 제어 중 어디에 둘지 정하고 재발을 측정하는 데 있다.

## Limitations / 한계

- 한 사건에 둘 이상의 원인이 있을 수 있다.
- 분류표는 도메인별 위험 분석과 보안 사고 대응을 대체하지 않는다.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Karpukhin et al., Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: 제목별 핵심 개념, 비교·평가 절차, 근거 연결을 보강한 내부 검토용 개정본. `published: false`; 발행 일정은 정하지 않았다.
