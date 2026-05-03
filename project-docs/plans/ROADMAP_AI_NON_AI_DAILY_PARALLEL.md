# AI and Non-AI Weekly Parallel Roadmap

## Snapshot

- 검토 기준일: 2026-04-29 KST
- 목적: 예약 글이 조정된 뒤에도 AI 운영/보안과 Non-AI 보안 엔지니어링 흐름을 병행하되, 발행량을 품질 검증 가능한 수준으로 낮춘다.
- 현재 예약분: `_posts`의 생성 완료 예약 글은 2026-06-13 K8S 10 KOR/ENG 동시 발행까지 이어진다.
- 후속 시작일: 2026-06-16
- 발행 단위: 주 2주제. 각 주제는 한국어 원문과 영어 미러를 같은 날짜에 발행한다.
- 실제 파일 수 기준: 8주 동안 16주제, 32개 `_posts` 파일.
- 이전 계획 대비 변경: 기존 일일 `AI 1주제 + Non-AI 1주제` 계획은 품질 검증과 독자 소화 속도에 비해 과했으므로 주간 병행 계획으로 축소한다.

## Cadence

| Day | Publish item | Reason |
| --- | --- | --- |
| Monday | 예약 없음 | 전주 글 점검, 링크 보강, 빌드/메타데이터 확인 |
| Tuesday | AI 주제 KOR/ENG 동시 발행 | 주간 AI 운영/보안 주제 시작, hreflang 쌍 동시 노출 |
| Wednesday | 예약 없음 | 전날 발행 글 링크와 메타데이터 확인 |
| Thursday | Non-AI 주제 KOR/ENG 동시 발행 | 보안 엔지니어링 또는 운영 보안 주제 발행 |
| Friday | 예약 없음 | 주간 마감, 번역 표현과 참고자료 보강 |
| Weekend | 예약 없음 | 재현 테스트, 참고자료 검증, 다음 주 초안 준비 |

## Positioning

- AI 흐름: `trace/audit -> guardrail/approval -> prompt injection -> tool permission -> MCP/data exposure -> threat modeling -> sensitive data -> incident review`
- Non-AI 흐름: `Kubernetes troubleshooting -> RBAC -> GitHub Actions security -> SBOM/SLSA -> CI/CD secrets -> container image security -> IAM/service account -> incident timeline`
- SEO 기준: 검색량보다 검증 가능성, 문제 구체성, 최신성 기준일, 한계와 예외를 우선한다.
- 전문성 기준: 공식 문서, 표준 문서, 원저자 저장소, 직접 재현 결과를 주장 옆에 연결한다.

## Topic Keys and Tags

### AI 후속 시리즈

- 권장 시리즈명: `AI 에이전트 운영과 보안`
- 저장 위치: `_posts`
- `section`: `development`
- `topic_key`: `ai`
- 기본 태그: `[ai, llm, agents, harness-engineering, ai-agent-operations]`
- 주제별 추가 태그 후보: `ai-security`, `guardrails`, `mcp`, `trace`, `evaluation`, `context`, `prompt-injection`, `supply-chain`
- 글 성격: 보안/평가 글은 `analysis` 또는 `tutorial`을 우선한다.

### Non-AI 후속 축

- DevOps/Kubernetes 운영 글: `section: development`, `topic_key: devops`
- 보안 엔지니어링 글: `section: security`, `topic_key: security-engineering`
- 보안 엔지니어링 기본 태그: `[security, supply-chain-security, cloud-security, devsecops]`
- DevOps 운영 기본 태그: `[devops, kubernetes, operations]`

## Evidence Baseline

- Google Search Central SEO Starter Guide: unique, up-to-date, helpful, reliable, people-first content를 기준으로 삼는다.
- Google Search Central Helpful Content: 검색 엔진 우선 콘텐츠보다 기존 독자와 목적에 맞는 people-first 콘텐츠를 우선한다.
- OWASP GenAI Security Project: LLM 애플리케이션 보안 위험과 agentic AI 시스템 위험을 AI 보안 글의 기준 출처로 사용한다.
- OWASP ASVS, OWASP Top 10, OWASP Cheat Sheet Series, OWASP Secure Coding Practices: secure coding, code review, 애플리케이션 보안 요구사항 글의 기준 출처로 사용한다.
- World Economic Forum Global Cybersecurity Outlook 2026: AI, 공급망, cloud가 2026년 보안 리스크에서 중요한 축이라는 근거로 사용한다.
- Verizon DBIR 2025: 취약점 악용, credential abuse, third-party breach 증가를 보안 트렌드 글의 배경 근거로 사용한다.
- NIST SSDF SP 800-218, CISA SBOM 자료: 소프트웨어 공급망 보안, secure development, SBOM 글의 기준 출처로 사용한다.

