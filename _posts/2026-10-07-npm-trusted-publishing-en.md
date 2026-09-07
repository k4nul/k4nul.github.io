---
layout: single
title: "Trusted Publishing and Provenance: What npm Release Evidence Still Cannot Prove"
description: "Reading npm's multiple OIDC trusted-publishing configurations and staged publishing through CI trust boundaries, approval, and provenance-policy enforcement."
date: 2026-10-07 09:00:00 +09:00
lang: en
translation_key: npm-trusted-publishing-provenance-boundaries
section: security
topic_key: supply-chain-security
categories: Security
tags: [security, npm, oidc, supply-chain, provenance, ci-cd]
published: false
permalink: /en/security/npm-trusted-publishing-provenance-boundaries/
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

OIDC trusted publishing replaces a long-lived npm publish token with a short-lived CI identity. The npm registry authorizes a publish or stage operation against configured provider-specific identity criteria—for example, repository, workflow filename, and optional environment for GitHub Actions. On 2026-09-03, npm announced GA support for multiple trusted-publishing configurations per package and staged-publishing improvements.

A valid OIDC token or provenance record does not by itself make an artifact safe. **A compromised workflow with legitimate identity can create an artifact that still appears legitimate.** This article treats signing as an input to policy enforcement, not the end of trust.

## Document Info / Environment

- Draft and verification baseline: 2026-09-07
- Document type: release analysis / CI security design guide
- Test environment: no npm package was published and no CI credential was used.
- Scope: public changelog and SLSA public post-incident analysis; no organization-specific incident claim.

## Problem Statement / 문제 정의

When a package has multiple release workflows, “use OIDC” is incomplete. Stable, prerelease, and staging paths require answers:

- Which workflow may publish or stage from which environment?
- Is direct publishing genuinely necessary?
- Which scan and provenance fields does review check?
- How are cache poisoning, broad `id-token` permission, and workflow changes controlled?

## Verified Facts / 확인된 사실

- npm announced on 2026-09-03 that a package may have more than one trusted-publishing configuration. Each configuration uses provider-specific identity criteria; for GitHub Actions these include owner, repository, workflow filename, and an optional environment.
  Evidence: [GitHub Changelog](https://github.blog/changelog/2026-09-03-multiple-trusted-publishing-configurations-for-npm/)
- A `npm publish` or `npm stage publish` operation is authorized only when its incoming OIDC token matches a configuration that permits that specific action. Configurations are additive: a token matching any applicable configuration can be authorized, and evaluation order is not guaranteed.
  Evidence: [GitHub Changelog](https://github.blog/changelog/2026-09-03-multiple-trusted-publishing-configurations-for-npm/)
- Direct publish is opt-in per configuration. GitHub/npm recommends staging-only configurations, and staged packages cannot be approved until malware scanning completes.
  Evidence: [GitHub Changelog](https://github.blog/changelog/2026-09-03-multiple-trusted-publishing-configurations-for-npm/)
- SLSA's public Mini Shai-Hulud analysis explains the boundary where a compromised build can create artifacts with legitimate identity and valid provenance.
  Evidence: [SLSA analysis](https://slsa.dev/blog/2026/05/mini-shai-hulud-what-slsa-can-and-cannot-do)

## Reproduction Steps / 재현 순서

Create a separate configuration and review table for each release path.

| Path | OIDC policy | Recommended delivery | Approval checks |
| --- | --- | --- | --- |
| stable | protected workflow + production environment | stage | version, diff, scan, provenance identity |
| prerelease | distinct workflow/environment | stage or separate registry | tag, channel, dependency changes |
| emergency | distinct short approval path | stage where its documented prerequisites fit | reason, approver, follow-up audit |

Operational constraint (verify immediately before release): staged publishing is currently for an existing npm package and requires npm CLI 11.15.0+ and Node.js 22.14.0+. A maintainer approves a staged package with 2FA; confirm these prerequisites and release ownership before making staging the default path.

Add these guardrails to CI:

1. Grant `id-token` only to the job that needs to publish.
2. Treat publish workflows and environment protection as reviewable code.
3. Treat cache keys and restore sources as trust boundaries.
4. Define an attestation-verification policy for the provenance format and producer you accept. Verify the artifact digest and available source, builder, workflow, ref, and identity fields against that policy—not merely that a signature exists. Do not rely on a `trigger` field unless the chosen producer documents it.
5. Record the owner and expiry of every direct-publish exception.

## Observations / 관찰 결과

Multiple configurations can separate release paths, but one overly broad rule becomes the weak link for the package. Staged publishing requires a maintainer to review and explicitly approve the staged package with 2FA before it is public. That is an important gate, but it can still degrade into a button click if the approver does not inspect the staged artifact and relevant release evidence.

Provenance is signed, verifiable evidence linking a package artifact to source and build information recorded by the build platform; its exact fields and trust guarantees depend on the provenance format and producer. Do not assume every trusted-published package has provenance: npm documents automatic provenance for qualifying GitHub Actions and GitLab CI/CD releases, while CircleCI trusted publishing currently does not generate provenance attestations. It does not replace source review, dependency review, secure runners, or cache isolation.

## Interpretation / 해석

A trustworthy release decision is not a Boolean. It asks five questions.

```text
right artifact?
from the intended repository and workflow?
at the intended ref and trigger?
with a reviewed dependency/build context?
approved after scan and policy checks?
```

OIDC is a strong start for reducing long-lived secrets and narrowing identity. Whether that legitimate identity was compromised remains the responsibility of separate controls.

## Limitations / 한계

- This draft analyzes public documents and did not change an npm registry or CI configuration.
- Malware scanning and staged approval do not guarantee detection or prevention of every malicious behavior or source compromise.
- Exact SLSA provenance policy depends on build system, registry, and organizational risk tolerance.

## References / 참고자료

- [Multiple trusted publishing configurations for npm](https://github.blog/changelog/2026-09-03-multiple-trusted-publishing-configurations-for-npm/)
- [npm trusted publishers](https://docs.npmjs.com/trusted-publishers)
- [npm staged publishing](https://docs.npmjs.com/staged-publishing/)
- [npm provenance statements](https://docs.npmjs.com/generating-provenance-statements)
- [Mini Shai-Hulud: What SLSA can and cannot do](https://slsa.dev/blog/2026/05/mini-shai-hulud-what-slsa-can-and-cannot-do)

## Change Log / 변경 이력

- 2026-09-07: Created as an English local draft. `published: false`; no publishing, CI, or registry setting was changed.
