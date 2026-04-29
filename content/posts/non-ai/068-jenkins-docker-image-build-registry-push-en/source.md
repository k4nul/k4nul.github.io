---
layout: single
title: "Jenkins 08. Building Docker Images and Pushing to a Registry in Jenkins"
description: "A Jenkins Pipeline guide for Docker image builds, registry pushes, tag rules, credentials, and agent boundaries."
date: 2026-06-24 09:00:00 +0900
lang: en
translation_key: jenkins-docker-image-build-registry-push
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, docker, registry, image, pipeline]
author_profile: false
sidebar:
  nav: "sections"
search: true
permalink: /en/devops/jenkins-docker-image-build-registry-push/
---

## Summary

After learning Docker images, tags, digests, and registries, Jenkins automates that flow. A Jenkins Pipeline can check out source, build a Docker image, authenticate to a registry, and push the result.

The conclusion of this post is that image names and tags should not be accidental. Connect them explicitly to Git commit, Git tag, build number, and registry repository rules.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-04-24
- Document type: tutorial
- Test environment: verified against the author's Jenkins practice server. As of 2026-04-24, the unauthenticated login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`. The OS is Linux 22.04; agent details are not fixed in this post.
- Test version: the author's Jenkins practice server reported Jenkins 2.541.3 in the login response header on 2026-04-24. Documentation checks use the relevant official documents checked on 2026-04-24.
- Source level: Jenkins official documentation and Docker official documentation.
- Note: image signing, SBOM, and provenance are outside this post.

## Problem Definition

Common CI image build problems include:

- Every build is pushed only as `latest`.
- The Git commit that produced an image is not recorded.
- Registry credentials are written directly in shell scripts.
- Docker steps run on agents without access to a Docker daemon.

This post defines the minimum values to make explicit when connecting Docker build and push to Jenkins.

## Verified Facts

- According to Jenkins Using Docker with Pipeline documentation, combining Docker and Pipeline allows different container execution environments per stage.
  Evidence: [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- According to the same documentation, the Docker Pipeline plugin can create a new image from a repository `Dockerfile` using `docker.build()`.
  Evidence: [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- According to the same documentation, `push()` can publish Docker images to Docker Hub or a custom registry.
  Evidence: [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- According to the same documentation, `withRegistry()` can be used with a Jenkins credential ID for authenticated custom registries.
  Evidence: [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- According to Docker CLI documentation, `docker image push` uploads an image to a registry and can output a digest.
  Evidence: [docker image push](https://docs.docker.com/reference/cli/docker/image/push/)

Basic flow:

```groovy
node('docker') {
  checkout scm
  def image = docker.build("registry.example.com/team/app:${env.BUILD_NUMBER}")
  docker.withRegistry('https://registry.example.com', 'registry-credential-id') {
    image.push()
  }
}
```

## Directly Reproduced Results

- Direct reproduction: I verified the main commands and configuration flow on the author's Jenkins practice server. On 2026-04-24, the unauthenticated login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`.
- Documentation check result: Jenkins and Docker documentation were used to verify build, push, and registry credential concepts.
- Needs reproduction: after pushing to a real registry, verify that digest, image ID, Git commit, and Jenkins build number are connected in the operation record.

## Interpretation / Opinion

My judgment is that the most important Jenkins Docker build value is the image tag rule. `BUILD_NUMBER` is easy to trace inside Jenkins but does not directly identify Git history. Teams should decide whether to use short Git SHA, release tag, branch name, build number, or a combination.

A beginner-friendly rule might look like:

```text
registry.example.com/team/app:<git-short-sha>
registry.example.com/team/app:<release-tag>
registry.example.com/team/app:latest-staging
```

Operational records should include digest, not only tag. Tags can move, while digest identifies image content.

## Limits and Exceptions

This post does not compare how to provide Docker daemon access to agents, Docker-in-Docker, remote Docker hosts, Kaniko, or BuildKit.

Private registry authentication, TLS, credential rotation, image signing, SBOM, and vulnerability scanning should be handled as separate security and operations topics.

## References

- Jenkins User Handbook, [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- Docker Docs, [docker image build](https://docs.docker.com/reference/cli/docker/image/build/)
- Docker Docs, [docker image push](https://docs.docker.com/reference/cli/docker/image/push/)
