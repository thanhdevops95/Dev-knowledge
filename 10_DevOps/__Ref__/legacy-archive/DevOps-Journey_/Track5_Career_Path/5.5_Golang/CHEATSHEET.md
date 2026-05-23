# 📋 Cheatsheet: Golang

> **Quick Reference for Golang**
>
> *Tham khảo nhanh Golang.*

---

## 🔧 Go Commands

| Command | Description |
|---------|-------------|
| `go mod init <name>` | Initialize module *(Khởi tạo module)* |
| `go run main.go` | Run program *(Chạy chương trình)* |
| `go build` | Compile binary *(Biên dịch binary)* |
| `go test ./...` | Run tests *(Chạy tests)* |
| `go mod tidy` | Clean dependencies *(Dọn dependencies)* |
| `go fmt ./...` | Format code *(Format code)* |
| `go vet ./...` | Static analysis *(Phân tích tĩnh)* |
| `go get <package>` | Add dependency *(Thêm dependency)* |

---

## 📝 Syntax Basics

### Variables

```go
// Declaration (Khai báo)
var name string = "Go"
var age int = 10

// Short declaration (Khai báo ngắn)
name := "Go"
age := 10

// Constants (Hằng số)
const PI = 3.14
```

### Functions

```go
// Basic function (Hàm cơ bản)
func add(a, b int) int {
    return a + b
}

// Multiple returns (Nhiều giá trị trả về)
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("cannot divide by zero")
    }
    return a / b, nil
}
```

### Structs

```go
type User struct {
    Name  string `json:"name"`
    Email string `json:"email"`
}

user := User{Name: "John", Email: "john@example.com"}
```

### Error Handling

```go
result, err := someFunction()
if err != nil {
    log.Fatal(err)
}
```

---

## 🌐 HTTP Server

```go
http.HandleFunc("/", handler)
http.ListenAndServe(":8080", nil)

func handler(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Hello"))
}
```

---

## 🐳 Dockerfile

```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o app

FROM scratch
COPY --from=builder /app/app /app
ENTRYPOINT ["/app"]
```

---

## 🔗 Useful Packages

| Package | Use |
|---------|-----|
| `cobra` | CLI framework |
| `gin` | Web framework |
| `zap` | Logging |
| `viper` | Config |
| `testify` | Testing |

---

**[← Back to README](./README.md)**
