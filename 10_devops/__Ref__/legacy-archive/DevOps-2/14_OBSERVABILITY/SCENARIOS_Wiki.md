# 🚨 Tình huống Thực chiến - Observability

Đây là 5 tình huống thực tế mà DevOps Engineer thường gặp khi vận hành Monitoring & Logging.

---

## Scenario 1: Alert Fatigue - Quá nhiều alerts, team ignore

### 📋 Bối cảnh

Team nhận **100+ alerts/ngày**. Mọi người bắt đầu ignore Slack channel.

> "Ô cái alert nào cũng warning, chắc không quan trọng đâu"

Kết quả: Outage thật xảy ra, không ai để ý.

### 🔍 Triệu chứng

```
Slack #alerts channel:
⚠️ [WARN] CPU > 70% on web-1  
⚠️ [WARN] Memory > 60% on web-2
⚠️ [WARN] Disk > 50% on db-1
⚠️ [WARN] Response time > 100ms
... (100 messages/day)

Team: *mutes channel*
```

### 🕵️ Điều tra

```yaml
# Prometheus alerting rules
groups:
- name: basic
  rules:
  - alert: HighCPU
    expr: cpu_usage > 70  # Threshold quá thấp
    for: 1m                # Duration quá ngắn
    labels:
      severity: warning   # Mọi thứ đều warning
```

### 💡 Giải pháp

**1. Review và categorize alerts:**

| Severity | Criteria | Action |
|----------|----------|--------|
| **Critical** | Service down, data loss | PagerDuty, wake up on-call |
| **Warning** | Degraded performance | Slack, fix trong work hours |
| **Info** | Anomaly, cần investigate | Dashboard only |

**2. Tune thresholds:**

```yaml
# Thay vì
- alert: HighCPU
  expr: cpu_usage > 70
  for: 1m

# Đổi thành
- alert: HighCPU
  expr: cpu_usage > 90  # Higher threshold
  for: 10m              # Sustained issue
  labels:
    severity: warning  # Chỉ warning, không critical
```

**3. Alert on symptoms, not causes:**

```yaml
# ❌ Quá chi tiết (causes)
- alert: HighCPU
- alert: HighMemory
- alert: HighDisk
- alert: SlowQuery

# ✅ Focus vào user impact (symptoms)
- alert: HighErrorRate
  expr: rate(http_errors[5m]) / rate(http_total[5m]) > 0.01

- alert: HighLatency
  expr: histogram_quantile(0.99, http_duration) > 1
```

**4. Silence recurring noise:**

```bash
# Prometheus Alertmanager silence
amtool silence add alertname=HighCPU instance="noisy-server"
```

**5. Track alert quality:**

```yaml
# Dashboard: Alert Metrics
- Alerts per day
- False positive rate
- Mean Time to Acknowledge
- Alerts that led to action
```

### 🧠 Bài học

- **Không alert = không biết. Quá nhiều alert = ignore** - Balance
- **Alert on symptoms** - User impact, không internal metrics
- **Review alerts monthly** - Xóa những cái không actionable
- **Severity levels có nghĩa** - Critical = wake someone up

---

## Scenario 2: "Có alert nhưng không biết root cause"

### 📋 Bối cảnh

Alert: "Error rate > 5%"

Nhưng:

- Error rate ở đâu?
- Bắt đầu từ khi nào?
- Do component nào?
- Do deploy mới hay load tăng?

### 🔍 Triệu chứng

```
Alert: Error rate high!
You: *frantically SSHing to 20 servers*
You: *grepping logs manually*
You: *45 minutes later* "Aha! Found it!"
```

### 🕵️ Điều tra

Thiếu **correlated data**:

- Metrics có, nhưng không link với logs
- Logs có, nhưng không biết trace
- Events có, nhưng không timeline

### 💡 Giải pháp

**1. Structured logging với correlation IDs:**

