# 🦀 Rust — Ngôn ngữ Systems Programming an toàn

> `[INTERMEDIATE]` — Performance của C++ với memory safety, không cần GC

---

## Tại sao Rust?

Mỗi ngôn ngữ giải quyết **1 bài toán khác nhau** về quản lý bộ nhớ:

- **C/C++**: Lập trình viên tự quản lý → nhanh nhưng dễ crash (buffer overflow, use-after-free, memory leak)
- **Java/Python/Go**: Garbage Collector (GC) tự dọn → an toàn nhưng có "GC pause" + dùng nhiều RAM hơn
- **Rust**: **Ownership system** kiểm tra tại compile time → nhanh như C, an toàn như Java, không cần GC

Đây là lý do Rust liên tục được bình chọn là ngôn ngữ "yêu thích nhất" trên StackOverflow (8 năm liên tiếp). Nó đang được dùng trong:
- **Linux kernel** (first non-C language được chấp nhận)
- **Firefox** (Servo engine)
- **Discord** (chuyển từ Go → Rust để giảm latency spikes do GC)
- **Cloudflare, AWS, Microsoft** (infrastructure services)

### Khi nào nên học Rust?

| Dùng Rust | Chưa cần Rust |
|---|---|
| Systems programming (OS, drivers) | Web CRUD apps (dùng Node/Python) |
| Performance-critical services | Prototype, MVP |
| WebAssembly modules | Script automation |
| CLI tools (ripgrep, fd) | Data science (dùng Python) |
| Embedded/IoT | Mobile apps (dùng Swift/Kotlin) |

---

## 1. Ownership — Khái niệm cốt lõi

### Vấn đề Rust giải quyết

Trong C, bạn có thể tạo ra 2 con trỏ tới cùng 1 vùng nhớ, free 1 lần, và con trỏ còn lại trở thành "dangling pointer" → crash hoặc security vulnerability. Rust **không cho phép** điều này từ lúc compile.

### 3 quy tắc Ownership

```rust
fn main() {
    // Quy tắc 1: Mỗi value chỉ có 1 owner tại 1 thời điểm
    let s1 = String::from("hello");  // s1 OWN string data

    // Quy tắc 2: Khi owner ra khỏi scope → value bị drop (free memory)
    {
        let s2 = String::from("world");
        println!("{}", s2);  // OK
    }
    // s2 ra khỏi scope → memory tự động freed. Không cần GC!

    // Quy tắc 3: Assignment = MOVE ownership (không phải copy!)
    let s3 = s1;         // Ownership MOVED từ s1 → s3
    // println!("{}", s1);  // ❌ COMPILE ERROR! s1 không còn valid

    println!("{}", s3);  // ✅ OK, s3 là owner

    // Nếu muốn copy → dùng .clone() (deep copy)
    let s4 = s3.clone();
    println!("{} {}", s3, s4);  // ✅ Cả 2 đều valid
}
```

**Tại sao lại thiết kế như vậy?** Vì nếu 2 biến cùng "own" 1 vùng nhớ, khi 1 biến ra khỏi scope và free → biến kia sẽ trỏ vào rác. Rust triệt tiêu bug này bằng cách chỉ cho phép 1 owner.

---

## 2. Borrowing — Mượn tạm, không lấy

Nếu mỗi lần truyền data đều phải move ownership thì rất bất tiện. Rust cho phép "mượn" (borrow) qua references:

```rust
// Immutable borrow (&): đọc, không sửa
fn calculate_length(s: &String) -> usize {
    s.len()  // Đọc OK
    // s.push_str("!"); // ❌ Không được sửa!
}

// Mutable borrow (&mut): đọc VÀ sửa
fn add_greeting(s: &mut String) {
    s.push_str(", chào bạn!");  // ✅ OK
}

fn main() {
    let mut name = String::from("Nguyễn An");

    // Mượn immutable — có thể nhiều cái cùng lúc
    let len = calculate_length(&name);
    println!("Độ dài: {}", len);

    // Mượn mutable — chỉ 1 cái tại 1 thời điểm!
    add_greeting(&mut name);
    println!("{}", name);  // "Nguyễn An, chào bạn!"
}
```

**Quy tắc borrowing** (bắt buộc, compiler kiểm tra):
- Có thể có **nhiều** `&` (immutable references) cùng lúc
- Hoặc **chỉ 1** `&mut` (mutable reference) tại 1 thời điểm
- **Không thể** vừa có `&` vừa có `&mut` cùng lúc

Tại sao? Vì nếu ai đó đang đọc data mà người khác sửa → data inconsistency (data race). Rust ngăn chặn điều này ở compile time!

---

## 3. Structs, Enums & Pattern Matching

Rust không có classes (OOP) mà dùng **structs** cho data và **impl** cho methods, giống composition hơn inheritance:

```rust
// Struct — khai báo kiểu dữ liệu
struct User {
    name: String,
    email: String,
    active: bool,
    login_count: u64,
}

// Implement methods
impl User {
    // Constructor (convention: fn new)
    fn new(name: String, email: String) -> Self {
        Self {
            name,
            email,
            active: true,
            login_count: 0,
        }
    }

    fn login(&mut self) {
        self.login_count += 1;
    }

    fn display_name(&self) -> &str {
        &self.name
    }
}

// Enum — type an toàn, mỗi variant có data khác nhau
enum PaymentMethod {
    Cash,
    Card { number: String, expiry: String },
    EWallet { provider: String, phone: String },
}

// Pattern matching — compiler BẮT BUỘC handle mọi case!
fn process_payment(method: &PaymentMethod) {
    match method {
        PaymentMethod::Cash => {
            println!("Thanh toán tiền mặt");
        }
        PaymentMethod::Card { number, .. } => {
            println!("Thanh toán thẻ: ****{}", &number[number.len()-4..]);
        }
        PaymentMethod::EWallet { provider, phone } => {
            println!("Thanh toán {} qua {}", phone, provider);
        }
        // Nếu quên 1 case → COMPILE ERROR! Không bao giờ bỏ lỡ.
    }
}
```

---

## 4. Error Handling — Không có exceptions

Rust **không có try/catch**. Thay vào đó dùng `Result<T, E>` — buộc lập trình viên xử lý lỗi **tường minh**:

```rust
use std::fs;

// Result<T, E>: T = success value, E = error value
fn read_config(path: &str) -> Result<String, std::io::Error> {
    fs::read_to_string(path)
}

fn main() {
    // Cách 1: match
    match read_config("config.toml") {
        Ok(content) => println!("Config: {}", content),
        Err(e) => eprintln!("Cannot read config: {}", e),
    }

    // Cách 2: ? operator — propagate error lên caller
    // Ngắn gọn, đẹp, và an toàn!
    fn load_app() -> Result<(), Box<dyn std::error::Error>> {
        let config = fs::read_to_string("config.toml")?;  // Lỗi → return Err
        let db_url = parse_db_url(&config)?;
        let conn = connect_db(&db_url)?;
        Ok(())
    }

    // Cách 3: unwrap (ONLY for prototyping!)
    let content = fs::read_to_string("config.toml").unwrap();
    // Panic nếu lỗi! ❌ Không dùng trong production.
}
```

**Tại sao thiết kế này tốt hơn exceptions?** Vì bạn thấy ngay function nào có thể fail (trả về `Result`), và compiler bắt bạn xử lý — không bao giờ quên catch.

---

## 5. Traits — Tương tự Interfaces

```rust
// Trait = Interface (hành vi chung)
trait Printable {
    fn to_display(&self) -> String;

    // Default implementation (các struct có thể override)
    fn print(&self) {
        println!("{}", self.to_display());
    }
}

struct Product {
    name: String,
    price: f64,
}

impl Printable for Product {
    fn to_display(&self) -> String {
        format!("{}: {}đ", self.name, self.price)
    }
}

// Generic function với trait bound
fn print_all<T: Printable>(items: &[T]) {
    for item in items {
        item.print();
    }
}
```

---

## 6. Concurrency — "Fearless Concurrency"

Ownership system giúp Rust ngăn data races tại **compile time**:

```rust
use std::thread;
use std::sync::{Arc, Mutex};

fn main() {
    // Arc = Atomic Reference Counted (shared ownership across threads)
    // Mutex = Mutual Exclusion (1 thread access at a time)
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);  // Clone reference, không clone data
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();  // Lock → access
            *num += 1;
            // Lock tự release khi `num` ra khỏi scope
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Counter: {}", *counter.lock().unwrap());  // 10
}
```

**Tại sao "fearless"?** Nếu bạn viết code có data race potential, **compiler sẽ báo lỗi** — không phải debug race condition lúc runtime!

---

## Hệ sinh thái Rust

| Tool | Mô tả |
|---|---|
| **cargo** | Package manager + build tool (tuyệt vời!) |
| **rustup** | Toolchain manager |
| **crates.io** | Package registry (giống npm) |
| **tokio** | Async runtime (giống Node.js event loop) |
| **serde** | Serialization (JSON, YAML...) |
| **actix-web / axum** | Web frameworks |
| **clap** | CLI argument parser |

---

## Bài tập thực hành

- [ ] Viết CLI tool: đọc file, đếm từ, output kết quả
- [ ] Implement struct `BankAccount` với deposit/withdraw (ownership + borrowing)
- [ ] Error handling: đọc config file, parse JSON, xử lý mọi error cases
- [ ] Concurrency: download multiple URLs song song với tokio

---

## Tài nguyên thêm

- [The Rust Book](https://doc.rust-lang.org/book/) — Free, official, tuyệt vời
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/) — Học qua ví dụ
- [Rustlings](https://github.com/rust-lang/rustlings) — Interactive exercises
- [Are We Web Yet?](https://www.arewewebyet.org/) — Rust web ecosystem status
