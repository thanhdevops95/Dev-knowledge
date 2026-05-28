# 05. Availability, Scalability & Rate Limiting

[← Caching & CDN](04_CACHING_CDN.md) | [Tiếp: Security →](06_SECURITY.md)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Availability** | /əˌveɪləˈbɪləti/ | Tính sẵn sàng - Thời gian hệ thống hoạt động bình thường |
| **Uptime** | - | Thời gian hoạt động - Thời gian hệ thống online |
| **Downtime** | - | Thời gian ngừng - Thời gian hệ thống offline |
| **SLA** | - | Service Level Agreement - Cam kết mức độ dịch vụ |
| **The 9's** | - | Cách đo availability (99.9% = "three nines") |
| **HA** | - | High Availability - Tính sẵn sàng cao |
| **Fault Tolerance** | - | Chịu lỗi - Hệ thống vẫn hoạt động khi có lỗi |
| **Failover** | - | Chuyển đổi dự phòng - Tự động chuyển sang backup |
| **Redundancy** | - | Dự phòng - Có nhiều bản sao để phòng trường hợp lỗi |
| **Resilience** | - | Khả năng phục hồi - Có thể tự hồi phục sau lỗi |
| **Self-healing** | - | Tự phục hồi - Hệ thống tự động sửa lỗi |
| **Scalability** | - | Khả năng mở rộng - Có thể tăng tài nguyên khi cần |
| **Vertical Scaling** | - | Mở rộng dọc - Nâng cấp phần cứng (thêm RAM, CPU) |
| **Horizontal Scaling** | - | Mở rộng ngang - Thêm nhiều máy chủ |
| **Rate Limiting** | - | Giới hạn tốc độ - Giới hạn số request trong khoảng thời gian |
| **Auto-scaling** | - | Tự động mở rộng - Tự động thêm/bớt tài nguyên |

---

# 🤔 Tại sao DevOps cần biết Availability và Scalability?

## Nỗi đau thực tế

> "Website down lúc 2 giờ sáng, khách hàng gọi điện than phiền"

> "Flash sale mà server sập, mất hàng triệu đồng doanh thu"

> "Sếp hỏi: Hệ thống của mình có thể chịu được bao nhiêu user?"

## Kiến thức này giúp bạn

| Tình huống | Cần biết |
|------------|----------|
| Cam kết SLA với khách hàng | The 9's, availability calculation |
| Thiết kế hệ thống không downtime | HA, failover, redundancy |
| Chuẩn bị cho traffic đột biến | Rate limiting, auto-scaling |
| Tối ưu chi phí infrastructure | Vertical vs Horizontal scaling |
| Xử lý sự cố tự động | Self-healing, resilience |

Availability và Scalability là hai yếu tố quyết định sự thành công của hệ thống production. Một hệ thống không available là hệ thống không có giá trị.

---

# 📊 Availability

## Availability là gì?

**Availability** là thời gian một hệ thống **hoạt động bình thường** để thực hiện chức năng cần thiết trong một khoảng thời gian cụ thể. Đây là một **thước đo đơn giản** về phần trăm thời gian mà hệ thống, dịch vụ, hoặc máy móc **vận hành dưới điều kiện bình thường**.

Availability thường được đo bằng **uptime (hoặc downtime)** dưới dạng phần trăm:

```
                    Uptime
Availability = ─────────────────────
               Uptime + Downtime
```

### Tại sao Availability quan trọng?

Trong production environment, downtime có thể gây ra:

- **Mất doanh thu**: Amazon estimated mất ~$200K mỗi phút downtime
- **Mất niềm tin khách hàng**: Users chuyển sang competitor
- **Vi phạm SLA**: Phải đền bù cho khách hàng
- **Ảnh hưởng thương hiệu**: Reputation damage

---

## The Nine's of Availability

Availability thường được measured bằng **number of 9s**. Mỗi "9" thêm vào có nghĩa là giảm downtime đáng kể.

