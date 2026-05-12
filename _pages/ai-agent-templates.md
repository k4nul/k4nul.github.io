---
title: "AI agent 운영 실전 템플릿"
layout: single
permalink: /ai-engineering/templates/
description: "AGENTS.md, CLAUDE.md, Codex 작업 요청, agent 결과 리뷰, Claude Code permissions/settings 점검을 위한 최소 템플릿"
author_profile: true
sidebar:
  nav: "sections"
lang: ko
translation_key: ai-agent-operations-templates
---

이 페이지는 AI coding agent를 프로젝트에 붙일 때 처음부터 길고 복잡한 운영 문서를 만들지 않기 위한 최소 템플릿 모음입니다. 각 템플릿은 복사해서 늘리는 출발점이 아니라, 프로젝트에 맞는 것만 남기는 기준으로 사용합니다.

## AGENTS.md 최소 템플릿

```md
# AGENTS.md

## Repository Purpose

- 이 저장소가 무엇을 만들고 운영하는지 2-4줄로 적는다.
- agent가 착각하면 안 되는 핵심 도메인 경계를 적는다.

## First Places To Inspect

- 작업 전 먼저 읽을 파일과 디렉터리를 적는다.
- 예: README.md, package.json, src/, tests/, docs/

## Working Rules

- URL, public API, database schema처럼 쉽게 바꾸면 안 되는 경계를 적는다.
- 기존 패턴을 우선한다는 기준을 적는다.
- 대량 리팩터링이 금지라면 명시한다.

## Verification

- 변경 종류별 검증 명령을 적는다.
- 실행하지 못한 검증은 이유와 함께 보고하게 한다.

## Completion Checklist

- 변경 파일 요약
- 실행한 검증 명령과 결과
- 남은 리스크
- 후속 작업 후보
```

## CLAUDE.md 최소 템플릿

```md
# CLAUDE.md

## Project

- 저장소 목적:
- 주요 코드 경로:
- 테스트 경로:
- 문서 경로:

## Commands

- Build:
- Test:
- Lint:
- Format:

## Always-On Rules

- 매 세션마다 필요한 기준만 남긴다.
- 특정 디렉터리 전용 규칙은 rules로 분리한다.
- 반복 절차는 skills로 분리한다.
- 강제 경계는 settings, permissions, hooks, CI로 내려보낸다.

## Done Means

- 변경 사항을 요약한다.
- 검증 결과를 보고한다.
- 미실행 검증과 리스크를 숨기지 않는다.
```

## Codex 작업 요청 프롬프트 템플릿

```md
목표:
- 무엇을 바꿀지 한 문장으로 적는다.

범위:
- 수정 가능한 파일/디렉터리:
- 수정하지 말아야 할 파일/디렉터리:

제약:
- URL, public API, 데이터 형식, 호환성, 성능, 보안 경계를 적는다.

작업 방식:
- 먼저 구조를 파악하고, 필요한 최소 변경만 한다.
- 기존 사용자 변경을 되돌리지 않는다.
- 새 dependency는 필요할 때만 이유와 함께 제안한다.

검증:
- 실행할 명령:
- 확인할 페이지 또는 산출물:
- 실패 시 보고할 정보:

완료 기준:
- 변경 파일 목록
- 각 변경의 목적
- 검증 결과
- 남은 리스크
```

## AI agent 작업 결과 리뷰 체크리스트

- 요구한 목표가 실제 변경에 반영되었는가?
- URL, public API, 파일명, 데이터 스키마가 의도치 않게 바뀌지 않았는가?
- agent가 기존 사용자 변경을 되돌리지 않았는가?
- 새 dependency가 추가되었다면 꼭 필요한 이유가 있는가?
- build, test, lint, link check 중 필요한 검증이 실행되었는가?
- 실행하지 못한 검증이 결과에 명시되었는가?
- diff가 리뷰 가능한 크기와 범위에 머무는가?
- 보안상 민감 파일, secret, credential, 내부 로그가 노출되지 않았는가?
- 관련 문서나 운영 체크리스트가 필요한 만큼 업데이트되었는가?

## Claude Code permissions/settings 점검표

- `CLAUDE.md`에는 매번 필요한 짧은 기준만 남겼는가?
- 긴 절차는 skill이나 별도 문서로 내려갔는가?
- 경로별 규칙은 `.claude/rules/` 같은 범위 규칙으로 분리했는가?
- `.env`, secret, credential, production config 접근을 deny할지 검토했는가?
- 위험 명령 삭제, 강제 push, credential 출력은 permission 또는 hook으로 막을 수 있는가?
- MCP 연결 전에 노출되는 데이터 범위와 인증 주체를 확인했는가?
- hook이 단순 알림인지, 차단 가능한 guardrail인지 구분했는가?
- permission mode가 팀의 승인 정책과 맞는가?
- 설정 변경 후 실제로 어떤 tool call이 허용/차단되는지 테스트했는가?

## 함께 읽을 글

- [AI Engineering 허브](/ai-engineering/)
- [AGENTS.md 작성법: 저장소 목적과 검증 기준을 짧게 담기](/ai/how-to-write-agents-md-for-codex/)
- [CLAUDE.md 작성 범위: rules, skills, settings로 나누는 기준](/ai/how-far-should-claude-md-go/)
- [Codex 첫 작업 요청 작성법](/ai/how-to-write-first-codex-task-request/)
- [AI agent 검증에서 build와 test만으로 부족한 이유](/ai/build-and-test-are-not-enough-to-validate-an-agent/)
- [Claude Code settings와 permissions로 작업 경계 고정하기](/ai/fix-claude-code-boundaries-with-settings-and-permissions/)
