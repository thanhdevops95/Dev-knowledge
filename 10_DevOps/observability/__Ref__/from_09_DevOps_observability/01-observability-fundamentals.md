# 📈 Observability — Logs, Metrics & Traces

> `[INTERMEDIATE → ADVANCED]` — Hiểu hệ thống đang chạy thế nào

---

## Ba trụ cột Observability

```
                    Observability
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       Logs          Metrics         Traces
    "Đã xảy ra gì"  "Đang thế nào"  "Đi qua đâu"

    Error messages    CPU 85%         Request path:
    Stack traces      Memory 2GB      API → Auth → DB → Cache
    Audit events      Latency P99     Bottleneck ở đâu?
```

---

## 1. Structured Logging — Logs có cấu trúc

```javascript
// ❌ Unstructured log: khó parse, khó search
console.log('User 123 ordered product 456 for $50');

// ✅ Structured log: JSON format
const logger = require('pino')();

logger.info({
    event: 'order_created',
    userId: 123,
    orderId: 'ORD-789',
    productId: 456,
    amount: 50,
    currency: 'USD',
}, 'Order created successfully');

// Output:
// {"level":30,"time":1709553600000,"event":"order_created",
//  "userId":123,"orderId":"ORD-789","amount":50,
//  "msg":"Order created successfully"}
```

### Log Levels

```
FATAL  → Hệ thống sắp chết (DB connection lost)
ERROR  → Lỗi cần xử lý ngay (payment failed)
WARN   → Sắp có vấn đề (disk 90%, rate limit approaching)
INFO   → Events quan trọng (user login, order created)
DEBUG  → Chi tiết cho debugging (request payload, SQL query)
TRACE  → Cực kỳ chi tiết (function entry/exit)

Production: INFO + WARN + ERROR + FATAL
Development: DEBUG + tất cả trên
```

### Correlation ID — Theo dõi request xuyên services

```javascript
import { v4 as uuid } from 'uuid';

// Middleware: gắn correlationId cho mỗi request
app.use((req, res, next) => {
    req.correlationId = req.headers['x-correlation-id'] || uuid();
    res.setHeader('x-correlation-id', req.correlationId);
    next();
});

// Logger mang theo correlationId
app.get('/api/orders/:id', async (req, res) => {
    const logger = baseLogger.child({ correlationId: req.correlationId });

    logger.info({ orderId: req.params.id }, 'Fetching order');

    const order = await orderService.findById(req.params.id);
    // orderService cũng log với CÙNG correlationId
    // → Tìm tất cả logs liên quan 1 request: search correlationId!

    res.json(order);
});
```

---

## 2. Metrics — Đo lường hệ thống

### Prometheus + Grafana

```javascript
// prom-client — Expose metrics cho Prometheus scrape
import { Registry, Counter, Histogram, Gauge, collectDefaultMetrics } from 'prom-client';

const register = new Registry();
collectDefaultMetrics({ register });   // CPU, memory, event loop...

// Counter: chỉ tăng (requests, errors)
const httpRequests = new Counter({
    name: 'http_requests_total',
    help: 'Total HTTP requests',
    labelNames: ['method', 'path', 'status'],
    registers: [register],
});

// Histogram: phân bố giá trị (latency, response size)
const httpDuration = new Histogram({
    name: 'http_request_duration_seconds',
    help: 'HTTP request duration in seconds',
    labelNames: ['method', 'path'],
    buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5],
    registers: [register],
});

// Gauge: lên xuống (active connections, queue size)
const activeConnections = new Gauge({
    name: 'active_connections',
    help: 'Number of active connections',
    registers: [register],
});

// Middleware: track metrics tự động
app.use((req, res, next) => {
    const end = httpDuration.startTimer({ method: req.method, path: req.route?.path });
    activeConnections.inc();

    res.on('finish', () => {
        end();
        activeConnections.dec();
        httpRequests.inc({ method: req.method, path: req.route?.path, status: res.statusCode });
    });
    next();
});

// Endpoint cho Prometheus scrape
app.get('/metrics', async (req, res) => {
    res.set('Content-Type', register.contentType);
    res.end(await register.metrics());
});
```

### RED & USE Methods

```
RED Method (Services):
  Rate   — Requests per second
  Errors — Error rate (%)
  Duration — Latency (P50, P95, P99)

USE Method (Infrastructure):
  Utilization — % resource được sử dụng (CPU 75%)
  Saturation  — Mức độ quá tải (queue length)
  Errors      — Error count
```

