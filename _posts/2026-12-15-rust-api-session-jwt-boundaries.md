---
layout: single
title: "Rust Service 13. 인증을 붙이기 전에 세션과 JWT 경계 이해하기"
description: "Rust API에 인증을 붙이기 전에 session, JWT, token 저장 위치, 만료, 폐기 경계를 비교한다."
date: 2026-12-15 09:00:00 +09:00
lang: ko
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
---

## 요약

인증은 로그인 endpoint 하나가 아니라 신뢰 경계 전체를 바꾸는 기능이다.

구현을 시작하기 전에 먼저 정해야 할 것은 “JWT를 쓸 것인가”보다 “credential을 어디에 저장하고, 누가 검증하고, 어떻게 만료시키고, 어떻게 폐기할 것인가”다. 세션과 JWT는 대체재처럼 보이지만 운영 경계가 다르다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: API 테스트에서 unit test와 integration test 분리하기
- 다음 글: CORS, rate limit, request size limit 기본값 정하기
- 보강 기준: 실제 발행 전 예제 저장소에서 session cookie 흐름 또는 JWT 흐름 중 하나를 선택하고, 실패 응답과 로그 정책을 기록한다.

## 문서 정보

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial / 보안 경계 설계
- 테스트 환경: 직접 실행 테스트 없음. 이 글은 구현 전 선택 기준을 다루며, 특정 Rust JWT crate 사용 결과를 포함하지 않는다.
- 확인한 문서: RFC 7519, RFC 8725, OWASP Session Management Cheat Sheet, OWASP JSON Web Token Cheat Sheet, OWASP REST Security Cheat Sheet
- 출처 성격: 표준 문서, 보안 가이드, 원 프로젝트 문서

## 문제 정의

인증을 붙이면 API의 모든 handler 앞에 새로운 질문이 생긴다.

- 이 요청은 누구의 요청인가?
- credential은 변조되지 않았는가?
- credential은 아직 유효한가?
- logout, 계정 정지, 권한 변경을 어떻게 반영할 것인가?
- 실패했을 때 무엇을 응답하고 무엇을 로그로 남길 것인가?

이 질문에 답하지 않은 상태에서 JWT library부터 붙이면, 나중에 만료와 폐기 정책이 구현을 끌고 다니게 된다.

## 확인한 사실

- RFC 7519는 JWT를 두 당사자 사이에 claim을 전달하기 위한 compact하고 URL-safe한 수단으로 정의한다.
- RFC 7519의 registered claim에는 `iss`, `sub`, `aud`, `exp`, `nbf`, `iat`, `jti`가 포함된다.
- RFC 8725는 RFC 7519를 업데이트하는 JWT Best Current Practice이며, 구현과 배포를 안전하게 하기 위한 지침을 제공한다.
- RFC 8725는 library가 허용 algorithm 집합을 caller가 지정할 수 있게 해야 하며, cryptographic operation에서 다른 algorithm을 사용해서는 안 된다고 설명한다.
- OWASP Session Management Cheat Sheet는 session ID exchange에 cookie를 사용하고, 다른 교환 방식은 session fixation 방어 관점에서 제한하라고 설명한다.
- OWASP Session Management Cheat Sheet는 전체 web session에 HTTPS/TLS를 사용하고 `Secure` cookie attribute를 사용해야 한다고 설명한다.
- OWASP JSON Web Token Cheat Sheet는 JWT가 기본적으로 사용자에 의한 built-in revocation 기능을 갖지 않으며, denylist 같은 방식으로 logout을 흉내 낼 수 있다고 설명한다.
- OWASP REST Security Cheat Sheet는 JWT consumer가 token integrity와 claim을 검증해야 하며, `iss`, `aud`, `exp`, `nbf` 같은 claim 확인을 언급한다.

## 선택 기준

세션과 JWT를 단순히 “stateful vs stateless”로만 비교하면 부족하다.

