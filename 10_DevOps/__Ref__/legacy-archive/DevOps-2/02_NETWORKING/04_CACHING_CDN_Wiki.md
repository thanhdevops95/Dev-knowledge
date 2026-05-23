# 04. Caching & CDN

[← Load Balancing](03_LOAD_BALANCING.md) | [Tiếp: Availability →](05_AVAILABILITY.md)

---

# � Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Cache** | /kæʃ/ | Bộ nhớ đệm - Lưu trữ tạm thời dữ liệu để truy cập nhanh hơn |
| **Cache Hit** | - | Đúng cache - Dữ liệu được tìm thấy trong cache |
| **Cache Miss** | - | Trượt cache - Dữ liệu không có trong cache, phải lấy từ nguồn |
| **TTL** | - | Time To Live - Thời gian dữ liệu tồn tại trong cache trước khi hết hạn |
| **Eviction** | - | Loại bỏ - Xóa dữ liệu khỏi cache khi đầy |
| **LRU** | - | Least Recently Used - Loại bỏ dữ liệu ít được dùng gần đây nhất |
| **LFU** | - | Least Frequently Used - Loại bỏ dữ liệu ít được dùng nhất |
| **CDN** | /ˌsiːdiːˈen/ | Content Delivery Network - Mạng phân phối nội dung toàn cầu |
| **Edge Server** | - | Máy chủ biên - Máy chủ CDN gần người dùng nhất |
| **Origin Server** | - | Máy chủ gốc - Máy chủ chính chứa dữ liệu gốc |
| **Proxy** | /ˈprɒksi/ | Máy chủ trung gian giữa client và server |
| **Forward Proxy** | - | Proxy thuận - Đại diện cho client, ẩn danh tính client |
| **Reverse Proxy** | - | Proxy ngược - Đại diện cho server, ẩn danh tính server |
| **Redis** | /ˈredɪs/ | Cơ sở dữ liệu in-memory phổ biến dùng làm cache |

---

# 🤔 Tại sao DevOps cần biết Caching và CDN?

## Nỗi đau thực tế

> "Database bị quá tải vì mọi request đều truy vấn database"

> "Website chậm với user ở châu Á vì server đặt ở Mỹ"

> "Hóa đơn cloud tăng vọt vì bandwidth quá lớn"

## Kiến thức này giúp bạn

| Tình huống | Cần biết |
|------------|----------|
| Giảm tải cho database | Cache strategies (Write-through, Write-back) |
| Website nhanh hơn toàn cầu | CDN configuration |
| Debug "stale data" | Cache invalidation |
| Tiết kiệm chi phí bandwidth | CDN caching |
| Hiểu Nginx config | Reverse proxy |

Caching và CDN là hai trong những kỹ thuật quan trọng nhất để tối ưu performance. Một cache hit có thể nhanh hơn database query đến hàng trăm lần.

---

# 💾 Caching

## Caching là gì?

**Caching** là kỹ thuật **lưu trữ bản sao dữ liệu** ở vị trí có thể truy cập **nhanh hơn** so với nguồn gốc.

```
┌─────────────────────────────────────────────────────────────┐
│                     CACHING CONCEPT                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Without Cache:                                              │
│  Client ──────────────────────────► Database (100ms)        │
│                                                              │
│  With Cache:                                                 │
│  Client ───► Cache (1ms)                                    │
│              │                                               │
│              ├── Cache Hit: Return immediately              │
│              │                                               │
│              └── Cache Miss: Fetch from DB → Store → Return │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Cache Hit vs Cache Miss

| Scenario | Mô tả |
|----------|-------|
| **Cache Hit** | Data found in cache → return immediately |
| **Cache Miss** | Data NOT in cache → fetch from source |

### Hit Ratio

```
Hit Ratio = Cache Hits / (Cache Hits + Cache Misses)

Example: 950 hits, 50 misses → 95% hit ratio
```

**Targets:**

- **90%+**: Good
- **95%+**: Excellent
- **99%+**: Outstanding

---

## Cache Invalidation

Khi data thay đổi, cache cần được **invalidated** để avoid stale data.

### Write-Through

**Write to cache AND database simultaneously.**

```
Write Request
    ├───► Cache ───┐
    │              │ Both complete before success
    └───► Database ┘
```

| Pros | Cons |
|------|------|
| Data consistency | Higher write latency |
| No data loss | Write amplification |

### Write-Around

**Write directly to database, bypass cache.**

```
Write ───► Database only
Next Read → Cache Miss → Fetch → Update Cache
```

| Pros | Cons |
|------|------|
| No cache churn | Higher read latency for new data |

### Write-Back

**Write to cache first, database updated later (async).**

```
Write ───► Cache only (return success)
           └──► Async flush to Database
