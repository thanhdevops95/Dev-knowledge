# 🔗 Microservices — Kiến trúc phân tán

> `[INTERMEDIATE → ADVANCED]` — Khi monolith không đủ scale

---

## Microservices là gì?

**Monolith:** 1 app chứa TẤT CẢ tính năng → deploy cùng nhau.

**Microservices:** Chia thành nhiều service NHỎ, ĐỘC LẬP → mỗi service có DB riêng, deploy riêng.

```
Monolith:                          Microservices:
┌──────────────────────┐          ┌──────┐ ┌──────┐ ┌──────┐
│ ┌──────┐ ┌────────┐ │          │ User │ │Order │ │Paymt │
│ │ User │ │ Order  │ │          │ Svc  │ │ Svc  │ │ Svc  │
│ │      │ │        │ │   →      │ ┌──┐ │ │ ┌──┐ │ │ ┌──┐ │
│ │      │ │        │ │          │ │DB│ │ │ │DB│ │ │ │DB│ │
│ ├──────┤ ├────────┤ │          │ └──┘ │ │ └──┘ │ │ └──┘ │
│ │Paymt │ │Notific.│ │          └──────┘ └──────┘ └──────┘
│ └──────┘ └────────┘ │            ▲ API    ▲ API    ▲ API
│     1 Database      │            └────────┴────────┘
└──────────────────────┘                    │
                                     API Gateway
```

---

## 1. Monolith vs Microservices

| | Monolith | Microservices |
|---|---|---|
| **Deploy** | Toàn bộ app | Từng service riêng |
| **Scale** | Scale toàn bộ | Scale từng service |
| **Tech stack** | 1 ngôn ngữ | Mỗi service khác nhau OK |
| **Team** | 1 team lớn | Nhiều team nhỏ (2-pizza) |
| **Complexity** | Code phức tạp | Infra phức tạp |
| **Data** | 1 database | Mỗi service có DB riêng |
| **Failure** | 1 lỗi → sập tất cả | 1 service lỗi → còn lại OK |
| **Khi nào** | MVP, team nhỏ, <10 dev | Scale lớn, >20 dev |

> ⚠️ **Bắt đầu bằng Monolith!** Chỉ chuyển Microservices khi thực sự cần scale.

---

## 2. Communication Patterns

### Synchronous — REST/gRPC

```
User Service ──HTTP──► Order Service
   │                        │
   │ GET /api/users/123     │
   │◄───── User data ───────│

Ưu: Đơn giản, real-time response
Nhược: Coupling, cascade failure, latency
```

### Asynchronous — Message Queue

```
Order Service ──► [Message Queue] ──► Email Service
                  (RabbitMQ/Kafka)    Inventory Service
                                      Analytics Service

Ưu: Decouple, resilient, buffer spikes
Nhược: Complex, eventual consistency
```

```javascript
// Event-driven: Order Service publish event
const event = {
    type: 'ORDER_CREATED',
    data: { orderId: '123', userId: '456', total: 500000 }
};
await messageQueue.publish('orders', event);

// Email Service subscribe
messageQueue.subscribe('orders', (event) => {
    if (event.type === 'ORDER_CREATED') {
        sendConfirmationEmail(event.data.userId, event.data.orderId);
    }
});

// Inventory Service subscribe (cùng event, xử lý khác)
messageQueue.subscribe('orders', (event) => {
    if (event.type === 'ORDER_CREATED') {
        reduceStock(event.data.items);
    }
});
```

---

## 3. API Gateway

```
Client ──► API Gateway ──┬──► User Service    (/api/users/*)
                          ├──► Order Service   (/api/orders/*)
                          ├──► Product Service (/api/products/*)
                          └──► Auth Service    (/api/auth/*)

API Gateway responsibilities:
• Routing: chuyển request đến đúng service
• Authentication: verify JWT trước khi forward
• Rate Limiting: chặn abuse
• Load Balancing: phân phôi giữa instances
• Caching: cache response phổ biến
• Request Aggregation: gộp nhiều service calls
```

---

## 4. Service Discovery

