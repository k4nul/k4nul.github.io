# KR/EN Operating Policy

검증 기준일: 2026-05-13

## Core Principle

K4NUL은 이미 한국어판과 영어판을 병행 발행하고 있다. 따라서 기존 영어판은 삭제하거나 폐기하지 않는다. 영어판의 품질이 낮거나 내용이 오래되었으면 삭제가 아니라 리라이트, 링크 보강, canonical/hreflang 수정 후보로 표시한다.

## Existing Pages

- 기존 한국어 페이지와 영어 페이지는 유지한다.
- 각 언어 페이지는 자기 자신을 canonical로 가져야 한다.
- 대응되는 한국어/영어 페이지가 있다면 같은 `translation_key`와 올바른 `hreflang` alternate를 점검한다.
- 동등하지 않은 페이지끼리는 `hreflang`으로 연결하지 않는다.
- 깨진 링크, 잘못된 canonical, 누락된 `hreflang`을 우선 수정한다.
- 영어판을 한국어판으로 canonical 처리하지 않는다.

## New Content

- AI coding agent 운영, Codex, Claude Code, `AGENTS.md`, `CLAUDE.md`, hooks, MCP, permissions/settings, token/context management, AI agent security, AI agent verification 관련 글은 KR/EN 병행 발행을 기본으로 한다.
- 템플릿/체크리스트/reference/how-to 성격의 글도 KR/EN 병행 발행을 기본으로 한다.
- Rust/DevOps/Security 일반 글은 한국어 우선으로 발행하고, AI agent 운영/보안과 직접 연결되는 경우에만 영어판을 함께 발행한다.
- 짧은 메모성 글이나 한국어 독자 맥락에 강하게 의존하는 글은 영어판을 무리하게 만들지 않는다.

## English Investment Priority

1. 템플릿/체크리스트
2. `AGENTS.md` / `CLAUDE.md` 관련 글
3. Codex / Claude Code 운영 글
4. hooks / MCP / permissions/settings 보안 글
5. AI agent 검증/postmortem 글
6. Rust/DevOps 일반 글

## Checks Before KR/EN Changes

- 기존 URL, slug, permalink를 바꾸지 않는다.
- 한국어/영어 pair가 실제로 동등한지 확인한다.
- `lang`, `translation_key`, `permalink`, `description`을 확인한다.
- build 후 sample page에서 canonical URL이 자기 자신인지 확인한다.
- 대응 pair가 있으면 `hreflang="ko"`, `hreflang="en"`, `hreflang="x-default"` 출력이 맞는지 확인한다.

## Do Not

- 기존 영어판 일괄 삭제 금지.
- 기존 영어판 폐기 금지.
- 영어판을 한국어판으로 canonical 처리 금지.
- 동등하지 않은 페이지끼리 `hreflang` 연결 금지.
- 모든 글을 기계적으로 영어화하느라 핵심 허브 보강을 미루지 말 것.
- 기존 URL, slug, permalink 변경 금지.
