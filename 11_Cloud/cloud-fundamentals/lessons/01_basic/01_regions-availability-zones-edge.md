# 🎓 Regions, Availability Zones, Edge — Geographic distribution

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~17 phút\
> **Prerequisites:** [00_what-is-cloud-computing.md](00_what-is-cloud-computing.md), [Networking basics](../../../../05_Networking/)

> 🎯 *Cloud không phải "1 server lớn". Là hàng trăm **datacenter** ở 30+ **region** worldwide. Bài này dạy: **Region**, **AZ**, **Edge**, **CDN**, **latency** decision, **redundancy tiers**, chọn region đúng + multi-region patterns.*

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **Region** vs **Availability Zone** vs **Edge location**
- [ ] Hiểu **latency**: physical distance + network hops + serialization
- [ ] **CDN**: Cloudflare, CloudFront, Fastly — khi nào dùng
- [ ] **Redundancy tiers**: Single AZ → Multi-AZ → Multi-region → Multi-cloud
- [ ] Pick **right region** based on customer location + compliance + cost
- [ ] **Multi-region patterns**: active-passive, active-active, geo-routed
- [ ] **Data residency** + GDPR

---

## Tình huống — Customer Vietnam, app deploy us-east-1

Startup deploy FastAPI on AWS, region `us-east-1` (default Virginia).

Customers Vietnam complain:
- Page load 3-5 seconds (vs 800ms cho US customer).
- Mobile users churn.
- Conversion rate Vietnam 1/3 US rate.

Reason: **Vietnam → Virginia network latency**:
- ICMP ping: ~250-350ms.
- TCP handshake: 3 round trips = ~1 second.
- TLS handshake: +2 round trips = ~1.5 sec.
- HTTP request: +1 round trip.
- **Total before app responds**: ~2 seconds for any request.

Sếp: *"Cần deploy region gần users + CDN cho static assets. Bài này dạy."*

---

## 1️⃣ Region — Geographic distribution

### Definition

**Region** = geographic cluster of datacenters trong cùng country/area.

Cloud vendors có Regions:
- **AWS**: 32+ regions 2026 (us-east-1, eu-west-1, ap-southeast-1, etc.).
- **GCP**: 40+ regions.
- **Azure**: 60+ regions.
- **DigitalOcean**: 15 regions.
- **Cloudflare**: 300+ cities (edge, not regions per se).

### Naming convention

AWS:
- `us-east-1` = US East (N. Virginia)
- `us-west-2` = US West (Oregon)
- `eu-west-1` = Europe (Ireland)
- `ap-southeast-1` = Asia Pacific (Singapore)
- `ap-southeast-2` = Asia Pacific (Sydney)
- `ap-northeast-1` = Asia Pacific (Tokyo)
- `sa-east-1` = South America (São Paulo)

GCP:
- `us-central1` = Iowa
- `europe-west1` = Belgium
- `asia-southeast1` = Singapore

Azure:
- `eastus` = Virginia
- `westeurope` = Netherlands
- `southeastasia` = Singapore

### Region structure

```
Region (e.g., ap-southeast-1 Singapore)
├── AZ-a (datacenter 1)
├── AZ-b (datacenter 2)
├── AZ-c (datacenter 3)
└── Edge locations nearby
```

→ Each region = **multiple datacenters** (AZs) within ~100km, connected by high-speed fiber.

### Region capabilities

Not all services in all regions. Newest regions = fewer services.

```bash
# AWS — services per region
aws ec2 describe-regions --query "Regions[?RegionName=='ap-southeast-1']"
# Then check service availability:
# https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/
```

→ Pick region with services you need.

🪞 **Ẩn dụ**: *Region như **bưu cục thành phố**. Singapore region = bưu cục Singapore. Mỗi region có nhiều datacenter (AZ) như nhiều phòng trong bưu cục. Customers gần region nào → giao hàng nhanh region đó.*

---

## 2️⃣ Availability Zone (AZ)

### Definition

**AZ** = isolated datacenter trong region. Independent power, cooling, networking.

```
Region: us-east-1
├── AZ us-east-1a (~100MW power, separate building)
├── AZ us-east-1b
├── AZ us-east-1c
├── AZ us-east-1d
├── AZ us-east-1e
└── AZ us-east-1f
```

→ 6 AZs in `us-east-1`. Each ~10-30km apart.

### Why multiple AZs?

**Failure isolation**:
- AZ-a fire → AZ-b, AZ-c unaffected.
- Power outage AZ-a → other AZs still serve.

**Deploy 1 AZ vs Multi-AZ**:
- **Single-AZ**: 1 datacenter, cheaper, but SPOF.
- **Multi-AZ**: spread across AZs, automatic failover.

### Multi-AZ pattern

