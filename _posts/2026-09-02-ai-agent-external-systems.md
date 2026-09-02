---
layout: single
title: "AI 에이전트가 외부 시스템에서 일한다는 것"
description: "AI 에이전트가 답변을 생성하는 단계를 넘어 데이터와 도구를 읽고 행동할 때, 인터페이스 계약·권한·승인·검증을 왜 함께 설계해야 하는지 정리한다."
date: 2026-09-02 00:00:00 +09:00
lang: ko
translation_key: ai-agent-external-systems
section: development
topic_key: ai
categories: AI
tags: [ai, agents, tools, mcp, agent-security, agent-evaluation]
track: agent-interface-engineering
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

AI 에이전트는 이제 텍스트를 답하는 인터페이스에만 머물지 않는다. 데이터 소스를 읽고, 도구를 호출하고, 여러 단계의 작업을 이어 가며, 경우에 따라 외부 시스템에 변경을 요청한다. 이때 핵심 문제는 모델이 얼마나 자연스러운 문장을 만드는가가 아니라 **어떤 행동을 어떤 권한으로 허용하고, 그 결과를 어떻게 확인할 것인가**다.

이 글은 새 연재의 출발점으로서 에이전트가 외부 시스템에서 일할 때 필요한 네 가지 설계 축—도구 계약, 권한 경계, 사람 승인, 검증 가능한 기록—을 정의한다. 특정 SDK의 설치법이나 특정 모델 성능 비교는 다루지 않는다.

## Document Info / Environment

- 작성일: 2026-09-02
- 검증 기준일: 2026-09-02
- 문서 성격: concept analysis / operations guide
- 테스트 환경: 직접 실행 테스트 없음. 이 글은 공식 문서의 공개 설명을 비교해 설계 경계를 정리한 글이다.
- 테스트 버전: MCP 문서 경로 `2026-07-28`, Chrome WebMCP 문서 2026-08-07 업데이트본. 각 제품·브라우저의 실제 지원 범위는 이후 바뀔 수 있다.
- 출처 등급: 공식 제품 문서, 공식 프로토콜 문서, 공식 연구 자료.

## Problem Statement / 문제 정의

사용자가 에이전트에게 “이 메일을 요약해 줘”라고 요청하는 상황과 “이 메일을 읽고 고객에게 답장을 보내 줘”라고 요청하는 상황은 다르다. 후자는 외부 데이터를 읽고, 신뢰하기 어려운 콘텐츠를 처리하며, 외부 시스템에서 되돌리기 어려운 행동을 할 수 있다.

여기서 흔한 오해는 도구 연결을 단순한 기능 확장으로 보는 것이다. 연결은 기능을 늘리지만, 동시에 데이터 노출 경로와 행동 권한도 늘린다. 따라서 도구를 연결한 뒤에 보안을 덧붙이는 방식보다, 처음부터 다음 질문을 답할 수 있는 인터페이스를 설계해야 한다.

1. 에이전트가 읽을 수 있는 정보는 무엇인가.
2. 에이전트가 제안만 할 수 있는가, 실제 변경도 할 수 있는가.
3. 누가 어떤 시점에 그 행동을 승인하는가.
4. 결과가 성공했다는 증거와 실패했을 때의 기록은 무엇인가.

## Verified Facts / 확인된 사실

- OpenAI Agents SDK 문서는 에이전트를 계획, 도구 호출, 전문 에이전트 간 협업, 다단계 작업을 위한 상태 유지를 수행하는 애플리케이션으로 설명한다. 또한 애플리케이션 서버가 배포, 도구 구현, 상태 저장, 승인 결정을 소유할 수 있다고 명시한다.
  근거: [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents)

- MCP 공식 문서는 MCP를 AI 애플리케이션과 외부 시스템을 연결하는 오픈 소스 표준으로 설명한다. 문서가 예시로 드는 연결 대상에는 로컬 파일·데이터베이스 같은 데이터 소스, 검색·계산기 같은 도구, 특화 프롬프트 같은 워크플로가 포함된다.
  근거: [Model Context Protocol: What is MCP?](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro)

