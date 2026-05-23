# 🐹 Go (Golang) — Ngôn ngữ hiệu năng cao từ Google

> `[INTERMEDIATE]` — Backend, CLI, DevOps tools — nhanh như C, dễ như Python

---

## Tại sao Go?

Go ra đời năm 2009 tại Google bởi Rob Pike, Ken Thompson (creator of Unix), và Robert Griesemer. Họ frustrated với C++ compile chậm, Java verbose quá, Python chậm quá. Go được thiết kế để giải quyết **cả 3 vấn đề cùng lúc**.

### Go giải quyết vấn đề gì?

**Vấn đề 1: Compile chậm.** Ở Google, build 1 C++ project mất **hàng giờ**. Go compile cực nhanh — project lớn compile trong **vài giây**. Tại sao? Go import là DAG (directed acyclic graph), mỗi package compile 1 lần duy nhất, không cần header files.

**Vấn đề 2: Ngôn ngữ phức tạp.** C++ có templates, multiple inheritance, operator overloading, exceptions... Mỗi developer viết C++ "theo style riêng". Go **cố tình đơn giản**: không có classes, không có exceptions, không có generics (đến 1.18 mới thêm), chỉ 25 keywords. MỌI Go code đọc giống nhau → team mới join hiểu ngay.

**Vấn đề 3: Concurrency khó.** Viết concurrent code bằng C/Java = quản lý threads, locks, mutexes → dễ deadlock, race conditions. Go dùng **goroutines + channels** — concurrent programming đơn giản như gọi function.

### So sánh với các ngôn ngữ khác

| | Go | Node.js | Python | Java | Rust |
|---|---|---|---|---|---|
| **Type system** | Static, compiled | Dynamic | Dynamic | Static, compiled | Static, compiled |
| **Speed** | Rất nhanh | Nhanh (V8) | Chậm | Nhanh | Nhanh nhất |
| **Concurrency** | Goroutines (excellent) | Event loop | GIL (limited) | Threads | Async/threads |
| **Memory** | ~10MB/service | ~50MB | ~30MB | ~100MB+ | ~5MB |
| **Learning** | Dễ (25 keywords) | Dễ | Rất dễ | Trung bình | Khó |
| **Best for** | APIs, CLI, DevOps | Web APIs, real-time | ML, scripting | Enterprise | Systems, safety-critical |
| **Dùng bởi** | Google, Uber, Docker | Netflix, LinkedIn | Google, Meta | Banks, enterprise | Mozilla, Cloudflare |

**Chọn Go khi:**
- Backend API cần high throughput (hàng chục nghìn requests/s)
- CLI tools (Docker, Kubernetes, Terraform đều viết bằng Go)
- Microservices (binary nhỏ, startup nhanh, memory thấp)
- DevOps / Infrastructure tools

---

## 1. Syntax cơ bản

Go có cú pháp **ngắn gọn, ít ambiguity**. Mọi file bắt đầu bằng `package`, import rõ ràng, `main()` là entry point.

```go
package main

import (
    "fmt"
    "strings"
)

func main() {
    // Variables — Go infer type từ giá trị
    name := "An"                    // Short declaration (trong function)
    var age int = 25                // Explicit type
    var isActive bool               // Zero value: false
    
    // Constants
    const maxRetries = 3
    
    // String formatting
    fmt.Printf("Name: %s, Age: %d\n", name, age)
    fmt.Println(strings.ToUpper(name))  // "AN"
    
    // Arrays & Slices
    // Array: fixed size. Slice: dynamic (dùng slice 99% thời gian)
    numbers := []int{1, 2, 3, 4, 5}          // Slice literal
    numbers = append(numbers, 6)               // Thêm element
    subset := numbers[1:3]                     // Slice: [2, 3]
    
    // Maps (dictionary/object)
    user := map[string]string{
        "name":  "An",
        "email": "an@example.com",
    }
    user["role"] = "admin"         // Thêm key
    email, exists := user["email"] // Check key exists
    if exists {
        fmt.Println(email)
    }
    delete(user, "role")           // Xóa key
    
    // Loops — Go CHỈ có for (không có while, do-while)
    for i := 0; i < 5; i++ {
        fmt.Println(i)
    }
    
    // Range — iterate over slices, maps
    for index, value := range numbers {
        fmt.Printf("index: %d, value: %d\n", index, value)
    }
    
    for key, value := range user {
        fmt.Printf("%s: %s\n", key, value)
    }
    
    // While-style loop
    count := 0
    for count < 10 {
        count++
    }
    
    _ = age       // _ = ignore variable (Go không cho unused variables)
    _ = isActive
}
```

