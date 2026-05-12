# Weekly Execution Plan

검증 기준일: 2026-05-13

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

목표: 검색 노출과 실무 재사용에 맞는 템플릿 자산을 만든다.

- `AGENTS.md` 최소 템플릿 보강.
- `CLAUDE.md` 최소 템플릿 보강.
- Codex 작업 요청 프롬프트 템플릿 보강.
- Claude Code hooks 예제 후보 설계.
- MCP permissions/settings 보안 체크리스트 후보 설계.

완료 기준:

- 템플릿 페이지 또는 연결 글 2개 이상이 허브에서 접근 가능하다.
- 각 템플릿은 목적, 적용 조건, 금지 사항, 검증 방법을 포함한다.

## Week 3: Long-Tail Search Writing

목표: 대량 발행이 아니라 long-tail intent에 맞는 글 또는 기존 글 리라이트를 수행한다.

- `AGENTS.md는 왜 짧게 써야 할까` 유형 글을 우선 검토한다.
- `CLAUDE.md와 system prompt는 무엇이 다를까` 유형 글을 우선 검토한다.
- hooks, MCP, permissions/settings, token/context, validation/security 후보 중 1개만 작성한다.
- 이미 비슷한 글이 있으면 새 글 대신 해당 글을 리라이트하고 허브에 연결한다.

완료 기준:

- 신규 글은 주 1개 이하.
- 기존 URL을 보존한다.
- 관련 허브와 템플릿 링크가 포함된다.

## Week 4: Search Console Rewrite

목표: 실제 검색 데이터를 기준으로 리라이트한다.

- 노출 있음 + 클릭 없음: 제목과 description 수정 후보를 만든다.
- 평균 순위 8-30위: 본문 보강, 요약 보강, 내부링크 추가.
- 클릭 있음 + 체류 낮음: 첫 문단, TL;DR, 예제 보강.
- 비슷한 쿼리로 여러 글 노출: cannibalization 점검.
- 템플릿 페이지 노출 발생: 영어화 후보 지정.

완료 기준:

- 데이터가 있으면 query/page/action 표를 남긴다.
- 데이터가 없으면 추정하지 않고 사용자가 입력해야 하는 값만 기록한다.

## Months 2-3: Expand Three Hubs

목표: 허브 3개를 검색 의도별로 확장한다.

- AI Coding Agent 운영 허브.
- Instruction Files 허브.
- AI Agent Security 허브.
- 기존 AI Engineering 허브와 templates 페이지에서 서로 연결한다.
- Rust/DevOps/Security 글은 agent 검증, 자동화, 권한 경계와 연결 가능한 글만 보조 경로로 넣는다.

완료 기준:

- 허브 3개가 검색 의도, 추천 경로, 관련 템플릿, 대표 글을 가진다.
- build와 link check가 성공한다.

## Months 4-6: English Only For Winners

목표: 성과가 나온 템플릿과 허브만 영어화한다.

- Search Console에서 노출, 클릭, 평균 순위가 확인된 페이지만 후보로 지정한다.
- 전체 번역보다 reference, template, how-to 페이지를 우선한다.
- Korean canonical/hreflang 구조를 깨지 않는다.
- 영어 mirror는 필요한 경우 명시적 `permalink`와 같은 `translation_key`를 둔다.

완료 기준:

- 영어화 후보 선정 근거가 Search Console 데이터 또는 사용자 제공 데이터에 연결된다.
- 수치 추정 없이 실제 입력값 또는 `사용자 입력 필요`로 표시한다.
