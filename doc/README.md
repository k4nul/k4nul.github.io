# doc_index

```yaml
schema_version: 1
verification_date: "2026-04-25"
purpose: repository-internal operational rules
rule_separation:
  github_blog_originals:
    paths:
      - _posts/AGENTS.md
      - docs/blog-style.md
      - templates/post-template.md
    scope:
      - GitHub Pages canonical posts
      - Minimal Mistakes rendering
      - source article verification structure
  external_channel_variants:
    path: doc/channel-posting/
    scope:
      - Naver Blog derivative posts
      - Tistory derivative posts
      - manual upload packages
      - channel-specific titles, leads, body structure, and status
    rule:
      - do_not_store_external_channel_rules_in_AGENTS_md
      - do_not_mix_channel_strategy_with_github_blog_style
      - keep_channel_rules_schema_first
```

```yaml
document_map:
  external_channel_index: doc/channel-posting/README.md
  channel_schema: doc/channel-posting/channels.md
  naver_rules: doc/channel-posting/naver.md
  tistory_rules: doc/channel-posting/tistory.md
  state_schema: doc/channel-posting/state.md
  workflows: doc/channel-posting/workflows.md
  prompt_policy: doc/channel-posting/prompts.md
  schedule_policy: doc/channel-posting/schedule.md
  todo: doc/channel-posting/todo.md
```
