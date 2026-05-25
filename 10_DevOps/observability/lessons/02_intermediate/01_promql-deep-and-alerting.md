# 🎓 PromQL deep + Recording rules + Alerting strategy

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Intermediate\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~25 phút\
> **Prerequisites:** [00_intermediate-overview.md](00_intermediate-overview.md), Prometheus basic queries

> 🎯 *Basic: `rate(http_requests_total[5m])`. Production: histogram quantile + recording rules + multi-window burn rate alerts + Alertmanager routing tree + Mimir long-term. Bài này dạy PromQL fluent + alerting strategy thực tế.*

## 🎯 Sau bài này bạn sẽ

- [ ] Dùng **PromQL functions** advanced: `histogram_quantile`, `predict_linear`, `quantile_over_time`
- [ ] Viết **recording rules** giảm 90% query CPU
- [ ] Viết **alerting rules** với **multi-window burn rate** (Google SRE pattern)
- [ ] Setup **Alertmanager** routing tree + silence + inhibition
- [ ] **Cardinality control** — tránh metrics explosion
- [ ] **Federation + Mimir/Thanos** cho long-term + multi-cluster
- [ ] Tránh **8 alert anti-patterns** phổ biến

---

## Tình huống — Alert noise 200 lần/ngày, on-call rage

On-call SRE rotation 1 tuần. Last week:
- 200+ alerts/day. Mostly "CPU > 80%" (auto-scale handle, no action needed).
- "Disk > 85%" page 3am (host has 10TB disk, 85% = 1.5TB free → not urgent).
- "Service down" — investigate → service is OK, alert misfiring.
- Real incident at 2pm — buried in 50 false alerts, missed by 20 min.

On-call: *"Alert fatigue. I ignore everything now. Will miss real one."*

Sếp post-mortem:
- **Threshold-based alerts** = lazy. Production cần **SLO-based + multi-window**.
- **No actionable runbook** = on-call mò.
- **No silence/inhibition** = same root cause spams 100 alerts.

→ Bài này fix end-to-end.

---

## 1️⃣ PromQL functions deep

🪞 **Ẩn dụ**: *PromQL như **ngôn ngữ pha chế cocktail** — `rate()`, `sum()`, `histogram_quantile()` là các bước "đong - lắc - rót"; chỉ khi đúng thứ tự và đúng tỉ lệ thì ly cocktail (alert) mới ngon và không gây ngộ độc (false alarm).*

### Data types

PromQL có **4 data type** — phân biệt sai = query không chạy hoặc trả sai. Đặc biệt cần nắm Instant vector (1 giá trị/series) vs Range vector (mảng giá trị theo thời gian):

| Type | Description | Example |
|---|---|---|
| **Instant vector** | Single value at single timestamp per series | `up`, `http_requests_total` |
| **Range vector** | Series of values over time range | `up[5m]`, `http_requests_total[1h]` |
| **Scalar** | Single number | `42`, `time()` |
| **String** | Text (rarely used) | `"hello"` |

### Operators

PromQL support 4 nhóm operator — arithmetic (tính toán), comparison (lọc), logical (kết hợp series), aggregation (gộp theo label). Mỗi nhóm có cú pháp riêng. 4 ví dụ tiêu biểu:

```promql
# Arithmetic
node_memory_usage_bytes / node_memory_total_bytes * 100

# Comparison (returns 0/1 series)
node_cpu_usage > 0.8

# Logical (vector ops)
up{job="api"} == 1 and up{job="db"} == 1

# Aggregation
sum by (service) (rate(http_requests_total[5m]))
avg without (instance) (http_request_duration_seconds)
max by (cluster) (kube_pod_status_phase{phase="Pending"})
```

### Aggregation operators

10 aggregation operator chính — sum/avg/min/max là 4 cái dùng 80% case. `topk/bottomk` hữu ích cho dashboard "top N noisy services". `quantile` xếp percentile distribution:

| Operator | Use case |
|---|---|
| `sum` | Total (combine series) |
| `avg` | Average |
| `min` / `max` | Extremes |
| `count` | Count series |
| `quantile(0.95, ...)` | Percentile (deprecated — use histogram_quantile) |
| `topk(5, ...)` | Top 5 highest |
| `bottomk(5, ...)` | Bottom 5 |
| `stddev` / `stdvar` | Standard deviation / variance |
| `group` | Like `sum` but binary 0/1 |
| `count_values("status", ...)` | Distribution by label value |

### Range functions (operate on range vector)

Range function operate trên **range vector** (vd `[5m]`) — `rate()` là cái dùng nhiều nhất (per-second rate cho counter). `predict_linear` đặc biệt: forecast tương lai từ trend hiện tại:

```promql
# Rate of increase per second (for counters)
rate(http_requests_total[5m])

# Increase over period
increase(http_requests_total[5m])    # rate * range duration

# Instant rate (last 2 points)
irate(http_requests_total[5m])       # for fast-changing — graph-friendly

# Average over time
avg_over_time(cpu_usage[10m])

# Quantile over time (e.g., P95 of CPU over 10m window)
quantile_over_time(0.95, cpu_usage[10m])

# Max over time
max_over_time(memory_usage[1h])

# Delta (for gauges, not counters)
delta(temperature[5m])

# Derivative (per-second slope for gauge)
deriv(temperature[5m])

# Prediction (linear regression)
predict_linear(disk_free_bytes[1h], 24*3600)  # extrapolate 24h
```

### Histogram quantile

**Counter `_bucket`** + `_count` + `_sum` recorded for histograms (e.g., HTTP request duration).

```promql
# P95 latency
histogram_quantile(0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)

# P95 per service
histogram_quantile(0.95,
  sum by (service, le) (rate(http_request_duration_seconds_bucket[5m]))
)

# P50 (median)
histogram_quantile(0.5, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))
```

→ `le` = "less than or equal" label (bucket boundary). `histogram_quantile` interpolate value at given quantile.

### Common patterns

**Success rate**:
```promql
sum(rate(http_requests_total{status!~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

**Error rate per service**:
```promql
sum by (service) (rate(http_requests_total{status=~"5.."}[5m]))
/
sum by (service) (rate(http_requests_total[5m]))
```

**Saturation (connection pool)**:
```promql
postgres_connections_in_use / postgres_connections_max > 0.8
```

**Predict disk full (in 4h)**:
```promql
predict_linear(node_filesystem_avail_bytes[1h], 4*3600) < 0
```

**Pod restart spike**:
```promql
rate(kube_pod_container_status_restarts_total[15m]) > 0
```

**Top 5 noisy logs source**:
```promql
topk(5,
  sum by (source) (rate(loki_log_entries_received_total[5m]))
)
```

---

## 2️⃣ Recording rules — Precompute

### Vấn đề

Dashboard có 10 panels, mỗi panel query 1 expensive expression. Mỗi panel refresh 30s → 200 queries/minute → Prometheus CPU saturated.

### Solution

Precompute expression → store as new time series → dashboard query precomputed.

### Define recording rule

```yaml
# prometheus rules file
groups:
  - name: http_recording_rules
    interval: 30s
    rules:
      # P95 latency per service
      - record: service:http_request_duration_seconds:p95
        expr: |
          histogram_quantile(0.95,
            sum by (service, le) (rate(http_request_duration_seconds_bucket[5m]))
          )
      
      # Success rate per service
      - record: service:http_success_rate:5m
        expr: |
          sum by (service) (rate(http_requests_total{status!~"5.."}[5m]))
          /
          sum by (service) (rate(http_requests_total[5m]))
      
      # Total requests per service (1m, 5m, 30m windows)
      - record: service:http_requests:rate1m
        expr: sum by (service) (rate(http_requests_total[1m]))
      - record: service:http_requests:rate5m
        expr: sum by (service) (rate(http_requests_total[5m]))
      - record: service:http_requests:rate30m
        expr: sum by (service) (rate(http_requests_total[30m]))
```

### Naming convention (Prometheus official)

```
level:metric:operations
```

- `level`: aggregation level (`service`, `cluster`, `region`, `global`).
- `metric`: original metric name.
- `operations`: ops applied (`p95`, `rate5m`, `sum`).

Examples:
- `service:http_requests:rate5m`
- `cluster:node_cpu_usage:avg`
- `global:user_signups:total`

### Apply via Prometheus Operator (K8s)

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: http-recording-rules
  namespace: monitoring
  labels:
    release: kube-prometheus
spec:
  groups:
    - name: http_recording
      interval: 30s
      rules:
        - record: service:http_success_rate:5m
          expr: |
            sum by (service) (rate(http_requests_total{status!~"5.."}[5m]))
            /
            sum by (service) (rate(http_requests_total[5m]))
```

### Performance impact

| Without recording rules | With recording rules |
|---|---|
| Dashboard load: 200 queries × expensive = 5 phút CPU | Dashboard load: 200 lookup × precomputed = 5s |
| Refresh 30s × 24h = 86400 evaluations | Rule evaluate 30s = 86400, dashboard lookup free |
| **Net**: same total compute, but distributed (continuous), không spike when user open dashboard |

→ **Use recording rules** cho mọi query repeated trong dashboard + alert.

---

## 3️⃣ Alerting rules

### Basic threshold (often misused)

```yaml
- alert: HighCPU
  expr: node_cpu_usage > 0.8
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "High CPU on {{ $labels.instance }}"
    description: "CPU is {{ $value }}"
```

❌ Problems:
- 80% CPU may be intentional (batch job).
- Single instance noisy.
- No actionable info.

### SLO-based alert (Google SRE pattern)

Define SLO (99.9% success), then alert when **error budget burning fast**.

**Single-window**:
```yaml
- alert: HighErrorRate
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m]))
    /
    sum(rate(http_requests_total[5m])) > 0.01      # 1% error rate
  for: 5m
```