```
Load Balancer (multi-AZ)
    ├── EC2 in AZ-a
    ├── EC2 in AZ-b
    └── EC2 in AZ-c

RDS Multi-AZ:
    ├── Primary in AZ-a
    └── Standby in AZ-b (synchronous replication)
       (failover automatic if AZ-a down)
```

→ AZ-a fail → LB stop sending traffic to AZ-a, RDS promote AZ-b. Recovery 60-120 seconds.

### AZ ID vs AZ name

⚠️ **Trap**: AZ name (`us-east-1a`) maps differently per account.

- Your account: `us-east-1a` = physical zone X.
- Friend's account: `us-east-1a` = physical zone Y.

→ AWS does this for **load balancing** new accounts.

**Solution**: use **AZ ID** (e.g., `use1-az1`) for cross-account consistency.

```bash
aws ec2 describe-availability-zones --region us-east-1
# Names + IDs
```

### Cross-AZ data transfer cost

⚠️ AWS charges **$0.01/GB** for cross-AZ traffic.

- 100GB/day cross-AZ = $30/month per service.
- Multi-AZ database with replication: + cross-AZ cost.

→ Balance: redundancy (multi-AZ) vs cost (single-AZ).

---

## 3️⃣ Edge locations + CDN

### Edge locations

**Edge location** = small datacenter close to users, hosting **CDN** + sometimes compute.

```
                        Region us-east-1
                              ┃
                      ┏━━━━━━━┻━━━━━━━┓
                      ┃   Internet     ┃
                      ┗━━━━━━┳━━━━━━━━┛
            ┌─────────────────┼─────────────────┐
       Edge Singapore     Edge Tokyo        Edge Sydney
       (cache + compute)  (cache + compute) (cache + compute)
            ↑                  ↑                  ↑
       User Vietnam       User Japan         User Australia
       (50ms latency)     (10ms latency)     (15ms latency)
```

→ User → Edge (close) → if cache miss, Edge → Region (far). Most requests hit edge.

### CDN — Content Delivery Network

**Use case**: static assets (images, JS, CSS, fonts, videos).

**Vendors 2026**:
- **Cloudflare**: market leader, 300+ cities, free tier.
- **AWS CloudFront**: integrated with AWS, complex pricing.
- **Fastly**: developer-focused, fast cache invalidation.
- **Akamai**: enterprise/media legacy.
- **Bunny.net**: cheap, growing.
- **Google Cloud CDN**: GCP-native.

### How CDN works

```
User browser → DNS resolve www.acmeshop.vn → CDN node (closest)
                                              ↓
                                              Has cache?
                                              ├── YES → return immediately
                                              └── NO → fetch from origin
                                                       ↓
                                                       Cache at edge
                                                       ↓
                                                       Return to user
```

### CDN cost saving

100K users, each load 10MB image:
- **Without CDN**: 1TB/month from origin = $90 egress (AWS).
- **With CDN**: 1TB at CDN (cheaper), 50GB at origin (cache miss) = $5 egress + CDN cost.

→ CDN reduces origin load + bandwidth cost.

### Edge compute (advanced)

2018+: edge locations run **compute**, not just cache.

- **Cloudflare Workers**: V8 isolates, fast startup, JS/TS/Rust.
- **AWS Lambda@Edge**: Lambda functions at CloudFront edge.
- **Fastly Compute@Edge**: Rust WebAssembly.
- **Deno Deploy**: V8-based.

Use cases:
- **A/B testing routing** (50% users → variant A).
- **Bot protection** (block at edge).
- **Header rewriting**.
- **Geolocation routing**.
- **Authentication at edge** (verify JWT before reaching origin).

```javascript
// Cloudflare Worker
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const country = request.cf.country;     // user country
  
  if (country === 'CN') {
    return new Response('Sorry, not available', { status: 451 });
  }
  
  // Cache headers
  const response = await fetch(request);
  response.headers.set('Cache-Control', 'public, max-age=3600');
  return response;
}
```

→ Code runs at edge near user. Latency 10-50ms vs 200ms+ for origin.

---

## 4️⃣ Latency: physics + network

### Speed of light limit

Vacuum speed of light = 300,000 km/s. **Fiber optic = ~200,000 km/s** (slower).

| Distance | Min latency (one-way) |
|---|---|
| Hanoi → Ho Chi Minh City (1100 km) | ~5.5ms |
| Hanoi → Singapore (3000 km) | ~15ms |
| Hanoi → Tokyo (3700 km) | ~18ms |
| Hanoi → Frankfurt (8800 km) | ~44ms |
| Hanoi → New York (13000 km) | ~65ms |

**Round-trip** = 2x one-way + network hops + processing.

### Network reality

Real latency:
- Vietnam → us-east-1: **~200-280ms RTT**.
- Vietnam → ap-southeast-1 (Singapore): **~50-80ms RTT**.
- Vietnam → ap-southeast-3 (Jakarta): **~40-60ms RTT**.

