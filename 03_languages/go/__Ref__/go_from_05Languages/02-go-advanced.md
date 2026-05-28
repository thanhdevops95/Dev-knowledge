# 🔄 Go nâng cao — Concurrency, Interfaces & Patterns

> `[INTERMEDIATE → ADVANCED]` — Viết Go production-grade

---

## 1. Goroutines & Channels — Deep Dive

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

// Fan-out / Fan-in pattern
func producer(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for _, n := range nums {
            out <- n
        }
    }()
    return out
}

func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            out <- n * n
        }
    }()
    return out
}

func merge(channels ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    out := make(chan int)

    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan int) {
            defer wg.Done()
            for v := range c {
                out <- v
            }
        }(ch)
    }

    go func() {
        wg.Wait()
        close(out)
    }()
    return out
}

func main() {
    nums := producer(1, 2, 3, 4, 5)

    // Fan-out: 3 workers cùng xử lý
    w1 := square(nums)
    w2 := square(nums)
    w3 := square(nums)

    // Fan-in: gộp kết quả
    for result := range merge(w1, w2, w3) {
        fmt.Println(result)
    }
}
```

---

## 2. Context — Cancellation & Timeout

```go
import (
    "context"
    "fmt"
    "net/http"
    "time"
)

// Timeout cho HTTP request
func fetchWithTimeout(url string) (string, error) {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return "", err  // Timeout hoặc cancel
    }
    defer resp.Body.Close()

    body, _ := io.ReadAll(resp.Body)
    return string(body), nil
}

// Cancellation pattern
func longRunningTask(ctx context.Context) error {
    for i := 0; i < 100; i++ {
        select {
        case <-ctx.Done():
            return ctx.Err()  // Bị cancel → dọn dẹp và thoát
        default:
            // Làm việc...
            time.Sleep(100 * time.Millisecond)
        }
    }
    return nil
}

// Sử dụng
ctx, cancel := context.WithCancel(context.Background())
go func() {
    time.Sleep(2 * time.Second)
    cancel()  // Cancel sau 2 giây
}()
err := longRunningTask(ctx)
// err = context.Canceled
```

---

## 3. Interfaces — Duck Typing

```go
// Interface = contract. Implicit implementation (không cần "implements")
type Writer interface {
    Write(p []byte) (n int, err error)
}

type Logger interface {
    Log(msg string)
}

// Bất kỳ struct nào có method Write() đều thỏa Writer interface
type FileWriter struct {
    filename string
}

func (fw *FileWriter) Write(p []byte) (int, error) {
    return os.WriteFile(fw.filename, p, 0644), nil
}

type ConsoleWriter struct{}

func (cw *ConsoleWriter) Write(p []byte) (int, error) {
    return fmt.Print(string(p))
}

// Dùng interface → không phụ thuộc implementation cụ thể
func SaveData(w Writer, data []byte) error {
    _, err := w.Write(data)
    return err
}

SaveData(&FileWriter{"log.txt"}, []byte("hello"))
SaveData(&ConsoleWriter{}, []byte("hello"))
// Cùng function, khác behavior!

// Empty interface = any type
func printAnything(v interface{}) {
    fmt.Println(v)
}
// Go 1.18+: dùng `any` thay `interface{}`
```

---

## 4. Error Handling Patterns

```go
import (
    "errors"
    "fmt"
)

// Custom error types
type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s with ID %s not found", e.Resource, e.ID)
}

// Sentinel errors
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrForbidden    = errors.New("forbidden")
)

// Wrapping errors (Go 1.13+)
func getUserByID(id string) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, fmt.Errorf("getUserByID(%s): %w", id, err)
        // %w wraps error → giữ nguyên error gốc
    }
    return user, nil
}

// Checking wrapped errors
func handler(w http.ResponseWriter, r *http.Request) {
    user, err := getUserByID(id)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            http.Error(w, "User not found", 404)
            return
        }
        var notFound *NotFoundError
        if errors.As(err, &notFound) {
            http.Error(w, notFound.Error(), 404)
            return
        }
        http.Error(w, "Internal error", 500)
    }
}
```

---

## 5. Generics (Go 1.18+)

```go
// Generic function
func Filter[T any](slice []T, predicate func(T) bool) []T {
    result := make([]T, 0)
    for _, v := range slice {
        if predicate(v) {
            result = append(result, v)
        }
    }
    return result
}

func Map[T any, U any](slice []T, transform func(T) U) []U {
    result := make([]U, len(slice))
    for i, v := range slice {
        result[i] = transform(v)
    }
    return result
}

// Sử dụng
numbers := []int{1, 2, 3, 4, 5}
evens := Filter(numbers, func(n int) bool { return n%2 == 0 })
// [2, 4]

doubled := Map(numbers, func(n int) int { return n * 2 })
// [2, 4, 6, 8, 10]

// Constrained generics
type Number interface {
    int | int64 | float64
}

func Sum[T Number](nums []T) T {
    var total T
    for _, n := range nums {
        total += n
    }
    return total
}
```

---

## 6. HTTP Server Production

```go
package main

import (
    "encoding/json"
    "log"
    "net/http"
    "time"
)

type Server struct {
    router *http.ServeMux
    db     *sql.DB
}

func NewServer(db *sql.DB) *Server {
    s := &Server{
        router: http.NewServeMux(),
        db:     db,
    }
    s.routes()
    return s
}

func (s *Server) routes() {
    s.router.HandleFunc("GET /api/users", s.handleGetUsers)
    s.router.HandleFunc("POST /api/users", s.handleCreateUser)
    s.router.HandleFunc("GET /api/users/{id}", s.handleGetUser)
}

func (s *Server) handleGetUsers(w http.ResponseWriter, r *http.Request) {
    users, err := s.db.Query("SELECT id, name, email FROM users")
    if err != nil {
        http.Error(w, "Internal error", 500)
        return
    }
    json.NewEncoder(w).Encode(users)
}

// Middleware
func logging(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(start))
    })
}

func main() {
    db := connectDB()
    srv := NewServer(db)

    server := &http.Server{
        Addr:         ":8080",
        Handler:      logging(srv.router),
        ReadTimeout:  5 * time.Second,
        WriteTimeout: 10 * time.Second,
        IdleTimeout:  120 * time.Second,
    }

    log.Println("Server running on :8080")
    log.Fatal(server.ListenAndServe())
}
```

---

## Các lỗi thường gặp

```go
// ❌ Goroutine leak: không close channel
ch := make(chan int)
go func() {
    for { ch <- 1 } // Goroutine chạy mãi!
}()

// ✅ Dùng context hoặc done channel
go func() {
    for {
        select {
        case ch <- 1:
        case <-done:
            return
        }
    }
}()

// ❌ Race condition
var counter int
go func() { counter++ }()
go func() { counter++ }()

// ✅ Dùng sync.Mutex hoặc atomic
var mu sync.Mutex
go func() { mu.Lock(); counter++; mu.Unlock() }()
```

---

## Bài tập thực hành

- [ ] Fan-out/Fan-in pipeline xử lý 1000 URLs song song
- [ ] HTTP server: CRUD API + middleware (logging, auth, recovery)
- [ ] Worker pool: N goroutines xử lý jobs từ channel
- [ ] Generic: viết Filter, Map, Reduce cho Go

---

## Tài nguyên thêm

- [Go by Example](https://gobyexample.com/) — Code examples
- [Effective Go](https://go.dev/doc/effective_go) — Official best practices
- [Go Concurrency Patterns (Rob Pike)](https://www.youtube.com/watch?v=f6kdp27TYZs) — Talk
