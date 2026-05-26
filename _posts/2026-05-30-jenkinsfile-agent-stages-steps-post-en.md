---
layout: single
title: "Jenkins 06. How to Read a Jenkinsfile: agent, stages, steps, and post"
description: "A practical guide for first-time Jenkinsfile readers to separate agent, stages, steps, and post by execution flow."
date: 2026-05-30 09:00:00 +09:00
lang: en
translation_key: jenkinsfile-agent-stages-steps-post
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, jenkinsfile, agent, stages, post]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/jenkinsfile-agent-stages-steps-post/
---

## Summary

When you first open a Jenkinsfile, `agent`, `stages`, `steps`, and `post` appear again and again inside `pipeline { ... }`. These four blocks are not just Groovy syntax to memorize. They are the operating structure that tells you where work runs, how it is split, what each stage does, and what must happen after completion.

The conclusion of this post is that beginners should read Jenkinsfile as an execution plan before treating it like Groovy code. If you already read [Jenkins 05. Introduction to Declarative Pipeline](/en/devops/jenkins-declarative-pipeline-introduction/), this is the next step that makes Docker build and deployment stages easier to follow.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: tutorial
- Test environment: verified against the author's Jenkins practice server. As of 2026-04-24, the unauthenticated login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`. The OS is Linux 22.04; agent details are not fixed in this post.
- Test version: the author's Jenkins practice server reported Jenkins 2.541.3 in the login response header on 2026-04-24. Documentation checks use the relevant official documents checked on 2026-04-24.
- Source level: Jenkins official documentation.
- Note: `options`, `tools`, `input`, `parallel`, and `matrix` are outside the core scope of this post.

## Problem Definition

Jenkinsfile can look intimidating because of nested braces. At the beginner level, you do not need to memorize every directive. First separate execution location, stages, stage steps, and post-run behavior.

Teams that keep copying `agent any` or repeating `steps { sh '...' }` without reading the surrounding structure often lose track of why a stage runs on a given node and what cleanup or reporting should still happen after failure. This post narrows the reading model down to that minimum.

## Verified Facts

- According to Jenkins Pipeline Syntax documentation, the `agent` section specifies where the entire Pipeline or a specific stage executes in the Jenkins environment.
  Evidence: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- According to the same documentation, the `stages` section contains one or more `stage` directives and holds most of the work described by a Pipeline.
  Evidence: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- According to the same documentation, the `steps` section defines one or more steps executed in a given `stage`.
  Evidence: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- According to the same documentation, the `post` section defines additional steps to run after a Pipeline or stage completes and supports condition blocks such as `always`, `success`, `failure`, and `cleanup`.
  Evidence: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)

A basic structure can be read like this:

```groovy
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'make'
      }
    }
    stage('Test') {
      steps {
        sh 'make test'
      }
    }
  }
  post {
    always {
      echo 'finished'
    }
  }
}
```

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow on the author's Jenkins practice server. On 2026-04-24, the unauthenticated login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`.
- Documentation check result: official documentation was used to verify the role and location of the four blocks.
- Needs reproduction: use `sh` on Linux agents and `bat` or `powershell` on Windows agents to run this structure directly.

## Interpretation / Opinion

My judgment is that teams should move beyond leaving `agent` as `any` everywhere. Jobs that need Docker builds, Windows builds, or deployment credentials may need different agents.

`stages` are operational units for humans. Names like Build, Test, Package, Push, and Deploy make failures easier to locate.

`post` matters most when things fail. Notifications, log cleanup, temporary file cleanup, and test report collection may need to run regardless of success.

## Limits and Exceptions

This post covers only part of Jenkinsfile syntax. Real operational Pipelines may also use `options`, `environment`, `parameters`, `when`, `tools`, and `parallel`.

Agent operating systems affect whether `sh`, `bat`, `powershell`, or `pwsh` should be used.

## Related Posts

- [DevOps Operations Flow](/en/development/devops/)
- [Jenkins 05. Introduction to Declarative Pipeline](/en/devops/jenkins-declarative-pipeline-introduction/)
- [What Jenkins Is and Why It Is Still Used](/en/devops/jenkins-what-and-why-still-used/)
- [PR/MR Collaboration Flow and Review Criteria](/en/devops/git-pr-mr-collaboration-review/)
- [Docker registry push and image management](/en/devops/docker-registry-push-and-image-management/)

## References

- Jenkins User Handbook, [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- Jenkins User Handbook, [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
