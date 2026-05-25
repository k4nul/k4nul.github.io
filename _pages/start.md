---
title: "Start Here"
layout: single
permalink: /start-here/
description: "AI coding agent 운영, Rust/DevOps 기반, 보안 분석 관점으로 K4NUL 블로그를 처음 읽는 문제별 경로"
author_profile: true
sidebar:
  nav: "sections"
lang: ko
translation_key: page-start
---

K4NUL 블로그는 보안 분석, Rust, DevOps, AI coding agent 운영을 다룹니다. 처음부터 전체 글 목록을 훑기보다, 지금 해결하려는 문제에 가까운 경로로 시작하는 편이 좋습니다.

## 처음 온 독자를 위한 3가지 경로

### 1. AI coding agent를 실무에 붙이고 싶은 사람

Codex나 Claude Code를 단순 코드 생성기가 아니라 저장소 작업을 수행하는 agent로 다루고 싶다면 이 경로로 시작하세요.

1. [AI 코딩 도구 결과가 달라지는 이유](/ai/why-ai-tools-produce-different-results/)
2. [하네스 엔지니어링 개념](/ai/what-is-harness-engineering/)
3. [Codex를 작업 수행 에이전트로 운영하는 기준](/ai/codex-as-work-execution-agent/)
4. [AGENTS.md 작성법](/ai/how-to-write-agents-md-for-codex/)
5. [CLAUDE.md 작성 범위](/ai/how-far-should-claude-md-go/)

### 2. Rust/DevOps 기반을 다지고 싶은 사람

agent가 만든 결과를 검증하려면 코드와 운영 기본기가 필요합니다. Rust와 DevOps 글은 그 기반을 만드는 경로입니다.

1. [Rust 설치와 Hello World 실행하기](/rust/rust-install-hello-world/)
2. [Rust ownership, borrowing, lifetime 기초](/rust/rust-ownership-borrowing-lifetimes/)
3. [작은 Rust CLI 프로젝트 만들기](/rust/rust-build-a-small-cli-project/)
4. [Docker 컨테이너와 VM 차이](/devops/docker-containers-vs-vms/)
5. [Dockerfile과 build context 이해하기](/devops/dockerfile-basics-and-build-context/)

### 3. 보안 분석과 자동화 관점으로 읽고 싶은 사람

AI agent 운영에서도 민감정보, 권한, trace, 승인 경계가 중요합니다. 보안 글과 AI 운영 글을 함께 읽으면 검증 관점이 선명해집니다.

1. [매크로 문서형 악성코드 분석](/malware/macro-malware/)
2. [RTF 문서형 악성코드 분석](/malware/rtf-malware/)
3. [approval과 guardrail 경계](/ai/approval-boundaries-and-guardrails/)
4. [agent trace가 결과보다 중요한 이유](/ai/why-trace-matters-more-than-results/)
5. [Claude Code settings와 permissions 경계](/ai/fix-claude-code-boundaries-with-settings-and-permissions/)

## 문제별 읽기 경로

- Codex가 매번 다른 결과를 낼 때: [Codex에 하네스가 필요한 이유](/ai/why-codex-needs-a-harness/) → [Codex plan-first 운영](/ai/operating-codex-plan-first/) → [Codex config로 일관성 확보하기](/ai/using-config-to-keep-codex-consistent/)
- `AGENTS.md`가 길어질 때: [AGENTS.md 작성법](/ai/how-to-write-agents-md-for-codex/) → [좋은 AGENTS.md를 짧게 쓰는 기준](/ai/why-good-agents-md-should-be-short/) → [instruction file과 control plane 경계](/ai/project-instruction-files-should-not-be-control-planes/)
- `CLAUDE.md`와 rules가 비대해질 때: [Claude Code 운영 구조](/ai/claude-code-as-operating-structure/) → [CLAUDE.md 작성 범위](/ai/how-far-should-claude-md-go/) → [Claude Code 프로젝트 운영 템플릿](/ai/claude-code-project-operations-template/)
- Claude Code 작업을 분리할지 판단할 때: [멀티에이전트 사용 기준](/ai/multi-agent-is-not-the-default/) → [Codex subagent 사용 기준](/ai/when-to-use-codex-subagents/) → [Claude Code subagent 사용 기준](/ai/when-to-use-claude-code-subagents/)
- 컨텍스트가 너무 커질 때: [AI 에이전트 토큰 관리](/ai/why-token-management-matters-in-harness-engineering/) → [agent context 비대화 원인](/ai/long-logs-long-plans-long-memory-agent-context-bloat/) → [Claude Code context budget 관리](/ai/handle-logs-issues-and-auto-memory-with-context-budget/) → [working state summary 설계법](/ai/how-to-design-state-summaries-that-save-tokens/)
- 작업 결과를 검증하고 싶을 때: [build와 test만으로 부족한 이유](/ai/build-and-test-are-not-enough-to-validate-an-agent/) → [handoff schema 계약](/ai/from-prose-to-schema-turning-handoff-into-a-contract/) → [PR/MR 기반 협업 흐름과 리뷰 기준](/devops/git-pr-mr-collaboration-review/)

## 추천 첫 글 5개

1. [AI 코딩 도구 결과가 달라지는 이유](/ai/why-ai-tools-produce-different-results/)
2. [하네스 엔지니어링 개념](/ai/what-is-harness-engineering/)
3. [AGENTS.md 작성법](/ai/how-to-write-agents-md-for-codex/)
4. [AI 에이전트 토큰 관리와 컨텍스트 안정성](/ai/why-token-management-matters-in-harness-engineering/)
5. [Rust 설치와 Hello World 실행하기](/rust/rust-install-hello-world/)

## 깊게 읽을 시리즈

- [AI Engineering 허브](/ai-engineering/): Codex, Claude Code, 하네스, 검증, 보안 경계를 문제별로 묶은 중심 허브
- [토큰 관리 시리즈](/development/token-management/): 긴 지시, 로그, memory, 압축, Codex/Claude Code 차이
- [Rust 학습 가이드](/rust/): Rust 기본기와 작은 CLI 프로젝트
- [DevOps 운영 흐름](/devops/): Docker에서 시작해 운영 자동화로 확장하는 기반
- [Security 아카이브](/security/): 문서형 악성코드 분석과 보안 엔지니어링 관점
