# naver_posting_rules

```yaml
schema_version: 1
verification_date: "2026-04-25"
channel: naver_blog
variant_path: content/posts/<stream>/<sequence>-<slug>/variants/naver.md
goal:
  - make_technical_post_readable_on_mobile
  - help_reader_understand_problem_fast
  - support_manual_upload_with_image_slots
  - keep_facts_and_verification_from_source
  - avoid_github_original_copy_paste
reader_intent:
  primary:
    - beginner_search
    - quick_problem_understanding
    - screenshot_guided_execution
  secondary:
    - save_for_later
    - compare_terms
    - decide_next_learning_step
tone:
  preferred:
    - friendly
    - practical
    - concise
    - first_person_when_it_clarifies_direct_experience
  avoid:
    - official_document_style_only
    - overly_dense_code_walkthrough
    - exaggerated_clickbait
    - keyword_stuffing
```

```yaml
title_rules:
  min_candidates: 3
  best_title_rule:
    - put_problem_or_environment_first
    - remove_series_number_prefix
    - keep_title_natural_for_blog_search
    - avoid_overpromising
  good_patterns:
    - "<환경>에서 <기술> 시작하기"
    - "<도구> 설치부터 실행까지 한 번에 정리"
    - "<개념 A>와 <개념 B> 차이 쉽게 정리"
    - "<문제 상황>일 때 먼저 확인할 것"
  bad_patterns:
    - "Rust 01. 설치와 Hello World 실행하기"
    - "무조건 해결되는 최고의 방법"
    - "공식 문서 전체 요약"
```

```yaml
frontmatter_schema:
  channel: naver_blog
  source: github_blog
  slug: string
  best_title: string
  title_candidates:
    min_items: 5
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
  content_type: beginner_guide
  tone: friendly_explainer
  status: ready_for_draft
  requires_manual_review: true
  recommended_images:
    min_items: 2
  post_folder: content/posts/<stream>/<sequence>-<slug>
  variant_path: content/posts/<stream>/<sequence>-<slug>/variants/naver.md
```

```yaml
body_structure:
  required_order:
    - yaml_frontmatter
    - title_candidates_and_best_title
    - body_title
    - short_opening
    - what_this_post_covers
    - quick_answer
    - baseline_environment
    - simple_core_concepts
    - step_by_step_body
    - common_confusions
    - troubleshooting
    - daily_summary
    - references
    - tag_candidates
    - original_link_only
  section_rules:
    short_opening:
      paragraphs: 2-4
      must_include:
        - problem_this_post_solves
        - target_environment
        - what_reader_can_do_after_reading
    quick_answer:
      bullets: 3-5
      rule: answer_first_then_detail
    step_by_step_body:
      paragraph_length: short
      code_density: medium
      rule:
        - explain_why_before_command
        - place_image_slot_after_visual_step
    image_slots:
      format: "[사진 N 삽입: 설명]"
      rule:
        - include_when_source_has_image
        - suggest_needed_screenshot_when_source_has_no_image
    common_confusions:
      count: 2-5
      format:
        - confusion
        - how_to_read_it
    short_faq:
      count: 3-5
    original_link_only:
      position: final_section
      rule:
        - include_only_the_original_link_or_repository_path
        - do_not_write_please_refer_to_the_original_post
        - do_not_include_next_post_or_related_post_placeholders
```

```yaml
naver_keyword_rules:
  placement:
    - title
    - first_two_paragraphs
    - one_mid_body_heading_or_sentence
    - tag_candidates
  avoid:
    - same_keyword_every_paragraph
    - unrelated_trend_keywords
    - unnatural_repetition
  examples_for_rust_install:
    focus_keyword: "Windows Rust 설치"
    secondary_keywords:
      - "VS Code Rust 실행"
      - "Rust Hello World"
      - "rustup 설치"
      - "cargo run"
```

```yaml
naver_image_rules:
  priority: high
  reason:
    - mobile_scan
    - step_confirmation
    - manual_upload_readiness
  image_list_file:
    optional_path: content/posts/<stream>/<sequence>-<slug>/assets/naver-images.md
  body_marker:
    format: "[사진 N 삽입: <what_this_image_confirms>]"
  recommended_images:
    - first_result_or_final_state
    - installation_screen
    - command_output
    - editor_screen
    - error_or_troubleshooting_screen
```

```yaml
quality_checklist:
  - title_removes_github_series_prefix
  - opening_feels_like_blog_not_manual
  - answer_or_benefit_visible_before_first_scroll
  - code_blocks_are_not_excessively_long
  - image_slots_exist_for_visual_steps
  - source_verification_date_is_preserved
  - official_links_are_preserved_when_used
  - uncertainty_is_marked_instead_of_asserted
  - final_section_suggests_next_action_naturally
```
