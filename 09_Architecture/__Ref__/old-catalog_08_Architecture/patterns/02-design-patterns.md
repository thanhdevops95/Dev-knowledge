# Design Patterns — GoF, Structural, Behavioral

> **Tags:** `design-patterns` `oop` `solid` `creational` `structural` `behavioral`
> **Level:** Intermediate | **Prerequisite:** `cs/01-how-computers-work.md`

---

## 1. SOLID Principles

```typescript
// S — Single Responsibility Principle
// Each class has ONE reason to change

// BAD: UserService doing too much
class UserServiceBad {
  createUser(data) { /* ... */ }
  sendWelcomeEmail(user) { /* ... */ }  // Should be EmailService
  saveToDatabase(user) { /* ... */ }    // Should be UserRepository
  generatePDFReport(users) { /* ... */ } // Should be ReportService
}

// GOOD: Each class has one job
class UserService {
  constructor(private repo: UserRepository, private emailService: EmailService) {}
  
  async createUser(data: CreateUserDto): Promise<User> {
    const user = await this.repo.create(data);
    await this.emailService.sendWelcome(user);  // Delegate to EmailService
    return user;
  }
}

// O — Open/Closed Principle
// Open for extension, CLOSED for modification

// BAD: Need to modify existing code to add new discount type
function calcDiscount(user: User, type: string): number {
  if (type === 'student') return 0.1;
  if (type === 'senior') return 0.15;
  if (type === 'employee') return 0.2;   // Adding new type = modifying method!
}

// GOOD: Use interface, extend without modifying
interface DiscountStrategy {
  calculate(price: number, user: User): number;
}

class StudentDiscount implements DiscountStrategy {
  calculate(price: number) { return price * 0.1; }
}

class SeniorDiscount implements DiscountStrategy {
  calculate(price: number) { return price * 0.15; }
}

// Adding VIPDiscount = new class, no modification needed!
class VIPDiscount implements DiscountStrategy {
  calculate(price: number) { return price * 0.3; }
}

// L — Liskov Substitution
// Subclasses must be substitutable for their parent

// BAD: Square violates Rectangle's contract
class Rectangle {
  setWidth(w: number) { this.width = w; }
  setHeight(h: number) { this.height = h; }
  area() { return this.width * this.height; }
}

class Square extends Rectangle {
  setWidth(w: number) { this.width = this.height = w; }  // Violates parent's expectation!
  setHeight(h: number) { this.width = this.height = h; }
}

// I — Interface Segregation
// Don't force clients to implement interfaces they don't use

// BAD: Fat interface
interface Worker {
  work(): void;
  eat(): void;    // Robots can't eat!
  sleep(): void;  // Robots don't sleep!
}

// GOOD: Segregated interfaces
interface Workable { work(): void; }
interface Eatable  { eat(): void; }
interface Sleepable { sleep(): void; }

class Human implements Workable, Eatable, Sleepable { /* ... */ }
class Robot implements Workable { /* ... */ }   // Only implements what it needs

// D — Dependency Inversion
// Depend on abstractions, not concretions

// BAD: High-level module depends on low-level
class OrderService {
  private db = new PostgresDatabase();  // Tightly coupled!
  
  createOrder(data) {
    this.db.save(data);  // Can't easily swap DB or test
  }
}

// GOOD: Depend on abstraction
interface Database {
  save(entity: any): Promise<void>;
  findById(id: string): Promise<any>;
}

class OrderService {
  constructor(private db: Database) {}  // Inject abstraction
  
  createOrder(data) {
    this.db.save(data);  // Works with any Database implementation!
  }
}

// Testing uses in-memory database:
new OrderService(new InMemoryDatabase());
// Production uses real database:
new OrderService(new PostgresDatabase());
```

---

## 2. Creational Patterns

### Singleton
```typescript
class DatabaseConnection {
  private static instance: DatabaseConnection;
  private connection: Connection;
  
  private constructor() {   // Private constructor prevents `new`
    this.connection = createConnection(process.env.DATABASE_URL);
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

// Usage
const db = DatabaseConnection.getInstance();  // Same instance always!
```

