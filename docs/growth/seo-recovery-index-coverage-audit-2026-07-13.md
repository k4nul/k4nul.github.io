# SEO Recovery Index Coverage Audit — 2026-07-13

Source data: Google Search Console Coverage drilldown exports received on 2026-07-13, plus local Jekyll build inspection from the isolated `seo-recovery-20260713` worktree.

## Summary

- Files changed by this audit: this report, the companion CSV, and `_pages/en-contact.md`.
- No pages were deleted, no sitewide noindex was added, and no redirect mapping was changed.
- The strongest index finding remains: many sitemap URLs are discovered but not crawled/indexed, while the live technical checks are mostly valid.

### Counts by GSC issue
- 발견됨 - 현재 색인이 생성되지 않음: 79
- Soft 404: 1
- 리디렉션이 포함된 페이지: 4
- ‘NOINDEX’ 태그에 의해 제외되었습니다.: 7
- 크롤링됨 - 현재 색인이 생성되지 않음: 4
- 적절한 표준 태그가 포함된 대체 페이지: 8

### Counts by recommended action
- Improve: 80
- Review: 5
- Fix: 1
- Keep/monitor: 17

### Counts by priority
- P0: 1
- P1: 80
- P2: 5
- P3: 17

## P0/P1 URLs

| Priority | Action | Issue | URL | 3mo clicks | 3mo impressions | Reason |
|---|---|---|---|---:|---:|---|
| P0 | Fix | Soft 404 | https://www.k4nul.com/en/contact/ |  |  | GSC marks as Soft 404; original page was thin and should be strengthened or intentionally noindexed. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/ai/approval-boundaries-and-guardrails/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/ai/build-and-test-are-not-enough-to-validate-an-agent/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/ai/fix-claude-code-boundaries-with-settings-and-permissions/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/ai/from-document-centered-ops-to-observable-harness/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/ai/from-principles-to-enforcement/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/ai/from-prose-to-schema-turning-handoff-into-a-contract/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/ai/how-token-management-strategies-differ-between-codex-and-claude-code/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/ai/multi-agent-is-not-the-default/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/ai/prompt-injection-as-a-harness-problem/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/ai/split-instructions-with-rules-and-skills/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/ai/standardize-codex-workflows-with-skills/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/ai/use-claude-code-with-agents-md/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/ai/why-everything-claude-code-is-trending/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/docker-containers-vs-vms/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/docker-registry-push-and-image-management/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/dockerfile-basics-and-build-context/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/git-pr-mr-collaboration-review/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/git-rebase-squash-force-push/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/git-records-and-boundaries/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/git-tags-releases-docker-image-versions/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/jenkins-freestyle-job-vs-pipeline/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/jenkins-plugins-credentials-tools-management/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/jenkins-to-kubernetes-deployment-boundary/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/jenkins-what-and-why-still-used/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/jenkinsfile-agent-stages-steps-post/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/kubernetes-first-manifests-pod-deployment-service/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/kubernetes-kubeadm-installation-strategy-on-prem/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/devops/kubernetes-what-it-solves-and-does-not/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/ai/approval-boundaries-and-guardrails/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/ai/build-and-test-are-not-enough-to-validate-an-agent/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/ai/from-prose-to-schema-turning-handoff-into-a-contract/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/ai/how-to-write-first-codex-task-request/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/ai/multi-agent-is-not-the-default/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/ai/prompt-injection-as-a-harness-problem/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/ai/what-should-agent-trace-record/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/ai/why-do-results-change-when-you-switch-ai-coding-tools/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/development/rust/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/docker-registry-push-and-image-management/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/git-conflict-resolution-basics/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/git-rebase-squash-force-push/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/git-remote-fetch-pull-push/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/git-tags-releases-docker-image-versions/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/jenkins-declarative-pipeline-introduction/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/jenkins-freestyle-job-vs-pipeline/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/jenkins-to-kubernetes-deployment-boundary/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/jenkins-what-and-why-still-used/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/jenkinsfile-agent-stages-steps-post/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/kubernetes-configmap-secret-ingress-manifests/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/kubernetes-control-plane-install-basic-checks/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/kubernetes-first-manifests-pod-deployment-service/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/kubernetes-kubeadm-installation-strategy-on-prem/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/kubernetes-pod-deployment-replicaset-service/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/kubernetes-pv-pvc-storageclass-basics/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/kubernetes-requests-limits-probes/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/kubernetes-troubleshooting-describe-events-logs/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/kubernetes-what-it-solves-and-does-not/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/rust/build-a-small-cli-project/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/rust/debugging-with-rust-analyzer-and-codelldb/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/rust/generics-error-handling-closures-and-iterators/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/rust/install-rust-and-run-hello-world/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/rust/serde-with-json-and-toml-basics/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/rust/structs-enums-pattern-matching-and-traits/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/rust/testing-in-rust/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/rust/variables-types-control-flow-and-functions/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/rust/vec-string-str-and-hashmap-basics/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/security/kubernetes-rbac-least-privilege-basics/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/rust/rust-build-a-small-cli-project/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/rust/rust-crates-packages-project-layout/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/rust/rust-debugging-with-rust-analyzer/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/rust/rust-file-io-and-cli-input/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/rust/rust-install-hello-world/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/rust/rust-modules-smart-pointers-concurrency-async/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/rust/rust-testing-basics/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/rust/rust-variables-types-control-flow-functions/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/rust/rust-vec-string-str-hashmap/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 발견됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/security/kubernetes-rbac-least-privilege-basics/ |  |  | Sitemap URL is discovered but not crawled; strengthen internal links and prioritize only core pages. |
| P1 | Improve | 크롤링됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/ai/handle-logs-issues-and-auto-memory-with-context-budget/ | 0 | 2 | Google crawled the page but did not index it; likely quality, duplication, or search-intent weakness. |
| P1 | Improve | 크롤링됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/devops/docker-images-layers-tags-digests/ | 0 | 2 | Google crawled the page but did not index it; likely quality, duplication, or search-intent weakness. |
| P1 | Improve | 크롤링됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/en/rust/crates-packages-and-project-layout/ |  |  | Google crawled the page but did not index it; likely quality, duplication, or search-intent weakness. |
| P1 | Improve | 크롤링됨 - 현재 색인이 생성되지 않음 | https://www.k4nul.com/rust/rust-generics-error-handling-closures-iterators/ |  |  | Google crawled the page but did not index it; likely quality, duplication, or search-intent weakness. |

