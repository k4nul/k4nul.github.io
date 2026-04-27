# SEO and i18n Rules

검증 기준일: 2026-04-27

이 사이트는 Jekyll과 Minimal Mistakes 기반이며, `site.url`은 `https://www.k4nul.com`을 canonical 기준으로 사용한다.

## Required Front Matter

- `lang`: `ko` 또는 `en`
- `translation_key`: 한국어 원문과 영어 미러 글이 공유하는 안정적인 키
- `description`: 검색 결과와 Open Graph에 사용할 1문장 요약
- 영어 글은 기존 URL을 유지하기 위해 필요한 경우 명시적 `permalink`를 둔다.

## hreflang

`_includes/seo.html`은 같은 `translation_key`를 가진 `site.pages`와 `site.posts`를 찾아 `rel="alternate"`와 `hreflang`을 출력한다. 번역본을 추가할 때는 두 언어의 `translation_key`를 반드시 맞춘다.

자동 매핑은 `translation_key`에 의존한다. 파일명이나 제목이 비슷하다는 이유만으로 번역 관계를 추정하지 않는다.

## Canonical

별도 `canonical_url`이 없으면 `page.url | absolute_url`을 사용한다. `_config.yml`의 `url` 값이 canonical 도메인이므로 GitHub Pages 기본 도메인을 front matter에 넣지 않는다.

## Metadata

주요 페이지와 포스트는 `title`, `description`, `lang`, `translation_key`를 가진다. 확인되지 않은 번역 관계, 작성자 경력, 조직, 자격 정보는 구조화 데이터에 넣지 않는다.
