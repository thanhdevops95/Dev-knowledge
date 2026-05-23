# ⚡ Async Programming — Lập trình bất đồng bộ

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Hiểu cách xử lý I/O không chặn trong mọi ngôn ngữ

---

## Tại sao cần Async?

Hãy tưởng tượng bạn đang nấu ăn:

```
❌ Đồng bộ (Synchronous):
  Luộc trứng (10 phút) → CHỜ XONG → Chiên rau (5 phút) → CHỜ XONG → Nấu cơm (20 phút)
  Tổng: 35 phút 😫

✅ Bất đồng bộ (Asynchronous):
  Luộc trứng ─┐
  Chiên rau  ─┤── Làm song song!
  Nấu cơm   ─┘
  Tổng: 20 phút 🚀 (chỉ bằng task lâu nhất)
```

Trong phần mềm, **I/O operations** (đọc file, gọi API, query DB) rất chậm — CPU phải chờ:

| Thao tác | Thời gian | So sánh |
|---|---|---|
| CPU tính toán | ~1 ns | 1 giây |
| Đọc RAM | ~100 ns | 1.5 phút |
| Đọc SSD | ~100 μs | 1 ngày |
| Đọc HDD | ~10 ms | 4 tháng |
| Network call | ~100 ms | 3 năm |

> Nếu CPU là người chạy bộ, gọi API giống như... **đứng chờ 3 năm**. Async giúp CPU làm việc khác trong lúc chờ.

---

## Sync vs Async — Hình dung

```
Synchronous (đồng bộ):
  Đọc file      ████████████ (3s)
  Query DB                    ████████ (2s)
  Gọi API                              ██████████ (3s)
  Total: 8 giây (lần lượt, chờ nhau)

Asynchronous (bất đồng bộ):
  Đọc file      ████████████ (3s)
  Query DB      ████████     (2s)     ← Chạy song song!
  Gọi API       ██████████   (3s)     ← Chạy song song!
  Total: 3 giây (song song, không chờ)
```

---

## 1. Callback — Cách cổ điển nhất

**Ý tưởng:** "Khi xong, gọi hàm này giúp tôi"

```javascript
// Callback: đọc file xong → gọi hàm xử lý
const fs = require('fs');

fs.readFile('data.txt', 'utf-8', (err, data) => {
    if (err) {
        console.error("Lỗi:", err);
        return;
    }
    console.log("Nội dung:", data);
});

console.log("Dòng này chạy TRƯỚC readFile xong!");
// Output:
// Dòng này chạy TRƯỚC readFile xong!
// Nội dung: Hello World
```

**Vấn đề: Callback Hell** 😵

```javascript
// ❌ Callback hell — "kim tự tháp diệt vong"
getUser(userId, (err, user) => {
    getOrders(user.id, (err, orders) => {
        getProducts(orders[0].id, (err, products) => {
            getReviews(products[0].id, (err, reviews) => {
                // 💀 4 levels deep! Đọc không nổi!
            });
        });
    });
});
```

---

## 2. Promise — Lời hứa trả kết quả

**Ý tưởng:** Promise đại diện cho giá trị *sẽ có trong tương lai*.

```
Promise có 3 trạng thái:
┌──────────┐    resolve(value)    ┌───────────┐
│ PENDING  │ ──────────────────►  │ FULFILLED │  ✅ Thành công
│ (chờ)    │                      │ (xong)    │
└──────────┘                      └───────────┘
      │
      │       reject(error)       ┌───────────┐
      └──────────────────────────►│ REJECTED  │  ❌ Thất bại
                                  │ (lỗi)     │
                                  └───────────┘
```

```javascript
// Tạo Promise
function fetchUser(id) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (id > 0) {
                resolve({ id, name: "Nguyễn Văn A" });
            } else {
                reject(new Error("ID không hợp lệ"));
            }
        }, 1000);
    });
}

// Dùng Promise — hết callback hell!
fetchUser(1)
    .then(user => getOrders(user.id))
    .then(orders => getProducts(orders[0].id))
    .then(products => getReviews(products[0].id))
    .then(reviews => console.log(reviews))
    .catch(err => console.error(err));  // 1 chỗ xử lý lỗi!

// Helper: delay
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// fetchWithRetry — exponential backoff
function fetchWithRetry(url, retries = 3) {
    return new Promise(async (resolve, reject) => {
        for (let i = 0; i < retries; i++) {
            try {
                const res = await fetch(url);
                return resolve(res);
            } catch (err) {
                if (i === retries - 1) reject(err);
                await delay(1000 * (i + 1));
            }
        }
    });
}
```

---

## 3. Async/Await — Viết async như sync

**Ý tưởng:** `async/await` là "cú pháp đẹp" của Promise — đọc tuần tự, chạy bất đồng bộ.