→ Pick region close to users. Singapore best for SEA, Tokyo for Japan/Korea.

### TCP / TLS handshake amplifies

```
TCP connect:    3 packets = 1 RTT  → 200ms
TLS handshake:  2 RTTs            → 400ms more
HTTP request:   1 RTT             → 200ms more
                                  ────────────
First request total:              ~800ms-1s
```

→ One slow request can ruin UX. **Latency budget** for good UX = < 500ms total.

### Latency improvement tactics

| Tactic | Saving |
|---|---|
| **Pick close region** | 80% latency reduction |
| **CDN for static** | 90% on cache hit |
| **HTTP/2** (multiplexing) | reduce TLS handshakes |
| **HTTP/3 over QUIC** | 1 RTT setup vs 3 |
| **Connection pooling** | save TCP/TLS per request |
| **Edge compute** | run logic at edge |
| **Pre-warm DNS** | save DNS lookup |
| **Compression** (Brotli) | reduce payload size |

---

## 5️⃣ Choose right region

### Decision factors

1. **Customer location**: where most users are.
2. **Compliance**: data residency requirements (EU = EU region, China = China cloud).
3. **Service availability**: newer regions miss some services.
4. **Cost**: pricing varies (us-east-1 cheapest, mainland China + GovCloud expensive).
5. **Latency to dependencies**: if app uses Stripe (US), think about cross-region latency.
6. **Disaster recovery**: pick DR region far enough (different earthquake zone).

### Geographic clusters

| Cluster | Primary regions |
|---|---|
| **North America** | us-east-1 (Virginia), us-west-2 (Oregon), ca-central-1 (Canada) |
| **Europe** | eu-west-1 (Ireland), eu-central-1 (Frankfurt), eu-north-1 (Stockholm) |
| **Asia Pacific** | ap-southeast-1 (Singapore), ap-northeast-1 (Tokyo), ap-south-1 (Mumbai), ap-southeast-2 (Sydney) |
| **China** | cn-north-1 (Beijing — AWS China, separate account) |
| **South America** | sa-east-1 (São Paulo) |
| **Middle East** | me-south-1 (Bahrain), me-central-1 (UAE) |
| **Africa** | af-south-1 (Cape Town) |

### For Vietnam-based startup

Recommendations:
1. **ap-southeast-1 (Singapore)**: closest, mature region, all services.
2. **ap-southeast-3 (Jakarta)**: closer but newer (some services missing).
3. **ap-east-1 (Hong Kong)**: closer to North Vietnam.

→ **Singapore is default** for Vietnam. Backup: Tokyo or Sydney.

### Cost comparison (relative)

| Region | Index |
|---|---|
| us-east-1 | 1.00 (cheapest base) |
| us-west-2 | 1.05 |
| eu-west-1 | 1.10 |
| ap-southeast-1 | 1.15 |
| ap-northeast-1 | 1.20 |
| Sydney, Brazil | 1.30 |
| Mainland China | 1.40 |
| GovCloud | 1.50 |

→ Building from scratch in US? `us-east-1` cheapest. Vietnamese startup? `ap-southeast-1` (extra cost worth latency).

---

## 6️⃣ Multi-region patterns

### When multi-region

- **Global user base**: serve users worldwide with low latency.
- **Disaster recovery**: regional outage failover.
- **Compliance**: data residency per region (EU data in EU).
- **HA tier-1**: 99.99%+ SLA.

### Pattern 1: Single-region, multi-AZ (most common)

```
Region us-east-1
    ├── AZ-a  (active)
    ├── AZ-b  (active)
    └── AZ-c  (active)
Users from anywhere → us-east-1 → distributed across AZs
```

**Pros**: simple, sufficient for 99.9% SLA.
**Cons**: regional outage = full outage. Latency for far users.

### Pattern 2: Multi-region active-passive

```
Region us-east-1 (active)    Region eu-west-1 (passive)
    ├── EC2 fleet                ├── EC2 fleet (stopped)
    ├── RDS primary  ──repl──→    ├── RDS read replica
    └── S3 (cross-region rep) ─→  └── S3 backup
                ↑
        DNS routes 100% users to us-east-1
        
If us-east-1 down → switch DNS → eu-west-1
```

**Pros**: DR ready, simpler than active-active.
**Cons**: paying for idle DR capacity, slower failover (5-10 min DNS).

### Pattern 3: Multi-region active-active

```
Region us-east-1                 Region eu-west-1
    ├── EC2 fleet (active)            ├── EC2 fleet (active)
    ├── RDS read+write                ├── RDS read+write
    └── S3                            └── S3
                ↑                          ↑
        Route53 latency routing
        US users → us-east-1, EU users → eu-west-1
```

**Pros**: 
- Lowest global latency.
- Active capacity DR.
- Geographic compliance.

**Cons**:
- **Database consistency hard**: writes in 2 regions → conflict.
- Complex cache invalidation.
- 2x cost.

