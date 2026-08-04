---
layout: single
title: "Context window와 memory는 같은 것이 아니다"
description: "현재 요청에 포함된 문맥, 대화 밖에 저장한 상태, 외부 검색 문서를 구분해 장기 AI 기능의 정보 흐름을 설계하는 기준을 정리한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: context-window-is-not-memory
section: development
topic_key: ai
categories: AI
tags: [ai, llm, context-window, memory, rag, agents]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

AI 제품에서 “기억한다”는 말은 최소 세 가지를 섞어 부르기 쉽다. 첫째는 모델이 **이번 요청에서 참고할 수 있는 context window**다. 둘째는 다음 요청에도 다시 불러올 수 있도록 애플리케이션이나 도구가 보관한 **외부 상태(memory)** 다. 셋째는 필요할 때 문서 저장소에서 찾아오는 **검색 결과**다.

셋은 모두 답변에 정보를 넣을 수 있지만, 저장 위치·수명·갱신 방식·권한 검사의 위치가 다르다. 이 글은 ‘긴 context window가 있으니 memory는 필요 없다’는 단순화를 피하고, 어떤 정보를 어디에 둘지 판단하는 기준을 제안한다.

## Document Info / Environment

- 작성일: 2026-08-01
- 검증 기준일: 2026-08-01
- 문서 성격: concept analysis
- 테스트 환경: 실행 테스트 없음. 공개 API 문서의 context window 정의와 RAG 원 논문을 기준으로 개념을 비교했다.
- 테스트 버전: 제품별 context 크기와 memory 기능은 변경될 수 있으므로 수치 비교를 하지 않았다.
- 출처 등급: 공식 개발자 문서, 원 논문

## Problem Statement / 문제 정의

긴 대화에서 모델이 앞선 내용을 참조했다고 해서 그 정보가 영구히 보관되었다고 볼 수는 없다. 반대로 별도 저장소에 사용자의 선호를 기록했다고 해서 다음 요청에 자동으로 전달되는 것도 아니다. 애플리케이션이 그 데이터를 읽고, 관련성을 판단하고, 요청에 포함하거나 도구를 통해 조회해야 모델이 사용할 수 있다.

이 구분이 빠지면 다음과 같은 설계 문제가 생긴다.

- 대화 이력을 무한히 넣어 비용과 관련 없는 문맥을 키운다.
- 장기 상태를 채팅 기록에만 의존해 세션이 바뀌면 작업이 끊긴다.
- 권한이 다른 문서를 같은 ‘기억’으로 묶어 잘못 노출한다.
- 요약본을 원문처럼 취급해 세부 근거를 잃는다.

## Verified Facts / 확인된 사실

- Anthropic의 공개 문서는 context window를 모델이 응답을 생성할 때 참조할 수 있는 모든 텍스트로 정의하며, 학습 데이터 전체와는 구분한다. 같은 문서는 system prompt, 메시지, tool result, 이미지·문서, 도구 정의와 생성 출력이 context 사용량에 포함된다고 설명한다.
  근거: [Anthropic Context windows](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)

