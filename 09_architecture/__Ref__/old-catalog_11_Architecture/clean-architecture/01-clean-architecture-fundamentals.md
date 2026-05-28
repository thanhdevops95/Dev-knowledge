# 🏛️ Clean Architecture — Kiến trúc sạch

> `[ADVANCED]` — Code dễ test, dễ thay đổi, dễ bảo trì

---

## Tại sao Clean Architecture?

```
❌ Spaghetti code:
  Controller → trực tiếp query DB + gửi email + validate + business logic
  → Thay đổi DB? Sửa 50 files.
  → Test? Cần setup cả DB + email server.
  → Reuse? Không thể.

✅ Clean Architecture:
  Controller → Use Case → Entity
                  ↓
           Repository Interface → (Prisma, MongoDB, in-memory...)
  → Thay đổi DB? Sửa 1 file (repository implementation).
  → Test? Mock interfaces. Không cần DB.
  → Reuse? Business logic độc lập, dùng lại được.
```

---

## 1. Dependency Rule — Luật quan trọng nhất

```
┌─────────────────────────────────────────────────────┐
│  Frameworks & Drivers (ngoài cùng)                  │
│  Express, Prisma, Redis, AWS SDK                    │
│  ┌─────────────────────────────────────────────┐    │
│  │  Interface Adapters                         │    │
│  │  Controllers, Presenters, Gateways          │    │
│  │  ┌─────────────────────────────────────┐    │    │
│  │  │  Application (Use Cases)            │    │    │
│  │  │  CreateOrder, GetUser, ProcessPay   │    │    │
│  │  │  ┌─────────────────────────────┐    │    │    │
│  │  │  │  Domain (Entities)          │    │    │    │
│  │  │  │  User, Order, Money         │    │    │    │
│  │  │  │  KHÔNG phụ thuộc gì!        │    │    │    │
│  │  │  └─────────────────────────────┘    │    │    │
│  │  └─────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘

Dependency Rule: Mũi tên CHỈ hướng VÀO TRONG.
  Outer → Inner: OK (Controller dùng UseCase)
  Inner → Outer: ❌ KHÔNG BAO GIỜ (Entity không import Express!)
```

---

## 2. Cấu trúc thư mục

```
src/
├── domain/                    ← Entities, Value Objects, Domain Rules
│   ├── entities/
│   │   ├── User.ts
│   │   └── Order.ts
│   ├── value-objects/
│   │   ├── Email.ts
│   │   └── Money.ts
│   └── repositories/          ← Interfaces ONLY (không implementation!)
│       ├── IUserRepository.ts
│       └── IOrderRepository.ts
│
├── application/               ← Use Cases (orchestration)
│   ├── use-cases/
│   │   ├── CreateUser.ts
│   │   ├── GetUserById.ts
│   │   └── CreateOrder.ts
│   └── dtos/
│       ├── CreateUserDTO.ts
│       └── UserResponseDTO.ts
│
├── infrastructure/            ← Implementations (frameworks, DB)
│   ├── database/
│   │   ├── PrismaUserRepository.ts
│   │   └── PrismaOrderRepository.ts
│   ├── services/
│   │   ├── StripePaymentService.ts
│   │   └── SendGridEmailService.ts
│   └── config/
│       └── database.ts
│
└── presentation/              ← HTTP, GraphQL, CLI
    ├── http/
    │   ├── controllers/
    │   │   ├── UserController.ts
    │   │   └── OrderController.ts
    │   ├── middleware/
    │   └── routes.ts
    └── graphql/
        └── resolvers/
```

---

## 3. Code Examples

### Domain Layer — Entity

```typescript
// domain/entities/Order.ts — KHÔNG import Prisma, Express, etc!
import { Money } from '../value-objects/Money';

export enum OrderStatus {
    PENDING = 'pending',
    CONFIRMED = 'confirmed',
    SHIPPED = 'shipped',
    CANCELLED = 'cancelled',
}

export class Order {
    private constructor(
        readonly id: string,
        private items: OrderItem[],
        private status: OrderStatus,
        readonly customerId: string,
        readonly createdAt: Date,
    ) {}

    static create(customerId: string, items: OrderItem[]): Order {
        if (items.length === 0) throw new Error('Order must have at least 1 item');
        return new Order(crypto.randomUUID(), items, OrderStatus.PENDING, customerId, new Date());
    }

    confirm(): void {
        if (this.status !== OrderStatus.PENDING) {
            throw new Error(`Cannot confirm order in ${this.status} status`);
        }
        this.status = OrderStatus.CONFIRMED;
    }

    cancel(): void {
        if (this.status === OrderStatus.SHIPPED) {
            throw new Error('Cannot cancel shipped order');
        }
        this.status = OrderStatus.CANCELLED;
    }

    get total(): Money {
        return this.items.reduce(
            (sum, item) => sum.add(item.subtotal),
            Money.zero('VND'),
        );
    }

    get currentStatus(): OrderStatus { return this.status; }
}
```

