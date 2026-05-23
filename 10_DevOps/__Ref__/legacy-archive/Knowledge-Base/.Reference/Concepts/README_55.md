# Module 02: Networking Fundamentals

---

## 🎬 Câu chuyện mở đầu

Bạn vừa deploy website lên server. Mọi thứ chạy OK trên localhost. Nhưng khi gửi link cho đồng nghiệp:

> "Tao vào không được, báo lỗi 'This site can't be reached'"

Bạn check server - app vẫn chạy. Browser - vẫn không vào được. **Vấn đề nằm ở đâu?**

Đây là lúc bạn cần hiểu **Networking**.

---

## 📖 Tại sao DevOps cần biết Networking?

### Thực tế công việc

```
70% vấn đề production liên quan đến network:
├── "Users không connect được" → DNS? Firewall? Load Balancer?
├── "App chậm quá" → Latency? Bandwidth? 
├── "Timeout liên tục" → Connection pool? Keep-alive?
└── "Service A không gọi được service B" → Network config?
```

### Những việc DevOps làm với network

| Task | Kiến thức cần |
|------|---------------|
| Setup domain cho website | DNS |
| Debug "connection refused" | Ports, Firewall |
| Config HTTPS/SSL | TLS certificates |
| Setup load balancer | HTTP, TCP |
| Debug container networking | IP, Subnets |
| Setup VPN/VPC | Routing, NAT |

---

## 📚 Nội dung Module

Module này được chia thành các phần sau:

### 🔹 Fundamentals

| # | Topic | File | Nội dung |
|---|-------|------|----------|
| 1 | IP & OSI Model | [01_IP_OSI.md](01_IP_OSI.md) | IPv4/IPv6, Subnets, CIDR, 7 Layers |
| 2 | TCP, UDP & DNS | [02_TCP_UDP_DNS.md](02_TCP_UDP_DNS.md) | Protocols, Handshakes, DNS Resolution |

### 🔹 Infrastructure

| # | Topic | File | Nội dung |
|---|-------|------|----------|
| 3 | Load Balancing | [03_LOAD_BALANCING.md](03_LOAD_BALANCING.md) | Algorithms, L4 vs L7, Clustering |
| 4 | Caching & CDN | [04_CACHING_CDN.md](04_CACHING_CDN.md) | Cache strategies, CDN, Proxy |
| 5 | Availability | [05_AVAILABILITY.md](05_AVAILABILITY.md) | The 9's, Scalability, Rate Limiting |

### 🔹 Security & APIs

| # | Topic | File | Nội dung |
|---|-------|------|----------|
| 6 | Security | [06_SECURITY.md](06_SECURITY.md) | SSL/TLS, PKI, mTLS |
| 7 | APIs | [07_APIS.md](07_APIS.md) | REST, gRPC, GraphQL |
| 8 | Real-time | [08_REALTIME.md](08_REALTIME.md) | WebSocket, SSE, Long Polling |

### 🔹 Architecture & Messaging

| # | Topic | File | Nội dung |
|---|-------|------|----------|
| 9 | Messaging | [09_MESSAGING.md](09_MESSAGING.md) | Message Queues, Pub/Sub, Kafka |
| 10 | Architecture | [10_ARCHITECTURE.md](10_ARCHITECTURE.md) | Monolith vs Microservices, API Gateway |

### 🔹 Troubleshooting

| # | Topic | File | Nội dung |
|---|-------|------|----------|
| 11 | Troubleshooting | [11_TROUBLESHOOTING.md](11_TROUBLESHOOTING.md) | Debug by Layer (L3, L4, L7) |

---

## 🎯 Thực hành

| File | Mô tả |
|------|-------|
| [LABS.md](LABS.md) | Bài thực hành hands-on |
| [SCENARIOS.md](SCENARIOS.md) | Tình huống troubleshooting thực tế |

---

## 📝 Tổng kết kiến thức

Sau khi hoàn thành Module này, bạn sẽ hiểu:

### Fundamentals

- ✅ IP Addressing (IPv4, IPv6, Public/Private, CIDR)
- ✅ OSI Model (7 layers)
- ✅ TCP vs UDP
- ✅ DNS (resolution, records, caching)

### Infrastructure

- ✅ Load Balancing (L4/L7, algorithms)
- ✅ Clustering (Active-Active, Active-Passive)
- ✅ Caching (strategies, invalidation)
- ✅ CDN (Push/Pull)
- ✅ Proxy (Forward/Reverse)

### System Design

- ✅ Availability (The 9's)
- ✅ Scalability (Vertical/Horizontal)
- ✅ Rate Limiting

### Security

- ✅ SSL/TLS/mTLS
- ✅ PKI

### APIs & Communication

- ✅ REST (HTTP methods)
- ✅ gRPC
- ✅ GraphQL
- ✅ WebSocket, SSE, Long Polling
- ✅ Message Queues (RabbitMQ)
- ✅ Pub/Sub (Kafka)

### Architecture

- ✅ Stateful vs Stateless
- ✅ 3-Tier Architecture
- ✅ Monolithic vs Microservices
- ✅ API Gateway
- ✅ Failover, Self-healing, Auto-scaling

### Troubleshooting

- ✅ Layer 3 (ping, nslookup, traceroute)
- ✅ Layer 4 (telnet, nc, ss)
- ✅ Layer 7 (curl, wget)

---

## ⏭️ Navigation

| Prev | Next |
|------|------|
| [01_LINUX](../01_LINUX/README.md) | [03_SCRIPTING](../03_SCRIPTING/README.md) |
