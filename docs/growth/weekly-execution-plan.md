# Weekly Execution Plan

검증 기준일: 2026-05-25

## Queue-First Operating Rule

최근 운영 공백 복구 이후 주간 실행 계획의 기본값은 신규 글 작성이 아니라 예약 포스팅 큐 운영이다. 매주 먼저 이미 작성된 예약 글의 발행 전 품질, 발행 후 내부링크, KR/EN 대응, Search Console 색인 후보를 확인한다.

- 공개 페이지에는 실제 공개된 글과 오늘 공개된 글만 링크한다.
- 미래 글의 publish date, filename slug, permalink는 변경하지 않는다.
- 기존 영어판은 삭제하지 않고, 품질 문제가 있으면 리라이트 후보로 기록한다.
- Search Console/GA4 데이터가 없으면 성과 수치를 추정하지 않는다.
- 광범위한 제목 변경, cannibalization 정리, 영어 확장은 별도 데이터 기반 프롬프트로 분리한다.

## Week 1: Structure Lock

목표: 성장 운영 체계와 핵심 허브 구조를 고정한다.

- `docs/growth/` 문서 세트를 완성한다.
- 루트 `AGENTS.md`에 매일 운영 원칙을 반영한다.
- `/ai-engineering/`, `/start-here/`, `/ai-engineering/templates/` 존재와 내부링크 상태를 확인한다.
- 주요 AI agent 글 10개 이상을 리라이트/링크 후보로 분류한다.
- 빌드와 링크 검증 명령을 문서화한다.

완료 기준:

- 성장 목표, 로드맵, 요일별 루틴, prompt bank, Search Console 규칙이 존재한다.
- build 성공 또는 정확한 실패 원인이 기록된다.

## Week 2: Template Assets

목표: 예약 글이 연결할 템플릿 자산을 보강한다.

- 예약 포스팅 인벤토리에서 템플릿 연결이 필요한 글을 먼저 확인한다.
- `AGENTS.md` 최소 템플릿 보강.
- `CLAUDE.md` 최소 템플릿 보강.
- Codex 작업 요청 프롬프트 템플릿 보강.
- Claude Code hooks 예제 후보 설계.
- MCP permissions/settings 보안 체크리스트 후보 설계.
- 다음 14일 예약 글에서 실제로 연결할 템플릿이 필요한지 먼저 확인한다. DevOps 기반 글처럼 템플릿 연결이 부자연스러운 경우 `N/A`로 기록한다.

완료 기준:

- 템플릿 페이지 또는 연결 글 2개 이상이 허브에서 접근 가능하다. 단, 미래 글은 공개 전 허브에서 직접 링크하지 않는다.
- 각 템플릿은 목적, 적용 조건, 금지 사항, 검증 방법을 포함한다.

## Week 3: Long-Tail Search Writing

목표: 새 글을 만들지 않고 예약 큐의 long-tail intent 글을 발행 전 보강한다.

- `docs/growth/scheduled-posts-inventory.md`에서 이번 달 AI 핵심축 글을 우선 검토한다.
- `AGENTS.md`, `CLAUDE.md`, Codex, Claude Code, hooks, MCP, permissions/settings, token/context, validation/security 글의 title, description, TL;DR, 내부링크를 보강한다.
- 예약 큐에 없는 핵심 템플릿이 필요한 경우에만 신규 작성 후보로 기록한다.
- 이미 비슷한 글이 있으면 새 글 대신 해당 예약 글 또는 공개 글을 리라이트하고 허브 연결은 발행 후 수행한다.
- 다음 7-14일 예약 글에 내부링크가 없으면, 현재 공개된 관련 글 2-3개와 허브를 먼저 연결한다.

완료 기준:

- 신규 글은 기본 금지. 예외는 예약 큐에 없는 핵심 템플릿, Search Console상 새 reference page 필요, 사용자 명시 요청뿐이다.
- 기존 URL을 보존한다.
- 관련 허브와 템플릿 링크는 공개된 대상만 포함한다.

## Week 4: Search Console Rewrite

목표: 실제 검색 데이터를 기준으로 리라이트한다.

- 노출 있음 + 클릭 없음: 제목과 description 수정 후보를 만든다.
- 평균 순위 8-30위: 본문 보강, 요약 보강, 내부링크 추가.
- 클릭 있음 + 체류 낮음: 첫 문단, TL;DR, 예제 보강.
- 비슷한 쿼리로 여러 글 노출: cannibalization 점검.
- 템플릿 페이지 노출 발생: 기존 EN 대응 페이지 유무, canonical/hreflang, KR/EN 품질 보강 후보 지정.
- 데이터가 없는 주에는 Search Console 작업을 추정하지 않고 다음 주 예약 글 점검으로 대체한다.

완료 기준:

- 데이터가 있으면 query/page/action 표를 남긴다.
- 데이터가 없으면 추정하지 않고 사용자가 입력해야 하는 값만 기록한다.

## Months 2-3: Expand Three Hubs

목표: 허브 3개를 검색 의도별로 확장한다.

- AI Coding Agent 운영 허브.
- Instruction Files 허브.
- AI Agent Security 허브.
- 기존 AI Engineering 허브와 templates 페이지에서 서로 연결한다.
- Rust/DevOps/Security 글은 이미 공개된 글 또는 오늘 공개된 글 중 agent 검증, 자동화, 권한 경계와 연결 가능한 글만 보조 경로로 넣는다.

완료 기준:

- 허브 3개가 검색 의도, 추천 경로, 관련 템플릿, 대표 글을 가진다.
- build와 link check가 성공한다.

## Months 4-6: Maintain EN And Prioritize Core KR/EN

목표: 기존 영어판을 유지하면서, 핵심축 영어판과 KR/EN pair 품질을 우선 보강한다.

- 기존 영어판은 삭제하거나 폐기하지 않는다.
- 각 언어 페이지는 자기 자신을 canonical로 가져야 한다.
- 대응되는 한국어/영어 페이지가 있으면 같은 `translation_key`와 올바른 `hreflang` alternate를 점검한다.
- 번역 품질이 낮거나 내용이 오래된 영어판은 삭제하지 않고 리라이트 후보로 표시한다.
- 투자는 템플릿/체크리스트, `AGENTS.md`/`CLAUDE.md`, Codex/Claude Code 운영, hooks/MCP/permissions 보안, AI agent 검증/postmortem 순서로 배분한다.
- Rust/DevOps 일반 글은 한국어 우선이며, AI agent 운영/보안과 직접 연결될 때 영어판을 함께 발행하거나 보강한다.

완료 기준:

- KR/EN 보강 후보 선정 근거가 Search Console 데이터, 사용자 제공 데이터, 또는 canonical/hreflang/link 감사 결과에 연결된다.
- 수치 추정 없이 실제 입력값, 감사 결과, 또는 `사용자 입력 필요`로 표시한다.