---

## 3. Distributed Tracing — Xuyên services

```
Request flow qua nhiều services:
  Client → API Gateway → User Service → Order Service → Payment → DB

Trace: toàn bộ journey của 1 request
  Span: 1 operation trong trace

Trace ID: abc-123
├── Span 1: API Gateway (2ms)
├── Span 2: User Service (15ms)
│   └── Span 3: User DB Query (8ms)
├── Span 4: Order Service (50ms)
│   ├── Span 5: Validate Order (5ms)
│   └── Span 6: Payment Service (40ms)
│       └── Span 7: Stripe API call (35ms)  ← Bottleneck!
└── Total: 67ms
```

### OpenTelemetry — Standard cho tracing

```javascript
// setup.js — OpenTelemetry initialization
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

const sdk = new NodeSDK({
    traceExporter: new OTLPTraceExporter({
        url: 'http://jaeger:4318/v1/traces',  // Jaeger / Zipkin / Tempo
    }),
    instrumentations: [
        getNodeAutoInstrumentations({
            // Tự động trace HTTP, Express, DB queries, Redis...
            '@opentelemetry/instrumentation-express': { enabled: true },
            '@opentelemetry/instrumentation-pg': { enabled: true },
            '@opentelemetry/instrumentation-redis': { enabled: true },
        }),
    ],
});

sdk.start();

// Custom spans cho business logic
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('order-service');

async function processOrder(order) {
    return tracer.startActiveSpan('processOrder', async (span) => {
        span.setAttribute('order.id', order.id);
        span.setAttribute('order.total', order.total);

        try {
            await validateOrder(order);
            await chargePayment(order);
            await updateInventory(order);
            span.setStatus({ code: SpanStatusCode.OK });
        } catch (err) {
            span.setStatus({ code: SpanStatusCode.ERROR, message: err.message });
            span.recordException(err);
            throw err;
        } finally {
            span.end();
        }
    });
}
```

---

## 4. Alerting — Cảnh báo thông minh

```yaml
# Prometheus Alert Rules
groups:
  - name: application
    rules:
      # Error rate > 5% trong 5 phút
      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status=~"5.."}[5m])
          / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate: {{ $value | humanizePercentage }}"

      # P99 latency > 2 giây
      - alert: HighLatency
        expr: |
          histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning

      # Memory > 90%
      - alert: HighMemory
        expr: |
          (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
          / node_memory_MemTotal_bytes > 0.9
        for: 10m
        labels:
          severity: warning
```

---

## 5. Observability Stack

```
Popular stacks:

┌─────────────────────────────────────────┐
│           Grafana (Dashboard)           │
├──────────┬──────────┬───────────────────┤
│ Loki     │Prometheus│  Tempo            │
│ (Logs)   │(Metrics) │  (Traces)         │
└──────────┴──────────┴───────────────────┘
         ↑ Grafana Stack (tightly integrated)

Other options:
  Logs:    ELK (Elasticsearch + Logstash + Kibana)
  Metrics: Datadog, New Relic, CloudWatch
  Traces:  Jaeger, Zipkin, AWS X-Ray
  All-in-1: Datadog, New Relic, Dynatrace
```

---

## Các lỗi thường gặp

```
❌ Sai: Log mọi thứ ở DEBUG level trong production
✅ Đúng: Production = INFO+. Dynamic log level switching cho debug khi cần.

❌ Sai: Metrics cardinality quá cao (label = userId!)
✅ Đúng: Labels ít giá trị: method, path, status. KHÔNG dùng userId, requestId.

❌ Sai: Alert mọi thứ → alert fatigue
✅ Đúng: Chỉ alert actionable items. Symptom-based (error rate) > cause-based (CPU).
```

---

## Bài tập thực hành

- [ ] Thêm structured logging vào 1 project thực
- [ ] Setup Prometheus + Grafana, tạo dashboard cho API
- [ ] Tạo alert khi error rate > 1%
- [ ] Add OpenTelemetry auto-instrumentation vào FastAPI/Express

---

## Tài nguyên thêm

- [OpenTelemetry Docs](https://opentelemetry.io/docs/) — Standard
- [Grafana Tutorials](https://grafana.com/tutorials/) — Dashboard
- [Google SRE Book: Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/)
