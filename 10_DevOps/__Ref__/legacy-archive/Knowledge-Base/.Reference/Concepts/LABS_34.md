# 🧪 MODULE 07: LABS - ChatOps & Post-Mortem

## LAB 1: Thiết lập Slack Bot cho Triển khai

### Yêu cầu

- Slack workspace
- Slack App đã tạo (<https://api.slack.com/apps>)

### Tạo Slack Bot

1. **Create App** → From scratch → Name: "DevOps Bot"
2. **OAuth & Permissions** → Add scopes:
   - `chat:write`
   - `channels:read`
3. **Install App** → Copy OAuth Token

### Script Python Thông báo

```python
# slack_notify.py
import requests
import os

SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK_URL')

def notify_deployment(app_name, version, status):
    message = {
        "text": f"🚀 Deployment Alert",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Deployment: {app_name}*\nVersion: `{version}`\nStatus: {'✅ Success' if status == 'success' else '❌ Failed'}"
                }
            }
        ]
    }
    
    requests.post(SLACK_WEBHOOK, json=message)

# Usage
notify_deployment("counter-app", "v2.0", "success")
```

### Tích hợp với GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy and Notify

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy
        run: kubectl apply -f k8s/
      
      - name: Notify Slack
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
        run: |
          python slack_notify.py
```

---

## LAB 2: Quy trình Quản lý Sự cố

### Sổ tay Xử lý Sự cố

```markdown
# Incident Response Runbook

## 1. Detection (0-5 min)
- [ ] Alert fires (PagerDuty/Slack)
- [ ] Acknowledge alert
- [ ] Check dashboard: http://grafana.company.com

## 2. Triage (5-15 min)
- [ ] Assess severity (P0/P1/P2)
- [ ] Create incident channel: #incident-YYYYMMDD-HHMM
- [ ] Post initial status update

## 3. Investigation (15-60 min)
- [ ] Check logs: `kubectl logs <pod>`
- [ ] Check metrics: CPU, Memory, Error rate
- [ ] Identify root cause

## 4. Mitigation (variable)
- [ ] Apply temporary fix
- [ ] Verify service restored
- [ ] Update stakeholders

## 5. Resolution
- [ ] Apply permanent fix
- [ ] Close incident channel
- [ ] Schedule post-mortem
```

### Thực hành Diễn tập

```bash
# Simulate incident
# 1. Kill Redis pod
kubectl delete pod redis-0

# 2. Monitor alerts
# 3. Follow runbook
# 4. Restore service

# Expected time: <15 minutes
```

---

## LAB 3: Viết Post-Mortem

### Template: `docs/post-mortem-template.md`

```markdown
# Post-Mortem: [Incident Title]

**Date**: YYYY-MM-DD  
**Author**: [Your Name]  
**Reviewers**: [Team Members]

## Executive Summary
[2-3 sentences: What broke? How long? Impact?]

## Incident Details
- **Start Time**: 
- **End Time**: 
- **Duration**: 
- **Severity**: P0/P1/P2
- **Impact**: 
  - Users affected: 
  - Revenue loss: 
  - SLO burned: 

## Timeline
| Time | Event |
|------|-------|
| 14:30 | Alert fired |
| 14:35 | Engineer paged |
| ... | ... |

## Root Cause
[5W1H: What, When, Where, Who, Why, How]

## Phát hiện
Phát hiện sự cố như thế nào?
- [ ] Cảnh báo monitoring
- [ ] Báo cáo từ người dùng
- [ ] Phát hiện thủ công

## Impact
- Users: 
- Revenue: 
- Reputation: 

## Giải quyết
Đã sửa bằng cách nào?

## Yếu tố Góp phần
Điều gì làm tệ hơn?
- Monitoring không đủ
- Thiếu auto-scaling
- ...

## Bài học Rút ra

### Điều gì Tốt
- ✅
- ✅

### Điều gì Sai
- ❌
- ❌

## Hành động Cần làm
| Hành động | Người phụ trách | Hạn chót | Trạng thái |
|-----------|-----------------|----------|------------|
| Thêm monitoring | Nam | 2024-01-20 | TODO |

## Phụ lục
- Logs
- Screenshots
- Chat transcripts
```

### Viết Post-Mortem Đầu tiên

**Bài tập**: Viết post-mortem cho một sự cố giả định:

- Counter App down trong 30 phút
- Nguyên nhân: Redis OOM (Out of Memory)
- Sử dụng template ở trên

---

## LAB 4: Theo dõi DORA Metrics

### Thiết lập Thu thập Metrics

```python
# dora_metrics.py
import json
from datetime import datetime, timedelta

class DORAMetrics:
    def __init__(self):
        self.deployments = []
        self.incidents = []
    
    def log_deployment(self, version, status):
        """Track deployment"""
        self.deployments.append({
            "timestamp": datetime.now(),
            "version": version,
            "status": status  # success or failed
        })
    
    def log_incident(self, start_time, end_time):
        """Track incident"""
        self.incidents.append({
            "start": start_time,
            "end": end_time,
            "duration": (end_time - start_time).total_seconds()
        })
    
    def deployment_frequency(self, days=7):
        """Deployments per day"""
        recent = [d for d in self.deployments 
                  if d["timestamp"] > datetime.now() - timedelta(days=days)]
        return len(recent) / days
    
    def change_failure_rate(self):
        """% of failed deployments"""
        if not self.deployments:
            return 0
        failed = sum(1 for d in self.deployments if d["status"] == "failed")
        return (failed / len(self.deployments)) * 100
    
    def mttr(self):
        """Mean Time To Recovery (seconds)"""
        if not self.incidents:
            return 0
        return sum(i["duration"] for i in self.incidents) / len(self.incidents)
    
    def report(self):
        """Generate DORA report"""
        return {
            "deployment_frequency": f"{self.deployment_frequency():.2f}/day",
            "change_failure_rate": f"{self.change_failure_rate():.1f}%",
            "mttr": f"{self.mttr()/60:.1f} minutes"
        }

# Example usage
metrics = DORAMetrics()

# Log deployments
metrics.log_deployment("v1.0", "success")
metrics.log_deployment("v1.1", "success")
metrics.log_deployment("v1.2", "failed")
metrics.log_deployment("v1.3", "success")

# Log incidents
metrics.log_incident(
    datetime(2024, 1, 15, 14, 30),
    datetime(2024, 1, 15, 16, 45)
)

print(json.dumps(metrics.report(), indent=2))
```

**Kết quả mong đợi:**

```json
{
  "deployment_frequency": "0.57/day",
  "change_failure_rate": "25.0%",
  "mttr": "135.0 minutes"
}
```

---

## ✅ Checklist Module 07

- [ ] Thông báo Slack bot hoạt động
- [ ] Runbook sự cố đã tạo và test
- [ ] Post-mortem đã viết (thật hoặc mô phỏng)
- [ ] DORA metrics đã theo dõi

---

## 🎉 Chúc mừng hoàn thành khóa học

Bạn đã đi qua cả 7 giai đoạn DevOps:

1. ✅ PLAN - Chiến lược & Hợp tác
2. ✅ BUILD - Git & Docker
3. ✅ CI - Kiểm thử Tự động
4. ✅ CD - Triển khai Kubernetes
5. ✅ OPERATE - Infrastructure as Code
6. ✅ MONITOR - Quan sát Hệ thống
7. ✅ FEEDBACK - Cải tiến Liên tục

**Bước tiếp theo:**

- Áp dụng vào dự án thực tế
- Tham gia cộng đồng DevOps
- Tiếp tục học hỏi!

🚀 **Bạn giờ đã là DevOps Engineer!**
