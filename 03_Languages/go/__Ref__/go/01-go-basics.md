# 🔋 Go (Golang) — Ngôn ngữ cho hệ thống hiệu năng cao

> `[INTERMEDIATE]` — Đơn giản, nhanh, perfect cho microservices & DevOps tools

---

## Tại sao Go?

- **Hiệu năng cao** — gần bằng C, nhanh hơn Python/JS 10-100x
- **Concurrency built-in** — Goroutines và Channels
- **Compile nhanh** — Binary đơn lẻ, deploy dễ dàng
- **Tooling tuyệt vời** — gofmt, go test, go build tích hợp sẵn
- **Dùng ở đâu** — Docker, Kubernetes, Terraform, GitHub Copilot backend

---

## Cài đặt

```bash
# macOS
brew install go

# Kiểm tra
go version

# Tạo project mới
mkdir my-app && cd my-app
go mod init github.com/username/my-app
```

---

## Cú pháp cơ bản

```go
package main

import (
    "fmt"
    "strings"
)

func main() {
    // Khai báo biến
    var name string = "Jesse"
    age := 25               // Short declaration (hay dùng nhất)
    const PI = 3.14

    // Multiple assignment
    x, y := 10, 20
    x, y = y, x            // Swap!

    fmt.Printf("Xin chào %s, %d tuổi\n", name, age)
    fmt.Println(strings.ToUpper(name))
}
```

---

## Kiểu dữ liệu

```go
// Primitive
var i int = 42
var f float64 = 3.14
var b bool = true
var s string = "hello"

// Zero values (Go không có null, có zero value)
var n int       // 0
var str string  // ""
var ok bool     // false

// Array và Slice
arr := [5]int{1, 2, 3, 4, 5}  // Array (fixed size)
slice := []int{1, 2, 3}        // Slice (dynamic)
slice = append(slice, 4, 5)

// Map
user := map[string]interface{}{
    "name": "Jesse",
    "age":  25,
}
value, exists := user["email"]  // Check tồn tại

// Struct
type User struct {
    ID    int    `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email,omitempty"`
}

jesse := User{ID: 1, Name: "Jesse", Email: "jesse@example.com"}
```

---

## Functions & Error Handling

```go
// Go trả về nhiều giá trị — dùng cho error handling
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("không thể chia cho 0")
    }
    return a / b, nil
}

result, err := divide(10, 2)
if err != nil {
    log.Fatal(err)  // Xử lý lỗi ngay lập tức
}
fmt.Println(result)

// Named return values
func minMax(arr []int) (min, max int) {
    min, max = arr[0], arr[0]
    for _, v := range arr[1:] {
        if v < min { min = v }
        if v > max { max = v }
    }
    return  // Naked return
}
```

---

## Goroutines & Channels (Concurrency)

```go
// Goroutine — lightweight thread
go func() {
    fmt.Println("Chạy song song!")
}()

// Channel — giao tiếp giữa goroutines
ch := make(chan int)

go func() {
    ch <- 42  // Gửi vào channel
}()

value := <-ch  // Nhận từ channel
fmt.Println(value)

// Buffered channel
ch := make(chan string, 3)
ch <- "a"
ch <- "b"
ch <- "c"

// Select — nhận từ nhiều channel
select {
case msg := <-ch1:
    fmt.Println("ch1:", msg)
case msg := <-ch2:
    fmt.Println("ch2:", msg)
case <-time.After(1 * time.Second):
    fmt.Println("Timeout!")
}
```

---

## Interfaces

```go
type Animal interface {
    Speak() string
    Name() string
}

type Dog struct{ name string }
func (d Dog) Speak() string { return "Woof!" }
func (d Dog) Name() string  { return d.name }

type Cat struct{ name string }
func (c Cat) Speak() string { return "Meow!" }
func (c Cat) Name() string  { return c.name }

func makeNoise(a Animal) {
    fmt.Printf("%s nói: %s\n", a.Name(), a.Speak())
}

makeNoise(Dog{name: "Buddy"})  // Buddy nói: Woof!
makeNoise(Cat{name: "Kitty"})  // Kitty nói: Meow!
```

---

## Web Server đơn giản

```go
package main

import (
    "encoding/json"
    "net/http"
)

func main() {
    http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        json.NewEncoder(w).Encode(map[string]string{
            "status": "ok",
        })
    })
    
    http.ListenAndServe(":8080", nil)
}
```

---

## Bài tập thực hành

- [ ] Viết CLI tool đơn giản (ví dụ: word counter, file organizer)
- [ ] REST API với `net/http` hoặc framework Gin
- [ ] Concurrent web scraper với goroutines
- [ ] Implement một data structure (stack, queue) với generics

---

## Tài nguyên thêm

- [A Tour of Go](https://go.dev/tour/) — Interactive tutorial chính thức
- [Go by Example](https://gobyexample.com/) — Ví dụ thực tế
- [Effective Go](https://go.dev/doc/effective_go) — Best practices
