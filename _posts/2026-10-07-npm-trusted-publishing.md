---
layout: single
title: "npm OIDC trusted publishing과 provenance: release evidence가 여전히 증명하지 못하는 것"
description: "npm의 복수 OIDC trusted-publishing 설정과 staged publishing을 CI 신뢰 경계·승인·provenance 검증 정책의 관점에서 해석한다."
date: 2026-10-07 09:00:00 +09:00
lang: ko
translation_key: npm-trusted-publishing-provenance-boundaries
section: security
topic_key: supply-chain-security
categories: Security
tags: [security, npm, oidc, supply-chain, provenance, ci-cd]
published: false
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## Summary / 요약

OIDC trusted publishing은 장기 npm publish token을 짧은 CI identity로 바꾼다. npm registry는 CI provider별 identity criteria에 따라 publish 또는 stage를 허용한다. 예를 들어 GitHub Actions에서는 repository, workflow filename, optional environment 같은 기준을 사용한다. 2026-09-03 npm은 패키지당 복수 trusted-publishing configuration과 staged publishing 개선을 GA로 발표했다.

그러나 provenance가 존재하거나 OIDC token이 유효하다는 사실만으로 artifact가 안전하다는 뜻은 아니다. **정상 신원을 가진 workflow가 침해되면, 그 workflow는 정상처럼 보이는 artifact를 만들 수 있다.** 이 글은 서명을 신뢰의 끝이 아닌 policy enforcement의 입력으로 다룬다.

## Document Info / Environment

- 작성일·검증 기준일: 2026-09-07
- 문서 성격: release analysis / CI security design guide
- 테스트 환경: npm package를 publish하거나 CI credential을 사용하지 않았다.
- 범위: 공식 changelog와 SLSA의 공개 사후 분석. 특정 조직의 침해 사례를 주장하지 않는다.

## Problem Statement / 문제 정의

release workflow가 여러 개면 "OIDC를 쓰자"만으로는 충분하지 않다. stable, prerelease, staging workflow가 같은 package에 접근할 때 다음이 중요하다.

- 어떤 workflow가 어느 environment에서 publish 또는 stage할 수 있는가?
- direct publish는 정말 필요한가?
- review는 scan 결과와 provenance의 어떤 field를 확인하는가?
- cache poisoning, 과도한 `id-token` 권한, workflow 변경은 어떻게 통제하는가?

## Verified Facts / 확인된 사실

