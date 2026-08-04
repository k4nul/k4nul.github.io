---
layout: single
title: "좋은 RAG는 검색 이전에 문서 품질에서 결정된다"
description: "RAG의 검색 품질을 높이기 전에 확인해야 할 문서 원본, 최신성, 구조, 메타데이터, 권한, 갱신 기준을 정리한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: document-quality-before-retrieval
section: development
topic_key: ai
categories: AI
tags: [ai, llm, rag, document-quality, chunking, retrieval]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

RAG 프로젝트는 embedding 모델, vector DB, chunk 크기부터 논의하기 쉽다. 하지만 검색 시스템에 들어가는 문서가 오래되었거나, 같은 정책의 여러 버전이 섞여 있거나, 제목·작성일·권한 같은 메타데이터가 없다면 좋은 검색 알고리즘도 신뢰할 수 있는 답변을 만들기 어렵다.

이 글의 주장은 단순하다. **검색 품질은 색인 이후에만 결정되지 않는다.** 무엇을 원본 문서로 인정할지, 문서가 현재 유효한지, 문서 구조가 보존되었는지, 누가 접근할 수 있는지가 먼저 정해져야 한다. chunking은 그 다음 단계다.

## Document Info / Environment

- 작성일: 2026-08-01
- 검증 기준일: 2026-08-01
- 문서 성격: design guide
- 테스트 환경: 실행 테스트 없음. 공개 RAG 설계 문서와 NIST의 생성형 AI 위험 관리 지침을 기준으로 작성했다.
- 테스트 버전: 특정 문서 파서, OCR, 벡터 DB, 모델을 고정하지 않았다.
- 출처 등급: 공식 아키텍처 문서, 정부 기술 지침, 원 논문

## Problem Statement / 문제 정의

사용자는 “문서에 답이 있는데 AI가 못 찾는다”고 말할 수 있다. 이 말에는 적어도 네 가지 서로 다른 상황이 들어 있다.

1. 답이 있는 최신 문서가 아예 색인되지 않았다.
2. 최신 문서와 폐기된 문서가 함께 색인되어 서로 다른 답을 준다.
3. 표·제목·예외 조항 같은 구조가 텍스트 변환 중 사라져 문장이 원래 뜻을 잃었다.
4. 답이 있는 문서는 검색됐지만, 사용자의 권한에 맞지 않아 보여 주면 안 된다.

이 중 어느 것도 embedding 모델만 바꿔 해결되지 않는다. 검색 이전의 문서 준비 단계는 데이터 원본, 갱신, 권한, 구조 보존을 다루는 운영 문제다.

## Verified Facts / 확인된 사실

- Microsoft의 RAG chunking 설계 문서는 chunking을 의미적으로 관련 있는 내용을 가진 적절한 크기의 단위로 문서를 나누는 작업으로 설명한다. 같은 문서는 문서 전체나 지나치게 큰 chunk를 모델에 넣으면 비용이 커지고 token 한도를 압박하며, 질문과 관련 없는 정보가 들어갈 경우 부정확하거나 무관한 응답이 나올 수 있다고 설명한다. 반대로 너무 작은 chunk는 질문에 답할 충분한 문맥을 잃을 수 있다.
  근거: [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)

- 같은 문서는 chunking 전략이 문서의 유형·구조·내용과 비용·품질·처리량 요구에 따라 달라질 수 있으며, 하나의 전략을 모든 문서에 기계적으로 적용하기보다 실험이 필요하다고 설명한다.
  근거: [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)

