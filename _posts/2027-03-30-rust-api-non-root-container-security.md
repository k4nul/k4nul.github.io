---
layout: single
title: "Rust Service 28. non-root container와 최소 권한 실행 기준"
description: "Rust API 컨테이너를 non-root로 실행하고 readOnlyRootFilesystem, allowPrivilegeEscalation, capabilities drop 같은 최소 권한 기준을 정리한다."
date: 2027-03-30 09:00:00 +09:00
lang: ko
translation_key: rust-api-non-root-container-security
section: development
topic_key: rust
featured: false
track: rust
repo:
demo:
references:
categories: Rust
tags: [rust, axum, api, production, devops]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Rust API가 작은 바이너리 하나로 실행된다면 컨테이너 안에서 root가 필요한 이유를 먼저 의심해야 한다. non-root 실행은 보안 장식이 아니라 컨테이너 탈출이나 취약점 악용 때 피해 범위를 줄이는 기본 경계다.

이 글에서는 Dockerfile의 `USER`, Kubernetes `securityContext`, writable directory, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, Linux capabilities drop을 함께 맞춘다. 한 곳만 바꾸면 운영에서 예상하지 못한 파일 권한 오류나 admission 거부를 만날 수 있다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: 장애를 일부러 만들고 describe, events, logs로 추적하기
- 다음 글: Kubernetes RBAC를 서비스 운영 관점에서 다시 보기
- 이번 글의 범위: Rust API 컨테이너가 root 권한 없이 실행되도록 이미지와 Pod security context를 맞추는 최소 기준

## 문서 정보

- 작성일: 2026-05-05
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial | analysis
- 테스트 환경: 직접 클러스터 실행 테스트 없음. Docker와 Kubernetes 공식 문서, 일반 manifest 예시를 기준으로 정리했다.
- 테스트 버전: Dockerfile reference와 Kubernetes 문서 기준. Docker Engine, container runtime, Kubernetes 버전은 고정하지 않았다.
- 출처 성격: 공식 문서

## 문제 정의

컨테이너는 격리되어 있지만, 컨테이너 안의 root가 아무 의미 없는 것은 아니다. 잘못된 volume mount, 과도한 Linux capabilities, writable root filesystem, privilege escalation 허용이 겹치면 작은 취약점의 영향 범위가 커진다.

Rust API는 보통 아래 조건을 만족할 수 있다.

- 낮은 포트가 아닌 `8080` 같은 unprivileged port를 사용한다.
- 실행에 shell, package manager, compiler가 필요하지 않다.
- 로그는 파일이 아니라 stdout/stderr로 남긴다.
- 임시 파일이 필요하다면 `/tmp` 같은 제한된 writable path만 쓴다.

따라서 기본값은 root 실행이 아니라 non-root 실행이어야 한다.

## 확인한 사실

