# 📈 Scalability — Mở rộng hệ thống

> `[ADVANCED]` — Từ 100 users đến 1 triệu users

---

## Tại sao cần Scale?

Mọi hệ thống bắt đầu đơn giản: 1 server, 1 database. Nhưng khi users tăng:

```
100 users:    1 server đủ 😊
1,000 users:  Server chậm lại 😐
10,000 users: Server crash lúc peak 😰
100,000 users: Cần architecture mới 🏗️
1,000,000 users: Distributed system 🌍
```

Scale không chỉ là "thêm RAM" — cần thay đổi **cách thiết kế** hệ thống.

---

## 1. Vertical vs Horizontal Scaling

```
Vertical Scaling (Scale Up):
  ┌──────────┐     ┌──────────────┐
  │ 4GB RAM  │  →  │  64GB RAM    │
  │ 2 cores  │     │  32 cores    │
  │ Server   │     │  Bigger Server│
  └──────────┘     └──────────────┘
  
  ✅ Đơn giản (upgrade hardware)
  ❌ Có giới hạn (max RAM/CPU)
  ❌ Single point of failure
  ❌ Downtime khi upgrade

Horizontal Scaling (Scale Out):
  ┌──────────┐     ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
  │  Server  │  →  │ S1  │ │ S2  │ │ S3  │ │ S4  │
  └──────────┘     └─────┘ └─────┘ └─────┘ └─────┘
                        ↑ Load Balancer ↑

  ✅ Gần như unlimited (thêm máy)
  ✅ Fault tolerant (S1 chết → S2,S3,S4 vẫn chạy)
  ❌ Phức tạp hơn (session, data consistency)
```

---

## 2. Load Balancing — Phân tải

```
                    ┌─────────────────┐
                    │  Load Balancer  │
                    │  (Nginx/HAProxy)│
                    └────────┬────────┘
                    ┌────────┼────────┐
                    ▼        ▼        ▼
               ┌────────┐ ┌────────┐ ┌────────┐
               │ App 1  │ │ App 2  │ │ App 3  │
               └────────┘ └────────┘ └────────┘
                    ┌────────┼────────┐
                    ▼        ▼        ▼
               ┌──────────────────────────┐
               │      Database (shared)    │
               └──────────────────────────┘
```

**Algorithms:**
- **Round Robin**: Lần lượt server 1, 2, 3, 1, 2, 3... (đơn giản)
- **Least Connections**: Gửi đến server ít connections nhất (thông minh hơn)
- **IP Hash**: Cùng IP → cùng server (sticky sessions)
- **Weighted**: Server mạnh hơn → nhận nhiều traffic hơn

**Stateless rule**: App servers PHẢI stateless — không lưu session trong memory. Lưu sessions ở Redis/DB → bất kỳ server nào cũng handle được bất kỳ request nào.

---

## 3. Database Scaling

### Read Replicas — Scale reads

```
Writes ──► Primary DB ──replication──► Replica 1 (reads)
                                  ──► Replica 2 (reads)
                                  ──► Replica 3 (reads)
Reads ◄──────────────────────────────┘

80% operations là reads → scale reads bằng replicas.
Primary xử lý writes (1 server đủ cho most cases).
```

### Sharding — Scale writes

Khi 1 database không đủ chứa TẤT CẢ data:

```
Shard key: user_id

Users 1-1M    → Shard 1 (DB Server A)
Users 1M-2M   → Shard 2 (DB Server B)  
Users 2M-3M   → Shard 3 (DB Server C)

Mỗi shard chỉ chứa 1/3 data → mỗi shard nhanh hơn!
```

**Trade-offs của sharding:**
- ✅ Scale gần như unlimited
- ❌ Cross-shard queries rất khó (JOIN giữa 2 shards?)
- ❌ Rebalancing khi thêm shard phức tạp
- ❌ Application logic phải biết shard nào cho data nào

