# 🚒 SRE Practices — Site Reliability Engineering

> `[ADVANCED]` — Vận hành hệ thống ở quy mô production

---

## SRE là gì?

SRE = **Software Engineering áp dụng vào Operations**. Thay vì ops team xử lý manual, SRE dùng code + automation để đảm bảo hệ thống reliable.

Google tạo ra SRE năm 2003 khi nhận ra: "Nếu thuê thêm ops mỗi khi scale, chi phí tăng tuyến tính với traffic. Phải **automate everything**."

**SRE vs DevOps:**
- DevOps = **văn hóa** (dev + ops collaborate)
- SRE = **implementation cụ thể** (DevOps + engineering rigor)
- Mọi SRE team đều DevOps, nhưng không phải DevOps team nào cũng SRE

---

## 1. SLI, SLO, SLA — Đo reliability bằng số

### Tại sao cần metrics cụ thể?

"Hệ thống phải ổn định" là yêu cầu mơ hồ. 99% uptime nghe đẹp, nhưng thực tế:

```
99%    uptime = 3.65 ngày downtime/năm   (≈ 7.2 giờ/tháng)
99.9%  uptime = 8.76 giờ downtime/năm    (≈ 43 phút/tháng)
99.99% uptime = 52.6 phút downtime/năm   (≈ 4.3 phút/tháng)
99.999% ("five nines") = 5.26 phút/năm   (≈ 26 giây/tháng!)
```

Mỗi "9" thêm vào **tốn gấp 10x chi phí** để đạt được. Vậy target bao nhiêu "9" là đủ?

### SLI (Service Level Indicator) — "Đo cái gì?"

```
SLI = metric cụ thể phản ánh user experience

Phổ biến nhất:
  Availability:  % requests thành công (non-5xx)
  Latency:       % requests < threshold (P99 < 200ms)
  Error rate:    % requests trả error
  Throughput:    requests/second xử lý được

Ví dụ:
  SLI: "99.2% requests trả về thành công trong 30 ngày qua"
  SLI: "P99 latency = 180ms (99% requests < 200ms)"
```

### SLO (Service Level Objective) — "Target bao nhiêu?"

```
SLO = target cho SLI mà team CAM KẾT

Ví dụ:
  SLO: "Availability ≥ 99.9% per month"
  SLO: "P99 latency ≤ 200ms"
  SLO: "Error rate ≤ 0.1%"

Tại sao không target 100%?
→ 100% = không bao giờ deploy (mỗi deploy có risk!)
→ SRE cân bằng: reliability VỪA ĐỦ + velocity deploy nhanh
```

### Error Budget — "Còn bao nhiêu lỗi được phép?"

Error budget là concept cốt lõi của SRE — nó biến reliability từ cuộc tranh cãi "dev muốn ship nhanh vs ops muốn ổn định" thành **con số cụ thể** cả 2 bên đồng ý:

```
SLO: 99.9% availability/tháng
Error Budget: 100% - 99.9% = 0.1% = 43 phút downtime/tháng

Tháng này đã dùng 20 phút (1 incident) → còn 23 phút
→ Đủ budget → ship feature mới! 🚀

Tháng sau đã dùng 40 phút (2 incidents) → còn 3 phút
→ Gần hết budget → FREEZE deployments! Chỉ fix bugs. 🛑
```

---

## 2. Incident Management — Khi hệ thống gặp sự cố

### Incident Response Process

```
Detection (phát hiện):
  Alert → PagerDuty/Opsgenie → On-call engineer nhận

Triage (đánh giá):
  Severity 1 (Critical): Toàn bộ hệ thống down → Toàn team
  Severity 2 (Major):    1 feature chính down → On-call + lead
  Severity 3 (Minor):    Performance degraded → On-call
  Severity 4 (Low):      No user impact → Next business day

Response (xử lý):
  1. MITIGATE trước (rollback, restart, failover) — goal: giảm impact
  2. ROOT CAUSE sau (debug, analyze) — goal: hiểu tại sao
  
  ❌ Sai: Dành 2 giờ debug trong khi users bị ảnh hưởng
  ✅ Đúng: Rollback ngay (2 phút) → users OK → debug khi calm
```

