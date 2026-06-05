# Daily Change Log

## 2026-06-05

### 오늘의 목표

- 금요일 작업으로 예약 큐에서 실험/postmortem 성격에 가까운 글이 오늘 즉시 보강 대상인지 다시 확인한다.
- 이미 2026-05-29에 사전 보강한 `2026-06-16` agent trace KR/EN pair를 중복 수정하지 않고, 가까운 후속 후보만 candidate-only로 정리한다.
- publish date, filename slug, permalink, public 링크 구조는 변경하지 않는다.

### 변경 파일

- `docs/growth/schedule-adjustment-candidates.md`: 오늘 금요일 검토 결과, 즉시 재작업할 가까운 실험/postmortem형 예약 글이 없다는 판단과 다음 후보(`2026-06-16`, `2026-06-23`, `2026-06-30`)를 candidate-only로 기록했다.
- `docs/growth/daily-change-log.md`: 오늘 문서형 Friday handoff와 검증 결과를 기록했다.

### 변경 이유

- `docs/growth/daily-codex-routine.md`의 금요일 규칙은 예약된 실험/postmortem 글을 보강하되, 맞는 글이 없으면 후보만 기록하도록 한다.
- 이번 주의 실제 활성 큐는 `K8S 02~10` KR/EN pair 중심이고, 금요일 성격에 더 가까운 `2026-06-16` agent trace pair는 이미 2026-05-29에 description, 요약, 관련 공개 링크 기준으로 사전 보강이 끝나 있다.
- 따라서 오늘은 같은 예약 글을 반복 수정하지 않고, 다음 품질 점검 후보와 재확인 시점을 문서에 남기는 편이 더 정확하다.

### 실행한 검증 명령

- `git branch --show-current`: `master`
- `git status --short`: 작업 시작 시 출력 없음.
- `git diff --check`: 통과
- `bundle exec jekyll build`: 미실행. `docs/growth/` 문서만 바꾼 documentation-only 작업이라 public build 산출물 영향이 없다.
- `npm run check:links:local`: 미실행. public 링크 구조 변경이 없다.

### 결과

- 오늘 금요일 lane은 candidate-only 기록 작업으로 마감했다.
- `2026-06-16` agent trace, `2026-06-23` guardrails, `2026-06-30` prompt injection KR/EN pair를 다음 AI/security 품질 점검 후보로 고정했다.
- publish date, filename slug, permalink, public 허브 링크는 변경하지 않았다.

### 다음 작업

- 2026-06-06 토요일: 실제 공개된 글만 기준으로 `/devops/`와 `/en/development/devops/`에 `K8S 02` 반영 여부를 확인한다.
- 2026-06-08 월요일: `K8S 06~10` KR/EN pair의 title tone, description parity, future-link 안전성을 다시 점검한다.
- 2026-06-12 또는 2026-06-15: `2026-06-16` agent trace KR/EN pair의 canonical, hreflang, meta description 출력값 최종 확인을 준비한다.
- 2026-06-19 금요일 후보: `2026-06-23` guardrails KR/EN pair의 사실/관찰/한계 분리와 EN terminology parity를 점검한다.

### 남은 리스크

- Search Console 데이터: 사용자 입력 필요
- GA4 데이터: 사용자 입력 필요
- 링크 검증 미실행 사유: public 링크 구조 변경 없음
- build 실패 시 파일/플러그인/오류: 해당 없음. 이번 작업은 build 미실행
- 오늘 판단은 레포 내 예약 큐 문서와 기존 사전 보강 기록 기준이므로, 실제 우선순위는 사용자 제공 Search Console/GA4 입력이 들어오면 바뀔 수 있다.

## 2026-06-04

### 오늘의 목표

- 목요일 작업으로 `K8S 01` KR/EN pair의 실제 공개 여부를 build 기준으로 확인한다.
- 아직 공개되지 않은 `K8S 01` public 링크는 보류하고, 이미 공개된 Jenkins 05~10 KR/EN 글을 DevOps 허브에 반영한다.
- `K8S 01` 예약 글에는 공개된 `Jenkins 10` 경계 글을 연결해 publication-time 관련 링크를 준비한다.
- 미래 K8S 글은 공개 전까지 허브와 공개 글에서 직접 링크하지 않는다.

