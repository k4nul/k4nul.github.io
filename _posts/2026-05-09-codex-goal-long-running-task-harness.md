---
layout: single
description: "Codex CLI의 실험적 /goal 기능을 공식 문서와 changelog 기준으로 확인하고, 장기 작업 하네스에서 왜 중요한지 설명하는 글."
title: "Codex 실전 활용 11. /goal은 장기 작업의 목표를 어떻게 붙잡는가"
lang: ko
translation_key: codex-goal-long-running-task-harness
date: 2026-05-09 09:00:00 +09:00
section: development
topic_key: ai
categories: AI
tags: [ai, codex, goal, harness-engineering, long-running-task]
author_profile: false
sidebar:
  nav: "sections"
search: false
published: false
---

## 요약

2026-05-08 기준으로 Codex CLI의 `/goal`은 짧은 명령 편의 기능이라기보다 장기 작업에서 목표를 계속 붙잡기 위한 실험적 상태 기능에 가깝다. 공식 CLI slash command 문서는 `/goal`을 장기 실행 작업을 위한 실험적 goal 설정 또는 조회 명령으로 설명하고, Codex changelog는 2026-04-30에 persisted `/goal` workflow가 추가되었다고 기록한다.

하네스 엔지니어링 관점에서 중요한 점은 명령 이름이 아니라 위치다. 프롬프트 한 번, 계획 한 번, `AGENTS.md` 한 파일로는 긴 작업의 목표 drift를 완전히 막기 어렵다. `/goal`은 그 사이에 놓이는 "현재 세션이 끝까지 붙잡아야 할 목표"라는 런타임 상태에 가깝다.

## 문서 정보

- 작성일: 2026-05-08
- 검증 기준일: 2026-05-08
- 문서 성격: analysis
- 테스트 환경: Windows PowerShell에서 로컬 CLI 버전만 확인. `/goal` 대화형 흐름은 직접 실행하지 않음.
- 테스트 버전: 로컬 `codex-cli 0.129.0-alpha.15`, 공식 changelog의 Codex CLI 0.128.0 및 0.129.0 기록
- 출처 등급: OpenAI 공식 문서, OpenAI Codex 공식 changelog, 로컬 버전 확인

## 문제 정의

에이전트가 짧은 작업을 할 때는 사용자 메시지 하나만으로도 충분할 때가 많다. 예를 들어 "이 함수에 null check를 추가해" 같은 요청은 목표, 범위, 검증 조건이 비교적 작다.

문제는 장기 작업이다.

- 여러 파일과 모듈을 오간다.
- 중간에 빌드 실패, 테스트 실패, 충돌, 새 요구사항이 생긴다.
- 컨텍스트가 길어져 compaction이나 resume이 필요해진다.
- 처음 목표와 지금 하고 있는 작업 사이가 서서히 벌어진다.

하네스 엔지니어링은 이 drift를 줄이기 위해 프롬프트, instruction file, tool 권한, sandbox, 승인 정책, 상태 저장, 로그, 검증 루프를 설계한다. `/goal`이 흥미로운 이유는 바로 이 "상태 저장된 목표" 영역을 제품 기능으로 다루기 시작했다는 점이다.

## 확인된 사실