| Availability | Nines | Downtime/Year | Downtime/Month | Downtime/Week | Downtime/Day |
|--------------|-------|---------------|----------------|---------------|--------------|
| 90% | One 9 | 36.53 days | 72 hours | 16.8 hours | 2.4 hours |
| 99% | Two 9s | 3.65 days | 7.20 hours | 1.68 hours | 14.4 min |
| 99.9% | Three 9s | 8.77 hours | 43.8 minutes | 10.1 minutes | 1.44 min |
| 99.99% | Four 9s | 52.6 minutes | 4.32 minutes | 1.01 minutes | 8.64 sec |
| 99.999% | Five 9s | 5.25 minutes | 25.9 seconds | 6.05 seconds | 864 ms |
| 99.9999% | Six 9s | 31.56 seconds | 2.59 seconds | 604.8 ms | 86.4 ms |

### Thực tế về "The 9's"

**Three 9s (99.9%)** = ~8.77 hours downtime/year

- Phù hợp cho hầu hết internal applications
- Cho phép maintenance windows

**Four 9s (99.99%)** = ~52 minutes downtime/year

- Standard cho production services
- Requires redundancy và automation

**Five 9s (99.999%)** = ~5 minutes downtime/year

- Mission-critical systems (banks, healthcare)
- Extremely expensive to achieve
- Requires sophisticated architecture

> **Quy tắc thực tế**: Mỗi "9" thêm vào thường tốn **gấp 10 lần** chi phí để đạt được.

---

## Availability in Sequence vs Parallel

### Sequence (Nối tiếp)

Nếu service consists of **multiple components in sequence** (phụ thuộc nhau), overall availability **giảm**:

```
┌─────────────────────────────────────────────────────────────┐
│                    SEQUENCE                                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│     ┌───────┐      ┌───────┐      ┌───────┐                 │
│  ───►│   A   ├─────►│   B   ├─────►│   C   ├───►             │
│     │ 99.9% │      │ 99.9% │      │ 99.9% │                 │
│     └───────┘      └───────┘      └───────┘                 │
│                                                              │
│  Availability = A × B × C                                    │
│               = 0.999 × 0.999 × 0.999                        │
│               = 0.997 (99.7%)                                │
│                                                              │
│  ⚠️ Mỗi component thêm vào làm GIẢM overall availability!   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Ví dụ thực tế:**

```
Web Request Flow:
DNS (99.99%) → Load Balancer (99.99%) → App Server (99.9%) → Database (99.9%)

Overall = 0.9999 × 0.9999 × 0.999 × 0.999
        = 0.9978 (99.78%)
```

### Parallel (Song song)

Nếu components hoạt động **in parallel** (redundant), overall availability **tăng**:

```
┌─────────────────────────────────────────────────────────────┐
│                     PARALLEL                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│              ┌───────┐                                       │
│         ┌───►│   A   ├───┐                                  │
│         │    │ 99.9% │   │                                  │
│     ────┤    └───────┘   ├────►                             │
│         │                │                                   │
│         │    ┌───────┐   │                                  │
│         └───►│   B   ├───┘                                  │
│              │ 99.9% │                                       │
│              └───────┘                                       │
│                                                              │
│  Availability = 1 - (1-A) × (1-B)                           │
│               = 1 - (0.001) × (0.001)                        │
│               = 1 - 0.000001                                 │
│               = 0.999999 (99.9999%)                          │
│                                                              │
│  ✅ Redundancy dramatically IMPROVES availability!          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Kết hợp Sequence và Parallel:**

