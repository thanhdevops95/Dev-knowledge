# 🧠 Memory Management — Quản lý bộ nhớ

> `[INTERMEDIATE → ADVANCED]` — Hiểu cách máy tính quản lý RAM

---

## 1. Stack vs Heap

```
┌─────────────────────────────────────────┐
│                                         │
│              STACK                      │  ← Nhanh, tự động, kích thước cố định
│         (LIFO - Last In First Out)      │
│  ┌─────────────────────────────────┐    │
│  │ main()    → int x = 5           │    │  Primitive values
│  │ foo()     → int y = 10          │    │  Function call frames
│  │ bar()     → int z = 15          │    │  Local variables
│  └─────────────────────────────────┘    │
│                                         │
├─────────────────────────────────────────┤
│                                         │
│              HEAP                       │  ← Chậm hơn, linh hoạt, cần quản lý
│         (Dynamic allocation)            │
│  ┌───┐  ┌─────────┐  ┌──────┐         │
│  │ A │  │  Array  │  │ Obj  │         │  Objects, Arrays
│  └───┘  └─────────┘  └──────┘         │  Closures
│     ┌──────┐        ┌───────────┐      │  Dynamic data
│     │String│        │  HashMap  │      │
│     └──────┘        └───────────┘      │
│                                         │
└─────────────────────────────────────────┘

Stack: Tự dọn khi function return. Nhanh, an toàn.
Heap:  Cần Garbage Collector dọn. Chậm hơn, linh hoạt.
```

```javascript
function example() {
    // Stack: primitive values
    let x = 42;           // Stack
    let name = "An";      // Stack (reference) → Heap (string data)

    // Heap: objects, arrays
    let user = { name: "An", age: 25 };  // Reference trên Stack → Object trên Heap
    let nums = [1, 2, 3];                // Reference trên Stack → Array trên Heap

    return user;
    // x, name, nums references bị pop khỏi Stack
    // user reference trả về → Object vẫn sống trên Heap
    // nums Object trên Heap → không ai reference → GC sẽ dọn!
}
```

---

## 2. Garbage Collection — Dọn rác tự động

### Reference Counting (Python, Swift)

```python
# Python dùng Reference Counting + Cycle Detection
import sys

a = [1, 2, 3]
print(sys.getrefcount(a))  # 2 (a + getrefcount arg)

b = a        # refcount = 3
del a        # refcount = 2
del b        # refcount = 1 (getrefcount) → GC sẽ thu hồi!
```

### Mark-and-Sweep (JavaScript V8, Java)

```
Phase 1: MARK — Đi từ root (global, stack), đánh dấu mọi object reachable
Phase 2: SWEEP — Thu hồi object KHÔNG được đánh dấu

Root (global, stack)
  │
  ├──► Object A ──► Object B     ← Reachable (giữ lại)
  │
  └──► Object C                  ← Reachable (giữ lại)

  Object D ──► Object E          ← Unreachable (thu hồi!)
  Object F                       ← Unreachable (thu hồi!)
```

### Generational GC (V8 Engine)

```
Young Generation (Nursery)          Old Generation (Tenured)
┌───────────────────────┐          ┌───────────────────────┐
│ Mới tạo               │          │ Sống lâu              │
│ GC thường xuyên       │ ──────► │ GC ít khi             │
│ (Minor GC - nhanh!)   │ promote │ (Major GC - chậm!)    │
└───────────────────────┘          └───────────────────────┘

80% objects chết trẻ → Minor GC rất hiệu quả.
Objects sống qua nhiều GC cycles → promote lên Old Generation.
```

---

## 3. Memory Leaks — Rò rỉ bộ nhớ

```javascript
// ❌ Leak 1: Global variables
function process() {
    result = [];          // Quên let/const → global! Không bao giờ bị GC!
}

// ❌ Leak 2: Event listeners không gỡ
element.addEventListener('click', handler);
// Component unmount nhưng quên removeEventListener → handler giữ reference!

// ✅ Fix:
const controller = new AbortController();
element.addEventListener('click', handler, { signal: controller.signal });
// Cleanup: controller.abort();

// ❌ Leak 3: Closures giữ reference
function createLeak() {
    const hugeArray = new Array(1000000).fill('data');
    return function () {
        console.log(hugeArray.length);  // Closure giữ hugeArray sống mãi!
    };
}

// ❌ Leak 4: Timers
const id = setInterval(() => {
    // Quên clearInterval → chạy mãi + giữ references
}, 1000);

// ❌ Leak 5: Map/Set chứa references
const cache = new Map();
function addToCache(key, largeObject) {
    cache.set(key, largeObject);  // Không bao giờ xóa → memory tăng mãi!
}

// ✅ Fix: Dùng WeakMap
const cache = new WeakMap();     // Key bị GC → entry tự xóa!
```

---

## 4. Memory in Different Languages

| Ngôn ngữ | Quản lý | GC | Đặc điểm |
|---|---|---|---|
| **C/C++** | Manual (malloc/free) | Không | Full control, dễ leak |
| **Rust** | Ownership system | Không | Compile-time safety |
| **Java** | Automatic | JVM GC | Generational |
| **JavaScript** | Automatic | V8 GC | Mark-Sweep + Generational |
| **Python** | Automatic | Ref Count + GC | Cycle detection |
| **Go** | Automatic | Concurrent GC | Low-latency |

### Rust Ownership — Zero-cost memory safety

```rust
fn main() {
    let s1 = String::from("hello");  // s1 owns the string
    let s2 = s1;                      // Ownership MOVED to s2. s1 invalid!
    // println!("{}", s1);            // Compile ERROR! s1 no longer valid

    let s3 = s2.clone();             // Deep copy → cả hai valid
    println!("{} {}", s2, s3);       // OK!
}   // s2, s3 dropped → memory freed. No GC needed!
```

---

## 5. Profiling Memory

```javascript
// Node.js
const used = process.memoryUsage();
console.log({
    rss: `${Math.round(used.rss / 1024 / 1024)} MB`,       // Total process
    heapTotal: `${Math.round(used.heapTotal / 1024 / 1024)} MB`,
    heapUsed: `${Math.round(used.heapUsed / 1024 / 1024)} MB`,
    external: `${Math.round(used.external / 1024 / 1024)} MB`,
});

// Chrome DevTools:
// 1. F12 → Memory tab
// 2. Take Heap Snapshot → So sánh 2 snapshots
// 3. Allocation Timeline → Xem allocations theo thời gian

// Python
import tracemalloc
tracemalloc.start()
# ... code ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

---

## Các lỗi thường gặp

```
❌ Sai: Object pool cho mọi thứ (premature optimization)
✅ Đúng: GC hiện đại rất nhanh. Chỉ pool cho objects đắt (DB connections, threads)

❌ Sai: WeakMap/WeakRef cho mọi cache
✅ Đúng: WeakMap khi key lifecycle = entry lifecycle. Map + TTL cho cache thông thường.

❌ Sai: Không bao giờ nghĩ về memory
✅ Đúng: Profile khi app chậm hoặc memory tăng liên tục (upward trend = leak!)
```

---

## Bài tập thực hành

- [ ] Tạo memory leak bằng closure → fix bằng WeakMap
- [ ] Profile Node.js app: tìm top memory consumers
- [ ] So sánh: Map vs WeakMap — behavior khi key bị GC
- [ ] Chrome DevTools: Heap snapshot comparison

---

## Tài nguyên thêm

- [V8 Blog: Trash Talk (GC deep dive)](https://v8.dev/blog/trash-talk) — V8 team
- [Memory Management (MDN)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Memory_management)
- [Understanding Rust Ownership](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html)
