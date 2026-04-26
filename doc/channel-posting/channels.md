# external_channel_schema

```yaml
schema_version: 1
verification_date: "2026-04-25"
policy_scope: external_channel_variants_only
not_scope:
  - GitHub Pages post writing rules
  - Minimal Mistakes theme files
  - _posts front matter rules
  - docs/blog-style.md prose rules
canonical_source:
  path: content/posts/<stream>/<sequence>-<slug>/source.md
  bootstrap_source: _posts/<date>-<slug>.md
  rule:
    - source.md provides facts, code, verification dates, official links, and test versions
    - each channel variant rewrites structure and presentation for its platform
    - channel variants are not canonical replacements for GitHub source
```

```yaml
channels:
  naver:
    variant_path: content/posts/<stream>/<sequence>-<slug>/variants/naver.md
    purpose:
      - manual_upload_body
      - mobile_readable_technical_post
      - search_plus_feed_discovery
    primary_reader_mode:
      - quick_scan
      - problem_empathy
      - screenshot_guided_follow_along
    content_density: medium
    style_reference: doc/channel-posting/naver.md
    publish_route:
      primary: manual_review
      optional: browser_draft_when_requested
  tistory:
    variant_path: content/posts/<stream>/<sequence>-<slug>/variants/tistory.md
    purpose:
      - manual_upload_body
      - search_structured_technical_post
      - long_tail_problem_solving
    primary_reader_mode:
      - search_intent
      - step_by_step_resolution
      - troubleshooting_reference
    content_density: medium_high
    style_reference: doc/channel-posting/tistory.md
    publish_route:
      primary: manual_review
      optional: browser_draft_when_requested
```

```yaml
shared_frontmatter_fields:
  required:
    - channel
    - source
    - slug
    - best_title
    - title_candidates
    - focus_keyword
    - secondary_keywords
    - content_type
    - status
    - source_updated_at
    - variant_updated_at
    - requires_manual_review
  channel_values:
    - naver
    - tistory
  source_value: github_blog
  status_default: ready_for_draft
  requires_manual_review_default: true
  platform_topic_group:
    field: channel_category
    allowed_values:
      - AI
      - 프로그래밍 언어
      - DevOps
    slug_field: channel_category_slug
    slug_values:
      - ai
      - programming_language
      - devops
```