**Database solutions**:
- **Aurora Global Database** (AWS): one region writer, others readers, < 1s replication.
- **Spanner** (GCP): truly global DB with consistency.
- **CockroachDB**: distributed SQL, multi-region.
- **DynamoDB Global Tables**: eventually consistent across regions.

### Pattern 4: Geo-routed (per-region tenant)

```
US users → us-east-1 (separate DB)
EU users → eu-west-1 (separate DB)
APAC users → ap-southeast-1 (separate DB)
```

Each region serves only its own users, isolated.

**Pros**: simplest multi-region. Compliance built-in.
**Cons**: users can't share data across regions easily.

**Best for**: SaaS with tenant-per-region, e.g., B2B platform.

---

## 7️⃣ Data residency + GDPR

### Data residency

**Some countries require data physically stay within country**:
- **EU GDPR**: EU citizen data must be processed under GDPR-compliant rules.
- **Russia**: personal data must be in Russia (Federal Law 242).
- **China**: data on Chinese citizens must be in China (Cybersecurity Law).
- **India**: certain financial data must be in India.
- **Brazil LGPD**: similar to GDPR.

→ Pick region within country.

### GDPR practical

For EU customers:
- Deploy in **eu-west-1**, **eu-central-1**, **eu-north-1**, etc.
- DPA (Data Processing Agreement) with vendor.
- Right to erasure (delete user data on request).
- Data breach notification 72 hours.
- DPO (Data Protection Officer) if processing > certain threshold.

### Schrems II (EU-US data transfer)

2020 EU court ruling: US cloud companies subject to US surveillance (CLOUD Act) → EU data in US risk.

**Mitigation**:
- Store EU data **physically in EU region**.
- Encrypt data, vendor doesn't have keys (BYOK / Customer-managed keys).
- Use EU-only vendors (OVH, Hetzner, Scaleway) for strict cases.

→ For EU customers: AWS eu-west-1 (Ireland) + KMS encryption + data classification.

---

## 8️⃣ Reliability tiers — How much redundancy needed?

### Tiers

| SLA target | Pattern | Downtime/month |
|---|---|---|
| **99% (2 nines)** | Single AZ, single instance | 7h 18m |
| **99.5%** | Single AZ, 2+ instances + LB | 3h 39m |
| **99.9% (3 nines)** | Multi-AZ (3+ AZs) | 43m 12s |
| **99.95%** | Multi-AZ + RDS Multi-AZ + S3 cross-region | 21m 36s |
| **99.99% (4 nines)** | Multi-region active-passive | 4m 19s |
| **99.999% (5 nines)** | Multi-region active-active + extensive DR drills | 25.9s |

### Cost vs reliability

```
Cost
 │
 │                            ╱  99.999%
 │                          ╱
 │                        ╱  99.99%
 │                      ╱
 │                ────╱  99.9%
 │       ────╱
 │  ────╱
 │ ╱  99%
 └──────────────────────────────► Availability
```

→ Each "9" = ~10x cost. Most apps: 99.9% sweet spot.

### Pick tier strategically

| Service | Recommend |
|---|---|
| Internal tool | 99% (single AZ) |
| Marketing site | 99.5% (CDN handles) |
| B2B SaaS | 99.9% (multi-AZ) |
| E-commerce | 99.95% (multi-AZ + RDS Multi-AZ) |
| Payment processing | 99.99% (multi-region) |
| Banking, healthcare | 99.99%+ (multi-region active-active) |
| Telco, life-critical | 99.999%+ (custom infra) |

---

## 9️⃣ Hands-on: Pick region for Vietnamese startup

### Scenario

- **App**: FastAPI + React e-commerce.
- **Customers**: 90% Vietnam, 10% Singapore.
- **Compliance**: not strict (no PCI yet).
- **Budget**: tight.

### Decision

**Primary region**: `ap-southeast-1` (Singapore).
- Closest to Vietnam (50-80ms latency).
- Mature region, all services.
- Singapore compliance friendly to Vietnam.

**AZ strategy**: Multi-AZ (3 AZs).
- LB + EC2 across 3 AZs.
- RDS Multi-AZ (failover automatic).

**CDN**: Cloudflare (free tier — generous).
- Cache static assets globally.
- Vietnam users hit Singapore edge (still ~50ms).

**Cost estimate**:
- 3x t3.medium EC2: $90/month.
- RDS Multi-AZ db.t3.medium: $80/month.
- S3 + bandwidth: $30/month.
- Cloudflare free: $0.
- Total: ~$200/month.

### Setup

```bash
# AWS CLI
aws configure
# region: ap-southeast-1

# Create VPC across 3 AZs
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --region ap-southeast-1

# (Bài 02 networking will deep dive)
```

### Test latency

