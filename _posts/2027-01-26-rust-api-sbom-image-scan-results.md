---
layout: single
title: "Rust Service 19. SBOM과 image scan 결과 읽기"
description: "Rust API 컨테이너의 SBOM, 취약점 scan 결과, false positive, 조치 우선순위를 읽는 기준을 정리한다."
date: 2027-01-26 09:00:00 +09:00
lang: ko
translation_key: rust-api-sbom-image-scan-results
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

scan 결과는 단순한 pass/fail 버튼이 아니라 운영 판단을 돕는 입력이다.

SBOM은 image 안에 무엇이 들어 있는지 보여 주고, vulnerability scan은 그 구성 요소가 알려진 취약점과 연결되는지 보여 준다. 조치 여부는 package 이름, version, CVE, fix 가능 여부, runtime 영향, base image 교체 가능성을 함께 보고 결정한다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: release tag와 Docker image tag 연결하기
- 다음 글: Kubernetes Deployment와 Service로 배포하기
- 보강 기준: 실제 발행 전 예제 저장소에서 SBOM 생성, CVE scan, 결과 파일 저장, 조치/보류 판단 예시를 추가한다.

## 문서 정보

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial / supply chain security 결과 해석
- 테스트 환경: 직접 SBOM 생성 또는 image scan 실행 없음. 이 글은 결과를 읽고 운영 판단으로 연결하는 기준을 정리한다.
- 확인한 문서: CISA SBOM 자료, Docker Scout 문서, Docker Scout CLI 문서, Docker SBOM attestation 문서, SLSA v1.2
- 출처 성격: 정부/공식 문서, Docker 공식 문서, supply chain security specification

## 문제 정의

release tag와 digest를 기록한 다음에는 "그 image를 배포해도 되는가"를 판단해야 한다. 이때 scan 결과만 보고 기계적으로 막거나 통과시키면 운영 현실을 놓치기 쉽다.

검토해야 할 질문은 다음과 같다.

- scan한 대상이 tag인가, digest인가?
- SBOM이 어느 image digest에서 만들어졌는가?
- 취약점이 OS package에서 왔는가, Rust crate에서 왔는가?
- fixed version이 있는가?
- vulnerable package가 runtime image에 실제로 포함되어 있는가?
- exploit 가능성과 서비스 노출 조건은 어떤가?
- base image 교체로 해결되는가, application dependency update가 필요한가?
- 조치하지 않는다면 누가, 언제까지, 어떤 근거로 accept하는가?

이번 글의 목표는 도구 하나를 고르는 것이 아니라 scan 결과를 release 판단으로 바꾸는 기준을 만드는 것이다.

## 확인한 사실

- CISA는 SBOM을 software transparency와 supply chain security를 위한 자료로 다루며, 2025년 SBOM minimum elements draft guidance를 공개 의견 수렴 대상으로 게시했다.
- Docker Scout 문서는 image를 분석해 구성 요소 inventory, 즉 SBOM을 만들고, 이를 vulnerability database와 대조해 보안 약점을 찾는다고 설명한다.
- `docker scout sbom`은 SBOM을 `json`, `spdx`, `cyclonedx`, `list` 형식으로 출력할 수 있다.
- `docker scout cves`는 vulnerability report를 package grouping, SARIF, SPDX, GitLab, markdown, SBOM 형식 등으로 출력할 수 있고, vulnerability 발견 시 특정 exit code를 반환하는 옵션을 제공한다.
- Docker BuildKit은 SBOM attestation 생성을 지원하며, Docker 문서는 BuildKit이 기본적으로 Syft 기반 scanner plugin을 사용한다고 설명한다.
- SLSA v1.2는 software supply chain security를 위한 점진적 가이드라인이며, source부터 build, packaging, distribution까지의 신뢰 문제를 다룬다.
- SLSA는 code quality나 producer trust 전체를 대신하지 않으며, dependency 전체에 하나의 SLSA level을 자동으로 부여하는 것도 아니라고 설명한다.

## SBOM과 Scan 결과 분리

SBOM과 vulnerability scan을 같은 것으로 보면 안 된다.

| 산출물 | 답하는 질문 | 예시 사용 |
| --- | --- | --- |
| SBOM | 이 artifact 안에 무엇이 들어 있는가? | package inventory, license 검토, 새 CVE 발표 시 영향 범위 검색 |
| Vulnerability scan | 알려진 취약점 database와 매칭되는 항목이 있는가? | release gate, 조치 우선순위, 보안 ticket 생성 |
| Provenance / attestation | 이 artifact가 기대한 source와 build system에서 만들어졌는가? | build tampering 방지, 감사 증적 |
| VEX | 취약점이 이 artifact에 실제로 영향이 있는가? | false positive 또는 not affected 근거 기록 |

SBOM은 ingredient list에 가깝고, scan은 알려진 취약점과의 매칭이다. 둘 다 release 판단에 필요하지만 역할이 다르다.

## 재현 명령

실제 예제 저장소에서는 image tag보다 digest를 기준으로 기록한다.

1. image digest를 확인한다.

```powershell
docker pull ghcr.io/org/rust-api:v0.3.0
docker image inspect ghcr.io/org/rust-api:v0.3.0
```

2. SBOM을 파일로 저장한다.

```powershell
docker scout sbom `
  --format spdx `
  --output rust-api-v0.3.0.spdx.json `
  ghcr.io/org/rust-api:v0.3.0
