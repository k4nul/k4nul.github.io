---
title: "DevOps Operations Flow"
layout: section-archive
permalink: /en/development/devops/
description: "Archive for Docker, Git, Jenkins, Kubernetes, and practical operations automation workflows."
author_profile: true
sidebar:
  nav: "sections"
lang: en
translation_key: topic-development-devops
section_key: development
topic_key: devops
topic_description: "Archive for Docker, Git, Jenkins, Kubernetes, and practical operations automation workflows."
---

This archive connects Docker images and registries, Git collaboration, Jenkins CI/CD, and Kubernetes operations into one learning path. The focus is on operational boundaries, failure conditions, and verification steps rather than tool introductions alone.

## Connection to AI Agent Operations

The DevOps track provides the automation and deployment boundary behind agent work. When an agent changes a repository, pair this archive with [observable harness migration](/en/ai/from-document-centered-ops-to-an-observable-harness/), [approval boundaries and guardrails](/en/ai/approval-boundaries-and-guardrails/), and the [AI Engineering Hub](/en/development/ai/).

## Suggested Flow

- Docker: [containers vs. VMs](/en/devops/docker-containers-vs-vms/), [Dockerfile and build context](/en/devops/dockerfile-basics-and-build-context/), [images, layers, tags, and digests](/en/devops/docker-images-layers-tags-digests/), [registry push and image management](/en/devops/docker-registry-push-and-image-management/)
- Git: [what Git records](/en/devops/git-records-and-boundaries/), [status/diff/add/commit/log flow](/en/devops/git-status-diff-add-commit-log/), [branch and merge](/en/devops/git-branch-and-merge/), [remote/fetch/pull/push](/en/devops/git-remote-fetch-pull-push/), [conflict basics](/en/devops/git-conflict-resolution-basics/), [rebase/squash/force push care](/en/devops/git-rebase-squash-force-push/), [tags, releases, and Docker image versions](/en/devops/git-tags-releases-docker-image-versions/), [PR/MR review flow](/en/devops/git-pr-mr-collaboration-review/)
- Jenkins: [what Jenkins is and why it is still used](/en/devops/jenkins-what-and-why-still-used/), [installation and initial setup](/en/devops/jenkins-installation-initial-setup/), [managing plugins, credentials, and tools](/en/devops/jenkins-plugins-credentials-tools-management/), [Freestyle Job vs Pipeline](/en/devops/jenkins-freestyle-job-vs-pipeline/), [Introduction to Declarative Pipeline](/en/devops/jenkins-declarative-pipeline-introduction/), [How to Read a Jenkinsfile](/en/devops/jenkinsfile-agent-stages-steps-post/), [environment, parameters, and when](/en/devops/jenkinsfile-environment-parameters-when/), [Docker image builds and registry pushes](/en/devops/jenkins-docker-image-build-registry-push/), [Jenkins failure separation](/en/devops/jenkins-common-failures-troubleshooting/), [Jenkins and Kubernetes deployment boundary](/en/devops/jenkins-to-kubernetes-deployment-boundary/)
- Kubernetes: core resources, installation strategy, manifests, resources, storage, and on-prem add-ons will be added after publication
