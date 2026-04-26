# AI and Non-AI Daily Parallel Roadmap

## Snapshot

- 검토 기준일: 2026-04-26 KST
- 목적: 예약 글이 끝나는 2026-06-25 이후, 매일 `AI 1주제 + Non-AI 1주제`를 KOR/ENG 미러로 발행하는 8주 계획을 보관한다.
- 시작일: 2026-06-26
- 발행 단위: 하루 2주제, 주제마다 한국어 원문과 영어 미러를 같은 날짜에 발행한다.
- 실제 파일 수 기준: 하루 4개 `_posts` 파일, 52일 동안 208개 파일.
- 현재 구현 상태: 이 문서는 발행 계획과 허브 기준을 고정한다. 각 포스트 파일은 검증 가능한 본문, 환경, 버전, 출처를 채울 수 있을 때 생성한다.

## Positioning

- AI 흐름: `하네스 엔지니어링 -> 토큰 관리 -> Codex 실전 활용 -> Claude Code 실전 활용 -> AI 에이전트 운영/보안/평가`
- Non-AI 흐름: `Docker -> Git -> Jenkins -> K8S -> Kubernetes 운영 -> 소프트웨어 공급망 보안 -> 클라우드/컨테이너 보안 -> Rust 기반 보안 도구 -> secure coding / AI-assisted secure coding`
- SEO 기준: 검색량만 좇지 않고, 독자가 직접 실행하거나 판단할 수 있는 `검증 가능성`, `구체적 문제`, `최신성 기준일`, `한계와 예외`를 우선한다.
- 전문성 기준: 공식 문서, 표준 문서, 원저자 저장소, 직접 재현 결과를 주장 옆에 연결한다.

## Topic Keys and Tags

### AI 후속 시리즈

- 권장 시리즈명: `AI 에이전트 운영과 보안`
- 저장 위치: `_posts`
- `section`: `development`
- `topic_key`: `ai`
- 기본 태그: `[ai, llm, agents, harness-engineering, ai-agent-operations]`
- 주제별 추가 태그 후보: `ai-security`, `guardrails`, `mcp`, `trace`, `evaluation`, `context`, `codex`, `claude-code`, `prompt-injection`, `supply-chain`
- 글 성격: `analysis`, `comparison`, `tutorial`, `opinion` 중 글에 맞게 선택하되, 보안/평가 글은 `analysis` 또는 `tutorial`을 우선한다.

### Non-AI 후속 축

- DevOps/Kubernetes 운영 글: `section: development`, `topic_key: devops`
- 보안 트렌드/보안 엔지니어링 글: `section: security`, `topic_key: security-engineering`
- Rust 기반 보안 도구 글: `section: development`, `topic_key: rust`
- 보안 엔지니어링 기본 태그: `[security, supply-chain-security, cloud-security, devsecops]`
- DevOps 운영 기본 태그: `[devops, kubernetes, operations]`
- Rust 보안 도구 기본 태그: `[rust, cli, security-tooling]`

## Evidence Baseline

- Google Search Central SEO Starter Guide: unique, up-to-date, helpful, reliable, people-first content를 기준으로 삼는다.
- Google Search Central Helpful Content: 검색 엔진 우선 콘텐츠보다 기존 독자와 목적에 맞는 people-first 콘텐츠를 우선한다.
- OWASP GenAI Security Project: LLM 애플리케이션 보안 위험과 agentic AI 시스템 위험을 AI 보안 글의 기준 출처로 사용한다.
- OWASP ASVS, OWASP Top 10, OWASP Cheat Sheet Series, OWASP Secure Coding Practices: secure coding, code review, 애플리케이션 보안 요구사항 글의 기준 출처로 사용한다.
- World Economic Forum Global Cybersecurity Outlook 2026: AI, 공급망, cloud가 2026년 보안 리스크에서 중요한 축이라는 근거로 사용한다.
- Verizon DBIR 2025: 취약점 악용, credential abuse, third-party breach 증가를 보안 트렌드 글의 배경 근거로 사용한다.
- NIST SSDF SP 800-218, CISA SBOM 자료: 소프트웨어 공급망 보안, secure development, SBOM 글의 기준 출처로 사용한다.

