# Concurrency & Parallelism

> **Tags:** `concurrency` `parallelism` `threads` `async` `lock` `deadlock`
> **Level:** Intermediate | **Prerequisite:** `cs/02-os-concepts.md`

---

## 1. Concurrency vs Parallelism

```
Concurrency (đồng thời logic):          Parallelism (song song vật lý):
  Task A: ──▶ pause ──▶ resume ──▶       Task A: ─────────────────────▶
  Task B:       ──▶ pause ──▶ ──▶        Task B: ─────────────────────▶
  (1 core, interleaved)                  (2 cores, simultaneous)

"Concurrency is about dealing with lots of things at once.
 Parallelism is about doing lots of things at once." — Rob Pike
```

- **Concurrency** = cấu trúc chương trình có thể xử lý nhiều việc (không nhất thiết cùng lúc).
- **Parallelism** = thực sự thực thi nhiều việc cùng một thời điểm (cần nhiều cores/CPUs).
- Concurrency không cần Parallelism (single-core CPU), nhưng Parallelism cần Concurrency.

---

## 2. Race Condition

**Race condition** xảy ra khi kết quả phụ thuộc vào thứ tự/timing của các thread thực thi.

```python
# BUG: Race condition
counter = 0

def increment():
    global counter
    # Đây là 3 operations: READ, ADD, WRITE
    # Nếu 2 threads thực hiện đồng thời → lost update
    counter += 1

import threading
threads = [threading.Thread(target=increment) for _ in range(1000)]
for t in threads: t.start()
for t in threads: t.join()

print(counter)  # Có thể ra 987, 993, 1000... không đoán được!
```

### Fix với Lock
```python
import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    with lock:  # acquire → critical section → release
        counter += 1

threads = [threading.Thread(target=increment) for _ in range(1000)]
for t in threads: t.start()
for t in threads: t.join()

print(counter)  # Luôn là 1000
```

---

## 3. Mutex & Semaphore

### Mutex (Mutual Exclusion)
- Chỉ **1 thread** được giữ mutex tại một thời điểm.
- Thread muốn vào critical section → `lock()`, thoát ra → `unlock()`.
- **Ownership**: chỉ thread đã lock mới được unlock.

```go
// Go example
var mu sync.Mutex
var count int

func increment() {
    mu.Lock()
    defer mu.Unlock()
    count++
}
```

### Semaphore
- Có **counter** — cho phép N threads truy cập đồng thời.
- `sem.acquire()` → decrement counter (block nếu counter = 0)
- `sem.release()` → increment counter

```python
import threading

# Binary semaphore (N=1) ≈ Mutex
# Counting semaphore — giới hạn kết nối database
db_pool = threading.Semaphore(5)  # Tối đa 5 connections

def query_db():
    with db_pool:  # acquire
        # Chỉ 5 threads cùng lúc được vào đây
        result = execute_query()
    # release
    return result
```

### So sánh

| | Mutex | Semaphore |
|---|---|---|
| Counter | Binary (0/1) | N ≥ 0 |
| Ownership | Có (chỉ locker mới unlock) | Không |
| Use case | Protect shared resource | Rate limiting, producer-consumer |
| Deadlock risk | Cao hơn | Thấp hơn |

---

## 4. Deadlock

**Deadlock** = 2 hoặc nhiều threads bị block mãi mãi, mỗi thread chờ resource mà thread khác đang giữ.

### 4 Điều kiện Coffman (đủ cả 4 → deadlock)
1. **Mutual Exclusion** — resource không thể share
2. **Hold and Wait** — thread giữ ≥1 resource trong khi chờ resource khác
3. **No Preemption** — resource chỉ được release bởi thread đang giữ
4. **Circular Wait** — T1 chờ T2, T2 chờ T3, T3 chờ T1

```python
import threading

lock_a = threading.Lock()
lock_b = threading.Lock()

def thread1():
    lock_a.acquire()   # Giữ A
    time.sleep(0.1)
    lock_b.acquire()   # Chờ B → DEADLOCK nếu thread2 giữ B
    # ...
    lock_b.release()
    lock_a.release()

def thread2():
    lock_b.acquire()   # Giữ B
    time.sleep(0.1)
    lock_a.acquire()   # Chờ A → DEADLOCK nếu thread1 giữ A
    # ...
    lock_a.release()
    lock_b.release()
```

