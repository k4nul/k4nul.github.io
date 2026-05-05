---
layout: single
title: "Rust Service 21. ConfigMap, Secret, env 주입 기준 정하기"
description: "Kubernetes에서 Rust API 설정값과 비밀값을 ConfigMap, Secret, env로 주입할 때의 책임 경계와 운영 절차를 정리한다."
date: 2027-02-09 09:00:00 +09:00
lang: ko
translation_key: rust-api-kubernetes-configmap-secret-env
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

Kubernetes에서 Rust API를 배포할 때 설정값과 비밀값은 둘 다 컨테이너 환경 변수로 들어올 수 있다. 하지만 저장 위치, 접근 권한, 회전 절차, 로그 노출 위험은 다르게 다뤄야 한다.

이 글에서는 일반 설정은 ConfigMap, 민감한 값은 Secret, 애플리케이션이 읽는 최종 인터페이스는 명시적 환경 변수로 두는 기준을 사용한다. 중요한 점은 Secret을 쓴다고 해서 자동으로 안전해지는 것이 아니라는 점이다. Secret 값의 생성, 접근 권한, 암호화, 회전, 배포 재시작까지 같이 설계해야 한다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: Kubernetes Deployment와 Service로 배포하기
- 다음 글: readiness/liveness probe와 resource limit 잡기
- 이번 글의 범위: 컨테이너 이미지 밖에서 설정을 주입하고, 비밀값을 코드와 이미지에 섞지 않는 최소 기준

## 문서 정보

- 작성일: 2026-05-05
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial | analysis
- 테스트 환경: 직접 클러스터 실행 테스트 없음. Kubernetes 공식 문서와 일반 manifest 예시를 기준으로 절차를 정리했다.
- 테스트 버전: Kubernetes 문서 기준. `kubectl`과 클러스터 버전은 고정하지 않았다.
- 출처 성격: 공식 문서

## 문제 정의

앞 글에서 Deployment와 Service로 Rust API Pod를 띄우는 최소 단위를 만들었다. 그 다음 문제는 이미지 안에 무엇을 넣고, 이미지 밖에서 무엇을 주입할지 나누는 것이다.

예를 들어 아래 값들은 모두 API 실행에 필요할 수 있지만 같은 성격이 아니다.

- `RUST_LOG`: 로그 레벨이다. 일반 설정이다.
- `APP_BIND_ADDR`: 앱이 바인딩할 주소다. 일반 설정이다.
- `DATABASE_URL`: 데이터베이스 인증 정보가 들어갈 수 있다. 비밀값으로 다뤄야 한다.
- `JWT_SIGNING_KEY`: 토큰 서명 키다. 비밀값이며 회전 절차가 필요하다.

이 값을 모두 Dockerfile의 `ENV`에 넣으면 이미지 재사용성이 떨어지고, 비밀값이 이미지 레이어나 레지스트리 권한 경계에 섞일 위험이 생긴다. 반대로 모든 값을 Secret에 넣으면 일반 설정의 변경 이력과 검토 흐름이 불필요하게 어두워진다. 이 글의 목표는 "어디에 넣을지"보다 "어떤 책임으로 관리할지"를 먼저 정하는 것이다.

## 확인한 사실