```bash
# From Vietnam
ping ec2.ap-southeast-1.amazonaws.com
# 50-80ms

# Vs us-east-1
ping ec2.us-east-1.amazonaws.com
# 200-280ms
```

→ Singapore is 4x faster from Vietnam. Worth ~15% extra cost.

### Future: expand to Tokyo, Mumbai?

Once 10K+ users across regions:
- Add Tokyo (ap-northeast-1) for Japan/Korea.
- Mumbai (ap-south-1) for India.
- Multi-region active-passive with Aurora Global Database.

→ Plan for growth, not over-engineer day 1.

---

## 💡 Pitfall & Best practice

### ❌ Pitfall: Default region `us-east-1` cho non-US users

→ Most AWS examples use `us-east-1`. Vietnamese dev copy-paste → high latency.

→ **Fix**: explicit region per project. CLI default in `~/.aws/config`.

### ❌ Pitfall: Single AZ deploy for "saving cost"

→ AZ outage = full outage. SLA broken.

→ **Fix**: Multi-AZ even for staging. Cost diff small, reliability huge.

### ❌ Pitfall: AZ name assumed consistent

```yaml
# Hardcoded
availability_zone: us-east-1a
```

→ "1a" different physical AZ per account.

→ **Fix**: Use AZ ID (`use1-az1`) or query dynamically:
```bash
aws ec2 describe-availability-zones --filters Name=zone-id,Values=use1-az1
```

### ❌ Pitfall: Cross-AZ traffic surprise

→ Architecture: app in AZ-a, cache in AZ-b → every request cross-AZ → $$$ data transfer.

→ **Fix**: Co-locate dependent services in same AZ when possible, OR design to be AZ-aware.

### ❌ Pitfall: CDN without cache strategy

```
Cache-Control: no-cache
```

→ CDN useless, every request hits origin.

→ **Fix**: Cache headers per asset type:
- Images/CSS/JS: `Cache-Control: public, max-age=31536000, immutable` (1 year).
- HTML: `Cache-Control: public, max-age=60` (short).
- API: `Cache-Control: no-cache` (correct).

### ❌ Pitfall: Multi-region without database consistency plan

→ Write region A, read region B → not yet replicated → stale data → user confusion.

→ **Fix**: Choose consistency model:
- Eventual (DynamoDB Global Tables): OK for non-critical.
- Strong (Spanner, Aurora Global writer-reader): for financial.
- App-level handling (e.g., user always reads from write region).

### ❌ Pitfall: No DR drill

→ Setup multi-region active-passive. Never tested failover. Real disaster → procedure broken.

→ **Fix**: Quarterly DR drill. Document procedure. Test full failover in staging.

### ❌ Pitfall: Schrems II ignored for EU data

→ EU customer data in us-east-1. GDPR audit fails. Fines.

→ **Fix**: Map data by jurisdiction. EU data in EU region. DPA contracts in order.

### ✅ Best practice: Edge compute for global API

```
Pattern: Cloudflare Worker entry point
    ├── Static (HTML/CSS/JS): cache at edge
    ├── API GET (read): cache at edge with short TTL
    ├── API POST (write): route to closest region
    └── Auth: validate JWT at edge before forwarding
```

→ Reduce origin load 80%+. Global latency cut by 50%.

### ✅ Best practice: Region-aware naming

Resources tagged with region:
```hcl
locals {
  region = "ap-southeast-1"
}

resource "aws_instance" "web" {
  tags = {
    Name = "${var.app}-${local.region}-web"
    Region = local.region
  }
}
```

→ Easy to identify in multi-region setup.

### ✅ Best practice: Latency budget

Define + enforce:
- **P50 latency budget**: 200ms.
- **P99 latency budget**: 1000ms.
- Per-component: DB query < 50ms, cache < 5ms, external API < 200ms.

→ Alert if exceeded. Optimize hot path.

---

## 🧠 Self-check

**Q1.** Why **3+ AZs** thay vì 2?

<details>
<summary>💡 Đáp án</summary>

**2 AZs**: 1 AZ fails → 1 left. Can survive 1 failure, but:
- During failover, 1 AZ handles 2x load — may overload.
- If you need quorum (RDS Multi-AZ standby, etcd 3-node), 2 = no quorum.

**3 AZs**: 1 AZ fails → 2 left. Better:
- Each AZ handles 1.5x load (better than 2x).
- Quorum: 3 → 2 = still majority for distributed systems (etcd, Postgres replicas, etc.).
- **N+1 redundancy**: lose 1, still have N capacity.

**Best practice**:
- **Stateless apps**: 2 AZs OK if traffic low.
- **Stateful (DB, K8s control plane)**: 3+ AZs for quorum.
- **Tier-1 services**: 3 AZs always.

**Quorum systems**:
- etcd: 3 nodes → tolerate 1 failure. 5 → tolerate 2.
- Postgres synchronous replication: 3 → 1 primary + 2 standby (quorum 2).
- Kafka: 3 brokers → replication factor 3.

