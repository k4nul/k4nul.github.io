---
layout: single
title: "Rust Service 14. CORS, rate limit, request size limit 기본값 정하기"
description: "Rust API의 CORS, rate limit, request body 크기 제한을 운영 기본값으로 고정하는 기준을 정리한다."
date: 2026-12-22 09:00:00 +09:00
lang: ko
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
---

## 요약

공개 API의 기본값은 넓게 열어 둔 뒤 막는 방식이 아니라, 필요한 요청만 통과시키는 방식에서 시작해야 한다.

CORS, rate limit, request body size limit은 모두 "요청을 제한한다"는 점에서 비슷해 보이지만 책임이 다르다. CORS는 브라우저의 cross-origin 접근 허용 정책이고, rate limit은 남용과 과부하를 줄이는 운영 정책이며, body limit은 handler가 감당할 입력 크기의 상한이다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: 인증을 붙이기 전에 세션과 JWT 경계 이해하기
- 다음 글: Docker multi-stage build로 Rust API 이미지 만들기
- 보강 기준: 실제 발행 전 예제 저장소에서 CORS 허용/거부, body limit 초과, rate limit 초과 응답을 재현하고 로그 예시를 추가한다.

## 문서 정보

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial / 운영 기본값 설계
- 테스트 환경: 직접 실행 테스트 없음. 이 글은 Axum API에 적용할 보안/운영 기본값을 설계하는 글이다.
- 확인한 버전: axum 0.8.9 문서, tower-http 0.6.6 문서, tower 0.5.3 문서
- 출처 성격: 공식 문서, 보안 가이드, 2차 설명 자료

## 문제 정의

인증을 붙인 API라도 요청 입구가 너무 넓으면 운영 중에 다른 문제가 생긴다.

- 브라우저 앱이 아닌 origin에서 인증 쿠키를 사용할 수 있는가?
- 필요하지 않은 HTTP method가 열려 있는가?
- 작은 JSON API인데 몇 MB짜리 body를 받아 파싱하려 하는가?
- rate limit이 사용자별 남용 방지인지, 서비스 전체 backpressure인지 구분되어 있는가?
- 차단된 요청이 로그에서 진단 가능한가?

이번 글의 목표는 "나중에 바꾸기 쉬운 운영 기본값"을 먼저 문서화하는 것이다. 구현은 단순한 middleware 추가처럼 보여도, 실제 정책은 CORS, ingress, API gateway, 애플리케이션 코드가 나누어 가진다.

## 확인한 사실

- MDN CORS 문서는 CORS를 서버가 cross-origin 요청 허용 여부를 알려 주는 HTTP header 기반 메커니즘으로 설명한다.
- CORS는 브라우저 보안 모델에 속한다. curl, 서버 간 호출, 악성 클라이언트까지 인증하거나 차단하는 인증 기능으로 볼 수 없다.
- `tower_http::cors::CorsLayer`는 allowed origins, methods, headers, credentials, max age 같은 CORS 응답 정책을 구성한다.
- 자격 증명을 포함하는 browser CORS 요청에서는 wildcard origin을 기본값으로 두지 않는다. 인증 cookie 기반 API는 허용 origin을 명시적으로 좁히는 편이 안전하다.
- axum 0.8.9의 `DefaultBodyLimit` 문서는 `Bytes`, `String`, `Json`, `Form` extractor에 기본 body limit이 적용되며 기본값이 2 MB라고 설명한다.
- `DefaultBodyLimit::max`로 extractor body limit을 조정할 수 있고, `tower_http::limit::RequestBodyLimitLayer`로 middleware 계층의 요청 body limit을 둘 수 있다.
- tower 0.5.3의 `RateLimitLayer`는 service에 대한 요청 rate를 제한하는 계층이다. 이 기능은 IP별, 사용자별, API key별 남용 방지 정책과는 다르게 보아야 한다.

## 기본값 표

먼저 표로 정책을 고정한 뒤 코드에 옮긴다.

| 항목 | 권장 시작점 | 이유 |
| --- | --- | --- |
| Allowed origins | `https://app.example.com`처럼 명시 | 인증 cookie 또는 browser token을 다루면 `*`는 너무 넓다 |
| Allowed methods | 필요한 method만, 예: `GET`, `POST`, `PATCH`, `DELETE` | 열려 있는 method는 운영자가 설명할 수 있어야 한다 |
| Allowed headers | `Authorization`, `Content-Type`, `x-request-id` 등 필요한 값만 | 불필요한 custom header 허용을 줄인다 |
| Credentials | cookie 인증일 때만 `true` | credential 포함 CORS는 origin 정책과 함께 검토해야 한다 |
| JSON body limit | command API는 예: 16 KiB부터 시작 | 작은 API에서 큰 body는 장애와 남용의 표면이 된다 |
| Upload body limit | upload endpoint에서만 별도 상향 | 전체 API 기본값을 키우지 않는다 |
| Rate limit | ingress/API gateway 또는 keyed app limiter에서 사용자/IP/API key 기준으로 설정 | tower의 전역 rate limit과 남용 방지를 구분한다 |
| Logs | origin, method, route, status, rejection code, request id | body, token, cookie 값은 남기지 않는다 |

숫자는 예시다. 중요한 것은 값을 고정하는 것이 아니라, 왜 이 값에서 시작했고 어떤 신호를 보고 바꿀지 남기는 것이다.

## Axum 설정 예시

