---
layout: single
title: "GitHub Actions 보안 체크리스트"
description: "GitHub Actions 보안 체크리스트에 대해 공식 문서와 운영 관점으로 확인할 기준, 점검 순서, 한계를 정리한 글."
date: 2026-07-02 09:00:00 +09:00
lang: ko
translation_key: github-actions-security-checklist
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

GitHub Actions 보안 점검은 workflow YAML 문법 확인에서 끝나지 않는다. trigger, `GITHUB_TOKEN` 권한, secrets, third-party actions, runner, 배포 인증, untrusted input을 각각 따로 확인해야 한다.

## 예시: 최소 권한 CI workflow

이 예시는 실습용 CI workflow다. 목적은 pull request에서 테스트만 실행하고, `GITHUB_TOKEN`에는 repository contents 읽기 권한만 주는 것이다. `<full-length-sha>`는 실제 action commit SHA로 바꿔야 한다.

{% raw %}
```yaml
name: ci

on:
  pull_request:
    branches: [main]

permissions: {}

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@<full-length-sha>
      - name: Run tests
        run: npm test
```
{% endraw %}

정상 결과 예시:

```text
Run npm test
...
✓ all tests passed
```

위 출력은 예시 출력이다. 실제 출력은 프로젝트의 test runner에 따라 달라진다.

## 잘못된 예와 수정된 예

잘못된 예:

{% raw %}
```yaml
permissions: write-all

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "${{ github.event.pull_request.title }}" | bash
```
{% endraw %}

문제:

- `write-all`은 테스트 job에 필요하지 않은 write 권한까지 준다.
- `actions/checkout@v4`처럼 tag만 고정하면 해당 tag의 이동 여부와 공급망 리스크를 따로 봐야 한다.
- PR 제목처럼 외부 사용자가 바꿀 수 있는 값을 shell 코드로 흘려보내면 script injection 위험이 생긴다.

수정된 예:

{% raw %}
```yaml
permissions: {}

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@<full-length-sha>
      - name: Print PR title as data
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
        run: |
          printf '%s\n' "$PR_TITLE"
```
{% endraw %}

`<full-length-sha>`는 review한 action commit SHA로 바꾼다. PR 제목은 shell script 본문에 직접 삽입하지 않고 환경 변수 데이터로 넘긴다.

## 실패 로그 예시

권한을 줄인 뒤 기존 workflow가 repository에 write를 시도하면 아래와 비슷한 실패가 날 수 있다.

```text
remote: Permission to <owner>/<repo>.git denied to github-actions[bot].
fatal: unable to access 'https://github.com/<owner>/<repo>/': The requested URL returned error: 403
```

이때 권한을 바로 넓히지 말고 먼저 질문을 나눈다.

- 이 job이 정말 write를 해야 하는가?
- write가 필요하다면 `contents: write`, `packages: write`, `pull-requests: write` 중 어떤 권한만 필요한가?
- write 작업을 pull request job이 아니라 release/deploy job으로 분리할 수 있는가?

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-06-05
- 문서 성격: analysis | tutorial
- 테스트 환경: 실행 테스트 없음. GitHub Actions 공식 보안 문서 기준으로 점검 항목 정리.
- 테스트 버전: GitHub Docs 2026-06-05 확인본. 특정 runner image나 workflow 실행 버전은 고정하지 않음.
- 출처 등급: 공식 문서

## 문제 정의

GitHub Actions는 저장소 코드와 secret, release, package, cloud 배포 권한을 한 workflow 안에서 다룰 수 있다. 따라서 작은 workflow도 공급망 공격면이 된다. 특히 PR에서 들어온 문자열, third-party action, 과도한 `GITHUB_TOKEN`, self-hosted runner, 장기 cloud credential은 별도 보안 경계로 봐야 한다.

이 글은 새 workflow를 추가하거나 기존 workflow를 리뷰할 때 확인할 최소 체크리스트를 정리한다.

## 확인된 사실