```javascript
// ✅ Clean, đọc như code đồng bộ
async function getUserReviews(userId) {
    try {
        const user = await getUser(userId);
        const orders = await getOrders(user.id);
        const products = await getProducts(orders[0].id);
        const reviews = await getReviews(products[0].id);
        return reviews;
    } catch (err) {
        console.error('Failed:', err.message);
        throw err;
    }
}
```

---

## 4. Parallel vs Sequential

```javascript
// ❌ Sequential: chạy lần lượt (CHẬM!)
const user = await fetchUser(1);          // 1 giây
const posts = await fetchPosts(1);        // 1 giây
const photos = await fetchPhotos(1);      // 1 giây
// Tổng: 3 giây 😫

// ✅ Parallel: chạy song song (NHANH!)
const [user, posts, photos] = await Promise.all([
    fetchUser(1),         // 1s ─┐
    fetchPosts(1),        // 1s ─┤ Song song!
    fetchPhotos(1),       // 1s ─┘
]);
// Tổng: 1 giây 🚀
```

### Promise combinators

```javascript
// Promise.all — tất cả phải thành công (1 fail → ALL fail!)
const [a, b, c] = await Promise.all([taskA(), taskB(), taskC()]);

// Promise.allSettled — chạy hết, không fail
const results = await Promise.allSettled([taskA(), taskB(), taskC()]);
// [
//   { status: 'fulfilled', value: 'A result' },
//   { status: 'rejected', reason: Error('B failed') },
//   { status: 'fulfilled', value: 'C result' },
// ]

// Promise.race — ai xong trước thắng
const fastest = await Promise.race([
    fetch('https://api1.com/data'),
    fetch('https://api2.com/data'),  // Fallback server
]);

// Promise.any — ai thành công trước thắng (ignore failures)
const first = await Promise.any([
    fetch('https://cdn1.com/img.jpg'),
    fetch('https://cdn2.com/img.jpg'),
    fetch('https://cdn3.com/img.jpg'),
]);
```

---

## 5. Event Loop — Trái tim của JavaScript

JavaScript chỉ có **1 thread** nhưng xử lý async được nhờ Event Loop:

```
┌───────────────────────────────────────┐
│           Call Stack                  │
│  (Thực thi code đồng bộ)             │
│  ┌─────────────────────────────┐     │
│  │ console.log("Start")        │     │
│  └─────────────────────────────┘     │
└──────────────┬────────────────────────┘
               │ Gặp async → đẩy xuống
┌──────────────▼────────────────────────┐
│        Web APIs / Node.js APIs        │
│  setTimeout, fetch, readFile...       │
│  (Chạy ở background, KHÔNG block!)   │
└──────────────┬────────────────────────┘
               │ Xong → đẩy callback vào queue
┌──────────────▼────────────────────────┐
│   ┌─── Microtask Queue ◄── Promise   │
│   │    (Ưu tiên cao)    ◄── async    │
│   │                                   │
│   └─── Macrotask Queue ◄── setTimeout│
│        (Ưu tiên thấp)  ◄── setInterval│
└──────────────┬────────────────────────┘
               │ Event Loop kiểm tra:
               │ Stack trống? → Lấy task từ queue → Đưa lên stack
               ▼
            Lặp lại...
```

```javascript
console.log("1. Start");

setTimeout(() => console.log("2. setTimeout"), 0);  // Macrotask

Promise.resolve().then(() => console.log("3. Promise"));  // Microtask

console.log("4. End");

// Output:
// 1. Start
// 4. End
// 3. Promise    ← Microtask chạy TRƯỚC macrotask!
// 2. setTimeout
```

---

## 6. Error Handling bất đồng bộ

```javascript
// ❌ Quên await → lỗi bị nuốt
async function bad() {
    fetchData();  // Quên await! Promise rejection không bị catch!
}

// ✅ Luôn await hoặc .catch()
async function good() {
    try {
        await fetchData();
    } catch (err) {
        handleError(err);
    }
}

// Parallel error handling an toàn
async function loadAll() {
    const results = await Promise.allSettled([
        fetchUsers(),
        fetchOrders(),
        fetchStats(),
    ]);

    const users = results[0].status === 'fulfilled' ? results[0].value : [];
    const orders = results[1].status === 'fulfilled' ? results[1].value : [];
    const stats = results[2].status === 'fulfilled' ? results[2].value : null;

    return { users, orders, stats };
}
```

---

## 7. Async Patterns thực tế

### Queue — Xử lý tuần tự

```javascript
class AsyncQueue {
    #queue = [];
    #processing = false;

    async add(task) {
        this.#queue.push(task);
        if (!this.#processing) await this.#process();
    }

    async #process() {
        this.#processing = true;
        while (this.#queue.length > 0) {
            const task = this.#queue.shift();
            await task();
        }
        this.#processing = false;
    }
}

const queue = new AsyncQueue();
queue.add(() => sendEmail('user1@mail.com'));
queue.add(() => sendEmail('user2@mail.com'));
// Gửi email 1 → xong → gửi email 2 (không bị trùng!)
```

