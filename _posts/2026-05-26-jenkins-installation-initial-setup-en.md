---
layout: single
title: "Jenkins 02. Jenkins Installation and Initial Setup"
description: "A Docker-based Jenkins setup walkthrough covering the initial password, plugins, first admin user, Jenkins URL, validation, cleanup, and common failures."
date: 2026-05-26 09:00:00 +09:00
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

## What You Can Do With This Post

- Start a Jenkins controller with Docker while preserving `/var/jenkins_home` in a named volume.
- Read the initial administrator password from container logs or `/var/jenkins_home/secrets/initialAdminPassword`.
- Open `http://localhost:8080` and complete the setup wizard.
- Choose between suggested plugins and selected plugins, then create the first administrator account and Jenkins URL.
- Restart Jenkins and verify that configuration persists.
- Check the first places to look when port 8080, volume permissions, Java requirements, plugin downloads, or the initial password file fail.

## Prerequisites

- Runtime: local Linux, macOS, Windows WSL, or Docker Desktop with Docker available
- Shell: Bash-style examples
- Permissions: the current user can run `docker`. On Linux, use `sudo docker ...` if your user is not in the Docker group.
- Port: host port `8080` should be free. If it is not, change `8080:8080` to something like `18080:8080`.
- Scope: this is a local practice setup. For production, review the production caveats later in this post.

## Expected Result

After the walkthrough:

- the `jenkins` container is running;
- the `jenkins_home` Docker volume is mounted at `/var/jenkins_home`;
- `http://localhost:8080` opens the Jenkins UI;
- the first admin user and Jenkins URL are configured;
- Jenkins settings survive a container restart.

## Quick Setup Steps

```bash
docker volume create jenkins_home
```

```bash
docker run \
  --name jenkins \
  --detach \
  --publish 8080:8080 \
  --publish 50000:50000 \
  --volume jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

Watch the logs while Jenkins starts.

```bash
docker logs -f jenkins
```

Read the initial administrator password.

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

You can also check the `docker logs jenkins` output around `Please use the following password to proceed to installation`.

Open Jenkins in a browser.

```text
http://localhost:8080
```

Complete the setup wizard in this order.

1. Paste the initial administrator password on the `Unlock Jenkins` screen.
2. For beginner practice, choose `Install suggested plugins` on the `Customize Jenkins` screen.
3. For an operations-oriented setup, choose `Select plugins to install` and record each required plugin with a reason.
4. Create a real first administrator account on the `Create First Admin User` screen, not a disposable temporary account.
5. On `Instance Configuration`, use `http://localhost:8080/` for local practice. For production, decide the externally reachable URL and reverse proxy boundary first.

## Verify Normal Operation

Check that the container is running.

```bash
docker ps --filter name=jenkins
```

Check that Jenkins returns an HTTP response.

```bash
curl -I http://localhost:8080/login
```

Check the mounted Docker volume.

{% raw %}
```bash
docker inspect jenkins --format '{{ range .Mounts }}{{ .Name }} -> {{ .Destination }}{{ println }}{{ end }}'
```
{% endraw %}

Restart Jenkins and verify that configuration persists.

```bash
docker restart jenkins
docker exec jenkins test -f /var/jenkins_home/config.xml && echo "JENKINS_HOME persisted"
```

If the command prints `JENKINS_HOME persisted`, the Jenkins home directory is preserved in the Docker volume.

## Example: Verify a First Build With a Jenkinsfile

This minimal example verifies that Jenkins can accept and run a Pipeline job after setup. It is a practice controller check, not a production pipeline.

Create `Jenkinsfile` at the repository root.

```groovy
pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                echo 'Hello, Jenkins'
            }
        }
    }
}
```

In the UI, choose `New Item` -> `Pipeline`, then use either `Pipeline script from SCM` or the practice-only `Pipeline script` option. After the build, check `Console Output`.

Example output:

```text
[Pipeline] echo
Hello, Jenkins
Finished: SUCCESS
```

`Finished: SUCCESS` means the controller accepted the job, parsed the pipeline, and ran the stage. For production, avoid treating controller-side builds as the default. Design agent separation and credential scope separately.

## Cleanup

Removing only the container leaves the volume intact.

```bash
docker stop jenkins
docker rm jenkins
```

Remove the volume only when you intentionally want to delete the practice data. Do not run this command for a production or reusable practice controller.

```bash
docker volume rm jenkins_home
```

## Common Failures

### Port 8080 Is Already In Use

Symptom: Docker reports `Bind for 0.0.0.0:8080 failed`, or the browser opens another service.

Example error message:

```text
Bind for 0.0.0.0:8080 failed: port is already allocated
```

Check:

{% raw %}
```bash
docker ps --format 'table {{.Names}}\t{{.Ports}}'
```
{% endraw %}

On Linux/macOS, also check which host process owns port 8080.

```bash
lsof -i :8080
```

Fix: use a different host port.

```bash
docker run \
  --name jenkins \
  --detach \
  --publish 18080:8080 \
  --publish 50000:50000 \
  --volume jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

The browser URL becomes `http://localhost:18080`.

### Volume Permission Problems

Symptom: Jenkins does not start, or logs say it cannot write to `/var/jenkins_home`.

Check:

```bash
docker logs jenkins
```

Fix: for beginner practice, prefer a named volume over a host bind mount. If you must bind a host directory, set ownership and permissions according to your operations policy. Do not use `chmod 777` as a default fix.

### Java Version Problems

Symptom: a non-Docker Jenkins installation fails to start because the Java runtime is unsupported.

