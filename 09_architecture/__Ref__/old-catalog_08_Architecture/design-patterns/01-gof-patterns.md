# 🏗️ Design Patterns — Gang of Four & Modern

> `[INTERMEDIATE → ADVANCED]` — Giải pháp tái sử dụng cho vấn đề phổ biến

---

## Design Pattern là gì?

**Design Pattern** là các giải pháp đã được kiểm chứng cho các vấn đề thiết kế phần mềm phổ biến. Chúng **không phải code cụ thể** mà là blueprint (mẫu thiết kế) có thể áp dụng trong nhiều ngôn ngữ.

**3 nhóm chính (GoF):**
1. **Creational** — Cách tạo objects
2. **Structural** — Cách tổ chức objects
3. **Behavioral** — Cách objects giao tiếp với nhau

---

## Creational Patterns

### Singleton — Chỉ 1 instance

```typescript
class DatabaseConnection {
    private static instance: DatabaseConnection;
    private connection: any;

    private constructor() {
        this.connection = connect("postgresql://...");
    }

    static getInstance(): DatabaseConnection {
        if (!DatabaseConnection.instance) {
            DatabaseConnection.instance = new DatabaseConnection();
        }
        return DatabaseConnection.instance;
    }

    query(sql: string) {
        return this.connection.query(sql);
    }
}

// Dùng: Luôn cùng 1 connection
const db1 = DatabaseConnection.getInstance();
const db2 = DatabaseConnection.getInstance();
console.log(db1 === db2);  // true
```

**Dùng cho:** Logger, Config, Database connection, Cache

---

### Factory Method — Tạo object qua factory

```typescript
interface Notification {
    send(message: string): void;
}

class EmailNotification implements Notification {
    constructor(private email: string) {}
    send(message: string) {
        console.log(`Gửi email đến ${this.email}: ${message}`);
    }
}

class SMSNotification implements Notification {
    constructor(private phone: string) {}
    send(message: string) {
        console.log(`Gửi SMS đến ${this.phone}: ${message}`);
    }
}

class PushNotification implements Notification {
    constructor(private deviceToken: string) {}
    send(message: string) {
        console.log(`Push notification: ${message}`);
    }
}

// Factory
class NotificationFactory {
    static create(type: "email" | "sms" | "push", target: string): Notification {
        switch (type) {
            case "email": return new EmailNotification(target);
            case "sms":   return new SMSNotification(target);
            case "push":  return new PushNotification(target);
        }
    }
}

// Dùng
const notif = NotificationFactory.create("email", "user@example.com");
notif.send("Đơn hàng của bạn đã được xử lý");
```

---

### Builder — Xây dựng object phức tạp từng bước

```typescript
class QueryBuilder {
    private table = "";
    private conditions: string[] = [];
    private selectedFields: string[] = ["*"];
    private orderByField = "";
    private limitValue = 0;

    from(table: string): this {
        this.table = table;
        return this;
    }

    select(...fields: string[]): this {
        this.selectedFields = fields;
        return this;
    }

    where(condition: string): this {
        this.conditions.push(condition);
        return this;
    }

    orderBy(field: string, direction: "ASC" | "DESC" = "ASC"): this {
        this.orderByField = `${field} ${direction}`;
        return this;
    }

    limit(n: number): this {
        this.limitValue = n;
        return this;
    }

    build(): string {
        let query = `SELECT ${this.selectedFields.join(", ")} FROM ${this.table}`;
        if (this.conditions.length) query += ` WHERE ${this.conditions.join(" AND ")}`;
        if (this.orderByField) query += ` ORDER BY ${this.orderByField}`;
        if (this.limitValue) query += ` LIMIT ${this.limitValue}`;
        return query;
    }
}

const query = new QueryBuilder()
    .from("users")
    .select("id", "name", "email")
    .where("is_active = true")
    .where("age >= 18")
    .orderBy("name")
    .limit(10)
    .build();
```

---

## Structural Patterns

### Decorator — Mở rộng behavior không sửa class gốc

```typescript
interface Repository<T> {
    findById(id: string): Promise<T | null>;
    save(entity: T): Promise<T>;
}

// Base implementation
class UserRepository implements Repository<User> {
    async findById(id: string) {
        return db.query(`SELECT * FROM users WHERE id = $1`, [id]);
    }
    async save(user: User) {
        return db.query(`INSERT INTO users ...`);
    }
}

// Caching Decorator
class CachedRepository<T> implements Repository<T> {
    constructor(
        private readonly repo: Repository<T>,
        private readonly cache: Redis,
        private readonly ttl: number = 3600
    ) {}

    async findById(id: string): Promise<T | null> {
        const cached = await this.cache.get(`entity:${id}`);
        if (cached) return JSON.parse(cached);

        const entity = await this.repo.findById(id);
        if (entity) await this.cache.setex(`entity:${id}`, this.ttl, JSON.stringify(entity));
        return entity;
    }

    async save(entity: T): Promise<T> {
        const saved = await this.repo.save(entity);
        await this.cache.del(`entity:${(entity as any).id}`);
        return saved;
    }
}

// Logging Decorator
class LoggedRepository<T> implements Repository<T> {
    constructor(private readonly repo: Repository<T>, private logger: Logger) {}

    async findById(id: string): Promise<T | null> {
        this.logger.info(`findById: ${id}`);
        const start = Date.now();
        const result = await this.repo.findById(id);
        this.logger.info(`findById took ${Date.now() - start}ms`);
        return result;
    }

    async save(entity: T): Promise<T> {
        this.logger.info(`save called`);
        return this.repo.save(entity);
    }
}

// Compose decorators
const userRepo = new LoggedRepository(
    new CachedRepository(
        new UserRepository(),
        redis
    ),
    logger
);
```

