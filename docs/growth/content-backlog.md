# Content Backlog

검증 기준일: 2026-06-01

상태 값:

- `candidate`: 예약 글 보강, 공개 글 리라이트, 또는 예외적 신규 작성 후보.
- `needs-data`: Search Console/GA4 데이터가 있어야 우선순위 판단 가능.
- `ready`: 다음 작업으로 바로 착수 가능.
- `defer`: 지금은 보류.

운영 원칙:

- 기본적으로 새 글을 만들지 않고 `scheduled-posts-inventory.md`의 예약 포스팅을 우선 활용한다.
- 예약 큐에 없는 핵심 템플릿이 필요하거나, Search Console상 새 reference page가 필요하거나, 사용자가 명시적으로 요청할 때만 신규 글을 후보로 둔다.
- 미래 포스트의 publish date, slug, permalink는 임의로 바꾸지 않는다. 일정 변경은 `schedule-adjustment-candidates.md`에 후보로만 기록한다.
- 공개 페이지에는 이미 공개된 글과 오늘 실제 공개된 글만 직접 링크한다.

## Monthly Review Snapshot: 2026-06-01

### Data Availability

| 항목 | 상태 | 메모 |
| --- | --- | --- |
| Search Console impressions/clicks/CTR/average position | 사용자 입력 필요 | 레포 내 월간 입력값 없음 |
| non-brand query 수 | 사용자 입력 필요 | 레포 내 월간 입력값 없음 |
| 평균 순위 30위 안쪽 페이지 수 | 사용자 입력 필요 | 레포 내 월간 입력값 없음 |
| GA4 organic/direct sessions | 사용자 입력 필요 | 레포 내 월간 입력값 없음 |
| 월간 사용자 수 | 사용자 입력 필요 | 추정 금지 |

### Queue Balance And Coverage Notes

- future queue는 `130 posts / 65 KR/EN pairs`로 언어 균형은 유지된다.
- `2026-06`과 `2026-07`은 trace, guardrail, RBAC, prompt injection, least privilege, MCP처럼 AI agent 운영·보안 축이 강하다.
- `2026-08`은 첫 주 incident/security pair 뒤에 Rust/Tauri 중심으로 이동하고, `2026-09~2026-10`은 대부분 Rust/DevOps라 핵심 AI 축 밀도가 약해진다.
- `2026-06-01~2027-04-30` 큐 스냅샷에는 exact `AGENTS.md`, `CLAUDE.md`, Codex 운영 템플릿 리프레시 블록이 뚜렷하지 않다. 다음 달 보강은 새 글 양산이나 일정 변경보다 템플릿/체크리스트와 evergreen 리라이트 쪽이 우선이다.

### Stale Evergreen Watchlist

| 공개일 | 후보 | 상태 | 이유 |
| --- | --- | --- | --- |
| 2026-04-21 | `why-agents-md-claude-md-and-system-prompts-burn-tokens` KR/EN pair | candidate | instruction-file 핵심축이지만 1개월 이상 경과. `AGENTS.md`/`CLAUDE.md` 템플릿과 내부링크 재점검 후보 |
| 2026-04-30 | `how-to-write-agents-md-for-codex` KR/EN pair | candidate | AGENTS.md long-tail evergreen. exact future queue 보강 부재를 메울 공개 글 후보 |
| 2026-05-06 | `codex-project-operations-template` KR/EN pair | candidate | Codex 운영 템플릿 축의 대표 공개 글. 템플릿 허브 연결 강화 후보 |
| 2026-05-11 | `fix-claude-code-boundaries-with-settings-and-permissions` | candidate | permissions/settings 핵심축 공개 글. KR-only 자산이라 KR/EN 및 template 연결 감사 후보 |
| 2026-05-12 | `automate-validation-and-guardrails-with-hooks` | candidate | hooks/validation evergreen이지만 future queue 직접 후속이 얕다 |
| 2026-05-13 | `connect-external-context-with-mcp` | candidate | MCP 핵심축 공개 글. 2026-07-14 MCP pair와 연결할 대표 evergreen 후보 |

### Next-Month Top 5 Priorities

