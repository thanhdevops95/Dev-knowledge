# 🧩 Domain-Driven Design — Thiết kế hướng nghiệp vụ

> `[ADVANCED]` — Xây dựng phần mềm phản ánh đúng thế giới thực

---

## DDD là gì?

**Domain-Driven Design** = Thiết kế phần mềm xoay quanh **nghiệp vụ kinh doanh** chứ không phải công nghệ.

```
❌ Sai: "Mình dùng MongoDB, microservices, Kafka..."
✅ Đúng: "Order Service xử lý đặt hàng, quản lý trạng thái từ
         Pending → Confirmed → Shipped → Delivered"
```

---

## 1. Strategic DDD — Chia hệ thống lớn

### Bounded Context — Ranh giới nghiệp vụ

```
E-commerce System:

┌─────────────┐  ┌──────────────┐  ┌─────────────┐
│  Catalog     │  │   Orders     │  │  Shipping   │
│  Context     │  │   Context    │  │  Context    │
│              │  │              │  │             │
│ • Product    │  │ • Order      │  │ • Shipment  │
│ • Category   │  │ • OrderItem  │  │ • Tracking  │
│ • Price      │  │ • Payment    │  │ • Carrier   │
└──────┬───────┘  └──────┬───────┘  └──────┬──────┘
       │                 │                 │
       └────── Events ───┴──── Events ─────┘

Mỗi context có MÔ HÌNH RIÊNG cho cùng 1 thực thể:
  Catalog.Product  = { name, description, images, price }
  Orders.Product   = { productId, name, price, quantity }
  Shipping.Product = { productId, weight, dimensions }
```

### Ubiquitous Language — Ngôn ngữ chung

```
Developers + Domain Experts NÓI CÙNG 1 NGÔN NGỮ:
  ❌ "user entity trong table users..."
  ✅ "Khách hàng (Customer) đặt đơn hàng (Order)"

  ❌ "update status field to 2"
  ✅ "Xác nhận đơn hàng (Confirm Order)"

  ❌ "isActive boolean = false"
  ✅ "Vô hiệu hóa tài khoản (Deactivate Account)"

Ngôn ngữ này phải NHẤT QUÁN trong code, docs, conversation.
```

---

## 2. Tactical DDD — Building Blocks

### Entity vs Value Object

```typescript
// Entity — có identity, thay đổi theo thời gian
class Order {
    constructor(
        readonly id: OrderId,        // Identity!
        private status: OrderStatus,
        private items: OrderItem[],
        private shippingAddress: Address,
    ) {}

    confirm() {
        if (this.status !== OrderStatus.PENDING) {
            throw new Error('Only pending orders can be confirmed');
        }
        this.status = OrderStatus.CONFIRMED;
        this.addEvent(new OrderConfirmed(this.id));
    }
}

// Value Object — không có identity, bất biến (immutable)
class Money {
    constructor(
        readonly amount: number,
        readonly currency: Currency,
    ) {
        if (amount < 0) throw new Error('Amount cannot be negative');
    }

    add(other: Money): Money {
        if (this.currency !== other.currency) throw new Error('Currency mismatch');
        return new Money(this.amount + other.amount, this.currency);  // Trả về object MỚI!
    }

    equals(other: Money): boolean {
        return this.amount === other.amount && this.currency === other.currency;
    }
}

class Address {
    constructor(
        readonly street: string,
        readonly city: string,
        readonly country: string,
    ) {}

    equals(other: Address): boolean {
        return this.street === other.street && this.city === other.city;
    }
}
```

### Aggregate — Nhóm đối tượng

```typescript
// Aggregate Root = điểm truy cập duy nhất
// Bên ngoài KHÔNG ĐƯỢC thao tác trực tiếp với OrderItem
class Order {  // ← Aggregate Root
    private items: OrderItem[] = [];

    addItem(product: Product, quantity: number) {
        const existing = this.items.find(i => i.productId === product.id);
        if (existing) {
            existing.increaseQuantity(quantity);
        } else {
            this.items.push(new OrderItem(product.id, product.price, quantity));
        }
    }

    removeItem(productId: ProductId) {
        this.items = this.items.filter(i => i.productId !== productId);
    }

    get total(): Money {
        return this.items.reduce(
            (sum, item) => sum.add(item.subtotal),
            new Money(0, Currency.VND),
        );
    }
}

// Rule: Bên ngoài chỉ tương tác qua Order, KHÔNG truy cập trực tiếp OrderItem
// orderRepository.save(order) → lưu cả order + items
```

---

## 3. Domain Events — Giao tiếp giữa contexts