## Calendar

각 행은 같은 날짜에 발행할 2개 주제를 뜻한다. 각 주제는 KOR/ENG 미러를 함께 만든다.

| Date | AI topic | AI slug | Non-AI topic | Non-AI topic key | Non-AI slug |
| --- | --- | --- | --- | --- | --- |
| 2026-06-26 | 에이전트 trace에는 무엇을 남겨야 하는가 | what-should-agent-trace-record | Kubernetes 장애 대응: describe, events, logs | devops | kubernetes-troubleshooting-describe-events-logs |
| 2026-06-27 | AI agent 작업 기록을 감사 가능한 형태로 남기기 | auditable-ai-agent-work-records | CrashLoopBackOff와 ImagePullBackOff 분리 | devops | kubernetes-crashloopbackoff-imagepullbackoff |
| 2026-06-28 | 하네스 관점의 guardrail과 approval 경계 | guardrails-and-approval-boundaries-in-harness | Ingress 404/502 원인 좁히기 | devops | kubernetes-ingress-404-502-troubleshooting |
| 2026-06-29 | MCP 연결 전 데이터 노출 점검 | mcp-data-exposure-check-before-connection | Helm values와 rollback 기준 | devops | helm-values-and-rollback-criteria |
| 2026-06-30 | AI agent 평가를 반복 실험으로 설계하기 | design-ai-agent-evaluation-as-repeatable-experiments | Prometheus/Grafana 첫 관측성 흐름 | devops | prometheus-grafana-first-observability-flow |
| 2026-07-01 | 실패한 agent 작업을 재현 가능한 case로 남기기 | turn-failed-agent-work-into-reproducible-cases | PVC 장애와 backup/restore 검증 | devops | kubernetes-pvc-backup-restore-validation |
| 2026-07-02 | AGENTS.md와 CLAUDE.md 지시 중복 줄이기 | reduce-duplicate-instructions-in-agents-md-and-claude-md | Kubernetes RBAC 최소 권한 입문 | security-engineering | kubernetes-rbac-least-privilege-basics |
| 2026-07-03 | prompt injection을 하네스 문제로 보기 | prompt-injection-as-a-harness-problem | SBOM은 무엇이고 왜 다시 중요해졌나 | security-engineering | what-is-sbom-and-why-it-matters-again |
| 2026-07-04 | tool call 권한을 task 단위로 제한하기 | limit-tool-call-permissions-per-task | SLSA와 provenance를 입문자 관점에서 이해하기 | security-engineering | slsa-and-provenance-for-beginners |
| 2026-07-05 | agent가 읽어도 되는 문서와 안 되는 문서 | documents-agents-should-and-should-not-read | GitHub Actions 보안 체크리스트 | security-engineering | github-actions-security-checklist |
| 2026-07-06 | context summary 품질을 평가하는 기준 | criteria-for-evaluating-context-summary-quality | CI/CD secret leak 방지 기준 | security-engineering | ci-cd-secret-leak-prevention |
| 2026-07-07 | 긴 로그를 agent에게 넘기기 전 압축 기준 | compress-long-logs-before-giving-them-to-agents | container image signing과 cosign 입문 | security-engineering | container-image-signing-and-cosign-basics |
| 2026-07-08 | multi-agent 작업에서 파일 소유권 나누기 | split-file-ownership-in-multi-agent-work | container image scan 결과 해석하기 | security-engineering | how-to-read-container-image-scan-results |
| 2026-07-09 | subagent 결과를 검증하는 checklist | checklist-for-verifying-subagent-results | Kubernetes admission control 입문 | security-engineering | kubernetes-admission-control-basics |
| 2026-07-10 | Codex와 Claude Code 공통 운영 템플릿 v2 | shared-codex-and-claude-code-operations-template-v2 | CISA KEV와 EPSS로 패치 우선순위 잡기 | security-engineering | prioritize-patches-with-cisa-kev-and-epss |
| 2026-07-11 | AI coding agent 보안 위협 모델 입문 | threat-modeling-ai-coding-agents | 취약점 CVSS만 보면 안 되는 이유 | security-engineering | why-cvss-alone-is-not-enough |
| 2026-07-12 | agent 작업 요청에 threat model 넣기 | add-threat-model-to-agent-task-requests | 외부 의존성 업데이트 정책 세우기 | security-engineering | dependency-update-policy-for-external-libraries |
| 2026-07-13 | LLM output을 그대로 실행하면 안 되는 이유 | why-you-should-not-run-llm-output-directly | Dependabot/Renovate 운영 기준 | security-engineering | dependabot-renovate-operation-criteria |
| 2026-07-14 | AI agent가 만든 코드를 리뷰하는 순서 | review-order-for-code-written-by-ai-agents | npm/pip 패키지 공급망 공격 흐름 | security-engineering | npm-pip-package-supply-chain-attack-flow |
| 2026-07-15 | 자동 수정 agent의 rollback 설계 | rollback-design-for-auto-fixing-agents | Git submodule과 hook 보안 경계 | security-engineering | git-submodule-and-hook-security-boundaries |
| 2026-07-16 | agent 작업의 Definition of Done 만들기 | definition-of-done-for-agent-work | Jenkins credentials 보안 운영 | security-engineering | jenkins-credentials-security-operations |
| 2026-07-17 | agent 평가 지표: 성공률보다 중요한 것 | ai-agent-metrics-beyond-success-rate | Jenkins agent 격리와 controller 보호 | security-engineering | jenkins-agent-isolation-controller-protection |
| 2026-07-18 | hallucination을 운영 위험으로 다루기 | hallucination-as-an-operational-risk | Jenkins Pipeline에서 secret masking 한계 | security-engineering | limits-of-secret-masking-in-jenkins-pipeline |
| 2026-07-19 | AI agent와 개인정보/민감정보 경계 | ai-agents-and-sensitive-data-boundaries | 로그에 secret이 남는 경로 점검 | security-engineering | where-secrets-leak-into-logs |
| 2026-07-20 | retrieval context를 검증하는 방법 | how-to-validate-retrieval-context | cloud IAM 과권한을 줄이는 기본 원칙 | security-engineering | reduce-cloud-iam-overprivilege |
| 2026-07-21 | MCP server 신뢰 경계 설계 | mcp-server-trust-boundary-design | service account와 non-human identity 관리 | security-engineering | service-accounts-and-non-human-identity-management |
| 2026-07-22 | agent memory를 운영 문서와 분리하기 | separate-agent-memory-from-operations-docs | Kubernetes ServiceAccount token 점검 | security-engineering | kubernetes-serviceaccount-token-checks |
| 2026-07-23 | AI agent 운영 runbook 만들기 | ai-agent-operations-runbook | container runtime 보안 기본값 | security-engineering | container-runtime-security-defaults |
| 2026-07-24 | AI 코드 리뷰 자동화의 한계와 예외 | limits-and-exceptions-of-ai-code-review-automation | network policy 첫 적용 전략 | security-engineering | first-network-policy-rollout-strategy |
| 2026-07-25 | agent에게 맡기면 안 되는 승인 작업 | approvals-you-should-not-delegate-to-agents | API key rotation 운영 기준 | security-engineering | api-key-rotation-operations |
| 2026-07-26 | AI agent incident review 템플릿 | ai-agent-incident-review-template | Terraform state 보안 기본 | security-engineering | terraform-state-security-basics |
| 2026-07-27 | prompt, policy, config의 책임 나누기 | split-responsibility-between-prompt-policy-and-config | IaC drift와 보안 변경 추적 | security-engineering | iac-drift-and-security-change-tracking |
| 2026-07-28 | AI agent 작업 비용을 통제하는 방법 | control-ai-agent-work-costs | GitOps가 보안 감사에 주는 이점 | security-engineering | how-gitops-helps-security-audit |
| 2026-07-29 | human-in-the-loop를 형식이 아니라 통제로 보기 | human-in-the-loop-as-control-not-ceremony | Argo CD 권한과 sync 경계 | security-engineering | argocd-permissions-and-sync-boundaries |
| 2026-07-30 | AI agent 운영 maturity model | ai-agent-operations-maturity-model | Kubernetes upgrade 전 점검 목록 | devops | kubernetes-upgrade-preflight-checklist |
| 2026-07-31 | AI 하네스와 DevSecOps를 연결하기 | connect-ai-harness-and-devsecops | Rust로 파일 해시 CLI 만들기 | rust | rust-file-hash-cli |
| 2026-08-01 | AI 보안 테스트 케이스 작성법 | how-to-write-ai-security-test-cases | Rust로 디렉터리 스캐너 CLI 만들기 | rust | rust-directory-scanner-cli |
| 2026-08-02 | agent prompt 테스트와 regression 관리 | agent-prompt-tests-and-regression-management | Rust error handling을 보안 도구에 적용하기 | rust | rust-error-handling-for-security-tools |
| 2026-08-03 | AI agent 결과를 schema로 검증하기 | validate-ai-agent-results-with-schema | Rust logging/tracing 기초 | rust | rust-logging-and-tracing-basics |
| 2026-08-04 | agent output contract 설계 | agent-output-contract-design | Rust CLI config 파일 처리 | rust | rust-cli-config-file-handling |
| 2026-08-05 | eval dataset을 작게 시작하는 방법 | start-small-with-eval-datasets | Rust로 JSON 로그 파서 만들기 | rust | rust-json-log-parser |
| 2026-08-06 | agent 작업 샘플링 리뷰 운영 | sampling-review-for-agent-work | Rust로 YARA 결과 요약 도구 만들기 | rust | rust-yara-result-summary-tool |
| 2026-08-07 | AI agent가 외부 링크를 쓸 때 검증 기준 | verification-rules-for-external-links-used-by-ai-agents | YARA 룰 작성 입문: 샘플 특징에서 규칙까지 | security-engineering | yara-rule-writing-from-sample-features |
| 2026-08-08 | AI agent와 supply chain 보안 연결 | connect-ai-agents-and-supply-chain-security | Sigma rule 입문: 로그 탐지 규칙 읽기 | security-engineering | sigma-rule-basics-for-log-detection |
| 2026-08-09 | LLM 앱 OWASP Top 10을 개발자 관점에서 보기 | owasp-llm-top-10-for-developers | EDR alert를 기술 블로그 글감으로 바꾸는 법 | security-engineering | turn-edr-alerts-into-technical-blog-topics |
| 2026-08-10 | prompt injection 대응을 코드로 고정하기 | encode-prompt-injection-mitigations-in-code | phishing kit 트렌드를 안전하게 분석하는 방법 | security-engineering | safely-analyze-phishing-kit-trends |
| 2026-08-11 | agentic workflow에서 untrusted input 다루기 | handle-untrusted-input-in-agentic-workflows | 계정 탈취와 MFA fatigue 공격 흐름 | security-engineering | account-takeover-and-mfa-fatigue-flow |
| 2026-08-12 | RAG 문서 오염과 source validation | rag-document-poisoning-and-source-validation | OAuth 앱 권한 검토 체크리스트 | security-engineering | oauth-app-permission-review-checklist |
| 2026-08-13 | AI agent 권한 최소화 checklist | ai-agent-least-privilege-checklist | SaaS audit log에서 봐야 할 필드 | security-engineering | fields-to-check-in-saas-audit-logs |
| 2026-08-14 | AI agent 운영 정책 샘플 문서 | sample-ai-agent-operations-policy | cloud storage 공개 노출 점검 | security-engineering | cloud-storage-public-exposure-checks |
| 2026-08-15 | agent 보안/운영 FAQ 허브 글 | ai-agent-security-operations-faq-hub | incident timeline 작성법 | security-engineering | how-to-write-an-incident-timeline |
| 2026-08-16 | AI 에이전트 운영 시리즈 정리 | ai-agent-operations-series-wrap-up | 보안 엔지니어링 시리즈 정리 | security-engineering | security-engineering-series-wrap-up |

