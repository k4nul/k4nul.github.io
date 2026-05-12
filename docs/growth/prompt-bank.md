# Prompt Bank

검증 기준일: 2026-05-13

아래 프롬프트는 Codex에게 그대로 붙여 넣어 실행한다. 대량 수정, 영어화, cannibalization, Search Console 기반 판단처럼 데이터가 필요한 작업은 즉시 실행하지 않고 이 프롬프트로 분리한다.

## Daily Prompt

```md
너는 www.k4nul.com Git 블로그 레포지토리를 매일 관리하는 Codex다.

목적:
- 오늘 요일에 맞는 작은 성장 작업 1개를 수행한다.
- 신규 발행보다 기존 콘텐츠 구조화, 내부링크, 리라이트, 템플릿화를 우선한다.

범위:
- 먼저 `git branch --show-current`로 `master`인지 확인한다.
- `git status --short`로 기존 사용자 변경을 확인한다.
- 오늘 작업은 1-3개 파일 또는 1개 허브/글 묶음으로 제한한다.

작업 목록:
- `docs/growth/daily-codex-routine.md`의 요일별 작업표에서 오늘 작업을 고른다.
- Search Console/GA4 데이터가 없으면 수치를 추정하지 않는다.
- title, description, TL;DR, internal links, hub link, template link, related posts를 점검한다.
- 기존 URL, slug, permalink, translation_key를 보존한다.

수정 금지 사항:
- 기존 post body 대량 재작성 금지.
- 전체 제목 대량 변경 금지.
- 영어화 금지.
- 새 글 대량 생성 금지.
- 사용자가 만든 기존 변경 되돌리기 금지.

검증 방법:
- `bundle exec jekyll build`
- 링크 구조 변경 시 가능하면 `npm run check:links:local`
- `git diff --check`

완료 보고 형식:
- 변경 파일
- 변경 이유
- 실행한 검증 명령과 결과
- 남은 리스크
- 다음 작업 3개
```

## Week 1 Prompt: Structure Lock

```md
목적:
- K4NUL의 AI coding agent 운영·검증·보안 성장 구조를 고정한다.

범위:
- `docs/growth/`
- 루트 `AGENTS.md`
- 안전한 범위의 허브 점검: `/ai-engineering/`, `/start-here/`, `/ai-engineering/templates/`

작업 목록:
- 성장 목표, 로드맵, 요일별 루틴, Search Console 규칙, prompt bank가 최신인지 확인한다.
- AI Engineering 허브가 templates 페이지로 명확히 연결되는지 확인한다.
- Start Here가 AI agent 운영 경로를 명확히 제시하는지 확인한다.
- 홈에서 AI agent 운영·검증·보안 중심축이 보이는지 확인한다.

수정 금지 사항:
- 기존 URL 변경 금지.
- 새 글 대량 생성 금지.
- theme upstream 파일 변경 금지.
- Search Console/GA4 수치 추정 금지.

검증 방법:
- `bundle exec jekyll build`
- `git diff --check`
- 링크 구조 변경 시 `npm run check:links:local`

완료 보고 형식:
- 변경 파일과 목적
- 즉시 처리한 공통 작업
- 주차별로 넘긴 작업
- 검증 결과
- 남은 리스크
```

## Week 2 Prompt: Template Assets

```md
목적:
- 템플릿/체크리스트 자산을 만들어 K4NUL을 실무형 지식베이스로 강화한다.

범위:
- `/ai-engineering/templates/`
- 관련 AI agent 글 1-2개
- 필요 시 `docs/growth/content-backlog.md`

작업 목록:
- `AGENTS.md` 최소 템플릿, `CLAUDE.md` 최소 템플릿, Codex 작업 요청 프롬프트, Claude Code hooks 예제, MCP permissions/settings 보안 체크리스트 중 1개를 고른다.
- 템플릿에 목적, 적용 조건, 금지 사항, 검증 방법을 포함한다.
- 허브에서 템플릿으로, 템플릿에서 관련 글로 연결한다.

수정 금지 사항:
- 실제 도구 동작이나 옵션을 확인하지 못했으면 단정하지 않는다.
- 템플릿을 길고 범용적인 만능 문서로 만들지 않는다.
- URL 변경 금지.

검증 방법:
- `bundle exec jekyll build`
- 링크 추가 시 `npm run check:links:local`

완료 보고 형식:
- 작성/보강한 템플릿
- 연결한 허브와 관련 글
- 검증 결과
- 다음 템플릿 후보
```

## Week 3 Prompt: Long-Tail Search Writing

