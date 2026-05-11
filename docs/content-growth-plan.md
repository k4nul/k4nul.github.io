# Content Growth Plan

검증 기준일: 2026-05-11
범위: `www.k4nul.com` Jekyll 블로그의 정보구조, 내부링크, SEO 기본기, 콘텐츠 허브

## Repo 기반 관찰

- 사이트는 Minimal Mistakes 기반 Jekyll 블로그다. 주요 콘텐츠는 `_posts/`, 주요 허브는 `_pages/`, 탐색 구조는 `_data/navigation.yml`과 섹션 아카이브 레이아웃에 있다.
- canonical, Open Graph, Twitter Card, JSON-LD, `hreflang`은 `_includes/seo.html`에서 처리한다.
- sitemap은 `jekyll-sitemap`, RSS는 `jekyll-feed`, robots는 `robots.txt`로 처리한다.
- AI Engineering 관련 글은 Codex, Claude Code, 하네스 엔지니어링, 토큰 관리, 검증, guardrail로 이미 충분히 쌓여 있지만, 기존 허브는 발행순 아카이브 성격이 강했다.
- `section-archive` 레이아웃이 페이지 본문을 출력하지 않아, 각 섹션 페이지에 작성된 소개와 추천 링크가 실제 허브 경험으로 충분히 살아나기 어려웠다.
- Search Console 또는 GA4 export 파일은 레포에서 확인하지 못했다. 따라서 클릭, 노출, CTR, organic session 수치는 추정하지 않는다.

## 이번 변경으로 해결한 것

- AI Engineering 페이지를 문제 해결형 허브로 개편했다.
- Start Here 페이지를 주제별 목록보다 독자의 문제 기준으로 재구성했다.
- AI agent 운영 템플릿 페이지를 추가해 `AGENTS.md`, `CLAUDE.md`, Codex 요청, 리뷰 체크리스트, permissions/settings 점검을 한곳에서 찾게 했다.
- AI/토큰 관리 글 하단에 공통 관련 읽기 경로를 자동 노출하는 include를 추가했다.
- Codex, Claude Code, AGENTS.md, CLAUDE.md, 토큰 관리, 하네스 엔지니어링 글의 제목에서 시리즈 번호보다 검색 의도가 먼저 보이도록 조정했다.
- Rust, DevOps, Security 허브에 AI agent 운영, 검증, 보안 경계와 연결되는 안내를 추가했다.
- 404 페이지가 주요 허브와 검색으로 이동하도록 보강했다.

## 아직 하지 않은 것

- 실제 Search Console query/page 데이터를 기반으로 title과 description을 재작성하지 않았다.
- GA4 organic landing page 성과를 기준으로 우선순위를 재정렬하지 않았다.
- 모든 Rust/DevOps/Security 개별 글 하단에 AI agent 맥락 링크를 수동으로 넣지는 않았다.
- 미래 발행일의 글은 빌드 시점에 공개되지 않을 수 있으므로, 허브의 고정 링크는 2026-05-11 기준 공개 가능한 글 중심으로 제한했다.
- 외부 백링크, 이미지 검색, schema 확장은 이번 범위에 넣지 않았다.

## 다음 30일 운영 작업

- Search Console에서 AI Engineering 허브, Start Here, Codex/Claude/AGENTS/token 글의 노출과 CTR을 확인한다.
- 노출은 높은데 CTR이 낮은 글은 title과 description을 먼저 손본다.
- 평균 게재순위 8-20위 글은 본문 상단 요약, 내부링크, 관련 글 블록을 우선 보강한다.
- Codex와 Claude Code 글 중 발행일이 지난 글부터 허브의 문제별 경로에 추가한다.
- Rust/DevOps/Security 글 중 agent 검증, CI, permissions, supply chain, observability와 직접 연결되는 글을 AI Engineering 허브의 보조 경로로 연결한다.
- 새 글을 늘리기보다 기존 글의 첫 문단, 요약, 제목, description, 관련 글을 매주 3-5개씩 개선한다.
- 영어 미러가 없는 Claude Code 글은 유입 가능성이 확인될 때 우선 번역 후보로 잡는다.

## Search Console에서 볼 지표

- 클릭
- 노출
- CTR
- 평균 게재순위
- 페이지
- 검색어

운영 메모: 먼저 페이지별로 보고, 그다음 검색어를 본다. 같은 검색어가 여러 글로 분산되면 허브나 대표 글로 내부링크를 모은다.

## GA4에서 볼 지표

- organic sessions
- engaged sessions
- page views
- landing pages

운영 메모: 이벤트 총량만 보면 콘텐츠 성장 판단이 흐려진다. organic landing page가 어디인지, 해당 세션이 다른 허브나 관련 글로 이어지는지 확인한다.