❌ Problems:
- Fast (5m) window: noisy, false positive.
- Slow window (1h): real incident detected too late.

### Multi-window multi-burn-rate (production pattern)

```yaml
# SLO: 99.9% success → error budget = 0.1%
# Burn rate × normal rate = how fast budget consumed

- alert: ErrorBudgetBurnFast
  expr: |
    (
      sum(rate(http_requests_total{status=~"5.."}[5m]))
      /
      sum(rate(http_requests_total[5m]))
    ) > (14.4 * 0.001)              # 14.4x normal rate → burn 5% budget in 1h
    and
    (
      sum(rate(http_requests_total{status=~"5.."}[1h]))
      /
      sum(rate(http_requests_total[1h]))
    ) > (14.4 * 0.001)              # confirmed over 1h
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "Burning error budget 14.4x faster than normal"
    description: "Will exhaust 30-day budget in {{ ... }}"
    runbook: "https://wiki/runbooks/error-budget-burn"

- alert: ErrorBudgetBurnSlow
  expr: |
    (... 1h window ...) > (3 * 0.001)
    and
    (... 6h window ...) > (3 * 0.001)
  for: 15m
  labels:
    severity: warning
```

### Burn rate window matrix (SRE textbook)

| Burn rate | Short window | bạn window | Time to consume budget |
|---|---|---|---|
| **Critical (page)** | 5m | 1h | 2% in 1h, ~30-day budget burn |
| **Critical (page)** | 30m | 6h | 5% in 6h |
| **Warning (ticket)** | 2h | 24h | 10% in 24h |
| **Warning (ticket)** | 6h | 72h | 30% in 72h |

→ Multiple thresholds → catch fast burn (real incident) + slow burn (gradual degradation) without noise.

### Annotations with templating

```yaml
annotations:
  summary: "Error rate {{ humanizePercentage $value }} for {{ $labels.service }}"
  description: |
    Service {{ $labels.service }} in namespace {{ $labels.namespace }}
    has error rate {{ humanizePercentage $value }} (threshold 1%).
    
    Dashboard: https://grafana/d/api-overview?var-service={{ $labels.service }}
    Logs: https://grafana/explore?...
    Runbook: https://wiki/runbooks/{{ $labels.service }}-errors
```

→ Alert message includes: what, where, link to dashboard + logs + runbook.

---

## 4️⃣ Alertmanager — Routing + Silence + Inhibition

### Routing tree

```yaml
# alertmanager.yaml
route:
  receiver: default-team
  group_by: [alertname, cluster, namespace]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  
  routes:
    # Critical → PagerDuty
    - matchers:
        - severity=~"critical"
      receiver: pagerduty
      group_wait: 0s
      repeat_interval: 1h
    
    # Database team alerts
    - matchers:
        - team="database"
      receiver: database-team-slack
      routes:
        - matchers:
            - severity=~"critical"
          receiver: database-team-pagerduty
    
    # Payment service
    - matchers:
        - service=~"payment.*"
      receiver: payment-team-slack
    
    # Maintenance window suppress
    - matchers:
        - alertname="HostDown"
        - environment="maintenance"
      receiver: blackhole          # /dev/null

receivers:
  - name: default-team
    slack_configs:
      - api_url: $SLACK_WEBHOOK
        channel: '#ops-alerts'
  
  - name: pagerduty
    pagerduty_configs:
      - service_key: $PD_KEY
        description: "{{ .GroupLabels.alertname }}"
  
  - name: payment-team-slack
    slack_configs:
      - channel: '#payment-alerts'
        title: "{{ .GroupLabels.alertname }}"
        text: "{{ range .Alerts }}{{ .Annotations.summary }}\n{{ end }}"
  
  - name: blackhole
```

### Grouping — Reduce noise

```yaml
group_by: [alertname, cluster]
group_wait: 30s        # wait 30s for related alerts
group_interval: 5m     # send updates every 5m
repeat_interval: 4h    # re-send if still firing after 4h
```

→ 100 alerts from same incident → grouped → 1 notification with all instances.

### Silence — Temporary mute

UI Alertmanager → New Silence:
```
Matchers:
  - service="payment"
  - environment="production"

Starts: now
Ends: now + 2h
Comment: "Deploying v2.5.0, suppress noise during rolling restart"
Creator: oncall@acme.com
```

→ Or CLI:
```bash
amtool silence add \
  service=payment environment=production \
  --duration=2h \
  --comment="Deploy v2.5.0"
```

### Inhibition — Suppress dependent alerts

When `ClusterDown` fires, don't also page `PodDown` (consequence).

```yaml
inhibit_rules:
  - source_matchers:
      - alertname="ClusterDown"
    target_matchers:
      - alertname=~"PodDown|ServiceDown|HighLatency"
    equal: [cluster]
```

→ `ClusterDown` fire → suppress `PodDown` for same cluster.

### Receivers — Multi-channel