| 선택지 | 서버 저장 상태 | 폐기 방식 | 어울리는 상황 | 주의점 |
| --- | --- | --- | --- | --- |
| 서버 세션 + cookie | session store 필요 | session row 삭제 또는 만료 | browser 중심 앱, 즉시 logout 중요 | store 가용성, CSRF, cookie 설정 |
| 짧은 수명 access JWT | 검증 key 중심 | 짧은 `exp`, 필요 시 denylist | 여러 API가 token을 검증해야 하는 환경 | claim 검증, key rotation, 탈취 시 만료 전 위험 |
| refresh token + access token | refresh token 저장 또는 회전 상태 필요 | refresh token 폐기 | mobile/client가 access token을 자주 갱신 | 저장 위치, 재사용 감지, 탈취 대응 |

처음 서비스라면 “세션 cookie로 충분한가?”를 먼저 물어보는 편이 좋다. JWT는 분산 검증에 강점이 있지만, logout과 권한 변경을 즉시 반영하려면 다시 state가 필요해질 수 있다.

## 저장 위치 경계

credential 저장 위치는 보안 성격을 바꾼다.

| 저장 위치 | 장점 | 위험 |
| --- | --- | --- |
| `HttpOnly`, `Secure`, `SameSite` cookie | JavaScript가 직접 읽기 어렵고 browser 전송 흐름과 맞음 | CSRF 방어와 cookie scope 설정 필요 |
| JavaScript memory | page reload 후 사라져 지속성이 낮음 | XSS가 있으면 접근 가능 |
| `localStorage` | 구현이 쉬움 | XSS 발생 시 token 탈취 위험이 커짐 |
| native secure storage | mobile/desktop client에 적합 | 플랫폼별 구현과 rotation 정책 필요 |

저장 위치를 먼저 정해야 CORS, CSRF, SameSite, refresh 흐름이 이어진다. 다음 글의 CORS와 request limit 기준도 여기서 영향을 받는다.

## Axum 경계 예시

handler가 raw token parsing을 직접 반복하지 않게 한다. 인증 middleware 또는 extractor가 credential을 검증하고, handler에는 검증된 principal만 전달하는 구조가 읽기 쉽다.

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

handler는 다음 정도만 알면 된다.

```rust
pub async fn get_me(user: AuthenticatedUser) -> Result<Json<MeResponse>, ApiError> {
    Ok(Json(MeResponse::from(user)))
}
```

실제 Axum extractor 구현은 다음 단계에서 다룬다. 이 글에서는 인증 결과를 handler 입력으로 제한한다는 경계만 잡는다.

## JWT 검증 기준

JWT를 쓴다면 최소한 다음을 고정한다.

- 허용 algorithm을 설정으로 명시하고 token header만 믿지 않는다.
- `iss`가 기대한 issuer인지 확인한다.
- `aud`가 이 API를 대상으로 하는지 확인한다.
- `exp`와 `nbf`를 현재 시간 기준으로 확인한다.
- `sub`를 내부 user id로 사용할 수 있는지 별도 조회 또는 mapping 기준을 둔다.
- `jti` 또는 token digest 기반 denylist를 사용할지 결정한다.
- key rotation과 `kid` 처리 기준을 문서화한다.
- claim 값으로 database lookup이나 URL fetch를 할 때 injection/SSRF 같은 2차 위험을 고려한다.

JWT payload는 편리한 데이터 가방이 아니다. 필요한 claim만 넣고, 민감한 개인정보를 넣지 않는 것을 기본값으로 둔다. 서명된 JWT는 무결성을 보호하지만, 암호화된 JWT가 아니라면 claim 기밀성을 보장하지 않는다.

## 세션 검증 기준

서버 세션을 쓴다면 다음을 고정한다.

- session ID는 충분한 entropy를 가진 예측 불가능한 값으로 생성한다.
- session ID 자체에는 사용자 정보나 권한 정보를 넣지 않는다.
- cookie에는 `HttpOnly`, `Secure`, `SameSite` 기준을 명시한다.
- login 후 session ID를 새로 발급한다.
- idle timeout과 absolute timeout을 구분한다.
- logout, 비밀번호 변경, 계정 정지 시 session을 폐기하는 기준을 둔다.
- session store 장애 시 API가 어떤 오류를 반환할지 정한다.

