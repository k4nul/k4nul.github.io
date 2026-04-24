---
layout: single
title: "Jenkins 07. Practical Jenkinsfile: environment, parameters, when"
description: "A practical Jenkinsfile guide covering environment variables, user parameters, and conditional stage execution."
date: 2026-05-30 09:00:00 +0900
lang: en
translation_key: jenkinsfile-environment-parameters-when
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, jenkinsfile, environment, parameters, when]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/jenkinsfile-environment-parameters-when/
---

## Summary

After learning the basic Pipeline structure, the next step is deciding how values enter the Pipeline and when stages should be skipped. In Declarative Pipeline, `environment`, `parameters`, and `when` cover those needs.

The conclusion of this post is that changing values such as deploy environment, debug mode, and branch conditions should be explicit variables and conditions, not hidden constants in shell commands.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: tutorial
- Test environment: verified against the author's Jenkins practice server. As of 2026-04-24, the unauthenticated login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`. The OS is Linux 22.04; agent details are not fixed in this post.
- Test version: the author's Jenkins practice server reported Jenkins 2.541.3 in the login response header on 2026-04-24. Documentation checks use the relevant official documents checked on 2026-04-24.
- Source level: Jenkins official documentation.
- Note: credential binding security details should be handled more deeply in a separate security post.

## Problem Definition

Simple Pipelines can start with only Build and Test. Closer to real work, more questions appear:

- How should staging and production be separated?
- Which values should users provide for manual runs?
- Should deploy run only on a certain branch or tag?
- Can unnecessary agent allocation be avoided?

## Verified Facts

- According to Jenkins Pipeline Syntax documentation, the `environment` directive defines key-value environment variables for all steps or stage-specific steps.
  Evidence: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- According to the same documentation, the `environment` directive supports the `credentials()` helper for accessing predefined Jenkins credentials by identifier.
  Evidence: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- According to the same documentation, the `parameters` directive defines user-provided parameters for Pipeline triggering, and values are available through the `params` object and environment variables.
  Evidence: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- According to the same documentation, the `when` directive determines whether a stage should execute based on conditions.
  Evidence: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- According to the same documentation, `beforeAgent true` lets `when` be evaluated before entering the stage agent.
  Evidence: [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)

Example:

```groovy
pipeline {
  agent any
  parameters {
    choice(name: 'DEPLOY_ENV', choices: ['staging', 'production'], description: '')
  }
  environment {
    IMAGE_NAME = 'registry.example.com/team/app'
  }
  stages {
    stage('Deploy') {
      when {
        branch 'main'
      }
      steps {
        echo "deploy to ${params.DEPLOY_ENV}"
      }
    }
  }
}
```

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow on the author's Jenkins practice server. On 2026-04-24, the unauthenticated login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`.
- Documentation check result: official documentation was used to verify `environment`, `parameters`, `when`, and `beforeAgent`.
- Needs reproduction: in a Multibranch Pipeline, verify that branch conditions actually control stage execution.

## Interpretation / Opinion

My judgment is that `parameters` are useful but easy to overuse. Too many parameters can turn a Pipeline into a manual deployment button. Separate values needed for automated verification from values that require human approval.

`environment` is good for repeated names and external system addresses. Secret values should not be placed there as plain text; use credential IDs instead.

`when` can also save resources. If a branch is not deployable, Jenkins should not allocate a deploy agent. This matters when Docker build agents or deployment agents are limited.

## Limits and Exceptions

The basic conditional and parameter flow was checked in the author's practice environment. Multibranch Pipeline behavior, credential binding, and protected branch policy still need checks against the actual repository and permission model.

The `branch` condition depends on job type. Verify it in the actual Jenkins job type being used.

## References

- Jenkins User Handbook, [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- Jenkins User Handbook, [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