## Proposed batches

### CONTENT CLEANUP BATCH 01 — Soft 404

- URL: `https://www.k4nul.com/en/contact/`
- Problem: GSC reported Soft 404; original page had only two short paragraphs and little standalone value.
- Change made locally: expanded the page with contact channels, valid inquiry types, what to include, and sensitive-data handling guidance.
- Risk: exposes the same public email/GitHub already present in the Korean contact page; no secret or private identifier added.
- Rollback: restore `_pages/en-contact.md` from the previous commit.

### CONTENT AUDIT BATCH 02 — Crawled but not indexed

- `https://www.k4nul.com/en/devops/docker-images-layers-tags-digests/` — Improve (P1): Google crawled the page but did not index it; likely quality, duplication, or search-intent weakness.
- `https://www.k4nul.com/en/rust/crates-packages-and-project-layout/` — Improve (P1): Google crawled the page but did not index it; likely quality, duplication, or search-intent weakness.
- `https://www.k4nul.com/rust/rust-generics-error-handling-closures-iterators/` — Improve (P1): Google crawled the page but did not index it; likely quality, duplication, or search-intent weakness.
- `https://www.k4nul.com/ai/handle-logs-issues-and-auto-memory-with-context-budget/` — Improve (P1): Google crawled the page but did not index it; likely quality, duplication, or search-intent weakness.

### CONTENT AUDIT BATCH 03 — Discovered but not indexed

Treat these as crawl-priority/content-quality candidates, not deletion candidates. Prioritize only core AI/DevOps/Rust pages with existing impressions or strong topical importance.

## Rollback

- Restore `_pages/en-contact.md` from `origin/master` or revert the eventual commit.
- Remove `docs/growth/seo-recovery-index-coverage-audit-2026-07-13.*` if the audit artifacts should not be published.

## Full inventory

See `docs/growth/seo-recovery-index-coverage-audit-2026-07-13.csv`.