### 변경 파일

- `_pages/development-devops.md`: 공개된 Jenkins 05~10 한국어 글을 DevOps 추천 흐름에 추가했다. `K8S 01` public 링크는 build exclusion 확인 후 보류했다.
- `_pages/en-development-devops.md`: 공개된 Jenkins 05~10 EN 글을 DevOps 추천 흐름에 추가했다. `K8S 01` public 링크는 build exclusion 확인 후 보류했다.
- `_posts/2026-06-04-kubernetes-what-it-solves-and-does-not.md`: 관련 글에 이미 공개된 `Jenkins 10` 한국어 글을 추가했다.
- `_posts/2026-06-04-kubernetes-what-it-solves-and-does-not-en.md`: related posts에 이미 공개된 `Jenkins 10` EN 글을 추가했다.
- `docs/growth/daily-change-log.md`: 오늘 post-publish 링크 작업과 검증 결과를 기록했다.

### 변경 이유

- `docs/growth/weekly-execution-plan.md`는 2026-06-04 작업으로 `K8S 01` 공개 후 public URL이 확인되면 DevOps 허브 반영을 검토하라고 지정했다.
- 2026-06-04 08:01 KST 기준 `bundle exec jekyll build`는 `K8S 01`을 future-dated post로 제외했다. 따라서 public hub와 이미 공개된 `Jenkins 10` 글에서 `K8S 01`로 연결하지 않았다.
- DevOps 허브의 Jenkins 추천 흐름은 `Jenkins 04`에서 멈춰 있었으므로, 이미 공개된 Jenkins 05~10까지 보강했다.
- `K8S 01` 자체는 아직 build output에 없으므로, publication-time 준비로 공개된 `Jenkins 10`으로 향하는 관련 링크만 추가했다.

### 실행한 검증 명령

- `git branch --show-current`: 빈 출력. maintainer temporary worktree가 detached HEAD로 생성되었기 때문이다.
- `git status --short --branch`: `## HEAD (no branch)`
- `git rev-parse HEAD`와 `git rev-parse master`: 둘 다 `e46a92f823bdd35a2858ada33dc6a5628a7fe7e5`
- `date '+%F %T %Z %z'`: `2026-06-04 08:01:29 KST +0900`
- `git diff --check`: 통과
- `bundle exec jekyll build`: 성공
- `npm run check:links:local`: 성공

### 결과

- `/devops/`와 `/en/development/devops/`에서 공개된 Jenkins 05~10을 추천 흐름으로 찾을 수 있게 되었다.
- `K8S 01` KR/EN 예약 글은 공개 시점에 이미 공개된 `Jenkins 10` 경계 글로 이어진다.
- `K8S 01`과 미래 글인 `K8S 02` 이후는 공개 허브와 공개 글에 직접 링크하지 않았다.

### 다음 작업

- 2026-06-04 09:00 KST 이후 `K8S 01`이 build output에 포함되는 것을 확인한 뒤 DevOps 허브와 `Jenkins 10` 관련 글에 추가할지 판단한다.
- 2026-06-05 이후 `K8S 02`가 공개되면 DevOps 허브와 `K8S 01` 관련 글에 추가할지 공개 URL 기준으로 판단한다.
- 2026-06-08 월요일에는 `K8S 06~10` 발행 전 점검을 다시 수행한다.
- 2026-06-11 `K8S 08` 공개 후 AI Engineering/templates 연결이 실제로 맞는지 검토한다.
- Search Console/GA4 데이터가 제공되면 제목/description 리라이트 후보를 데이터 기준으로 재정렬한다.

### 남은 리스크

- Search Console 데이터: 사용자 입력 필요
- GA4 데이터: 사용자 입력 필요
- `origin/master` ref는 temporary bare clone에 없어서 비교하지 못했고, local `master`와 detached `HEAD` 일치만 확인했다.
- 2026-06-04 08:01 KST build에서는 `K8S 01`이 future-dated post로 제외되므로, `K8S 01` public hub 연결은 09:00 KST 이후 재확인이 필요하다.
- 링크 검증은 local build output 기준이며, 실제 운영 반영은 runner publish 이후 확인해야 한다.

