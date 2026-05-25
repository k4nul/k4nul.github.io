---
title: "AI Engineering 허브: 코딩 에이전트 운영과 검증"
layout: section-archive
permalink: /ai-engineering/
description: "Codex, Claude Code, 하네스 엔지니어링, 토큰 관리, 검증 루프, 보안 경계를 문제별로 따라 읽는 AI Engineering 허브"
author_profile: true
sidebar:
  nav: "sections"
lang: ko
translation_key: topic-development-ai
section_key: development
topic_key: ai
topic_description: "AI 코딩 도구를 더 많이 쓰는 방법보다, 작업 결과를 예측 가능하게 만들기 위한 하네스, 컨텍스트, 검증, 권한 경계를 정리하는 허브다."
---

이 페이지는 Codex나 Claude Code를 “잘 물어보는 법”보다, AI coding agent가 저장소 안에서 반복 가능한 결과를 내도록 만드는 운영 구조를 다룹니다. 글 발행 순서가 아니라 독자가 겪는 문제 기준으로 읽기 경로를 묶었습니다.

운영 템플릿부터 보고 싶다면 [AI agent 운영 실전 템플릿](/ai-engineering/templates/)에서 AGENTS.md, CLAUDE.md, Codex 작업 요청, permissions/settings, MCP 연결 전 점검 기준을 묶어 볼 수 있습니다.

## 이 페이지에서 다루는 문제

- 같은 요청인데 Codex나 Claude Code 결과가 매번 달라진다.
- `AGENTS.md`와 `CLAUDE.md`에 무엇을 넣고 무엇을 빼야 할지 모르겠다.
- 긴 로그, 긴 계획, auto memory 때문에 컨텍스트가 쉽게 비대해진다.
- build/test는 통과했지만 agent가 제대로 일했는지 확신하기 어렵다.
- MCP, hooks, settings, permissions가 편의 기능인지 보안 경계인지 헷갈린다.

## 빠른 결론

AI agent 운영의 핵심은 프롬프트를 길게 쓰는 것이 아니라, 작업 요청, instruction file, config, tool permission, trace, 검증 루프를 서로 다른 책임으로 나누는 것입니다. 문서에는 매번 필요한 기준만 남기고, 반복 절차는 template이나 skill로, 강제 경계는 settings, permissions, hook, CI로 내려야 합니다.

## 핵심 개념

- Harness Engineering: 모델 바깥의 실행 환경, 권한, 검증, 기록을 설계하는 일입니다. 먼저 [하네스 엔지니어링 개념](/ai/what-is-harness-engineering/)을 읽으면 전체 지도가 잡힙니다.
- Context/Token Management: 토큰 절약보다 컨텍스트 안정성이 중요합니다. 시작점은 [AI 에이전트 토큰 관리와 컨텍스트 안정성](/ai/why-token-management-matters-in-harness-engineering/)입니다.
- Agent Workflow: 요청, 계획, 수정, 검증, handoff를 반복 가능한 흐름으로 만드는 일입니다. [Codex 첫 작업 요청 작성법](/ai/how-to-write-first-codex-task-request/)과 [Codex plan-first 운영](/ai/operating-codex-plan-first/)을 함께 보세요.
- Verification Loop: build/test 결과만으로는 부족합니다. [AI agent 검증에서 build와 test만으로 부족한 이유](/ai/build-and-test-are-not-enough-to-validate-an-agent/)가 기준점입니다.
- Guardrail/Approval: 자연어 지시가 아니라 승인 경계와 차단 규칙으로 위험 행동을 줄입니다. [approval과 guardrail 경계](/ai/approval-boundaries-and-guardrails/)에서 출발하세요.

## 읽는 순서

1. [AI 코딩 도구 결과가 달라지는 이유](/ai/why-ai-tools-produce-different-results/)
2. [하네스 엔지니어링 개념](/ai/what-is-harness-engineering/)
3. [프로젝트 지침 파일과 하네스의 책임 경계](/ai/project-instruction-files-should-not-be-control-planes/)
4. [AGENTS.md 작성법](/ai/how-to-write-agents-md-for-codex/)
5. [CLAUDE.md 작성 범위](/ai/how-far-should-claude-md-go/)
6. [AI 에이전트 토큰 관리와 컨텍스트 안정성](/ai/why-token-management-matters-in-harness-engineering/)
7. [agent 작업 검증 루프](/ai/build-and-test-are-not-enough-to-validate-an-agent/)

## 문제별 추천 경로

### Codex가 매번 다른 결과를 낼 때

- [AI 코딩 도구 결과가 달라지는 이유](/ai/why-ai-tools-produce-different-results/)
- [Codex를 작업 수행 에이전트로 운영하는 기준](/ai/codex-as-work-execution-agent/)
- [Codex에 하네스가 필요한 이유](/ai/why-codex-needs-a-harness/)
- [Codex 작업을 plan-first로 운영하기](/ai/operating-codex-plan-first/)

