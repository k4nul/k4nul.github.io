---
layout: single
title: "incident timeline 작성법과 보안 엔지니어링 정리"
description: "보안 사고 timeline을 사실, 추정, 의사결정, 증거로 나누어 작성하고 보안 엔지니어링 개선으로 연결하는 방법을 정리한다."
date: 2026-08-06 09:00:00 +09:00
lang: ko
translation_key: incident-timeline-and-security-engineering-wrap-up
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

Incident timeline은 사고 보고서의 장식이 아니라 대응 품질을 높이는 엔지니어링 도구다. 좋은 timeline은 "언제 무엇이 일어났는가"뿐 아니라 "그 사실을 어떤 증거로 확인했는가", "그때 어떤 결정을 했는가", "무엇은 아직 추정인가"를 분리한다.

보안 엔지니어링 관점의 마무리는 하나다. 사고에서 드러난 약한 경계를 다음 설계에 반영해야 한다. 권한, 로그, 승인, 배포, secret, 탐지, runbook이 그 대상이다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: tutorial | analysis
- 테스트 환경: 로컬 실행 테스트 없음. NIST SP 800-61 Rev. 3와 CISA incident response playbook을 기준으로 사고 기록 구조를 정리했다.
- 테스트 버전: 공식 문서 2026-04-29 확인. 조직별 incident severity와 법적 보고 기준은 별도 적용해야 한다.
- 출처 성격: 공식 문서, 정부 보안 문서

## 확인한 사실

- NIST SP 800-61 Rev. 3는 2025년 4월에 발행됐고, SP 800-61 Rev. 2를 대체한다.
- NIST SP 800-61 Rev. 3는 incident response를 CSF 2.0 기반의 cybersecurity risk management 활동과 연결한다.
- CISA Federal Government Cybersecurity Incident and Vulnerability Response Playbooks는 incident response와 vulnerability response를 표준 운영 절차로 정리한다.
- 이 글의 검증 기준일은 2026-04-29이다.

## Timeline에 반드시 남길 항목

| 항목 | 내용 | 예시 |
| --- | --- | --- |
| 시각 | timezone 포함, 가능하면 UTC와 local time 중 하나로 통일 | `2026-04-29 10:15 KST` |
| 이벤트 | 관찰된 사실 중심의 짧은 문장 | `production deploy job failed` |
| 출처 | 로그, alert, commit, ticket, trace, 사용자 신고 | `GitHub Actions run 12345` |
| 상태 | confirmed 또는 assumption | `confirmed` |
| 영향 | 사용자, 서비스, 데이터, 비용, 보안 영향 | `admin API 5xx 증가` |
| 조치 | containment, rollback, key rotation, 권한 회수 | `deploy token revoked` |
| 결정 | 누가 어떤 기준으로 결정했는지 | `incident lead approved rollback` |

## 작성 절차

1. 먼저 timeline의 기준 timezone을 정한다. 여러 시스템 로그를 섞는다면 변환 기준을 문서 상단에 적는다.
2. 탐지 시각과 실제 발생 추정 시각을 분리한다. `detected_at`과 `started_at`은 다를 수 있다.
3. 로그 원문을 그대로 붙이기보다 event, evidence, interpretation을 나눈다.
4. 확인된 사실과 추정을 구분한다. 추정은 나중에 수정할 수 있도록 남겨야 한다.
5. containment 조치와 recovery 조치를 분리한다. 막은 것과 복구한 것은 다르다.
6. 권한 변경, secret rotation, 배포, 데이터 삭제처럼 되돌리기 어려운 조치는 승인자와 근거를 함께 기록한다.
7. timeline 끝에는 `unknowns`를 남긴다. 아직 모르는 것을 감추면 후속 조치가 약해진다.

## 나쁜 Timeline과 좋은 Timeline

나쁜 예:

```text
10:00 장애 발생
10:20 확인함
10:40 복구함
```

좋은 예:

```text
2026-04-29 10:03 KST | alert | API 5xx rate > 5% | Prometheus alert #123 | confirmed
2026-04-29 10:07 KST | investigation | deploy run 456 changed auth middleware | GitHub Actions run 456, commit abc123 | confirmed
2026-04-29 10:12 KST | decision | incident lead approved rollback | Slack incident channel, ticket INC-9 | confirmed
2026-04-29 10:18 KST | containment | rollback completed | deploy run 457 | confirmed
2026-04-29 10:32 KST | recovery | 5xx rate returned below threshold | dashboard snapshot | confirmed
```

## 보안 엔지니어링으로 연결하기

사고 리뷰의 결론은 "주의하자"가 아니다. 다음 변경으로 이어져야 한다.

- 탐지가 늦었다면 alert rule, log field, metric cardinality를 고친다.
- 원인 파악이 늦었다면 deploy record, trace ID, commit SHA, change owner를 연결한다.
- 피해 범위가 컸다면 IAM, RBAC, service account, tool permission을 줄인다.
- 승인 경계가 모호했다면 high-risk action 승인 기준을 만든다.
- secret이 노출됐다면 secret scanning, rotation, short-lived credential을 적용한다.
- 복구가 느렸다면 rollback runbook과 dry-run 검증을 만든다.

## 마무리 기준

Incident는 서비스가 살아났다고 끝나지 않는다. 다음 항목이 닫혀야 마무리로 볼 수 있다.

- timeline의 confirmed/assumption 상태가 정리됨
- 영향 범위와 데이터 노출 가능성이 판단됨
- credential, permission, 배포 상태가 복구됨
- 고객/내부/외부 보고 필요성이 검토됨
- follow-up action에 담당자와 기한이 있음
- 같은 실패를 다시 만들 수 있는 재현 조건이 문서화됨

## 한계와 예외

- 이 글은 법적 보고, 개인정보 침해 신고, 고객 공지를 대체하지 않는다.
- 법무, 개인정보보호, compliance 요구사항이 있는 사고는 조직 정책이 우선한다.
- 공격자에게 유리한 내부 탐지 세부사항은 공개 보고서에 그대로 넣지 않는다.

## 참고자료

- [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
- [NIST Incident Response project](https://csrc.nist.gov/projects/incident-response)
- [CISA Federal Government Cybersecurity Incident and Vulnerability Response Playbooks](https://www.cisa.gov/resources-tools/resources/federal-government-cybersecurity-incident-and-vulnerability-response-playbooks)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: timeline 작성 기준, 증거 분리, 보안 엔지니어링 후속 조치 기준을 보강.
