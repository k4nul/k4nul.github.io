# Rust Tauri Curriculum Roadmap

## Snapshot

- 검토 기준일: 2026-04-29
- 목적: Rust 코어 입문 이후 Tauri 프레임워크 학습과 후속 포스팅 후보를 계획으로 보관한다.
- 현재 상태: 계획 문서만 작성한다. `_posts/`에는 아직 Tauri 포스트를 만들지 않는다.
- 일정 위치: DevOps 예약분과 2026-07-21~2026-09-11 AI+Non-AI 병행 로드맵이 끝난 뒤, 2026-09-15부터 Rust 후속 블록으로 배치한다.
- 발행 단위: 주 1주제. 한국어 원문은 화요일, 영어 미러는 수요일에 발행한다.
- 권장 구조: 실제 발행 시 `section: development`, `topic_key: rust`, `categories: Rust`
- 기준 버전: Tauri 공식 release 페이지 기준 `tauri` v2.10.3, `@tauri-apps/api` v2.10.1, `tauri-cli` v2.10.1
- 출처 기준: Tauri 공식 문서와 공식 저장소 우선

## Scope

- 포함: Tauri 개발 환경, 프로젝트 구조, Rust command와 IPC, capability와 permission, plugin, sidecar, build와 updater, 첫 capstone 앱
- 제외: 모바일 app store 배포 절차, code signing 계정별 세부 절차, 프런트엔드 프레임워크별 상태 관리 심화, Electron 비교 일반론
- 전제: Rust 01~13의 설치, Cargo, ownership, module, testing, file I/O, serde, 작은 CLI 프로젝트까지 학습했다고 본다.

## Curriculum Sequence

### 0. Rust 선행 조건 점검

- 목적: Tauri로 넘어가기 전에 Rust 쪽 막힘을 줄인다.
- 포함 항목: `cargo run`, `cargo test`, `Result`, `Option`, `?`, `serde::Serialize`, `serde::Deserialize`, `main.rs`와 `lib.rs` 분리
- 산출물 후보: 기존 CLI 프로젝트에서 JSON 입출력과 테스트를 갖춘 작은 예제

### 1. 개발 환경과 첫 Tauri 앱

- 목적: OS별 개발 의존성과 첫 실행 흐름을 고정한다.
- 포함 항목: Rust, Node.js, Microsoft C++ Build Tools, WebView2, Xcode 또는 Linux WebKitGTK 계열 의존성
- 산출물 후보: `create-tauri-app`으로 만든 빈 앱 실행 기록

### 2. 프로젝트 구조와 설정 파일

- 목적: 웹 프로젝트와 Rust backend가 어떻게 분리되는지 이해한다.
- 포함 항목: `src-tauri/`, `src-tauri/src/lib.rs`, `src-tauri/tauri.conf.json`, 루트 `package.json`, `src-tauri/Cargo.toml`
- 산출물 후보: 앱 이름, window title, 기본 크기 변경 실습

### 3. Rust command와 frontend invoke

- 목적: 프런트엔드 이벤트가 Rust 함수와 연결되는 최소 단위를 익힌다.
- 포함 항목: `#[tauri::command]`, `invoke_handler`, `@tauri-apps/api/core`의 `invoke`, command 인자와 반환 타입
- 산출물 후보: 문자열 정규화 또는 파일 경로 검증 command

### 4. 상태 관리와 비동기 작업

- 목적: 화면 상태와 backend 상태를 섞지 않는다.
- 포함 항목: 프런트엔드 UI state, Rust-managed state, 실패 가능한 command, 긴 작업의 진행 상태
- 산출물 후보: 작은 설정 객체 읽기/저장 기능

### 5. Capability와 permission

- 목적: 기능 추가와 권한 허용을 분리해서 다룬다.
- 포함 항목: `src-tauri/capabilities/default.json`, window label, plugin permission, scope
- 산출물 후보: dialog 또는 file system plugin을 최소 권한으로 붙이는 실습

### 6. 앱 기능 확장

- 목적: 데스크톱 앱다운 기능을 하나씩 붙이고 권한 변화를 기록한다.
- 포함 후보: system tray, window customization, menu, clipboard, notifications, store 또는 SQL plugin, opener
- 산출물 후보: 기능 1개를 end-to-end로 붙이고 실패, 취소, 권한 부족 상태를 처리하는 예제

### 7. Sidecar와 외부 바이너리

- 목적: Rust command만으로 부족한 작업을 외부 실행 파일로 분리할 때의 비용을 이해한다.
- 포함 항목: `externalBin`, target triple suffix, `rustc --print host-tuple`, 플랫폼별 바이너리 준비
- 산출물 후보: sidecar가 정말 필요한 조건과 대체 가능한 Rust crate 검토표

### 8. Build, bundle, updater

- 목적: 개발 모드 앱과 배포 앱의 차이를 이해한다.
- 포함 항목: `tauri build`, bundle format, signing, versioning, updater endpoint, rollback 정책
- 산출물 후보: Windows, macOS, Linux 중 하나를 대상으로 한 release 준비 체크리스트

## Posting Candidates

1. `Rust 14. Tauri는 Rust GUI 프레임워크가 아니라 앱 경계다`
   - 핵심 메시지: Tauri를 "Rust로 화면을 그리는 도구"가 아니라 WebView frontend와 Rust backend를 묶는 앱 프레임워크로 설명한다.
   - 포함 항목: WebView, WRY, OS별 렌더러, frontend/backend 책임 분리

2. `Rust 15. Tauri 개발 환경과 첫 앱 실행`
   - 핵심 메시지: 첫 성공 조건은 코드보다 OS별 의존성을 정확히 맞추는 것이다.
   - 포함 항목: Windows Build Tools/WebView2, macOS Xcode, Linux WebKitGTK, `create-tauri-app`

