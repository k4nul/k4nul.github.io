---
layout: single
title: "Rust Service 19. Reading SBOMs and image scan results"
description: "Explains how to read SBOMs, vulnerability scan results, false positives, and remediation priority for a Rust API image."
date: 2027-01-26 09:00:00 +09:00
lang: en
translation_key: rust-api-sbom-image-scan-results
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
permalink: /en/rust/rust-api-sbom-image-scan-results/
---

## Summary

Scan output is not a simple pass/fail button. It is input for operational judgment.

An SBOM shows what is inside an image, while a vulnerability scan shows whether those components match known vulnerability data. Remediation should consider package name, version, CVE, fix availability, runtime exposure, and base-image replacement together.

## Curriculum Position

- Series: Rust Service to Production
- Previous post: Connecting release tags and Docker image tags
- Next post: Deploying with Kubernetes Deployment and Service
- Expansion criteria: before publication, add SBOM generation, CVE scan, saved result files, and examples of fix/defer decisions in the example repository.

## Document Information

- Written date: 2026-05-04
- Verification date: 2026-05-05
- Document type: tutorial / supply chain security result interpretation
- Test environment: No direct SBOM generation or image scan execution. This post defines how to read results and convert them into release decisions.
- Checked documents: CISA SBOM resources, Docker Scout documentation, Docker Scout CLI documentation, Docker SBOM attestation documentation, SLSA v1.2
- Evidence level: government and official documentation, Docker official documentation, supply chain security specification

## Problem Statement

After release tags and digests are recorded, the next question is whether the image is acceptable to deploy. Treating scan output as a mechanical pass/fail answer can miss operational reality.

Review these questions:

- Was the scan run against a tag or a digest?
- Which image digest produced the SBOM?
- Did the vulnerability come from an OS package or a Rust crate?
- Is there a fixed version?
- Is the vulnerable package actually present in the runtime image?
- What are the exploitability and service exposure conditions?
- Can a base-image update fix it, or does an application dependency need to change?
- If it is not fixed now, who accepts the risk, until when, and why?

The goal is not to choose one scanner. The goal is to turn scan output into release judgment.

## Verified Facts

- CISA treats SBOMs as material for software transparency and supply chain security, and published 2025 minimum-elements draft guidance for public comment.
- Docker Scout documentation says Docker Scout analyzes images, compiles a component inventory known as an SBOM, and matches it against a vulnerability database.
- `docker scout sbom` can output SBOM data as `json`, `spdx`, `cyclonedx`, or `list`.
- `docker scout cves` can output vulnerability reports as package grouping, SARIF, SPDX, GitLab, markdown, or SBOM formats, and provides an option to return a non-zero exit code when vulnerabilities are detected.
- Docker BuildKit supports SBOM attestations, and Docker documentation says BuildKit uses a Syft-based scanner plugin by default.
- SLSA v1.2 is an incrementally adoptable guideline set for software supply chain security, covering trust from source through build, packaging, and distribution.
- SLSA does not replace code quality review, producer trust decisions, or recursive evaluation of all dependency trust by one automatic level.

## Separate SBOM And Scan Output

An SBOM and a vulnerability scan are not the same thing.

| Artifact | Question answered | Example use |
| --- | --- | --- |
| SBOM | What is inside this artifact? | Package inventory, license review, impact lookup after a new CVE |
| Vulnerability scan | Which components match known vulnerability data? | Release gate, remediation priority, security tickets |
| Provenance / attestation | Was this artifact built from the expected source and build system? | Build-tampering defense, audit evidence |
| VEX | Is a vulnerability actually exploitable or applicable for this artifact? | False positive or not-affected evidence |

The SBOM is closer to an ingredient list. The scan is a matching process against known vulnerability data. Both help release decisions, but they play different roles.

## Reproduction Commands

In the example repository, record results against an image digest when possible.

1. Confirm the image digest.

```powershell
docker pull ghcr.io/org/rust-api:v0.3.0
docker image inspect ghcr.io/org/rust-api:v0.3.0
```

2. Save the SBOM to a file.

```powershell
docker scout sbom `
  --format spdx `
  --output rust-api-v0.3.0.spdx.json `
  ghcr.io/org/rust-api:v0.3.0
