# 🚨 MODULE 07: SCENARIOS - Incident Management & Culture

## Scenario 1: Blame Culture Toxic

### 🚨 Bối cảnh

Production outage 2 giờ. Trong post-mortem meeting:

**Manager:** "Ai đã deploy lần cuối?"  
**Team:** "Anh Nam deploy sáng nay."  
**Manager:** "Tại sao anh không test kỹ? Anh làm mất $50,000 revenue!"  
**Nam:** (im lặng, cảm thấy tội lỗi)

Tuần sau, developer sợ deploy, giữ code trong branch 2 tuần.

### 🕵️ Điều tra

**Nguyên nhân gốc rễ của văn hóa độc hại:**

- Lãnh đạo đổ lỗi cho cá nhân, không phải hệ thống
- Không có sự an toàn tâm lý
- Văn hóa sợ hãi → Deploy chậm → Bugs tích tụ nhiều hơn

### 💡 Giải pháp

**1. Thiết lập Văn hóa Không Đổ lỗi:**

Hướng dẫn Post-mortem:

```markdown
# Quy tắc Post-Mortem Không Đổ lỗi

1. ❌ KHÔNG BAO GIỜ hỏi "Ai đã làm chuyện này?"
2. ✅ HỎI "Điều gì trong HỆ THỐNG cho phép chuyện này xảy ra?"
3. ❌ KHÔNG trừng phạt vì sai lầm
4. ✅ KHEN THƯỞNG sự minh bạch và học hỏi

Cụm từ không được phép:
- "Tại sao anh không..."
- "Anh đáng lẽ phải..."
- "Đây là lỗi của anh"

Cụm từ khuyến khích:
- "Chúng ta có thể cải thiện quy trình như thế nào?"
- "Làm sao để ngăn chặn có hệ thống?"
- "Chúng ta học được gì?"
```

**2. Tập trung vào Cải thiện Hệ thống:**

Thay vì:
> "Nam test không kỹ"

Nói:
> "CI pipeline của chúng ta không bắt được loại bug này. Chúng ta cần integration tests."

**3. Tôn vinh Thất bại:**

```markdown
# Giải thưởng "Học từ Thất bại" hàng tháng

Tiêu chí:
- Engineer tìm ra bug khó nhất
- Team có post-mortem tốt nhất
- Cá nhân ngăn chặn incident trong tương lai

Giải thưởng: $500 Amazon gift card + Công nhận
```

**4. Review Sự cố Không Đổ lỗi:**

```yaml
Câu hỏi Review:
  - Vấn đề hệ thống nào đã góp phần?
  - Thiếu sót gì trong công cụ/quy trình?
  - Chúng ta có thể tự động hóa gì?
  - Làm sao ngăn chặn tái diễn?

KHÔNG HỎI:
  - Ai đã làm sai?
  - Tại sao họ không biết?
```

### 🧠 Bài học

- **Đổ lỗi cá nhân = Văn hóa sợ hãi = Deploy chậm hơn**
- **Đổ lỗi hệ thống = Văn hóa học hỏi = Cải thiện nhanh hơn**
- **An toàn tâm lý kích thích đổi mới**
- **Engineer không dám mạo hiểm nếu bị phạt vì thất bại**

---

## Scenario 2: Superficial Post-Mortems, Issues Repeat

### 🚨 Bối cảnh

3 tháng liên tiếp, Redis OOM crash:

- **Tháng 1**: Post-mortem → "Increase Redis memory" → Done
- **Tháng 2**: Crash lại → "Increase more memory" → Done  
- **Tháng 3**: Crash lại → Team frustrated

### 🕵️ Điều tra

Post-mortem không đào sâu root cause:

❌ **Phân tích nông cạn:**
> "Redis crashed vì hết bộ nhớ"

✅ **Phân tích 5 Tại sao:**
>
> 1. Tại sao Redis hết bộ nhớ? → Rò rỉ bộ nhớ
> 2. Tại sao rò rỉ? → App không đóng connections
> 3. Tại sao không đóng? → Developer không biết best practice
> 4. Tại sao không biết? → Không có code review
> 5. Tại sao không review? → Team quá bận

**Nguyên nhân gốc rễ thực sự:** Thiếu quy trình code review

### 💡 Giải pháp

**1. Sử dụng Kỹ thuật 5 Tại sao:**