### Functions — Multiple return values

Go cho phép return **nhiều giá trị** — đặc biệt pattern `(result, error)` bạn sẽ gặp KHẮP NƠI:

```go
// Function cơ bản
func add(a, b int) int {
    return a + b
}

// Multiple return values — Go idiom quan trọng nhất
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil  // nil = no error
}

func main() {
    result, err := divide(10, 3)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Println("Result:", result)  // 3.333...
    
    // Variadic function (số lượng args không cố định)
    fmt.Println(sum(1, 2, 3, 4, 5))
}

func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}

// First-class functions (function as value)
func applyOperation(a, b int, op func(int, int) int) int {
    return op(a, b)
}
// applyOperation(5, 3, add) → 8
```

---

## 2. Structs & Methods — "OOP kiểu Go"

Go **không có classes**. Thay vào đó dùng **structs** (data) + **methods** (behavior). Đây là design choice cố ý — Go ưu tiên **composition over inheritance**.

```go
// Struct = data container (giống class nhưng không có inheritance)
type User struct {
    ID        string
    Name      string
    Email     string
    Age       int
    CreatedAt time.Time
}

// Method = function gắn với struct
// (u User) = "receiver" — method này thuộc về User
func (u User) FullName() string {
    return u.Name
}

// Pointer receiver — khi cần MODIFY struct
// Dùng pointer (*User) khi:
// 1. Cần modify state
// 2. Struct lớn (tránh copy) — nhỏ hơn 3 fields thì OK copy
func (u *User) UpdateEmail(email string) {
    u.Email = email  // Modify original struct
}

// Constructor (Go convention: New + TypeName)
func NewUser(name, email string) *User {
    return &User{
        ID:        generateID(),
        Name:      name,
        Email:     email,
        CreatedAt: time.Now(),
    }
}

func main() {
    user := NewUser("An", "an@example.com")
    fmt.Println(user.FullName())
    user.UpdateEmail("newemail@example.com")
}
```

### Composition — "Kế thừa" kiểu Go

Go không có inheritance. Thay vào đó dùng **embedding** — nhúng 1 struct vào struct khác:

```go
// Base "class"
type BaseModel struct {
    ID        string
    CreatedAt time.Time
    UpdatedAt time.Time
}

func (b *BaseModel) SetTimestamps() {
    now := time.Now()
    if b.CreatedAt.IsZero() {
        b.CreatedAt = now
    }
    b.UpdatedAt = now
}

// "Kế thừa" bằng embedding
type Post struct {
    BaseModel           // Embedded — Post "có" tất cả fields và methods của BaseModel
    Title   string
    Content string
    Author  *User
}

func main() {
    post := &Post{
        Title:   "Hello Go",
        Content: "Go is awesome",
    }
    post.SetTimestamps()  // Gọi trực tiếp! (từ BaseModel)
    fmt.Println(post.CreatedAt)
    fmt.Println(post.ID)  // Access trực tiếp fields của BaseModel
}
```

---

## 3. Interfaces — "Duck typing" có type safety

"If it walks like a duck and quacks like a duck, it's a duck."

Go interfaces là **implicit** — struct không cần khai báo "implements interface". Chỉ cần có đúng methods → tự động satisfy interface.

