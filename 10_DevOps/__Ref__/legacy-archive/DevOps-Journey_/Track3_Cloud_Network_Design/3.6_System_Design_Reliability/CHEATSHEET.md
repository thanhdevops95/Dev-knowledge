# 📋 System Design & Reliability - Cheatsheet

> **Quick Reference for System Design Concepts**
>
> *Tra cứu nhanh thiết kế hệ thống*

---

## 📊 Key Metrics (Chỉ số quan trọng)

| Metric | Formula | Target |
|--------|---------|--------|
| **Availability** | Uptime / Total Time | 99.9% (3 nines) |
| **Latency** | Response time | < 100ms |
| **Throughput** | Requests/second | Domain specific |
| **Error Rate** | Errors / Total | < 1% |

---

## 🎯 Availability Targets

| SLA | Downtime/Year | Downtime/Month |
|-----|---------------|----------------|
| 99% | 3.65 days | 7.2 hours |
| 99.9% | 8.76 hours | 43.8 minutes |
| 99.99% | 52.6 minutes | 4.38 minutes |
| 99.999% | 5.26 minutes | 26.3 seconds |

---

## ⚖️ Scaling Patterns (Mô hình mở rộng)

### Horizontal vs Vertical (So sánh)

| Type | Description | Pros | Cons |
|------|-------------|------|------|
| **Vertical** | More resources | Simple | Limited |
| **Horizontal** | More instances | Unlimited | Complex |

---

## 🏗️ Architecture Patterns (Kiến trúc)

### Load Balancing

```
             ┌──────────────┐
             │Load Balancer │
             └──────┬───────┘
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   ┌────────┐ ┌────────┐ ┌────────┐
   │Server 1│ │Server 2│ │Server 3│
   └────────┘ └────────┘ └────────┘
```

### Caching Layers (Lớp cache)

```
Client → CDN → App Cache → Database Cache → Database
```

---

## 🔄 Reliability Strategies (Chiến lược tin cậy)

| Strategy | Description (Mô tả) |
|----------|---------------------|
| **Redundancy** | Multiple instances (Nhiều instances) |
| **Replication** | Data copies (Sao chép dữ liệu) |
| **Failover** | Automatic switch (Chuyển đổi tự động) |
| **Circuit Breaker** | Prevent cascade failures |
| **Rate Limiting** | Protect from overload |
| **Retry + Backoff** | Handle transient failures |

---

## 📈 Capacity Planning (Lập kế hoạch dung lượng)

```
Daily Active Users (DAU)
× Actions per User
× Data per Action
= Daily Data
× Growth Rate
= Required Capacity
```

---

## 🎯 CAP Theorem

```
     Consistency
         /\
        /  \
       /    \
      /______\
 Availability  Partition Tolerance
```

**Choose 2 of 3** (Chọn 2 trong 3):

- **CP**: MongoDB, Redis Cluster
- **AP**: Cassandra, DynamoDB
- **CA**: Traditional RDBMS (no partition tolerance)

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
