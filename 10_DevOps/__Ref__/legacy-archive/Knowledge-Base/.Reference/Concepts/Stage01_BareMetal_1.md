# GIAI ĐOẠN 1: BARE-METAL & GIAO TIẾP LIÊN DỊCH VỤ

## 📌 MỤC TIÊU GIAI ĐOẠN 1
Ở giai đoạn này, chúng ta sẽ xây dựng nền móng cho hệ thống Microservices. Bạn sẽ viết code chạy trực tiếp trên máy tính cá nhân (Bare-metal) mà chưa dùng Docker.

**Bạn sẽ đạt được:**
✅ Hiểu luồng hoạt động: User -> Python Gateway -> Go Service.
✅ Viết được Go Service xử lý CRUD Todo (Lưu RAM).
✅ Viết được Python Service làm Gateway.
✅ Hiểu sâu sắc **tại sao dữ liệu bị mất** khi lưu trên RAM (tiền đề cho việc cần Database sau này).
✅ Biết cách dùng `cURL` để test API.

---

## 🛠️ PHẦN 1: CẤU TRÚC DỰ ÁN
Mở VS Code, tạo một thư mục mới cho dự án, ví dụ `Todo-App-DevOps`. Bên trong, tạo cấu trúc sau:

```text
Todo-App-DevOps/
├── go-service/          # Backend chính (xử lý logic, lưu data RAM)
│   ├── main.go          # Code nguồn Go
│   └── go.mod           # Quản lý thư viện Go
├── python-service/      # API Gateway (cổng vào)
│   ├── app.py           # Code nguồn Python Flask
│   └── requirements.txt # Danh sách thư viện Python
└── frontend/            # (Để dành cho Giai đoạn 5)
```

---

## 🐍 PHẦN 2: XÂY DỰNG GO BACKEND (PORT 8081)
Go service sẽ chịu trách nhiệm quản lý danh sách Todo.

### B1. Khởi tạo Module
Mở Terminal tại thư mục `go-service/` và chạy:
```bash
# Di chuyển vào thư mục go-service
cd go-service

# Khởi tạo Go module (tạo file go.mod để quản lý dependencies)
# todo-go-service là tên module của project
go mod init todo-go-service

# Tải thư viện Gin Framework (Web framework cho Go, giống Flask/Express)
# Dùng để tạo HTTP server, xử lý routing (GET, POST, DELETE...)
go get github.com/gin-gonic/gin

# Tải thư viện UUID Generator của Google
# Dùng để tạo ID duy nhất cho mỗi TODO item
# VD: "550e8400-e29b-41d4-a716-446655440000"
go get github.com/google/uuid

# Tải thư viện CORS Middleware
# Cho phép Frontend (chạy trên port khác) gọi API vào Backend
# Không có CORS → Browser sẽ chặn request (CORS Error)
go get github.com/gin-contrib/cors
```

**📝 Giải thích:**
- `go mod init`: Giống `npm init` (Node.js) hay `pip install` (Python), tạo file quản lý thư viện
- `go get`: Tải package từ internet về máy, tự động cập nhật `go.mod` và `go.sum`
- Sau khi chạy xong, bạn sẽ thấy 2 file mới: `go.mod` (danh sách thư viện) và `go.sum` (checksum)

### B2. Viết code `main.go`
Tạo file `go-service/main.go` và dán nội dung sau. Code này cài đặt API Ping-Pong và CRUD Todo, lưu trữ biến toàn cục `todos` (RAM).

```go
package main

import (
    "net/http"
    "sync"
    "time"

    "github.com/gin-contrib/cors"
    "github.com/gin-gonic/gin"
    "github.com/google/uuid"
)

// --- DATA MODELS ---
type Todo struct {
    ID        string    `json:"id"`
    Title     string    `json:"title"`
    Completed bool      `json:"completed"`
    CreatedAt time.Time `json:"created_at"`
}

type CreateTodoRequest struct {
    Title string `json:"title" binding:"required"`
}

// --- GLOBAL STORAGE (RAM) ---
var (
    todos      = make(map[string]Todo) // Lưu dữ liệu tại đây! Mất khi tắt app.
    todosMutex sync.RWMutex            // Khóa thread-safe
)

func main() {
    router := gin.Default()

    // Cấu hình CORS (cho phép ai gọi cũng được - dev mode)
    router.Use(cors.Default())

    // --- ROUTES ---
    router.POST("/ping", func(c *gin.Context) {
        c.JSON(200, gin.H{"message": "pong", "from": "Go Service"})
    })

    // CRUD TODO
    router.GET("/todos", getAllTodos)
    router.POST("/todos", createTodo)
    router.DELETE("/todos/:id", deleteTodo)

    // Chạy trên port 8081
    router.Run(":8081")
}

// --- HANDLERS ---
func getAllTodos(c *gin.Context) {
    todosMutex.RLock()
    defer todosMutex.RUnlock()

    // Convert Map to Slice
    todoList := make([]Todo, 0, len(todos))
    for _, todo := range todos {
        todoList = append(todoList, todo)
    }
    c.JSON(http.StatusOK, todoList)
}

func createTodo(c *gin.Context) {
    var req CreateTodoRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    newTodo := Todo{
        ID:        uuid.New().String(),
        Title:     req.Title,
        Completed: false,
        CreatedAt: time.Now(),
    }

    todosMutex.Lock()
    todos[newTodo.ID] = newTodo // Ghi vào RAM
    todosMutex.Unlock()

    c.JSON(http.StatusCreated, newTodo)
}

func deleteTodo(c *gin.Context) {
    id := c.Param("id")
    todosMutex.Lock()
    delete(todos, id) // Xóa khỏi RAM
    todosMutex.Unlock()
    c.Status(http.StatusNoContent)
}
```