Check:

```bash
java -version
```

Fix: check the Java Support Policy for the exact Jenkins LTS you plan to run. For practice with the official `jenkins/jenkins:lts` Docker image, the Java runtime inside the image is separate from the host Java version.

### Plugin Installation Fails

Symptom: plugin downloads fail or the setup wizard appears stuck.

Check:

```bash
docker logs jenkins
```

Fix: check network, proxy, DNS, and update center access. For production, do not install every suggested plugin by habit. Record the plugin inventory and manage it reproducibly.

### Initial Password File Is Missing

Symptom: `/var/jenkins_home/secrets/initialAdminPassword` does not exist.

Check:

```bash
docker logs jenkins
docker exec jenkins ls -la /var/jenkins_home/secrets
```

Fix: if Jenkins is still initializing, wait and check again. If you are reusing an existing volume that already completed the setup wizard, the first-run password flow may no longer apply. Delete both the container and volume only when you intentionally want to reset a practice environment.

## Document Information

- Written on: 2026-04-24
- Verification date: 2026-06-05
- Document type: tutorial
- Test environment: based on the author's Jenkins practice server response headers checked on 2026-04-24 and the official Jenkins Docker installation documentation checked on 2026-06-05. The OS is Linux 22.04; agent details are not fixed in this post.
- Test version: the author's Jenkins practice server reported Jenkins 2.541.3 in the login response header on 2026-04-24. Java requirements and Docker setup flow are based on Jenkins official documentation checked on 2026-06-05.
- Source level: Jenkins official documentation and Jenkins LTS changelog.
- Note: the Docker commands in this post are for local practice. Before production use, recheck Jenkins LTS, Java requirements, plugin compatibility, and backup/restore procedures.

## Problem Definition

First Jenkins installations often fail in predictable ways:

- The controller state location is ignored.
- Java requirements are checked only after installation.
- Suggested plugins are installed without recording why they are needed.
- Initial admin account, URL, and port settings are left as temporary values.

This post starts with a Docker-based first installation flow, then separates the decisions that should be made before a production installation.

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

- Direct reproduction: on 2026-04-24, the author's Jenkins practice server login response reported `X-Jenkins: 2.541.3` and `Server: Jetty(12.1.5)`.
- Verified through documentation: as of 2026-06-05, Jenkins Docker installation documentation describes `/var/jenkins_home` volume mapping, initial administrator password retrieval, and the setup wizard flow.
- Not rerun in this edit: I did not start a fresh Docker container and complete the setup wizard in the current workspace. The commands above are a local practice flow based on official documentation and the earlier practice environment.

## Interpretation / Opinion

My judgment is that the first value to stabilize is `JENKINS_HOME`. Jenkins is not just an executable. It is a server that accumulates controller state over time. Losing that directory can mean losing job configuration, plugin state, build history, and credentials-related state.

For beginner practice, Docker is a good path because it connects directly to the image, container, and volume concepts from the Docker posts. For operations, the installation method is less important than these questions:

- Does the Java version match the Jenkins LTS requirement?
- Is the controller data directory placed somewhere that can be backed up?
- Is the plugin list recorded with reasons?
- Are Jenkins URL, HTTP/HTTPS, and reverse proxy boundaries clear?
- Will builds run on the controller or on agents?

After installation, it is safer to verify controller persistence, plugin reproducibility, and non-temporary admin settings before writing a complex Pipeline.

## Production Caveats

Do not promote the local Docker practice setup directly into production. At minimum, verify these items separately:

- TLS and reverse proxy: do not expose the Jenkins HTTP port directly to the internet. Align Jenkins with your authentication, proxy, and TLS boundary.
- Backup and restore: back up `JENKINS_HOME`, then rehearse restore.
- Credential management: do not leave secrets in code, logs, or job descriptions.
- Controller and agent separation: do not make controller-side builds the default operating model.
- Plugin management: record why each plugin exists, which version is installed, how updates are reviewed, and when a plugin should be removed.
- Authorization: do not keep operating with the first administrator account. Define roles or an authorization strategy.
- Upgrade checks: Jenkins LTS, Java requirements, and plugin compatibility can change after publication, so recheck them before production changes.

## Limits and Exceptions

This post verified the Jenkins installation flow in the author's practice environment. Errors specific to Windows, Linux distributions, Docker Desktop, or WSL still need environment-specific checks.

Jenkins LTS and Java requirements are date-sensitive. This post is based on documents checked on 2026-04-24.

Production environments should separately verify TLS, reverse proxy, backup, restore, plugin pinning, controller/agent separation, and account authorization policies.

## Related Posts

- [DevOps Operations Flow](/en/development/devops/)
- [What Jenkins Is and Why It Is Still Used](/en/devops/jenkins-what-and-why-still-used/)
- [PR/MR Collaboration Flow and Review Criteria](/en/devops/git-pr-mr-collaboration-review/)
- [Docker registry push and image management](/en/devops/docker-registry-push-and-image-management/)

## References

- Jenkins User Handbook, [Installing Jenkins](https://www.jenkins.io/doc/book/installing/)
- Jenkins User Handbook, [Installing Jenkins - Docker](https://www.jenkins.io/doc/book/installing/docker/)
- Jenkins User Handbook, [Initial Settings](https://www.jenkins.io/doc/book/installing/initial-settings/)
- Jenkins, [LTS Changelog](https://www.jenkins.io/changelog-stable/)
- Jenkins User Handbook, [Java Support Policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/)
