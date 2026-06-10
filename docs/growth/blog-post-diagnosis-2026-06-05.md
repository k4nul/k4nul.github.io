# 블로그 포스팅 진단 리포트

검증 기준일: 2026-06-05
검사 기준: repository Markdown/MDX inventory, Jekyll front matter, filename date, `published`/`draft` flags, title-body intent heuristic, and manual review of the highest-risk posts.

## 요약

- 전체 검사 파일 수: 669
- 실제 포스팅으로 판단한 글 수: 567
- 공개 글 수: 144 (`_posts`, 2026-06-05 이하, `published: false` 제외)
- 공개 페이지/허브 수: 48 (`_pages`)
- 미공개 글 수: 185 (`content/posts/**/source.md` 184, `_posts` `published: false` 1)
- draft 글 수: 1 (`docs/_drafts/post-draft.md`; 루트 `_drafts` 없음)
- 예약 글 수: 120 (`_posts`, 2026-06-06 이후)
- 2026년 예약 글 수: 90
- 2027년 예약 글 수: 30
- 예시 품질 별도 리뷰 대상: 318
- 예시 점수 낮음: 22
- 예시 점수 매우 낮음: 5
- 수정 필요 글 수: 최소 51
- 우선 수정 대상: Jenkins 설치/초기 설정 원문과 외부 채널 source 4개, K8S 02 KR/EN 원문과 외부 source 4개, GitHub Actions 보안 체크리스트 KR/EN 예약 글과 외부 source 4개, 2027년 예약 글 30개, `published: false`인 Codex `/goal` 글 1개
- 가장 흔한 문제: 실습형 제목인데 앞부분이 의사결정/개념 설명 중심인 글, 예약 글에서 발행 예정일과 검증 기준일이 분리되지 않은 글, 미래 기술 변화 리스크를 발행 전 재확인 항목으로 분리하지 않은 글, 개념 설명은 있으나 최소 실행 예시/정상 출력/실패 예시가 부족한 글
- 신뢰성 보존 관련 주의사항: 기존 `문서 정보`, `검증 기준일`, `테스트 환경`, `확인된 사실`, `직접 재현한 결과`, `해석 / 의견`, `한계와 예외`, `참고자료`는 삭제하지 않는다.
- SEO 보존 관련 주의사항: URL, filename slug, `permalink`, `canonical`, `date`, `published`, `draft` 값은 변경하지 않는다. 제목은 검색 유입 리스크가 있으므로 본문 보강을 우선한다.

## 검사 범위

| 경로 | 검사 파일 수 | 포스팅 판단 수 | 비고 |
|---|---:|---:|---|
| `_posts` | 266 | 265 | K4NUL 원문 포스트. `_posts/AGENTS.md`는 운영 지침으로 제외. |
| `_drafts` | 0 | 0 | 루트 draft 없음. |
| `content` | 184 | 184 | 외부 채널용 `source.md`; GitHub 원문과 사실/검증 기준 동기화 필요. |
| `posts` | 0 | 0 | 디렉터리 없음. |
| `blog` | 0 | 0 | 디렉터리 없음. |
| `articles` | 0 | 0 | 디렉터리 없음. |
| `docs` | 143 | 70 | 대부분 Minimal Mistakes 예제/운영 문서. K4NUL 성장 작업에서는 수정 대상에서 분리. |
| `pages` | 0 | 0 | 디렉터리 없음. |
| `src/content` | 0 | 0 | 디렉터리 없음. |
| `app` | 0 | 0 | 디렉터리 없음. |
| `data` | 0 | 0 | 디렉터리 없음. |
| `scheduled` | 0 | 0 | 디렉터리 없음. |
| `future` | 0 | 0 | 디렉터리 없음. |
| `_pages` | 48 | 48 | 공개 페이지/허브. 포스트와 별도 분류. |
| `doc`, `project-docs`, `templates`, `skills`, root docs | 28 | 0 | 운영/템플릿/스킬 문서. 포스팅으로 판단하지 않음. |

## 공개 상태별 분류

