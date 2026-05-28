# ⚙️ Concurrency Patterns — Mẫu thiết kế xử lý đồng thời

> `[ADVANCED]` — Prerequisite: `cs/03-concurrency-parallelism-fundamentals.md`
> Các pattern tái sử dụng để xử lý concurrent workloads trong production.

---

## Tại sao cần Concurrency Patterns?

Khi xây dựng hệ thống thực tế — web server xử lý hàng nghìn request, pipeline xử lý data, hoặc game engine render 60fps — bạn không thể "tự nghĩ" cách tổ chức concurrency mỗi lần. **Concurrency patterns** là những giải pháp đã được chứng minh, giúp bạn tránh deadlock, race condition, và viết code ổn định hơn.

Hãy nghĩ về concurrency patterns như **"công thức nấu ăn"** cho xử lý song song: mỗi pattern giải quyết một loại bài toán cụ thể. Thay vì tự sáng chế, bạn chọn pattern phù hợp.

```
Bài toán concurrency nào?
│
├─ Nhiều task cùng loại, cần giới hạn resources?
│  → Thread Pool
│
├─ Producer tạo data, Consumer xử lý?
│  → Producer-Consumer
│
├─ I/O-bound, cần xử lý hàng nghìn connections?
│  → Reactor Pattern (Event-driven)
│
├─ Async I/O với completion notification?
│  → Proactor Pattern
│
├─ Mix sync + async trong cùng hệ thống?
│  → Half-Sync/Half-Async
│
├─ Decouple method invocation khỏi execution?
│  → Active Object
│
└─ Synchronized access với condition waiting?
   → Monitor Object
```

---

## 1. Thread Pool — Tái sử dụng threads

### Vấn đề

Tạo thread mới cho mỗi task rất **tốn kém**: mỗi thread cần ~1MB stack memory, OS phải context switch, và tạo/hủy thread có overhead. Nếu có 10,000 requests đồng thời → 10,000 threads → **hết RAM**.

### Giải pháp

Tạo sẵn **N threads** (pool), các task được đưa vào **queue**. Thread rảnh lấy task từ queue để xử lý. Khi xong, thread quay lại pool chờ task tiếp.

```
            ┌─── Thread 1 ──→ [processing task A]
            │
Task Queue  ├─── Thread 2 ──→ [processing task B]
[D][C][...] │
            ├─── Thread 3 ──→ [idle, waiting]
            │
            └─── Thread 4 ──→ [processing task C]
```

### Implementation

```python
from concurrent.futures import ThreadPoolExecutor
import time

def process_order(order_id: int) -> str:
    """Simulate processing an order (I/O-bound: DB query, API call)."""
    time.sleep(0.5)  # Simulate I/O
    return f"Order {order_id} processed"

# Thread Pool với tối đa 4 workers
with ThreadPoolExecutor(max_workers=4) as pool:
    # Submit 10 orders — chỉ 4 chạy song song
    futures = [pool.submit(process_order, i) for i in range(10)]
    
    for future in futures:
        print(future.result())  # Block until done

# Không cần 10 threads — 4 threads xử lý luân phiên
```

```java
// Java ThreadPoolExecutor
ExecutorService pool = Executors.newFixedThreadPool(4);

for (int i = 0; i < 10; i++) {
    final int orderId = i;
    pool.submit(() -> {
        System.out.println("Processing order " + orderId);
        Thread.sleep(500);
    });
}

pool.shutdown();
pool.awaitTermination(1, TimeUnit.MINUTES);
```

### Sizing — Bao nhiêu threads?

```
CPU-bound tasks:  pool_size = CPU cores (hoặc cores + 1)
I/O-bound tasks:  pool_size = CPU cores × (1 + wait_time / compute_time)

Ví dụ: 4 cores, I/O wait 200ms, compute 50ms
→ pool_size = 4 × (1 + 200/50) = 20 threads

Quy tắc ngón tay cái:
- CPU-bound: cores × 1
- I/O-bound: cores × 5~10
- Mixed: benchmark để tìm optimal
```

---

## 2. Producer-Consumer — Bounded Buffer

### Vấn đề

Một component **tạo dữ liệu** (producer) và component khác **xử lý dữ liệu** (consumer). Tốc độ produce và consume **khác nhau** — cần buffer ở giữa để tránh mất data hoặc producer phải chờ.

### Giải pháp

Dùng **blocking queue** (bounded buffer) ở giữa. Producer đẩy vào queue, Consumer lấy từ queue. Queue đầy → Producer chờ. Queue rỗng → Consumer chờ.

```
Producer 1 ──→ ┌─────────────┐ ──→ Consumer 1
Producer 2 ──→ │ Blocking    │ ──→ Consumer 2
Producer 3 ──→ │ Queue (N)   │ ──→ Consumer 3
               └─────────────┘
               Bounded buffer
```

