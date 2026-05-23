# 🎨 Design Patterns nâng cao — Enterprise Patterns

> `[ADVANCED]` — Patterns giải quyết vấn đề thực tế trong production

---

## 1. Repository Pattern — Tách data access

```typescript
// Interface (domain layer) — không biết gì về DB!
interface UserRepository {
    findById(id: string): Promise<User | null>;
    findByEmail(email: string): Promise<User | null>;
    save(user: User): Promise<void>;
    delete(id: string): Promise<void>;
}

// Implementation (infrastructure layer) — Prisma
class PrismaUserRepository implements UserRepository {
    constructor(private prisma: PrismaClient) {}

    async findById(id: string): Promise<User | null> {
        const data = await this.prisma.user.findUnique({ where: { id } });
        return data ? UserMapper.toDomain(data) : null;
    }

    async save(user: User): Promise<void> {
        const data = UserMapper.toPersistence(user);
        await this.prisma.user.upsert({
            where: { id: data.id },
            create: data,
            update: data,
        });
    }
}

// Implementation khác — In-Memory (cho testing!)
class InMemoryUserRepository implements UserRepository {
    private users: Map<string, User> = new Map();

    async findById(id: string): Promise<User | null> {
        return this.users.get(id) || null;
    }

    async save(user: User): Promise<void> {
        this.users.set(user.id, user);
    }
}

// Test: inject InMemoryUserRepository → không cần DB thật!
```

---

## 2. Strategy Pattern — Đổi algorithm runtime

```typescript
// Interface
interface PricingStrategy {
    calculate(basePrice: number, quantity: number): number;
}

// Strategies
class RegularPricing implements PricingStrategy {
    calculate(basePrice: number, quantity: number) {
        return basePrice * quantity;
    }
}

class BulkPricing implements PricingStrategy {
    calculate(basePrice: number, quantity: number) {
        const discount = quantity >= 100 ? 0.2 : quantity >= 50 ? 0.1 : 0;
        return basePrice * quantity * (1 - discount);
    }
}

class SubscriptionPricing implements PricingStrategy {
    constructor(private discountRate: number) {}
    calculate(basePrice: number, quantity: number) {
        return basePrice * quantity * (1 - this.discountRate);
    }
}

// Context
class OrderProcessor {
    constructor(private pricing: PricingStrategy) {}

    setPricing(strategy: PricingStrategy) {
        this.pricing = strategy;
    }

    processOrder(basePrice: number, quantity: number) {
        return this.pricing.calculate(basePrice, quantity);
    }
}

// Sử dụng
const processor = new OrderProcessor(new RegularPricing());
processor.processOrder(100, 10);  // 1000

processor.setPricing(new BulkPricing());
processor.processOrder(100, 100); // 8000 (20% off)
```

---

## 3. Observer Pattern — Event system

```typescript
// EventEmitter tự viết
type Listener<T> = (data: T) => void;

class EventBus {
    private listeners: Map<string, Set<Listener<any>>> = new Map();

    on<T>(event: string, listener: Listener<T>): () => void {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, new Set());
        }
        this.listeners.get(event)!.add(listener);

        // Return unsubscribe function
        return () => this.listeners.get(event)?.delete(listener);
    }

    emit<T>(event: string, data: T): void {
        this.listeners.get(event)?.forEach(listener => listener(data));
    }
}

// Sử dụng
const bus = new EventBus();

const unsub = bus.on('user:created', (user: User) => {
    sendWelcomeEmail(user.email);
});

bus.on('user:created', (user: User) => {
    createDefaultSettings(user.id);
});

bus.emit('user:created', { id: '123', email: 'an@mail.com' });
// Cả 2 listeners đều chạy!

unsub(); // Gỡ listener email
```

---

## 4. Builder Pattern — Construct complex objects