## Calendar

각 주는 `AI 1주제 + Non-AI 1주제`로 구성한다. 한국어 원문과 영어 미러는 같은 날짜에 함께 발행한다.

| Week | Date | Stream | Lang | Topic | Topic key | Slug |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2026-06-16 | AI | ko | 에이전트 trace에는 무엇을 남겨야 하는가 | ai | what-should-agent-trace-record |
| 1 | 2026-06-16 | AI | en | What should an agent trace record? | ai | what-should-agent-trace-record-en |
| 1 | 2026-06-18 | Non-AI | ko | Kubernetes 장애 대응: describe, events, logs | devops | kubernetes-troubleshooting-describe-events-logs |
| 1 | 2026-06-18 | Non-AI | en | Kubernetes troubleshooting with describe, events, and logs | devops | kubernetes-troubleshooting-describe-events-logs-en |
| 2 | 2026-06-23 | AI | ko | 하네스 관점의 guardrail과 approval 경계 | ai | guardrails-and-approval-boundaries-in-harness |
| 2 | 2026-06-23 | AI | en | Guardrails and approval boundaries from a harness perspective | ai | guardrails-and-approval-boundaries-in-harness-en |
| 2 | 2026-06-25 | Non-AI | ko | Kubernetes RBAC 최소 권한 입문 | security-engineering | kubernetes-rbac-least-privilege-basics |
| 2 | 2026-06-25 | Non-AI | en | Kubernetes RBAC least privilege basics | security-engineering | kubernetes-rbac-least-privilege-basics-en |
| 3 | 2026-06-30 | AI | ko | prompt injection을 하네스 문제로 보기 | ai | prompt-injection-as-a-harness-problem |
| 3 | 2026-06-30 | AI | en | Prompt injection as a harness problem | ai | prompt-injection-as-a-harness-problem-en |
| 3 | 2026-07-02 | Non-AI | ko | GitHub Actions 보안 체크리스트 | security-engineering | github-actions-security-checklist |
| 3 | 2026-07-02 | Non-AI | en | GitHub Actions security checklist | security-engineering | github-actions-security-checklist-en |
| 4 | 2026-07-07 | AI | ko | tool call 권한을 task 단위로 제한하기 | ai | limit-tool-call-permissions-per-task |
| 4 | 2026-07-07 | AI | en | Limit tool-call permissions per task | ai | limit-tool-call-permissions-per-task-en |
| 4 | 2026-07-09 | Non-AI | ko | SBOM, SLSA, provenance 입문 | security-engineering | sbom-slsa-provenance-basics |
| 4 | 2026-07-09 | Non-AI | en | SBOM, SLSA, and provenance basics | security-engineering | sbom-slsa-provenance-basics-en |
| 5 | 2026-07-14 | AI | ko | MCP 연결 전 데이터 노출 점검 | ai | mcp-data-exposure-check-before-connection |
| 5 | 2026-07-14 | AI | en | Check data exposure before connecting MCP | ai | mcp-data-exposure-check-before-connection-en |
| 5 | 2026-07-16 | Non-AI | ko | CI/CD secret leak 방지 기준 | security-engineering | ci-cd-secret-leak-prevention |
| 5 | 2026-07-16 | Non-AI | en | CI/CD secret leak prevention criteria | security-engineering | ci-cd-secret-leak-prevention-en |
| 6 | 2026-07-21 | AI | ko | AI coding agent 보안 위협 모델 입문 | ai | threat-modeling-ai-coding-agents |
| 6 | 2026-07-21 | AI | en | Threat modeling AI coding agents | ai | threat-modeling-ai-coding-agents-en |
| 6 | 2026-07-23 | Non-AI | ko | container image signing과 scan 결과 해석 | security-engineering | container-image-signing-and-scan-results |
| 6 | 2026-07-23 | Non-AI | en | Container image signing and scan result interpretation | security-engineering | container-image-signing-and-scan-results-en |
| 7 | 2026-07-28 | AI | ko | AI agent와 개인정보/민감정보 경계 | ai | ai-agents-and-sensitive-data-boundaries |
| 7 | 2026-07-28 | AI | en | AI agents and sensitive data boundaries | ai | ai-agents-and-sensitive-data-boundaries-en |
| 7 | 2026-07-30 | Non-AI | ko | cloud IAM 과권한과 service account 관리 | security-engineering | cloud-iam-and-service-account-least-privilege |
| 7 | 2026-07-30 | Non-AI | en | Cloud IAM and service account least privilege | security-engineering | cloud-iam-and-service-account-least-privilege-en |
| 8 | 2026-08-04 | AI | ko | AI agent incident review 템플릿 | ai | ai-agent-incident-review-template |
| 8 | 2026-08-04 | AI | en | AI agent incident review template | ai | ai-agent-incident-review-template-en |
| 8 | 2026-08-06 | Non-AI | ko | incident timeline 작성법과 보안 엔지니어링 정리 | security-engineering | incident-timeline-and-security-engineering-wrap-up |
| 8 | 2026-08-06 | Non-AI | en | Incident timelines and security engineering wrap-up | security-engineering | incident-timeline-and-security-engineering-wrap-up-en |

