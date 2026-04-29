---
layout: single
title: "AI agent incident review template"
description: "A practical template for reviewing AI agent incidents across timeline, tool calls, approvals, guardrails, traces, data exposure, and follow-up actions."
date: 2026-08-04 09:00:00 +09:00
lang: en
translation_key: ai-agent-incident-review-template
section: development
topic_key: ai
categories: AI
tags: [ai, llm, agents, ai-security, ai-agent-operations]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/ai/ai-agent-incident-review-template/
---

## Summary

An AI agent incident review needs the normal incident facts plus agent-specific evidence: input sources, model and harness configuration, tool calls, approvals, guardrails, and trace contents.

This template is meant to support reproducible facts and prevention work, not blame.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: tutorial | analysis
- Test environment: No local execution. The template is based on NIST incident response guidance, CISA playbooks, and OpenAI agent trace and approval documentation.
- Tested versions: Official documentation checked on 2026-04-29. Organization-specific severity levels and legal reporting rules still apply.
- Evidence level: official documentation, security project documentation

## Verified Facts

- NIST SP 800-61 Rev. 3 frames incident response as part of cybersecurity risk management and focuses on improving preparation, detection, response, and recovery.
- CISA incident and vulnerability response playbooks emphasize standardized operating procedures and coordinated response.
- OpenAI Agents SDK tracing documents that LLM generations, tool calls, handoffs, guardrails, and custom events can appear in traces.
- OpenAI Codex security documentation advises treating prompts, tool arguments, and tool outputs as sensitive and applying retention and access controls.
- The verification date for this post is 2026-04-29.

## Template

### 1. Incident Summary

- Incident ID:
- Date written:
- Author:
- Severity:
- Current status: investigating | contained | recovered | closed
- One-line summary:
- Scope of impact:
- First detected at:
- Resolved or recovered at:

### 2. Scope and Impact

- Affected repositories, services, workspaces, cloud accounts, clusters:
- Affected users or teams:
- Data exposure status: none | possible | confirmed | under investigation
- External transfer:
- Production change:
- Cost, availability, and security impact:

### 3. Agent Task Context

- User request, original or summarized:
- Task objective:
- Agent or harness name:
- Model name and version:
- Execution location: local | CI | cloud sandbox | IDE | desktop
- Sandbox mode:
- Network access:
- Allowed tools:
- Connected MCP servers or connectors:
- System/developer instruction version:

### 4. Timeline

| Time | Event | Evidence |
| --- | --- | --- |
| HH:MM | User request received | chat/session record |
| HH:MM | First tool call executed | trace or audit log |
| HH:MM | Guardrail or approval triggered | approval record |
| HH:MM | Anomaly detected | alert or user report |
| HH:MM | Containment action | change record |
| HH:MM | Recovery verified | command output or monitoring |

Separate confirmed facts from assumptions. Mark unconfirmed entries as `assumption`.

### 5. Tool Calls and Side Effects

- Tool calls executed:
- Files and directories read:
- Files changed:
- Shell commands executed:
- External network requests:
- Cloud/API calls:
- Side effects such as deployment, deletion, permission changes, or billing actions:
- Tool calls that failed or were blocked:

### 6. Approvals and Guardrails

- Approval request timestamps:
- Approver:
- Difference between approval wording and actual execution:
- Automatic approval or pre-approval policy:
- Guardrail tripwire status:
- Input, output, and tool-call validation results:
- High-risk actions executed without approval:

### 7. Trace, Log, and Data Review

- Trace ID or session ID:
- Whether traces include prompts, tool arguments, or tool outputs:
- Personal or sensitive data included:
- Redaction status:
- Trace/log access permissions:
- Retention period:
- External collector or telemetry endpoint:

### 8. Root Cause and Contributing Factors

- Direct cause:
- Contributing factors:
- Missing guardrail:
- Excessive tool permission:
- Weak approval boundary:
- External content or prompt injection possibility:
- Missing test or documentation:

### 9. Containment, Recovery, Verification

- Containment actions:
- Credential rotation:
- Permission removal:
- Deployment rollback:
- Data deletion or recall request:
- Recovery verification:
- Recurrence monitoring:

### 10. Follow-up Actions

| Action | Owner | Due Date | Status |
| --- | --- | --- | --- |
| Reduce tool permissions |  |  | open |
| Add high-risk approval policy |  |  | open |
| Apply trace redaction |  |  | open |
| Add reproduction test |  |  | open |
| Update runbook |  |  | open |

## Writing Principles

Do not paste raw secrets into the review. Use redacted hashes, secret IDs, rotation tickets, or trace IDs when you need a verifiable reference.

"The agent made a mistake" is not a root cause. The review should explain which input, permission, guardrail, approval, or trace design made the behavior possible.

## Limitations

- This template does not replace legal reporting, privacy breach notification, or customer communication procedures.
- Organization-specific incident severity, evidence retention, and legal hold policies take precedence.
- If traces contain sensitive data, isolation and access control come before normal retention.

## References

- [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
- [CISA Federal Government Cybersecurity Incident and Vulnerability Response Playbooks](https://www.cisa.gov/resources-tools/resources/federal-government-cybersecurity-incident-and-vulnerability-response-playbooks)
- [OpenAI Agents SDK: Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [OpenAI Codex: Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [OWASP GenAI Security Project](https://genai.owasp.org/)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Expanded the template with timeline, tool-call, approval, guardrail, trace, and data-review fields for AI agent incidents.