```typescript
class QueryBuilder {
    private table: string = '';
    private conditions: string[] = [];
    private orderByClause: string = '';
    private limitValue: number = 0;
    private selectFields: string[] = ['*'];

    static from(table: string): QueryBuilder {
        const builder = new QueryBuilder();
        builder.table = table;
        return builder;
    }

    select(...fields: string[]) {
        this.selectFields = fields;
        return this;
    }

    where(condition: string) {
        this.conditions.push(condition);
        return this;
    }

    orderBy(field: string, direction: 'ASC' | 'DESC' = 'ASC') {
        this.orderByClause = `ORDER BY ${field} ${direction}`;
        return this;
    }

    limit(n: number) {
        this.limitValue = n;
        return this;
    }

    build(): string {
        let query = `SELECT ${this.selectFields.join(', ')} FROM ${this.table}`;
        if (this.conditions.length) query += ` WHERE ${this.conditions.join(' AND ')}`;
        if (this.orderByClause) query += ` ${this.orderByClause}`;
        if (this.limitValue) query += ` LIMIT ${this.limitValue}`;
        return query;
    }
}

// Đọc dễ hiểu, flexible
const query = QueryBuilder
    .from('users')
    .select('id', 'name', 'email')
    .where('active = true')
    .where('age >= 18')
    .orderBy('created_at', 'DESC')
    .limit(10)
    .build();
// SELECT id, name, email FROM users WHERE active = true AND age >= 18 ORDER BY created_at DESC LIMIT 10
```

---

## 5. Decorator Pattern — Thêm tính năng không sửa code

```typescript
// Base interface
interface Logger {
    log(message: string): void;
}

class ConsoleLogger implements Logger {
    log(message: string) {
        console.log(message);
    }
}

// Decorators: wrap và thêm tính năng
class TimestampLogger implements Logger {
    constructor(private inner: Logger) {}
    log(message: string) {
        this.inner.log(`[${new Date().toISOString()}] ${message}`);
    }
}

class ColorLogger implements Logger {
    constructor(private inner: Logger, private color: string) {}
    log(message: string) {
        this.inner.log(`\x1b[${this.color}m${message}\x1b[0m`);
    }
}

class FileLogger implements Logger {
    constructor(private inner: Logger, private filePath: string) {}
    log(message: string) {
        this.inner.log(message);
        fs.appendFileSync(this.filePath, message + '\n');
    }
}

// Stack decorators!
const logger = new FileLogger(
    new TimestampLogger(
        new ColorLogger(
            new ConsoleLogger(),
            '32',  // green
        ),
    ),
    'app.log',
);

logger.log('Server started');
// Console: [2026-03-04T20:00:00.000Z] Server started (green)
// File:    [2026-03-04T20:00:00.000Z] Server started
```

---

## 6. Middleware Pattern — Chain of responsibility

```typescript
// Express-style middleware
type Middleware = (ctx: Context, next: () => Promise<void>) => Promise<void>;

class Pipeline {
    private middlewares: Middleware[] = [];

    use(middleware: Middleware) {
        this.middlewares.push(middleware);
        return this;
    }

    async execute(ctx: Context) {
        let index = 0;
        const next = async (): Promise<void> => {
            if (index < this.middlewares.length) {
                const middleware = this.middlewares[index++];
                await middleware(ctx, next);
            }
        };
        await next();
    }
}

// Sử dụng
const pipeline = new Pipeline();

pipeline.use(async (ctx, next) => {
    const start = Date.now();
    await next();
    console.log(`${ctx.method} ${ctx.path} - ${Date.now() - start}ms`);
});

pipeline.use(async (ctx, next) => {
    if (!ctx.headers.authorization) {
        ctx.status = 401;
        return;
    }
    ctx.user = verifyToken(ctx.headers.authorization);
    await next();
});

pipeline.use(async (ctx, next) => {
    // Handler
    ctx.body = { message: 'Hello' };
});
```

---

## Pattern Selection Guide

| Vấn đề | Pattern | Khi nào |
|---|---|---|
| Tách DB khỏi logic | Repository | Mọi project có DB |
| Đổi algorithm runtime | Strategy | Pricing, sorting, auth providers |
| React to changes | Observer | Events, pub/sub, state changes |
| Build complex objects | Builder | Queries, configs, HTTP requests |
| Thêm feature không sửa code | Decorator | Logging, caching, auth wrapping |
| Pipeline xử lý | Middleware | HTTP, message processing |
| Tạo objects mà không biết class cụ thể | Factory | IoC/DI containers, plugins |
| Đảm bảo 1 instance duy nhất | Singleton | DB connections, config |

---

## Bài tập thực hành

- [ ] Repository: CRUD Users với interface + Prisma implementation
- [ ] Strategy: payment processing (Stripe, PayPal, VNPay)
- [ ] Observer: custom EventBus với typing
- [ ] Decorator: logging + caching + retry wrapper

---

## Tài nguyên thêm

- [Refactoring Guru](https://refactoring.guru/design-patterns) — Visual patterns
- [Head First Design Patterns](https://www.oreilly.com/library/view/head-first-design/9781492077992/) — Beginner friendly
- [Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/) — Martin Fowler