- OpenAI의 공개 프롬프트 가이드는 모델이 생성 요청에서 고려할 수 있는 데이터의 한도를 context window라고 설명하며, 관련 문맥을 요청에 추가하는 방식으로 벡터 데이터베이스 조회나 file search를 예시로 든다.
  근거: [OpenAI Prompt engineering guide](https://developers.openai.com/api/docs/guides/prompt-engineering)

- RAG 원 논문은 생성 모델의 파라미터 메모리와 문서 인덱스라는 비모수적 메모리를 결합하는 구조를 설명한다. 즉 외부 문서 인덱스는 모델의 현재 요청 문맥과 같은 저장소가 아니라, 검색을 거쳐 생성에 제공되는 별도 구성 요소다.
  근거: [Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*](https://arxiv.org/abs/2005.11401)

따라서 context window, application memory, retrieval index는 서로 대체 관계가 아니라 연결 방식이 다른 구성 요소다. 특정 제품이 ‘memory’라는 기능명을 쓰더라도, 실제로 무엇을 저장하고 어떤 조건에서 다시 요청에 포함하는지는 제품 문서와 설계 구현을 따로 확인해야 한다.

## Reproduction Steps / 재현 순서

아래처럼 하나의 업무를 세 종류의 정보로 나눠 본다. 예시는 설계 연습이며, 특정 공급자 기능을 실행한 결과는 아니다.

| 정보 | 예시 | 권장 위치 | 다음 요청에 넣는 방법 |
| --- | --- | --- | --- |
| 현재 작업 문맥 | 사용자가 지금 수정 중인 문단, 직전 도구 결과 | context window | 현재 요청에 직접 포함 |
| 장기 작업 상태 | 완료한 단계, 결정 사항, 미해결 이슈 | 상태 파일·DB·issue | 관련 항목을 읽어 요약 또는 원문으로 주입 |
| 지식 문서 | 정책, 매뉴얼, 기술 문서 | 문서 저장소·검색 인덱스 | 질문과 권한에 맞는 문서를 검색 후 주입 |

설계 절차는 다음과 같다.

1. 정보가 ‘이번 응답이 끝나면 사라져도 되는가’를 묻는다.
2. 다음 요청에서도 필요하다면, 채팅 이력이 아닌 외부 저장 위치와 갱신 주체를 정한다.
3. 모든 저장 정보를 요청에 넣지 말고, 현재 질문과 권한에 맞는 항목만 선택한다.
4. 요약을 넣었다면 원문 위치와 마지막 갱신 시각도 함께 보관한다.
5. 모델의 답변이 아니라 저장소의 원문과 상태 기록을 최종 근거로 삼는다.

## Observations / 관찰 결과

이 구분을 적용하면 ‘메모리가 안 된다’는 문제를 더 작게 쪼갤 수 있다.

- 앞선 대화를 잊은 것처럼 보인다: context에 과거 대화가 실제로 포함되었는지, 요약·압축 과정에서 무엇이 빠졌는지 확인한다.
- 예전 결정과 다른 답을 한다: 장기 상태의 단일 원본이 있는지, 최신 상태를 조회했는지 확인한다.
- 관련 문서를 못 찾는다: 문서가 색인되었는지, 검색 조건과 메타데이터 필터가 맞는지 확인한다.
- 다른 사용자의 정보가 섞인다: 저장 단위와 검색 단계에서 테넌트·사용자·역할 권한이 함께 필터링되는지 확인한다.

특히 context는 클수록 자동으로 좋아지는 버퍼가 아니다. Anthropic 문서도 문맥이 늘면 정확성과 회상이 저하될 수 있으므로, 얼마나 많이 넣는가만큼 무엇을 넣는가가 중요하다고 설명한다. 이 점은 제품별 한도 수치와 별개로 설계에서 확인해야 할 원칙이다.

## Interpretation / 해석

내 해석으로는 장기 AI 기능의 memory는 ‘모델의 기억력’보다 **애플리케이션의 상태 관리 문제**에 가깝다. 모델은 현재 요청에 제공된 정보를 바탕으로 응답한다. 그러므로 장기 작업을 이어 가려면 사람이 읽을 수 있고, 갱신 규칙이 있고, 권한을 검사할 수 있는 외부 상태가 필요하다.

간단한 운영 원칙은 다음과 같다.

- 짧고 현재적인 정보는 context에 둔다.
- 다음 실행에도 필요한 결정은 파일·DB·issue 같은 외부 상태에 둔다.
- 넓은 문서 집합은 검색 대상으로 두고 필요할 때만 가져온다.
- 어떤 정보든 원문 위치·갱신 시각·권한을 잃지 않게 한다.

이 원칙은 특정 모델의 context window가 커져도 사라지지 않는다. 긴 입력 한도는 더 많은 정보를 한 번에 처리할 수 있게 하지만, 어떤 정보의 원본이 무엇이고 누가 변경했는지까지 해결하지는 않는다.

## Limitations / 한계

- 이 글은 제품별 memory 기능을 비교하거나, 특정 API의 저장 정책을 보장하지 않는다.
- context window의 실제 크기, 과금, 압축 방식은 모델·공급자·요청 형식에 따라 달라질 수 있다.
- 외부 상태 저장과 검색 인덱스의 보안 요구는 조직의 데이터 분류·법적 의무·접근 제어 모델에 따라 달라진다.
- 이 글의 표는 설계 판단을 위한 단순화이며, 실제 시스템에서는 캐시·감사 로그·백업·삭제 정책도 추가로 필요하다.

## References / 참고자료

- [Anthropic Context windows](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)
- [OpenAI Prompt engineering guide](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*](https://arxiv.org/abs/2005.11401)

## Change Log / 변경 이력

- 2026-08-01: 내부 검토용 초안 작성. 게시 일정과 공개 상태는 확정하지 않았다.
