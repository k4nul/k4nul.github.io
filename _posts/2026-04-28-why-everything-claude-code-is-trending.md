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
featured: false
track: ai-engineering
repo: https://github.com/affaan-m/everything-claude-code
references:
  - https://github.com/affaan-m/everything-claude-code
  - https://code.claude.com/docs/en/best-practices
  - https://code.claude.com/docs/en/skills
  - https://code.claude.com/docs/en/sub-agents
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/plugins
  - https://www.npmjs.com/package/ecc-universal
  - https://www.npmjs.com/package/ecc-agentshield
  - https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/
  - https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/
  - https://www.bighatgroup.com/blog/everything-claude-code-ai-agent-harness-guide/
  - https://emelia.io/hub/everything-claude-code-explained
  - https://opentools.ai/resources/everything-claude-code
author_profile: false
sidebar:
  nav: "sections"
---

최근 Claude Code 주변에서 가장 빠르게 눈에 띄는 저장소를 하나만 고르라면 Everything Claude Code를 빼기 어렵다. 2026-04-28 GitHub API 기준으로 이 저장소는 168K stars를 넘겼고, 생성된 지 몇 달 되지 않은 시점에 Claude Code를 "개인 도구"가 아니라 "팀 운영 시스템"처럼 다루는 예제로 소비되고 있다.

이 글은 그 인기가 단순한 숫자 놀음인지, 아니면 실제로 참고할 만한 구조가 있는지 빠르게 확인하기 위한 요약이다.

## Summary / 요약

Everything Claude Code는 Claude Code용 설정 모음처럼 보이지만, 실제로는 AI coding agent를 운영하기 위한 하네스 예제에 가깝다. 이 저장소가 빠르게 주목받은 이유는 `CLAUDE.md`를 잘 쓰는 수준을 넘어서, agents, skills, hooks, MCP, rules, install profiles, security scan을 하나의 운영 표면으로 묶었기 때문이다.

내 판단으로는 이 저장소의 가치는 "그대로 전부 설치하라"가 아니다. 더 중요한 가치는 Claude Code를 팀에서 반복 가능하게 쓰려면 어떤 역할 분리, 검증 루프, 보안 경계, 세션 관리가 필요한지 보여주는 참조 구현이라는 점이다.

## Document Info / Environment

- 작성일: 2026-04-28
- 검증 기준일: 2026-04-28 12:39 +09:00
- 문서 성격: analysis
- 테스트 환경: Windows, PowerShell, 로컬 저장소 `D:/git/everything-claude-code`
- 테스트 버전: Everything Claude Code `1.10.0`, 로컬 HEAD `4e66b28`
- 출처 등급: 공식 문서, 원본 저장소, 직접 확인, 보안 리서치, 2차 블로그 자료

## Problem Statement / 문제 정의

최근 Claude Code 주변에서 Everything Claude Code라는 저장소가 빠르게 언급되고 있다. GitHub star 수가 비정상적으로 빠르게 늘었고, 여러 블로그와 커뮤니티 글에서 "Claude Code를 엔지니어링 팀처럼 쓰게 해준다"는 식으로 소개된다.

하지만 star 수만 보고 좋은 저장소라고 판단하기는 어렵다. 이 글에서는 다음 세 가지를 분리해서 본다.

1. 저장소 코드와 파일 구조에서 직접 확인되는 것
2. Claude Code 공식 확장 방향과 맞물리는 부분
3. 외부 블로그와 보안 리서치가 이 저장소를 이슈로 만드는 이유

## Verified Facts / 확인한 사실