## 2026-06-01

### 오늘의 목표

- 월간 Codex automation lane으로 최근 28일/월간 성장 운영을 좁은 문서 감사 범위에서 리뷰한다.
- Search Console/GA4 데이터가 레포에 없다는 사실을 명시하고, 미래 예약 큐의 균형, 핵심 주제 커버리지, KR/EN parity 후보, stale evergreen 후보, 다음 달 우선순위를 growth 문서에 기록한다.
- publish date, filename slug, permalink, public 링크 구조는 건드리지 않는다.

### 변경 파일

- `docs/growth/content-backlog.md`: 월간 리뷰 스냅샷, data availability, queue balance, stale evergreen watchlist, 다음 달 우선순위 5개를 기록했다.
- `docs/growth/schedule-adjustment-candidates.md`: 월간 리뷰 기준의 candidate-only 메모를 추가하고, 일정 변경 후보가 없음을 명시했다.
- `docs/growth/daily-change-log.md`: 월간 automation lane 수행 결과를 기록했다.

### 변경 이유

- `docs/growth/prompt-bank.md`의 Monthly Review Prompt는 Search Console/GA4 데이터가 있을 때 성과를 읽도록 되어 있지만, 현재 레포에는 월간 입력값이 없다.
- 데이터가 없더라도 queue balance, core-topic coverage, KR/EN parity candidate, stale evergreen candidate, next-month priority는 레포 기준으로 좁게 정리할 수 있다.
- future queue는 KR/EN 균형이 유지되지만, `2026-08` 이후 Rust/DevOps 비중이 높아져 핵심 AI 성장축은 템플릿/허브/evergreen 리라이트로 보완할 필요가 있다.

### 실행한 검증 명령

- `git branch --show-current`: `master`
- `git status --short`: 작업 시작 시 출력 없음.
- `git diff --check`: 통과
- `bundle exec jekyll build`: 미실행. `docs/growth/` 문서만 바꾼 documentation-only 작업이라 public build 산출물 영향이 없다.
- `npm run check:links:local`: 미실행. public 링크 구조 변경이 없다.

### 결과

- Search Console 데이터: `사용자 입력 필요`
- GA4 데이터: `사용자 입력 필요`
- 월간 사용자, non-brand query 수, 평균 순위 30위 안쪽 페이지 수: `사용자 입력 필요`
- future queue는 `130 posts / 65 KR/EN pairs`로 균형을 유지한다.
- `2026-06`과 `2026-07`은 AI agent 운영·보안 교차 주제가 강하지만, `2026-08` 이후는 Rust/DevOps 비중이 높아져 exact `AGENTS.md`/`CLAUDE.md`/Codex template refresh는 backlog 자산 보강으로 메워야 한다.
- 새 publish-date 변경 후보는 기록하지 않았고, stale evergreen watchlist와 다음 달 우선순위 5개만 남겼다.

### 다음 작업

- 2026-06-02 이후 공개되는 `2026-06-16`, `2026-06-23`, `2026-06-25`, `2026-06-30`, `2026-07-14` KR/EN pair를 post-publish 링크 및 EN parity 우선 후보로 유지한다.
- `/ai-engineering/templates/`에서 `AGENTS.md`, `CLAUDE.md`, Codex 작업 요청 템플릿 자산 보강을 다음 달 상위 작업으로 유지한다.
- stale evergreen watchlist인 `2026-04-21`, `2026-04-30`, `2026-05-06`, `2026-05-11`, `2026-05-12`, `2026-05-13` 공개 글은 Search Console 입력 전까지 좁은 범위 감사 후보로만 둔다.
- Search Console/GA4 월간 입력값을 받으면 Week 4 또는 Monthly Review prompt로 넘길 page/query 표를 준비한다.

### 남은 리스크

- Search Console 데이터: 사용자 입력 필요
- GA4 데이터: 사용자 입력 필요
- 링크 검증 미실행 사유: public 링크 구조 변경 없음
- build 실패 시 파일/플러그인/오류: 해당 없음. 이번 작업은 build 미실행
- 월간 리뷰는 레포에 있는 queue/문서 데이터만 사용했으므로 실제 검색 성과 우선순위는 사용자 제공 Search Console/GA4 입력 후 재정렬해야 한다.