### Factory Method
```typescript
// Let subclasses decide which class to instantiate
abstract class Notification {
  abstract send(message: string, recipient: string): void;
  
  notify(message: string, recipient: string) {
    console.log(`Sending notification...`);
    this.send(message, recipient);
  }
}

class EmailNotification extends Notification {
  send(message: string, email: string) {
    emailClient.send({ to: email, body: message });
  }
}

class SMSNotification extends Notification {
  send(message: string, phone: string) {
    smsClient.send(phone, message);
  }
}

class PushNotification extends Notification {
  send(message: string, deviceToken: string) {
    pushClient.send(deviceToken, message);
  }
}

// Factory
class NotificationFactory {
  static create(channel: 'email' | 'sms' | 'push'): Notification {
    switch (channel) {
      case 'email': return new EmailNotification();
      case 'sms':   return new SMSNotification();
      case 'push':  return new PushNotification();
      default:      throw new Error(`Unknown channel: ${channel}`);
    }
  }
}

const notification = NotificationFactory.create('email');
notification.notify('Order confirmed!', 'alice@example.com');
```

### Builder
```typescript
// For constructing complex objects step by step
class QueryBuilder {
  private conditions: string[] = [];
  private fields: string[] = ['*'];
  private table: string = '';
  private orderByClause?: string;
  private limitValue?: number;
  
  static from(table: string): QueryBuilder {
    const builder = new QueryBuilder();
    builder.table = table;
    return builder;
  }
  
  select(...fields: string[]): this {
    this.fields = fields;
    return this;   // Return this for chaining
  }
  
  where(condition: string): this {
    this.conditions.push(condition);
    return this;
  }
  
  orderBy(field: string, direction: 'ASC' | 'DESC' = 'ASC'): this {
    this.orderByClause = `ORDER BY ${field} ${direction}`;
    return this;
  }
  
  limit(n: number): this {
    this.limitValue = n;
    return this;
  }
  
  build(): string {
    const fields = this.fields.join(', ');
    const where = this.conditions.length > 0
      ? `WHERE ${this.conditions.join(' AND ')}`
      : '';
    const limit = this.limitValue ? `LIMIT ${this.limitValue}` : '';
    
    return `SELECT ${fields} FROM ${this.table} ${where} ${this.orderByClause ?? ''} ${limit}`.trim();
  }
}

const query = QueryBuilder.from('users')
  .select('id', 'name', 'email')
  .where('active = true')
  .where('age >= 18')
  .orderBy('name')
  .limit(20)
  .build();
// SELECT id, name, email FROM users WHERE active = true AND age >= 18 ORDER BY name ASC LIMIT 20
```

---

## 3. Structural Patterns

### Adapter
```typescript
// Convert incompatible interfaces to work together
// Example: Adapting a legacy payment API to our standard interface

interface PaymentGateway {
  charge(amount: number, currency: string, token: string): Promise<PaymentResult>;
}

// Old Stripe SDK (legacy interface)
class LegacyStripeAPI {
  createCharge(opts: { amount_cents: number; currency: string; source: string }) {
    // ... old implementation
  }
}

// Adapter: makes LegacyStripeAPI compatible with PaymentGateway
class StripeAdapter implements PaymentGateway {
  constructor(private stripe: LegacyStripeAPI) {}
  
  async charge(amount: number, currency: string, token: string): Promise<PaymentResult> {
    // Convert our interface to legacy interface
    const result = await this.stripe.createCharge({
      amount_cents: Math.round(amount * 100),  // Convert amount
      currency: currency.toLowerCase(),
      source: token,
    });
    
    // Convert legacy result to our standard result
    return {
      id: result.charge_id,
      success: result.status === 'succeeded',
      amount,
    };
  }
}

// Usage: PaymentService only knows PaymentGateway, not legacy API
class PaymentService {
  constructor(private gateway: PaymentGateway) {}  // Works with any adapter!
  
  async processPayment(order: Order) {
    return this.gateway.charge(order.total, 'USD', order.paymentToken);
  }
}
```

### Decorator
```typescript
// Add behavior to objects dynamically (wrapping pattern)
interface Logger {
  log(message: string): void;
}

class ConsoleLogger implements Logger {
  log(message: string) {
    console.log(message);
  }
}

// Decorator adds timestamp without modifying ConsoleLogger
class TimestampLoggerDecorator implements Logger {
  constructor(private logger: Logger) {}
  
  log(message: string) {
    this.logger.log(`[${new Date().toISOString()}] ${message}`);
  }
}

// Decorator adds log level filtering
class FilterLoggerDecorator implements Logger {
  constructor(private logger: Logger, private level: 'info' | 'warn' | 'error') {}
  
  log(message: string) {
    if (message.includes(this.level.toUpperCase())) {
      this.logger.log(message);
    }
  }
}

// Stacking decorators
const logger = new FilterLoggerDecorator(
  new TimestampLoggerDecorator(
    new ConsoleLogger()
  ),
  'error'
);
logger.log('ERROR: Something went wrong!');
// → [2024-01-15T10:30:00Z] ERROR: Something went wrong!
```

