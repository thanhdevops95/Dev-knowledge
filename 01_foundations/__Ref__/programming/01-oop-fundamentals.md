# 🏛️ OOP — Lập trình hướng đối tượng

> `[BEGINNER → INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Nền tảng thiết kế phần mềm

---

## OOP là gì?

**Tổ chức code thành các "đối tượng"** — mỗi object chứa cả data (thuộc tính) và behavior (phương thức). Thay vì viết function rời rạc, ta gom liên quan lại.

```
Procedural:                  OOP:
getBankBalance(accountId)    account.getBalance()
deposit(accountId, amount)   account.deposit(amount)
withdraw(accountId, amount)  account.withdraw(amount)
                             → Data + Logic nằm cùng 1 chỗ!
```

---

## 1. Bốn trụ cột OOP

### Encapsulation — Đóng gói

```javascript
class BankAccount {
    #balance;  // Private — bên ngoài KHÔNG truy cập được

    constructor(initialBalance) {
        this.#balance = initialBalance;
    }

    deposit(amount) {
        if (amount <= 0) throw new Error('Amount must be positive');
        this.#balance += amount;
        return this;
    }

    withdraw(amount) {
        if (amount > this.#balance) throw new Error('Insufficient funds');
        this.#balance -= amount;
        return this;
    }

    get balance() { return this.#balance; }
}

const acc = new BankAccount(1000);
acc.deposit(500).withdraw(200);   // Method chaining
acc.balance;    // 1300 (getter)
acc.#balance;   // SyntaxError! Private!
```

### Inheritance — Kế thừa

```javascript
class Animal {
    constructor(name) { this.name = name; }
    speak() { console.log(`${this.name} makes a sound`); }
}

class Dog extends Animal {
    bark() { console.log('Woof!'); }
    speak() {  // Override
        console.log(`${this.name} barks`);
    }
}

class Cat extends Animal {
    speak() { console.log(`${this.name} meows`); }
}

const dog = new Dog('Rex');
dog.speak(); // Rex barks (override)
dog.bark();  // Woof! (method riêng)
dog instanceof Animal; // true
```

### Polymorphism — Đa hình

```javascript
// Cùng method, hành vi khác nhau tùy loại object
function makeAnimalSpeak(animal) {
    animal.speak();  // Không cần biết là Dog hay Cat!
}

makeAnimalSpeak(new Dog('Rex'));  // Rex barks
makeAnimalSpeak(new Cat('Miu')); // Miu meows
// → 1 function xử lý NHIỀU loại object
```

### Abstraction — Trừu tượng

```javascript
// Ẩn chi tiết phức tạp, chỉ lộ interface đơn giản
class EmailService {
    send(to, subject, body) {
        this.#validate(to);
        this.#connect();
        this.#authenticate();
        this.#sendEmail(to, subject, body);
        this.#disconnect();
    }

    // Chi tiết phức tạp ẩn bên trong
    #validate(email)  { /* ... */ }
    #connect()        { /* SMTP connection */ }
    #authenticate()   { /* OAuth */ }
    #sendEmail(...)   { /* ... */ }
    #disconnect()     { /* ... */ }
}

// Người dùng chỉ cần:
const email = new EmailService();
email.send('an@mail.com', 'Hello', 'World');
// Không cần biết SMTP, OAuth, connection... bên trong!
```

---

## 2. SOLID Principles

```
S — Single Responsibility: 1 class = 1 nhiệm vụ
O — Open/Closed: Mở để mở rộng, đóng để sửa đổi
L — Liskov Substitution: Subclass thay thế parent không lỗi
I — Interface Segregation: Interface nhỏ > interface to
D — Dependency Inversion: Phụ thuộc abstractions, không implementations
```

```javascript
// ❌ Vi phạm S: class làm quá nhiều thứ
class User {
    save() { /* lưu DB */ }
    sendEmail() { /* gửi email */ }
    generateReport() { /* tạo PDF */ }
}

// ✅ Tách ra:
class UserRepository { save(user) { /* DB */ } }
class EmailService { send(to, msg) { /* email */ } }
class ReportGenerator { generate(data) { /* PDF */ } }

// ❌ Vi phạm O: Sửa code cũ mỗi khi thêm shape
function area(shape) {
    if (shape.type === 'circle') return Math.PI * shape.r ** 2;
    if (shape.type === 'rect') return shape.w * shape.h;
    // Thêm triangle → phải sửa function này!
}

// ✅ Open/Closed: Mở rộng bằng cách thêm class mới
class Circle { area() { return Math.PI * this.r ** 2; } }
class Rectangle { area() { return this.w * this.h; } }
class Triangle { area() { return 0.5 * this.b * this.h; } }
// Thêm shape mới → thêm class mới, KHÔNG sửa code cũ!
```

---

## 3. Composition over Inheritance

```javascript
// ❌ Deep inheritance → fragile base class problem
class Animal { }
class FlyingAnimal extends Animal { fly() {} }
class SwimmingAnimal extends Animal { swim() {} }
// Duck vừa bay vừa bơi → kế thừa ai? Multiple inheritance!

// ✅ Composition: gắn behaviors
const canFly = (obj) => ({
    ...obj,
    fly() { console.log(`${obj.name} is flying`); },
});

const canSwim = (obj) => ({
    ...obj,
    swim() { console.log(`${obj.name} is swimming`); },
});

function createDuck(name) {
    let duck = { name };
    duck = canFly(duck);
    duck = canSwim(duck);
    return duck;
}

const duck = createDuck('Donald');
duck.fly();   // Donald is flying
duck.swim();  // Donald is swimming
```

---

## 4. Design Patterns liên quan

| Pattern | Mục đích | OOP Concept |
|---|---|---|
| Factory | Tạo objects | Encapsulation |
| Strategy | Đổi algorithm | Polymorphism |
| Observer | Event system | Abstraction |
| Template Method | Skeleton algorithm | Inheritance |
| Decorator | Thêm tính năng | Composition |

---

## OOP vs Functional Programming

| | OOP | FP |
|---|---|---|
| **Unit** | Object (data + methods) | Function (pure) |
| **State** | Mutable (thay đổi) | Immutable (không đổi) |
| **Style** | Imperative | Declarative |
| **Reuse** | Inheritance, Composition | Higher-order functions |
| **Khi nào** | Domain phức tạp, nhiều entity | Data transformation, pipeline |

> Thực tế: Hầu hết projects dùng **cả hai**. React = FP (components) + OOP (class services).

---

## Bài tập thực hành

- [ ] Tạo class hierarchy: Shape → Circle, Rectangle, Triangle (polymorphism)
- [ ] Refactor code vi phạm SOLID → tuân thủ SOLID
- [ ] Implement Observer pattern bằng OOP
- [ ] So sánh: viết 1 feature bằng OOP vs Functional

---

## Tài nguyên thêm

- [SOLID Principles](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design) — Visual guide
- [Refactoring Guru](https://refactoring.guru/design-patterns) — Patterns + OOP
- [Clean Code (Robert Martin)](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) — Classic book
