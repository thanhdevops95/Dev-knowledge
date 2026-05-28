# 🔬 Labs: Golang for DevOps

> **Hands-on Labs for Golang Development**
>
> *Bài thực hành Golang cho DevOps.*

---

## 🔬 Lab 1: Go Environment Setup

### Objective

Install Go and set up development environment.

*(Cài đặt Go và thiết lập môi trường phát triển.)*

### Steps

```bash
# Install Go (macOS)
brew install go

# Or download from https://golang.org/dl/

# Verify installation (Xác nhận cài đặt)
go version

# Set up workspace (Thiết lập workspace)
mkdir -p ~/go/{src,bin,pkg}
export GOPATH=~/go
export PATH=$PATH:$GOPATH/bin
```

---

## 🔬 Lab 2: First Go Program

```go
// main.go
package main

import "fmt"

func main() {
    fmt.Println("Hello, DevOps!")
}
```

```bash
# Initialize module (Khởi tạo module)
go mod init hello
go run main.go
go build -o hello
./hello
```

---

## 🔬 Lab 3: CLI Tool with Cobra

```bash
# Install Cobra CLI
go install github.com/spf13/cobra-cli@latest

# Create project
mkdir mycli && cd mycli
go mod init mycli
cobra-cli init

# Add command
cobra-cli add greet
```

```go
// cmd/greet.go
var greetCmd = &cobra.Command{
    Use:   "greet",
    Short: "Greet a user",
    Run: func(cmd *cobra.Command, args []string) {
        name, _ := cmd.Flags().GetString("name")
        fmt.Printf("Hello, %s!\n", name)
    },
}

func init() {
    rootCmd.AddCommand(greetCmd)
    greetCmd.Flags().StringP("name", "n", "World", "Name to greet")
}
```

---

## 🔬 Lab 4: HTTP Server

```go
// server.go
package main

import (
    "encoding/json"
    "log"
    "net/http"
)

type Response struct {
    Status  string `json:"status"`
    Message string `json:"message"`
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(Response{Status: "ok", Message: "healthy"})
}

func main() {
    http.HandleFunc("/health", healthHandler)
    log.Println("Server starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

```bash
go run server.go &
curl http://localhost:8080/health
```

---

## 🔬 Lab 5: Docker Image for Go App

```dockerfile
# Dockerfile
# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/server

# Production stage
FROM scratch
COPY --from=builder /app/server /server
EXPOSE 8080
ENTRYPOINT ["/server"]
```

```bash
docker build -t go-server .
docker run -p 8080:8080 go-server
```

---

## ✅ Checklist

- [ ] Lab 1: Go Setup
- [ ] Lab 2: First Program
- [ ] Lab 3: CLI Tool
- [ ] Lab 4: HTTP Server
- [ ] Lab 5: Docker Image

---

## ✅ General Verification (Kiểm chứng tổng quát)

```bash
# Check Go installation (Kiểm tra cài đặt Go)
go version
go env GOPATH

# Test built binaries (Kiểm tra binary đã build)
./hello
./mycli greet --name DevOps
curl http://localhost:8080/health
```

---

## 🔧 General Troubleshooting (Xử lý sự cố chung)

| Issue | Solution |
|-------|----------|
| `go: command not found` | Add Go to PATH *(Thêm Go vào PATH)* |
| `cannot find package` | Run `go mod tidy` *(Chạy go mod tidy)* |
| `permission denied` | Check file permissions *(Kiểm tra quyền file)* |
| `port already in use` | Change port or kill process *(Đổi port)* |

---

## 🧹 General Cleanup (Dọn dẹp tổng quát)

```bash
# Remove built binaries (Xóa binary)
rm -f hello mycli server

# Remove Docker images (Xóa Docker images)
docker rmi go-server

# Clean Go cache (Dọn cache Go)
go clean -cache
```

---

**[← Back to README](./README.md)**