```
┌────────────────────────────────────────────────────────────────┐
│                    REAL-WORLD ARCHITECTURE                      │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│                     ┌──────────┐                                │
│               ┌────►│ Server 1 │                                │
│               │     └──────────┘                                │
│  ┌────────┐   │     ┌──────────┐     ┌────────────┐            │
│  │  LB    │───┼────►│ Server 2 │────►│  Database  │            │
│  │(99.99%)│   │     └──────────┘     │  Primary   │            │
│  └────────┘   │     ┌──────────┐     │  (99.9%)   │            │
│               └────►│ Server 3 │     └──────┬─────┘            │
│                     └──────────┘            │ replication       │
│                                       ┌─────┴──────┐            │
│                 (99.9% each,          │  Database  │            │
│                  parallel = 99.9999%) │  Replica   │            │
│                                       │  (99.9%)   │            │
│                                       └────────────┘            │
│                                                                 │
│  Overall = LB × Servers(parallel) × DB(parallel)               │
│          = 99.99% × 99.9999% × 99.9999%                        │
│          ≈ 99.98%                                              │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## Availability vs Reliability

| Concept | Definition | Focus | Example |
|---------|------------|-------|---------|
| **Availability** | % time system is operational | Uptime | System online 99.99% of time |
| **Reliability** | Probability system performs correctly | Correctness | System returns correct results |

**Ví dụ để phân biệt:**

- System available 99.99% nhưng returns wrong data 10% of time → **High availability, low reliability**
- System available 95% nhưng always returns correct data → **Lower availability, high reliability**

> Một system có thể highly available nhưng unreliable (ví dụ: API luôn response nhưng đôi khi trả sai data).

---

## High Availability (HA) vs Fault Tolerance

| Aspect | High Availability | Fault Tolerance |
|--------|-------------------|-----------------|
| **Goal** | Minimize downtime | Zero downtime |
| **Approach** | Quick recovery after failure | No interruption at all |
| **Downtime during failure** | Brief (seconds to minutes) | None |
| **Cost** | Moderate | Very high |
| **Complexity** | Medium | High |
| **Data loss risk** | Minimal | None |
| **Example** | Database with failover | Airplane with redundant systems |

**High Availability:**

```
Primary fails → 30 seconds → Standby takes over → Service restored
                  ↓
             Brief downtime
```

**Fault Tolerance:**

```
Primary fails → Standby already processing → No interruption
                       ↓
                   Zero downtime
```

---

## Failover

### Failover là gì?

**Failover** là process tự động chuyển sang **backup system** khi primary system fails. Đây là foundation của High Availability.

```
┌─────────────────────────────────────────────────────────────┐
│                       FAILOVER                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  NORMAL OPERATION:                                           │
│  ┌────────────────────────────────────────────────────┐     │
│  │                                                    │     │
│  │  Traffic ─────────────► Primary Server            │     │
│  │                              │                     │     │
│  │                              │ replication         │     │
│  │                              ▼                     │     │
│  │                         Standby Server            │     │
│  │                                                    │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  AFTER PRIMARY FAILURE:                                      │
│  ┌────────────────────────────────────────────────────┐     │
│  │                                                    │     │
│  │  Traffic ─────────────► Standby (now Active)      │     │
│  │                         (automatic switchover)     │     │
│  │                                                    │     │
│  │                          Primary (down)           │     │
│  │                              X                     │     │
│  │                                                    │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Types of Failover

| Type | RTO (Recovery Time) | Data Loss | Use Case |
|------|---------------------|-----------|----------|
| **Cold** | Hours | Possible | Dev/Test environments |
| **Warm** | Minutes | Minimal | Non-critical systems |
| **Hot** | Seconds | None | Production, critical systems |

**Cold Failover:**

- Standby server off or minimal config
- Start và configure khi primary fails
- Có thể mất data chưa backup

**Warm Failover:**

- Standby server running với old data
- Sync data khi primary fails
- Brief downtime để sync

**Hot Failover:**

- Standby server fully synced (real-time replication)
- Takeover ngay lập tức
- Zero data loss

---

## Resilience / Self-healing

### Resilience là gì?

**Resilience** là khả năng của system để **recover from failures** và continue operating. Một resilient system có thể:

- **Absorb** unexpected failures
- **Recover** quickly
- **Adapt** to changing conditions

### Self-healing là gì?

**Self-healing** là hệ thống có thể **tự động detect và fix** problems mà không cần human intervention.