```markdown
# 5 Whys Example

Problem: Counter App crashed

Why 1: Why did app crash?
→ Redis connection failed

Why 2: Why did Redis fail?
→ Too many open connections (max 10,000 exceeded)

Why 3: Why too many connections?
→ App opens new connection per request, never closes

Why 4: Why not closing connections?
→ Developer used wrong Redis client pattern

Why 5: Why wrong pattern?
→ No code review caught it + Lack of documentation

ROOT CAUSE: Missing code review + Insufficient docs
```

**2. Triển khai Hành động Khắc phục và Phòng ngừa:**

```markdown
# Action Items Template

## Immediate (Stop bleeding)
- [ ] Restart Redis (mitigation)
- [ ] Add connection limit

## Short-term (Fix root cause)
- [ ] Refactor code to use connection pooling
- [ ] Add unit test for connection handling

## Long-term (Prevent class of issues)
- [ ] Mandatory code review policy
- [ ] Create Redis best practices doc
- [ ] Add linter rule to detect connection leaks
- [ ] Training session on Redis patterns
```

**3. Theo dõi Các Hành động:**

```python
# action_tracker.py
class ActionItem:
    def __init__(self, description, owner, deadline, priority):
        self.description = description
        self.owner = owner
        self.deadline = deadline
        self.priority = priority  # P0, P1, P2
        self.status = "TODO"  # TODO, IN_PROGRESS, DONE
    
    def is_overdue(self):
        return datetime.now() > self.deadline and self.status != "DONE"

# Weekly review: Any overdue P0/P1 items?
```

**4. Post-Mortem Theo dõi (1 tháng sau):**

```markdown
# Follow-up Review

Original Incident: Redis OOM (2024-01-15)

Actions Completed:
✅ Code review policy enforced
✅ Redis best practices documented
✅ Linter added

Actions Pending:
⚠️ Training session (delayed to Feb)

Has issue repeated?
✅ NO - No Redis OOM in 30 days

Conclusion: Root cause addressed successfully
```

### 🧠 Bài học

- **Phân tích nông cạn → Vấn đề tái diễn**
- **5 Tại sao đào sâu đến nguyên nhân gốc**
- **Theo dõi hành động, không chỉ viết**
- **Review theo dõi xác nhận hiệu quả**

---

## Scenario 3: Chaotic Incident Response (No Runbook)

### 🚨 Bối cảnh

2am, production down. 3 engineers paged:

**Engineer 1:** "Ai biết password Redis?"  
**Engineer 2:** "Thử `admin123`?"  
**Engineer 3:** "Không được. Tôi tìm trong Slack..."  
*30 phút lãng phí tìm credentials*

**Engineer 1:** "OK có password rồi. Restart Redis?"  
**Engineer 2:** "Chờ đã, backup chưa?"  
**Engineer 1:** "Ơ...backup thế nào?"

→ 2 giờ mới khôi phục vì không có runbook

### 🕵️ Điều tra

**Vấn đề:**

- Không có quy trình được ghi chép
- Kiến thức bộ lạc (chỉ 1-2 người biết)
- Không có checklist → Bỏ sót bước quan trọng

### 💡 Giải pháp

**1. Tạo Runbook cho Sự cố Thường gặp:**

```markdown
# Runbook: Redis Down

## Symptoms
- App returns 500 errors
- Logs: "Redis connection failed"
- Alert: "Redis service unhealthy"

## Severity
P1 (High) - Core functionality affected

## Yêu cầu
- Truy cập production K8s cluster
- Thông tin xác thực Redis (LastPass: "Production/Redis")

## Các Bước Điều tra

### 1. Kiểm tra Trạng thái Redis Pod
```bash
kubectl get pods -n production | grep redis
# Expected: Running
```

### 2. Kiểm tra Logs Redis

```bash
kubectl logs redis-0 -n production --tail=100
# Look for: OOM, crash, errors
```

### 3. Kiểm tra Dung lượng Disk

```bash
kubectl exec redis-0 -n production -- df -h /data
# Alert if > 90% full
```

## Các Bước Giảm thiểu

### Tùy chọn A: Khởi động lại Redis (nếu crashed)

```bash
kubectl delete pod redis-0 -n production
# StatefulSet will recreate
# Wait 30s
kubectl get pods -n production | grep redis
# Verify: Running
```

### Tùy chọn B: Xóa Logs (nếu disk đầy)

```bash
kubectl exec redis-0 -- find /var/log -name "*.log" -mtime +7 -delete
```

## Xác minh

```bash
# Test Redis
kubectl exec redis-0 -- redis-cli ping
# Expected: PONG

