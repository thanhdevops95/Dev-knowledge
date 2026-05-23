GIAI ĐOẠN 3: THÊM CHỨC NĂNG TODO (VẪN LƯU RAM)
📌 MỤC TIÊU GIAI ĐOẠN 3
Sau khi hoàn thành giai đoạn này, bạn sẽ:

✅ Mở rộng từ Ping-Pong sang TODO App hoàn chỉnh
✅ Xây dựng CRUD (Create, Read, Update, Delete) operations
✅ Hiểu cách quản lý state phức tạp hơn
✅ Thành thạo RESTful API design
✅ Biết validate dữ liệu và xử lý edge cases
✅ Sẵn sàng thêm giao diện web (Giai đoạn 4)


🗂️ PHẦN 1: PHÂN TÍCH YÊU CẦU TODO APP
1.1. User Stories
Là người dùng, tôi muốn:

Tạo TODO mới với tiêu đề
Xem danh sách tất cả TODO
Xem chi tiết 1 TODO
Đánh dấu TODO đã hoàn thành/chưa hoàn thành
Chỉnh sửa tiêu đề TODO
Xóa TODO

1.2. Data Model
TODO Structure:
json{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Học Docker từ cơ bản",
  "completed": false,
  "created_at": "2026-01-25T10:30:00+07:00",
  "updated_at": "2026-01-25T10:30:00+07:00"
}
Giải thích fields:

id: UUID (Universally Unique Identifier) - ID duy nhất
title: Tiêu đề TODO (string, required)
completed: Trạng thái hoàn thành (boolean, default: false)
created_at: Thời gian tạo (timestamp)
updated_at: Thời gian cập nhật cuối (timestamp)

1.3. API Endpoints Design
MethodEndpointDescriptionRequest BodyResponseGET/todosLấy tất cả TODO-[{todo}, {todo}]GET/todos/:idLấy 1 TODO-{todo}POST/todosTạo TODO mới{title}{todo}PUT/todos/:idCập nhật TODO{title, completed}{todo}DELETE/todos/:idXóa TODO-204 No Content
Gateway Endpoints (Python):

Tương tự nhưng prefix /api: /api/todos, /api/todos/:id


🔧 PHẦN 2: XÂY DỰNG GO SERVICE - TODO BACKEND
2.1. Cập nhật main.go - Thêm TODO Structure
Mở file go-service/main.go, thay thế toàn bộ bằng code sau:
gopackage main

