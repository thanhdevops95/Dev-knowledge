# 🏗️ Design Patterns — Gang of Four (GoF)

> `[INTERMEDIATE → ADVANCED]` ⭐ `[MUST-KNOW]` — Giải pháp tái sử dụng cho vấn đề phổ biến trong thiết kế phần mềm

---

## Tại sao cần học Design Patterns?

Khi viết phần mềm, bạn sẽ gặp đi gặp lại cùng một loại vấn đề:
- Làm sao tạo object linh hoạt mà không phụ thuộc vào class cụ thể?
- Làm sao thêm tính năng mới mà không sửa code cũ?
- Làm sao để nhiều module giao tiếp mà không phụ thuộc lẫn nhau?

**Design Patterns** là câu trả lời — đây là những giải pháp đã được hàng triệu developer kiểm chứng trong hơn 30 năm.

> ⚠️ **Quan trọng:** Pattern là *mẫu tư duy*, không phải code copy-paste. Hiểu **khi nào dùng** quan trọng hơn hiểu **cách code**.

---

## 3 nhóm chính

| Nhóm | Mục đích | Pattern phổ biến |
|---|---|---|
| **Creational** | Cách tạo objects | Singleton, Factory, Builder |
| **Structural** | Cách tổ chức objects | Adapter, Decorator, Proxy |
| **Behavioral** | Cách objects giao tiếp | Observer, Strategy, Command |

---

## Creational Patterns — Tạo objects

### 1. Singleton — Chỉ 1 instance duy nhất

**Vấn đề:** Cần đảm bảo chỉ có DUY NHẤT 1 instance trong toàn bộ ứng dụng (ví dụ: kết nối database, logger, config).

**Ý tưởng:** Đặt constructor thành private, truy cập qua method static.

```typescript
class DatabaseConnection {
    private static instance: DatabaseConnection;
    private connection: any;

    // Private constructor — không ai có thể "new" từ bên ngoài
    private constructor() {
        this.connection = connect("postgresql://...");
    }

    // Điểm truy cập duy nhất
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

// Dùng ở bất kỳ đâu — luôn cùng 1 instance
const db1 = DatabaseConnection.getInstance();
const db2 = DatabaseConnection.getInstance();
console.log(db1 === db2);  // true — cùng 1 object
```

**Khi nào dùng:** Database connection, Logger, Config, Cache  
**Cẩn thận:** Singleton là *global state* — lạm dụng sẽ khiến code khó test. Ưu tiên dùng Dependency Injection thay thế.

---

### 2. Factory Method — Ẩn logic tạo object

**Vấn đề:** Bạn cần tạo nhiều loại object khác nhau, nhưng không muốn code client phải biết cụ thể class nào.

**Ý tưởng:** Tạo method/class chuyên quyết định tạo object nào.

```typescript
// Giao diện chung cho mọi notification
interface Notification {
    send(message: string): void;
}

class EmailNotification implements Notification {
    constructor(private email: string) {}
    send(message: string) {
        console.log(`📧 Gửi email đến ${this.email}: ${message}`);
    }
}

class SMSNotification implements Notification {
    constructor(private phone: string) {}
    send(message: string) {
        console.log(`📱 Gửi SMS đến ${this.phone}: ${message}`);
    }
}

// Factory — client không cần biết EmailNotification hay SMSNotification
class NotificationFactory {
    static create(type: "email" | "sms", target: string): Notification {
        switch (type) {
            case "email": return new EmailNotification(target);
            case "sms":   return new SMSNotification(target);
        }
    }
}

// Client chỉ cần biết Factory — muốn thêm Push? Chỉ sửa Factory!
const notif = NotificationFactory.create("email", "user@example.com");
notif.send("Đơn hàng của bạn đã được xử lý");
```

**Khi nào dùng:** Hệ thống plugin, thanh toán nhiều cổng, notification đa kênh.

---

### 3. Builder — Xây dựng object phức tạp từng bước

**Vấn đề:** Object có quá nhiều tham số, constructor dài dòng và khó đọc.

**Ý tưởng:** Builder cho phép chọn từng thuộc tính một cách rõ ràng qua method chaining.

