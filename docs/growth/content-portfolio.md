# Content Portfolio

검증 기준일: 2026-05-13

## Operating Ratio

K4NUL의 성장 운영은 신규 발행량 회복보다 이미 작성된 예약 포스팅 큐와 기존 공개 자산의 검색 구조화, 신뢰성 개선을 우선한다.

| 유형 | 비율 | 목적 | 예시 |
| --- | --- | --- | --- |
| 예약 글 발행 전 점검 | 30% | 이미 작성된 미래 글을 long-tail intent에 맞게 보강 | AGENTS.md, CLAUDE.md, Codex, Claude Code, hooks, MCP, token/context |
| 기존 공개 글 리라이트 | 30% | 노출/CTR/평균 순위 개선 | 제목, description, 첫 문단, TL;DR, 근거, 내부링크 |
| 템플릿/체크리스트 | 20% | 실무 재사용과 저장/공유 가치 확보 | AGENTS.md 템플릿, MCP 보안 체크리스트, agent 리뷰 체크리스트 |
| 허브 보강 | 10% | 검색 의도별 길잡이와 내부링크 중심점 확보 | AI Engineering, Start Here, Templates |
| 예약된 실험/postmortem 보강 | 10% | 신뢰와 차별화 확보 | 실패 사례, 검증 기준, 한계, 직접 재현 |

## Content Principles

- 한 주에 모든 유형을 다 하려고 하지 않는다. 요일별 루틴으로 작은 개선을 반복한다.
- 기본적으로 새 글을 만들지 않고 `scheduled-posts-inventory.md`의 예약 글을 우선 활용한다.
- 비슷한 짧은 글을 계속 쪼개지 말고 허브 아래에 연결한다.
- 미래 글은 발행 전 공개 페이지에서 직접 링크하지 않는다.
- Rust, DevOps, Security는 중심축을 보조하는 실무 기반으로 연결한다.
- 검색 의도가 분명한 제목을 우선하고, 시리즈 번호나 내부 라벨은 뒤로 보낸다.
- 약한 앵커 텍스트 대신 `AGENTS.md 작성법`, `AI agent 검증 루프`, `Claude Code permissions/settings`처럼 의도가 보이는 앵커를 쓴다.

## KR/EN Publishing Criteria

- 기존 영어판은 유지한다. 품질이 낮거나 오래된 영어판은 삭제하지 않고 리라이트 후보로 표시한다.
- AI coding agent 운영, Codex, Claude Code, `AGENTS.md`, `CLAUDE.md`, hooks, MCP, permissions/settings, token/context management, AI agent security, AI agent verification 글은 KR/EN 병행 발행을 기본으로 한다.
- 템플릿/체크리스트/reference/how-to 성격의 글도 KR/EN 병행 발행을 기본으로 한다.
- Rust/DevOps/Security 일반 글은 한국어 우선으로 발행하고, AI agent 운영/보안과 직접 연결되는 경우에만 영어판을 함께 발행하거나 보강한다.
- 짧은 메모성 글이나 한국어 독자 맥락에 강하게 의존하는 글은 영어판을 무리하게 만들지 않는다.
- 각 언어 페이지는 자기 자신을 canonical로 갖고, 동등한 대응 페이지에만 `hreflang` alternate를 둔다.

## Portfolio Review Questions

- 예약 글 점검보다 신규 작성이 앞서고 있지 않은가?
- 템플릿/체크리스트가 단순 복사용 문구가 아니라 적용 조건과 검증 방법을 담고 있는가?
- 허브가 글 목록이 아니라 문제별 경로를 제공하는가?
- 실험/postmortem 글이 사실, 관찰, 해석, 한계를 분리하는가?
- KR/EN 보강 후보가 실제 검색 성과, canonical/hreflang/link 감사 결과, 또는 핵심축 병행 발행 기준에 근거하는가?