### Postmortem — Blameless Culture

Sau mỗi incident, viết postmortem. **Blameless** = không đổ lỗi cá nhân, focus vào hệ thống:

```markdown
## Incident Postmortem: API Outage 2026-03-04

### Summary
API down 23 phút do database connection pool exhausted.

### Timeline (UTC)
- 14:00 — Deploy v2.3.1 with new feature
- 14:15 — Alert: error rate > 5%
- 14:17 — On-call acknowledges
- 14:20 — Identified: DB connections maxed out (100/100)
- 14:23 — Rollback to v2.3.0
- 14:25 — Service recovered

### Root Cause
New feature opened DB connections without closing them in error path.
Connection pool exhausted in ~15 minutes under production load.

### Contributing Factors
- No connection pool monitoring alert (chỉ alert error rate)
- Load testing missed this scenario (test data quá nhỏ)

### Action Items
- [ ] Add connection pool monitoring alert (Owner: SRE, Due: 3/7)
- [ ] Fix connection leak in new feature (Owner: Dev, Due: 3/5)
- [ ] Add load test for connection patterns (Owner: QA, Due: 3/10)
- [ ] Add pre-deploy DB connection check to CI (Owner: SRE, Due: 3/14)
```

---

## 3. On-Call — Trực sự cố

### Thiết kế on-call bền vững

On-call burn out nhanh nếu thiết kế sai. Principles:

```
1. Rotation: Maximum 1 tuần on-call, ít nhất 2 tuần off
2. Compensation: Trả thêm tiền hoặc thời gian nghỉ bù
3. Escalation: Nếu on-call không resolve trong 30 phút → escalate
4. Runbooks: Document sẵn cách handle common alerts
5. Reduce toil: Mỗi quarter, automate ≥1 manual task
```

### Runbook example

```markdown
## Alert: High Error Rate (> 5%)

### Quick Check
1. Check dashboard: grafana.internal/d/api-overview
2. Identify: which endpoint? which error code?
3. Check recent deploys: `kubectl rollout history deployment/api`

### Common Causes
| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| All 5xx | DB down | Check DB status, failover |
| 1 endpoint | Code bug | Rollback last deploy |
| Intermittent | External dependency | Check third-party status |

### Rollback
kubectl rollout undo deployment/api
# Verify: watch 'curl -s api.internal/health'
```

---

## 4. Toil — Công việc manual lặp lại

**Toil** = công việc manual, repetitive, automatable, không tạo giá trị lâu dài.

```
❌ Toil examples:
  - Manually restart crashed pods
  - Manually scale instances khi traffic cao
  - Manually approve routine deploys
  - Copy-paste config giữa environments
  - Manually create user accounts

✅ Automate:
  - Auto-restart: Kubernetes liveness probes
  - Auto-scale: HPA, KEDA
  - Auto-deploy: CI/CD pipelines
  - Config as code: Terraform, Helm
  - Self-service: Internal tools, chatops
```

**Target**: Toil < 50% thời gian SRE. Nếu > 50% → quá nhiều manual work, cần hire hoặc automate.

---

## Bài tập thực hành

- [ ] Định nghĩa SLI/SLO cho API service (availability, latency)
- [ ] Viết runbook cho 3 common alerts
- [ ] Tính error budget: 99.9% SLO, track downtime 1 tháng
- [ ] Postmortem: viết blameless review cho 1 incident giả lập

---

## Tài nguyên thêm

- [Google SRE Book](https://sre.google/sre-book/table-of-contents/) — Free, definitive guide
- [Google SRE Workbook](https://sre.google/workbook/table-of-contents/) — Practical examples
- [Incident.io Blog](https://incident.io/blog) — Incident management best practices
