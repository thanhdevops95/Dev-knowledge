# 🚨 MODULE 06: SCENARIOS - Monitoring Issues

## Scenario 1: Dashboard Green, App Down

### 🚨 Bối cảnh

Grafana dashboard shows all metrics green. Users complain app is down.

### 🕵️ Điều tra

```bash
curl http://app.com
# Connection refused

# Prometheus still showing metrics → Old data!
```

**Nguyên nhân:** Health check endpoint `/metrics` cached, app crashed nhưng metrics vẫn hiển thị giá trị cũ.

### 💡 Giải pháp

**1. Add `up` metric monitoring:**

```promql
# Alert when target is down
up{job="counter-app"} == 0
```

**2. Synthetic monitoring:**

```python
# External probe
import requests
response = requests.get('http://app.com/')
assert response.status_code == 200
```

**3. Black-box monitoring:**

- Monitor from user perspective
- Check actual endpoints, not just `/metrics`

### 🧠 Bài học

- Monitor `up` metric
- External probes > Internal metrics
- Black-box + White-box monitoring

---

## Scenario 2: Alert Fatigue (1000 alerts/day)

### 🚨 Bối cảnh

On-call engineer receives 1000 alerts/day → Ignores all → Misses critical outage.

### 🕵️ Điều tra

```yaml
# alert.rules.yml - TOO SENSITIVE
- alert: HighCPU
  expr: cpu_usage > 50%  # ← Too low threshold
  for: 10s  # ← Too short
```

### 💡 Giải pháp

**1. Tune thresholds:**

```yaml
- alert: HighCPU
  expr: cpu_usage > 80%  # Realistic threshold
  for: 5m  # Wait 5 minutes before alerting
```

**2. Alert routing:**

```yaml
# alertmanager.yml
routes:
  - match:
      severity: critical
    receiver: pagerduty  # Page on-call
  
  - match:
      severity: warning
    receiver: slack  # Slack notification only
```

**3. Alert grouping:**

```yaml
group_by: ['cluster', 'alertname']
group_wait: 30s
group_interval: 5m
```

**4. Runbooks:**

```yaml
annotations:
  runbook: "https://wiki.company.com/runbooks/high-cpu"
```

### 🧠 Bài học

- Set realistic thresholds
- Route by severity
- Group related alerts
- Provide runbooks

---

## Scenario 3: Logs Overwhelming (10GB/day)

### 🚨 Bối cảnh

Elasticsearch disk full, logs overwhelming storage.

### 🕵️ Điều tra

```bash
# Check log volume
du -sh /var/log/elasticsearch
# 500GB!

# Top log sources
grep -o 'DEBUG.*' app.log | wc -l
# 10 million DEBUG logs/day
```

### 💡 Giải pháp

**1. Log levels:**

```python
# Production: INFO or WARNING only
logging.basicConfig(level=logging.WARNING)

# Development: DEBUG
if os.getenv('ENV') == 'dev':
    logging.basicConfig(level=logging.DEBUG)
```

**2. Sampling:**

```python
# Log only 1% of requests
if random.random() < 0.01:
    logger.info(f"Request: {request}")
```

**3. Retention policies:**

```yaml
# Elasticsearch ILM
DELETE /logs-* WHERE @timestamp < now-7d
```

**4. Structured logging:**

```python
# JSON format for better compression
logger.info(json.dumps({
    "event": "request",
    "path": "/increment",
    "latency_ms": 42
}))
```

### 🧠 Bài học

- Use appropriate log levels
- Sample high-volume logs
- Set retention policies
- Structured logging > Plain text

---

## Scenario 4: High Cardinality Metrics Crash Prometheus

### 🚨 Bối cảnh

Prometheus OOMKilled (Out of Memory).

### 🕵️ Điều tra

```promql
# Check cardinality
prometheus_tsdb_head_series
# 10 million series!

# Find culprit metric
topk(10, count by (__name__)({__name__=~".+"}))
# http_requests_total{user_id="12345", session_id="abc"} ← BAD!
```

**Nguyên nhân:** Metric có label `user_id` (1 million users) = 1 million time series!

### 💡 Giải pháp

**1. Remove high-cardinality labels:**

```python
❌ request_count.labels(user_id=user_id).inc()  # BAD
✅ request_count.inc()  # GOOD (no user_id label)
```

**2. Use logs for high-cardinality data:**

```python
# Metrics: aggregated data
request_count.inc()

# Logs: individual events
logger.info(f"User {user_id} made request")
```

**3. Limit label values:**

```python
# Bucket instead of exact values
status_code = "5xx" if code >= 500 else "4xx" if code >= 400 else "2xx"
request_count.labels(status=status_code).inc()
```

### 🧠 Bài học

- **Metrics for aggregates, logs for details**
- Avoid user IDs, session IDs in labels
- Limit label cardinality (<100 values)

---

## Scenario 5: On-Call Engineer Burned Out

### 🚨 Bối cảnh

Engineer on-call 24/7, paged every night, sleep deprived, quitting job.

### 🕵️ Điều tra

- Alerts at 2am, 3am, 4am every night
- Same issue: out of disk space (predictable!)
- No follow-up during business hours → Repeats next night

### 💡 Giải pháp

**1. Predictive alerts (business hours only):**

```yaml
- alert: DiskWillFillIn24H
  expr: predict_linear(disk_free[1h], 24*3600) < 0
  for: 1h
  # Only during business hours
  annotations:
    summary: "Disk will fill in 24 hours (non-urgent)"
```

**2. Auto-remediation:**

```yaml
# Kubernetes: Auto-delete old logs
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cleanup-logs
spec:
  schedule: "0 2 * * *"  # 2am daily
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: cleanup
            command: ["find", "/var/log", "-mtime", "+7", "-delete"]
```

**3. Escalation policies:**

```yaml
# PagerDuty
Level 1: Page engineer after 5 minutes
Level 2: Page manager after 15 minutes
Level 3: Page CTO after 30 minutes (critical only)
```

**4. Incident rotation:**

- Weekly rotation (not 24/7 for 1 person)
- Compensatory time off after on-call week
- Post-incident reviews to prevent recurrence

**5. Toil reduction:**

- Automate recurring tasks
- Track toil percentage (target <30% of time)
- Dedicate time to fix root causes

### 🧠 Bài học

- **Predictive > Reactive alerts**
- Automate remediation
- Fair rotation schedules
- Reduce toil, fix root causes
- Respect work-life balance

---

## 🎯 Tổng kết Module 06

| Scenario | Vấn đề | Giải pháp |
|----------|--------|-----------|
| 1 | False positive green | Monitor `up` + External probes |
| 2 | Alert fatigue | Tune thresholds + Routing |
| 3 | Log overwhelming | Log levels + Sampling + Retention |
| 4 | High cardinality | Remove high-cardinality labels |
| 5 | Burnout | Predictive alerts + Auto-remediation |

✅ **Next:** Module 07 - FEEDBACK (Final module!)
