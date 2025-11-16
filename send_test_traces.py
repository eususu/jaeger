#!/usr/bin/env python3
"""
OpenTelemetry 테스트 trace 데이터를 전송하는 스크립트
"""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
import time

# TracerProvider 설정
resource = Resource.create({"service.name": "test-service"})
provider = TracerProvider(resource=resource)

# OTLP HTTP Exporter 설정
otlp_exporter = OTLPSpanExporter(
    endpoint="http://172.30.1.15:4318/v1/traces",
)

# Span Processor 추가
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# Global TracerProvider 설정
trace.set_tracer_provider(provider)

# Tracer 생성
tracer = trace.get_tracer(__name__)

def send_test_traces():
    """3개의 테스트 trace 생성 및 전송"""
    
    # Trace 1: 사용자 로그인
    print("📤 Trace 1: 사용자 로그인 전송 중...")
    with tracer.start_as_current_span("user-login") as span:
        span.set_attribute("user.id", "user123")
        span.set_attribute("http.method", "POST")
        span.set_attribute("http.url", "/api/login")
        span.set_attribute("http.status_code", 200)
        time.sleep(0.1)  # 작업 시뮬레이션
        
        with tracer.start_as_current_span("database-query") as child_span:
            child_span.set_attribute("db.system", "postgresql")
            child_span.set_attribute("db.statement", "SELECT * FROM users WHERE id = ?")
            time.sleep(0.05)
    
    print("✅ Trace 1 전송 완료\n")
    time.sleep(0.5)
    
    # Trace 2: 상품 조회
    print("📤 Trace 2: 상품 조회 전송 중...")
    with tracer.start_as_current_span("product-search") as span:
        span.set_attribute("product.category", "electronics")
        span.set_attribute("http.method", "GET")
        span.set_attribute("http.url", "/api/products")
        span.set_attribute("http.status_code", 200)
        time.sleep(0.08)
        
        with tracer.start_as_current_span("cache-lookup") as child_span:
            child_span.set_attribute("cache.hit", True)
            child_span.set_attribute("cache.key", "products:electronics")
            time.sleep(0.02)
    
    print("✅ Trace 2 전송 완료\n")
    time.sleep(0.5)
    
    # Trace 3: 주문 처리 (에러 포함)
    print("📤 Trace 3: 주문 처리 (에러) 전송 중...")
    with tracer.start_as_current_span("order-processing") as span:
        span.set_attribute("order.id", "order456")
        span.set_attribute("http.method", "POST")
        span.set_attribute("http.url", "/api/orders")
        span.set_attribute("http.status_code", 500)
        time.sleep(0.12)
        
        with tracer.start_as_current_span("payment-processing") as child_span:
            child_span.set_attribute("payment.method", "credit_card")
            child_span.set_attribute("payment.amount", 99.99)
            # 에러 기록
            child_span.set_status(trace.Status(trace.StatusCode.ERROR, "Payment gateway timeout"))
            child_span.record_exception(Exception("Payment gateway timeout"))
            time.sleep(0.05)
    
    print("✅ Trace 3 전송 완료\n")
    
    # Span이 모두 전송될 때까지 대기
    time.sleep(2)
    provider.force_flush()
    
    print("🎉 모든 테스트 trace 전송 완료!")

if __name__ == "__main__":
    print("=" * 50)
    print("OpenTelemetry 테스트 Trace 전송 시작")
    print("=" * 50)
    print()
    
    send_test_traces()
