# Post-Publish Checklist

검증 기준일: 2026-05-13

이 체크리스트는 발행 당일 또는 발행 후 사용한다. 미래 포스트는 Jekyll build에서 공개되지 않다가 발행일이 지나면 공개 대상이 되므로, 내부링크와 허브 반영은 발행 후 확인을 기본으로 한다.

## Publish Verification

- 글이 실제 공개 URL에서 접근 가능한가?
- `bundle exec jekyll build` 결과에서 해당 글이 더 이상 future-dated skip으로 제외되지 않는가?
- canonical URL이 자기 자신인가?
- KR/EN pair가 있다면 `hreflang="ko"`, `hreflang="en"`, `hreflang="x-default"`가 의도대로 출력되는가?
- `og:title`, `og:description`, `og:url`, Twitter Card description이 비어 있지 않은가?

## Internal Link Actions

- `/ai-engineering/` 허브에 추가해야 하는가?
- `/start-here/`에 추가해야 하는가?
- `/ai-engineering/templates/`에 연결해야 하는가?
- Rust/DevOps/Security 허브에 추가해야 하는가?
- 기존 공개 관련 글에서 새 글로 내부링크를 추가해야 하는가?
- 새 글에서 링크한 대상이 모두 공개 URL인가?
- 같은 KR/EN pair 양쪽에 필요한 내부링크가 균형 있게 반영되었는가?

## Search And Operations

- Search Console 색인 요청 대상인가?
- `docs/growth/change-log-template.md` 형식으로 변경 기록을 남겼는가?
- Search Console 확인 예정일을 기록했는가?
- 발행 후 7-14일 뒤 title, description, 평균 순위, CTR 확인 후보로 남길 것인가?

## Verification

- `bundle exec jekyll build`
- 내부링크 변경 시 `npm.cmd run check:links:local`
- 메타 변경 시 `npm.cmd run seo:audit`를 시도하되, 기존 legacy canonical warning과 새 오류를 구분한다.
