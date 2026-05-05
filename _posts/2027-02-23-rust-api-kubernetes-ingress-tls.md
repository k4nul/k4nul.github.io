---
layout: single
title: "Rust Service 23. Ingress로 외부 접근 열고 TLS 경계 이해하기"
description: "Kubernetes Ingress로 Rust API 외부 접근을 열 때 host/path routing, Ingress Controller, TLS 종료 경계를 구분한다."
date: 2027-02-23 09:00:00 +09:00
lang: ko
translation_key: rust-api-kubernetes-ingress-tls
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

Ingress는 Rust 애플리케이션 라우터가 아니다. 클러스터 밖에서 들어온 HTTP/HTTPS 요청을 클러스터 안의 Service로 연결하는 Kubernetes API 객체다.

Ingress를 쓸 때는 manifest만으로 충분하지 않다. 실제 트래픽을 처리하는 Ingress Controller가 필요하고, TLS가 어디서 종료되는지, 백엔드 Pod로 어떤 헤더가 전달되는지, 인증과 health check가 어느 경계에서 동작하는지 기록해야 한다.

## 커리큘럼 위치

- 시리즈: Rust Service to Production
- 이전 글: readiness/liveness probe와 resource limit 잡기
- 다음 글: rollout, rollback, 장애 대응 runbook 만들기
- 이번 글의 범위: Service 앞에 HTTP 외부 접근 경계를 만들고 TLS 종료 위치를 문서화하는 최소 기준

## 문서 정보

- 작성일: 2026-05-05
- 검증 기준일: 2026-05-05
- 문서 성격: tutorial | analysis
- 테스트 환경: 직접 클러스터 실행 테스트 없음. Kubernetes 공식 문서와 일반 manifest 예시를 기준으로 절차를 정리했다.
- 테스트 버전: Kubernetes 문서 기준. Ingress Controller 구현체와 클러스터 버전은 고정하지 않았다.
- 출처 성격: 공식 문서

## 문제 정의

Service는 클러스터 내부에서 Pod 집합을 안정적인 네트워크 대상으로 묶는다. 그러나 사용자가 브라우저나 외부 클라이언트에서 `https://api.example.com`으로 접근하려면 Service만으로는 부족하다.

Ingress는 이 외부 HTTP 경계를 표현한다. 하지만 Ingress 객체는 선언일 뿐이다. 실제 동작은 NGINX Ingress Controller, Traefik, HAProxy, 클라우드 로드 밸런서 컨트롤러 같은 구현체가 담당한다. 따라서 이 글에서는 Kubernetes Ingress의 공통 구조와 TLS 경계를 먼저 잡고, 컨트롤러별 annotation은 별도 운영 문서로 분리한다.

## 확인한 사실