3. `Rust 16. Tauri 프로젝트 구조 읽기`
   - 핵심 메시지: `package.json`과 `Cargo.toml`, `tauri.conf.json`의 책임을 분리해서 읽는다.
   - 포함 항목: `src-tauri`, config, window, dev server, build command

4. `Rust 17. Frontend에서 Rust command 호출하기`
   - 핵심 메시지: Tauri의 첫 핵심은 UI 이벤트와 Rust command의 경계를 작게 설계하는 것이다.
   - 포함 항목: `#[tauri::command]`, `invoke`, 인자 직렬화, 반환값, 오류 처리

5. `Rust 18. Tauri capability와 permission 기초`
   - 핵심 메시지: 플러그인을 붙였다고 프런트엔드 권한이 자동으로 열리는 것은 아니다.
   - 포함 항목: capability file, window label, permission, plugin scope

6. `Rust 19. Tauri 첫 로컬 도구 만들기`
   - 핵심 메시지: 작은 capstone 앱으로 UI, command, file access, 설정 저장, build를 한 번 연결한다.
   - 포함 후보: Markdown note manager, local JSON/TOML config editor, log file viewer

## Calendar

기존 예약 글과 2026-07-21부터 2026-09-11까지의 AI+Non-AI 병행 로드맵을 침범하지 않도록, Tauri 글은 다음 주 화요일인 2026-09-15부터 시작한다.

| Week | Date | Lang | Topic | Translation key | Slug |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-09-15 | ko | Rust 14. Tauri는 Rust GUI 프레임워크가 아니라 앱 경계다 | rust-tauri-app-boundary | rust-tauri-app-boundary |
| 1 | 2026-09-16 | en | Rust 14. Tauri is an app boundary, not a Rust GUI framework | rust-tauri-app-boundary | rust-tauri-app-boundary-en |
| 2 | 2026-09-22 | ko | Rust 15. Tauri 개발 환경과 첫 앱 실행 | rust-tauri-development-environment-first-app | rust-tauri-development-environment-first-app |
| 2 | 2026-09-23 | en | Rust 15. Tauri development environment and first app | rust-tauri-development-environment-first-app | rust-tauri-development-environment-first-app-en |
| 3 | 2026-09-29 | ko | Rust 16. Tauri 프로젝트 구조 읽기 | rust-tauri-project-structure | rust-tauri-project-structure |
| 3 | 2026-09-30 | en | Rust 16. Reading the Tauri project structure | rust-tauri-project-structure | rust-tauri-project-structure-en |
| 4 | 2026-10-06 | ko | Rust 17. Frontend에서 Rust command 호출하기 | rust-tauri-frontend-invoke-rust-command | rust-tauri-frontend-invoke-rust-command |
| 4 | 2026-10-07 | en | Rust 17. Calling Rust commands from the frontend | rust-tauri-frontend-invoke-rust-command | rust-tauri-frontend-invoke-rust-command-en |
| 5 | 2026-10-13 | ko | Rust 18. Tauri capability와 permission 기초 | rust-tauri-capabilities-permissions | rust-tauri-capabilities-permissions |
| 5 | 2026-10-14 | en | Rust 18. Tauri capabilities and permissions basics | rust-tauri-capabilities-permissions | rust-tauri-capabilities-permissions-en |
| 6 | 2026-10-20 | ko | Rust 19. Tauri 첫 로컬 도구 만들기 | rust-tauri-first-local-tool | rust-tauri-first-local-tool |
| 6 | 2026-10-21 | en | Rust 19. Building a first local tool with Tauri | rust-tauri-first-local-tool | rust-tauri-first-local-tool-en |

## Planning Notes

- 커리큘럼 자체는 포스트로 발행하지 않는다. 이 문서는 후속 개별 포스트의 범위와 순서를 잡기 위한 계획이다.
- 실제 포스트로 전환할 때는 각 글마다 직접 실행한 환경, 도구 버전, 실패 조건, 한계를 분리해서 적는다.
- Tauri 관련 CLI, plugin permission, updater 설정은 버전 민감 내용이므로 발행 직전에 공식 문서를 다시 확인한다.
- KOR/ENG 미러를 같은 `translation_key`로 묶고, 영어 글에는 명시적 `permalink`를 둔다.
- 실제 포스트 파일을 만들기 전에는 `_data/start_tracks.yml`이나 home featured 항목에 연결하지 않는다.

## References For Future Drafting

- [Tauri official site](https://tauri.app/)
- [Tauri Core Ecosystem Releases](https://tauri.app/release/)
- [Tauri Prerequisites](https://v2.tauri.app/start/prerequisites/)
- [Tauri Create a Project](https://v2.tauri.app/start/create-project/)
- [Calling Rust from the Frontend](https://v2.tauri.app/develop/calling-rust/)
- [Tauri Capabilities](https://v2.tauri.app/security/capabilities/)
- [Embedding External Binaries](https://v2.tauri.app/develop/sidecar/)
- [Tauri Distribute](https://v2.tauri.app/distribute/)
- [Tauri Updater Plugin](https://v2.tauri.app/plugin/updater/)
- [tauri-apps/tauri GitHub repository](https://github.com/tauri-apps/tauri)

## Update Triggers

- Tauri v2 CLI, project layout, capability model, plugin permission 이름이 바뀐 경우
- Rust 시리즈 확장 순서가 trait 심화 대신 Tauri 앱 개발로 확정된 경우
- Tauri 관련 포스트를 실제 `_posts/`에 추가하기로 결정한 경우
- KOR/ENG 미러 발행 일정이나 2026-09-15 시작일이 바뀐 경우
