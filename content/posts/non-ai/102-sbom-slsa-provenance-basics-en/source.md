---
layout: single
title: "SBOM, SLSA, and provenance basics"
description: "Explains SBOM, SLSA, and provenance basics with official documentation, operational checks, and limitations."
date: 2026-07-09 09:00:00 +09:00
lang: en
translation_key: sbom-slsa-provenance-basics
section: security
topic_key: security-engineering
categories: Security
tags: [security, devsecops, supply-chain-security, cloud-security]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/security/sbom-slsa-provenance-basics/
---

## Summary

SBOM, SLSA, and provenance are related but not interchangeable. An SBOM lists software components, provenance explains how an artifact was built, and SLSA defines supply-chain security tracks, levels, and requirements.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: tutorial | comparison
- Test environment: No live execution. This post is based on NTIA/CISA SBOM material and the official SLSA specification.
- Test version: SLSA v1.2 and NTIA/CISA SBOM material checked on 2026-04-29.
- Evidence level: official documentation, specification documentation

## Problem Statement

If SBOM, SLSA, and provenance are mixed together, the review criteria become unclear. An SBOM does not prove the build was safe. Provenance does not prove dependencies are vulnerability-free. Each artifact answers a different operational question.

This post separates the three terms.

## Verified Facts

- NTIA describes an SBOM as a formal record of components and supply chain relationships used in building software.
  Evidence: [NTIA Minimum Elements for SBOM](https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom)
- CISA supports SBOM adoption and operationalization and publishes 2025 SBOM Minimum Elements material.
  Evidence: [CISA SBOM](https://www.cisa.gov/sbom)
- The SLSA v1.2 specification defines SLSA levels, tracks, and recommended attestation formats including provenance.
  Evidence: [SLSA specification](https://slsa.dev/spec/)
- The SLSA build track defines levels intended to increase confidence that software has not been tampered with and can be traced back to source.
  Evidence: [SLSA Build Track](https://slsa.dev/spec/v1.2/)
- SLSA provenance is an attestation that links a build artifact to builder, source, build parameters, materials, and subject.
  Evidence: [SLSA Provenance](https://slsa.dev/spec/v1.2/provenance)

## Reproduction Steps

Use these questions to separate the terms.

| Item | Question answered | Typical contents | Caution |
| --- | --- | --- | --- |
| SBOM | What is inside this artifact? | component name, version, supplier, dependency relationship, identifier | It is input to analysis, not the vulnerability decision itself |
| Provenance | Where and how was this artifact built? | source, builder, build type, parameters, materials, subject | It is build evidence, not a dependency vulnerability list |
| SLSA | What supply-chain control level is met? | build/source track, level, requirements, verification | Treat it as requirements, not only a badge |

An initial rollout can look like this.

1. Choose the artifact: container image, binary, library package, or release archive.
2. Generate an SBOM: choose a consumable format such as SPDX or CycloneDX.
3. Check SBOM quality: component names, versions, suppliers, dependencies, licenses, and identifiers such as package URLs.
4. Generate build provenance: source commit, builder identity, build workflow, build parameters, and output artifact digest.
5. Verify artifact and provenance: digest match, trusted builder, expected source repository and ref.
6. Choose a SLSA target: record missing requirements instead of overstating the current level.

For a container image release, keep these records together:

```text
artifact: ghcr.io/example/app@sha256:...
sbom: app.spdx.json
provenance: app.intoto.jsonl
source: https://github.com/example/app@<commit>
builder: github-actions workflow <workflow file>@<commit>
verification:
  - image digest matched
  - provenance signature verified
  - SBOM generated for release artifact
```

## Observations

- SBOM improves component transparency, but it does not prove the build was trustworthy.
- Provenance connects an artifact to its build, but it does not automatically triage every dependency vulnerability.
- SLSA is closer to a supply-chain control maturity model than a single checklist.

## Interpretation

In my view, early adoption should focus less on "we generated an SBOM" and more on connecting artifact digest, SBOM, provenance, and source commit for the same release.

Opinion: use SLSA levels first as an internal gap analysis, not as marketing copy.

## Limitations

- SBOM formats, field expectations, and SLSA versions should be rechecked at adoption time.
- SBOM and provenance do not replace vulnerability triage, VEX, license review, image signing, or policy enforcement.
- This is an introduction and does not evaluate the output quality of specific tools.

## References

- [NTIA Minimum Elements for SBOM](https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom)
- [CISA SBOM](https://www.cisa.gov/sbom)
- [CISA 2025 Minimum Elements for SBOM](https://www.cisa.gov/resources-tools/resources/2025-minimum-elements-software-bill-materials-sbom)
- [SLSA specification](https://slsa.dev/spec/)
- [SLSA Provenance](https://slsa.dev/spec/v1.2/provenance)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Separated SBOM, SLSA, and provenance and added release-level review criteria.
