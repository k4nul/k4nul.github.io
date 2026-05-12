# Search Console Decision Rules

검증 기준일: 2026-05-13

## Required Inputs

Search Console 데이터가 없으면 아래 값을 추정하지 않는다. 사용자가 CSV, 표, 스크린샷 요약, 수동 입력 중 하나로 제공해야 한다.

- 기간.
- page URL.
- query.
- impressions.
- clicks.
- CTR.
- average position.
- 필요 시 GA4 organic landing page, engaged sessions.

## Action Rules

| 조건 | 액션 | 우선순위 |
| --- | --- | --- |
| 노출 있음 + 클릭 없음 | 제목과 description을 수정한다. 검색 의도가 제목 앞쪽에 오게 하고, description에 해결 대상과 조건을 명확히 쓴다. | 높음 |
| 평균 순위 8-30위 | 본문 보강, 첫 문단/TL;DR 개선, 허브/템플릿/관련 글 내부링크 추가. | 높음 |
| 클릭 있음 + 체류 낮음 | 첫 문단, 요약, 예제, 체크리스트, next step을 보강한다. GA4 데이터가 없으면 추정하지 않는다. | 중간 |
| 비슷한 쿼리로 여러 글 노출 | cannibalization 점검. 대표 글/허브를 정하고 내부링크를 한쪽으로 모은다. | 중간 |
| 템플릿 페이지 노출 발생 | 영어화 후보로 지정하되, 바로 번역하지 않고 클릭/평균 순위 추이를 본다. | 중간 |
| 평균 순위 1-7위 + CTR 낮음 | 제목/description을 작게 실험한다. URL과 permalink는 유지한다. | 중간 |
| 노출 없음 | 색인 여부, 내부링크, sitemap 포함 여부, 허브 연결 여부를 먼저 확인한다. | 낮음 |

## Query Classification

- Brand: `k4nul`, 작성자명, 사이트명 중심 query.
- Non-brand: `AGENTS.md`, `CLAUDE.md`, Codex, Claude Code, hooks, MCP, permissions, token management, AI agent validation 등 사이트명 없이 주제 자체를 찾는 query.
- Template intent: template, example, checklist, sample, 작성법, 예제, 체크리스트가 포함된 query.
- Security intent: permission, settings, allowlist, secret, prompt injection, MCP security가 포함된 query.

## Rewrite Workflow

1. page별로 impressions, clicks, CTR, average position을 본다.
2. page 안에서 query를 보고 검색 의도를 분류한다.
3. 하나의 page에 여러 의도가 섞이면 대표 의도와 보조 의도를 나눈다.
4. 대표 의도가 title/description/첫 문단에 보이지 않으면 먼저 고친다.
5. 평균 순위 8-30위면 본문 근거, 예제, 내부링크를 보강한다.
6. 여러 page가 같은 query를 먹고 있으면 허브 또는 대표 글을 정한다.
7. 변경 후 7-14일 뒤 같은 기간 비교로 다시 본다.

## Change Table Template

| page | query | current metric | decision | files to edit | verification |
| --- | --- | --- | --- | --- | --- |
| 사용자 입력 필요 | 사용자 입력 필요 | 사용자 입력 필요 | title/description/body/link/canonical check | 사용자 입력 필요 | build/link check |

## Guardrails

- 기존 URL, slug, permalink는 보존한다.
- Search Console 데이터 없이 전체 제목 대량 변경을 하지 않는다.
- click이 낮다고 무조건 새 글을 만들지 않는다. 먼저 허브, description, 첫 문단, 내부링크를 본다.
- GA4 engaged sessions가 없으면 체류가 낮다고 단정하지 않는다.
- 영어화는 template page 노출 또는 클릭이 확인된 뒤 후보로만 지정한다.
