---
layout: single
title: "GitHub Actions security checklist"
description: "Explains GitHub Actions security checklist with official documentation, operational checks, and limitations."
date: 2026-07-02 09:00:00 +09:00
lang: en
translation_key: github-actions-security-checklist
section: security
topic_key: security-engineering
categories: Security
tags: [security, devsecops, supply-chain-security, cloud-security]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/security/github-actions-security-checklist/
---

## Summary

A GitHub Actions security review should not stop at YAML syntax. Review triggers, `GITHUB_TOKEN` permissions, secrets, third-party actions, runners, deployment identity, and untrusted input as separate security boundaries.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: analysis | tutorial
- Test environment: No live execution. This checklist is based on official GitHub Actions security documentation.
- Test version: GitHub Docs checked on 2026-04-29. No specific runner image or workflow execution version is fixed.
- Evidence level: official documentation

## Problem Statement

GitHub Actions can handle repository code, secrets, releases, packages, and cloud deployment credentials in one workflow. That makes even a small workflow part of the software supply chain. PR-controlled strings, third-party actions, broad `GITHUB_TOKEN` permissions, self-hosted runners, and long-lived cloud credentials should be reviewed explicitly.

This post gives a minimum checklist for adding or reviewing a workflow.

## Verified Facts

- GitHub documentation explains that attacker-controlled contexts can be interpreted as executable code in workflows, custom actions, and composite actions.
  Evidence: [GitHub Actions script injections](https://docs.github.com/en/actions/concepts/security/script-injections)
- An action can access `GITHUB_TOKEN` through the `github.token` context even if the workflow does not explicitly pass it, so GitHub recommends limiting token permissions.
  Evidence: [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
- The `permissions` key is the official way to modify `GITHUB_TOKEN` permissions at workflow or job scope.
  Evidence: [Modifying the permissions for the GITHUB_TOKEN](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token#modifying-the-permissions-for-the-github_token)
- GitHub's secure use reference recommends pinning third-party actions to a full-length commit SHA.
  Evidence: [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use#using-third-party-actions)
- GitHub documentation recommends OIDC for cloud-provider authentication to reduce long-lived cloud secrets.
  Evidence: [OpenID Connect in GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

## Reproduction Steps

Review a workflow in this order.

1. Check triggers.

- Compare `pull_request`, `pull_request_target`, `workflow_run`, `workflow_dispatch`, and `schedule`.
- Review whether forked PRs need secrets or write permissions.
- Do not place PR titles, branch names, issue bodies, or commit messages directly into shell code.

2. Reduce `GITHUB_TOKEN` permissions per job.

```yaml
permissions: {}

jobs:
  test:
    permissions:
      contents: read
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<full-length-sha>
```

3. Review third-party actions.

- Prefer full-length commit SHA pinning over `uses: owner/repo@v1`.
- Check source code, provenance, maintainers, update process, and Dependabot alerts.
- Apply the same review to composite actions and reusable workflows.

4. Scope secrets and environments.

- Do not provide deployment secrets to test jobs.
- Use production environments with required reviewers and branch/tag restrictions.
- Do not print secrets or pass them as command-line arguments.

5. Review runners.

- Self-hosted runners are especially risky for public repositories.
- Check whether the runner can reach internal networks, cloud metadata, Docker socket, or deployment credentials.
- Review whether workspaces, caches, or artifacts can move secrets between jobs.

6. Review deployment identity.

- Prefer OIDC over long-lived cloud keys where possible.
- Restrict OIDC subject, audience, repository, branch, and environment in the cloud IAM policy.

## Observations

- Without explicit `permissions`, a workflow depends on repository defaults, which makes review harder.
- A compromised third-party action can access secrets and token permissions available to its job.
- Script injection is not just a YAML issue. It happens when untrusted context flows into shell, JavaScript, or API calls.

## Interpretation

In my view, the core question is "which code runs with which authority?" That means triggers, token permissions, action provenance, secret scope, and runner isolation must be reviewed together.

Opinion: start every workflow with `permissions: {}` or a read-only default, then add write permissions only to the job that needs them.

## Limitations

- GitHub Enterprise settings, organization policies, repository visibility, and fork settings can change details.
- This checklist is GitHub Actions-specific. It does not directly cover GitLab CI, Jenkins, or CircleCI.
- Incident response also needs audit logs, secret rotation, runner forensics, and dependency review output.

## References

- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub Actions script injections](https://docs.github.com/en/actions/concepts/security/script-injections)
- [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
- [GitHub Actions secrets reference](https://docs.github.com/en/actions/reference/security/secrets)
- [OpenID Connect in GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added trigger, token, action pinning, secret, runner, and OIDC checks based on GitHub Actions official documentation.
