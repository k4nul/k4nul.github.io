# external_channel_workflow_schema

```yaml
schema_version: 1
verification_date: "2026-04-25"
workflows:
  sync_tistory_variants:
    command: python scripts/sync_tistory_variants.py
    dry_run: python scripts/sync_tistory_variants.py --dry-run
    status: implemented
    inputs:
      - _posts/*.md
      - content/posts/**/source.md
    writes:
      - content/posts/<stream>/<sequence>-<slug>/source.md
      - content/posts/<stream>/<sequence>-<slug>/metadata.yaml
      - content/posts/<stream>/<sequence>-<slug>/variants/tistory.md
      - content/posts/<stream>/<sequence>-<slug>/publish-state.json
  sync_naver_variants:
    command: python scripts/sync_naver_variants.py
    dry_run: python scripts/sync_naver_variants.py --dry-run
    status: implemented
    inputs:
      - content/posts/**/source.md
    writes:
      - content/posts/<stream>/<sequence>-<slug>/variants/naver.md
      - content/posts/<stream>/<sequence>-<slug>/publish-state.json
  schedule_channel_posts:
    command: python scripts/schedule_channel_posts.py
    dry_run: python scripts/schedule_channel_posts.py --dry-run
    status: implemented
    inputs:
      - content/posts/**/source.md
      - content/posts/**/metadata.yaml
      - content/posts/**/variants/naver.md
      - content/posts/**/variants/tistory.md
      - content/posts/**/publish-state.json
    writes:
      - content/posts/ai/<sequence>-<slug>
      - content/posts/non-ai/<sequence>-<slug>
      - content/posts/<stream>/<sequence>-<slug>/metadata.yaml
      - content/posts/<stream>/<sequence>-<slug>/variants/naver.md
      - content/posts/<stream>/<sequence>-<slug>/variants/tistory.md
      - content/posts/<stream>/<sequence>-<slug>/publish-state.json
    schedule_rule:
      - base_date: "2026-04-26"
      - ai_daily: one AI post per day
      - non_ai_daily: one non-AI post per day
      - channel_category: visible Naver/Tistory topic group
      - channel_category_values: [AI, 프로그래밍 언어, DevOps]
      - security_topics: excluded and GitHub-only
  export_channel_upload_queue:
    command: python scripts/export_channel_upload_queue.py --body-mode path
    direct_payload_example: python scripts/export_channel_upload_queue.py --date 2026-04-26 --body-mode inline
    status: implemented
    inputs:
      - content/posts/**/variants/naver.md
      - content/posts/**/variants/tistory.md
      - content/posts/**/publish-state.json
    writes: []
    output:
      format: json
      use:
        - upload_automation_queue
        - parser_validation
        - scheduled_day_payload
```

```yaml
selection_rules:
  exclusions:
    - macro-malware
    - macro-malware-en
    - rtf-malware
    - rtf-malware-en
  common:
    - variant file missing
    - source.md newer than variant
    - metadata.yaml scheduled_at exists
    - channel status in [draft, ready, scheduled, needs_refresh, needs_manual_review]
    - channel conversion policy changed
    - existing variant lacks required channel structure
  naver_required_structure:
    - best_title frontmatter
    - short_opening
    - quick_answer
    - image_slots_or_image_suggestions
    - common_confusions
    - short_faq
  tistory_required_structure:
    - best_title frontmatter
    - covered_topics
    - execution_environment
    - term_comparison_table
    - troubleshooting
    - faq
```

```yaml
manual_upload_flow:
  step_1: run channel sync dry-run
  step_2: run channel sync write
  step_3: open content/posts/<stream>/<sequence>-<slug>/variants/<channel>.md
  step_4: review best_title and body for channel fit
  step_5: paste into platform editor
  step_6: upload images manually according to body slots
  step_7: update publish-state.json channel status
```

```yaml
browser_draft_flow:
  status: optional
  rule:
    - use_only_when_user_explicitly_requests_platform_browser_draft
    - repository_variant_file_remains_source_of_manual_review
    - failed_browser_draft_must_not_block_variant_file_update
```

```yaml
repository_tracking_policy:
  generated_variant_bodies:
    paths:
      - content/posts/**/variants/naver.md
      - content/posts/**/variants/tistory.md
    git_tracking: ignored
    gitignore_pattern: content/posts/**/variants/
    github_policy: do_not_push
    automation_source: local_workspace_files
  manual_upload_rule:
    - automation reads local variants when creating platform drafts
    - GitHub remote is not treated as the source for Naver or Tistory bodies
```
