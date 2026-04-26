#!/usr/bin/env python3
"""Generate Tistory-optimized variants for every managed post."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote


KST = timezone(timedelta(hours=9))
SITE_URL = "https://www.k4nul.com"
POLICY_VERSION = "2026-04-25.tistory-search-variant.v3"
POST_FILE_RE = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.+)\.md$")
ORDERED_CONTENT_DIR_RE = re.compile(r"^\d{3,6}-(?P<slug>.+)$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
EXTERNAL_CHANNEL_EXCLUDED_SLUGS = {
    "macro-malware",
    "macro-malware-en",
    "rtf-malware",
    "rtf-malware-en",
}
EXTERNAL_CHANNEL_EXCLUSION_REASON = "security_topic_github_only"


@dataclass(frozen=True)
class ManagedPost:
    slug: str
    post_path: Path | None
    content_dir: Path
    source_path: Path


@dataclass(frozen=True)
class SourceDoc:
    front_matter: dict[str, Any]
    body: str
    source_text: str
    source_hash: str


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def sha256_text(text: str) -> str:
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


def write_text_if_changed(path: Path, text: str, dry_run: bool) -> bool:
    normalized = normalize_text(text).strip() + "\n"
    if path.exists() and normalize_text(read_text(path)).strip() + "\n" == normalized:
        return False
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(normalized, encoding="utf-8", newline="\n")
    return True


def write_json_if_changed(path: Path, value: dict[str, Any], dry_run: bool) -> bool:
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    return write_text_if_changed(path, text, dry_run)


def yaml_quote(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    return json.dumps(str(value), ensure_ascii=False)


def yaml_doc(value: dict[str, Any]) -> str:
    lines: list[str] = []
    for key, item in value.items():
        if isinstance(item, list):
            lines.append(f"{key}:")
            if item:
                for entry in item:
                    lines.append(f"  - {yaml_quote(entry)}")
            else:
                lines.append("  []")
        else:
            lines.append(f"{key}: {yaml_quote(item)}")
    return "\n".join(lines) + "\n"


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"", "null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_front_matter(front_matter: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    lines = front_matter.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#") or line.startswith((" ", "\t")):
            index += 1
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if not match:
            index += 1
            continue
        key, raw_value = match.group(1), match.group(2) or ""
        if raw_value == "":
            values: list[Any] = []
            probe = index + 1
            while probe < len(lines):
                child = lines[probe]
                if not child.startswith((" ", "\t")):
                    break
                item = child.strip()
                if item.startswith("- "):
                    values.append(parse_scalar(item[2:]))
                probe += 1
            result[key] = values if values else ""
            index = probe
            continue
        result[key] = parse_scalar(raw_value)
        index += 1
    return result


def parse_source(source_text: str) -> SourceDoc:
    text = normalize_text(source_text)
    match = FRONTMATTER_RE.match(text)
    if not match:
        return SourceDoc({}, text.strip(), text, sha256_text(text))
    front_matter = parse_front_matter(match.group(1))
    body = text[match.end() :].strip()
    return SourceDoc(front_matter, body, text, sha256_text(text))


def external_channel_exclusion_reason(slug: str) -> str | None:
    return EXTERNAL_CHANNEL_EXCLUSION_REASON if slug in EXTERNAL_CHANNEL_EXCLUDED_SLUGS else None


def discover_posts(root: Path, posts_root: Path, content_root: Path) -> list[ManagedPost]:
    posts: list[ManagedPost] = []
    seen: set[str] = set()
    existing_dirs = existing_content_dirs(content_root)
    if posts_root.exists():
        for post_path in sorted(posts_root.glob("*.md")):
            match = POST_FILE_RE.match(post_path.name)
            if not match:
                continue
            slug = match.group("slug")
            if external_channel_exclusion_reason(slug):
                continue
            seen.add(slug)
            content_dir = existing_dirs.get(slug, content_root / slug)
            posts.append(
                ManagedPost(slug, post_path, content_dir, content_dir / "source.md")
            )
    if content_root.exists():
        for source_path in source_paths(content_root):
            slug = content_slug_from_dir(source_path.parent)
            if external_channel_exclusion_reason(slug):
                continue
            if slug in seen:
                continue
            posts.append(ManagedPost(slug, None, source_path.parent, source_path))
    return posts


def content_slug_from_dir(post_dir: Path) -> str:
    match = ORDERED_CONTENT_DIR_RE.match(post_dir.name)
    return match.group("slug") if match else post_dir.name


def source_paths(content_root: Path) -> list[Path]:
    if not content_root.exists():
        return []
    return sorted(path for path in content_root.glob("**/source.md") if path.is_file())


def existing_content_dirs(content_root: Path) -> dict[str, Path]:
    return {
        content_slug_from_dir(source_path.parent): source_path.parent
        for source_path in source_paths(content_root)
    }


def ensure_source(post: ManagedPost, dry_run: bool) -> bool:
    if post.post_path is None:
        return False
    if not post.source_path.exists():
        return write_text_if_changed(post.source_path, read_text(post.post_path), dry_run)
    if post.post_path.stat().st_mtime > post.source_path.stat().st_mtime:
        return write_text_if_changed(post.source_path, read_text(post.post_path), dry_run)
    return False


def parse_datetime(raw: Any, fallback_path: Path | None = None) -> datetime | None:
    if isinstance(raw, str):
        value = raw.strip()
        patterns = (
            "%Y-%m-%d %H:%M:%S %z",
            "%Y-%m-%d %H:%M %z",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d",
        )
        for pattern in patterns:
            try:
                parsed = datetime.strptime(value, pattern)
            except ValueError:
                continue
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=KST)
            return parsed.astimezone(KST)
    if fallback_path:
        match = POST_FILE_RE.match(fallback_path.name)
        if match:
            return parse_datetime(match.group("date"))
    return None


def slug_words(slug: str) -> list[str]:
    return [word for word in slug.replace("_", "-").split("-") if word]


def tags(front_matter: dict[str, Any]) -> list[str]:
    raw = front_matter.get("tags")
    if isinstance(raw, str):
        return [raw]
    if isinstance(raw, list):
        return [str(item) for item in raw if item]
    return []


def clean_title(title: str) -> str:
    title = re.sub(r"^\s*(Rust|Docker|Git|K8S|Jenkins|Codex|Claude)\s+\d+\.\s*", "", title)
    title = re.sub(r"^\s*\d+\.\s*", "", title)
    return title.strip() or title


def topic(front_matter: dict[str, Any], slug: str, body: str) -> str:
    haystack = " ".join(
        [slug, str(front_matter.get("title") or ""), " ".join(tags(front_matter)), body[:500]]
    ).lower()
    if "rust" in haystack:
        return "rust"
    if "docker" in haystack or "container" in haystack:
        return "docker"
    if "kubernetes" in haystack or "k8s" in haystack or "kubectl" in haystack:
        return "kubernetes"
    if "jenkins" in haystack:
        return "jenkins"
    if " git" in f" {haystack}" or "github" in haystack or "branch" in haystack:
        return "git"
    if "codex" in haystack:
        return "codex"
    if "claude" in haystack:
        return "claude"
    if "malware" in haystack or "rtf" in haystack or "security" in haystack:
        return "security"
    return "general"


def title_candidates(post: ManagedPost, doc: SourceDoc) -> tuple[list[str], str, list[str]]:
    original = str(doc.front_matter.get("title") or post.slug)
    cleaned = clean_title(original)
    t = topic(doc.front_matter, post.slug, doc.body)
    words = slug_words(post.slug)
    lower_slug = post.slug.lower()

    if t == "rust" and {"install", "hello", "world"} & set(words):
        candidates = [
            "Windows에서 Rust 설치하고 Hello World 실행하기",
            "VS Code에서 Rust 시작하기: rustup 설치부터 cargo run까지",
            "Rust 입문 환경 세팅: rustup, rustc, cargo 차이까지",
        ]
        return candidates, "Windows Rust 설치", [
            "VS Code Rust 실행",
            "Rust Hello World",
            "rustup 설치",
            "cargo run",
        ]
    if t == "rust" and "debug" in lower_slug:
        candidates = [
            "VS Code에서 Rust 디버깅하기: rust-analyzer와 CodeLLDB 설정",
            "Rust 디버깅 환경 세팅: 중단점부터 변수 확인까지",
            "rust-analyzer와 CodeLLDB 차이, VS Code Rust 디버깅 흐름",
        ]
        return candidates, "VS Code Rust 디버깅", [
            "rust-analyzer",
            "CodeLLDB",
            "Rust 중단점",
            "Rust 디버깅 설정",
        ]
    if t == "rust":
        core = cleaned.replace("Rust", "").strip(" .:-") or "기본 개념"
        candidates = [
            f"Rust {core} 정리: 입문자가 헷갈리는 부분부터",
            f"Rust 입문자가 알아야 할 {core}",
            f"Rust {core} 예제로 이해하기",
        ]
        return candidates, f"Rust {core}", ["Rust 입문", "Rust 예제", "Rust 개발"]
    if t == "docker":
        candidates = [
            f"Docker {cleaned} 실무 정리",
            f"Docker 입문자가 헷갈리는 {cleaned}",
            f"Docker 문제 해결 흐름: {cleaned}",
        ]
        return candidates, "Docker 실무", ["Docker 이미지", "Docker 컨테이너", "Docker 명령어"]
    if t == "kubernetes":
        candidates = [
            f"Kubernetes {cleaned} 실무 정리",
            f"쿠버네티스 입문자를 위한 {cleaned}",
            f"K8S {cleaned}: 개념부터 확인 방법까지",
        ]
        return candidates, "Kubernetes 입문", ["K8S", "kubectl", "쿠버네티스 실무"]
    if t == "jenkins":
        candidates = [
            f"Jenkins {cleaned} 실무 정리",
            f"젠킨스 입문자를 위한 {cleaned}",
            f"Jenkins Pipeline 흐름으로 보는 {cleaned}",
        ]
        return candidates, "Jenkins 실무", ["Jenkins Pipeline", "CI/CD", "Jenkins 설정"]
    if t == "git":
        candidates = [
            f"Git {cleaned} 실무 정리",
            f"Git 입문자가 헷갈리는 {cleaned}",
            f"Git 협업에서 필요한 {cleaned}",
        ]
        return candidates, "Git 실무", ["Git 명령어", "Git 협업", "GitHub"]
    if t in {"codex", "claude"}:
        label = "Codex" if t == "codex" else "Claude Code"
        candidates = [
            f"{label} {cleaned} 실무 운영 정리",
            f"AI 코딩 도구를 팀에서 쓸 때 필요한 {cleaned}",
            f"{label} 작업 흐름을 안정적으로 만드는 방법",
        ]
        return candidates, f"{label} 운영", ["AI 코딩 도구", "개발 자동화", "작업 지시"]
    if t == "security":
        candidates = [
            f"{cleaned} 분석 흐름 정리",
            f"보안 분석 입문자를 위한 {cleaned}",
            f"악성코드 분석에서 보는 {cleaned}",
        ]
        return candidates, "보안 분석", ["악성코드 분석", "문서 악성코드", "분석 절차"]

    candidates = [
        f"{cleaned} 실무 정리",
        f"{cleaned} 이해하기: 핵심 개념과 확인 방법",
        f"{cleaned}를 처음 볼 때 확인할 것",
    ]
    return candidates, cleaned, [word for word in words[:4] if word]


def section_map(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = "본문"
    sections[current] = []
    for line in body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items() if "\n".join(value).strip()}


def section_by_names(sections: dict[str, str], names: list[str]) -> str:
    normalized = {key.lower(): value for key, value in sections.items()}
    for name in names:
        if name in sections:
            return sections[name]
        lower = name.lower()
        if lower in normalized:
            return normalized[lower]
    return ""


def extract_doc_info(body: str) -> dict[str, str]:
    sections = section_map(body)
    info = section_by_names(sections, ["문서 정보", "Document Information", "Document info"])
    result: dict[str, str] = {}
    for raw in info.splitlines():
        line = raw.strip()
        if not line.startswith("- "):
            continue
        pair = line[2:].split(":", 1)
        if len(pair) == 2:
            result[pair[0].strip()] = pair[1].strip()
    return result


def verification_date(body: str) -> str | None:
    match = re.search(r"검증 기준일:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", body)
    if match:
        return match.group(1)
    match = re.search(r"Verification date:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", body, re.I)
    return match.group(1) if match else None


def first_sentences(text: str, limit: int = 4) -> list[str]:
    cleaned = IMAGE_RE.sub("", normalize_text(text))
    cleaned = re.sub(r"```.*?```", "", cleaned, flags=re.DOTALL)
    items: list[str] = []
    for line in cleaned.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()
        parts = re.split(r"(?<=[.!?])\s+", stripped)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            items.append(part)
            if len(items) >= limit:
                return items
    return items


def extract_code_blocks(text: str, limit: int = 6) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    in_code = False
    language = "text"
    buffer: list[str] = []
    for line in normalize_text(text).splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                language = stripped.removeprefix("```").strip() or "text"
                buffer = []
            else:
                in_code = False
                content = "\n".join(buffer).strip()
                if content:
                    blocks.append((language, content))
                    if len(blocks) >= limit:
                        return blocks
                buffer = []
            continue
        if in_code:
            buffer.append(line)
    return blocks


def collect_links(body: str) -> list[tuple[str, str]]:
    seen: set[str] = set()
    links: list[tuple[str, str]] = []
    for text, url in LINK_RE.findall(body):
        if url in seen:
            continue
        seen.add(url)
        links.append((text.strip(), url.strip()))
    return links[:10]


def comparison_table(t: str, body: str) -> str:
    lower = body.lower()
    if t == "rust" or any(word in lower for word in ["rustup", "rustc", "cargo"]):
        return "\n".join(
            [
                "| 도구 | 역할 | 언제 쓰나 |",
                "|---|---|---|",
                "| rustup | Rust 설치와 toolchain 관리 | 처음 설치하거나 버전을 관리할 때 |",
                "| rustc | Rust 컴파일러 | 단일 파일을 빠르게 컴파일할 때 |",
                "| cargo | 프로젝트 관리 도구 | 실제 프로젝트 생성, 빌드, 실행, 의존성 관리 |",
            ]
        )
    if t == "docker":
        return "\n".join(
            [
                "| 용어 | 역할 | 확인 포인트 |",
                "|---|---|---|",
                "| image | 실행 환경을 담은 템플릿 | 태그와 digest를 구분한다 |",
                "| container | 이미지에서 실행된 프로세스 | 상태와 로그를 확인한다 |",
                "| layer | 이미지 변경 단위 | 캐시와 용량에 영향을 준다 |",
                "| registry | 이미지를 저장하는 곳 | push/pull 권한을 확인한다 |",
            ]
        )
    if t == "kubernetes":
        return "\n".join(
            [
                "| 용어 | 역할 | 먼저 확인할 것 |",
                "|---|---|---|",
                "| Pod | 컨테이너 실행 단위 | `kubectl get pods` 상태 |",
                "| Deployment | Pod 배포와 롤링 업데이트 관리 | replica와 rollout 상태 |",
                "| Service | Pod 접근 경로 | selector와 port 매핑 |",
                "| Ingress | HTTP 진입점 | controller와 host rule |",
            ]
        )
    if t == "jenkins":
        return "\n".join(
            [
                "| 용어 | 역할 | 확인 포인트 |",
                "|---|---|---|",
                "| Job | 실행 단위 | 입력값과 실행 이력 |",
                "| Pipeline | 코드로 관리하는 빌드 흐름 | stage와 step |",
                "| Credential | 외부 시스템 인증 정보 | 권한 범위와 노출 여부 |",
                "| Agent | 작업을 실제로 수행하는 실행 환경 | label과 도구 설치 상태 |",
            ]
        )
    if t == "git":
        return "\n".join(
            [
                "| 용어 | 역할 | 언제 확인하나 |",
                "|---|---|---|",
                "| working tree | 아직 커밋하지 않은 작업 상태 | 수정 중인 파일을 볼 때 |",
                "| branch | 작업 흐름을 나누는 포인터 | 기능 작업이나 협업 시 |",
                "| commit | 변경 기록 단위 | 작업을 남길 때 |",
                "| remote | 원격 저장소 | fetch, pull, push 시 |",
            ]
        )
    return "\n".join(
        [
            "| 항목 | 의미 | 확인할 것 |",
            "|---|---|---|",
            "| 문제 | 이 글에서 해결하려는 상황 | 내 상황과 같은지 먼저 본다 |",
            "| 환경 | 글의 테스트 기준 | 운영체제, 버전, 도구 차이를 확인한다 |",
            "| 결과 | 직접 확인한 내용 | 명령 출력과 화면 상태를 비교한다 |",
            "| 한계 | 그대로 적용하면 안 되는 조건 | 미확인 환경과 예외를 따로 본다 |",
        ]
    )


def troubleshooting(t: str) -> list[tuple[str, str, str, str]]:
    if t == "rust":
        return [
            (
                "rustc 명령어를 찾을 수 없는 경우",
                "`rustc --version`을 실행했을 때 명령을 찾을 수 없다는 메시지가 나온다.",
                "설치 직후 기존 PowerShell을 계속 쓰고 있는지, PATH가 갱신됐는지 먼저 본다.",
                "새 PowerShell을 열어 다시 확인하고, 그래도 안 되면 rustup 설치가 끝났는지 확인한다.",
            ),
            (
                "cargo 명령어가 안 잡히는 경우",
                "`cargo --version`이 실패하거나 프로젝트 생성 명령이 동작하지 않는다.",
                "`rustc --version`도 함께 실패하는지 확인해 설치 문제인지 cargo만의 문제인지 나눈다.",
                "Rust toolchain을 다시 확인하고, 필요하면 rustup 설치 흐름을 다시 실행한다.",
            ),
            (
                "설치 후 기존 터미널에서 명령이 안 되는 경우",
                "설치는 완료됐는데 같은 터미널 창에서 버전 확인이 실패한다.",
                "설치 과정에서 PATH가 바뀌었지만 현재 셸에 반영되지 않았을 수 있다.",
                "PowerShell 또는 VS Code 터미널을 새로 열고 다시 실행한다.",
            ),
            (
                "VS Code에서 Rust 코드 인식이 안 되는 경우",
                "문법 강조나 자동 완성이 기대한 만큼 동작하지 않는다.",
                "Rust 설치와 VS Code 확장 설치를 혼동하지 않았는지 확인한다.",
                "Rust toolchain을 먼저 확인한 뒤 rust-analyzer 확장을 설치하거나 다시 로드한다.",
            ),
        ]
    if t == "docker":
        return [
            (
                "이미지와 컨테이너가 헷갈리는 경우",
                "빌드는 됐는데 실행 중인 대상이 무엇인지 구분하기 어렵다.",
                "`docker images`와 `docker ps`가 서로 다른 대상을 보여 준다는 점을 먼저 확인한다.",
                "이미지는 템플릿, 컨테이너는 실행 인스턴스로 나눠서 상태를 본다.",
            ),
            (
                "태그는 같은데 결과가 다른 경우",
                "같은 태그를 pull했는데 기대한 이미지와 다르게 보인다.",
                "태그는 움직일 수 있고 digest는 특정 이미지를 가리킨다는 점을 확인한다.",
                "재현성이 중요하면 digest 기준으로 확인한다.",
            ),
            (
                "명령은 맞는데 권한 오류가 나는 경우",
                "pull, push, run 과정에서 permission denied 계열 메시지가 나온다.",
                "로컬 Docker 권한, registry 로그인, 저장소 권한을 나눠 본다.",
                "권한 문제를 명령어 문법 문제로 단정하지 않는다.",
            ),
        ]
    if t == "kubernetes":
        return [
            (
                "kubectl이 다른 클러스터를 보고 있는 경우",
                "명령 결과가 기대한 클러스터 상태와 다르다.",
                "`kubectl config current-context`로 현재 context를 확인한다.",
                "context를 바꾼 뒤 같은 명령을 다시 실행한다.",
            ),
            (
                "Pod가 Running이 되지 않는 경우",
                "Pod가 Pending, CrashLoopBackOff, ImagePullBackOff 상태에 머문다.",
                "`kubectl describe pod`와 이벤트를 먼저 확인한다.",
                "이미지, 리소스, 네트워크, 스토리지 문제를 순서대로 분리한다.",
            ),
            (
                "Service로 접근이 안 되는 경우",
                "Pod는 떠 있지만 Service 주소로 접속되지 않는다.",
                "selector가 Pod label과 맞는지, port와 targetPort가 맞는지 확인한다.",
                "Service 정의와 실제 Pod label을 나란히 비교한다.",
            ),
        ]
    if t == "jenkins":
        return [
            (
                "플러그인이 없어 단계가 실패하는 경우",
                "예제와 같은 Jenkinsfile인데 특정 step을 찾을 수 없다고 나온다.",
                "필요한 플러그인이 설치돼 있는지, 버전 차이가 있는지 확인한다.",
                "플러그인 설치 후 Jenkins 재시작 또는 job 재실행이 필요한지 본다.",
            ),
            (
                "Credential을 찾지 못하는 경우",
                "Pipeline에서 credential id를 찾을 수 없다는 오류가 난다.",
                "credential id, scope, job 권한을 먼저 확인한다.",
                "코드의 id와 Jenkins에 등록된 id를 정확히 맞춘다.",
            ),
            (
                "Agent에서 도구가 없는 경우",
                "로컬에서는 되는데 Jenkins agent에서는 명령이 실패한다.",
                "agent에 필요한 CLI, JDK, Docker 같은 도구가 설치돼 있는지 본다.",
                "Pipeline 내부에서 실행 환경을 명시하거나 agent 이미지를 정리한다.",
            ),
        ]
    if t == "git":
        return [
            (
                "현재 브랜치를 착각한 경우",
                "수정한 파일이 예상한 브랜치에 없거나 push 대상이 다르다.",
                "`git branch --show-current`와 `git status`를 먼저 확인한다.",
                "작업 전후 브랜치와 remote 대상을 분리해서 본다.",
            ),
            (
                "pull 후 충돌이 난 경우",
                "merge conflict 메시지와 충돌 표시가 파일에 남는다.",
                "충돌 파일을 확인하고 어느 쪽 변경을 살릴지 결정한다.",
                "수정 후 테스트하고 commit으로 충돌 해결을 기록한다.",
            ),
            (
                "push가 거절되는 경우",
                "non-fast-forward 또는 권한 관련 오류가 난다.",
                "원격에 새 커밋이 있는지, 내가 push할 권한이 있는지 확인한다.",
                "먼저 fetch/pull로 차이를 확인하고 팀 규칙에 맞게 처리한다.",
            ),
        ]
    return [
        (
            "명령어가 글과 다르게 동작하는 경우",
            "같은 명령을 실행했는데 출력이 다르거나 실패한다.",
            "운영체제, 도구 버전, 실행 위치가 글의 기준과 같은지 먼저 확인한다.",
            "환경 차이를 적어 두고 한 단계씩 범위를 줄인다.",
        ),
        (
            "설정 파일을 바꿨는데 반영되지 않는 경우",
            "파일을 수정했지만 실행 결과가 그대로다.",
            "프로그램 재시작, 캐시, 현재 작업 디렉터리, 파일 경로를 확인한다.",
            "적용 대상 파일이 실제로 읽히는지 로그나 출력으로 검증한다.",
        ),
        (
            "공식 문서와 화면이 다른 경우",
            "문서와 현재 UI 또는 CLI 메시지가 다르게 보인다.",
            "문서 기준일과 현재 버전을 비교한다.",
            "변경 가능성이 있는 항목은 단정하지 말고 현재 환경 기준으로 재확인한다.",
        ),
    ]


def faq(t: str) -> list[tuple[str, str]]:
    if t == "rust":
        return [
            ("rustup과 rustc는 같은 건가요?", "아니다. rustup은 Rust toolchain을 설치하고 관리하는 도구이고, rustc는 Rust 코드를 컴파일하는 컴파일러다."),
            ("cargo 없이 Rust를 실행할 수 있나요?", "단일 파일은 rustc로 컴파일할 수 있다. 다만 실제 프로젝트에서는 cargo를 쓰는 흐름이 일반적이다."),
            ("VS Code 확장만 설치하면 Rust가 설치되나요?", "아니다. VS Code 확장은 편집 보조 도구이고, Rust toolchain 설치는 별도로 확인해야 한다."),
            ("rust-analyzer는 꼭 필요한가요?", "컴파일 자체에 필수는 아니지만 VS Code에서 코드 이해, 자동 완성, 오류 표시를 위해 설치하는 편이 좋다."),
            ("Hello World 다음에는 무엇을 보면 좋나요?", "변수, 타입, 제어 흐름, 함수, ownership 같은 기본 문법으로 넘어가면 흐름이 자연스럽다."),
        ]
    if t == "docker":
        return [
            ("Docker 이미지는 컨테이너와 같은 건가요?", "같지 않다. 이미지는 실행 전 템플릿이고 컨테이너는 이미지에서 실행된 인스턴스다."),
            ("tag와 digest 중 무엇을 써야 하나요?", "편의성은 tag가 좋지만 재현성이 중요하면 digest를 함께 확인하는 편이 안전하다."),
            ("Dockerfile만 있으면 항상 같은 이미지가 나오나요?", "기반 이미지 태그나 외부 패키지 상태에 따라 달라질 수 있다. 고정이 필요한 항목은 명시해야 한다."),
        ]
    if t == "kubernetes":
        return [
            ("Pod와 Deployment는 무엇이 다른가요?", "Pod는 실행 단위이고 Deployment는 Pod 복제와 업데이트를 관리하는 상위 리소스다."),
            ("kubectl 결과가 이상하면 무엇부터 확인하나요?", "먼저 현재 context와 namespace를 확인한다."),
            ("Service를 만들면 바로 외부에서 접속되나요?", "Service 타입과 클러스터 환경에 따라 다르다. NodePort, LoadBalancer, Ingress 조건을 따로 확인해야 한다."),
        ]
    if t == "jenkins":
        return [
            ("Freestyle과 Pipeline 중 무엇을 써야 하나요?", "간단한 작업은 Freestyle도 가능하지만 반복 관리와 코드 리뷰가 필요하면 Pipeline이 유리하다."),
            ("Jenkinsfile은 어디에 두나요?", "보통 애플리케이션 저장소 루트에 두고 코드와 함께 변경 이력을 관리한다."),
            ("플러그인은 많이 설치해도 되나요?", "필요한 것만 설치하는 편이 관리와 보안 측면에서 낫다."),
        ]
    if t == "git":
        return [
            ("commit 전에 꼭 확인할 것은 무엇인가요?", "`git status`와 `git diff`로 어떤 파일이 들어가는지 확인한다."),
            ("pull과 fetch는 무엇이 다른가요?", "fetch는 원격 변경을 가져오기만 하고, pull은 가져온 뒤 현재 브랜치에 합치는 흐름이다."),
            ("force push는 언제 조심해야 하나요?", "공유 브랜치에서는 다른 사람의 기록을 덮을 수 있으므로 팀 규칙이 있을 때만 사용한다."),
        ]
    return [
        ("이 글의 기준을 그대로 적용해도 되나요?", "테스트 환경과 버전이 같을 때 가장 가깝다. 다른 환경에서는 먼저 차이를 확인해야 한다."),
        ("공식 문서 링크는 왜 남기나요?", "기술 글은 시간이 지나면 바뀔 수 있으므로 확인 가능한 근거를 남기는 편이 좋다."),
        ("결과가 다르면 무엇을 먼저 봐야 하나요?", "명령어 위치, 버전, 운영체제, 설정 파일 경로를 먼저 비교한다."),
    ]


def body_without_frontmatter(text: str) -> str:
    return parse_source(text).body


def render_original_flow(body: str, t: str) -> str:
    sections = section_map(body)
    direct = section_by_names(sections, ["직접 재현한 결과", "Direct Reproduction Results", "재현 결과"])
    facts = section_by_names(sections, ["확인된 사실", "Confirmed Facts", "근거 기반 확인 사항"])
    problem = section_by_names(sections, ["문제 정의", "Problem Definition", "문제와 범위"])
    chosen = direct or problem or facts or body
    lines: list[str] = []

    code_blocks = extract_code_blocks(chosen)
    if code_blocks:
        lines.append("아래 명령은 이 글에서 바로 따라 하기 좋은 흐름만 뽑아 정리한 것이다.")
        lines.append("")
        for language, content in code_blocks[:6]:
            lines.append(f"```{language}")
            lines.append(content)
            lines.append("```")
            lines.append("")

    summary_items = first_sentences(chosen, 8)
    if summary_items:
        lines.append("명령어를 실행하기 전에 흐름을 이렇게 잡으면 덜 헷갈린다.")
        lines.append("")
        for item in summary_items[:6]:
            lines.append(f"- {item}")

    if not lines:
        lines.append("이 글은 환경, 실행 순서, 결과를 나눠서 읽는 편이 좋다.")
    return "\n".join(lines).strip()


def original_link_for_post(post: ManagedPost, doc: SourceDoc) -> str:
    raw_categories = doc.front_matter.get("categories")
    if isinstance(raw_categories, list) and raw_categories:
        category = str(raw_categories[0])
    elif isinstance(raw_categories, str) and raw_categories:
        category = raw_categories
    else:
        category = ""
    if category:
        return f"{SITE_URL}/{quote(category.strip('/'))}/{post.slug}/"
    return f"{SITE_URL}/{post.slug}/"


def render_tistory(post: ManagedPost, doc: SourceDoc, source_updated_at: str, now: str) -> str:
    candidates, focus_keyword, secondary = title_candidates(post, doc)
    best_title = candidates[0]
    t = topic(doc.front_matter, post.slug, doc.body)
    doc_info = extract_doc_info(doc.body)
    verify_date = verification_date(doc.body) or doc_info.get("검증 기준일")
    description = str(doc.front_matter.get("description") or "")
    tag_candidates = tags(doc.front_matter)[:8]
    sections = section_map(doc.body)
    summary = section_by_names(sections, ["요약", "Summary"])
    refs = section_by_names(sections, ["참고자료", "References", "참고 자료"])
    links = collect_links(refs or doc.body)

    frontmatter = {
        "channel": "tistory",
        "source": "github_blog",
        "slug": post.slug,
        "best_title": best_title,
        "title_candidates": candidates,
        "focus_keyword": focus_keyword,
        "secondary_keywords": secondary[:6],
        "content_type": "tutorial",
        "status": "ready_for_draft",
        "source_updated_at": source_updated_at,
        "variant_updated_at": now,
        "requires_manual_review": True,
    }

    intro_paragraphs = [
        f"이 글은 {focus_keyword}를 검색해서 들어온 사람이 처음 확인해야 할 흐름을 정리한 글이다.",
        description or f"{best_title}를 기준으로 환경, 실행 순서, 확인 포인트를 나눠 본다.",
        "실제로 따라 할 때 막히기 쉬운 지점과 확인 순서를 앞쪽에 배치했다.",
    ]
    if verify_date:
        intro_paragraphs.append(f"검증 기준일은 {verify_date}이며, 버전이나 화면은 시간이 지나면 달라질 수 있다.")

    covered = [
        f"{focus_keyword}를 시작하기 전에 확인할 환경",
        "핵심 용어와 도구의 역할 차이",
        "명령어 또는 설정을 실행하는 순서",
        "처음 막힐 때 먼저 확인할 문제 해결 포인트",
        "관련 공식 문서와 확인 기준",
    ]

    env_lines: list[str] = []
    for key in ["테스트 환경", "테스트 버전", "문서 성격", "출처 등급", "비고"]:
        if key in doc_info:
            env_lines.append(f"- {key}: {doc_info[key]}")
    if verify_date and not any("검증 기준일" in line for line in env_lines):
        env_lines.append(f"- 검증 기준일: {verify_date}")
    if not env_lines:
        env_lines.append("- 이 글에 명시된 환경과 버전 기준을 먼저 확인한다.")
        env_lines.append("- 다른 운영체제나 도구 버전에서는 메시지와 화면이 달라질 수 있다.")

    summary_items = first_sentences(summary or doc.body, 5)
    trouble = troubleshooting(t)
    faq_items = faq(t)

    lines: list[str] = ["---", yaml_doc(frontmatter).strip(), "---", "", f"# {best_title}", ""]
    lines.extend(["## 도입부", ""])
    for para in intro_paragraphs[:5]:
        lines.extend([para, ""])

    lines.extend(["## 이 글에서 다루는 내용", ""])
    lines.extend(f"- {item}" for item in covered)
    lines.append("")

    lines.extend(["## 실행 환경", ""])
    lines.extend(env_lines)
    lines.append("")

    lines.extend(["## 핵심 요약", ""])
    if summary_items:
        lines.extend(f"- {item}" for item in summary_items)
    else:
        lines.append(f"- {focus_keyword}를 이해하려면 환경, 명령, 결과를 나눠서 확인하는 편이 좋다.")
    lines.append("")

    lines.extend(["## 핵심 용어 비교", "", comparison_table(t, doc.body), ""])

    if t == "rust" and "rustup" in doc.body.lower():
        lines.extend(
            [
                "## rustup, rustc, cargo 차이",
                "",
                "Rust 입문에서 가장 먼저 헷갈리는 부분은 설치 도구와 실행 도구가 한꺼번에 등장한다는 점이다. `rustup`은 설치와 toolchain 관리를 맡고, `rustc`는 단일 파일을 컴파일하며, `cargo`는 실제 프로젝트 흐름을 관리한다.",
                "",
                "처음에는 세 도구를 모두 외우기보다 `설치 = rustup`, `단일 파일 확인 = rustc`, `프로젝트 실행 = cargo run` 정도로 나눠서 보면 충분하다.",
                "",
            ]
        )

    lines.extend(["## 단계별 실행 흐름", "", render_original_flow(doc.body, t), ""])

    lines.extend(["## 자주 막히는 문제", ""])
    for title, symptom, check, direction in trouble:
        lines.extend(
            [
                f"### {title}",
                f"- 증상: {symptom}",
                f"- 먼저 확인할 것: {check}",
                f"- 해결 방향: {direction}",
                "",
            ]
        )

    lines.extend(["## FAQ", ""])
    for question, answer in faq_items[:6]:
        lines.extend([f"### {question}", "", answer, ""])

    if links:
        lines.extend(["## 참고 자료", ""])
        for text, url in links:
            lines.append(f"- [{text}]({url})")
        lines.append("")

    lines.extend(
        [
            "## 마무리",
            "",
            f"{focus_keyword}를 볼 때는 명령어 자체보다 어떤 도구가 어떤 역할을 하는지 먼저 나누는 것이 중요하다. 그래야 오류가 났을 때 설치 문제인지, 실행 위치 문제인지, 설정 문제인지 빠르게 좁힐 수 있다.",
            "",
            "## 태그 후보",
            "",
        ]
    )
    tag_values = list(dict.fromkeys([focus_keyword, *secondary, *tag_candidates]))
    lines.extend(f"- {tag}" for tag in tag_values[:12])
    lines.extend(["", "## 원문 링크", "", f"- {original_link_for_post(post, doc)}"])
    return "\n".join(lines).strip() + "\n"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(read_text(path))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def variant_updated_at(path: Path) -> str | None:
    if not path.exists():
        return None
    match = FRONTMATTER_RE.match(read_text(path))
    if not match:
        return None
    front_matter = parse_front_matter(match.group(1))
    value = front_matter.get("variant_updated_at")
    return str(value) if value else None


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def metadata_for(
    root: Path,
    post: ManagedPost,
    doc: SourceDoc,
    status: str,
    scheduled_at: str | None,
    source_updated_at: str,
) -> dict[str, Any]:
    post_date = parse_datetime(doc.front_matter.get("date"), post.post_path)
    return {
        "schema_version": 1,
        "slug": post.slug,
        "title": doc.front_matter.get("title") or post.slug,
        "lang": doc.front_matter.get("lang"),
        "translation_key": doc.front_matter.get("translation_key"),
        "section": doc.front_matter.get("section"),
        "tags": tags(doc.front_matter),
        "status": status,
        "scheduled_at": scheduled_at,
        "source_date": post_date.isoformat() if post_date else None,
        "source_path": rel(post.source_path, root),
        "source_sha256": doc.source_hash,
        "source_updated_at": source_updated_at,
        "tistory_policy_version": POLICY_VERSION,
    }


def source_status(post: ManagedPost, doc: SourceDoc) -> tuple[str, str | None]:
    explicit = doc.front_matter.get("status")
    if isinstance(explicit, str) and explicit:
        status = explicit
    else:
        date = parse_datetime(doc.front_matter.get("date"), post.post_path)
        status = "scheduled" if date and date > datetime.now(KST) else "published"
    scheduled_at = None
    date = parse_datetime(doc.front_matter.get("date"), post.post_path)
    if status == "scheduled" and date:
        scheduled_at = date.isoformat()
    return status, scheduled_at


def tistory_status(
    previous: dict[str, Any],
    variant_existed: bool,
    variant_changed: bool,
    source_status_value: str,
    source_hash: str,
) -> tuple[str, str | None]:
    previous_tistory = previous.get("tistory") if isinstance(previous.get("tistory"), dict) else {}
    previous_status = previous_tistory.get("status")
    previous_reason = previous_tistory.get("reason")
    if (
        not variant_changed
        and previous_status in {"needs_manual_review", "draft_created", "scheduled", "published"}
    ):
        return str(previous_status), str(previous_reason) if previous_reason else None
    previous_source_hash = previous_tistory.get("source_sha256")
    previous_policy = previous_tistory.get("policy_version")
    source_or_policy_changed = bool(
        previous_source_hash
        and previous_source_hash != source_hash
        or previous_policy
        and previous_policy != POLICY_VERSION
    )
    if (
        source_status_value == "scheduled"
        and variant_existed
        and variant_changed
        and source_or_policy_changed
    ):
        return "needs_manual_review", "scheduled_post_variant_updated"
    return "ready_for_draft", None


def sync_one(root: Path, post: ManagedPost, dry_run: bool) -> dict[str, Any]:
    source_written = ensure_source(post, dry_run)
    if dry_run and not post.source_path.exists() and post.post_path:
        source_text = read_text(post.post_path)
    else:
        source_text = read_text(post.source_path)
    doc = parse_source(source_text)
    now = datetime.now(KST).isoformat()
    source_updated_at = (
        datetime.fromtimestamp((post.post_path or post.source_path).stat().st_mtime, KST).isoformat()
        if dry_run and not post.source_path.exists() and post.post_path
        else datetime.fromtimestamp(post.source_path.stat().st_mtime, KST).isoformat()
    )
    status, scheduled_at = source_status(post, doc)
    metadata_path = post.content_dir / "metadata.yaml"
    variant_path = post.content_dir / "variants" / "tistory.md"
    state_path = post.content_dir / "publish-state.json"
    previous_state = load_json(state_path)
    variant_existed = variant_path.exists()

    previous_tistory = (
        previous_state.get("tistory") if isinstance(previous_state.get("tistory"), dict) else {}
    )
    stable_variant_updated_at = (
        previous_tistory.get("updated_at")
        or variant_updated_at(variant_path)
        or now
    )
    candidate_variant_text = render_tistory(
        post, doc, source_updated_at, str(stable_variant_updated_at)
    )
    if variant_path.exists() and normalize_text(read_text(variant_path)).strip() + "\n" == normalize_text(candidate_variant_text).strip() + "\n":
        variant_text = candidate_variant_text
    else:
        variant_text = render_tistory(post, doc, source_updated_at, now)
    needs_quality_refresh = False
    if variant_path.exists():
        existing_variant = read_text(variant_path)
        needs_quality_refresh = any(
            marker not in existing_variant
            for marker in ["best_title:", "## 자주 막히는 문제", "## FAQ", "focus_keyword:"]
        )

    variant_changed = write_text_if_changed(variant_path, variant_text, dry_run)
    metadata = metadata_for(root, post, doc, status, scheduled_at, source_updated_at)
    metadata_changed = write_text_if_changed(metadata_path, yaml_doc(metadata), dry_run)
    t_status, reason = tistory_status(
        previous_state,
        variant_existed,
        variant_changed or needs_quality_refresh,
        status,
        doc.source_hash,
    )
    variant_hash = sha256_text(variant_text)

    state = previous_state.copy()
    state.setdefault("schema_version", 1)
    state["slug"] = post.slug
    state["source"] = {
        "path": rel(post.source_path, root),
        "source_sha256": doc.source_hash,
        "source_updated_at": source_updated_at,
        "status": status,
        "scheduled_at": scheduled_at,
    }
    state["policy_version"] = POLICY_VERSION
    state["tistory"] = {
        "status": t_status,
        "reason": reason,
        "requires_manual_review": True,
        "variant_path": "variants/tistory.md",
        "absolute_variant_path": rel(variant_path, root),
        "source_sha256": doc.source_hash,
        "variant_sha256": variant_hash,
        "policy_version": POLICY_VERSION,
        "updated_at": now if variant_changed else str(stable_variant_updated_at),
    }
    state_changed = write_json_if_changed(state_path, state, dry_run)
    return {
        "slug": post.slug,
        "source_written": source_written,
        "metadata_changed": metadata_changed,
        "variant_changed": variant_changed,
        "state_changed": state_changed,
        "tistory_status": t_status,
        "reason": reason,
        "scheduled": status == "scheduled",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--posts-root", default="_posts")
    parser.add_argument("--content-root", default="content/posts")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path.cwd()
    posts = discover_posts(root, root / args.posts_root, root / args.content_root)
    results = [sync_one(root, post, args.dry_run) for post in posts]
    status_counts: dict[str, int] = {}
    for result in results:
        status_counts[result["tistory_status"]] = status_counts.get(result["tistory_status"], 0) + 1
    summary = {
        "mode": "dry-run" if args.dry_run else "write",
        "checked_posts": len(results),
        "sources_written": sum(1 for result in results if result["source_written"]),
        "metadata_changed": sum(1 for result in results if result["metadata_changed"]),
        "variants_changed": sum(1 for result in results if result["variant_changed"]),
        "states_changed": sum(1 for result in results if result["state_changed"]),
        "scheduled_posts": sum(1 for result in results if result["scheduled"]),
        "tistory_status_counts": status_counts,
        "policy_version": POLICY_VERSION,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    changed_slugs = [
        result["slug"]
        for result in results
        if result["source_written"]
        or result["metadata_changed"]
        or result["variant_changed"]
        or result["state_changed"]
    ]
    if changed_slugs:
        preview = ", ".join(changed_slugs[:12])
        suffix = "" if len(changed_slugs) <= 12 else f", ... +{len(changed_slugs) - 12}"
        print(f"changed_slugs={preview}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