```python
# App code
import uuid

@app.before_request
def add_trace_id():
    request.trace_id = request.headers.get('X-Trace-ID', str(uuid.uuid4()))

@app.after_request  
def log_request(response):
    logger.info("Request completed", extra={
        "trace_id": request.trace_id,
        "path": request.path,
        "status": response.status_code,
        "duration": request.duration
    })
```

**2. Grafana dashboards với drill-down:**

```yaml
# Dashboard layout
Row 1: Overview metrics (error rate, latency, throughput)
Row 2: Breakdown by service
Row 3: Breakdown by endpoint
Row 4: Recent changes (deployments, config changes)
Row 5: Link to logs (Loki/Elasticsearch)
```

**3. Annotations cho events:**

```bash
# Deploy annotation
curl -X POST http://grafana/api/annotations \
  -H "Content-Type: application/json" \
  -d '{
    "time": 1609459200000,
    "text": "Deploy v1.2.3",
    "tags": ["deploy", "production"]
  }'
```

**4. Distributed tracing:**

```yaml
# Jaeger/Zipkin integration
Trace ID: abc123
├── web-frontend (50ms)
│   └── api-gateway (45ms)
│       ├── user-service (20ms) ← Slow!
│       └── order-service (10ms)
```

### 🧠 Bài học

- **Metrics → Logs → Traces** - Three pillars linked
- **Correlation IDs** - Trace request across services
- **Timeline of changes** - Annotations cho deploys, config
- **Pre-built dashboards** - Đừng build khi có incident

---

## Scenario 3: Prometheus OOM - Monitoring down

### 📋 Bối cảnh

Prometheus server bị **OOM killed**. Không có metrics trong 2 tiếng.

> "Monitoring nên stable nhất, sao lại down?"

### 🔍 Triệu chứng

```bash
kubectl get pods -n monitoring
# prometheus-0   0/1   OOMKilled   15   2h

dmesg | grep -i oom
# Out of memory: Kill process prometheus
```

### 🕵️ Điều tra

```yaml
# Prometheus TSDB metrics
prometheus_tsdb_head_series: 2,500,000  # Quá nhiều time series!
prometheus_tsdb_head_chunks_created_total: increasing rapidly

# High cardinality labels
rate(http_requests{user_id="..."}[5m])  # Mỗi user = 1 series!
```

### 💡 Giải pháp

**1. Tìm high cardinality metrics:**

```promql
# Query top series
topk(10, count by (__name__)({__name__=~".+"}))

# Output:
# http_requests_total{user_id=...}: 500,000 series  ← Problem!
```

**2. Remove high cardinality labels:**

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'app'
    metric_relabel_configs:
    - source_labels: [user_id]
      action: drop  # Không lưu user_id label
```

**3. Tăng resources:**

```yaml
# Prometheus statefulset
resources:
  requests:
    memory: "4Gi"
  limits:
    memory: "8Gi"
```

**4. Retention và compaction:**

```yaml
# prometheus args
--storage.tsdb.retention.time=15d  # Giảm từ 30d
--storage.tsdb.retention.size=50GB
```

**5. Remote storage cho long-term:**

```yaml
# Gửi data ra Thanos/Cortex
remote_write:
  - url: "http://thanos-receive:19291/api/v1/receive"
```

### 🧠 Bài học

- **High cardinality = OOM** - Đừng dùng user_id, session_id làm labels
- **Monitor the monitoring** - Prometheus cũng cần được monitor
- **Retention limits** - Không giữ data forever
- **Remote storage** - Cho long-term queries

---

## Scenario 4: Log volume explosion - 100GB/day

### 📋 Bối cảnh

Elasticsearch cluster đầy disk. Log ingestion rate tăng từ 10GB → **100GB/day**.

### 🔍 Triệu chứng

```bash
# Elasticsearch
GET _cat/indices?v
# logs-2024.01.01   100gb   <- Huge!