| 상태 | 글 수 | 설명 |
|---|---:|---|
| 공개 글 | 144 | `_posts`에서 현재 기준 공개 대상인 원문 글 |
| 예약/미래 날짜 글 | 120 | `_posts`에서 2026-06-06 이후 날짜 |
| 2026년 예약 글 | 90 | 2026-06-06부터 2026-12-31까지 |
| 2027년 예약 글 | 30 | 2027-01-01부터 2027-04-13까지 |
| published false 글 | 1 | `_posts/2026-05-09-codex-goal-long-running-task-harness.md` |
| 미공개 외부채널 source | 184 | `content/posts/**/source.md` |
| draft 글 | 1 | `docs/_drafts/post-draft.md`, 테마 예제 |
| 공개 페이지/허브 | 48 | `_pages` |
| 구조상 글인지 애매한 문서 | 167 | 테마 문서, 운영 문서, 템플릿 등 |

## 우선순위 표

| 우선순위 | 파일 | 공개 상태 | 발행일 | 현재 제목 | 문제 유형 | 예시 부족 유형 | 권장 조치 |
|---|---|---|---|---|---|---|---|
| P0 | `_posts/2026-05-26-jenkins-installation-initial-setup.md` | 공개 글 | 2026-05-26 | Jenkins 02. Jenkins 설치와 초기 설정 | 제목은 설치/초기 설정인데 본문 앞부분이 의사결정 체크리스트 중심 | Docker 실행, 초기 비밀번호, 정상 출력, Jenkinsfile, 포트 충돌 예시 | 제목 유지, Docker 기반 설치 절차와 검증/오류 대응 보강 |
| P0 | `_posts/2026-05-26-jenkins-installation-initial-setup-en.md` | 공개 글 | 2026-05-26 | Jenkins 02. Jenkins Installation and Initial Setup | EN pair도 같은 문제 | Docker command, setup wizard, Jenkinsfile, failure examples | KR과 같은 범위로 절차 보강 |
| P0 | `content/posts/non-ai/055-jenkins-installation-initial-setup/source.md` | 미공개 외부채널 source | 2026-05-26 | Jenkins 02. Jenkins 설치와 초기 설정 | 외부 채널 source가 원문과 같은 약속 불일치 | 원문과 같은 설치/검증/오류 예시 부족 | 원문 보강분 반영 |
| P0 | `content/posts/non-ai/056-jenkins-installation-initial-setup-en/source.md` | 미공개 외부채널 source | 2026-05-26 | Jenkins 02. Jenkins Installation and Initial Setup | EN 외부 source 동기화 필요 | 원문 EN과 같은 예시 부족 | 원문 보강분 반영 |
| P0 | `_posts/2026-05-09-codex-goal-long-running-task-harness.md` | published false | 2026-05-09 | Codex 실전 활용 11. /goal은 장기 작업의 목표를 어떻게 붙잡는가 | 미공개인데 Experimental 기능과 changelog 의존 | 직접 실행 예시는 일부러 제한. 공개 전 재검증 예시 필요 | 공개 전 재검증 필요 항목 추가 |
| P1 | `_posts/2026-06-05-kubernetes-pod-deployment-replicaset-service.md` 및 EN/source | 공개 글 | 2026-06-05 | K8S 02. Pod, Deployment, ReplicaSet, Service를 운영 흐름으로 이해하기 | 운영 흐름 제목 대비 실행 절차 신호가 약함 | manifest YAML, `kubectl apply/get/describe/logs`, 정상/실패 상태 예시 | 최소 Deployment/Service manifest와 확인 흐름 보강 |
| P1 | `_posts/2026-07-02-github-actions-security-checklist.md` 및 EN/source | 예약 글 | 2026-07-02 | GitHub Actions 보안 체크리스트 | 체크리스트는 있으나 실제 workflow 예시와 실패 로그가 부족함 | 최소 workflow YAML, `permissions` 전/후, 403 실패 로그 | least-privilege workflow와 bad/fixed 예시 보강 |
| P1 | `_posts/2027-01-05-rust-api-dockerignore-cache-image-size.md` 외 29개 | 2027년 예약 글 | 2027 | Rust Service 16~30 KR/EN | 발행 전 재검증 표시가 일관되지 않음 | 현재 예시는 있으나 2027 발행 전 version/tooling 재확인 필요 | 기술 변화 가능성이 큰 글에 재검증 섹션 추가 |
| P2 | `_posts/2026-04-30-how-to-write-agents-md-for-codex.md` | 공개 글 | 2026-04-30 | AGENTS.md 작성법: Codex가 먼저 읽을 운영 기준을 짧게 쓰기 | 작성법 제목 대비 실제 작성-검증 루프가 짧음 | 실패한 AGENTS.md와 수정된 AGENTS.md 비교 예시 부족 | 템플릿 적용/검증 체크를 보강 후보로 유지 |
| P2 | `_posts/2026-05-13-connect-external-context-with-mcp.md` | 공개 글 | 2026-05-13 | Claude Code MCP 운영: 외부 문맥을 붙여 넣지 않고 연결하는 법 | "연결하는 법" 제목 대비 실제 연결 절차가 약함 | MCP 설정 파일, 권한 실패, 데이터 노출 점검 예시 부족 | 공식 MCP/Claude Code 문서 확인 후 절차 보강 |
| P3 | `docs/_posts`, `docs/_docs`, `docs/_pages` | 구조상 애매한 문서 | 다양 | Minimal Mistakes 예제 문서 | 테마 샘플, K4NUL 성장 콘텐츠 아님 | K4NUL 포스팅 예시 기준 적용 대상 아님 | 이번 작업에서는 수정하지 않음 |

