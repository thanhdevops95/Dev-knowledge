# 🏛️ System Design — Thiết kế hệ thống

> `[INTERMEDIATE → ADVANCED]` ⭐ `[MUST-KNOW]` — Kỹ năng thăng tiến lên Senior/Staff Engineer

---

## Tại sao cần học System Design?

- **Phỏng vấn:** Vòng System Design là vòng quan trọng nhất cho Senior+
- **Thực tế:** Kiến trúc sai → không scale được → làm lại từ đầu
- **Tư duy:** Học cách đánh đổi (tradeoffs) — không có giải pháp hoàn hảo

---

## 1. Quy trình thiết kế (Framework)

```
┌─────────────────────────────────────────────────┐
│ Bước 1: CLARIFY REQUIREMENTS (5 phút)           │
│   • Functional: Features chính?                  │
│   • Non-functional: Scale, latency, availability?│
│   • Constraints: Budget, team size?              │
├─────────────────────────────────────────────────┤
│ Bước 2: ESTIMATE (5 phút)                       │
│   • DAU, QPS, storage, bandwidth                 │
├─────────────────────────────────────────────────┤
│ Bước 3: HIGH-LEVEL DESIGN (10 phút)             │
│   • API design                                   │
│   • Database schema                              │
│   • Architecture diagram                         │
├─────────────────────────────────────────────────┤
│ Bước 4: DEEP DIVE (15 phút)                     │
│   • Bottleneck analysis                          │
│   • Scaling strategies                           │
│   • Edge cases                                   │
└─────────────────────────────────────────────────┘
```

---

## 2. Scaling — Mở rộng hệ thống

### Vertical vs Horizontal Scaling

```
Vertical Scaling (Scale Up):
┌──────────┐         ┌──────────────┐
│ 4GB RAM  │   →     │ 64GB RAM     │
│ 2 CPU    │         │ 32 CPU       │
│ 1 server │         │ 1 BIG server │
└──────────┘         └──────────────┘
  Giới hạn: 1 máy = giới hạn vật lý

Horizontal Scaling (Scale Out):
┌──────────┐         ┌───┐ ┌───┐ ┌───┐ ┌───┐
│ 1 server │   →     │ S1│ │ S2│ │ S3│ │ S4│
└──────────┘         └───┘ └───┘ └───┘ └───┘
                     Load Balancer phân phối requests
  Giới hạn: ∞ (thêm máy = thêm capacity)
```

---

### Load Balancer — Phân phối traffic

```
                    ┌──────────────┐
Users ──────────►   │Load Balancer │
                    └──────┬───────┘
                    ┌──────┼───────┐
                    ▼      ▼       ▼
                 ┌─────┐┌─────┐┌─────┐
                 │ S1  ││ S2  ││ S3  │
                 └─────┘└─────┘└─────┘

Thuật toán phân phối:
• Round Robin:    S1 → S2 → S3 → S1 → ...
• Least Connections: Gửi đến server ít request nhất
• IP Hash:        Cùng user → cùng server (sticky session)
• Weighted:       Server mạnh nhận nhiều hơn
```

---

### Caching — Giảm tải database

```
Client ──► Cache (Redis) ──► Database
             │
             │  Cache HIT: trả ngay (< 1ms)
             │  Cache MISS: query DB → lưu cache → trả
             ▼

Chiến lược cache:
┌──────────────────────────────────────────────┐
│ Cache-Aside (Lazy Loading):                  │
│   1. App check cache                         │
│   2. Cache miss → query DB → write cache     │
│   3. Tiếp theo → cache hit!                  │
├──────────────────────────────────────────────┤
│ Write-Through:                               │
│   1. App write cache + DB cùng lúc           │
│   2. Đảm bảo cache luôn đồng bộ             │
├──────────────────────────────────────────────┤
│ Write-Behind (Write-Back):                   │
│   1. App write cache                         │
│   2. Cache async write DB (batch)            │
│   3. Nhanh nhưng risk mất data              │
└──────────────────────────────────────────────┘
```

---

### Database Scaling

```
Replication — Nhân bản:
┌──────────┐
│  Master  │ ← Ghi (write)
│  (Primary)│
└─────┬────┘
   ┌──┴──┐
   ▼     ▼
┌──────┐ ┌──────┐
│Replica│ │Replica│ ← Đọc (read)
│  1   │ │  2   │
└──────┘ └──────┘
  Tách read/write → Master xử lý write, Replicas xử lý read

Sharding — Chia nhỏ dữ liệu:
┌───────────────────────────────────────┐
│         Users Table (100M rows)       │
├───────────┬───────────┬───────────────┤
│ Shard 1   │ Shard 2   │ Shard 3      │
│ Users A-H │ Users I-P │ Users Q-Z    │
│ 33M rows  │ 33M rows  │ 34M rows     │
└───────────┴───────────┴───────────────┘
  Mỗi shard = 1 DB riêng → query nhanh hơn
```

