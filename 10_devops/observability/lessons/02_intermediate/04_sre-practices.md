# 🎓 SRE practices — SLO + Error budget + Postmortem + On-call

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.1\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 11/06/2026\
> **Level:** Intermediate\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [03_opentelemetry-instrumentation.md](03_opentelemetry-instrumentation.md), basic obs cluster done

> 🎯 *Bài cuối Observability intermediate + cuối DevOps intermediate sprint. Tools alone không reliable production — cần **process**: SLI/SLO numerical commitment, error budget trade reliability vs velocity, blameless postmortem learn from incidents, sustainable on-call rotation. Apply Google SRE book principles.*

## 🎯 Sau bài này bạn sẽ

- [ ] Định nghĩa **SLI/SLO/SLA** cho service production
- [ ] Compute **error budget** + **burn rate**
- [ ] Setup **error budget policy** (freeze deploy khi budget burn)
- [ ] Viết **blameless postmortem** với template
- [ ] **On-call rotation patterns**: schedule, escalation, runbook
- [ ] **Toil reduction**: automate repetitive ops
- [ ] Hiểu **chaos engineering** intro
- [ ] Building reliability culture

---

## Tình huống — Engineering velocity stuck, on-call burnout

Engineering team 20 person, 6 tháng:
- Deploy 5x/day → 1x/week (slow down vì incidents).
- Last 30 days: 12 incidents, 8 different on-calls woken 3am.
- On-call rotation 1 person 1 week. Same SRE on-call 1/3 weeks. Burnout.
- Postmortem: 10 of 12 incidents → "Will look into it". No action items.
- Sếp ask: "Are we 99.9% or 99.99% uptime?". No one knows.

Problems:
1. **No SLO** → no consensus on reliability target.
2. **No error budget** → push deploys when degraded.
3. **Alert noise** → on-call burnout.
4. **Postmortem dead** → no learning.
5. **No toil reduction** → repeat manual work.

Sếp: *"Apply SRE practices. Read Google SRE book + workbook. Bài 04 dạy."*

---

## 1️⃣ SLI / SLO / SLA — Nền tảng

### Định nghĩa

**SLI (Service Level Indicator)**: quantitative measure of aspect of service.
- "% of HTTP requests served < 500ms".
- "% of orders successfully processed".
- "% of frontend page loads < 2s".

**SLO (Service Level Objective)**: target value of SLI.
- "99.9% of HTTP requests served < 500ms over 28-day window".
- "99.95% of orders processed successfully".

**SLA (Service Level Agreement)**: contract with customer, often with penalty.
- "If uptime < 99.95% in any month, customer gets 10% refund".

Hierarchy: SLA = SLO + customer contract. SLO ≥ SLA (internal target stricter than promise).

### Chọn SLI

Categories:
- **Availability**: % success requests.
- **Latency**: % requests faster than threshold.
- **Throughput**: requests/sec capacity.
- **Quality**: % responses with full feature (vs degraded).
- **Freshness**: data lag (cache, replication).
- **Correctness**: % data integrity (rare metric).

User-facing SLIs > infrastructure SLIs. User cares about success/latency, not CPU%.

### Chọn SLO target

SLO target ("3 nines, 4 nines, 5 nines") quyết định cost + complexity. Mỗi "9" thêm tăng cost ~10x. Bảng dưới mapping downtime budget với SLO + recommendation cho từng business type:

| Target | Downtime/month | Downtime/year | Apply to |
|---|---|---|---|
| 99% | 7h 18m | 3.65 days | Internal tool, MVP |
| 99.5% | 3h 39m | 1.83 days | Beta product |
| 99.9% (3 nines) | 43m 12s | 8.76h | **Startup production default** |
| 99.95% | 21m 36s | 4.38h | SaaS, business hours strict |
| 99.99% (4 nines) | 4m 19s | 52m 36s | Banking, payment |
| 99.999% (5 nines) | 25.9s | 5m 15s | Telco, life-critical (expensive!) |

🪞 **Ẩn dụ**: *Mỗi "9" thêm khoảng 10x cost. 99% → 99.9% = simple HA. 99.9% → 99.99% = multi-region active-active. 99.99% → 99.999% = + redundancy infra + custom hardware + military-grade ops.*

### Đừng nhắm 100%

**Why not 100%**:
- Cost rises exponentially (10x per "9").
- Users can't tell difference 99.9% vs 99.99% in most cases.
- **No room for velocity** — every deploy risks SLA.

→ **Aim "good enough"**. Most B2B SaaS: 99.9%. E-commerce: 99.95%. Mission-critical: 99.99%.

### Ví dụ định nghĩa SLI

**FastAPI availability SLI**:
```promql
# SLI = success rate
sum(rate(http_requests_total{status!~"5..", service="fastapi"}[28d]))
/
sum(rate(http_requests_total{service="fastapi"}[28d]))
```

**FastAPI latency SLI** (% requests < 500ms):
```promql
sum(rate(http_request_duration_seconds_bucket{le="0.5", service="fastapi"}[28d]))
/
sum(rate(http_request_duration_seconds_count{service="fastapi"}[28d]))
```

### Định nghĩa SLO as code