| 우선순위 | 항목 | 상태 | 메모 |
| --- | --- | --- | --- |
| 1 | `2026-06-16`, `2026-06-23`, `2026-06-25`, `2026-06-30`, `2026-07-14` KR/EN pair의 post-publish 링크와 EN 품질 점검 | ready | AI core axis와 직접 연결되는 다음 달 공개 묶음 |
| 2 | `/ai-engineering/templates/`에서 `AGENTS.md` 최소 템플릿, `CLAUDE.md` 최소 템플릿, Codex 작업 요청 프롬프트를 우선 보강 | ready | future queue의 exact template refresh 공백 보완 |
| 3 | stale evergreen shortlist의 title, description, TL;DR, hub/template/internal link 감사 | candidate | Search Console 입력 전에는 좁은 범위 감사만 허용 |
| 4 | 기존 EN AI Engineering pages와 schedule-adjustment 문서의 EN rewrite candidates를 묶어 KR/EN parity 감사 | candidate | 삭제 없이 self-canonical, hreflang, parity 유지 |
| 5 | Search Console/GA4 월간 입력값 수집 후 Week 4 또는 월간 rewrite prompt로 넘길 page/query 표 준비 | needs-data | 수치 추정 금지, mass title change 금지 |

## Hub Candidates

| 후보 | 상태 | 목적 | 우선 확인 |
| --- | --- | --- | --- |
| AI Coding Agent 운영 허브 | candidate | Codex/Claude Code를 작업 수행 agent로 운영하는 글 묶기 | 기존 `/ai-engineering/`과 중복 여부 |
| Instruction Files 허브 | candidate | `AGENTS.md`, `CLAUDE.md`, system prompt, rules/skills 경계 묶기 | 관련 글 수와 cannibalization |
| AI Agent Security 허브 | candidate | MCP, permissions/settings, prompt injection, secret 노출, hook guardrail 묶기 | 보안 글과 AI 글 사이 내부링크 |
| Agent Verification 허브 | candidate | build/test, trace, handoff, checklist, reviewer 기준 묶기 | 검증 관련 글의 평균 순위 |

## Template Candidates

| 후보 | 상태 | 연결 허브 |
| --- | --- | --- |
| AGENTS.md 최소 템플릿 | ready | `/ai-engineering/templates/` |
| CLAUDE.md 최소 템플릿 | ready | `/ai-engineering/templates/` |
| Codex 작업 요청 프롬프트 템플릿 | ready | `/ai-engineering/templates/` |
| Claude Code hooks 예제 | candidate | AI Agent Security 허브 |
| MCP permissions/settings 보안 체크리스트 | candidate | AI Agent Security 허브 |
| AI agent 작업 결과 리뷰 체크리스트 | ready | Agent Verification 허브 |
| token/context 관리 체크리스트 | candidate | AI Coding Agent 운영 허브 |

## Long-Tail Search Candidates

| 후보 | 상태 | 메모 |
| --- | --- | --- |
| AGENTS.md는 왜 짧게 써야 할까 | candidate | 기존 글이 있으면 리라이트 우선 |
| CLAUDE.md와 system prompt는 무엇이 다를까 | candidate | instruction file 허브 후보와 연결 |
| Codex 프로젝트에서 AGENTS.md를 어떻게 구성해야 할까 | candidate | 템플릿 페이지와 연결 |
| Claude Code hooks로 무엇을 자동화해야 할까 | candidate | hook guardrail과 build/test 자동화 분리 |
| Claude Code permissions/settings는 어디까지 막아야 할까 | candidate | 보안/검증 허브 연결 |
| MCP tool을 coding agent에 붙일 때 보안상 무엇을 조심해야 할까 | candidate | 데이터 노출, 인증 주체, allowlist 중심 |
| AI coding agent의 결과를 어떻게 검증해야 할까 | candidate | review checklist와 연결 |
| 토큰 관리가 AI agent 품질에 영향을 주는 이유 | candidate | token/context series와 연결 |
| prompt injection이 coding agent에서 위험한 이유 | candidate | 보안 허브 후보 |
| AI agent가 파일을 수정하기 전에 확인해야 할 체크리스트 | candidate | Codex prompt template과 연결 |

## Security And Verification Candidates