```md
목적:
- AI coding agent 운영·검증·보안 long-tail 검색 의도를 받을 글 1개를 작성하거나 기존 글 1개를 리라이트한다.

범위:
- `_posts/`의 기존 AI 관련 글 또는 신규 글 1개 이하
- 관련 허브 1개
- 관련 템플릿 1개

작업 목록:
- `docs/growth/content-backlog.md`의 long-tail 후보 중 하나를 고른다.
- 같은 검색 의도를 이미 다루는 글이 있으면 새 글 대신 리라이트한다.
- 제목은 검색 의도를 앞에 둔다.
- 첫 문단에 결론/TL;DR을 둔다.
- 허브, 템플릿, 관련 글 3개를 연결한다.

수정 금지 사항:
- 새 글 여러 개 생성 금지.
- URL, slug, permalink, translation_key 변경 금지.
- 확인하지 않은 사실, metrics, 실험 결과 작성 금지.

검증 방법:
- `_posts/AGENTS.md`, `docs/blog-style.md`, `templates/post-template.md` 준수 확인
- `bundle exec jekyll build`
- 링크 추가 시 `npm run check:links:local`

완료 보고 형식:
- 신규/리라이트 여부
- target query
- 변경 파일
- 검증 결과
- Search Console에서 나중에 확인할 query
```

## Week 4 Prompt: Search Console Rewrite

```md
목적:
- Search Console 데이터를 기준으로 제목, description, 본문, 내부링크를 개선한다.

범위:
- 사용자가 제공한 Search Console 데이터에 포함된 page/query만.
- 평균 순위 8-30위 또는 노출 있음 + 클릭 없음 page를 우선.

작업 목록:
- page/query/impressions/clicks/CTR/average position을 표로 정리한다.
- `docs/growth/search-console-decision-rules.md`에 따라 액션을 정한다.
- 제목/description 수정, 첫 문단/TL;DR 보강, 내부링크 추가 중 필요한 최소 변경만 한다.
- 변경한 page의 다음 확인 기준을 기록한다.

수정 금지 사항:
- 데이터 밖의 page 대량 수정 금지.
- 전체 제목 일괄 변경 금지.
- URL 변경 금지.
- 체류 시간 데이터 없이 engagement 문제라고 단정 금지.

검증 방법:
- `bundle exec jekyll build`
- 링크 구조 변경 시 `npm run check:links:local`
- 변경 후 7-14일 뒤 같은 query/page로 재확인

완료 보고 형식:
- 사용한 Search Console 입력값
- page별 decision
- 변경 파일
- 검증 결과
- 다음 데이터 확인일
```

## Monthly Review Prompt

```md
목적:
- 최근 28일 또는 월간 Search Console/GA4 데이터를 기준으로 K4NUL 성장 운영을 리뷰한다.

범위:
- Search Console: impressions, clicks, CTR, average position, non-brand queries, pages.
- GA4: organic sessions, direct sessions, organic landing pages, engaged sessions.

작업 목록:
- 데이터가 제공된 항목만 분석한다.
- non-brand query 증가 여부를 확인한다.
- 평균 순위 30위 안쪽 page를 세고 후보를 분류한다.
- 신규 글/리라이트/템플릿/허브/실험 비율이 `content-portfolio.md`와 맞는지 본다.
- 다음 달 우선순위 5개를 정한다.

수정 금지 사항:
- 누락된 데이터를 추정하지 않는다.
- 월간 사용자 수를 임의로 만들지 않는다.
- 영어화는 성과가 나온 후보만 선정한다.

검증 방법:
- 문서 변경 시 `bundle exec jekyll build`
- 링크 변경 시 `npm run check:links:local`

완료 보고 형식:
- 데이터 기간
- 확인된 성장 신호
- 문제 page/query
- 다음 달 우선순위 5개
- 사용자 입력이 더 필요한 값
```

## English Candidate Selection Prompt

```md
목적:
- 영어화할 템플릿과 허브 후보를 Search Console 성과 기준으로 선정한다.

범위:
- `/ai-engineering/templates/`
- AI Engineering 허브와 관련 template/how-to/reference page
- Search Console에서 노출 또는 클릭이 확인된 page만

작업 목록:
- page별 impressions, clicks, CTR, average position을 확인한다.
- template intent가 있는 query를 분류한다.
- 영어화 후보를 `ready`, `watch`, `defer`로 나눈다.
- 영어화가 필요한 경우 같은 `translation_key`와 명시적 `permalink` 계획을 세운다.

수정 금지 사항:
- 전체 번역 금지.
- 성과 없는 글 영어화 금지.
- canonical/hreflang 구조 변경 금지.
- 확인하지 않은 해외 검색 수요 추정 금지.

검증 방법:
- 후보 선정 문서만 수정하면 build.
- 실제 영어 page 생성 시 `bundle exec jekyll build`, `npm run check:links:local`, hreflang 샘플 확인.

완료 보고 형식:
- 후보 page
- 근거 query/metric
- 영어화 범위
- 보류 이유
- 다음 확인일
```
