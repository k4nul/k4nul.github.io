---
layout: single
title: "Rust Service 14. Choosing defaults for CORS, rate limits, and request size"
description: "Defines operational defaults for CORS, rate limiting, and request body size limits in a Rust API."
date: 2026-12-22 09:00:00 +09:00
lang: en
translation_key: rust-api-cors-rate-limit-request-size
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
permalink: /en/rust/rust-api-cors-rate-limit-request-size/
---

## Summary

Public API defaults should start from allowing only the requests the service actually needs, not from leaving everything open and trying to close gaps later.

CORS, rate limits, and request body size limits all restrict requests, but they are not the same control. CORS is a browser cross-origin permission policy, rate limiting is an abuse and overload control, and a body limit is the maximum input size a handler should accept.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Understanding session and JWT boundaries before auth
- Next post: Building a Rust API image with Docker multi-stage builds
- Expansion criteria: before publication, reproduce allowed CORS, blocked CORS, body-limit rejection, and rate-limit rejection in the example repository, then add log examples.

## Document Information

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial / operational defaults design
- Test environment: No direct execution test. This post designs security and operational defaults for an Axum API.
- Checked versions: axum 0.8.9 documentation, tower-http 0.6.6 documentation, tower 0.5.3 documentation
- Evidence level: official documentation, security guidance, secondary explanatory material

## Problem Statement

Even after authentication is added, an API can still be too wide at the request boundary.

- Can a browser app from an unexpected origin use authenticated cookies?
- Are unnecessary HTTP methods open?
- Is a small JSON API trying to parse multi-megabyte request bodies?
- Is the rate limit protecting against per-user abuse or only adding service-wide backpressure?
- Are blocked requests diagnosable in logs?

The goal of this post is to document operational defaults that can be adjusted later. The implementation may look like adding middleware, but the policy is shared across CORS, ingress, API gateway, and application code.

## Verified Facts

- MDN explains CORS as an HTTP-header mechanism that lets a server indicate whether cross-origin browser requests are allowed.
- CORS belongs to the browser security model. It is not an authentication mechanism for curl, server-to-server calls, or malicious clients.
- `tower_http::cors::CorsLayer` configures CORS response policy, including allowed origins, methods, headers, credentials, and max age.
- For browser CORS requests that include credentials, wildcard origins should not be used as the authenticated API default. Cookie-based APIs should narrow allowed origins explicitly.
- axum 0.8.9 `DefaultBodyLimit` documentation states that the default body limit applies to extractors such as `Bytes`, `String`, `Json`, and `Form`, and that the default is 2 MB.
- `DefaultBodyLimit::max` can adjust extractor body limits, while `tower_http::limit::RequestBodyLimitLayer` can set a request body limit at the middleware layer.
- tower 0.5.3 `RateLimitLayer` limits the request rate for a service. Treat that separately from per-IP, per-user, or per-API-key abuse controls.

## Defaults Table

Write the policy as a table before turning it into code.

| Item | Suggested starting point | Reason |
| --- | --- | --- |
| Allowed origins | Explicit origins such as `https://app.example.com` | `*` is too broad for authenticated browser APIs |
| Allowed methods | Only required methods, such as `GET`, `POST`, `PATCH`, `DELETE` | Every open method should be explainable |
| Allowed headers | Required values such as `Authorization`, `Content-Type`, `x-request-id` | Avoid broad custom-header acceptance |
| Credentials | `true` only for cookie-based auth | Credentialed CORS must be reviewed with origin policy |
| JSON body limit | Start small for command APIs, for example 16 KiB | Large bodies can become an outage and abuse surface |
| Upload body limit | Raise only on upload endpoints | Do not increase the whole API default |
| Rate limit | Use ingress/API gateway or a keyed app limiter for IP/user/API-key limits | Separate abuse control from Tower's service-wide rate limit |
| Logs | origin, method, route, status, rejection code, request ID | Do not log body, token, or cookie values |

The numbers are examples. The important part is documenting why the service starts with a value and what signal would justify changing it.

## Axum Configuration Example

This example shows the shape of the policy. Adjust it for the real route layout, feature flags, environment variables, and proxy setup.

```rust
use axum::{
    extract::DefaultBodyLimit,
    http::{header, HeaderValue, Method},
    routing::post,
    Router,
};
use std::time::Duration;
use tower::ServiceBuilder;
use tower_http::{
    cors::{AllowOrigin, CorsLayer},
    limit::RequestBodyLimitLayer,
    trace::TraceLayer,
};

let allowed_origin: HeaderValue = "https://app.example.com"
    .parse()
    .expect("valid origin");

let cors = CorsLayer::new()
    .allow_origin(AllowOrigin::exact(allowed_origin))
    .allow_methods([Method::GET, Method::POST, Method::PATCH, Method::DELETE])
    .allow_headers([header::AUTHORIZATION, header::CONTENT_TYPE])
    .allow_credentials(true)
    .max_age(Duration::from_secs(600));

let app = Router::new()
    .route("/users", post(create_user))
    .layer(DefaultBodyLimit::max(16 * 1024))
    .layer(
        ServiceBuilder::new()
            .layer(TraceLayer::new_for_http())
            .layer(RequestBodyLimitLayer::new(64 * 1024))
            .layer(cors),
    );
```

