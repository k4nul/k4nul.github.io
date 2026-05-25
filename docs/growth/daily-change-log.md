# Daily Change Log

## 2026-05-13

### 오늘의 목표

- 2026-05-13 공개 글인 Claude Code MCP 운영 글을 공개 허브와 템플릿 페이지에 안전하게 연결한다.
- 다음 7일 예약 글에 필요한 템플릿/체크리스트 기반을 보강하되, 공개 페이지에서 미래 글로 링크하지 않는다.

### 변경 파일

- `_pages/development-ai.md`: MCP/hooks/permissions/settings 경로에 공개된 hooks 글과 MCP 글을 추가하고, 추후 후보 문구에서 이미 공개된 항목을 제거했다.
- `_pages/ai-agent-templates.md`: MCP 연결 전 점검표를 추가하고 공개된 hooks/MCP 글로 연결했다.
- `_pages/en-ai-agent-templates.md`: KR 템플릿 페이지와 같은 범위의 MCP pre-connection checklist를 추가했다. 대응 영어 글이 없는 KR-only 글 링크는 추가하지 않았다.

### 변경 이유

- 오늘 공개된 MCP 글이 `/ai-engineering/` 및 `/ai-engineering/templates/`에서 발견될 수 있게 post-publish 내부링크를 반영했다.
- 2026-05-14부터 이어지는 Claude Code context/subagent/operations 예약 글이 연결할 수 있는 템플릿 점검 항목을 보강했다.
- 공개 페이지에는 2026-05-13 기준 이미 공개된 글만 연결하고, 2026-05-14 이후 예약 글 링크는 넣지 않았다.

### 실행한 검증 명령

- `git branch --show-current`: `master`
- `git status --short`: 기존 사용자 변경으로 보이는 2026-09~2026-11 Rust 예약 글 수정과 untracked `2026-05-09-codex-goal-long-running-task-harness.md` 확인. 이번 작업에서는 건드리지 않음.
- `bundle exec jekyll build`: 성공. 2026-05-14 이후 미래 글은 expected future-date skip으로 제외됨. Sass deprecation warning은 기존 theme 경고로 보임.
- `npm.cmd run check:links:local`: 성공. Source pages 151, internal references 8750, unique targets 169, broken targets 0.
- `git diff --check`: 통과. 일부 `_pages` 파일의 LF/CRLF warning만 출력됨.

### 결과

- 오늘 공개 글 `/ai/connect-external-context-with-mcp/`가 `/ai-engineering/`와 `/ai-engineering/templates/`에서 연결됨.
- `/ai-engineering/templates/`와 `/en/development/ai/templates/`에 MCP 연결 전 점검표가 추가됨.
- 샘플 산출물에서 canonical, og:title, og:description, og:url, Twitter description이 비어 있지 않음을 확인했다.
- KR/EN 템플릿 페이지의 `translation_key`와 hreflang 출력은 유지됨.

### 다음 작업

- 2026-05-14 `handle-logs-issues-and-auto-memory-with-context-budget` pre-publish 점검.
- 2026-05-15 `when-to-use-claude-code-subagents` pre-publish 점검.
- 2026-05-16 `claude-code-project-operations-template` pre-publish 점검.
- 공개 후 각 글에서 `/ai-engineering/`와 `/ai-engineering/templates/`로 돌아가는 링크를 추가할지 확인.
- Git 01~04 KR/EN 쌍은 발행일 전 title/description/TL;DR 및 내부링크 점검 후보로 유지.

### 남은 리스크

- Search Console 데이터: 사용자 입력 필요
- GA4 데이터: 사용자 입력 필요
- 링크 검증 미실행 사유: 해당 없음
- build 실패 시 파일/플러그인/오류: 해당 없음
- 기존 작업트리의 Rust 예약 글 수정과 untracked 2026-05-09 글은 사용자 변경으로 보고 그대로 둠.

## 2026-05-14

### 오늘의 목표