```yaml
receivers:
  - name: payment-team
    # Multiple channels per receiver
    slack_configs:
      - channel: '#payment-alerts'
    pagerduty_configs:
      - service_key: ...    # business-hours only via PD schedule
    email_configs:
      - to: payment-team@acme.com
    webhook_configs:
      - url: https://incident.io/api/alerts
```

→ Slack + PagerDuty + Email + custom webhook (Incident.io for incident management).

---

## 5️⃣ Cardinality management

### What's cardinality?

**Cardinality** = # of unique label combinations.

```promql
http_requests_total{service="api", method="GET", path="/users", status="200"}
http_requests_total{service="api", method="GET", path="/users", status="500"}
http_requests_total{service="api", method="POST", path="/orders", status="200"}
# ...
```

Each unique combination = separate time series. Prometheus stores **per series**.

### Cardinality explosion

❌ **High cardinality labels** (NEVER):
- `user_id` (millions of users).
- `request_id` (millions of requests).
- `email` (each user unique).
- `IP address` (many IPs).
- `URL with query params` (`?page=N&filter=...`).

```promql
http_requests_total{user_id="u-12345"}    # ← 1 million series!
```

→ Prometheus OOM, slow, expensive.

### Acceptable cardinality

✅ Low cardinality:
- `service` (10s of values).
- `method` (GET, POST, PUT, DELETE).
- `status` (200, 400, 500 — ~10 values).
- `pod` (100-1000s).
- `namespace` (10s).

Rule of thumb: each label should have **< 100 unique values**. Total cardinality per metric: **< 10,000 series**.

### Detect high cardinality

```bash
# Top 10 metrics by cardinality
curl -s http://prometheus:9090/api/v1/status/tsdb | jq '.data.seriesCountByMetricName[]' | head -10

# Or via PromQL
topk(10, count by (__name__)({__name__=~".+"}))
```

### Mitigations

1. **Drop labels via relabeling** (Prometheus scrape config):
   ```yaml
   scrape_configs:
     - job_name: api
       relabel_configs:
         - source_labels: [__meta_kubernetes_pod_label_user_id]
           action: drop
   ```

2. **Aggregate before storing** (recording rules without high-card labels):
   ```yaml
   - record: service:http_requests:rate5m
     expr: sum without (user_id, request_id) (rate(http_requests_total[5m]))
   ```

3. **Use traces for per-request data**: instead of `user_id` label, put in span attribute. Traces designed for high cardinality.

4. **Use histogram buckets** for path/route: instead of per-path metric, use `le` bucket for latency.

### Mimir/Thanos for high-scale

If genuinely need millions of series:
- **Grafana Mimir**: Cortex successor, scale Prometheus horizontally.
- **Thanos**: federation + long-term S3 storage.
- **VictoriaMetrics**: alternative, simpler ops.

→ Bài advanced. Intermediate: just avoid cardinality explosion.

---

## 6️⃣ Hands-on: Full alert + recording setup

### Step 1: Recording rules for FastAPI

```yaml
# fastapi-recording.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: fastapi-recording
  namespace: production
  labels:
    release: kube-prometheus
spec:
  groups:
    - name: fastapi_recording
      interval: 30s
      rules:
        - record: service:http_requests:rate5m
          expr: |
            sum by (service, status) (rate(http_requests_total{service="fastapi"}[5m]))
        
        - record: service:http_success_rate:5m
          expr: |
            sum(rate(http_requests_total{service="fastapi",status!~"5.."}[5m]))
            /
            sum(rate(http_requests_total{service="fastapi"}[5m]))
        
        - record: service:http_p95_latency:5m
          expr: |
            histogram_quantile(0.95,
              sum by (le) (rate(http_request_duration_seconds_bucket{service="fastapi"}[5m]))
            )
        
        - record: service:http_p99_latency:5m
          expr: |
            histogram_quantile(0.99,
              sum by (le) (rate(http_request_duration_seconds_bucket{service="fastapi"}[5m]))
            )
```

### Step 2: SLO definitions

```yaml
# fastapi-slo.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fastapi-slo
data:
  slo.yaml: |
    service: fastapi
    slo:
      success_rate: 0.999          # 99.9% requests success
      p95_latency: 0.5             # P95 < 500ms
      p99_latency: 1.0             # P99 < 1s
    error_budget:
      window: 30d                  # 30-day rolling
```

### Step 3: Alerting rules with burn rate

