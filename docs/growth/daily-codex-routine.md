# Daily Codex Routine

검증 기준일: 2026-05-25

## Role

Codex는 매일 K4NUL 블로그를 `AI coding agent 운영·검증·보안` 한국어 실무형 지식베이스로 관리한다. 기본 작업은 신규 발행이 아니라 이미 예약된 포스팅 큐의 품질 점검, 구조화, 리라이트, 내부링크, 템플릿화, 검증 기록이다.

## Before Work

- `git branch --show-current`로 현재 브랜치가 `master`인지 확인한다. `master`가 아니면 작업하지 않고 현재 브랜치명만 보고한다.
- `git status --short`로 기존 사용자 변경을 확인하고, 이번 작업과 무관한 변경은 건드리지 않는다.
- 글을 작성하거나 고칠 때는 `_posts/AGENTS.md`, `docs/blog-style.md`, `templates/post-template.md`를 먼저 확인한다.
- Search Console/GA4 데이터가 레포나 사용자 입력에 없으면 수치를 추정하지 않는다.
- 기존 URL, slug, permalink, `translation_key`는 보존한다.
- 예약 글의 publish date, filename slug, permalink는 임의로 변경하지 않는다.
- `docs/growth/scheduled-posts-inventory.md`, `docs/growth/scheduled-posts-calendar.md`, `docs/growth/pre-publish-checklist.md`, `docs/growth/post-publish-checklist.md`를 확인한다.
- 오늘 작업이 즉시 처리할 공통 작업인지, 주차별 프롬프트로 넘길 작업인지 구분한다.

## Daily Common Routine

1. 전날 변경과 빌드 상태를 확인한다.
2. 오늘의 작업 유형을 요일표에서 고르고, 이번 주 예약 발행 글을 먼저 확인한다.
3. 변경 범위를 1-3개 파일 또는 1개 허브/글 묶음으로 제한한다.
4. title, description, 첫 문단, TL;DR, 내부링크, 허브 링크, 템플릿 링크를 점검한다. 미래 글 링크는 공개 페이지에 추가하지 않는다.
5. 필요한 경우 Search Console 규칙에 따라 제목/description/본문/링크 액션을 선택한다.
6. 변경 후 `bundle exec jekyll build`를 실행한다.
7. 링크 구조를 바꿨다면 가능할 때 `npm run check:links:local`을 실행한다.
8. 결과를 change log 형식으로 남긴다.

## Weekday Table

| 요일 | 주요 작업 | 완료 기준 |
| --- | --- | --- |
| 월요일 | 이번 주 예약 글 점검일. 다음 7일 발행 글의 title, description, TL;DR, 내부링크, KR/EN 대응, 공개 시점 링크 안전성을 확인한다. | 예약 글별 보강 여부와 남은 리스크 기록 |
| 화요일 | 다음 7일 예약 글 리라이트일. 새 글을 만들지 않고 예약 글 1-2개의 제목 후보, description, 첫 문단, 관련 링크를 보강한다. | URL, slug, permalink, publish date 보존 |
| 수요일 | 예약 글과 연결될 템플릿 보강일. AGENTS.md, CLAUDE.md, Codex 요청, hooks, MCP, permissions/settings, review checklist 중 필요한 1개만 보강한다. | 템플릿 적용 조건, 금지 사항, 검증 방법 포함 |
| 목요일 | 최근 발행 글 내부링크 정리일. 발행 후 공개된 글을 허브, 관련 공개 글, 템플릿에서 안전하게 연결한다. | 미래 글 링크 없음, 관련 공개 글 2-3개 연결 |
| 금요일 | 예약된 실험/postmortem 글 품질 보강일. 실제 재현, 실패 사례, 검증 기준, 한계를 확인하고 부족하면 후보로만 기록한다. | 사실/관찰/해석/한계 분리, 검증 기준일 기록 |
| 토요일 | 공개 허브 반영일. `/ai-engineering/`, `/start-here/`, `/ai-engineering/templates/`에는 실제 공개된 글만 추가한다. | 허브와 템플릿 경로 유지, 미래 글 링크 없음 |
| 일요일 | Search Console/GA4 또는 다음 주 예약 글 점검일. 데이터가 있으면 분석하고, 없으면 다음 주 예약 글 보강 후보만 정리한다. | 수치 추정 없음, 사용자 입력 필요 값 명시 |

## After Work

- `git diff --stat`과 `git diff --check`로 변경 범위와 whitespace 문제를 확인한다.
- `bundle exec jekyll build` 결과를 기록한다.
- 링크 구조 변경이 있으면 `npm run check:links:local` 결과를 기록한다.
- 실행하지 못한 검증은 이유를 숨기지 않는다.
- 다음 작업 후보 3-5개를 남긴다.

## Do Not

- 새 글을 대량 생성하지 않는다.
- 기본적으로 새 글을 만들지 않는다. 예약 큐에 없는 핵심 템플릿, Search Console상 새 reference page 필요, 사용자 명시 요청일 때만 예외로 한다.
- 기존 post body를 site-structure 작업 때문에 통째로 다시 쓰지 않는다.
- 미래 글 publish date, slug, permalink를 임의로 바꾸지 않는다.
- 공개 페이지에서 미래 글로 직접 링크하지 않는다.
- Search Console/GA4 수치를 임의로 만들지 않는다.
- 비슷한 짧은 글을 계속 쪼개지 않는다.
- 전체 제목 대량 변경, 광범위한 KR/EN 보강, cannibalization 정리는 데이터와 별도 프롬프트 없이 즉시 실행하지 않는다.