- 2026-05-14 발행 글인 `Claude Code context budget: 긴 로그, 이슈, auto memory 관리 기준`의 공개 접근성을 확인한다.
- 공개 접근 가능할 때만 `/ai-engineering/`, `/start-here/`, `/ai-engineering/templates/`, 관련 기존 공개 글에서 안전하게 연결한다.
- Search Console 색인 요청 후보와 발행 후 검증 결과를 기록한다.

### 변경 파일

- `_posts/2026-05-14-handle-logs-issues-and-auto-memory-with-context-budget.md`: 새 글에서 AI Engineering 허브, 템플릿, 관련 토큰/컨텍스트 글로 돌아가는 `함께 읽을 글` 섹션을 추가했다.
- `_pages/development-ai.md`: 토큰/컨텍스트 관리 추천 경로에 오늘 공개 글을 추가했다.
- `_pages/start.md`: `컨텍스트가 너무 커질 때` 읽기 경로에 오늘 공개 글을 추가했다.
- `_pages/ai-agent-templates.md`: 함께 읽을 글에 오늘 공개 글을 추가했다.
- `_posts/2026-04-22-long-logs-long-plans-long-memory-agent-context-bloat.md`: 관련 기존 글에서 오늘 공개 글로 내부링크를 추가했다.
- `_posts/2026-04-23-how-to-design-state-summaries-that-save-tokens.md`: 관련 기존 글에서 오늘 공개 글로 내부링크를 추가했다.
- `_posts/2026-04-25-how-token-management-strategies-differ-between-codex-and-claude-code.md`: 관련 기존 글에서 오늘 공개 글로 내부링크를 추가했다.
- `_posts/2026-05-15-when-to-use-claude-code-subagents.md`: 발행 전 점검으로 AI Engineering 허브, 템플릿, 공개된 관련 글로 이어지는 `함께 읽을 글` 섹션을 추가했다.
- `_posts/2026-05-16-claude-code-project-operations-template.md`: 발행 전 점검으로 Claude Code 운영 구조, CLAUDE.md, permissions/settings, hooks, MCP, subagent 글로 이어지는 `함께 읽을 글` 섹션을 추가했다.
- `docs/growth/search-console-indexing-candidates.md`: 오늘 공개 글을 Search Console 색인 요청 후보로 기록했다.
- `docs/growth/daily-change-log.md`: post-publish 작업 결과를 이 형식으로 기록했다.

### 변경 이유

- 오늘 글은 Claude Code의 긴 로그, 이슈, auto memory, context budget을 다루는 AI coding agent 운영 글이므로 `/ai-engineering/` 허브와 Start Here의 context 경로에 연결할 가치가 있다.
- 템플릿 페이지는 `CLAUDE.md`, permissions/settings, MCP 점검표를 다루므로 오늘 글의 auto memory/context budget 기준으로 이어지는 보조 링크가 유효하다.
- 2026-05-15 이후 예약 글은 아직 future-dated skip 대상이므로 공개 페이지에 링크하지 않았다.
- 2026-05-15와 2026-05-16 예약 글은 발행 직후 독자가 핵심 허브, 템플릿, 선행 공개 글로 이동할 수 있게 본문 내부링크만 보강했다.
- KR 단독 글이므로 EN 허브/템플릿/Start Here에는 KR-only 링크를 추가하지 않았다.

### 실행한 검증 명령

- `git branch --show-current`: `master`
- `git status --short`: 작업 시작 시 출력 없음. 작업 후 변경 파일은 2026-05-15/2026-05-16 예약 글 2개와 `docs/growth/daily-change-log.md`로 제한됨.
- `curl.exe -I https://www.k4nul.com/ai/handle-logs-issues-and-auto-memory-with-context-budget/`: `HTTP/1.1 200 OK`
- `bundle exec jekyll build`: 성공. 오늘 글은 `_site/AI/handle-logs-issues-and-auto-memory-with-context-budget/index.html`에 생성됨. 2026-05-15 이후 글은 expected future-date skip으로 제외됨. Sass deprecation warning은 기존 theme 경고로 보임.
- `npm run check:links:local`: PowerShell 실행 정책 때문에 `npm.ps1` 로딩에서 실패. `npm.cmd run check:links:local`로 재실행.
- `npm.cmd run check:links:local`: 성공. Source pages 152, internal references 8833, unique internal targets 170, broken targets 0.
- `rg` 공개 산출물 미래 slug 점검: `_site` HTML에서 2026-05-15 이후 예약 slug 링크 없음.
- `git diff --check`: 통과. 일부 작업 파일의 LF/CRLF warning만 출력됨.