```go
// Interface: định nghĩa behavior (KHÔNG phải data)
type Storage interface {
    Save(key string, data []byte) error
    Load(key string) ([]byte, error)
    Delete(key string) error
}

// FileStorage implements Storage (KHÔNG cần khai báo "implements")
type FileStorage struct {
    BasePath string
}

func (fs *FileStorage) Save(key string, data []byte) error {
    return os.WriteFile(filepath.Join(fs.BasePath, key), data, 0644)
}

func (fs *FileStorage) Load(key string) ([]byte, error) {
    return os.ReadFile(filepath.Join(fs.BasePath, key))
}

func (fs *FileStorage) Delete(key string) error {
    return os.Remove(filepath.Join(fs.BasePath, key))
}

// RedisStorage cũng implements Storage
type RedisStorage struct {
    client *redis.Client
}

func (rs *RedisStorage) Save(key string, data []byte) error {
    return rs.client.Set(ctx, key, data, 0).Err()
}
// ... Load, Delete methods

// Dùng interface → KHÔNG care implementation cụ thể
type UserService struct {
    storage Storage  // FileStorage, RedisStorage, S3Storage... đều OK
}

func (s *UserService) SaveUser(user *User) error {
    data, _ := json.Marshal(user)
    return s.storage.Save("user:"+user.ID, data)
}

// Dependency injection
fileService := &UserService{storage: &FileStorage{BasePath: "./data"}}
redisService := &UserService{storage: &RedisStorage{client: redisClient}}
// Cùng interface, khác implementation!
```

---

## 4. Error Handling — Explicit, không có exceptions

Go KHÔNG có try/catch. Errors là **values** — bạn xử lý explicitly tại mỗi bước. Đây là design choice quan trọng: bạn KHÔNG BAO GIỜ "quên" xử lý error (compiler sẽ warn nếu ignore return value).

```go
// Standard error pattern: if err != nil { handle }
func readConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("reading config file: %w", err)
        // %w = wrap error: giữ nguyên error gốc + thêm context
    }
    
    var config Config
    if err := json.Unmarshal(data, &config); err != nil {
        return nil, fmt.Errorf("parsing config JSON: %w", err)
    }
    
    if config.Port == 0 {
        return nil, fmt.Errorf("config: port is required")
    }
    
    return &config, nil
}

// Caller
func main() {
    config, err := readConfig("config.json")
    if err != nil {
        log.Fatalf("Failed to read config: %v", err)
        // Output: "Failed to read config: reading config file: open config.json: no such file..."
        // → Error chain rõ ràng, dễ debug!
    }
    fmt.Println("Server port:", config.Port)
}

// Custom error types
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation: %s %s", e.Field, e.Message)
}

// Check error type
if errors.Is(err, os.ErrNotExist) {
    // File not found
}
var vErr *ValidationError
if errors.As(err, &vErr) {
    fmt.Println("Invalid field:", vErr.Field)
}
```

---

## 5. Goroutines & Channels — Concurrency

Đây là **killer feature** của Go. Goroutine = lightweight thread (~2KB stack, vs ~1MB per OS thread). Bạn có thể chạy **hàng triệu** goroutines đồng thời.

```go
// Goroutine: thêm "go" trước function call
func fetchURL(url string) {
    resp, err := http.Get(url)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    defer resp.Body.Close()
    fmt.Printf("%s: %d\n", url, resp.StatusCode)
}

func main() {
    urls := []string{
        "https://google.com",
        "https://github.com",
        "https://stackoverflow.com",
    }
    
    // Sequential: 3 requests × 200ms = 600ms
    // Concurrent: 3 requests song song = 200ms!
    
    var wg sync.WaitGroup
    for _, url := range urls {
        wg.Add(1)
        go func(u string) {         // "go" = chạy goroutine
            defer wg.Done()
            fetchURL(u)
        }(url)
    }
    wg.Wait()  // Chờ TẤT CẢ goroutines xong
}
```

