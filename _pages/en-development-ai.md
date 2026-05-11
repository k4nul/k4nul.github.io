---
title: "AI Engineering Hub: Coding Agent Operations and Verification"
layout: section-archive
permalink: /en/development/ai/
description: "A problem-first hub for Codex, Claude Code, harness engineering, context management, verification loops, and agent security boundaries."
author_profile: true
sidebar:
  nav: "sections"
lang: en
translation_key: topic-development-ai
section_key: development
topic_key: ai
topic_description: "A hub for making AI coding agents more repeatable through harness design, context control, verification, permissions, and security boundaries."
---

This page treats AI coding agents as operational systems, not just prompt targets. It organizes existing posts by the problem a reader is trying to solve.

## Problems Covered Here

- Codex or Claude Code gives different results for similar requests.
- `AGENTS.md` and `CLAUDE.md` keep growing without a clear boundary.
- Long logs, plans, and memory consume the context budget.
- Build and test pass, but agent work still needs a verification loop.
- MCP, hooks, settings, permissions, approvals, and guardrails need security boundaries.

## Short Answer

Reliable agent work comes from separating responsibilities: task request, instruction file, config, tool permissions, trace, and validation loop. Keep always-on documents short, move repeated procedures into templates or skills, and use settings, permissions, hooks, and CI for enforceable boundaries.

## Core Concepts

- Harness Engineering: start with [What Is Harness Engineering?](/en/ai/what-is-harness-engineering/).
- Context/Token Management: start with [Why Token Management Matters in Harness Engineering](/en/ai/why-token-management-matters-in-harness-engineering/).
- Agent Workflow: pair [How to Write Your First Codex Task Request](/en/ai/how-to-write-first-codex-task-request/) with [Operating Codex Plan-First](/en/ai/operating-codex-plan-first/).
- Verification Loop: use [Build and Test Are Not Enough to Validate an Agent](/en/ai/build-and-test-are-not-enough-to-validate-an-agent/).
- Guardrail/Approval: use [Approval Boundaries and Guardrails](/en/ai/approval-boundaries-and-guardrails/).

## Reading Order

1. [Why Do AI Coding Tools Produce Different Results?](/en/ai/why-do-results-change-when-you-switch-ai-coding-tools/)
2. [What Is Harness Engineering?](/en/ai/what-is-harness-engineering/)
3. [Project Instruction Files Should Not Be Control Planes](/en/ai/how-far-should-a-project-instruction-file-go/)
4. [How to Write AGENTS.md for Codex](/en/ai/how-to-write-agents-md-for-codex/)
5. [Why Token Management Matters in Harness Engineering](/en/ai/why-token-management-matters-in-harness-engineering/)
6. [Build and Test Are Not Enough to Validate an Agent](/en/ai/build-and-test-are-not-enough-to-validate-an-agent/)

## Problem-Based Paths

### When Codex results keep drifting

- [Treat Codex as a Work Execution Agent](/en/ai/codex-as-work-execution-agent/)
- [Why Codex Needs a Harness](/en/ai/why-codex-needs-a-harness/)
- [How to Write Your First Codex Task Request](/en/ai/how-to-write-first-codex-task-request/)
- [Operating Codex Plan-First](/en/ai/operating-codex-plan-first/)

### When AGENTS.md is unclear

- [How to Write AGENTS.md for Codex](/en/ai/how-to-write-agents-md-for-codex/)
- [Why a Good AGENTS.md Should Be Short](/en/ai/why-good-agents-md-should-be-short/)
- [Project Instruction Files Should Not Be Control Planes](/en/ai/how-far-should-a-project-instruction-file-go/)
- [Shared Problems in AGENTS.md, CLAUDE.md, and System Prompts That Burn Tokens](/en/ai/why-agents-md-claude-md-and-system-prompts-burn-tokens/)

### When context and token pressure grow

- [Why Token Management Matters in Harness Engineering](/en/ai/why-token-management-matters-in-harness-engineering/)
- [Long Logs, Long Plans, Long Memory](/en/ai/long-logs-long-plans-long-memory-agent-context-bloat/)
- [How to Design State Summaries That Save Tokens](/en/ai/how-to-design-state-summaries-that-save-tokens/)
- [How Token Management Strategies Differ Between Codex and Claude Code](/en/ai/how-token-management-strategies-differ-between-codex-and-claude-code/)
- [Token Management Series](/en/development/token-management/)

### When agent output needs verification

- [Build and Test Are Not Enough to Validate an Agent](/en/ai/build-and-test-are-not-enough-to-validate-an-agent/)
- [From Prose to Schema: Turning Handoff Into a Contract](/en/ai/from-prose-to-schema-turning-handoff-into-a-contract/)
- [Why Trace Matters More Than Results](/en/ai/why-trace-matters-more-than-the-result/)
- [From Documents to an Observable Harness](/en/ai/from-document-centered-ops-to-an-observable-harness/)

### When MCP, hooks, and permissions need boundaries

- [Approval Boundaries and Guardrails](/en/ai/approval-boundaries-and-guardrails/)
- [From Principles to Enforcement](/en/ai/from-principles-to-enforcement/)
- Future candidates: Claude Code hooks, MCP data exposure checks, task-level tool permissions, and prompt injection as a harness problem

## Practical Templates

- [AI agent operations templates](/en/development/ai/templates/)
- Includes a minimal `AGENTS.md`, minimal `CLAUDE.md`, Codex task request prompt, agent work review checklist, and Claude Code permissions/settings checklist.

## Related Posts

- [A Project Operations Template for Codex](/en/ai/codex-project-operations-template/)
- [When Should You Use Codex Subagents?](/en/ai/when-to-use-codex-subagents/)
- [Good Compression vs. Bad Compression](/en/ai/good-compression-vs-bad-compression-what-to-keep-and-what-to-drop/)
- [Why Multi-Agent Is Not the Default](/en/ai/multi-agent-is-not-the-default/)
