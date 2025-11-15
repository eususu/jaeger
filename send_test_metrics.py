#!/usr/bin/env python3
"""
OpenTelemetry 테스트 metric 데이터를 전송하는 스크립트
"""

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
import time
import random

# Resource 설정
resource = Resource.create({"service.name": "test-metrics-service"})

# OTLP HTTP Metric Exporter 설정
otlp_exporter = OTLPMetricExporter(
    endpoint="http://localhost:4318/v1/metrics",
)

# Metric Reader 설정 (5초마다 export)
metric_reader = PeriodicExportingMetricReader(
    exporter=otlp_exporter,
    export_interval_millis=5000
)

# MeterProvider 설정
provider = MeterProvider(
    resource=resource,
    metric_readers=[metric_reader]
)

# Global MeterProvider 설정
metrics.set_meter_provider(provider)

# Meter 생성
meter = metrics.get_meter(__name__)


# Metric 1: Counter - HTTP 요청 수
http_request_counter = meter.create_counter(
    name="http.requests.total",
    description="Total number of HTTP requests",
    unit="1"
)

# Metric 2: Histogram - 응답 시간
response_time_histogram = meter.create_histogram(
    name="http.response.duration",
    description="HTTP response duration in milliseconds",
    unit="ms"
)

# Metric 3: UpDownCounter - 활성 연결 수
active_connections = meter.create_up_down_counter(
    name="system.active.connections",
    description="Number of active connections",
    unit="1"
)

def send_test_metrics():
    """3개의 테스트 metric 생성 및 전송"""
    
    print("📊 Metric 데이터 생성 시작...\n")
    
    # 30초 동안 metric 데이터 생성
    for i in range(30):
        # Metric 1: HTTP 요청 카운터
        http_request_counter.add(
            random.randint(1, 5),
            {"http.method": "GET", "http.status_code": "200", "endpoint": "/api/users"}
        )
        http_request_counter.add(
            random.randint(1, 3),
            {"http.method": "POST", "http.status_code": "201", "endpoint": "/api/orders"}
        )
        
        # Metric 2: 응답 시간 히스토그램
        response_time_histogram.record(
            random.uniform(10, 100),
            {"http.method": "GET", "endpoint": "/api/users"}
        )
        response_time_histogram.record(
            random.uniform(50, 200),
            {"http.method": "POST", "endpoint": "/api/orders"}
        )
        
        # Metric 3: 활성 연결 수 (증가/감소)
        change = random.randint(-2, 3)
        active_connections.add(
            change,
            {"connection.type": "http", "server": "web-01"}
        )
        
        if (i + 1) % 5 == 0:
            print(f"✅ {i + 1}초 경과 - metric 데이터 생성 중...")
        
        time.sleep(1)
    
    print("\n⏳ Metric 데이터 전송 대기 중...")
    time.sleep(6)  # 마지막 export 대기
    
    provider.force_flush()
    provider.shutdown()
    
    print("🎉 모든 테스트 metric 전송 완료!")

if __name__ == "__main__":
    print("=" * 50)
    print("OpenTelemetry 테스트 Metric 전송 시작")
    print("=" * 50)
    print()
    print("📌 전송할 Metric 종류:")
    print("  1. http.requests.total (Counter)")
    print("  2. http.response.duration (Histogram)")
    print("  3. system.active.connections (UpDownCounter)")
    print()
    
    send_test_metrics()
