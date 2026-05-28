# 🔬 Labs: System Design & Reliability

---

## 🔬 Lab 1: Design High Availability

Design HA architecture cho web application:

```
Requirements:
- 99.9% uptime (8.76 hours downtime/year)
- Handle 10,000 concurrent users
- Data must be replicated

Architecture:
┌─────────────────────────────────────────┐
│           Route 53 (DNS)                │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│        CloudFront (CDN)                  │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│     Application Load Balancer           │
└────────┬────────────────────┬───────────┘
         │                    │
    ┌────┴────┐          ┌────┴────┐
    │  AZ-a   │          │  AZ-b   │
    │  EC2    │          │  EC2    │
    │  ASG    │          │  ASG    │
    └────┬────┘          └────┬────┘
         │                    │
    ┌────┴────────────────────┴────┐
    │        RDS Multi-AZ          │
    │   Primary ──→ Standby        │
    └──────────────────────────────┘
```

---

## 🔬 Lab 2: Calculate SLAs

```
Service Dependencies:
- Load Balancer: 99.99%
- EC2: 99.99%
- RDS: 99.95%

Combined SLA = 99.99% × 99.99% × 99.95% = 99.93%

Downtime per year:
- 99.9%  = 8.76 hours
- 99.95% = 4.38 hours
- 99.99% = 52.6 minutes
```

---

## 🔬 Lab 3: Disaster Recovery

```
DR Strategies:

1. Backup & Restore (RTO: hours, RPO: 24h)
   - S3 cross-region replication
   - RDS automated backups

2. Pilot Light (RTO: 10min, RPO: minutes)
   - AMIs in DR region
   - RDS read replica

3. Warm Standby (RTO: minutes, RPO: seconds)
   - Scaled-down infrastructure running
   - Route 53 failover
```

---

## 🔬 Lab 4: Capacity Planning

```python
# Calculate required capacity
def calculate_capacity(
    peak_users: int,
    requests_per_user: int,
    response_time_ms: int,
    instance_capacity: int
) -> int:
    total_rps = peak_users * requests_per_user / 60
    instances_needed = total_rps / instance_capacity
    # Add 20% buffer
    return int(instances_needed * 1.2) + 1

# Example
capacity = calculate_capacity(
    peak_users=10000,
    requests_per_user=10,
    response_time_ms=100,
    instance_capacity=500
)
print(f"Need {capacity} instances")
```

---

## 🔬 Lab 5: Chaos Engineering

```yaml
# Chaos Monkey experiment
apiVersion: chaos-mesh.chaos
kind: PodChaos
metadata:
  name: pod-failure
spec:
  action: pod-failure
  mode: one
  selector:
    namespaces:
      - production
    labelSelectors:
      app: api
  duration: "30s"
```

---

## ✅ Checklist

- [ ] Lab 1: HA Design
- [ ] Lab 2: SLA Calculation
- [ ] Lab 3: DR Strategy
- [ ] Lab 4: Capacity Planning
- [ ] Lab 5: Chaos Engineering

---

**[← Back to README](./README.md)**