```yaml
# fastapi-alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: fastapi-alerts
  namespace: production
spec:
  groups:
    - name: fastapi_burn_rate
      rules:
        # Fast burn (page immediately)
        - alert: FastAPIErrorBudgetBurnFast
          expr: |
            (
              1 - (
                sum(rate(http_requests_total{service="fastapi",status!~"5.."}[5m]))
                /
                sum(rate(http_requests_total{service="fastapi"}[5m]))
              )
            ) > (14.4 * (1 - 0.999))
            and
            (
              1 - (
                sum(rate(http_requests_total{service="fastapi",status!~"5.."}[1h]))
                /
                sum(rate(http_requests_total{service="fastapi"}[1h]))
              )
            ) > (14.4 * (1 - 0.999))
          for: 2m
          labels:
            severity: critical
            team: backend
          annotations:
            summary: "FastAPI: Error budget burning 14.4x faster than allowed"
            description: |
              FastAPI error rate is 14.4x faster than SLO (99.9%) burn allows.
              At this rate, 30-day error budget exhausted in ~2 days.
              
              Dashboard: https://grafana.acmeshop.vn/d/fastapi
              Logs: https://grafana.acmeshop.vn/explore?service=fastapi&type=logs
              Runbook: https://wiki.acmeshop.vn/runbooks/fastapi-error-spike
        
        # Slow burn (ticket)
        - alert: FastAPIErrorBudgetBurnSlow
          expr: |
            (
              1 - (
                sum(rate(http_requests_total{service="fastapi",status!~"5.."}[6h]))
                /
                sum(rate(http_requests_total{service="fastapi"}[6h]))
              )
            ) > (3 * (1 - 0.999))
            and
            (
              1 - (
                sum(rate(http_requests_total{service="fastapi",status!~"5.."}[24h]))
                /
                sum(rate(http_requests_total{service="fastapi"}[24h]))
              )
            ) > (3 * (1 - 0.999))
          for: 30m
          labels:
            severity: warning
            team: backend
          annotations:
            summary: "FastAPI: Error budget slow burn"
            description: |
              Persistent elevated error rate over 6h+24h.
              Less urgent than fast burn, but trend negative.
        
        # Latency SLO
        - alert: FastAPILatencyP95High
          expr: service:http_p95_latency:5m > 0.5     # 500ms
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: "FastAPI P95 latency > 500ms"
            description: "Currently {{ $value }}s"
```

### Step 4: Alertmanager config

```yaml
# alertmanager.yaml
route:
  receiver: default
  group_by: [alertname, service]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  
  routes:
    - matchers:
        - severity=~"critical"
      receiver: pagerduty-backend
      group_wait: 0s
      repeat_interval: 1h
    
    - matchers:
        - team="backend"
      receiver: backend-team-slack
      routes:
        - matchers:
            - severity=~"critical"
          receiver: pagerduty-backend

receivers:
  - name: default
    slack_configs:
      - channel: '#ops-alerts'
        api_url: $SLACK_WEBHOOK
  
  - name: backend-team-slack
    slack_configs:
      - channel: '#backend-alerts'
        title: "[{{ .GroupLabels.severity | toUpper }}] {{ .GroupLabels.alertname }}"
        text: |
          {{ range .Alerts }}
          *Service:* {{ .Labels.service }}
          *Summary:* {{ .Annotations.summary }}
          *Description:* {{ .Annotations.description }}
          {{ end }}
  
  - name: pagerduty-backend
    pagerduty_configs:
      - service_key: $PD_KEY_BACKEND

inhibit_rules:
  - source_matchers:
      - alertname="ClusterDown"
    target_matchers:
      - severity=~"warning|critical"
    equal: [cluster]
```

### Step 5: Test

Trigger high error rate:
```bash
# Inject errors (curl loop)
for i in {1..1000}; do
  curl https://api.acmeshop.vn/intentional-error
done
```

Watch:
1. Prometheus → query `service:http_success_rate:5m` → see drop.
2. Alertmanager → see alert firing (after `for: 2m`).
3. Slack #backend-alerts → notification.
4. PagerDuty → page on-call.

---

## 7️⃣ Federation + Mimir/Thanos

### Single Prometheus limits

- ~10M series.
- ~15TB local disk.
- Single node = SPOF.

### Federation (basic)

```yaml
# Cluster-level Prometheus federates from team Prometheus
scrape_configs:
  - job_name: federate
    scrape_interval: 60s
    honor_labels: true
    metrics_path: /federate
    params:
      match[]:
        - '{__name__=~"job:.+"}'         # only `job:*` recording rules
        - '{__name__=~"service:.+"}'      # only `service:*`
    static_configs:
      - targets:
          - prometheus-team-a:9090
          - prometheus-team-b:9090
```

→ Cluster Prometheus pull pre-aggregated metrics from team Prometheus. Reduces data while keeping cross-team view.

### Mimir (Grafana, Cortex successor)

```bash
helm install mimir grafana/mimir-distributed \
  --namespace mimir \
  --create-namespace \
  -f values.yaml
```

→ Horizontal Prometheus:
- Ingest path: receive metrics via remote_write.
- Storage: S3/GCS for blocks.
- Query path: query across all storage.
- Scale: 100M+ series, year+ retention.

Cluster Prometheus remote_write to Mimir:
```yaml
remote_write:
  - url: http://mimir.mimir.svc/api/v1/push
```

### Thanos (older, still popular)

Same goals as Mimir, different architecture:
- Sidecar mode: attach to each Prometheus, upload blocks to S3.
- Query mode: federated query.

→ Choose Mimir if starting 2026 (CNCF Sandbox, active dev). Thanos if existing setup.

