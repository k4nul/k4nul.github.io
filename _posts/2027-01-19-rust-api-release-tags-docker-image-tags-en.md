---
layout: single
title: "Rust Service 18. Connecting release tags and Docker image tags"
description: "Connects Git tags, releases, Docker image tags, and digests into a traceable deployment history."
date: 2027-01-19 09:00:00 +09:00
lang: en
translation_key: rust-api-release-tags-docker-image-tags
section: development
topic_key: rust
featured: false
track: rust
repo:
demo:
references:
categories: Rust
tags: [rust, axum, api, production, devops]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/rust/rust-api-release-tags-docker-image-tags/
---

## Summary

`latest` alone is not enough to reconstruct what code was deployed. Record the release tag, Docker image tag, and image digest together.

A Git tag points to a source revision. A Docker image tag provides a convenient name in a registry. The reproducible operational identifier is the record that includes the digest, not the tag alone.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Automating fmt, clippy, test, and build with GitHub Actions
- Next post: Reading SBOMs and image scan results
- Expansion criteria: before publication, reproduce tag creation, image build, registry push, digest lookup, and release-note recording in the example repository.

## Document Information

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial / release traceability design
- Test environment: No direct Git tag push, registry push, or release creation. This post documents tag and digest recording criteria.
- Tested versions: Git, Docker CLI/Engine, registry, and GitHub Actions runtime versions not recorded. Actual execution environment must be recorded before publication.
- Evidence level: Docker official documentation, GitHub official documentation, Git documentation

## Problem Statement

Even if CI passes, a release process is weak if operators cannot later answer: "Which commit produced the image that is currently deployed?"

Release records should answer:

- Which Git commit produced this release?
- Which image tag was pushed to the registry?
- Which image digest did that tag point to?
- Did the deployment tool use a tag or a digest?
- Can rollback pull the same image again?
- Does the release note record migrations, config changes, and known limitations?

This post connects release names and image identifiers before adding image scanning or SBOM policy.

## Verified Facts

- GitHub Releases documentation says releases are based on Git tags, and Git tags mark a specific point in repository history.
- GitHub Releases documentation describes releases as deployable software iterations that can include release notes and links to binary files.
- Docker image pull documentation says images can be pulled by name and tag, while a digest can be used as an immutable identifier for a specific image.
- Docker documentation treats tags as convenient names; pulling the same tag again can retrieve the current image that tag points to.
- Docker documentation for GitHub Actions shows a flow for managing image tags and labels with Docker metadata action.

## Identifier Roles

Traceability is not about adding many names. It is about assigning each identifier a clear role.

| Identifier | Example | Role | Watch out for |
| --- | --- | --- | --- |
| Git commit SHA | `6f3a1c8...` | Exact source location | Hard for humans to read |
| Git tag | `v0.3.0` | Release candidate or release point | Moving tags break traceability |
| GitHub Release | `v0.3.0` release page | Release note, asset, change history | Tag date and release date can differ |
| Docker image tag | `ghcr.io/org/rust-api:v0.3.0` | Human-friendly registry reference | Tags can move |
| Docker image digest | `sha256:...` | Image content identity | Long, but important for audit and reproduction |
| Deployment revision | Kubernetes ReplicaSet revision, for example | Actual deployment history | Must be connected to cluster state |

At minimum, operational records should include Git tag, commit SHA, image tag, and image digest together.

## Tag Policy Example

Start with a simple rule set.

| Situation | Git tag | Image tag | Purpose |
| --- | --- | --- | --- |
| Formal release | `v0.3.0` | `ghcr.io/org/rust-api:v0.3.0` | Human-readable release identifier |
| Commit trace | none | `ghcr.io/org/rust-api:sha-6f3a1c8` | Commit-based traceability |
| Default branch preview | none | `ghcr.io/org/rust-api:main` | Latest main-branch check, not a production pin |
| Moving alias | none | `ghcr.io/org/rust-api:latest` | Convenience alias, not an audit key |

