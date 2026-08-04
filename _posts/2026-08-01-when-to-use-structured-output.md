---
layout: single
title: "언제 구조화 출력을 사용해야 하는가"
description: "사람이 읽는 생성문과 시스템이 처리하는 데이터를 구분해 JSON Schema 기반 출력을 선택하는 기준을 정리한다."
date: 2026-08-01 09:00:00 +09:00
lang: ko
translation_key: when-to-use-structured-output
section: development
topic_key: ai
categories: AI
tags: [ai, llm, structured-output, json-schema, validation]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

구조화 출력은 AI의 문장을 바로 프로그램 입력으로 써야 할 때 유용하다. 핵심은 JSON처럼 보이는 텍스트를 얻는 것이 아니라, 필드·형식·필수값을 명시하고 애플리케이션이 검증할 수 있게 하는 일이다. 반대로 공감 표현, 긴 설명, 초안처럼 사람의 해석이 중심인 작업에는 지나친 스키마가 오히려 목적을 흐릴 수 있다.

## Document Info / Environment

- 작성일: 2026-08-01
- 검증 기준: 공식 개발자 문서와 NIST 지침
- 문서 성격: concept analysis
- 테스트 환경: 직접 실행 실험 없음.
- 특정 API의 가용성이나 준수율을 주장하지 않는다.

## Problem Statement / 문제 정의

자연어 응답을 파싱해 티켓 우선순위, 양식 입력, 도구 인자로 넘기면 작은 표현 변화도 운영 오류가 될 수 있다. 반면 모든 답을 엄격한 객체로 만들면 설명에 필요한 맥락과 불확실성 표시가 사라질 수 있다. 출력 소비자가 사람인지 프로그램인지, 실패 시 무엇을 할지 먼저 정해야 한다.

## Verified Facts / 확인된 사실

OpenAI는 Structured Outputs가 제공된 JSON Schema를 따르도록 설계되었고 JSON mode와 구분된다고 문서화한다([Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)). JSON Schema는 JSON 구조의 검증을 위한 어휘와 키워드를 정의한다([JSON Schema specification](https://json-schema.org/specification)). NIST AI 600-1은 생성형 AI 위험 관리의 측정과 거버넌스를 다룬다([NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)).

## Reproduction Steps / 재현 순서

직접 호출 대신 출력 소비 경로를 그린다. 프로그램이 읽는 값이면 필수 필드, 타입, 열거값, 범위, 누락 시 실패 처리를 정의한다. 구조 검증 뒤에도 권한·업무 규칙·원본 데이터와의 일치를 검증한다. 사람이 읽는 설명은 구조 필드에 근거와 불확실성 상태를 담고, 본문은 별도 텍스트로 제공하는 혼합 방식을 검토한다.

## Observations / 관찰 결과

스키마 통과는 업무 성공이 아니다. 날짜 문자열이 형식에는 맞아도 존재하지 않는 예약을 가리킬 수 있고, 분류 값이 허용 목록에 있어도 입력 문서를 오독했을 수 있다. 따라서 파서 성공, 규칙 검증, 권한 확인, 실제 실행 승인을 각각 기록해야 한다.

## Interpretation / 해석

내 해석으로 구조화 출력은 모델 신뢰의 대체물이 아니라 시스템 경계의 명세다. 형식이 중요한 곳에서 변동을 줄이고, 사람이 판단해야 하는 곳에는 근거와 검토 흐름을 남긴다. 행동을 실행하는 도구 인자는 특히 별도 검증과 승인에 연결해야 한다.

## Limitations / 한계

스키마는 사실성, 최신성, 권한을 보장하지 않는다. 기능 세부 사항은 공급자별로 달라질 수 있다. 이 글은 실제 API 호출이나 직접 실험 결과를 제공하지 않는다.

## References / 참고자료

- [OpenAI, Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [JSON Schema specification](https://json-schema.org/specification)
- [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

- 2026-08-01: 내부 검토용 초안 작성. 게시 일정과 공개 상태는 변경하지 않았다.