### Throttle & Debounce

```javascript
// Debounce: chờ user ngừng gõ rồi mới chạy
function debounce(fn, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), delay);
    };
}
const search = debounce(query => fetchResults(query), 300);

// Throttle: chạy tối đa 1 lần mỗi N ms
function throttle(fn, limit) {
    let lastRun = 0;
    return function (...args) {
        const now = Date.now();
        if (now - lastRun >= limit) {
            lastRun = now;
            return fn.apply(this, args);
        }
    };
}
const onScroll = throttle(() => updatePosition(), 100);
```

---

## 8. Async trong ngôn ngữ khác

### Python asyncio

```python
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        # Parallel — giống Promise.all
        tasks = [
            fetch(session, 'https://api.example.com/users'),
            fetch(session, 'https://api.example.com/orders'),
            fetch(session, 'https://api.example.com/stats'),
        ]
        users, orders, stats = await asyncio.gather(*tasks)

asyncio.run(main())
```

### Go Goroutines & Channels

Go dùng **goroutines** (lightweight threads) + **channels** (giao tiếp):

```go
package main

import (
    "fmt"
    "time"
)

func fetchData(name string, ch chan<- string) {
    time.Sleep(1 * time.Second) // Giả lập I/O
    ch <- fmt.Sprintf("Dữ liệu từ %s", name)
}

func main() {
    ch := make(chan string, 3)

    // Khởi chạy 3 goroutines song song
    go fetchData("API 1", ch)
    go fetchData("API 2", ch)
    go fetchData("API 3", ch)

    // Nhận kết quả
    for i := 0; i < 3; i++ {
        fmt.Println(<-ch)
    }
    // Tổng ~1 giây (song song), không phải 3 giây!
}
```

---

## 9. Backpressure — Khi Producer nhanh hơn Consumer

```
Producer (nhanh) ────► Buffer ────► Consumer (chậm)
  1000 msg/s            ▲           100 msg/s
                        │
                  Buffer đầy → OOM!
```

**Giải pháp:**
- **Buffered queue** — Giới hạn kích thước buffer
- **Rate limiting** — Giới hạn tốc độ producer
- **Dropping** — Bỏ message cũ khi buffer đầy
- **Reactive Streams** — Consumer báo cho producer biết "tôi chỉ xử lý được 100/s"

---

## So sánh mô hình async

| Mô hình | Ngôn ngữ | Đặc điểm |
|---|---|---|
| **Event Loop** | JavaScript, Python | Single-thread, callback/async-await |
| **Goroutines** | Go | Lightweight threads (~2KB), channels |
| **Actors** | Elixir, Akka | Mỗi actor là process riêng, message passing |
| **Threads** | Java, C++ | OS threads (~1MB), shared memory, locks |
| **Coroutines** | Kotlin, Python | Cooperative multitasking, suspend/resume |

---

## Các lỗi thường gặp

```
❌ Sai: await trong vòng for → tuần tự, không tận dụng async
✅ Đúng: Dùng Promise.all() hoặc asyncio.gather() để chạy song song

❌ Sai: Quên try/catch cho async → lỗi "unhandled rejection"
✅ Đúng: LUÔN wrap async code trong try/catch

❌ Sai: Blocking event loop bằng tính toán nặng (CPU-bound)
✅ Đúng: Dùng Worker Threads (JS) hoặc multiprocessing (Python) cho CPU-bound

❌ Sai: Fire-and-forget → mất lỗi
✅ Đúng: Track Promise, handle rejection
```

---

## Bài tập thực hành

- [ ] Refactor callback hell → async/await
- [ ] Implement: fetchWithRetry (exponential backoff)
- [ ] Viết debounce + throttle từ đầu
- [ ] Promise.allSettled: load dashboard data an toàn
- [ ] Viết script Python dùng asyncio tải 10 URLs song song
- [ ] Dự đoán output của code có setTimeout, Promise, console.log (Event Loop quiz)

---

## Tài nguyên thêm

- [What the heck is the Event Loop?](https://www.youtube.com/watch?v=8aGhZQkoFbQ) — Philip Roberts (JSConf) — Video hay nhất
- [JavaScript Visualized: Promises & Async/Await](https://dev.to/lydiahallie/javascript-visualized-promises-async-await-5gke) — Lydia Hallie
- [Concurrency is not Parallelism](https://go.dev/blog/waza-talk) — Rob Pike (Go)
- [JavaScript.info: Promises](https://javascript.info/promise-basics)
- [MDN: Async/Await](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous)