### Phòng tránh Deadlock

**1. Lock Ordering** — luôn acquire locks theo thứ tự cố định:
```python
def thread1():
    lock_a.acquire()   # Luôn A trước B
    lock_b.acquire()
    ...

def thread2():
    lock_a.acquire()   # Luôn A trước B  
    lock_b.acquire()
    ...
```

**2. Timeout**:
```python
if lock_a.acquire(timeout=1.0):
    try:
        if lock_b.acquire(timeout=1.0):
            # critical section
            lock_b.release()
    finally:
        lock_a.release()
else:
    # Handle timeout — retry or abort
```

**3. trylock / non-blocking**:
```go
if mu.TryLock() {
    defer mu.Unlock()
    // critical section
} else {
    // Do something else
}
```

---

## 5. Lock-Free Programming

Dùng **atomic operations** (CPU instructions như CAS — Compare-And-Swap) thay vì locks:

```python
from threading import atomic  # Python 3.12+
# hoặc dùng ctypes/multiprocessing.Value

# Go — atomic
import "sync/atomic"

var counter int64

func increment() {
    atomic.AddInt64(&counter, 1)
}

func compareAndSwap() {
    old := atomic.LoadInt64(&counter)
    // Chỉ set nếu giá trị vẫn == old
    swapped := atomic.CompareAndSwapInt64(&counter, old, old+1)
}
```

### Wait-free vs Lock-free
- **Lock-free**: ít nhất 1 thread luôn tiến triển (không bị starve toàn bộ)
- **Wait-free**: mọi thread đều đảm bảo tiến triển trong bounded steps

### Khi nào dùng lock-free?
✅ High contention, low latency requirements (trading systems, game engines)
❌ Phức tạp, khó đúng, dễ ABA problem

---

## 6. Event Loop (JavaScript / Python asyncio)

**Event loop** = concurrency model không dùng threads — 1 thread, nhiều I/O concurrent.

```
Event Loop:
┌─────────────────────────────────────────┐
│  while True:                            │
│    events = poll_ready_events()         │
│    for event in events:                 │
│      callback = event.handler           │
│      callback()    ← runs to completion │
└─────────────────────────────────────────┘
```

### JavaScript Event Loop chi tiết
```javascript
console.log("1");          // Sync — call stack

setTimeout(() => {
    console.log("4");      // Macro task queue (after 0ms)
}, 0);

Promise.resolve().then(() => {
    console.log("3");      // Micro task queue (runs before macro tasks)
});

console.log("2");          // Sync — call stack

// Output: 1, 2, 3, 4
// Thứ tự: Call Stack → Microtask Queue → Macrotask Queue
```

```
Call Stack   Microtask Queue    Macrotask Queue
    |               |                  |
 console.log  Promise.then()    setTimeout(cb)
 console.log       ↓                  ↓
    |          runs first       runs after micros
    ↓
   empty → check micro → check macro
```

### Python asyncio
```python
import asyncio

async def fetch_data(url: str) -> str:
    # Không block event loop — suspend task, chạy task khác
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    # Chạy 3 requests ĐỒNG THỜI (concurrent), không tuần tự
    results = await asyncio.gather(
        fetch_data("https://api1.com"),
        fetch_data("https://api2.com"),
        fetch_data("https://api3.com"),
    )

asyncio.run(main())
```

### I/O-bound vs CPU-bound

```python
# I/O-bound task: asyncio / threading là đủ
async def download_file():
    data = await aiohttp.get(url)   # Chờ network → yield control

# CPU-bound task: cần multiprocessing (thoát GIL)
import multiprocessing

def cpu_heavy(n):
    return sum(i**2 for i in range(n))

with multiprocessing.Pool() as pool:
    results = pool.map(cpu_heavy, [10**7, 10**7, 10**7])
```

---

## 7. Goroutines & Channels (Go)

Go có **goroutine** — extremely lightweight (2KB stack, grows dynamically), managed by Go runtime:

```go
// Goroutine — chạy concurrent với goroutine hiện tại
go func() {
    doSomething()
}()

// Channel — communication between goroutines (CSP model)
ch := make(chan int, 10)  // Buffered channel, capacity 10

// Producer
go func() {
    for i := 0; i < 10; i++ {
        ch <- i    // Send
    }
    close(ch)
}()

// Consumer
for val := range ch {  // Receive until channel closed
    fmt.Println(val)
}
```

### Select — multiplexing channels
```go
select {
case msg1 := <-ch1:
    fmt.Println("ch1:", msg1)
case msg2 := <-ch2:
    fmt.Println("ch2:", msg2)
case <-time.After(1 * time.Second):
    fmt.Println("timeout")
default:
    fmt.Println("no message ready")  // Non-blocking
}
```

### Worker Pool pattern
```go
func workerPool(jobs <-chan int, results chan<- int, workers int) {
    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                results <- process(job)
            }
        }()
    }
    wg.Wait()
    close(results)
}
```

---

## 8. Backpressure

**Backpressure** = cơ chế slow consumer thông báo cho fast producer giảm tốc độ.

```
Producer ──────▶ Queue ──────▶ Consumer
   fast            ↑              slow
                   │
             Queue full → producer blocks/errors
```

```python
# asyncio Queue với maxsize
queue = asyncio.Queue(maxsize=100)

async def producer():
    for item in data:
        await queue.put(item)  # Block nếu queue đầy
    
async def consumer():
    while True:
        item = await queue.get()
        await process(item)
        queue.task_done()
```

### Strategies
1. **Drop** — bỏ qua item khi queue đầy (acceptable for metrics/logs)
2. **Block** — producer chờ (đơn giản, có thể gây bottleneck)
3. **Error** — trả lỗi về producer để retry sau
4. **Batching** — gom nhiều items → giảm overhead

---

## 9. Actor Model

Thay vì shared memory + locks → **actors** giao tiếp qua messages:

```
Actor A ──message──▶ Actor B's mailbox ──▶ Actor B processes sequentially
                                           (no shared state, no locks)
```

- Mỗi actor có **mailbox** — FIFO queue
- Actors xử lý 1 message tại một thời điểm → không cần locks
- Actors có thể spawn actors khác, gửi messages

```python
# Akka-style (Python: Pykka)
import pykka

class CounterActor(pykka.ThreadingActor):
    def __init__(self):
        super().__init__()
        self.count = 0

    def on_receive(self, message):
        if message['cmd'] == 'increment':
            self.count += 1
        elif message['cmd'] == 'get':
            return self.count

actor = CounterActor.start()
actor.tell({'cmd': 'increment'})
actor.tell({'cmd': 'increment'})
count = actor.ask({'cmd': 'get'})  # Returns 2
actor.stop()
```

---

## 10. Concurrency Bugs Cheatsheet

| Bug | Mô tả | Phát hiện | Fix |
|---|---|---|---|
| **Race condition** | Kết quả phụ thuộc timing | ThreadSanitizer, Helgrind | Lock, atomic |
| **Deadlock** | Circular wait | Timeout + logging | Lock ordering |
| **Livelock** | Threads active nhưng không tiến triển | Monitor CPU + no progress | Randomized retry |
| **Starvation** | Thread không bao giờ được CPU | Monitor wait time | Fair scheduling, priority |
| **Priority inversion** | Low-priority task giữ lock cần bởi high-priority | RTOS monitoring | Priority inheritance |
| **ABA problem** | Value thay đổi A→B→A, CAS không detect | Careful design | Version tagging (ABA stamp) |

---

## 11. Bài tập

1. **Bank Transfer**: viết thread-safe bank transfer giữa 2 accounts, kiểm tra xem bạn có thể gây deadlock không?
2. **Producer-Consumer**: implement queue với Semaphore (không dùng `queue.Queue`).
3. **Dining Philosophers**: giải quyết 5 philosophers, 5 forks — tránh deadlock.
4. **Async vs Sync benchmark**: so sánh thời gian download 100 URLs với `requests` (sync) vs `aiohttp` (async).
5. **Go pipeline**: tạo pipeline: numbers → square → filter even → print.

---

*Tài liệu liên quan: `cs/02-os-concepts.md` | `programming/03-async-programming.md` | `programming/07-concurrency-patterns.md`*