import (
	"net/http"
	"sync"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

// ==================== DATA STRUCTURES ====================

// Todo struct - Cấu trúc dữ liệu TODO
type Todo struct {
	ID        string    `json:"id"`
	Title     string    `json:"title"`
	Completed bool      `json:"completed"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// CreateTodoRequest - Request body khi tạo TODO
type CreateTodoRequest struct {
	Title string `json:"title" binding:"required"` // binding:"required" = validation
}

// UpdateTodoRequest - Request body khi cập nhật TODO
type UpdateTodoRequest struct {
	Title     *string `json:"title"`     // Con trỏ để phân biệt null vs empty
	Completed *bool   `json:"completed"` // Con trỏ để phân biệt null vs false
}

// Stats - Thống kê Ping/Pong (giữ lại từ Giai đoạn 2)
type Stats struct {
	SuccessCount int       `json:"success_count"`
	FailedCount  int       `json:"failed_count"`
	LastPingTime time.Time `json:"last_ping_time"`
}

// ==================== GLOBAL VARIABLES ====================

var (
	// todos map: key=ID, value=Todo object
	// Lưu trong RAM → restart thì mất
	todos = make(map[string]Todo)
	
	// stats cho Ping/Pong
	stats Stats
	
	// Mutex để đảm bảo thread-safe
	todosMutex sync.RWMutex // RWMutex: cho phép nhiều reader, 1 writer
	statsMutex sync.Mutex
)

// ==================== MAIN FUNCTION ====================

func main() {
	// Khởi tạo Gin router
	router := gin.Default()

	// Cấu hình CORS
	router.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Accept"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	// ===== Health & Stats Routes (từ Giai đoạn 2) =====
	router.GET("/health", healthCheck)
	router.POST("/ping", handlePing)
	router.GET("/stats", getStats)

	// ===== TODO Routes =====
	router.GET("/todos", getAllTodos)           // Lấy tất cả TODO
	router.GET("/todos/:id", getTodoByID)       // Lấy 1 TODO
	router.POST("/todos", createTodo)           // Tạo TODO mới
	router.PUT("/todos/:id", updateTodo)        // Cập nhật TODO
	router.DELETE("/todos/:id", deleteTodo)     // Xóa TODO

	// Chạy server
	router.Run(":8081")
}

// ==================== HEALTH & PING HANDLERS (từ Giai đoạn 2) ====================

func healthCheck(c *gin.Context) {
	// Thêm thông tin số lượng TODO
	todosMutex.RLock()
	todoCount := len(todos)
	todosMutex.RUnlock()

	c.JSON(http.StatusOK, gin.H{
		"status":      "healthy",
		"service":     "go-todo-service",
		"time":        time.Now(),
		"todo_count":  todoCount,
	})
}

func handlePing(c *gin.Context) {
	statsMutex.Lock()
	defer statsMutex.Unlock()

	stats.SuccessCount++
	stats.LastPingTime = time.Now()

	c.JSON(http.StatusOK, gin.H{
		"message":       "Pong",
		"timestamp":     time.Now(),
		"success_count": stats.SuccessCount,
	})
}

func getStats(c *gin.Context) {
	statsMutex.Lock()
	defer statsMutex.Unlock()

	c.JSON(http.StatusOK, stats)
}

// ==================== TODO HANDLERS ====================

// GET /todos - Lấy tất cả TODO
func getAllTodos(c *gin.Context) {
	todosMutex.RLock() // Read Lock (nhiều goroutine có thể đọc cùng lúc)
	defer todosMutex.RUnlock()

	// Convert map → slice để trả về JSON array
	todoList := make([]Todo, 0, len(todos))
	for _, todo := range todos {
		todoList = append(todoList, todo)
	}

	// Trả về array (ngay cả khi rỗng)
	c.JSON(http.StatusOK, todoList)
}

// GET /todos/:id - Lấy 1 TODO theo ID
func getTodoByID(c *gin.Context) {
	id := c.Param("id") // Lấy ID từ URL parameter

	todosMutex.RLock()
	defer todosMutex.RUnlock()

	// Tìm TODO trong map
	todo, exists := todos[id]
	if !exists {
		// Không tìm thấy → 404
		c.JSON(http.StatusNotFound, gin.H{
			"error": "TODO not found",
			"id":    id,
		})
		return
	}

	// Tìm thấy → trả về
	c.JSON(http.StatusOK, todo)
}

// POST /todos - Tạo TODO mới
func createTodo(c *gin.Context) {
	var req CreateTodoRequest

	// Bind JSON request body vào struct
	// ShouldBindJSON tự động validate "required" fields
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request body",
			"details": err.Error(),
		})
		return
	}

	// Validate: Title không được rỗng sau khi trim
	if len(req.Title) == 0 {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Title cannot be empty",
		})
		return
	}

	// Tạo TODO mới
	todo := Todo{
		ID:        uuid.New().String(), // Tạo UUID mới
		Title:     req.Title,
		Completed: false, // Mặc định chưa hoàn thành
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}

	// Lưu vào map
	todosMutex.Lock()
	todos[todo.ID] = todo
	todosMutex.Unlock()

	// Trả về TODO vừa tạo với status 201 Created
	c.JSON(http.StatusCreated, todo)
}

// PUT /todos/:id - Cập nhật TODO
func updateTodo(c *gin.Context) {
	id := c.Param("id")

	var req UpdateTodoRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "Invalid request body",
			"details": err.Error(),
		})
		return
	}

	todosMutex.Lock()
	defer todosMutex.Unlock()

	// Kiểm tra TODO có tồn tại không
	todo, exists := todos[id]
	if !exists {
		c.JSON(http.StatusNotFound, gin.H{
			"error": "TODO not found",
			"id":    id,
		})
		return
	}

	// Cập nhật các fields (chỉ cập nhật nếu được gửi lên)
	if req.Title != nil {
		// Validate title không rỗng
		if len(*req.Title) == 0 {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "Title cannot be empty",
			})
			return
		}
		todo.Title = *req.Title
	}

	if req.Completed != nil {
		todo.Completed = *req.Completed
	}

	// Cập nhật timestamp
	todo.UpdatedAt = time.Now()

	// Lưu lại vào map
	todos[id] = todo

	// Trả về TODO đã cập nhật
	c.JSON(http.StatusOK, todo)
}

// DELETE /todos/:id - Xóa TODO
func deleteTodo(c *gin.Context) {
	id := c.Param("id")

	todosMutex.Lock()
	defer todosMutex.Unlock()

	// Kiểm tra TODO có tồn tại không
	_, exists := todos[id]
	if !exists {
		c.JSON(http.StatusNotFound, gin.H{
			"error": "TODO not found",
			"id":    id,
		})
		return
	}

	// Xóa khỏi map
	delete(todos, id)

	// Trả về 204 No Content (không có body)
	c.Status(http.StatusNoContent)
}
2.2. Cài đặt thư viện UUID
bash# Di chuyển vào thư mục go-service
cd go-service

# Cài thư viện UUID
go get github.com/google/uuid

# Cập nhật dependencies
go mod tidy
2.3. Giải thích chi tiết code Go mới
UUID Generation:
goimport "github.com/google/uuid"

todo.ID = uuid.New().String()

uuid.New(): Tạo UUID version 4 (random)
.String(): Convert sang string format: 550e8400-e29b-41d4-a716-446655440000
Tại sao dùng UUID thay vì số đếm?

Tránh conflict khi có nhiều instance
Bảo mật hơn (không đoán được)
Dễ merge data từ nhiều nguồn



Pointer trong UpdateTodoRequest:
gotype UpdateTodoRequest struct {
	Title     *string `json:"title"`
	Completed *bool   `json:"completed"`
}
Vấn đề cần giải quyết:

User chỉ muốn cập nhật completed, không sửa title
Nếu dùng bool thay vì *bool:

completed: false → không biết là "giữ nguyên" hay "set = false"
completed không gửi lên → Go nhận false (zero value)



Giải pháp với pointer:
goif req.Completed != nil {
    todo.Completed = *req.Completed
}

nil: Field không được gửi lên → không cập nhật
*bool: Field có giá trị → cập nhật

Ví dụ:
json// Chỉ cập nhật completed
{
  "completed": true
}

// Chỉ cập nhật title
{
  "title": "Học Docker nâng cao"
}

// Cập nhật cả 2
{
  "title": "Học Kubernetes",
  "completed": false
}
RWMutex vs Mutex:
govar todosMutex sync.RWMutex
RWMutex (Read-Write Mutex):

RLock(): Read lock - nhiều goroutine đọc cùng lúc
Lock(): Write lock - chỉ 1 goroutine ghi, chặn tất cả đọc/ghi khác

Khi nào dùng gì:

Đọc nhiều: RLock() (getAllTodos, getTodoByID)
Ghi: Lock() (createTodo, updateTodo, deleteTodo)

Lợi ích:

Performance tốt hơn khi có nhiều read operations
Vẫn đảm bảo data consistency

Map operations:
gotodos = make(map[string]Todo)

Map trong Go: key-value store (như dictionary Python, object JS)
make(): Khởi tạo map rỗng

Các thao tác:
go// Thêm/Cập nhật
todos[id] = todo

// Đọc
todo, exists := todos[id]

// Xóa
delete(todos, id)

// Lấy số lượng
len(todos)
Convert Map → Slice:
gotodoList := make([]Todo, 0, len(todos))
for _, todo := range todos {
    todoList = append(todoList, todo)
}
Tại sao cần:

Map không có thứ tự
JSON array cần slice, không phải map
make([]Todo, 0, len(todos)): tạo slice với capacity = len(todos) để tránh realloc

2.4. Chạy Go Service mới
bash# Dừng Go service cũ nếu đang chạy (Ctrl+C)

# Chạy lại với code mới
go run main.go
```

**Output mong đợi:**
```
[GIN-debug] GET    /health                   --> main.healthCheck (4 handlers)
[GIN-debug] POST   /ping                     --> main.handlePing (4 handlers)
[GIN-debug] GET    /stats                    --> main.getStats (4 handlers)
[GIN-debug] GET    /todos                    --> main.getAllTodos (4 handlers)
[GIN-debug] GET    /todos/:id                --> main.getTodoByID (4 handlers)
[GIN-debug] POST   /todos                    --> main.createTodo (4 handlers)
[GIN-debug] PUT    /todos/:id                --> main.updateTodo (4 handlers)
[GIN-debug] DELETE /todos/:id                --> main.deleteTodo (4 handlers)
[GIN-debug] Listening and serving HTTP on :8081
2.5. Test Go TODO API với curl
Test 1: Lấy tất cả TODO (ban đầu rỗng)
bashcurl http://localhost:8081/todos
Kết quả:
json[]
Test 2: Tạo TODO mới
bashcurl -X POST http://localhost:8081/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Học Docker"}'
Kết quả:
json{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "title": "Học Docker",
  "completed": false,
  "created_at": "2026-01-25T16:30:00+07:00",
  "updated_at": "2026-01-25T16:30:00+07:00"
}
Lưu lại ID để test tiếp!
Test 3: Tạo thêm TODO
bashcurl -X POST http://localhost:8081/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Học Kubernetes"}'

curl -X POST http://localhost:8081/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Học GitLab CI/CD"}'
Test 4: Lấy tất cả TODO (giờ có 3 items)
bashcurl http://localhost:8081/todos
Kết quả:
json[
  {
    "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "title": "Học Docker",
    "completed": false,
    "created_at": "2026-01-25T16:30:00+07:00",
    "updated_at": "2026-01-25T16:30:00+07:00"
  },
  {
    "id": "a1b2c3d4-5678-90ab-cdef-1234567890ab",
    "title": "Học Kubernetes",
    "completed": false,
    "created_at": "2026-01-25T16:31:00+07:00",
    "updated_at": "2026-01-25T16:31:00+07:00"
  },
  {
    "id": "f9e8d7c6-b5a4-3210-fedc-ba9876543210",
    "title": "Học GitLab CI/CD",
    "completed": false,
    "created_at": "2026-01-25T16:32:00+07:00",
    "updated_at": "2026-01-25T16:32:00+07:00"
  }
]
Test 5: Lấy 1 TODO theo ID
bash# Thay YOUR_TODO_ID bằng ID thực tế từ kết quả trên
curl http://localhost:8081/todos/7c9e6679-7425-40de-944b-e07fc1f90ae7
Kết quả:
json{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "title": "Học Docker",
  "completed": false,
  "created_at": "2026-01-25T16:30:00+07:00",
  "updated_at": "2026-01-25T16:30:00+07:00"
}
Test 6: Cập nhật TODO - đánh dấu hoàn thành
bashcurl -X PUT http://localhost:8081/todos/7c9e6679-7425-40de-944b-e07fc1f90ae7 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
Kết quả:
json{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "title": "Học Docker",
  "completed": true,
  "created_at": "2026-01-25T16:30:00+07:00",
  "updated_at": "2026-01-25T16:35:00+07:00"
}
Test 7: Cập nhật TODO - sửa title
bashcurl -X PUT http://localhost:8081/todos/7c9e6679-7425-40de-944b-e07fc1f90ae7 \
  -H "Content-Type: application/json" \
  -d '{"title":"Học Docker từ cơ bản đến nâng cao"}'
Test 8: Xóa TODO
bashcurl -X DELETE http://localhost:8081/todos/7c9e6679-7425-40de-944b-e07fc1f90ae7 -i
```

**Kết quả:**
```
HTTP/1.1 204 No Content
...
Test 9: Kiểm tra lại danh sách (TODO đã xóa)
bashcurl http://localhost:8081/todos
Test 10: Test error cases
bash# Lấy TODO không tồn tại
curl http://localhost:8081/todos/invalid-id

# Tạo TODO thiếu title
curl -X POST http://localhost:8081/todos \
  -H "Content-Type: application/json" \
  -d '{}'

# Tạo TODO với title rỗng
curl -X POST http://localhost:8081/todos \
  -H "Content-Type: application/json" \
  -d '{"title":""}'

🐍 PHẦN 3: CẬP NHẬT PYTHON SERVICE - TODO GATEWAY
3.1. Cập nhật app.py - Thêm TODO endpoints
Mở file python-service/app.py, thay thế toàn bộ bằng code sau:
pythonfrom flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import logging
from datetime import datetime

# ==================== FLASK APP SETUP ====================

app = Flask(__name__)

# Cấu hình CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# URL của Go service
GO_SERVICE_URL = "http://localhost:8081"

# ==================== HELPER FUNCTIONS ====================

def call_go_service(method, endpoint, json_data=None, timeout=5):
    """
    Helper function để gọi Go service
    
    Args:
        method: HTTP method ('GET', 'POST', 'PUT', 'DELETE')
        endpoint: Endpoint path (ví dụ: '/todos')
        json_data: Request body (dict)
        timeout: Timeout in seconds
    
    Returns:
        tuple: (success: bool, data: dict, status_code: int)
    """
    url = f"{GO_SERVICE_URL}{endpoint}"
    
    try:
        logger.info(f"{method} {url}")
        
        # Gọi request tương ứng
        if method == 'GET':
            response = requests.get(url, timeout=timeout)
        elif method == 'POST':
            response = requests.post(url, json=json_data, timeout=timeout)
        elif method == 'PUT':
            response = requests.put(url, json=json_data, timeout=timeout)
        elif method == 'DELETE':
            response = requests.delete(url, timeout=timeout)
        else:
            return False, {'error': 'Invalid HTTP method'}, 400
        
        # Kiểm tra status code
        if response.status_code == 204:
            # No Content - DELETE success
            return True, None, 204
        
        # Parse JSON response
        try:
            data = response.json()
        except:
            data = {'message': 'No JSON response'}
        
        # Nếu Go trả về error (4xx, 5xx)
        if response.status_code >= 400:
            logger.error(f"Go service error: {response.status_code} - {data}")
            return False, data, response.status_code
        
        logger.info(f"Go service success: {response.status_code}")
        return True, data, response.status_code
        
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Go service")
        return False, {'error': 'Go service unavailable'}, 503
        
    except requests.exceptions.Timeout:
        logger.error("Go service timeout")
        return False, {'error': 'Go service timeout'}, 504
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False, {'error': str(e)}, 500

# ==================== HEALTH & PING ROUTES (từ Giai đoạn 2) ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'python-gateway',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/ping', methods=['POST'])
def ping():
    """Ping endpoint - forward to Go service"""
    success, data, status = call_go_service('POST', '/ping')
    
    if not success:
        return jsonify(data), status
    
    return jsonify({
        'status': 'success',
        'message': 'Ping forwarded successfully',
        'go_response': data,
        'gateway_timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get ping stats from Go service"""
    success, data, status = call_go_service('GET', '/stats')
    
    if not success:
        return jsonify(data), status
    
    return jsonify({
        'status': 'success',
        'data': data,
        'retrieved_at': datetime.now().isoformat()
    }), 200

# ==================== TODO ROUTES ====================

@app.route('/api/todos', methods=['GET'])
def get_all_todos():
    """
    GET /api/todos
    Lấy tất cả TODO từ Go service
    """
    logger.info("GET /api/todos - Fetching all todos")
    
    success, data, status = call_go_service('GET', '/todos')
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': 'Failed to fetch todos',
            'error': data
        }), status
    
    return jsonify({
        'status': 'success',
        'data': data,
        'count': len(data) if data else 0,
        'retrieved_at': datetime.now().isoformat()
    }), 200


@app.route('/api/todos/<todo_id>', methods=['GET'])
def get_todo_by_id(todo_id):
    """
    GET /api/todos/:id
    Lấy 1 TODO theo ID
    """
    logger.info(f"GET /api/todos/{todo_id}")
    
    success, data, status = call_go_service('GET', f'/todos/{todo_id}')
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': f'TODO {todo_id} not found',
            'error': data
        }), status
    
    return jsonify({
        'status': 'success',
        'data': data
    }), 200


@app.route('/api/todos', methods=['POST'])
def create_todo():
    """
    POST /api/todos
    Tạo TODO mới
    
    Request body:
    {
        "title": "TODO title"
    }
    """
    logger.info("POST /api/todos - Creating new todo")
    
    # Validate request body
    if not request.json:
        return jsonify({
            'status': 'error',
            'message': 'Request body must be JSON'
        }), 400
    
    title = request.json.get('title')
    
    # Validate title
    if not title:
        return jsonify({
            'status': 'error',
            'message': 'Title is required'
        }), 400
    
    if not isinstance(title, str) or len(title.strip()) == 0:
        return jsonify({
            'status': 'error',
            'message': 'Title must be a non-empty string'
        }), 400
    
    # Gọi Go service
    success, data, status = call_go_service('POST', '/todos', {'title': title})
    
    if not success:
        return jsonify({
            'status': 'error',
            'message': 'Failed to create todo',
            'error': data
        }), status
    
    logger.info(f"TODO created successfully: {data.get('id')}")
return jsonify({
    'status': 'success',
    'message': 'TODO created successfully',
    'data': data
}), 201
@app.route('/api/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
"""
PUT /api/todos/:id
Cập nhật TODO
Request body (tất cả optional):
{
    "title": "New title",
    "completed": true
}
"""
logger.info(f"PUT /api/todos/{todo_id}")

# Validate request body
if not request.json:
    return jsonify({
        'status': 'error',
        'message': 'Request body must be JSON'
    }), 400

update_data = {}

# Validate và thêm title nếu có
if 'title' in request.json:
    title = request.json['title']
    if not isinstance(title, str) or len(title.strip()) == 0:
        return jsonify({
            'status': 'error',
            'message': 'Title must be a non-empty string'
        }), 400
    update_data['title'] = title

# Validate và thêm completed nếu có
if 'completed' in request.json:
    completed = request.json['completed']
    if not isinstance(completed, bool):
        return jsonify({
            'status': 'error',
            'message': 'Completed must be a boolean'
        }), 400
    update_data['completed'] = completed

# Kiểm tra có data để update không
if not update_data:
    return jsonify({
        'status': 'error',
        'message': 'No valid fields to update'
    }), 400

# Gọi Go service
success, data, status = call_go_service('PUT', f'/todos/{todo_id}', update_data)

if not success:
    return jsonify({
        'status': 'error',
        'message': f'Failed to update TODO {todo_id}',
        'error': data
    }), status

logger.info(f"TODO {todo_id} updated successfully")

return jsonify({
    'status': 'success',
    'message': 'TODO updated successfully',
    'data': data
}), 200
@app.route('/api/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
"""
DELETE /api/todos/:id
Xóa TODO
"""
logger.info(f"DELETE /api/todos/{todo_id}")
success, data, status = call_go_service('DELETE', f'/todos/{todo_id}')

if not success:
    return jsonify({
        'status': 'error',
        'message': f'Failed to delete TODO {todo_id}',
        'error': data
    }), status

logger.info(f"TODO {todo_id} deleted successfully")

return jsonify({
    'status': 'success',
    'message': f'TODO {todo_id} deleted successfully'
}), 200  # Trả về 200 thay vì 204 để có message
==================== TESTING & DEBUG ROUTES ====================
@app.route('/api/test-connectivity', methods=['GET'])
def test_connectivity():
"""Test kết nối Python ↔ Go"""
try:
response = requests.get(f"{GO_SERVICE_URL}/health", timeout=3)
    if response.status_code == 200:
        return jsonify({
            'status': 'connected',
            'message': 'Python can reach Go service',
            'go_health': response.json()
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Go service responded but not healthy',
            'status_code': response.status_code
        }), 500
        
except Exception as e:
    return jsonify({
        'status': 'disconnected',
        'message': 'Cannot reach Go service',
        'error': str(e)
    }), 503
==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
"""Handle 404 errors"""
return jsonify({
'status': 'error',
'message': 'Endpoint not found',
'path': request.path
}), 404
@app.errorhandler(405)
def method_not_allowed(error):
"""Handle 405 errors"""
return jsonify({
'status': 'error',
'message': 'Method not allowed',
'method': request.method,
'path': request.path
}), 405
@app.errorhandler(500)
def internal_error(error):
"""Handle 500 errors"""
logger.error(f"Internal error: {str(error)}")
return jsonify({
'status': 'error',
'message': 'Internal server error'
}), 500
==================== MAIN ====================
if name == 'main':
logger.info("=" * 50)
logger.info("Starting Python TODO Gateway Service")
logger.info(f"Port: 8080")
logger.info(f"Go Service URL: {GO_SERVICE_URL}")
logger.info("=" * 50)
app.run(
    host='0.0.0.0',
    port=8080,
    debug=True
)

### 3.2. Giải thích chi tiết code Python mới

#### **Helper Function:**
```python
def call_go_service(method, endpoint, json_data=None, timeout=5):
    ...
```

**Lợi ích:**
- Tránh duplicate code
- Xử lý error tập trung
- Dễ maintain và test

**Cách sử dụng:**
```python
# GET request
success, data, status = call_go_service('GET', '/todos')

# POST request
success, data, status = call_go_service('POST', '/todos', {'title': 'Test'})

# PUT request
success, data, status = call_go_service('PUT', '/todos/123', {'completed': True})

# DELETE request
success, data, status = call_go_service('DELETE', '/todos/123')
```

#### **Validation layers:**
```python
# Layer 1: Kiểm tra có JSON không
if not request.json:
    return jsonify({'error': 'Request body must be JSON'}), 400

# Layer 2: Kiểm tra field required
title = request.json.get('title')
if not title:
    return jsonify({'error': 'Title is required'}), 400

# Layer 3: Kiểm tra type và value
if not isinstance(title, str) or len(title.strip()) == 0:
    return jsonify({'error': 'Title must be a non-empty string'}), 400
```

**Tại sao cần validate ở Python nếu Go đã validate?**
- **Defense in depth**: Nhiều lớp bảo mật
- **Better UX**: Lỗi rõ ràng hơn từ gateway
- **Reduce load**: Không gọi Go nếu data rõ ràng sai

#### **Error handlers:**
```python
@app.errorhandler(404)
def not_found(error):
    ...
```
- Tự động bắt mọi 404 error trong app
- Trả về JSON thay vì HTML (mặc định Flask)
- Consistent error format

### 3.3. Chạy Python Service mới
```bash
# Dừng Python service cũ (Ctrl+C)

# Đảm bảo venv đã activate
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Chạy lại
python app.py
```

**Output mong đợi:**
==================================================
Starting Python TODO Gateway Service
Port: 8080
Go Service URL: http://localhost:8081

Serving Flask app 'app'
Debug mode: on
Running on all addresses (0.0.0.0)
Running on http://127.0.0.1:8080


### 3.4. Test Python TODO Gateway với curl

**Test 1: Tạo TODO qua gateway**
```bash
curl -X POST http://localhost:8080/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Học Docker qua Gateway"}'
```

**Kết quả:**
```json
{
  "data": {
    "id": "abc123...",
    "title": "Học Docker qua Gateway",
    "completed": false,
    "created_at": "2026-01-25T17:00:00+07:00",
    "updated_at": "2026-01-25T17:00:00+07:00"
  },
  "message": "TODO created successfully",
  "status": "success"
}
```

**Test 2: Lấy tất cả TODO qua gateway**
```bash
curl http://localhost:8080/api/todos
```

**Kết quả:**
```json
{
  "count": 3,
  "data": [
    {...},
    {...},
    {...}
  ],
  "retrieved_at": "2026-01-25T17:01:00",
  "status": "success"
}
```

**Test 3: Validation errors**
```bash
# Title rỗng
curl -X POST http://localhost:8080/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":""}'

# Thiếu title
curl -X POST http://localhost:8080/api/todos \
  -H "Content-Type: application/json" \
  -d '{}'

# Không phải JSON
curl -X POST http://localhost:8080/api/todos \
  -H "Content-Type: application/json" \
  -d 'not json'
```

**Test 4: Cập nhật qua gateway**
```bash
# Lấy ID từ lệnh create ở trên
TODO_ID="abc123..."

# Chỉ cập nhật completed
curl -X PUT http://localhost:8080/api/todos/$TODO_ID \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

# Chỉ cập nhật title
curl -X PUT http://localhost:8080/api/todos/$TODO_ID \
  -H "Content-Type: application/json" \
  -d '{"title":"Học Docker - Hoàn thành"}'

# Cập nhật cả 2
curl -X PUT http://localhost:8080/api/todos/$TODO_ID \
  -H "Content-Type: application/json" \
  -d '{"title":"Completed Task","completed":true}'
```

**Test 5: Xóa qua gateway**
```bash
curl -X DELETE http://localhost:8080/api/todos/$TODO_ID
```

**Test 6: Error handling**
```bash
# TODO không tồn tại
curl http://localhost:8080/api/todos/invalid-id-123

# Endpoint không tồn tại
curl http://localhost:8080/api/invalid-endpoint

# Method không được phép
curl -X PATCH http://localhost:8080/api/todos
```

---

## 🧪 PHẦN 4: TEST TỔNG HỢP VỚI POSTMAN

### 4.1. Tạo Postman Collection mới

1. Mở Postman
2. New Collection: "TODO App - Complete CRUD"
3. Tạo folder: "Go Service Direct"
4. Tạo folder: "Python Gateway"

### 4.2. Setup Collection Variables

**Variables:**
- `go_url`: `http://localhost:8081`
- `py_url`: `http://localhost:8080`
- `todo_id`: (để trống, sẽ set tự động)

### 4.3. Requests trong folder "Python Gateway"

**1. Create TODO**
- Method: POST
- URL: `{{py_url}}/api/todos`
- Body (raw JSON):
```json
{
  "title": "Test TODO from Postman"
}
```
- Tests (lưu ID vào variable):
```javascript
var jsonData = pm.response.json();
if (jsonData.status === 'success') {
    pm.collectionVariables.set("todo_id", jsonData.data.id);
}
```

**2. Get All TODOs**
- Method: GET
- URL: `{{py_url}}/api/todos`

**3. Get TODO by ID**
- Method: GET
- URL: `{{py_url}}/api/todos/{{todo_id}}`

**4. Update TODO - Mark Complete**
- Method: PUT
- URL: `{{py_url}}/api/todos/{{todo_id}}`
- Body:
```json
{
  "completed": true
}
```

**5. Update TODO - Change Title**
- Method: PUT
- URL: `{{py_url}}/api/todos/{{todo_id}}`
- Body:
```json
{
  "title": "Updated Title from Postman"
}
```

**6. Delete TODO**
- Method: DELETE
- URL: `{{py_url}}/api/todos/{{todo_id}}`

### 4.4. Chạy Collection Runner

1. Click Collection → Run
2. Select tất cả requests
3. Click "Run TODO App"
4. Quan sát kết quả

---

## 📊 PHẦN 5: SO SÁNH TRƯỚC VÀ SAU GIAI ĐOẠN 3

### 5.1. Trước (Giai đoạn 2)
Chức năng:

Ping/Pong đơn giản
Đếm số lần ping
Không có business logic thực sự

Data:

1 struct Stats đơn giản
2 counters: success, failed


### 5.2. Sau (Giai đoạn 3)
Chức năng:

Full CRUD operations
TODO management hoàn chỉnh
Validation đầy đủ
Error handling tốt

Data:

Struct Todo phức tạp (5 fields)
Map storage với UUID keys
Timestamp tracking
Thread-safe với RWMutex


### 5.3. Vấn đề còn tồn tại

❌ **Dữ liệu vẫn lưu trong RAM**
```bash
# Tạo 10 TODO
for i in {1..10}; do
  curl -X POST http://localhost:8080/api/todos \
    -H "Content-Type: application/json" \
    -d "{\"title\":\"TODO $i\"}"
done

# Kiểm tra
curl http://localhost:8080/api/todos
# → Có 10 TODO

# Restart Go service (Ctrl+C, go run main.go)

# Kiểm tra lại
curl http://localhost:8080/api/todos
# → [] (RỖNG - DỮ LIỆU MẤT!)
```

**→ Cần giải quyết ở Giai đoạn 6 (Docker Volumes)**

---

## 🎯 PHẦN 6: BÀI TẬP THỰC HÀNH

### Bài 1: Thêm Filter cho Get All TODOs

**Yêu cầu:** Thêm query parameters để filter TODO

**Ví dụ:**
```bash
# Lấy chỉ TODO đã hoàn thành
GET /api/todos?completed=true

# Lấy chỉ TODO chưa hoàn thành
GET /api/todos?completed=false

# Tìm kiếm theo title
GET /api/todos?search=docker
```

**Gợi ý Go:**
```go
func getAllTodos(c *gin.Context) {
    completedParam := c.Query("completed") // Lấy query param
    searchParam := c.Query("search")
    
    todosMutex.RLock()
    defer todosMutex.RUnlock()
    
    todoList := make([]Todo, 0)
    for _, todo := range todos {
        // Filter logic here
        if completedParam != "" {
            // Parse và so sánh completed
        }
        if searchParam != "" {
            // Search trong title
        }
        todoList = append(todoList, todo)
    }
    
    c.JSON(http.StatusOK, todoList)
}
```

### Bài 2: Thêm Pagination

**Yêu cầu:** Thêm phân trang cho danh sách TODO
```bash
GET /api/todos?page=1&limit=10
GET /api/todos?page=2&limit=10
```

**Response format:**
```json
{
  "data": [...],
  "page": 1,
  "limit": 10,
  "total": 50,
  "total_pages": 5
}
```

### Bài 3: Thêm Priority field

**Yêu cầu:** Mở rộng TODO struct với priority

**Thay đổi:**
```go
type Todo struct {
    ID        string    `json:"id"`
    Title     string    `json:"title"`
    Completed bool      `json:"completed"`
    Priority  string    `json:"priority"` // "low", "medium", "high"
    CreatedAt time.Time `json:"created_at"`
    UpdatedAt time.Time `json:"updated_at"`
}
```

**Validation:** Priority chỉ được là "low", "medium", hoặc "high"

### Bài 4: Bulk Delete

**Yêu cầu:** Xóa nhiều TODO cùng lúc
```bash
DELETE /api/todos/bulk
Body: {
  "ids": ["id1", "id2", "id3"]
}
```

**Response:**
```json
{
  "deleted_count": 3,
  "failed_ids": []
}
```

---

## ✅ PHẦN 7: CHECKLIST HOÀN THÀNH GIAI ĐOẠN 3

- [ ] Go service có đầy đủ CRUD endpoints
- [ ] Python gateway có đầy đủ CRUD endpoints
- [ ] Tạo TODO thành công qua cả 2 services
- [ ] Lấy danh sách TODO hoạt động
- [ ] Lấy 1 TODO theo ID hoạt động
- [ ] Cập nhật TODO (title và completed) hoạt động
- [ ] Xóa TODO hoạt động
- [ ] Validation hoạt động đúng (title required, không rỗng)
- [ ] Error handling hoạt động (404, 400, 503...)
- [ ] Hiểu được UUID và tại sao dùng UUID
- [ ] Hiểu được pointer trong Go UpdateTodoRequest
- [ ] Hiểu được RWMutex vs Mutex
- [ ] Test được với curl
- [ ] Test được với Postman
- [ ] Làm được ít nhất 1 bài tập thực hành
- [ ] Nhận ra vấn đề data loss khi restart

---

## 🐛 PHẦN 8: XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: UUID import error (Go)
cannot find package "github.com/google/uuid"

**Giải pháp:**
```bash
cd go-service
go get github.com/google/uuid
go mod tidy
```

### Lỗi 2: JSON parsing error

**Triệu chứng:**
```json
{
  "error": "invalid character 'n' looking for beginning of value"
}
```

**Nguyên nhân:** Request body không phải JSON hợp lệ

**Kiểm tra:**
```bash
# Sai - thiếu quotes
curl -X POST ... -d '{title:Test}'

# Đúng
curl -X POST ... -d '{"title":"Test"}'
```

### Lỗi 3: 404 Not Found

**Triệu chứng:**
```json
{
  "error": "TODO not found",
  "id": "abc123"
}
```

**Checklist:**
1. [ ] ID có chính xác không? (copy/paste đúng)
2. [ ] TODO đó có tồn tại không? (GET /todos trước)
3. [ ] Service có bị restart không? (data mất)

### Lỗi 4: Race condition

**Triệu chứng:** Data inconsistent khi có nhiều requests đồng thời

**Kiểm tra:**
```bash
# Gọi nhiều requests cùng lúc
for i in {1..100}; do
  curl -X POST http://localhost:8081/todos \
    -H "Content-Type: application/json" \
    -d "{\"title\":\"TODO $i\"}" &
done

# Đợi tất cả hoàn thành
wait

# Kiểm tra count
curl http://localhost:8081/todos | jq 'length'
# Phải là 100
```

**Giải pháp:** Đã được xử lý bằng Mutex trong code

---

## 📚 PHẦN 9: TÀI LIỆU THAM KHẢO

### Go:
- UUID package: https://github.com/google/uuid
- Go maps: https://go.dev/blog/maps
- Pointers in Go: https://go.dev/tour/moretypes/1
- RWMutex: https://pkg.go.dev/sync#RWMutex

### Python:
- Flask routing: https://flask.palletsprojects.com/en/3.0.x/quickstart/#routing
- Request data: https://flask.palletsprojects.com/en/3.0.x/quickstart/#accessing-request-data
- Error handling: https://flask.palletsprojects.com/en/3.0.x/errorhandling/

### RESTful API Design:
- Best practices: https://restfulapi.net/
- HTTP methods: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
- Status codes guide: https://httpstatuses.com/

---

## 🎊 KẾT LUẬN GIAI ĐOẠN 3

Chúc mừng! Bạn đã hoàn thành Giai đoạn 3 - TODO App với đầy đủ CRUD operations!

**Đã đạt được:**
✅ Full TODO application functionality  
✅ RESTful API design chuẩn  
✅ Validation và error handling đầy đủ  
✅ Thread-safe operations  
✅ Clean code structure  

**Vấn đề cần giải quyết tiếp:**
❌ Chưa có giao diện web (chỉ có API)  
❌ Dữ liệu vẫn lưu RAM (mất khi restart)  
❌ Chưa có Docker (chạy bare metal)  
❌ Test thủ công với curl/Postman