### Channels — Giao tiếp giữa goroutines

Goroutines giao tiếp qua **channels** (pipe truyền data an toàn):

```go
// Channel: typed pipe
func producer(ch chan<- int) {
    for i := 0; i < 5; i++ {
        ch <- i  // Gửi vào channel
        time.Sleep(100 * time.Millisecond)
    }
    close(ch)  // Đóng channel khi xong
}

func main() {
    ch := make(chan int, 10)  // Buffered channel (capacity 10)
    
    go producer(ch)
    
    // Nhận từ channel (tự dừng khi channel closed)
    for value := range ch {
        fmt.Println("Received:", value)
    }
}

// Fan-out / Fan-in pattern
// 1 producer → nhiều workers → 1 collector
func worker(id int, jobs <-chan int, results chan<- int) {
    for job := range jobs {
        fmt.Printf("Worker %d processing job %d\n", id, job)
        time.Sleep(time.Second)
        results <- job * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)
    
    // Start 3 workers
    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }
    
    // Send 9 jobs → 3 workers xử lý song song → ~3 giây thay vì 9 giây
    for j := 1; j <= 9; j++ {
        jobs <- j
    }
    close(jobs)
    
    for r := 1; r <= 9; r++ {
        fmt.Println("Result:", <-results)
    }
}

// Select — listen nhiều channels cùng lúc
select {
case msg := <-channel1:
    fmt.Println("From ch1:", msg)
case msg := <-channel2:
    fmt.Println("From ch2:", msg)
case <-time.After(5 * time.Second):
    fmt.Println("Timeout!")
}
```

---

## 6. HTTP Server — Web development

```go
package main

import (
    "encoding/json"
    "log"
    "net/http"
)

type User struct {
    ID    string `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email"`
}

func main() {
    mux := http.NewServeMux()
    
    // GET /api/users
    mux.HandleFunc("GET /api/users", func(w http.ResponseWriter, r *http.Request) {
        users := []User{
            {ID: "1", Name: "An", Email: "an@example.com"},
        }
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(users)
    })
    
    // GET /api/users/{id}
    mux.HandleFunc("GET /api/users/{id}", func(w http.ResponseWriter, r *http.Request) {
        id := r.PathValue("id")  // Go 1.22+ path params
        user := User{ID: id, Name: "An", Email: "an@example.com"}
        json.NewEncoder(w).Encode(user)
    })
    
    log.Println("Server running on :8080")
    log.Fatal(http.ListenAndServe(":8080", mux))
}
```

**Production frameworks:**
- **Gin** — Nhanh nhất, phổ biến nhất
- **Echo** — Tương tự Gin, API ergonomic hơn
- **Fiber** — Express-inspired, extremely fast
- **Chi** — Lightweight, idiomatic Go

---

## Go Tooling — Built-in, không cần setup

```bash
go mod init myapp          # Initialize module
go run main.go             # Run
go build -o myapp          # Compile → binary
go test ./...              # Run all tests
go fmt ./...               # Format code (tự động, cả team cùng style!)
go vet ./...               # Static analysis (tìm bugs)
go mod tidy                # Clean unused dependencies
```

---

## Bài tập thực hành

- [ ] CLI tool: file organizer (đọc folder, phân loại files theo extension)
- [ ] REST API: CRUD + middleware (logging, auth) với net/http hoặc Gin
- [ ] Concurrent: fetch 10 URLs song song, collect results
- [ ] Worker pool: fan-out/fan-in pattern với channels

---

## Tài nguyên thêm

- [Go Tour](https://go.dev/tour/) — Interactive tutorial (official, START HERE)
- [Go by Example](https://gobyexample.com/) — Practical examples
- [Effective Go](https://go.dev/doc/effective_go) — Idiomatic Go
- [Learn Go with Tests](https://quii.gitbook.io/learn-go-with-tests) — TDD approach