## 글별 진단

### `_posts/2026-05-26-jenkins-installation-initial-setup.md`

- 공개 상태: 공개 글
- 발행일: 2026-05-26
- 현재 제목: Jenkins 02. Jenkins 설치와 초기 설정
- 현재 description: Jenkins 설치 방식을 고르기 전에 Java 요구사항, JENKINS_HOME, 초기 비밀번호, plugin 선택을 점검하는 글.
- 현재 slug/permalink: `jenkins-installation-initial-setup` / 기본 Jekyll permalink
- 독자 기대: Docker 또는 로컬 환경에서 Jenkins를 설치하고 초기 관리자 설정까지 따라 할 수 있음
- 실제 본문: 설치 전 의사결정, Java/JENKINS_HOME/plugin 기준 중심. 공식 문서 링크와 신뢰성 구조는 좋음
- 불일치: Docker volume 생성, container 실행, 초기 비밀번호 확인, UI 흐름, 삭제/정리, 흔한 오류 대응이 부족함
- 신뢰성 구조: `문서 정보`, `검증 기준일`, `확인된 사실`, `직접 재현한 결과`, `해석 / 의견`, `한계와 예외`, `참고자료` 존재
- SEO 구조: title/description/tags가 검색 의도에 맞지만 description이 체크리스트 성격으로 낮춰져 있음
- 미래 예약 글 여부: 아니오
- 발행 전 재검증 필요 여부: 아니오
- 점수:
  - 제목 충족도: 1
  - 독자 친화성: 1
  - 절차 완결성: 0
  - 명령어/설정 구체성: 1
  - 결과 검증: 1
  - 오류 대응: 0
  - 신뢰도: 2
  - 제목-본문 정합성: 1
  - SEO 검색 의도 충족도: 1
  - SEO 구조 보존성: 2
  - 예약 글 안정성: 2
  - 미래 정보 리스크: 2
- 권장 조치: 제목과 URL은 유지하고 본문을 설치 튜토리얼 수준으로 보강
- 수정 방향: 요약 직후 실행 중심 섹션을 추가하고 기존 신뢰성 섹션은 뒤에서 유지
- 예시 충분성: 부족
- 부족한 예시 유형: Docker 실행 명령, 초기 관리자 비밀번호 확인, 정상 출력, Jenkinsfile, 포트 충돌 오류, 정리 명령
- 추가해야 할 예시: Docker volume/container, `curl -I`, `docker logs`, `docker exec`, Jenkinsfile, `Finished: SUCCESS`, `port is already allocated`
- 예시 관련 신뢰성 리스크: Docker 명령은 실습용이며 운영 환경에 그대로 적용하면 TLS, backup, credential, controller/agent 분리 문제가 남음
- 예시 관련 SEO 기회: `initialAdminPassword`, `/var/jenkins_home`, `Bind for 0.0.0.0:8080 failed`, Jenkinsfile 검색 의도 대응
- 예시 보강 우선순위: P0