# Test App
curl https://counter-app.com/health
# Expected: {"status": "healthy"}
```

## Rollback (nếu giảm thiểu thất bại)

```bash
# Khôi phục từ backup
kubectl apply -f backups/redis-backup-2024-01-14.yaml
```

## Sau Sự cố

- [ ] Cập nhật timeline sự cố
- [ ] Lên lịch post-mortem
- [ ] Giám sát thêm 1 giờ

```

**2. Runbook Library:**

```

runbooks/
├── redis-down.md
├── high-latency.md
├── database-full.md
├── deployment-failed.md
├── ssl-certificate-expired.md
└── ddos-attack.md

```

**3. Incident Commander Role:**

```markdown
# Incident Commander Checklist

## During Incident
- [ ] Declare incident severity
- [ ] Create #incident-YYYYMMDD channel
- [ ] Assign roles:
  - Investigator: Debug root cause
  - Communicator: Update stakeholders
  - Scribe: Document timeline
- [ ] Follow relevant runbook
- [ ] Coordinate actions
- [ ] Approve risky changes

## After Resolution
- [ ] Post all-clear message
- [ ] Archive incident channel
- [ ] Schedule post-mortem (within 48h)
```

**4. Thực hành Diễn tập:**

```markdown
# Monthly Incident Drill

Scenario: Simulate Redis crash
Steps:
1. Kill Redis pod (in staging)
2. Page on-call engineer
3. Follow runbook
4. Measure MTTR

Goal: MTTR < 15 minutes

Debrief:
- What went well?
- What slowed us down?
- Update runbook
```

### 🧠 Bài học

- **Không có runbook = Hỗn loạn + Phục hồi chậm**
- **Runbook giúp junior engineer xử lý được**
- **Diễn tập thực hành xác thực runbook**
- **Incident Commander cung cấp sự phối hợp**

---

## Scenario 4: Unrealistic SLA (100% Uptime)

### 🚨 Bối cảnh

CEO to CTO:

**CEO:** "Competitor has 99.99% uptime. We need 100%!"  
**CTO:** "100% is impossible. We'd need to—"  
**CEO:** "I don't care. Customers expect it. Make it happen."

Engineering team burned out trying to achieve impossible goal.

### 🕵️ Điều tra

**Math of Uptime:**

| SLA | Downtime/Year | Downtime/Month | Realistic? |
|-----|---------------|----------------|------------|
| 90% | 36.5 days | 3 days | ❌ Terrible |
| 99% | 3.65 days | 7.2 hours | ⚠️ OK for non-critical |
| 99.9% | 8.76 hours | 43.2 minutes | ✅ Good |
| 99.99% | 52.6 minutes | 4.3 minutes | ⚠️ Expensive |
| 100% | 0 seconds | 0 seconds | ❌ **IMPOSSIBLE** |

**Tại sao 100% là không thể:**

- Phần cứng hỏng
- Phần mềm có bugs
- Vấn đề mạng
- Lỗi con người
- Thiên tai

Ngay cả AWS, Google, Facebook cũng có outage!

### 💡 Giải pháp

**1. Giáo dục Stakeholders:**

```markdown
# SLA Education for Executives

## The Cost of "Nines"

Each additional "9" increases cost exponentially:

99% → 99.9%: 2x cost (redundancy, monitoring)
99.9% → 99.99%: 5x cost (multi-region, 24/7 on-call)
99.99% → 99.999%: 10x cost (chaos engineering, dedicated SRE team)

## What does downtime mean?

99.9% = 43 minutes/month
- Scheduled maintenance: 30 min
- Unplanned incidents: 13 min

99.99% = 4 minutes/month
- MUST automate everything
- Cannot do manual deployment
- Multi-region active-active

## Recommendation

For Counter App (non-life-critical):
- Target: 99.9% (industry standard)
- Cost: $5K/month
- Budget for 99.99%: $25K/month
- Budget for 99.999%: $100K/month

ROI Analysis:
- Extra revenue from 99.99% vs 99.9%: $2K/month
- Extra cost: $20K/month
- ROI: -90% ❌

Conclusion: 99.9% is optimal
```

**2. Triển khai Ngân sách Lỗi:**

