# Module 15: SRE (Site Reliability Engineering)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **SRE** | - | Site Reliability Engineering - Kỹ thuật đảm bảo độ tin cậy |
| **SLI** | - | Service Level Indicator - Chỉ số đo (latency, error rate) |
| **SLO** | - | Service Level Objective - Mục tiêu (99.9% uptime) |
| **SLA** | - | Service Level Agreement - Cam kết với khách hàng |
| **Error Budget** | - | Ngân sách lỗi - Thời gian downtime cho phép |
| **Toil** | - | Công việc thủ công, lặp lại, có thể tự động hóa |
| **Incident** | - | Sự cố ảnh hưởng service |
| **Postmortem** | - | Phân tích sau sự cố để học hỏi |
| **Blameless** | - | Không đổ lỗi - Focus vào hệ thống, không phải cá nhân |
| **On-call** | - | Trực ca - Người phản hồi alerts |
| **MTTR** | - | Mean Time To Recovery - Thời gian phục hồi trung bình |
| **MTTF** | - | Mean Time To Failure - Thời gian giữa các lỗi |
| **Runbook** | - | Hướng dẫn xử lý sự cố |

---

## 📖 SRE là gì? (Định nghĩa từ gốc)

### Bối cảnh: Tại sao SRE ra đời?

**Năm 2003, Google gặp vấn đề:**

Họ có hàng nghìn servers chạy services cho hàng trăm triệu users. Đội Operations (Ops) truyền thống không thể scale:

- Manual work tăng theo số servers
- "Firefighting" liên tục - chạy từ incident này sang incident khác
- Dev muốn release nhanh, Ops muốn ổn định → Conflict

**Google tạo ra SRE để giải quyết:**

> **SRE (Site Reliability Engineering) = Áp dụng software engineering để giải quyết operations problems**

Thay vì Ops làm manual tasks, SRE engineers **viết code để automate** những công việc đó.

### SRE vs DevOps vs Traditional Ops

| Aspect | Traditional Ops | DevOps | SRE |
|--------|-----------------|--------|-----|
| **Focus** | Keep systems running | Culture, collaboration | Reliability qua engineering |
| **Approach** | Manual, reactive | Automation, CI/CD | Automation + SLOs + Error Budgets |
| **Metrics** | Uptime | Deployment frequency | SLI/SLO/Error Budget |
| **Team structure** | Separate from Dev | Integrated with Dev | Embedded OR separate with defined interface |

**Quan hệ DevOps và SRE:**

> "SRE là một implementation cụ thể của DevOps" - Google

```
DevOps = Philosophy, Culture (WHAT)
SRE = Specific practices, tools, metrics (HOW)
```

Ví dụ:

- DevOps nói: "Dev và Ops nên collaborate"
- SRE nói: "Đây là cách: Error Budgets định nghĩa khi nào Dev được phép ship features"

### Core principles của SRE

| Principle | Giải thích |
|-----------|------------|
| **50% Engineering** | SRE dành ≤50% time cho ops work, còn lại cho engineering |
| **SLO-based** | Mọi quyết định dựa trên Service Level Objectives |
| **Error Budgets** | 100% reliability là impossible và expensive, accept a small failure rate |
| **Blameless Postmortems** | Focus vào hệ thống, không đổ lỗi cá nhân |
| **Toil Elimination** | Automate repetitive work |

---

## 🎬 Câu chuyện thực tế

**Scenario:** DevOps team muốn deploy 10 lần/ngày, nhưng mỗi deploy có risk gây outage.

**Cách tiếp cận SRE:**

1. **Đặt SLO:** "99.9% uptime = 43 phút downtime/tháng allowed"
2. **Track Error Budget:** Tháng này đã dùng 20 phút
3. **Quyết định:**
   - Còn budget → Deploy freely
   - Hết budget → STOP. Fix stability trước.

→ Balance giữa velocity và reliability bằng **data**, không phải ý kiến.

---

## 📖 SRE Concepts

**SRE** là discipline của Google để maintain large-scale systems. Core idea: Dùng software engineering để giải quyết operations problems.

### SLI, SLO, SLA - The Reliability Stack

Ba khái niệm này liên quan chặt chẽ với nhau. Hãy hiểu từng cái:

**SLI (Service Level Indicator)** - Đo cái gì?

SLI là con số bạn có thể đo được. Ví dụ:

- 99.8% requests trả về trong < 200ms
- 0.1% error rate

```
SLI (Indicator): What we measure
    ↓
"99.8% of requests served in < 200ms"
```

**SLO (Service Level Objective)** - Mục tiêu là gì?

