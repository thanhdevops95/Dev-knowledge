# 🎓 Traces & OpenTelemetry — Distributed tracing

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.1\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 11/06/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [Logs](02_logs-loki-elk.md)

> 🎯 *Master distributed tracing: **OpenTelemetry** (CNCF standard), **spans + trace**, **context propagation** across services, **sampling** strategy, **Tempo vs Jaeger vs Honeycomb**, instrument FastAPI + auto-instrument, correlate **traces ↔ logs ↔ metrics**.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **distributed tracing** model (trace + spans)
- [ ] **OpenTelemetry** components (SDK, Collector, Exporters)
- [ ] **Context propagation** (W3C TraceContext header)
- [ ] **Sampling** — head vs tail, ratio strategies
- [ ] Setup **Tempo** (Grafana traces)
- [ ] Auto-instrument **FastAPI + Postgres + Redis**
- [ ] Correlate **traces ↔ logs ↔ metrics** via trace_id
- [ ] So sánh **Tempo / Jaeger / Honeycomb / Datadog APM**

---

## 1️⃣ Distributed tracing — Mô hình

### Vấn đề

Request `POST /checkout` chậm 2s. Where?

```
Frontend → API Gateway → FastAPI → Postgres → Redis → Payment API → Email Service
                              ↑ 200ms      ↑ 5ms       ↑ 1800ms (← here!)
```

Without tracing: hard pinpoint. With tracing: see full waterfall.

### Trace = Cây Span

**Trace** = toàn bộ journey 1 request đi qua hệ thống. Mỗi đoạn nhỏ trong journey (gọi DB, gọi API ngoài, render template) là 1 **Span**. Span lồng nhau như cây — root span là entry point, children là sub-operation. Khi vẽ ra waterfall, bottleneck lộ ngay:

```
Trace ID: abc-123 (total 2050ms)
├─ Span: POST /checkout         (2050ms) ← root span
│  ├─ Span: DB.create_order      (50ms)
│  ├─ Span: cache.get_user        (5ms)
│  ├─ Span: payment.charge        (1800ms)  ← bottleneck
│  │  ├─ Span: HTTP /stripe        (1750ms)
│  │  │  └─ Span: SSL.connect       (200ms)
│  │  └─ Span: db.save_payment      (40ms)
│  └─ Span: email.send             (180ms)
```

### Giải phẫu Span

Mỗi Span là 1 object JSON chứa 7 trường chính: ID, parent ID, name, timestamp start/end, attributes (metadata custom), events (log point trong span), status. `trace_id` giống nhau giữa tất cả span trong cùng 1 trace — đây là "ID đoàn tàu" giúp ráp lại đường đi:

```json
{
  "trace_id": "abc-123",
  "span_id": "span-456",
  "parent_span_id": "span-444",
  "name": "POST /checkout",
  "start_time": "2026-05-23T14:32:01.000Z",
  "end_time": "2026-05-23T14:32:03.050Z",
  "attributes": {
    "http.method": "POST",
    "http.url": "/checkout",
    "http.status_code": 200,
    "user.id": "42"
  },
  "events": [
    { "name": "cache_miss", "timestamp": "..." }
  ],
  "status": "OK"
}
```

| Field | Purpose |
|---|---|
| `trace_id` | Unique per request (correlate cross-service) |
| `span_id` | Unique per span |
| `parent_span_id` | Tree structure |
| `name` | Operation name (`POST /checkout`, `db.query`) |
| `attributes` | Key-value metadata |
| `events` | Timestamped events within span |
| `status` | OK / ERROR |

---

## 2️⃣ OpenTelemetry — Chuẩn 2026

**OTel** = CNCF standard (graduated 2024). Vendor-neutral instrumentation.

### Các thành phần

OTel chia làm 3 lớp: **SDK** trong app (gọi `span.start()` thủ công hoặc auto-instrument lib), **OTel Collector** (sidecar/standalone — gom span từ nhiều app, batch, transform, export), và **backend** (Tempo, Jaeger, Datadog — nơi lưu + render trace). Collector ở giữa cho phép đổi backend mà không sửa app:

```
┌─────────────────┐
│   App (SDK)      │  Instrument code
│   span.start()    │
└────────┬────────┘
         │ OTLP protocol
         ▼
┌─────────────────┐
│ OTel Collector   │  Receive, process, batch, export
└────────┬────────┘
         │
   ┌─────┴─────┐
   ▼            ▼
[Tempo]      [Datadog]    (any backend)
```

