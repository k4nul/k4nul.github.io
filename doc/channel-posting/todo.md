# external_channel_todo_schema

```yaml
schema_version: 1
verification_date: "2026-04-25"
todo:
  - id: implement_naver_variant_sync
    channel: naver
    status: open
    description: Implement scripts/sync_naver_variants.py or extend channel sync to generate variants/naver.md.
  - id: naver_image_upload_checklist
    channel: naver
    status: open
    description: Generate per-post image slot checklist for manual Naver upload.
  - id: tistory_related_link_map
    channel: tistory
    status: open
    description: Replace CTA placeholders with actual related post links.
  - id: publish_state_unification
    channel: all
    status: open
    description: Move publish-state.json toward a uniform channel map with naver and tistory keys.
  - id: quality_sampling_by_topic
    channel: all
    status: open
    description: Sample generated variants by topic family and tune channel prompts where posts remain too close to source.
```
