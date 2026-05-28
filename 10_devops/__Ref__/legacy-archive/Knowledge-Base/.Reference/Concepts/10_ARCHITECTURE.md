# 10. Application Architecture

[← Messaging](09_MESSAGING.md) | [Tiếp: Troubleshooting →](11_TROUBLESHOOTING.md)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Stateless** | - | Không trạng thái - Không lưu thông tin phiên của client |
| **Stateful** | - | Có trạng thái - Lưu thông tin phiên của client |
| **Monolithic** | /ˌmɒnəˈlɪθɪk/ | Một khối - Tất cả code trong một ứng dụng duy nhất |
| **Microservices** | - | Vi dịch vụ - Chia nhỏ thành nhiều service độc lập |
| **3-Tier** | - | 3 tầng - Kiến trúc Presentation, Application, Data |
| **API Gateway** | - | Cổng API - Điểm vào duy nhất cho tất cả client requests |
| **Session** | - | Phiên làm việc - Thông tin trạng thái của người dùng |
| **Sticky Session** | - | Phiên dính - Client luôn được gửi đến cùng server |
| **JWT** | - | JSON Web Token - Token xác thực lưu phía client |
| **Service Mesh** | - | Lưới dịch vụ - Quản lý giao tiếp giữa các microservices |
| **Containerization** | - | Container hóa - Đóng gói ứng dụng và dependencies |

---

# 🤔 Tại sao DevOps cần biết Application Architecture?

## Nỗi đau thực tế

> "Mỗi lần deploy một tính năng nhỏ phải deploy lại toàn bộ hệ thống"

> "Team backend và frontend không thể làm việc độc lập"

> "Scale một module thì phải scale cả hệ thống, tốn tiền"

## Kiến thức này giúp bạn

| Tình huống | Cần biết |
|------------|----------|
| Design hệ thống mới | Monolith vs Microservices |
| Scale horizontal | Stateless design |
| Quản lý nhiều services | API Gateway, Service Mesh |
| Deploy độc lập | Microservices decomposition |
| Migrate từ monolith | Strangler fig pattern |

Hiểu architecture patterns giúp bạn đưa ra quyết định đúng đắn khi thiết kế và vận hành hệ thống. Chọn sai architecture có thể khiến team phải trả giá đắt về sau.

---

# 🔄 Stateful vs Stateless

## Stateless Application

**Stateless** application không lưu trạng thái client giữa các requests. Mỗi request độc lập với nhau.

```
┌─────────────────────────────────────────────────────────────┐
│                    STATELESS                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Request 1 → Server A → Response                            │
│  Request 2 → Server B → Response  (different server OK!)   │
│  Request 3 → Server C → Response                            │
│                                                              │
│  ✅ Easy to scale horizontally                              │
│  ✅ Any server can handle any request                       │
│  ✅ Simple load balancing                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Where to store state?**

- External database
- Redis/Memcached (session store)
- JWT tokens (client-side)

---

## Stateful Application

**Stateful** application lưu client state trong server memory.

```
┌─────────────────────────────────────────────────────────────┐
│                     STATEFUL                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Request 1 → Server A → stores session                      │
│  Request 2 → Server B → ❌ NO SESSION! Error!               │
│  Request 2 → Server A → ✅ Session found                    │
│                                                              │
│  ⚠️ Requires sticky sessions                                │
│  ⚠️ Scaling is harder                                       │
│  ⚠️ Server failure = lost state                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Best Practice

> **Prefer Stateless** for cloud-native design.

| Aspect | Stateless | Stateful |
|--------|-----------|----------|
| **Scaling** | ✅ Easy | ❌ Hard |
| **Failure recovery** | ✅ Simple | ❌ Complex |
| **Load balancing** | ✅ Any algorithm | Sticky sessions |

---

