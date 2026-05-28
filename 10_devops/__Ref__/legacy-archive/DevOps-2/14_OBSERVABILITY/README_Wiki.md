# Module 14: Observability (Monitoring & Logging)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Observability** | - | Khả năng quan sát - Hiểu hệ thống qua outputs |
| **Monitoring** | - | Giám sám - Theo dõi metrics và alerts |
| **Logging** | - | Ghi log - Thu thập và lưu trữ log |
| **Metrics** | - | Chỉ số đo lường (CPU, memory, requests) |
| **Traces** | - | Theo dõi request đi qua các services |
| **Alert** | - | Cảnh báo khi có vấn đề |
| **Prometheus** | - | Tool thu thập metrics phổ biến |
| **Grafana** | - | Tool visualization dashboards |
| **ELK Stack** | - | Elasticsearch + Logstash + Kibana - Logging stack |
| **Loki** | - | Log aggregation system của Grafana |
| **Jaeger** | - | Distributed tracing system |
| **SLI** | - | Service Level Indicator - Chỉ số đo |
| **Dashboard** | - | Bảng điều khiển hiển thị metrics |

---

## 📖 Observability là gì? (Định nghĩa từ gốc)

### Trước hết: Monitoring là gì?

**Monitoring = Theo dõi những thứ bạn biết trước có thể hỏng.**

Bạn đặt alerts cho những metrics đã biết:

- CPU > 90% → Alert
- Disk > 80% → Alert
- Service down → Alert

**Vấn đề với Monitoring truyền thống:**

| Vấn đề | Ví dụ |
|--------|-------|
| **Chỉ biết "known unknowns"** | Bạn alert cho CPU cao, nhưng vấn đề thực sự là memory leak |
| **Không biết "tại sao"** | Alert nói "CPU cao" nhưng không nói tại sao |
| **Khó debug distributed systems** | Request đi qua 10 services, lỗi ở đâu? |

### Observability giải quyết

> **Observability = Khả năng hiểu trạng thái bên trong hệ thống thông qua những gì nó xuất ra (outputs)**

Sự khác biệt quan trọng:

| Monitoring | Observability |
|------------|---------------|
| Hỏi: "Hệ thống có hoạt động không?" | Hỏi: "Tại sao hệ thống hoạt động như vậy?" |
| Chỉ biết điều đã đặt alert | Có thể khám phá vấn đề mới |
| Check known failure modes | Explore unknown unknowns |
| Dashboard cố định | Ad-hoc queries |

**Ẩn dụ:**

```
Monitoring = Đèn check engine trên xe
            "Có vấn đề!" - Nhưng vấn đề gì?

Observability = Diagnostic port (OBD-II)
            "P0301 - Cylinder 1 misfire, 
             caused by: faulty spark plug"
            → Biết chính xác vấn đề gì, ở đâu
```

### Ba trụ cột của Observability

