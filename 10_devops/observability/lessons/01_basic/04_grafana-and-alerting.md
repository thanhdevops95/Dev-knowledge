# 🎓 Grafana & Alerting — Unified dashboard + alert routing

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.1\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 11/06/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [Traces OTel](03_traces-opentelemetry.md)

> 🎯 *Master **Grafana**: dashboards (panels, variables, templating), **data sources** (Prometheus + Loki + Tempo), **Grafana Alerting** (rules + Alertmanager routing), **on-call workflows** (PagerDuty, OpsGenie), **SLO-based alerts**, **incident response** patterns.*

## 🎯 Sau bài này bạn sẽ

- [ ] Setup Grafana + data sources
- [ ] Build **dashboard** với panels + variables + templating
- [ ] Master **Grafana Alerting** (Unified alerting)
- [ ] Configure **Alertmanager** routing (Slack, email, PagerDuty)
- [ ] **SLO-based** alerts (burn rate alerts)
- [ ] **Silence + acknowledge** patterns
- [ ] **On-call rotation** workflow
- [ ] **Runbook** linkage + post-incident review

---

## 1️⃣ Grafana — Visualization hợp nhất

**Grafana** = OSS dashboard tool, support 100+ data sources.

### Cài đặt K8s

Cài Grafana đơn giản qua Helm chart `grafana/grafana`. Tham số bắt buộc cho production: `adminPassword` (thay đổi sau login đầu) + `persistence.enabled=true` (dashboard không mất khi Pod restart). Truy cập UI qua port-forward (dev) hoặc Ingress (prod):

```bash
helm install grafana grafana/grafana -n monitoring \
  --set adminPassword='admin123' \
  --set persistence.enabled=true

kubectl port-forward -n monitoring svc/grafana 3000:80
# Login: admin / admin123
```

### Data sources

Add via UI: Configuration → Data Sources → Add.

| Source | URL |
|---|---|
| **Prometheus** | `http://prometheus:9090` |
| **Loki** | `http://loki:3100` |
| **Tempo** | `http://tempo:3100` |
| **Postgres** | `postgres:5432` (with auth) |
| **CloudWatch** | (AWS auth) |
| **InfluxDB** | `http://influxdb:8086` |

→ Each source has query editor specific (PromQL / LogQL / SQL).

---

## 2️⃣ Dashboards + Panels

### Giải phẫu

Dashboard Grafana có cấu trúc 3 lớp: **Variables** (dropdown trên top — filter cả dashboard), **Time range** (cửa sổ thời gian — last 6h, 24h, custom), và **Panels** (mỗi panel = 1 query + 1 visualization). Layout grid 24 cột — kéo thả panel resize tuỳ ý:

```
Dashboard
├── Variables    (dropdowns: env, namespace, service)
├── Time range    (last 6h, 24h, custom)
└── Panels
    ├── Time series (line chart)
    ├── Stat (single number)
    ├── Gauge
    ├── Bar chart
    ├── Heatmap
    ├── Logs panel
    ├── Trace panel
    └── Table
```

### Ví dụ panel — Latency

Ví dụ kinh điển: panel vẽ P99 latency theo service. Query dùng `histogram_quantile` trên metric `http_request_duration_seconds_bucket`. Visualization "Time series" hiển thị line chart, unit "seconds". Thresholds 0.5s vàng / 1.0s đỏ giúp đọc nhanh khi service nào sắp vượt ngưỡng SLO:

```
Panel: P99 Latency

Data source: Prometheus
Query:
  histogram_quantile(0.99,
    sum by (le, service) (rate(http_request_duration_seconds_bucket{$service_var}[5m]))
  )

Visualization: Time series
Unit: seconds
Thresholds:
  - 0.5s yellow
  - 1.0s red
```

### Variables (template)

**Variables** biến dashboard tĩnh thành dashboard tương tác. Khai báo `$service` query từ Prometheus → top dashboard có dropdown chọn service → tất cả panel auto-filter `{service="$service"}`. Tránh tạo 10 dashboard cho 10 service — 1 dashboard + variable đủ:

```
Variable: $service
  Type: Query
  Data source: Prometheus
  Query: label_values(http_requests_total, service)
  Multi-value: yes
  All option: yes
```

→ Dropdown ở top dashboard. User pick service → all panels filter `{service="$service"}`.

### Các variable hữu ích