### 결과

- 오늘 공개 URL `https://www.k4nul.com/ai/handle-logs-issues-and-auto-memory-with-context-budget/`는 `HTTP 200 OK`로 확인했다.
- 생성 HTML에서 canonical, og:title, og:description, og:url, Twitter description이 비어 있지 않음을 확인했다.
- `hreflang="ko"`와 `hreflang="x-default"`가 출력되며, EN 대응 글이 없어 `hreflang="en"`은 추가하지 않았다.
- `/ai-engineering/`, `/start-here/`, `/ai-engineering/templates/`와 관련 기존 KR 공개 글 3개에서 오늘 글로 연결된다.
- 2026-05-15와 2026-05-16 예약 글은 발행 시점에 이미 공개되어 있을 글 또는 발행 순서상 안전한 선행 글만 링크한다.
- `_site` HTML에서 2026-05-15 이후 미래 글 slug 링크가 발견되지 않았다.

### 다음 작업

- 2026-05-15 `when-to-use-claude-code-subagents` 발행 후 post-publish 접근성 확인.
- 2026-05-16 `claude-code-project-operations-template` 발행 후 post-publish 접근성 확인.
- Git 01 KR/EN 쌍 발행 전후 title, description, TL;DR, 내부링크 점검.
- 오늘 글의 Search Console 색인/노출은 2026-05-21~2026-05-28 사이 확인.
- EN 대응 글이 필요하다는 데이터나 편집 판단이 생기면 별도 후보로 기록하되, 지금은 생성하지 않는다.

### 남은 리스크

- Search Console 데이터: 사용자 입력 필요
- GA4 데이터: 사용자 입력 필요
- 링크 검증 미실행 사유: 해당 없음
- build 실패 시 파일/플러그인/오류: 해당 없음
- 오늘 글은 `search: false`가 있어 사이트 내부 검색 노출 의도는 별도 확인이 필요하다. HTML robots noindex는 출력되지 않았다.

## 2026-05-15

### 오늘의 목표

- 금요일 기준으로 2026-05-15 발행 글인 `Claude Code subagent 사용 기준: 전문 에이전트를 언제 분리할까`의 post-publish 접근성과 내부링크를 확인한다.
- 최근 7일 내 공개된 Claude Code 운영 글과 공개 허브에서 오늘 글로 들어오는 안전한 링크를 보강한다.
- 다음 7일 예약 글은 공개 페이지에서 링크하지 않고, 2026-05-16 예약 글의 기존 pre-publish 변경만 유지한다.

### 변경 파일

- `_pages/development-ai.md`: Claude Code 운영 경로와 관련 글 링크에 오늘 공개 글을 추가했다.
- `_pages/start.md`: 문제별 읽기 경로에 subagent 판단 경로를 추가했다.
- `_pages/ai-agent-templates.md`: 함께 읽을 글에 오늘 공개 글을 추가했다.
- `_posts/2026-04-15-multi-agent-is-not-the-default.md`: 공개된 관련 글에서 오늘 글로 이어지는 `함께 읽을 글` 섹션을 추가했다.
- `_posts/2026-05-05-when-to-use-codex-subagents.md`: Codex subagent 글에서 Claude Code subagent 글로 이어지는 관련 링크를 추가했다.
- `_posts/2026-05-14-handle-logs-issues-and-auto-memory-with-context-budget.md`: context budget 글에서 오늘 subagent 글로 이어지는 링크를 추가했다.
- `docs/growth/search-console-indexing-candidates.md`: 오늘 공개 URL을 Search Console 색인 요청 후보로 기록했다.
- `docs/growth/daily-change-log.md`: 오늘 작업 결과를 이 형식으로 기록했다.

작업 시작 전 이미 수정되어 있던 `_posts/2026-05-15-when-to-use-claude-code-subagents.md`, `_posts/2026-05-16-claude-code-project-operations-template.md` 변경은 되돌리지 않고 유지했다.

