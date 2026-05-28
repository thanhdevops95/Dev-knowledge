# 📡 Event-Driven Architecture — Kiến trúc hướng sự kiện

> `[ADVANCED]` — Giao tiếp lỏng lẻo giữa microservices

---

## Tại sao Event-Driven?

```
❌ Synchronous (Request/Response):
  Order Service ──HTTP──► Payment Service ──HTTP──► Email Service
  → Payment chết → Order chết → Cả hệ thống chết! (Coupling)
  → Thêm SMS Service? Phải SỬA code Order Service!

✅ Event-Driven:
  Order Service ──publish──► "OrderCreated" Event
                                  │
                     ┌────────────┼────────────┐
                     ▼            ▼            ▼
              Payment Service  Email Service  SMS Service
  → Payment chết? → Kệ. Order vẫn OK. Event chờ retry.
  → Thêm SMS? → Subscribe event. KHÔNG sửa Order Service!
```

---

## 1. Event Types

### Domain Event — Đã xảy ra trong domain

```typescript
// Tên = past tense (quá khứ) — đã xảy ra rồi!
class OrderPlaced {
    readonly type = 'OrderPlaced';
    constructor(
        readonly orderId: string,
        readonly customerId: string,
        readonly items: OrderItem[],
        readonly totalAmount: number,
        readonly occurredAt: Date = new Date(),
    ) {}
}

class PaymentCompleted {
    readonly type = 'PaymentCompleted';
    constructor(
        readonly orderId: string,
        readonly paymentId: string,
        readonly amount: number,
    ) {}
}
```

### Integration Event — Giao tiếp giữa services

```
Domain Event = nội bộ 1 service
Integration Event = gửi qua message broker cho services khác

OrderPlaced (domain) → OrderService publish
    → Kafka/RabbitMQ
        → PaymentService subscribe → charge payment
        → InventoryService subscribe → reserve stock
        → NotificationService subscribe → send email
```

---

## 2. Patterns

### Event Sourcing — Lưu lịch sử events thay vì state

```
Traditional: Lưu STATE hiện tại
  orders table: { id: 1, status: "shipped", total: 500000 }
  → Mất lịch sử! Không biết status thay đổi thế nào.

Event Sourcing: Lưu EVENTS (Append-only log)
  Event 1: OrderPlaced    { orderId: 1, total: 500000 }
  Event 2: PaymentReceived { orderId: 1, amount: 500000 }
  Event 3: OrderConfirmed  { orderId: 1 }
  Event 4: OrderShipped    { orderId: 1, trackingId: "VN123" }

  → Replay events → rebuild state bất kỳ lúc nào!
  → Audit trail hoàn chỉnh.
  → Time travel debugging.
```

```typescript
// Rebuild state từ events
class Order {
    private status: OrderStatus;
    private total: Money;

    static fromEvents(events: DomainEvent[]): Order {
        const order = new Order();
        for (const event of events) {
            order.apply(event);
        }
        return order;
    }

    private apply(event: DomainEvent) {
        switch (event.type) {
            case 'OrderPlaced':
                this.status = OrderStatus.PENDING;
                this.total = new Money(event.totalAmount);
                break;
            case 'OrderConfirmed':
                this.status = OrderStatus.CONFIRMED;
                break;
            case 'OrderShipped':
                this.status = OrderStatus.SHIPPED;
                break;
        }
    }
}
```

### CQRS — Tách Read và Write

```
Traditional:
  API → Service → Same Database (read + write)

CQRS (Command Query Responsibility Segregation):
  Commands (Write) → Write Model → Write DB (normalized)
       │
       └── Events ──► Read Model → Read DB (denormalized, optimized)
       
  Queries (Read) → Read Model → Read DB

Ví dụ e-commerce:
  Write DB: orders, order_items (normalized, consistent)
  Read DB:  order_summaries (denormalized, fast queries)
           dashboard_stats (pre-computed aggregations)
```

---

## 3. Message Broker — Kafka vs RabbitMQ

### Kafka