## 2026-05-31

### 오늘의 목표

- 일요일 작업으로 Search Console/GA4 데이터 부재를 명시하고, 2026-06-01~2026-06-13 예약 큐를 다시 읽어 다음 7-14일 창의 한 구간만 보강한다.
- 미래 글 링크, publish date, filename slug, permalink는 건드리지 않고 `K8S 06~10` KR/EN pair의 큐 준비 상태만 문서화한다.

### 변경 파일

- `docs/growth/daily-change-log.md`: 2026-05-31 일요일 점검 결과와 `K8S 06~10` 집중 보강 이유를 기록했다.
- `docs/growth/weekly-execution-plan.md`: 다음 7-14일 창에서 선택한 `K8S 06~10` 큐 준비 작업을 명시했다.
- `docs/growth/scheduled-posts-inventory.md`: 미래 큐 기준일과 집계 범위를 2026-05-31 기준으로 갱신하고 `K8S 06~10` 점검 메모를 추가했다.
- `docs/growth/scheduled-posts-calendar.md`: 현재 future queue 창을 2026-06-01~2026-06-13 기준으로 갱신하고 `K8S 06~10` 사전 메모를 추가했다.

### 변경 이유

- `docs/growth/daily-codex-routine.md`의 일요일 규칙에 따라 Search Console/GA4 분석 대신 다음 주 예약 글 운영 후보만 준비했다.
- 레포 내 Search Console/GA4 입력값은 여전히 없으므로 수치를 추정하지 않고 `사용자 입력 필요`로 유지했다.
- 다음 14일 예약 큐는 `Jenkins 08~10`, `K8S 01~10`으로 이어지며, 그중 `2026-06-09~2026-06-13`의 `K8S 06~10`은 아직 주간 메모가 얕았다.
- `K8S 07`과 `K8S 08`은 DevOps를 넘어 각각 AI agent security, AI agent verification과 연결될 수 있어 KR/EN 큐 메타데이터 정합성을 지금 맞춰 두는 편이 안전하다.

### 실행한 검증 명령

- `git branch --show-current`: `master`
- `git status --short`: 작업 시작 시 출력 없음.
- `bundle exec jekyll build`: 미실행. `docs/growth/` 문서만 바꾼 documentation-only 작업이라 public build 산출물 영향이 없다.
- `npm run check:links:local`: 미실행. 링크 구조 변경이 없다.
- `git diff --check`: 통과

### 결과

- Search Console 데이터: `사용자 입력 필요`
- GA4 데이터: `사용자 입력 필요`
- 미래 큐 집계를 2026-05-31 기준으로 갱신했다. 현재 future queue는 130 posts / 65 KR/EN pairs다.
- 다음 14일 창은 `2026-06-01~2026-06-13` 26 posts / 13 KR/EN pairs로 정리했다.
- 선택한 주간 개선 범위는 `2026-06-09~2026-06-13`의 `K8S 06~10`이며, 내부 future-link 위험은 보이지 않았고 `K8S 08`의 KR/EN 포지셔닝 메모를 맞췄다.

### 다음 작업

- 2026-06-01 월요일: `Jenkins 08~10`과 `K8S 01~04` KR/EN pair의 title, description, TL;DR, 선행 공개 링크, future-link 안전성을 점검한다.
- 2026-06-02 화요일: `Jenkins 09. Common Jenkins Failures and Root Cause Separation` KR/EN pair를 리라이트 후보로 다룬다.
- 2026-06-03 수요일: `agent trace` 및 guardrail 계열 예약 글이 연결할 수 있는 incident/trace 체크리스트 보강 여부를 검토한다.
- 2026-06-08 월요일: `K8S 06~10` KR/EN pair의 title tone, description parity, post-publish 연결 후보를 다시 확인한다.
- 2026-06-11 목요일: `K8S 08` 공개 후 AI Engineering/templates 연결이 실제로 맞는지 공개 URL 기준으로만 판단한다.

### 남은 리스크