### AGENTS.md를 어떻게 써야 할지 모를 때

- [AGENTS.md 작성법: 저장소 목적과 검증 기준을 짧게 담기](/ai/how-to-write-agents-md-for-codex/)
- [좋은 AGENTS.md를 짧게 쓰는 기준](/ai/why-good-agents-md-should-be-short/)
- [instruction file이 control plane이 되면 안 되는 이유](/ai/project-instruction-files-should-not-be-control-planes/)
- [AGENTS.md, CLAUDE.md, system prompt가 토큰을 태우는 구조](/ai/why-agents-md-claude-md-and-system-prompts-burn-tokens/)

### Claude Code 설정이 비대해질 때

- [Claude Code를 운영 구조로 이해하기](/ai/claude-code-as-operating-structure/)
- [CLAUDE.md 작성 범위: rules, skills, settings로 나누는 기준](/ai/how-far-should-claude-md-go/)
- [AGENTS.md가 있는 저장소에서 Claude Code를 함께 쓰는 법](/ai/use-claude-code-with-agents-md/)
- [rules와 skills로 지시 로딩을 나누는 기준](/ai/split-instructions-with-rules-and-skills/)
- [Claude Code subagent 사용 기준: 전문 에이전트를 언제 분리할까](/ai/when-to-use-claude-code-subagents/)
- [Claude Code 프로젝트 운영 템플릿: CLAUDE.md, rules, skills, settings 묶기](/ai/claude-code-project-operations-template/)

### 토큰/컨텍스트 관리가 어려울 때

- [AI 에이전트 토큰 관리: 비용보다 중요한 컨텍스트 안정성](/ai/why-token-management-matters-in-harness-engineering/)
- [긴 로그와 긴 계획이 agent context를 비대하게 만드는 이유](/ai/long-logs-long-plans-long-memory-agent-context-bloat/)
- [Claude Code context budget: 긴 로그, 이슈, auto memory 관리 기준](/ai/handle-logs-issues-and-auto-memory-with-context-budget/)
- [working state summary 설계법](/ai/how-to-design-state-summaries-that-save-tokens/)
- [Codex와 Claude Code의 토큰 관리 전략 차이](/ai/how-token-management-strategies-differ-between-codex-and-claude-code/)
- [토큰 관리 시리즈 아카이브](/development/token-management/)

### AI agent 작업 결과를 검증하고 싶을 때

- [build와 test만으로 agent 작업 검증이 부족한 이유](/ai/build-and-test-are-not-enough-to-validate-an-agent/)
- [handoff를 schema 계약으로 바꾸는 방법](/ai/from-prose-to-schema-turning-handoff-into-a-contract/)
- [trace가 결과보다 중요한 이유](/ai/why-trace-matters-more-than-results/)
- [문서 중심 운영에서 observable harness로 전환하기](/ai/from-document-centered-ops-to-observable-harness/)
- [PR/MR 기반 협업 흐름과 리뷰 기준](/devops/git-pr-mr-collaboration-review/)

### MCP/hooks/permissions/settings 보안 경계를 잡고 싶을 때

- [approval과 guardrail 경계](/ai/approval-boundaries-and-guardrails/)
- [Claude Code settings와 permissions로 작업 경계 고정하기](/ai/fix-claude-code-boundaries-with-settings-and-permissions/)
- [Claude Code hooks 활용: 검증과 guardrail을 자동화하는 기준](/ai/automate-validation-and-guardrails-with-hooks/)
- [Claude Code MCP 운영: 외부 문맥을 붙여 넣지 않고 연결하는 법](/ai/connect-external-context-with-mcp/)
- [하네스 원칙을 enforcement로 옮기는 기준](/ai/from-principles-to-enforcement/)
- 추후 작성 후보: task 단위 tool permission 제한, prompt injection을 하네스 문제로 다루는 글

## 실전 템플릿

- [AI agent 운영 실전 템플릿](/ai-engineering/templates/)
- 포함 내용: `AGENTS.md` 최소 템플릿, `CLAUDE.md` 최소 템플릿, Codex 작업 요청 프롬프트, agent 결과 리뷰 체크리스트, Claude Code permissions/settings 점검표, MCP 연결 전 점검표

## 관련 글 링크

- [Codex 프로젝트 운영 템플릿](/ai/codex-project-operations-template/)
- [Codex subagent 사용 기준](/ai/when-to-use-codex-subagents/)
- [Claude Code subagent 사용 기준](/ai/when-to-use-claude-code-subagents/)
- [Claude Code 프로젝트 운영 템플릿](/ai/claude-code-project-operations-template/)
- [Claude Code settings와 permissions 경계](/ai/fix-claude-code-boundaries-with-settings-and-permissions/)
- [좋은 압축과 나쁜 압축](/ai/good-compression-vs-bad-compression-what-to-keep-and-what-to-drop/)
- [멀티 에이전트가 기본값이 아닌 이유](/ai/multi-agent-is-not-the-default/)
