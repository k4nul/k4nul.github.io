---
layout: single
title: "Everything Claude Code가 뜬 이유: Claude Code를 운영 시스템으로 바꾸는 저장소"
date: 2026-04-28 10:00:00 +09:00
lang: ko
translation_key: why-everything-claude-code-is-trending
section: development
topic_key: ai
categories: AI
tags: [ai, claude-code, agents, skills, hooks, mcp, security]
description: "168K stars를 받은 Everything Claude Code 저장소를 코드 구조, Claude Code 공식 확장 방향, 외부 글과 보안 이슈를 기준으로 정리한다."
repo: https://github.com/affaan-m/everything-claude-code
---

## 요약

Everything Claude Code는 Claude Code용 설정 모음처럼 보이지만, 실제로는 AI coding agent를 운영하기 위한 하네스 예제에 가깝다. 이 저장소가 빠르게 주목받은 이유는 `CLAUDE.md`를 잘 쓰는 수준을 넘어서 agents, skills, hooks, MCP, rules, install profiles, security scan을 하나의 운영 표면으로 묶었기 때문이다.

내 판단으로는 이 저장소의 가치는 "그대로 전부 설치하라"가 아니다. 더 중요한 가치는 Claude Code를 팀에서 반복 가능하게 쓰려면 어떤 역할 분리, 검증 루프, 보안 경계, 세션 관리가 필요한지 보여주는 참조 구현이라는 점이다.

## 문서 정보

- 작성일: 2026-04-28
- 외부 채널 게시 기준일: 2026-04-29
- 검증 기준일: 2026-04-28 12:39 +09:00
- 문서 성격: analysis
- 테스트 환경: Windows, PowerShell, 로컬 저장소 `D:/git/everything-claude-code`
- 테스트 버전: Everything Claude Code `1.10.0`, 로컬 HEAD `4e66b28`
- 출처 등급: 공식 문서, 원본 저장소, 직접 확인, 보안 리서치, 2차 블로그 자료

## 확인한 사실

원본 저장소는 `affaan-m/everything-claude-code`이며, 2026-04-28 12:39 +09:00 GitHub API 기준으로 168,513 stars와 26,124 forks를 가지고 있었다. 생성일은 2026-01-18로 확인했다.

로컬 저장소의 `VERSION`은 `1.10.0`이고, `node scripts/ci/catalog.js --text` 실행 결과 catalog count는 `48 agents`, `183 skills`, `79 commands`로 확인됐다. 이 숫자는 README의 현재 catalog summary와도 맞는다.

npm 기준 `ecc-universal` 최신 버전은 `1.10.0`이고, `ecc-agentshield` 최신 버전은 `1.4.0`으로 확인했다.

Anthropic의 Claude Code 공식 문서는 Claude Code를 단순 챗봇이 아니라 파일을 읽고, 명령을 실행하고, 코드를 수정하고, 검증할 수 있는 agentic coding environment로 설명한다. 공식 문서의 주요 확장 축은 skills, subagents, hooks, plugins, MCP다.

Check Point Research는 Claude Code의 프로젝트 설정, hooks, MCP, `ANTHROPIC_BASE_URL` 경계가 공격 표면이 될 수 있음을 공개했다. Snyk는 agent skills 생태계를 공급망 보안 관점에서 분석했고, 공개 skills에 prompt injection과 악성 payload 문제가 관찰된다고 설명했다.

## 직접 확인한 절차

```powershell
cd D:\git\everything-claude-code
git branch --show-current
git log -5 --oneline --decorate
Get-Content VERSION
node scripts/ci/catalog.js --text
npm.cmd view ecc-universal version time.created time.modified
npm.cmd view ecc-agentshield version time.created time.modified
```

직접 확인 범위는 저장소 구조, catalog count, 주요 agent/skill/hook 파일, GitHub API와 npm registry 메타데이터다. 실제 Claude Code에 ECC를 설치해 장기 사용 성능을 비교한 것은 아니다.

## 관찰 결과

저장소의 첫인상은 "많은 markdown 파일"이지만, 구조를 보면 단순 prompt 모음보다 넓다.

```text
agents/          전문 subagent 정의
skills/          재사용 workflow와 domain playbook
commands/        legacy slash command 호환 표면
hooks/           Claude Code lifecycle hook 설정
scripts/hooks/   hook 실행 스크립트
rules/           항상 적용할 공통/언어별 규칙
mcp-configs/     MCP server catalog 예시
manifests/       selective install profile
ecc2/            Rust 기반 ECC 2.0 alpha control plane
```

`agents/code-reviewer.md`는 diff 확인, 주변 코드 읽기, severity 분류, 80% 이상 확신할 때만 보고하는 규칙을 둔다. `skills/tdd-workflow/SKILL.md`는 RED/GREEN/REFACTOR를 명시하고, 테스트가 실제로 실패했는지 확인한 뒤 구현으로 넘어가도록 강제한다.

`skills/gateguard/SKILL.md`와 `scripts/hooks/gateguard-fact-force.js`는 첫 Edit/Write/Bash 전에 관련 import, public surface, 데이터 schema, 사용자 지시를 확인하도록 막는다. `skills/security-scan/SKILL.md`는 AgentShield를 통해 `.claude/`, settings, MCP, hooks, agent 정의를 스캔하는 흐름을 제공한다.

## 해석

Claude Code 공식 문서가 제시하는 확장 표면은 skills, subagents, hooks, plugins, MCP다. Everything Claude Code는 이 표면을 각각 따로 설명하는 데 그치지 않고, 한 저장소 안에 실제 파일 구조로 배치한다.

그래서 이 저장소는 "Claude Code를 더 잘 쓰는 팁"보다 "Claude Code를 운영 가능한 하네스로 다루는 예시"에 가깝다. 좋은 점은 기능 수 자체가 아니라 agent가 자주 실패하는 지점에 role, workflow, hook, scan이라는 마찰을 넣어둔 것이다.

보안 관점에서는 양면적이다. 한편으로는 AgentShield, security-scan, config-protection, MCP health check 같은 보안 장치를 제공한다. 다른 한편으로는 그 자체가 많은 hook, skill, MCP config를 포함하기 때문에 설치 전에 검토해야 할 표면도 넓다.

## 한계

이 글은 Everything Claude Code를 장기간 실사용한 성능 평가가 아니다. 저장소 구조, 코드 파일, 공식 문서, 외부 글, 보안 리서치를 기준으로 한 빠른 분석이다.

GitHub stars, forks, npm metadata는 2026-04-28 12:39 +09:00 기준 값이며 이후 달라질 수 있다. 또한 ECC의 모든 skill과 hook을 안전하다고 검증한 것도 아니다. 특히 hook과 MCP는 실행 표면이므로, 팀 환경에 적용하기 전에는 실제 설정 파일과 권한 범위를 별도로 검토해야 한다.

## 참고자료

- Everything Claude Code 원본 저장소: https://github.com/affaan-m/everything-claude-code
- Claude Code Best Practices: https://code.claude.com/docs/en/best-practices
- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code Subagents: https://code.claude.com/docs/en/sub-agents
- Claude Code Hooks: https://code.claude.com/docs/en/hooks
- Claude Code Plugins: https://code.claude.com/docs/en/plugins
- npm ecc-universal: https://www.npmjs.com/package/ecc-universal
- npm ecc-agentshield: https://www.npmjs.com/package/ecc-agentshield
- Check Point Research: https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/
- Snyk ToxicSkills: https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/

