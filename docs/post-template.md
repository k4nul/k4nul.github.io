# Post Templates

검증 가능한 기술 글은 `templates/post-template.md`를 사용한다. 보안 분석 글은 `templates/security-analysis-template.md`를 우선 사용한다.

두 템플릿은 다음 기준을 공통으로 강제한다.

- 사실, 직접 재현, 관찰, 해석, 한계를 분리한다.
- `검증 기준일`, 테스트 환경, 테스트 버전을 비워 두지 않는다.
- `featured`, `track`, `repo`, `demo`, `references` front matter는 선택 필드다.
- 대표 글이 아니면 `featured: false`를 유지한다.
- 확인하지 못한 샘플 출처, CVE 매핑, 경력/소속/자격은 만들지 않는다.