```
┌─────────────────────────────────────────────────────────────┐
│                    SELF-HEALING FLOW                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ① Health Check detects failure                             │
│       │                                                      │
│       ▼                                                      │
│  ② System identifies unhealthy instance                     │
│       │                                                      │
│       ▼                                                      │
│  ③ Automatically terminate unhealthy instance               │
│       │                                                      │
│       ▼                                                      │
│  ④ Spin up new healthy instance                             │
│       │                                                      │
│       ▼                                                      │
│  ⑤ Route traffic to healthy instances                       │
│       │                                                      │
│       ▼                                                      │
│  ⑥ System back to desired state                             │
│                                                              │
│  All automatic - no human intervention!                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Examples của Self-healing:**

| Technology | Self-healing behavior |
|------------|----------------------|
| **Kubernetes** | Restarts crashed pods, reschedules to healthy nodes |
| **AWS Auto Scaling** | Replaces unhealthy EC2 instances |
| **Database HA** | Automatic failover to replica |
| **Container orchestration** | Restart failed containers |

---

# 📈 Scalability

## Scalability là gì?

**Scalability** là measure của how well a system **responds to changes** bằng cách **adding hoặc removing resources** to meet demands.

Một scalable system có thể **handle increased load** mà không có significant performance degradation. Có hai approaches chính:

---

## Vertical Scaling (Scale Up)

**Vertical scaling** expands system's scalability bằng cách **adding more power to an existing machine**: more CPU, more RAM, more storage.

```
┌────────────────────────────────────────────────────────────┐
│                  VERTICAL SCALING                           │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  BEFORE:                    AFTER:                          │
│  ┌──────────────┐          ┌──────────────────────┐        │
│  │    2 CPU     │   ───►   │       8 CPU          │        │
│  │   4GB RAM    │          │      64GB RAM        │        │
│  │  100GB SSD   │          │     1TB NVMe SSD     │        │
│  │              │          │                      │        │
│  │  Can handle  │          │    Can handle        │        │
│  │  100 users   │          │    500 users         │        │
│  └──────────────┘          └──────────────────────┘        │
│                                                             │
│  Same machine, just more powerful hardware                  │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### Advantages

| Advantage | Explanation |
|-----------|-------------|
| **Simple** | No code changes needed |
| **No distribution** | Data stays on one machine |
| **No coordination** | No network between nodes |
| **Easy management** | Single server to manage |

### Disadvantages