---

## 💡 Pitfall & Best practice

### ❌ Pitfall: Alert on raw CPU/memory

```yaml
- alert: HighCPU
  expr: cpu_usage > 0.8
```

→ Noisy, not actionable. CPU 80% may be desired (batch).

→ **Fix**: Alert on **user-facing impact** (error rate, latency). CPU saturation is mostly self-handling via HPA.

### ❌ Pitfall: `for: 1m` too short

```yaml
for: 1m
```

→ Flapping noise. Short transients trigger alert.

→ **Fix**: `for: 5m` minimum for non-critical. Burn rate alerts auto-handle this.

### ❌ Pitfall: No runbook link in alert

```yaml
annotations:
  summary: "Service down"
```

→ On-call wakes 3am, no idea what to do.

→ **Fix**: Mandatory `runbook_url` field. CI lint check.

### ❌ Pitfall: Cardinality explosion via labels

```promql
http_requests_total{user_id="u-123", request_id="r-abc"}
```

→ Prometheus OOM.

→ **Fix**: Audit metric exporters. Remove high-card labels. Move per-request data to traces.

### ❌ Pitfall: Recording rule expensive expression

```yaml
- record: foo:complex:5m
  expr: |
    histogram_quantile(0.99, 
      sum by (le, user_id) (rate(http_request_duration_seconds_bucket[5m]))
    )
```

→ Even precomputed, recording rule run every 30s. If expression itself takes 5s → Prometheus stuck.

→ **Fix**: Profile recording rules:
```bash
curl http://prometheus:9090/api/v1/rules | jq '.data.groups[].rules[] | {name, evaluationTime}'
```

Rules taking > 1s = optimize or break down.

### ❌ Pitfall: Static threshold scales poorly

```yaml
- alert: HighRequests
  expr: rate(http_requests_total[5m]) > 1000
```

→ Threshold OK now. App grows 10x → false positive constant.

→ **Fix**: Use rate-of-rate (anomaly) or burn rate (SLO-relative).

### ❌ Pitfall: All alerts same priority

→ Every alert paging on-call = burnout.

→ **Fix**: 3 tiers:
- **critical** → PagerDuty (call/SMS).
- **warning** → Slack channel.
- **info** → Email digest.

### ❌ Pitfall: Alerts not tested

```yaml
- alert: ServiceDown
  expr: up == 0
```

→ Never tested. Bug in expr. When service actually down, alert doesn't fire.

→ **Fix**: 
- Unit test via `promtool test rules`.
- Periodic chaos exercise (kill service, verify alert).

### ✅ Best practice: Alert hygiene metrics

Track:
- Alert volume per week (target: < 50/week).
- Time-to-acknowledge.
- Resolved without action (= false positive — remove).
- Repeat alerts (= need automation).

→ Weekly alert review. Delete useless alerts.

### ✅ Best practice: Runbook generator

Auto-link alert to runbook by name:
```yaml
annotations:
  runbook_url: "https://wiki.acmeshop.vn/runbooks/{{ .Labels.alertname }}"
```

Runbook wiki path matches alert name → standardize.

### ✅ Best practice: SLI/SLO co-located with code

```python
# slos.yaml in app repo
service: fastapi
slos:
  - name: availability
    target: 0.999
    sli: |
      sum(rate(http_requests_total{service="fastapi",status!~"5.."}[5m]))
      / sum(rate(http_requests_total{service="fastapi"}[5m]))
  - name: latency
    target: 0.99
    sli: |
      histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket{service="fastapi"}[5m]))) < 1
```

→ SLO owned by service team, version with code. Tools like **OpenSLO** or **Sloth** generate Prometheus rules.

---

## 🧠 Self-check

**Q1.** Vì sao multi-window burn rate alert better than threshold?

<details>
<summary>💡 Đáp án</summary>

**Threshold alert** (`error_rate > 1%`):
- **False positive at high traffic**: 1% of 100K req/sec = 1000 errors/sec. May be normal jitter.
- **False negative at low traffic**: 1% of 10 req/sec = 0.1 errors/sec. Tiny but bad service.
- **No time dimension**: 1 minute spike treated same as 6h sustained.

**Multi-window burn rate**:
- **Normalized to SLO**: "Are we burning error budget faster than allowed?"
- **Short + long windows**:
  - Short (5min) — fast detect spike.
  - bạn (1h) — confirm not transient.
  - Both must agree → reduce false positive.
- **Multiple burn rates**:
  - Fast (14.4x) — page urgently, real incident.
  - Slow (3x) — ticket, gradual degradation.

**Net effect**:
- Catch big spikes within 2-5 min (fast burn).
- Catch slow degradation over hours (slow burn).
- Avoid noise from transient blips (long window confirms).

→ Industry standard 2026: multi-window. Threshold for legacy systems only.
</details>

**Q2.** Vì sao recording rule cải thiện performance dù total compute same?

<details>
<summary>💡 Đáp án</summary>

