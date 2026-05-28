# GIAI ĐOẠN 6: MYSQL DATABASE - CHUẨN HÓA LƯU TRỮ

## 📌 MỤC TIÊU GIAI ĐOẠN 6
Lưu trữ file JSON (Giai đoạn 3) chỉ phù hợp cho bài tập nhỏ. Trong thực tế, file JSON sẽ gặp lỗi khi nhiều người writte cùng lúc (Race Condition) và tốc độ chậm.
Chúng ta sẽ chuyển sang **MySQL 8.0** - Hệ quản trị CSDL quan hệ phổ biến nhất.

**Công việc:**
✅ Thêm MySQL Service vào Docker Compose.
✅ Sửa code Go để kết nối và query MySQL thay vì ghi file.
✅ Dùng DBeaver kết nối kiểm tra dữ liệu.

---

## 🛠️ PHẦN 1: CẬP NHẬT DOCKER COMPOSE

Sửa file `docker-compose.yaml` để thêm service `db`.

```yaml
version: '3.8'

services:
  backend:
    container_name: go-app
    image: todo-go:v3           # Version 3 cho code DB mới
    environment:
      - DB_HOST=db              # Truyền host DB
      - DB_USER=root
      - DB_PASSWORD=secret      # (Lưu ý: Thực tế dùng Docker Secrets)
      - DB_NAME=todo_db
    depends_on:
      - db
    networks:
      - app-network
    restart: always

  gateway:
    container_name: python-app
    image: todo-python:v1
    environment:
      - GO_HOST=backend
    depends_on:
      - backend
    networks:
      - app-network

  web:
    image: nginx:alpine
    container_name: todo-web
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
      - ./nginx/conf.d:/etc/nginx/conf.d
    depends_on:
      - gateway
    networks:
      - app-network

  # --- Service Mới: Database ---
  db:
    image: mysql:8.0
    container_name: mysql-db
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: todo_db
    volumes:
      - ./mysql-data:/var/lib/mysql  # Mount volume để data DB bất tử
    networks:
      - app-network
    ports:
      - "3306:3306" # Expose ra ngoài để DBeaver connect debug

networks:
  app-network:
    driver: bridge
```

---

## 💻 PHẦN 2: CẬP NHẬT CODE GO

### 1. Cài driver MySQL cho Go
Tại máy host (dev enviroment), bạn cần tải thư viện này để code không báo lỗi đỏ, dù khi chạy ta chạy trong Docker.
```bash
cd go-service
go get github.com/go-sql-driver/mysql
```

### 2. Sửa file `go-service/main.go`
Thay thế toàn bộ logic file/map bằng SQL.

