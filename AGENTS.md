# AGENTS.md

## Repository Purpose

This repository is the operating source for `www.k4nul.com`. It combines original blog content with a copied Minimal Mistakes Jekyll theme. Prefer editing blog operation files, pages, content structure, and documentation over upstream/theme files unless the task explicitly requires theme changes.

K4NUL should grow from a posting blog into a Korean practical knowledge base for `AI coding agent operations, validation, and security`.

Primary growth topics:

- AI coding agent operations
- Codex
- Claude Code
- `AGENTS.md`
- `CLAUDE.md`
- hooks
- MCP
- permissions/settings
- token/context management
- AI agent validation
- AI agent security

Rust, DevOps, and Security posts should be preserved and, where truthful, connected back to agent operations, validation, security, automation, permission boundaries, reproducible testing, or supply-chain/security practice.

The repository already has a long scheduled-post queue. Default growth work should operate that queue, not create more posts.

## Growth Goals

Use `docs/growth/` as the operating source for growth work.

- 30 days: stabilize indexing for `/ai-engineering/`, `/start-here/`, `/ai-engineering/templates/`; start increasing non-brand Search Console queries; add hub/template/related internal links to at least 10 important posts; prioritize rewrites and internal links over new post volume.
- 90 days: make Organic Search comparable to or larger than Direct; secure 10+ pages with average position inside 30; build long-tail query coverage for `AGENTS.md`, `CLAUDE.md`, Codex, and Claude Code; operate 5+ template pages; target a conservative 2-3x increase over the current user baseline.
- 180 days: conservative target of 500-1,000 monthly users, aggressive target of 2,000-5,000 monthly users; make K4NUL recognizable in Korean long-tail searches for AI coding agent operations, validation, and security; keep existing English pages, and prioritize KR/EN improvement for core templates, references, and how-to pages.

Do not estimate Search Console or GA4 numbers if they are not present in the repo or explicitly supplied by the user. Record missing values as `사용자 입력 필요`.

## Repo Layout

- `_posts/`: original GitHub blog posts. Read `_posts/AGENTS.md`, `docs/blog-style.md`, and `templates/post-template.md` before writing or revising posts.
- `_pages/`: top-level pages, section archives, search, about, contact, privacy, AI Engineering hubs, and templates.
- `_data/`: navigation, section/topic metadata, SEO descriptions, featured/start track data.
- `_includes/`, `_layouts/`: Minimal Mistakes includes and local layout overrides.
- `assets/`, `images/`: site images, CSS, JS assets.
- `docs/`, `templates/`, `project-docs/`, `skills/`: internal documentation and writing aids. These are excluded from the generated site.
- `docs/growth/`: growth goals, roadmap, daily routine, weekly plan, scheduled-post inventory/calendar, pre/post-publish checklists, content backlog, Search Console rules, prompt bank, and change-log template.
- `content/posts/`: local derivative posts for external channels. Use only `doc/channel-posting/` rules there.

## Build / Test Commands

- Check current branch before edits, commits, or pushes: `git branch --show-current`
- Build site: `bundle exec jekyll build`
- Serve locally: `bundle exec jekyll serve`
- Link check after link structure changes: `npm run check:links:local`
- SEO audit when metadata/canonical/social output changes: `npm run seo:audit`
- Minify theme JS only when JS changes: `npm run build:js`

## Git Rules

- The working branch for this repository is always `master`.
- Do not create `codex/` or other work branches unless the user explicitly asks in the same conversation.
- Before file edits, commits, or pushes, verify the branch is `master`.
- If the branch is not `master`, stop immediately and report only the current branch name.
- Do not create pull requests unless the user explicitly asks.
- Push only when explicitly requested, and only to `origin master`.
- Do not revert user changes. If the working tree already has unrelated changes, leave them alone.

## Daily Codex Routine

Every daily operation starts with:

1. Run `git branch --show-current`; continue only on `master`.
2. Run `git status --short`; identify existing user changes and avoid touching unrelated files.
3. Read the relevant local rules:
   - General growth work: `docs/growth/daily-codex-routine.md`
   - Post writing/revision: `_posts/AGENTS.md`, `docs/blog-style.md`, `templates/post-template.md`
   - Search-driven rewrites: `docs/growth/search-console-decision-rules.md`
