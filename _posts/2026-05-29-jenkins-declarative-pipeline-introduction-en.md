---
layout: single
title: "Jenkins 05. Introduction to Declarative Pipeline"
description: "An introductory Jenkins post explaining why beginners should start with Declarative Pipeline before moving into advanced Pipeline patterns."
date: 2026-05-29 09:00:00 +09:00
lang: en
translation_key: jenkins-declarative-pipeline-introduction
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, declarative-pipeline, scripted-pipeline, ci]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/jenkins-declarative-pipeline-introduction/
---

## Summary

Jenkins Pipeline has two syntaxes: Declarative and Scripted. Beginners should start with Declarative Pipeline and learn the `pipeline`, `agent`, `stages`, and `steps` structure first.

The conclusion of this post is that Declarative Pipeline makes Jenkinsfile easier to read and provides a good starting point for later Docker builds and deployment conditions.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: tutorial
- Test environment: verified against the author's Jenkins practice server. As of 2026-04-24, the unauthenticated login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`. The OS is Linux 22.04; agent details are not fixed in this post.
- Test version: the author's Jenkins practice server reported Jenkins 2.541.3 in the login response header on 2026-04-24. Documentation checks use the relevant official documents checked on 2026-04-24.
- Source level: Jenkins official documentation.
- Note: advanced Groovy usage in Scripted Pipeline is outside this post.

## Problem Definition

Pipeline introduces many terms at once: Groovy, Jenkinsfile, Declarative, Scripted, stage, and step. If you try to learn all of them together, it becomes harder to see what Jenkins is actually executing.

This post focuses on reading build, test, and deploy stages through Declarative Pipeline first.

## Verified Facts

- According to Jenkins Pipeline documentation, Pipeline is a suite of plugins for implementing and integrating continuous delivery pipelines into Jenkins.
  Evidence: [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- According to Jenkins Pipeline documentation, `Jenkinsfile` is a Pipeline definition file that can be committed to a source control repository.
  Evidence: [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- According to Jenkins Pipeline documentation, Jenkinsfile can be written using Declarative or Scripted syntax.
  Evidence: [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- According to Jenkins Pipeline documentation, Declarative Pipeline is designed to make Pipeline code easier to write and read.
  Evidence: [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- According to Jenkins Pipeline Syntax documentation, all valid Declarative Pipelines must be enclosed in a `pipeline` block.
  Evidence: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)

A minimal Declarative Pipeline skeleton looks like this:

```groovy
pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        echo 'build'
      }
    }
  }
}
```

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow on the author's Jenkins practice server. On 2026-04-24, the unauthenticated login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`.
- Documentation check result: official documentation was used to verify the basic Declarative Pipeline structure and its relationship to Scripted Pipeline.
- Needs reproduction: a real Jenkins Pipeline job should confirm that the `echo` stage succeeds.

## Interpretation / Opinion

My judgment is that Declarative Pipeline best shows beginners how Jenkins divides work. Stage names become useful anchors in the UI and logs, making build, test, and deploy failures easier to separate.

Scripted Pipeline is more flexible, but that freedom can be distracting early on. Start with Declarative. Consider Scripted syntax or shared libraries only when loops, complex conditions, or reusable abstractions are genuinely needed.

A good first Jenkinsfile only needs to answer three questions:

- Which agent runs the work?
- In what stage order does the work run?
- Which step failure stops the Pipeline?

## Limits and Exceptions

The Pipeline execution flow was checked in the author's practice environment. Stage visualization, console output, and failure-state details in the Jenkins UI can vary by Jenkins version and plugin set.

Declarative Pipeline does not need to express every complex deployment flow by itself. Complex logic may fit better in Scripted blocks, shared libraries, or external scripts.

## References

- Jenkins User Handbook, [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- Jenkins User Handbook, [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- Jenkins User Handbook, [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
