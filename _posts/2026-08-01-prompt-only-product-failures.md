---
layout: single
title: "프롬프트만으로 제품 문제를 해결하기 어려운 이유"
description: "프롬프트 개선의 역할과 한계, 그리고 제품 수준의 경계·평가·통제가 필요한 이유를 설명한다."
date: 2026-08-01
lang: ko
translation_key: prompt-only-product-failures
section: development
topic_key: ai
categories: AI
tags: [ai, prompting, security, evaluation]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

프롬프트는 모델에게 역할, 형식, 제약을 전달하는 유용한 인터페이스지만 제품 전체의 통제 경계는 아니다. 입력 데이터의 권한, 도구 실행 권한, 출력 검증, 실패 시 사용자 경험은 프롬프트 바깥에서 설계되어야 한다. 좋은 지시는 도움이 되지만, 그것만으로 제품의 안전성과 신뢰성을 증명하지는 못한다.

## Document Info / Environment

이 글은 2026-08-01 기준의 설계 초안이며 특정 프롬프트나 모델을 실행 시험하지 않았다. 공개 위험 관리 및 보안 안내를 바탕으로 일반적인 제품 설계 원칙을 정리한다.

## Problem Statement / 문제 정의

팀은 기대와 다른 출력이 나오면 시스템 지시문을 더 길게 쓰는 방식으로 대응하기 쉽다. 그러나 사용자가 입력한 텍스트, 검색된 문서, 외부 도구의 결과도 모델의 행동에 영향을 준다. 프롬프트가 정책을 말해도 애플리케이션이 권한 없는 데이터를 전달하거나 검증 없이 행동을 실행하면 문제는 남는다.

## Verified Facts / 확인된 사실

OWASP Top 10 for LLM Applications는 프롬프트 인젝션을 중요한 위험으로 다루며, 신뢰할 수 없는 입력이 모델의 의도된 지시를 바꾸도록 시도할 수 있음을 설명한다. NIST AI 600-1도 생성형 AI의 위험을 맥락에 따라 식별·측정·관리할 것을 제시한다. 두 자료는 프롬프트를 유일한 보안 경계로 보지 않는 이유를 제공한다.

## Reproduction Steps / 재현 순서

먼저 모델에 닿는 입력을 사용자 요청, 검색 문서, 도구 결과, 시스템 지시로 구분한다. 다음으로 모델 출력이 단순 표시인지, 데이터 조회인지, 외부 행동 요청인지 기록한다. 행동이 수반되면 애플리케이션 계층에서 허용 목록, 권한 확인, 인자 검증, 승인 또는 중단 경로를 설계한다. 프롬프트는 이 흐름의 설명과 형식 제어에 사용한다.

## Observations / 관찰 결과

이 분리는 실패 원인을 더 명확하게 만든다. 관련 없는 문서가 검색됐다면 검색과 데이터 경계를, 허용되지 않은 작업이 제안됐다면 도구 권한과 검증을, 부정확한 서술이라면 평가와 표시 방식을 살펴볼 수 있다. 모든 문제를 ‘프롬프트가 약했다’고 부르면 개선 지점이 흐려진다.

## Interpretation / 해석

프롬프트는 제품 설계의 한 구성 요소이지 정책 집행 엔진이 아니다. 제품은 모델이 제안한 내용을 신뢰 가능한 사실이나 허가된 행동으로 바꾸기 전에 독립적인 검사 지점을 가져야 한다. 이 방식은 모델이나 지시문이 바뀌어도 유지할 수 있는 경계를 만든다.

## Limitations / 한계

어떤 통제 조합도 프롬프트 인젝션이나 부정확한 출력을 완전히 없앤다고 보장할 수 없다. 실제 위협 모델과 허용할 위험은 사용 사례에 따라 검토해야 한다. OWASP와 NIST 자료는 유용한 지침이지만 개별 조직의 법적 준수 여부를 판정하지 않는다.

## References / 참고자료

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

2026-08-01: 내부 검토용 초안 작성. 게시 일정과 제공 상태는 확정하지 않았다.