- Kubernetes 공식 문서는 Ingress를 클러스터 안의 Service로 HTTP와 HTTPS 경로를 노출하는 API 객체로 설명한다.
  근거: [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- Kubernetes 공식 문서는 Ingress가 동작하려면 Ingress Controller가 필요하다고 설명한다.
  근거: [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- Kubernetes 공식 문서는 Ingress가 frozen 상태이며, 새로운 기능은 Gateway API를 보라고 안내한다. 따라서 새 설계에서는 Gateway API 검토도 함께 남기는 것이 좋다.
  근거: [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- Kubernetes Secret 문서는 `kubernetes.io/tls` 타입 Secret을 TLS 인증서와 개인 키 저장에 사용할 수 있다고 설명한다.
  근거: [Kubernetes TLS Secrets](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets)

## 실습 기준

앞 글의 Service가 아래처럼 있다고 가정한다.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: rust-api
  namespace: rust-api
spec:
  type: ClusterIP
  selector:
    app: rust-api
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

Ingress는 이 Service 앞에 HTTP routing 규칙을 둔다.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rust-api
  namespace: rust-api
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
      secretName: rust-api-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: rust-api
                port:
                  number: 80
```

이 manifest에서 봐야 할 경계는 세 가지다.

| 항목 | 의미 | 운영 확인 |
| --- | --- | --- |
| `ingressClassName` | 어떤 Ingress Controller가 처리할지 지정 | 클러스터에 해당 controller가 설치되어 있는지 확인 |
| `rules.host` | 어떤 Host 헤더를 라우팅할지 지정 | DNS 또는 테스트용 `--resolve` 설정 확인 |
| `tls.secretName` | TLS 인증서와 개인 키를 담은 Secret | 인증서 CN/SAN, 만료일, 키 보호 절차 확인 |

테스트용 TLS Secret은 아래처럼 만들 수 있다. 실제 운영 개인 키는 Git에 커밋하지 않는다.

```bash
kubectl create secret tls rust-api-tls \
  --cert=./tls.crt \
  --key=./tls.key \
  -n rust-api
```

적용과 확인 흐름은 Ingress 객체, controller, backend Service를 분리해서 본다.

```bash
kubectl apply -f k8s/ingress.yaml
kubectl get ingress -n rust-api
kubectl describe ingress rust-api -n rust-api
kubectl get service rust-api -n rust-api
kubectl get endpointslice -n rust-api -l kubernetes.io/service-name=rust-api
```

Ingress 주소가 `203.0.113.10`이라고 가정하면, DNS 반영 전에는 아래처럼 Host와 IP를 고정해서 확인할 수 있다.

```bash
curl --resolve api.example.com:443:203.0.113.10 https://api.example.com/health
```

자체 서명 인증서를 쓰는 로컬 실습에서는 TLS 검증이 실패할 수 있다. 그 경우 `-k`로 우회할 수 있지만, 운영 검증 절차에는 넣지 않는다.

```bash
curl -k --resolve api.example.com:443:203.0.113.10 https://api.example.com/health
```

## 관찰 결과

직접 실행 결과는 포함하지 않았다. 실제 검증 시에는 아래 관찰 지점을 분리해서 기록한다.

| 상황 | 기대되는 관찰 |
| --- | --- |
| Ingress Controller 없음 | Ingress 객체는 있어도 외부 주소나 실제 routing이 준비되지 않을 수 있다 |
| `rules.host` 불일치 | IP로 직접 접근하면 기대한 backend로 가지 않을 수 있다 |
| TLS Secret 없음 또는 이름 오류 | controller event나 log에 인증서 관련 오류가 남을 수 있다 |
| Service selector 오류 | Ingress는 있어도 backend endpoint가 비어 요청이 실패한다 |
| 인증서 host 불일치 | 클라이언트 TLS 검증에서 hostname mismatch가 발생한다 |

## 해석 / 의견

Ingress를 "외부 URL을 여는 manifest" 정도로만 보면 장애 때 어디를 봐야 할지 흐려진다. 요청 경로는 보통 DNS, load balancer, Ingress Controller, Ingress rule, Service, EndpointSlice, Pod 순서로 이어진다. 따라서 장애 대응 문서도 이 순서로 나눠야 한다.

TLS 종료 위치도 중요하다. 일반적인 Ingress 구성에서는 클라이언트와 Ingress Controller 사이에서 HTTPS가 종료되고, Ingress Controller에서 Service/Pod까지는 클러스터 내부 HTTP로 전달될 수 있다. 이 경우 Rust API가 직접 TLS를 처리하는 것이 아니므로, 앱이 `X-Forwarded-Proto`, `X-Forwarded-For`, `Host` 같은 헤더를 신뢰할지 별도 기준이 필요하다.

프록시 헤더는 편리하지만 신뢰 경계가 필요하다. 앱이 외부 클라이언트가 임의로 보낸 `X-Forwarded-*` 헤더를 그대로 믿으면 scheme, client IP, redirect URL 판단이 틀어질 수 있다. 신뢰할 수 있는 Ingress Controller 뒤에서만 해당 헤더를 사용하도록 서버 또는 미들웨어 정책을 둔다.

## 한계와 예외

- Ingress annotation은 controller마다 다르다. NGINX, Traefik, HAProxy, AWS ALB, GCE Ingress의 세부 설정을 이 글에서 일반화하지 않는다.
- 인증서 자동 발급과 갱신은 cert-manager 같은 별도 구성 요소가 필요할 수 있다. 이 글은 TLS Secret을 사용하는 Ingress 경계만 다룬다.
- 새로운 기능이 필요한 설계라면 Gateway API 검토가 필요하다. 이 글은 기존 Ingress API를 이해하기 위한 글이다.
- mTLS, end-to-end TLS, WAF, rate limiting, external-dns는 별도 운영 주제로 분리한다.

## 참고자료

- [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Kubernetes TLS Secrets](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets)
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
- [Gateway API](https://gateway-api.sigs.k8s.io/)

## 변경 이력

- 2026-05-05: Ingress Controller, host/path routing, TLS Secret, TLS 종료 경계를 공식 문서 기준으로 재작성.