세션 방식은 폐기가 명확하지만 session store가 운영 의존성이 된다. 따라서 health check, metric, 장애 응답 기준까지 함께 둬야 한다.

## 실패 응답과 로그

인증 실패는 자세할수록 공격자에게 단서가 될 수 있다. public response는 단순하게, 내부 로그는 진단 가능하게 나눈다.

| 상황 | public response | 내부 로그 예 |
| --- | --- | --- |
| credential 없음 | `401 unauthorized` | `auth.missing_credential` |
| 서명 또는 session ID 불일치 | `401 unauthorized` | `auth.invalid_credential` |
| 만료 | `401 unauthorized` | `auth.expired` |
| 폐기된 token/session | `401 unauthorized` | `auth.revoked` |
| 권한 부족 | `403 forbidden` | `auth.forbidden` |

token 원문, session ID 원문, cookie 값은 로그에 남기지 않는다. 필요하면 digest나 request id를 사용한다.

## 재현 계획

실제 구현 전 다음 결정을 문서화한다.

```text
credential type: server session cookie 또는 access JWT
storage: HttpOnly Secure SameSite cookie 또는 Authorization header
expiration: idle timeout / absolute timeout / exp
revocation: session delete 또는 token denylist
key rotation: 적용 여부와 절차
test cases: missing, invalid, expired, revoked, forbidden
```

발행 전에는 다음 테스트 결과를 추가한다.

```powershell
cargo test auth
cargo test --test auth_http
```

## 관찰 상태

아직 이 글에는 실제 실행 결과가 없다. 구현 글로 넘어가기 전에 최소한 다음 실패 사례를 기록해야 한다.

- credential이 없을 때 `401`이 반환되는 사례
- 만료된 credential이 `401`로 매핑되는 사례
- 인증은 되었지만 권한이 부족해 `403`이 반환되는 사례
- logout 후 같은 credential이 거부되는 사례

## 검증 체크리스트

- session 또는 JWT 중 첫 구현 대상을 하나로 좁혔는가?
- credential 저장 위치와 browser 보안 속성을 정했는가?
- 만료와 폐기 정책이 구현 전에 문서화되어 있는가?
- JWT를 쓴다면 algorithm allowlist, issuer, audience, expiration 검증을 명시했는가?
- 세션을 쓴다면 session store 장애와 session 폐기 기준을 정했는가?
- token, cookie, session ID 원문이 로그에 남지 않는가?
- `401`과 `403`의 기준이 분리되어 있는가?

## 해석 / 의견

JWT를 쓰면 서버가 stateless해진다는 말은 절반만 맞다. 짧은 만료만으로 충분한 시스템은 단순해질 수 있지만, 즉시 logout, 계정 정지, 권한 변경 반영이 필요하면 denylist나 token version 같은 state가 다시 들어온다.

반대로 서버 세션은 오래된 방식이라서 나쁜 것이 아니다. browser 중심 서비스에서는 cookie와 session store가 더 단순하고 폐기 가능성이 명확할 때가 많다. 중요한 것은 유행이 아니라 운영 요구사항이다.

## 한계와 예외

- 이 글은 OAuth 2.0, OpenID Connect, SSO provider 연동을 구현하지 않는다.
- JWT crate 선택, key format, password hashing은 별도 글의 범위다.
- 보안 권장사항은 조직 정책과 threat model에 따라 더 엄격해질 수 있다.
- 이 글은 구현 전 경계 설계이며 실행 로그를 포함하지 않는다.

## 참고자료

- [RFC 7519: JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519)
- [RFC 8725: JSON Web Token Best Current Practices](https://datatracker.ietf.org/doc/html/rfc8725)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP JSON Web Token Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)

## 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: 세션/JWT 선택 기준, 저장 위치, 만료/폐기, 검증 claim, 실패 응답 경계를 표준 문서와 OWASP 기준으로 보강.