5 variable nên có trong mọi dashboard production. `$env` cho switch giữa dev/staging/prod, `$namespace` filter theo K8s namespace, `$service` chọn service, `$instance` cho deep-dive 1 pod, `$interval` cho phép user đổi rate window (đọc 1m chi tiết hoặc 30m smooth):

```
$env        environment (dev/staging/prod)
$namespace   K8s namespace
$service     selected service
$instance    specific pod
$interval    rate window (1m / 5m / 30m)
```

### Import dashboard có sẵn

```
Grafana → + → Import → grafana.com ID
```

| Dashboard ID | Purpose |
|---|---|
| **315** | K8s cluster overview |
| **1860** | Node Exporter Full |
| **7249** | Postgres |
| **11074** | Loki + dashboards |
| **12239** | FastAPI |

→ 1000s community dashboards. Import → customize.

### Dashboard as code

```bash
# Export
curl -H "Authorization: Bearer $TOKEN" \
  http://grafana/api/dashboards/uid/abc > dashboard.json

# Git-track JSON
# Re-import via Terraform Grafana provider or sync
```

→ Production: dashboards in git. `grafanaspaceman/grafanactl` or `grafana-operator` for sync.

---

## 3️⃣ Grafana Alerting — Hợp nhất

Grafana **Unified Alerting** (since v9) — rules + routing + notifications all in Grafana.

### Kiến trúc

```
Data sources (Prometheus, Loki, ...)
    ↓ query
Grafana evaluates rule
    ↓ fires
Alert state: pending → firing
    ↓
Notification policy routes
    ↓
Contact point (Slack/PagerDuty/email)
```

### Ví dụ alert rule

```yaml
# Via Grafana UI or YAML
name: HighErrorRate
condition: A > 0.05

queries:
- refId: A
  datasource: prometheus
  expr: |
    sum(rate(http_requests_total{status=~"5.."}[5m]))
      / sum(rate(http_requests_total[5m]))

for: 10m                                  # Must be true 10 min before fire
labels:
  severity: warning
  team: backend
annotations:
  summary: "Error rate > 5%"
  description: "Current: {{ $value | humanizePercentage }}"
  runbook_url: "https://wiki/runbooks/high-error-rate"
```

→ Eval every 1 min. Fire if condition true for 10 min straight.

### Vòng đời alert

```
Normal   ─── condition true ───►   Pending (waiting "for" duration)
                                       │
                                       ▼ "for" elapsed
                                  Firing   ───► Notification sent
                                       │
                                       ▼ condition false
                                  Resolved ───► Resolved notification
```

→ `for` prevents flaky alerts (spike < 10min = ignored).

---

## 4️⃣ Notification policies + routing

Match labels → route to contact point.

```yaml
# Notification policy tree
root:
  receiver: default-slack
  group_by: [alertname, cluster]
  routes:
  - match: { severity: critical }
    receiver: pagerduty
    continue: true                        # Also send to default
  - match_re: { team: ^(backend|data)$ }
    receiver: backend-slack
    routes:
    - match: { service: payment }
      receiver: payment-team-pagerduty
```

### Luật match

| Type | Example |
|---|---|
| `match` | Exact label value match |
| `match_re` | Regex label match |
| `continue: true` | Continue to next route after match |

### Contact points

| Type | Use |
|---|---|
| **Slack** | Webhook to Slack channel |
| **Email** | SMTP |
| **PagerDuty** | Incident escalation |
| **OpsGenie** | Alternative to PD |
| **Webhook** | Custom integration |
| **Microsoft Teams** | Team chat |
| **Telegram** | Personal alerts |

### Ví dụ Slack

```yaml
contact_point:
  name: backend-slack
  type: slack
  settings:
    url: https://hooks.slack.com/services/...
    title: "{{ .Status }}: {{ .Labels.alertname }}"
    text: |
      *Alert*: {{ .Labels.alertname }}
      *Severity*: {{ .Labels.severity }}
      *Service*: {{ .Labels.service }}
      *Summary*: {{ .Annotations.summary }}
      *Runbook*: {{ .Annotations.runbook_url }}
```

→ Slack notify với label/annotation interpolated.

---

## 5️⃣ Grouping + Inhibition + Silence

### Grouping — Giảm alert spam

```yaml
group_by: [alertname, cluster]
group_wait: 30s                            # Wait 30s for more alerts before send
group_interval: 5m                         # Subsequent batches
repeat_interval: 4h                        # Resend if still firing after 4h
```