`latest` does not need to be banned, but it should not be the only identifier in release notes or deployment manifests. Tags are convenient for humans; digests are stronger for reproduction.

## Manual Reproduction Steps

Before automation, verify the record fields manually.

1. Confirm the release commit.

```powershell
git status --short
git rev-parse HEAD
```

2. Create an annotated tag.

```powershell
git tag -a v0.3.0 -m "v0.3.0"
git push origin v0.3.0
```

3. Build the image from the same commit.

```powershell
docker build `
  -t ghcr.io/org/rust-api:v0.3.0 `
  -t ghcr.io/org/rust-api:sha-6f3a1c8 `
  .
```

4. Push the image tags.

```powershell
docker push ghcr.io/org/rust-api:v0.3.0
docker push ghcr.io/org/rust-api:sha-6f3a1c8
```

5. Pull and inspect the digest, then record it in the release note.

```powershell
docker pull ghcr.io/org/rust-api:v0.3.0
docker image inspect ghcr.io/org/rust-api:v0.3.0
```

Check the `RepoDigests` field in `docker image inspect` output. The published example should record the actual digest value.

## GitHub Actions Boundary

A tag-push workflow can build and push the image later in the series. For now, fix the policy boundary.

```yaml
on:
  push:
    tags:
      - "v*.*.*"
```

Automation should follow these rules:

- Only release tags such as `v*.*.*` push release images.
- Add both release tag and commit-based image tag.
- Record the pushed digest in workflow output or release notes.
- Grant registry write permission only to the release job.
- Include config changes, migration status, and rollback target in the release note.

Docker metadata action can reduce manual tag and label logic. Its generated rules are still release policy, so document which Git refs create which image tags.

## Release Note Format

Release notes should include both human-readable change information and operational identifiers.

```text
Release: v0.3.0
Commit: 6f3a1c8...
Image tag: ghcr.io/org/rust-api:v0.3.0
Image digest: ghcr.io/org/rust-api@sha256:...
Built by: GitHub Actions run URL
Database migration: yes/no
Config change: yes/no
Rollback target: ghcr.io/org/rust-api@sha256:...
Known limitations:
- ...
```

This looks verbose, but it saves time during incident response. It avoids the late question of whether a tag moved and which digest it pointed to at deployment time.

## Observation Status

This post does not yet include actual tag push or registry push output. Before publication, add:

- `git rev-parse HEAD` output
- Created Git tag and GitHub Release URL
- Docker image tag list
- Registry push result
- Confirmed image digest
- Confirmation that the release-note digest and deployment-manifest digest match

## Verification Checklist

- Is the commit pointed to by the release tag recorded?
- Does the image provide both release-tag and commit-based tags?
- Is `latest` excluded as the only audit or rollback identifier?
- Is the digest confirmed after registry push?
- Do release notes include commit SHA, image tag, image digest, and build run URL?
- Can the deployment manifest or deployment record trace to a digest?
- Is there an operational rule that prevents moving release tags?

## Interpretation

The goal is not to make version names look tidy. The goal is to answer quickly what was deployed and what can be rolled back.

Tags are good for humans, and digests are good for systems and audits. Using only one leaves a gap. Keep the human release tag and the reproducible digest together in the operational record.

## Limitations

- This post does not perform a real registry push or GitHub Release creation.
- Whether SemVer is appropriate depends on the service compatibility policy.
- Multi-architecture images require distinguishing the manifest-list digest from platform-specific image digests.
- Signed images, provenance, SBOMs, and vulnerability scans are covered in the next post.

## References

- [GitHub Docs: About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [Docker Docs: Pull an image by digest](https://docs.docker.com/reference/cli/docker/image/pull/)
- [Docker Docs: Manage tags and labels with GitHub Actions](https://docs.docker.com/build/ci/github-actions/manage-tags-labels/)
- [Git documentation: git tag](https://git-scm.com/docs/git-tag)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Expanded Git tag, GitHub Release, Docker image tag, image digest, and release-note criteria using official documentation.