**Lời khuyên**: Sharding là **last resort**. Thử đủ các cách khác trước: indexing, query optimization, caching, read replicas.

---

## 4. Caching — Giảm load cho DB

```
Không cache:
  Request → App → Database (100ms) → Response
  1000 RPS → 1000 DB queries/second 😰

Có cache:
  Request → App → Cache hit? (1ms) → Response    (95% cache hit)
                 → Cache miss → Database → Cache → Response (5%)
  1000 RPS → 50 DB queries/second 🎉
```

### Caching layers

```
Client ──► CDN (static assets) 
       ──► App Server ──► Redis (application cache)
                      ──► Database (source of truth)

Layer 1: CDN cache (Cloudflare, CloudFront)
  → Static files: JS, CSS, images. TTL: days/months.

Layer 2: Application cache (Redis, Memcached)
  → DB query results, API responses. TTL: seconds/minutes.

Layer 3: Database cache (query cache, buffer pool)
  → Tự quản lý, tuning config.
```

### Cache Invalidation — Bài toán khó nhất

```
"There are only two hard things in Computer Science:
 cache invalidation and naming things."

Strategies:
  1. TTL (Time-To-Live): Cache expires sau N seconds
     → Đơn giản, nhưng stale data trong N seconds
  
  2. Write-through: Write DB + write cache cùng lúc
     → Consistent, nhưng chậm hơn (2 writes)
  
  3. Write-behind: Write cache → async write DB
     → Nhanh, nhưng risk data loss
  
  4. Cache-aside (lazy): Read miss → load from DB → write cache
     + Write: update DB → delete cache
     → Phổ biến nhất, flexible
```

---

## 5. Message Queues — Decouple & Buffer

```
Không queue:
  User → API → Process (5 phút) → Response
  User chờ 5 phút! API timeout! 😫

Có queue:
  User → API → Queue → Response "Processing..." (200ms)
               Queue → Worker → Process (5 phút)
               Worker → Notify user "Done!"
```

Queues cũng giúp **buffer traffic spikes**: nếu đột nhiên 10x requests, queue giữ messages, workers xử lý dần → hệ thống không crash.

---

## 6. CDN — Content Delivery Network

```
Không CDN:
  User (VN) ──200ms──► Server (US) ──200ms──► User
  Mỗi request: 400ms network latency

Có CDN:
  User (VN) ──5ms──► CDN Edge (SG) ──5ms──► User
  Mỗi request: 10ms network latency 🚀

CDN caching:
  First request: CDN → Origin → cache → User
  Next requests: CDN → cache hit → User (không call origin!)
```

---

## 7. Lộ trình Scale (thực tế)

| Stage | Users | Architecture |
|---|---|---|
| 1 | < 1K | 1 server + 1 DB (đủ!) |
| 2 | 1K-10K | + CDN + caching (Redis) |
| 3 | 10K-100K | + Load balancer + multiple app servers |
| 4 | 100K-500K | + Read replicas + queue workers |
| 5 | 500K-1M | + Sharding hoặc managed DB (Aurora, PlanetScale) |
| 6 | > 1M | + Microservices + Kubernetes + multi-region |

**Rule quan trọng nhất**: **Premature optimization is the root of all evil.** Đừng sharding khi có 100 users. Optimize database queries, thêm indexes, thêm caching TRƯỚC. Chỉ scale khi thực sự cần.

---

## Bài tập thực hành

- [ ] Caching: thêm Redis cache cho API endpoint, đo latency trước/sau
- [ ] Load test: dùng k6 hoặc Artillery, tìm bottleneck
- [ ] Read replica: setup PostgreSQL primary + replica
- [ ] CDN: deploy static assets lên Cloudflare

---

## Tài nguyên thêm

- [System Design Primer](https://github.com/donnemartin/system-design-primer) — Free
- [Designing Data-Intensive Applications](https://dataintensive.net/) — Martin Kleppmann
- [High Scalability Blog](http://highscalability.com/) — Real case studies
