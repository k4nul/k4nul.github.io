---
title: "보안 분석과 악성코드 리서치"
layout: section-archive
permalink: /security/
description: "문서형 악성코드 분석, exploit chain 추적, CVE 분석, reverse engineering 흐름을 정리하는 보안 아카이브"
author_profile: true
sidebar:
  nav: "sections"
lang: ko
translation_key: section-security
section_key: security
section_description: "문서형 악성코드 분석, exploit chain 추적, CVE 분석, reverse engineering 흐름을 정리하는 보안 아카이브다."
---

문서형 악성코드, 드로퍼, 취약점 악용 흐름을 실제 샘플 기준으로 정리합니다. 현재 공개 글은 DOCM/RTF 문서형 악성코드 분석이 중심이며, CVE 분석과 reverse engineering 글은 같은 Security 트랙 안에서 확장합니다. 정적 분석과 동적 분석 과정, 주요 도구 사용 흐름, 쉘코드와 OLE 객체 추적 포인트를 중심으로 다룹니다.

## AI agent 보안과의 연결

Security 글은 AI agent 운영에서 권한, 민감정보, trace, 승인 경계를 보는 기준과 연결됩니다. agent를 실제 저장소에 붙일 때는 [approval과 guardrail 경계](/ai/approval-boundaries-and-guardrails/), [agent trace 설계](/ai/why-trace-matters-more-than-results/), [Claude Code permissions/settings 기준](/ai/fix-claude-code-boundaries-with-settings-and-permissions/)을 함께 보세요.

## 대표 글

- [문서형 악성코드 분석 모음](/security/malware-analysis/)
- [Macro 기반 문서형 악성코드 분석](/malware/macro-malware/)
- [RTF 기반 문서형 악성코드 분석](/malware/rtf-malware/)