### `_posts/2026-05-26-jenkins-installation-initial-setup-en.md`

- 공개 상태: 공개 글
- 발행일: 2026-05-26
- 현재 제목: Jenkins 02. Jenkins Installation and Initial Setup
- 현재 description: A checklist-style Jenkins installation guide covering Java requirements, JENKINS_HOME, initial password, and first plugin choices.
- 현재 slug/permalink: `/en/devops/jenkins-installation-initial-setup/`
- 독자 기대: 영어 독자도 Docker 실습과 setup wizard를 끝까지 따라 할 수 있음
- 실제 본문: KR 글과 동일하게 의사결정 중심
- 불일치: command, verification, common failures가 부족함
- 신뢰성 구조: Document Information, Verified Facts, Directly Reproduced Results, Limits and References 존재
- SEO 구조: permalink 유지 필요, title 유지 가능
- 미래 예약 글 여부: 아니오
- 발행 전 재검증 필요 여부: 아니오
- 점수: KR 글과 동일하게 절차/오류 대응 보강 필요
- 권장 조치: KR 보강 범위와 동등하게 수정
- 수정 방향: Docker quick path, setup wizard, cleanup, common failures, production caveats 추가
- 예시 충분성: 부족
- 부족한 예시 유형: Docker setup, first password, first Pipeline build, port conflict
- 추가해야 할 예시: `docker volume create`, `docker run`, `docker exec`, Jenkinsfile, example success output, failure message
- 예시 관련 신뢰성 리스크: example output must be marked as sample output unless rerun in the current workspace
- 예시 관련 SEO 기회: Jenkins Docker installation, Jenkins initial admin password, Jenkinsfile hello pipeline
- 예시 보강 우선순위: P0

### `content/posts/non-ai/055-jenkins-installation-initial-setup/source.md`

- 공개 상태: 미공개 외부채널 source
- 발행일: 2026-05-26
- 현재 제목: Jenkins 02. Jenkins 설치와 초기 설정
- 불일치: GitHub 원문과 동일
- 권장 조치: 외부 채널 파생본의 사실 기준이 원문과 어긋나지 않게 같은 보강 반영
- 수정 방향: 원문 KR과 같은 구조로 보강하되, 내부 링크는 source 구조를 유지
- 예시 충분성: 부족
- 부족한 예시 유형: 원문 KR과 같은 설치/검증/오류 예시
- 추가해야 할 예시: 원문 KR 보강분 전체
- 예시 관련 신뢰성 리스크: 외부 채널 source가 원문보다 더 강한 검증을 약속하지 않게 유지
- 예시 관련 SEO 기회: 외부 채널에서 Jenkins 설치/초기 설정 long-tail 대응
- 예시 보강 우선순위: P0

### `content/posts/non-ai/056-jenkins-installation-initial-setup-en/source.md`

- 공개 상태: 미공개 외부채널 source
- 발행일: 2026-05-26
- 현재 제목: Jenkins 02. Jenkins Installation and Initial Setup
- 불일치: GitHub EN 원문과 동일
- 권장 조치: EN 원문과 같은 범위로 보강
- 수정 방향: Docker command, setup wizard, validation, cleanup, failures, production caveats 추가
- 예시 충분성: 부족
- 부족한 예시 유형: EN 원문과 같은 installation walkthrough examples
- 추가해야 할 예시: EN 원문 보강분 전체
- 예시 관련 신뢰성 리스크: keep sample output explicit and avoid implying current live execution
- 예시 관련 SEO 기회: Jenkins installation and initial setup search intent
- 예시 보강 우선순위: P0

### `_posts/2026-05-09-codex-goal-long-running-task-harness.md`