### Tại sao dùng OTel?

Trước OTel, mỗi vendor (Jaeger, Zipkin, Datadog, New Relic) có SDK riêng. Đổi vendor = viết lại toàn bộ instrumentation. OTel là **chuẩn CNCF** (graduated 2024) giải bài này — instrument 1 lần, đổi backend bao nhiêu lần cũng được. Đây là lý do 2026 OTel là default lựa chọn:

- ✅ **Vendor-neutral** — switch backend without re-instrumenting.
- ✅ **Unified** — metrics + logs + traces single SDK.
- ✅ **Auto-instrumentation** — zero code change many frameworks.
- ✅ **Standard format** (OTLP) — most vendors support.

→ 2026: **always start with OTel**. Avoid vendor SDK lock-in.

---

## 3️⃣ Context propagation

Trace spans across services need **propagate trace context**.

### W3C TraceContext header

Khi Service A gọi Service B, **trace_id phải được truyền theo** — nếu không, B sinh trace mới và đường đi bị "đứt". W3C chuẩn hoá việc này qua HTTP header `traceparent` — chuỗi gồm version, trace_id (32 hex), parent_span_id (16 hex), flags. Mọi OTel SDK đều auto-inject + auto-extract header này:

```http
GET /api/users HTTP/1.1
traceparent: 00-abc1234567890abcdef1234567890abcd-1234567890abcdef-01
            └┬┘ └──────────── trace-id ────────────┘ └─ span-id ──┘ └flags┘
            ver
```

Service B receive request → extract → continue same trace.

### Propagation thủ công (Python)

```python
import httpx
from opentelemetry.propagate import inject

async def call_other_service(url):
    headers = {}
    inject(headers)            # ← Inject trace context
    async with httpx.AsyncClient() as client:
        return await client.get(url, headers=headers)
```

### Auto-propagation

OTel **auto-instrumentation** propagates automatically:
- HTTP client libs (requests, httpx, axios).
- gRPC.
- Message queues (Kafka, RabbitMQ).

→ Zero code change needed when use instrumented libs.

---

## 4️⃣ Cài đặt OTel + FastAPI

### Cài đặt

```bash
pip install \
  opentelemetry-distro \
  opentelemetry-exporter-otlp \
  opentelemetry-instrumentation-fastapi \
  opentelemetry-instrumentation-sqlalchemy \
  opentelemetry-instrumentation-redis \
  opentelemetry-instrumentation-httpx

opentelemetry-bootstrap --action=install     # Auto-install detected packages
```

### Code

```python
# app.py
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Setup tracer
resource = Resource.create({SERVICE_NAME: "acmeshop-api"})
provider = TracerProvider(resource=resource)
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="otel-collector:4317", insecure=True))
)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)        # ← Auto-instrument all endpoints
SQLAlchemyInstrumentor().instrument(engine=engine)   # ← All DB queries

# Custom span
@app.post("/checkout")
async def checkout(order: OrderCreate):
    with tracer.start_as_current_span("validate_order") as span:
        span.set_attribute("order.amount", order.amount)
        validate(order)
    with tracer.start_as_current_span("charge_payment") as span:
        result = await payment.charge(order.amount)
        span.set_attribute("payment.status", result.status)
    return {"status": "ok"}
```

### Đơn giản hơn nữa — Auto-instrumentation

```bash
# Zero code change!
opentelemetry-instrument \
  --traces_exporter otlp \
  --exporter_otlp_endpoint http://otel-collector:4317 \
  --service_name acmeshop-api \
  uvicorn app:app
```

→ Detects FastAPI/Flask/DB/Redis/HTTP automatically. Traces flowing.

---

## 5️⃣ OTel Collector

### Tại sao dùng Collector (thay vì ship thẳng tới backend)?

- ✅ **Buffer** — backend down, collector queue.
- ✅ **Process** — sample, filter, enrich, batch.
- ✅ **Multi-backend** — send to Tempo + Datadog same time.
- ✅ **Resource attribute** — add `cluster=prod`, `region=us-east`.

### Cấu hình

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc: { endpoint: 0.0.0.0:4317 }
      http: { endpoint: 0.0.0.0:4318 }

processors:
  batch:                                  # Batch before send
    timeout: 1s
    send_batch_size: 1024
  memory_limiter:                          # Prevent OOM
    check_interval: 1s
    limit_mib: 400
  attributes:
    actions:
    - key: env
      value: production
      action: insert