---

## 3. Design a URL Shortener (ví dụ)

### Requirements

```
Functional:
• Rút gọn URL dài → URL ngắn (bit.ly/abc123)
• Redirect URL ngắn → URL gốc
• Analytics: đếm số lần click

Non-functional:
• 100M URLs tạo/tháng
• Read:Write = 100:1
• Latency < 50ms
• Availability 99.9%
```

### Estimation

```
• 100M URLs/tháng ≈ ~40 URLs/giây (write)
• Read: 40 × 100 = 4000 QPS (read)
• Storage: 100M × 500 bytes = 50GB/tháng

URL ngắn: 7 ký tự (a-z, A-Z, 0-9) = 62⁷ = 3.5 tỷ combinations → đủ
```

### High-Level Design

```
Client ──► Load Balancer ──► API Servers ──► Database
                                  │
                                  ├──► Cache (Redis)
                                  │
                                  └──► Counter Service

API:
POST /api/shorten  { longUrl: "..." }  → { shortUrl: "bit.ly/abc123" }
GET  /abc123       → 301 Redirect → originalUrl
```

### Database Schema

```sql
-- URLs table
CREATE TABLE urls (
    id          BIGSERIAL PRIMARY KEY,
    short_code  VARCHAR(7) UNIQUE NOT NULL,
    long_url    TEXT NOT NULL,
    created_at  TIMESTAMP DEFAULT NOW(),
    expires_at  TIMESTAMP,
    click_count BIGINT DEFAULT 0
);

CREATE INDEX idx_short_code ON urls(short_code);
```

### Deep Dive — ID Generation

```
Cách 1: Hash (MD5/SHA256) → lấy 7 ký tự đầu
  hash("https://example.com/very-long-url")
  → "abc123d..."
  → Vấn đề: collision!

Cách 2: Auto-increment ID → Base62 encode
  ID: 12345 → Base62 → "dnh"
  → Unique, nhưng predictable

Cách 3: Snowflake ID (distributed)
  Timestamp + Machine ID + Sequence
  → Unique + distributed
```

---

## 4. Các khái niệm quan trọng

### CAP Theorem

```
Chỉ có thể chọn 2 trong 3:

         Consistency (C)
        / \
       /   \
      /     \
   CP /       \ CA
    /    ❌    \
   /   Không    \
  /   thể cả 3  \
Availability ──── Partition Tolerance
   (A)    AP    (P)

CA: PostgreSQL (single node) — network partition xảy ra → mất availability
CP: MongoDB, HBase — mất availability khi partition
AP: Cassandra, DynamoDB — eventual consistency khi partition

Thực tế: P luôn xảy ra → chọn giữa CP hoặc AP
```

### Rate Limiting

```
Token Bucket Algorithm:
┌─────────────┐
│ Bucket      │ Capacity: 10 tokens
│ ●●●●●●●●●● │ Refill: 1 token/giây
│             │
└──────┬──────┘
       │ Request đến → lấy 1 token
       │ Hết token → 429 Too Many Requests
```

### Message Queue

```
Producer ──► [Message Queue] ──► Consumer

         ┌───────────────────────┐
Order    │ RabbitMQ / Kafka      │    Email
Service ─┤                       ├── Service
         │ ┌───┐┌───┐┌───┐┌───┐│    Inventory
         │ │msg││msg││msg││msg││    Service
         │ └───┘└───┘└───┘└───┘│    Analytics
         └───────────────────────┘

Lợi ích:
• Decouple services
• Buffer traffic spikes
• Retry failed processing
• Async processing
```

---

## So sánh

| Vấn đề | Giải pháp |
|---|---|
| Quá nhiều read | Cache (Redis), Read replicas |
| Quá nhiều write | Sharding, Message queue |
| Single point of failure | Redundancy, Load balancer |
| Slow response | Cache, CDN, async processing |
| Data integrity | Transactions, idempotency |
| Geographic latency | CDN, multi-region deployment |

---

## Bài tập thực hành

- [ ] Design URL Shortener: vẽ diagram + estimate + schema
- [ ] Design Chat App: WebSocket, message queue, presence
- [ ] Design News Feed: Fan-out on write vs Fan-out on read
- [ ] Design Rate Limiter: Token bucket implementation

---

## Tài nguyên thêm

- [System Design Primer](https://github.com/donnemartin/system-design-primer) — GitHub #1 — free
- [Designing Data-Intensive Applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) — Sách kinh điển
- [ByteByteGo (YouTube)](https://www.youtube.com/@ByteByteGo) — Alex Xu — Visual System Design
