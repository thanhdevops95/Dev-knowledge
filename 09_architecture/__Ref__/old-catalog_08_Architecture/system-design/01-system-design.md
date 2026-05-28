# 🏗️ System Design — Thiết kế hệ thống lớn

> `[ADVANCED]` — Dành cho Senior Developer và Technical Interview

---

## Quy trình thiết kế hệ thống

```
1. Clarify requirements (5 phút)
   └── Functional: Hệ thống làm gì?
   └── Non-functional: Scale, latency, availability?

2. Estimate scale (2 phút)
   └── Users: 1M DAU?
   └── Requests: QPS bao nhiêu?
   └── Storage: bao nhiêu GB/TB?

3. High-level design (10 phút)
   └── Main components
   └── Data flow

4. Deep dive (20 phút)
   └── Database schema
   └── API design
   └── Bottlenecks & solutions

5. Wrap up
   └── Monitoring, alerting
   └── Failure scenarios
```

---

## Các khái niệm quan trọng

### Scalability

```
Vertical Scaling (Scale Up)
  → Thêm RAM, CPU vào 1 server
  → Đơn giản, nhưng có giới hạn và single point of failure

Horizontal Scaling (Scale Out)
  → Thêm nhiều servers
  → Phức tạp hơn, nhưng không giới hạn và fault tolerant
  → Cần: Load Balancer, Stateless app, Shared storage
```

### CAP Theorem

```
Trong hệ thống distributed, chỉ đảm bảo được 2 trong 3:

C — Consistency     : Mọi node thấy cùng data
A — Availability    : Hệ thống luôn phản hồi
P — Partition Tol.  : Hoạt động dù mạng bị chia cắt

Network partition không tránh được → Luôn phải có P
→ Chọn: CP (SQL, HBase) hoặc AP (Cassandra, DynamoDB)
```

### Latency Numbers (biết thuộc lòng!)

```
L1 cache reference          0.5 ns
L2 cache reference          7 ns
RAM reference               100 ns
SSD random read             100 μs
Network (same datacenter)   500 μs
HDD random read             10 ms
Network (US → Europe)       150 ms

→ Cache mọi thứ có thể cache được
→ Tránh disk I/O trong hot path
→ Tránh inter-datacenter calls trong critical path
```

---

## Patterns cơ bản

### Load Balancing

```
Algorithms:
- Round Robin          — Lần lượt từng server
- Weighted Round Robin — Server mạnh nhận nhiều hơn
- Least Connections    — Server ít kết nối nhất
- IP Hash              — Session sticky (cùng IP → cùng server)
- Consistent Hashing   — Ổn định khi thêm/xóa server
```

### Caching

```
Cache-Aside (Lazy Loading) — Phổ biến nhất:
  Read: Check cache → Hit: return | Miss: DB → write cache → return
  Write: Invalidate cache, write DB

Write-Through:
  Write: Write cache → Write DB (synchronous)
  → Consistent, nhưng write latency cao hơn

Write-Behind (Write-Back):
  Write: Write cache → Return | async write DB sau
  → Nhanh hơn, nhưng có thể mất data nếu crash

Read-Through:
  Read: Check cache → Miss: cache load DB → return
  → Cache tự manage, transparent với app
```

### Database Scaling

```
Read Replicas:
  → Master (write) + Replicas (read)
  → Tốt cho read-heavy workloads
  → Eventual consistency trên replicas

Sharding (Horizontal Partitioning):
  → Chia data theo shard key (user_id % N)
  → Mỗi shard là 1 database riêng
  → Tăng write throughput
  → Phức tạp: cross-shard queries, rebalancing

Database per Service:
  → Microservices: mỗi service có DB riêng
  → Không join cross-service
  → Dùng events để sync data
```

---

## Thiết kế URL Shortener (Ví dụ)

