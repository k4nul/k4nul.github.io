---
layout: single
title: "Jenkins 02. Jenkins Installation and Initial Setup"
description: "A checklist-style Jenkins installation guide covering Java requirements, JENKINS_HOME, initial password, and first plugin choices."
date: 2026-06-12 09:00:00 +0900
lang: en
translation_key: jenkins-installation-initial-setup
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, installation, initial-setup, java, docker]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/jenkins-installation-initial-setup/
---

## Summary

Installing Jenkins is less about which button to click and more about deciding where controller state lives, which Java version runs Jenkins, and which plugins should exist from the beginning. Jenkins stores UI configuration, job configuration, credentials-related state, and plugin state under `JENKINS_HOME`, so that path should not be treated as temporary.

The conclusion of this post is that Docker is useful for beginner practice, but production installation needs a separate checklist for Java version, storage, backups, network ports, and plugin inventory.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: tutorial
- Test environment: verified against the author's Jenkins practice server. As of 2026-04-24, the unauthenticated login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`. The OS is Linux 22.04; agent details are not fixed in this post.
- Test version: the author's Jenkins practice server reported Jenkins 2.541.3 in the login response header on 2026-04-24. Documentation checks use the relevant official documents checked on 2026-04-24.
- Source level: Jenkins official documentation and Jenkins LTS changelog.
- Note: real Docker command execution and first screen verification should be reproduced in a separate practice environment.

## Problem Definition

First Jenkins installations often fail in predictable ways:

- The controller state location is ignored.
- Java requirements are checked only after installation.
- Suggested plugins are installed without recording why they are needed.
- Initial admin account, URL, and port settings are left as temporary values.

This post focuses on what to decide before installation, not on memorizing one installation command.

## Verified Facts

- According to Jenkins installation documentation, the installation chapter covers new installations, and Jenkins is typically run as a standalone process.
  Evidence: [Installing Jenkins](https://www.jenkins.io/doc/book/installing/)
- According to the Jenkins LTS changelog and Java Support Policy checked on 2026-04-24, Jenkins LTS 2.555.1 requires Java 21 or Java 25.
  Evidence: [LTS Changelog](https://www.jenkins.io/changelog-stable/), [Java Support Policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/)
- The author's Jenkins practice server reported Jenkins 2.541.3 in the login response header on 2026-04-24. Java requirements can differ by LTS version, so check the Java Support Policy for the exact version you plan to install.
  Evidence: login response header from the author's Jenkins practice server
- According to the Jenkins Docker installation documentation, the Docker path maps `/var/jenkins_home` to a volume to preserve the Jenkins home directory.
  Evidence: [Installing Jenkins - Docker](https://www.jenkins.io/doc/book/installing/docker/)
- According to the Jenkins Docker installation documentation, the initial administrator password can be read from `/var/jenkins_home/secrets/initialAdminPassword` when Jenkins runs in Docker.
  Evidence: [Installing Jenkins - Docker](https://www.jenkins.io/doc/book/installing/docker/)
- According to Jenkins Initial Settings documentation, Jenkins networking settings can be adjusted through command line arguments, and the default HTTP port is 8080.
  Evidence: [Initial Settings](https://www.jenkins.io/doc/book/installing/initial-settings/)

A beginner setup flow can be summarized as:

```text
check Java requirements
choose installation method
decide how to persist JENKINS_HOME
start the Jenkins controller
read initialAdminPassword
choose plugins
create the first administrator account
verify Jenkins URL and basic security settings
```

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow on the author's Jenkins practice server. On 2026-04-24, the unauthenticated login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`.
- Verified through documentation: installation methods, Java requirements, initial password location, and startup parameters were checked in official documentation.
- Needs reproduction: Jenkins should be started on Docker Desktop or a Linux host, and the first screen plus `JENKINS_HOME` persistence should be checked directly.

## Interpretation / Opinion

My judgment is that the first value to stabilize is `JENKINS_HOME`. Jenkins is not just an executable. It is a server that accumulates controller state over time. Losing that directory can mean losing job configuration, plugin state, build history, and credentials-related state.

For beginner practice, Docker is a good path because it connects directly to the image, container, and volume concepts from the Docker posts. For operations, the installation method is less important than these questions:

- Does the Java version match the Jenkins LTS requirement?
- Is the controller data directory placed somewhere that can be backed up?
- Is the plugin list recorded with reasons?
- Are Jenkins URL, HTTP/HTTPS, and reverse proxy boundaries clear?
- Will builds run on the controller or on agents?

After installation, it is safer to verify controller persistence, plugin reproducibility, and non-temporary admin settings before writing a complex Pipeline.

## Limits and Exceptions

This post verified the Jenkins installation flow in the author's practice environment. Errors specific to Windows, Linux distributions, Docker Desktop, or WSL still need environment-specific checks.

Jenkins LTS and Java requirements are date-sensitive. This post is based on documents checked on 2026-04-24.

Production environments should separately verify TLS, reverse proxy, backup, restore, plugin pinning, controller/agent separation, and account authorization policies.

## References

- Jenkins User Handbook, [Installing Jenkins](https://www.jenkins.io/doc/book/installing/)
- Jenkins User Handbook, [Installing Jenkins - Docker](https://www.jenkins.io/doc/book/installing/docker/)
- Jenkins User Handbook, [Initial Settings](https://www.jenkins.io/doc/book/installing/initial-settings/)
- Jenkins, [LTS Changelog](https://www.jenkins.io/changelog-stable/)
- Jenkins User Handbook, [Java Support Policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/)