```python
# error_budget.py

class SLO:
    def __init__(self, target_percentage):
        self.target = target_percentage
        self.error_budget = 100 - target_percentage
    
    def downtime_allowed_per_month(self):
        """Minutes of downtime allowed per month"""
        minutes_per_month = 30 * 24 * 60  # 43,200
        return minutes_per_month * (self.error_budget / 100)
    
    def budget_remaining(self, downtime_this_month):
        """How much error budget remains?"""
        allowed = self.downtime_allowed_per_month()
        remaining = allowed - downtime_this_month
        return remaining

# Example
slo = SLO(target_percentage=99.9)
print(f"Downtime allowed: {slo.downtime_allowed_per_month():.1f} min/month")

# This month: 30 minutes downtime
remaining = slo.budget_remaining(downtime_this_month=30)
print(f"Remaining budget: {remaining:.1f} minutes")

if remaining < 0:
    print("⚠️ EXCEEDED ERROR BUDGET! Freeze feature deployments, focus on reliability.")
else:
    print(f"✅ {remaining:.1f} minutes left. Can take calculated risks.")
```

**3. Bảng điều khiển SLO:**

```markdown
# Monthly SLO Report (January 2024)

## Target: 99.9% uptime

### Actual Performance
- Uptime: 99.87%
- Downtime: 56 minutes
- Error Budget: 43 minutes
- **Status: ⚠️ EXCEEDED by 13 minutes**

### Incidents
| Date | Duration | Impact | Root Cause |
|------|----------|--------|------------|
| Jan 5 | 20 min | 100% users | Redis OOM |
| Jan 15 | 30 min | 100% users | Disk full |
| Jan 22 | 6 min | 50% users | Network blip |

### Action Plan (February)
- ✅ Fix Redis memory leak → Prevent 20 min class of outage
- ✅ Add disk monitoring → Prevent 30 min class
- ❌ Network issues (external) → Cannot prevent

### Forecast February
- Estimated uptime: 99.92%
- Within SLO: ✅ YES
```

**4. Chính sách Đóng băng Tính năng:**

```yaml
# Policy: Error Budget Exceeded

IF error_budget < 0 THEN:
  - FREEZE all feature deployments
  - ONLY bug fixes and reliability improvements allowed
  - Daily reliability reviews
  - Post-mortem all incidents

IF error_budget restored THEN:
  - Resume feature development
  - Lessons learned documentation
```

### 🧠 Bài học

- **100% uptime là huyền thoại**
- **Mỗi "số 9" tốn chi phí tăng theo cấp số nhân**
- **Ngân sách lỗi cân bằng đổi mới vs ổn định**
- **SLO phải phù hợp với mức độ quan trọng nghiệp vụ**
- **Giáo dục stakeholders về mục tiêu thực tế**

---

## Scenario 5: Team Morale Low After Repeated Incidents

### 🚨 Bối cảnh

Past 3 months:

- 12 production incidents
- On-call paged every week
- Weekends interrupted
- No time to fix root causes (always firefighting)

**Team sentiment:**

- "I'm exhausted"
- "Feels like we're failing"
- "Thinking about quitting"

### 🕵️ Điều tra

**Vòng luẩn quẩn:**

```text
Sự cố → Dập lửa → Không có thời gian sửa → Nhiều sự cố hơn → Kiệt sức
```

**Nguyên nhân gốc:**

- Nợ kỹ thuật tích tụ
- Không có thời gian dành cho công việc reliability
- Phản ứng thụ động, không chủ động
- Thiếu sự công nhận

### 💡 Giải pháp

**1. Phân bổ Sprint Reliability:**

```markdown
# Sprint Planning Policy

Every 4th sprint = "Reliability Sprint"

Goals:
- Fix top 3 recurring issues
- Improve monitoring
- Update runbooks
- Pay down technical debt

NO new features during reliability sprint.
```

**2. Ngân sách Công việc Vặt (Toil):**

```text
Quy tắc Google SRE: Engineers dành tối đa 50% thời gian cho toil

Toil = Công việc lặp đi lặp lại, thủ công, có thể tự động hóa

Phân bổ mục tiêu:
- 50% Kỹ thuật (tự động hóa, cải thiện)
- 50% Toil (xử lý sự cố, vận hành thủ công)

NẾU toil > 50%:
  → Thuê thêm người HOẶC giảm dịch vụ HOẶC tự động hóa
```

**3. Tôn vinh Thành công:**

