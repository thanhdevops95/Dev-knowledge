# Observability — Metrics, Logs, Traces

> **Tags:** `observability` `prometheus` `grafana` `opentelemetry` `logging` `monitoring`
> **Level:** Intermediate | **Prerequisite:** `docker/01-docker-basics.md`

---

## 1. The Three Pillars

```
Observability = Metrics + Logs + Traces

Metrics: Aggregate numeric data over time
  - "What is happening?"
  - CPU usage, request rate, error rate, latency percentiles
  - Tools: Prometheus, Datadog, InfluxDB

Logs: Timestamped discrete events
  - "What happened?"
  - User logged in, error occurred, order created
  - Tools: ELK (Elasticsearch + Logstash + Kibana), Loki + Grafana

Traces: End-to-end request journey across services
  - "Why is it slow?"
  - Which service is the bottleneck, which DB query is slow
  - Tools: Jaeger, Zipkin, Grafana Tempo, AWS X-Ray
```

---

## 2. Prometheus — Metrics Collection

```
Architecture:
  Applications → (expose /metrics) → Prometheus (scrapes) → Grafana (visualizes)
                                    ↓
                                AlertManager (alerts)
                                    ↓
                                Slack/PagerDuty/Email
```

### Instrument Python App
```python
from prometheus_client import Counter, Histogram, Gauge, Info, start_http_server
import time

# Metric types
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    labelnames=['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    labelnames=['method', 'endpoint'],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

ACTIVE_USERS = Gauge(
    'active_users_total',
    'Currently active users'
)

DB_POOL_SIZE = Gauge(
    'db_connection_pool_size',
    'Database connection pool size',
    labelnames=['state']  # 'used', 'idle'
)

APP_INFO = Info('app', 'Application information')
APP_INFO.info({'version': '1.2.3', 'git_commit': 'abc1234'})

# FastAPI middleware
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start
        endpoint = request.url.path
        
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status_code=response.status_code
        ).inc()
        
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(duration)
        
        return response

# Expose metrics endpoint
from prometheus_client import make_asgi_app

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

### Instrument Node.js App
```typescript
import promClient from 'prom-client';

// Enable default metrics (CPU, memory, GC, event loop)
promClient.collectDefaultMetrics({ prefix: 'nodejs_' });

const httpRequests = new promClient.Counter({
    name: 'http_requests_total',
    help: 'Total HTTP requests',
    labelNames: ['method', 'route', 'status_code'],
});

const httpDuration = new promClient.Histogram({
    name: 'http_request_duration_seconds',
    help: 'HTTP request duration in seconds',
    labelNames: ['method', 'route'],
    buckets: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5],
});

// Express middleware
app.use((req, res, next) => {
    const start = Date.now();
    
    res.on('finish', () => {
        const duration = (Date.now() - start) / 1000;
        const route = req.route?.path ?? req.path;
        
        httpRequests.labels(req.method, route, res.statusCode.toString()).inc();
        httpDuration.labels(req.method, route).observe(duration);
    });
    
    next();
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
    res.set('Content-Type', promClient.register.contentType);
    res.end(await promClient.register.metrics());
});
```

---

## 3. Prometheus Config

```yaml
# prometheus.yml
global:
  scrape_interval: 15s          # Pull metrics every 15 seconds
  evaluation_interval: 15s      # Evaluate rules every 15 seconds
  external_labels:
    cluster: production