- OpenAI 공식 CLI slash command 문서 기준으로 `/goal`은 장기 실행 작업을 위한 실험적 goal을 설정하거나 조회하는 명령이다. 같은 표는 이 기능이 `features.goals`를 요구한다고 설명한다.
  근거: [OpenAI, Slash commands in Codex CLI](https://developers.openai.com/codex/cli/slash-commands)

- OpenAI Codex changelog 기준으로 2026-04-30의 Codex CLI 0.128.0에는 persisted `/goal` workflows가 추가되었다. changelog는 app-server API, model tool, runtime continuation, TUI의 create, pause, resume, clear 제어가 함께 들어갔다고 기록한다.
  근거: [OpenAI, Codex changelog](https://developers.openai.com/codex/changelog)

- OpenAI Codex changelog 기준으로 2026-05-07의 Codex CLI 0.129.0에는 experimental goals 관련 개선이 들어갔다. changelog는 goal discoverability, resume 이후 paused 상태 유지, validation과 multi-day duration 출력 개선을 언급한다.
  근거: [OpenAI, Codex changelog](https://developers.openai.com/codex/changelog)

- OpenAI의 feature maturity 문서 기준으로 Experimental 기능은 불안정하며 변경되거나 제거될 수 있고, 사용자가 위험을 감수하고 써야 하는 단계다.
  근거: [OpenAI, Feature Maturity](https://developers.openai.com/codex/feature-maturity)

- OpenAI Codex best practices 문서는 큰 저장소나 높은 위험도의 작업에서 Goal, Context, Constraints, Done when을 명확히 주는 것이 결과를 더 검토 가능하게 만든다고 설명한다. Prompting 문서도 복잡한 작업은 작은 단계로 나누고 필요하면 계획을 요청하라고 설명한다.
  근거: [OpenAI, Codex best practices](https://developers.openai.com/codex/learn/best-practices), [OpenAI, Prompting](https://developers.openai.com/codex/prompting)

## 직접 재현한 결과

로컬 환경에서 확인한 Codex CLI 버전은 다음과 같다.

```powershell
codex --version
```

```text
codex-cli 0.129.0-alpha.15
```

직접 재현하지 않은 범위는 아래와 같다.

- `/goal` 입력 후 create, pause, resume, clear 흐름
- `features.goals` 설정 여부에 따른 표시 차이
- goal 상태가 로컬에 저장되는 정확한 파일 또는 내부 구현

따라서 이 글의 기능 동작 설명은 공식 문서와 changelog에 근거한다. 로컬 버전 확인은 현재 작업 환경에 설치된 Codex CLI가 어떤 버전인지 밝히기 위한 보조 정보다.

## 해석 / 의견

아래 내용은 위에서 확인한 공식 문서와 로컬 버전 확인을 바탕으로 한 해석이다. `/goal`의 내부 구현, 저장 위치, 모든 클라이언트에서의 동일 동작은 단정하지 않는다.

### /goal은 계획이 아니다

`/goal`을 `/plan`의 다른 이름으로 보면 헷갈린다.

`/plan`은 작업에 들어가기 전에 "어떻게 할지"를 잡는 데 가깝다. 반면 `/goal`은 "이 장기 작업이 끝까지 무엇을 향해야 하는지"를 세션 상태로 붙잡는 쪽에 가깝다.

예를 들어 다음 두 문장은 역할이 다르다.

```md
/plan 이 결제 모듈 리팩터링의 단계별 계획을 제안해줘.
```

```md
/goal 결제 모듈의 외부 동작을 유지하면서 중복된 검증 로직을 하나의 정책 계층으로 모으고, 기존 테스트와 신규 회귀 테스트가 통과할 때까지 진행한다.
```

첫 번째는 다음 행동을 정리한다. 두 번째는 작업이 길어져도 돌아와야 할 기준점을 세운다.

### /goal은 AGENTS.md도 아니다

`AGENTS.md`는 저장소의 지속 규칙이다. 코딩 스타일, 빌드 명령, 금지 사항, 검증 기준처럼 저장소 안에서 반복 적용되어야 하는 지침을 담는다.

`/goal`은 특정 장기 작업의 현재 목표다. 같은 저장소에서도 오늘의 목표는 "권한 경계를 좁히는 것"일 수 있고, 내일의 목표는 "테스트 실행 시간을 줄이는 것"일 수 있다. 이 둘을 모두 `AGENTS.md`에 넣으면 저장소 규칙과 작업 목표가 섞인다.

하네스 관점에서는 이렇게 나누는 편이 깔끔하다.

```text
AGENTS.md: 저장소 전체의 지속 규칙
skill: 반복 가능한 절차와 참고 자료
/plan: 이번 작업의 실행 계획
/goal: 이번 장기 작업이 끝까지 지켜야 할 목표
/status, /diff, test: 현재 상태와 검증
```

### 왜 하네스 엔지니어링에서 중요한가

에이전트 하네스는 모델을 둘러싼 실행 환경이다. 모델이 파일을 읽고, 수정하고, 명령을 실행하고, 외부 도구를 부르고, 중간 상태를 저장하고, 사용자 승인을 받는 전체 구조가 하네스다.

좋은 하네스는 "모델이 똑똑한가"만 묻지 않는다. 다음 질문을 같이 묻는다.

- 목표가 명확하게 유지되는가?
- 지금 하는 작업이 원래 목표와 아직 연결되어 있는가?
- 멈춰야 할 조건과 검증 조건이 보이는가?
- resume이나 compaction 이후에도 같은 목표로 돌아올 수 있는가?
- 사용자가 중간에 방향을 바꾸면 이전 목표를 pause 또는 clear할 수 있는가?

`/goal`은 이 질문 중 목표 유지와 resume 이후 일관성에 직접 닿아 있다. 그래서 단순한 slash command보다 하네스 기능으로 보는 편이 더 정확하다.

### 좋은 /goal 문장

좋은 goal은 짧지만 모호하지 않아야 한다. "사이트를 개선해"처럼 넓은 목표는 장기 작업에서 drift를 막지 못한다.

다음 구조가 더 낫다.

```md
/goal [결과]를 만들되, [유지해야 할 조건]을 깨지 않고, [범위] 안에서 작업하며, [검증 조건]이 만족되면 완료로 본다.
```

예시는 다음과 같다.

```md
/goal Codex /goal 기능에 대한 2026-05-09 한국어 블로그 글을 작성한다. 공식 문서와 changelog로 확인한 사실과 하네스 관점 해석을 분리하고, 기존 예약 글의 날짜 이동 상태를 깨지 않으며, Jekyll build가 통과하면 완료로 본다.
```

이 문장은 결과, 근거 기준, 범위, 완료 조건을 함께 담는다. 에이전트가 중간에 다른 흥미로운 리팩터링을 발견해도 돌아올 기준이 생긴다.

### 언제 쓰면 좋은가

`/goal`은 모든 작업에 필요하지 않다. 작은 수정에는 오히려 무겁다.

어울리는 경우는 다음과 같다.

- 며칠에 걸쳐 이어질 수 있는 리팩터링
- 대규모 문서 개편 또는 포스트 시리즈 재배치
- 마이그레이션처럼 단계가 많고 중간 검증이 필요한 작업
- 실패 로그 분석, 수정, 재검증을 반복해야 하는 작업
- resume 이후에도 같은 목표를 유지해야 하는 작업

어울리지 않는 경우도 있다.

- 단일 파일의 작은 오타 수정
- 질문에 대한 짧은 설명 요청
- 한 번의 명령 실행으로 끝나는 확인 작업
- 목표가 아직 너무 모호해서 먼저 탐색이 필요한 작업

목표가 모호한 상태라면 `/goal`보다 먼저 `/plan`이나 일반 질문으로 범위를 좁히는 편이 낫다.

### 운영할 때의 주의점

첫째, Experimental 기능이라는 점을 잊지 말아야 한다. 공식 maturity 문서 기준으로 Experimental은 안정적 계약이 아니다. 팀 표준 문서에 넣는다면 "필수 절차"가 아니라 "실험적 선택지"로 적는 편이 안전하다.

둘째, goal에 비밀이나 민감 정보를 넣지 않는 편이 좋다. 공식 changelog가 persisted workflow를 언급하는 만큼, 운영상 기록으로 남을 수 있다고 보고 보수적으로 다루는 편이 안전하다. API key, 내부 고객명, 미공개 사고 세부 정보는 goal이 아니라 안전한 내부 문서나 승인된 secret store에서 다뤄야 한다.

셋째, goal은 검증을 대신하지 않는다. 목표를 잘 써도 빌드, 테스트, diff review, 로그 확인은 여전히 필요하다. OpenAI prompting 문서가 말하는 것처럼 Codex는 검증할 수 있을 때 더 좋은 결과를 낸다.

넷째, 목표가 바뀌면 기존 goal을 그대로 두지 말아야 한다. changelog상 TUI에는 create, pause, resume, clear 흐름이 들어갔다. 방향이 바뀐 작업에서는 이전 goal을 pause 또는 clear하고 새 목표를 명시하는 것이 낫다.

## 추천 사용 패턴

내가 쓴다면 `/goal`은 다음 순서로 쓴다.

1. 먼저 작업을 한 문장으로 좁힌다.
2. 깨지면 안 되는 조건을 붙인다.
3. 범위 밖 일을 적는다.
4. 완료 조건을 검증 가능한 문장으로 쓴다.
5. 작업 중 `/diff`, 테스트, 빌드 결과로 goal과 실제 변경이 맞는지 확인한다.

예시는 다음과 같다.

```md
/goal 사용자 프로필 저장 흐름에서 중복 validation을 제거한다. API 응답 형식과 DB schema는 바꾸지 않고, profile 관련 unit test와 integration test가 통과하면 완료로 본다. 인증 정책 변경과 UI 수정은 범위에서 제외한다.
```

이렇게 쓰면 Codex가 할 일뿐 아니라 하지 말아야 할 일도 보인다. 장기 작업에서 "좋은 목표"는 추진력보다 경계선을 더 잘 제공한다.

## 한계와 예외

이 글은 `/goal`의 내부 구현을 분석한 글이 아니다. 공식 문서와 changelog에 공개된 범위에서 기능의 의미를 해석한 글이다.

또한 `/goal`은 이 글 작성 시점에 CLI slash command 문서에서 확인한 기능이다. IDE extension이나 Codex app에서 동일한 방식으로 쓸 수 있다고 일반화하지 않는다.

마지막으로 "하네스 엔지니어링에서 핫하다"는 표현은 커뮤니티 분위기에 대한 인상일 수 있다. 이 글에서는 그 인상 자체를 사실로 증명하지 않고, 공식 문서상 확인되는 `/goal`의 기능 위치가 왜 하네스 설계 관점에서 중요해 보이는지만 다뤘다.

## 참고자료

- OpenAI, [Slash commands in Codex CLI](https://developers.openai.com/codex/cli/slash-commands) (2026-05-08 확인)
- OpenAI, [Codex changelog](https://developers.openai.com/codex/changelog) (2026-05-08 확인)
- OpenAI, [Feature Maturity](https://developers.openai.com/codex/feature-maturity) (2026-05-08 확인)
- OpenAI, [Codex best practices](https://developers.openai.com/codex/learn/best-practices) (2026-05-08 확인)
- OpenAI, [Prompting](https://developers.openai.com/codex/prompting) (2026-05-08 확인)

## 변경 이력

- 2026-05-08: 공식 문서 기준, 직접 재현 범위, 한계, 참고자료 확인일, 변경 이력을 보강했다.
