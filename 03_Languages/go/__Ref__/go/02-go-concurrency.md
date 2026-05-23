# Go Concurrency

> **Tags:** `go` `goroutines` `channels` `sync` `context` `concurrency`
> **Level:** Intermediate | **Prerequisite:** `go/01-go-basics.md`

---

## 1. Goroutines

Goroutine = extremely lightweight concurrent function (2KB stack ban đầu, tự expand):

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func main() {
    // Launch goroutine — non-blocking
    go func() {
        fmt.Println("Hello from goroutine!")
    }()

    // Named function goroutine
    go processJob("job-1")

    // Goroutine là cheap — có thể launch hàng nghìn
    var wg sync.WaitGroup
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            // Capture id by value! (NOT i)
            fmt.Printf("Worker %d done\n", id)
        }(i)  // Pass i as argument
    }
    wg.Wait()
    fmt.Println("All workers done")
}

func processJob(name string) {
    time.Sleep(100 * time.Millisecond)
    fmt.Printf("Job %s done\n", name)
}
```

### WaitGroup
```go
var wg sync.WaitGroup

wg.Add(3)          // Expect 3 goroutines
go worker1(&wg)    // defer wg.Done()
go worker2(&wg)    // defer wg.Done()
go worker3(&wg)    // defer wg.Done()
wg.Wait()          // Block until counter = 0
```

---

## 2. Channels

Channel = typed conduit for goroutine communication (CSP model — Communicating Sequential Processes):

```go
// Unbuffered channel: send blocks until receiver ready
ch := make(chan int)

go func() {
    ch <- 42    // Send — blocks until someone receives
}()

value := <-ch   // Receive — blocks until something sent

// Buffered channel: send only blocks when buffer full
buffered := make(chan string, 10)
buffered <- "hello"   // Non-blocking if buffer not full
buffered <- "world"

fmt.Println(<-buffered)  // "hello"
fmt.Println(<-buffered)  // "world"

// Close channel + range
ch2 := make(chan int)
go func() {
    for i := 0; i < 5; i++ {
        ch2 <- i
    }
    close(ch2)    // Signal: no more values
}()

for val := range ch2 {   // Receives until channel closed
    fmt.Println(val)
}

// Check if closed
val, ok := <-ch2
if !ok {
    fmt.Println("Channel closed")
}
```

### Directional channels
```go
// chan<- T: send-only
// <-chan T: receive-only (enforced by compiler!)

func producer(out chan<- int) {
    for i := 0; i < 5; i++ {
        out <- i
    }
    close(out)
}

func consumer(in <-chan int) {
    for val := range in {
        fmt.Println(val)
    }
}

func main() {
    ch := make(chan int, 5)  // Bidirectional in main
    go producer(ch)   // Implicitly converted to chan<-
    consumer(ch)      // Implicitly converted to <-chan
}
```

---

## 3. Select — Multiplexing Channels

```go
// select = non-deterministic choice between channel operations
select {
case msg := <-ch1:
    fmt.Println("Received from ch1:", msg)
case ch2 <- "hello":
    fmt.Println("Sent to ch2")
case <-time.After(1 * time.Second):
    fmt.Println("Timeout!")
default:
    fmt.Println("No channels ready") // Non-blocking select
}

// Fan-in: merge multiple channels into one
func merge(ch1, ch2 <-chan int) <-chan int {
    out := make(chan int)
    var wg sync.WaitGroup

    forward := func(in <-chan int) {
        defer wg.Done()
        for val := range in {
            out <- val
        }
    }

    wg.Add(2)
    go forward(ch1)
    go forward(ch2)

    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}

// Quit signal pattern
func generator(quit <-chan struct{}) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for i := 0; ; i++ {
            select {
            case out <- i:
                // Keep generating
            case <-quit:
                fmt.Println("Generator stopping")
                return
            }
        }
    }()
    return out
}
```

---

## 4. Mutex & sync package

```go
import "sync"

// Mutex — protect shared state
type SafeCounter struct {
    mu sync.Mutex
    v  map[string]int
}

func (c *SafeCounter) Inc(key string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.v[key]++
}

func (c *SafeCounter) Value(key string) int {
    c.mu.RLock()   // RWMutex: multiple readers OR one writer
    defer c.mu.RUnlock()
    return c.v[key]
}

// sync.Once — run exactly once (singleton init)
var (
    instance *Database
    once     sync.Once
)

func GetDB() *Database {
    once.Do(func() {
        instance = &Database{...}
    })
    return instance
}

// sync.Map — concurrent-safe map
var m sync.Map

m.Store("key", "value")
val, ok := m.Load("key")
m.LoadOrStore("key", "default")
m.Delete("key")
m.Range(func(k, v any) bool {
    fmt.Println(k, v)
    return true  // Return false to stop iteration
})
```

---

## 5. Context — Cancellation & Timeout

```go
import (
    "context"
    "time"
)

// context.WithCancel — manual cancellation
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()   // Always call cancel to free resources

    go worker(ctx)

    time.Sleep(2 * time.Second)
    cancel()   // Signal all workers to stop
}

