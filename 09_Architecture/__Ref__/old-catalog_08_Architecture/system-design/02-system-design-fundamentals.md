# System Design Fundamentals

> **Tags:** `system-design` `scalability` `availability` `cap-theorem` `database` `caching`
> **Level:** Intermediate | **Prerequisite:** `networking/01-http-networking.md`

---

## 1. Scalability Patterns

### Vertical vs Horizontal Scaling

```
Vertical (Scale Up):              Horizontal (Scale Out):
  Server                           Server 1
  CPU: 8 → 32 cores                Server 2
  RAM: 16 → 128 GB                 Server 3
  
Pros: Simple, no code change      Pros: Linear scaling, no single point of failure
Cons: Limits, expensive, SPOF     Cons: Complexity, distributed systems problems
```

### Load Balancing Algorithms

```
Round Robin:      S1 → S2 → S3 → S1 → S2 → ...
Weighted RR:      S1(3) → S1 → S1 → S2(1) → S3(2) → S3 → ...
Least Connections: Route to server with fewest active connections
IP Hash:          hash(client_ip) % N servers → sticky sessions
Random:           Random server each request
```

### Stateful vs Stateless Services

```
Stateful (hard to scale):
  Client ─── Request ─── Server (has session state)
  Client must go back to SAME server → sticky sessions needed

Stateless (easy to scale):
  Client ─── Request ─── ANY Server (state stored externally: Redis, DB)
  Any server can handle any request → perfect for horizontal scaling
```

---

## 2. CAP Theorem

**In a distributed system, you can only guarantee 2 of 3:**

```
        C (Consistency)
       / \
      /   \
     /     \
    /       \
   A ─────── P
(Availability) (Partition Tolerance)

CA: Traditional RDBMS (single node — no partition)
CP: MongoDB, HBase, ZooKeeper — consistent even during partition (some requests fail)
AP: Cassandra, CouchDB, DynamoDB — available even during partition (may return stale data)
```

### PACELC Extension
Even without partition: tradeoff between Latency and Consistency.
`If Partition → A or C; Else → L or C`

- DynamoDB: PA/EL — Available during partition, Latency optimized normally
- BigTable: PC/EC — Consistent always, Latency may increase
- MySQL: PC/EC — Always consistent

---

## 3. Caching Strategies

```
┌────────────────────────────────────────────────┐
│                  Cache Patterns                 │
├────────────┬───────────────┬────────────────────┤
│  Cache-Aside │  Write-Through │  Write-Behind      │
│  (Lazy)     │               │  (Write-back)      │
└────────────┴───────────────┴────────────────────┘
```

### Cache-Aside (Lazy Loading)
```
Read:
  1. App checks cache
  2. If miss → query DB → write to cache → return
  3. If hit → return from cache

Write:
  1. Write to DB
  2. Invalidate (delete) cache entry

Pros: Only cache what's needed, cache failure doesn't break app
Cons: First request always slow (cold cache), potential stale data
```

### Write-Through
```
Write:
  1. Write to cache
  2. Write to DB synchronously

Read:
  1. Always check cache first (always warm)

Pros: Cache always consistent with DB
Cons: Write latency increased (2 writes), cache may have cold data never read
```

### Write-Behind (Write-Back)
```
Write:
  1. Write to cache
  2. Return OK immediately
  3. Async write to DB later (batch/delayed)

Pros: Lowest write latency
Cons: Data loss if cache fails before flush, complex implementation
```

### Cache Eviction Policies
- **LRU** (Least Recently Used): evict the least recently accessed item
- **LFU** (Least Frequently Used): evict the least frequently accessed item
- **TTL** (Time To Live): expire after fixed duration
- **FIFO**: evict oldest item first

---

## 4. Database Scaling

### Read Replicas
```
              ┌─── Read Replica 1
Writer ───────┤─── Read Replica 2    ← Handle 80-90% of traffic
(Primary)     └─── Read Replica 3

Replication lag: Typically <1s (async)
Use case: Analytics, reports, read-heavy workloads
Caveat: Reads might be slightly stale (replication lag)
```

### Database Sharding (Horizontal Partitioning)
```
Shard 1: users where user_id % 3 == 0  (users 0, 3, 6, ...)
Shard 2: users where user_id % 3 == 1  (users 1, 4, 7, ...)
Shard 3: users where user_id % 3 == 2  (users 2, 5, 8, ...)

Shard key options:
  - Range: user_id 1-1000 → Shard1, 1001-2000 → Shard2
  - Hash: hash(user_id) % N
  - Directory: lookup table maps key → shard
  - Geo: users in US → Shard1, EU → Shard2

Problems:
  - Joins across shards are expensive/impossible
  - Rebalancing when adding shards
  - Hot spots (if shard key poorly chosen)
```

### CQRS — Command Query Responsibility Segregation
```
Commands (writes):
  Client → Command Handler → Write DB (optimized for writes)
            └─ emits events → Event Bus

Queries (reads):
  Client → Query Handler → Read DB (optimized for reads, denormalized)
                           ↑ Updated by Event Bus
```

---

## 5. Message Queues & Async Processing

```
Synchronous:                     Asynchronous:
  Client ─── Request ───▶ API      Client ─── Request ───▶ API
  Client ◀── Response ──── API       └── puts job in Queue
  (blocks until done)               API ─── 202 Accepted
                                    Worker consumes queue → does work
                                    Worker notifies client (webhook/polling)
```

### Queue Patterns

**Work Queue (Competing Consumers)**:
```
Producer → [Queue] → Consumer 1
                  → Consumer 2
                  → Consumer 3
Each message processed ONCE by ONE consumer
Use case: Email notifications, image processing, payments
```