- NIST의 Generative AI Profile은 AI 생애주기의 서로 다른 단계에서 사용되는 데이터의 정확성, 대표성, 관련성, 적합성을 검토하고 문서화하라고 제안한다. 또한 생성형 AI 출력의 출처와 인용을 배포 전 평가와 지속적인 모니터링에서 검토할 것을 제안한다.
  근거: [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

- RAG 원 논문은 문서 인덱스를 비모수적 메모리로 사용하고, 문서 청크를 검색 대상 단위로 다룬다. 이는 문서가 검색 가능한 단위로 준비되어야 생성 단계에서 근거로 쓰일 수 있음을 보여 준다.
  근거: [Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*](https://arxiv.org/abs/2005.11401)

이 출처들은 특정 제품의 기본 설정이 모든 조직에 맞는다고 말하지 않는다. 오히려 문서 유형과 의도한 질문을 기준으로 원본·분할·평가 기준을 정해야 한다는 근거다.

## Reproduction Steps / 재현 순서

RAG 색인 전에 문서 집합을 다음 체크리스트로 분류한다.

### 1. 원본과 최신성

- 이 문서는 공식 원본인가, 복사본·요약본·개인 메모인가?
- 작성일과 마지막 검토일이 있는가?
- 같은 주제의 문서가 충돌할 때 우선순위가 정해져 있는가?
- 폐기된 문서를 삭제하지 못한다면 `status: archived` 같은 상태를 명시하고 검색에서 제외할 수 있는가?

### 2. 구조와 의미

- 문서의 제목, 섹션, 표, 각주, 예외 조항, 링크가 텍스트 변환 뒤에도 식별되는가?
- 표의 행·열 관계가 문장으로 바뀌며 의미를 잃지 않았는가?
- 스캔 PDF의 OCR 오류를 확인했는가?
- 문단을 나눌 때 상위 제목·문서명·버전 같은 맥락을 함께 보존하는가?

### 3. 메타데이터와 권한

- 최소한 문서 ID, 제목, 원본 경로, 버전 또는 갱신일, 소유자, 상태를 붙일 수 있는가?
- 사용자·조직·역할 기준의 접근 범위를 검색 단계에서 필터링할 수 있는가?
- 답변 인용이 원본 문서와 정확한 위치로 돌아갈 수 있는가?

### 4. 평가용 질문

- 실제 사용자가 물을 질문과, 답을 찾으면 안 되는 질문을 함께 모았는가?
- 각 질문에 기대 문서, 최신 버전, 허용되는 답변 범위를 기록했는가?
- 문서가 업데이트됐을 때 재색인·재평가가 필요한 항목을 정했는가?

## Observations / 관찰 결과

문서 품질을 먼저 확인하면 RAG 문제의 우선순위가 달라진다.

| 관찰된 증상 | 먼저 확인할 원인 | 성급한 대응 |
| --- | --- | --- |
| 오래된 정책을 인용한다 | 문서 상태·갱신·색인 삭제 | 모델 교체 |
| 표의 조건을 누락한다 | 원본 구조·파싱·chunk 경계 | prompt만 길게 작성 |
| 질문마다 답이 달라진다 | 중복 문서·서로 다른 버전 | top-k 수만 증가 |
| 권한 밖 문서를 언급한다 | 검색 전 권한 필터·메타데이터 | 답변 후 마스킹만 추가 |
| 근거 링크가 무의미하다 | chunk와 원본 위치 연결 | URL 형식만 강제 |

이 표는 문서 품질 문제가 모델 문제가 아니라는 뜻이 아니다. 다만 검색 단계에 유효한 근거가 없으면, 생성 모델의 출력 형식을 바꿔도 근본 원인을 해결하기 어렵다는 뜻이다.

## Interpretation / 해석

내 해석으로는 RAG의 문서 전처리는 단순한 ETL 작업이 아니라 **지식의 책임 범위를 정하는 과정**이다. ‘무엇이 사실인가’에 대한 조직의 원본을 정하지 않은 채 문서를 모으면, 검색 시스템은 빠르게 모순된 답변을 제공할 수 있다.

실무에서 가장 작은 시작점은 복잡한 chunk 알고리즘이 아니라 다음 다섯 항목이다.

1. 공식 원본 문서 목록
2. 문서별 소유자와 검토 주기
3. 최신/폐기 상태
4. 권한 필터에 쓸 메타데이터
5. 실제 질문과 기대 근거가 들어 있는 평가 세트

이 다섯 가지가 있는 상태에서 chunking과 검색 전략을 바꾸면, 무엇이 개선됐는지 측정할 수 있다. 없으면 ‘답변이 좋아진 것 같다’는 인상만 남는다.

## Limitations / 한계

- 이 글은 문서 포맷별 최적 chunk 크기나 overlap 값을 제시하지 않는다. 값은 문서·질문·모델·비용 제약을 포함한 실험으로 정해야 한다.
- 문서 품질이 좋아도 모호한 질문, 권한 정책의 누락, 모델의 과잉 추론 때문에 잘못된 답이 나올 수 있다.
- NIST 문서는 위험 관리의 권고·가이드이며, 개별 조직의 법적 준수 여부를 보증하지 않는다.
- 고위험 또는 개인정보가 포함된 문서 집합은 별도의 보안·법무·데이터 거버넌스 검토가 필요하다.

## References / 참고자료

- [Microsoft Learn, RAG chunking phase](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-chunking-phase)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*](https://arxiv.org/abs/2005.11401)

## Change Log / 변경 이력

- 2026-08-01: 내부 검토용 초안 작성. 게시 일정과 공개 상태는 확정하지 않았다.
