# ✅ Solutions: System Design

---

## Exercise 1: Web Application Design

```
Architecture for 100K concurrent users:

┌─────────────────────────────────────────────────┐
│                  CloudFront CDN                  │
└─────────────────────┬───────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────┐
│           Application Load Balancer              │
└────────────────┬──────────────┬─────────────────┘
                 │              │
    Region US-EAST-1      Region EU-WEST-1
    ┌────────────┐        ┌────────────┐
    │ ASG (EC2)  │        │ ASG (EC2)  │
    │ Min:5      │        │ Min:5      │
    │ Max:50     │        │ Max:50     │
    └─────┬──────┘        └─────┬──────┘
          │                     │
    ┌─────┴──────┐        ┌─────┴──────┐
    │ElastiCache │        │ElastiCache │
    └────────────┘        └────────────┘
          │                     │
    ┌─────┴──────┐        ┌─────┴──────┐
    │   Aurora   │◀──────▶│   Aurora   │
    │  Primary   │ Replica│  Replica   │
    └────────────┘        └────────────┘

Calculations:
- 100K users × 10 req/min = 1M req/min = 16,666 req/sec
- Each t3.large handles ~500 req/sec
- Need ~35 instances (with 20% buffer)
```

---

## Exercise 4: DR Strategy

```
RPO: 5 minutes
RTO: 30 minutes

Strategy: Warm Standby

Primary Region (us-east-1):
- Full production stack
- Aurora Primary
- Active Auto Scaling

DR Region (us-west-2):
- Scaled-down infrastructure (20%)
- Aurora Read Replica
- AMIs synced

Failover Process:
1. Route 53 health check fails (2 min)
2. Automatic DNS failover triggered
3. Scale up DR region (5 min)
4. Promote Aurora replica (5 min)
5. Verify services (5 min)

Total RTO: ~17 minutes (within 30 min target)
```

---

**[← Back to Exercises](./EXERCISES.md)**
