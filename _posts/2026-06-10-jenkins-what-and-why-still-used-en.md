---
layout: single
title: "Jenkins 01. What Jenkins Is and Why It Is Still Used"
description: "An introductory Jenkins guide that connects Git, Docker, CI/CD automation, controller, agent, plugin, and Pipeline concepts."
date: 2026-06-10 09:00:00 +09:00
lang: en
translation_key: jenkins-what-and-why-still-used
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, ci, cd, automation, pipeline]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/jenkins-what-and-why-still-used/
---

## Summary

The Git posts covered history, branches, tags, and PR/MR workflows. The Docker posts covered images and registries. Jenkins is easiest to understand as the tool that automates the flow between them: fetch code, build it, test it, and leave a repeatable record of the result.

The conclusion of this post is that Jenkins should not be treated as a mere deploy button. It is a self-hosted automation server. Jenkins is still selected not because it is the newest option, but because plugins, agents, Pipeline, and Jenkinsfile can be combined to fit an organization's internal CI/CD environment.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: analysis
- Test environment: verified against the author's Jenkins practice server. As of 2026-04-24, the unauthenticated login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`. The OS is Linux 22.04; agent details are not fixed in this post.
- Test version: the author's Jenkins practice server reported Jenkins 2.541.3 in the login response header on 2026-04-24. Documentation checks use the relevant official documents checked on 2026-04-24.
- Source level: Jenkins official documentation, Jenkins LTS changelog, and Jenkins Java Support Policy.
- Note: this post focuses on Jenkins concepts before onboarding. It does not compare Jenkins against GitHub Actions, GitLab CI, or Tekton.

## Problem Definition

After learning Git, the next question is where automated checks should run. People can review diffs in PR/MR, but build, test, image creation, and registry push steps become painful if they are run manually every time.

Common Jenkins misunderstandings include:

- Treating Jenkins as a replacement for Git.
- Seeing Jenkins only as a web page with a deploy button.
- Assuming that installing more plugins always makes Jenkins better.
- Assuming that keeping Pipeline code directly in the UI is enough.
- Running every build on one server without separating controller and agent responsibilities.

This post explains what problem Jenkins solves and why it belongs after Git and Docker in this series. Installation, initial passwords, plugin selection, and first job creation are left for the next post.

## Verified Facts