---

### Adapter — Chuyển đổi interface

```typescript
// Bạn muốn dùng interface này
interface PaymentGateway {
    processPayment(amount: number, currency: string): Promise<{ success: boolean; transactionId: string }>;
}

// Nhưng thư viện cũ có interface khác
class LegacyStripeSDK {
    charge(cents: number, curr: string, callback: (err: Error | null, chargeId: string) => void): void { }
}

// Adapter chuyển đổi
class StripeAdapter implements PaymentGateway {
    constructor(private stripe: LegacyStripeSDK) {}

    processPayment(amount: number, currency: string) {
        return new Promise<{ success: boolean; transactionId: string }>((resolve, reject) => {
            this.stripe.charge(amount * 100, currency, (err, chargeId) => {
                if (err) reject(err);
                else resolve({ success: true, transactionId: chargeId });
            });
        });
    }
}
```

---

## Behavioral Patterns

### Observer — Publish/Subscribe

```typescript
type EventHandler<T> = (data: T) => void;

class EventEmitter<Events extends Record<string, any>> {
    private listeners: Partial<{
        [K in keyof Events]: EventHandler<Events[K]>[]
    }> = {};

    on<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>): () => void {
        if (!this.listeners[event]) this.listeners[event] = [];
        this.listeners[event]!.push(handler);
        
        // Return unsubscribe function
        return () => this.off(event, handler);
    }

    off<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>) {
        this.listeners[event] = this.listeners[event]?.filter(h => h !== handler);
    }

    emit<K extends keyof Events>(event: K, data: Events[K]) {
        this.listeners[event]?.forEach(handler => handler(data));
    }
}

// Sử dụng
type AppEvents = {
    'user.created': { id: string; email: string };
    'order.placed': { orderId: string; userId: string; amount: number };
};

const emitter = new EventEmitter<AppEvents>();

const unsubscribe = emitter.on('order.placed', ({ orderId, amount }) => {
    console.log(`Đơn hàng ${orderId} - ${amount}đ`);
    sendConfirmationEmail(orderId);
});

emitter.emit('order.placed', { orderId: '123', userId: 'u1', amount: 99000 });
unsubscribe();  // Clear listener
```

---

### Strategy — Hoán đổi thuật toán

```typescript
interface SortStrategy<T> {
    sort(data: T[]): T[];
}

class BubbleSort<T> implements SortStrategy<T> {
    sort(data: T[]): T[] { /* ... */ return data; }
}

class QuickSort<T> implements SortStrategy<T> {
    sort(data: T[]): T[] { /* ... */ return data; }
}

class DataSorter<T> {
    constructor(private strategy: SortStrategy<T>) {}

    setStrategy(strategy: SortStrategy<T>) {
        this.strategy = strategy;
    }

    sort(data: T[]): T[] {
        return this.strategy.sort(data);
    }
}

const sorter = new DataSorter(new QuickSort());
sorter.sort([3, 1, 4, 1, 5]);

// Đổi strategy runtime
sorter.setStrategy(new BubbleSort());
```

---

### Command — Encapsulate requests, support undo

```typescript
interface Command {
    execute(): void;
    undo(): void;
}

class TextEditor {
    private text = "";
    private history: Command[] = [];

    executeCommand(cmd: Command) {
        cmd.execute();
        this.history.push(cmd);
    }

    undoLastCommand() {
        this.history.pop()?.undo();
    }

    getText() { return this.text; }
    setText(text: string) { this.text = text; }
}

class InsertTextCommand implements Command {
    private previousText: string;

    constructor(
        private editor: TextEditor,
        private textToInsert: string,
        private position: number
    ) {
        this.previousText = editor.getText();
    }

    execute() {
        const current = this.editor.getText();
        this.editor.setText(
            current.slice(0, this.position) + this.textToInsert + current.slice(this.position)
        );
    }

    undo() {
        this.editor.setText(this.previousText);
    }
}
```

---

## Khi nào dùng Pattern nào?

| Vấn đề | Pattern |
|---|---|
| Cần 1 instance duy nhất | Singleton |
| Ẩn logic tạo object phức tạp | Factory / Abstract Factory |
| Tạo object bước-by-bước | Builder |
| Thêm tính năng không sửa code gốc | Decorator |
| Interface không tương thích | Adapter |
| Cần notify nhiều object | Observer |
| Đổi thuật toán runtime | Strategy |
| Undo/Redo, Queue commands | Command |
| Duyệt collection | Iterator |
| Giảm coupling giữa nhiều objects | Mediator |

---

## Bài tập thực hành

- [ ] Implement Logger với Singleton
- [ ] Xây dựng form validator dùng Chain of Responsibility
- [ ] Tạo UI component system dùng Composite pattern
- [ ] Implement undo/redo cho text editor

---

## Tài nguyên thêm

- [Refactoring Guru](https://refactoring.guru/design-patterns) — Giải thích visual đẹp nhất
- [Design Patterns (GoF book)](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [patterns.dev](https://www.patterns.dev/) — Modern JavaScript Patterns
