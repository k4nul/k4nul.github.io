---
title: "DevOps 운영 흐름"
layout: section-archive
permalink: /devops/
description: "Docker, Git, Jenkins, Kubernetes와 운영 자동화 흐름을 단계적으로 정리하는 DevOps 아카이브"
author_profile: true
sidebar:
  nav: "sections"
lang: ko
translation_key: topic-development-devops
section_key: development
topic_key: devops
topic_description: "Docker, Git, Jenkins, Kubernetes와 운영 자동화 흐름을 단계적으로 정리하는 분류다."
---

이 아카이브는 Docker 이미지와 레지스트리, Git 협업 흐름, Jenkins CI/CD, Kubernetes 설치와 운영을 하나의 학습 흐름으로 묶습니다. 도구 소개보다 실제 운영에서 확인해야 할 경계, 실패 조건, 검증 절차에 초점을 둡니다.

## AI agent 운영과의 연결

DevOps 글은 AI agent 작업을 자동 검증하고 배포 경계 안에 묶기 위한 기반입니다. agent가 만든 변경을 운영에 연결할 때는 [observable harness 전환](/ai/from-document-centered-ops-to-observable-harness/), [approval과 guardrail 경계](/ai/approval-boundaries-and-guardrails/), [AI Engineering 허브](/ai-engineering/)를 함께 보세요.

## 추천 흐름

- Docker: [컨테이너와 VM 차이](/devops/docker-containers-vs-vms/), [Dockerfile과 build context](/devops/dockerfile-basics-and-build-context/), [image와 tag/digest](/devops/docker-images-layers-tags-digests/), [registry push와 image 관리](/devops/docker-registry-push-and-image-management/)
- Git: [Git이 기록하는 것과 기록하지 않는 것](/devops/git-records-and-boundaries/), [status/diff/add/commit/log 흐름](/devops/git-status-diff-add-commit-log/), [branch와 merge](/devops/git-branch-and-merge/), [remote/fetch/pull/push](/devops/git-remote-fetch-pull-push/), [conflict 기본 절차](/devops/git-conflict-resolution-basics/), [rebase/squash/force push 주의점](/devops/git-rebase-squash-force-push/), [tag와 release로 Docker image version 연결](/devops/git-tags-releases-docker-image-versions/), [PR/MR 협업 흐름과 리뷰 기준](/devops/git-pr-mr-collaboration-review/)
- Jenkins: [Jenkins는 무엇이고 왜 아직도 많이 쓰이는가](/devops/jenkins-what-and-why-still-used/), [Jenkins 설치와 초기 설정](/devops/jenkins-installation-initial-setup/), [플러그인, credentials, tools를 어떻게 관리해야 하는가](/devops/jenkins-plugins-credentials-tools-management/), [Freestyle Job과 Pipeline은 무엇이 다른가](/devops/jenkins-freestyle-job-vs-pipeline/), [Declarative Pipeline 입문](/devops/jenkins-declarative-pipeline-introduction/), [Jenkinsfile 읽기](/devops/jenkinsfile-agent-stages-steps-post/), [environment, parameters, when 실전](/devops/jenkinsfile-environment-parameters-when/), [Docker image build와 registry push](/devops/jenkins-docker-image-build-registry-push/), [Jenkins 장애 원인 분리](/devops/jenkins-common-failures-troubleshooting/), [Jenkins와 Kubernetes 배포 경계](/devops/jenkins-to-kubernetes-deployment-boundary/)
- Kubernetes: 기본 리소스, 설치 전략, manifest, resource, storage, 온프렘 보완 요소는 공개 후 순차 반영