→ 10 pods CrashLoop same time → 1 grouped notification. Else 10 alerts spam.

### Inhibition — Nén alert liên quan

```yaml
inhibit_rules:
- source_match:
    severity: critical
  target_match:
    severity: warning
  equal: [cluster, service]
```

→ Critical alert fires → suppress warnings on same cluster/service. Reduce noise.

### Silence — Tắt tạm thời

```
Grafana UI → Alerting → Silences → New
Matchers: alertname=HighLatency, service=payment
Duration: 2h
Reason: Deploying new payment service v2.0
```

→ Suppress matching alerts for 2h. Maintenance window.

---

## 6️⃣ SLO-based alerting — Burn rate

Traditional: "error rate > 5%" — too late or too sensitive.

**SLO burn rate** = "are we burning error budget faster than expected?"

### Ví dụ: 99.9% SLO over 30 days

```
SLO: 99.9% success
Allowed error budget: 0.1% × 30 days × 24h = ~43 minutes of errors total

If burn rate = 1.0 → on track (will consume budget exactly by day 30)
If burn rate = 14.4 → consume 100% budget in 30 days/14.4 = 2 days! 🚨
```

### Multi-window, multi-burn-rate alerts

```yaml
- alert: ErrorBudgetBurnFast
  expr: |
    (
      sum(rate(http_errors_total[1h])) / sum(rate(http_requests_total[1h])) > (14.4 * 0.001)
    ) and (
      sum(rate(http_errors_total[5m])) / sum(rate(http_requests_total[5m])) > (14.4 * 0.001)
    )
  for: 2m
  labels: { severity: critical }
  annotations:
    summary: "Fast burn: 100% budget in 2 days"

- alert: ErrorBudgetBurnSlow
  expr: |
    (
      sum(rate(http_errors_total[6h])) / sum(rate(http_requests_total[6h])) > (6 * 0.001)
    ) and (
      sum(rate(http_errors_total[30m])) / sum(rate(http_requests_total[30m])) > (6 * 0.001)
    )
  for: 15m
  labels: { severity: warning }
  annotations:
    summary: "Slow burn: 100% budget in 5 days"
```

→ **Multi-window** prevents both false positive + missed slow drift.

→ Recipe from Google SRE Workbook. **2026 standard SLO alerts**.

---

## 7️⃣ Alert quality — Tránh fatigue

### Triệu chứng alert tồi

- 🚨 100+ alerts/day → ignored.
- 🚨 Alerts at 3 AM not actionable → burnout.
- 🚨 Alert fires before user even notices → tune sensitivity.
- 🚨 Page on every transient blip → flaky.

### Nguyên tắc

1. **Alert on symptoms, not causes**.
   - ❌ "CPU > 80%" (cause).
   - ✅ "P99 latency > 1s" (symptom user feels).

2. **Actionable**: who? what? where?
   - Include runbook link.
   - Include service/team labels.

3. **Severity tiers**:
   - **Critical** — page on-call immediately (3 AM OK).
   - **Warning** — Slack to team, look at business hours.
   - **Info** — log only, no notification.

4. **`for` duration** prevents flakiness.

5. **Inhibit + group** reduce volume.

### Audit alert

```promql
# Count alerts fired in last 30 days
sum by (alertname) (changes(ALERTS{alertstate="firing"}[30d]))

# Top 10 noisy
topk(10, ...)
```

→ Each quarter: remove unused, tune thresholds, archive runbooks.

---

## 8️⃣ On-call rotation

### Cài đặt PagerDuty / OpsGenie

```
Team: Backend
Schedule:
  - Mon-Fri 9-17: primary = alice, secondary = bob
  - Mon-Fri 17-09: primary = carol, secondary = david
  - Weekend: rotate weekly

Escalation:
  - Page primary
  - 5 min no ack → page secondary
  - 10 min no ack → page manager
```

→ Grafana → PagerDuty integration → auto-page on-call schedule.

### Acknowledge (xác nhận)

```
Alert fires → page on-call
  ↓
On-call ack → stop paging, claim incident
  ↓
Resolve → mark in PD + Slack
  ↓
Post-mortem within 48h
```

### Luồng Slack

```
Channel #incidents:
🚨 [CRITICAL] HighErrorRate on payment service
  Summary: Error rate 12% (SLO 1%)
  Runbook: https://wiki/runbooks/payment-errors
  Dashboard: https://grafana/d/payment
  ACK by @alice 14:32 (3 min after alert)
```