exporters:
  otlphttp/tempo:
    endpoint: http://tempo:4318
  prometheus:
    endpoint: 0.0.0.0:8889
  logging:
    loglevel: info

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [otlphttp/tempo, logging]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [prometheus]
```

→ Collector = ETL pipeline for telemetry.

### Deploy

```bash
docker run -d --name otel-collector \
  -p 4317:4317 -p 4318:4318 \
  -v $(pwd)/otel-collector-config.yaml:/etc/otel-collector-config.yaml \
  otel/opentelemetry-collector-contrib \
  --config=/etc/otel-collector-config.yaml
```

→ K8s: helm chart `opentelemetry-collector`.

---

## 6️⃣ Sampling — Kiểm soát cost

100% tracing = expensive at scale. **Sample**.

### Head sampling — Quyết định lúc bắt đầu

```yaml
# Sample 10%
processors:
  probabilistic_sampler:
    sampling_percentage: 10
```

→ Simple, predictable. **Lose detail** for sampled-out requests.

### Tail sampling — Quyết định lúc kết thúc

```yaml
# Keep ALL errors + slow, sample others 1%
processors:
  tail_sampling:
    decision_wait: 30s                    # Wait for trace complete
    policies:
    - name: errors-policy
      type: status_code
      status_code: { status_codes: [ERROR] }
    - name: slow-policy
      type: latency
      latency: { threshold_ms: 1000 }
    - name: probabilistic
      type: probabilistic
      probabilistic: { sampling_percentage: 1 }
```

→ **Smart** — never miss errors/slow. Sample healthy traffic.

→ **Recommended 2026**: tail sampling with rules.

### Ngân sách sampling rate

```
100K req/day × 100% sample      = 100K traces/day = 100MB
100K req/day × 10% sample        = 10K traces/day = 10MB
1M req/day × tail (keep errors)  = ~20K traces/day = 20MB (cost OK)
```

→ Tail sampling = best signal/cost ratio.

---

## 7️⃣ Tempo, Jaeger, Honeycomb — Các backend

### Tempo (của Grafana)

```bash
helm install tempo grafana/tempo -n monitoring
```

- ✅ Integrate Grafana stack (LGTM: Loki+Grafana+Tempo+Mimir).
- ✅ Object storage backend (S3, GCS) — cheap.
- ✅ **TraceQL** query language.
- ❌ Newer (2021), smaller community than Jaeger.

### Jaeger (CNCF)

```bash
helm install jaeger jaegertracing/jaeger -n monitoring
```

- ✅ Mature (CNCF graduated 2019), large community.
- ✅ UI rich, search by service/operation/duration.
- ✅ Cassandra/Elasticsearch backend.
- ❌ Heavier than Tempo.

### Honeycomb (thương mại)

- ✅ **Best DX** for tracing. Fast query.
- ✅ **High cardinality** events (Honeycomb's bet).
- ✅ Distributed trace exploration.
- ❌ $$$ paid.

### Datadog APM

- ✅ Integrated với metrics + logs + RUM.
- ✅ Code-level APM (line-level).
- ❌ $$$$.

### Chọn

| Use case | Pick |
|---|---|
| OSS + Grafana stack | **Tempo** |
| OSS + mature ecosystem | **Jaeger** |
| Best DX, willing to pay | **Honeycomb** |
| All-in-one observability $$$$ | **Datadog APM** |
| Cost-sensitive K8s | Tempo |

---

## 8️⃣ Tương quan traces ↔ logs ↔ metrics

Magic of OTel: **shared trace_id** unifies signals.

### Log enriched với trace_id

```python
import logging
from opentelemetry import trace

class TraceContextFilter(logging.Filter):
    def filter(self, record):
        span = trace.get_current_span()
        if span.is_recording():
            ctx = span.get_span_context()
            record.trace_id = format(ctx.trace_id, "032x")
            record.span_id = format(ctx.span_id, "016x")
        return True
```

→ Every log includes `trace_id`. From Loki:
```logql
{app="fastapi"} |= "abc1234567890abcdef"
```

→ Or from Grafana panel showing log: **click trace_id → jump Tempo trace view**. Cross-link in dashboard.

### Metric sinh ra từ traces

```yaml
# OTel Collector config
processors:
  spanmetrics:
    metrics_exporter: prometheus
