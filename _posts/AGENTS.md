# AGENTS.md

이 파일은 `_posts` 바로 아래 원문 기술 블로그 글에 적용한다. 네이버/티스토리 파생본은 `content/posts`와 `doc/channel-posting/` 규칙을 따른다.

## 필수 Front Matter

- `title`, `date`, `lang`, `translation_key`, `section`, `tags`, `description`을 넣는다.
- `section` 값은 기존 URL 구조를 고려해 `security`, `development`, `life` 중 하나만 사용한다. 단, 빈 `life` 섹션을 주요 메뉴에 노출하지 않는다.
- `topic_key`는 섹션 안의 트랙을 묶을 때 사용한다: `malware-analysis`, `security-engineering`, `ai`, `token-management`, `rust`, `devops`.
- 대표 글이나 포트폴리오 노출이 필요할 때만 `featured: true`를 쓴다.
- 선택 필드: `track`, `repo`, `demo`, `references`.
- 영어 미러 글은 `lang: en`, 같은 `translation_key`, 필요한 경우 명시적 `permalink`를 둔다.

## 기본 본문 구조

- `## Summary / 요약`
- `## Document Info / Environment`
- `## Problem Statement / 문제 정의`
- `## Verified Facts / 확인된 사실`
- `## Reproduction Steps / 재현 순서`
- `## Observations / 관찰 결과`
- `## Interpretation / 해석`
- `## Limitations / 한계`
- `## References / 참고자료`
- `## Change Log / 변경 이력`

기존 글은 예전 한국어 헤더를 유지할 수 있다. 새 글은 `templates/post-template.md`를 기준으로 작성한다. 보안 분석 글은 `templates/security-analysis-template.md`를 우선 사용한다.

## 검증 규칙

- 사실은 출처와 연결하고, 직접 실험은 환경과 결과를 적고, 의견은 의견임을 표시한다.
- 최신성에 민감한 내용은 `검증 기준일`을 적는다.
- 버전 의존 내용은 테스트 환경과 테스트 버전을 적는다.
- 검증하지 못한 내용은 단정하지 않는다.
- 기존 글을 수정할 때는 본문을 대량으로 다시 쓰지 말고 근거, 날짜, 환경, 한계부터 보강한다.