- Dockerfile reference는 `USER` instruction이 현재 stage의 기본 사용자와 그룹을 설정하고, 이후 `RUN` 및 runtime의 `ENTRYPOINT`, `CMD`에 적용된다고 설명한다.
  근거: [Dockerfile USER](https://docs.docker.com/reference/dockerfile/#user)
- Kubernetes security context 문서는 `runAsUser`, `runAsGroup`, `fsGroup`, `allowPrivilegeEscalation`, `readOnlyRootFilesystem` 같은 필드로 Pod 또는 container 보안 설정을 제어할 수 있음을 설명한다.
  근거: [Kubernetes Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
- Kubernetes Pod Security Standards의 Restricted profile은 privilege escalation을 허용하지 않아야 하며, container가 non-root user로 실행되어야 한다고 정의한다.
  근거: [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- Kubernetes Linux kernel security constraints 문서는 seccomp, AppArmor, SELinux, Linux capabilities 같은 커널 보안 경계를 설명한다. 이 글은 그중 capabilities와 seccomp 기본 경계만 다룬다.
  근거: [Linux kernel security constraints for Pods and containers](https://kubernetes.io/docs/concepts/security/linux-kernel-security-constraints/)

## 실습 기준

Dockerfile에서는 숫자 UID/GID를 명시한다. 배포 환경에서 `/etc/passwd` 이름 해석에 기대지 않기 위해서다.

```dockerfile
FROM gcr.io/distroless/cc-debian12:nonroot
WORKDIR /app
COPY --chown=65532:65532 target/release/rust-api /app/rust-api
USER 65532:65532
EXPOSE 8080
ENTRYPOINT ["/app/rust-api"]
```

이미지 안에서 쓸 수 있는 경로도 제한한다. 애플리케이션이 파일을 써야 한다면 root filesystem 전체가 아니라 명시한 volume에만 쓴다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rust-api
  namespace: rust-api
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 65532
        runAsGroup: 65532
        fsGroup: 65532
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: rust-api
          image: ghcr.io/example/rust-api:2027.03.30
          ports:
            - containerPort: 8080
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
```

검증 순서는 image와 Pod를 나눠 본다.

```bash
docker image inspect ghcr.io/example/rust-api:2027.03.30
```

```bash
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/rust-api -n rust-api --timeout=180s
kubectl get pod -n rust-api -l app=rust-api
kubectl describe pod -n rust-api -l app=rust-api
```

debug shell이 없는 distroless image에서는 `kubectl exec`로 `id`를 확인하지 못할 수 있다. 이 경우 ephemeral container나 별도 debug image가 필요하지만, 운영에서 main container에 shell을 넣기 위한 이유가 되지는 않는다.

## 관찰 결과

직접 실행 결과는 포함하지 않았다. 실제 검증 시 아래 항목을 기록한다.

| 확인 항목 | 기대 결과 |
| --- | --- |
| 이미지 사용자 | Dockerfile 또는 image metadata에 root가 아닌 UID/GID가 설정되어 있다 |
| Pod security context | `runAsNonRoot`, `runAsUser`, `runAsGroup`이 명시되어 있다 |
| privilege escalation | `allowPrivilegeEscalation: false`다 |
| capabilities | 기본 capabilities를 모두 drop하고 필요한 것만 예외로 추가한다 |
| root filesystem | `readOnlyRootFilesystem: true`이며 필요한 writable path만 volume으로 연다 |
| 로그 | 파일이 아니라 stdout/stderr로 출력된다 |
| port | 80이 아니라 8080 같은 unprivileged port를 사용한다 |

## 해석 / 의견

non-root 실행은 단독으로 완성되는 보안이 아니다. 하지만 다른 방어선이 실패했을 때 피해 범위를 줄이는 기본 경계다. 특히 static에 가까운 Rust API는 root 권한이 필요한 경우가 많지 않으므로, root 실행은 예외로 다루는 편이 낫다.

`readOnlyRootFilesystem`을 켜면 숨겨진 쓰기 경로가 드러난다. 앱이 `/app`, `/var`, 현재 작업 디렉터리에 cache나 임시 파일을 쓰고 있었다면 이 시점에 실패한다. 이 실패는 귀찮지만 좋은 신호다. 쓰기 경로를 `/tmp`나 명시된 volume으로 옮길 기회이기 때문이다.

Linux capabilities는 "root가 아니면 끝"이 아니라는 점을 보여준다. 필요 없는 capability는 drop하고, 정말 필요한 capability만 이유와 함께 추가해야 한다. 일반 HTTP API가 8080 포트에서 뜬다면 대개 추가 capability가 필요 없다.

## 한계와 예외

- 이 글은 Linux container 기준이다. Windows container의 user와 security context 의미는 다르다.
- distroless image, scratch image, Alpine image는 사용자 생성과 파일 소유권 처리 방식이 다를 수 있다.
- `fsGroup`은 volume 소유권과 성능에 영향을 줄 수 있으므로 큰 volume에서는 별도 검토가 필요하다.
- service mesh sidecar, APM agent, debug sidecar가 추가되면 Pod 전체 security context를 다시 검토해야 한다.

## 참고자료

- [Dockerfile USER](https://docs.docker.com/reference/dockerfile/#user)
- [Kubernetes Security Context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Linux kernel security constraints for Pods and containers](https://kubernetes.io/docs/concepts/security/linux-kernel-security-constraints/)
- [Kubernetes Security Context API](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.34/#securitycontext-v1-core)

## 변경 이력

- 2026-05-05: non-root 실행, securityContext, read-only root filesystem, capabilities 기준을 공식 문서 기준으로 재작성.