```

3. CVE scan 결과를 사람이 읽는 형식과 CI가 읽을 형식으로 나눈다.

```powershell
docker scout cves `
  --format markdown `
  --output rust-api-v0.3.0-cves.md `
  ghcr.io/org/rust-api:v0.3.0

docker scout cves `
  --format sarif `
  --output rust-api-v0.3.0-cves.sarif.json `
  ghcr.io/org/rust-api:v0.3.0
```

4. release 판단 표를 작성한다.

```text
image: ghcr.io/org/rust-api@sha256:...
sbom: rust-api-v0.3.0.spdx.json
scan: rust-api-v0.3.0-cves.md
critical: 0
high: 0
medium: 2
accepted: 1
action required: 1
decision owner: security/platform
decision date: 2026-05-05
```

위 숫자는 예시다. 실제 글에는 실행 결과의 숫자와 판단 근거를 그대로 기록해야 한다.

## 결과 판독 표

scan 결과를 ticket으로 옮길 때는 severity만 복사하지 않는다.

| 항목 | 확인 질문 | 기록 예시 |
| --- | --- | --- |
| Package | 어떤 package가 걸렸는가? | `openssl`, `glibc`, Rust crate 이름 |
| Version | 현재 version과 fixed version은 무엇인가? | `1.2.3 -> 1.2.4` |
| Source | OS package인가, language dependency인가? | base image update 또는 Cargo update |
| CVE | 어떤 취약점 ID인가? | `CVE-...` |
| Fix available | fixed package가 있는가? | yes/no |
| Runtime exposure | runtime image에 포함되고 실행 경로와 연결되는가? | yes/no/unknown |
| Action | update, base image 교체, 보류, false positive | owner와 due date |

중요한 것은 "high니까 무조건 실패"보다 "high인데 fixed version이 있고 runtime image에 포함되어 있으므로 오늘 고친다" 같은 판단 문장이다.

## Release Gate 예시

처음 release gate는 지나치게 복잡할 필요가 없다.

| 조건 | 기본 판단 |
| --- | --- |
| Critical vulnerability with fix | release 차단 |
| High vulnerability with fix and runtime exposure | release 차단 또는 긴급 승인 필요 |
| High vulnerability without fix | risk acceptance와 follow-up ticket 필요 |
| Medium/Low | SLA에 따라 ticket화 |
| Base image에서 온 취약점 | base image update 가능 여부 확인 |
| Rust crate 취약점 | `cargo update`, dependency 교체, feature 비활성화 검토 |

조직 정책이 더 엄격하면 이 표를 강화한다. 중요한 것은 release마다 기준이 바뀌지 않게 문서화하는 것이다.

## 관찰 상태

이 글에는 아직 실제 scan 결과가 없다. 발행 전에는 다음 값을 추가해야 한다.

- Docker Scout 또는 사용한 scanner version
- scan한 image digest
- SBOM 파일명과 format
- CVE summary 숫자
- 조치한 항목과 보류한 항목
- false positive 또는 not affected 판단이 있다면 근거
- release gate 통과/차단 결정과 결정자

## 검증 체크리스트

- tag가 아니라 digest 기준으로 SBOM과 scan 결과를 연결했는가?
- SBOM과 vulnerability scan의 역할을 분리했는가?
- scanner version과 scan 날짜를 기록했는가?
- OS package와 Rust crate 취약점의 조치 경로를 분리했는가?
- fixed version이 있는지 확인했는가?
- severity 외에 runtime exposure와 exploit 가능성을 검토했는가?
- 보류 또는 risk acceptance에 owner와 due date가 있는가?
- release note나 보안 ticket에 결과 파일이 연결되어 있는가?

## 해석 / 의견

취약점 scan 결과는 운영자를 대신해 판단하지 않는다. 도구는 "무엇이 알려진 취약점 database와 맞는지"를 알려 주고, 팀은 그 결과가 이 image와 이 서비스에 어떤 의미인지 판단해야 한다.

SBOM은 그 판단의 출발점이다. 나중에 새로운 CVE가 발표되었을 때 image를 다시 열어 보지 않고도 "우리가 이 package를 포함했는가"를 추적할 수 있어야 한다. 그래서 SBOM, scan 결과, image digest는 release 기록에 함께 남기는 편이 좋다.

## 한계와 예외

- 이 글은 Docker Scout를 예시 도구로 사용하지만 특정 scanner 도입을 강제하지 않는다.
- scanner마다 vulnerability database, package 탐지 방식, reachability 분석 수준이 다를 수 있다.
- Rust binary에 정적으로 포함된 의존성과 OS package 탐지는 도구별 차이가 있을 수 있다.
- regulatory compliance, license policy, VEX 운영은 별도 정책 문서가 필요할 수 있다.

## 참고자료

- [CISA: Software Bill of Materials](https://www.cisa.gov/sbom)
- [CISA: 2025 Minimum Elements for a Software Bill of Materials](https://www.cisa.gov/resources-tools/resources/2025-minimum-elements-software-bill-materials-sbom)
- [Docker Scout documentation](https://docs.docker.com/scout/)
- [Docker Scout SBOM command](https://docs.docker.com/reference/cli/docker/scout/sbom/)
- [Docker Scout CVEs command](https://docs.docker.com/reference/cli/docker/scout/cves/)
- [Docker: SBOM attestations](https://docs.docker.com/build/metadata/attestations/sbom/)
- [SLSA v1.2: About SLSA](https://slsa.dev/spec/v1.2/about)

## 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: SBOM, vulnerability scan, attestation, image digest, release gate, risk acceptance 기준을 CISA/Docker/SLSA 문서 기반으로 보강.
