---
layout: single
title: "Jenkins 10. Jenkins에서 Kubernetes 배포로 연결할 때 경계는 어디에 두는가"
description: "Jenkins가 Docker 이미지를 만들고 Kubernetes가 원하는 상태를 맞추는 구조로 CI/CD 경계를 나누는 글."
date: 2026-06-27 09:00:00 +09:00
lang: ko
translation_key: jenkins-to-kubernetes-deployment-boundary
section: development
topic_key: devops
categories: DevOps
tags: [jenkins, kubernetes, deployment, ci-cd, boundary]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Jenkins와 Kubernetes를 연결할 때 Jenkins가 모든 것을 직접 처리하게 만들면 경계가 흐려진다. Jenkins는 source를 검증하고 image를 만들고 배포 요청을 발생시키는 쪽에 가깝고, Kubernetes는 manifest에 적힌 원하는 상태를 cluster 안에서 맞추는 쪽에 가깝다.

이 글의 결론은 Jenkins Pipeline에 cluster 운영 지식을 무한히 넣지 말고, image build와 deploy trigger, manifest 변경, cluster reconciliation의 책임을 분리해야 한다는 것이다.

## 문서 정보

- 작성일: 2026-04-24
- 검증 기준일: 2026-04-24
- 문서 성격: analysis
- 테스트 환경: 작성자 Jenkins 실습 서버에서 확인. 2026-04-24 비인증 로그인 페이지 응답 헤더 기준 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다. OS는 Linux 22.04이며, agent 구성은 이 글에 고정하지 않았다.
- 테스트 버전: 작성자 Jenkins 실습 서버 Jenkins 2.541.3(2026-04-24 로그인 응답 헤더 기준). 문서 검증은 2026-04-24 확인한 관련 공식 문서를 기준으로 했다.
- 출처 등급: Jenkins 공식 문서와 Kubernetes 공식 문서를 사용했다.
- 비고: Argo CD, Flux, Helm, Kustomize, GitOps 비교는 이 글의 범위가 아니다.

## 문제 정의

Jenkins에서 Kubernetes 배포까지 연결할 때 자주 생기는 문제는 아래와 같다.

- Jenkinsfile 안에 cluster 접속 정보와 배포 로직이 모두 들어간다.
- image tag는 바뀌었지만 manifest 변경 이력이 남지 않는다.
- Jenkins job 성공을 Kubernetes 배포 성공과 같은 뜻으로 본다.
- rollback 기준이 Jenkins build number인지 Kubernetes rollout인지 불분명하다.

이번 글은 Jenkins에서 Kubernetes로 넘어가기 전 경계를 정리한다.

## 확인된 사실

- Jenkins Using Docker with Pipeline 문서 기준으로 Jenkins Pipeline은 Docker image build와 custom registry push를 수행할 수 있다.
  근거: [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- Kubernetes Objects 문서 기준으로 Kubernetes object는 cluster 상태를 나타내는 persistent entity이며, object를 만들면 Kubernetes system이 그 object가 존재하도록 계속 동작한다.
  근거: [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- Kubernetes Objects 문서 기준으로 `spec`은 원하는 상태를, `status`는 Kubernetes system과 component가 제공하고 갱신하는 현재 상태를 설명한다.
  근거: [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- Kubernetes Deployment 문서 기준으로 Deployment는 application workload를 실행할 Pod 집합을 관리하고 Pods와 ReplicaSets에 대한 declarative update를 제공한다.
  근거: [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- Kubernetes Service 문서 기준으로 Service는 cluster 안의 하나 이상의 Pod로 실행되는 network application을 노출하는 방법이다.
  근거: [Service](https://kubernetes.io/docs/concepts/services-networking/service/)

경계는 아래처럼 나누면 이해하기 쉽다.

```text
Jenkins: checkout, test, image build, registry push, deploy request
Manifest repository: desired state change history
Kubernetes: scheduling, rollout, service routing, reconciliation
Registry: image storage and digest
```

## 직접 재현한 결과

- 직접 재현함: 작성자 Jenkins 실습 서버에서 이 글의 주요 명령과 설정 흐름을 확인했다. 2026-04-24 비인증 로그인 페이지 응답 헤더에서 `X-Jenkins: 2.541.3`, `Server: Jetty(12.1.5)`를 확인했다.
- 확인한 결과: Jenkins 공식 문서와 Kubernetes 공식 문서 기준으로 image build/push와 object desired state 경계를 확인했다.
- 직접 확인 항목: 같은 image tag를 Deployment manifest에 반영하고 `kubectl rollout status` 결과를 Jenkins build 결과와 분리해서 기록했다.

## 해석 / 의견

내 판단으로는 Jenkins job 성공은 "배포가 끝났다"가 아니라 "배포 요청을 보냈다"에 가까운 경우가 많다. 실제 배포 성공은 Kubernetes Deployment rollout, Pod readiness, Service routing, Ingress 상태를 따로 봐야 한다.

초급 단계에서는 Jenkins가 `kubectl apply`까지 직접 수행하는 방식이 이해하기 쉽다. 하지만 운영으로 갈수록 manifest 변경 이력을 Git에 남기고, Jenkins는 image와 변경 요청을 만드는 쪽으로 제한하는 편이 추적에 유리하다.

중요한 것은 하나의 source commit, 하나의 image digest, 하나의 manifest 변경, 하나의 rollout 결과를 연결하는 것이다. 이 네 가지가 분리되면 장애 때 어떤 버전이 실제로 떠 있는지 찾기 어려워진다.

## 한계와 예외

작성자 실습 환경에서 기본 배포 경계와 rollout 확인 흐름을 확인했다. RBAC, kubeconfig 보관, namespace 권한, rollout 실패, image pull error는 후속 Kubernetes 글에서 더 자세히 다뤄야 한다.

작은 내부 시스템에서는 Jenkins가 직접 `kubectl apply`를 실행하는 방식도 충분할 수 있다. 반대로 여러 cluster와 환경을 운영한다면 GitOps controller를 쓰는 편이 경계가 더 명확할 수 있다.

## 참고자료

- Jenkins User Handbook, [Using Docker with Pipeline](https://www.jenkins.io/doc/book/pipeline/docker/)
- Kubernetes Docs, [Objects In Kubernetes](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- Kubernetes Docs, [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- Kubernetes Docs, [Service](https://kubernetes.io/docs/concepts/services-networking/service/)
