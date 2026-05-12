# Change Log Template

아래 템플릿을 매일 작업 기록 또는 주간 리뷰에 사용한다. Search Console/GA4 데이터가 없으면 `사용자 입력 필요` 또는 `데이터 없음`으로 적고 추정하지 않는다.

```md
## YYYY-MM-DD

### 오늘의 목표

-

### 변경 파일

- `path/to/file.md`:

### 변경 이유

-

### 실행한 검증 명령

- `git branch --show-current`:
- `git status --short`:
- `bundle exec jekyll build`:
- `npm run check:links:local`: 실행 여부와 이유
- `git diff --check`:

### 결과

-

### 다음 작업

-

### 남은 리스크

- Search Console 데이터: 사용자 입력 필요 / 사용함 / 해당 없음
- GA4 데이터: 사용자 입력 필요 / 사용함 / 해당 없음
- 링크 검증 미실행 사유:
- build 실패 시 파일/플러그인/오류:
```