아래 예시는 정책의 모양을 보여 주기 위한 코드다. 실제 프로젝트에서는 route 구조, feature flag, 환경 변수, proxy 배치에 맞춰 조정해야 한다.

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

`DefaultBodyLimit`과 `RequestBodyLimitLayer`를 동시에 쓴다면 역할을 분리해서 문서화한다. 예를 들어 extractor의 JSON 기본값은 16 KiB로 두고, middleware 계층은 route 진입 전 전체 body 상한을 64 KiB로 둔다. 이 둘이 왜 다른지 운영자가 이해할 수 있어야 한다.

## Rate Limit 경계

Rate limit은 하나의 설정값이 아니다.

| 계층 | 예시 | 목적 |
| --- | --- | --- |
| Ingress / API gateway | IP, API key, user별 quota | 공개 API 남용 방지 |
| 애플리케이션 middleware | 로그인 시도, 비밀번호 재설정 같은 민감 route 제한 | 비즈니스 규칙에 가까운 제한 |
| Tower service layer | service 전체 요청 속도 제한 또는 backpressure | 내부 service 보호 |

Tower의 `RateLimitLayer`는 유용하지만 "사용자별 1분 60회" 같은 keyed 정책을 자동으로 제공한다고 보면 안 된다. 공개 API에서는 ingress, API gateway, Redis 기반 limiter, 또는 애플리케이션 상태를 이용한 keyed limiter를 별도로 설계해야 한다.

## 재현 순서

실제 구현 후에는 허용/거부를 모두 재현한다.

1. 허용 origin의 preflight가 성공하는지 확인한다.

```powershell
curl.exe -i -X OPTIONS http://127.0.0.1:3000/users `
  -H "Origin: https://app.example.com" `
  -H "Access-Control-Request-Method: POST"
```

2. 허용하지 않은 origin의 preflight가 거부되거나 CORS header 없이 응답하는지 확인한다.

```powershell
curl.exe -i -X OPTIONS http://127.0.0.1:3000/users `
  -H "Origin: https://evil.example" `
  -H "Access-Control-Request-Method: POST"
```

3. body limit보다 큰 요청이 기대한 상태 코드와 로그로 남는지 확인한다.

```powershell
$body = "{`"name`":`"" + ("x" * (17 * 1024)) + "`"}"
curl.exe -i -X POST http://127.0.0.1:3000/users `
  -H "Content-Type: application/json" `
  --data $body
```

4. rate limit은 선택한 계층에서 따로 검증한다. ingress에서 제한한다면 ingress 로그와 metric을 확인하고, 앱에서 제한한다면 route별 rejection code를 확인한다.

## 관찰 상태

이 글에는 아직 실제 실행 결과가 없다. 발행 전에는 다음 관찰값을 추가해야 한다.

- 허용 origin 요청의 CORS 응답 header
- 차단 origin 요청의 응답 header
- body limit 초과 요청의 HTTP status와 내부 로그 code
- rate limit 초과 요청의 HTTP status, 내부 로그 code, 계층 위치
- token, cookie, request body가 로그에 남지 않는다는 확인

## 검증 체크리스트

- CORS를 인증 기능처럼 설명하지 않았는가?
- credential 포함 CORS에서 허용 origin을 명시했는가?
- 허용 method와 header가 route 요구사항과 일치하는가?
- 일반 JSON API와 upload endpoint의 body limit이 분리되어 있는가?
- `DefaultBodyLimit`과 `RequestBodyLimitLayer`의 역할이 문서화되어 있는가?
- rate limit이 per-client 정책인지 service-wide backpressure인지 구분되어 있는가?
- 차단된 요청의 로그에 body, token, cookie 값이 빠져 있는가?

## 해석 / 의견

CORS, body limit, rate limit은 보안 설정이면서 운영 설정이다. 너무 넓으면 장애와 남용이 쉬워지고, 너무 좁으면 정상 클라이언트가 막힌다. 그래서 "정답 숫자"보다 "바꿀 수 있는 표와 검증 명령"이 더 중요하다.

특히 rate limit은 이름이 같아도 계층마다 의미가 다르다. Tower의 전역 제한은 service 보호에 가깝고, 공개 API 남용 방지는 사용자/IP/API key 같은 식별자를 기준으로 해야 한다.

## 한계와 예외

- 이 글은 Axum 0.8.9, tower-http 0.6.6, tower 0.5.3 문서 기준의 설계 글이며 직접 실행 결과를 포함하지 않는다.
- 실제 CORS 동작은 browser, reverse proxy, CDN header 처리에 영향을 받을 수 있다.
- upload, streaming, multipart endpoint는 별도 body limit과 timeout 정책이 필요하다.
- rate limit 수치와 key 기준은 서비스 트래픽, 인증 방식, 위협 모델에 따라 달라진다.

## 참고자료

- [MDN: Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)
- [tower-http 0.6.6 CORS module](https://docs.rs/tower-http/0.6.6/tower_http/cors/)
- [tower-http 0.6.6 RequestBodyLimitLayer](https://docs.rs/tower-http/0.6.6/tower_http/limit/struct.RequestBodyLimitLayer.html)
- [tower 0.5.3 RateLimitLayer](https://docs.rs/tower/0.5.3/tower/limit/struct.RateLimitLayer.html)
- [axum 0.8.9 DefaultBodyLimit](https://docs.rs/axum/0.8.9/axum/extract/struct.DefaultBodyLimit.html)
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)

## 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: CORS, body limit, rate limit의 책임을 분리하고 axum/tower-http/tower 문서 기준으로 운영 기본값과 재현 계획을 보강.