| 후보 | 상태 | 메모 |
| --- | --- | --- |
| MCP tool allowlist 설계 기준 | candidate | permissions/settings 체크리스트와 연결 |
| Agent 작업 전 secret 노출 점검 | candidate | Security/DevOps 글과 연결 가능 |
| Hook으로 막아야 하는 위험 명령 | candidate | Claude Code hooks 예제와 연결 |
| Build/test 이후 사람이 봐야 하는 diff 기준 | ready | agent review checklist와 연결 |
| Prompt injection을 coding agent 하네스 문제로 보는 법 | candidate | AI Agent Security 허브 후보 |

## Experiment/Postmortem Candidates

| 후보 | 상태 | 메모 |
| --- | --- | --- |
| Codex가 블로그 레포를 잘못 수정한 사례와 방지책 | candidate | 실제 사례가 없으면 가정으로 쓰지 않는다 |
| AGENTS.md가 길어졌을 때 발생한 문제 | candidate | 직접 관찰 또는 재현이 필요 |
| Claude Code hooks로 검증을 자동화하면서 생긴 실패 사례 | needs-data | 실제 hooks 실험 필요 |
| AI agent 작업 결과를 사람이 리뷰해야 하는 기준 | ready | 체크리스트 기반으로 작성 가능 |
| MCP tool allowlist를 잘못 잡았을 때의 위험 | needs-data | 실제 설정 또는 문서 근거 필요 |

## Recovery Follow-Up Candidates: 2026-05-25

아래 항목은 신규 글 작성 후보가 아니라, 운영 공백 복구 이후 예약 큐와 공개 글을 계속 관리하기 위한 후보이다.

| 후보 | 상태 | 메모 |
| --- | --- | --- |
| Jenkins 02-10 KR/EN post-publish 처리 | ready | 2026-05-26~2026-06-03 발행 후 DevOps 허브에 실제 공개 글만 추가 |
| Kubernetes 01-05 KR/EN pre-publish 재확인 | ready | 2026-06-04~2026-06-08 발행 전 링크와 검증 한계 재확인 |
| K8S 06-10 KR/EN 내부링크 보강 | candidate | 2026-06-09~2026-06-13 예약 글, 아직 이번 14일 범위 밖 일부 포함 |
| 2026-06-16 agent trace KR/EN 품질 점검 | candidate | AI agent verification 핵심축, `/ai-engineering/`와 `/start-here/` 연결 후보 |
| Git/Jenkins 제목 검색 의도 보강 | needs-data | 전체 제목 대량 변경 금지. Search Console 또는 scoped prompt 필요 |

## KR/EN Priority Candidates

아래 목록은 신규 영어판 생성 후보가 아니라, 기존 영어판 유지, 리라이트, canonical/hreflang/link 보강, 또는 핵심축 KR/EN 병행 발행 우선순위다. 기존 영어판은 삭제하거나 폐기하지 않는다.

| 우선순위 | 후보 | 기본 작업 | 조건 |
| --- | --- | --- | --- |
| 1 | AGENTS.md template | KR/EN 병행 발행 또는 기존 EN 리라이트 | template/checklist 핵심축 |
| 1 | CLAUDE.md template | KR/EN 병행 발행 또는 기존 EN 리라이트 | `CLAUDE.md` 관련 핵심축 |
| 1 | Codex prompt template | KR/EN 병행 발행 또는 기존 EN 리라이트 | Codex prompt/template 핵심축 |
| 2 | Claude Code hooks example | KR/EN 병행 발행 또는 기존 EN 리라이트 | hooks/security 핵심축 |
| 2 | MCP security checklist | KR/EN 병행 발행 또는 기존 EN 리라이트 | MCP security/permissions 핵심축 |
| 2 | AI agent review checklist | KR/EN 병행 발행 또는 기존 EN 리라이트 | validation/review 핵심축 |
| 3 | Existing English AI Engineering pages | canonical/hreflang/link 감사 후 리라이트 후보 표시 | 기존 EN 유지 |
| 4 | Rust/DevOps general posts | 한국어 우선, agent 운영/보안과 직접 연결될 때만 EN 보강 | 비핵심축 |