```

| Pros | Cons |
|------|------|
| Lowest write latency | Risk of data loss |
| Batch writes | More complex |

---

## Eviction Policies

Khi cache đầy, cần decide **data nào remove**.

### LRU (Least Recently Used)

Evict data **chưa access lâu nhất**.

```
Cache: [A, B, C, D] (D most recent)
Access B → [A, C, D, B]
New E → Evict A → [C, D, B, E]
```

### LFU (Least Frequently Used)

Evict data **access ít nhất**.

```
A: 10 accesses
B: 2 accesses  ← Evict
C: 15 accesses
```

### FIFO (First In, First Out)

Evict data **oldest** in cache.

### TTL (Time To Live)

Evict data **sau khi expired**.

```bash
SET user:123 "data" EX 3600  # expires in 1 hour
```

---

## Types of Caches

### Distributed Cache

Cache **shared across multiple nodes**.

```
┌───────────────┐
│   App Node 1  │───┐     ┌────────────────┐
└───────────────┘   ├────►│  Distributed   │
┌───────────────┐   │     │  Cache Cluster │
│   App Node 2  │───┘     └────────────────┘
└───────────────┘
```

**Examples:** Redis Cluster, Memcached

### Local Cache

Cache **on each application node**.

**Examples:** In-process cache, Caffeine (Java)

---

## Cache Pros and Cons

| Pros | Cons |
|------|------|
| ✅ Faster response | ❌ Stale data risk |
| ✅ Reduced DB load | ❌ Added complexity |
| ✅ Better UX | ❌ Memory cost |
| ✅ Cost savings | ❌ Cache invalidation hard |

---

## Examples

| Product | Mô tả |
|---------|-------|
| **Redis** | In-memory data store, most popular |
| **Memcached** | Simple key-value cache |
| **Varnish** | HTTP cache |

---

# 🌐 Content Delivery Network (CDN)

## CDN là gì?

**CDN** là một **geographically distributed group of servers** làm việc together để provide **fast delivery of Internet content**.

```
┌─────────────────────────────────────────────────────────────┐
│                    CDN DISTRIBUTION                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                    ┌────────────┐                            │
│                    │   Origin   │                            │
│                    │   Server   │                            │
│                    └─────┬──────┘                            │
│                          │                                   │
│         ┌────────────────┼────────────────┐                  │
│         ▼                ▼                ▼                  │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│   │CDN Edge  │    │CDN Edge  │    │CDN Edge  │              │
│   │(Europe)  │    │(Asia)    │    │(Americas)│              │
│   └──────────┘    └──────────┘    └──────────┘              │
│        ↓               ↓               ↓                     │
│     Users           Users           Users                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Benefits

| Benefit | Mô tả |
|---------|-------|
| **Performance** | Content served from nearby edge |
| **Reliability** | Multiple servers, DDoS protection |
| **Scalability** | Handle traffic spikes |
| **Cost** | Reduced bandwidth costs |

---

## Types

### Pull CDN

CDN **pulls content from origin on demand** (first request).

```
User request → CDN Edge
               ├── Cache miss
               └──► Pull from origin → Cache → Serve
```

### Push CDN

Content **pushed to CDN proactively** by origin.

```
Origin ───push───► CDN Edge (pre-populated)
```

| Type | Use case |
|------|----------|
| **Pull** | Most websites, dynamic content |
| **Push** | Large files, videos |

---

## Examples

- **Cloudflare**: Most popular, security features
- **AWS CloudFront**: Integrated with AWS
- **Akamai**: Enterprise, largest network
- **Fastly**: Developer-friendly

---

# 🔄 Proxy

## Proxy là gì?

**Proxy server** là **intermediary** sitting giữa client và backend server.

---

## Types

### Forward Proxy

Sits in front of **clients**.

```
Clients → Forward Proxy → Internet
         (hides clients)
```

**Use cases:**

- Hide client identity
- Content filtering
- Bypass restrictions

### Reverse Proxy

Sits in front of **servers**.

```
Internet → Reverse Proxy → Servers
          (hides servers)
```

**Use cases:**

- Load balancing
- SSL termination
- Caching
- Security

**Examples:** Nginx, HAProxy

---

## Forward vs Reverse

| Aspect | Forward | Reverse |
|--------|---------|---------|
| Protects | Clients | Servers |
| Hides | Client IP | Server IP |
| Example | Corporate proxy | Nginx |

---

[← Load Balancing](03_LOAD_BALANCING.md) | [Tiếp: Availability →](05_AVAILABILITY.md)