```typescript
import { Kafka } from 'kafkajs';

const kafka = new Kafka({ brokers: ['localhost:9092'] });

// Producer
const producer = kafka.producer();
await producer.connect();
await producer.send({
    topic: 'order-events',
    messages: [{
        key: orderId,
        value: JSON.stringify({
            type: 'OrderPlaced',
            data: { orderId, customerId, items, total },
        }),
    }],
});

// Consumer
const consumer = kafka.consumer({ groupId: 'payment-service' });
await consumer.connect();
await consumer.subscribe({ topic: 'order-events' });
await consumer.run({
    eachMessage: async ({ message }) => {
        const event = JSON.parse(message.value.toString());
        switch (event.type) {
            case 'OrderPlaced':
                await processPayment(event.data);
                break;
        }
    },
});
```

### So sánh

| | Kafka | RabbitMQ |
|---|---|---|
| **Model** | Log (append-only) | Queue (message consumed) |
| **Replay** | ✅ Đọc lại events | ❌ Đã consume = mất |
| **Throughput** | Triệu msg/s | Chục nghìn msg/s |
| **Use case** | Event sourcing, analytics | Task queue, RPC |
| **Ordering** | Per partition | Per queue |
| **Complexity** | Cao | Thấp |

---

## 4. Saga Pattern — Transaction xuyên services

```
Vấn đề: Order cần Payment + Inventory + Shipping.
         Nếu Inventory hết hàng SAU KHI đã charge tiền?
         → Cần rollback Payment!

Saga = chuỗi local transactions + compensating transactions

Choreography Saga (Event-based):
  OrderService                PaymentService           InventoryService
       │                           │                         │
       │── OrderPlaced ──────────► │                         │
       │                           │── PaymentCharged ──────►│
       │                           │                         │── StockReserved ──► ✅
       │                           │                         │
       │                           │                  (Hết hàng!)
       │                           │◄── ReservationFailed ──│
       │◄── PaymentRefunded ──────│   (Compensate: refund)  │
       │                           │                         │
  OrderCancelled                   │                         │
```

```typescript
// Saga coordinator
class OrderSaga {
    async execute(order: Order) {
        try {
            // Step 1: Charge payment
            const paymentId = await this.paymentService.charge(order.total);

            try {
                // Step 2: Reserve inventory
                await this.inventoryService.reserve(order.items);
            } catch {
                // Compensate step 1: Refund payment
                await this.paymentService.refund(paymentId);
                throw new Error('Inventory reservation failed');
            }

            try {
                // Step 3: Create shipping
                await this.shippingService.createShipment(order);
            } catch {
                // Compensate step 1 + 2
                await this.inventoryService.release(order.items);
                await this.paymentService.refund(paymentId);
                throw new Error('Shipping creation failed');
            }
        } catch (err) {
            order.cancel(err.message);
            await this.orderRepo.save(order);
        }
    }
}
```

---

## 5. Idempotency — Xử lý duplicate events

```typescript
// Event có thể gửi 2 lần (at-least-once delivery)
// → Handler phải idempotent!

class PaymentHandler {
    async handle(event: OrderPlaced) {
        // Check đã xử lý chưa?
        const existing = await this.processedEvents.find(event.eventId);
        if (existing) return;  // Đã xử lý → bỏ qua!

        // Xử lý
        await this.paymentService.charge(event.totalAmount);

        // Ghi nhận đã xử lý
        await this.processedEvents.save(event.eventId);
    }
}
```

---

## Các lỗi thường gặp

```
❌ Sai: Dùng events cho MỌI giao tiếp → over-engineering
✅ Đúng: Sync (HTTP) cho simple queries. Events cho decoupling + async workflows.

❌ Sai: Event payload chứa quá ít data → consumer phải gọi lại producer
✅ Đúng: Event chứa đủ data cần thiết (fat event) hoặc link tới resource.

❌ Sai: Không xử lý duplicate events
✅ Đúng: Mọi consumer phải idempotent. Dùng eventId để dedup.
```

---

## Bài tập thực hành

- [ ] Thiết kế event flow: Order → Payment → Inventory → Shipping
- [ ] Implement Saga pattern cho order processing
- [ ] Event sourcing: rebuild Order state từ event log
- [ ] Kafka producer/consumer: publish và xử lý OrderPlaced events

---

## Tài nguyên thêm

- [Building Event-Driven Microservices](https://www.oreilly.com/library/view/building-event-driven-microservices/9781492057888/) — O'Reilly
- [Saga Pattern](https://microservices.io/patterns/data/saga.html) — microservices.io
- [Event Sourcing (Martin Fowler)](https://martinfowler.com/eaaDev/EventSourcing.html)
