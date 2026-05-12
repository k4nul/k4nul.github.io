# K4NUL Growth Goals

검증 기준일: 2026-05-13

## Positioning

K4NUL은 단순 포스팅 블로그가 아니라 `AI coding agent 운영`, `검증`, `보안`에 대한 한국어 실무형 지식베이스로 성장한다. 중심축은 Codex, Claude Code, `AGENTS.md`, `CLAUDE.md`, hooks, MCP, permissions/settings, token/context management, AI agent validation, AI agent security다.

Rust, DevOps, Security 글은 독립 주제로 보존하되, 가능한 경우 agent 운영, 검증, 자동화, 권한 경계, 공급망 보안, 재현 가능한 실험과 연결한다.

## 30일 목표

- `/ai-engineering/`, `/start-here/`, `/ai-engineering/templates/` 주요 허브 페이지의 색인 안정화.
- Search Console 기준 non-brand query 증가 시작.
- `AGENTS.md`, `CLAUDE.md`, Codex, Claude Code, hooks 관련 검색어 노출 발생.
- 주요 글 10개 이상에 허브, 템플릿, 관련 글 내부링크 추가.
- 새 글 양산보다 예약 포스팅 큐의 발행 전 점검, 기존 글 리라이트, 내부링크 개선을 우선.

## 90일 목표

- Organic Search가 Direct와 비슷하거나 더 커지는 구조 만들기.
- 평균 순위 30위 안쪽에 들어오는 페이지 10개 이상 확보.
- `AGENTS.md`, `CLAUDE.md`, Codex, Claude Code 관련 long-tail query 확보.
- 템플릿 페이지 5개 이상 운영.
- 월간 사용자 수를 현재 기준 대비 보수적으로 2-3배 성장시키는 것을 목표로 함.

## 180일 목표

- 보수적 목표: 월간 사용자 500-1,000명대 진입.
- 공격적 목표: 월간 사용자 2,000-5,000명대 진입.
- K4NUL을 `AI coding agent 운영·검증·보안` 한국어 long-tail 검색에서 인지되는 블로그로 만든다.
- 기존 영어판은 유지하고, canonical/hreflang/link 문제가 있는 영어판을 우선 보정한다.
- 핵심축 콘텐츠는 KR/EN 병행 발행과 보강을 기본으로 하되, 투자는 reference, template, checklist, how-to 페이지에 우선 배분한다.

## Conservative And Aggressive Targets

- 보수적 운영: 주 1개 예약 long-tail 글 발행 전 점검, 주 1-2개 기존 공개 글 리라이트, 주 1개 템플릿/체크리스트 보강.
- 공격적 운영: Search Console에서 노출이 확인된 주제만 추가 보강하고, 허브와 템플릿을 중심으로 내부링크를 촘촘히 연결.
- 신규 글은 기본 운영 작업이 아니다. 예약 큐에 없는 핵심 템플릿, Search Console상 새 reference page 필요, 사용자 명시 요청일 때만 예외로 한다.
- 금지: 현재 레포에 없는 Search Console, GA4 수치를 추정해 목표 달성률로 쓰지 않는다.

## Why Search Console Comes Before GA4

- Search Console은 검색어, 페이지, 노출, CTR, 평균 순위를 보여주므로 long-tail topic이 실제로 검색에 잡히는지 판단하기 좋다.
- GA4 이벤트와 engaged sessions는 사이트 안에서의 행동을 보는 데 유용하지만, 검색 수요가 생겼는지 직접 보여주지는 않는다.
- 발행량을 줄인 뒤 GA4 이벤트와 트래픽이 감소했더라도, 복구 판단은 먼저 Search Console에서 `노출이 생기는 쿼리`, `30위 안쪽 페이지`, `CTR 낮은 페이지`를 보고 한다.
- Analytics 데이터가 레포에 없으면 수치를 추정하지 않고, 사용자가 Search Console 또는 GA4에서 직접 입력해야 하는 값으로 문서화한다.

## KPI

- Search Console: impressions, clicks, CTR, average position, non-brand queries, indexed pages.
- GA4: organic landing pages, engaged sessions, organic sessions, page views.
- Content operations: 리라이트한 기존 글 수, 내부링크 추가 글 수, 템플릿/체크리스트 수, 허브에 연결된 글 수.
- Scheduled queue operations: 발행 전 점검한 예약 글 수, 발행 후 허브에 반영한 글 수, 일정 변경 후보로만 기록한 글 수.
- Quality: 검증 기준일/버전 명시율, 공식 문서 또는 직접 재현 근거 연결률, 언어별 self-canonical 여부, 대응되는 KR/EN pair의 hreflang 보존 여부.

## User-Provided Data Slots

아래 값은 레포에서 확인하지 못하면 추정하지 않는다. 매주 일요일 또는 월간 리뷰 때 사용자가 Search Console/GA4에서 입력한다.

| 항목 | 입력값 | 기간 |
| --- | --- | --- |
| 월간 사용자 | 사용자 입력 필요 | 최근 28일 또는 월간 |
| Organic Search sessions | 사용자 입력 필요 | 최근 28일 또는 월간 |
| Direct sessions | 사용자 입력 필요 | 최근 28일 또는 월간 |
| AI Engineering impressions | 사용자 입력 필요 | 최근 28일 |
| AI Engineering clicks | 사용자 입력 필요 | 최근 28일 |
| non-brand query 수 | 사용자 입력 필요 | 최근 28일 |
| 평균 순위 30위 안쪽 페이지 수 | 사용자 입력 필요 | 최근 28일 |