**Without recording rules**:
- Dashboard opens → 20 panels × expensive query × 30 user concurrent → 600 query bursts.
- Prometheus CPU spike, query latency 10s+.
- Alerts query same expressions → compete for CPU.
- User experience: dashboard slow, alerts delayed.

**With recording rules**:
- Recording rule runs every 30s (constant load).
- Dashboard query lookup precomputed metric = 1ms.
- 20 panels × 30 users × 1ms = nothing.
- Alerts also use precomputed.

**Total compute same**:
- Recording rule: query runs 1× per 30s, all day = 2880 evals.
- Without: query runs N× per dashboard view, but spiky.

**Key benefit**: **distribute load**. Constant 1 eval / 30s instead of spike when users access.

**Bonus**: same query result available to ALL consumers (dashboards + alerts + API). Single source of truth.

**Caveat**: high-cardinality recording rule wastes storage. Be selective. Only precompute expensive + frequently-used queries.
</details>

**Q3.** Cardinality vs trace data — phân biệt khi nào dùng cái nào?

<details>
<summary>💡 Đáp án</summary>

**Metric (Prometheus)**:
- **Aggregate** over time (rate, sum, percentile).
- **Low cardinality** by design (< 10K series per metric).
- **Time-series** efficient storage.
- Use for: "How many requests/sec? P99 latency? Error rate per service?"

**Trace (Tempo/Jaeger)**:
- **Per-request** detail.
- **High cardinality** by nature (every request unique trace_id).
- **Index by trace_id**, slow scan otherwise.
- Use for: "Why was request X slow? Which DB call took 1s in trace abc123?"

**Rule of thumb**:
| Question | Use |
|---|---|
| Aggregate stats | Metric |
| Specific request investigation | Trace |
| Per-user breakdown across all requests | High-card metric (bad) OR exemplars (good) |
| Performance distribution | Histogram metric |
| Cause-effect chain (call hierarchy) | Trace |

**Exemplars** (Prometheus + traces bridge):
- Histogram bucket can include `trace_id` exemplar.
- "Show me a sample slow request for this P99 bucket" → click → jump to trace.
- Best of both worlds.

→ Don't put `user_id` in metric label. Put in trace span attribute. Use exemplars to bridge.
</details>

**Q4.** Alertmanager inhibition vs silence — khi nào dùng cái nào?

<details>
<summary>💡 Đáp án</summary>

**Silence** = **manual, temporary** mute.
- Use case: deploying v2.5, expect 5 min noisy → silence 30 min.
- Set start/end time, comment, creator.
- Re-fire automatically when silence ends.

**Inhibition** = **rule-based, automatic** suppression.
- Use case: `ClusterDown` fires → suppress all dependent alerts (PodDown, ServiceDown, etc.).
- Configured in Alertmanager config (always active).
- Automatic — no human action.

**Examples**:

Silence:
- Maintenance window (planned, manual).
- Investigating issue, don't want repeat pages.
- Deprecating service.

Inhibition:
- Cluster outage → service outages (suppress).
- Node down → pod evictions (suppress).
- Network partition → cross-AZ alerts (suppress).

**Both can coexist**: silence for ad-hoc, inhibition for permanent dependencies.

**Anti-pattern**: too many silences indicate alert quality issues. Audit silences quarterly — if same silence recurring, fix root cause (delete or fix alert).

→ Silence = "ignore now". Inhibition = "ignore when X happens".
</details>

**Q5.** Mimir/Thanos vs raw Prometheus — quanto cần?

<details>
<summary>💡 Đáp án</summary>

**Raw Prometheus đủ khi**:
- Single cluster, ≤ 10M series.
- Retention < 15 days.
- 1-2 person ops team.
- < 15TB metric data.

**Cần Mimir/Thanos khi**:
- **Multi-cluster**: federated query across regions.
- **Long-term retention**: 1 year+ for capacity planning, compliance.
- **High availability**: Prometheus replica = duplicate writes; Mimir dedupe.
- **Multi-tenant**: separate teams' metrics with quotas.
- **Cost**: S3 storage cheaper than local SSD for old data.

**Mimir advantages 2026**:
- Active development (Grafana Labs).
- Single binary, simpler ops than Thanos.
- Built-in alerting.

**Thanos advantages**:
- Larger community (older).
- Sidecar mode = drop-in for existing Prometheus.

**VictoriaMetrics alternative**:
- Simpler than both.
- 10x less RAM than Prometheus.
- Drop-in PromQL compatible.

**Decision**:
- New deployment 2026: Mimir (active dev) or VictoriaMetrics (simpler).
- Existing Prometheus, want long-term: Thanos sidecar.
- Cost-sensitive: VictoriaMetrics.

**Migration path**: Prometheus → add remote_write to Mimir → query Mimir for long-term + Prometheus for hot. Eventually deprecate local Prometheus.
</details>

---

## ⚡ Cheatsheet