원본 저장소는 `affaan-m/everything-claude-code`이며, 2026-04-28 12:39 +09:00 GitHub API 기준으로 168,513 stars와 26,124 forks를 가지고 있었다. 생성일은 2026-01-18로 확인했다.
근거: [GitHub 저장소](https://github.com/affaan-m/everything-claude-code)

로컬 저장소의 `VERSION`은 `1.10.0`이고, `node scripts/ci/catalog.js --text` 실행 결과 catalog count는 `48 agents`, `183 skills`, `79 commands`로 확인됐다. 이 숫자는 README의 현재 catalog summary와도 맞는다.
근거: 로컬 직접 확인, [README](https://github.com/affaan-m/everything-claude-code)

npm 기준 `ecc-universal` 최신 버전은 `1.10.0`이고, `ecc-agentshield` 최신 버전은 `1.4.0`으로 확인했다.
근거: npm registry 직접 조회, [ecc-universal](https://www.npmjs.com/package/ecc-universal), [ecc-agentshield](https://www.npmjs.com/package/ecc-agentshield)

Anthropic의 Claude Code 공식 문서는 Claude Code를 단순 챗봇이 아니라 파일을 읽고, 명령을 실행하고, 코드를 수정하고, 검증할 수 있는 agentic coding environment로 설명한다. 공식 문서의 주요 확장 축은 skills, subagents, hooks, plugins, MCP다.
근거: [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices), [Skills](https://code.claude.com/docs/en/skills), [Subagents](https://code.claude.com/docs/en/sub-agents), [Hooks](https://code.claude.com/docs/en/hooks), [Plugins](https://code.claude.com/docs/en/plugins)

Check Point Research는 Claude Code의 프로젝트 설정, hooks, MCP, `ANTHROPIC_BASE_URL` 경계가 공격 표면이 될 수 있음을 공개했다. 해당 글은 `CVE-2025-59536`, `CVE-2026-21852`를 다룬다.
근거: [Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)

Snyk는 agent skills 생태계를 공급망 보안 관점에서 분석했고, 공개 skills에 prompt injection과 악성 payload 문제가 관찰된다고 설명했다.
근거: [Snyk ToxicSkills](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)

## Reproduction Steps / 재현 절차

이 글은 기능 성능 벤치마크가 아니라 저장소 구조와 외부 자료를 기준으로 한 분석이다. 로컬에서 확인한 절차는 다음과 같다.

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

## Observations / 관찰 결과

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

`agents/code-reviewer.md`는 단순히 "코드 리뷰해라"가 아니라 diff 확인, 주변 코드 읽기, severity 분류, 80% 이상 확신할 때만 보고하는 규칙을 둔다. 이건 AI review의 흔한 문제인 noise를 줄이려는 설계다.

`skills/tdd-workflow/SKILL.md`는 RED/GREEN/REFACTOR를 명시하고, 테스트가 실제로 실패했는지 확인한 뒤 구현으로 넘어가도록 강제한다. Claude Code가 테스트를 실행할 수 있다는 점을 workflow로 굳힌 사례다.

`skills/gateguard/SKILL.md`와 `scripts/hooks/gateguard-fact-force.js`는 더 흥미롭다. 첫 Edit/Write/Bash 전에 관련 import, public surface, 데이터 schema, 사용자 지시를 확인하도록 막는다. 모델에게 "조심해"라고 말하는 대신, 편집 전에 사실을 모으게 하는 방식이다.

`agents/silent-failure-hunter.md`는 empty catch, 숨겨진 fallback, 실패를 성공처럼 보이게 만드는 코드를 찾는다. 실제 Claude Code 사용자들이 자주 말하는 "겉으로는 동작하는 것처럼 보였는데 나중에 보니 실패를 숨겼다"는 문제와 맞닿아 있다.

`skills/security-scan/SKILL.md`는 AgentShield를 통해 `.claude/`, settings, MCP, hooks, agent 정의를 스캔하는 흐름을 제공한다. Claude Code 설정 자체가 실행 표면이 될 수 있다는 점을 전제로 한다.

## Interpretation / 해석

### 1. 이 저장소는 Claude Code의 현재 방향과 맞물린다

Claude Code 공식 문서가 제시하는 확장 표면은 skills, subagents, hooks, plugins, MCP다. Everything Claude Code는 이 표면을 각각 따로 설명하는 데 그치지 않고, 한 저장소 안에 실제 파일 구조로 배치한다.

그래서 이 저장소는 "Claude Code를 더 잘 쓰는 팁"보다 "Claude Code를 운영 가능한 하네스로 다루는 예시"에 가깝다. 공식 기능이 빠르게 늘어나는 시점에, 그 기능들을 어떻게 조합할지 보여준 점이 주목을 받기 쉬웠다.

### 2. 좋은 점은 기능 수가 아니라 실패 모드를 줄이려는 설계다

AI coding agent의 실패는 대부분 코드 생성 능력 부족만으로 설명되지 않는다. 더 흔한 문제는 다음과 같다.

- 맥락을 충분히 읽지 않고 바로 수정한다.
- 테스트가 실제로 실패했는지 확인하지 않고 구현한다.
- 오류를 숨기는 fallback을 넣는다.
- 보안 경계를 instruction으로만 처리한다.
- 세션이 길어지면 앞의 합의를 잊는다.

ECC는 이 문제를 role, workflow, hook, scan으로 나눠서 다룬다. `planner`, `code-reviewer`, `tdd-guide`, `security-reviewer`처럼 역할을 나누고, `tdd-workflow`, `gateguard`, `continuous-learning-v2`, `security-scan`처럼 반복 절차를 skill과 hook으로 옮긴다.

내 판단으로는 이 지점이 ECC의 핵심 가치다. 좋은 prompt를 많이 모은 것이 아니라, agent가 자주 실패하는 지점에 마찰을 넣어둔 것이다.

### 3. 보안 이슈와도 같은 방향을 본다

Claude Code의 hooks, MCP, project settings는 편리하지만 실행 표면이다. Check Point가 공개한 Claude Code CVE 사례는 프로젝트 안의 설정이 신뢰 경계가 될 수 있음을 보여준다. Snyk의 ToxicSkills 분석도 skills를 새로운 공급망 표면으로 본다.

이 관점에서 ECC는 양면적이다. 한편으로는 AgentShield, security-scan, config-protection, MCP health check 같은 보안 장치를 제공한다. 다른 한편으로는 그 자체가 많은 hook, skill, MCP config를 포함하기 때문에 설치 전에 검토해야 할 표면도 넓다.

따라서 이 저장소를 "보안까지 해결해주는 만능 패키지"로 소개하면 안 된다. 더 정확한 설명은 "Claude Code 설정도 공급망처럼 검토해야 한다는 문제의식을 포함한 대형 설정 프레임워크"다.

### 4. 전부 설치보다 필요한 패턴을 가져오는 편이 현실적이다

확인한 외부 글은 대체로 ECC를 구체 모듈 중심으로 설명한다. Big Hat Group은 agent, skill, hook, learning layer를 나눠 설명하고, Emelia는 agents, skills, hooks, AgentShield, continuous learning을 성장 배경으로 다룬다. 다만 이런 2차 자료가 커뮤니티 전체의 합의를 대표한다고 보기는 어렵다. 그래서 여기서는 외부 반응을 "전부 설치할 근거"가 아니라 "어떤 패턴이 주목받는지 보여주는 보조 맥락"으로만 본다.
근거: [Big Hat Group](https://www.bighatgroup.com/blog/everything-claude-code-ai-agent-harness-guide/), [Emelia](https://emelia.io/hub/everything-claude-code-explained), [OpenTools](https://opentools.ai/resources/everything-claude-code)

내 의견은 선택적 채택에 가깝다. 처음부터 full profile을 설치하기보다는 다음 순서가 낫다.

1. `code-reviewer`와 `tdd-workflow`를 읽고 자신의 프로젝트 규칙으로 줄인다.
2. `gateguard`처럼 편집 전 조사 gate가 필요한지 판단한다.
3. MCP는 필요한 것만 켜고, credential이 들어가는 서버는 별도로 검토한다.
4. hooks는 `minimal`에 가까운 구성으로 시작하고, 문제가 반복되는 지점에만 추가한다.
5. AgentShield 같은 scanner로 `.claude/`와 MCP 설정을 검토한다.

## Limitations / 한계

이 글은 Everything Claude Code를 장기간 실사용한 성능 평가가 아니다. 저장소 구조, 코드 파일, 공식 문서, 외부 글, 보안 리서치를 기준으로 한 빠른 분석이다.

GitHub stars, forks, npm metadata는 2026-04-28 12:39 +09:00 기준 값이며 이후 달라질 수 있다. 또한 일부 외부 글은 작성 당시의 수치를 사용하기 때문에, 현재 저장소의 `48 agents / 183 skills / 79 commands`와 다르게 `28 agents`, `119 skills`, `60 commands`처럼 과거 숫자를 적고 있다.

ECC의 모든 skill과 hook을 안전하다고 검증한 것도 아니다. 특히 hook과 MCP는 실행 표면이므로, 팀 환경에 적용하기 전에는 실제 설정 파일과 권한 범위를 별도로 검토해야 한다.

## References / 참고자료

- Everything Claude Code 원본 저장소: [github.com/affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)
- Claude Code Best Practices: [code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices)
- Claude Code Skills: [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)
- Claude Code Subagents: [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents)
- Claude Code Hooks: [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks)
- Claude Code Plugins: [code.claude.com/docs/en/plugins](https://code.claude.com/docs/en/plugins)
- npm ecc-universal: [npmjs.com/package/ecc-universal](https://www.npmjs.com/package/ecc-universal)
- npm ecc-agentshield: [npmjs.com/package/ecc-agentshield](https://www.npmjs.com/package/ecc-agentshield)
- Check Point Research, Claude Code CVE 분석: [research.checkpoint.com](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)
- Snyk, ToxicSkills 분석: [snyk.io](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
- Big Hat Group, ECC 소개 글: [bighatgroup.com](https://www.bighatgroup.com/blog/everything-claude-code-ai-agent-harness-guide/)
- Emelia, ECC 성장 배경 소개: [emelia.io](https://emelia.io/hub/everything-claude-code-explained)
- OpenTools, ECC resource page: [opentools.ai](https://opentools.ai/resources/everything-claude-code)

## Change Log / 변경 이력

- 2026-04-28: Everything Claude Code 로컬 코드 분석과 외부 자료를 바탕으로 초안 작성.