- Chrome의 WebMCP 문서는 브라우저 에이전트가 DOM을 해석해 클릭·입력을 흉내 내는 actuation에만 의존하지 않도록, 웹사이트가 구조화된 호출 가능 도구를 등록하는 **제안 단계의 웹 플랫폼 API**를 설명한다. 현재 도구는 `inputSchema`로 기대 입력을 기술할 수 있다. 다만 WebMCP는 MCP 전송 프로토콜 자체를 브라우저에 구현하거나 모든 에이전트의 자동 발견을 보장하는 규격이 아니며, 2026-09-02 기준 Chrome 149부터 origin trial로 실험할 수 있다. 따라서 범용 웹 표준, 모든 브라우저의 기본 기능, 또는 인증·인가·사용자 승인을 자동 보장하는 기능으로 단정할 수 없다.
  근거: [Chrome for Developers: WebMCP](https://developer.chrome.com/docs/ai/webmcp), [WebMCP Draft Community Group Report](https://webmachinelearning.github.io/webmcp/)

- OpenAI의 agent 안전 가이드는 신뢰할 수 없는 텍스트가 의도된 동작을 바꾸려는 지시를 포함할 수 있는 prompt injection, MCP에 의도하지 않은 개인정보가 전달될 수 있는 위험, 도구 승인, 구조화된 출력, 평가와 trace grading의 필요성을 다룬다. 가이드는 완화책이 위험을 줄이지만 에이전트를 완벽하게 만들지는 않는다고 명시한다.
  근거: [OpenAI: Safety in building agents](https://developers.openai.com/api/docs/guides/agent-builder-safety)

- Anthropic은 브라우저 에이전트가 웹페이지, 문서, 광고, 검색 결과처럼 신뢰할 수 없는 내용을 처리하면서 행동할 수 있기 때문에 prompt injection 공격면이 커진다고 설명한다. 해당 연구는 방어 성능이 개선되더라도 브라우저 에이전트가 prompt injection에 면역인 것은 아니라고 밝힌다.
  근거: [Anthropic: Mitigating the risk of prompt injections in browser use](https://www.anthropic.com/research/prompt-injection-defenses)

## Reproduction Steps / 재현 순서

이 글은 특정 제품을 연결해 실행한 튜토리얼이 아니다. 대신 외부 시스템 연결을 검토할 때 아래 설계 검토를 재현 가능한 문서 작업으로 수행할 수 있다.

1. 후보 행동을 `조회`, `초안 생성`, `변경 요청`, `되돌릴 수 없는 실행`으로 분류한다.
2. 각 행동마다 필요한 입력, 허용된 데이터 범위, 필요한 권한, 승인자, 성공 증거를 한 줄씩 기록한다.
3. 외부 콘텐츠를 신뢰할 수 있는 지시로 취급하지 않는다는 경계를 정한다.
4. 변경 도구에는 실패·재시도·중복 실행·취소의 처리 방식을 정한다.
5. 운영 전에는 정상 사례뿐 아니라 권한 부족, 잘못된 입력, prompt injection 의심 콘텐츠, 승인 거부 사례를 평가 집합에 넣는다.

직접 재현 없음: 특정 MCP 서버, 브라우저 에이전트 또는 상용 API를 이 글을 위해 연결·실행하지 않았다. 따라서 특정 도구의 실제 성공률, 비용, 지연 시간, 보안 수준을 주장하지 않는다.

## Observations / 관찰 결과

공식 문서를 비교하면, 에이전트 구현에서 모델 호출은 전체 구조의 일부일 뿐이다. 외부 시스템과 연결될수록 제품은 도구 정의, 상태 저장, 승인, trace, 평가라는 애플리케이션 계층을 필요로 한다.

또한 브라우저 화면 조작과 구조화된 도구 호출은 같은 문제가 아니다. 화면 조작은 인간용 인터페이스를 해석해 여러 단계를 수행하는 방식이고, 구조화 도구는 입력과 행동의 의도를 계약으로 표현하는 방식이다. WebMCP는 사이트가 정의한 작업에 점진적 보강 경로를 제공하는 제안이지, 기존 UI 자동화를 즉시 대체하거나 도구의 출력 정확성·업무 성공을 보장한다는 증거는 아니다.

## Interpretation / 해석

내 판단으로 에이전트 기능의 최소 단위는 “프롬프트 + 모델”이 아니라 다음 계약이다.

```text
허용된 목적
+ 명시적 입력
+ 최소 권한
+ 승인 조건
+ 관찰 가능한 결과
+ 실패·재시도·취소 규칙
```

이 계약이 없으면 도구 호출이 성공해도 업무가 올바르게 끝났는지 판단하기 어렵다. 예를 들어 `send_email` 호출이 HTTP 성공을 반환해도, 잘못된 수신자에게 보냈거나 중복 전송했거나 승인되지 않은 내용을 전송했다면 업무 결과는 성공이 아니다.

그래서 초기에 가장 안전한 선택은 모든 것을 자동화하는 것이 아니라, 읽기 전용 조회와 초안 생성처럼 영향이 작고 검토 가능한 동작부터 분리하는 것이다. 쓰기, 전송, 삭제, 결제, 배포 같은 동작은 도구 이름만으로 안전해지지 않는다. 권한 범위, 사용자 확인, 감사 기록, 되돌림 가능성을 함께 설계해야 한다.

## Limitations / 한계

- 이 글은 공개 문서 분석이며, 특정 조직의 권한 체계·규제·업무 절차를 검증하지 않았다.
- MCP와 WebMCP의 실제 지원 범위, SDK 구현, 브라우저 기능, 제품 UI는 변경될 수 있다.
- WebMCP의 입력 스키마는 에이전트가 기대 입력을 이해하도록 돕지만, 독립적인 인증·인가, 서버 측 입력 검증, 거래 확인 또는 사용자 승인을 대체하지 않는다.
- 구조화된 도구 계약은 prompt injection이나 모델 오류를 제거하지 않는다. 승인, 최소 권한, 입력 검증, trace, 평가를 함께 적용해야 한다.
- 실제 출시 판단에는 개인정보, 접근 제어, 감사 보존, 결제·삭제·배포 정책, 장애 대응 기준을 조직별로 추가 검토해야 한다.

## References / 참고자료

- [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents)
- [OpenAI: Safety in building agents](https://developers.openai.com/api/docs/guides/agent-builder-safety)
- [Model Context Protocol: What is MCP?](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro)
- [Chrome for Developers: WebMCP](https://developer.chrome.com/docs/ai/webmcp)
- [WebMCP Draft Community Group Report](https://webmachinelearning.github.io/webmcp/)
- [Anthropic: Mitigating the risk of prompt injections in browser use](https://www.anthropic.com/research/prompt-injection-defenses)

## Change Log / 변경 이력

- 2026-09-02: 신뢰성 검토: WebMCP의 실험 상태, MCP와의 경계, 입력 스키마의 비보장 범위를 명확히 하고 1차 명세 출처를 추가했다. `published: false`; 게시 일정·공개 상태·사이트 파일은 변경하지 않았다.
- 2026-09-02: 신뢰 가능한 1차 자료만 인용한 로컬 초안 작성. `published: false`; 게시 일정·공개 상태·사이트 파일은 변경하지 않았다.