### Proxy
```typescript
// Placeholder that controls access to another object

interface DatabaseService {
  query(sql: string): Promise<QueryResult>;
}

// Real service
class PostgresService implements DatabaseService {
  async query(sql: string) {
    return db.execute(sql);
  }
}

// Caching Proxy
class CachingProxy implements DatabaseService {
  private cache = new Map<string, { data: QueryResult; expiry: number }>();
  
  constructor(private service: DatabaseService, private ttlMs: number = 60000) {}
  
  async query(sql: string): Promise<QueryResult> {
    const cached = this.cache.get(sql);
    if (cached && Date.now() < cached.expiry) {
      return cached.data;
    }
    
    const result = await this.service.query(sql);
    this.cache.set(sql, { data: result, expiry: Date.now() + this.ttlMs });
    return result;
  }
}

// Logging Proxy
class LoggingProxy implements DatabaseService {
  constructor(private service: DatabaseService, private logger: Logger) {}
  
  async query(sql: string): Promise<QueryResult> {
    const start = Date.now();
    try {
      const result = await this.service.query(sql);
      this.logger.log(`Query completed in ${Date.now() - start}ms: ${sql}`);
      return result;
    } catch (error) {
      this.logger.log(`Query failed: ${sql}`);
      throw error;
    }
  }
}

// Chain proxies
const db = new LoggingProxy(
  new CachingProxy(new PostgresService(), 5000),
  console
);
```

---

## 4. Behavioral Patterns

### Observer
```typescript
// Event system: notify multiple objects when state changes
type EventCallback<T> = (data: T) => void;

class EventEmitter<Events extends Record<string, any>> {
  private listeners: { [K in keyof Events]?: Set<EventCallback<Events[K]>> } = {};
  
  on<K extends keyof Events>(event: K, callback: EventCallback<Events[K]>): () => void {
    (this.listeners[event] ??= new Set()).add(callback);
    return () => this.listeners[event]?.delete(callback);  // Returns unsubscribe fn
  }
  
  emit<K extends keyof Events>(event: K, data: Events[K]): void {
    this.listeners[event]?.forEach(callback => callback(data));
  }
  
  off<K extends keyof Events>(event: K, callback: EventCallback<Events[K]>): void {
    this.listeners[event]?.delete(callback);
  }
}

// Usage
interface OrderEvents {
  'order.created': { orderId: string; userId: string; total: number };
  'order.confirmed': { orderId: string };
  'payment.failed': { orderId: string; reason: string };
}

const orderBus = new EventEmitter<OrderEvents>();

// Subscribe
orderBus.on('order.created', ({ orderId, userId }) => {
  sendConfirmationEmail(userId, orderId);
});

orderBus.on('order.created', ({ orderId }) => {
  reserveInventory(orderId);
});

// Publish
orderBus.emit('order.created', { orderId: 'ORD-123', userId: 'user-456', total: 99.99 });
```

### Strategy
```typescript
// Family of algorithms, swap at runtime
interface SortStrategy<T> {
  sort(data: T[], compareFn: (a: T, b: T) => number): T[];
}

class BubbleSortStrategy<T> implements SortStrategy<T> {
  sort(data: T[], compareFn: (a: T, b: T) => number): T[] {
    const arr = [...data];
    for (let i = 0; i < arr.length; i++) {
      for (let j = 0; j < arr.length - i - 1; j++) {
        if (compareFn(arr[j], arr[j + 1]) > 0) {
          [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        }
      }
    }
    return arr;
  }
}

class QuickSortStrategy<T> implements SortStrategy<T> {
  sort(data: T[], compareFn: (a: T, b: T) => number): T[] {
    if (data.length <= 1) return data;
    const pivot = data[Math.floor(data.length / 2)];
    const left = data.filter(x => compareFn(x, pivot) < 0);
    const mid = data.filter(x => compareFn(x, pivot) === 0);
    const right = data.filter(x => compareFn(x, pivot) > 0);
    return [...this.sort(left, compareFn), ...mid, ...this.sort(right, compareFn)];
  }
}

class DataSorter<T> {
  constructor(private strategy: SortStrategy<T>) {}
  
  setStrategy(strategy: SortStrategy<T>) {
    this.strategy = strategy;  // Swap at runtime!
  }
  
  sort(data: T[], compareFn: (a: T, b: T) => number): T[] {
    return this.strategy.sort(data, compareFn);
  }
}

const sorter = new DataSorter(new QuickSortStrategy<number>());
const sorted = sorter.sort([5, 3, 1, 4, 2], (a, b) => a - b);

// Swap to bubble sort for small arrays
if (data.length < 10) sorter.setStrategy(new BubbleSortStrategy());
```