- 공개 상태: published false 글
- 발행일: 2026-05-09
- 현재 제목: Codex 실전 활용 11. /goal은 장기 작업의 목표를 어떻게 붙잡는가
- 현재 description: Codex CLI의 실험적 /goal 기능을 공식 문서와 changelog 기준으로 확인하고, 장기 작업 하네스에서 왜 중요한지 설명하는 글.
- 현재 slug/permalink: `codex-goal-long-running-task-harness` / 기본 Jekyll permalink
- 독자 기대: `/goal`의 기능 위치와 사용 기준을 알 수 있음
- 실제 본문: 공식 문서/changelog 기반 분석이 중심. 직접 실행 범위와 한계가 분리되어 있음
- 불일치: 제목 불일치는 크지 않지만 미공개 상태인데 발행 전 재검증 항목이 없음
- 신뢰성 구조: 검증 기준일, 직접 재현하지 않은 범위, 한계가 명확함
- SEO 구조: `search: false`, `published: false` 유지 필요
- 미래 예약 글 여부: 아니오
- 발행 전 재검증 필요 여부: 예. Codex CLI Experimental 기능과 공식 문서 URL이 변할 수 있음
- 점수:
  - 제목 충족도: 2
  - 독자 친화성: 2
  - 절차 완결성: 1
  - 명령어/설정 구체성: 1
  - 결과 검증: 1
  - 오류 대응: 1
  - 신뢰도: 2
  - 제목-본문 정합성: 2
  - SEO 검색 의도 충족도: 1
  - SEO 구조 보존성: 2
  - 예약 글 안정성: 1
  - 미래 정보 리스크: 1
- 권장 조치: 공개 전 재검증 필요 섹션 추가
- 수정 방향: `published`, `date`, URL은 유지하고 확인 항목만 추가
- 예시 충분성: 보통
- 부족한 예시 유형: `/goal` 실제 create/pause/resume/clear 실행 예시
- 추가해야 할 예시: 공개 전 로컬 CLI에서 `/goal` 흐름을 재현한 뒤 명령과 관찰 결과 추가
- 예시 관련 신뢰성 리스크: Experimental 기능이라 현재 확인 없이 명령 흐름을 단정하면 위험
- 예시 관련 SEO 기회: Codex `/goal`, long-running task, resume, persisted goal 검색 의도 대응
- 예시 보강 우선순위: P0이지만 이번 작업에서는 재검증 항목만 추가

### 2027년 예약 Rust Service 글 30개

- 공개 상태: 예약/미래 날짜 글
- 발행일: 2027-01-05부터 2027-04-13까지
- 현재 제목: Rust Service 16~30 KR/EN
- 현재 slug/permalink: filename slug 및 기존 explicit permalink 유지
- 독자 기대: 2027년 발행 시점에도 Docker, GitHub Actions, Kubernetes, SBOM, OpenTelemetry, Prometheus, container security 절차를 신뢰할 수 있음
- 실제 본문: 대체로 명령어, 검증, 한계는 있으나 일부 글에만 발행 전 재검증 문구가 있음
- 불일치: `date`가 미래인데 검증 기준일은 2026-05-05인 글에서 발행 전 재확인 항목이 일관되지 않음
- 신뢰성 구조: `문서 정보` 또는 `Document Info`는 대부분 존재
- SEO 구조: title/description/date/permalink 유지
- 미래 예약 글 여부: 예
- 발행 전 재검증 필요 여부: 예. 기술 변화 가능성이 큰 운영/배포 글
- 점수:
  - 제목 충족도: 2
  - 독자 친화성: 2
  - 절차 완결성: 1~2
  - 명령어/설정 구체성: 2
  - 결과 검증: 1~2
  - 오류 대응: 0~2
  - 신뢰도: 1~2
  - 제목-본문 정합성: 2
  - SEO 검색 의도 충족도: 1~2
  - SEO 구조 보존성: 2
  - 예약 글 안정성: 0~1
  - 미래 정보 리스크: 2