- npm은 2026-09-03 하나의 package에 둘 이상의 trusted-publishing configuration을 둘 수 있다고 발표했다. configuration은 CI provider별 identity criteria를 사용하며, GitHub Actions에서는 owner, repository, workflow filename, optional environment가 해당한다.
  근거: [GitHub Changelog](https://github.blog/changelog/2026-09-03-multiple-trusted-publishing-configurations-for-npm/)
- `npm publish` 또는 `npm stage publish`는 incoming OIDC token이 해당 action을 허용하는 configuration 중 하나와 일치할 때만 허용된다. configuration은 additive하며 평가 순서는 보장되지 않는다.
  근거: [GitHub Changelog](https://github.blog/changelog/2026-09-03-multiple-trusted-publishing-configurations-for-npm/)
- direct publish는 configuration별 opt-in이며, GitHub/npm은 staging-only 구성을 권장한다. staged package는 malware scan이 끝날 때까지 승인할 수 없다.
  근거: [GitHub Changelog](https://github.blog/changelog/2026-09-03-multiple-trusted-publishing-configurations-for-npm/)
- SLSA의 Mini Shai-Hulud 공개 분석은 침해된 build가 정상 신원으로 artifact와 유효한 provenance를 만들 수 있는 경계를 설명한다.
  근거: [SLSA analysis](https://slsa.dev/blog/2026/05/mini-shai-hulud-what-slsa-can-and-cannot-do)

## Reproduction Steps / 재현 순서

release path마다 별도 configuration과 검토 표를 만든다.

| 경로 | OIDC policy | 권장 delivery | 승인에서 확인할 것 |
| --- | --- | --- | --- |
| stable | protected workflow + production environment | stage | version, diff, scan, provenance identity |
| prerelease | distinct workflow/environment | stage 또는 registry 분리 | tag·channel·의존성 변화 |
| emergency | 별도 짧은 승인 경로 | 문서화된 전제가 맞을 때 stage | 사유·승인자·후속 audit |

운영 제약(공개 직전 재검증): staged publishing은 현재 이미 npm registry에 존재하는 package에서만 사용할 수 있으며 npm CLI 11.15.0+와 Node.js 22.14.0+가 필요하다. maintainer는 2FA로 staged package를 승인하므로, stage를 기본 경로로 정하기 전에 이 전제와 release ownership을 확인해야 한다.

그리고 CI에는 다음 guardrail을 둔다.

1. `id-token` 권한은 publish가 필요한 job에만 부여한다.
2. publish workflow와 environment 보호 규칙을 code review 대상으로 둔다.
3. cache key와 restore source를 신뢰 경계로 취급한다.
4. provenance format과 허용 producer에 맞는 attestation-verification policy를 정한다. artifact digest와 제공되는 source·builder·workflow·ref·identity field를 그 policy와 대조하고, 단지 서명이 있다는 사실만으로 승인하지 않는다. 선택한 producer가 문서화하지 않은 `trigger` field는 요구하거나 신뢰하지 않는다.
5. direct publish 예외는 기간과 책임자를 남긴다.

## Observations / 관찰 결과

복수 configuration은 release path를 분리할 수 있지만, 하나라도 지나치게 넓으면 전체 policy의 약한 고리가 된다. 그리고 staged publishing에서는 maintainer가 2FA로 staged package를 검토·명시 승인해야 공개된다. 이는 중요한 gate이지만, 승인자가 staged artifact와 관련 release evidence를 검토하지 않으면 단순한 버튼 누르기로 약화될 수 있다.

provenance는 package artifact와 build platform이 기록한 source·build 정보를 검증 가능하게 연결하는 evidence이며, 정확한 field와 trust guarantee는 provenance format과 producer에 따라 달라진다. 모든 trusted-published package에 provenance가 있다고 가정해서는 안 된다. npm은 조건을 충족하는 GitHub Actions·GitLab CI/CD release에는 자동 provenance를 문서화하지만 CircleCI trusted publishing은 현재 provenance attestation을 생성하지 않는다. 그것만으로 source review, dependency review, secure runner, cache isolation을 대체하지 않는다.

## Interpretation / 해석

신뢰할 만한 release 판단은 하나의 boolean이 아니라 다섯 개의 질문이다.

```text
right artifact?
from the intended repository and workflow?
at the intended ref and trigger?
with a reviewed dependency/build context?
approved after scan and policy checks?
```

OIDC는 장기 secret을 줄이고 identity를 좁히는 좋은 출발점이다. 그러나 **정상 identity가 침해되지 않았다는 보장**은 별도 controls의 몫이다.

## Limitations / 한계

- 이 글은 공개 문서 분석이며 npm registry 설정을 실제 변경하지 않았다.
- malware scanning과 staged approval은 모든 악성 동작이나 source compromise를 탐지·차단한다고 보장하지 않는다.
- SLSA provenance의 정확한 policy는 build system, registry, 조직의 risk tolerance에 따라 달라진다.

## References / 참고자료

- [Multiple trusted publishing configurations for npm](https://github.blog/changelog/2026-09-03-multiple-trusted-publishing-configurations-for-npm/)
- [npm trusted publishers](https://docs.npmjs.com/trusted-publishers)
- [npm staged publishing](https://docs.npmjs.com/staged-publishing/)
- [npm provenance statements](https://docs.npmjs.com/generating-provenance-statements)
- [Mini Shai-Hulud: What SLSA can and cannot do](https://slsa.dev/blog/2026/05/mini-shai-hulud-what-slsa-can-and-cannot-do)

## Change Log / 변경 이력

- 2026-09-07: KR local draft 작성. `published: false`; 실제 publish·CI·registry 설정은 변경하지 않았다.
