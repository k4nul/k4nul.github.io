#!/usr/bin/env python3
"""Assign external-channel publish dates to AI and non-AI post streams."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from sync_tistory_variants import (
    EXTERNAL_CHANNEL_EXCLUDED_SLUGS,
    FRONTMATTER_RE,
    KST,
    external_channel_exclusion_reason,
    parse_datetime,
    parse_source,
    read_text,
    write_json_if_changed,
    write_text_if_changed,
)


BASE_DATE = "2026-04-26"
AI_SLOT_TIME = "09:00:00"
NON_AI_SLOT_TIME = "18:00:00"
ORDERED_POST_DIR_RE = re.compile(r"^\d{3,6}-(?P<slug>.+)$")
GROUP_DIRS = {
    "ai": "ai",
    "non_ai": "non-ai",
}
SCHEDULE_KEYS = {
    "post_folder",
    "source_path",
    "variant_path",
    "content_group",
    "channel_category",
    "channel_category_slug",
    "publish_sequence",
    "external_publish_sequence",
    "planned_publish_date",
    "planned_publish_at",
    "publish_slot",
    "schedule_base_date",
}
NON_AI_PREFIXES = (
    "docker-",
    "git-",
    "jenkins-",
    "jenkinsfile-",
    "kubernetes-",
    "rust-",
)
AI_TERMS = (
    "codex",
    "claude",
    "ai",
    "agent",
    "agents",
    "harness",
    "하네스",
    "토큰",
    "token",
    "context-budget",
    "auto-memory",
    "mcp",
    "guardrail",
    "guardrails",
    "instruction",
    "instructions",
    "prompt",
    "subagent",
    "subagents",
    "trace",
    "handoff",
    "schema",
    "enforcement",
    "compression",
    "memory",
)
CATEGORY_SLUGS = {
    "AI": "ai",
    "프로그래밍 언어": "programming_language",
    "DevOps": "devops",
}
PROGRAMMING_LANGUAGE_PREFIXES = (
    "rust-",
)
DEVOPS_PREFIXES = (
    "docker-",
    "git-",
    "jenkins-",
    "jenkinsfile-",
    "kubernetes-",
    "macro-malware",
    "rtf-malware",
)


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def yaml_quote(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def source_title(source_text: str) -> str:
    match = re.search(r"^title:\s*\"?([^\"\n]+)\"?", source_text, re.M)
    return match.group(1).strip() if match else ""


def slug_from_post_dir(post_dir: Path) -> str:
    match = ORDERED_POST_DIR_RE.match(post_dir.name)
    return match.group("slug") if match else post_dir.name


def rel_path(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def classify_post(slug: str, source_text: str) -> str:
    slug_lower = slug.lower()
    if slug_lower.startswith(NON_AI_PREFIXES):
        return "non_ai"
    title_lower = source_title(source_text).lower()
    haystack = f"{slug_lower} {title_lower}"
    return "ai" if any(term in haystack for term in AI_TERMS) else "non_ai"


def classify_channel_category(slug: str, source_text: str) -> str:
    slug_lower = slug.lower()
    if slug_lower.startswith(PROGRAMMING_LANGUAGE_PREFIXES):
        return "프로그래밍 언어"
    if slug_lower.startswith(DEVOPS_PREFIXES):
        return "DevOps"
    if classify_post(slug, source_text) == "ai":
        return "AI"
    return "DevOps"


def source_sort_key(source_path: Path) -> tuple[datetime, str]:
    doc = parse_source(read_text(source_path))
    parsed = parse_datetime(doc.front_matter.get("date"), None)
    if not parsed:
        parsed = datetime.fromtimestamp(source_path.stat().st_mtime, KST)
    return parsed, slug_from_post_dir(source_path.parent)


def ordered_dir_name(sequence: int, slug: str) -> str:
    return f"{sequence:03d}-{slug}"


def desired_post_dir(content_root: Path, slug: str, group: str, sequence: int) -> Path:
    return content_root / GROUP_DIRS[group] / ordered_dir_name(sequence, slug)


def build_plan(
    root: Path,
    base_date: str,
    group: str,
    category: str,
    sequence: int,
    post_dir: Path,
) -> dict[str, Any]:
    base = datetime.strptime(base_date, "%Y-%m-%d").replace(tzinfo=KST)
    day = base + timedelta(days=sequence - 1)
    slot_time = AI_SLOT_TIME if group == "ai" else NON_AI_SLOT_TIME
    hour, minute, second = map(int, slot_time.split(":"))
    planned = day.replace(hour=hour, minute=minute, second=second)
    return {
        "post_folder": rel_path(post_dir, root),
        "source_path": rel_path(post_dir / "source.md", root),
        "content_group": group,
        "channel_category": category,
        "channel_category_slug": CATEGORY_SLUGS[category],
        "publish_sequence": sequence,
        "external_publish_sequence": sequence,
        "planned_publish_date": day.date().isoformat(),
        "planned_publish_at": planned.isoformat(),
        "publish_slot": "ai_daily" if group == "ai" else "non_ai_daily",
        "schedule_base_date": base_date,
    }


def strip_schedule_lines(lines: list[str]) -> list[str]:
    result: list[str] = []
    for line in lines:
        if any(re.match(rf"^{re.escape(key)}:", line) for key in SCHEDULE_KEYS):
            continue
        result.append(line)
    while result and not result[-1].strip():
        result.pop()
    return result


def append_schedule_block(text: str, plan: dict[str, Any]) -> str:
    lines = strip_schedule_lines(normalize(text).strip().splitlines())
    additions = [
        f"post_folder: {yaml_quote(plan['post_folder'])}",
        f"source_path: {yaml_quote(plan['source_path'])}",
        f"content_group: {yaml_quote(plan['content_group'])}",
        f"channel_category: {yaml_quote(plan['channel_category'])}",
        f"channel_category_slug: {yaml_quote(plan['channel_category_slug'])}",
        f"external_publish_sequence: {yaml_quote(plan['external_publish_sequence'])}",
        f"planned_publish_date: {yaml_quote(plan['planned_publish_date'])}",
        f"planned_publish_at: {yaml_quote(plan['planned_publish_at'])}",
        f"publish_slot: {yaml_quote(plan['publish_slot'])}",
        f"schedule_base_date: {yaml_quote(plan['schedule_base_date'])}",
    ]
    return "\n".join([*lines, *additions]) + "\n"


def update_variant_frontmatter(text: str, plan: dict[str, Any], variant_path: Path, root: Path) -> str:
    normalized = normalize(text)
    match = FRONTMATTER_RE.match(normalized)
    if not match:
        return normalized
    frontmatter = match.group(1)
    rest = normalized[match.end() :].lstrip("\n")
    lines = strip_schedule_lines(frontmatter.splitlines())
    additions = [
        f"post_folder: {yaml_quote(plan['post_folder'])}",
        f"variant_path: {yaml_quote(rel_path(variant_path, root))}",
        f"content_group: {yaml_quote(plan['content_group'])}",
        f"channel_category: {yaml_quote(plan['channel_category'])}",
        f"channel_category_slug: {yaml_quote(plan['channel_category_slug'])}",
        f"publish_sequence: {yaml_quote(plan['publish_sequence'])}",
        f"planned_publish_date: {yaml_quote(plan['planned_publish_date'])}",
        f"planned_publish_at: {yaml_quote(plan['planned_publish_at'])}",
        f"publish_slot: {yaml_quote(plan['publish_slot'])}",
        f"schedule_base_date: {yaml_quote(plan['schedule_base_date'])}",
    ]
    return "---\n" + "\n".join([*lines, *additions]) + "\n---\n\n" + rest.strip() + "\n"


def update_state(path: Path, plan: dict[str, Any], root: Path, post_dir: Path, dry_run: bool) -> bool:
    data = json.loads(read_text(path)) if path.exists() else {}
    data["external_publish_plan"] = {
        "post_folder": plan["post_folder"],
        "source_path": plan["source_path"],
        "content_group": plan["content_group"],
        "channel_category": plan["channel_category"],
        "channel_category_slug": plan["channel_category_slug"],
        "sequence": plan["publish_sequence"],
        "planned_publish_date": plan["planned_publish_date"],
        "planned_publish_at": plan["planned_publish_at"],
        "publish_slot": plan["publish_slot"],
        "base_date": plan["schedule_base_date"],
        "cadence_days": 1,
        "timezone": "Asia/Seoul",
    }
    if isinstance(data.get("source"), dict):
        data["source"]["path"] = plan["source_path"]
    for channel in ("naver", "tistory"):
        if isinstance(data.get(channel), dict):
            variant_path = post_dir / "variants" / f"{channel}.md"
            data[channel]["variant_path"] = f"variants/{channel}.md"
            data[channel]["absolute_variant_path"] = rel_path(variant_path, root)
            data[channel]["content_group"] = plan["content_group"]
            data[channel]["channel_category"] = plan["channel_category"]
            data[channel]["channel_category_slug"] = plan["channel_category_slug"]
            data[channel]["publish_sequence"] = plan["publish_sequence"]
            data[channel]["planned_publish_date"] = plan["planned_publish_date"]
            data[channel]["planned_publish_at"] = plan["planned_publish_at"]
            data[channel]["publish_slot"] = plan["publish_slot"]
    return write_json_if_changed(path, data, dry_run)


def collect_posts(content_root: Path) -> list[Path]:
    sources: dict[str, Path] = {}
    for path in sorted(content_root.glob("**/source.md")):
        if not path.is_file():
            continue
        slug = slug_from_post_dir(path.parent)
        if external_channel_exclusion_reason(slug):
            continue
        if slug in sources:
            raise RuntimeError(
                f"Duplicate managed post slug {slug}: {sources[slug]} and {path}"
            )
        sources[slug] = path
    return sorted(sources.values())


def ensure_post_dir(
    source_path: Path,
    content_root: Path,
    target_dir: Path,
    dry_run: bool,
) -> tuple[Path, bool]:
    current_dir = source_path.parent
    if current_dir.resolve() == target_dir.resolve():
        return current_dir, False
    if target_dir.exists():
        raise RuntimeError(f"Target post directory already exists: {target_dir}")
    if not dry_run:
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        current_dir.rename(target_dir)
        if current_dir.parent != content_root and current_dir.parent.exists():
            try:
                current_dir.parent.rmdir()
            except OSError:
                pass
    return target_dir, True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content-root", default="content/posts")
    parser.add_argument("--base-date", default=BASE_DATE)
    parser.add_argument("--schedule-output", default="content/channel-publish-schedule.json")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(".")
    content_root = Path(args.content_root)
    grouped: dict[str, list[Path]] = {"ai": [], "non_ai": []}
    for source_path in collect_posts(content_root):
        source_text = read_text(source_path)
        group = classify_post(slug_from_post_dir(source_path.parent), source_text)
        grouped[group].append(source_path)
    for group in grouped:
        grouped[group].sort(key=source_sort_key)

    changes = {
        "folder_moves": 0,
        "metadata": 0,
        "naver": 0,
        "tistory": 0,
        "state": 0,
    }
    category_counts = {category: 0 for category in CATEGORY_SLUGS}
    schedule_rows: list[dict[str, Any]] = []
    for group, posts in grouped.items():
        for index, source_path in enumerate(posts, start=1):
            slug = slug_from_post_dir(source_path.parent)
            source_text = read_text(source_path)
            target_dir = desired_post_dir(content_root, slug, group, index)
            post_dir, moved = ensure_post_dir(source_path, content_root, target_dir, args.dry_run)
            if moved:
                changes["folder_moves"] += 1
            source_path = post_dir / "source.md"
            category = classify_channel_category(slug, source_text)
            plan = build_plan(root, args.base_date, group, category, index, post_dir)
            category_counts[category] += 1
            metadata_path = post_dir / "metadata.yaml"
            state_path = post_dir / "publish-state.json"
            naver_path = post_dir / "variants" / "naver.md"
            tistory_path = post_dir / "variants" / "tistory.md"
            if metadata_path.exists():
                if write_text_if_changed(
                    metadata_path,
                    append_schedule_block(read_text(metadata_path), plan),
                    args.dry_run,
                ):
                    changes["metadata"] += 1
            if naver_path.exists():
                if write_text_if_changed(
                    naver_path,
                    update_variant_frontmatter(read_text(naver_path), plan, naver_path, root),
                    args.dry_run,
                ):
                    changes["naver"] += 1
            if tistory_path.exists():
                if write_text_if_changed(
                    tistory_path,
                    update_variant_frontmatter(read_text(tistory_path), plan, tistory_path, root),
                    args.dry_run,
                ):
                    changes["tistory"] += 1
            if state_path.exists() and update_state(state_path, plan, root, post_dir, args.dry_run):
                changes["state"] += 1
            schedule_rows.append(
                {
                    "slug": slug,
                    "post_folder": plan["post_folder"],
                    "source_path": plan["source_path"],
                    "naver_variant_path": rel_path(naver_path, root),
                    "tistory_variant_path": rel_path(tistory_path, root),
                    "content_group": group,
                    "channel_category": plan["channel_category"],
                    "channel_category_slug": plan["channel_category_slug"],
                    "sequence": index,
                    "planned_publish_date": plan["planned_publish_date"],
                    "planned_publish_at": plan["planned_publish_at"],
                    "publish_slot": plan["publish_slot"],
                }
            )

    schedule_doc = {
        "schema_version": 1,
        "base_date": args.base_date,
        "timezone": "Asia/Seoul",
        "rule": "one AI post and one non-AI post per day from the beginning of each stream",
        "exclusion_rule": "security topics stay on GitHub only and are not scheduled for Naver/Tistory",
        "excluded_posts": sorted(EXTERNAL_CHANNEL_EXCLUDED_SLUGS),
        "slots": {
            "ai_daily": "09:00:00+09:00",
            "non_ai_daily": "18:00:00+09:00",
        },
        "counts": {
            "ai": len(grouped["ai"]),
            "non_ai": len(grouped["non_ai"]),
        },
        "channel_categories": {
            "allowed": list(CATEGORY_SLUGS.keys()),
            "counts": category_counts,
        },
        "posts": sorted(schedule_rows, key=lambda row: (row["planned_publish_date"], row["publish_slot"], row["sequence"])),
    }
    schedule_output_changed = write_json_if_changed(
        Path(args.schedule_output), schedule_doc, args.dry_run
    )

    summary = {
        "mode": "dry-run" if args.dry_run else "write",
        "base_date": args.base_date,
        "ai_posts": len(grouped["ai"]),
        "non_ai_posts": len(grouped["non_ai"]),
        "channel_category_counts": category_counts,
        "changes": changes,
        "schedule_output": args.schedule_output,
        "schedule_output_changed": schedule_output_changed,
        "first_ai": schedule_rows[0] if schedule_rows else None,
        "last_ai": next((row for row in reversed(schedule_rows) if row["content_group"] == "ai"), None),
        "last_non_ai": next((row for row in reversed(schedule_rows) if row["content_group"] == "non_ai"), None),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