- Search Console 데이터: 사용자 입력 필요
- GA4 데이터: 사용자 입력 필요
- 링크 검증 미실행 사유: 링크 구조 변경 없음
- build 실패 시 파일/플러그인/오류: 해당 없음. 이번 작업은 build 미실행
- 예약 큐 검토는 문서 기준 후보 정리까지만 끝냈고, 실제 본문 리라이트와 허브 반영은 각 발행일/요일 작업에서 다시 확인해야 한다.
- `K8S 07`, `K8S 08`의 AI/security 성격은 현재 문서 메모 수준이며, 공개 후 실제 허브 연결 적합성은 다시 검토해야 한다.

## 2026-05-30

### 오늘의 목표

- 토요일 작업으로 오늘 공개된 `Jenkins 06` KR/EN pair를 공개 허브에서 안전하게 찾을 수 있게 `/ai-engineering/`와 `/en/development/ai/`를 보강한다.
- 미래 글 링크를 추가하지 않고, 2026-05-30 기준 실제 공개된 Jenkins 글만 반영한다.

### 변경 파일

- `_pages/development-ai.md`: AI agent 검증 경로에 오늘 공개된 `Jenkins 06. Jenkinsfile 읽기: agent, stages, steps, post를 어떻게 구분할까` 링크를 추가했다.
- `_pages/en-development-ai.md`: EN AI Engineering hub의 verification path에 오늘 공개된 `Jenkins 06. How to Read a Jenkinsfile: agent, stages, steps, and post` 링크를 추가했다.
- `docs/growth/daily-change-log.md`: 오늘 공개 허브 반영 작업과 검증 결과를 기록했다.

### 변경 이유

- `docs/growth/daily-codex-routine.md`의 토요일 규칙에 따라 공개 허브 1개 묶음만 작게 보강했다.
- `Jenkins 06`은 2026-05-30 09:00 KST 공개 글이며, Jenkinsfile을 실행 계획과 후처리 기준으로 읽는 관점이 AI agent 작업 검증 경로와 맞닿아 있다.
- 기존 AI Engineering 허브는 PR/MR 리뷰 기준까지만 연결하고 있었고, agent가 만든 CI 변경을 읽는 공개 글이 바로 노출되지 않았다.

### 실행한 검증 명령

- `git branch --show-current`: `master`
- `git status --short`: 작업 시작 시 출력 없음.
- `git diff --check`: 통과
- `bundle exec jekyll build`: 성공. 미래 글은 expected future-date skip으로 제외됐고, 기존 Minimal Mistakes Sass division deprecation warning은 유지됐다.
- `npm run check:links:local`: 성공. Source pages 182, internal link references 11081, unique internal targets 200, broken targets 0.

### 결과

- `/ai-engineering/`와 `/en/development/ai/`에서 Jenkinsfile 구조 읽기 글이 AI agent verification 경로의 공개 글로 바로 발견되게 된다.
- Jenkins 07 이후 글은 여전히 future-dated post이므로 공개 허브에는 추가하지 않았다.

### 다음 작업

- `/start-here/`와 `/en/start-here/`에 오늘 공개된 Jenkins 06을 넣을 가치가 있는지 경로 적합성만 검토.
- 2026-06-02 공개 전 `Jenkins 09` KR/EN pair를 금요일 후보로 점검.
- 2026-06-16 공개 예정 `agent trace` KR/EN pair를 AI Engineering 허브의 high-priority post-publish 후보로 유지.

### 남은 리스크

- Search Console 데이터: 사용자 입력 필요
- GA4 데이터: 사용자 입력 필요

## 2026-05-28

### 오늘의 목표

- 목요일 작업으로 최근 공개된 Jenkins 글을 공개 허브에서 안전하게 찾을 수 있게 KR/EN DevOps 허브의 내부링크를 정리한다.
- 미래 글 링크를 추가하지 않고, 2026-05-28 기준 공개된 Jenkins 04까지만 반영한다.

### 변경 파일