```python
import queue
import threading
import time

# Bounded buffer — tối đa 5 items
buffer = queue.Queue(maxsize=5)

def producer(name: str, items: list):
    for item in items:
        buffer.put(item)  # Block nếu queue đầy
        print(f"[{name}] Produced: {item}")
        time.sleep(0.1)
    buffer.put(None)  # Sentinel: báo hiệu done

def consumer(name: str):
    while True:
        item = buffer.get()  # Block nếu queue rỗng
        if item is None:
            break
        print(f"  [{name}] Consumed: {item}")
        time.sleep(0.3)  # Consumer chậm hơn producer

# 1 producer, 2 consumers
producer_thread = threading.Thread(
    target=producer, args=("P1", ["order_1", "order_2", "order_3", "order_4"])
)
consumer_threads = [
    threading.Thread(target=consumer, args=(f"C{i}",))
    for i in range(2)
]

producer_thread.start()
for t in consumer_threads:
    t.start()

producer_thread.join()
for t in consumer_threads:
    t.join()
```

```go
// Go — channels là built-in Producer-Consumer
func main() {
    orders := make(chan string, 5) // Buffered channel (size 5)
    
    // Producer
    go func() {
        for i := 0; i < 10; i++ {
            order := fmt.Sprintf("order_%d", i)
            orders <- order // Block nếu channel đầy
            fmt.Println("Produced:", order)
        }
        close(orders) // Signal done
    }()
    
    // Consumer
    for order := range orders { // Block nếu channel rỗng
        fmt.Println("  Consumed:", order)
        time.Sleep(100 * time.Millisecond)
    }
}
```

### Ứng dụng thực tế

- **Kafka**: Producer gửi messages → Topic (buffer) → Consumer groups xử lý
- **Celery/BullMQ**: Web server đẩy task → Queue (Redis) → Workers xử lý
- **Log pipeline**: App ghi log → Buffer → Elasticsearch/S3

---

## 3. Reactor Pattern — Event-driven I/O

### Vấn đề

Web server cần xử lý **hàng nghìn connections** đồng thời. Thread-per-connection không scale (C10K problem). Cần cách xử lý I/O mà **không block thread**.

### Giải pháp: Event Loop + I/O Multiplexing

**Reactor** dùng **1 thread** (hoặc ít threads) kết hợp **I/O multiplexing** (epoll/kqueue) để theo dõi nhiều file descriptors (sockets). Khi có event (data ready, connection new) → dispatch đến handler tương ứng.

```
              ┌──────────────────────────┐
              │      Event Loop          │
              │   (single thread)        │
              │                          │
  Sockets ──→ │  epoll_wait() / kqueue   │
  (1000s)     │       ↓                  │
              │  Event ready?            │
              │    ├─ READ  → onRead()   │
              │    ├─ WRITE → onWrite()  │
              │    └─ CONN  → onAccept() │
              └──────────────────────────┘
```

```python
# Python asyncio — Reactor pattern built-in
import asyncio

async def handle_client(reader, writer):
    """Handle one client connection — non-blocking."""
    data = await reader.read(1024)  # Non-blocking read
    message = data.decode()
    
    response = f"Echo: {message}"
    writer.write(response.encode())
    await writer.drain()  # Non-blocking write
    writer.close()

async def main():
    # Event loop manages all connections with 1 thread
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8080)
    async with server:
        await server.serve_forever()

asyncio.run(main())
```

### Ai dùng Reactor?

| Runtime/Framework | I/O Multiplexer | Mô tả |
|---|---|---|
| **Node.js** | libuv (epoll/kqueue/IOCP) | Single-threaded event loop |
| **Python asyncio** | selectors (epoll/kqueue) | async/await syntax |
| **Nginx** | epoll (Linux) | Event-driven web server |
| **Redis** | ae (epoll/kqueue) | Single-threaded, I/O multiplexing |
| **Netty (Java)** | NIO (epoll) | High-performance networking |

---

## 4. Proactor Pattern — Async I/O Completion

### Khác biệt với Reactor

| | Reactor | Proactor |
|---|---|---|
| **Khi nào notify?** | "Data **sẵn sàng** để đọc" | "OS đã **đọc xong** data cho bạn" |
| **Ai đọc data?** | Application (sau khi nhận notify) | OS/Kernel (trước khi notify) |
| **Ví dụ** | epoll (Linux), kqueue (macOS) | IOCP (Windows), io_uring (Linux 5.1+) |

```
Reactor:  App waits → "data ready" → App reads → processes
Proactor: App submits read → OS reads → "read complete" → App processes
                                        ↑ OS đã copy data vào buffer
```

### io_uring (Linux) — Proactor hiện đại

