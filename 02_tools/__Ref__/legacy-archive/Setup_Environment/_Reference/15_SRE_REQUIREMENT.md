# Module 15: SITE RELIABILITY ENGINEERING (SRE)

> **"SRE là đội cứu hỏa + đội phòng cháy - vừa dập lửa, vừa ngăn lửa xảy ra"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu SRE principles
- ✅ SLOs, SLIs, SLAs và Error Budgets
- ✅ Incident management
- ✅ On-call practices
- ✅ Post-mortem (Blameless)
- ✅ Chaos Engineering basics
- ✅ Toil reduction
- ✅ Capacity planning

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| SRE | Site Reliability Engineering | Kỹ thuật độ tin cậy |
| SLO | Service Level Objective | Mục tiêu mức dịch vụ |
| SLI | Service Level Indicator | Chỉ số đo SLO |
| SLA | Service Level Agreement | Thỏa thuận mức dịch vụ |
| Error Budget | Error Budget | Ngân sách lỗi cho phép |
| Reliability | Reliability | Độ tin cậy |
| Availability | Availability | Độ khả dụng |
| Latency | Latency | Độ trễ |
| Throughput | Throughput | Thông lượng |
| Incident | Incident | Sự cố |
| Severity | Severity | Mức độ nghiêm trọng |
| On-call | On-call | Trực ca |
| Escalation | Escalation | Leo thang xử lý |
| Runbook | Runbook | Hướng dẫn xử lý sự cố |
| Post-mortem | Post-mortem | Họp rút kinh nghiệm |
| Blameless | Blameless | Không đổ lỗi |
| RCA | Root Cause Analysis | Phân tích nguyên nhân gốc |
| MTTR | Mean Time To Recovery | Thời gian phục hồi TB |
| MTBF | Mean Time Between Failures | Thời gian giữa các lỗi |
| Toil | Toil | Công việc lặp đi lặp lại thủ công |
| Chaos Engineering | Chaos Engineering | Kỹ thuật gây lỗi có chủ đích |
| DORA | DORA Metrics | 4 metrics từ Google |

---

## ✅ Checklist Labs

### Labs SRE Concepts

- [ ] Lab 1: SRE vs DevOps vs SysAdmin
- [ ] Lab 2: SRE principles
- [ ] Lab 3: Google SRE book overview
- [ ] Lab 4: Reliability engineering mindset

### Labs SLOs, SLIs, Error Budgets

- [ ] Lab 5: Define SLI cho web service
- [ ] Lab 6: Calculate availability SLI
- [ ] Lab 7: Latency SLI (p50, p90, p99)
- [ ] Lab 8: Error rate SLI
- [ ] Lab 9: Define SLO từ SLI
- [ ] Lab 10: Error budget calculation
- [ ] Lab 11: Error budget policy
- [ ] Lab 12: SLO documentation
- [ ] Lab 13: SLO dashboard
- [ ] Lab 14: Alert on SLO breach
- [ ] Lab 15: Burn rate alerts

### Labs Incident Management

- [ ] Lab 16: Incident severity levels
- [ ] Lab 17: Incident response process
- [ ] Lab 18: Incident Commander role
- [ ] Lab 19: Communication durante incident
- [ ] Lab 20: Status page setup
- [ ] Lab 21: Incident timeline documentation
- [ ] Lab 22: Incident declaration
- [ ] Lab 23: Escalation matrix
- [ ] Lab 24: War room practices

### Labs On-call

- [ ] Lab 25: On-call rotation schedule
- [ ] Lab 26: On-call expectations
- [ ] Lab 27: Alert routing to on-call
- [ ] Lab 28: PagerDuty/Opsgenie setup
- [ ] Lab 29: On-call handoff
- [ ] Lab 30: On-call compensation concepts
- [ ] Lab 31: Reducing on-call burden

### Labs Runbooks

- [ ] Lab 32: Runbook template
- [ ] Lab 33: Create runbook cho common incidents
- [ ] Lab 34: Runbook automation
- [ ] Lab 35: Runbook testing
- [ ] Lab 36: Runbook maintenance

### Labs Post-mortem

- [ ] Lab 37: Blameless post-mortem principles
- [ ] Lab 38: Post-mortem template
- [ ] Lab 39: Timeline reconstruction
- [ ] Lab 40: 5 Whys technique
- [ ] Lab 41: Root cause identification
- [ ] Lab 42: Action items definition
- [ ] Lab 43: Post-mortem meeting facilitation
- [ ] Lab 44: Post-mortem review và follow-up
- [ ] Lab 45: Post-mortem database/library

### Labs Toil Reduction