| Disadvantage | Explanation |
|--------------|-------------|
| **Hardware limits** | Maximum capacity exists (can't add infinite CPU) |
| **Single point of failure** | One machine down = all down |
| **Expensive** | High-end hardware costs exponentially more |
| **Downtime** | Often requires restart to upgrade |
| **Diminishing returns** | 2x hardware ≠ 2x performance |

---

## Horizontal Scaling (Scale Out)

**Horizontal scaling** expands system's scale bằng cách **adding more machines** to the pool.

```
┌────────────────────────────────────────────────────────────┐
│                 HORIZONTAL SCALING                          │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  BEFORE:                                                    │
│  ┌──────────────┐                                          │
│  │   Server     │  Can handle 100 users                    │
│  └──────────────┘                                          │
│                                                             │
│  AFTER:                                                     │
│              ┌─────────────┐                                │
│         ┌───►│  Server 1   │                                │
│         │    └─────────────┘                                │
│         │    ┌─────────────┐                                │
│  LB ────┼───►│  Server 2   │  Can handle 400 users         │
│         │    └─────────────┘                                │
│         │    ┌─────────────┐                                │
│         ├───►│  Server 3   │                                │
│         │    └─────────────┘                                │
│         │    ┌─────────────┐                                │
│         └───►│  Server 4   │                                │
│              └─────────────┘                                │
│                                                             │
│  More machines, distributed load                            │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### Advantages

| Advantage | Explanation |
|-----------|-------------|
| **No limits** | Add machines indefinitely |
| **Redundancy** | Failure of one doesn't affect others |
| **Cost-effective** | Use cheaper commodity hardware |
| **Geographic distribution** | Place servers closer to users |
| **Linear scaling** | More machines ≈ more capacity |

### Disadvantages

| Disadvantage | Explanation |
|--------------|-------------|
| **Complexity** | Need load balancing, coordination |
| **Data consistency** | Synchronization challenges |
| **Code changes** | May need to design for distribution |
| **Network latency** | Communication between nodes adds delay |
| **Stateless requirement** | Usually requires stateless design |

---

## When to use which?

| Criteria | Vertical Scaling | Horizontal Scaling |
|----------|------------------|-------------------|
| **Initial stage** | ✅ Start simple | More complex setup |
| **Predictable growth** | Good fit | May be overkill |
| **Rapid/unlimited growth** | Limited by hardware | ✅ Best choice |
| **Stateless apps** | Either works | ✅ Preferred |
| **Stateful apps** | ✅ Simpler | Needs careful design |
| **Cost at scale** | Exponentially expensive | More cost-effective |
| **Downtime tolerance** | Requires maintenance window | ✅ Zero-downtime scaling |

### Real-world recommendation

```
Startup phase:
├── Start with vertical scaling (simple)
├── Focus on product, not infrastructure
└── Scale up as needed

Growth phase:
├── Design for horizontal scaling
├── Move to stateless architecture
└── Implement load balancing

Scale phase:
├── Horizontal scaling is the only way
├── Use auto-scaling
└── Geographic distribution
```

---

# 🚦 Rate Limiting

## Rate Limiting là gì?

**Rate limiting** refers to **preventing the frequency of an operation from exceeding a defined limit**. Trong large-scale systems, rate limiting được commonly used để **protect underlying services và resources**.

Rate limiting là một **defensive mechanism** trong distributed systems để shared resources có thể **maintain availability**.

---

## Tại sao cần Rate Limiting?

| Reason | Explanation |
|--------|-------------|
| **Prevent DoS attacks** | Stop malicious actors from overwhelming your system |
| **Control costs** | API calls = money (cloud resources, third-party APIs) |
| **Fair usage** | Prevent one user from consuming all resources |
| **Protect backend** | Databases và downstream services có giới hạn |
| **Improve reliability** | Graceful degradation under load |

**Real-world example:**

```
GitHub API: 5000 requests/hour for authenticated users
Twitter API: 300 requests/15 minutes per endpoint
Google Maps: 25,000 requests/day free tier
```

---

## Rate Limiting Algorithms

### Token Bucket

**Token Bucket** là algorithm phổ biến nhất. Tokens được thêm vào bucket theo rate cố định, mỗi request cần 1 token.

```
┌────────────────────────────────────────────────────────────┐
│                    TOKEN BUCKET                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Tokens refill: 10 tokens/second                            │
│  Bucket size: 100 tokens (max)                              │
│                                                             │
│       Refill                                                │
│         ↓                                                   │
│   ┌─────────────────────────────────┐                      │
│   │ ████████████████░░░░░░░░░░░░░░░ │                      │
│   │     70/100 tokens available     │                      │
│   └─────────────────────────────────┘                      │
│                     ↓                                       │
│              Request arrives                                │
│                     │                                       │
│            ┌────────┴────────┐                             │
│            │                 │                              │
│       Has token?         No token?                          │
│            │                 │                              │
│       ✅ Allow           ❌ Reject                          │
│       (spend 1)         (429 error)                         │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

**Đặc điểm:**

- Allows **burst** traffic (up to bucket size)
- Smooth average rate
- Most flexible

### Leaky Bucket

**Leaky Bucket** processes requests at a **constant rate**, like water leaking from a bucket.

```
┌────────────────────────────────────────────────────────────┐
│                    LEAKY BUCKET                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│     Incoming requests (variable rate)                       │
│         ↓ ↓ ↓ ↓ ↓ ↓                                        │
│   ┌─────────────────────────────────┐                      │
│   │                                 │                      │
│   │     Bucket (Queue)              │ ← Overflow rejected  │
│   │     [R1][R2][R3][R4]            │                      │
│   │                                 │                      │
│   └──────────────┬──────────────────┘                      │
│                  │                                          │
│                  ↓ (leak = constant rate)                   │
│          Process 1 request/second                           │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

**Đặc điểm:**

- Smooth output rate
- No bursts allowed
- Queue-based

### Fixed Window

**Fixed Window** counts requests per **fixed time window**.

```
┌────────────────────────────────────────────────────────────┐
│                    FIXED WINDOW                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Window: 1 minute    Limit: 100 requests                    │
│                                                             │
│  [0:00 ─────── 1:00] [1:00 ─────── 2:00] [2:00 ───         │
│        95 reqs ✅          105 reqs                         │
│                            100 ✅ + 5 ❌                     │
│                                                             │
│  ⚠️ Problem: 100 reqs at 0:59 + 100 reqs at 1:01            │
│             = 200 requests in 2 seconds!                    │
│             (boundary problem)                              │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### Sliding Window

**Sliding Window** fixes boundary problem bằng cách track requests trong **rolling time window**.

```
┌────────────────────────────────────────────────────────────┐
│                   SLIDING WINDOW                            │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Current time: 1:30                                         │
│  Window: Last 1 minute (0:30 - 1:30)                        │
│                                                             │
│  Timeline:                                                  │
│  ─────[────────window────────]─────────                    │
│   0:00   0:30             1:30   2:00                       │
│            ↑               ↑                                │
│       Window start    Current time                          │
│                                                             │
│  Count all requests in [0:30, 1:30] range                   │
│  Smoother rate limiting, no boundary issues                 │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## HTTP 429 Response

Khi rate limit exceeded, server trả về **HTTP 429 Too Many Requests**:

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 60
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1640000000

{
  "error": "Rate limit exceeded",
  "message": "You have exceeded the rate limit of 100 requests per minute",
  "retry_after": 60
}
```

**Response Headers giải thích:**

| Header | Meaning |
|--------|---------|
| `Retry-After` | Seconds to wait before retry |
| `X-RateLimit-Limit` | Maximum requests allowed |
| `X-RateLimit-Remaining` | Requests remaining in window |
| `X-RateLimit-Reset` | Unix timestamp when limit resets |

---

## Rate Limiting Best Practices

1. **Return informative errors**: Tell clients when they can retry
2. **Different limits per endpoint**: Critical vs non-critical
3. **Different limits per user tier**: Free vs paid
4. **Implement graceful degradation**: Serve cached/partial data
5. **Log rate limiting events**: Monitor for attacks

---

# 🔄 Auto-scaling

## Auto-scaling là gì?

**Auto-scaling** tự động adjusts số lượng compute resources based on current demand. Thay vì manually add/remove servers, system tự động làm.

```
┌────────────────────────────────────────────────────────────┐
│                    AUTO-SCALING                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Resources                                                  │
│     ▲                                                       │
│     │         ┌─────────────────────────┐                  │
│  10 │         │   Scale Out            │   │               │
│     │      ┌──┘                     ┌──┘   │ Scale In      │
│   5 │   ┌──┘                       │       └──┐            │
│     │───┘                          │          └──┐         │
│   2 │──────────────────────────────┴─────────────│         │
│     └────────────────────────────────────────────►  Time   │
│         6AM    9AM     12PM    6PM    12AM                  │
│          └──────┴───────┴───────┴───────┘                  │
│         Morning  Peak    Lunch   Evening  Night            │
│                                                             │
│  RULES:                                                     │
│  • CPU > 80% for 5 min → Add 2 instances                   │
│  • CPU < 30% for 10 min → Remove 1 instance                │
│  • Min: 2 instances, Max: 20 instances                      │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## Types of Auto-scaling

| Type | Trigger | Example | Pros | Cons |
|------|---------|---------|------|------|
| **Reactive** | Metrics threshold | CPU > 80% | Simple, reliable | Lag behind demand |
| **Scheduled** | Time-based | Scale up at 9 AM | Predictable costs | Inflexible |
| **Predictive** | ML-based forecast | Predicted traffic | Proactive | Requires data, complex |

### Reactive (Target-based)

```yaml
# AWS Auto Scaling Example
ScalingPolicy:
  TargetValue: 75.0  # Target CPU %
  MetricType: ASGAverageCPUUtilization
  ScaleOutCooldown: 300  # 5 min
  ScaleInCooldown: 300
```

### Scheduled

```yaml
# Scale up before business hours
ScheduledAction:
  Schedule: "cron(0 8 * * MON-FRI)"
  MinSize: 5
  MaxSize: 20
  DesiredCapacity: 10
```

### Predictive

Uses machine learning to analyze historical traffic patterns và scale **before** demand increases.

---

## Key Metrics for Auto-scaling

| Metric | Scale Out When | Scale In When |
|--------|----------------|---------------|
| **CPU Utilization** | > 75% | < 30% |
| **Memory Usage** | > 80% | < 40% |
| **Request Count** | > threshold | < threshold |
| **Response Time** | > 500ms | < 100ms |
| **Queue Depth** | Growing | Empty |

---

[← Caching & CDN](04_CACHING_CDN.md) | [Tiếp: Security →](06_SECURITY.md)