## Post-8-Week Extension: Secure Coding and AI-Assisted Secure Coding

이 확장 계획은 2026-08-16까지의 8주 캘린더가 끝난 뒤에 이어 붙인다. 8주 안의 발행 순서나 주제는 바꾸지 않는다.

- 목적: `보안 엔지니어링` 허브를 인프라/공급망 보안에서 애플리케이션 secure coding까지 확장한다.
- 위치: `section: security`, `topic_key: security-engineering`
- 권장 시리즈명: `Secure Coding with AI`
- 기본 태그: `[security, secure-coding, code-review, devsecops]`
- AI 보조 코딩 글 추가 태그: `ai-security`, `ai-assisted-coding`, `llm`, `secure-code-review`
- 기준 출처: OWASP ASVS, OWASP Top 10, OWASP Cheat Sheet Series, OWASP Secure Coding Practices, NIST SSDF SP 800-218
- 작성 원칙: AI가 안전한 코드를 "만들었다"고 단정하지 않고, 어떤 요구사항을 prompt/checklist/test로 고정했고 어떤 취약점 범위를 직접 점검했는지 분리해서 쓴다.

### Candidate Sequence

| Order | Topic | Slug |
| --- | --- | --- |
| 1 | AI에게 안전한 코드를 요청할 때 prompt에 넣어야 할 것 | prompt-ai-to-write-safer-code |
| 2 | 내가 만든 코드가 안전한지 점검하는 첫 체크리스트 | first-checklist-for-reviewing-code-security |
| 3 | OWASP Top 10을 코드 리뷰 질문으로 바꾸기 | turn-owasp-top-10-into-code-review-questions |
| 4 | 입력 검증과 output encoding을 AI 코드 리뷰로 확인하기 | review-input-validation-and-output-encoding-with-ai |
| 5 | 인증/인가 버그를 AI가 놓치지 않게 만드는 방법 | help-ai-review-authentication-and-authorization |
| 6 | SQL injection과 command injection을 테스트 케이스로 막기 | prevent-injection-with-security-test-cases |
| 7 | secret, token, API key가 코드와 로그에 새는지 점검하기 | check-secret-token-api-key-leaks-in-code-and-logs |
| 8 | dependency 취약점을 AI 설명이 아니라 도구 결과로 검증하기 | verify-dependency-vulnerabilities-with-tools-not-ai |
| 9 | 안전한 error handling과 logging 기준 만들기 | secure-error-handling-and-logging-criteria |
| 10 | AI 코드 리뷰 결과를 사람이 다시 검증하는 절차 | human-verification-for-ai-code-review-results |
| 11 | Rust 코드에서 panic, path traversal, unsafe 사용 점검하기 | review-rust-panic-path-traversal-and-unsafe |
| 12 | 웹 API 보안 체크: 인증, rate limit, CORS, schema validation | web-api-security-check-auth-rate-limit-cors-schema |
| 13 | SAST 결과를 false positive와 실제 위험으로 나누기 | triage-sast-results-false-positive-vs-real-risk |
| 14 | secure coding Definition of Done 만들기 | secure-coding-definition-of-done |

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
- 일일 2주제 발행 정책을 주간 또는 격일 발행으로 바꾸는 경우
