# 개요

설정하면서 참고하고 고민했던 부분을 기록

## jaeger

- all-in-one 모듈에서 v2인 jaeger 모듈로 바뀌는 중. 때문에 주요 문서들이 유효하지 않은 경우가 많았음
- trace 전용 모듈이므로 metric 수집까지 하고 싶은 관계로 otel api endpoint는 otel collector가 받고, metrics는 prometheus에 traces는 jaeger가 받도록 했음

## jaeger 설정

- 설정 파일 부분의 설명이 와닿지 않아. 실제 예시를 보면서 만들었음.
https://github.com/jaegertracing/jaeger/blob/main/docker-compose/tail-sampling/jaeger-v2-config.yml