- Kubernetes 공식 문서는 ConfigMap을 비기밀 데이터를 키-값 쌍으로 저장하는 API 객체로 설명한다. ConfigMap은 컨테이너 이미지에서 환경별 설정을 분리하는 데 사용할 수 있다.
  근거: [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- Kubernetes 공식 문서는 Secret을 암호, 토큰, 키 같은 민감 데이터를 담기 위한 객체로 설명한다. 다만 기본 상태의 Secret 값은 API 서버의 기반 저장소인 etcd에 암호화되지 않은 형태로 저장될 수 있으므로, RBAC와 저장 시 암호화 설정 같은 추가 보호가 필요하다.
  근거: [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- ConfigMap은 환경 변수, 명령 인자, 볼륨 파일로 사용할 수 있다. ConfigMap을 환경 변수로 사용한 값은 자동으로 갱신되지 않으며, 변경 값을 반영하려면 Pod 재시작이 필요하다.
  근거: [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- Kubernetes는 `env`, `envFrom`, `configMapKeyRef`, `secretKeyRef` 같은 방식으로 컨테이너 환경 변수를 구성할 수 있다.
  근거: [Define Environment Variables for a Container](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/)

## 실습 기준

이 글에서는 애플리케이션 코드가 `std::env` 또는 설정 로더를 통해 최종 값을 읽는다고 가정한다. Rust 코드의 설정 파싱은 앞선 설정 글에서 다뤘고, 여기서는 Kubernetes manifest의 경계를 다룬다.

운영 기준은 다음처럼 잡는다.

| 값 | 저장 객체 | 주입 방식 | 운영 기준 |
| --- | --- | --- | --- |
| `RUST_LOG` | ConfigMap | 명시적 `env` | 값 변경 시 배포 재시작으로 반영 |
| `APP_BIND_ADDR` | ConfigMap | 명시적 `env` | 이미지 기본값보다 manifest 값을 우선 |
| `APP_ENV` | ConfigMap | 명시적 `env` | `prod`, `staging` 같은 환경 이름만 저장 |
| `DATABASE_URL` | Secret | 명시적 `env` | 로그 출력 금지, 회전 시 Pod 재시작 |
| `JWT_SIGNING_KEY` | Secret | 명시적 `env` | 키 회전 절차와 이전 키 허용 기간 문서화 |

`envFrom`은 짧고 편하지만 이름 충돌을 놓치기 쉽다. 서비스의 핵심 설정은 아래처럼 어떤 키가 어떤 환경 변수로 들어가는지 명시하는 편이 운영 리뷰에 유리하다.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: rust-api-config
  namespace: rust-api
data:
  RUST_LOG: info
  APP_BIND_ADDR: 0.0.0.0:8080
  APP_ENV: production
---
apiVersion: v1
kind: Secret
metadata:
  name: rust-api-secret
  namespace: rust-api
type: Opaque
stringData:
  DATABASE_URL: postgres://app:change-me@example-postgres:5432/app
  JWT_SIGNING_KEY: replace-with-a-real-rotated-key
```

위 예시는 구조 설명용이다. 실제 비밀값을 Git에 커밋하면 안 된다. 운영에서는 Sealed Secrets, External Secrets, 클라우드 secret manager, GitOps secret 암호화 같은 별도 흐름을 사용해야 한다.

Deployment에서는 값의 출처를 명시한다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rust-api
  namespace: rust-api
spec:
  template:
    spec:
      containers:
        - name: rust-api
          image: ghcr.io/example/rust-api:2027.02.09
          ports:
            - containerPort: 8080
          env:
            - name: RUST_LOG
              valueFrom:
                configMapKeyRef:
                  name: rust-api-config
                  key: RUST_LOG
            - name: APP_BIND_ADDR
              valueFrom:
                configMapKeyRef:
                  name: rust-api-config
                  key: APP_BIND_ADDR
            - name: APP_ENV
              valueFrom:
                configMapKeyRef:
                  name: rust-api-config
                  key: APP_ENV
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: rust-api-secret
                  key: DATABASE_URL
            - name: JWT_SIGNING_KEY
              valueFrom:
                secretKeyRef:
                  name: rust-api-secret
                  key: JWT_SIGNING_KEY
```

적용과 확인은 아래 흐름으로 나눈다.

```bash
kubectl apply -f k8s/config.yaml
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/rust-api -n rust-api
kubectl describe deployment/rust-api -n rust-api
```

ConfigMap이나 Secret을 바꾼 뒤 환경 변수로 주입된 값을 반영하려면 Pod 재시작을 운영 절차에 포함한다.

```bash
kubectl apply -f k8s/config.yaml
kubectl rollout restart deployment/rust-api -n rust-api
kubectl rollout status deployment/rust-api -n rust-api
```

Secret 확인 명령은 조심해서 다룬다. 운영 문서에는 Secret의 실제 값을 출력하는 명령을 기본 절차로 넣지 않는다.

```bash
kubectl get secret rust-api-secret -n rust-api
kubectl describe secret rust-api-secret -n rust-api
```

## 관찰 결과

직접 클러스터에서 실행한 결과는 이 글에 포함하지 않았다. 대신 검증 시 확인해야 할 관찰 지점은 다음과 같다.

- ConfigMap 또는 Secret 이름이 틀리면 Pod 생성 또는 컨테이너 시작 단계에서 이벤트가 남아야 한다.
- 필수 키가 없으면 컨테이너가 실행되지 않거나 애플리케이션 시작 시 설정 검증에서 실패해야 한다.
- 환경 변수로 주입한 ConfigMap 값은 ConfigMap을 수정해도 이미 실행 중인 컨테이너에 자동 반영되지 않는다는 전제로 배포 재시작을 수행해야 한다.
- Secret 값을 로그에 출력하지 않아야 한다. 특히 설정 덤프, panic 메시지, tracing field에 민감 값이 섞이지 않는지 확인해야 한다.

## 해석 / 의견

ConfigMap과 Secret의 차이는 "Kubernetes 객체 이름"보다 운영 리뷰 방식에서 더 크게 드러난다. ConfigMap 변경은 비교적 공개적인 설정 변경으로 검토할 수 있지만, Secret 변경은 누가 값을 만들고, 어디에 저장하고, 어떻게 회전하며, 이전 값이 언제 폐기되는지까지 따라간다.

Rust API 입장에서는 둘 다 환경 변수일 수 있다. 그래서 코드 안에서는 값의 출처보다 값의 의미를 기준으로 검증하는 편이 낫다. 예를 들어 `DATABASE_URL`이 비어 있으면 시작 실패, `RUST_LOG`가 비어 있으면 기본값 사용처럼 정책을 분리한다.

`envFrom`은 작은 데모에서는 편하지만 운영 글에서는 명시적 `env`를 우선한다. 이름 충돌, 불필요한 키 노출, 리뷰 난이도 때문이다. 설정 키가 많아졌다면 무조건 `envFrom`으로 숨기기보다 설정 구조 자체가 커졌는지 먼저 봐야 한다.

## 한계와 예외

- 이 글은 Kubernetes 기본 객체 기준이다. 특정 클라우드 secret manager, Vault, External Secrets Operator, Sealed Secrets의 세부 동작은 범위 밖이다.
- Secret을 사용해도 RBAC, etcd 암호화, 감사 로그, secret 회전 정책이 없으면 충분한 보호라고 보기 어렵다.
- 파일 볼륨으로 주입한 ConfigMap/Secret은 환경 변수 주입과 갱신 동작이 다르다. 이 글의 기본 예시는 환경 변수 주입에 맞췄다.
- 실제 운영에서는 비밀값을 manifest 평문으로 저장하지 않는다. 예시는 구조 설명용이다.

## 참고자료

- [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Define Environment Variables for a Container](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/)
- [Distribute Credentials Securely Using Secrets](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/)

## 변경 이력

- 2026-05-05: ConfigMap, Secret, env 주입 기준과 검증 절차를 공식 문서 기준으로 재작성.
