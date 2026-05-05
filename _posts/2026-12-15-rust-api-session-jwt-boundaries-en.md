---
layout: single
title: "Rust Service 13. Understanding session and JWT boundaries before auth"
description: "Compares sessions, JWTs, token storage, expiry, and revocation boundaries before adding auth to a Rust API."
date: 2026-12-15 09:00:00 +09:00
lang: en
translation_key: rust-api-session-jwt-boundaries
section: development
topic_key: rust
featured: false
track: rust
repo:
demo:
references:
categories: Rust
tags: [rust, axum, api, production, devops]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/rust/rust-api-session-jwt-boundaries/
---

## Summary

Authentication is not one login endpoint. It changes the trust boundary of every handler in the service.

Before choosing a JWT crate or a session store, decide where the credential lives, who validates it, when it expires, and how revocation works. Sessions and JWTs look interchangeable at the API surface, but their operational boundaries are different.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Separating unit and integration tests for an API
- Next post: Choosing defaults for CORS, rate limits, and request size
- Expansion criteria: before publication, choose one implementation path, either session cookies or JWTs, and record failure responses and logging policy.

## Document Information

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial / security boundary design
- Test environment: No direct execution test. This post defines implementation criteria and is not tied to a specific Rust JWT crate.
- Checked documents: RFC 7519, RFC 8725, OWASP Session Management Cheat Sheet, OWASP JSON Web Token Cheat Sheet, OWASP REST Security Cheat Sheet
- Evidence level: standards documents, security guidance, official project documentation

## Problem Statement

Adding authentication creates new questions in front of every API handler.

- Who made this request?
- Has the credential been modified?
- Is the credential still valid?
- How are logout, account suspension, and permission changes reflected?
- What should the public response say, and what should the internal log record?

If these questions are left open, the implementation tends to grow around whichever library was added first. The result is usually expiry, revocation, and logging policy hidden across middleware and handlers.

## Verified Facts

- RFC 7519 defines a JSON Web Token as a compact, URL-safe way to represent claims between two parties.
- RFC 7519 defines registered claim names including `iss`, `sub`, `aud`, `exp`, `nbf`, `iat`, and `jti`.
- RFC 8725 is a Best Current Practice document that updates RFC 7519 with security guidance for JWT implementation and deployment.
- RFC 8725 states that libraries should let callers specify the allowed algorithm set and should not use any other algorithm during cryptographic operations.
- OWASP Session Management guidance recommends exchanging session IDs through cookies and limiting other exchange mechanisms to reduce session fixation risk.
- OWASP Session Management guidance recommends HTTPS/TLS for the whole web session and the `Secure` cookie attribute.
- OWASP JSON Web Token guidance notes that JWTs do not include built-in user revocation by default, and that a denylist can simulate logout behavior.
- OWASP REST Security guidance says JWT consumers should verify token integrity and claims such as `iss`, `aud`, `exp`, and `nbf`.

## Decision Criteria

Comparing sessions and JWTs only as "stateful versus stateless" is too shallow.

| Option | Server-side state | Revocation model | Fits well when | Watch out for |
| --- | --- | --- | --- | --- |
| Server session + cookie | Session store required | Delete or expire the session row | Browser-first services where immediate logout matters | Store availability, CSRF, cookie settings |
| Short-lived signed access JWT | Verification key required | Mostly `exp`, with denylist when needed | Multiple services need to validate the same token | Claim validation, key rotation, still-valid leaked tokens |
| Refresh token + access token | Refresh token state or rotation state required | Revoke refresh token | Mobile or installed clients frequently refresh access tokens | Storage location, reuse detection, leaked refresh tokens |

For a first browser-facing service, ask whether a plain cookie-backed session is enough. JWTs are useful for distributed verification, but immediate logout or permission changes often reintroduce server-side state through denylists, token versions, or refresh-token stores.

## Storage Boundary

Where the credential lives changes the security model.

| Storage location | Strength | Risk |
| --- | --- | --- |
| `HttpOnly`, `Secure`, `SameSite` cookie | JavaScript cannot directly read it; browser sends it consistently | CSRF defense and cookie scope still matter |
| JavaScript memory | Disappears on page reload | XSS can still access it while the page is running |
| `localStorage` | Easy to implement | High token theft risk after XSS |
| Native secure storage | Fits mobile or desktop clients | Platform-specific rotation and recovery policy required |

Storage comes first because it affects CORS, CSRF, SameSite, and refresh-token design. The next post uses this decision when choosing CORS and request-limit defaults.

## Axum Boundary Example

Do not make every handler parse raw tokens. Keep credential parsing and validation in middleware or extractors, then pass a verified principal into handlers.