→ 3-AZ deploy = standard for HA. AWS default for managed services (RDS, MSK).
</details>

**Q2.** Multi-region active-active — main complexity?

<details>
<summary>💡 Đáp án</summary>

**Main complexity**: **database consistency**.

**Single-region**: 1 database, single source of truth. Reads + writes consistent (ACID).

**Multi-region active-active**:
- 2+ regions, each can write.
- Network latency between regions: 100-200ms+.
- Writes can conflict (same row updated in 2 regions simultaneously).

**Resolution strategies**:

1. **Last-write-wins (LWW)**:
   - Timestamp on each write.
   - Newer wins.
   - DynamoDB Global Tables default.
   - **Risk**: data loss on concurrent writes.

2. **Conflict-free Replicated Data Types (CRDT)**:
   - Special data structures merge automatically (counters, sets).
   - Riak, some Postgres extensions.
   - **Limited**: not all data fits CRDT.

3. **Per-region primary keys**:
   - User belongs to region. All writes for user go to that region.
   - Cross-region read OK (eventually consistent).
   - **Common in SaaS** (tenant-per-region).

4. **Synchronous multi-region**:
   - Spanner, CockroachDB, Aurora Global with strict consistency.
   - **Cost**: every write waits for cross-region ack (100-200ms write latency).

5. **Hybrid**: 
   - One region is "global writer", others read replicas.
   - Aurora Global Database default: us-east-1 primary, eu-west-1 reader.
   - Writes go to primary, reads can be local.
   - **Trade-off**: write latency high for non-primary users.

**Other complexities**:
- **Cache invalidation** cross-region.
- **Session affinity**: user sticky to region.
- **Cost**: 2-3x infra + data transfer cross-region.
- **Operational**: 2x deploys, 2x debugging.

**Recommend**:
- **< 99.99% SLA**: multi-AZ in one region is enough.
- **99.99%+**: multi-region active-passive (simpler than active-active).
- **Global low latency**: read-local + write-global pattern.

→ True active-active rare. Most "multi-region" = active-passive or geo-routed.
</details>

**Q3.** CDN caching strategy — header values?

<details>
<summary>💡 Đáp án</summary>

**Cache-Control header** controls CDN + browser caching.

**By asset type**:

```
# Static assets (hash in URL, version-locked)
GET /static/js/main.abc123.js
Cache-Control: public, max-age=31536000, immutable
# 1 year cache, never re-validate

# CSS (versioned URL)
Cache-Control: public, max-age=31536000, immutable

# Images (less critical)
Cache-Control: public, max-age=86400
# 1 day, ok to re-fetch

# HTML
Cache-Control: public, max-age=60, must-revalidate
# 1 minute (UX dynamic), revalidate via 304

# API response (varies)
Cache-Control: private, max-age=10  # short, per-user
# OR
Cache-Control: no-cache, must-revalidate  # never cache

# Authenticated API
Cache-Control: private, no-store  # never cache anywhere
```

**Key directives**:
- `public`: any cache (CDN + browser).
- `private`: only browser, not CDN.
- `max-age=N`: cache N seconds.
- `s-maxage=N`: CDN-specific TTL (overrides max-age for CDN).
- `immutable`: hint that content never changes (skip revalidation).
- `must-revalidate`: re-check expired content with origin.
- `no-cache`: cache but always revalidate.
- `no-store`: don't cache at all.
- `stale-while-revalidate=N`: serve stale while fetching fresh in background.

**Versioning strategy**:
- **Hash in filename** (Vite, Webpack default): `main.abc123.js`. New version = new filename. Cache forever.
- **Query string** (`?v=2`): less effective, some CDNs ignore.
- **Versioned path**: `/v2/static/`. Clean.

**Cache invalidation**:
- Hash-based: no invalidation needed (new file = new URL).
- Manual purge: Cloudflare/CloudFront API `purge_cache(url)`.

**Stale-while-revalidate**:
```
Cache-Control: max-age=60, stale-while-revalidate=86400
```
→ Fresh for 60s. After expiry, serve stale + fetch fresh in background. User never waits.

**Recommended**:
- Static: `max-age=31536000, immutable` (with hash filenames).
- HTML: `max-age=60, stale-while-revalidate=600`.
- API: `private, max-age=10` or `no-cache`.
- Auth: `private, no-store`.

→ Result: CDN cache hit rate 95%+, origin load 5%.
</details>

**Q4.** Schrems II + GDPR — practical compliance for EU customer?

<details>
<summary>💡 Đáp án</summary>

**Schrems II** (2020 EU court ruling): US-based cloud vendors (AWS, GCP, Azure US-based) subject to **US CLOUD Act** = US government can request EU data.

This conflicts with **GDPR Article 44** (transfer outside EU only with adequate protection).