→ Pre-built Slack bots: GitHub `#incidents` workflow.

---

## 9️⃣ Incident response + Runbooks

### Template runbook

```markdown
# Runbook: HighErrorRate on Payment Service

## Alert
- **Metric**: error_rate{service=payment} > 5%
- **Severity**: Critical
- **SLO impact**: Burn rate >14.4

## Initial response (<5 min)
1. Check Grafana dashboard: https://grafana/d/payment
2. Recent deploys: https://argo/payment
3. Recent traffic spike: https://grafana/d/traffic

## Investigation
1. Filter logs by error: `{service=payment} | json | level="error"`
2. Check upstream services: Stripe API status
3. Database connection pool: query `db_connections_active`
4. Tail traces: Tempo search service=payment status=error

## Mitigation
- If recent deploy: `kubectl rollout undo deployment/payment`
- If upstream: open status page, switch to backup payment gateway
- If DB pool: scale Postgres connections or restart pool

## Escalation
- 15 min no fix: page @backend-lead
- 30 min: page CTO

## Resolution
- Verify error rate < 1% sustained 10 min
- Post-mortem within 48h
```

→ Each alert linked to runbook. On-call doesn't think — execute.

### Template post-mortem

```markdown
# Post-mortem: Payment outage 2026-05-22

## Impact
- Duration: 14:32 - 15:12 (40 min)
- Affected: 5000 checkout attempts failed
- Revenue impact: ~$15,000

## Timeline
- 14:25 Deploy v2.0
- 14:32 Alert fires
- 14:33 On-call ack
- 14:45 Identified bad release
- 14:50 Rollback
- 15:12 Error rate back normal

## Root cause
- DB migration v2.0 dropped index, slow queries timeout

## Action items
- [ ] CI: add migration plan review (owner: alice, by 2026-05-30)
- [ ] Add canary deploy for payment service (owner: bob, by 2026-06-15)
- [ ] Improve rollback automation (owner: carol)

## Lessons
- Blameless. What system fail allowed this?
```

→ Post-mortem culture: **blameless**. Improve system, not punish people.

---

## 1️⃣0️⃣ Cài đặt đầy đủ của bạn

### Dashboards (4 cái bắt buộc)

```
1. Service Overview (FastAPI RED + USE)
   - Request rate, error rate, P50/P95/P99 latency
   - CPU, RAM, restarts
   - DB connection pool

2. Business KPIs
   - Orders/min, revenue/min
   - Active users
   - Conversion funnel

3. Infrastructure
   - K8s nodes
   - Postgres
   - Redis

4. SLO Dashboard
   - SLO status
   - Error budget remaining
   - Burn rate alerts
```

### Alert rules (bắt đầu với 8 cái)

```
Critical:
  HighErrorRate (>5% 10m)
  AppDown (no responses 2m)
  PodCrashLooping
  DiskFull (>90%)

Warning:
  HighLatency (P99 > 1s 15m)
  HighMemory (>80% 30m)
  SLOBurnRate (fast burn)
  DBConnectionsHigh (>80%)
```

### Routing

```
Critical → PagerDuty (24/7)
Warning  → Slack #ops (business hours)
Info     → Slack #ops-info (silent)
```

### Công cụ

```
Grafana (dashboards + alerts)
Slack (#incidents)
PagerDuty (on-call rotation)
Wiki (runbooks)
GitHub (post-mortems repo)
```

→ Production observability stack. Set up 1 week, debt-free year+.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Too many alerts** → ignored. Audit quarterly, delete unused, tune thresholds.
2. **Alert on causes** (CPU) → noisy. Alert on **symptoms** (latency P99, error rate).
3. **No `for` duration** → spike trigger. Always `for: 5m+`.
4. **Missing runbook** → on-call confused at 3 AM. Every alert → runbook URL.
5. **Blameful post-mortem** → fear culture, hide issues. **Blameless** focus on system fixes.

---

## 🧠 Tự kiểm tra (Self-check)

1. **Dashboard variables** — vai trò?
2. Khác **alert on cause** vs **alert on symptom**? Ví dụ.
3. **SLO burn rate alert** — sao tốt hơn "error rate > 5%"?
4. **Inhibition** + **Grouping** — giải quyết vấn đề gì?
5. **Runbook** + **blameless post-mortem** — culture vì sao quan trọng?

<details>
<summary>Gợi ý đáp án</summary>

