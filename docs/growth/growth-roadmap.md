# Growth Roadmap

검증 기준일: 2026-05-13

## Today

- 레포 구조를 확인하고 블로그 엔진, 글/페이지 디렉터리, build/test 명령, sitemap/robots/canonical/hreflang/RSS 처리 방식을 기록한다.
- `docs/growth/` 운영 문서 세트를 만든다.
- 예약 포스팅 큐를 `scheduled-posts-inventory.md`와 `scheduled-posts-calendar.md`로 관리한다.
- 루트 `AGENTS.md`에 매일 Codex 운영 원칙, URL 보존, 수치 추정 금지, 완료 보고 형식을 반영한다.
- `/ai-engineering/`, `/start-here/`, `/ai-engineering/templates/`가 존재하는지 확인한다.
- 빌드를 실행하고 실패 시 정확한 파일/플러그인/오류를 기록한다.

## This Week

- 주요 허브 3개를 고정한다: `/ai-engineering/`, `/start-here/`, `/ai-engineering/templates/`.
- 기존 AI agent 관련 글 10개 이상을 후보로 뽑고 허브/템플릿/관련 글 내부링크 상태를 점검한다.
- 새 글은 기본적으로 만들지 않고, 이번 주 예약 발행 글과 기존 공개 글의 리라이트/내부링크 개선을 우선한다.
- Search Console 데이터가 제공되면 쿼리별 액션을 `search-console-decision-rules.md`에 따라 정한다.

## Week 2

- 템플릿 자산을 2개 이상 보강한다.
- 후보: `AGENTS.md` 최소 템플릿, `CLAUDE.md` 최소 템플릿, Codex 작업 요청 프롬프트, Claude Code hooks 예제, MCP permissions/settings 보안 체크리스트.
- 템플릿 페이지는 복사 가능한 문구보다 적용 조건, 금지 사항, 검증 방법을 함께 둔다.
- 템플릿/체크리스트/reference/how-to 성격의 핵심축 글은 KR/EN 병행 발행을 기본으로 하되, 기존 영어판이 있으면 삭제하지 않고 canonical, hreflang, 링크, 품질을 먼저 점검한다.

## Week 3

- 예약 큐에 있는 long-tail 검색 글 또는 기존 공개 글을 long-tail 의도에 맞게 리라이트한다.
- 후보 축: `AGENTS.md`, `CLAUDE.md`, Codex, Claude Code, hooks, MCP, token/context, validation, security.
- 제목은 시리즈 번호보다 검색 의도가 먼저 보이게 한다.
- 비슷한 짧은 글을 계속 쪼개지 않고 허브 아래에 연결한다.
- 미래 글은 공개 전 허브나 Start Here에서 직접 링크하지 않는다.

## Week 4

- Search Console 기반으로 제목, description, 첫 문단, 내부링크를 고친다.
- 평균 순위 8-30위 글은 본문 보강과 내부링크 추가를 우선한다.
- 노출은 있는데 클릭이 없는 글은 제목과 description을 먼저 점검한다.
- 같은 쿼리로 여러 글이 노출되면 cannibalization 여부를 확인한다.

## Months 2-3

- 허브 3개를 확장한다: AI Coding Agent 운영 허브, Instruction Files 허브, AI Agent Security 허브.
- 템플릿 페이지 5개 이상을 운영한다.
- 검색 노출이 발생한 주제를 중심으로 리라이트 주기를 만든다.
- Rust, DevOps, Security 글 중 agent 검증/보안과 자연스럽게 연결되는 공개 글만 내부링크로 묶는다. 예약 글은 발행 후 연결한다.

## Months 4-6

- 기존 영어판은 유지하고, 품질이 낮거나 오래된 영어판은 삭제하지 않고 리라이트 후보로 표시한다.
- canonical/hreflang/link 오류가 있는 KR/EN pair를 우선 수정한다.
- 핵심축 영어판 투자는 reference, template, checklist, how-to 페이지에 먼저 배분한다.
- AI coding agent 운영, Codex, Claude Code, `AGENTS.md`, `CLAUDE.md`, hooks, MCP, permissions/settings, token/context, agent security/verification 글은 KR/EN 병행 발행을 기본으로 한다.
- Rust/DevOps/Security 일반 글은 한국어 우선이며, agent 운영/보안과 직접 연결될 때 영어판을 함께 보강한다.
- 월간 사용자 목표는 보수적 500-1,000명대, 공격적 2,000-5,000명대 진입으로 관리한다.