**Practical mitigations** for EU customer data:

1. **Physical region in EU**:
   - AWS: eu-west-1 (Ireland), eu-central-1 (Frankfurt), eu-west-3 (Paris), eu-north-1 (Stockholm).
   - GCP: europe-west1 (Belgium), europe-west3 (Frankfurt), europe-north1 (Finland).
   - Azure: westeurope (Netherlands), northeurope (Ireland), francecentral, germanywestcentral.

2. **Customer-managed encryption** (CMEK/BYOK):
   - Encrypt data with your keys, not vendor's.
   - Vendor accesses encrypted data only.
   - AWS KMS Customer Managed Keys + S3 SSE-KMS.

3. **Data Processing Agreement (DPA)**:
   - Sign DPA with vendor.
   - Vendors (AWS, GCP, Azure) have standard DPAs.

4. **Standard Contractual Clauses (SCC)**:
   - 2021 EU Commission updated SCCs.
   - Vendor includes SCC in terms.

5. **Transfer Impact Assessment (TIA)**:
   - Document specific data + safeguards.
   - Auditor checks at GDPR audit.

6. **EU-only vendors** (strict cases):
   - OVH (France), Hetzner (Germany), Scaleway (France).
   - IONOS, Aruba (EU-based).
   - Not subject to US CLOUD Act.

7. **Encryption-at-rest + in-transit**:
   - AES-256 default.
   - TLS 1.3 transit.

8. **Right to access + deletion**:
   - API endpoint for user to request data export.
   - Delete on user request (within 30 days typical).

**EU-only architecture**:
```
User EU → CDN EU (Cloudflare EU) → Load Balancer EU region → App in EU AZ → DB in EU AZ → S3 EU bucket → Backups EU
```

All data stays EU. No US datacenter involved.

**Documentation needed**:
- Data flow diagram.
- DPA + SCC signed.
- DPIA (Data Protection Impact Assessment) for sensitive processing.
- Privacy policy disclosure of vendors used.
- Sub-processor list (vendors of vendors).

**Realistic challenges**:
- Some SaaS (e.g., support tools) US-only → use EU alternative or accept risk.
- Multi-region: ensure no replica in non-EU region.
- AI services: many in US (OpenAI etc.). Use EU AI services or self-host.

→ GDPR compliance = ongoing process, not one-time setup.
</details>

**Q5.** Reliability tier 99.9% vs 99.99% — realistic cost increase?

<details>
<summary>💡 Đáp án</summary>

**99.9% (3 nines)** = 43 min downtime/month allowed.

**Architecture**:
- Multi-AZ in 1 region.
- 3 EC2 instances (1 per AZ).
- RDS Multi-AZ.
- LB across AZs.
- Backups daily.

**Cost example (Singapore, small app)**:
- 3 × t3.medium EC2: $90/month.
- RDS Multi-AZ db.t3.medium: $80/month.
- ALB: $20/month.
- S3 + bandwidth: $30/month.
- **Total: ~$220/month**.

**99.99% (4 nines)** = 4.32 min downtime/month allowed.

**Architecture**:
- Multi-region active-passive.
- Primary region: us-east-1 (us-east-1 multi-AZ).
- DR region: us-west-2 (us-west-2 multi-AZ).
- Cross-region RDS replica.
- Route53 failover.
- S3 cross-region replication.
- More monitoring + alerting.

**Cost increase**:
- Duplicate infra: ~2x = $440/month.
- Cross-region data transfer: $50/month.
- Cross-region RDS replica: $80/month.
- Route53 health checks: $5/month.
- **Total: ~$580/month** (~2.6x).

**99.999% (5 nines)** = 25.9 sec downtime/month.

**Architecture**:
- Multi-region active-active.
- Spanner/Aurora Global Database.
- DNS load balancing.
- Real-time replication.
- Chaos engineering exercises.

**Cost increase**:
- Active-active infra: 3x = $660/month.
- Spanner: $300+/month minimum.
- Operations team for 24/7 watch.
- Quarterly DR drills.
- **Total: ~$2000+/month** (~10x).

→ **Pattern**: each "9" = ~3x cost.

**Other factors**:
- **Engineering time**: more 9s = more code complexity + ops time.
- **MTTR investment**: lower 9s OK with 1h MTTR; 5 nines need < 30s MTTR.
- **Chaos engineering**: 4 nines+ need active failure testing.

**Reality**:
- Most apps **don't need 99.99%**. 99.9% sufficient.
- **Spec SLO realistic**: measure actual reliability, aim 1 tier higher.
- **Customer perception**: 99.9% vs 99.99% rarely noticed unless incident concentrated (1 month all 43 min in 1 incident vs spread out).

**Recommend tier by use case**:
- **Internal tool**: 99% (single AZ OK).
- **B2B SaaS**: 99.9% (multi-AZ).
- **E-commerce**: 99.9-99.95%.
- **Payments**: 99.99% (multi-region warranted).
- **Healthcare critical**: 99.99%+.
- **Telco/utility**: 99.999%+.

