# 개요

설정하면서 참고하고 고민했던 부분을 기록

## jaeger

- all-in-one 모듈에서 v2인 jaeger 모듈로 바뀌는 중. 때문에 주요 문서들이 유효하지 않은 경우가 많았음
- trace 전용 모듈이므로 metric 수집까지 하고 싶은 관계로 otel api endpoint는 otel collector가 받고, metrics는 prometheus에 traces는 jaeger가 받도록 했음

## jaeger 설정

- 설정 파일 부분의 설명이 와닿지 않아. 실제 예시를 보면서 만들었음.
https://github.com/jaegertracing/jaeger/blob/main/docker-compose/tail-sampling/jaeger-v2-config.yml


- Service Performance Monitor 설정
https://www.jaegertracing.io/docs/2.11/architecture/spm/

- prometheus 같은 monitor설정이 보여서 아래 문서를 참조
https://github.com/jaegertracing/jaeger/blob/main/docker-compose/monitor/docker-compose.yml
https://github.com/jaegertracing/jaeger/blob/main/cmd/jaeger/config-spm.yaml



## 컨테이너

- synology nas에서 동작 시키는 경우 컨테이너 자체가 방화벽에 걸리는 문제가 있으므로, 여러 컨테이너간에 통신을 시키려면.. 컨테이너의 네트워크에 대한 방화벽 설정을 해야 함




## 통합

- 위의 synology 문제 우회를 위해서는.. 결국 하나의 container에 묶는 것이 정답에 가까움.
- `jaeger`는 v2부터는 하나의 실행파일이라 좀 괜찮음
- `open telemetry collector`는 contrib 이랑 나뉘어져 있는 것 같아보임
- `prometheus` 도 단일 파일 이라 좋음 (promql 도구가 분리되어있음)