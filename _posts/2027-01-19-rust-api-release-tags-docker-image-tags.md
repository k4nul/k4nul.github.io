---
layout: single
title: "Rust Service 18. release tag와 Docker image tag 연결하기"
description: "Git tag, release, Docker image tag, digest를 연결해 배포 이력을 추적 가능한 형태로 만든다."
date: 2027-01-19 09:00:00 +09:00
lang: ko
translation_key: rust-api-release-tags-docker-image-tags
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

`latest`만으로는 어떤 코드가 배포되었는지 복원하기 어렵다. release tag, Docker image tag, image digest를 함께 기록해야 한다.

Git tag는 source revision을 가리키고, Docker image tag는 registry에서 image를 찾기 쉬운 이름을 제공한다. 운영에서 재현 가능한 기준은 tag만이 아니라 digest까지 포함한 기록이다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: GitHub Actions로 fmt, clippy, test, build 자동화하기
- 다음 글: SBOM과 image scan 결과 읽기
- 보강 기준: 실제 발행 전 예제 저장소에서 tag 생성, image build, registry push, digest 확인, release note 기록을 재현한다.

## 문서 정보

- 작성일: 2026-05-04
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial / release 추적성 설계
- 테스트 환경: 직접 Git tag push, registry push, release 생성 실행 없음. 이 글은 tag와 digest 기록 기준을 정리한다.
- 테스트 버전: Git, Docker CLI/Engine, registry, GitHub Actions 실행 버전 미기록. 발행 전 실제 실행 환경을 기록해야 한다.
- 출처 성격: Docker 공식 문서, GitHub 공식 문서, Git 문서

## 문제 정의

CI가 build를 통과해도 운영자가 나중에 "지금 배포된 image가 어느 commit인가?"를 답하지 못하면 release 체계가 약하다.

release 기록은 다음 질문에 답해야 한다.

- 이 release가 어느 Git commit에서 만들어졌는가?
- registry에 어떤 image tag로 push되었는가?
- 그 tag가 가리킨 image digest는 무엇인가?
- Kubernetes나 배포 도구에는 tag로 배포했는가, digest로 배포했는가?
- rollback할 때 다시 같은 image를 가져올 수 있는가?
- release note에서 migration, config 변경, 알려진 한계를 확인할 수 있는가?

이번 글은 image scan이나 SBOM을 다루기 전, release 이름과 image 식별자를 연결하는 단계다.

## 확인한 사실

- GitHub Releases 문서는 release가 Git tag를 기반으로 하며, tag는 repository history의 특정 지점을 표시한다고 설명한다.
- GitHub Releases 문서는 release를 release notes와 binary file link를 포함해 package할 수 있는 deployable software iteration으로 설명한다.
- Docker image pull 문서는 image를 name과 tag로 pull할 수 있지만, digest는 immutable identifier로 특정 image를 pull하는 데 사용할 수 있다고 설명한다.
- Docker 문서는 tag를 편리한 이름으로 설명하며, 같은 tag를 다시 pull하면 그 tag가 현재 가리키는 최신 image를 가져올 수 있다고 설명한다.
- Docker GitHub Actions 문서는 Docker metadata action을 사용해 GitHub Actions에서 image tag와 label을 관리하는 흐름을 제공한다.

## 식별자 역할 분리

release 추적성은 이름을 많이 붙이는 일이 아니라, 각 식별자의 역할을 분리하는 일이다.

| 식별자 | 예시 | 역할 | 주의점 |
| --- | --- | --- | --- |
| Git commit SHA | `6f3a1c8...` | source의 정확한 위치 | 사람이 읽기 어렵다 |
| Git tag | `v0.3.0` | release 후보 또는 release 지점 | tag 이동을 금지해야 추적성이 유지된다 |
| GitHub Release | `v0.3.0` release page | release note, asset, 변경 이력 | tag와 release 날짜가 다를 수 있다 |
| Docker image tag | `ghcr.io/org/rust-api:v0.3.0` | registry에서 image를 찾는 이름 | tag는 움직일 수 있다 |
| Docker image digest | `sha256:...` | image content 식별 | 길지만 재현과 감사에 중요하다 |
| Deployment revision | Kubernetes ReplicaSet revision 등 | 실제 배포 이력 | cluster 상태와 연결해 기록해야 한다 |

운영 기록에는 최소한 Git tag, commit SHA, image tag, image digest를 함께 남긴다.

## Tag 정책 예시

처음에는 단순한 규칙이면 충분하다.

| 상황 | Git tag | Image tag | 용도 |
| --- | --- | --- | --- |
| 정식 release | `v0.3.0` | `ghcr.io/org/rust-api:v0.3.0` | 사람이 읽는 release 식별자 |
| commit 추적 | 없음 | `ghcr.io/org/rust-api:sha-6f3a1c8` | commit 기반 추적 |
| 기본 branch preview | 없음 | `ghcr.io/org/rust-api:main` | 최신 main 확인용, 운영 고정값으로는 부적합 |
| moving alias | 없음 | `ghcr.io/org/rust-api:latest` | 편의 alias, 감사 기준으로 사용하지 않음 |

`latest`를 금지할 필요는 없지만, release note와 deployment manifest의 유일한 식별자로 쓰면 안 된다. 사람에게는 tag가 편하고, 재현에는 digest가 강하다.

