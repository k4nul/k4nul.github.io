---
layout: single
title: "RAG·Fine-tuning·Tool calling·Agent는 언제 각각 써야 하는가"
description: "최신 문서 근거, 반복 행동, 정확한 시스템 조회, 다단계 작업의 경계로 RAG·fine-tuning·tool calling·agent를 선택하는 기준을 제시한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: choosing-rag-finetuning-tools-agents
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

이 네 용어는 경쟁 제품 이름이 아니라 해결하려는 문제 경계가 다르다. 선택은 “모델을 더 똑똑하게”가 아니라 사실의 원본, 행동의 위험, 형식의 반복성, 운영 통제를 기준으로 해야 한다.

## Document Info / Environment

- 작성일·검증 기준일: 2026-08-01
- 문서 성격: 개념·설계 가이드
- 직접 실행 테스트: 없음. 인용한 연구와 공식 문서로 개념을 검토했다.
- 공급자 기능·기본값은 변경될 수 있으므로 링크는 발행 전 다시 확인한다.

## Problem Statement / 문제 정의

RAG·Fine-tuning·Tool calling·Agent는 언제 각각 써야 하는가라는 질문은 모델 하나의 기능으로 답할 수 없다. 문서 원본, 검색 후보, 사용자 권한, 생성 계약을 분리해 관찰해야 한다.

## Verified Facts / 확인된 사실

- RAG는 외부 문서 인덱스를 생성 모델과 결합하는 접근이다. [Lewis et al.](https://arxiv.org/abs/2005.11401)
- OpenAI의 retrieval 가이드는 vector store를 검색용 데이터 구조로 설명한다. [OpenAI Retrieval](https://developers.openai.com/api/docs/guides/retrieval)
- OWASP는 LLM 애플리케이션에서 과도한 권한과 민감정보 노출을 주요 위험으로 다룬다. [OWASP](https://genai.owasp.org/llm-top-10/)

- RAG: 자주 바뀌는 문서에서 근거를 찾아 설명할 때. 원본·권한·인용을 운영해야 한다.
- Fine-tuning: 반복되는 문체, 분류, 형식 같은 모델 행동을 학습시킬 때. 최신 사실 저장소의 대체물은 아니다.
- Tool calling: 주문 조회, 계산, 예약처럼 정확한 외부 시스템 결과나 실제 행위가 필요할 때. 입력 검증과 최소 권한이 핵심이다.
- Agent: 여러 단계의 계획·도구 사용·상태 관리가 필요한 때. 각 tool의 권한·승인·중단 조건을 별도 설계해야 한다.

## Reproduction Steps / 재현 순서

1. 질문이 최신 문서 근거, 정확한 시스템 값, 반복 형식, 다단계 작업 중 무엇을 요구하는지 분류한다.
2. 각 후보에 대해 사실 원본, 실패 비용, 사용자 승인, 로그, 평가 방법을 기록한다.
3. 가장 작은 조합부터 평가한다. 예: RAG 답변에 agent를 붙이기 전 retrieval과 no-answer를 검증한다.
4. 실제 변경 tool에는 dry-run, 입력 검증, 승인, 감사 로그, 중단 권한을 포함한다.

## Observations / 관찰 결과

평가 결과는 답변 문장만이 아니라 후보 문서, 선택 문맥, 인용, 권한 조건과 함께 남겨야 한다. 그래야 같은 오류를 문서·검색·생성·권한의 어느 층에서 고칠지 판단할 수 있다.

## Interpretation / 해석

내 해석으로 기술 선택은 하나만 고르는 문제가 아니다. RAG+tool calling처럼 결합할 수 있지만, 결합할수록 실패 경계와 운영 비용도 늘어난다.

## Limitations / 한계

- fine-tuning과 agent의 정의·기능은 공급자마다 다를 수 있다.
- 고위험·규제 분야는 추가적인 도메인 검토가 필요하다.

## References / 참고자료

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [Karpukhin et al., Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-02: 제목별 핵심 개념, 비교·평가 절차, 근거 연결을 보강한 내부 검토용 개정본. `published: false`; 발행 일정은 정하지 않았다.