If `DefaultBodyLimit` and `RequestBodyLimitLayer` are both used, document their separate roles. For example, extractor JSON input might start at 16 KiB while middleware rejects any request body above 64 KiB before the route does more work.

## Rate Limit Boundary

Rate limiting is not one setting.

| Layer | Example | Purpose |
| --- | --- | --- |
| Ingress / API gateway | Quota by IP, API key, or user | Public API abuse control |
| Application middleware | Limit login or password-reset attempts | Route-specific business protection |
| Tower service layer | Service-wide request rate or backpressure | Internal service protection |

Tower's `RateLimitLayer` is useful, but do not treat it as an automatic "60 requests per user per minute" feature. Public APIs usually need an ingress rule, API gateway rule, Redis-backed limiter, or application state keyed by the identity being limited.

## Reproduction Steps

After implementation, reproduce both accepted and rejected paths.

1. Confirm that preflight succeeds for an allowed origin.

```powershell
curl.exe -i -X OPTIONS http://127.0.0.1:3000/users `
  -H "Origin: https://app.example.com" `
  -H "Access-Control-Request-Method: POST"
```

2. Confirm that preflight from a disallowed origin is rejected or receives no CORS allow headers.

```powershell
curl.exe -i -X OPTIONS http://127.0.0.1:3000/users `
  -H "Origin: https://evil.example" `
  -H "Access-Control-Request-Method: POST"
```

3. Confirm that an oversized body returns the expected status and log code.

```powershell
$body = "{`"name`":`"" + ("x" * (17 * 1024)) + "`"}"
curl.exe -i -X POST http://127.0.0.1:3000/users `
  -H "Content-Type: application/json" `
  --data $body
```

4. Verify rate limiting at the selected layer. If ingress enforces it, inspect ingress logs and metrics. If the app enforces it, inspect route-level rejection codes.

## Observation Status

This post does not yet include executed output. Before publication, add these observations:

- CORS response headers for an allowed origin
- Response headers for a blocked origin
- HTTP status and internal log code for an oversized body
- HTTP status, internal log code, and enforcement layer for rate-limit rejection
- Confirmation that tokens, cookies, and request bodies are absent from logs

## Verification Checklist

- Is CORS described as a browser permission mechanism rather than authentication?
- Are allowed origins explicit when credentials are involved?
- Do allowed methods and headers match the route requirements?
- Are ordinary JSON body limits separated from upload endpoint limits?
- Are the roles of `DefaultBodyLimit` and `RequestBodyLimitLayer` documented?
- Is per-client rate limiting separated from service-wide backpressure?
- Do rejection logs exclude body, token, and cookie values?

## Interpretation

CORS, body limits, and rate limits are security settings and operational settings at the same time. If they are too broad, abuse and outages become easier. If they are too narrow, legitimate clients break. The useful artifact is not a perfect number; it is a table and a repeatable verification command.

Rate limiting is especially easy to flatten into one phrase. A global Tower limit protects the service. Public API abuse control usually needs a key such as user, IP address, or API key.

## Limitations

- This is a design post based on axum 0.8.9, tower-http 0.6.6, and tower 0.5.3 documentation. It does not include direct execution output.
- Real CORS behavior can be affected by browser behavior, reverse proxies, and CDN header handling.
- Upload, streaming, and multipart endpoints need separate body limits and timeout policy.
- Rate-limit numbers and keys depend on traffic patterns, authentication model, and threat model.

## References

- [MDN: Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)
- [tower-http 0.6.6 CORS module](https://docs.rs/tower-http/0.6.6/tower_http/cors/)
- [tower-http 0.6.6 RequestBodyLimitLayer](https://docs.rs/tower-http/0.6.6/tower_http/limit/struct.RequestBodyLimitLayer.html)
- [tower 0.5.3 RateLimitLayer](https://docs.rs/tower/0.5.3/tower/limit/struct.RateLimitLayer.html)
- [axum 0.8.9 DefaultBodyLimit](https://docs.rs/axum/0.8.9/axum/extract/struct.DefaultBodyLimit.html)
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Separated CORS, body-limit, and rate-limit responsibilities and added operational defaults plus a reproduction plan based on axum, tower-http, and tower documentation.
