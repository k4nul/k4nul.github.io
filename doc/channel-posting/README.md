# external_channel_posting_index

```yaml
schema_version: 1
verification_date: "2026-04-25"
purpose: manage derivative posts for external publishing channels
managed_channels:
  - naver
  - tistory
separation_from_github_blog:
  github_blog_role:
    - canonical factual source
    - verification baseline
    - original article archive
  external_channel_role:
    - platform-specific rewrite
    - manual upload draft
    - search and reader-flow optimization
    - channel publish state tracking
  not_shared:
    - title_strategy
    - opening_lead_strategy
    - section_order
    - platform_tags
    - manual_upload_status
  github_only_topics:
    security:
      rule: do_not_generate_naver_or_tistory_variants
      slugs:
        - macro-malware
        - macro-malware-en
        - rtf-malware
        - rtf-malware-en
```

```yaml
directory_contract:
  managed_root: content/posts
  post_unit: content/posts/<stream>/<sequence>-<slug>
  streams:
    ai:
      path: content/posts/ai
      sequence_rule: 001부터 AI 발행 순서대로 증가
    non_ai:
      path: content/posts/non-ai
      sequence_rule: 001부터 AI가 아닌 글 발행 순서대로 증가
  examples:
    - content/posts/ai/001-why-ai-tools-produce-different-results
    - content/posts/non-ai/001-macro-malware
  required_source:
    path: source.md
    meaning: canonical content input for external channel variants
  optional_variants:
    naver: variants/naver.md
    tistory: variants/tistory.md
  variant_git_policy:
    scope:
      - variants/naver.md
      - variants/tistory.md
    rule: local_only_do_not_commit
    gitignore_pattern: content/posts/**/variants/
    reason:
      - platform_drafts_are_generated_local_artifacts
      - manual_upload_does_not_require_github_copy
  shared_metadata:
    path: metadata.yaml
  shared_state:
    path: publish-state.json
```

```yaml
policy_documents:
  channels: doc/channel-posting/channels.md
  naver: doc/channel-posting/naver.md
  tistory: doc/channel-posting/tistory.md
  state: doc/channel-posting/state.md
  workflows: doc/channel-posting/workflows.md
  prompts: doc/channel-posting/prompts.md
  schedule: doc/channel-posting/schedule.md
  automation_parser: doc/channel-posting/automation-parser.md
  todo: doc/channel-posting/todo.md
```