- 권장 조치: 발행 전 재검증 섹션을 추가하되 날짜/slug/permalink는 변경하지 않음
- 수정 방향: 한국어 글은 `## 발행 전 재검증 필요`, 영어 글은 `## Pre-publication Recheck Required`로 추가
- 예시 충분성: 글마다 다름. Docker/Kubernetes/Rust API 운영 글은 대체로 명령 예시가 있으나 일부 EN 글은 정상 출력/실패 출력 예시가 약함
- 부족한 예시 유형: 발행 시점 기준 정상 출력, 실패 로그, runner/toolchain/version별 차이
- 추가해야 할 예시: 발행 전 재검증 때 실제 toolchain version과 실행 결과를 추가
- 예시 관련 신뢰성 리스크: 2027년 발행일을 현재 검증일처럼 보이게 쓰면 안 됨
- 예시 관련 SEO 기회: 2027년 발행 시점의 Docker/Kubernetes/Rust 오류 메시지와 명령어 long-tail 대응
- 예시 보강 우선순위: P1

### `_posts/2026-06-05-kubernetes-pod-deployment-replicaset-service.md`

- 공개 상태: 공개 글
- 발행일: 2026-06-05
- 현재 제목: K8S 02. Pod, Deployment, ReplicaSet, Service를 운영 흐름으로 이해하기
- 현재 description: Kubernetes의 Pod, Deployment, ReplicaSet, Service를 개별 암기보다 운영 흐름으로 연결해 설명한 글.
- 현재 slug/permalink: `kubernetes-pod-deployment-replicaset-service` / 기본 Jekyll permalink
- 독자 기대: 네 리소스의 관계를 실제 manifest와 `kubectl` 확인 흐름으로 이해
- 실제 본문: 개념 관계 설명은 좋지만 최소 manifest와 정상/실패 출력 예시가 부족했음
- 불일치: 운영 흐름 제목 대비 독자가 직접 따라 할 예시가 약함
- 신뢰성 구조: 문서 정보, 확인된 사실, 직접 재현, 한계, 공식 Kubernetes 참고자료 존재
- SEO 구조: URL/slug 유지, Kubernetes object 키워드 보존
- 미래 예약 글 여부: 아니오
- 발행 전 재검증 필요 여부: 아니오
- 점수:
  - 최소 실행 예시: 1
  - 실제 상황 예시: 2
  - 설정 파일 예시: 0
  - 정상 결과 예시: 1
  - 실패 예시: 0
  - 수정 전/후 예시: 2
  - 실습용/운영용 예시 구분: 0
  - 예시의 신뢰성: 2
  - 예시의 SEO 기여도: 1
  - 예시의 독자 친화성: 2
- 예시 충분성: 부족
- 부족한 예시 유형: Deployment/Service YAML, `kubectl apply/get/describe/logs`, 정상 출력, `ImagePullBackOff`/`CrashLoopBackOff`/`Pending`
- 추가해야 할 예시: `demo-nginx.yaml`, 정상 출력 예시, 실패 상태별 첫 확인 지점, cleanup
- 예시 관련 신뢰성 리스크: 출력 예시를 실제 현재 실행 결과처럼 쓰면 안 됨
- 예시 관련 SEO 기회: `kubectl get pods`, `kubectl describe`, `CrashLoopBackOff`, `ImagePullBackOff` 검색 의도 대응
- 예시 보강 우선순위: P1
- 권장 조치: KR/EN 원문과 외부 source 모두 같은 예시 보강
- 수정 방향: 요약 직후 최소 실습 예시를 추가하고 문서 정보의 검증 기준일을 갱신

### `_posts/2026-07-02-github-actions-security-checklist.md`

- 공개 상태: 예약 글
- 발행일: 2026-07-02
- 현재 제목: GitHub Actions 보안 체크리스트
- 현재 description: GitHub Actions 보안 체크리스트에 대해 공식 문서와 운영 관점으로 확인할 기준, 점검 순서, 한계를 정리한 글.
- 현재 slug/permalink: `github-actions-security-checklist` / 기본 Jekyll permalink
- 독자 기대: 보안 체크리스트를 실제 workflow YAML에 적용할 수 있음
- 실제 본문: trigger/token/secret/runner/OIDC 체크 순서는 있으나 예시 YAML과 실패 로그가 부족했음
- 불일치: 체크리스트 글로는 충분하지만 CI/CD 보안 실무 적용 예시가 약함
- 신뢰성 구조: 공식 GitHub 문서 기반, 문서 정보, 한계와 예외, 참고자료 존재
- SEO 구조: title/description/slug 유지
- 미래 예약 글 여부: 예
- 발행 전 재검증 필요 여부: 예
- 점수:
  - 최소 실행 예시: 1
  - 실제 상황 예시: 2
  - 설정 파일 예시: 1
  - 정상 결과 예시: 1
  - 실패 예시: 0
  - 수정 전/후 예시: 0
  - 실습용/운영용 예시 구분: 1
  - 예시의 신뢰성: 2
  - 예시의 SEO 기여도: 1
  - 예시의 독자 친화성: 2