```

→ Auto-generate metrics from traces:
- `http_server_duration_milliseconds_count{operation="GET /users"}`
- `http_server_duration_milliseconds_bucket{operation="GET /users", le="100"}`

→ RED metrics free from traces. No double instrumentation.

### Exemplars — Trace từ Prometheus

Prometheus histogram bucket có **exemplar** (trace_id sample). Click bucket trong Grafana → trace.

```promql
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

Hover slow point → exemplar trace_id → click → Tempo → full trace.

→ **2026 holy grail**: metrics → trace → log all interconnected. Investigation in seconds.

---

## 9️⃣ Cài đặt production của bạn

### Stack

```
FastAPI (OTel instrumented)
   ↓ OTLP gRPC
OTel Collector
   ↓ Tail sampling
   ├─► Tempo (traces)
   ├─► Prometheus (metrics, spanmetrics)
   └─► Loki (logs with trace_id)
        ↓
      Grafana (unified view)
```

### Deploy

```bash
# Helm
helm install otel-collector open-telemetry/opentelemetry-collector \
  -n monitoring --values otel-values.yaml

helm install tempo grafana/tempo -n monitoring
```

### Code app tối thiểu

```bash
# Dockerfile add
RUN opentelemetry-bootstrap --action=install

# CMD wrap
CMD ["opentelemetry-instrument", "uvicorn", "app:app", "--host", "0.0.0.0"]
```

```yaml
# K8s deployment env
env:
- name: OTEL_EXPORTER_OTLP_ENDPOINT
  value: "http://otel-collector:4317"
- name: OTEL_SERVICE_NAME
  value: "fastapi"
- name: OTEL_RESOURCE_ATTRIBUTES
  value: "deployment.environment=production"
```

→ Pod auto-trace every HTTP request + DB query + Redis + HTTPX call. Ship to OTel Collector → tail sample → Tempo.

### Grafana — Dashboard hợp nhất

```
Panel 1: P99 latency (from spanmetrics, with exemplars)
   → Click slow point → trace
Panel 2: Error rate
   → Click bar → filter trace by error
Panel 3: Logs panel (filtered by trace_id from URL var)
   → Auto-shows logs for selected trace
Panel 4: Service map (auto from spans)
```

→ Single dashboard answer: WHAT (metrics) + WHY (trace) + DETAIL (logs).

---

## 1️⃣0️⃣ Best practice

### Đặt tên Span

```
✅ Good: "POST /users", "db.query", "cache.get"
❌ Bad: "user_42_action_xyz", "/api/v1/users/12345"
```

→ **Generic name**, **specific attribute**. E.g., `name: "GET /users/:id"`, `attribute: user.id = 42`.

### Đừng trace mọi thứ

```python
# ❌ Span per loop iteration
for item in items:
    with tracer.start_as_current_span("process_item"):  # 1000 spans / trace
        process(item)

# ✅ 1 span batch
with tracer.start_as_current_span("process_batch") as span:
    span.set_attribute("batch.size", len(items))
    for item in items:
        process(item)
```

### Đặt status

```python
with tracer.start_as_current_span("query") as span:
    try:
        result = db.execute(sql)
        span.set_status(Status(StatusCode.OK))
    except Exception as e:
        span.set_status(Status(StatusCode.ERROR, str(e)))
        span.record_exception(e)
        raise
```

### PII — Đừng đưa vào attributes

```python
# ❌
span.set_attribute("user.email", email)
span.set_attribute("user.password", password)

# ✅
span.set_attribute("user.id", user_id)        # Just ID
```

→ Spans + attributes saved in backend. Treat like logs — no PII.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **100% sampling** → Tempo OOM, $$$$. Tail sampling 1-10% normal + 100% errors.
2. **High cardinality attribute** (`user.id`, `request.id`) → slow query. Use as needed but watch.
3. **Skip context propagation** → broken traces (each service own root span). Use OTel auto-instrument.
4. **PII in spans** → backend = log clone. Mask.
5. **Manual span everywhere** → noise. Auto-instrument 80%, custom 20% business spans.

---

## 🧠 Tự kiểm tra (Self-check)

1. **Trace** vs **Span** — relationship?
2. **OpenTelemetry** — 3 components?
3. **Head sampling** vs **Tail sampling** — khi nào dùng cái nào?
4. **W3C TraceContext** — header tên gì? Vai trò?
5. Correlate **traces ↔ logs ↔ metrics** — chìa khoá?

<details>
<summary>Gợi ý đáp án</summary>

1. **Trace** = full request flow, identified by `trace_id`. **Span** = single operation within trace (HTTP request, DB query, function call), has `span_id` + optional `parent_span_id`. Trace = tree of spans. Visualized as waterfall.

