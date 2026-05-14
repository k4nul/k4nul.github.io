---
title: "AI Agent Operations Templates"
layout: single
permalink: /en/development/ai/templates/
description: "Minimal templates for AGENTS.md, CLAUDE.md, Codex task requests, agent output review, Claude Code permissions/settings, and MCP connection checks."
author_profile: true
breadcrumbs: false
sidebar:
  nav: "sections"
lang: en
translation_key: ai-agent-operations-templates
---

This page collects small templates for operating AI coding agents without turning project instructions into long control-plane documents. Use them as starting points, then remove anything that does not apply to the repository. Before connecting external tools or context, check permissions, provenance, and auditability first.

## Minimal AGENTS.md

```md
# AGENTS.md

## Repository Purpose

- Describe what this repository builds and operates in 2-4 lines.
- Name the domain boundaries the agent must not misunderstand.

## First Places To Inspect

- List files and directories to read before editing.
- Example: README.md, package.json, src/, tests/, docs/

## Working Rules

- Name boundaries such as URLs, public APIs, database schemas, and generated files.
- Prefer existing repository patterns.
- Make large refactors explicit instead of accidental.

## Verification

- List verification commands by change type.
- Require skipped checks to be reported with reasons.

## Completion Checklist

- Changed files
- Verification commands and results
- Remaining risks
- Follow-up candidates
```

## Minimal CLAUDE.md

```md
# CLAUDE.md

## Project

- Repository purpose:
- Main code paths:
- Test paths:
- Documentation paths:

## Commands

- Build:
- Test:
- Lint:
- Format:

## Always-On Rules

- Keep only rules needed every session.
- Move path-specific rules to rules files.
- Move repeated procedures to skills.
- Move enforceable boundaries to settings, permissions, hooks, or CI.

## Done Means

- Summarize changes.
- Report verification results.
- Do not hide skipped checks or risks.
```

## Codex Task Request Prompt

```md
Goal:
- State the change in one sentence.

Scope:
- Files/directories Codex may edit:
- Files/directories Codex should not edit:

Constraints:
- Note URL, public API, data format, compatibility, performance, or security boundaries.

Working Method:
- Inspect the structure first, then make the smallest useful change.
- Do not revert existing user changes.
- Add dependencies only when necessary and explain why.

Verification:
- Commands to run:
- Pages or artifacts to inspect:
- What to report if verification fails:

Done Means:
- Changed files
- Purpose of each change
- Verification results
- Remaining risks
```

## Agent Output Review Checklist

- Does the diff solve the requested goal?
- Were URLs, public APIs, filenames, or data schemas changed unintentionally?
- Did the agent avoid reverting existing user work?
- If a dependency was added, is the reason clear?
- Were the needed build, test, lint, or link checks run?
- Are skipped checks reported?
- Is the diff small enough to review?
- Were secrets, credentials, sensitive files, or internal logs exposed?
- Were required docs or operating checklists updated?

## Claude Code Permissions/Settings Checklist

- Does `CLAUDE.md` contain only short always-on guidance?
- Did long procedures move into skills or separate docs?
- Did path-specific rules move into scoped rule files?
- Should `.env`, secrets, credentials, or production config reads be denied?
- Can destructive commands, forced pushes, or credential output be blocked by permissions or hooks?
- Was the data exposed through each MCP connection reviewed?
- Is each hook an advisory check or an enforceable guardrail?
- Does the permission mode match the team's approval policy?
- Were allowed and denied tool calls tested after changing settings?

## MCP Pre-Connection Checklist

- Did you identify the owner and data classification of the system being connected?
- Did you separate read-only, write-capable, and auto-executable permissions?
- Will the agent report which issues, logs, dashboards, docs, or databases it read from?
- Are secrets, customer data, or internal security materials excluded unless explicitly approved?
- Was each third-party MCP server reviewed for trust and prompt-injection risk?
- Are tool schemas and outputs small enough to avoid polluting the working context?
- If write access is needed, do approval, dry-run, audit log, and rollback rules exist?
- Could the same task be handled more safely through file references or a short source summary?

## Related Posts

- [AI Engineering Hub](/en/development/ai/)
- [How to Write AGENTS.md for Codex](/en/ai/how-to-write-agents-md-for-codex/)
- [How to Write Your First Codex Task Request](/en/ai/how-to-write-first-codex-task-request/)
- [Build and Test Are Not Enough to Validate an Agent](/en/ai/build-and-test-are-not-enough-to-validate-an-agent/)
- [Why a Good AGENTS.md Should Be Short](/en/ai/why-good-agents-md-should-be-short/)
- [Approval Boundaries and Guardrails](/en/ai/approval-boundaries-and-guardrails/)