Để có observability, bạn cần **ba loại data** bổ sung cho nhau:

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY                             │
├───────────────────┬─────────────────┬───────────────────────┤
│      METRICS      │      LOGS       │       TRACES          │
│   (What?)         │    (Why?)       │     (Where?)          │
├───────────────────┼─────────────────┼───────────────────────┤
│ CPU: 95%          │ ERROR: DB conn  │ API→Auth→DB (500ms)   │
│ Requests: 1000/s  │ timeout at...   │         ↑ slow!       │
│ Errors: 5%        │ Stack trace...  │                       │
└───────────────────┴─────────────────┴───────────────────────┘
```

---

## 🎬 Câu chuyện thực tế

3h sáng, bạn nhận được alert:

> "Error rate > 5%!"

**Với chỉ Monitoring:**

- "Error rate cao" - OK, nhưng tại sao?
- SSH vào server, grep logs thủ công
- 2 tiếng sau mới tìm ra nguyên nhân

**Với Observability:**

1. **Metrics:** Error rate tăng từ 10:45 PM, correlate với memory spike
2. **Logs:** Filter logs có error code, thấy "Connection pool exhausted"
3. **Traces:** Trace request thấy bottleneck ở Database service

→ 15 phút xác định: Database connection pool quá nhỏ cho traffic spike

---

## 📖 Three Pillars of Observability

**Observability** là khả năng hiểu trạng thái bên trong của hệ thống thông qua những gì nó outputs. Ba pillars bổ sung cho nhau:

| Pillar | Câu hỏi trả lời | Đặc điểm |
|--------|-----------------|----------|
| **Metrics** | What's happening? | Numerical, aggregated, cheap to store |
| **Logs** | Why did it happen? | Text, detailed, context-rich |
| **Traces** | Where in the system? | Request flow qua nhiều services |

### 1. Metrics - "Chuyện gì đang xảy ra?"

Metrics là các **con số** được thu thập theo thời gian. Giúp bạn xây dựng dashboards và alerts.

```
CPU: 85%           ← Gần ngưỡng nguy hiểm?
Memory: 3.2GB / 4GB ← Sắp hết RAM?
Requests: 1000/min  ← Traffic bình thường hay spike?
Error rate: 2%      ← Có vấn đề với app?
```

**Khi nào dùng Metrics:**

- Dashboard overview của hệ thống
- Alerting (CPU > 90% → alert)
- Capacity planning (cần thêm server không?)
- SLO tracking (99.9% uptime)

**Tools:** Prometheus, Grafana, Datadog, CloudWatch

### 2. Logs - "Tại sao lại xảy ra?"

Logs là **text** ghi lại các events. Khi metrics cho thấy có vấn đề, logs giúp debug tại sao.

```
[2024-01-15 10:00:01] ERROR Database connection timeout
[2024-01-15 10:00:02] ERROR Retry 1/3 failed
[2024-01-15 10:00:03] ERROR Service unavailable
```

> 💡 **Tip:** Log theo format chuẩn (JSON) để dễ search và filter. Thêm correlation ID để track request qua nhiều services.

**Khi nào dùng Logs:**

- Debug errors và exceptions
- Audit trail (ai làm gì, khi nào)
- Security investigation
- Debugging complex issues

**Tools:** ELK Stack (Elasticsearch, Logstash, Kibana), Loki, CloudWatch Logs

### 3. Traces - "Ở đâu trong hệ thống?"

Trong microservices, một request đi qua nhiều services. Trace cho thấy **path** và **time** ở mỗi service.

```
Request → API Gateway (5ms) → Auth Service (10ms) → Database (500ms!) → Response
                                                          ↑
                                                    Bottleneck here!
```

**Khi nào dùng Traces:**

- Performance debugging trong microservices
- Tìm bottleneck
- Hiểu dependencies giữa services

**Tools:** Jaeger, Zipkin, AWS X-Ray, OpenTelemetry

---

## 🔧 Prometheus + Grafana

**Stack phổ biến nhất cho monitoring:**

- **Prometheus**: Thu thập và lưu trữ metrics (time-series database)
- **Grafana**: Visualization dashboards, alerting

### Prometheus Config

```yaml
# prometheus.yml
global:
  scrape_interval: 15s  # Thu thập metrics mỗi 15 giây

scrape_configs:
  - job_name: 'myapp'
    static_configs:
      - targets: ['localhost:8080']  # App expose metrics ở port 8080
```

**Giải thích:**

| Field | Ý nghĩa |
|-------|---------|
| `scrape_interval` | Prometheus pull metrics mỗi 15s |
| `job_name` | Tên để group metrics |
| `targets` | Endpoints expose /metrics |

### App Metrics - Expose trong code

Để Prometheus thu thập được, app phải expose metrics ở endpoint `/metrics`:

```python
from prometheus_client import Counter, Histogram, start_http_server

# Định nghĩa metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total requests')
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency')

# Tự động đo latency với decorator
@REQUEST_LATENCY.time()
def handle_request():
    REQUEST_COUNT.inc()  # Tăng counter mỗi request
    # ... business logic

# Expose metrics ở port 8080
start_http_server(8080)
```

**Các loại metrics:**

| Type | Use case | Ví dụ |
|------|----------|-------|
| **Counter** | Luôn tăng | Total requests, errors |
| **Gauge** | Lên xuống | CPU %, active connections |
| **Histogram** | Distribution | Request latency |

---

## 📊 Key Metrics

### USE Method

- **Utilization**: % resource in use
- **Saturation**: Queue length
- **Errors**: Error count

### RED Method

- **Rate**: Requests/second
- **Errors**: Failed requests
- **Duration**: Latency

---

## 📝 Tổng kết

✅ Metrics, Logs, Traces  
✅ Prometheus & Grafana  
✅ USE and RED methods  

👉 **[LABS.md](LABS.md)** | **[SCENARIOS.md](SCENARIOS.md)**