func worker(ctx context.Context) {
    for {
        select {
        case <-ctx.Done():
            fmt.Println("Worker stopping:", ctx.Err())
            return
        default:
            doWork()
        }
    }
}

// context.WithTimeout — auto-cancel after duration
func fetchData(url string) ([]byte, error) {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        // err wraps context.DeadlineExceeded if timeout
        return nil, fmt.Errorf("fetch failed: %w", err)
    }
    defer resp.Body.Close()
    return io.ReadAll(resp.Body)
}

// context.WithValue — pass request-scoped values
type contextKey string

const (
    UserIDKey   contextKey = "userID"
    TraceIDKey  contextKey = "traceID"
)

func withUser(ctx context.Context, userID int) context.Context {
    return context.WithValue(ctx, UserIDKey, userID)
}

func getUserID(ctx context.Context) (int, bool) {
    id, ok := ctx.Value(UserIDKey).(int)
    return id, ok
}

// HTTP handler pattern
func handler(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    ctx = withUser(ctx, getCurrentUser(r).ID)
    ctx = context.WithValue(ctx, TraceIDKey, generateTraceID())

    result, err := processRequest(ctx)
    // ... ctx is passed through the entire call stack
}
```

---

## 6. Worker Pool Pattern

```go
// Classic worker pool
func workerPool(jobs <-chan Job, results chan<- Result, numWorkers int) {
    var wg sync.WaitGroup
    
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func(workerID int) {
            defer wg.Done()
            for job := range jobs {
                result := processJob(job)
                results <- result
            }
        }(i)
    }

    go func() {
        wg.Wait()
        close(results)
    }()
}

func main() {
    numJobs := 100
    numWorkers := 10

    jobs := make(chan Job, numJobs)
    results := make(chan Result, numJobs)

    // Start pool
    workerPool(jobs, results, numWorkers)

    // Send jobs
    go func() {
        for i := 0; i < numJobs; i++ {
            jobs <- Job{ID: i, Data: i * 2}
        }
        close(jobs)
    }()

    // Collect results
    for result := range results {
        fmt.Printf("Result: %v\n", result)
    }
}
```

---

## 7. errgroup — Goroutines with Error Handling

```go
import "golang.org/x/sync/errgroup"

func fetchAll(ctx context.Context, urls []string) ([][]byte, error) {
    g, ctx := errgroup.WithContext(ctx)
    results := make([][]byte, len(urls))

    for i, url := range urls {
        i, url := i, url  // Capture loop variables
        g.Go(func() error {
            data, err := fetchURL(ctx, url)
            if err != nil {
                return fmt.Errorf("fetch %q: %w", url, err)
            }
            results[i] = data
            return nil
        })
    }

    if err := g.Wait(); err != nil {
        return nil, err   // First non-nil error
    }
    return results, nil
}
```

---

## 8. sync.Pool — Reuse Objects

```go
var bufPool = sync.Pool{
    New: func() any {
        return &bytes.Buffer{}
    },
}

func processRequest(data []byte) string {
    // Get buffer from pool (or create new if empty)
    buf := bufPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufPool.Put(buf)   // Return to pool
    }()

    buf.Write(data)
    // ... process
    return buf.String()
}
```

---

## 9. Race Detector

```bash
# Go has built-in race detector!
go test -race ./...
go run -race main.go

# Output example when race detected:
# ==================
# WARNING: DATA RACE
# Write at 0x00c000016070 by goroutine 7:
#   main.main.func1()
# Previous read at 0x00c000016070 by goroutine 6:
#   main.main.func2()
```

---

## 10. Concurrency Patterns Cheatsheet

```go
// Pipeline
gen := func(nums ...int) <-chan int { /* send nums to channel */ }
sq := func(in <-chan int) <-chan int { /* square each */ }

// Chain
c := gen(2, 3)
out := sq(sq(c))   // 2 → 4 → 16, 3 → 9 → 81

// Fan-out (same input → multiple workers)
in := gen(1, 2, 3, 4, 5)
c1 := process(in)
c2 := process(in)  // Both consume from same channel

// Done channel (quit signal)
done := make(chan struct{})
// Select with done check in every goroutine

// Timeout per operation
select {
case result := <-workCh:
    use(result)
case <-time.After(100 * time.Millisecond):
    // Handle slow operation
}

// Heartbeat
ticker := time.NewTicker(1 * time.Second)
defer ticker.Stop()
for {
    select {
    case <-ctx.Done():
        return
    case <-ticker.C:
        ping()
    case job := <-jobs:
        handle(job)
    }
}
```

---

## 11. Bài tập

1. **Concurrent web scraper**: Tạo scraper fetch 100 URLs với controlled concurrency (max 10 concurrent).
2. **Pipeline**: Implement processing pipeline với 3 stages — generate numbers → filter primes → square them.
3. **Rate limiter**: Implement token bucket rate limiter dùng channels.
4. **Timeout retry**: Tạo function retry với exponential backoff và context cancellation.
5. **Pub/Sub**: Implement simple pub/sub system dùng channels và goroutines.

---

*Tài liệu liên quan: `go/01-go-basics.md` | `go/03-go-tooling.md` | `programming/07-concurrency-patterns.md`*