- `_pages/development-devops.md`: DevOps 허브의 Jenkins 추천 흐름에 오늘 공개된 `Jenkins 04. Freestyle Job과 Pipeline은 무엇이 다른가` 링크를 추가했다.
- `_pages/en-development-devops.md`: EN DevOps 허브의 Jenkins 추천 흐름에 오늘 공개된 `Jenkins 04. Freestyle Job vs Pipeline` 링크를 추가했다.
- `docs/growth/daily-change-log.md`: 오늘 허브 내부링크 정리 작업과 검증 결과를 기록했다.

### 변경 이유

- `docs/growth/daily-codex-routine.md`의 목요일 규칙에 따라 최근 공개 글의 post-publish 내부링크 정리를 선택했다.
- KR/EN DevOps 허브는 Jenkins 03까지만 노출하고 있었고, 2026-05-28 공개 글 Jenkins 04가 허브에서 바로 발견되지 않았다.
- 2026-05-29 이후 Jenkins 글은 여전히 future-dated post이므로 허브 문구는 유지하고 공개된 Jenkins 04까지만 추가했다.

### 실행한 검증 명령

- `git branch --show-current`: `master`
- `git status --short`: 작업 시작 시 출력 없음.
- `git diff --check`: 통과
- `bundle exec jekyll build`: 성공. 2026-05-29 이후 미래 글은 expected future-date skip으로 제외됨. 기존 Sass division deprecation warning은 유지됨.
- `npm run check:links:local`: 성공. Source pages 178, internal link references 10807, unique internal targets 196, broken targets 0.

### 결과

- `/devops/`와 `/en/development/devops/`에서 Jenkins 04 공개 글까지 바로 접근할 수 있게 됐다.
- 허브 문구는 아직 비공개인 Declarative Pipeline, Jenkinsfile, 장애 분리 글을 future-link 없이 예고만 하도록 유지했다.
- KR/EN 허브가 동일한 공개 범위를 반영하도록 정리됐다.

### 다음 작업

- 2026-05-29 공개 후 KR/EN DevOps 허브에 `Jenkins 05`를 안전하게 반영할지 확인.
- 2026-05-30 공개 후 `Jenkins 06`이 AI coding agent operations와 연결되는 지점을 `/ai-engineering/` 후보로 검토.
- 2026-06-02 공개 전 `Jenkins 09` KR/EN pair의 실패 원인 분리 표현을 금요일 후보로 점검.

### 남은 리스크

- Search Console 데이터: 사용자 입력 필요
- GA4 데이터: 사용자 입력 필요
- 기존 theme Sass deprecation warning은 이번 변경과 무관하며 그대로 남아 있다.

## 2026-05-26

### 오늘의 목표

- 화요일 작업으로 다음 7일 예약 글 중 `Jenkins 06` KR/EN 쌍의 제목, description, 첫 문단, 내부링크를 작게 보강한다.
- publish date, filename slug, permalink는 바꾸지 않고 검색 의도와 읽기 흐름만 선명하게 만든다.

### 변경 파일

- `_posts/2026-05-30-jenkinsfile-agent-stages-steps-post.md`: KR 제목과 description을 검색 의도 중심으로 다듬고, 요약/문제 정의에서 Jenkinsfile 읽기 관점을 더 분명히 했으며, 발행 순서상 안전한 선행 Jenkins 05 링크를 추가했다.
- `_posts/2026-05-30-jenkinsfile-agent-stages-steps-post-en.md`: EN 제목과 description을 같은 기준으로 조정하고, opening summary/problem definition/related posts를 KR과 대응되게 보강했다.
- `docs/growth/daily-change-log.md`: 오늘 작업 결과를 기록했다.

### 변경 이유

- `docs/growth/daily-codex-routine.md`의 화요일 규칙에 따라 새 글을 만들지 않고 다음 7일 예약 글 1개 KR/EN pair만 리라이트 대상으로 골랐다.
- `Jenkins 06`은 일정 문서에서 weak-title candidate로 남아 있었고, 현재 제목은 문법 항목 나열에 가까워 검색 의도가 약했다.
- 링크는 공개 글과 발행 순서상 앞선 `2026-05-29` Jenkins 05 글만 추가해 future-link 안전성을 유지했다.

### 실행한 검증 명령

