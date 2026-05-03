---
layout: single
title: "SBOM, SLSA, provenance 입문"
description: "SBOM, SLSA, provenance 입문에 대해 공식 문서와 운영 관점으로 확인할 기준, 점검 순서, 한계를 정리한 글."
date: 2026-07-09 09:00:00 +09:00
lang: ko
translation_key: sbom-slsa-provenance-basics
section: security
topic_key: security-engineering
categories: Security
tags: [security, devsecops, supply-chain-security, cloud-security]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

SBOM, SLSA, provenance는 같은 말이 아니다. SBOM은 소프트웨어 구성품 목록이고, provenance는 artifact가 어떤 source와 build 과정에서 만들어졌는지 설명하는 증명이며, SLSA는 공급망 위협을 줄이기 위한 수준과 요구사항을 정의한다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: tutorial | comparison
- 테스트 환경: 실행 테스트 없음. NTIA/CISA SBOM 자료와 SLSA 공식 사양 기준으로 개념 정리.
- 테스트 버전: SLSA v1.2 문서와 NTIA/CISA SBOM 자료 2026-04-29 확인본.
- 출처 등급: 공식 문서, 표준/사양 문서

## 문제 정의

공급망 보안 글에서 SBOM, SLSA, provenance를 섞어 쓰면 점검 기준이 흐려진다. SBOM이 있다고 빌드가 안전하다는 뜻은 아니고, provenance가 있다고 취약한 dependency가 없다는 뜻도 아니다. 각 문서는 다른 질문에 답한다.

이 글은 세 용어가 운영에서 어떤 질문에 답하는지 분리한다.

## 확인된 사실

- NTIA는 SBOM을 소프트웨어를 구성하는 component와 supply chain relationship의 formal record로 설명한다.
  근거: [NTIA Minimum Elements for SBOM](https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom)
- CISA는 SBOM 채택과 운영화를 지원하며 2025 SBOM Minimum Elements 자료를 제공한다.
  근거: [CISA SBOM](https://www.cisa.gov/sbom)
- SLSA v1.2 사양은 여러 SLSA level과 track, provenance를 포함한 attestation format을 정의한다.
  근거: [SLSA specification](https://slsa.dev/spec/)
- SLSA build track은 artifact가 변조되지 않았고 source까지 추적될 수 있다는 신뢰를 높이는 방향으로 level을 정의한다.
  근거: [SLSA Build Track](https://slsa.dev/spec/v1.2/)
- SLSA provenance는 build artifact와 builder, source, build parameters 같은 정보를 연결하는 attestation의 한 종류다.
  근거: [SLSA Provenance](https://slsa.dev/spec/v1.2/provenance)

## 직접 재현한 결과

- 직접 재현 없음: 이 글은 실제 SBOM 파일을 생성하거나 SLSA provenance를 검증한 실험 보고서가 아니다.
- 직접 확인한 범위: 2026-04-29 기준 NTIA/CISA와 SLSA 공식 문서의 정의와 구조.

## 재현 순서

세 용어는 아래 질문으로 구분하면 쉽다.

| 항목 | 답하는 질문 | 대표 내용 | 주의할 점 |
| --- | --- | --- | --- |
| SBOM | 이 artifact 안에 무엇이 들어 있는가 | component name, version, supplier, dependency relationship, identifier | 취약점 판단 자체가 아니라 분석 입력이다 |
| Provenance | 이 artifact는 어디서 어떻게 만들어졌는가 | source, builder, build type, parameters, materials, subject | build 증명이지 component 취약점 목록은 아니다 |
| SLSA | 이 공급망 통제 수준은 어느 정도인가 | build/source track, level, 요구사항, verification | badge가 아니라 요구사항 충족 여부로 봐야 한다 |

초기 도입 순서는 다음처럼 잡을 수 있다.

1. artifact를 정한다: container image, binary, library package, release archive.
2. SBOM을 생성한다: SPDX 또는 CycloneDX 등 조직에서 소비 가능한 형식을 고른다.
3. SBOM 품질을 확인한다: component 이름, version, supplier, dependency, license, package URL 같은 식별자가 충분한지 본다.
4. build provenance를 생성한다: source commit, builder identity, build workflow, build parameters, output artifact digest를 연결한다.
5. artifact와 provenance를 검증한다: digest가 맞는지, builder가 trusted인지, source repository와 ref가 기대한 값인지 확인한다.
6. SLSA level을 목표로 정한다: 현재 수준을 과장하지 말고 어떤 requirement가 부족한지 기록한다.

예를 들어 container image release 기록에는 최소한 아래 값이 같이 있어야 후속 분석이 가능하다.

```text
artifact: ghcr.io/example/app@sha256:...
sbom: app.spdx.json
provenance: app.intoto.jsonl
source: https://github.com/example/app@<commit>
builder: github-actions workflow <workflow file>@<commit>
verification:
  - image digest matched
  - provenance signature verified
  - SBOM generated for release artifact
```

## 관찰 결과

- SBOM은 dependency와 component 투명성을 높이지만, build 과정이 안전했다는 증거는 아니다.
- provenance는 artifact와 build 과정을 연결하지만, 모든 dependency 취약점을 자동으로 판단하지 않는다.
- SLSA는 checklist라기보다 supply chain control의 maturity model에 가깝다.

## 해석 / 의견

내 판단으로는 초반에는 "SBOM 생성"보다 "artifact digest, SBOM, provenance, source commit을 같은 release 단위로 묶는 것"이 더 중요하다. 파일이 있어도 어떤 release와 연결되는지 모르면 사고 대응에서 쓰기 어렵다.

의견: SLSA level은 마케팅 문구로 쓰기보다 내부 gap 분석 표로 먼저 쓰는 편이 안전하다.

## 한계와 예외

- SBOM 형식, field 요구사항, SLSA version은 도입 시점에 다시 확인해야 한다.
- SBOM과 provenance를 생성해도 vulnerability triage, VEX, license 검토, image signing, policy enforcement는 별도 작업이다.
- 이 글은 입문용 개념 정리이며 특정 tool의 출력 품질을 검증하지 않았다.

## 참고자료

- [NTIA Minimum Elements for SBOM](https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom)
- [CISA SBOM](https://www.cisa.gov/sbom)
- [CISA 2025 Minimum Elements for SBOM](https://www.cisa.gov/resources-tools/resources/2025-minimum-elements-software-bill-materials-sbom)
- [SLSA specification](https://slsa.dev/spec/)
- [SLSA Provenance](https://slsa.dev/spec/v1.2/provenance)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: SBOM, SLSA, provenance 차이와 release 단위 점검 기준 보강.
