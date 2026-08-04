---
layout: single
title: "AI 워크플로에 사람의 검토를 배치하는 법"
description: "사람의 검토를 형식적 승인으로 만들지 않고, 영향과 불확실성에 맞춰 배치하는 방법을 설명한다."
date: 2026-08-01
lang: ko
translation_key: placing-human-in-the-loop
section: development
topic_key: ai
categories: AI
tags: [ai, human-in-the-loop, governance, safety]
track: ai-knowledge-foundations
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

사람을 워크플로에 넣는다는 말은 단순히 승인 버튼을 추가하는 뜻이 아니다. 사람이 언제 개입하는지, 어떤 근거를 보고 무엇을 바꿀 수 있는지, 거절 뒤에는 어떤 경로가 있는지까지 설계해야 한다. 검토자는 모델 결과를 반복해서 클릭하는 장식이 아니라, 영향과 불확실성이 큰 지점에서 판단을 행사할 수 있어야 한다.

## Document Info / Environment

이 글은 2026-08-01 기준의 개념 초안이다. 특정 조직의 인력, 승인 정책, 모델 성능을 조사하거나 시험하지 않았다. 사람의 검토 필요도는 업무의 영향과 맥락에 따라 별도로 정해야 한다.

## Problem Statement / 문제 정의

모든 결과를 사람에게 보내면 지연과 피로가 쌓이고, 아무 결과도 검토하지 않으면 오류가 조용히 다음 단계로 간다. 더 어려운 문제는 검토자에게 원문, 모델의 한계, 수정 권한이 없는데 책임만 주는 경우다. 사람의 개입은 존재 여부보다 정보와 권한의 품질로 평가해야 한다.

## Verified Facts / 확인된 사실

NIST AI RMF 1.0은 다양한 관점과 역할을 위험 관리에 반영하고, 관련 AI 행위자 사이의 책임과 소통을 강조한다. NIST AI 600-1은 인간-AI 구성의 과도한 의존, 자동화 편향, 인간의 감독 약화를 위험으로 다룬다. 이는 ‘사람이 봤다’는 기록만으로 감독이 충분하지 않다는 배경을 제공한다.

## Reproduction Steps / 재현 순서

먼저 AI 출력이 정보 제공, 초안 작성, 우선순위 제안, 외부 행동 요청 중 어디에 쓰이는지 기록한다. 영향이 커지거나 근거가 약하거나 되돌리기 어려운 지점에는 검토를 배치한다. 검토 화면에는 원본 근거, 입력 범위, 수정·거절·에스컬레이션 선택지를 제공하고, 검토자가 처리할 수 없는 경우의 중단 경로도 둔다.

## Observations / 관찰 결과

이 접근에서는 사람의 역할이 최종 승인에만 머물지 않는다. 데이터 수집 단계의 예외 처리, 평가 기준의 작성, 사건 검토에도 서로 다른 사람이 참여할 수 있다. 검토 결과를 기록하면 반복되는 오류 유형과 애매한 정책을 발견하는 자료가 된다.

## Interpretation / 해석

사람의 검토는 AI의 오류를 자동으로 상쇄하는 보험이 아니다. 검토자에게 시간, 맥락, 권한이 없으면 자동화 편향을 강화할 수도 있다. 따라서 사람을 넣는 설계는 ‘누가 승인하는가’보다 ‘누가 무엇을 근거로 바꾸거나 멈출 수 있는가’를 먼저 묻는다.

## Limitations / 한계

이 글은 특정 업무에 필요한 검토 비율이나 인력 규모를 제시하지 않는다. 모든 사용 사례에 같은 승인 절차를 적용할 수 없으며, 고위험 판단은 분야별 전문가 및 관련 운영·법무 검토가 필요하다. NIST 지침은 적합성 인증이 아니다.

## References / 참고자료

- [NIST AI RMF 1.0 (NIST AI 100-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

## Change Log / 변경 이력

2026-08-01: 내부 검토용 초안 작성. 게시 일정과 제공 상태는 확정하지 않았다.
