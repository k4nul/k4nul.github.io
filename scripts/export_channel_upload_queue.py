#!/usr/bin/env python3
"""Export normalized Naver/Tistory upload queue items from channel variants."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sync_tistory_variants import (
    FRONTMATTER_RE,
    external_channel_exclusion_reason,
    normalize_text,
    parse_front_matter,
    read_text,
)


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

KST = timezone(timedelta(hours=9))
CHANNEL_FILES = {
    "naver": "naver.md",
    "tistory": "tistory.md",
}
EXPECTED_PLATFORM = {
    "naver": "naver_blog",
    "tistory": "tistory",
}
COMMON_REQUIRED = {
    "channel",
    "source",
    "slug",
    "post_folder",
    "variant_path",
    "best_title",
    "title_candidates",
    "focus_keyword",
    "secondary_keywords",
    "content_type",
    "status",
    "requires_manual_review",
    "content_group",
    "channel_category",
    "channel_category_slug",
    "publish_sequence",
    "planned_publish_date",
    "planned_publish_at",
    "publish_slot",
    "schedule_base_date",
}
CHANNEL_REQUIRED = {
    "naver": {"tone", "recommended_images"},
    "tistory": {"source_updated_at", "variant_updated_at"},
}
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
RELATIVE_URL_RE = re.compile(r"\{\{\s*['\"]([^'\"]+)['\"]\s*\|\s*relative_url\s*\}\}")


def json_default(value: Any) -> str:
    if isinstance(value, Path):
        return value.as_posix()
    return str(value)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(read_text(path))


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def parse_variant(path: Path) -> tuple[dict[str, Any], str]:
    text = normalize_text(read_text(path))
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter")
    frontmatter = parse_front_matter(match.group(1))
    body = text[match.end() :].lstrip("\n")
    return frontmatter, body


def normalize_image_reference(raw: str) -> str:
    value = raw.strip()
    match = RELATIVE_URL_RE.fullmatch(value)
    if match:
        value = match.group(1)
    if value.startswith("/"):
        value = value[1:]
    return value


def resolve_image_path(root: Path, reference: str, owner: Path) -> str:
    normalized = normalize_image_reference(reference)
    if re.match(r"^[a-z]+://", normalized, re.I):
        return normalized
    candidates = [normalized]
    decoded = unquote(normalized)
    if decoded != normalized:
        candidates.append(decoded)
    for candidate in candidates:
        path = Path(candidate)
        if path.is_absolute():
            return path.as_posix()
        root_candidate = root / path
        if root_candidate.exists():
            return rel(root_candidate, root)
        owner_candidate = owner.parent / path
        if owner_candidate.exists():
            return rel(owner_candidate, root)
    return normalized


def collect_markdown_images(root: Path, path: Path, label: str) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    text = read_text(path)
    assets: list[dict[str, Any]] = []
    for index, match in enumerate(MARKDOWN_IMAGE_RE.finditer(text), start=1):
        reference = match.group(2)
        local_path = resolve_image_path(root, reference, path)
        is_remote = bool(re.match(r"^[a-z]+://", local_path, re.I))
        exists = True if is_remote else (root / local_path).exists()
        assets.append(
            {
                "source": label,
                "index": index,
                "alt": match.group(1),
                "reference": reference,
                "path": local_path,
                "exists": exists,
                "remote": is_remote,
            }
        )
    return assets


def collect_image_assets(root: Path, post_dir: Path, variant_path: Path) -> list[dict[str, Any]]:
    seen: set[str] = set()
    assets: list[dict[str, Any]] = []
    for asset in [
        *collect_markdown_images(root, variant_path, "variant"),
        *collect_markdown_images(root, post_dir / "source.md", "source"),
    ]:
        key = str(asset.get("path"))
        if key in seen:
            continue
        seen.add(key)
        asset["upload_order"] = len(assets) + 1
        assets.append(asset)
    return assets


def validate_frontmatter(channel: str, frontmatter: dict[str, Any]) -> list[str]:
    required = COMMON_REQUIRED | CHANNEL_REQUIRED[channel]
    missing = sorted(key for key in required if key not in frontmatter)
    problems = [f"missing frontmatter field: {key}" for key in missing]
    expected_platform = EXPECTED_PLATFORM[channel]
    if frontmatter.get("channel") != expected_platform:
        problems.append(
            f"channel mismatch: expected {expected_platform}, got {frontmatter.get('channel')}"
        )
    return problems


def build_item(
    root: Path,
    post_dir: Path,
    channel: str,
    body_mode: str,
) -> tuple[dict[str, Any] | None, list[str]]:
    variant_path = post_dir / "variants" / CHANNEL_FILES[channel]
    state_path = post_dir / "publish-state.json"
    problems: list[str] = []
    if not variant_path.exists():
        return None, [f"missing variant: {variant_path.as_posix()}"]

    try:
        frontmatter, body = parse_variant(variant_path)
    except ValueError as exc:
        return None, [f"{variant_path.as_posix()}: {exc}"]

    problems.extend(validate_frontmatter(channel, frontmatter))
    state = load_json(state_path)
    channel_state = state.get(channel) if isinstance(state.get(channel), dict) else {}
    status = channel_state.get("status") or frontmatter.get("status")
    planned_publish_at = channel_state.get("planned_publish_at") or frontmatter.get(
        "planned_publish_at"
    )

    item: dict[str, Any] = {
        "slug": frontmatter.get("slug") or post_dir.name,
        "channel": channel,
        "platform": frontmatter.get("channel"),
        "post_folder": frontmatter.get("post_folder"),
        "variant_path": frontmatter.get("variant_path") or rel(variant_path, root),
        "state_path": rel(state_path, root),
        "body_format": "markdown",
        "parse_rule": "split leading YAML frontmatter, upload body after closing frontmatter",
        "title": frontmatter.get("best_title"),
        "title_candidates": frontmatter.get("title_candidates") or [],
        "status": status,
        "requires_manual_review": frontmatter.get("requires_manual_review"),
        "content_group": frontmatter.get("content_group"),
        "channel_category": frontmatter.get("channel_category"),
        "channel_category_slug": frontmatter.get("channel_category_slug"),
        "publish_sequence": frontmatter.get("publish_sequence"),
        "planned_publish_date": frontmatter.get("planned_publish_date"),
        "planned_publish_at": planned_publish_at,
        "publish_slot": frontmatter.get("publish_slot"),
        "focus_keyword": frontmatter.get("focus_keyword"),
        "secondary_keywords": frontmatter.get("secondary_keywords") or [],
        "variant_sha256": channel_state.get("variant_sha256"),
        "source_sha256": channel_state.get("source_sha256"),
    }
    if channel == "naver":
        item["recommended_images"] = frontmatter.get("recommended_images") or []
        item["image_slot_rule"] = "scan body lines that match [사진 N 삽입: ...]"
    else:
        item["image_slot_rule"] = "scan Markdown image syntax in body when present"
    image_assets = collect_image_assets(root, post_dir, variant_path)
    item["image_assets"] = image_assets
    item["image_asset_count"] = len(image_assets)
    item["missing_image_asset_count"] = sum(
        1 for asset in image_assets if not asset.get("exists")
    )

    if body_mode == "inline":
        item["body_markdown"] = body
    elif body_mode == "path":
        item["body_source"] = {
            "path": frontmatter.get("variant_path") or rel(variant_path, root),
            "frontmatter_delimiter": "---",
            "body_starts_after_frontmatter": True,
        }

    return item, problems


def collect_items(args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    root = Path(args.root).resolve()
    content_root = root / args.content_root
    channels = list(CHANNEL_FILES) if args.channel == "all" else [args.channel]
    statuses = set(args.status or [])
    items: list[dict[str, Any]] = []
    problems: list[dict[str, Any]] = []

    source_paths = sorted(path for path in content_root.glob("**/source.md") if path.is_file())
    for source_path in source_paths:
        post_dir = source_path.parent
        slug = post_dir.name
        if "-" in slug:
            slug = re.sub(r"^\d{3,6}-", "", slug)
        if external_channel_exclusion_reason(slug):
            continue
        for channel in channels:
            item, item_problems = build_item(root, post_dir, channel, args.body_mode)
            if item_problems:
                problems.append(
                    {
                        "slug": post_dir.name,
                        "channel": channel,
                        "problems": item_problems,
                    }
                )
            if not item:
                continue
            if statuses and item.get("status") not in statuses:
                continue
            if args.date and item.get("planned_publish_date") != args.date:
                continue
            items.append(item)

    items.sort(
        key=lambda item: (
            item.get("planned_publish_at") or "",
            item.get("channel") or "",
            item.get("slug") or "",
        )
    )
    return items, problems


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--content-root", default="content/posts")
    parser.add_argument("--channel", choices=["all", "naver", "tistory"], default="all")
    parser.add_argument("--status", action="append", help="Keep only this channel status")
    parser.add_argument("--date", help="Keep only this planned_publish_date")
    parser.add_argument(
        "--body-mode",
        choices=["path", "inline", "none"],
        default="path",
        help="Use path for compact queues, inline for direct upload payloads",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    items, problems = collect_items(args)
    output = {
        "schema_version": 1,
        "generated_at": datetime.now(KST).isoformat(),
        "body_mode": args.body_mode,
        "item_count": len(items),
        "problem_count": len(problems),
        "items": items,
        "problems": problems,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, default=json_default))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
