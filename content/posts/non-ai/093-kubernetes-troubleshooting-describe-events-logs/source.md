---
layout: single
title: "Kubernetes 장애 대응: describe, events, logs"
description: "Kubernetes 장애 대응: describe, events, logs에 대해 공식 문서와 운영 관점으로 확인할 기준, 점검 순서, 한계를 정리한 글."
date: 2026-06-18 09:00:00 +09:00
lang: ko
translation_key: kubernetes-troubleshooting-describe-events-logs
section: development
topic_key: devops
categories: DevOps
tags: [devops, kubernetes, troubleshooting, operations]
author_profile: false
sidebar:
  nav: "sections"
search: true
---

## 요약

Kubernetes 장애 대응에서 `describe`, `events`, `logs`는 같은 정보를 반복해서 보는 명령이 아니다. `describe`는 객체 상태와 최근 event를 한 번에 보고, `events`는 시간순으로 control plane 결정을 추적하고, `logs`는 컨테이너 내부 애플리케이션 출력을 확인하는 데 쓴다.

## 문서 정보

- 작성일: 2026-04-29
- 검증 기준일: 2026-04-29
- 문서 성격: tutorial | analysis
- 테스트 환경: 실행 테스트 없음. Kubernetes 공식 문서와 kubectl reference 기준으로 장애 대응 순서 정리.
- 테스트 버전: Kubernetes 공식 문서 2026-04-29 확인본. 클러스터와 kubectl 로컬 버전은 고정하지 않음.
- 출처 등급: 공식 문서

## 문제 정의

장애 상황에서 바로 `kubectl logs`만 보면 원인을 놓칠 수 있다. Pod가 아직 scheduling되지 않았거나 image pull 단계에서 실패한 경우에는 애플리케이션 로그가 없을 수 있기 때문이다. 반대로 event만 보면 컨테이너 내부 예외나 애플리케이션 초기화 실패를 확인하지 못한다.

이 글은 Pod 또는 Deployment 장애를 처음 볼 때 `describe`, `events`, `logs`를 어떤 순서로 확인할지 정리한다.

## 확인된 사실

- Kubernetes debug 문서는 애플리케이션 장애 조사에서 Pod 상태, event, log를 나누어 확인하도록 안내한다.
  근거: [Kubernetes Debug Applications](https://kubernetes.io/docs/tasks/debug/debug-application/)
- Kubernetes 문서는 Pending Pod를 조사할 때 `kubectl describe pod`로 event를 확인하는 예시를 제공한다.
  근거: [Kubernetes Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)
- 공식 문서 기준으로 컨테이너 로그는 `kubectl logs ${POD_NAME} -c ${CONTAINER_NAME}`로 확인하며, 이전에 crash한 컨테이너는 `--previous`로 확인할 수 있다.
  근거: [Kubernetes Examining pod logs](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#examining-pod-logs)
- `kubectl events`는 namespace 전체, 모든 namespace, 특정 resource 기준 event를 조회할 수 있다.
  근거: [kubectl events](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_events/)

## 직접 재현한 결과

- 직접 재현 없음: 이 글은 실제 클러스터에서 장애를 발생시킨 실험 보고서가 아니다.
- 직접 확인한 범위: 2026-04-29 기준 Kubernetes 공식 문서와 kubectl reference의 명령 의미와 옵션.

## 재현 순서

장애 대응의 첫 순서는 "어떤 계층에서 멈췄는지"를 좁히는 것이다.

1. 문제가 있는 workload를 찾는다.

```bash
kubectl get pods -n <namespace>
kubectl get deploy,rs,pod -n <namespace>
```

2. Pod 상세 상태를 본다.

```bash
kubectl describe pod <pod-name> -n <namespace>
```

우선 확인할 항목:

- `Status`, `Conditions`: `PodScheduled`, `Initialized`, `Ready`, `ContainersReady`
- `Containers`: image, command, args, ports, env, mounts
- `State`, `Last State`, `Restart Count`
- `Events`: scheduler, kubelet, image pull, probe 실패 메시지

3. event를 시간순으로 다시 본다.

```bash
kubectl events -n <namespace> --for pod/<pod-name>
kubectl events -n <namespace> --types=Warning
kubectl events --all-namespaces --types=Warning
```

여러 Pod가 동시에 흔들릴 때는 개별 `describe`보다 namespace 또는 전체 event 흐름을 먼저 보는 편이 빠르다.

4. 컨테이너 로그를 본다.

```bash
kubectl logs <pod-name> -n <namespace> -c <container-name>
kubectl logs <pod-name> -n <namespace> -c <container-name> --previous
```

`--previous`는 `CrashLoopBackOff`처럼 컨테이너가 재시작된 뒤 직전 컨테이너의 로그를 볼 때 중요하다.

5. 원인 후보를 상태별로 나눈다.

- `Pending` + `FailedScheduling`: node selector, taint/toleration, resource request, PVC binding 확인
- `ImagePullBackOff` 또는 `ErrImagePull`: image 이름, tag, registry 인증, network, pull policy 확인
- `CrashLoopBackOff`: `Last State`, exit code, `--previous` 로그, probe 설정 확인
- `Running`이지만 `Ready=False`: readiness probe, dependency, service endpoint 확인
- event는 정상인데 애플리케이션 실패: app log, config, secret mount, env 확인

## 관찰 결과

- `describe`는 한 Pod에 대한 현재 상태와 최근 event를 빠르게 묶어 보여준다.
- `events`는 control plane과 kubelet이 어떤 결정을 내렸는지 시간순으로 추적하는 데 유리하다.
- `logs`는 컨테이너가 실행된 뒤 애플리케이션이 무엇을 출력했는지 보여준다. Pod가 실행 전 단계에서 실패하면 로그가 비어 있을 수 있다.

## 해석 / 의견

내 판단으로는 Kubernetes 장애 대응의 기본 순서는 `describe`로 범위를 좁히고, `events`로 클러스터 결정 흐름을 확인한 뒤, `logs`로 애플리케이션 내부 원인을 확인하는 것이다.

의견: 장애 기록에는 원문 로그 전체보다 `namespace`, `pod`, `container`, 확인한 명령, 핵심 event reason, exit code, 재시작 횟수, 사용한 `--previous` 여부를 남기는 편이 후속 분석에 더 유용하다.

## 한계와 예외

- event는 영구 보관 로그가 아니다. 장기 사고 분석에는 별도 logging/observability 구성이 필요하다.
- managed Kubernetes, CNI, CSI, registry, node OS에 따라 실패 메시지와 원인 후보가 다를 수 있다.
- 이 글은 Pod/Deployment 중심의 초동 대응 순서이며 control plane 장애, network policy, DNS, storage 장애 전체를 다루지 않는다.

## 참고자료

- [Kubernetes Debug Applications](https://kubernetes.io/docs/tasks/debug/debug-application/)
- [Kubernetes Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/)
- [kubectl describe](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe)
- [kubectl logs](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#logs)
- [kubectl events](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_events/)

## 변경 이력

- 2026-04-29: 초안 작성.
- 2026-04-29: `describe`, `events`, `logs` 점검 순서와 상태별 해석 기준 보강.
