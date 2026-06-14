# external_channel_schedule_schema

```yaml
schema_version: 1
verification_date: "2026-04-25"
scope: external_channel_publish_plan
not_scope:
  - GitHub Pages canonical post date
  - _posts front matter date
  - security_topic_posts
base_date: "2026-04-26"
timezone: Asia/Seoul
daily_slots:
  ai:
    slot_name: ai_daily
    time: "09:00:00+09:00"
    cadence: every_day
    order: source_date_ascending
  non_ai:
    slot_name: non_ai_daily
    time: "18:00:00+09:00"
    cadence: every_day
    order: source_date_ascending
rule:
  - assign one AI post per day from the first AI post
  - assign one non-AI post per day from the first non-AI post
  - both streams start on the base_date
  - if one stream ends earlier, the remaining stream continues one post per day
exclusion_rule:
  security_topics:
    reason: github_only
    excluded_from:
      - naver
      - tistory
      - external_channel_schedule
      - upload_queue
    slugs:
      - macro-malware
      - macro-malware-en
      - rtf-malware
      - rtf-malware-en
folder_rule:
  ai: content/posts/ai/<sequence>-<slug>
  non_ai: content/posts/non-ai/<sequence>-<slug>
  sequence_format: zero_padded_3_digits
  examples:
    - content/posts/ai/001-why-ai-tools-produce-different-results
    - content/posts/non-ai/001-macro-malware
```

```yaml
classification_rules:
  ai:
    include_when_title_or_slug_contains:
      - codex
      - claude
      - ai
      - agent
      - harness
      - token
      - context-budget
      - mcp
      - guardrail
      - instruction
      - prompt
      - subagent
      - trace
      - handoff
      - schema
      - enforcement
      - compression
      - memory
  non_ai:
    prefix_priority:
      - docker-
      - git-
      - jenkins-
      - jenkinsfile-
      - kubernetes-
      - rust-
      - macro-malware
      - rtf-malware
    rule: non_ai_prefix_priority_over_ai_terms
```

```yaml
channel_category_rules:
  allowed_values:
    - AI
    - 프로그래밍 언어
    - DevOps
  purpose: naver_and_tistory_visible_topic_group
  not_same_as:
    - content_group
    - publish_slot
  mapping:
    AI:
      rule:
        - content_group_is_ai
    프로그래밍 언어:
      prefix_priority:
        - rust-
    DevOps:
      prefix_priority:
        - docker-
        - git-
        - jenkins-
        - jenkinsfile-
        - kubernetes-
        - macro-malware
        - rtf-malware
      fallback_for_non_ai: true
```

```yaml
written_fields:
  schedule_manifest:
    path: content/channel-publish-schedule.json
    fields:
      - base_date
      - timezone
      - slots
      - counts
      - channel_categories
      - posts
  metadata_yaml:
    - post_folder
    - source_path
    - content_group
    - channel_category
    - channel_category_slug
    - external_publish_sequence
    - planned_publish_date
    - planned_publish_at
    - publish_slot
    - schedule_base_date
  variant_frontmatter:
    - post_folder
    - variant_path
    - content_group
    - channel_category
    - channel_category_slug
    - publish_sequence
    - planned_publish_date
    - planned_publish_at
    - publish_slot
    - schedule_base_date
  publish_state_json:
    external_publish_plan:
      - post_folder
      - source_path
      - content_group
      - channel_category
      - channel_category_slug
      - sequence
      - planned_publish_date
      - planned_publish_at
      - publish_slot
      - base_date
      - cadence_days
      - timezone
```