```c
// Pseudocode — io_uring async read
struct io_uring ring;
io_uring_queue_init(32, &ring, 0);

// Submit async read request
struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
io_uring_prep_read(sqe, fd, buffer, size, offset);
io_uring_submit(&ring);

// Wait for completion (OS đã đọc xong!)
struct io_uring_cqe *cqe;
io_uring_wait_cqe(&ring, &cqe);
// buffer đã có data — xử lý ngay, không cần read()
```

**Ưu điểm Proactor:** Ít system calls hơn (OS batch I/O operations), phù hợp cho extremely high throughput.

---

## 5. Half-Sync/Half-Async — Chia tầng Sync/Async

### Vấn đề

Hệ thống có cả phần **async** (network I/O) và phần **sync** (business logic phức tạp). Trộn 2 loại code gây khó đọc và dễ bug.

### Giải pháp

Chia thành 2 tầng rõ ràng, nối bằng **queue**:

```
┌─────────────────────┐
│   Async Layer       │  ← Event-driven, non-blocking
│   (I/O handling)    │     (Reactor/Proactor)
│                     │
│   Network events    │
└────────┬────────────┘
         │ Queue (bounded buffer)
┌────────▼────────────┐
│   Sync Layer        │  ← Thread pool, blocking OK
│   (Business logic)  │     (Sequential, easy to reason)
│                     │
│   Process requests  │
└─────────────────────┘
```

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

# Sync layer — business logic phức tạp (CPU-bound)
def process_order_sync(order_data: dict) -> dict:
    """Complex business logic — runs in thread pool."""
    time.sleep(0.5)  # Simulate heavy computation
    return {"status": "processed", "total": order_data["amount"] * 1.08}

# Async layer — I/O handling
async def handle_request(reader, writer):
    """Async I/O layer — receives request."""
    data = await reader.read(4096)
    order = json.loads(data)
    
    # Bridge: async → sync via thread pool
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        thread_pool,  # Sync layer
        process_order_sync, order
    )
    
    writer.write(json.dumps(result).encode())
    await writer.drain()
    writer.close()

thread_pool = ThreadPoolExecutor(max_workers=8)  # Sync layer
```

### Ví dụ thực tế

- **Node.js + Worker Threads**: Event loop (async) + CPU-heavy tasks in workers (sync)
- **Nginx + uWSGI**: Nginx handles connections (async) → uWSGI processes requests (sync)
- **LMAX Disruptor**: Network I/O (async) → Ring buffer → Business logic (sync)

---

## 6. Active Object — Decouple invocation từ execution

### Vấn đề

Bạn muốn gọi method trên object từ nhiều threads, nhưng không muốn dùng locks (phức tạp, dễ deadlock). Cần object tự quản lý concurrency.

### Giải pháp

Active Object có **thread riêng** + **message queue**. Method calls được chuyển thành messages trong queue, object xử lý tuần tự trong thread riêng.

```
Thread A ──→ proxy.doWork(x) ──→ ┌──────────┐
Thread B ──→ proxy.doWork(y) ──→ │  Queue    │ ──→ Active Object Thread
Thread C ──→ proxy.doWork(z) ──→ │ [x][y][z] │     (xử lý tuần tự)
                                 └──────────┘
```

```python
import queue
import threading
from concurrent.futures import Future

class ActiveObject:
    """Object with its own thread — no external locking needed."""
    
    def __init__(self):
        self._queue = queue.Queue()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
    
    def _run(self):
        """Private thread — processes messages sequentially."""
        while True:
            func, args, future = self._queue.get()
            if func is None:
                break
            try:
                result = func(*args)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
    
    def submit(self, func, *args) -> Future:
        """Submit work — returns Future, non-blocking."""
        future = Future()
        self._queue.put((func, args, future))
        return future

# Usage — multiple threads call, no locks needed
account = ActiveObject()

# Từ Thread A
future1 = account.submit(lambda: deposit(100))

# Từ Thread B  
future2 = account.submit(lambda: withdraw(50))

# Không race condition — xử lý tuần tự trong Active Object thread
print(future1.result())
print(future2.result())
```

### Liên hệ

- **Erlang/Elixir Processes**: Mỗi process = Active Object với mailbox
- **Akka Actors (Scala/Java)**: Actor = Active Object pattern
- **Go goroutines + channels**: Goroutine đọc từ channel = tương tự

---

## 7. Monitor Object — Synchronized methods với condition

### Vấn đề

Nhiều threads cần truy cập shared resource, nhưng cần **đợi điều kiện** (VD: buffer không rỗng) trước khi tiến hành.

### Giải pháp

Monitor = Mutex + Condition Variable. Lock bảo vệ data, condition variable cho phép threads **chờ** và **được đánh thức** khi điều kiện thay đổi.

```python
import threading

