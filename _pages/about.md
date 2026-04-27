---
title: "소개"
layout: single
permalink: /about/
description: "K4NUL 블로그의 보안 분석, Rust, AI Engineering, DevOps 초점과 글 작성 원칙"
author_profile: true
sidebar:
  nav: "sections"
lang: ko
translation_key: page-about
---

이 블로그는 보안 분석, Rust, AI Engineering, DevOps를 중심으로 정리하는 개인 기술 블로그입니다. 빠르게 소비되는 요약보다, 시간이 지난 뒤에도 근거와 재현 조건을 다시 확인할 수 있는 기록을 남기는 데 목적을 둡니다.

## Focus Areas

- Security Analysis: 문서형 악성코드, 드로퍼, exploit chain, CVE 분석과 reverse engineering으로 확장되는 보안 분석 기록
- Rust: 설치, 디버깅, ownership/borrowing, error handling, CLI 프로젝트까지 이어지는 학습 기록
- AI Engineering / Agent Harness: Codex, Claude Code, 하네스 엔지니어링, 토큰 관리, agent workflow 운영 기록
- DevOps: Docker, build cache, registry, Git, Jenkins, Kubernetes, 운영 자동화와 트러블슈팅 기록

## Writing Principles

- 사실, 직접 재현한 결과, 해석, 한계를 구분해서 적습니다.
- 재현 가능한 환경과 버전을 가능한 한 명시합니다.
- 확인하지 못한 내용을 단정하지 않습니다.
- 최신성이나 버전에 민감한 내용은 검증 기준일을 남깁니다.
- 기술적 주장은 공식 문서, 표준 문서, 원저자 자료, 직접 재현 결과를 우선 근거로 삼습니다.

## Representative Work

- [Macro 기반 문서형 악성코드 분석](/malware/macro-malware/)
- [토큰 관리 01. 왜 하네스 엔지니어링에서 토큰 관리가 중요한가](/ai/why-token-management-matters-in-harness-engineering/)
- [Rust 13. 작은 CLI 프로젝트 만들기](/rust/rust-build-a-small-cli-project/)
- [Docker 04. 이미지 빌드가 느려지는 이유와 캐시가 깨지는 지점](/devops/docker-build-cache-and-invalidation/)

## Links

- [GitHub](https://github.com/k4nul)
- [RSS](/feed.xml)
- [Contact](/contact/)

## 검증과 출처에 대한 기본 방침

기술적인 주장이나 설정 방법을 다룰 때에는 공식 문서, 원문 자료, 직접 재현한 결과를 우선 참고합니다. 외부 자료를 인용하거나 해석할 때에는 출처를 확인할 수 있도록 연결하고, 직접 검증하지 못한 부분은 한계나 미확인 사항으로 남겨 둡니다.

실험 기록이 포함된 글에서는 가능한 범위에서 테스트 환경, 사용 버전, 관찰한 출력이나 실패 사례를 함께 남겨 독자가 맥락을 판단할 수 있도록 유지합니다.