```typescript
// Event = "đã xảy ra điều gì đó"
class OrderConfirmed {
    constructor(
        readonly orderId: string,
        readonly confirmedAt: Date,
        readonly totalAmount: Money,
    ) {}
}

class PaymentReceived {
    constructor(
        readonly orderId: string,
        readonly paymentId: string,
        readonly amount: Money,
    ) {}
}

// Event handler — context khác lắng nghe
class ShippingService {
    @OnEvent('OrderConfirmed')
    async handleOrderConfirmed(event: OrderConfirmed) {
        // Tạo shipment khi order được xác nhận
        await this.createShipment(event.orderId);
    }
}

class NotificationService {
    @OnEvent('OrderConfirmed')
    async handleOrderConfirmed(event: OrderConfirmed) {
        // Gửi email xác nhận
        await this.sendConfirmationEmail(event.orderId);
    }
}

// Luồng: Order confirmed → Event published → Shipping + Notification xử lý
```

---

## 4. Repository Pattern — Data Access

```typescript
// Repository = collection-like interface cho Aggregates
interface OrderRepository {
    findById(id: OrderId): Promise<Order | null>;
    findByCustomerId(customerId: CustomerId): Promise<Order[]>;
    save(order: Order): Promise<void>;
    delete(id: OrderId): Promise<void>;
}

// Implementation (infrastructure layer)
class PrismaOrderRepository implements OrderRepository {
    constructor(private prisma: PrismaClient) {}

    async findById(id: OrderId): Promise<Order | null> {
        const data = await this.prisma.order.findUnique({
            where: { id: id.value },
            include: { items: true },
        });
        if (!data) return null;
        return OrderMapper.toDomain(data);  // Map DB → Domain
    }

    async save(order: Order): Promise<void> {
        const data = OrderMapper.toPersistence(order);  // Map Domain → DB
        await this.prisma.order.upsert({
            where: { id: data.id },
            create: data,
            update: data,
        });
    }
}
```

---

## 5. Application Service — Orchestration

```typescript
// Use Case = Application Service
class ConfirmOrderUseCase {
    constructor(
        private orderRepo: OrderRepository,
        private paymentService: PaymentService,
        private eventBus: EventBus,
    ) {}

    async execute(orderId: string): Promise<void> {
        // 1. Load aggregate
        const order = await this.orderRepo.findById(new OrderId(orderId));
        if (!order) throw new NotFoundException('Order not found');

        // 2. Business logic (domain layer)
        order.confirm();  // Validation + state change

        // 3. Side effects
        await this.paymentService.charge(order.total);

        // 4. Persist
        await this.orderRepo.save(order);

        // 5. Publish events
        await this.eventBus.publish(new OrderConfirmed(orderId, new Date(), order.total));
    }
}
```

---

## 6. Layered Architecture

```
┌─────────────────────────────────────────┐
│  Presentation (Controllers, API)        │    ← HTTP request/response
├─────────────────────────────────────────┤
│  Application (Use Cases, DTOs)          │    ← Orchestration
├─────────────────────────────────────────┤
│  Domain (Entities, Value Objects,       │    ← Business rules
│          Domain Events, Repositories)   │       KHÔNG phụ thuộc gì!
├─────────────────────────────────────────┤
│  Infrastructure (DB, External APIs,     │    ← Implementations
│                   Message Queues)       │
└─────────────────────────────────────────┘

Dependency Rule:
  Presentation → Application → Domain ← Infrastructure
  Domain KHÔNG import từ bất kỳ layer nào!
```

---

## Khi nào dùng DDD?

| Dùng DDD | Không cần DDD |
|---|---|
| Nghiệp vụ phức tạp, nhiều rules | CRUD đơn giản |
| Domain expert + dev cùng làm | Todo app, blog |
| Nhiều bounded contexts | Single microservice nhỏ |
| Long-term project | Prototype, MVP |

---

## Bài tập thực hành

- [ ] Xác định Bounded Contexts cho hệ thống E-learning
- [ ] Viết Aggregate: Order + OrderItem (validations, domain events)
- [ ] Implement Repository Pattern với Prisma
- [ ] Event-driven: Order → Payment → Notification flow

---

## Tài nguyên thêm

- [Domain-Driven Design (Eric Evans)](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215) — "Blue Book" gốc
- [Implementing DDD (Vaughn Vernon)](https://www.amazon.com/Implementing-Domain-Driven-Design-Vaughn-Vernon/dp/0321834577) — "Red Book" thực hành
- [DDD Quickly](https://www.infoq.com/minibooks/domain-driven-design-quickly/) — Free PDF