4. Decide whether the task is an immediate common task or should be separated into a weekly prompt from `docs/growth/prompt-bank.md`.
5. Keep the change small: one post, one hub, one template, or a narrow documentation update.

Daily work priorities:

- Monday: inspect this week's scheduled long-tail posts for `AGENTS.md`, `CLAUDE.md`, Codex, Claude Code, hooks, MCP, or token/context quality.
- Tuesday: rewrite 1-2 existing posts for title, description, first paragraph, TL;DR, and internal links.
- Wednesday: improve templates/checklists that scheduled posts should link to.
- Thursday: improve internal links between hubs, posts, templates, and related posts.
- Friday: improve already scheduled experiment/postmortem posts, or record candidates when no scheduled item fits.
- Saturday: strengthen `/ai-engineering/`, `/start-here/`, and `/ai-engineering/templates/`.
- Sunday: analyze user-provided Search Console/GA4 data. If no data is provided, only prepare next-week candidates.

## Scheduled Post Queue Policy

- Default to using existing scheduled future posts instead of creating new posts.
- Do not change future post publish dates, filename slugs, or permalinks unless the user explicitly asks.
- If a schedule change looks useful, record it only in `docs/growth/schedule-adjustment-candidates.md`.
- Track the queue in `docs/growth/scheduled-posts-inventory.md` and `docs/growth/scheduled-posts-calendar.md`.
- Use `docs/growth/pre-publish-checklist.md` before publication and `docs/growth/post-publish-checklist.md` after publication.
- New posts are allowed only when a core template is missing from the scheduled queue, Search Console shows a clear need for a new reference page and no existing landing page can be improved, or the user explicitly asks for a new post.
- For KR/EN pairs, review both sides together for title, description, TL;DR, internal links, canonical, and hreflang.

## Public Future-Link Policy

- Do not link from public pages to future-dated posts by default.
- This repo uses Jekyll and does not configure `future: true`; current builds exclude future-dated posts.
- Public hubs, Start Here, and home should link only to already published posts or posts that are publicly available on the current build date.
- If a future-dated post is actually included in the build output, an exception can be reviewed, but do not assume that behavior.
- Add hub and related-post links on the publish day or after the URL is confirmed public.
- Future-post-to-future-post links must be checked against publication order so they do not create 404s at release time.

## Content Modification Principles

- Do not rewrite existing post bodies in bulk for site-structure tasks.
- Preserve existing URLs, slugs, permalinks, front matter identity fields, and Korean/English `translation_key` pairs unless the user explicitly asks for a URL change.
- Do not invent facts, metrics, traffic data, Search Console data, GA4 data, career history, affiliations, experiments, or representative work.
- Keep facts, direct reproduction, interpretation, limitations, and references separate.
- Date-sensitive claims need `검증 기준일`; version-sensitive claims need test environment and versions.
- Prefer primary sources: official docs, standards, original repositories, or directly reproduced results.
- Keep existing permalinks unless the user explicitly requests a URL change. If a URL must change, add a redirect or clear navigation path.
- New content should support the AI coding agent operations/validation/security axis unless the user asks for another topic.
- Do not mass-produce new posts. Prefer existing content structure, internal links, rewrites, and templates.
- Do not add new posts when a scheduled post can be improved instead.
- Do not split many similar short posts. Connect them under a hub.

## SEO And Internal Linking Principles

- Canonical domain is `https://www.k4nul.com`.
- Major pages and posts should have `title`, `description`, `lang`, and `translation_key`.
- Korean/English pairs share the same `translation_key`; English pages use explicit `permalink` when needed.
- Optional post fields supported for portfolio surfacing: `featured`, `track`, `repo`, `demo`, `references`.
- Do not put unverifiable profile details into JSON-LD or About content.
- Title search intent comes before series numbering or internal labels.
- Use descriptive anchor text. Avoid weak anchors like `여기`, `이 글`, or `this post`.
- Prefer links among:
  - hub -> individual post
  - individual post -> hub
  - individual post -> template/checklist
  - related posts, 3-5 where useful
- When adding or changing link structure, run `npm run check:links:local` if Node dependencies are available.

## KR/EN Operating Policy

K4NUL already publishes Korean and English pages in parallel. Do not treat English as a future-only experiment, and do not delete or discard existing English pages.

