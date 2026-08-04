---
layout: single
title: "RAG란 무엇이고, LLM 단독 사용과 무엇이 다른가"
description: "외부 문서 검색 결과를 생성에 연결하는 RAG의 구조, 강점, 한계를 LLM 단독 사용과 비교해 정리한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: what-is-rag
section: development
topic_key: ai
categories: AI
tags: [ai, llm, rag, retrieval, vector-search, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

RAG(Retrieval-Augmented Generation)는 언어 모델의 답변을 만들기 전에 관련 외부 문서를 검색하고, 그 결과를 모델 입력 문맥에 넣어 생성하도록 구성하는 방식이다. 핵심은 ‘모델에게 새 지식을 주입했다’는 표현보다, **질문 시점에 선택한 문서를 답변 조건으로 제공한다**는 데 있다.

RAG는 최신 문서나 조직 내부 문서를 답변에 반영하기 위한 유용한 구조지만, 정확성 보증 장치가 아니다. 검색 결과가 틀리거나 오래되었거나 권한 밖 문서라면, 생성 모델은 그 잘못된 문맥을 바탕으로도 그럴듯한 답을 만들 수 있다. 이 글은 RAG를 LLM 단독 사용, 데이터베이스 조회, fine-tuning과 구분해 언제 선택할지 판단하는 출발점을 제공한다.

## Document Info / Environment

- 작성일: 2026-08-01
- 검증 기준일: 2026-08-01
- 문서 성격: concept analysis
- 테스트 환경: 실행 테스트 없음. RAG 원 논문과 공개 API 문서를 기준으로 구조를 정리했다.
- 테스트 버전: 특정 벡터 DB, 모델, embedding 모델, 관리형 검색 제품을 고정하지 않았다.
- 출처 등급: 원 논문, 공식 개발자 문서

## Problem Statement / 문제 정의

LLM은 사용자가 요청에 제공하지 않은 최신 조직 문서나 특정 고객의 현재 상태를 자동으로 확인하지 않는다. 이때 흔한 해법은 문서를 모두 프롬프트에 붙여 넣거나, 모델이 알아서 알고 있을 것이라 기대하는 것이다. 첫 방법은 문서가 늘수록 비용·한도·관련성 문제가 생기고, 두 번째는 근거와 최신성을 확인할 수 없다.

RAG는 문서 전체를 항상 넣는 대신 다음 흐름을 만든다.

```text
질문 → 관련 문서/청크 검색 → 선택된 문맥 + 질문 → LLM 생성 → 답변과 근거 제시
```

이 흐름에서 모델은 최종 답변을 만들지만, 검색 시스템은 어떤 근거 후보를 제공할지 결정한다. 따라서 RAG의 실패는 ‘LLM이 틀렸다’ 하나로 끝내기보다, 문서·색인·검색·생성·인용의 어느 단계에서 문제가 생겼는지 나눠 봐야 한다.

## Verified Facts / 확인된 사실

- Lewis 등은 RAG를 사전학습된 seq2seq 모델의 파라미터 메모리와, 신경 검색기로 접근하는 비모수적 메모리(문서 인덱스)를 결합한 구조로 제시했다. 논문은 지식 집약적 작업에서 외부 지식 접근과 provenance, 세계 지식 갱신이 과제라고 설명한다.
  근거: [Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*](https://arxiv.org/abs/2005.11401)

- OpenAI의 프롬프트 가이드는 벡터 데이터베이스를 조회한 텍스트나 file search 결과를 생성 요청의 추가 문맥으로 넣는 방식을 RAG라고 설명한다.
  근거: [OpenAI Prompt engineering guide](https://developers.openai.com/api/docs/guides/prompt-engineering)

- OpenAI Retrieval API 문서는 vector store를 데이터의 인덱스로 설명하고 semantic search를 수행하는 방법을 다룬다. 즉 RAG에서 vector store는 답변 그 자체가 아니라 검색을 위한 데이터 구조다.
  근거: [OpenAI Retrieval guide](https://developers.openai.com/api/docs/guides/retrieval)

이 사실들은 RAG가 ‘문서가 있으면 항상 정답을 보장하는 기능’이라는 뜻은 아니다. RAG 원 논문도 특정 데이터셋과 실험 설정에서의 결과를 제시했으며, 실제 조직 문서의 품질·권한·갱신·질문 분포까지 대신 검증하지는 않는다.

## Reproduction Steps / 재현 순서

RAG 도입 전에는 API부터 호출하기보다 다음 질문으로 문제를 분류한다.

1. 답변에 필요한 사실은 고정된 레코드인가, 사람이 읽는 문서인가, 아니면 추론·요약이 필요한가?
2. 문서의 소유자, 갱신 시각, 접근 권한을 확인할 수 있는가?
3. 질문마다 관련 문서가 몇 개 정도인지, 그리고 검색 실패를 사람이 검토할 수 있는지 정했는가?
4. 답변에 어떤 문서가 쓰였는지 사용자가 확인할 수 있도록 문서명·경로·버전·인용을 남길 수 있는가?
5. 답을 못 찾은 경우에는 ‘모르겠다’고 답하거나 사람에게 넘기는 흐름이 있는가?

선택 기준을 간단히 정리하면 다음과 같다.

| 문제 | 우선 검토할 방식 | 이유 |
| --- | --- | --- |
| 주문 상태·재고·계약 금액처럼 정확한 현재 값 | 업무 DB/API 조회 | 검색된 자연어 문서보다 원본 레코드가 근거에 가깝다. |
| 매뉴얼·정책·회의록에서 관련 근거를 찾아 설명 | RAG | 질문별로 관련 문서를 찾아 모델 입력에 제공할 수 있다. |
| 문체·분류 기준·반복 형식을 바꾸는 작업 | fine-tuning 또는 규칙/프롬프트 | 외부 문서 검색만으로 해결되지 않는 행동·형식 문제일 수 있다. |
| 외부 시스템에서 계산·예약·변경을 수행 | tool calling + 권한·검증 | 답변 생성이 아니라 실제 행위와 승인 경계가 핵심이다. |

## Observations / 관찰 결과

RAG 품질을 볼 때 ‘답변이 자연스러운가’만 보면 원인을 놓치기 쉽다. 최소한 아래 두 결과를 분리해서 기록할 필요가 있다.

- **retrieval 결과:** 질문에 실제로 답할 수 있는 문서·청크가 상위 결과에 있었는가?
- **generation 결과:** 제공된 문맥만으로 답할 수 있는 범위에서, 모델이 과장·생략·오독 없이 답했는가?

예를 들어 답변이 틀렸을 때 검색 결과에 정답 문서가 없었다면, 프롬프트를 고치는 일보다 문서 수집·분할·검색 조건을 먼저 봐야 한다. 반대로 정답 문서가 있었는데 모델이 다른 결론을 냈다면, 입력 구성·출력 형식·인용 연결·생성 모델의 동작을 조사해야 한다.

## Interpretation / 해석

내 해석으로는 RAG의 가치는 ‘모델의 머릿속을 최신화한다’보다 **답변의 근거 후보를 운영 가능한 문서 집합으로 분리한다**는 데 있다. 문서 원본을 고치고, 색인을 갱신하고, 접근 권한을 바꾸고, 검색 로그를 검토하는 일이 가능해지기 때문이다.

그러나 RAG를 도입해도 다음 책임은 사라지지 않는다.

- 어떤 문서를 지식 원본으로 인정할 것인가
- 문서가 오래되거나 모순될 때 무엇을 우선할 것인가
- 사용자가 볼 수 없는 문서를 어떻게 걸러 낼 것인가
- 답변이 어떤 문서에 기대고 있는지 어떻게 보여 줄 것인가
- 검색 실패를 어떻게 측정하고 개선할 것인가

RAG는 모델 단독 사용의 부족한 근거를 보완할 수 있지만, 문서 거버넌스와 평가를 대신하지는 않는다.

## Limitations / 한계

- 이 글은 특정 RAG 프레임워크나 벡터 데이터베이스의 성능을 비교하지 않는다.
- RAG는 이미지, 표, 스캔 PDF, 코드, 여러 언어가 섞인 문서에서 별도 전처리와 평가가 필요할 수 있다.
- 출처를 표시해도, 인용 문서가 질문에 답하는지와 모델의 해석이 맞는지는 별도로 검토해야 한다.
- 개인·민감정보가 포함된 문서를 검색 대상으로 만들 때는 데이터 분류, 보관, 접근 제어, 감사 요구를 별도로 검토해야 한다.

## References / 참고자료

- [Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*](https://arxiv.org/abs/2005.11401)
- [OpenAI Prompt engineering guide](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [OpenAI Retrieval guide](https://developers.openai.com/api/docs/guides/retrieval)

## Change Log / 변경 이력

- 2026-08-01: 내부 검토용 초안 작성. 게시 일정과 공개 상태는 확정하지 않았다.