1. **Variables** = dropdowns at top dashboard (env, service, namespace). User pick → all panels filter automatically. DRY: 1 dashboard reused multiple environments/services. Plus templating from Prometheus labels.

2. **Cause**: low-level metric (CPU > 80%, memory > 90%). Noisy — sometimes high but no impact. **Symptom**: user-facing (P99 latency > 1s, error rate > 1%). What user feels. Cause alerts ignored eventually. Always alert symptoms.

3. **"error rate > 5%"** — either too late (1% might be hours of bad UX) or too sensitive. **SLO burn rate** considers **error budget consumption**. "Burn 100% budget in 2 days" = critical regardless of current %. Multi-window (1h + 5m) prevents false positives + missed slow drift. Google SRE recipe.

4. **Grouping**: 10 pods CrashLoop same time → 1 batched notification (not 10 spam). **Inhibition**: critical alert fire → suppress related warnings on same service. Both reduce alert volume → reduce fatigue → on-call respond effectively.

5. **Runbook**: on-call at 3 AM doesn't think, executes documented steps. Faster MTTR. **Blameless**: post-mortem focus "what allowed this" not "who messed up". Culture engineers report incidents fully → learn → improve system. Blameful = hide issues, repeat mistakes.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Install Grafana

```bash
helm install grafana grafana/grafana -n monitoring
kubectl port-forward -n monitoring svc/grafana 3000:80
```

### Data sources

```
Prometheus     http://prometheus:9090
Loki            http://loki:3100
Tempo           http://tempo:3100
```

### Useful imports

```
315    K8s cluster
1860   Node Exporter
7249   Postgres
12239  FastAPI
```

### Alert rule structure

```yaml
expr: <PromQL>
for: 10m            # Must hold this long
labels: { severity: warning, team: x }
annotations:
  summary: "..."
  runbook_url: "..."
```

### SLO burn rate

```
1h window + 5m window must both exceed (14.4 × SLO_error) = fast burn page
6h window + 30m window must both exceed (6 × SLO_error)   = slow burn warn
```

### Routing

```
Critical → PagerDuty
Warning  → Slack team
Info     → Slack info channel
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Grafana** | OSS dashboard tool |
| **Data source** | Backend Grafana queries |
| **Panel** | Single visualization |
| **Variable** | Dashboard dropdown filter |
| **Dashboard as code** | Git-tracked JSON |
| **Grafana Alerting** | Unified alerting in Grafana |
| **Alertmanager** | Routing + grouping alerts |
| **`for` duration** | Min time condition true before fire |
| **Grouping** | Batch related alerts |
| **Inhibition** | Suppress alerts when superset fires |
| **Silence** | Temporary alert suppression |
| **SLO burn rate** | Error budget consumption velocity |
| **Multi-window alert** | 2 windows must agree |
| **Contact point** | Notification destination (Slack/PD) |
| **Runbook** | Operations procedure doc |
| **Post-mortem** | Incident review document |
| **Blameless** | Culture focus system fixes |
| **MTTR** | Mean Time To Recovery |
| **On-call rotation** | Schedule for incident response |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [Traces & OpenTelemetry — Distributed tracing](03_traces-opentelemetry.md)
- ↑ **Về cụm:** [observability README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [DORA + DevOps](../../../ci-cd/lessons/01_basic/00_what-is-cicd.md) — DevOps metrics include MTTR
- [Linux journalctl](../../../../04_os/linux/lessons/02_intermediate/01_systemd-services.md) — local logs

### 🌐 Tài nguyên tham khảo khác
- 📖 [Grafana docs](https://grafana.com/docs/)
- 📖 [Google SRE Workbook — Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- 📖 [PagerDuty Incident Response](https://response.pagerduty.com/)
- 📖 [Awesome Prometheus alerts](https://samber.github.io/awesome-prometheus-alerts/)
- 📖 [Postmortem template — PagerDuty](https://response.pagerduty.com/after/post_mortem_process/)

---

> 🎯 *Cluster Observability basic 5/5 đóng. Bạn vận hành full observability stack production-grade. Bài kế tiếp ngoài cluster: SLO calculator, OpenTelemetry deep, eBPF observability.*

---

## 📜 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước Install K8s + Anatomy + Panel example Latency + Variables template + Useful variables.
- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Observability sprint #5.
- **v1.1.1 (11/06/2026)** — Việt hoá heading nội dung mô tả sang tiếng Việt (giữ thuật ngữ/brand/param) theo Vietnamese-first.