- `git branch --show-current`: `master`
- `git status --short`: 작업 시작 시 출력 없음.
- `bundle exec jekyll build`: 실패. `/bin/bash: line 1: bundle: command not found`
- `npm run check:links:local`: 실패. 내부 스크립트가 `bundle exec jekyll build`를 먼저 호출하며 `sh: 1: bundle: not found`
- `git diff --check`: 통과

### 결과

- `Jenkins 06` KR/EN 예약 글의 제목이 "Jenkinsfile을 어떻게 읽을까" 검색 의도에 맞게 정리됐다.
- 두 글의 첫 문단이 문법 항목 나열보다 실행 구조 해석에 초점을 두도록 바뀌었다.
- 관련 링크에 `Jenkins 05`를 추가해 Declarative Pipeline 글에서 Jenkinsfile 읽기 글로 이어지는 선행 학습 경로를 만들었다.

### 다음 작업

- 2026-05-27 예약 글 `Jenkins 03` KR/EN 쌍의 title/description/첫 문단 점검.
- 2026-05-28 예약 글 `Jenkins 04` KR/EN 쌍의 비교 의도와 내부링크 점검.
- Jenkins 02~10 예약 글의 EN title tone 일관성만 따로 묶을지 주간 프롬프트 후보로 검토.

### 남은 리스크

- Search Console 데이터: 사용자 입력 필요
- GA4 데이터: 사용자 입력 필요
- 링크 검증 미실행 사유: 로컬 link check 스크립트가 `bundle exec jekyll build`에 의존하는데 현재 shell에 `bundle`이 없다.
- build 실패 시 파일/플러그인/오류: `bundle` 실행 파일 부재로 Jekyll build 자체를 시작하지 못했다.

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

## 2026-05-29

### 오늘의 목표

- 금요일 기준으로 예약된 AI 운영 글 중 incident review와 trace/postmortem 관점에 가까운 `2026-06-16` agent trace KR/EN pair를 점검한다.
- 기존 URL, slug, permalink, publish date는 유지한 채 description, 요약 문장, 관련 공개 링크를 보강한다.
- 미래 글끼리 연결하지 않고, 이미 공개된 AI Engineering 허브/템플릿/관련 글만 사용한다.

### 변경 파일

- `_posts/2026-06-16-what-should-agent-trace-record.md`: KR 예약 글의 description을 구체화하고, incident review 관점 요약과 공개된 관련 글 링크를 추가했다.
- `_posts/2026-06-16-what-should-agent-trace-record-en.md`: EN 예약 글의 description을 구체화하고, approval audit 관점 요약과 공개된 관련 글 링크를 추가했다.
- `docs/growth/daily-change-log.md`: 오늘 작업 결과를 기록했다.

### 변경 이유

- 금요일 작업 기준은 예약된 실험/postmortem 성격 글의 사실/관찰/해석/한계와 검증 기준을 확인하고, 부족하면 좁은 범위에서 보강하는 것이다.
- 이 pair는 기본 구조는 갖춰져 있었지만 search intent가 약한 description과 related-link 부재가 남아 있었다.
- trace 글은 결과 로그보다 approval chain, verification trail, guardrail 경계를 설명하는 운영 글이므로, 이미 공개된 AI Engineering 허브와 인접 검증 글로 안전하게 연결하는 편이 적절하다.

### 실행한 검증 명령

- `git branch --show-current`: `master`
- `git status --short`: 작업 시작 시 변경 없음.
- `bundle exec jekyll build`: 성공. 미래 날짜 예약 글은 expected skip 처리되었고, Minimal Mistakes Sass division deprecation warning은 기존 경고로 유지됨.
- `npm run check:links:local`: 성공. Source pages 180, internal references 10939, unique internal targets 198, broken targets 0.
- `git diff --check`: 통과.

### 결과

- 예약 글 1개 KR/EN pair 범위에서만 수정했다.
- publish date, filename slug, permalink, `translation_key`는 변경하지 않았다.
- 공개 페이지에는 미래 글 링크를 추가하지 않았고, 미래 글 내부에는 이미 공개된 허브/템플릿/관련 글만 연결했다.
- Jekyll build와 로컬 링크 점검 모두 통과했고, 새 broken link는 생기지 않았다.

### 다음 작업