```typescript
class QueryBuilder {
    private table = "";
    private conditions: string[] = [];
    private fields: string[] = ["*"];
    private orderByField = "";
    private limitValue = 0;

    from(table: string): this {
        this.table = table;
        return this;  // Trả về this → cho phép method chaining
    }

    select(...fields: string[]): this { this.fields = fields; return this; }
    where(condition: string): this { this.conditions.push(condition); return this; }
    orderBy(field: string, dir: "ASC" | "DESC" = "ASC"): this {
        this.orderByField = `${field} ${dir}`;
        return this;
    }
    limit(n: number): this { this.limitValue = n; return this; }

    build(): string {
        let query = `SELECT ${this.fields.join(", ")} FROM ${this.table}`;
        if (this.conditions.length) query += ` WHERE ${this.conditions.join(" AND ")}`;
        if (this.orderByField) query += ` ORDER BY ${this.orderByField}`;
        if (this.limitValue) query += ` LIMIT ${this.limitValue}`;
        return query;
    }
}

// Đọc rõ ràng, dễ hiểu hơn constructor dài
const query = new QueryBuilder()
    .from("users")
    .select("id", "name", "email")
    .where("is_active = true")
    .where("age >= 18")
    .orderBy("name")
    .limit(10)
    .build();
// → SELECT id, name, email FROM users WHERE is_active = true AND age >= 18 ORDER BY name ASC LIMIT 10
```

**Khi nào dùng:** Query builder, HTTP request builder, form builder, config objects.

---

## Structural Patterns — Tổ chức objects

### 4. Adapter — Chuyển đổi interface không tương thích

**Vấn đề:** Bạn muốn dùng thư viện/code cũ mà interface không khớp với hệ thống mới.

**Ý tưởng:** Tạo lớp trung gian "dịch" giữa 2 interface.

```
Hệ thống mới ──► [Adapter] ──► Thư viện cũ
   (PaymentGateway)    ↕          (LegacyStripeSDK)
                   Chuyển đổi
```

```typescript
// Interface mới mà hệ thống bạn mong đợi
interface PaymentGateway {
    processPayment(amount: number, currency: string): Promise<{ success: boolean }>;
}

// Thư viện cũ — không thể sửa, interface khác hoàn toàn
class LegacyStripeSDK {
    charge(cents: number, curr: string, callback: (err: Error | null, id: string) => void) { }
}

// Adapter chuyển đổi old → new
class StripeAdapter implements PaymentGateway {
    constructor(private stripe: LegacyStripeSDK) {}

    processPayment(amount: number, currency: string) {
        return new Promise<{ success: boolean }>((resolve, reject) => {
            this.stripe.charge(amount * 100, currency, (err, id) => {
                if (err) reject(err);
                else resolve({ success: true });
            });
        });
    }
}
```

**Khi nào dùng:** Tích hợp API bên thứ 3, migration code cũ, wrapper cho thư viện.

---

### 5. Decorator — Thêm behavior mà không sửa code gốc

**Vấn đề:** Muốn thêm tính năng (logging, caching, auth...) nhưng không muốn sửa class ban đầu.

**Ý tưởng:** Bọc object gốc trong lớp mới, giữ nguyên interface.

```
Client ──► [LoggingDecorator] ──► [CachingDecorator] ──► [UserRepository]
              Thêm log              Thêm cache            Code gốc
```

```typescript
interface Repository<T> {
    findById(id: string): Promise<T | null>;
}

// Repository gốc
class UserRepository implements Repository<User> {
    async findById(id: string) {
        return db.query(`SELECT * FROM users WHERE id = $1`, [id]);
    }
}

// Decorator 1: Thêm caching — không sửa UserRepository!
class CachedRepository<T> implements Repository<T> {
    constructor(private repo: Repository<T>, private cache: Redis) {}

    async findById(id: string): Promise<T | null> {
        const cached = await this.cache.get(`entity:${id}`);
        if (cached) return JSON.parse(cached);

        const result = await this.repo.findById(id);
        if (result) await this.cache.setex(`entity:${id}`, 3600, JSON.stringify(result));
        return result;
    }
}

// Decorator 2: Thêm logging — không sửa UserRepository!
class LoggedRepository<T> implements Repository<T> {
    constructor(private repo: Repository<T>) {}

    async findById(id: string): Promise<T | null> {
        console.log(`[LOG] findById: ${id}`);
        const start = Date.now();
        const result = await this.repo.findById(id);
        console.log(`[LOG] Took ${Date.now() - start}ms`);
        return result;
    }
}

// Xếp chồng decorators — mỗi lớp thêm 1 tính năng
const userRepo = new LoggedRepository(
    new CachedRepository(new UserRepository(), redis)
);
```