# Kibana shows
# Top source: payment-service
# Log level: DEBUG ← Ai đã bật debug?
```

### 🕵️ Điều tra

```bash
# Kiểm tra log levels
kubectl logs payment-service | head -100
# 2024-01-01 DEBUG: Processing request...
# 2024-01-01 DEBUG: Validating input...
# 2024-01-01 DEBUG: Calling external API...
# (1000 DEBUG lines per request!)
```

### 💡 Giải pháp

**1. Set log levels via environment:**

```yaml
# deployment.yaml
env:
  - name: LOG_LEVEL
    value: "INFO"  # Không "DEBUG" trên production!
```

**2. Log sampling:**

```python
# Chỉ log 1% DEBUG messages
import random

if log_level == "DEBUG" and random.random() > 0.01:
    return  # Skip 99% DEBUG logs
```

**3. Index lifecycle management:**

```json
// Elasticsearch ILM policy
{
  "policy": {
    "phases": {
      "hot": { "actions": {} },
      "warm": {
        "min_age": "7d",
        "actions": { "shrink": { "number_of_shards": 1 } }
      },
      "delete": {
        "min_age": "30d",
        "actions": { "delete": {} }
      }
    }
  }
}
```

**4. Log streaming filter:**

```yaml
# Fluentd config
<filter **>
  @type grep
  <exclude>
    key log_level
    pattern /DEBUG/
  </exclude>
</filter>
```

**5. Cost monitoring:**

```yaml
# Grafana dashboard
- Log volume per service per day
- Cost per GB
- Alert if volume increases 50%
```

### 🧠 Bài học

- **DEBUG logs ≠ production** - Chỉ bật khi debug
- **Log costs money** - 100GB/day = $$$
- **ILM for retention** - Tự động xóa logs cũ
- **Sampling cho high-volume** - Không cần 100% logs

---

## Scenario 5: Dashboard quá chậm - Không xem được khi incident

### 📋 Bối cảnh

Incident xảy ra. Mở Grafana dashboard...

> Loading... Loading... Timeout!

Chính lúc cần nhất thì dashboard chậm như rùa.

### 🔍 Triệu chứng

```
Grafana dashboard load time:
- Normal: 2-3 seconds
- During incident: 60+ seconds or timeout

Prometheus:
- Query latency: 30+ seconds
- Memory usage: 95%
```

### 🕵️ Điều tra

```yaml
# Heavy queries
rate(http_requests_total[1h])  # 1 hour range, nhiều data
sum by (path) (rate(...))      # High cardinality
```

### 💡 Giải pháp

**1. Optimize queries:**

```yaml
# Thay vì
rate(http_requests_total[1h])

# Dùng
rate(http_requests_total[5m])  # Shorter range

# Hoặc pre-recorded rules
```

**2. Recording rules:**

```yaml
# prometheus-rules.yml
groups:
  - name: precomputed
    rules:
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(http_requests_total[5m]))
```

**3. Dashboard time range:**

```yaml
# Grafana dashboard settings
Time range: Last 6 hours  # Không Last 30 days!
Refresh: 1m during incident, 5m normal
```

**4. Separate incident dashboards:**

```yaml
# incident-dashboard.json
# Chỉ có essential metrics
# Pre-optimized queries
# Minimal time range
```

**5. Prometheus query cache:**

```yaml
# Thanos Query Frontend
--query-frontend.compress-responses
--query-range.response-cache-max-freshness=1m
```

### 🧠 Bài học

- **Dashboard phải fast** - 2-3 seconds max
- **Recording rules** - Pre-compute heavy queries
- **Incident dashboards** - Separate, optimized
- **Test dashboards under load** - Trước khi incident

---

## 📝 Observability Checklist

- [ ] Three pillars: Metrics + Logs + Traces
- [ ] Correlation IDs across services
- [ ] Alert severity levels defined
- [ ] False positive rate < 10%
- [ ] Dashboard load time < 3s
- [ ] Log retention policy
- [ ] Recording rules for heavy queries
- [ ] Monitoring for the monitoring
