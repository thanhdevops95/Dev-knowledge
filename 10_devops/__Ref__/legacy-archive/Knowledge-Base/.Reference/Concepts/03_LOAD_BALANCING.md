# 03. Load Balancing & Clustering

[← TCP/UDP/DNS](02_TCP_UDP_DNS.md) | [Tiếp: Caching & CDN →](04_CACHING_CDN.md)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Load Balancer** | - | Bộ cân bằng tải - Thiết bị/phần mềm phân phối traffic đến nhiều server |
| **L4** | - | Layer 4 - Cân bằng tải dựa trên IP và Port (TCP/UDP) |
| **L7** | - | Layer 7 - Cân bằng tải dựa trên nội dung HTTP (URL, headers, cookies) |
| **Round Robin** | - | Phân phối tuần tự - Luân phiên gửi request đến từng server |
| **Least Connections** | - | Ít kết nối nhất - Gửi đến server có ít connection nhất |
| **Health Check** | - | Kiểm tra sức khỏe - Xác định server có hoạt động hay không |
| **Failover** | - | Chuyển đổi dự phòng - Tự động chuyển sang server backup khi primary lỗi |
| **Cluster** | /ˈklʌstər/ | Cụm máy chủ - Nhóm server làm việc cùng nhau như một đơn vị |
| **Active-Active** | - | Cả hai node đều xử lý traffic |
| **Active-Passive** | - | Một node hoạt động, một node dự phòng |
| **HAProxy** | - | High Availability Proxy - Phần mềm cân bằng tải phổ biến |
| **Nginx** | /ˈɛndʒɪnˌeks/ | Web server kiêm reverse proxy và load balancer |
| **Upstream** | - | Các server backend mà load balancer forward traffic đến |
| **Sticky Session** | - | Phiên dính - Client luôn được gửi đến cùng một server |

---

# 🤔 Tại sao DevOps cần biết Load Balancing?

## Nỗi đau thực tế

> "Black Friday, website sập vì một server không chịu nổi traffic"

> "Deploy version mới mà user thấy lúc cũ lúc mới, không nhất quán"

> "Sếp hỏi: Làm sao scale web server để chịu được 10x traffic?"

## Kiến thức này giúp bạn

| Tình huống | Cần biết |
|------------|----------|
| Website cần chịu tải cao | Load balancing algorithms |
| Không muốn downtime khi deploy | Rolling deployment với LB |
| Một server chết, hệ thống vẫn chạy | Health checks, failover |
| Route API và static assets khác nhau | L7 load balancing |
| Database cluster setup | Active-Active vs Active-Passive |

Load Balancing là kỹ năng cốt lõi để xây dựng hệ thống có khả năng mở rộng (scalable) và sẵn sàng cao (high availability). Hầu như mọi hệ thống production đều cần load balancer.

---

# ⚖️ Load Balancing

## Load Balancing là gì?

**Load Balancing** cho phép chúng ta **phân phối traffic đến** giữa nhiều server, đảm bảo **tính sẵn sàng cao và độ tin cậy** bằng cách chỉ gửi requests đến các server đang hoạt động.