- [ ] Lab 46: Identify toil trong workflow
- [ ] Lab 47: Measure toil percentage
- [ ] Lab 48: Toil budget
- [ ] Lab 49: Automation priorities
- [ ] Lab 50: Self-healing systems concepts
- [ ] Lab 51: Auto-remediation

### Labs Chaos Engineering

- [ ] Lab 52: Chaos engineering principles
- [ ] Lab 53: Chaos Monkey concepts
- [ ] Lab 54: Litmus Chaos installation
- [ ] Lab 55: Pod kill experiment
- [ ] Lab 56: Network latency experiment
- [ ] Lab 57: CPU stress experiment
- [ ] Lab 58: Gameday planning
- [ ] Lab 59: Controlled chaos in production

### Labs DORA Metrics

- [ ] Lab 60: Deployment Frequency
- [ ] Lab 61: Lead Time for Changes
- [ ] Lab 62: Change Failure Rate
- [ ] Lab 63: Time to Restore Service
- [ ] Lab 64: DORA metrics tracking
- [ ] Lab 65: DORA dashboard

### Labs Capacity Planning

- [ ] Lab 66: Current capacity assessment
- [ ] Lab 67: Growth prediction
- [ ] Lab 68: Load testing for capacity
- [ ] Lab 69: Capacity planning documentation
- [ ] Lab 70: Cost vs capacity tradeoffs

### Labs Counter App SRE

- [ ] Lab 71: Define SLOs cho Counter App
- [ ] Lab 72: Counter App runbook
- [ ] Lab 73: Counter App post-mortem template
- [ ] Lab 74: Chaos experiment Counter App
- [ ] Lab 75: Full SRE practices implementation

---

## 🚨 Checklist Scenarios

### Scenarios về Incidents

- [ ] Scenario 1: Production down, nobody know why
- [ ] Scenario 2: Partial outage, difficult to detect
- [ ] Scenario 3: Cascading failure
- [ ] Scenario 4: Third-party dependency failure
- [ ] Scenario 5: Database corruption
- [ ] Scenario 6: Security incident

### Scenarios về Response

- [ ] Scenario 7: On-call không respond
- [ ] Scenario 8: Escalation needed but unclear who
- [ ] Scenario 9: Too many people on incident call
- [ ] Scenario 10: Communication breakdown
- [ ] Scenario 11: Customer impact unknown
- [ ] Scenario 12: Need to page off-duty expert

### Scenarios về SLOs

- [ ] Scenario 13: Error budget exhausted
- [ ] Scenario 14: Feature vs reliability tradeoff
- [ ] Scenario 15: SLO không realistic
- [ ] Scenario 16: Stakeholder pressure on 100% uptime
- [ ] Scenario 17: SLI measurement incorrect

### Scenarios về Post-mortem

- [ ] Scenario 18: Blame culture in post-mortem
- [ ] Scenario 19: Same incident happens again
- [ ] Scenario 20: Action items không complete
- [ ] Scenario 21: Post-mortem fatigue

### Scenarios về On-call

- [ ] Scenario 22: Alert fatigue
- [ ] Scenario 23: Pager storm
- [ ] Scenario 24: Work-life balance issues
- [ ] Scenario 25: Burnout signs
- [ ] Scenario 26: New person on-call không biết system

### Scenarios về Chaos

- [ ] Scenario 27: Chaos experiment causes real outage
- [ ] Scenario 28: System less resilient than expected
- [ ] Scenario 29: Unknown dependency discovered

### Scenarios về Culture

- [ ] Scenario 30: Resistance to change
- [ ] Scenario 31: Toil always prioritized over projects
- [ ] Scenario 32: Reliability not valued by leadership

---

## ⏱️ Thời lượng

**Ước tính:** 4-6 giờ

| Phần | Thời gian |
|------|-----------|
| SRE concepts (Labs 1-4) | 0.5 giờ |
| SLOs & Error Budgets (Labs 5-15) | 1.5 giờ |
| Incident management (Labs 16-24) | 1 giờ |
| On-call & Runbooks (Labs 25-36) | 1 giờ |
| Post-mortem (Labs 37-45) | 1 giờ |
| Toil & Chaos (Labs 46-59) | 1 giờ |
| DORA & Capacity (Labs 60-75) | 1 giờ |
| Scenarios | 1 giờ |

---

## 🔗 Tài liệu tham khảo

- [Google SRE Book (Free)](https://sre.google/sre-book/table-of-contents/)
- [Google SRE Workbook](https://sre.google/workbook/table-of-contents/)
- [DORA Metrics](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance)
- [Chaos Engineering](https://principlesofchaos.org/)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
