# 🌐 Distributed Systems — Hệ thống phân tán

> `[ADVANCED]` — Hiểu thách thức khi hệ thống chạy trên nhiều máy

---

## Tại sao cần Distributed Systems?

Khi 1 server không đủ:
- **Scale**: 1 triệu users → 1 server không handle nổi
- **Reliability**: Server chết → hệ thống chết
- **Latency**: User ở Việt Nam, server ở US → 200ms network latency

Distributed system giải quyết bằng cách chạy trên **nhiều máy**. Nhưng nhiều máy = nhiều vấn đề mới.

---

## 1. CAP Theorem — Giới hạn vật lý

```
Trong hệ thống phân tán, bạn CHỈ ĐƯỢC CHỌN 2/3:

C — Consistency:    Mọi node đọc cùng data tại cùng thời điểm
A — Availability:   Mọi request đều nhận response (không timeout)
P — Partition Tolerance: Hệ thống chạy khi network giữa nodes bị đứt

┌───────────────┐
│       C       │
│   ┌───────┐   │
│   │  CA   │   │     CA: Single-node DB (PostgreSQL single)
│   └───┬───┘   │         → Không thể partition tolerant
│       │       │
│  ┌────┴────┐  │
│  │   CP    │  │     CP: MongoDB (strong consistency), HBase
│  └────┬────┘  │         → Có thể unavailable khi partition
│       │       │
└───────┤───────┘
        │
   ┌────┴────┐
   │   AP    │        AP: Cassandra, DynamoDB, CouchDB
   └─────────┘            → Eventual consistency khi partition

Thực tế: P LUÔN xảy ra (network LUÔN có thể fail).
→ Bạn chọn giữa CP (consistency over availability)
  hoặc AP (availability over consistency).
```

**Ví dụ thực tế:**
- **Banking (CP)**: Thà chờ lâu hơn là số dư sai. Consistency quan trọng.
- **Social media feed (AP)**: Ai đó chưa thấy post mới 5 giây? OK. Availability quan trọng.

---

## 2. Consistency Models

### Strong Consistency

Sau khi write thành công, TẤT CẢ reads đều thấy giá trị mới:

```
Client write: x = 5
→ ALL replicas updated
→ Client read from ANY replica: x = 5 ✅

Cost: Chậm hơn (phải chờ tất cả replicas confirm).
Use: Financial transactions, inventory count.
```

### Eventual Consistency

Sau khi write, replicas sẽ **eventually** converge. Tạm thời có thể đọc được giá trị cũ:

```
Client write: x = 5 (to replica A)
→ Replica A: x = 5
→ Replica B: x = 3 (chưa update)   ← Stale read!
→ (vài ms-giây sau) Replica B: x = 5 ✅

Cost: Nhanh hơn, available hơn.
Use: Social feeds, analytics, shopping cart.
```

### Read-Your-Writes Consistency

User luôn thấy data **mình vừa write**, dù replicas chưa sync:

```
User update profile → Read profile ngay → Thấy data mới ✅
Người khác read → Có thể thấy data cũ (chấp nhận được)

Implementation: Read from same replica mà user vừa write vào.
Hoặc: Read from leader, write to leader.
```

---

## 3. Replication — Sao chép data

### Leader-Follower (Primary-Replica)

```
             Writes
Client ───────────────► Leader (Primary)
                           │
                    Replicate (async)
                    ┌──────┼──────┐
                    ▼      ▼      ▼
                 Follower Follower Follower
                    │      │      │
Client ◄────────────┤      │      │  Reads (load balanced)
Client ◄───────────────────┤      │
Client ◄──────────────────────────┤
```

**Trade-off**: Write đều vào leader (bottleneck), reads scale ra followers. Nếu leader chết → cần failover (election) → brief downtime.

### Multi-Leader

```
Cho phép write vào nhiều leaders (multi-region):

US Region:   Leader ←→ Leader    EU Region
              ↓                    ↓
           Followers            Followers

Problem: Write conflict! 
  US: update name = "An" (cùng lúc)
  EU: update name = "Bình" (cùng lúc)
  → Name = "An" hay "Bình"?

Resolution: Last-write-wins, merge, hoặc custom logic.
```

---

## 4. Consensus — Các node đồng ý với nhau