**Khi nào dùng:** Thêm logging, caching, auth, retry, rate limiting mà không sửa code gốc.

---

### 6. Proxy — Kiểm soát truy cập

**Vấn đề:** Cần kiểm soát trước khi truy cập object (quyền, cache, lazy loading...).

**Ý tưởng:** Proxy đứng giữa client và object thật, cùng interface nhưng thêm logic kiểm soát.

```typescript
interface ImageLoader {
    load(url: string): Promise<Buffer>;
}

// Object thật — tải ảnh từ network
class RealImageLoader implements ImageLoader {
    async load(url: string) {
        return fetch(url).then(r => r.buffer());  // Tốn thời gian!
    }
}

// Proxy — cache ảnh đã tải, không tải lại
class CachingImageProxy implements ImageLoader {
    private cache = new Map<string, Buffer>();

    constructor(private loader: ImageLoader) {}

    async load(url: string) {
        if (this.cache.has(url)) {
            console.log("✅ Lấy từ cache");
            return this.cache.get(url)!;
        }
        console.log("⬇️ Tải từ network...");
        const data = await this.loader.load(url);
        this.cache.set(url, data);
        return data;
    }
}
```

**Khi nào dùng:** Caching proxy, protection proxy (kiểm tra quyền), virtual proxy (lazy loading).

---

## Behavioral Patterns — Giao tiếp giữa objects

### 7. Observer — Theo dõi và thông báo thay đổi

**Vấn đề:** Khi 1 object thay đổi, nhiều object khác cần biết — nhưng không muốn chúng phụ thuộc trực tiếp.

**Ý tưởng:** Publish/Subscribe — publisher phát sự kiện, subscribers lắng nghe.

```
                    ┌── [EmailService]    → Gửi email xác nhận
[OrderCreated] ─────┤── [InventoryService] → Trừ hàng tồn kho
                    └── [AnalyticsService] → Ghi nhận metrics
```

```typescript
type EventHandler<T> = (data: T) => void;

class EventEmitter<Events extends Record<string, any>> {
    private listeners: Partial<{
        [K in keyof Events]: EventHandler<Events[K]>[]
    }> = {};

    // Đăng ký lắng nghe event
    on<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>): () => void {
        (this.listeners[event] ??= []).push(handler);
        return () => this.off(event, handler);  // Trả về hàm hủy đăng ký
    }

    off<K extends keyof Events>(event: K, handler: EventHandler<Events[K]>) {
        this.listeners[event] = this.listeners[event]?.filter(h => h !== handler);
    }

    // Phát event cho tất cả subscribers
    emit<K extends keyof Events>(event: K, data: Events[K]) {
        this.listeners[event]?.forEach(handler => handler(data));
    }
}

// Sử dụng
type AppEvents = {
    'order.created': { orderId: string; userId: string; amount: number };
};

const emitter = new EventEmitter<AppEvents>();

// Mỗi service đăng ký riêng — không biết nhau
emitter.on('order.created', ({ orderId }) => sendEmail(orderId));
emitter.on('order.created', ({ orderId }) => updateInventory(orderId));

emitter.emit('order.created', { orderId: '123', userId: 'u1', amount: 99000 });
```

**Khi nào dùng:** Event bus, real-time notifications, reactive UI (React, Vue), webhook handlers.

---

### 8. Strategy — Hoán đổi thuật toán runtime

**Vấn đề:** Cùng 1 chức năng nhưng cần nhiều cách xử lý khác nhau (ví dụ: nhiều phương thức thanh toán).

**Ý tưởng:** Đóng gói mỗi thuật toán vào class riêng, đổi qua lại bất cứ lúc nào.