```
Requirements:
  Functional: Tạo short URL, redirect, analytics
  Non-functional: 100M URLs, 10:1 read/write ratio, low latency

Scale:
  Writes: 10M/day = 115 writes/sec
  Reads:  100M/day = 1150 reads/sec
  Storage: 10M × 500 bytes = 5GB/year

API:
  POST /api/shorten         { url: "https://..." }  → { shortCode: "abc123" }
  GET  /{shortCode}         → 301 Redirect
  GET  /api/stats/{code}    → { clicks, countries, ... }

Database Schema:
  urls: { id, original_url, short_code, user_id, created_at, expires_at }
  clicks: { id, url_id, ip, country, user_agent, clicked_at }

Short Code Generation:
  Option 1: Base62 encode của auto-increment ID
             ID=1000 → "G8" (6 ký tự = 56.8B URLs)
  Option 2: MD5 hash → lấy 7 ký tự đầu (collision risk)
  Option 3: UUID → base62 encode

Architecture:
  Client
    → Load Balancer
    → API Servers (stateless, horizontal scale)
    → Redis Cache (short_code → original_url, TTL 24h)
    → PostgreSQL (source of truth)
    → Analytics Service (Kafka + ClickHouse)
```

---

## Thiết kế Twitter Feed (Timeline)

```
Requirements:
  Functional: Post tweet, follow, home timeline
  Non-functional: 200M DAU, eventual consistency OK

Scale:
  Tweets: 100 tweet/sec
  Reads:  100K reads/sec (read-heavy!)

Fan-out Approaches:

  Fan-out on Write (Push):
    Khi user post tweet → push vào inbox của tất cả followers
    → Đọc nhanh (inbox sẵn sàng)
    → Viết chậm nếu user có nhiều follower (celeb problem)

  Fan-out on Read (Pull):
    Khi user đọc feed → merge tweets của tất cả người follow
    → Viết nhanh
    → Đọc chậm (nhiều DB queries)

  Hybrid (Twitter thực tế):
    - Regular users (< 10K followers): Fan-out on Write
    - Celebrities (> 10K followers): Fan-out on Read
    - Timeline = Pre-computed cache + Real-time celeb tweets
```

---

## Microservices vs Monolith

```
Monolith — Bắt đầu ở đây:
  ✅ Đơn giản, dễ debug, dễ deploy
  ✅ No network latency giữa components
  ❌ Scale toàn bộ dù chỉ 1 phần cần scale
  ❌ Công nghệ bị lock-in
  → Tốt cho: startup, team nhỏ, domain chưa rõ

Microservices — Khi thực sự cần:
  ✅ Scale từng service độc lập
  ✅ Deploy độc lập
  ✅ Technology diversity
  ❌ Network latency, distributed tracing
  ❌ Data consistency khó hơn
  ❌ Cần DevOps culture mạnh
  → Tốt cho: large scale, multiple teams, clear domain boundaries
```

### Microservices Communication

```
Synchronous (REST/gRPC):
  → Request cần response ngay
  → API Gateway → Services
  → Dùng cho: User-facing APIs

Asynchronous (Message Queue):
  → Fire and forget, eventual consistency
  → Kafka, RabbitMQ, AWS SQS
  → Dùng cho: Notifications, emails, analytics, payment processing
```

---

## Observability — 3 Pillars

```
Logs — What happened?
  → Structured logging (JSON)
  → Log levels: DEBUG, INFO, WARN, ERROR
  → ELK Stack hoặc Loki + Grafana

Metrics — How is the system?
  → RED: Rate, Errors, Duration
  → USE: Utilization, Saturation, Errors
  → Prometheus + Grafana

Traces — Where did the request go?
  → Distributed tracing
  → OpenTelemetry + Jaeger/Zipkin
  → Trace request qua nhiều services
```

---

## Cheat Sheet cho interview

**Tốc độ cần biết:**
```
10^3 = 1K/sec = dễ dàng với 1 server
10^4 = 10K/sec = cần optimize
10^5 = 100K/sec = cần cache + multiple servers
10^6 = 1M/sec = cần serious architecture
```

**Tools phổ biến:**
```
Load Balancer    : Nginx, HAProxy, AWS ALB
Cache            : Redis, Memcached
Message Queue    : Kafka, RabbitMQ, AWS SQS
Search           : Elasticsearch, Typesense
Object Storage   : S3, GCS
CDN              : CloudFront, Cloudflare
Database         : PostgreSQL, MySQL, Cassandra, DynamoDB
```

---

## Tài nguyên thêm

- [System Design Primer](https://github.com/donnemartin/system-design-primer) — GitHub repo nổi tiếng nhất
- [ByteByteGo Newsletter](https://bytebytego.com/) — Weekly system design
- [Designing Data-Intensive Applications (DDIA)](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) — Cuốn sách kinh điển
- [High Scalability Blog](http://highscalability.com/) — Case studies thực tế