- GitHub 문서는 workflow, custom action, composite action에서 attacker-controlled context가 실행 코드로 해석될 수 있다고 설명한다.
  근거: [GitHub Actions script injections](https://docs.github.com/en/actions/concepts/security/script-injections)
- `GITHUB_TOKEN`은 workflow에서 명시적으로 넘기지 않아도 `github.token` context를 통해 action이 접근할 수 있으므로 최소 권한으로 제한해야 한다.
  근거: [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
- `permissions` key는 workflow 전체 또는 job 단위로 `GITHUB_TOKEN` 권한을 줄이는 공식 방법이다.
  근거: [Modifying the permissions for the GITHUB_TOKEN](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token#modifying-the-permissions-for-the-github_token)
- GitHub 공식 보안 문서는 third-party action을 full-length commit SHA로 pinning하는 것을 권장한다.
  근거: [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use#using-third-party-actions)
- GitHub 문서는 OIDC를 사용해 cloud provider에 직접 인증하면 장기 cloud secret 저장을 줄일 수 있다고 설명한다.
  근거: [OpenID Connect in GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

## 직접 재현한 결과

- 직접 재현 없음: 이 글은 특정 저장소의 workflow를 스캔한 보고서가 아니다.
- 직접 확인한 범위: 2026-04-29 기준 GitHub Actions 공식 문서의 보안 권고와 설정 항목.

## 재현 순서

workflow 리뷰는 아래 순서로 진행한다.

1. trigger를 확인한다.

- `pull_request`, `pull_request_target`, `workflow_run`, `workflow_dispatch`, `schedule`의 권한 차이를 확인한다.
- fork PR에서 secret이나 write 권한이 필요한지 따로 본다.
- PR 제목, branch name, issue body, commit message 같은 context 값을 shell에 직접 넣지 않는다.

2. `GITHUB_TOKEN` 권한을 job 단위로 줄인다.

```yaml
permissions: {}

jobs:
  test:
    permissions:
      contents: read
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<full-length-sha>
```

3. third-party action을 검토한다.

- `uses: owner/repo@v1`보다 full-length commit SHA pinning을 우선한다.
- action source와 release provenance, maintainer, update 방식, Dependabot alert 여부를 확인한다.
- composite action과 reusable workflow도 같은 기준으로 본다.

4. secrets와 environment를 분리한다.

- 테스트 job에는 배포 secret을 주지 않는다.
- production 배포는 environment protection, required reviewers, branch/tag 제한과 함께 본다.
- secret 값을 로그에 출력하지 않고, command-line argument로 넘기지 않는다.

5. runner를 확인한다.

- public repository의 self-hosted runner는 특히 위험하다.
- self-hosted runner가 내부 network, cloud metadata, Docker socket, 배포 credential에 접근 가능한지 확인한다.
- job 간 workspace, cache, artifact 공유가 secret을 옮기지 않는지 본다.

6. 배포 인증을 확인한다.

- 가능하면 long-lived cloud key 대신 OIDC를 쓴다.
- OIDC subject, audience, repository, branch/environment 조건을 cloud IAM에서 제한한다.

## 관찰 결과

- `permissions`를 명시하지 않으면 repository 기본 설정에 의존하게 되어 리뷰가 어려워진다.
- third-party action 하나가 compromise되면 같은 job의 secret과 token을 볼 수 있으므로 action pinning과 권한 축소를 같이 해야 한다.
- script injection은 workflow 문법 오류가 아니라 untrusted context가 shell, JavaScript, API call로 흘러 들어가는 문제다.

## 해석 / 의견

내 판단으로는 GitHub Actions 보안의 중심은 "workflow가 어떤 권한으로 어떤 코드를 실행하는가"다. 따라서 trigger, token 권한, action provenance, secret scope, runner 격리를 한꺼번에 봐야 한다.

의견: 모든 workflow 상단에 `permissions: {}` 또는 읽기 전용 기본값을 두고, write 권한은 필요한 job에만 추가하는 방식이 리뷰하기 쉽다.

## 한계와 예외

- GitHub Enterprise, organization policy, repository visibility, fork 설정에 따라 세부 동작이 다를 수 있다.
- 이 글은 GitHub Actions 중심 체크리스트이며 GitLab CI, Jenkins, CircleCI에는 그대로 적용되지 않는다.
- 실제 공격 대응에는 audit log, secret rotation, runner forensic, dependency review 결과가 추가로 필요하다.
- 위 workflow와 로그는 예시다. 발행 전에는 GitHub Actions workflow syntax, `GITHUB_TOKEN` 권한 이름, runner image, action pinning 정책을 다시 확인해야 한다.

## 발행 전 재검증 필요

이 글은 예약 글이다. 발행 전에 아래 항목을 다시 확인해야 한다.

- `GITHUB_TOKEN` 권한 이름과 기본 권한 정책이 바뀌지 않았는지
- workflow syntax의 `permissions`, `pull_request`, `pull_request_target`, `workflow_run` 동작 설명이 유지되는지
- GitHub Actions secure use reference의 third-party action pinning 권고가 바뀌지 않았는지
- secrets와 OIDC 관련 공식 문서 URL이 유지되는지
- `ubuntu-latest` runner image와 기본 도구 구성이 바뀌지 않았는지

## 참고자료

- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub Actions script injections](https://docs.github.com/en/actions/concepts/security/script-injections)
- [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
- [GITHUB_TOKEN](https://docs.github.com/actions/concepts/security/github_token)
- [GitHub Actions secrets reference](https://docs.github.com/en/actions/reference/security/secrets)
- [OpenID Connect in GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: GitHub Actions 공식 문서 기준으로 trigger, token, action pinning, secret, runner, OIDC 체크리스트 보강.
