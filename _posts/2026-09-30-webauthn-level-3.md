---
layout: single
title: "패스키 도입 뒤에 남는 서버 설계: WebAuthn Level 3"
description: "W3C WebAuthn Level 3를 기준으로 RP ID, 사용자 매개, attestation, credential lifecycle과 계정 복구를 서버 설계 문제로 정리한다."
date: 2026-09-30 09:00:00 +09:00
lang: ko
translation_key: webauthn-level-3-server-design
section: security
topic_key: security-engineering
categories: Security
tags: [security, webauthn, passkeys, authentication, web-security]
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

패스키 도입은 로그인 화면 하나를 바꾸는 일이 아니다. 서버는 어떤 relying party(RP)가 credential을 받아들일지, credential을 어떤 계정과 묶을지, 기기 교체와 복구를 어떤 증거로 처리할지 결정해야 한다. W3C는 2026-08-25 WebAuthn Level 3를 Recommendation으로 발표했다.

이 글은 WebAuthn을 "비밀번호 없는 로그인"이라는 홍보 문구가 아니라 scoped public-key credential의 lifecycle과 서버 검증 문제로 본다.

## Document Info / Environment

- 작성일·검증 기준일: 2026-09-07
- 문서 성격: standards analysis / security design guide
- 테스트 환경: authenticator나 browser 구현을 직접 테스트하지 않았다.
- 범위: WebAuthn standard의 보안 모델. 특정 passkey provider의 동기화·복구 UX는 제품별로 다를 수 있다.

## Problem Statement / 문제 정의

사용자는 새 기기를 사고, authenticator를 잃고, 이메일과 계정을 바꾸며, 여러 subdomain을 사용한다. 이때 "등록 성공"만 기록하면 다음 질문이 남는다.

- 이 credential은 어느 RP ID에서만 쓸 수 있는가?
- 서버는 `clientDataJSON`의 type·challenge·origin, `authenticatorData`의 기대 RP ID hash·flags, 그리고 assertion signature를 무엇과 어떻게 검증하는가?
- attestation을 저장·검증할 이유와 개인정보 비용은 무엇인가?
- credential을 쓸 수 없을 때 복구 절차가 약한 인증 우회가 되지 않는가?

## Verified Facts / 확인된 사실

- W3C는 2026-08-25 Web Authentication: An API for accessing Public Key Credentials Level 3를 W3C Recommendation으로 발표했다.
  근거: [W3C announcement](https://www.w3.org/news/2026/web-authentication-an-api-for-accessing-public-key-credentials-level-3-is-now-a-w3c-recommendation/)
- 이 사양은 web application이 strong, attested, scoped public-key credential을 만들고 사용하게 하는 API를 정의한다. credential은 특정 WebAuthn RP에 scoped되고 authenticator에 bound된다.
  근거: [W3C announcement](https://www.w3.org/news/2026/web-authentication-an-api-for-accessing-public-key-credentials-level-3-is-now-a-w3c-recommendation/)
- user agent는 privacy를 위해 authenticator와 public-key credential 접근을 매개하며, authenticator는 user consent 없이 작업하지 않도록 책임진다.
  근거: [W3C announcement](https://www.w3.org/news/2026/web-authentication-an-api-for-accessing-public-key-credentials-level-3-is-now-a-w3c-recommendation/)

## Reproduction Steps / 재현 순서

배포 전 다음 서버 측 계약을 문서화한다.

| 항목 | 확인 질문 |
| --- | --- |
| RP ID·origin | 실제 서비스 도메인과 허용 origin은 무엇인가? |
| challenge | server가 생성한 예측 불가능한 값을 한 번만 쓰고 만료시키며 ceremony에 묶는가? 사전에 계정이나 세션이 정해진 흐름에서는 그것들과도 올바르게 연결하는가? |
| credential record | 검증과 risk policy에 필요한 credential ID·public key·signature counter·transports·UV initialization state·backup eligibility/state 등을 해당되는 범위에서 저장하고, 불필요한 attestation 보존은 피하는가? |
| attestation | 신뢰 판단에 실제 필요한가, 아니면 privacy 비용만 늘리는가? |
| account recovery | 기존 강한 credential을 잃었을 때 어떤 별도 검증이 필요한가? |
| fallback | fallback이 passkey보다 약한 영구 우회로가 되지 않는가? |

등록과 인증 모두에서 server는 client의 "성공" 메시지가 아니라 검증 가능한 response를 확인해야 한다. 복구·credential 삭제·새 authenticator 등록은 감사 이벤트로 남긴다.

## Observations / 관찰 결과

WebAuthn ceremony에서 RP는 password를 비교하는 대신 공개키 assertion을 검증한다. 다만 서비스가 더 약한 recovery 또는 fallback 경로를 제공하면 전체 계정 보안은 여전히 그 경로에 의해 제한될 수 있다. attestation은 모든 서비스에 자동으로 필요한 기능이 아니다. 개인정보와 보존 영향은 RP의 conveyance preference, authenticator의 attestation 동작, RP가 실제 저장·사용하는 데이터에 따라 달라지므로 문서화된 정책 목적이 있을 때만 수집·보존해야 한다.

passkey 동기화나 platform support는 편의성을 바꾸지만, RP ID·challenge 검증·복구 승인처럼 서버가 소유하는 경계는 대신해 주지 않는다.

## Interpretation / 해석

좋은 WebAuthn 도입의 산출물은 "passkey 버튼"이 아니라 다음의 운영 계약이다.

```text
scoped credential
+ one-time verified challenge
+ 검증과 선언한 risk policy에 충분한 credential record
+ 계정 위험도에 맞게 정하고 명시적으로 문서화한 recovery assurance
+ auditable lifecycle changes
```

복구 경로가 일반 인증 경로보다 실질적으로 더 쉽게 침해될 수 있다면 공격 경로가 될 수 있으므로, 그 위험을 평가하고 모니터링해야 한다.

## Limitations / 한계

- 이 글은 W3C 표준 분석이며 브라우저·OS·password manager의 기능을 비교하지 않았다.
- WebAuthn이 phishing risk를 줄일 수 있어도 서비스의 session theft, recovery abuse, authorization flaw를 자동 제거하지 않는다.
- attestation 정책은 규제·기기 관리·개인정보 요구사항에 따라 조직별로 달라진다.

## References / 참고자료

- [WebAuthn Level 3 W3C Recommendation announcement](https://www.w3.org/news/2026/web-authentication-an-api-for-accessing-public-key-credentials-level-3-is-now-a-w3c-recommendation/)
- [WebAuthn Level 3 Recommendation](https://www.w3.org/TR/2026/REC-webauthn-3-20260825/)

## Change Log / 변경 이력

- 2026-09-07: KR local draft 작성. `published: false`; 사이트·외부 채널·실제 일정은 변경하지 않았다.
