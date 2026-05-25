# Content Backlog

검증 기준일: 2026-05-25

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