### Domain Layer — Repository Interface

```typescript
// domain/repositories/IOrderRepository.ts
export interface IOrderRepository {
    findById(id: string): Promise<Order | null>;
    findByCustomerId(customerId: string): Promise<Order[]>;
    save(order: Order): Promise<void>;
}
// Chỉ interface! KHÔNG biết gì về Prisma, MongoDB, etc.
```

### Application Layer — Use Case

```typescript
// application/use-cases/CreateOrder.ts
export class CreateOrderUseCase {
    constructor(
        private orderRepo: IOrderRepository,     // Interface!
        private userRepo: IUserRepository,        // Interface!
        private paymentService: IPaymentService,  // Interface!
    ) {}

    async execute(input: CreateOrderDTO): Promise<OrderResponseDTO> {
        // 1. Validate user existence
        const user = await this.userRepo.findById(input.customerId);
        if (!user) throw new NotFoundError('User not found');

        // 2. Create domain entity (business rules enforced here)
        const order = Order.create(input.customerId, input.items);

        // 3. Process payment
        await this.paymentService.charge(user, order.total);

        // 4. Confirm order
        order.confirm();

        // 5. Persist
        await this.orderRepo.save(order);

        // 6. Return DTO (not entity!)
        return OrderResponseDTO.fromEntity(order);
    }
}
```

### Infrastructure Layer — Implementation

```typescript
// infrastructure/database/PrismaOrderRepository.ts
import { PrismaClient } from '@prisma/client';
import { IOrderRepository } from '../../domain/repositories/IOrderRepository';

export class PrismaOrderRepository implements IOrderRepository {
    constructor(private prisma: PrismaClient) {}

    async findById(id: string): Promise<Order | null> {
        const data = await this.prisma.order.findUnique({
            where: { id },
            include: { items: true },
        });
        return data ? OrderMapper.toDomain(data) : null;
    }

    async save(order: Order): Promise<void> {
        const data = OrderMapper.toPersistence(order);
        await this.prisma.order.upsert({
            where: { id: data.id },
            create: data,
            update: data,
        });
    }
}
```

### Presentation Layer — Controller

```typescript
// presentation/http/controllers/OrderController.ts
export class OrderController {
    constructor(private createOrder: CreateOrderUseCase) {}

    async create(req: Request, res: Response) {
        try {
            const result = await this.createOrder.execute({
                customerId: req.user.id,
                items: req.body.items,
            });
            res.status(201).json(result);
        } catch (err) {
            if (err instanceof NotFoundError) return res.status(404).json({ error: err.message });
            if (err instanceof ValidationError) return res.status(400).json({ error: err.message });
            res.status(500).json({ error: 'Internal error' });
        }
    }
}
```

### Dependency Injection — Wiring

```typescript
// main.ts — Gắn dependencies
const prisma = new PrismaClient();

// Infrastructure
const orderRepo = new PrismaOrderRepository(prisma);
const userRepo = new PrismaUserRepository(prisma);
const paymentService = new StripePaymentService(process.env.STRIPE_KEY);

// Use Cases
const createOrderUseCase = new CreateOrderUseCase(orderRepo, userRepo, paymentService);

// Controllers
const orderController = new OrderController(createOrderUseCase);

// Routes
app.post('/api/orders', (req, res) => orderController.create(req, res));
```

---

## 4. Testing dễ dàng

```typescript
// Test USE CASE — không cần DB thật!
describe('CreateOrderUseCase', () => {
    test('create order successfully', async () => {
        const mockOrderRepo = { save: jest.fn(), findById: jest.fn() };
        const mockUserRepo = { findById: jest.fn().mockResolvedValue({ id: '1' }) };
        const mockPayment = { charge: jest.fn() };

        const useCase = new CreateOrderUseCase(mockOrderRepo, mockUserRepo, mockPayment);

        const result = await useCase.execute({
            customerId: '1',
            items: [{ productId: 'p1', quantity: 2, price: 100 }],
        });

        expect(result.status).toBe('confirmed');
        expect(mockPayment.charge).toHaveBeenCalled();
        expect(mockOrderRepo.save).toHaveBeenCalled();
    });
});
// → Test chạy trong 10ms! Không cần DB, không cần Stripe!
```

---

## Bài tập thực hành

- [ ] Tách code spaghetti thành 4 layers
- [ ] Viết Entity với business rules (validation, state transitions)
- [ ] Repository interface + Prisma implementation
- [ ] Test Use Case với mocked dependencies

---

## Tài nguyên thêm

- [Clean Architecture (Robert Martin)](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164) — The book
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) — Alistair Cockburn
- [Bulletproof Node.js](https://softwareontheroad.com/ideal-nodejs-project-structure/) — Practical guide