- 예시 충분성: 부족
- 부족한 예시 유형: least-privilege workflow, bad/fixed permissions, 403 실패 로그, 발행 전 재검증
- 추가해야 할 예시: `permissions: {}`, `contents: read`, action SHA pinning placeholder, PR title untrusted input 처리, 403 failure log
- 예시 관련 신뢰성 리스크: GitHub Actions syntax와 permission names는 발행 전 바뀔 수 있으므로 재검증 표시 필요
- 예시 관련 SEO 기회: `GITHUB_TOKEN permissions`, `permissions: write-all`, `github-actions[bot] 403`, `actions/checkout` 검색 의도 대응
- 예시 보강 우선순위: P1
- 권장 조치: KR/EN 예약 글과 외부 source에 같은 예시 보강
- 수정 방향: 요약 직후 최소 workflow, bad/fixed 예시, failure log를 추가하고 발행 전 재검증 섹션 추가

### 2026년 예약 Kubernetes 글

- 공개 상태: 예약/미래 날짜 글
- 발행일: 2026-06-06부터 2026-06-13까지 우선 확인
- 독자 기대: kubeadm 설치, control plane, worker join, manifest 작성 등 실제 절차를 따라 할 수 있음
- 실제 본문: 명령어와 확인 흐름은 다수 존재하지만 발행 전 재검증 표시는 일관되지 않음
- 불일치: 예약 글 안정성 면에서 재검증 표시 후보
- 권장 조치: 다음 작업에서 Kubernetes 03~10 KR/EN 및 외부 source의 발행 전 확인 항목을 보강
- 수정 방향: 이번 작업에서는 Jenkins 특수 지시와 2027년 예약 글 안정성을 우선하고, Kubernetes 보강은 weekly prompt로 분리

### `_pages/development-rust.md`, `_pages/en-development-rust.md`

- 공개 상태: 공개 페이지/허브
- 현재 제목: Rust 학습 가이드 / Rust Learning Guides
- 불일치: 제목에 guide가 있으나 허브 페이지 성격이므로 명령어가 없는 것은 즉시 결함으로 보지 않음
- 권장 조치: 별도 허브 개선 작업에서 경로 안내와 공개 글 묶음만 보강
- 수정 방향: 이번 작업에서는 변경하지 않음

### `docs/_posts`, `docs/_docs`, `docs/_pages`, `docs/_drafts`

- 공개 상태: 구조상 글인지 애매한 문서
- 실제 본문: Minimal Mistakes theme 예제 및 문서
- 불일치: K4NUL 콘텐츠 전략 대상이 아님
- 권장 조치: upstream/theme 예제는 이번 콘텐츠 품질 수정에서 제외
- 수정 방향: 변경하지 않음

## 즉시 수정 작업

- Jenkins 설치/초기 설정 KR/EN 원문과 외부 source를 절차 중심으로 보강한다.
- `published: false` Codex `/goal` 글에 공개 전 재검증 항목을 추가한다.
- 2027년 예약 글 중 발행 전 재검증 표시가 없는 글에 현재 기준 검증일과 미래 발행 전 확인 항목을 분리한다.

## 주차별 프롬프트로 분리할 작업

- Kubernetes 03~10 KR/EN 예약 글의 발행 전 재검증 표시와 오류 대응 보강
- K8S 02 공개 글의 `kubectl` 중심 정상 확인 절차 보강
- AGENTS.md 작성법 글의 실제 작성-검증 루프 보강
- Claude Code MCP 연결 글의 실제 연결 절차 보강
- `_pages` Rust/AI/DevOps 허브의 독자 경로 안내 점검