```rust
#[derive(Clone, Debug)]
pub struct AuthenticatedUser {
    pub user_id: UserId,
    pub session_id: Option<String>,
    pub roles: Vec<String>,
}

pub enum Credential {
    SessionCookie(String),
    BearerToken(String),
}

pub enum AuthError {
    MissingCredential,
    InvalidCredential,
    Expired,
    Revoked,
}
```

Handlers should only need the authenticated result.

```rust
pub async fn get_me(user: AuthenticatedUser) -> Result<Json<MeResponse>, ApiError> {
    Ok(Json(MeResponse::from(user)))
}
```

The concrete Axum extractor can be added later. The important boundary in this post is that handlers receive a verified principal, not raw credential strings.

## JWT Verification Criteria

If JWTs are used, fix at least these rules before implementation.

- Configure an explicit algorithm allowlist instead of trusting the token header.
- Verify `iss` against the expected issuer.
- Verify `aud` targets this API.
- Verify `exp` and `nbf` against server time.
- Decide whether `sub` can be used directly as a user ID or must be mapped through a database lookup.
- Decide whether `jti` or a token digest will be used for a denylist.
- Document key rotation and `kid` handling.
- Do not let claim values trigger database queries, URL fetches, or authorization shortcuts without validation.

JWT payloads are not secret storage. Put only the claims the API needs into the token. A signed JWT protects integrity; it does not provide confidentiality unless the token is also encrypted.

## Session Verification Criteria

If server sessions are used, fix these rules before implementation.

- Generate session IDs with enough entropy and make them unpredictable.
- Do not store user identity, role, or permission data inside the session ID itself.
- Set cookie attributes such as `HttpOnly`, `Secure`, and `SameSite`.
- Regenerate the session ID after login.
- Separate idle timeout from absolute timeout.
- Define revocation for logout, password change, and account suspension.
- Decide what the API returns when the session store is unavailable.

Sessions make revocation clear, but they add an operational dependency on the session store. Health checks, metrics, and failure responses should include that dependency.

## Failure Responses And Logs

Detailed auth failures can help an attacker. Keep the public response simple and make internal logs diagnosable.

| Case | Public response | Internal log code |
| --- | --- | --- |
| Missing credential | `401 unauthorized` | `auth.missing_credential` |
| Invalid signature or unknown session ID | `401 unauthorized` | `auth.invalid_credential` |
| Expired credential | `401 unauthorized` | `auth.expired` |
| Revoked token or session | `401 unauthorized` | `auth.revoked` |
| Authenticated but not allowed | `403 forbidden` | `auth.forbidden` |

Do not log raw tokens, session IDs, or cookie values. If correlation is needed, use a request ID or a non-reversible digest.

## Reproduction Plan

Before publication, record the selected implementation with this checklist.

```text
credential type: server session cookie or access JWT
storage: HttpOnly Secure SameSite cookie or Authorization header
expiration: idle timeout / absolute timeout / exp
revocation: session delete or token denylist
key rotation: applicable or not applicable
test cases: missing, invalid, expired, revoked, forbidden
```

Expected local test commands after implementation:

```powershell
cargo test auth
cargo test --test auth_http
```

## Observation Status

This post does not yet include executed output. Before implementation moves forward, record at least these failure cases:

- Missing credential returns `401`.
- Expired credential returns `401`.
- Authenticated but underprivileged user returns `403`.
- A credential used after logout is rejected.

## Verification Checklist

- Has the first implementation target been narrowed to either sessions or JWTs?
- Is the credential storage location compatible with browser security behavior?
- Are expiry and revocation policy documented before implementation?
- If JWTs are used, are algorithm allowlist, issuer, audience, and expiry checks explicit?
- If sessions are used, are session-store failure and session revocation behavior explicit?
- Are token, cookie, and session ID values excluded from logs?
- Are `401` and `403` criteria separated?

## Interpretation

"Using JWT" does not automatically make a service stateless. That is only partly true when short expiry is enough. If immediate logout, account suspension, or permission-change propagation matters, some form of server-side state usually returns.

Likewise, server sessions are not outdated by default. For browser-first services, a cookie and a session store can be simpler and easier to revoke. The point is not to pick the fashionable mechanism; the point is to name the operational requirements first.

## Limitations

- This post does not implement OAuth 2.0, OpenID Connect, or SSO provider integration.
- JWT crate selection, key format, and password hashing are separate topics.
- Security recommendations may need to become stricter depending on organizational policy and threat model.
- This post is a pre-implementation boundary design and does not include runtime logs.

## References

- [RFC 7519: JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519)
- [RFC 8725: JSON Web Token Best Current Practices](https://datatracker.ietf.org/doc/html/rfc8725)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP JSON Web Token Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Expanded session/JWT decision criteria, storage boundaries, expiry/revocation policy, verification claims, and failure-response boundaries using RFC and OWASP references.