- Existing Korean and English pages stay in place.
- Each language page should canonicalize to itself, not to the other language.
- Equivalent Korean/English pairs should use matching `translation_key` values and valid `hreflang` alternates.
- Do not connect non-equivalent pages with `hreflang`.
- If an English page is outdated or low quality, mark it as a rewrite candidate instead of deleting it.
- Fix broken links, wrong canonical URLs, and missing `hreflang` before creating broad new language work.
- New posts about AI coding agent operations, Codex, Claude Code, `AGENTS.md`, `CLAUDE.md`, hooks, MCP, permissions/settings, token/context management, AI agent security, and AI agent verification default to KR/EN parallel publication.
- Template, checklist, reference, and how-to content also defaults to KR/EN parallel publication.
- General Rust/DevOps/Security posts are Korean-first unless they directly support AI agent operations, validation, security, automation, or permission boundaries.
- Short notes or posts that depend strongly on Korean reader context do not need forced English versions.
- English investment priority: templates/checklists, `AGENTS.md`/`CLAUDE.md`, Codex/Claude Code operations, hooks/MCP/permissions security, AI agent verification/postmortems, then general Rust/DevOps.

## Search Console / GA4 Rules

- Search Console is the primary source for growth decisions because it shows query, page, impressions, clicks, CTR, and average position.
- GA4 is useful for organic landing pages and engaged sessions, but do not use event totals alone as the main growth signal.
- If data is missing, write `사용자 입력 필요` rather than estimating.
- Decision rules live in `docs/growth/search-console-decision-rules.md`.
- Do not execute these without data and a scoped prompt:
  - large-scale existing post changes
  - broad non-core English expansion
  - expanding 3+ hubs
  - cannibalization cleanup
  - mass title changes
  - large structure changes

## Post / Hub Revision Checklist

When revising a post or hub page, check:

- `title`: search intent appears before series numbering or internal labels.
- `description`: present, concrete, and non-empty.
- TL;DR or summary: the first section gives the conclusion before deep detail.
- Internal links: descriptive anchors, not `여기` or `이 글`.
- Hub link: connect to `/ai-engineering/`, `/start-here/`, or the relevant section hub when useful.
- Template link: connect to `/ai-engineering/templates/` or a relevant checklist when useful.
- Related posts: connect to 3-5 existing posts or a relevant hub when possible; do not link to unpublished or nonexistent URLs.
- Canonical/hreflang: preserve `permalink`, `lang`, and `translation_key` behavior for Korean/English pairs.
- Verification: keep claims tied to sources, versions, direct reproduction, or explicit limitations.
- Build: `bundle exec jekyll build` succeeds, or the exact failure is reported.

## Do Not

- Do not expose empty `Life` or similar inactive sections in the primary navigation.
- Do not mix GitHub original post rules with Naver/Tistory derivative post rules.
- Do not add broad privacy-policy language for services that are not actually configured.
- Do not make large theme or build-system changes for content/navigation tasks.
- Do not hide build failures. Minimize the change, identify the failing file or plugin, and report the exact error.
- Do not delete existing English pages, mark them as deprecated, or canonicalize them to Korean pages.
- Do not mechanically English-publish every short note if it delays core hub, template, or checklist work.

## Verification Checklist

- Current branch is `master`.
- `bundle exec jekyll build` completes, or the exact failure is reported.
- When link structure changes, run `npm run check:links:local` if Node dependencies are available.
- Sample generated pages have canonical URLs under `https://www.k4nul.com`.
- `og:title`, `og:description`, `og:url`, Twitter Card metadata, and non-empty descriptions are present.
- `lang` and `hreflang` output are not broken for Korean/English pairs.
- `robots.txt` links to `https://www.k4nul.com/sitemap.xml`.
- Feed discovery remains available through `/feed.xml`.
- Primary navigation matches `Security / AI Engineering / Rust / DevOps / Start Here / About`.

## Completion Report Format

Final reports for growth/content work should include:

1. Generated or modified files.
2. Purpose of each file.
3. Immediate common tasks completed.
4. Tasks separated into weekly prompts.
5. Verification commands and results.
6. Remaining risks.
7. Location of the daily prompt for tomorrow.
8. Next five execution priorities.

For content growth work, also document what changed, what was intentionally left alone, and the next human editorial priorities.
