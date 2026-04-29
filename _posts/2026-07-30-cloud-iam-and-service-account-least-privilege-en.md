---
layout: single
title: "Cloud IAM and service account least privilege"
description: "Explains how to reduce Cloud IAM overpermission through service account scope, workload identity, temporary credentials, audit logs, and review criteria."
date: 2026-07-30 09:00:00 +09:00
lang: en
translation_key: cloud-iam-and-service-account-least-privilege
section: security
topic_key: security-engineering
categories: Security
tags: [security, devsecops, supply-chain-security, cloud-security]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/security/cloud-iam-and-service-account-least-privilege/
---

## Summary

Cloud IAM least privilege is more than avoiding administrator roles. You need to separate which workload can perform which action on which resource, and for how long its credential remains valid.

A service account is the identity of a workload such as an application, batch job, CI/CD workflow, VM, or container. Because it is not tied to a human lifecycle, it is easy to leave overpermissioned and unused. When compromised, it can become a path for lateral movement and privilege escalation.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: tutorial | analysis
- Test environment: No local execution. This post is based on Google Cloud IAM, AWS IAM, and Microsoft Entra official documentation.
- Tested versions: Official documentation checked on 2026-04-29. Provider console screens and role names may change.
- Evidence level: official cloud documentation

## Problem Statement

Many cloud IAM failures are caused less by the credential format itself and more by a broadly scoped, long-lived workload identity. A CI job with organization-wide admin rights, a default service account with project Editor permissions, or a long-lived key stored in repository secrets can turn one leak into broad impact.

This post focuses on common operating criteria rather than provider-specific IAM syntax.

## Verified Facts

- Google Cloud recommends managing service accounts as resources, creating dedicated service accounts, and avoiding automatic Editor grants for default service accounts.
- Google Cloud documents that access scopes do not replace fine-grained allow policies, and that key creation and impersonation rights should be restricted.
- AWS IAM recommends temporary credentials with IAM roles for workloads and least-privilege policies scoped by actions, resources, and conditions.
- Microsoft Entra managed identity documentation recommends granting only the permissions needed and warns that unnecessary contributor-level access increases blast radius.
- The verification date for this post is 2026-04-29.

## Least-Privilege Criteria

| Review Axis | Question | Bad Signal |
| --- | --- | --- |
| Identity | Is this service account dedicated to one workload? | Multiple apps share one account |
| Resource scope | Does it really need account, project, or subscription-wide access? | Broad roles at org, project, or subscription level |
| Action scope | Are read, write, delete, deploy, and permission changes separated? | `Owner`, `Editor`, `Administrator`, or `*` permissions |
| Credential type | Does it use temporary credentials or workload identity federation? | Long-lived keys stored in CI secrets or files |
| Lifetime | Does access exist only for the task duration? | Old keys and role bindings persist forever |
| Auditability | Can logs identify which workload acted? | One service account is shared by many systems |
| Review | Are unused permissions and identities removed? | Retired applications still have active service accounts |

## Operating Procedure

1. List workloads: web runtime, batch worker, CI build, deploy job, backup job, monitoring job.
2. Assign a separate service account or workload identity to each workload.
3. Split required API actions into read, write, delete, permission-change, and deploy actions.
4. Scope resources to the narrowest practical level, such as one bucket, one repository, or one namespace.
5. Prefer cloud-native runtime identities, IAM roles, managed identities, workload identity federation, and OIDC over long-lived keys.
6. Separate CI build and deploy identities so build jobs do not carry production deployment rights.
7. Review impersonation, key creation, secret read, and permission-change rights as high-risk permissions.
8. Use audit logs and access analysis to remove unused service accounts, keys, and permissions.

## Provider Interpretation

In Google Cloud, default service accounts and service account keys are common risk points. Check whether default service accounts still have broad project roles and whether users can impersonate service accounts that are more privileged than they are.

In AWS, IAM roles and temporary credentials should be the default for workloads. Managed policies may be useful at the start, but mature workloads should narrow customer-managed policies based on real access activity.

In Azure and Microsoft Entra, understand the lifecycle difference between system-assigned and user-assigned managed identities. The right choice depends on whether shared permissions across replicas or per-resource auditability matters more.

## Review Example

An identity named `ci-deploy-prod` with `AdministratorAccess` or subscription `Contributor` is unlikely to be least privilege. A cleaner split is:

- build job: push-only rights to the artifact registry
- scan job: artifact read and security report write rights
- deploy job: deployment update rights for one service or namespace
- break-glass identity: separate storage, MFA, short approval window, and post-use review

## Limitations

- This post does not cover every IAM syntax detail for each provider.
- Some administrative operations may require temporary broad permissions. They should still have approval, expiry, and post-action review.
- Actual role design depends on organization policy, compliance requirements, and account structure.

## References

- [Google Cloud: Best practices for using service accounts securely](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts)
- [Google Cloud: Best practices for managing service account keys](https://docs.cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys)
- [AWS IAM: Security best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Microsoft Entra: Managed identity best practice recommendations](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/managed-identity-best-practice-recommendations)
- [Microsoft Entra: Workload identities overview](https://learn.microsoft.com/en-us/entra/workload-id/workload-identities-overview)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added cloud IAM least-privilege criteria, service account lifecycle guidance, and provider-specific review notes.