**Pub/Sub (Fan-out)**:
```
Publisher → Topic → Subscriber 1
                  → Subscriber 2
                  → Subscriber 3
Each subscriber gets EVERY message
Use case: Event broadcasting, real-time updates
```

---

## 6. Rate Limiting Algorithms

### Token Bucket
```python
class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity      # Max tokens
        self.tokens = capacity        # Current tokens
        self.refill_rate = refill_rate  # tokens/second
        self.last_refill = time.time()

    def consume(self, tokens: int = 1) -> bool:
        now = time.time()
        # Refill tokens based on elapsed time
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True   # Allowed
        return False      # Rate limited

# Pros: Allows bursts (up to capacity), smooth rate
# Use: Most APIs (100 requests/minute, burst to 20)
```

### Sliding Window Log
```
Keep log of request timestamps
On each request: remove timestamps older than window
If log size < limit → allow, add timestamp

Pros: Accurate
Cons: Memory intensive (store all timestamps)
```

### Fixed Window Counter
```
Count requests in current time window (e.g., 1 minute)
If count < limit → allow, increment
Reset counter at window boundary

Cons: Burst at window boundary (200% rate for 2 seconds)
```

---

## 7. Consistent Hashing

Problem: Normal hash `hash(key) % N` — when N changes (add/remove server), most keys remapped.

**Consistent Hashing**: arrange servers and keys on a circle, key goes to next clockwise server:

```
        0 (Key A: 10)
       / \
      /   \
  300     Server 1 (at position 50)
  (Key D) /
    \   /
     \ /
    250  Key B: 150 → Server 2
         Server 2 (at position 100)
         
Adding Server 4: only keys between prev server and Server 4 move
Removing Server 2: only its keys move to next server
```

**Virtual nodes**: each server has multiple points on the circle → better balance:
```
Server 1: positions 50, 150, 250 (3 virtual nodes)
Server 2: positions 75, 175, 300
```

Used by: Cassandra, DynamoDB, Redis Cluster, CDNs

---

## 8. Content Delivery Network (CDN)

```
Without CDN:
  User in Vietnam ─── 150ms ──▶ Origin server in US

With CDN:
  User in Vietnam ─── 5ms ──▶ CDN PoP in Singapore
                                    ↑
                              Origin server in US
                              (consulted only on cache miss)
```

### CDN Caching Strategy
```nginx
# Cache static assets for 1 year (with cache-busting via filename hash)
Cache-Control: public, max-age=31536000, immutable
# File: /static/app.abc123.js  ← hash changes when file changes

# API responses: shorter TTL
Cache-Control: public, max-age=60, stale-while-revalidate=300

# Private data: no CDN caching
Cache-Control: private, no-store
```

---

## 9. Reliability Patterns

### Circuit Breaker
```
States:
  CLOSED → requests pass through, count failures
  OPEN → fail fast, no requests to service (after N failures)
  HALF-OPEN → allow 1 request to test if service recovered

         failures > threshold        success
CLOSED ──────────────────────▶ OPEN ──────────▶ HALF-OPEN
                                                     │
CLOSED ◀─────────────────────────────────────────────┘
                    success
```

```python
# Simplified circuit breaker
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = "CLOSED"
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF-OPEN"
            else:
                raise CircuitOpenError("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
```

### Bulkhead Pattern
```
Without bulkhead: one slow service exhausts thread pool → all services fail
With bulkhead: each service has its own thread pool / semaphore

Thread Pool Bulkhead:
  User Service:    10 threads
  Payment Service: 20 threads
  Email Service:    5 threads
  
  Even if Email is slow/down, User and Payment unaffected
```

### Retry with Exponential Backoff
```python
import random
import time

def retry_with_backoff(func, max_retries=3, base_delay=1.0, max_delay=60.0):
    for attempt in range(max_retries + 1):
        try:
            return func()
        except (ConnectionError, TimeoutError) as e:
            if attempt == max_retries:
                raise
            
            # Exponential backoff with jitter
            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0, delay * 0.1)  # ±10% jitter
            time.sleep(delay + jitter)
```

---

## 10. System Design Framework (Interview)

```
1. Clarify Requirements (5 min)
   - Functional: What features? [core + nice-to-have]
   - Non-functional: scale, latency, availability, consistency
   - Constraints: traffic (RPS), data size, users

2. Estimation (3 min)
   - DAU (Daily Active Users)
   - Read:Write ratio
   - Storage: X objects × Y bytes × Z years
   - Bandwidth: requests/s × avg response size

3. High-Level Design (10 min)
   - Main components: Client, Load Balancer, App Servers, DB, Cache, CDN
   - Data flow for primary use cases
   - API design (major endpoints)

4. Deep Dive (15 min)
   - Database schema
   - Caching strategy
   - Scalability: how to handle 10x traffic
   - Reliability: failure scenarios

5. Trade-offs & Discussion (5 min)
   - What you'd do differently at 100x scale
   - Monitoring & alerting plan
   - Security considerations
```

### Quick Reference Numbers
```
Latency:
  L1 cache: 1ns
  RAM: 100ns
  SSD: 100μs
  Network (same DC): 0.5ms
  Network (NYC→CA): 40ms
  Network (NYC→EU): 100ms

Throughput:
  Single MySQL (reads):  100K QPS
  Redis:                 1M ops/s
  Kafka:                 1M msgs/s
  Network (1Gbps):       125 MB/s

Storage:
  1 photo: 300KB
  1 video (1min): 50MB
  1B users × 1 photo/day: 300TB/day
```

---

*Tài liệu liên quan: `system-design/02-design-patterns.md` | `system-design/03-microservices.md` | `system-design/05-distributed-systems.md`*
