# AGENTS.md

## Repository Purpose

This repository is the operating source for `www.k4nul.com`. It combines original blog content with a copied Minimal Mistakes Jekyll theme. Prefer editing blog operation files and content structure over upstream/theme files unless the task explicitly requires theme changes.

## Repo Layout

- `_posts/`: original GitHub blog posts. Read `_posts/AGENTS.md`, `docs/blog-style.md`, and `templates/post-template.md` before writing or revising posts.
- `_pages/`: top-level pages, section archives, search, about, contact, privacy.
- `_data/`: navigation, section/topic metadata, SEO descriptions, featured/start track data.
- `_includes/`, `_layouts/`: Minimal Mistakes includes and local layout overrides.
- `assets/`, `images/`: site images, CSS, JS assets.
- `docs/`, `templates/`, `project-docs/`, `skills/`: internal documentation and writing aids. These are excluded from the generated site.
- `content/posts/`: local derivative posts for external channels. Use only `doc/channel-posting/` rules there.

## Build / Test Commands

- Build site: `bundle exec jekyll build`
- Serve locally: `bundle exec jekyll serve`
- Minify theme JS only when JS changes: `npm run build:js`
- Check current branch before edits, commits, or pushes: `git branch --show-current`

## Git Rules

- The working branch for this repository is always `master`.
- Do not create `codex/` or other work branches unless the user explicitly asks in the same conversation.
- Before file edits, commits, or pushes, verify the branch is `master`.
- If the branch is not `master`, stop immediately and report only the current branch name.
- Do not create pull requests unless the user explicitly asks.
- Push only when explicitly requested, and only to `origin master`.

## Writing Conventions

- Do not rewrite existing post bodies in bulk for site-structure tasks.
- Keep facts, direct reproduction, interpretation, limitations, and references separate.
- Date-sensitive claims need `검증 기준일`; version-sensitive claims need test environment and versions.
- Prefer primary sources: official docs, standards, original repositories, or directly reproduced results.
- Do not invent unverified career history, affiliation, education, certifications, representative work, experiments, or sample attribution.
- Keep existing permalinks unless the user explicitly requests a URL change. If a URL must change, add a redirect or clear navigation path.

## SEO Conventions

- Canonical domain is `https://www.k4nul.com`.
- Major pages and posts should have `title`, `description`, `lang`, and `translation_key`.
- Korean/English pairs share the same `translation_key`; English mirrors use explicit `permalink` when needed.
- Optional post fields supported for portfolio surfacing: `featured`, `track`, `repo`, `demo`, `references`.
- Do not put unverifiable profile details into JSON-LD or About content.

## Do Not

- Do not expose empty `Life` or similar inactive sections in the primary navigation.
- Do not mix GitHub original post rules with Naver/Tistory derivative post rules.
- Do not add broad privacy-policy language for services that are not actually configured.
- Do not make large theme or build-system changes for content/navigation tasks.
- Do not hide build failures. Minimize the change, identify the failing file or plugin, and report the exact error.

## Verification Checklist

- Current branch is `master`.
- `bundle exec jekyll build` completes, or the exact failure is reported.
- Sample generated pages have canonical URLs under `https://www.k4nul.com`.
- `og:title`, `og:description`, `og:url`, Twitter Card metadata, and non-empty descriptions are present.
- `lang` and `hreflang` output are not broken for Korean/English pairs.
- `robots.txt` links to `https://www.k4nul.com/sitemap.xml`.
- Feed discovery remains available through `/feed.xml`.
- Primary navigation matches `Security / AI Engineering / Rust / DevOps / Start Here / About`.