```go
package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	_ "github.com/go-sql-driver/mysql" // Import driver
	"github.com/google/uuid"
)

// --- STRUCT ---
type Todo struct {
	ID        string    `json:"id"`
	Title     string    `json:"title"`
	Completed bool      `json:"completed"`
	CreatedAt time.Time `json:"created_at"`
}

type CreateTodoRequest struct {
	Title string `json:"title" binding:"required"`
}

// --- GLOBAL DB ---
var db *sql.DB

// --- INIT DB FUNCTION ---
func initDB() {
	// Lấy config từ biến môi trường (Set trong Docker Compose)
	dbHost := os.Getenv("DB_HOST")
	dbUser := os.Getenv("DB_USER")
	dbPass := os.Getenv("DB_PASSWORD")
	dbName := os.Getenv("DB_NAME")

	// Nếu chạy local ko có env thì set default
	if dbHost == "" { dbHost = "localhost" }
	if dbUser == "" { dbUser = "root" }
	if dbPass == "" { dbPass = "secret" }
	if dbName == "" { dbName = "todo_db" }

	dsn := fmt.Sprintf("%s:%s@tcp(%s:3306)/%s?parseTime=true", dbUser, dbPass, dbHost, dbName)
	
	var err error
	// Retry connection (vì MySQL khởi động lâu hơn Go)
	for i := 0; i < 10; i++ {
		db, err = sql.Open("mysql", dsn)
		if err == nil {
			err = db.Ping()
			if err == nil {
				fmt.Println("Connected to MySQL!")
				break
			}
		}
		fmt.Println("Waiting for MySQL...", err)
		time.Sleep(2 * time.Second)
	}

	if err != nil {
		log.Fatal("Cannot connect to MySQL:", err)
	}

	// Tạo bảng nếu chưa có
	createTableQuery := `
	CREATE TABLE IF NOT EXISTS todos (
		id VARCHAR(36) PRIMARY KEY,
		title TEXT NOT NULL,
		completed BOOLEAN DEFAULT FALSE,
		created_at DATETIME
	);`
	_, err = db.Exec(createTableQuery)
	if err != nil {
		log.Fatal("Cannot create table:", err)
	}
}

// --- MAIN ---
func main() {
	initDB()
	defer db.Close() // Đóng kết nối khi app tắt

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

// --- HANDLERS (SQL QUERY) ---

func getAllTodos(c *gin.Context) {
	rows, err := db.Query("SELECT id, title, completed, created_at FROM todos")
	if err != nil {
		c.JSON(500, gin.H{"error": err.Error()})
		return
	}
	defer rows.Close()

	var todos []Todo
	for rows.Next() {
		var t Todo
		// Map cột SQL vào struct. Lưu ý MySQL lưu bool là tinyint (0/1) nhưng driver tự convert
		if err := rows.Scan(&t.ID, &t.Title, &t.Completed, &t.CreatedAt); err != nil {
			continue
		}
		todos = append(todos, t)
	}
	
	// Trả về mảng rỗng thay vì null
	if todos == nil {
		todos = []Todo{}
	}
	c.JSON(http.StatusOK, todos)
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

	query := "INSERT INTO todos (id, title, completed, created_at) VALUES (?, ?, ?, ?)"
	_, err := db.Exec(query, newTodo.ID, newTodo.Title, newTodo.Completed, newTodo.CreatedAt)
	
	if err != nil {
		c.JSON(500, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, newTodo)
}

func deleteTodo(c *gin.Context) {
	id := c.Param("id")
	_, err := db.Exec("DELETE FROM todos WHERE id = ?", id)
	if err != nil {
		c.JSON(500, gin.H{"error": err.Error()})
		return
	}
	c.Status(http.StatusNoContent)
}
```

---

## 🏗️ PHẦN 3: BUILD LẠI IMAGE

Do code Go thay đổi lớn (thêm thư viện MySQL), ta cần rebuild.

```bash
docker build -t todo-go:v3 ./go-service
```
*(Nếu gặp lỗi khi build, hãy đảm bảo file `go.mod` và `go.sum` đã được update bằng lệnh `go mod tidy` trên máy host trước, hoặc copy lệnh `RUN go mod tidy` vào Dockerfile)*. 
Khuyến nghị: Chạy `go mod tidy` ở máy host trong thư mục `go-service` để cập nhật `go.sum`.

---

## 🚀 PHẦN 4: DEPLOY & KIỂM TRA

```bash
# Xóa hệ thống cũ
docker compose down

# Bật hệ thống mới
docker compose up -d
```
Do MySQL cần thời gian khởi động (10-20s), Go App có thể sẽ in ra `Waiting for MySQL...` vài lần trong log rồi mới chạy. Bạn có thể xem log bằng `docker compose logs -f backend`.

### Test trên Web
Vào `http://localhost`. Thêm dữ liệu. Tắt bật container. Dữ liệu vẫn còn nguyên (nhờ Volume của MySQL).

### Test bằng DBeaver
1. Host: `localhost`
2. Port: `3306`
3. Username: `root`
4. Password: `secret`
5. Database: `todo_db`

Connect vào, Select bảng `todos`, bạn sẽ thấy dữ liệu nằm ở đó. Đây là cách Debug chuyên nghiệp.

---

## 📝 TỔNG KẾT
Hệ thống của bạn giờ đã có đủ 3 chân kiềng vững chắc: Frontend - Backend - Database.
Đây là mô hình tiêu chuẩn của mọi ứng dụng Web.

👉 **Bước tiếp theo:** Code xong rồi, làm sao để tự động test và build? Giai đoạn 7: **GitLab CI**.
