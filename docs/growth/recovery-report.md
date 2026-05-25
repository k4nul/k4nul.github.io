# Recovery Report

검증 기준일: 2026-05-25

## 운영 공백 기간

- 마지막 운영 기록: `docs/growth/daily-change-log.md`의 2026-05-15 항목.
- 복구 대상 기간: 2026-05-16부터 2026-05-25까지.
- 현재 기준: 2026-05-25 19:48 KST 확인.

## 공백 기간 동안 발행된 글

| Date | Post group | Count | KR/EN status |
| --- | --- | --- | --- |
| 2026-05-16 | Claude Code 프로젝트 운영 템플릿 | 1 | KR only |
| 2026-05-17~2026-05-24 | Git 01~08 | 16 | 8 KR/EN pairs |
| 2026-05-25 | Jenkins 01 | 2 | 1 KR/EN pair |

## 발행 후 처리가 누락되었던 글

- 2026-05-16 `claude-code-project-operations-template`: 공개 허브/Start Here/템플릿 페이지 반영이 누락되어 있었다.
- 2026-05-17~2026-05-24 Git 01~08 KR/EN pair: 각 글 본문에 관련 공개 글, DevOps hub, PR/MR/검증 경로 링크가 부족했다.
- 2026-05-25 Jenkins 01 KR/EN pair: DevOps hub와 Git/Docker 선행 글로 이어지는 관련 링크가 부족했다.

## 이번에 복구한 내부링크

- `/ai-engineering/`: Claude Code 프로젝트 운영 템플릿과 PR/MR 리뷰 기준을 추가했다.
- `/start-here/`: Claude Code 운영 템플릿과 PR/MR 리뷰 기준을 문제별 경로에 반영했다.
- `/ai-engineering/templates/`: Claude Code 프로젝트 운영 템플릿을 함께 읽을 글에 추가했다.
- `/devops/`, `/en/development/devops/`: 공개된 Docker, Git 01~08, Jenkins 01 링크를 추천 흐름에 반영했다.
- Git 01~08 KR/EN pair: 각 글에 DevOps hub와 공개된 전후 Git/Jenkins 관련 글 링크를 추가했다.
- Jenkins 01 KR/EN pair: DevOps hub, Git PR/MR, Git tag/release, Docker registry 글 링크를 추가했다.
- 기존 Claude Code 공개 글 4개: Claude Code 프로젝트 운영 템플릿으로 들어오는 링크를 추가했다.

## 다음 14일 예약 글 중 보강한 글

- 2026-05-26~2026-06-03 Jenkins 02~10 KR/EN pair: 현재 공개된 Jenkins 01, Git PR/MR, Docker registry, DevOps hub로 연결했다.
- 2026-06-04~2026-06-08 Kubernetes 01~05 KR/EN pair: 현재 공개된 Docker/Jenkins/DevOps 글로 연결했다.
- 미래 글끼리의 직접 링크는 추가하지 않았다.
- title 대량 변경은 하지 않았고, 약한 제목 후보는 `schedule-adjustment-candidates.md`와 인벤토리 리스크로 유지했다.

## KR/EN 보강이 필요한 글

- 2026-05-16 Claude Code 프로젝트 운영 템플릿은 KR only다. 기존 정책상 즉시 영어판을 새로 만들지 않고, 핵심축 EN 후보로만 남긴다.
- Git 01~08과 Jenkins 01~K8S 05는 KR/EN pair가 있으며 같은 `translation_key`를 유지한다.
- Jenkins/Kubernetes 예약 글의 영어 품질은 schedule-adjustment candidate에 남아 있는 `EN quality review needed` 상태를 유지한다.

## 일정 조정 후보

- 2026-05-25~2026-06-03 Jenkins KR/EN daily series는 밀도가 높지만 일정은 변경하지 않았다.
- 2026-06-04~2026-06-13 Kubernetes KR/EN daily series도 밀도가 높지만 일정은 변경하지 않았다.
- 일정 조정은 `docs/growth/schedule-adjustment-candidates.md`에 후보로만 기록한다.

## Search Console 색인 요청 후보

- 상세 목록: `docs/growth/indexing-candidates.md`
- 후보 범위: 2026-05-16 Claude Code 운영 템플릿, 2026-05-17~2026-05-24 Git 01~08 KR/EN pair, 2026-05-25 Jenkins 01 KR/EN pair.
- Search Console 수치: 사용자 입력 필요.

## 남은 리스크

- Search Console/GA4 데이터가 없어 성과 판단은 하지 않았다.
- 공개 페이지에서 다음 14일 미래 글 링크가 생기지 않았는지 `_site` HTML 기준으로 확인했고, 예약 slug는 발견되지 않았다.
- Jenkins/Kubernetes 예약 글 제목은 검색 의도 앞세우기 관점에서 약하지만, 대량 제목 변경 금지 원칙 때문에 이번에는 변경하지 않았다.
- Claude Code 프로젝트 운영 템플릿의 EN 대응 글은 없다. 삭제나 임의 생성 대신 후보로만 유지한다.
- `npm.cmd run seo:audit`는 실패했다. 주요 원인은 기존 redirect/thin page warning과 `AI` 생성 경로 대 `/ai/...` canonical mismatch이며, 이번 작업 범위를 넘어서는 구조 개선 후보로 둔다.

## 내일 작업 후보

1. 2026-05-26 Jenkins 02 KR/EN 발행 후 공개 URL, canonical/hreflang, DevOps hub 반영 여부 확인.
2. Jenkins 03~05의 제목/description을 대량 변경 없이 검색 의도 후보로만 재검토.
3. K8S 06~10 KR/EN 예약 글에 현재 공개된 글만 링크하는 pre-publish 보강.
4. 2026-06-16 agent trace KR/EN pair의 AI Engineering/Start Here 연결 후보 점검.
5. Search Console 입력값이 있으면 Git/Jenkins 색인 후보의 노출/클릭/CTR/평균 순위 기록.