### Command
```typescript
// Encapsulate operations as objects (undo/redo, queuing, logging)
interface Command {
  execute(): void;
  undo(): void;
}

class TextEditor {
  private content = '';
  private history: Command[] = [];
  private future: Command[] = [];
  
  executeCommand(command: Command) {
    command.execute();
    this.history.push(command);
    this.future = [];  // Clear redo history
  }
  
  undo() {
    const command = this.history.pop();
    if (command) {
      command.undo();
      this.future.push(command);
    }
  }
  
  redo() {
    const command = this.future.pop();
    if (command) {
      command.execute();
      this.history.push(command);
    }
  }
}

class InsertTextCommand implements Command {
  private insertedText: string;
  
  constructor(
    private editor: TextEditor,
    private text: string,
    private position: number
  ) {}
  
  execute() {
    this.editor.insert(this.text, this.position);
    this.insertedText = this.text;
  }
  
  undo() {
    this.editor.delete(this.position, this.insertedText.length);
  }
}

// Macro command (composite commands)
class MacroCommand implements Command {
  constructor(private commands: Command[]) {}
  
  execute() { this.commands.forEach(cmd => cmd.execute()); }
  undo() { [...this.commands].reverse().forEach(cmd => cmd.undo()); }
}
```

### Template Method
```typescript
// Define algorithm skeleton in base class, let subclasses fill in details
abstract class DataExporter {
  // Template method — orchestrates the algorithm
  export(data: any[]): void {
    const formatted = this.validate(data);
    const transformed = this.transform(formatted);
    const output = this.format(transformed);
    this.write(output);
    this.cleanup();
  }
  
  protected validate(data: any[]): any[] {
    // Common validation
    if (!Array.isArray(data)) throw new Error('Data must be an array');
    return data;
  }
  
  protected abstract transform(data: any[]): any[];  // Subclass must implement
  protected abstract format(data: any[]): string;    // Subclass must implement
  
  protected write(output: string): void {
    // Default: write to stdout
    console.log(output);
  }
  
  protected cleanup(): void {
    // Optional hook — subclass can override
  }
}

class CSVExporter extends DataExporter {
  protected transform(data: any[]) {
    return data.map(row => ({ ...row, exported_at: new Date().toISOString() }));
  }
  
  protected format(data: any[]): string {
    const headers = Object.keys(data[0]).join(',');
    const rows = data.map(row => Object.values(row).join(','));
    return [headers, ...rows].join('\n');
  }
}

class JSONExporter extends DataExporter {
  protected transform(data: any[]) {
    return data;
  }
  
  protected format(data: any[]): string {
    return JSON.stringify(data, null, 2);
  }
}

const csvExporter = new CSVExporter();
csvExporter.export(users);  // Runs the entire algorithm
```

---

## 5. Pattern Cheat Sheet

| Pattern | Intent | When to Use |
|---|---|---|
| **Singleton** | One instance globally | DB connection, config, logger |
| **Factory** | Create objects without specifying class | Plugin systems, extensibility |
| **Builder** | Construct complex objects step by step | Long constructors, query builders |
| **Adapter** | Make incompatible interfaces work together | Legacy code integration, 3rd party |
| **Decorator** | Add behavior without modification | Logging, caching, auth wrappers |
| **Proxy** | Control access to object | Caching, lazy loading, access control |
| **Observer** | Notify many objects of state change | Events, pub/sub, reactive systems |
| **Strategy** | Swap algorithms at runtime | Sorting, payment methods, validation |
| **Command** | Encapsulate actions as objects | Undo/redo, queueing, transactions |
| **Template** | Define algorithm with customizable steps | Data processing pipelines |

---

*Tài liệu liên quan: `architecture/01-clean-architecture.md` | `cs/01-how-computers-work.md`*
