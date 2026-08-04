---
layout: single
title: "AI가 안전하게 실패하도록 UX 설계하기"
description: "근거 부족, 불확실성, 오류 상황에서 사용자가 다음 행동을 판단할 수 있게 하는 AI 실패 경험을 다룬다."
date: 2026-08-01
lang: ko
translation_key: safe-failure-ux
section: development
topic_key: ai
categories: AI
tags: [ai, ux, safety, human-in-the-loop]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

AI 기능의 실패는 오류 화면만 뜻하지 않는다. 답할 근거가 없는데 그럴듯한 답을 내거나, 요청을 잘못 이해했는데 확신하는 표현을 쓰는 것도 실패다. 안전한 실패 UX는 무조건 답을 만들기보다 한계를 알리고, 근거를 보여 주고, 사용자가 검토·수정·재시도·사람 연결 중 다음 행동을 선택할 수 있게 한다.

## Document Info / Environment

이 문서는 2026-08-01 기준의 일반 UX 설계 초안이다. 실제 사용자 조사나 제품 시험을 주장하지 않으며, 특정 사용자 집단이나 서비스의 결과를 일반화하지 않는다.

## Problem Statement / 문제 정의

모델 출력은 자연스러운 문장이라도 근거가 부족하거나 요청 범위를 벗어날 수 있다. 사용자가 결과의 한계를 알아차리지 못하면, 단순한 생성 오류가 잘못된 후속 행동으로 이어질 수 있다. 따라서 인터페이스는 ‘정답처럼 보이는 답’을 우선하기보다 결과의 상태와 검토 필요성을 전달해야 한다.

## Verified Facts / 확인된 사실

NIST AI RMF 1.0은 배포 환경과 유사한 조건에서 성능 또는 보증 기준을 측정하고 한계를 문서화하는 MEASURE 결과를 제시한다. NIST AI 600-1은 인간-AI 구성에서 과도한 의존과 자동화 편향을 생성형 AI 위험으로 다룬다. 이는 UX가 모델의 불확실성을 가리지 않는 것이 위험 관리와 연결됨을 시사한다.

## Reproduction Steps / 재현 순서

결과 화면에 답변만 두지 말고 사용한 입력 범위와 가능한 근거를 함께 표시한다. 근거가 없거나 충돌하면 그 상태를 평이한 문장으로 알리고, 추측으로 채우지 않는 경로를 마련한다. 사용자가 원문을 확인하고, 질문을 좁히고, 오류를 신고하고, 필요하면 사람에게 넘길 수 있는 행동을 결과 가까이에 둔다.

## Observations / 관찰 결과

실패 상태를 미리 설계하면 빈 검색 결과, 처리 실패, 안전상 응답하지 않는 경우가 서로 다른 경험으로 보인다. 같은 “오류”라도 다시 입력하면 되는 문제와 검토가 필요한 문제를 구분할 수 있다. 이 구분은 지원팀과 개발팀이 사건을 기록하고 개선할 때도 유용하다.

## Interpretation / 해석

안전한 실패 UX의 목표는 사용자를 겁주거나 책임을 전가하는 것이 아니다. 모델의 답변을 독립적으로 확인해야 하는 상황과 확인할 수 없는 상황을 정직하게 보여 주는 것이다. 사용자가 결과를 수정하거나 거절할 수 있는 여지를 두면 AI는 결정권자를 대체하는 화면보다 보조 도구에 가까워진다.

## Limitations / 한계

경고 문구나 인용 표시만으로 사용자가 항상 적절히 판단한다고 볼 수 없다. 접근성, 언어, 작업 압박, 도메인 지식은 이해에 영향을 준다. 고위험 사용 사례는 별도의 전문가 검토와 운영 절차가 필요하며, 이 글은 그 적합성이나 법적 준수를 보장하지 않는다.

## References / 참고자료

- [NIST AI RMF 1.0 (NIST AI 100-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

2026-08-01: 내부 검토용 초안 작성. 게시 일정과 제공 상태는 확정하지 않았다.
