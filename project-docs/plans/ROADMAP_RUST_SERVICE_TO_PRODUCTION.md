# Rust Service to Production Roadmap

## Snapshot

- Verification date: 2026-05-04 KST
- Purpose: plan the next Rust track after the Tauri follow-up block.
- Current state: 30 Korean posts and 30 English mirror posts have been created under `_posts/`.
- Schedule position: starts after `2026-09-15-rust-tauri-first-local-tool`, on the next Tuesday, `2026-09-22`.
- Publishing unit: one topic per week. Korean and English mirrors share the same date and `translation_key`.
- Recommended structure: `section: development`, `topic_key: rust`, `track: rust`, `categories: Rust`.
- Series title: `Rust Service to Production`

## Positioning

This curriculum connects the earlier Rust language track with the Docker, CI/CD, Kubernetes, security, and observability tracks. The target reader has already seen Rust basics, Docker/Git/Jenkins/Kubernetes basics, and the Tauri follow-up block. The goal is to carry one Rust API service from project boundary to production readiness.

The posts are intentionally drafted as operational scaffolds. Before each actual publication date, the post should be expanded with a concrete example repository, command output, versions, failure logs, and any official-documentation changes.

## Calendar

| Week | Date | Topic | Slug |
| --- | --- | --- | --- |
| 1 | 2026-09-22 | Rust service production boundary | rust-service-production-boundary |
| 2 | 2026-09-29 | Minimal API server with Axum | rust-axum-minimal-api-server |
| 3 | 2026-10-06 | Rust Axum API project structure | rust-axum-project-structure |
| 4 | 2026-10-13 | Request and response types with serde | rust-api-request-response-serde |
| 5 | 2026-10-20 | Consistent API error responses | rust-api-consistent-error-response |
| 6 | 2026-10-27 | Configuration and environment separation | rust-api-configuration-environment |
| 7 | 2026-11-03 | Structured logging with tracing | rust-api-structured-logging-tracing |
| 8 | 2026-11-10 | Input validation and bad requests | rust-api-input-validation-bad-requests |
| 9 | 2026-11-17 | SQLx database storage | rust-api-sqlx-database-storage |
| 10 | 2026-11-24 | SQLx migrations and query checks | rust-api-sqlx-migrations-query-checks |
| 11 | 2026-12-01 | Repository and service boundaries | rust-api-repository-service-boundaries |
| 12 | 2026-12-08 | Unit and integration tests for APIs | rust-api-unit-and-integration-tests |
| 13 | 2026-12-15 | Session and JWT boundaries before auth | rust-api-session-jwt-boundaries |
| 14 | 2026-12-22 | CORS, rate limit, and request size defaults | rust-api-cors-rate-limit-request-size |
| 15 | 2026-12-29 | Docker multi-stage Rust API image | rust-api-docker-multistage-build |
| 16 | 2027-01-05 | `.dockerignore`, build cache, and image size | rust-api-dockerignore-cache-image-size |
| 17 | 2027-01-12 | GitHub Actions CI for Rust API | rust-api-github-actions-ci |
| 18 | 2027-01-19 | Release tags and Docker image tags | rust-api-release-tags-docker-image-tags |
| 19 | 2027-01-26 | SBOM and image scan results | rust-api-sbom-image-scan-results |
| 20 | 2027-02-02 | Kubernetes Deployment and Service | rust-api-kubernetes-deployment-service |
| 21 | 2027-02-09 | ConfigMap, Secret, and env injection | rust-api-kubernetes-configmap-secret-env |
| 22 | 2027-02-16 | Kubernetes probes and resource limits | rust-api-kubernetes-probes-resources |
| 23 | 2027-02-23 | Ingress and TLS boundaries | rust-api-kubernetes-ingress-tls |
| 24 | 2027-03-02 | Rollout, rollback, and runbooks | rust-api-rollout-rollback-runbook |
| 25 | 2027-03-09 | OpenTelemetry logs, metrics, and traces | rust-api-opentelemetry-logs-metrics-traces |
| 26 | 2027-03-16 | Prometheus metric design | rust-api-prometheus-metrics-design |
| 27 | 2027-03-23 | Kubernetes failure debugging | rust-api-kubernetes-failure-debugging |
| 28 | 2027-03-30 | Non-root container security | rust-api-non-root-container-security |
| 29 | 2027-04-06 | Kubernetes RBAC for service operations | rust-api-kubernetes-rbac-service-operations |
| 30 | 2027-04-13 | Production readiness checklist | rust-api-production-readiness-checklist |

## Source Baseline

- Axum and tower-http documentation for routing, handlers, extractors, responses, state, middleware, CORS, tracing, and request limits.
- SQLx documentation for pools, migrations, query macros, and database verification.
- Docker Build documentation for multi-stage builds, build context, build cache, and image construction.
- GitHub Actions documentation for workflow syntax and secure use.
- Kubernetes documentation for Deployment, Service, ConfigMap, Secret, probes, resources, Ingress, rollout, logging, debugging, security context, ServiceAccount, and RBAC.
- OpenTelemetry and Prometheus documentation for collector deployment, metrics, traces, and metric type choices.
- OWASP cheat sheets for input validation, error handling, CORS, session management, and JWT boundaries.

## Publication Expansion Checklist

- Add a concrete example repository path or code listing.
- Record `rustc`, `cargo`, dependency, Docker, Kubernetes, and CI versions relevant to the post.
- Include at least one local command and its observed result when the topic is executable.
- Include at least one failure mode and how it appears in logs, HTTP response, CI output, or Kubernetes events.
- Re-check official documentation links and option names at publication time.
- Keep Korean and English mirrors aligned through the same `translation_key`.

## Update Triggers

- Axum, SQLx, Docker, GitHub Actions, Kubernetes, OpenTelemetry, or Prometheus documentation changes in a way that affects examples.
- The actual publication cadence changes from weekly Tuesday KOR/ENG pairs.
- The series gains a companion example repository or changes its example application scope.
- The Rust track navigation or Start Here track begins surfacing these posts explicitly.
