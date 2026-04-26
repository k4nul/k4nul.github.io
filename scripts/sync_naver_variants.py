#!/usr/bin/env python3
"""Generate Naver Blog final-post variants for every managed post."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote

from sync_tistory_variants import (
    FRONTMATTER_RE,
    IMAGE_RE,
    KST,
    SourceDoc,
    clean_title,
    collect_links,
    comparison_table,
    discover_posts,
    ensure_source,
    extract_code_blocks,
    extract_doc_info,
    faq,
    first_sentences,
    load_json,
    normalize_text,
    parse_datetime,
    parse_front_matter,
    parse_source,
    read_text,
    rel,
    section_by_names,
    section_map,
    sha256_text,
    tags,
    title_candidates as tistory_title_candidates,
    topic,
    troubleshooting,
    write_json_if_changed,
    write_text_if_changed,
    yaml_doc,
)


SITE_URL = "https://www.k4nul.com"
POLICY_VERSION = "2026-04-25.naver-final-post.v3"


def variant_frontmatter(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    match = FRONTMATTER_RE.match(read_text(path))
    if not match:
        return {}
    return parse_front_matter(match.group(1))


def source_updated_at(post_path: Path, source_path: Path) -> str:
    path = source_path if source_path.exists() else post_path
    return datetime.fromtimestamp(path.stat().st_mtime, KST).isoformat()


def source_status(post_path: Path | None, doc: SourceDoc) -> tuple[str, str | None]:
    explicit = doc.front_matter.get("status")
    if isinstance(explicit, str) and explicit:
        status = explicit
    else:
        date = parse_datetime(doc.front_matter.get("date"), post_path)
        status = "scheduled" if date and date > datetime.now(KST) else "published"
    scheduled_at = None
    date = parse_datetime(doc.front_matter.get("date"), post_path)
    if status == "scheduled" and date:
        scheduled_at = date.isoformat()
    return status, scheduled_at


def naver_title_candidates(slug: str, doc: SourceDoc) -> tuple[list[str], str, list[str]]:
    tistory_candidates, focus_keyword, secondary = tistory_title_candidates(
        type("PostLike", (), {"slug": slug})(), doc
    )
    original = str(doc.front_matter.get("title") or slug)
    cleaned = clean_title(original)
    current_topic = topic(doc.front_matter, slug, doc.body)

    if current_topic == "rust" and "install" in slug:
        candidates = [
            "Windows에서 Rust 설치하고 Hello World 실행해보기",
            "VS Code로 Rust 시작하기: 설치부터 첫 실행까지",
            "Rust 처음 시작할 때 헷갈리는 rustup, rustc, cargo 정리",
            "Rust 입문자를 위한 설치와 Hello World 실행 방법",
            "윈도우에서 Rust 개발 환경 세팅하는 가장 쉬운 흐름",
        ]
        return candidates, "Windows Rust 설치", [
            "VS Code Rust 실행",
            "Rust Hello World",
            "rustup 설치",
            "cargo run",
        ]

    base = tistory_candidates[0] if tistory_candidates else cleaned
    candidates = [
        base.replace("정리:", "쉽게 정리:").replace("실무 정리", "쉽게 정리"),
        f"{cleaned} 쉽게 이해하기",
        f"{cleaned} 따라 하면서 정리하기",
        f"{cleaned} 처음 볼 때 헷갈리는 부분 정리",
        f"{cleaned} 시작하기 전에 알아둘 것",
    ]
    unique_candidates = []
    for candidate in candidates:
        candidate = re.sub(r"^\s*(Rust|Docker|Git|K8S|Jenkins)\s+\d+\.\s*", "", candidate).strip()
        if candidate and candidate not in unique_candidates:
            unique_candidates.append(candidate)
    while len(unique_candidates) < 5:
        unique_candidates.append(f"{cleaned} 블로그식 정리 {len(unique_candidates) + 1}")
    return unique_candidates[:5], focus_keyword, secondary[:4]


def recommended_images(doc: SourceDoc, focus_keyword: str) -> list[str]:
    image_matches = list(IMAGE_RE.finditer(doc.body))
    if image_matches:
        return [
            f"본문 이미지 {index}: 단계 확인용 캡처"
            for index, _ in enumerate(image_matches[:5], start=1)
        ]
    return [
        f"{focus_keyword} 전체 흐름을 보여주는 대표 이미지",
        "명령어 실행 결과 또는 설정 화면 캡처",
    ]


def image_slots(doc: SourceDoc) -> list[str]:
    slots: list[str] = []
    for index, match in enumerate(IMAGE_RE.finditer(doc.body), start=1):
        raw = match.group(0)
        alt_match = re.match(r"!\[([^\]]*)\]", raw)
        alt = alt_match.group(1).strip() if alt_match and alt_match.group(1).strip() else "단계 확인 이미지"
        slots.append(f"[사진 {index} 삽입: {alt}]")
    return slots


def doc_info_lines(doc: SourceDoc) -> list[str]:
    info = extract_doc_info(doc.body)
    lines: list[str] = []
    for key in ["테스트 환경", "테스트 버전", "검증 기준일"]:
        if key in info:
            lines.append(f"- {key}: {info[key]}")
    if not any("검증 기준일" in line for line in lines):
        verification = re.search(r"검증 기준일:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", doc.body)
        if verification:
            lines.append(f"- 검증 기준일: {verification.group(1)}")
    if not lines:
        lines = [
            "- 이 글에서 기준으로 삼은 환경과 버전을 먼저 확인해 주세요.",
            "- 다른 운영체제나 버전에서는 화면과 메시지가 조금 다를 수 있습니다.",
        ]
    return lines


def naver_intro(doc: SourceDoc, best_title: str, focus_keyword: str) -> list[str]:
    description = str(doc.front_matter.get("description") or "")
    current_topic = topic(doc.front_matter, "", doc.body)
    if current_topic == "rust" and "rustup" in doc.body.lower():
        return [
            "Rust를 처음 설치하려고 하면 `rustup`, `rustc`, `cargo` 같은 이름이 한꺼번에 나와서 헷갈릴 수 있습니다.",
            "이 글에서는 Windows와 VS Code 기준으로 Rust를 설치하고, Hello World를 직접 실행하는 흐름만 차근차근 정리해보겠습니다.",
            "끝까지 따라 하면 Rust 설치 확인부터 `cargo run`으로 첫 프로젝트를 실행하는 단계까지 한 번에 확인할 수 있습니다.",
        ]
    return [
        f"{focus_keyword}를 처음 확인할 때 막히기 쉬운 부분을 블로그식으로 풀어 정리했습니다.",
        description or f"이번 글에서는 {best_title} 흐름을 너무 딱딱하지 않게 따라가 보겠습니다.",
        "검증 기준과 공식 링크는 유지하되, 실제로 읽고 옮기기 편한 순서로 다시 정리했습니다.",
    ]


def render_code_flow(doc: SourceDoc) -> str:
    sections = section_map(doc.body)
    direct = section_by_names(sections, ["직접 재현한 결과", "Direct Reproduction Results", "재현 결과"])
    problem = section_by_names(sections, ["문제 정의", "Problem Definition", "문제와 범위"])
    chosen = direct or problem or doc.body
    blocks = extract_code_blocks(chosen, limit=5)
    slots = image_slots(doc)
    lines: list[str] = []

    if not blocks:
        summary = first_sentences(chosen, 5)
        for sentence in summary:
            lines.append(sentence)
            lines.append("")
        for slot in slots[:3]:
            lines.append(slot)
            lines.append("")
        return "\n".join(lines).strip()

    for index, (language, content) in enumerate(blocks, start=1):
        is_output = language.lower() in {"text", "console", "output"}
        if is_output:
            lines.append("위 단계가 정상적으로 진행되면 아래처럼 결과를 확인할 수 있습니다.")
        else:
            lines.append("아래 명령어는 이 단계에서 실제로 확인할 내용을 실행하는 부분입니다.")
        lines.append("")
        lines.append(f"```{language}")
        lines.append(content)
        lines.append("```")
        lines.append("")
        if is_output:
            lines.append("출력 문구가 완전히 같지 않아도, 버전이나 실행 결과가 확인되면 같은 단계로 볼 수 있습니다.")
        else:
            lines.append("여기서 중요한 것은 명령어를 외우는 것보다, 이 단계가 무엇을 확인하는지 이해하는 것입니다.")
        lines.append("")
        if index <= len(slots):
            lines.append(slots[index - 1])
            lines.append("")
    return "\n".join(lines).strip()


def common_confusions(doc: SourceDoc) -> list[tuple[str, str]]:
    current_topic = topic(doc.front_matter, "", doc.body)
    if current_topic == "rust":
        return [
            ("rustup과 rustc가 같은 것처럼 보이는 경우", "`rustup`은 설치와 버전 관리를 맡고, `rustc`는 실제 컴파일러라고 나눠서 보면 됩니다."),
            ("cargo가 왜 필요한지 헷갈리는 경우", "단일 파일 확인은 `rustc`로 가능하지만, 실제 프로젝트 생성과 실행은 `cargo` 흐름이 훨씬 자연스럽습니다."),
            ("VS Code 확장만 설치하면 끝난다고 생각하는 경우", "확장은 편집을 도와주는 도구이고, Rust toolchain 설치 여부는 별도로 확인해야 합니다."),
        ]
    if current_topic == "docker":
        return [
            ("이미지와 컨테이너를 같은 것으로 보는 경우", "이미지는 실행 전 템플릿이고, 컨테이너는 이미지에서 실제로 실행된 상태라고 나눠 보면 됩니다."),
            ("태그만 보면 항상 같은 결과라고 생각하는 경우", "태그는 바뀔 수 있으니 재현성이 중요하면 digest까지 확인하는 편이 좋습니다."),
        ]
    if current_topic == "kubernetes":
        return [
            ("Pod와 Deployment가 헷갈리는 경우", "Pod는 실행 단위이고, Deployment는 Pod를 관리하는 상위 리소스라고 보면 됩니다."),
            ("kubectl 결과가 이상한 경우", "명령이 틀렸다고 보기 전에 context와 namespace를 먼저 확인하는 것이 좋습니다."),
        ]
    return [
        ("명령어만 따라 하면 된다고 생각하는 경우", "명령어보다 먼저 어떤 상태를 확인하는 단계인지 보는 편이 좋습니다."),
        ("글과 결과가 조금 다르면 실패라고 생각하는 경우", "버전이나 운영체제가 다르면 출력 문구는 달라질 수 있습니다. 핵심 상태가 같은지 확인해보세요."),
    ]


def original_link_for_post(post: Any, doc: SourceDoc) -> str:
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


def render_naver(post_slug: str, doc: SourceDoc, updated_at: str, source_link: str) -> str:
    title_candidates, focus_keyword, secondary = naver_title_candidates(post_slug, doc)
    best_title = title_candidates[0]
    recommended = recommended_images(doc, focus_keyword)
    current_topic = topic(doc.front_matter, post_slug, doc.body)
    sections = section_map(doc.body)
    summary = section_by_names(sections, ["요약", "Summary"])
    summary_items = first_sentences(summary or doc.body, 4)
    trouble_items = troubleshooting(current_topic)[:4]
    faq_items = faq(current_topic)[:4]
    links = collect_links(section_by_names(sections, ["참고자료", "References", "참고 자료"]) or doc.body)
    tag_values = list(dict.fromkeys([focus_keyword, *secondary, *tags(doc.front_matter)]))[:12]
    frontmatter = {
        "channel": "naver_blog",
        "source": "github_blog",
        "slug": post_slug,
        "best_title": best_title,
        "title_candidates": title_candidates,
        "focus_keyword": focus_keyword,
        "secondary_keywords": secondary[:4],
        "content_type": "beginner_guide",
        "tone": "friendly_explainer",
        "status": "ready_for_draft",
        "requires_manual_review": True,
        "recommended_images": recommended,
    }

    lines: list[str] = ["---", yaml_doc(frontmatter).strip(), "---", ""]
    lines.extend(["# 제목 후보와 선택 제목", ""])
    lines.append(f"- 선택 제목: {best_title}")
    for index, candidate in enumerate(title_candidates, start=1):
        lines.append(f"- 후보 {index}: {candidate}")
    lines.extend(["", f"# {best_title}", ""])

    lines.extend(["## 도입부", ""])
    for paragraph in naver_intro(doc, best_title, focus_keyword):
        lines.extend([paragraph, ""])

    lines.extend(["## 이 글에서 해볼 것", ""])
    lines.extend(
        [
            f"- {focus_keyword} 흐름을 처음부터 확인합니다.",
            "- 필요한 환경과 기준 버전을 먼저 봅니다.",
            "- 핵심 개념을 너무 어렵지 않게 나눠 봅니다.",
            "- 실제 명령어와 결과를 보면서 따라갑니다.",
            "- 막힐 때 먼저 확인할 부분을 정리합니다.",
            "",
        ]
    )

    lines.extend(["## 먼저 결론", ""])
    if summary_items:
        lines.extend(f"- {item}" for item in summary_items[:4])
    else:
        lines.append(f"- {focus_keyword}는 환경, 개념, 실행 흐름을 나눠서 보면 훨씬 덜 헷갈립니다.")
    lines.append("")

    lines.extend(["## 이 글의 기준 환경", ""])
    lines.extend(doc_info_lines(doc))
    lines.append("")

    lines.extend(["## 핵심 개념을 쉽게 정리", ""])
    lines.append("먼저 용어를 한 번 나눠두면 뒤에서 명령어를 볼 때 훨씬 편합니다.")
    lines.append("")
    lines.append(comparison_table(current_topic, doc.body))
    lines.append("")

    lines.extend(["## 단계별 따라 하기", "", render_code_flow(doc), ""])

    lines.extend(["## 처음에 자주 헷갈리는 부분", ""])
    for title, explanation in common_confusions(doc):
        lines.extend([f"### {title}", "", explanation, ""])

    lines.extend(["## 따라 하다 막힐 때 확인할 것", ""])
    for title, symptom, check, direction in trouble_items:
        lines.extend(
            [
                f"### {title}",
                f"- 이런 증상이 보이면: {symptom}",
                f"- 먼저 확인할 것: {check}",
                f"- 이렇게 해보세요: {direction}",
                "",
            ]
        )

    lines.extend(["## 오늘의 정리", ""])
    lines.extend(
        [
            f"정리하면, {focus_keyword}를 볼 때는 명령어를 무작정 외우기보다 각 도구와 단계가 무엇을 확인하는지 나눠 보는 것이 좋습니다.",
            "",
            "처음에는 결과가 조금 다르게 보여도 바로 실패라고 보기보다, 운영체제와 버전 차이를 먼저 확인해보면 좋습니다.",
            "",
        ]
    )

    lines.extend(["## 참고한 자료", ""])
    if links:
        for text, url in links:
            lines.append(f"- [{text}]({url})")
    else:
        lines.append("- 확인 가능한 공식 문서와 직접 확인한 결과를 기준으로 정리했습니다.")
    lines.append("")

    lines.extend(["## 태그 후보", ""])
    lines.extend(f"- {tag}" for tag in tag_values)
    lines.extend(["", "## 원문 링크", "", f"- {source_link}"])
    return "\n".join(lines).strip() + "\n"


def naver_status(previous: dict[str, Any], variant_changed: bool, source_status_value: str) -> tuple[str, str | None]:
    previous_naver = previous.get("naver") if isinstance(previous.get("naver"), dict) else {}
    previous_status = previous_naver.get("status")
    previous_reason = previous_naver.get("reason")
    if not variant_changed and previous_status in {"needs_manual_review", "draft_created", "scheduled", "published"}:
        return str(previous_status), str(previous_reason) if previous_reason else None
    if source_status_value == "scheduled" and previous_naver and variant_changed:
        return "needs_manual_review", "scheduled_post_variant_updated"
    return "ready_for_draft", None


def sync_one(root: Path, post: Any, dry_run: bool) -> dict[str, Any]:
    source_written = ensure_source(post, dry_run)
    source_text = read_text(post.source_path if post.source_path.exists() else post.post_path)
    doc = parse_source(source_text)
    source_hash = sha256_text(source_text)
    source_status_value, scheduled_at = source_status(post.post_path, doc)
    updated_at = source_updated_at(post.post_path or post.source_path, post.source_path)
    variant_path = post.content_dir / "variants" / "naver.md"
    previous_state = load_json(post.content_dir / "publish-state.json")
    previous_naver = previous_state.get("naver") if isinstance(previous_state.get("naver"), dict) else {}
    stable_updated_at = previous_naver.get("updated_at") or datetime.now(KST).isoformat()
    source_link = original_link_for_post(post, doc)
    candidate = render_naver(post.slug, doc, str(stable_updated_at), source_link)
    if variant_path.exists() and normalize_text(read_text(variant_path)).strip() + "\n" == normalize_text(candidate).strip() + "\n":
        variant_text = candidate
    else:
        variant_text = render_naver(post.slug, doc, datetime.now(KST).isoformat(), source_link)
    variant_changed = write_text_if_changed(variant_path, variant_text, dry_run)
    variant_hash = sha256_text(variant_text)
    status, reason = naver_status(previous_state, variant_changed, source_status_value)

    state = previous_state.copy()
    state.setdefault("schema_version", 1)
    state["slug"] = post.slug
    state["source"] = {
        "path": rel(post.source_path, root),
        "source_sha256": source_hash,
        "source_updated_at": updated_at,
        "status": source_status_value,
        "scheduled_at": scheduled_at,
    }
    state["naver"] = {
        "status": status,
        "reason": reason,
        "requires_manual_review": True,
        "variant_path": "variants/naver.md",
        "absolute_variant_path": rel(variant_path, root),
        "source_sha256": source_hash,
        "variant_sha256": variant_hash,
        "policy_version": POLICY_VERSION,
        "updated_at": datetime.now(KST).isoformat() if variant_changed else str(stable_updated_at),
    }
    state_changed = write_json_if_changed(post.content_dir / "publish-state.json", state, dry_run)
    return {
        "slug": post.slug,
        "source_written": source_written,
        "variant_changed": variant_changed,
        "state_changed": state_changed,
        "naver_status": status,
        "scheduled": source_status_value == "scheduled",
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
        status_counts[result["naver_status"]] = status_counts.get(result["naver_status"], 0) + 1
    summary = {
        "mode": "dry-run" if args.dry_run else "write",
        "checked_posts": len(results),
        "sources_written": sum(1 for result in results if result["source_written"]),
        "variants_changed": sum(1 for result in results if result["variant_changed"]),
        "states_changed": sum(1 for result in results if result["state_changed"]),
        "scheduled_posts": sum(1 for result in results if result["scheduled"]),
        "naver_status_counts": status_counts,
        "policy_version": POLICY_VERSION,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    changed = [
        result["slug"]
        for result in results
        if result["source_written"] or result["variant_changed"] or result["state_changed"]
    ]
    if changed:
        preview = ", ".join(changed[:12])
        suffix = "" if len(changed) <= 12 else f", ... +{len(changed) - 12}"
        print(f"changed_slugs={preview}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