→ Choose tier based on **business impact**, not engineering pride.
</details>

---

## ⚡ Cheatsheet

```bash
# === Region/AZ commands ===
aws ec2 describe-regions
aws ec2 describe-availability-zones --region us-east-1
aws ec2 describe-availability-zones --filters Name=zone-id,Values=use1-az1

# Latency test
ping ec2.ap-southeast-1.amazonaws.com
mtr -r -c 10 host.example.com

# === CDN ===
# Check if cached:
curl -I https://cdn.example.com/asset.png | grep -i cache

# Cache headers:
Cache-Control: public, max-age=31536000, immutable   # static
Cache-Control: public, max-age=60                     # HTML
Cache-Control: private, no-store                      # auth
Cache-Control: max-age=60, stale-while-revalidate=600 # SWR

# Cloudflare purge:
curl -X POST "https://api.cloudflare.com/.../purge_cache" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -d '{"files": ["https://example.com/asset.png"]}'

# === DNS routing (Route53) ===
# Latency-based routing
# Failover routing
# Geo routing
# Weighted routing
```

```hcl
# === Multi-AZ Terraform ===
data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_subnet" "public" {
  count = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
}
```

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **Region** | Geographic cluster of datacenters (e.g., us-east-1) |
| **Availability Zone (AZ)** | Isolated datacenter within region |
| **AZ ID** | Cross-account consistent zone identifier (e.g., use1-az1) |
| **Edge location** | Small datacenter close to users (CDN + edge compute) |
| **CDN** | Content Delivery Network — cache static at edge |
| **Cloudflare** | CDN + DDoS + edge compute leader |
| **CloudFront** | AWS CDN |
| **Edge compute** | Run code at edge (Workers, Lambda@Edge) |
| **RTT** | Round-Trip Time (network latency) |
| **TCP handshake** | 3-packet exchange before data flows |
| **TLS handshake** | Encryption setup (2 RTTs default, 1 RTT with TLS 1.3 0-RTT) |
| **HTTP/2** | Multiplexed HTTP (one connection many requests) |
| **HTTP/3 / QUIC** | UDP-based, faster setup |
| **Multi-AZ** | Spread resources across AZs for HA |
| **Multi-region** | Spread across regions for global / DR |
| **Active-passive** | Primary serves, DR ready but idle |
| **Active-active** | Multiple regions serve simultaneously |
| **Geo-routing** | DNS routes user to closest region |
| **Latency-based routing** | DNS routes by lowest latency |
| **Aurora Global Database** | Multi-region Aurora with primary + readers |
| **Spanner** | GCP globally distributed DB with strong consistency |
| **CRDT** | Conflict-free Replicated Data Type |
| **Data residency** | Legal requirement data physically in country |
| **GDPR** | EU privacy regulation |
| **Schrems II** | EU court ruling on US data transfers |
| **CLOUD Act** | US law allowing data requests from US companies abroad |
| **DPA** | Data Processing Agreement |
| **SCC** | Standard Contractual Clauses (EU transfer mechanism) |
| **CMEK / BYOK** | Customer-managed encryption keys |
| **SLA** | Service Level Agreement (contract uptime) |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [00_what-is-cloud-computing.md](00_what-is-cloud-computing.md)
- → Tiếp: [02_cloud-networking.md](02_cloud-networking.md) *(sắp viết)*
- ↑ Cluster: [Cloud Fundamentals README](../../README.md)

### Cross-reference
- 🌐 [DNS basics](../../../../05_Networking/dns/) — DNS routing for multi-region
- 🌐 [TCP/IP](../../../../05_Networking/tcp-ip-fundamentals/) — latency physics

### Tài nguyên ngoài
- 📖 [AWS Global Infrastructure](https://aws.amazon.com/about-aws/global-infrastructure/)
- 📖 [GCP Regions and Zones](https://cloud.google.com/compute/docs/regions-zones)
- 📖 [Azure Regions](https://azure.microsoft.com/en-us/explore/global-infrastructure/geographies/)
- 📖 [Cloudflare network](https://www.cloudflare.com/network/)
- 📖 [GDPR text](https://gdpr.eu/)
- 📖 [Schrems II ruling explained](https://noyb.eu/en/schrems-ii)
- 📖 [Latency map cloud regions](https://www.cloudping.co/grid/p_99/timeframe/1Y)
- 📖 [CDN comparison 2026](https://blog.cloudflare.com/)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bài thứ 2 cluster cloud-fundamentals. Region + AZ + Edge + CDN + latency physics + multi-region patterns (active-passive/active-active/geo-routed) + GDPR/data residency + reliability tiers + hands-on Vietnam startup region pick. Apply Schrems II context cho EU compliance.