rule_files:
  - /etc/prometheus/rules/*.yml

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

scrape_configs:
  # Auto-discover services via Kubernetes
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # Only scrape pods with annotation
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
  
  # Static scrape
  - job_name: 'my-api'
    static_configs:
      - targets: ['api-service:8080']
    metrics_path: /metrics
    scrape_interval: 10s
  
  # Push gateway (for batch jobs)
  - job_name: 'pushgateway'
    static_configs:
      - targets: ['pushgateway:9091']
    honor_labels: true
```

---

## 4. PromQL — Query Language

```promql
# Instant vectors
http_requests_total                          # All time series
http_requests_total{job="api"}              # Filter by label
http_requests_total{status_code=~"5.."}     # Regex filter
http_requests_total{status_code!="200"}     # Not equal

# Rate/Increase (for counters)
rate(http_requests_total[5m])               # Per-second rate over 5 min
irate(http_requests_total[5m])              # Instant rate (last 2 samples)
increase(http_requests_total[1h])           # Total increase over 1 hour

# Aggregation
sum(rate(http_requests_total[5m]))          # Total RPS across all instances
sum by (endpoint)(rate(http_requests_total[5m]))  # RPS per endpoint
avg by (instance)(cpu_usage_seconds_total)
max by (pod)(memory_usage_bytes)

# Common operations
# Error rate
sum(rate(http_requests_total{status_code=~"5.."}[5m]))
/ sum(rate(http_requests_total[5m]))

# Latency percentiles (from histogram)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))  # p95
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))  # p99

# Join metrics from different time series
sum(rate(http_requests_total{status_code=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
* 100  # Error percentage
```

---

## 5. Alert Rules

```yaml
# rules/api_alerts.yml
groups:
  - name: api
    rules:
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{status_code=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) > 0.05
        for: 5m             # Must be true for 5 minutes
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "High error rate on {{ $labels.job }}"
          description: "Error rate is {{ $value | humanizePercentage }} for the last 5m"
          runbook: "https://runbooks.example.com/high-error-rate"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High P99 latency: {{ $value | humanizeDuration }}"
          
      - alert: InstanceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Instance {{ $labels.instance }} is down"
          
      - alert: HighMemoryUsage
        expr: |
          container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Container {{ $labels.container }} memory > 90%"
```

---

## 6. Grafana Dashboards

```json
// Example dashboard panel (JSON)
{
  "title": "Request Rate",
  "type": "timeseries",
  "gridPos": { "x": 0, "y": 0, "w": 12, "h": 8 },
  "targets": [
    {
      "expr": "sum by (endpoint) (rate(http_requests_total[5m]))",
      "legendFormat": "{{endpoint}}"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "reqps",
      "color": { "mode": "palette-classic" }
    }
  }
}
```

### Standard Dashboard Panels (RED Method)
- **Rate**: `rate(http_requests_total[5m])` — requests per second
- **Errors**: `rate(http_requests_total{status_code=~"5.."}[5m]) / rate(http_requests_total[5m])`
- **Duration**: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))`

### USE Method (Infrastructure)
- **Utilization**: `1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m]))`
- **Saturation**: `node_load1` (load average)
- **Errors**: `rate(node_disk_io_now[5m])`

---

## 7. Structured Logging

### Log Levels
```
TRACE   → Very detailed, development only
DEBUG   → Diagnostic info, not in production
INFO    → Normal operations, key events
WARNING → Unexpected but handled, no action required
ERROR   → Failed operation, needs attention
CRITICAL/FATAL → System is failing, immediate action
```

### Best Practices
```python
# Python (structlog)
import structlog

log = structlog.get_logger()

# BAD: string interpolation
log.info(f"User {user_id} logged in from {ip}")

# GOOD: structured key-value pairs
log.info("user_logged_in", user_id=user_id, ip=ip, user_agent=agent)

# Include context in all log lines
log = log.bind(request_id=request_id, user_id=user_id)
log.info("processing_started", action="create_order")
log.info("payment_initiated", amount=order.total, currency="USD")
log.info("order_confirmed", order_id=order.id)

# Log timing
import time
start = time.time()
result = expensive_operation()
log.info("operation_completed",
    duration_ms=int((time.time() - start) * 1000),
    result_count=len(result)
)
```

### Log Aggregation — Loki
```yaml
# docker-compose.yml with Loki stack
services:
  loki:
    image: grafana/loki:2.9.0
    ports: ["3100:3100"]
    volumes:
      - loki-data:/loki
    
  promtail:
    image: grafana/promtail:2.9.0
    volumes:
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - ./promtail-config.yml:/etc/promtail/config.yml
    command: -config.file=/etc/promtail/config.yml
    
  grafana:
    image: grafana/grafana:10.2.0
    ports: ["3000:3000"]
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
```

```yaml
# promtail-config.yml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        target_label: 'container'
    pipeline_stages:
      - json:
          expressions:
            level: level
            msg: message
      - labels:
          level:
```

---

## 8. Distributed Tracing

```
Request: API → UserService → DB + AuthService → Response

Trace ID: abc123
  Span 1: API Gateway (100ms total)
    Span 2: UserService.getUserProfile (80ms)
      Span 3: DB.SELECT users (15ms)
      Span 4: AuthService.validatePermissions (20ms)
      Span 5: Redis.GET cache (5ms)
```

### OpenTelemetry Setup
```python
# main.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

def setup_tracing():
    provider = TracerProvider(
        resource=Resource.create({
            "service.name": "user-service",
            "service.version": "1.2.3",
            "deployment.environment": os.getenv("ENV", "development"),
        })
    )
    
    exporter = OTLPSpanExporter(
        endpoint="http://tempo:4317",  # Or Jaeger, Zipkin
        insecure=True,
    )
    
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    
    # Auto-instrument libraries
    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
    SQLAlchemyInstrumentor().instrument(engine=engine)
    RedisInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()

# Manual spans
tracer = trace.get_tracer("user-service")

async def process_order(order_id: str):
    with tracer.start_as_current_span("process-order") as span:
        span.set_attributes({
            "order.id": order_id,
            "order.type": "standard",
        })
        
        with tracer.start_as_current_span("validate-inventory"):
            await validate_inventory(order_id)
        
        with tracer.start_as_current_span("charge-payment") as payment_span:
            try:
                result = await charge_payment(order_id)
                payment_span.set_attribute("payment.id", result.id)
            except PaymentError as e:
                payment_span.record_exception(e)
                payment_span.set_status(StatusCode.ERROR, str(e))
                raise
```

---

## 9. SLA, SLO, SLI

```
SLI (Service Level Indicator): Metric measuring service health
  - Availability: % of successful requests
  - Latency: 99th percentile < 200ms
  - Error rate: errors / total requests

SLO (Service Level Objective): Target for SLI
  - Availability > 99.9% (43 min downtime/month)
  - P99 latency < 200ms for 99% of time windows
  
SLA (Service Level Agreement): Contract with penalties
  - "We guarantee 99.9% availability or refund 10%"

Error Budget = 1 - SLO target
  99.9% SLO → 0.1% error budget = 43.8 min/month
  
Error Budget Policy:
  - Budget remains: deploy freely, run experiments
  - Budget nearly exhausted: freeze releases, fix reliability
  - Budget exhausted: no new features until budget replenishes
```

### Alerting Strategy (Google's CRE)
```
Alert on symptoms, not causes:
  ✅ "Error rate > 5%" (symptom — user impact)
  ❌ "CPU > 80%" (cause — may not affect users)
  ❌ "Disk > 90%" (cause — gives time to react normally)

Page (wake someone up) only for:
  - SLO burning too fast (will exhaust budget before action)
  - Data loss or corruption
  - Security breach
  
Ticket (handle during business hours) for:
  - Slow SLO burn (plenty of budget remaining)
  - Minor reliability issues
```

---

## 10. Observability Stack (Docker Compose)

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:v2.48.0
    ports: ["9090:9090"]
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./rules:/etc/prometheus/rules
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=30d'

  grafana:
    image: grafana/grafana:10.2.0
    ports: ["3000:3000"]
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin123
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning

  alertmanager:
    image: prom/alertmanager:v0.26.0
    ports: ["9093:9093"]
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml

  loki:
    image: grafana/loki:2.9.0
    ports: ["3100:3100"]
    volumes:
      - loki-data:/loki

  tempo:
    image: grafana/tempo:2.3.0
    ports: ["4317:4317"]   # OTLP gRPC
    volumes:
      - tempo-data:/tmp/tempo

  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.90.0
    volumes:
      - ./otel-config.yml:/etc/otel-collector-config.yaml
    command: ["--config=/etc/otel-collector-config.yaml"]

volumes:
  prometheus-data:
  grafana-data:
  loki-data:
  tempo-data:
```

---

*Tài liệu liên quan: `observability/01-monitoring-basics.md` | `kubernetes/02-kubernetes-advanced.md` | `cicd/01-github-actions.md`*