### 변경 이유

- 오늘 글은 Claude Code subagent, context isolation, parallel work 판단 기준을 다루는 AI coding agent 운영 글이므로 `/ai-engineering/`, `/start-here/`, `/ai-engineering/templates/`에서 발견될 수 있어야 한다.
- 관련 공개 글 3개에서 오늘 글로 연결해 subagent 주제를 Codex, Claude Code, multi-agent 기준으로 묶었다.
- 2026-05-16 이후 예약 글과 Git 01~06 KR/EN 쌍은 아직 future-dated skip 대상이므로 공개 페이지에 링크하지 않았다.
- KR 단독 글이므로 EN 허브/템플릿/Start Here에는 KR-only 링크를 추가하지 않았다.

### 실행한 검증 명령

- `git branch --show-current`: `master`
- `git status --short`: 작업 시작 시 기존 수정 파일은 `_posts/2026-05-15-when-to-use-claude-code-subagents.md`, `_posts/2026-05-16-claude-code-project-operations-template.md`, `docs/growth/daily-change-log.md`였음. 작업 후 공개 허브/관련 글/색인 후보 문서가 추가로 변경됨.
- `curl.exe -I https://www.k4nul.com/ai/when-to-use-claude-code-subagents/`: `HTTP/1.1 200 OK`
- `bundle exec jekyll build`: 성공. 오늘 글은 `_site/AI/when-to-use-claude-code-subagents/index.html`에 생성됨. 2026-05-16 이후 글은 expected future-date skip으로 제외됨. Sass deprecation warning은 기존 theme 경고로 보임.
- `npm.cmd run check:links:local`: 성공. Source pages 153, internal references 9056, unique internal targets 171, broken targets 0.
- `rg` 공개 산출물 미래 slug 점검: `_site` HTML에서 2026-05-16 이후 다음 7일 예약 slug 링크 없음.
- `git diff --check`: 통과. 일부 작업 파일의 LF/CRLF warning만 출력됨.

### 결과

- 오늘 공개 URL `https://www.k4nul.com/ai/when-to-use-claude-code-subagents/`는 `HTTP 200 OK`로 확인했다.
- 생성 HTML에서 canonical, og:title, og:description, og:url, Twitter description이 비어 있지 않음을 확인했다.
- `hreflang="ko"`와 `hreflang="x-default"`가 출력되며, EN 대응 글이 없어 `hreflang="en"`은 추가하지 않았다.
- `/ai-engineering/`, `/start-here/`, `/ai-engineering/templates/`와 관련 기존 KR 공개 글 3개에서 오늘 글로 연결된다.
- `robots.txt`는 `https://www.k4nul.com/sitemap.xml`을 가리키고, `_site/feed.xml`과 `_site/sitemap.xml` 생성도 확인했다.
- 공개 산출물에서 2026-05-16 이후 예약 글 slug 링크는 발견되지 않았다.

### 다음 작업

- 2026-05-16 `claude-code-project-operations-template` 발행 후 post-publish 접근성 확인.
- 2026-05-17~2026-05-22 Git 01~06 KR/EN 쌍의 title, description, TL;DR, 내부링크를 발행 전 점검한다.
- Git 05 conflict 재현 글은 금요일 실험/재현 관점 후보로 두고, 실제 재현 환경과 한계 표기가 충분한지 별도 점검한다.
- 오늘 글의 Search Console 색인/노출은 2026-05-22~2026-05-29 사이 확인.
- EN 대응 글이 필요하다는 데이터나 편집 판단이 생기면 별도 후보로 기록하되, 지금은 생성하지 않는다.

### 남은 리스크

- Search Console 데이터: 사용자 입력 필요
- GA4 데이터: 사용자 입력 필요
- 링크 검증 미실행 사유: 해당 없음
- build 실패 시 파일/플러그인/오류: 해당 없음
- 오늘 글은 `search: false`가 있어 사이트 내부 검색 노출 의도는 별도 확인이 필요하다. HTML robots noindex는 출력되지 않았다.
