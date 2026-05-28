# 🔭 Observability — Logging, Metrics & Tracing

> `[INTERMEDIATE → ADVANCED]` — "You can't manage what you can't measure"

---

## 3 Pillars of Observability

```
           OBSERVABILITY
          /      |       \
      Logs    Metrics   Traces
   "What      "How is    "Where did
  happened?"  system?"   request go?"
```

---

## 1. Logging — Ghi lại sự kiện

### Structured Logging (JSON > plain text)

```python
# ❌ Plain text logs — khó query
print(f"User {user_id} logged in from {ip} at {time}")

# ✅ Structured JSON logs — dễ search, filter, aggregate
import structlog
import logging

# Setup
logging.basicConfig(format="%(message)s", level=logging.INFO)
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer() if DEV else structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)

log = structlog.get_logger()

# Dùng
log.info("user.login", user_id=user_id, ip=ip, user_agent=req.headers.get("user-agent"))
log.error("payment.failed", order_id=order_id, amount=amount, error=str(e))
log.warning("rate_limit.exceeded", user_id=user_id, endpoint="/api/search")
```

```typescript
// Node.js với Pino (nhanh nhất)
import pino from 'pino'

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  base: {
    service: 'api-gateway',
    version: process.env.APP_VERSION
  }
})

// Child logger kế thừa context
const reqLogger = logger.child({ requestId: req.headers['x-request-id'] })
reqLogger.info({ userId: user.id, path: req.path }, 'Request received')
reqLogger.error({ err }, 'Unhandled error')
```

### Log Levels — Dùng đúng level

```
TRACE   → Chi tiết nhất, chỉ debug cực kỳ sâu (thường tắt)
DEBUG   → Debug info, bật khi cần investigate
INFO    → Sự kiện bình thường: user login, order created
WARN    → Điều gì đó không đúng nhưng chưa nguy hiểm: retry lần 2
ERROR   → Lỗi xảy ra, cần xử lý: DB connection failed
FATAL   → Hệ thống không thể tiếp tục: out of memory
```

### Log Stack — ELK

```yaml
# docker-compose với ELK
version: '3'
services:
  elasticsearch:
    image: elasticsearch:8.12.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports: ["9200:9200"]

  logstash:
    image: logstash:8.12.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: kibana:8.12.0
    ports: ["5601:5601"]
```

---

## 2. Metrics — Đo lường system health

### RED Method (cho Services)

```
R — Rate    : requests/sec
E — Errors  : error rate (%)
D — Duration: response time (p50, p95, p99)
```

### USE Method (cho Resources)

```
U — Utilization : CPU %, Memory %, Disk %
S — Saturation  : Queue length, wait time
E — Errors      : Hardware errors, disk errors
```

### Prometheus + Grafana

```python
# Python với prometheus-client
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Metrics definitions
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    labelnames=["method", "endpoint", "status_code"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    labelnames=["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

active_connections = Gauge(
    "active_connections",
    "Number of active connections"
)

# FastAPI middleware
import time
from fastapi import Request

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.perf_counter()
    active_connections.inc()

    response = await call_next(request)

    duration = time.perf_counter() - start
    http_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    ).inc()
    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    active_connections.dec()

    return response

# Expose /metrics endpoint
start_http_server(9090)  # Prometheus scrape từ đây
```

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'api'
    static_configs:
      - targets: ['api:9090']
  
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
  
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

### Grafana Dashboard Essentials

```
Panels cần có:
1. Request Rate (QPS) — Line graph
2. Error Rate (%) — Line graph + threshold alert
3. p50/p95/p99 Latency — Line graph
4. Active Connections — Gauge
5. CPU Usage — Line graph
6. Memory Usage — Line graph
7. Database connections — Gauge
8. Cache hit rate — Gauge
```

---

## 3. Distributed Tracing

```
Request A ──► Service B ──► Database
              │
              └──► Service C ──► Redis

Trace: parent span + child spans
  Span 1: A handles request (150ms total)
    Span 2: Call to B (80ms)
      Span 3: B queries DB (50ms)
      Span 4: B queries Redis (5ms)
    Span 5: Call to C (30ms)
```

### OpenTelemetry (Standard)

```python
# Cài đặt
pip install opentelemetry-sdk opentelemetry-exporter-otlp

# Setup
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Configure exporter (Jaeger, Tempo, ...)
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://jaeger:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Auto-instrument FastAPI + SQLAlchemy
FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine)

# Manual spans
tracer = trace.get_tracer("my_app")

async def checkout(order_data: dict):
    with tracer.start_as_current_span("checkout") as span:
        span.set_attribute("order.id", order_data["id"])
        span.set_attribute("order.amount", order_data["amount"])

        with tracer.start_as_current_span("validate_inventory"):
            await validate_inventory(order_data["items"])

        with tracer.start_as_current_span("process_payment"):
            result = await process_payment(order_data["amount"])
            span.set_attribute("payment.status", result.status)

        return result
```

---

## Alerting

```yaml
# Prometheus alerting rules
groups:
  - name: api_alerts
    rules:
      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status_code=~"5.."}[5m]) /
          rate(http_requests_total[5m]) > 0.05
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Error rate > 5%"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1.0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "p95 latency > 1s"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
```

---

## Loki — Log aggregation đơn giản hơn ELK

```yaml
# docker-compose với Loki + Grafana
services:
  loki:
    image: grafana/loki:latest
    ports: ["3100:3100"]

  promtail:  # Log collector
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log
      - ./promtail-config.yml:/etc/promtail/config.yml

  grafana:
    image: grafana/grafana:latest
    ports: ["3000:3000"]
```

---

## Bài tập thực hành

- [ ] Thêm structured logging vào 1 project thực
- [ ] Setup Prometheus + Grafana, tạo dashboard cho API
- [ ] Tạo alert khi error rate > 1%
- [ ] Add OpenTelemetry auto-instrumentation vào FastAPI/Express

---

## Tài nguyên thêm

- [Prometheus Docs](https://prometheus.io/docs/)
- [Grafana Docs](https://grafana.com/docs/)
- [OpenTelemetry](https://opentelemetry.io/) — Standard mới nhất
- [Jaeger Tracing](https://www.jaegertracing.io/)
