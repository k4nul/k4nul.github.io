---
layout: single
title: "cloud IAM 과권한과 service account 관리"
description: "Cloud IAM 과권한을 줄이기 위해 service account, workload identity, 임시 자격 증명, 감사 로그, 권한 검토 기준을 정리한다."
date: 2026-07-30 09:00:00 +09:00
lang: ko
translation_key: cloud-iam-and-service-account-least-privilege
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

Cloud IAM 최소 권한은 "관리자 권한을 주지 않는다"에서 끝나지 않는다. 어떤 workload가 어떤 resource에 어떤 action을 어떤 credential lifetime으로 수행하는지까지 쪼개야 한다.

Service account는 사람이 아니라 애플리케이션, 배치 작업, CI/CD, VM, container 같은 workload의 신원이다. 그래서 사용자 계정보다 방치되기 쉽고, 한 번 과권한이 붙으면 lateral movement와 privilege escalation의 통로가 될 수 있다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: tutorial | analysis
- 테스트 환경: 로컬 실행 테스트 없음. Google Cloud IAM, AWS IAM, Microsoft Entra 공식 문서를 기준으로 원칙을 정리했다.
- 테스트 버전: 공식 문서 2026-04-29 확인. provider별 콘솔 화면과 role 이름은 바뀔 수 있다.
- 출처 성격: 공식 클라우드 문서

## 문제 정의

Cloud IAM 사고의 많은 부분은 credential 자체보다 "권한이 넓고 오래 살아 있는 workload identity"에서 시작된다. 예를 들어 CI job이 조직 전체 관리자 권한을 갖거나, default service account가 프로젝트 Editor 권한을 갖거나, long-lived key가 저장소 secret에 오래 남아 있으면 하나의 유출이 넓은 피해로 이어진다.

이 글은 provider별 세부 문법보다 공통 운영 기준을 다룬다.

## 확인한 사실

- Google Cloud 문서는 service account를 resource처럼 관리하고, 전용 service account를 만들며, default service account의 자동 Editor 권한 부여를 피하라고 권고한다.
- Google Cloud 문서는 access scope가 fine-grained allow policy를 대체하지 못하며, service account key 생성과 impersonation 권한을 제한해야 한다고 설명한다.
- AWS IAM 문서는 workload가 IAM role 기반 temporary credentials를 사용하고, 작업에 필요한 action/resource/condition만 허용하는 least privilege를 적용하라고 권고한다.
- Microsoft Entra managed identity 문서는 managed identity에도 필요한 최소 권한만 부여하고, 불필요한 subscription contributor 권한은 blast radius를 키운다고 설명한다.
- 이 글의 검증 기준일은 2026-04-29이다.

## 최소 권한 기준

| 점검 축 | 질문 | 나쁜 신호 |
| --- | --- | --- |
| Identity | 이 workload만을 위한 service account인가? | 여러 앱이 같은 계정을 공유함 |
| Resource scope | project/account/subscription 전체가 필요한가? | 조직, 프로젝트, subscription 단위로 broad role 부여 |
| Action scope | 읽기, 쓰기, 삭제, 배포가 분리돼 있는가? | `Owner`, `Editor`, `Administrator`, `*` 권한 사용 |
| Credential type | 임시 credential이나 workload identity federation을 쓰는가? | long-lived key를 CI secret이나 파일로 보관 |
| Lifetime | 권한이 작업 시간 동안만 유효한가? | 한 번 만든 key와 role binding이 계속 유지됨 |
| Auditability | 어떤 workload가 실행했는지 로그로 구분되는가? | 하나의 service account를 여러 시스템이 공유 |
| Review | unused permission과 unused identity를 정기적으로 제거하는가? | 퇴역한 앱의 service account가 살아 있음 |

## 운영 절차

1. workload 목록을 만든다. 예: web runtime, batch worker, CI build, deploy job, backup job, monitoring job.
2. 각 workload에 별도 service account 또는 workload identity를 배정한다.
3. 필요한 API action을 읽기, 쓰기, 삭제, 권한 변경, 배포로 분리한다.
4. resource scope를 가능한 가장 좁은 단위로 제한한다. bucket 하나, repository 하나, namespace 하나처럼 구체화한다.
5. long-lived key 대신 cloud-native runtime identity, IAM role, managed identity, workload identity federation, OIDC를 우선 사용한다.
6. CI/CD에는 build와 deploy의 identity를 분리한다. build job이 production 권한을 갖지 않게 한다.
7. 권한 변경, impersonation, key 생성, secret 읽기 권한은 별도 high-risk 권한으로 리뷰한다.
8. audit log에서 최근 사용 기록을 확인하고 unused service account, unused key, unused permission을 제거한다.

## Provider별 해석

Google Cloud에서는 default service account와 service account key가 특히 자주 문제가 된다. default service account에 자동으로 넓은 권한이 붙어 있지 않은지, 사용자가 더 높은 권한의 service account를 impersonate할 수 있지 않은지 확인한다.

AWS에서는 IAM role과 temporary credentials가 기본값이어야 한다. managed policy로 시작하더라도 운영이 성숙해지면 Access Analyzer와 실제 사용 기록을 바탕으로 customer managed policy를 좁혀야 한다.

Azure/Microsoft Entra에서는 system-assigned managed identity와 user-assigned managed identity의 lifecycle 차이를 이해해야 한다. 같은 권한을 여러 replica가 공유해야 하는지, 개별 resource별 추적성이 더 중요한지에 따라 선택이 달라진다.

## 리뷰 예시

`ci-deploy-prod` identity가 `AdministratorAccess` 또는 subscription `Contributor`를 갖고 있다면 최소 권한으로 보기 어렵다. 더 좋은 형태는 다음과 같다.

- build job: artifact registry push 권한만 가진 identity
- scan job: artifact read와 security report write 권한만 가진 identity
- deploy job: 특정 service 또는 namespace에 대한 deployment update 권한만 가진 identity
- break-glass identity: 별도 보관, MFA, 짧은 승인 시간, 사용 후 리뷰

## 한계와 예외

- 이 글은 provider별 전체 IAM 문법을 다루지 않는다.
- 일부 관리 작업은 일시적으로 넓은 권한이 필요할 수 있다. 이때는 승인, 만료, 사후 리뷰가 함께 있어야 한다.
- 조직 정책, compliance 요구사항, 계정 구조에 따라 실제 role 설계는 달라질 수 있다.

## 참고자료

- [Google Cloud: Best practices for using service accounts securely](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts)
- [Google Cloud: Best practices for managing service account keys](https://docs.cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys)
- [AWS IAM: Security best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Microsoft Entra: Managed identity best practice recommendations](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/managed-identity-best-practice-recommendations)
- [Microsoft Entra: Workload identities overview](https://learn.microsoft.com/en-us/entra/workload-id/workload-identities-overview)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: cloud IAM 최소 권한, service account lifecycle, provider별 점검 기준을 보강.
