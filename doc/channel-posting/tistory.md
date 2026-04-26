# tistory_posting_rules

```yaml
schema_version: 1
verification_date: "2026-04-25"
channel: tistory
variant_path: content/posts/<stream>/<sequence>-<slug>/variants/tistory.md
goal:
  - search_intent_optimized_technical_post
  - practical_problem_solving
  - structured_long_tail_reference
  - preserve_source_verification
  - avoid_github_original_copy_paste
reader_intent:
  primary:
    - search_problem_solution
    - compare_terms
    - follow_steps
    - debug_common_error
  secondary:
    - bookmark_reference
    - continue_to_related_article
tone:
  preferred:
    - practical
    - explanatory
    - less_rigid_than_official_docs
    - more_structured_than_naver
  avoid:
    - pure_official_document_style
    - thin_summary
    - clickbait
    - unverified_claims
```

```yaml
title_rules:
  min_candidates: 3
  best_title_rule:
    - put_search_keyword_and_solution_intent_near_front
    - remove_series_number_prefix
    - avoid_copying_source_title
    - avoid_exaggeration
  good_patterns:
    - "Windows에서 Rust 설치하고 Hello World 실행하기"
    - "VS Code에서 Rust 시작하기: rustup 설치부터 cargo run까지"
    - "Rust 설치 방법 정리: rustup, rustc, cargo 차이까지"
    - "Rust 입문 환경 세팅: Windows + VS Code + Hello World"
```

```yaml
frontmatter_schema:
  channel: tistory
  source: github_blog
  slug: string
  best_title: string
  title_candidates:
    min_items: 3
  focus_keyword: string
  secondary_keywords:
    min_items: 3
  channel_category:
    enum:
      - AI
      - 프로그래밍 언어
      - DevOps
  channel_category_slug:
    enum:
      - ai
      - programming_language
      - devops
  content_type: tutorial
  status: ready_for_draft
  source_updated_at: iso8601_datetime
  variant_updated_at: iso8601_datetime
  requires_manual_review: true
  post_folder: content/posts/<stream>/<sequence>-<slug>
  variant_path: content/posts/<stream>/<sequence>-<slug>/variants/tistory.md
```

```yaml
body_structure:
  preferred_order:
    - title
    - short_search_intro
    - covered_topics
    - execution_environment
    - core_summary
    - term_comparison_table
    - step_flow
    - troubleshooting
    - faq
    - references
    - tag_candidates
    - original_link_only
  required_when_possible:
    - troubleshooting
    - faq
    - official_links_or_reference_section
    - verification_date_or_test_version
  troubleshooting_format:
    sections:
      - symptom
      - first_check
      - resolution_direction
  faq_count: 3-6
  original_link_only:
    position: final_section
    rule:
      - include_only_the_original_link_or_repository_path
      - do_not_write_please_refer_to_the_original_post
      - do_not_include_next_post_or_related_post_placeholders
```

```yaml
tistory_keyword_rules:
  placement:
    - best_title
    - first_intro_paragraph
    - one_or_more_headings_when_natural
    - troubleshooting
    - tag_candidates
  avoid:
    - keyword_list_disguised_as_paragraph
    - repeating_focus_keyword_without_context
    - adding_unrelated_keywords
  examples_for_rust_install:
    focus_keyword: "Windows Rust 설치"
    secondary_keywords:
      - "VS Code Rust 실행"
      - "Rust Hello World"
      - "rustup 설치"
      - "rustc 버전 확인"
      - "cargo run"
      - "rustc와 cargo 차이"
```

```yaml
technical_density_rules:
  naver_comparison: higher_than_naver
  github_source_comparison: softer_than_github_original
  command_blocks:
    keep: true
    rule:
      - explain_context_before_command
      - keep_command_and_expected_output_near_each_other
      - avoid_unnecessary_full_log
  tables:
    prefer_for:
      - tool_comparison
      - concept_comparison
      - command_role_comparison
```

```yaml
quality_checklist:
  - title_has_search_intent
  - introduction_shows_problem_and_environment
  - source_paragraphs_are_not_excessively_copied
  - important_tool_differences_are_clear
  - command_flow_is_not_broken
  - troubleshooting_section_exists
  - faq_section_exists
  - official_document_links_are_preserved
  - closing_cta_exists
  - markdown_is_tistory_editor_friendly
```