### B3. Chạy thử Go Service
```bash
go run main.go
```
✅ **Thành công:** Terminal hiện `Listening and serving HTTP on :8081`. Giữ Terminal này mở.

---

## 🚀 PHẦN 3: XÂY DỰNG PYTHON GATEWAY (PORT 8080)
Python service đóng vai trò Gateway, nhận request từ User và gọi sang Go.

### B1. Cài đặt thư viện
Tạo file `python-service/requirements.txt`:
```text
Flask==3.0.0
requests==2.31.0
flask-cors==4.0.0
```
Cài đặt (Mở Terminal `python-service/`):
```bash
cd python-service
pip install -r requirements.txt
```

### B2. Viết code `app.py`
Tạo file `python-service/app.py`:

```python
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Địa chỉ của Go Service (Giai đoạn này là localhost)
GO_SERVICE_URL = "http://localhost:8081"

@app.route('/ping', methods=['GET'])
def ping():
    try:
        # Gọi sang Go
        resp = requests.post(f"{GO_SERVICE_URL}/ping")
        return jsonify({
            "gateway_message": "Hello from Python Gateway",
            "backend_response": resp.json()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/todos', methods=['GET'])
def get_todos():
    try:
        resp = requests.get(f"{GO_SERVICE_URL}/todos")
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/todos', methods=['POST'])
def add_todo():
    try:
        data = request.json
        resp = requests.post(f"{GO_SERVICE_URL}/todos", json=data)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Chạy trên port 8080
    app.run(port=8080, debug=True)
```

### B3. Chạy thử Python Gateway
Mở **Terminal mới** (Terminal Go vẫn chạy):
```bash
cd python-service
python app.py
```
✅ **Thành công:** Terminal hiện `Running on http://127.0.0.1:8080`.

---

## 🧪 PHẦN 4: THỰC HÀNH KIỂM THỬ (TESTING)

Hiện tại bạn có 2 service đang chạy:
1. **Python Gateway**: Port 8080 (User gọi vào đây).
2. **Go Backend**: Port 8081 (Python gọi vào đây).

### Kịch bản 1: Test Kết Nối (Ping Pong)
Mở Terminal thứ 3 và gõ lệnh:
```bash
curl http://localhost:8080/ping
```
📌 **Kết quả mong đợi:**
```json
{
  "backend_response": {
    "from": "Go Service",
    "message": "pong"
  },
  "gateway_message": "Hello from Python Gateway"
}
```
> Điều này chứng tỏ: User -> Python -> Go -> Python -> User thành công!

### Kịch bản 2: Thêm dữ liệu (Create Todo)
```bash
curl -X POST http://localhost:8080/api/todos \
   -H "Content-Type: application/json" \
   -d "{\"title\": \"Học DevOps Giai đoạn 1\"}"
```
📌 **Kết quả:** Trả về JSON chứa ID của Todo vừa tạo.

### Kịch bản 3: Xem danh sách (Read Todos)
```bash
curl http://localhost:8080/api/todos
```
📌 **Kết quả:** Thấy danh sách có 1 bài "Học DevOps Giai đoạn 1".

### 💥 Kịch bản 4: Test Mất Dữ Liệu (Quan trọng!)
Đây là bài học cốt lõi của giai đoạn này.

1. Đang có 1 Todo trong danh sách (kiểm tra bằng lệnh curl ở Kịch bản 3).
2. **Tắt App Go**: Vào Terminal đang chạy Go, bấm `Ctrl+C` để tắt server.
3. **Bật lại App Go**: Gõ lại `go run main.go`.
4. **Kiểm tra lại danh sách**:
```bash
curl http://localhost:8080/api/todos
```
📌 **Kết quả:** `[]` (Danh sách rỗng).

> **Kết luận:** Go Services lưu biến `todos` trong RAM. Khi process tắt, RAM giải phóng -> Mất dữ liệu. Đây là lý do chúng ta cần Database ở các giai đoạn sau (MySQL) và Persistent Volume (Docker).

---

## 📝 TỔNG KẾT GIAI ĐOẠN 1
Bạn đã hoàn thành hệ thống Microservices sơ khai nhất:
- Biết cách dựng 2 service giao tiếp qua HTTP.
- Thấy tận mắt sự mỏng manh của việc lưu dữ liệu trên RAM.

👉 **Bước tiếp theo:** Đóng gói ứng dụng để "chạy đâu cũng được" với **Docker (Giai đoạn 2)**.