```
┌─────────────────────────────────────────────────────────────┐
│                    LOAD BALANCING                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│     Clients                    Load               Servers    │
│                               Balancer                       │
│     ┌───┐                    ┌──────┐           ┌───────┐   │
│     │ C1│───┐                │      │     ┌────►│ App 1 │   │
│     └───┘   │                │      │     │     └───────┘   │
│             │                │      │─────┤                  │
│     ┌───┐   ├───────────────►│  LB  │     │     ┌───────┐   │
│     │ C2│───┤                │      │─────┼────►│ App 2 │   │
│     └───┘   │                │      │     │     └───────┘   │
│             │                │      │     │                  │
│     ┌───┐   │                │      │─────┴────►┌───────┐   │
│     │ C3│───┘                │      │           │ App 3 │   │
│     └───┘                    └──────┘           └───────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Tại sao cần Load Balancing?

### Benefits

| Benefit | Mô tả |
|---------|-------|
| **Workload Distribution** | Prevent overload trên single server |
| **High Availability** | Eliminate single points of failure |
| **Scalability** | Add/remove servers theo demand |
| **Performance** | Improve response time |

---

## Layers

### Layer 4 (Network Layer)

**L4 Load Balancer** operates tại Transport layer (TCP/UDP).

| Đặc điểm | Mô tả |
|----------|-------|
| Decision based on | IP address và port |
| Visibility | Không thấy HTTP headers, URL, cookies |
| Speed | Faster (ít processing) |
| Use case | Simple routing |

```
Client → L4 LB → forward based on IP:Port → Server
```

### Layer 7 (Application Layer)

**L7 Load Balancer** operates tại Application layer (HTTP/HTTPS).

| Đặc điểm | Mô tả |
|----------|-------|
| Decision based on | HTTP headers, URL path, cookies |
| Visibility | Full HTTP inspection |
| Features | Content-based routing, SSL termination |
| Use case | Complex routing rules |

```
/api/*      → API servers
/images/*   → Image servers
/admin/*    → Admin servers
```

---

## Types

### Software Load Balancers

**Software-based** load balancers chạy trên standard hardware.

| Product | Mô tả |
|---------|-------|
| **Nginx** | Most popular, also reverse proxy |
| **HAProxy** | High performance, TCP/HTTP |
| **Traefik** | Native Docker/K8s support |
| **Envoy** | Modern, cloud-native |

### Hardware Load Balancers

**Hardware-based** load balancers là dedicated physical devices.

- F5 BIG-IP
- Citrix ADC
- A10 Networks

### DNS Load Balancing

```
dig example.com
example.com.  300  IN  A  192.0.2.1
example.com.  300  IN  A  192.0.2.2
example.com.  300  IN  A  192.0.2.3
```

---

## Routing Algorithms

### Round Robin

Requests được **distribute đến servers theo rotation**.

```
Request 1 → Server A
Request 2 → Server B
Request 3 → Server C
Request 4 → Server A  (cycle repeats)
```

### Weighted Round Robin

Account for **differing server capacities** using weights.

```
Server A (weight: 5) → gets 5 requests
Server B (weight: 3) → gets 3 requests
Server C (weight: 2) → gets 2 requests
```

### Least Connections

**New request đến server có fewest connections**.

```
Server A: 10 connections
Server B: 5 connections  ← Next request here
Server C: 15 connections
```

### Least Response Time

Server với **fastest response + fewest connections**.

### IP Hash

**Cùng client IP luôn đến cùng server** (session persistence).

```
hash(client_IP) % num_servers = server_index
```

---

## Health Checks

### Types

| Type | Mô tả |
|------|-------|
| **TCP** | Can connect to port? |
| **HTTP** | GET /health → 200 OK? |
| **Custom** | Execute script |

### Parameters

| Parameter | Typical Value |
|-----------|---------------|
| Interval | 5-30 seconds |
| Timeout | 2-10 seconds |
| Healthy threshold | 2-3 consecutive |
| Unhealthy threshold | 2-3 consecutive |

---

## Redundant Load Balancers

```
┌─────────────────────────────────────────────────────────────┐
│              REDUNDANT LOAD BALANCERS                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│              ┌──────────────┐                                │
│         ┌───►│ LB (Active)  │───┐                           │
│         │    └──────────────┘   │                            │
│  Users ─┤         ↓ heartbeat   ├───► Servers                │
│         │    ┌──────────────┐   │                            │
│         └───►│ LB (Passive) │───┘                           │
│              └──────────────┘                                │
│                                                              │
│  If Active fails → Passive takes over automatically         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

# 🔗 Clustering

## Clustering là gì?

**Computer cluster** là một group của **hai hoặc nhiều computers (nodes)**, chạy **in parallel** để achieve một common goal.

```
┌─────────────────────────────────────────────────────────────┐
│                      CLUSTER                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                    ┌─────────────┐                           │
│                    │Leader Node  │ ◄── Entry point           │
│                    │(Coordinator)│                           │
│                    └──────┬──────┘                           │
│                           │                                  │
│            ┌──────────────┼──────────────┐                   │
│            │              │              │                   │
│            ▼              ▼              ▼                   │
│     ┌──────────┐   ┌──────────┐   ┌──────────┐              │
│     │  Node 1  │   │  Node 2  │   │  Node 3  │              │
│     │ (Worker) │   │ (Worker) │   │ (Worker) │              │
│     └──────────┘   └──────────┘   └──────────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Types of Clusters

| Type | Purpose |
|------|---------|
| **HA Cluster** | Minimize downtime |
| **Load Balanced** | Distribute workload |
| **HPC Cluster** | Maximum computational power |
| **Storage Cluster** | Distributed storage |

---

## Configurations

### Active-Active

**All nodes actively handle traffic**.

```
┌─────────────────────────────────────────────────────────────┐
│                    ACTIVE-ACTIVE                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│              ┌────────────┐                                  │
│         ┌───►│  Node A    │ ◄── Handles 50% traffic         │
│  Traffic│    │  (Active)  │                                  │
│    ─────┤    └────────────┘                                  │
│         │                                                    │
│         │    ┌────────────┐                                  │
│         └───►│  Node B    │ ◄── Handles 50% traffic         │
│              │  (Active)  │                                  │
│              └────────────┘                                  │
│                                                              │
│  If Node A fails → Node B handles 100%                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Active-Passive

**One node handles traffic**, other is standby.

```
┌─────────────────────────────────────────────────────────────┐
│                    ACTIVE-PASSIVE                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│              ┌────────────┐                                  │
│  Traffic ───►│  Node A    │ ◄── Handles 100% traffic        │
│              │  (Active)  │                                  │
│              └────────────┘                                  │
│                   ↓ replicate                                │
│              ┌────────────┐                                  │
│              │  Node B    │ ◄── Standby                     │
│              │  (Passive) │                                  │
│              └────────────┘                                  │
│                                                              │
│  If Node A fails → Node B becomes Active                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Load Balancing vs Clustering

| Aspect | Load Balancing | Clustering |
|--------|----------------|------------|
| Purpose | Distribute traffic | Work as unit |
| Nodes | Independent | Coordinated |
| State | Usually stateless | Often shared |
| Example | Web servers | Databases |

---

[← TCP/UDP/DNS](02_TCP_UDP_DNS.md) | [Tiếp: Caching & CDN →](04_CACHING_CDN.md)