- According to Jenkins official user documentation, Jenkins is a self-contained open source automation server that can automate tasks related to building, testing, delivering, and deploying software.
  Evidence: [Jenkins User Documentation - What is Jenkins?](https://www.jenkins.io/doc/)
- According to the Jenkins official site, Jenkins can be used as a simple CI server or expanded into a continuous delivery hub for a project.
  Evidence: [Jenkins](https://www.jenkins.io/)
- According to the Jenkins official site, Jenkins is extensible through its plugin architecture, and the Update Center provides plugins for integrating build tools, cloud providers, analysis tools, and more.
  Evidence: [Jenkins](https://www.jenkins.io/), [Managing Plugins](https://www.jenkins.io/doc/book/managing/plugins/)
- According to Jenkins Pipeline documentation, Pipeline is a suite of plugins for implementing and integrating continuous delivery pipelines in Jenkins. A Pipeline definition can be written as a text file called `Jenkinsfile` and committed to a source control repository.
  Evidence: [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- According to Jenkins Pipeline documentation, storing a `Jenkinsfile` in source control provides benefits such as Pipeline build processes for branches and pull requests, Pipeline code review, audit trail, and a single source of truth.
  Evidence: [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- According to Jenkins agents documentation, the Jenkins controller manages agents and orchestrates job scheduling and monitoring. Agents provide executors that perform work requested by the controller and can run Pipeline steps, freestyle jobs, and other jobs.
  Evidence: [Using Jenkins agents](https://www.jenkins.io/doc/book/using/using-agents/)
- According to Jenkins controller isolation documentation, long-running Jenkins environments should avoid running builds on the built-in node and should run builds on agents. Builds on the built-in node have the same level of access to the controller filesystem as the Jenkins process.
  Evidence: [Controller Isolation](https://www.jenkins.io/doc/book/security/controller-isolation/)
- According to Jenkins credentials documentation, Jenkins credentials are stored in encrypted form on the controller and can be handled in Pipeline projects through credential IDs.
  Evidence: [Using credentials](https://www.jenkins.io/doc/book/using/using-credentials/)
- According to the Jenkins LTS changelog and Java Support Policy checked on 2026-04-24, Jenkins LTS 2.555.1 requires Java 21 or Java 25 and does not support Java 17.
  Evidence: [LTS Changelog](https://www.jenkins.io/changelog-stable/), [Java Support Policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/)
- The author's Jenkins practice server reported Jenkins 2.541.3 in the login response header on 2026-04-24. Java requirements can differ by LTS version, so the Java requirement above should be read as applying to 2.555.1.
  Evidence: login response header from the author's Jenkins practice server

After Git and Docker, the Jenkins flow can be viewed like this:

```text
Git push or PR/MR
Jenkins job or multibranch Pipeline
checkout source
build and test
create artifact or Docker image
publish result or push image
```

Jenkins is not the source history itself, and it is not the Docker image itself. Jenkins is the automation execution point that fetches source from Git, runs a defined process, and leaves results that people can inspect.

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow on the author's Jenkins practice server. On 2026-04-24, the unauthenticated login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`.
- Documentation check result: as of 2026-04-24, Jenkins official documentation was used to verify the automation server, plugin, Pipeline, Jenkinsfile, controller/agent, credentials, and Java requirement claims.
- Planned follow-up reproduction: Jenkins 02 will run Jenkins through Docker or a local installation path and record initial setup and basic verification results separately.

## Interpretation / Opinion

My judgment is that the most important Jenkins mental model is "where automation runs." Git provides change history and collaboration flow. Docker provides runnable images and registry flow. Jenkins takes those inputs and executes a defined sequence.

Jenkins is still selected more easily in environments like these:

- Internal networks, internal Git servers, internal registries, or internal artifact repositories that cannot be attached directly to an external SaaS workflow.
- Build agents that need to be separated by Linux, Windows, Docker, high-memory hardware, or specialized tools.
- CI/CD flows that should live as `Jenkinsfile` in the repository and be reviewed like source code.
- Older deployment scripts that need to be connected gradually to newer Pipeline workflows through plugins or shell steps.

Those strengths come with operational cost. If teams install plugins without discipline, lack credential management rules, or run all builds on the controller, Jenkins becomes opaque quickly. Beginners should separate the responsibilities of controller, agent, credential, plugin, and Jenkinsfile from the start.

This series will handle Jenkins in this order:

```text
installation and initial setup
plugin, credentials, and tools management
Freestyle Job versus Pipeline
Declarative Pipeline
basic Jenkinsfile syntax
Docker image build and registry push
operational troubleshooting
boundaries when connecting Jenkins to Kubernetes deployment
```

This order connects Git branches, PR/MR, and tags to Jenkins Pipeline triggers and verification gates. It also connects Docker image tags and digests to Jenkins build artifact records.

## Limits and Exceptions

The "why it is still used" conclusion is not based on usage statistics or market share research. It is an interpretation based on Jenkins capabilities confirmed in official documentation and common self-hosted CI/CD operating contexts.

This post focuses on Jenkins concepts. Detailed UI flow, plugin installation screens, initial password handling, and real Pipeline execution are covered in Jenkins 02 and later posts.

Jenkins LTS and Java requirements are date- and version-sensitive. This post is based on documents checked on 2026-04-24. Requirements may change in later LTS or weekly releases.

Jenkins may not be the simplest choice for teams that only use GitHub repositories and GitHub-hosted runners, teams that keep issues, MR, registry, and runners inside GitLab, or teams that prioritize Kubernetes-native pipelines.

## References

- Jenkins, [Jenkins User Documentation](https://www.jenkins.io/doc/)
- Jenkins, [Jenkins](https://www.jenkins.io/)
- Jenkins User Handbook, [Pipeline](https://www.jenkins.io/doc/book/pipeline/)
- Jenkins User Handbook, [Managing Plugins](https://www.jenkins.io/doc/book/managing/plugins/)
- Jenkins User Handbook, [Using Jenkins agents](https://www.jenkins.io/doc/book/using/using-agents/)
- Jenkins User Handbook, [Controller Isolation](https://www.jenkins.io/doc/book/security/controller-isolation/)
- Jenkins User Handbook, [Using credentials](https://www.jenkins.io/doc/book/using/using-credentials/)
- Jenkins, [LTS Changelog](https://www.jenkins.io/changelog-stable/)
- Jenkins User Handbook, [Java Support Policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/)