```

3. Split human-readable and CI-readable vulnerability output.

```powershell
docker scout cves `
  --format markdown `
  --output rust-api-v0.3.0-cves.md `
  ghcr.io/org/rust-api:v0.3.0

docker scout cves `
  --format sarif `
  --output rust-api-v0.3.0-cves.sarif.json `
  ghcr.io/org/rust-api:v0.3.0
```

4. Record a release decision table.

```text
image: ghcr.io/org/rust-api@sha256:...
sbom: rust-api-v0.3.0.spdx.json
scan: rust-api-v0.3.0-cves.md
critical: 0
high: 0
medium: 2
accepted: 1
action required: 1
decision owner: security/platform
decision date: 2026-05-05
```

The numbers are examples. The actual post should record the real output and the reasoning behind the decision.

## Reading The Results

Do not copy severity alone into a ticket.

| Field | Question | Example |
| --- | --- | --- |
| Package | Which package is affected? | `openssl`, `glibc`, Rust crate name |
| Version | Current and fixed version? | `1.2.3 -> 1.2.4` |
| Source | OS package or language dependency? | Base image update or Cargo update |
| CVE | Which vulnerability ID? | `CVE-...` |
| Fix available | Is a fixed package available? | yes/no |
| Runtime exposure | Is it in the runtime image and reachable? | yes/no/unknown |
| Action | Update, replace base image, defer, false positive | Owner and due date |

The useful judgment is not "high means fail." It is closer to "high severity, fixed version available, present in runtime image, so fix today."

## Release Gate Example

The first release gate can stay simple.

| Condition | Default decision |
| --- | --- |
| Critical vulnerability with fix | Block release |
| High vulnerability with fix and runtime exposure | Block release or require urgent approval |
| High vulnerability without fix | Require risk acceptance and follow-up ticket |
| Medium/Low | Ticket according to SLA |
| Vulnerability from base image | Check base image update |
| Vulnerability from Rust crate | Try `cargo update`, dependency replacement, or feature removal |

Make the table stricter when policy requires it. The key is to avoid changing release criteria ad hoc for each release.

## Observation Status

This post does not yet include real scan output. Before publication, add:

- Docker Scout or scanner version
- Scanned image digest
- SBOM filename and format
- CVE summary counts
- Fixed items and deferred items
- Evidence for false-positive or not-affected decisions
- Release gate pass/block decision and decision owner

## Verification Checklist

- Are SBOM and scan results connected to a digest, not only a tag?
- Are SBOM and vulnerability scan roles separated?
- Are scanner version and scan date recorded?
- Are OS package and Rust crate remediation paths separated?
- Was fix availability checked?
- Were runtime exposure and exploitability considered beyond severity?
- Do deferred or accepted risks have an owner and due date?
- Are result files linked from release notes or security tickets?

## Interpretation

Vulnerability scanners do not make operational decisions for the team. They report what matches known vulnerability data. The team still has to decide what that means for this image and this service.

The SBOM is the starting point for that decision. When a new CVE appears later, operators should be able to ask whether a released image contained the affected package without reopening the image manually. That is why SBOM, scan output, and image digest belong together in the release record.

## Limitations

- This post uses Docker Scout as an example tool, but does not require adopting a specific scanner.
- Scanners can differ by vulnerability database, package detection method, and reachability analysis.
- Static Rust binary dependencies and OS packages may be detected differently by different tools.
- Regulatory compliance, license policy, and VEX operations may require separate policy documents.

## References

- [CISA: Software Bill of Materials](https://www.cisa.gov/sbom)
- [CISA: 2025 Minimum Elements for a Software Bill of Materials](https://www.cisa.gov/resources-tools/resources/2025-minimum-elements-software-bill-materials-sbom)
- [Docker Scout documentation](https://docs.docker.com/scout/)
- [Docker Scout SBOM command](https://docs.docker.com/reference/cli/docker/scout/sbom/)
- [Docker Scout CVEs command](https://docs.docker.com/reference/cli/docker/scout/cves/)
- [Docker: SBOM attestations](https://docs.docker.com/build/metadata/attestations/sbom/)
- [SLSA v1.2: About SLSA](https://slsa.dev/spec/v1.2/about)

## Change Log

- 2026-05-04: Initial Rust Service to Production curriculum draft.
- 2026-05-05: Expanded SBOM, vulnerability scan, attestation, image digest, release gate, and risk-acceptance criteria using CISA, Docker, and SLSA documentation.