2. (a) **SDK** (in app, instrument code, create spans). (b) **Collector** (receive, process, export). (c) **Exporters** (send to backend: Tempo, Jaeger, Datadog). Plus auto-instrumentation libraries.

3. **Head sampling**: decide at start (e.g., 10% requests). Simple, predictable, but **lose errors** if sampled out. **Tail sampling**: decide at end after full trace (e.g., always keep errors + slow + 1% normal). Smart, best signal/cost, but needs OTel Collector buffer. **2026 default**: tail with rules.

4. **`traceparent`** header (`00-trace_id-span_id-flags`). Service receive → extract → continue same trace (new spans as children). Service make outbound call → inject header. Auto-handled by OTel HTTP instrumentation.

5. **Shared `trace_id`**. (a) Logs include `trace_id` (logger filter from current span context). (b) Metrics include **exemplars** (trace_id for sample histogram bucket). (c) Span attributes include service/user context. Grafana cross-link: click metric exemplar → Tempo trace → click trace span → Loki logs filtered by trace_id.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Install OTel + auto-instrument FastAPI

```bash
pip install opentelemetry-distro
opentelemetry-bootstrap --action=install

opentelemetry-instrument \
  --traces_exporter otlp \
  --exporter_otlp_endpoint http://otel-collector:4317 \
  --service_name myapp \
  uvicorn app:app
```

### Custom span

```python
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("name") as span:
    span.set_attribute("key", "val")
    span.add_event("event_name")
    # work
```

### Propagation

```python
from opentelemetry.propagate import inject
headers = {}
inject(headers)
requests.get(url, headers=headers)
```

### Tail sampling

```yaml
processors:
  tail_sampling:
    decision_wait: 30s
    policies:
    - type: status_code
      status_code: { status_codes: [ERROR] }
    - type: latency
      latency: { threshold_ms: 1000 }
    - type: probabilistic
      probabilistic: { sampling_percentage: 1 }
```

### Backends

```
Tempo       Grafana stack, S3, TraceQL
Jaeger       CNCF, mature
Honeycomb    Best DX, $$
Datadog APM  $$$
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Distributed tracing** | Track request across services |
| **Trace** | Full request flow |
| **Span** | Single operation in trace |
| **Trace ID / Span ID** | Unique identifiers |
| **Parent span ID** | Tree structure |
| **OpenTelemetry (OTel)** | CNCF instrumentation standard |
| **OTLP** | OTel Protocol (gRPC/HTTP) |
| **OTel Collector** | Process + export pipeline |
| **Auto-instrumentation** | Zero-code instrumentation |
| **Context propagation** | Pass trace_id across services |
| **W3C TraceContext** | Standard header format |
| **Head sampling** | Decision at start |
| **Tail sampling** | Decision at end (after full trace) |
| **Tempo / Jaeger / Honeycomb** | Trace backends |
| **Exemplar** | Trace ID in metric sample (Prometheus) |
| **Spanmetrics** | Auto-derive metrics from spans |
| **TraceQL** | Tempo query language |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [Logs — Loki, ELK, structured logging](02_logs-loki-elk.md)
- ➡️ **Bài tiếp theo:** [Grafana & Alerting — Unified dashboard + alert routing](04_grafana-and-alerting.md)
- ↑ **Về cụm:** [observability README](../../README.md)

### 🌐 Tài nguyên tham khảo khác
- 📖 [OpenTelemetry docs](https://opentelemetry.io/)
- 📖 [Tempo docs](https://grafana.com/docs/tempo/latest/)
- 📖 [Jaeger docs](https://www.jaegertracing.io/)
- 📖 [Honeycomb learn](https://www.honeycomb.io/blog) — Charity Majors
- 📖 [W3C TraceContext spec](https://www.w3.org/TR/trace-context/)
- 📖 [Tail-sampling article](https://opentelemetry.io/docs/concepts/sampling/)

---

> 🎯 *Sau bài này distributed tracing flowing. Bài cuối dạy **Grafana + Alerting** — unified view + alerts.*

---

## 📜 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước Trace Tree of Spans + Span anatomy + Components + Why OTel + W3C TraceContext header.
- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Observability sprint #4.
- **v1.1.1 (11/06/2026)** — Việt hoá heading nội dung mô tả sang tiếng Việt (giữ thuật ngữ/brand/param) theo Vietnamese-first.