# 🏛️ Web 3-Tier Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  3-TIER ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────┐                   │
│  │          Presentation Tier            │ ← Web servers    │
│  │    (Nginx, Apache, Load Balancer)     │   (HTML, CSS)    │
│  └──────────────────────────────────────┘                   │
│                      │                                       │
│                      ▼                                       │
│  ┌──────────────────────────────────────┐                   │
│  │          Application Tier             │ ← App servers    │
│  │     (Node.js, Python, Java)           │   (Business      │
│  │                                       │    logic)        │
│  └──────────────────────────────────────┘                   │
│                      │                                       │
│                      ▼                                       │
│  ┌──────────────────────────────────────┐                   │
│  │             Data Tier                 │ ← Databases      │
│  │     (PostgreSQL, MySQL, MongoDB)      │                   │
│  └──────────────────────────────────────┘                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

# 🏢 Monolithic vs Microservices

## Monolithic Application

**Monolith** là single deployable unit chứa tất cả functionality.

```
┌─────────────────────────────────────────────────────────────┐
│                     MONOLITH                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    ONE APPLICATION                    │   │
│  │ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐ │   │
│  │ │  Auth   │ │  Users  │ │ Orders  │ │  Payments   │ │   │
│  │ └─────────┘ └─────────┘ └─────────┘ └─────────────┘ │   │
│  │ ┌─────────────────────────────────────────────────┐ │   │
│  │ │               Shared Database                    │ │   │
│  │ └─────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  Deploy: All or nothing                                      │
│  Scale: Entire application                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

| Pros | Cons |
|------|------|
| Simple development | Hard to scale |
| Easy debugging | Technology lock-in |
| Single deployment | One bug can crash all |

---

## Microservices Application

**Microservices** chia application thành **small, independent services**.

```
┌─────────────────────────────────────────────────────────────┐
│                    MICROSERVICES                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌───────────┐   │
│  │  Auth   │   │  Users  │   │ Orders  │   │ Payments  │   │
│  │ Service │   │ Service │   │ Service │   │  Service  │   │
│  └────┬────┘   └────┬────┘   └────┬────┘   └─────┬─────┘   │
│       │             │             │               │         │
│  ┌────┴────┐   ┌────┴────┐   ┌────┴────┐   ┌─────┴─────┐   │
│  │ Auth DB │   │ User DB │   │Order DB │   │Payment DB │   │
│  └─────────┘   └─────────┘   └─────────┘   └───────────┘   │
│                                                              │
│  Deploy: Independent                                         │
│  Scale: Per service                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

| Pros | Cons |
|------|------|
| Independent scaling | Complex infrastructure |
| Technology flexibility | Distributed challenges |
| Fault isolation | Network latency |
| Team autonomy | Data consistency |

---

## Comparison

| Aspect | Monolithic | Microservices |
|--------|------------|---------------|
| **Complexity** | Simple | Complex |
| **Deployment** | All together | Independent |
| **Scaling** | Whole app | Per service |
| **Tech stack** | Single | Polyglot |
| **Best for** | Startups, MVPs | Large enterprises |

---

# 🚪 API Gateway

## API Gateway là gì?

**API Gateway** là single entry point cho tất cả client requests.

```
┌─────────────────────────────────────────────────────────────┐
│                      API GATEWAY                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────┐                               ┌───────────┐     │
│  │  Web   │──┐                       ┌───►│  Users    │     │
│  └────────┘  │     ┌─────────────┐   │    └───────────┘     │
│              │     │             │   │                       │
│  ┌────────┐  ├────►│ API Gateway │───┼───►┌───────────┐     │
│  │ Mobile │──┤     │             │   │    │  Orders   │     │
│  └────────┘  │     └─────────────┘   │    └───────────┘     │
│              │                       │                       │
│  ┌────────┐  │                       └───►┌───────────┐     │
│  │  IoT   │──┘                            │ Payments  │     │
│  └────────┘                               └───────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Functions

| Function | Mô tả |
|----------|-------|
| **Routing** | Route to appropriate service |
| **Authentication** | Verify identity |
| **Rate Limiting** | Prevent abuse |
| **SSL Termination** | Handle HTTPS |
| **Caching** | Cache responses |
| **Monitoring** | Logging, metrics |

---

## Examples

- **Kong**: Open source
- **AWS API Gateway**: Managed
- **Traefik**: Cloud-native
- **Nginx Plus**: Commercial

---

[← Messaging](09_MESSAGING.md) | [Tiếp: Troubleshooting →](11_TROUBLESHOOTING.md)