class BoundedBuffer:
    """Thread-safe bounded buffer using Monitor pattern."""
    
    def __init__(self, capacity: int):
        self._buffer = []
        self._capacity = capacity
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)
        self._not_empty = threading.Condition(self._lock)
    
    def put(self, item):
        with self._not_full:
            while len(self._buffer) >= self._capacity:
                self._not_full.wait()  # Release lock & sleep
            
            self._buffer.append(item)
            self._not_empty.notify()  # Wake up waiting consumers
    
    def get(self):
        with self._not_empty:
            while len(self._buffer) == 0:
                self._not_empty.wait()  # Release lock & sleep
            
            item = self._buffer.pop(0)
            self._not_full.notify()  # Wake up waiting producers
            return item
```

```java
// Java synchronized + wait/notify = Monitor
public class BoundedBuffer<T> {
    private final Queue<T> buffer = new LinkedList<>();
    private final int capacity;
    
    public synchronized void put(T item) throws InterruptedException {
        while (buffer.size() >= capacity) {
            wait();  // Release monitor, wait
        }
        buffer.add(item);
        notifyAll();  // Wake up waiting threads
    }
    
    public synchronized T get() throws InterruptedException {
        while (buffer.isEmpty()) {
            wait();
        }
        T item = buffer.poll();
        notifyAll();
        return item;
    }
}
```

---

## 8. Bảng so sánh patterns

| Pattern | Bài toán | Key mechanism | Use case |
|---|---|---|---|
| **Thread Pool** | Giới hạn concurrent tasks | Fixed threads + task queue | Web servers, batch processing |
| **Producer-Consumer** | Decouple produce/consume speed | Bounded buffer / blocking queue | Message queues, ETL pipelines |
| **Reactor** | Handle 10K+ connections | Event loop + I/O multiplexing | Node.js, Nginx, Redis |
| **Proactor** | True async I/O | OS-level async + completion | IOCP (Windows), io_uring |
| **Half-Sync/Half-Async** | Mix sync + async code | Queue bridge giữa 2 layers | Web app (async I/O + sync logic) |
| **Active Object** | Thread-safe object | Private thread + message queue | Actors (Erlang, Akka) |
| **Monitor** | Conditional synchronization | Mutex + condition variable | Shared resources with conditions |

### Khi nào dùng pattern nào?

```
Web server (HTTP)?
  → Reactor (event loop) + Thread Pool (handlers)

Message processing system?
  → Producer-Consumer + Thread Pool

Game server (real-time)?
  → Reactor + Active Object (per-player state)

Financial trading system?
  → Proactor (lowest latency) + Monitor (order book)

Microservices?
  → Producer-Consumer (Kafka) + Thread Pool (workers)
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Thread pool quá lớn cho CPU-bound | Pool size = CPU cores | Quá nhiều threads → context switch overhead |
| 2 | Unbounded queue trong Producer-Consumer | Luôn dùng bounded queue | Unbounded → memory leak khi producer nhanh hơn consumer |
| 3 | Blocking I/O trong Reactor event loop | Mọi I/O phải non-blocking | 1 blocking call → toàn bộ server bị block |
| 4 | Quên handle poison pill / shutdown signal | Luôn có graceful shutdown mechanism | Thread pool / Active Object không bao giờ tắt |
| 5 | notify() thay vì notifyAll() trong Monitor | Dùng notifyAll() khi có nhiều loại waiter | notify() có thể đánh thức sai thread |

---

## Bài tập thực hành

- [ ] **Bài 1 (Trung bình):** Implement Thread Pool từ đầu bằng Python (không dùng `concurrent.futures`). Hỗ trợ submit, shutdown, và result retrieval.
- [ ] **Bài 2 (Trung bình):** Viết Producer-Consumer pipeline: Producer đọc file CSV, Consumer xử lý từng row và ghi kết quả. Dùng bounded queue.
- [ ] **Bài 3 (Khó):** Implement Active Object pattern cho Bank Account. Test với 10 threads deposit/withdraw đồng thời — verify balance luôn đúng.
- [ ] **Bài 4 (Khó):** Viết simple HTTP server dùng Reactor pattern (asyncio). Support 1000 concurrent connections.

---

## Tài nguyên thêm

- [Pattern-Oriented Software Architecture Vol. 2](https://www.wiley.com/en-us/Pattern+Oriented+Software+Architecture%2C+Volume+2-p-9780471606956) — "Bible" concurrency patterns
- [Java Concurrency in Practice (Goetz)](https://jcip.net/) — Gold standard cho Java concurrency
- [Go Concurrency Patterns (Rob Pike)](https://www.youtube.com/watch?v=f6kdp27TYZs) — Google I/O talk
- [libuv Design Overview](https://docs.libuv.org/en/v1.x/design.html) — Node.js event loop internals
- [The LMAX Architecture](https://martinfowler.com/articles/lmax.html) — High-performance trading system
