# Pre-Publish Checklist

검증 기준일: 2026-05-13

이 체크리스트는 예약 글의 발행 7일 전 또는 발행 전날 사용한다. 기본 원칙은 새 글을 더 만드는 것이 아니라 이미 예약된 포스팅 큐의 품질, 링크, KR/EN 대응, 공개 시점 안전성을 점검하는 것이다.

## Scope

- 대상: `docs/growth/scheduled-posts-inventory.md`와 `docs/growth/scheduled-posts-calendar.md`에 있는 예약 글.
- 금지: publish date, filename slug, permalink를 임의로 변경하지 않는다.
- 일정 변경이 필요해 보이면 실제 변경하지 말고 `docs/growth/schedule-adjustment-candidates.md`에 후보로만 기록한다.
- 미래 글은 공개 페이지가 아니라 `docs/growth/` 운영 문서에서만 관리한다.

## Content Checklist

- `title`이 검색 의도를 드러내는가?
- `description`이 있고 구체적인가?
- TL;DR 또는 `## 요약`이 있는가?
- 관련 허브 링크가 있는가?
- 관련 템플릿 링크가 필요한 글인가?
- 이미 공개된 관련 글 2-3개로 연결되는가?
- 미래 글로 직접 링크하지 않는가?
- 코드/명령어 예제가 검증되었는가?
- 검증하지 않은 예제는 실행 테스트 없음, 버전 미고정, 한계로 명시했는가?
- KR/EN 대응 글의 품질과 범위가 서로 맞는가?
- canonical/hreflang에 문제가 없는가?

## Public Link Policy

- 공개 페이지에서 미래 글로 직접 링크하지 않는다.
- 단, 빌드 결과에서 해당 미래 글이 실제로 공개되는 구조라면 예외를 검토할 수 있다.
- 현재 레포는 Jekyll build에서 미래 포스트가 제외되는 구조이므로 기본값은 링크 금지다.
- 허브, Start Here, 홈에는 이미 공개된 글과 오늘 실제 공개된 글만 직접 링크한다.
- 발행 당일 또는 발행 후 post-publish 작업으로 허브와 기존 공개 글에 내부링크를 추가한다.
- 미래 글끼리의 내부링크도 발행 순서를 확인하고, 공개 시점에 404가 나지 않도록 점검한다.

## KR/EN Checklist

- 한국어와 영어 글이 같은 `translation_key`를 공유하는가?
- 영어 글은 자기 자신을 canonical로 갖는가?
- 한국어 글은 자기 자신을 canonical로 갖는가?
- 두 글이 동등한 범위일 때만 `hreflang` alternate로 연결되는가?
- 영어판 품질이 낮으면 삭제하지 않고 리라이트 후보로 기록했는가?

## Verification

- `bundle exec jekyll build`
- 링크를 바꿨다면 `npm.cmd run check:links:local`
- 샘플 출력에서 canonical URL과 hreflang 확인
- 공개 페이지에 미래 글 링크가 들어가지 않았는지 `rg` 또는 link check로 확인