- 2026-06-02 `Jenkins 09` KR/EN pair가 공개되면 AI Engineering 연결이 필요한지 post-publish 기준으로 다시 확인한다.
- 2026-06-16 agent trace pair 발행 직전에 canonical, hreflang, meta description 출력값을 최종 점검한다.
- 2026-06-23 guardrails and approval boundaries KR/EN pair를 다음 금요일 후보로 검토한다.

### 남은 리스크

- Search Console 데이터: 사용자 입력 필요
- GA4 데이터: 사용자 입력 필요
- 링크 검증 미실행 사유: 해당 없음
- build 실패 시 파일/플러그인/오류: 해당 없음

## 2026-05-25

### 오늘의 목표

- 2026-05-16부터 2026-05-25까지의 운영 공백을 복구한다.
- 공백 기간에 발행된 글의 post-publish 내부링크를 복구한다.
- 다음 14일 예약 글의 pre-publish 내부링크와 운영 문서를 재동기화한다.

### 변경 파일

- `_pages/development-ai.md`, `_pages/start.md`, `_pages/ai-agent-templates.md`: 공개된 Claude Code 운영 템플릿과 Git PR/MR 리뷰 글을 AI Engineering 경로에 연결했다.
- `_pages/development-devops.md`, `_pages/en-development-devops.md`: 공개된 Docker, Git 01~08, Jenkins 01 경로를 DevOps 추천 흐름에 반영했다.
- `_posts/2026-05-17*`~`_posts/2026-05-25*`: 공백 기간 발행 글에 관련 공개 글과 허브 링크를 추가했다.
- `_posts/2026-05-26*`~`_posts/2026-06-08*`: 다음 14일 예약 글에 현재 공개된 관련 글만 연결했다.
- `docs/growth/*`: 일일/주간 운영 원칙, 예약 인벤토리/캘린더, 색인 후보, 복구 보고서를 갱신했다.

### 변경 이유

- 최근 며칠 동안 발행 후 허브 반영과 내부링크 작업이 이어지지 않은 상태를 복구했다.
- 예약 글은 공개 페이지에서 아직 링크하지 않고, 글 본문에는 현재 이미 공개된 글만 연결해 발행 시점 404 위험을 줄였다.
- 새 글을 만들지 않고 예약 포스팅 큐 운영을 다시 기본값으로 고정했다.

### 실행한 검증 명령

- `git branch --show-current`: `master`
- `git status --short`: 작업 시작 시 출력 없음.
- `bundle exec jekyll build`: 성공. 2026-05-26 이후 글은 `Skipping: ... has a future date`로 제외됨.
- `npm.cmd run check:links:local`: 성공. Source pages 172, internal references 10393, unique internal targets 190, broken targets 0.
- `git diff --check`: 통과. LF/CRLF warning만 출력됨.
- `_site` 미래 slug 점검: 다음 14일 예약 slug가 `_site` HTML에서 발견되지 않음.
- `npm.cmd run seo:audit`: 실패. 기존 canonical mismatch와 thin redirect warning이 남아 있으며, `AI` 생성 경로와 `/ai/...` canonical 불일치가 포함됨.

### 결과

- 2026-05-16~2026-05-25 발행 글 19개를 복구 대상으로 확인했다.
- 2026-05-26~2026-06-08 예약 글 28개에 공개된 선행 글 링크를 추가했다.
- `docs/growth/indexing-candidates.md`와 `docs/growth/recovery-report.md`를 새로 만들었다.

### 다음 작업

- 2026-05-26 Jenkins 02 발행 후 post-publish 확인.
- K8S 06~10 예약 글 pre-publish 내부링크 보강.
- 2026-06-16 agent trace KR/EN pair의 AI Engineering 연결 후보 점검.

### 남은 리스크

- Search Console 데이터: 사용자 입력 필요
- GA4 데이터: 사용자 입력 필요
- 링크 검증 미실행 사유: 해당 없음
- build 실패 시 파일/플러그인/오류: 해당 없음
- SEO audit 실패: 기존 redirect/thin page warning과 canonical mismatch 49건. 이번 작업의 링크 추가로 새 broken link는 생기지 않았으나, AI category 생성 경로와 canonical 경로 불일치는 별도 구조 개선 후보로 남김.

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