```promql
# === Aggregation ===
sum by (service) (rate(http_requests_total[5m]))
avg without (instance) (cpu_usage)
topk(5, ...)
bottomk(5, ...)

# === Histogram ===
histogram_quantile(0.95, sum by (le) (rate(metric_bucket[5m])))

# === Predict ===
predict_linear(disk_free[1h], 24*3600)

# === Window functions ===
rate(metric[5m])               # per-second rate
irate(metric[5m])              # instant rate
increase(metric[5m])           # absolute increase
avg_over_time(metric[10m])
max_over_time(metric[1h])
quantile_over_time(0.95, metric[10m])

# === Counter resets ===
resets(metric[5m])              # # of resets (e.g., service restarts)
changes(metric[5m])             # # of value changes
```

```yaml
# === Recording rule template ===
- record: <level>:<metric>:<ops>
  expr: <expression>

# === Multi-window burn rate ===
- alert: ServiceBudgetBurnFast
  expr: |
    error_rate_5m > 14.4 * (1 - SLO_TARGET) 
    and 
    error_rate_1h > 14.4 * (1 - SLO_TARGET)
  for: 2m
  labels: { severity: critical }
  annotations:
    runbook_url: ...

# === Alertmanager ===
route:
  group_by: [alertname]
  routes:
    - matchers: [severity=critical]
      receiver: pagerduty
    - matchers: [team=backend]
      receiver: backend-slack
```

```bash
# === Tools ===
promtool check rules rules.yaml
promtool test rules tests.yaml
amtool alert query
amtool silence add foo=bar --duration=2h
amtool config routes show
amtool config routes test --tree
```

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **PromQL** | Prometheus Query Language |
| **Instant vector / Range vector** | Single value vs series over time |
| **`rate()`** | Per-second average rate of counter |
| **`irate()`** | Instant rate (last 2 points) |
| **`increase()`** | Absolute increase = rate × time |
| **`histogram_quantile()`** | Compute percentile from histogram buckets |
| **`predict_linear()`** | Extrapolate value via linear regression |
| **Recording rule** | Precompute query, store as new metric |
| **Alerting rule** | Query triggering alert when threshold met |
| **Burn rate** | Error budget consumption rate (× normal) |
| **Multi-window alert** | Alert validates over 2 windows (short + long) |
| **Alertmanager** | Route alerts to receivers (Slack/PagerDuty/email) |
| **Routing tree** | Hierarchical alert routing config |
| **Silence** | Manual temporary mute alerts matching selector |
| **Inhibition** | Auto-suppress alerts when other alert active |
| **Receiver** | Channel sending alert (Slack/PagerDuty/email/webhook) |
| **Cardinality** | # unique label combinations per metric |
| **Series** | Unique combination of metric + labels (1 time series) |
| **Federation** | Cluster Prometheus pull from team Prometheus |
| **Mimir** | Grafana's horizontally scalable Prometheus (Cortex successor) |
| **Thanos** | Federated Prometheus with S3 storage |
| **VictoriaMetrics** | Alternative high-performance metrics DB |
| **OpenSLO / Sloth** | Tools generate Prometheus rules from SLO spec |
| **Exemplar** | Sample (e.g., trace_id) attached to histogram bucket |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [00_intermediate-overview.md](00_intermediate-overview.md)
- → Tiếp: [02_loki-logql-deep.md](02_loki-logql-deep.md) *(sắp viết)*
- ↑ Cluster: [Observability README](../../README.md)

### Cross-reference
- ☸️ [K8s intermediate Autoscaling](../../../kubernetes/lessons/02_intermediate/04_autoscaling-and-operators.md) — HPA dùng PromQL custom metric
- 🔁 [CI/CD intermediate Progressive delivery](../../../ci-cd/lessons/02_intermediate/04_progressive-delivery.md) — Argo Rollouts metric analysis

### Tài nguyên ngoài
- 📖 [PromQL docs](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- 📖 [PromLabs cheat sheet](https://promlabs.com/promql-cheat-sheet/)
- 📖 [SRE Workbook — Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- 📖 [Alertmanager docs](https://prometheus.io/docs/alerting/latest/alertmanager/)
- 📖 [Mimir docs](https://grafana.com/docs/mimir/)
- 📖 [Thanos docs](https://thanos.io/)
- 📖 [VictoriaMetrics docs](https://docs.victoriametrics.com/)
- 📖 [OpenSLO](https://openslo.com/)
- 📖 [Sloth — SLO generator](https://sloth.dev/)
- 📖 [Awesome Prometheus alerts](https://samber.github.io/awesome-prometheus-alerts/) — recipe collection

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước Data types + Operators + Aggregation + Range functions.

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Lesson 01 intermediate. PromQL deep (functions, operators, aggregation, range, histogram_quantile, predict_linear) + recording rules + multi-window burn rate alerts (Google SRE pattern) + Alertmanager routing/silence/inhibition + cardinality management + Mimir/Thanos federation. Apply insight `__Ref__/`: alert on saturation, burn rate alerts. 8 pitfall + 3 best practice + 5 self-check + cheatsheet.
