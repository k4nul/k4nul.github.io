# external_channel_prompt_schema

```yaml
schema_version: 1
verification_date: "2026-04-25"
prompt_scope: external_channel_rewrite_only
not_scope:
  - GitHub canonical post authoring
  - _posts style guide
  - upstream theme documentation
shared_constraints:
  - do_not_copy_github_source_as_is
  - preserve_verified_facts
  - preserve_verification_date_when_present
  - preserve_test_version_when_present
  - preserve_official_links_when_used
  - mark_uncertainty_instead_of_asserting
  - avoid_clickbait
  - avoid_keyword_stuffing
```

```yaml
naver_prompt:
  policy_version: "2026-04-25.naver-final-post.v2"
  role: naver_technical_blog_rewriter
  input:
    - content/posts/<stream>/<sequence>-<slug>/source.md
    - metadata.yaml
  output: content/posts/<stream>/<sequence>-<slug>/variants/naver.md
  optimize_for:
    - mobile_readability
    - fast_understanding
    - image_guided_steps
    - friendly_practical_explanation
  rewrite_rules:
    - create_at_least_five_title_candidates
    - choose_one_best_title
    - make_opening_short_and_problem_oriented
    - put_quick_answer_before_long_context
    - split_long_paragraphs
    - keep_code_blocks_shorter_than_tistory_when_possible
    - add_image_slots_for_visual_confirmation
    - add_common_confusions
    - add_short_faq
    - move_official_references_to_bottom
```

```yaml
tistory_prompt:
  policy_version: "2026-04-25.tistory-search-variant.v2"
  role: tistory_technical_blog_rewriter
  input:
    - content/posts/<stream>/<sequence>-<slug>/source.md
    - metadata.yaml
  output: content/posts/<stream>/<sequence>-<slug>/variants/tistory.md
  optimize_for:
    - search_intent
    - structured_problem_solving
    - term_comparison
    - troubleshooting_reference
  rewrite_rules:
    - create_at_least_three_title_candidates
    - choose_best_title_with_search_intent
    - write_3_to_5_paragraph_intro
    - include_execution_environment
    - include_comparison_table_when_possible
    - include_troubleshooting
    - include_faq
    - include_closing_cta
```