SLO là target bạn đặt ra cho team. Luôn có một chút buffer so với SLA.

```
SLO (Objective): Our target
    ↓
"We aim for 99.9% availability"
```

**SLA (Service Level Agreement)** - Cam kết với khách hàng

SLA là contract. Vi phạm = phải đền bù (credits, refund).

```
SLA (Agreement): Contract with customers
    ↓
"If < 99.5%, customer gets credits"
```

**Relationship:**

```
SLA (99.5%) ← SLO (99.9%) ← SLI (measured: 99.8%)
   ↑              ↑              ↑
Contract      Target         Actual
```

> 💡 **Tip:** SLO > SLA để có buffer. Nếu SLO = SLA, bạn sẽ vi phạm SLA rất thường xuyên.

### Error Budget - "Ngân sách" để thất bại

**Ý tưởng:** Nếu SLO là 99.9%, bạn có 0.1% "budget" để fail. Đây là balance giữa reliability và velocity.

```
SLO: 99.9% uptime
    = 0.1% allowed downtime
    = 43 minutes/month (trong 30 ngày)

Error Budget used: 30 minutes
Error Budget remaining: 13 minutes

If budget exhausted → STOP deployments, fix stability first!
```

**Cách sử dụng Error Budget:**

| Budget Status | Action |
|---------------|--------|
| > 50% remaining | Deploy freely, take risks |
| 25-50% remaining | Deploy carefully, more testing |
| < 25% remaining | Only critical fixes |
| Exhausted | Freeze deployments, focus stability |

---

## 🔧 SRE Practices

### 1. Toil Elimination

**Toil** = Công việc manual, repetitive, có thể automate. SRE target: < 50% time cho toil.

```
❌ Toil - Cần eliminate:
• Manually restarting services khi fail
• SSH vào server để check disk space
• Copy-paste deployments

✅ Automated - Đây mới là engineering:
• Auto-restart on failure (K8s, systemd)
• Automated monitoring và alerting
• CI/CD pipelines cho mọi deployment
```

**Đo lường Toil:** Track time spent on manual operations. Nếu > 50%, bạn cần automate nhiều hơn.

### 2. Incident Response

Khi có sự cố, follow process này để response hiệu quả:

```
1. Detect  → Alert fires (automatic)
2. Triage  → Assess severity (P1? P2?)
3. Mitigate → Stop the bleeding (scale, rollback)
4. Fix     → Root cause (permanent fix)
5. Postmortem → Learn (prevent recurrence)
```

**Severity Levels:**

| Level | Impact | Response Time | Example |
|-------|--------|---------------|---------|
| P1 | Service down | 5 min | Homepage không load |
| P2 | Major feature broken | 30 min | Checkout fails 50% |
| P3 | Minor feature broken | 4 hours | Search slower |
| P4 | Cosmetic/minor | 2 days | Typo in UI |

### 3. Blameless Postmortems

**Mục đích:** Học từ failures, KHÔNG phải đổ lỗi. Nếu blame, người sẽ che giấu lỗi.

```markdown
# Postmortem: Database Outage 2024-01-15

## Summary
- Duration: 45 minutes (10:00 - 10:45)
- Impact: 10% of users affected
- Severity: P2

## Timeline
- 10:00 - Alert: High error rate on API
- 10:05 - On-call acknowledges, starts investigation
- 10:15 - Root cause identified: DB connection pool exhausted
- 10:30 - Mitigation: Increase pool size, restart pods
- 10:45 - Service fully restored

## Root Cause
Database connection pool exhausted do traffic spike
(Pool size: 50, cần ít nhất 200)

## What went well
- Alert fired immediately
- On-call response trong 5 phút
- Clear runbook helped

## What went wrong
- Pool size chưa được tune cho load
- Missing alert cho pool utilization

## Action Items
- [ ] Increase connection pool size to 500 (Owner: @devops)
- [ ] Add alerting for pool utilization > 80% (Owner: @sre)
- [ ] Update runbook với section về DB connections (Owner: @lead)
```

**Key elements:**

- **Timeline**: Facts, không opinions
- **Root Cause**: Technical analysis
- **Action Items**: Concrete, có owner, có deadline

---

## 📊 SRE Metrics

### Four Golden Signals

1. **Latency**: Request duration
2. **Traffic**: Requests per second
3. **Errors**: Failed requests
4. **Saturation**: Resource usage

---

## 📝 Tổng kết

✅ SLI, SLO, SLA  
✅ Error budgets  
✅ Toil elimination  
✅ Incident response  

👉 **[LABS.md](LABS.md)** | **[SCENARIOS.md](SCENARIOS.md)**
