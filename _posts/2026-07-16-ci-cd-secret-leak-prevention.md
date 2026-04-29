---
layout: single
title: "CI/CD secret leak 방지 기준"
description: "CI/CD secret leak 방지 기준에 대해 공식 문서와 운영 관점으로 확인할 기준, 점검 순서, 한계를 정리한 글."
date: 2026-07-16 09:00:00 +09:00
lang: ko
translation_key: ci-cd-secret-leak-prevention
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

CI/CD secret leak 방지는 "secret을 secret store에 넣었다"에서 끝나지 않는다. secret이 workflow trigger, runner, log, artifact, cache, command-line argument, third-party action, cloud credential로 어떻게 이동하는지 확인해야 한다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: analysis | tutorial
- 테스트 환경: 실행 테스트 없음. GitHub Actions 공식 보안 문서와 secret reference 기준으로 CI/CD 일반 기준 정리.
- 테스트 버전: GitHub Docs 2026-04-29 확인본. 특정 CI provider 실행 버전은 고정하지 않음.
- 출처 등급: 공식 문서

## 문제 정의

CI/CD는 source code, dependency, build artifact, deployment credential이 만나는 지점이다. secret leak은 코드 저장소에 token을 commit하는 경우만 뜻하지 않는다. workflow log, failed command, artifact upload, cache, self-hosted runner process list, fork PR, third-party action도 secret이 새는 경로가 될 수 있다.

## 확인된 사실

- GitHub Actions secrets reference는 secret redaction을 잘 동작시키려면 structured data를 secret 값으로 쓰는 것을 피하라고 설명한다.
  근거: [GitHub Actions secrets reference](https://docs.github.com/en/actions/reference/security/secrets)
- GitHub secure use reference는 secret 값이 변형될 수 있으므로 automatic redaction이 보장되지 않는다고 설명한다.
  근거: [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use#use-secrets-for-sensitive-information)
- GitHub 문서는 third-party action compromise가 repository secret과 `GITHUB_TOKEN` 접근으로 이어질 수 있다고 설명한다.
  근거: [GitHub Actions third-party actions](https://docs.github.com/en/actions/reference/security/secure-use#using-third-party-actions)
- GitHub 문서는 self-hosted runner가 public repository에서 특히 위험하며, command-line argument로 전달된 secret이 같은 runner의 다른 job에서 보일 수 있다고 설명한다.
  근거: [GitHub Actions self-hosted runners security](https://docs.github.com/en/actions/reference/security/secure-use#hardening-for-self-hosted-runners)
- GitHub 문서는 cloud provider 배포에 OIDC를 사용해 short-lived, well-scoped access token을 고려하라고 권장한다.
  근거: [OpenID Connect in GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

## 직접 재현한 결과

- 직접 재현 없음: 이 글은 특정 CI/CD provider에서 secret leak을 재현한 실험 보고서가 아니다.
- 직접 확인한 범위: 2026-04-29 기준 GitHub Actions 공식 문서의 secret, runner, OIDC, third-party action 보안 권고.

## 재현 순서

CI/CD secret leak 방지 기준은 아래 항목으로 점검한다.

1. secret 저장 위치를 분리한다.

- repository, organization, environment secret의 범위를 구분한다.
- production secret은 production environment와 reviewer, branch/tag 제한 뒤에 둔다.
- test job과 PR validation job에는 배포 secret을 주지 않는다.

2. workflow trigger를 확인한다.

- fork PR, `pull_request_target`, `workflow_run`에서 secret이 열리는지 확인한다.
- untrusted input이 secret을 사용하는 step, shell command, API request로 흘러가지 않게 한다.

3. log 노출을 줄인다.

- secret을 `echo`, debug output, stack trace, `set -x`, verbose CLI 출력에 노출하지 않는다.
- structured JSON blob 전체를 secret으로 저장하지 않는다.
- secret이 변형, 인코딩, 잘림, 조합된 경우 redaction이 실패할 수 있다고 가정한다.

4. artifact, cache, test report를 확인한다.

- `.env`, kubeconfig, cloud credential, npm token, docker config, crash dump가 artifact에 들어가지 않는지 본다.
- dependency cache와 build cache에 credential file이 섞이지 않게 한다.

5. runner를 확인한다.

- self-hosted runner에 남는 workspace, process list, Docker layer, local cache, credential helper를 확인한다.
- public repository에는 self-hosted runner 사용을 피한다.

6. 배포 인증을 줄인다.

- 가능하면 long-lived cloud key 대신 OIDC를 사용한다.
- OIDC token은 repository, branch, environment, workflow 조건으로 제한한다.
- 배포 job의 `GITHUB_TOKEN`은 필요한 권한만 둔다.

7. leak 대응 기준을 준비한다.

- leak 의심 시 token revoke, secret rotate, workflow disable, runner quarantine, audit log 확인, artifact/cache 삭제 순서를 문서화한다.

예시 기준은 다음과 같다.

```yaml
permissions:
  contents: read

jobs:
  deploy:
    environment: production
    permissions:
      contents: read
      id-token: write
    steps:
      - name: Authenticate with cloud using OIDC
        run: ./scripts/login-with-oidc.sh
```

## 관찰 결과

- secret masking은 방어선 중 하나일 뿐이며 유출 방지 보장은 아니다.
- third-party action, self-hosted runner, artifact upload는 secret store 밖에서 secret이 노출되는 대표 경로다.
- 장기 cloud key를 CI secret으로 저장하면 leak 시 피해 시간이 길어진다. OIDC와 짧은 수명의 token은 피해 시간을 줄이는 데 도움이 된다.

## 해석 / 의견

내 판단으로는 CI/CD secret leak 방지는 "저장"보다 "이동"을 보는 문제다. secret이 어떤 event에서 어떤 runner로 전달되고 어떤 step과 artifact를 거치는지 설명할 수 있어야 한다.

의견: 배포 secret은 test workflow와 분리하고, production 환경에는 reviewer와 branch 제한을 두는 것을 기본값으로 삼는 편이 안전하다.

## 한계와 예외

- GitHub Actions 기준으로 정리했으므로 다른 CI/CD provider는 secret scope, masking, runner 격리 동작을 따로 확인해야 한다.
- OIDC를 사용할 수 없는 cloud나 legacy system은 secret rotation 주기와 접근 범위를 더 엄격히 관리해야 한다.
- 사고 대응에는 provider audit log, cloud IAM log, registry log, runner forensic이 추가로 필요하다.

## 참고자료

- [GitHub Actions secrets reference](https://docs.github.com/en/actions/reference/security/secrets)
- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub Actions script injections](https://docs.github.com/en/actions/concepts/security/script-injections)
- [Use GITHUB_TOKEN for authentication in workflows](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
- [OpenID Connect in GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: secret 저장소, 로그 마스킹 한계, artifact/cache, runner, OIDC, leak 대응 기준 보강.
