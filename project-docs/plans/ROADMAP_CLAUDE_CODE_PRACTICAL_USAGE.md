# Claude Code Practical Usage Roadmap

## Snapshot

- 검토 기준일: 2026-04-29
- 목적: `development` 아래 `ai` 허브에 연결할 "Claude Code 실전 활용" 10편 연재 구조를 보관한다.
- 현재 상태: Claude Code 01~10 한국어 포스트를 `_posts/`에 반영했다. Codex 실전 활용 10편이 끝난 다음날인 2026-05-07부터 2026-05-16까지 하루 1편씩 예약한다.
- 권장 구조: `section: development`, `topic_key: ai`
- 권장 시리즈 제목: `Claude Code 실전 활용`
- 독자 전제: Codex 실전 활용 또는 AI 하네스 엔지니어링의 기본 개념을 이미 알고 있는 독자를 대상으로 한다.
- 운영 원칙: Claude Code를 기능 목록이 아니라 `CLAUDE.md`, rules, skills, settings, permissions, hooks, MCP, subagent가 만드는 운영 구조로 설명한다.

## Scope

- 포함: Claude Code 운영 계층, `CLAUDE.md`, `AGENTS.md` 연동, rules와 skills 분리, settings와 permissions, hooks, MCP, context budget, subagent, 프로젝트 운영 템플릿
- 제외: 모델 성능 비교, 특정 유료 플랜 비교, Claude Code와 다른 도구의 우열 비교, 검증하지 않은 최신 기능 단정
- 메모: OpenAI Codex 글과 중복되는 하네스 설명은 짧게 연결하고, Claude Code 고유의 문서·설정 계층에 집중한다.

## Proposed Sequence

1. Claude Code 01. Claude Code를 기능이 아니라 운영 구조로 이해하기
2. Claude Code 02. `CLAUDE.md`는 어디까지 써야 하는가
3. Claude Code 03. `AGENTS.md`가 있는 저장소에서 Claude Code를 함께 쓰는 법
4. Claude Code 04. rules와 skills로 지시를 언제 로드할지 나누기
5. Claude Code 05. settings와 permissions로 작업 경계 고정하기
6. Claude Code 06. hooks로 검증과 보호 장치를 자동화하기
7. Claude Code 07. MCP로 외부 문맥을 붙여 넣지 않고 연결하기
8. Claude Code 08. 긴 로그, 이슈, auto memory를 문맥 예산 안에서 다루기
9. Claude Code 09. Claude Code subagent는 언제 써야 하는가
10. Claude Code 10. Claude Code 프로젝트 적용용 운영 템플릿

## Calendar

| Date | Lang | Topic | Slug |
| --- | --- | --- | --- |
| 2026-05-07 | ko | Claude Code 01. Claude Code를 기능이 아니라 운영 구조로 이해하기 | claude-code-as-operating-structure |
| 2026-05-08 | ko | Claude Code 02. `CLAUDE.md`는 어디까지 써야 하는가 | how-far-should-claude-md-go |
| 2026-05-09 | ko | Claude Code 03. `AGENTS.md`가 있는 저장소에서 Claude Code를 함께 쓰는 법 | use-claude-code-with-agents-md |
| 2026-05-10 | ko | Claude Code 04. rules와 skills로 지시를 언제 로드할지 나누기 | split-instructions-with-rules-and-skills |
| 2026-05-11 | ko | Claude Code 05. settings와 permissions로 작업 경계 고정하기 | fix-claude-code-boundaries-with-settings-and-permissions |
| 2026-05-12 | ko | Claude Code 06. hooks로 검증과 보호 장치를 자동화하기 | automate-validation-and-guardrails-with-hooks |
| 2026-05-13 | ko | Claude Code 07. MCP로 외부 문맥을 붙여 넣지 않고 연결하기 | connect-external-context-with-mcp |
| 2026-05-14 | ko | Claude Code 08. 긴 로그, 이슈, auto memory를 문맥 예산 안에서 다루기 | handle-logs-issues-and-auto-memory-with-context-budget |
| 2026-05-15 | ko | Claude Code 09. Claude Code subagent는 언제 써야 하는가 | when-to-use-claude-code-subagents |
| 2026-05-16 | ko | Claude Code 10. Claude Code 프로젝트 적용용 운영 템플릿 | claude-code-project-operations-template |

## Planning Notes

- 각 글은 `검증 기준일`, 공식 문서 확인일, 직접 재현 여부, 한계와 예외를 분리한다.
- Claude Code 공식 문서의 URL, 설정 키, 기능명은 버전 민감 정보이므로 발행 전 다시 확인한다.
- 영어 미러는 현재 `_posts/` 일정에 넣지 않는다. 필요해지면 Codex/Git처럼 별도 날짜를 배정하고 `translation_key`를 공유한다.
- 네이버/티스토리 파생본은 `content/posts/`와 `doc/channel-posting/` 규칙에 맞춰 별도로 관리한다.

## Update Triggers

- Claude Code 글을 영어 미러까지 확장하기로 한 경우
- `CLAUDE.md`, rules, skills, settings, hooks, MCP, subagent 공식 문서 구조가 바뀐 경우
- 예약 날짜나 `topic_key`를 바꾸는 경우
- 실제 `_posts/` 파일을 추가, 삭제, 이름 변경하는 경우
