---
layout: single
title: "Container image signing and scan result interpretation"
description: "Separates container image signing, digest verification, SBOM evidence, and vulnerability scan interpretation for release review."
date: 2026-07-23 09:00:00 +09:00
lang: en
translation_key: container-image-signing-and-scan-results
section: security
topic_key: security-engineering
categories: Security
tags: [security, devsecops, supply-chain-security, cloud-security]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/security/container-image-signing-and-scan-results/
---

## Summary

Container image signing answers "who signed this exact image digest, with which identity?" Vulnerability scanning answers "does this image contain known vulnerable packages or configurations?" A signature does not mean the image is vulnerability-free, and a clean scan does not prove provenance.

The operational baseline is to pin the release artifact by digest, attach signature and SBOM or provenance evidence to that digest, and record signature verification separately from vulnerability triage.

## Document Information

- Written date: 2026-04-29
- Verification date: 2026-04-29
- Document type: tutorial | analysis
- Test environment: No local execution. The procedure is based on Sigstore Cosign, Docker Scout, and Trivy official documentation.
- Tested versions: Official documentation checked on 2026-04-29. CLI output format is not fixed.
- Evidence level: official documentation, original project documentation

## Problem Statement

Image review often collapses signing, SBOMs, and scanning into one pass/fail mark. That hides important differences. Signing is about artifact identity and integrity. Scanning is about comparing package metadata against vulnerability advisories.

A release record should therefore separate signature verification, SBOM presence, vulnerability scan results, and exception approval.

## Verified Facts

- Sigstore Cosign supports container image signing and attestations, including keyless signing through OIDC identity.
- Docker Scout image analysis extracts SBOM and image metadata and evaluates it against vulnerability advisory data.
- Docker Scout documents that severity can vary by advisory source, and a preferred advisory severity may appear with a fallback CVSS score.
- Trivy is documented as a scanner for container images, filesystems, root filesystems, and Git repositories.
- The verification date for this post is 2026-04-29. CLI flags and wording may change later.

## Baseline Procedure

1. Build the image and record the digest, such as `registry.example.com/app@sha256:...`, not only a tag.
2. Sign that digest with `cosign sign` or the organization's signing pipeline.
3. At the deployment gate, run `cosign verify` and check signer identity, certificate issuer, OIDC subject, bundle, or transparency log policy.
4. Generate SBOM and provenance attestations at build time and attach them to the image.
5. Scan the same digest with a scanner such as `trivy image` or `docker scout cves`.
6. For Critical and High findings, review package, installed version, fixed version, exploitability, and runtime exposure.
7. For findings that cannot be fixed immediately, record exception reason, expiry date, and reviewer.
8. Keep signature verification and vulnerability triage as separate release evidence.

## Interpreting Results

| Item | What to Check | Common Mistake |
| --- | --- | --- |
| Image digest | Which exact artifact is being deployed | Assuming a tag such as `latest` is stable |
| Signature | Which identity signed this digest | Treating a signature as proof of no vulnerabilities |
| SBOM | Which OS, package, and application dependencies exist | Treating SBOM presence as vulnerability resolution |
| CVE severity | Advisory source, CVSS, distribution judgment | Treating a score alone as final operational risk |
| Fixed version | Whether an upgrade path exists | Failing every unfixed CVE without triage |
| Runtime exposure | Whether the vulnerable component is reachable | Treating every package in the image as equal risk |

## Operational Judgment

Signature verification failure is usually a deployment blocker. If the artifact source cannot be verified, a good scan result does not repair the supply-chain gap.

Scan findings can either block release or require an approved exception. An exploitable Critical issue in an internet-facing service is close to a blocker. An unfixed Low finding in a development-only image might be acceptable with an expiry date and review owner.

Differences across scanners are normal. Advisory sources, operating-system distribution judgments, language lockfile parsing, and SBOM generation can all change results. The important record is which tool produced which judgment and why the release decision followed from it.

## Limitations

- Vulnerability scanners depend on known vulnerabilities and detectable package metadata.
- A signature verifies the signer-to-artifact relationship; it does not prove source code or build scripts are safe.
- Private registries, air-gapped environments, private CAs, and private KMS systems need their own verification policy.

## References

- [Sigstore Cosign: Signing Containers](https://docs.sigstore.dev/cosign/signing/signing_with_containers/)
- [Sigstore overview](https://docs.sigstore.dev/)
- [Docker Scout image analysis](https://docs.docker.com/scout/explore/analysis/)
- [Docker Scout CVEs CLI reference](https://docs.docker.com/reference/cli/docker/scout/cves/)
- [Trivy vulnerability scanning](https://trivy.dev/latest/docs/scanner/vulnerability/)

## Change Log

- 2026-04-29: Initial draft.
- 2026-04-29: Added digest-based verification, signing versus scanning boundaries, and CVE interpretation criteria.
