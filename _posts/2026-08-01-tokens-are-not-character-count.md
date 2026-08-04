---
layout: single
title: "토큰은 글자 수가 아니다: 입력 한도를 읽는 방법"
description: "토큰과 문자·단어·바이트의 차이를 구분하고 AI 입력 예산을 안전하게 설계하는 기준을 정리한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: tokens-are-not-character-count
section: development
topic_key: ai
categories: AI
tags: [ai, llm, tokens, context-window, prompt-engineering]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

AI 기능의 입력 한도를 문자 수로만 계산하면 예상과 다른 실패를 만난다. 언어 모델의 처리 단위인 토큰은 문자, 단어, 바이트와 일대일로 대응하지 않는다. 같은 문장도 사용하는 토크나이저, 공백·구두점, 언어와 표기 방식에 따라 다른 토큰 수가 될 수 있다. 따라서 입력 예산은 화면의 글자 수가 아니라 실제 요청에 포함되는 토큰 단위로 확인해야 한다.

## Document Info / Environment

- 작성일: 2026-08-01
- 검증 기준: 공식 개발자 문서와 원 논문
- 문서 성격: concept analysis
- 테스트 환경: 직접 실행 실험 없음.
- 범위: 특정 모델의 토큰 한도, 가격, 성능을 비교하지 않는다.

## Problem Statement / 문제 정의

“2,000자까지 입력 가능”이라는 UI 안내와 API의 context window는 같은 약속이 아니다. 시스템 지시문, 대화 이력, 도구 정의, 검색 문서, 출력 예약분도 요청에 포함될 수 있다. 글자 수만 제한하면 어떤 요청은 한도를 넘고, 어떤 요청은 필요한 출력 공간을 남기지 못한다. 특히 다국어 서비스에서는 문자 수 기반 규칙이 언어별로 불균등하게 작동할 수 있다.

## Verified Facts / 확인된 사실

Transformer는 텍스트를 attention 기반 모델이 처리할 수 있는 순서화된 입력으로 다룬다([Vaswani et al.](https://arxiv.org/abs/1706.03762)). OpenAI의 공식 문서는 토큰을 모델이 텍스트를 처리하는 단위로 설명하고 토크나이저 도구를 제공한다([What are tokens?](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)). Anthropic은 system prompt, 메시지, 도구 결과, 문서와 생성 출력이 context 사용량에 포함될 수 있다고 설명한다([Context windows](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)). 이 사실은 문자 수만으로 정확한 토큰 수를 일반화할 수 없음을 뜻한다.

## Reproduction Steps / 재현 순서

직접 모델을 시험하는 대신, 배포 전 요청 표본을 준비한다. 한국어, 영어, 긴 URL·코드·표가 있는 입력을 각각 포함하고, 실제 공급자의 토크나이저 또는 요청 사용량 정보를 기록한다. 이후 시스템 지시문·검색 결과·도구 정의·예상 출력 몫을 더한 총량을 측정한다. 한도 근처에서는 문서를 무작정 자르기보다 질문과 관련 없는 문맥을 먼저 제외하고, 원문 위치를 남긴다.

## Observations / 관찰 결과

운영에서 “짧아 보이는 요청”도 실패할 수 있다. 사용자가 보지 못하는 시스템 지시문과 도구 스키마, 자동으로 붙은 대화 이력이 원인일 수 있기 때문이다. 반대로 긴 문서라도 필요한 부분만 검색해 넣으면 총 입력은 줄어든다. 따라서 실패 기록에는 사용자 본문만이 아니라 실제로 모델에 전달한 구성 요소와 토큰 사용량을 함께 남기는 편이 원인 분석에 유리하다.

## Interpretation / 해석

내 해석으로 토큰 예산은 단순한 비용 계산이 아니라 제품 계약이다. UI는 사용자에게 어떤 길이의 내용을 받을지 정하고, 백엔드는 어떤 문맥을 선택할지 정하며, 출력 검증은 남은 공간에서 어떤 형식을 보장할지 정한다. 이 세 층을 함께 설계하면 긴 입력을 받는 기능도 예측 가능하게 제한할 수 있다.

## Limitations / 한계

토큰화 방식과 context 규칙은 모델·공급자·API 변경에 따라 달라질 수 있다. 토큰 수가 답변 품질이나 사실성을 보장하지 않는다. 이 글은 실제 요청의 사용량 데이터를 제시하지 않으며 직접 실험 결과가 아니다. 민감 문서를 측정할 때도 로그와 토크나이저 입력에 대한 보관·접근 정책을 별도로 검토해야 한다.

## References / 참고자료

- [Vaswani et al., Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [OpenAI, What are tokens?](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)
- [Anthropic, Context windows](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)

## Change Log / 변경 이력

- 2026-08-01: 내부 검토용 초안 작성. 게시 일정과 공개 상태는 변경하지 않았다.