```typescript
// Mỗi chiến lược thanh toán là 1 class riêng biệt
interface PaymentStrategy {
    pay(amount: number): void;
}

class CreditCardPayment implements PaymentStrategy {
    pay(amount: number) { console.log(`💳 Quẹt thẻ: ${amount}đ`); }
}

class MomoPayment implements PaymentStrategy {
    pay(amount: number) { console.log(`📱 Thanh toán Momo: ${amount}đ`); }
}

class BankTransferPayment implements PaymentStrategy {
    pay(amount: number) { console.log(`🏦 Chuyển khoản: ${amount}đ`); }
}

// Context — đổi strategy bất cứ lúc nào
class Checkout {
    constructor(private strategy: PaymentStrategy) {}

    setPaymentMethod(strategy: PaymentStrategy) {
        this.strategy = strategy;
    }

    processPayment(amount: number) {
        this.strategy.pay(amount);
    }
}

const checkout = new Checkout(new CreditCardPayment());
checkout.processPayment(500000);  // 💳 Quẹt thẻ: 500000đ

checkout.setPaymentMethod(new MomoPayment());
checkout.processPayment(500000);  // 📱 Thanh toán Momo: 500000đ
```

**Khi nào dùng:** Thanh toán, sorting, validation rules, compression, encryption.

---

### 9. Command — Đóng gói hành động thành object

**Vấn đề:** Cần lưu lại hành động để undo/redo, đặt vào queue, hoặc ghi log.

**Ý tưởng:** Mỗi hành động là 1 object có `execute()` và `undo()`.

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

    undo() {
        this.history.pop()?.undo();
    }

    getText() { return this.text; }
    setText(text: string) { this.text = text; }
}

class InsertTextCommand implements Command {
    private previousText: string;

    constructor(private editor: TextEditor, private textToInsert: string) {
        this.previousText = editor.getText();
    }

    execute() {
        this.editor.setText(this.editor.getText() + this.textToInsert);
    }

    undo() {
        this.editor.setText(this.previousText);
    }
}

// Sử dụng
const editor = new TextEditor();
editor.executeCommand(new InsertTextCommand(editor, "Xin chào "));
editor.executeCommand(new InsertTextCommand(editor, "thế giới!"));
console.log(editor.getText());  // "Xin chào thế giới!"

editor.undo();
console.log(editor.getText());  // "Xin chào "
```

**Khi nào dùng:** Undo/Redo, task queue, transaction logging, macro recording.

---

## Bảng tra nhanh — Pattern nào cho vấn đề nào?

| Vấn đề | Pattern | Nhóm |
|---|---|---|
| Cần 1 instance duy nhất | **Singleton** | Creational |
| Ẩn logic tạo object phức tạp | **Factory** | Creational |
| Object có quá nhiều tham số | **Builder** | Creational |
| Interface không tương thích | **Adapter** | Structural |
| Thêm tính năng không sửa code gốc | **Decorator** | Structural |
| Kiểm soát truy cập object | **Proxy** | Structural |
| Thông báo thay đổi cho nhiều nơi | **Observer** | Behavioral |
| Đổi thuật toán linh hoạt | **Strategy** | Behavioral |
| Undo/Redo, queue hành động | **Command** | Behavioral |

---

## Các lỗi thường gặp

```
❌ Sai: Dùng Singleton cho MỌI thứ → code khó test (global state)
✅ Đúng: Ưu tiên Dependency Injection, chỉ dùng Singleton khi thực sự cần

❌ Sai: Áp dụng pattern cho code đơn giản → over-engineering
✅ Đúng: Chỉ dùng pattern khi thấy RÕ RÀNG vấn đề mà pattern đó giải quyết

❌ Sai: Decorator lồng quá nhiều → khó debug
✅ Đúng: Giới hạn 2-3 decorator, đặt tên rõ ràng
```

---

## Bài tập thực hành

- [ ] Implement Logger dùng Singleton (kèm test kiểm chứng chỉ có 1 instance)
- [ ] Xây dựng hệ thống notification đa kênh (Email/SMS/Push) dùng Factory
- [ ] Tạo QueryBuilder hỗ trợ `SELECT`, `WHERE`, `JOIN`, `ORDER BY`
- [ ] Implement hệ thống thanh toán đổi phương thức runtime dùng Strategy
- [ ] Xây text editor có Undo/Redo dùng Command pattern

---

## Tài nguyên thêm

- [Refactoring Guru](https://refactoring.guru/design-patterns) — Giải thích visual đẹp nhất, có tiếng Việt
- [patterns.dev](https://www.patterns.dev/) — Modern JavaScript Patterns
- [Design Patterns (GoF book)](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612) — Sách gốc
- [Head First Design Patterns](https://www.oreilly.com/library/view/head-first-design/9781492077992/) — Dễ hiểu nhất cho beginner