## Deferred Candidate Pool

아래 주제는 좋은 후보지만 8주 핵심 계획에는 넣지 않는다. 실제 재현 자료, 공식 문서 변경, 독자 반응이 확인될 때 별도 시리즈나 보강 글로 승격한다.

- AI 운영/보안: context summary 품질 평가, subagent 결과 검증, agent memory 분리, output contract, eval dataset, prompt regression, AI 보안 FAQ 허브.
- 공급망/CI/CD 보안: CISA KEV와 EPSS, CVSS 한계, Dependabot/Renovate, npm/pip 공급망 공격, Git submodule과 hook 보안 경계.
- Kubernetes/container 보안: admission control, ServiceAccount token, container runtime 기본값, network policy, Kubernetes upgrade preflight.
- Cloud/IaC/GitOps 보안: API key rotation, Terraform state, IaC drift, GitOps 감사, Argo CD 권한과 sync 경계.
- 탐지/분석: YARA rule, Sigma rule, EDR alert 글감화, phishing kit trend, account takeover와 MFA fatigue, OAuth app permission, SaaS audit log, cloud storage 공개 노출.
- Secure Coding with AI: OWASP Top 10 리뷰 질문, 입력 검증과 output encoding, 인증/인가, injection 테스트, secret leak, dependency 취약점 검증, SAST triage, secure coding Definition of Done.

## Writing Requirements

- 모든 신규 글은 `_posts/AGENTS.md`, `docs/blog-style.md`, `templates/post-template.md`를 따른다.
- front matter 필수값: `title`, `date`, `lang`, `translation_key`, `section`, `topic_key`, `categories`, `tags`, `description`.
- 본문 필수 섹션: `## 요약`, `## 문서 정보`, `## 문제 정의`, `## 확인된 사실`, `## 직접 재현한 결과`, `## 해석 / 의견`, `## 한계와 예외`, `## 참고자료`.
- 최신성 민감 글은 `검증 기준일`을 명시하고, 공식 문서 확인일을 본문에 적는다.
- 실행 테스트가 가능한 글은 명령, 환경, 버전을 남긴다.
- 실행 테스트가 없는 분석 글은 `직접 재현 없음`과 이유를 명시한다.
- 영어 미러는 같은 `translation_key`를 공유하고, `lang: en`과 명시적 `permalink`를 둔다.

## Update Triggers

- 실제 포스트 파일을 생성하거나 발행 일정을 바꾸는 경우
- `topic_key`를 `ai`, `devops`, `security-engineering`, `rust`가 아닌 값으로 조정하는 경우
- AI 보안 또는 공급망 보안의 기준 출처가 새 버전으로 바뀌는 경우
- 주 2주제 발행 정책을 다시 일일 발행이나 격주 발행으로 바꾸는 경우
