# GIAI ĐOẠN 3: DOCKER VOLUME - CỨU DỮ LIỆU KHỎI "CỬA TỬ"

## 📌 MỤC TIÊU GIAI ĐOẠN 3
Container sinh ra là để "chết đi". Nhưng dữ liệu thì phải "sống mãi".
Giai đoạn này giải quyết bài toán mất dữ liệu khi restart container bằng cách sử dụng **Docker Volume** (Bind Mount).

**Bạn sẽ thực hiện:**
✅ Sửa code Go để ghi dữ liệu ra file JSON thay vì chỉ lưu RAM.
✅ Chạy container với cờ `-v` để mount thư mụcHost vào Container.
✅ Kiểm chứng dữ liệu vẫn còn sau khi xóa hẳn container.

---

## 🛠️ PHẦN 1: CẬP NHẬT CODE GO (PERSISTENCE LAYER)

Chúng ta cần sửa `go-service/main.go` để mỗi khi tạo Todo, nó sẽ ghi xuống đĩa cứng.

### Sửa file `go-service/main.go`
Thay thế (hoặc sửa) các đoạn code sau:

```go
package main

import (
	"encoding/json" // Thêm thư viện xử lý JSON
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

// ... (Giữ nguyên các Struct Todo, CreateTodoRequest)

var (
	todos      = make(map[string]Todo)
	todosMutex sync.RWMutex
	DB_FILE    = "/app/data/db.json" // Đường dẫn file DB trong Container
)

// --- HÀM ĐỌC/GHI FILE ---

// Load data từ file vào RAM khi khởi động
func loadTodos() {
	// Kiểm tra file có tồn tại không
	if _, err := os.Stat(DB_FILE); os.IsNotExist(err) {
		fmt.Println("DB file not found, creating new one...")
		return
	}

	file, err := ioutil.ReadFile(DB_FILE)
	if err != nil {
		fmt.Println("Error reading DB file:", err)
		return
	}

	// Đọc vào map tạm -> gán vào var todos
	var loadedTodos map[string]Todo
	if err := json.Unmarshal(file, &loadedTodos); err == nil {
		todos = loadedTodos
		fmt.Println("Loaded todos from disk:", len(todos))
	}
}

// Lưu RAM xuống file
func saveTodos() {
	todosMutex.RLock()
	defer todosMutex.RUnlock()

	data, err := json.MarshalIndent(todos, "", "  ")
	if err != nil {
		fmt.Println("Error marshalling todos:", err)
		return
	}

	// Ghi đè file
	err = ioutil.WriteFile(DB_FILE, data, 0644)
	if err != nil {
		fmt.Println("Error writing DB file:", err)
	} else {
		fmt.Println("Saved todos to disk")
	}
}

func main() {
	// 1. Load dữ liệu cũ lên trước
	loadTodos()

	router := gin.Default()
	router.Use(cors.Default())

	router.POST("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{"message": "pong"})
	})

	router.GET("/todos", getAllTodos)
	router.POST("/todos", createTodo)
    router.DELETE("/todos/:id", deleteTodo)

	router.Run(":8081")
}

// ... (Giữ nguyên getAllTodos)

func createTodo(c *gin.Context) {
    // ... (Phần bind request và tạo object Todo giữ nguyên)
    // Sau khi gán vào map:
    
    todosMutex.Lock()
    todos[newTodo.ID] = newTodo
    todosMutex.Unlock()

    // 👉 THÊM DÒNG NÀY: Lưu xuống file ngay lập tức
    saveTodos() 

    c.JSON(http.StatusCreated, newTodo)
}

func deleteTodo(c *gin.Context) {
    // ... (Giữ nguyên logic xóa map)
    
    // 👉 THÊM DÒNG NÀY
    saveTodos() 
    
    c.Status(http.StatusNoContent)
}
```

---

## 🏗️ PHẦN 2: REBUILD IMAGE

Do code Go đã thay đổi, ta PHẢI build lại image. Image Python không đổi thì không cần build lại.

```bash
docker build -t todo-go:v2 ./go-service
```
*(Đặt tag v2 để phân biệt)*

---

## 💾 PHẦN 3: CHẠY CONTAINER VỚI VOLUME

Dọn dẹp container cũ trước:
```bash
docker rm -f go-app python-app
```

### B1. Chạy Go với Volume Mount
```bash
docker run -d \
  --name go-app \
  --network todo-net \
  -v $(pwd)/data:/app/data \
  todo-go:v2
```

**Giải thích siêu quan trọng:**
> `-v $(pwd)/data:/app/data`
> - `$(pwd)/data`: Thư mục `data` ở host (máy bạn). `$(pwd)` là lệnh lấy đường dẫn hiện tại. (Windows PowerShell dùng `${PWD}/data` hoặc gõ đường dẫn tuyệt đối).
> - `/app/data`: Thư mục trong container mà Go code trỏ tới (`DB_FILE`).
> 👉 Hai thư mục này giờ là **MỘT**. Go ghi vào `/app/data/db.json` -> Tức là ghi vào máy thật của bạn.

### B2. Chạy Python (như cũ)
```bash
docker run -d \
  --name python-app \
  --network todo-net \
  -p 5000:8080 \
  -e GO_HOST=go-app \
  todo-python:v1
```

---

## 🧪 PHẦN 4: THỰC HÀNH KIỂM CHỨNG (MAGIC MOMENT)

### 1. Tạo dữ liệu
```bash
curl -X POST http://localhost:5000/api/todos \
   -H "Content-Type: application/json" \
   -d "{\"title\": \"Dữ liệu này bất tử\"}"
```

### 2. Kiểm tra trên máy thật
Mở thư mục `data` trong dự án. Bạn sẽ thấy file `db.json` xuất hiện! Mở nó ra xem, thấy nội dung Todo vừa tạo.
**-> Go trong container đã "thò tay" ra ngoài ghi file.**

### 3. Hủy diệt Container (Chaos Test)
```bash
# Xóa sạch container
docker rm -f go-app

# Kiểm tra web/curl -> Chết ngoẻo (đương nhiên)
```

### 4. Hồi sinh (Resurrection)
Chạy lại container Go (nhớ vẫn map volume):
```bash
docker run -d \
  --name go-app \
  --network todo-net \
  -v $(pwd)/data:/app/data \
  todo-go:v2
```

### 5. Kiểm tra lại dữ liệu
```bash
curl http://localhost:5000/api/todos
```
📌 **Kết quả:** Vẫn thấy "Dữ liệu này bất tử".
-> **Thành công:** Dù container bị xóa, dữ liệu vẫn an toàn trên máy Host. Khi container mới lên, nó đọc lại file cũ và phục hồi trạng thái.

---

## 📝 TỔNG KẾT
Bạn đã nắm được bí mật của việc lưu trữ trong Container: **Đừng bao giờ lưu data quan trọng bên trong Read-Write Layer của Container.** Hãy luôn map nó ra ngoài.

👉 **Bước tiếp theo:** Gõ lệnh `docker run` dài quá? Hãy dùng **Docker Compose (Giai đoạn 4)** để quản lý "nhàn" hơn.