```markdown
# Weekly Wins Ritual (Every Friday)

Share in #team-wins Slack channel:

This week we:
✅ Reduced latency by 40%
✅ Zero incidents for 7 days straight!
✅ Automated deployment process (saved 2 hours/week)
✅ Nam completed Kubernetes certification

Recognition:
- Public shout-out
- Bonus points for quarterly review
- "Engineer of the Month" award
```

**4. Sửa Vấn đề Ảnh hưởng Cao trước:**

```python
# prioritize_fixes.py

issues = [
    {"name": "Redis OOM", "frequency": 4, "impact": 100},  # 4x/month, 100% users
    {"name": "Slow query", "frequency": 20, "impact": 5},  # 20x/month, 5% users
    {"name": "Cert expiry", "frequency": 0.1, "impact": 100},  # 1x/year, 100% users
]

for issue in issues:
    issue["priority"] = issue["frequency"] * issue["impact"]

# Sort by priority
sorted_issues = sorted(issues, key=lambda x: x["priority"], reverse=True)

print("Fix in this order:")
for i, issue in enumerate(sorted_issues, 1):
    print(f"{i}. {issue['name']} (Priority: {issue['priority']})")

# Output:
# 1. Redis OOM (Priority: 400)
# 2. Slow query (Priority: 100)
# 3. Cert expiry (Priority: 10)
```

**5. Retrospective Sự cố (Sức khỏe Team):**

```markdown
# Quarterly Team Health Check

Anonymous survey:
1. Burnout level (1-10)?
2. Toil percentage?
3. Biggest pain point?
4. What would improve morale?

Results (Q1 2024):
- Avg burnout: 7/10 ⚠️
- Avg toil: 65% (target: 50%) ❌
- Top pain: "Same issues repeating"
- Morale boost: "Time to fix root causes"

Actions:
- Next sprint = Reliability sprint
- Hire 1 more SRE
- Target toil: 50% by Q2
```

**6. Hỗ trợ Sức khỏe Tinh thần:**

```markdown
# On-Call Wellness Program

- Max 1 week on-call per month
- +1 day PTO after incident-heavy week
- Therapy/counseling covered
- "No-meetings Thursday" for deep work
- Flexible hours after night pages
```

**7. Tự động hóa Công việc Vặt:**

```bash
# Examples of automation

# Before: Manual log cleanup (30 min/day)
# After: Cron job (0 min/day)
0 2 * * * find /var/log -mtime +7 -delete

# Before: Manual deployment (1 hour)
# After: GitHub Actions (5 min, automated)

# Before: Manual certificate renewal (2 hours/year)
# After: cert-manager (automatic)
```

### 🧠 Bài học

- **Dập lửa → Kiệt sức → Nghỉ việc**
- **Phân bổ thời gian cho công việc phòng ngừa**
- **Ngân sách toil ngăn kiệt sức**
- **Tôn vinh thành công, không chỉ sửa thất bại**
- **Tinh thần cao = Giữ chân người = Reliability tốt hơn**

---

## 🎯 Tổng kết Module 07

| Scenario | Vấn đề | Giải pháp |
|----------|--------|-----------|
| 1 | Blame culture | Blameless post-mortems |
| 2 | Superficial analysis | 5 Whys + Action tracking |
| 3 | Chaotic response | Runbooks + Drills |
| 4 | Unrealistic SLA | Error budgets + Stakeholder education |
| 5 | Team burnout | Toil reduction + Reliability sprints |

---

## ✅ HOÀN THÀNH KHÓA HỌC

🎉 **Congratulations!** Bạn đã hoàn thành toàn bộ **DevOps Zero to Hero**!

### Bạn đã học được

- ✅ 7 giai đoạn Vòng đời DevOps
- ✅ 35 tình huống thực chiến
- ✅ Thực hành tốt nhất từ ngành
- ✅ Công cụ: Git, Docker, K8s, Terraform, Prometheus, và nhiều hơn nữa

### Bước tiếp theo

1. **Xây dựng portfolio**: Deploy Counter App lên cloud công khai
2. **Đóng góp open source**: Tìm dự án DevOps trên GitHub
3. **Lấy chứng chỉ**: CKA, AWS DevOps, Terraform Associate
4. **Mở rộng mạng lưới**: Tham gia cộng đồng DevOps (Slack, Discord, Reddit)
5. **Tiếp tục học**: Công nghệ thay đổi, bạn cũng phải thay đổi!

---

**"DevOps is not a destination, it's a journey."**

Chúc may mắn trên con đường sự nghiệp DevOps của bạn! 🚀

```
