# external_channel_state_schema

```yaml
schema_version: 1
verification_date: "2026-04-25"
file: content/posts/<stream>/<sequence>-<slug>/publish-state.json
scope: external_channel_publish_state
not_scope:
  - GitHub Pages build state
  - original post editorial review
source:
  path: content/posts/<stream>/<sequence>-<slug>/source.md
  source_sha256: string
  source_updated_at: iso8601_datetime
  status:
    enum:
      - draft
      - ready
      - scheduled
      - published
  scheduled_at: iso8601_datetime|null
policy_version: string
variant_storage_policy:
  paths:
    - content/posts/<stream>/<sequence>-<slug>/variants/naver.md
    - content/posts/<stream>/<sequence>-<slug>/variants/tistory.md
  storage: local_workspace
  git_tracking: ignored
  github_policy: do_not_push
  gitignore_pattern: content/posts/**/variants/
external_publish_plan:
  post_folder: content/posts/<stream>/<sequence>-<slug>
  source_path: content/posts/<stream>/<sequence>-<slug>/source.md
  content_group:
    enum:
      - ai
      - non_ai
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
  sequence: integer
  planned_publish_date: yyyy-mm-dd
  planned_publish_at: iso8601_datetime
  publish_slot:
    enum:
      - ai_daily
      - non_ai_daily
  base_date: yyyy-mm-dd
  cadence_days: 1
  timezone: Asia/Seoul
```

```yaml
channel_status_values:
  missing_variant:
    meaning: channel variant file does not exist yet
  variant_generated:
    meaning: variant was generated but has not passed draft readiness rules
  ready_for_draft:
    meaning: ready for manual draft creation after human review
  needs_refresh:
    meaning: source or policy changed and variant should be regenerated
  needs_manual_review:
    meaning: variant has changed while platform draft, scheduled post, or published post may already exist
  draft_created:
    meaning: platform draft exists
  scheduled:
    meaning: platform scheduled post exists
  published:
    meaning: platform post has been published
```

```yaml
channel_state_shape:
  naver:
    status: channel_status_value
    reason: string|null
    requires_manual_review: true
    variant_path: variants/naver.md
    source_sha256: string
    variant_sha256: string
    policy_version: string
    updated_at: iso8601_datetime
    content_group:
      enum:
        - ai
        - non_ai
    channel_category:
      enum:
        - AI
        - 프로그래밍 언어
        - DevOps
  tistory:
    status: channel_status_value
    reason: string|null
    requires_manual_review: true
    variant_path: variants/tistory.md
    source_sha256: string
    variant_sha256: string
    policy_version: string
    updated_at: iso8601_datetime
    content_group:
      enum:
        - ai
        - non_ai
    channel_category:
      enum:
        - AI
        - 프로그래밍 언어
        - DevOps
```

```yaml
state_transition_rules:
  create_missing_variant:
    when:
      - channel variant missing
    next: ready_for_draft
  source_or_policy_changed:
    when:
      - source hash changed
      - channel policy changed
    next: ready_for_draft
  scheduled_variant_updated:
    when:
      - source.status is scheduled
      - existing channel variant changed
      - platform post may already be scheduled
    next: needs_manual_review
    reason: scheduled_post_variant_updated
  manual_platform_update_done:
    when:
      - user confirms external platform update
    allowed_next:
      - draft_created
      - scheduled
      - published
```
