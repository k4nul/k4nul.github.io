# external_channel_automation_parser_schema

```yaml
schema_version: 1
verification_date: "2026-04-25"
purpose: tell an upload automation how to parse Naver and Tistory variant posts
scope:
  - content/posts/<stream>/<sequence>-<slug>/variants/naver.md
  - content/posts/<stream>/<sequence>-<slug>/variants/tistory.md
  - content/posts/<stream>/<sequence>-<slug>/publish-state.json
not_scope:
  - generating new post text
  - changing GitHub canonical _posts dates
  - deciding platform credentials or browser automation details
  - uploading security topic posts
git_policy:
  variant_files:
    - content/posts/<stream>/<sequence>-<slug>/variants/naver.md
    - content/posts/<stream>/<sequence>-<slug>/variants/tistory.md
  tracking: ignored
  github_policy: do_not_push
  parser_source: local_workspace_only
encoding:
  file_encoding: utf-8
  line_endings: lf_preferred
  parser_rule: normalize_crlf_to_lf_before_parsing
```

```yaml
variant_file_shape:
  format: markdown_with_yaml_frontmatter
  delimiter: "---"
  parse_order:
    - read file as utf-8
    - normalize line endings
    - require file to start with "---\n"
    - read YAML frontmatter until the next "\n---\n"
    - parse frontmatter into metadata
    - treat the remaining text as body_markdown
  body_rule:
    - do not parse body headings as stable API fields
    - upload body_markdown to the platform editor
    - frontmatter must not be pasted into the public body
```

```yaml
github_only_exclusions:
  security_topics:
    rule: never upload to Naver or Tistory
    excluded_slugs:
      - macro-malware
      - macro-malware-en
      - rtf-malware
      - rtf-malware-en
    automation_rule:
      - skip if slug is in this list
      - do not create platform draft
      - leave original GitHub post unchanged
```

```yaml
common_frontmatter_contract:
  required_fields:
    channel:
      naver: naver_blog
      tistory: tistory
    source: github_blog
    slug: string
    post_folder: content/posts/<stream>/<sequence>-<slug>
    variant_path: content/posts/<stream>/<sequence>-<slug>/variants/<channel>.md
    best_title: upload_title
    title_candidates: string_array
    focus_keyword: string
    secondary_keywords: string_array
    content_type: string
    status: ready_for_draft
    requires_manual_review: boolean
    content_group:
      enum:
        - ai
        - non_ai
      meaning: publish_slot_stream
    channel_category:
      enum:
        - AI
        - 프로그래밍 언어
        - DevOps
      meaning: visible_topic_group_for_naver_and_tistory
    channel_category_slug:
      enum:
        - ai
        - programming_language
        - devops
    publish_sequence: integer
    planned_publish_date: yyyy-mm-dd
    planned_publish_at: iso8601_datetime
    publish_slot:
      enum:
        - ai_daily
        - non_ai_daily
    schedule_base_date: yyyy-mm-dd
```

```yaml
naver_variant_contract:
  path: content/posts/<stream>/<sequence>-<slug>/variants/naver.md
  frontmatter_extra_fields:
    tone: friendly_explainer
    recommended_images: string_array
  title_source: frontmatter.best_title
  category_source: frontmatter.channel_category
  scheduled_time_source:
    preferred: publish-state.json.naver.planned_publish_at
    fallback: frontmatter.planned_publish_at
  body_source: markdown_body_after_frontmatter
  image_handling:
    recommended_image_list: frontmatter.recommended_images
    actual_image_paths: upload_queue_item.image_assets
    body_slot_pattern: "^\\[사진\\s+\\d+\\s+삽입:\\s*(.+)\\]$"
    automation_rule:
      - upload images manually or through a separate image pipeline
      - replace image slot markers only when an actual image asset exists
      - do not invent image files from marker text
  expected_body_style:
    - friendly_explainer
    - mobile_readable
    - includes_title_candidates_section
    - includes_short_opening
    - includes_summary_and_troubleshooting
```

```yaml
tistory_variant_contract:
  path: content/posts/<stream>/<sequence>-<slug>/variants/tistory.md
  frontmatter_extra_fields:
    source_updated_at: iso8601_datetime
    variant_updated_at: iso8601_datetime
  title_source: frontmatter.best_title
  category_source: frontmatter.channel_category
  scheduled_time_source:
    preferred: publish-state.json.tistory.planned_publish_at
    fallback: frontmatter.planned_publish_at
  body_source: markdown_body_after_frontmatter
  image_handling:
    actual_image_paths: upload_queue_item.image_assets
    body_image_pattern: "!\\[[^\\]]*\\]\\([^\\)]+\\)"
    automation_rule:
      - keep Markdown image references only when upload pipeline can resolve them
      - otherwise create text draft and leave image handling to manual review
  expected_body_style:
    - search_structured
    - tutorial_or_reference
    - includes_intro
    - includes_environment
    - includes_troubleshooting
    - includes_faq_when_possible
```

```yaml
publish_state_contract:
  path: content/posts/<stream>/<sequence>-<slug>/publish-state.json
  use_for:
    - channel status
    - variant path
    - planned publish time
    - hashes for duplicate/update detection
  channel_keys:
    - naver
    - tistory
  status_gate:
    upload_candidate_statuses:
      - ready_for_draft
      - needs_manual_review
      - draft_created
      - scheduled
    skip_statuses:
      - published
      - missing_variant
  hash_rule:
    - if variant_sha256 changed after a draft was created, update or recreate platform draft
    - if source_sha256 changed, rerun variant sync before upload
```

```yaml
automation_queue_item_shape:
  slug: string
  post_folder: string
  channel:
    enum:
      - naver
      - tistory
  platform:
    enum:
      - naver_blog
      - tistory
  variant_path: string
  state_path: string
  body_format: markdown
  title: frontmatter.best_title
  status: channel_state.status
  requires_manual_review: boolean
  content_group: ai|non_ai
  channel_category: AI|프로그래밍 언어|DevOps
  channel_category_slug: ai|programming_language|devops
  publish_sequence: integer
  planned_publish_date: yyyy-mm-dd
  planned_publish_at: iso8601_datetime
  publish_slot: ai_daily|non_ai_daily
  focus_keyword: string
  secondary_keywords: string_array
  body_source:
    path: variant_path
    frontmatter_delimiter: "---"
    body_starts_after_frontmatter: true
  image_assets:
    type: array
    item_shape:
      upload_order: integer
      source:
        enum:
          - variant
          - source
      alt: string
      reference: original_markdown_image_reference
      path: repository_relative_or_remote_url
      exists: boolean
      remote: boolean
  image_asset_count: integer
  missing_image_asset_count: integer
```

```yaml
reference_export_command:
  all_channels_compact_queue: python scripts/export_channel_upload_queue.py --body-mode path
  direct_payload_for_one_day: python scripts/export_channel_upload_queue.py --date 2026-04-26 --body-mode inline
  naver_only: python scripts/export_channel_upload_queue.py --channel naver --body-mode path
  tistory_only: python scripts/export_channel_upload_queue.py --channel tistory --body-mode path
```

```yaml
parser_pseudocode:
  - for each content/posts/<stream>/<sequence>-<slug>:
      - read publish-state.json
      - for each channel in [naver, tistory]:
          - locate variants/<channel>.md
          - split frontmatter and body_markdown
          - validate channel-specific required fields
          - title = frontmatter.best_title
          - category = frontmatter.channel_category
          - scheduled_at = publish-state[channel].planned_publish_at or frontmatter.planned_publish_at
          - upload_body = body_markdown
          - never paste frontmatter into platform body
```
