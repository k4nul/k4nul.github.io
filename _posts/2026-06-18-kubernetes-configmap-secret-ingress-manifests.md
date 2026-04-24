---
layout: single
title: "K8S 07. 실무형 manifest 작성 ConfigMap, Secret, Ingress"
description: "Kubernetes manifest에서 설정, 민감 정보, 외부 HTTP 진입점을 분리해서 작성하는 기본 흐름을 정리한 글."
date: 2026-06-18 09:00:00 +0900
lang: ko
translation_key: kubernetes-configmap-secret-ingress-manifests
section: development
topic_key: devops
categories: DevOps
tags: [kubernetes, configmap, secret, ingress, manifest]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

앞 글에서 Deployment와 Service를 만들었다면, 다음 단계는 application 설정을 image 밖으로 빼고, 민감 정보를 코드와 분리하고, HTTP 요청을 Service까지 연결하는 것이다. Kubernetes에서는 이 역할을 주로 `ConfigMap`, `Secret`, `Ingress`로 나누어 표현한다.

이 글의 결론은 세 object를 "추가 YAML"로 외우기보다, 실행 설정과 보안 경계와 외부 진입점을 분리하는 장치로 이해해야 한다는 것이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: tutorial
- 테스트 환경: 작성자 별도 실습 환경에서 실행 확인. OS, 노드 사양, 클러스터 구성은 이 글에 고정하지 않았다.
- 테스트 버전: Kubernetes 공식 문서 2026-04-24 확인본. 문서 사이트는 v1.36 링크를 표시했다.
- 출처 등급: Kubernetes 공식 문서를 사용했다.
- 비고: Secret 암호화, 외부 Secret 관리 도구, TLS 인증서 자동화는 별도 운영 주제다.

## 문제 정의

처음 manifest를 작성할 때 자주 생기는 문제는 아래와 같다.

- 환경별 설정값을 container image 안에 넣는다.
- password나 token을 Git 저장소에 평문으로 남긴다.
- Service를 만들면 곧바로 외부 HTTP domain으로 접근할 수 있다고 오해한다.
- Ingress object와 Ingress controller를 같은 것으로 본다.

## 확인된 사실

- Kubernetes ConfigMap 문서 기준으로 ConfigMap은 confidential하지 않은 데이터를 key-value 형태로 저장하는 API object다.
  근거: [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- Kubernetes Secret 문서 기준으로 Secret은 password, token, key 같은 소량의 민감 정보를 담기 위한 object다.
  근거: [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- Kubernetes Secret 문서 기준으로 Secret과 ConfigMap은 비슷하게 동작하지만 Secret에는 추가 보호가 적용된다. 다만 접근 권한 설정이 Secret 데이터 접근 범위에 직접 영향을 준다.
  근거: [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- Kubernetes Ingress 문서 기준으로 Ingress는 cluster 안 Service로 들어오는 외부 HTTP/HTTPS 접근 규칙을 관리한다.
  근거: [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- Kubernetes Ingress 문서 기준으로 Kubernetes 프로젝트는 Ingress 대신 Gateway API 사용을 권장하며, Ingress API는 frozen 상태로 더 이상의 기능 변경이나 업데이트가 진행되지 않는다고 설명한다.
  근거: [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- Kubernetes Ingress Controllers 문서 기준으로 Ingress가 동작하려면 cluster 안에 Ingress controller가 있어야 한다.
  근거: [Ingress Controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)

설정을 분리한 예시는 아래와 같다.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_MODE: production
  LOG_LEVEL: info
```

민감 정보는 ConfigMap이 아니라 Secret으로 분리한다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  DB_PASSWORD: change-me
```

Deployment에서는 두 object를 환경 변수로 연결할 수 있다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
        - name: app
          image: example/app:1.0.0
          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: app-secret
```

Ingress는 외부 HTTP 요청을 Service로 보내는 규칙을 선언한다.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app
spec:
  ingressClassName: nginx
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-svc
                port:
                  number: 80
```

## 직접 재현한 결과

- 직접 재현함: 작성자 실습 환경에서 이 글의 주요 명령과 설정 흐름을 확인했다.
- 확인한 결과: 공식 문서 기준으로 ConfigMap, Secret, Ingress, Ingress controller의 역할을 구분했다.
- 직접 확인 항목: `kubectl apply -f`, `kubectl get configmap,secret,ingress`, `kubectl describe ingress`, Ingress controller event를 확인했다.

## 해석 / 의견

내 기준에서 ConfigMap과 Secret의 가장 중요한 차이는 "값의 성격"이다. 공개되어도 치명적이지 않은 실행 설정은 ConfigMap에 두고, password, token, private key처럼 노출되면 안 되는 값은 Secret으로 분리해야 한다.

다만 Secret을 썼다는 사실만으로 보안이 끝나지는 않는다. Secret 접근 권한, namespace 경계, audit, encryption at rest, 배포 pipeline에서의 masking까지 같이 봐야 한다. 특히 예제용 `stringData` 값은 실제 운영 값이 아니라 흐름을 보여주기 위한 자리표시자다.

Ingress는 LoadBalancer나 reverse proxy 그 자체가 아니라 "어떤 host와 path를 어떤 Service로 보낼지" 선언하는 object로 보는 편이 이해하기 쉽다. 실제 traffic 처리는 Ingress controller가 맡기 때문에, controller가 없거나 `ingressClassName`이 맞지 않으면 Ingress object만 있어도 요청은 들어오지 않는다.

신규 cluster나 장기 운영 설계에서는 Ingress만 기본값으로 두기보다 Gateway API도 함께 검토해야 한다. 이 글의 Ingress 예시는 기존 cluster와 초급 학습에서 여전히 자주 만나는 object를 읽기 위한 최소 설명이다.

## 한계와 예외

작성자 실습 환경에서 기본 manifest와 Ingress object 확인 흐름을 검증했다. DNS, TLS, certificate manager, cloud load balancer 연동은 별도 운영 검증이 필요하다. 또한 Secret의 encryption at rest 설정, external secrets, sealed secrets 같은 보완 도구도 다루지 않았다.

controller별 annotation은 구현체마다 다르다. NGINX Ingress, Traefik, HAProxy, cloud provider controller를 사용할 때는 해당 controller 문서를 별도로 확인해야 한다.

Kubernetes Ingress API는 stable이지만 frozen 상태다. 새로운 HTTP traffic routing 설계에서는 Gateway API가 더 적절할 수 있으며, 이 글의 예시는 Gateway API 비교나 migration guide가 아니다.

## 참고자료

- Kubernetes Docs, [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- Kubernetes Docs, [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- Kubernetes Docs, [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- Kubernetes Docs, [Ingress Controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)
