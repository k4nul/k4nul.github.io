---
layout: single
title: "After Passkeys: What Servers Must Design for WebAuthn Level 3"
description: "Using W3C WebAuthn Level 3 to frame RP ID, user mediation, attestation, credential lifecycle, and account recovery as server-design concerns."
date: 2026-09-30 09:00:00 +09:00
lang: en
translation_key: webauthn-level-3-server-design
section: security
topic_key: security-engineering
categories: Security
tags: [security, webauthn, passkeys, authentication, web-security]
published: false
permalink: /en/security/webauthn-level-3-server-design/
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

Adopting passkeys is not a single login-screen change. A server must decide which relying party (RP) accepts a credential, how a credential binds to an account, and how device loss or recovery is handled. W3C published WebAuthn Level 3 as a Recommendation on 2026-08-25.

This article treats WebAuthn not as passwordless-login marketing, but as the lifecycle and server verification problem of scoped public-key credentials.

## Document Info / Environment

- Draft and verification baseline: 2026-09-07
- Document type: standards analysis / security design guide
- Test environment: no authenticator or browser implementation was tested.
- Scope: the WebAuthn security model. Passkey-sync and recovery UX differ by product.

## Problem Statement / 문제 정의

Users replace devices, lose authenticators, change email addresses, and use multiple subdomains. A successful registration alone leaves important questions:

- Which RP ID can use this credential?
- What does the server verify in `clientDataJSON` (type, challenge, and origin), in `authenticatorData` (the expected RP ID hash and flags), and in the assertion signature?
- When does attestation add real value, and when does it add privacy cost?
- Does account recovery become a weaker authentication bypass?

## Verified Facts / 확인된 사실

- W3C published Web Authentication: An API for accessing Public Key Credentials Level 3 as a W3C Recommendation on 2026-08-25.
  Evidence: [W3C announcement](https://www.w3.org/news/2026/web-authentication-an-api-for-accessing-public-key-credentials-level-3-is-now-a-w3c-recommendation/)
- The specification defines an API for web applications to create and use strong, attested, scoped public-key credentials. A credential is scoped to a WebAuthn RP and bound to an authenticator.
  Evidence: [W3C announcement](https://www.w3.org/news/2026/web-authentication-an-api-for-accessing-public-key-credentials-level-3-is-now-a-w3c-recommendation/)
- The user agent mediates access to authenticators and credentials for privacy, while authenticators are responsible for ensuring operations do not occur without user consent.
  Evidence: [W3C announcement](https://www.w3.org/news/2026/web-authentication-an-api-for-accessing-public-key-credentials-level-3-is-now-a-w3c-recommendation/)

## Reproduction Steps / 재현 순서

Document this server-side contract before rollout.

| Item | Review question |
| --- | --- |
| RP ID and origin | What service domains and origins are allowed? |
| Challenge | How is it server-generated, unpredictable, single-use, expiry-bounded, and bound to the ceremony—and, where applicable, the session or pre-identified account? |
| Credential record | Are fields needed for verification and risk policy retained—such as credential ID, public key, signature counter, transports, UV-initialization state, and backup eligibility/state where applicable—while avoiding unnecessary attestation retention? |
| Attestation | Does policy truly need it, or only add privacy cost? |
| Recovery | What independent proof is required after loss of a strong credential? |
| Fallback | Does it become a permanent weaker bypass? |

For registration and authentication, verify the response server-side rather than accepting a client-side success message. Audit recovery, credential deletion, and new authenticator enrollment.

## Observations / 관찰 결과

In a WebAuthn ceremony, the RP verifies a public-key assertion rather than a password. If the service also offers a weaker recovery or fallback path, overall account security can still be limited by that path. Attestation is not automatically necessary: its privacy and retention impact depends on the RP’s conveyance preference, the authenticator’s attestation behavior, and what the RP stores or uses; collect and retain it only for a documented policy purpose.

Passkey synchronization and platform support affect convenience, but they do not replace server-owned boundaries such as RP ID, challenge validation, and recovery authorization.

## Interpretation / 해석

A good WebAuthn rollout produces an operating contract, not merely a passkey button.

```text
scoped credential
+ one-time verified challenge
+ credential record sufficient for verification and declared risk policy
+ recovery assurance selected for the account’s risk and documented explicitly
+ auditable lifecycle changes
```

Where recovery is materially easier to compromise than the normal authentication path, it can become an attractive attack path; assess and monitor it accordingly.

## Limitations / 한계

- This is a W3C-standard analysis, not a browser, OS, or password-manager comparison.
- WebAuthn can reduce phishing risk but does not automatically eliminate session theft, recovery abuse, or authorization flaws.
- Attestation policy depends on regulation, device management, and privacy requirements.

## References / 참고자료

- [WebAuthn Level 3 W3C Recommendation announcement](https://www.w3.org/news/2026/web-authentication-an-api-for-accessing-public-key-credentials-level-3-is-now-a-w3c-recommendation/)
- [WebAuthn Level 3 Recommendation](https://www.w3.org/TR/2026/REC-webauthn-3-20260825/)

## Change Log / 변경 이력

- 2026-09-07: Created as an English local draft. `published: false`; no site, external-channel, or actual schedule was changed.
