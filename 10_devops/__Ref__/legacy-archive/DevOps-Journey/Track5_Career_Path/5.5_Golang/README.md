# 🐹 Module 5.5: Golang for DevOps

[![Level: Advanced](https://img.shields.io/badge/Level-Advanced-red?style=flat-square)](.)
[![Language](https://img.shields.io/badge/Language-Go%20(Golang)-blue?style=flat-square)](.)

> **The Language of Cloud Native.**
>
> *Ngôn ngữ của Cloud Native.*

---

## 🎯 Learning Objectives (Mục Tiêu)

- ✅ Understand why Go is dominant in DevOps (Hiểu lý do Go thống trị DevOps: Docker, K8s, Terraform đều viết bằng Go).
- ✅ Master Go basic syntax (Thành thạo cú pháp Go): Variables, Loops, Structs, Interfaces.
- ✅ **Concurrency**: Goroutines & Channels (Xử lý đồng thời).
- ✅ Build a **CLI Tool** to automate infrastructure tasks (Xây dựng công cụ CLI tự động hóa).
- ✅ Interact with Kubernetes API using `client-go` (Tương tác với K8s API).

---

## 📚 Content (Nội Dung)

### 1. Why Go? (Tại sao lại là Go?)

| Feature | DevOps Benefit (Lợi ích cho DevOps) |
| :--- | :--- |
| **Static Binary** | Compile once, run anywhere (Biên dịch 1 lần, chạy mọi nơi - Không lo thiếu thư viện như Python). |
| **Performance** | Near C++ speed, much faster than Python (Tốc độ gần bằng C++, nhanh hơn nhiều so với Python). |
| **Concurrency** | Handles thousands of connection/tasks easily (Xử lý hàng nghìn kết nối/tác vụ dễ dàng với Goroutines). |

*Tại sao DevOps cần Go? Đơn giản vì các công cụ bạn dùng hàng ngày (Docker, Kubernetes, Prometheus) đều được viết bằng Go. Để debug sâu hoặc viết extension (Operator, Terraform Provider), bạn cần Go.*

### 2. Go Basics for Scripting (Cơ bản về Scripting với Go)

#### 2.1 Variables & Types (Biến & Kiểu dữ liệu)

Go is statically typed (Go là ngôn ngữ định kiểu tĩnh).

```go
package main

import "fmt"

func main() {
    var name string = "DevOps"
    count := 10 // Type inference
    fmt.Printf("Hello %s, count: %d\n", name, count)
}
```

#### 2.2 Structs & Interfaces (Core for K8s - Cốt lõi cho K8s)

Kubernetes resources (Pods, Services) are defined as Structs (Tài nguyên K8s được định nghĩa là Structs).

```go
type Server struct {
    IP   string
    Port int
}

func (s Server) Connect() {
    fmt.Println("Connecting to", s.IP)
}
```

### 3. Concurrency (Xử lý đồng thời)

Do 3 things at once without Threads overhead (Làm 3 việc cùng lúc mà không tốn tài nguyên như Threads truyền thống).

```go
go deployApp("app1") // Starts immediately in background
go deployApp("app2")
```

---

## 🛠️ Hands-on Project: System Monitor CLI

You will build a tool like `top` but customized for your infrastructure.
*Bạn sẽ xây dựng một công cụ CLI để giám sát hệ thống.*

**Steps (Các bước):**

1. Parse flags (`cmd --verbose`) (Phân tích cờ lệnh).
2. Read system metrics (CPU/RAM) (Đọc thông số hệ thống).
3. Output JSON for logging (Xuất ra JSON để ghi log).

---

## 🔗 Navigation

[⬅️ Back to Career Path](../README.md)
