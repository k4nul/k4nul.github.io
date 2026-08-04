---
layout: single
title: "AI 지시문 계층을 분리해야 하는 이유"
description: "시스템 정책, 애플리케이션 작업 규칙, 사용자 요청, 외부 데이터를 구분하는 안전한 설계 기준을 정리한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: separating-instruction-layers
section: development
topic_key: ai
categories: AI
tags: [ai, llm, prompting, security, tool-calling]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

AI 요청에는 서로 다른 권한의 문장이 함께 들어온다. 제품의 안전 정책, 업무 흐름 지시, 사용자의 목표, 검색된 문서 내용은 모두 텍스트이지만 같은 권한을 가져서는 안 된다. 계층을 분리하면 문서 속 “앞 지시를 무시하라” 같은 문자열을 데이터로 다루고, 변경 가능한 사용자 요구와 변경하면 안 되는 시스템 경계를 구분할 수 있다.

## Document Info / Environment

- 작성일: 2026-08-01
- 검증 기준: 공식 개발자 문서와 NIST 지침
- 문서 성격: concept analysis
- 테스트 환경: 직접 실행 실험 없음.
- 특정 공급자 보안 기능의 완전성을 주장하지 않는다.

## Problem Statement / 문제 정의

검색 문서, 이메일, 웹 페이지, 도구 결과는 신뢰되지 않은 데이터를 포함할 수 있다. 이를 운영 지시와 같은 층에 넣으면 사용자가 보지 못한 정책 변경이나 권한 확대가 텍스트 경쟁으로 바뀐다. 특히 도구 호출은 문장을 만드는 일과 외부 시스템 행동을 연결하므로, 지시 해석과 승인 경계를 분리해야 한다.

## Verified Facts / 확인된 사실

OpenAI의 프롬프트 가이드는 developer 메시지와 user 메시지의 역할을 구분하고, 신뢰되지 않은 입력을 명확한 경계로 분리하는 지침을 제공한다([Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)). OpenAI의 안전 가이드는 간접 프롬프트 인젝션을 위험으로 설명한다([Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)). NIST AI 600-1은 생성형 AI 위험의 거버넌스와 관리 필요성을 다룬다([NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)).

## Reproduction Steps / 재현 순서

직접 공격 실험 대신 요청을 네 상자로 분류한다: 변경 불가 안전·권한 정책, 애플리케이션 작업 규칙, 사용자의 목표, 외부 문서·도구 결과. 외부 내용은 인용할 데이터로 표시하고 실행 지시로 승격하지 않는다. 도구는 최소 권한, 인자 검증, 고위험 행동의 별도 승인, 감사 로그를 둔다.

## Observations / 관찰 결과

계층이 없으면 실패 원인을 찾기 어렵다. 모델이 문서를 요약했는지, 문서의 명령을 수행하려 했는지, 애플리케이션이 위험한 도구 호출을 허용했는지가 섞인다. 요청 로그에는 계층별 출처와 도구 승인 결과를 남겨야 하며, 비밀값이나 불필요한 원문을 기록해서는 안 된다.

## Interpretation / 해석

내 해석으로 지시 계층은 프롬프트 문장력보다 권한 모델이다. 모델이 모든 문자열을 읽더라도, 제품은 어떤 문자열이 정책을 바꿀 수 있는지와 어떤 행동이 승인을 요구하는지를 코드와 운영 절차로 제한해야 한다.

## Limitations / 한계

프롬프트 분리는 단독 보안 통제가 아니다. 인증, 인가, 입력·출력 검증, 비밀 관리, 감사가 함께 필요하다. 이 글은 침투 테스트나 직접 실험 결과가 아니다.

## References / 참고자료

- [OpenAI, Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [OpenAI, Safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices)
- [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-01: 내부 검토용 초안 작성. 게시 일정과 공개 상태는 변경하지 않았다.