```
Vấn đề: Service A cần gọi Service B, nhưng IP của B thay đổi liên tục
         (auto-scaling, redeployment)

Giải pháp: Service Registry (Consul, etcd, K8s DNS)

┌──────────────┐
│   Service    │  Service B đăng ký: "Tôi ở 10.0.1.5:3000"
│   Registry   │  Service B instance 2: "Tôi ở 10.0.1.6:3000"
└──────┬───────┘
       │
Service A hỏi: "Service B ở đâu?"
Registry trả: ["10.0.1.5:3000", "10.0.1.6:3000"]
Service A gọi: 10.0.1.5:3000/api/orders

Trong Kubernetes: tự động qua K8s Service DNS
  http://order-service:3000/api/orders
```

---

## 5. Patterns quan trọng

### Circuit Breaker — Ngắt mạch khi service lỗi

```
Normal:   Service A ──► Service B (OK)

B bị lỗi: Service A ──► Service B (timeout!)
                        ──► retry
                        ──► retry
                        ──► vẫn lỗi → cascade failure! 💥

Với Circuit Breaker:
  CLOSED (bình thường) → gọi B
  5 lỗi liên tiếp → OPEN (ngắt mạch) → trả fallback ngay
  Sau 30 giây → HALF-OPEN → thử 1 request
  Nếu OK → quay lại CLOSED
  Nếu lỗi → quay lại OPEN
```

### Saga Pattern — Distributed Transaction

```
Vấn đề: Order cần: tạo order + trừ tiền + giảm kho
         3 services, 3 databases → không thể 1 transaction!

Saga — Choreography:
  Order Created → Payment Charged → Stock Reduced → Done!
                  ↓ Nếu lỗi ↓
  Order Created → Payment Charged → Stock FAILED
                  → Payment Refunded (compensating action)
                  → Order Cancelled
```

### CQRS — Tách read/write

```
Traditional:
  Read + Write ──► Same Database

CQRS:
  Write (Command) ──► Write DB (normalized)
                         │ sync/event
  Read (Query)  ──► Read DB (denormalized, optimized for queries)
```

---

## 6. Observability — Giám sát

```
3 trụ cột:

1. Logging:    Ghi lại events (ELK Stack, CloudWatch)
   {"level":"error","service":"order","msg":"Payment failed","orderId":"123"}

2. Metrics:    Đo lường số liệu (Prometheus + Grafana)
   • Request rate, error rate, latency (p50, p95, p99)
   • CPU, Memory usage

3. Tracing:    Theo dõi request xuyên suốt services (Jaeger, Zipkin)
   Request → API Gateway (5ms) → User Service (10ms) → Order Service (50ms) → DB (30ms)
                                                        ↑ Bottleneck ở đây!
```

---

## Khi nào dùng Microservices?

```
✅ Team > 20 developers
✅ Cần scale từng phần riêng biệt
✅ Các domain rõ ràng, ít coupling
✅ Frequency deploy khác nhau giữa teams

❌ Team < 10 → Monolith đủ rồi
❌ Startup giai đoạn đầu → tốc độ ship feature quan trọng hơn
❌ Không hiểu distributed systems → sẽ tạo "distributed monolith" 💀
```

---

## Các lỗi thường gặp

```
❌ Sai: "Microservices = chia nhỏ monolith thành 50 services"
✅ Đúng: Chia theo business domain (bounded context), 5-10 services là đủ

❌ Sai: Shared database giữa services → coupling!
✅ Đúng: Mỗi service sở hữu data riêng, giao tiếp qua API/events

❌ Sai: Distributed monolith (microservices nhưng deploy cùng nhau)
✅ Đúng: Mỗi service deploy, scale, fail ĐỘC LẬP
```

---

## Bài tập thực hành

- [ ] Tách monolith thành 2 services: User + Order (Docker Compose)
- [ ] Giao tiếp giữa services qua REST API
- [ ] Thêm RabbitMQ/Redis cho async communication
- [ ] Implement Circuit Breaker pattern

---

## Tài nguyên thêm

- [Microservices.io](https://microservices.io/) — Patterns catalog
- [Building Microservices (Sam Newman)](https://www.oreilly.com/library/view/building-microservices-2nd/9781492034018/) — Sách kinh điển
- [Martin Fowler — Microservices](https://martinfowler.com/articles/microservices.html) — Bài viết gốc