## 수동 재현 순서

자동화하기 전에는 수동 절차로 기록 항목을 확인한다.

1. release commit을 확인한다.

```powershell
git status --short
git rev-parse HEAD
```

2. annotated tag를 만든다.

```powershell
git tag -a v0.3.0 -m "v0.3.0"
git push origin v0.3.0
```

3. 같은 commit에서 image를 build한다.

```powershell
docker build `
  -t ghcr.io/org/rust-api:v0.3.0 `
  -t ghcr.io/org/rust-api:sha-6f3a1c8 `
  .
```

4. registry에 push한다.

```powershell
docker push ghcr.io/org/rust-api:v0.3.0
docker push ghcr.io/org/rust-api:sha-6f3a1c8
```

5. digest를 확인하고 release note에 남긴다.

```powershell
docker pull ghcr.io/org/rust-api:v0.3.0
docker image inspect ghcr.io/org/rust-api:v0.3.0
```

`docker image inspect` 출력에서는 `RepoDigests` 항목을 확인한다. 발행 전 예제에서는 실제 digest 값을 본문에 기록한다.

## GitHub Actions 연결 기준

tag push에서 image를 만들고 push하는 workflow는 다음 글 이후에 더 단단히 다룬다. 여기서는 연결 기준만 고정한다.

```yaml
on:
  push:
    tags:
      - "v*.*.*"
```

자동화할 때는 다음 조건을 둔다.

- tag push workflow는 `v*.*.*` 같은 release tag에서만 image를 push한다.
- image tag에는 release tag와 commit 기반 tag를 함께 붙인다.
- push 후 digest를 workflow output이나 release note에 기록한다.
- registry write 권한은 release job에만 부여한다.
- release note에는 config 변경, migration 여부, rollback 기준을 포함한다.

Docker metadata action을 사용하면 tag와 label 생성을 줄일 수 있다. 다만 자동 생성 규칙도 release 정책의 일부이므로, 어떤 Git ref가 어떤 image tag를 만드는지 문서화해야 한다.

## Release Note 기록 형식

release note에는 사람이 읽는 변경 사항과 운영자가 필요한 식별자를 같이 둔다.

```text
Release: v0.3.0
Commit: 6f3a1c8...
Image tag: ghcr.io/org/rust-api:v0.3.0
Image digest: ghcr.io/org/rust-api@sha256:...
Built by: GitHub Actions run URL
Database migration: yes/no
Config change: yes/no
Rollback target: ghcr.io/org/rust-api@sha256:...
Known limitations:
- ...
```

이 형식은 길어 보이지만 장애 대응 때 시간을 줄인다. tag만 보고 배포했다가 tag가 움직였는지, 같은 tag가 어느 digest였는지 뒤늦게 찾는 상황을 피할 수 있다.

## 관찰 상태

이 글에는 아직 실제 tag push나 registry push 결과가 없다. 발행 전에는 다음 값을 추가해야 한다.

- `git rev-parse HEAD` 출력
- 생성한 Git tag와 GitHub Release URL
- Docker image tag 목록
- registry push 결과
- 확인한 image digest
- release note에 기록한 digest와 deployment manifest의 digest가 일치한다는 확인

## 검증 체크리스트

- release tag가 어떤 commit을 가리키는지 기록했는가?
- image tag가 release tag와 commit 기반 tag를 모두 제공하는가?
- `latest`를 감사나 rollback의 유일한 기준으로 쓰지 않는가?
- registry push 후 digest를 확인했는가?
- release note에 commit SHA, image tag, image digest, build run URL이 포함되어 있는가?
- 배포 manifest 또는 배포 기록이 digest까지 추적 가능한가?
- tag 이동을 막는 운영 규칙이 있는가?

## 해석 / 의견

release tag와 image tag를 연결하는 목적은 예쁜 버전 이름을 붙이는 것이 아니다. 장애가 났을 때 "무엇이 배포되었고, 무엇으로 되돌릴 수 있는가"를 빠르게 답하기 위해서다.

tag는 사람에게 좋고 digest는 시스템과 감사에 좋다. 둘 중 하나만 고르면 빈틈이 생긴다. 운영 기록에는 사람이 읽는 release tag와 기계가 재현할 수 있는 digest를 함께 둔다.

## 한계와 예외

- 이 글은 실제 registry push나 GitHub Release 생성을 실행하지 않았다.
- SemVer 적용 여부는 서비스의 호환성 정책에 따라 달라질 수 있다.
- multi-architecture image는 manifest list digest와 platform-specific digest를 구분해야 한다.
- signed image, provenance, SBOM, vulnerability scan은 다음 글에서 다룬다.

## 참고자료

- [GitHub Docs: About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [Docker Docs: Pull an image by digest](https://docs.docker.com/reference/cli/docker/image/pull/)
- [Docker Docs: Manage tags and labels with GitHub Actions](https://docs.docker.com/build/ci/github-actions/manage-tags-labels/)
- [Git documentation: git tag](https://git-scm.com/docs/git-tag)

## 변경 이력

- 2026-05-04: Rust Service to Production 커리큘럼 초안 작성.
- 2026-05-05: Git tag, GitHub Release, Docker image tag, image digest, release note 기록 기준을 공식 문서 기반으로 보강.
