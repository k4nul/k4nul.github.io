---
layout: single
title: "container image signing과 scan 결과 해석"
description: "컨테이너 이미지 서명과 취약점 스캔 결과를 혼동하지 않도록 digest, 서명 검증, SBOM, CVE 판정 기준을 분리해 정리한다."
date: 2026-07-23 09:00:00 +09:00
lang: ko
translation_key: container-image-signing-and-scan-results
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

컨테이너 이미지 서명은 "이 digest의 이미지를 누가, 어떤 신원으로 만들었는가"를 확인하는 절차이고, 취약점 스캔은 "그 이미지 안에 알려진 취약점이나 취약한 패키지가 있는가"를 확인하는 절차다. 서명이 있다고 안전한 이미지라는 뜻은 아니며, 스캔 결과가 깨끗하다고 provenance가 검증된 것도 아니다.

운영 기준은 간단하다. tag가 아니라 digest를 기준으로 빌드 산출물을 고정하고, 그 digest에 대해 서명과 SBOM 또는 provenance를 붙이고, 배포 전에는 서명 검증 결과와 스캔 결과를 서로 다른 증거로 기록한다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: tutorial | analysis
- 테스트 환경: 로컬 실행 테스트 없음. Sigstore Cosign, Docker Scout, Trivy 공식 문서를 기준으로 절차와 해석 기준을 정리했다.
- 테스트 버전: 공식 문서 2026-04-29 확인. 특정 CLI 버전의 출력 형식은 고정하지 않는다.
- 출처 성격: 공식 문서, 원 프로젝트 문서

## 문제 정의

이미지 보안 검토에서 자주 생기는 오류는 서명, SBOM, 취약점 스캔을 하나의 통과 표시로 합쳐 보는 것이다. 서명은 산출물의 출처와 무결성에 가깝고, 스캔은 알려진 취약점 데이터베이스와 패키지 메타데이터의 비교 결과다.

따라서 릴리스 승인 기록에는 "서명 검증 성공", "SBOM 존재", "취약점 스캔 결과", "예외 승인"을 분리해 남겨야 한다.

## 확인한 사실

- Sigstore Cosign 문서는 컨테이너 이미지 서명과 attestation을 지원하며, keyless 서명은 OIDC 인증을 사용할 수 있다고 설명한다.
- Docker Scout 문서는 이미지 분석에서 SBOM과 이미지 메타데이터를 추출하고 취약점 advisory와 비교한다고 설명한다.
- Docker Scout 문서는 severity가 advisory 출처에 따라 달라질 수 있으며, preferred advisory와 fallback CVSS가 함께 표시될 수 있다고 설명한다.
- Trivy 문서는 컨테이너 이미지, 파일시스템, Git 저장소 등을 대상으로 취약점 스캔을 수행하는 도구로 설명된다.
- 이 글의 검증 기준일은 2026-04-29이며, CLI 플래그와 출력 형식은 이후 버전에서 바뀔 수 있다.

## 기본 절차

1. 이미지를 빌드한 뒤 tag만 기록하지 말고 `registry.example.com/app@sha256:...` 형식의 digest를 기록한다.
2. digest 대상에 대해 `cosign sign` 또는 조직의 signing 파이프라인을 실행한다.
3. 배포 게이트에서 `cosign verify`로 서명자 신원, 인증서 issuer, OIDC subject, bundle 또는 transparency log 정책을 확인한다.
4. 빌드 시 SBOM과 provenance attestation을 생성하고 이미지에 연결한다.
5. `trivy image`, `docker scout cves` 같은 스캐너로 같은 digest를 스캔한다.
6. Critical/High 항목은 package, installed version, fixed version, exploitability, runtime exposure를 함께 확인한다.
7. 수정할 수 없는 항목은 "미수정"이 아니라 예외 사유, 만료일, 재검토자를 기록한다.
8. 최종 승인에는 서명 검증 결과와 스캔 판정 결과를 별도 항목으로 남긴다.

## 결과 해석 기준

| 항목 | 봐야 할 것 | 흔한 오해 |
| --- | --- | --- |
| Image digest | 배포 대상이 정확히 어떤 바이트인지 | `latest` tag가 같은 이미지를 가리킨다고 가정함 |
| Signature | 누가 어떤 신원으로 이 digest에 서명했는지 | 서명된 이미지는 취약점이 없다고 판단함 |
| SBOM | 어떤 OS/package/application dependency가 포함됐는지 | SBOM만 있으면 취약점 판단이 끝났다고 봄 |
| CVE severity | advisory 출처, CVSS, distro 판정 | 숫자만 보고 운영 위험을 확정함 |
| Fixed version | 실제 업데이트 가능한 버전이 있는지 | fixed version 없는 CVE를 즉시 빌드 실패로만 처리함 |
| Runtime exposure | 취약한 패키지가 실제 실행 경로에 있는지 | 컨테이너 안에 존재하면 모두 같은 위험으로 봄 |

## 운영 판단

서명 검증 실패는 대체로 배포 차단 사유다. 출처가 검증되지 않은 산출물을 배포하면 스캔 결과가 좋아도 공급망 통제가 깨진다.

스캔 실패는 정책에 따라 차단 또는 예외 승인으로 나뉜다. 예를 들어 외부에 노출되는 서비스 이미지의 exploitable Critical 취약점은 차단에 가깝지만, 개발 전용 이미지의 unfixed low severity 항목은 만료일이 있는 예외로 관리할 수 있다.

스캔 도구 간 결과 차이는 이상한 일이 아니다. advisory 출처, OS 배포판 판정, language package lockfile 해석, SBOM 생성 방식이 다르면 결과가 달라진다. 중요한 것은 "어떤 도구에서 왜 이 판정을 내렸는지"를 릴리스 기록에 남기는 것이다.

## 한계와 예외

- 취약점 스캐너는 알려진 취약점과 탐지 가능한 패키지 메타데이터에 의존한다.
- 서명은 서명자와 산출물 연결을 검증할 뿐, 소스 코드나 빌드 스크립트가 안전하다는 증명은 아니다.
- private registry, air-gapped 환경, 자체 CA, 자체 KMS를 쓰는 조직은 검증 정책을 별도로 문서화해야 한다.

## 참고자료

- [Sigstore Cosign: Signing Containers](https://docs.sigstore.dev/cosign/signing/signing_with_containers/)
- [Sigstore overview](https://docs.sigstore.dev/)
- [Docker Scout image analysis](https://docs.docker.com/scout/explore/analysis/)
- [Docker Scout CVEs CLI reference](https://docs.docker.com/reference/cli/docker/scout/cves/)
- [Trivy vulnerability scanning](https://trivy.dev/latest/docs/scanner/vulnerability/)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: 서명과 스캔의 역할, digest 기준 검증, CVE 해석 기준을 보강.