OpenSLO format:
```yaml
apiVersion: openslo/v1
kind: SLO
metadata:
  name: fastapi-availability
  displayName: "FastAPI availability"
spec:
  service: fastapi
  description: "% of requests serving 2xx/3xx/4xx (not 5xx)"
  indicator:
    metadata:
      name: success-rate
    spec:
      ratioMetric:
        counter: true
        good:
          metricSource:
            type: prometheus
            spec:
              query: 'sum(rate(http_requests_total{status!~"5..", service="fastapi"}[5m]))'
        total:
          metricSource:
            type: prometheus
            spec:
              query: 'sum(rate(http_requests_total{service="fastapi"}[5m]))'
  timeWindow:
    - duration: 28d
      isRolling: true
  budgetingMethod: Occurrences
  objectives:
    - displayName: "99.9% success"
      target: 0.999
```

Tools generate alerts:
- **Sloth** ([sloth.dev](https://sloth.dev)) — input OpenSLO → output Prometheus rules with burn rate alerts.
- **Pyrra** — UI for SLO management.
- **OpenSLO + Slothius** — modern toolchain.

---

## 2️⃣ Error budget

### Khái niệm

**Error budget** = 100% - SLO = allowed "bad" share.

Example:
- SLO: 99.9% over 28 days.
- Total requests last 28d: 10 million.
- Allowed failures: 0.1% × 10M = **10,000 errors**.
- If 5000 errors in 14 days → **50% budget consumed**.

### Burn rate

**Burn rate** = how fast budget consumed relative to SLO baseline.

- **1.0x burn**: at current error rate, budget exactly exhausted at end of window (sustainable).
- **10x burn**: budget will exhaust in 1/10 window (alert).
- **0.5x burn**: way under budget, can be more risky (deploy).

Formula:
```
burn_rate = current_error_rate / (1 - SLO_target)
         = error_rate / error_budget_allocation
```

Example:
- SLO 99.9% → allowed error rate 0.1%.
- Actual error rate last 5min: 1.44%.
- Burn rate = 1.44% / 0.1% = **14.4x**.

### Alert tiêu thụ budget (mẫu Google SRE)

(Recall lesson 01)

```
Severity   Short window  bạn window   Budget in 1 hour
Critical   5min          1h            14.4x burn   →  ~2% / hour
Critical   30min         6h            6x burn      →  ~5% / hour  
Warning    2h            24h           3x burn      →  ~10% / day
Warning    6h            72h           1x burn      →  baseline
```

→ Two windows confirm: short detects spike, long confirms sustained.

### Error budget policy

**Policy** = rules about what to do when budget consumed.

Example policy:
```
Service: fastapi
SLO: 99.9% availability, 28-day window

Error budget policy:
 ┌─────────────────────────┬──────────────────────────────────┐
 │ Budget Remaining        │ Action                            │
 ├─────────────────────────┼──────────────────────────────────┤
 │ > 50%                   │ Normal — deploy freely            │
 │ 20-50%                  │ Caution — peer review deploys     │
 │ 5-20%                   │ Engineering manager approval      │
 │ < 5%                    │ FREEZE feature deploys, reliability work only │
 │ < 0% (exhausted)        │ FREEZE all non-critical, postmortem mandatory │
 └─────────────────────────┴──────────────────────────────────┘
```

→ **Enforced**, not advisory. ArgoCD/CI integration: deploy gated by budget API.

### Vì sao error budget thiên tài

1. **Common language**: dev + SRE align on "how much can we afford to break".
2. **Velocity-reliability trade-off explicit**: budget left = ship. Budget burned = stabilize.
3. **No blame**: budget exists to be spent. Failures expected.
4. **Forces tooling discipline**: if budget low, can't deploy without canary + rollback ready.

### Tính budget trong Prometheus

Để tính error budget cụ thể, dùng PromQL query lấy success rate trong window 28 ngày + so với SLO target. Hiển thị dashboard Grafana cho team:

```promql
# Budget consumed in 28d
1 - (
  sum(rate(http_requests_total{status!~"5..", service="fastapi"}[28d]))
  /
  sum(rate(http_requests_total{service="fastapi"}[28d]))
)

# Budget remaining (assuming 0.999 target)
(0.001 - <above>) / 0.001 * 100    # as percentage
```

Grafana dashboard panel:
- Current error budget %.
- Trend graph budget over time.
- Burn rate gauge.

---

## 3️⃣ Blameless postmortem

### Vì sao blameless?

After incident, ask "Why?" 5 times → reach **system + process failure**, not individual.

**With blame**:
- "John pushed bad code at 3am" → John defensive, hides info next time.
- Postmortem becomes blame game.
- People stop reporting near-misses.

**Blameless**:
- "Code review missed bug. Why? Reviewer rushed. Why? Friday deadline. Why? Team understaffed. Why? Hiring slow."
- Action items: hire, deadline buffer, mandatory 24h cool-off for big changes.

→ Improve **system**, not punish person.

### Template postmortem

Template chuẩn cho blameless postmortem — 8 section (TL;DR, Impact, Timeline, Root cause, What went well/wrong, Action items, Lessons learned). Dùng cho mọi SEV-1/2 incident:

```markdown
# Postmortem: <Incident Title>

**Status**: Draft / Reviewed / Action items tracked  
**Severity**: SEV-1 / SEV-2 / SEV-3  
**Author**: SRE on-call name  
**Reviewers**: <list>  
**Date of incident**: YYYY-MM-DD  
**Date of postmortem**: YYYY-MM-DD  

## TL;DR
One paragraph: what happened, impact, root cause, fix.

## Impact

Section đầu tiên — định lượng impact cụ thể: bao nhiêu user, bao lâu, doanh thu mất, data loss, SLA breach. Đây là metric guide priority cho action items:

- **User impact**: # users affected, % traffic.
- **Duration**: HH:MM start - HH:MM resolved = total duration.
- **Revenue loss**: $X (if measurable).
- **Data loss**: yes/no, scope.
- **SLA breach**: yes/no.

## Timeline (UTC)

Timeline chi tiết phút phút giây giây — từ trigger (deploy/config change/external) đến resolve. Quan trọng để tìm root cause + cải thiện detection time. UTC để cross-timezone team đọc đúng:

| Time | Event | Source |
|---|---|---|
| 03:00 | Deploy v2.5.0 to prod | GitHub Actions |
| 03:05 | First user error report | Slack #help |
| 03:07 | Alert fired: ErrorRate > 5% | Prometheus → PagerDuty |
| 03:10 | On-call ack alert | PagerDuty |
| 03:15 | On-call identified deploy as suspect | Investigation |
| 03:20 | Rollback initiated | Manual ArgoCD revert |
| 03:25 | Service recovered | Metrics confirm |

## Root cause
Detailed analysis. Use "5 whys" or fishbone.

**Direct cause**: DB query timeout introduced in v2.5.0 commit abc123.

**Contributing factors**:
- Code review missed: reviewer focused on feature, not perf.
- No canary deploy: all-or-nothing rollout.
- No DB query latency alert.
- Test suite didn't cover this query pattern.

## Detection
- How was incident detected? (alert / user report / dashboard)
- Time to detect (TTD): time from impact start to first signal.

## Resolution
- What action ended incident?
- Time to resolve (TTR): time from detection to resolution.

## Lessons learned

### What went well
- Alert fired within 2 min of impact.
- Rollback procedure documented in runbook.
- Communication on Slack #incidents clear.

### What went wrong
- Took 5 min for human ACK (3am — sleeping).
- No automated rollback on error rate spike.
- Test suite missed query regression.

### Where we got lucky
- Incident at 3am (low traffic) — saved $50K loss vs noon.
- Postgres replica took over without manual failover.

## Action items
| # | Action | Owner | Priority | Due |
|---|---|---|---|---|
| 1 | Add canary deploy for payment service | @sre-team | P0 | 2026-06-01 |
| 2 | Add DB query latency SLO + alert | @platform | P1 | 2026-06-15 |
| 3 | Test suite: add slow query regression test | @backend | P1 | 2026-06-10 |
| 4 | Mandatory canary for prod deploys (CI gate) | @platform | P0 | 2026-06-01 |
| 5 | Compensation policy for affected users (10%off) | @customer-success | P2 | 2026-06-05 |

## Communication
- Status page update at <time>.
- Customer email sent to N affected users.
- Slack #incidents log.

## Supporting data
- Logs: https://grafana/loki?...
- Traces: https://tempo/...
- Metrics: https://grafana/dashboard/...
- Slack thread: https://acme.slack.com/...
```

### Họp review postmortem

- **Within 1 week** of incident.
- All involved + impact area.
- Read postmortem 1 day before meeting.
- Meeting: focus on action items, blockers.
- **No blame**. Facilitator interrupt blame.

### Theo dõi action items

Every action item → ticket (Jira/Linear) with:
- Owner.
- Due date.
- Priority.
- Link back to postmortem.

Weekly review: status of all open postmortem action items.

→ **Don't let action items rot**. If action item slip 3 times, escalate.

---

## 4️⃣ Các mẫu on-call rotation

### Mục tiêu của on-call

1. **Service reliability**: respond to alerts quickly.
2. **Sustainability**: SRE not burn out.
3. **Learning**: rotating expose more people to production.
4. **Process improvement**: each on-call surface gaps.

### Các mô hình rotation

**Follow-the-sun** (global team):
- US-West (9am-5pm PT) → US-East → EU → APAC → US-West.
- 24/7 coverage during business hours per region.
- No 3am pages.

**Primary + secondary**:
- Primary on-call gets pages.
- Secondary backup if primary unavailable (sick, asleep).
- Same person both rotates: weekly swap.

**Weekly rotation**:
- 1 person on-call for 1 week.
- Time off: 2-3 weeks before next.
- Bay area / Vietnam often have this.

### Lịch trực (schedule)

```
Week 1: Nguyen Van A (primary), Le Van B (secondary)
Week 2: Le Van B (primary), Carol (secondary)
Week 3: Carol (primary), Dan (secondary)
Week 4: Dan (primary), Nguyen Van A (secondary)
```

→ Rotate 4-week cycle. 4 people minimum. 6+ better for less pressure.

### Bàn giao (hand-off)

End of week, current on-call → next on-call:
- Active incidents.
- Pending action items.
- Known issues (silenced alerts, ongoing investigation).
- Schedule changes / maintenance windows planned.

15-30 min meeting. Documented in handover doc.

### Đãi ngộ (compensation)

- **Overtime pay**: 1-1.5x regular pay for on-call hours.
- **Time off**: 1 day after page-heavy week.
- **Phone reimbursement**.
- **Page allowance**: if > X pages, reduce next week.

→ Burnout prevention. SREs don't quit if compensated.

### Metric vệ sinh alert

Track per on-call:
- # alerts (target: < 5/week).
- # pages (target: < 2/week).
- # actionable alerts (target: > 80%).
- Time to ack.
- Time to resolve.

Weekly review:
- Top noisy alerts → fix.
- Repeat alerts → automate.
- False positives → silence/delete.

### Tự động hoá runbook

Every alert → runbook URL in annotation:
```
runbook_url: https://wiki.acme/runbooks/{{ .Labels.alertname }}
```

Runbook structure:
```markdown
# Runbook: HighErrorRate (FastAPI)

## What this alert means
FastAPI error rate exceeded 1% for 5 minutes.

## Immediate response
1. Check dashboard: https://grafana/d/fastapi
2. Check recent deploys: https://argo/applications/fastapi
3. If recent deploy → rollback:
   ```
   argocd app rollback fastapi <prev-rev>
   ```

## Investigation
1. Check logs: https://grafana/loki?q={service="fastapi"} | json | level="error"
2. Check upstream dependencies (DB, Redis):
   - Postgres: https://grafana/d/postgres
   - Redis: https://grafana/d/redis
3. Check infra: node CPU/memory.

## Escalation
If can't resolve in 30 min:
- Page secondary on-call.
- Notify @engineering-lead.
- Open #incident channel in Slack.

## Common causes
1. **Bad deploy** (50% of incidents): rollback first.
2. **DB overload**: check connection pool, slow queries.
3. **Upstream API down**: check Stripe/external status.
4. **Resource exhaustion**: K8s pod limits, node capacity.
```

→ Runbook = institutional knowledge. Reduce on-call cognitive load.

### Incident command (sự cố nghiêm trọng)

For SEV-1 (major outage):
- **Incident Commander (IC)**: coordinator. Not technical investigator.
- **Communications Lead**: customer status + Slack updates.
- **Technical Lead**: actual debugging.

Roles separate to avoid context-switching.

Tools:
- **Incident.io** / **PagerDuty Incident Response**: automated channel creation, roles.
- **Status page** for customer communication (Statuspage.io / Cachet).

---

## 5️⃣ Toil reduction

### Toil là gì?

Per Google SRE book:
> **Toil** = manual, repetitive, automatable, tactical (no enduring value) ops work.

Examples:
- Manually restart pod every Monday morning (memory leak).
- Approving routine PRs.
- Manually rotating credentials quarterly.
- Manual cert renewal.

**Not toil**:
- Investigating novel incident (not repetitive).
- Architecting new system (strategic).

### Quy tắc 50% (Google)

Aim: < 50% SRE time on toil. > 50% on engineering (automation, projects).

If toil > 50% → hire more, or automate.

### Ví dụ giảm toil

**Manual cert renewal** → cert-manager auto.
**Manual DB credential rotation** → Vault dynamic credentials.
**Manual scaling on Black Friday** → HPA + KEDA.
**Manual deploy** → ArgoCD GitOps.
**Manual SQL migration** → automated tools (Flyway, Liquibase).
**Manual pod restart on memory leak** → fix memory leak (root cause).

### Nhật ký toil

Each on-call week: log toil tasks done. Quarterly:
- Top toil → automate.
- Track # toil tasks reduction.

→ Engineering culture incentivize automation.

---

## 6️⃣ Giới thiệu chaos engineering

### Khái niệm

**Chaos engineering** = inject failures into production-like system → discover weaknesses before they cause real incident.

Pioneered by Netflix (Chaos Monkey 2010+).

### Game days

Quarterly exercise:
- Define hypothesis: "If we kill 1 Postgres replica, app continues with 0 impact."
- Inject failure: kubectl delete pod postgres-1.
- Observe: monitor SLOs.
- Result: pass/fail → action items.

### Công cụ

- **Chaos Mesh** (CNCF): K8s-native chaos.
- **Litmus**: K8s chaos.
- **Gremlin**: commercial.
- **AWS Fault Injection Simulator**: AWS native.

### Các kịch bản chaos thường gặp

1. **Pod kill**: random pod termination → test HPA, rolling update.
2. **Network partition**: between services → test retry, circuit breaker.
3. **DNS failure**: simulate DNS down.
4. **CPU spike**: stress test scaling.
5. **Disk full**: test alerting + cleanup.
6. **Latency injection**: 1s delay → test timeout config.

### Áp dụng chaos engineering

**Maturity tiers**:
1. **Pre-production only**: dev/staging chaos.
2. **Production-readiness review**: chaos test before launch.
3. **Continuous chaos**: scheduled chaos in production daily.
4. **GameDays**: monthly company-wide exercise.

→ Start small. Dev cluster, single failure type. Build muscle.

---

## 7️⃣ Văn hoá reliability

### Các trụ cột

1. **Embrace risk**: 100% reliability impossible. Aim "good enough", spend savings on velocity.
2. **Postmortem culture**: every incident learning opportunity. Blameless.
3. **Toil reduction**: 50% engineering, < 50% manual ops.
4. **Service ownership**: dev team responsible for production behavior, not "throw over wall to ops".
5. **Investment in reliability**: budget time/people. Reliability is feature.

### Dashboard metric reliability

Engineering org-level dashboard:
- SLO compliance per service.
- Incident frequency / MTTR / MTBF.
- Postmortem completion rate.
- Action item closure rate.
- Toil percentage (survey-based).
- Deploy frequency / lead time / change failure rate (DORA metrics).

### DORA metrics

Annual State of DevOps Report (Google):
| Metric | Elite | High | Medium | Low |
|---|---|---|---|---|
| Deploy frequency | On-demand | Daily-Weekly | Weekly-Monthly | < Monthly |
| Lead time for changes | < 1 hour | 1 day | 1 week | > 1 month |
| Change failure rate | 0-15% | 16-30% | 31-45% | > 45% |
| MTTR | < 1 hour | < 1 day | < 1 week | > 1 week |

→ Aim "Elite" or "High" via SRE practices.

### Playbook incident response (tổng quan)

```
Detect → Acknowledge → Investigate → Mitigate → Resolve → Postmortem
  ↓         ↓             ↓              ↓          ↓          ↓
Alert    On-call ack   Logs/traces   Rollback   All OK?    Action items
PageDuty                Dashboard     Failover   Verify
                                       Hotfix
```

Each step has SLA:
- Detect: ≤ 2 min (alert fires).
- Acknowledge: ≤ 5 min (on-call response).
- Mitigate: ≤ 30 min (stop bleeding).
- Resolve: ≤ 1 hour (full fix or workaround).
- Postmortem: ≤ 5 days draft, ≤ 14 days reviewed.

---

## 8️⃣ Hands-on: Cài đặt SLO + budget alert + dashboard

### Bước 1: Định nghĩa SLO với Sloth

```bash
# Install Sloth
brew install slok/sloth/sloth

# Or download binary
```

```yaml
# fastapi-slo.yaml
version: "prometheus/v1"
service: fastapi
labels:
  team: backend
slos:
  - name: requests-availability
    objective: 99.9
    description: "% of requests served (non-5xx)"
    sli:
      events:
        error_query: sum(rate(http_requests_total{service="fastapi",status=~"5.."}[{{.window}}]))
        total_query: sum(rate(http_requests_total{service="fastapi"}[{{.window}}]))
    alerting:
      name: FastapiAvailabilityHigh
      labels:
        category: availability
      annotations:
        summary: "FastAPI availability SLO error budget burning fast"
      page_alert:
        labels:
          severity: critical
      ticket_alert:
        labels:
          severity: warning

  - name: requests-latency
    objective: 99.0
    description: "% of requests served < 500ms"
    sli:
      events:
        error_query: sum(rate(http_request_duration_seconds_bucket{service="fastapi",le="0.5"}[{{.window}}]))
        total_query: sum(rate(http_request_duration_seconds_count{service="fastapi"}[{{.window}}]))
    alerting:
      ...
```

### Bước 2: Sinh Prometheus rules

```bash
sloth generate -i fastapi-slo.yaml -o fastapi-rules.yaml
```

Output: Prometheus rules with multi-window burn rate alerts auto-generated.

### Bước 3: Apply

```bash
kubectl create configmap fastapi-slo-rules \
  --from-file=fastapi-rules.yaml \
  -n monitoring
```

### Bước 4: Grafana dashboard

Use Sloth's pre-built Grafana dashboard:
- Budget remaining gauge.
- Burn rate timeseries.
- SLO compliance over 28 days.

Or import [SLO dashboard template](https://grafana.com/grafana/dashboards/14348).

### Bước 5: Kiểm chứng alert

```bash
kubectl get prometheusrule fastapi-slo -n monitoring
# Contains: ErrorBudgetBurnFast (critical, 5min/1h), ErrorBudgetBurnSlow (warning, 6h/24h)

# Watch Alertmanager
kubectl port-forward svc/alertmanager-operated -n monitoring 9093:9093
# Open http://localhost:9093
```

Generate errors:
```bash
for i in {1..1000}; do
  curl https://api.acmeshop.vn/error-endpoint
done
```

→ Alert fires within 2-5 min. Verify Slack/PagerDuty receive.

### Bước 6: Thực thi error budget policy

CI integration:
```yaml
# .github/workflows/deploy.yml
- name: Check error budget
  run: |
    BUDGET=$(curl -s 'http://prometheus:9090/api/v1/query?query=fastapi_slo_budget_remaining' | jq -r '.data.result[0].value[1]')
    if (( $(echo "$BUDGET < 5" | bc -l) )); then
      echo "Error budget below 5%. Blocking deploy."
      exit 1
    fi
```

→ Deploy gated. Force discipline.

---

## 💡 Cạm bẫy thường gặp & Best practice

### ❌ Cạm bẫy: SLO too strict — chronic violation

→ SLO 99.99% but actual 99.8%. SLO violated weekly → ignored.

→ **Fix**: Realistic SLO. Measure actual baseline, set SLO 1 tier higher. Iterate quarterly.

### ❌ Cạm bẫy: No error budget policy enforcement

→ "We have SLO 99.9%". But team deploys feature even at -10% budget. SLO advisory only.

→ **Fix**: Policy in writing + CI gate + leadership backing. Budget exhausted = freeze, no exception.

### ❌ Cạm bẫy: Postmortem becomes blame game

→ "John did X" → John defensive → next incident John hides info.

→ **Fix**: Facilitator interrupt blame. Reframe "John did X" → "System allowed X". Multiple people sign off on review.

### ❌ Cạm bẫy: Action items rot

→ 6 months later: 50 open action items from postmortems. No one tracks.

→ **Fix**: 
- Ticket each item with due date.
- Weekly review (engineering management).
- After 3 slips, escalate.
- Quarterly "action item amnesty" — close stale ones.

### ❌ Cạm bẫy: On-call 1-person small team

→ Same person on-call every other week → burnout in 3 months.

→ **Fix**: Hire to 4+ on-call rotation. If can't hire, reduce SLO (acknowledge limitation).

### ❌ Cạm bẫy: SLI doesn't match user experience

→ SLI: "Server return 200". But frontend JS broken → user sees error. SLI passes, user unhappy.

→ **Fix**: SLI based on **user-facing signals**. Synthetic monitoring (Datadog Synthetics, Pingdom). Real User Monitoring (RUM) — actual browser metrics.

### ❌ Cạm bẫy: Chaos engineering in production with no buy-in

→ SRE inject failures, leadership panics, banned.

→ **Fix**: Build trust gradually. Pre-prod chaos first → monthly GameDay → eventually continuous prod chaos. Document each, share learning.

### ✅ Best practice: Service ownership

Dev team responsible for:
- Run their service in production.
- Respond to their alerts.
- Write postmortems.

SRE team responsible for:
- Platform (K8s, observability, CI/CD).
- Cross-cutting concerns (capacity planning, networking).
- Training dev teams in SRE practices.

→ "You build it, you run it." (Werner Vogels, Amazon).

### ✅ Best practice: Engineering manager attend on-call

- Once per quarter, EM does on-call shadow.
- Experience pain firsthand.
- Drives toil reduction priority.

### ✅ Best practice: Public SLO dashboard

Internal dashboard visible to all engineering:
- Every service's SLO compliance.
- Trends over quarters.
- Highlight at-risk services.

→ Peer pressure for reliability. Visibility drives accountability.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** Vì sao 100% reliability không phải target?

<details>
<summary>💡 Đáp án</summary>

**Cost vs benefit**:
- 99% → 99.9% = ~10x infrastructure cost (HA + redundancy).
- 99.9% → 99.99% = ~10x more (multi-region active-active, more ops complexity).
- 99.99% → 99.999% = ~10x more (specialized hardware, military-grade processes).

**User perception**: most users can't tell difference 99.9% vs 99.99%. Below 99% they notice.

**Velocity cost**: every "9" adds ops burden. Less time for feature development. Higher process overhead.

**No room for risk**: 100% means **every deploy must be perfect**. No canary, no experiments, no learning.

**Cost-benefit example** (Google SRE book):
- Service makes $1M/year.
- 99% uptime cost: $100K infrastructure.
- 99.9%: $300K (3x cost for 10x less downtime).
- 99.99%: $1M (4x more, but downtime difference is 50 min/year vs 5 min/year — most users don't notice).

→ "Aim 99.9% is realistic SLO. Spend savings on features." (paraphrased Ben Treynor, SRE founder).

**Exception**: life-critical (medical, aerospace), regulatory (banking some) — pay the price.
</details>

**Q2.** Vì sao **error budget exhausted = freeze deploy** works?

<details>
<summary>💡 Đáp án</summary>

**Without budget freeze**:
- Service breaking → engineers deploy anyway (hoping to fix forward).
- Each deploy adds new bugs → spiral down.
- 1 month later: 99.5% actual, SLO 99.9%, customers angry.

**With budget freeze**:
- Budget hits 0% → freeze feature deploys.
- Engineers focus reliability work: fix bugs, improve tests, add canary.
- 2 weeks later: actual improves to 99.95%, budget refreshes.
- Then resume feature work.

**Why it works**:
1. **Forcing function**: dev incentive aligned. Want to ship features → must keep reliability.
2. **Explicit trade-off**: not "should we work on reliability?" but "we MUST until budget restored".
3. **Time-bound**: not permanent freeze. As soon as budget refreshes, ship.
4. **Cultural shift**: reliability is everyone's job, not just SRE.

**Implementation**:
- CI deploy step queries budget API.
- If < 5%, fail with "Budget exhausted. Reliability work only."
- Override possible with leadership approval (logged).

**Critical**: leadership must back. If EM say "deploy anyway, we need this feature", budget policy dies.

**Side effect**: feature teams learn to test better, add canary, write more reliable code — because their feature deploy depends on reliability of OTHER services in their org. Game-theoretic positive feedback.

→ Error budget aligns velocity + reliability incentives.
</details>

**Q3.** Postmortem "5 whys" method — example?

<details>
<summary>💡 Đáp án</summary>

**Method**: ask "Why?" 5 times to dig past surface symptoms to systemic root cause.

**Example**: Payment service crashed at 3am.

**Why 1**: Why did payment service crash?
→ OOM (out of memory).

**Why 2**: Why OOM?
→ Memory leak in v2.5.0 release.

**Why 3**: Why was memory leak in release?
→ Code review didn't catch it.

**Why 4**: Why didn't review catch?
→ Reviewer rushed; release deadline Friday.

**Why 5**: Why rushed?
→ Team underestimated complexity; sprint planning didn't allocate buffer.

**Action items**:
- L1 surface fix: rollback v2.5.0, fix memory leak.
- L2 immediate: add memory leak test to CI.
- L3 process: sprint planning include 20% buffer for complex changes.
- L4 culture: train team on code review for performance.
- L5 architecture: investigate memory profiler tooling in CI.

**Why "5 whys" works**:
- Don't stop at "John pushed bad code" (surface, individual blame).
- Reach **system + process** failure (allocation, training, tooling).
- Action items address root cause → prevent recurrence.

**Variations**:
- **Fishbone diagram**: visualize causes (people / process / tools / environment).
- **Cynefin framework**: classify domain (simple / complicated / complex / chaotic).
- **Pre-mortem**: "Imagine this fails in 1 year. Why?" — proactive.

→ Postmortem quality matters more than quantity. 1 good postmortem with implemented actions > 10 shallow ones.
</details>

**Q4.** On-call sustainable practices — what makes / breaks it?

<details>
<summary>💡 Đáp án</summary>

**Makes sustainable**:

1. **Sufficient rotation size** (4-6+ people).
   - 1 week on, 2-3 weeks off.
   - 2-person teams = burnout in 3 months.

2. **Quality alerts** (low noise).
   - < 5 alerts/week.
   - > 80% actionable.
   - No false positives.

3. **Documented runbooks**.
   - Every alert → runbook.
   - Common scenarios covered.
   - Update after each incident.

4. **Compensation**:
   - Overtime pay or time off (1 day after page-heavy week).
   - Phone bill reimbursement.

5. **Escalation paths**:
   - Secondary on-call.
   - Engineering lead.
   - SRE manager.
   - On-call can call for help without judgment.

6. **Tooling**:
   - PagerDuty / OpsGenie professional setup.
   - Auto-rollback / self-healing for common issues.

7. **Schedule swap flexibility**:
   - Tools (Google Calendar + PagerDuty schedule) allow self-swap.
   - No bureaucratic approval.

**Breaks**:

1. **Same person every week** (small team, can't hire).
2. **Alert spam** (200/week, ignore everything).
3. **No runbook** ("just figure out").
4. **No compensation** ("part of job, suck it up").
5. **No escalation** ("you handle alone").
6. **Bureaucratic schedule** (manager approval for swap).
7. **Pages for non-actionable** (warm-fuzzy alert, alert-fatigue).

**Anti-pattern**:
- "Hero culture": always-on Slack, glorify long hours.
- Encourage burnout, attrition.

**Net**: on-call should be **slightly inconvenient**, not **horrible**. If horrible, team has fundamental issues.

→ SRE manager job: make on-call sustainable. If fail, can't hire/retain.
</details>

**Q5.** Toil reduction — measuring + reducing in practice?

<details>
<summary>💡 Đáp án</summary>

**Definition** (Google SRE book):
- Manual.
- Repetitive.
- Automatable.
- Tactical (no enduring value).
- Devoid of long-term strategic value.
- Scales linearly with service growth.

**Measure**:

1. **Survey** (quarterly):
   - "% of last quarter on toil vs engineering?"
   - Categorize: cert renewal, manual deploy, troubleshoot known issues, etc.

2. **Time tracking** (if culturally OK):
   - Tag work as "toil" vs "project" in Jira/Linear.

3. **Toil log per on-call week**:
   - SRE records: "3 hours rotating certs, 1 hour DB credential rotation, 2 hours restarting OOM pod."

**50% rule**:
- Toil should be < 50% of SRE time.
- > 50% → hire more SREs OR automate aggressively.

**Reduce — pattern**:

| Toil | Automation |
|---|---|
| Manual cert renewal | cert-manager |
| Manual DB cred rotation | Vault dynamic credentials |
| Manual restart OOM pod | Fix memory leak (root cause) |
| Manual scale before sale | HPA + KEDA |
| Manual deploy | ArgoCD GitOps |
| Manual SQL migration | Flyway / Liquibase |
| Manual log cleanup | Loki retention |
| Manual disk monitoring | Predict_linear alert + Karpenter |
| Manual user onboarding | API + self-service portal |
| Manual K8s namespace creation | Crossplane / Backstage |

**Project**: each quarter, pick top toil item, allocate 20% of SRE time to automate.

**Anti-pattern**:
- "We don't have time to automate" — circular: toil consume time, prevent automation.
- Solution: leadership protect 20% engineering time.

**Cultural shift**:
- Reward automation work in performance review.
- Show ROI: "Automated cert renewal saved 50 hours/year."
- Track toil reduction quarterly.

→ Toil reduction = compound interest. Each saved hour invest in more reduction.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

```yaml
# === SLO definition (OpenSLO) ===
apiVersion: openslo/v1
kind: SLO
metadata: { name: <service-slo> }
spec:
  service: <service>
  indicator:
    spec:
      ratioMetric:
        good: { metricSource: { query: "..." } }
        total: { metricSource: { query: "..." } }
  objectives:
    - target: 0.999
  timeWindow:
    - duration: 28d
      isRolling: true
```

```bash
# === Sloth generate rules ===
sloth generate -i slo.yaml -o rules.yaml

# === Compute error budget ===
# In PromQL:
# 1 - (sum(rate(... status!~"5.." [28d])) / sum(rate(... [28d])))
```

```markdown
# === Postmortem template (minimal) ===
## TL;DR
## Impact (users, duration, $)
## Timeline (UTC)
## Root cause (5 whys)
## Action items (with owner + due)
## Lessons learned (went well / wrong / lucky)
```

```yaml
# === On-call rotation (PagerDuty equivalent) ===
schedule:
  rotation_type: weekly
  start: 2026-05-24T00:00:00Z
  members:
    - alice
    - bob
    - carol
    - dan
overrides:
  - user: alice
    start: 2026-06-15
    end: 2026-06-22
    reason: vacation
```

```yaml
# === Error budget policy (deploy gate) ===
- name: Check budget
  run: |
    BUDGET=$(curl -s 'http://prometheus/api/...')
    [[ $BUDGET < 0.05 ]] && exit 1
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Term | Vietnamese / Explanation |
|---|---|
| **SLI** | Service Level Indicator — metric measuring aspect |
| **SLO** | Service Level Objective — target value of SLI |
| **SLA** | Service Level Agreement — contract with penalty |
| **Error budget** | 100% - SLO = allowed unreliability |
| **Burn rate** | Speed of error budget consumption (× normal) |
| **Multi-window alert** | Alert with short + long windows confirming |
| **OpenSLO** | Open spec for SLO as code |
| **Sloth** | Tool generate Prometheus rules from OpenSLO |
| **Pyrra** | UI for SLO management |
| **Postmortem** | Document explaining incident |
| **Blameless** | Postmortem culture: focus system, not individual |
| **5 whys** | Root cause method (ask why 5 times) |
| **Action item** | Concrete task to prevent recurrence |
| **On-call rotation** | Schedule of who responds to alerts |
| **Primary / secondary** | On-call hierarchy |
| **Incident commander** | Coordinator during incident |
| **Runbook** | Step-by-step incident response document |
| **Toil** | Manual repetitive automatable ops work |
| **50% rule** | Aim < 50% SRE time on toil |
| **Chaos engineering** | Inject failures to discover weaknesses |
| **Game day** | Scheduled chaos exercise |
| **DORA metrics** | Deploy freq + Lead time + MTTR + Change failure rate |
| **MTTR** | Mean Time To Recovery |
| **MTBF** | Mean Time Between Failures |
| **TTD** | Time To Detect (alert fires after impact) |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [OpenTelemetry instrumentation — Spans + Context propagation + Sampling](03_opentelemetry-instrumentation.md)
- ↑ **Về cụm:** [Observability README](../../README.md)
- 🎯 Hoàn thành Observability intermediate cluster!

### 🧩 Các chủ đề có thể bạn quan tâm
- 🔁 [CI/CD intermediate Progressive delivery](../../../ci-cd/lessons/02_intermediate/04_progressive-delivery.md) — canary uses SLO threshold
- ☸️ [K8s intermediate](../../../kubernetes/lessons/02_intermediate/) — production foundation

### Tài nguyên ngoài (must-read)
- 📖 [Google SRE Book](https://sre.google/sre-book/table-of-contents/) — free, the bible
- 📖 [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) — practical
- 📖 [The Site Reliability Workbook](https://sre.google/workbook/alerting-on-slos/) — alerting on SLOs chapter
- 📖 [Sloth docs](https://sloth.dev/)
- 📖 [OpenSLO](https://openslo.com/)
- 📖 [Pyrra](https://github.com/pyrra-dev/pyrra)
- 📖 [Incident.io](https://incident.io/) — incident management SaaS
- 📖 [PagerDuty Incident Response](https://response.pagerduty.com/) — best practices
- 📖 [State of DevOps Report](https://cloud.google.com/devops/state-of-devops) — DORA metrics
- 📖 [Chaos Mesh](https://chaos-mesh.org/)
- 📖 [Awesome SRE](https://github.com/dastergon/awesome-sre)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Lesson 04 cuối Obs intermediate + cuối DevOps intermediate sprint. SLI/SLO/SLA definition + error budget compute + multi-window burn rate alert + error budget policy enforcement + blameless postmortem template (5 whys) + on-call sustainable rotation patterns + toil reduction (50% rule) + chaos engineering intro + DORA metrics. Apply Google SRE Book principles. 7 pitfall + 3 best practice + 5 self-check + cheatsheet.
- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước Choose SLO target + Compute budget Prometheus + Postmortem template + Impact + Timeline.
- **v1.1.1 (11/06/2026)** — Việt hoá heading nội dung mô tả sang tiếng Việt (giữ thuật ngữ/brand/param) theo Vietnamese-first.