Khi nodes cần **đồng ý 1 giá trị** (ai là leader? transaction commit?), cần consensus algorithms:

```
Raft Algorithm (simplified):
  1. Nodes bầu 1 Leader
  2. Client gửi write → Leader
  3. Leader replicate → Followers
  4. Khi MAJORITY (>50%) confirm → COMMIT
  5. Leader chết → followers bầu leader mới

Tại sao majority?
  5 nodes, 3 confirm = committed
  Nếu 2 nodes chết → 3 còn lại vẫn có committed data
  → Consistency + Fault tolerance!
```

---

## 5. Distributed Patterns thực tế

### Consistent Hashing — Phân data đều

```
Problem: 3 servers, hash(key) % 3 = server index
  Thêm 1 server → hash(key) % 4 → HẦU HẾT keys đổi server → massive redistribution!

Consistent Hashing:
  Servers và keys đều placed trên VÒNG TRÒN hash
  Key → di theo chiều kim đồng hồ → gặp server nào thì thuộc server đó

  Thêm/bớt 1 server → chỉ di chuyển keys GIỮA 2 servers lân cận
  → Minimal redistribution!

Used by: Redis Cluster, DynamoDB, Cassandra
```

### Circuit Breaker — Chống cascading failure

Khi 1 service downstream chết, nếu tiếp tục gửi requests → tất cả threads bị block → toàn hệ thống chết theo (cascading failure):

```typescript
// Circuit Breaker states:
// CLOSED → requests pass through normally
// OPEN   → requests fail immediately (không gọi downstream)
// HALF-OPEN → thử 1 request, nếu OK → closed, nếu fail → open

class CircuitBreaker {
    private failures = 0;
    private state: 'closed' | 'open' | 'half-open' = 'closed';
    private lastFailure: Date | null = null;

    constructor(
        private threshold: number = 5,     // 5 failures → open
        private timeout: number = 30000,    // 30s → try again
    ) {}

    async call<T>(fn: () => Promise<T>): Promise<T> {
        if (this.state === 'open') {
            if (Date.now() - this.lastFailure!.getTime() > this.timeout) {
                this.state = 'half-open';
            } else {
                throw new Error('Circuit is OPEN — service unavailable');
            }
        }

        try {
            const result = await fn();
            this.onSuccess();
            return result;
        } catch (err) {
            this.onFailure();
            throw err;
        }
    }

    private onSuccess() {
        this.failures = 0;
        this.state = 'closed';
    }

    private onFailure() {
        this.failures++;
        this.lastFailure = new Date();
        if (this.failures >= this.threshold) {
            this.state = 'open';
            console.warn(`Circuit OPENED after ${this.failures} failures`);
        }
    }
}

// Usage
const paymentBreaker = new CircuitBreaker(5, 30000);

async function processPayment(order) {
    return paymentBreaker.call(() =>
        fetch('https://payment-service/charge', { body: order })
    );
}
```

---

## 6. Fallacies of Distributed Computing

**8 giả định SAI** mà developer thường mắc:

```
1. Network là reliable          → Packets bị drop, timeout xảy ra!
2. Latency = zero               → Cross-region: 50-200ms mỗi call
3. Bandwidth vô hạn            → Gửi 1GB qua network ≠ đọc từ disk
4. Network là secure            → MITM, packet sniffing
5. Topology không thay đổi      → Servers up/down liên tục
6. Có 1 admin duy nhất         → Nhiều teams, nhiều cloud providers
7. Transport cost = zero        → Data transfer tốn tiền!
8. Network là homogeneous       → Đủ loại hardware, OS, versions
```

---

## Bài tập thực hành

- [ ] Simulate: 2 replicas, eventual consistency (viết vào A, đọc từ B)
- [ ] Circuit Breaker: implement + test với flaky service
- [ ] CAP: phân tích 3 systems bạn dùng → CP hay AP?
- [ ] Đọc: "Designing Data-Intensive Applications" Chapter 5-9

---

## Tài nguyên thêm

- [Designing Data-Intensive Applications](https://dataintensive.net/) — Martin Kleppmann (THE book)
- [System Design Primer](https://github.com/donnemartin/system-design-primer) — Free
- [Jepsen](https://jepsen.io/) — Database consistency testing
