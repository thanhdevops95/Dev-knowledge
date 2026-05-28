# Module 15: SRE Labs

---

## 🔧 Lab 1: Define SLOs

```yaml
# slo.yaml
service: counter-app
slos:
  - name: availability
    target: 99.9%
    window: 30d
    sli:
      type: availability
      
  - name: latency
    target: 95th percentile < 200ms
    window: 30d
    sli:
      type: latency
      threshold: 200ms
```

---

## 🔧 Lab 2: Calculate Error Budget

```python
# error_budget.py
import datetime

SLO = 0.999  # 99.9%
WINDOW_DAYS = 30

total_minutes = WINDOW_DAYS * 24 * 60
allowed_downtime = total_minutes * (1 - SLO)

print(f"Total minutes in window: {total_minutes}")
print(f"Allowed downtime: {allowed_downtime:.1f} minutes")
print(f"That's {allowed_downtime/60:.1f} hours per month")
```

---

## 🔧 Lab 3: Create Runbook

```markdown
# Runbook: High Error Rate

## Alert
Error rate > 5% for 5 minutes

## Steps
1. Check application logs
   ```

   kubectl logs -l app=myapp --tail=100

   ```

2. Check database connectivity
   ```

   kubectl exec -it postgres-0 -- pg_isready

   ```

3. Restart if needed
   ```

   kubectl rollout restart deployment/myapp

   ```

## Escalation
If not resolved in 15 minutes, page secondary on-call.
```

---

## 🔧 Lab 4: Write Postmortem

Template for any incident:

- Summary
- Impact
- Timeline
- Root Cause
- Action Items

---

## 📋 Tổng kết

| Lab | Skill |
|-----|-------|
| 1 | Define SLOs |
| 2 | Error budgets |
| 3 | Runbooks |
| 4 | Postmortems |

👉 **[SCENARIOS.md](SCENARIOS.md)**
