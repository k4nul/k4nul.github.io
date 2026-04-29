---
layout: single
title: "Incident timelines and security engineering wrap-up"
description: "Explains how to write incident timelines that separate facts, assumptions, decisions, evidence, and follow-up security engineering work."
date: 2026-08-06 09:00:00 +09:00
lang: en
translation_key: incident-timeline-and-security-engineering-wrap-up
section: security
topic_key: security-engineering
categories: Security
tags: [security, devsecops, supply-chain-security, cloud-security]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/security/incident-timeline-and-security-engineering-wrap-up/
---

## Summary

An incident timeline is not decoration for a report. It is an engineering tool for improving response quality. A useful timeline separates what happened, which evidence confirms it, which decision was made at the time, and what remains an assumption.

The security engineering wrap-up is the important part: weak boundaries found during the incident must become concrete changes to permissions, logs, approvals, deployments, secrets, detection, and runbooks.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: tutorial | analysis
- Test environment: No local execution. The structure is based on NIST SP 800-61 Rev. 3 and the CISA incident response playbook.
- Tested versions: Official documentation checked on 2026-04-29. Organization-specific severity and legal reporting rules still apply.
- Evidence level: official documentation, government security guidance

## Verified Facts

- NIST SP 800-61 Rev. 3 was published in April 2025 and supersedes SP 800-61 Rev. 2.
- NIST SP 800-61 Rev. 3 connects incident response to cybersecurity risk management using CSF 2.0.
- CISA Federal Government Cybersecurity Incident and Vulnerability Response Playbooks provide standardized operating procedures for incident and vulnerability response.
- The verification date for this post is 2026-04-29.

## What to Record

| Field | Meaning | Example |
| --- | --- | --- |
| Time | Include timezone and use one standard | `2026-04-29 10:15 KST` |
| Event | Short factual statement | `production deploy job failed` |
| Source | Log, alert, commit, ticket, trace, user report | `GitHub Actions run 12345` |
| Status | Confirmed or assumption | `confirmed` |
| Impact | User, service, data, cost, security impact | `admin API 5xx increased` |
| Action | Containment, rollback, key rotation, permission removal | `deploy token revoked` |
| Decision | Who decided what and why | `incident lead approved rollback` |

## Writing Procedure

1. Choose the timeline timezone first. If logs come from multiple systems, document the conversion rule.
2. Separate detection time from estimated start time. `detected_at` and `started_at` are often different.
3. Do not paste raw logs as the timeline. Split event, evidence, and interpretation.
4. Mark confirmed facts and assumptions explicitly.
5. Separate containment from recovery. Blocking the damage and restoring the service are different.
6. For hard-to-reverse actions such as permission changes, secret rotation, deployment, or deletion, record approver and evidence.
7. End with `unknowns`. Hidden unknowns create weak follow-up work.

## Bad and Better Timeline

Bad:

```text
10:00 outage started
10:20 checked
10:40 fixed
```

Better:

```text
2026-04-29 10:03 KST | alert | API 5xx rate > 5% | Prometheus alert #123 | confirmed
2026-04-29 10:07 KST | investigation | deploy run 456 changed auth middleware | GitHub Actions run 456, commit abc123 | confirmed
2026-04-29 10:12 KST | decision | incident lead approved rollback | Slack incident channel, ticket INC-9 | confirmed
2026-04-29 10:18 KST | containment | rollback completed | deploy run 457 | confirmed
2026-04-29 10:32 KST | recovery | 5xx rate returned below threshold | dashboard snapshot | confirmed
```

## Security Engineering Wrap-Up

An incident review should not end with "be more careful." It should produce changes.

- If detection was late, update alert rules, log fields, and metrics.
- If root cause was slow to find, connect deploy records, trace IDs, commit SHAs, and change owners.
- If blast radius was large, reduce IAM, RBAC, service account, and tool permissions.
- If approval was unclear, define high-risk action approval criteria.
- If secrets were exposed, add secret scanning, rotation, and short-lived credentials.
- If recovery was slow, create rollback runbooks and dry-run verification.

## Closure Criteria

An incident is not closed just because the service is back. Close it when:

- confirmed and assumption entries are reconciled
- impact and possible data exposure are assessed
- credentials, permissions, and deployment state are recovered
- customer, internal, external, and legal reporting needs are reviewed
- follow-up actions have owners and due dates
- the reproduction conditions are documented

## Limitations

- This post does not replace legal reporting, privacy breach notification, or customer communication procedures.
- Legal, privacy, and compliance requirements take precedence.
- Do not publish detection details that would help an attacker bypass monitoring.

## References

- [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
- [NIST Incident Response project](https://csrc.nist.gov/projects/incident-response)
- [CISA Federal Government Cybersecurity Incident and Vulnerability Response Playbooks](https://www.cisa.gov/resources-tools/resources/federal-government-cybersecurity-incident-and-vulnerability-response-playbooks)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added timeline fields, evidence separation, and security engineering follow-up criteria.
