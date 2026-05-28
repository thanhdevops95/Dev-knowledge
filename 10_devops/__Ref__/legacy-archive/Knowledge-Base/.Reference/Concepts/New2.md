# GIAI ĐOẠN 2: XÂY DỰNG APP CƠ BẢN - BARE METAL (PING-PONG)

## 📌 MỤC TIÊU GIAI ĐOẠN 2
Sau khi hoàn thành giai đoạn này, bạn sẽ:

✅ Xây dựng được Go Backend Service xử lý Ping/Pong  
✅ Xây dựng được Python Gateway API  
✅ Hiểu rõ cách 2 service giao tiếp qua HTTP  
✅ Biết cách debug và xử lý lỗi cơ bản  
✅ Nắm được khái niệm lưu trữ dữ liệu trong RAM  
✅ Sẵn sàng mở rộng sang TODO App hoàn chỉnh

---

## 🗂️ PHẦN 1: CHUẨN BỊ CẤU TRÚC DỰ ÁN

### 1.1. Tạo thư mục dự án

```bash
# Tạo thư mục gốc
mkdir todo-app-devsecops
cd todo-app-devsecops

# Tạo cấu trúc thư mục
mkdir -p go-service
mkdir -p python-service
mkdir -p frontend
mkdir -p docs
```

**Giải thích cấu trúc:**

```
todo-app-devsecops/
├── go-service/          ← Backend xử lý logic (Go)
├── python-service/      ← API Gateway (Python Flask)
├── frontend/            ← Giao diện web (HTML/CSS/JS)
├── docs/                ← Tài liệu, ghi chú
└── README.md            ← Hướng dẫn dự án
```

### 1.2. Tạo file README.md

```bash
# Tạo file README trong thư mục gốc
cd todo-app-devsecops
```

Tạo file `README.md` với nội dung:

```markdown
# TODO App - DevSecOps Learning Project

## Mô tả
Dự án xây dựng TODO application từ cơ bản đến chuyên gia DevSecOps

## Cấu trúc
- `go-service/`: Backend service (Go)
- `python-service/`: API Gateway (Python Flask)
- `frontend/`: Web UI (HTML/CSS/JS)

## Giai đoạn hiện tại
Giai đoạn 2: Ping-Pong Service

## Cách chạy
Xem hướng dẫn trong từng thư mục con
```

---

## 🔧 PHẦN 2: XÂY DỰNG GO SERVICE (BACKEND)

### 2.1. Khởi tạo Go Module

```bash
# Di chuyển vào thư mục go-service
cd go-service

# Khởi tạo Go module
go mod init github.com/yourusername/todo-go-service
```

**Giải thích:**

go mod init: Tạo file go.mod để quản lý dependencies
github.com/yourusername/todo-go-service: Module path (có thể thay bằng tên bất kỳ)
File go.mod sẽ được tạo tự động

### 2.2. Cài đặt thư viện cần thiết

```bash
# Cài Gin framework (web framework cho Go)
go get -u github.com/gin-gonic/gin

# Cài CORS middleware
go get -u github.com/gin-contrib/cors
```

**Giải thích:**

github.com/gin-gonic/gin: Framework web nhanh, dễ dùng cho Go
github.com/gin-contrib/cors: Middleware xử lý Cross-Origin Resource Sharing
go get -u: Download và cài đặt package

### 2.3. Tạo file main.go - Version 1 (Ping-Pong đơn giản)

Tạo file `main.go` trong thư mục `go-service/`:

```go
package main

import (
	"net/http"
	"sync"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

// Cấu trúc dữ liệu lưu thống kê
type Stats struct {
	SuccessCount int       `json:"success_count"` // Số lần ping thành công
	FailedCount  int       `json:"failed_count"`  // Số lần ping thất bại
	LastPingTime time.Time `json:"last_ping_time"` // Thời gian ping gần nhất
}

// Biến toàn cục lưu stats (lưu trong RAM)
var (
	stats Stats      // Dữ liệu thống kê
	mutex sync.Mutex // Mutex để đảm bảo thread-safe khi nhiều request đồng thời
)

func main() {
	// Khởi tạo Gin router
	router := gin.Default()

	// Cấu hình CORS (cho phép frontend gọi API)
	router.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"}, // Cho phép tất cả origins (chỉ dùng cho dev)
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	// Route: Health check
	router.GET("/health", healthCheck)

	// Route: Ping - nhận tín hiệu ping
	router.POST("/ping", handlePing)

	// Route: Stats - lấy thống kê
	router.GET("/stats", getStats)

	// Chạy server trên port 8081
	router.Run(":8081")
}

// Handler: Health check
func healthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status":  "healthy",
		"service": "go-ping-service",
		"time":    time.Now(),
	})
}

// Handler: Nhận ping và trả về pong
func handlePing(c *gin.Context) {
	// Lock để đảm bảo chỉ 1 goroutine cập nhật stats tại 1 thời điểm
	mutex.Lock()
	defer mutex.Unlock() // Unlock khi hàm kết thúc

	// Tăng counter thành công
	stats.SuccessCount++
	stats.LastPingTime = time.Now()

	// Trả về response
	c.JSON(http.StatusOK, gin.H{
		"message":       "Pong",
		"timestamp":     time.Now(),
		"success_count": stats.SuccessCount,
	})
}

// Handler: Lấy thống kê
func getStats(c *gin.Context) {
	// Lock khi đọc để tránh race condition
	mutex.Lock()
	defer mutex.Unlock()

	c.JSON(http.StatusOK, stats)
}
```

### 2.4. Giải thích chi tiết code Go

**Import packages:**

```go
import (
	"net/http"      // Các hằng số HTTP (StatusOK, StatusBadRequest...)
	"sync"          // Mutex để đồng bộ hóa
	"time"          // Xử lý thời gian

	"github.com/gin-contrib/cors" // CORS middleware
	"github.com/gin-gonic/gin"    // Gin framework
)
```

**Struct Stats:**

```go
type Stats struct {
	SuccessCount int       `json:"success_count"` 
	FailedCount  int       `json:"failed_count"`  
	LastPingTime time.Time `json:"last_ping_time"`
}
```

- **Struct**: Kiểu dữ liệu tùy chỉnh, giống class trong OOP
Backtick `json:"..."`: Tag để convert struct ↔ JSON

SuccessCount → "success_count" trong JSON


- **time.Time**: Kiểu dữ liệu thời gian của Go

**Biến toàn cục:**

```go
var (
	stats Stats      
	mutex sync.Mutex 
)
```

- **stats**: Biến lưu trữ dữ liệu trong RAM (mất khi restart)
- **mutex**: Khóa để tránh 2 request cùng lúc sửa stats → tránh data race

**Main function:**

```go
router := gin.Default()
```

- Khởi tạo Gin router với logger và recovery middleware mặc định

```go
router.Use(cors.New(cors.Config{...}))
```

- **CORS**: Cross-Origin Resource Sharing
- Cho phép frontend (chạy trên port khác) gọi API này
- `AllowOrigins: []string{"*"}`: Cho phép mọi domain (chỉ dùng dev, production cần cụ thể)

```go
router.GET("/health", healthCheck)
router.POST("/ping", handlePing)
router.GET("/stats", getStats)
```

- Đăng ký routes (endpoint) với handler functions
- `GET /health`: Kiểm tra service có sống không
- `POST /ping`: Nhận ping
- `GET /stats`: Lấy thống kê

```go
router.Run(":8081")
```

- Chạy HTTP server trên port 8081
- Blocking call (chương trình sẽ chờ tại đây)

**Handler functions:**

*healthCheck:*

```go
c.JSON(http.StatusOK, gin.H{...})
```

- `c`: Context của Gin, chứa thông tin request/response
- `JSON()`: Trả về response dạng JSON
- `http.StatusOK`: HTTP 200
- `gin.H`: Shorthand cho `map[string]interface{}`

*handlePing:*

```go
mutex.Lock()
defer mutex.Unlock()
```

- `Lock`: Khóa, chỉ 1 goroutine vào được
- `defer`: Thực thi khi hàm kết thúc (giống finally)
- Đảm bảo unlock ngay cả khi có lỗi

```go
stats.SuccessCount++
stats.LastPingTime = time.Now()
```

- Tăng counter
- Cập nhật thời gian

### 2.5. Chạy Go Service

```bash
# Trong thư mục go-service/
go run main.go
```

**Output mong đợi:**
```
[GIN-debug] [WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.

[GIN-debug] GET    /health                   --> main.healthCheck (4 handlers)
[GIN-debug] POST   /ping                     --> main.handlePing (4 handlers)
[GIN-debug] GET    /stats                    --> main.getStats (4 handlers)
[GIN-debug] Listening and serving HTTP on :8081
```

### 2.6. Test Go Service với curl

Mở terminal mới (giữ nguyên terminal cũ đang chạy Go):

```bash
# Test 1: Health check
curl http://localhost:8081/health
```

Kết quả mong đợi:

```json
  "service": "go-ping-service",
  "status": "healthy",
  "time": "2026-01-25T15:30:00+07:00"
}
```

```bash
# Test 2: Ping
curl -X POST http://localhost:8081/ping
```

Kết quả:

```json
  "message": "Pong",
  "success_count": 1,
  "timestamp": "2026-01-25T15:31:00+07:00"
}
```

```bash
# Test 3: Ping nhiều lần
curl -X POST http://localhost:8081/ping
curl -X POST http://localhost:8081/ping
curl -X POST http://localhost:8081/ping
```

```bash
# Test 4: Lấy stats
curl http://localhost:8081/stats
```

Kết quả:

```json
  "success_count": 4,
  "failed_count": 0,
  "last_ping_time": "2026-01-25T15:32:00+07:00"
}
```

### 2.7. Xử lý lỗi Go Service

#### **Lỗi 1: go: command not found**
```
Nguyên nhân: Go chưa cài đặt hoặc chưa có trong PATH
Giải pháp: Quay lại Giai đoạn 1, cài lại Go
```

#### **Lỗi 2: cannot find package**
```
go: cannot find module providing package github.com/gin-gonic/gin
```

Giải pháp:

```bash
go mod tidy  # Tải về các dependencies còn thiếu
```

#### **Lỗi 3: port already in use**
```
listen tcp :8081: bind: address already in use
```

Giải pháp:

```bash
# Windows
netstat -ano | findstr :8081
taskkill /PID [PID_NUMBER] /F

# Linux/Mac
lsof -i :8081
kill -9 [PID]

# Hoặc đổi port trong code: router.Run(":8082")
```

#### **Lỗi 4: CORS error (sẽ gặp khi thêm frontend)**
```
Access to fetch at 'http://localhost:8081/ping' from origin 'http://localhost:80' 
has been blocked by CORS policy
```

Giải pháp: Đã được xử lý sẵn bằng cors middleware trong code

---

## 🐍 PHẦN 3: XÂY DỰNG PYTHON SERVICE (API GATEWAY)

### 3.1. Khởi tạo Python Project

```bash
# Di chuyển vào thư mục python-service
cd ../python-service

# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

**Giải thích:**

- **Virtual environment**: Môi trường Python độc lập
- Tránh conflict giữa các project
- Mỗi project có dependencies riêng

### 3.2. Cài đặt thư viện

Tạo file `requirements.txt`:

```txt
Flask==3.0.0
Flask-CORS==4.0.0
requests==2.31.0
```

**Giải thích:**

- **Flask**: Web framework cho Python (nhẹ, đơn giản)
- **Flask-CORS**: Xử lý CORS cho Flask
- **requests**: Thư viện gọi HTTP requests (gọi sang Go service)

Cài đặt:

```bash
pip install -r requirements.txt
```

### 3.3. Tạo file app.py - Version 1 (Gateway đơn giản)

Tạo file `app.py` trong `python-service/`:

```python
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import logging
from datetime import datetime

# Khởi tạo Flask app
app = Flask(__name__)

# Cấu hình CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# URL của Go service
GO_SERVICE_URL = "http://localhost:8081"

# ==================== ROUTES ====================

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    Kiểm tra Python service có hoạt động không
    """
    return jsonify({
        'status': 'healthy',
        'service': 'python-gateway',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/ping', methods=['POST'])
def ping():
    """
    Gateway ping endpoint
    Nhận request từ user, forward sang Go service, trả kết quả
    
    Flow:
    User → Python (này) → Go Service → Python → User
    """
    try:
        # Log request
        logger.info("Received ping request from user")
        
        # Gọi sang Go service
        logger.info(f"Forwarding ping to Go service: {GO_SERVICE_URL}/ping")
        response = requests.post(
            f"{GO_SERVICE_URL}/ping",
            timeout=5  # Timeout 5 giây
        )
        
        # Kiểm tra response từ Go
        response.raise_for_status()  # Raise exception nếu status code >= 400
        
        # Lấy dữ liệu JSON từ Go
        go_data = response.json()
        
        # Log thành công
        logger.info(f"Ping successful. Go response: {go_data}")
        
        # Trả về cho user (có thể thêm thông tin khác)
        return jsonify({
            'status': 'success',
            'message': 'Ping forwarded successfully',
            'go_response': go_data,
            'gateway_timestamp': datetime.now().isoformat()
        }), 200
        
    except requests.exceptions.ConnectionError:
        # Lỗi: Không kết nối được Go service
        logger.error("Cannot connect to Go service")
        return jsonify({
            'status': 'error',
            'message': 'Go service is not available',
            'error': 'Connection refused'
        }), 503  # Service Unavailable
        
    except requests.exceptions.Timeout:
        # Lỗi: Go service timeout
        logger.error("Go service timeout")
        return jsonify({
            'status': 'error',
            'message': 'Go service timeout',
            'error': 'Request timeout after 5s'
        }), 504  # Gateway Timeout
        
    except requests.exceptions.RequestException as e:
        # Lỗi khác
        logger.error(f"Error calling Go service: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error calling Go service',
            'error': str(e)
        }), 500  # Internal Server Error


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Lấy thống kê từ Go service
    """
    try:
        logger.info("Fetching stats from Go service")
        
        # Gọi Go service
        response = requests.get(
            f"{GO_SERVICE_URL}/stats",
            timeout=5
        )
        response.raise_for_status()
        
        # Lấy stats
        stats_data = response.json()
        
        logger.info(f"Stats retrieved: {stats_data}")
        
        # Trả về stats (có thể format lại hoặc thêm thông tin)
        return jsonify({
            'status': 'success',
            'data': stats_data,
            'retrieved_at': datetime.now().isoformat()
        }), 200
        
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Go service for stats")
        return jsonify({
            'status': 'error',
            'message': 'Go service is not available'
        }), 503
        
    except requests.exceptions.Timeout:
        logger.error("Go service timeout when getting stats")
        return jsonify({
            'status': 'error',
            'message': 'Timeout getting stats'
        }), 504
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error getting stats',
            'error': str(e)
        }), 500


@app.route('/api/test-connectivity', methods=['GET'])
def test_connectivity():
    """
    Endpoint để test kết nối Python ↔ Go
    """
    try:
        # Thử gọi health check của Go
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


# ==================== MAIN ====================

if __name__ == '__main__':
    # Chạy Flask development server
    logger.info("Starting Python Gateway Service on port 8080")
    app.run(
        host='0.0.0.0',  # Lắng nghe trên tất cả network interfaces
        port=8080,
        debug=True       # Bật debug mode (tự động reload khi code thay đổi)
    )
```

### 3.4. Giải thích chi tiết code Python

**Import và khởi tạo:**

```python
from flask import Flask, jsonify, request
```

- **Flask**: Class chính của Flask framework
- **jsonify**: Hàm chuyển dict Python → JSON response
- **request**: Object chứa thông tin HTTP request

```python
app = Flask(__name__)
```
```

- Khởi tạo Flask application
- `__name__`: Tên module hiện tại

```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

- Cho phép CORS cho tất cả routes bắt đầu `/api/`
- `origins: "*"`: Cho phép mọi domain (chỉ dùng dev)

```python
logging.basicConfig(...)
```

- Cấu hình logging để dễ debug
- `level=INFO`: Log các message từ INFO trở lên
- `format`: Định dạng log message

**Route decorator:**

```python
@app.route('/api/ping', methods=['POST'])
def ping():
    ...
```

- `@app.route()`: Decorator đăng ký route
- `/api/ping`: Endpoint path
- `methods=['POST']`: Chỉ chấp nhận POST request
- `ping()`: Handler function

**Gọi HTTP request sang Go:**

```python
response = requests.post(
    f"{GO_SERVICE_URL}/ping",
    timeout=5
)
```

- `requests.post()`: Gửi POST request
- `f"{GO_SERVICE_URL}/ping"`: F-string, format URL
- `timeout=5`: Timeout sau 5 giây

```python
response.raise_for_status()
```

- Tự động raise exception nếu status code >= 400
- Ví dụ: 404, 500 → raise HTTPError

```python
go_data = response.json()
```

- Parse JSON response từ Go
- Tự động convert → Python dict

**Error handling:**

```python
except requests.exceptions.ConnectionError:
    ...
```

- Bắt lỗi kết nối (Go service không chạy)

```python
except requests.exceptions.Timeout:
    ...
```

- Bắt lỗi timeout (Go service phản hồi quá lâu)

```python
except requests.exceptions.RequestException as e:
    ...
```

- Bắt tất cả lỗi requests khác

**Response:**

```python
return jsonify({...}), 200
```

- Trả về JSON response với HTTP status code 200

### 3.5. Chạy Python Service

```bash
# Đảm bảo đang trong thư mục python-service/ và venv đã activate
python app.py
```

**Output mong đợi:**
```
2026-01-25 15:40:00 - INFO - Starting Python Gateway Service on port 8080
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://192.168.1.100:8080
Press CTRL+C to quit
```

### 3.6. Test Python Service

Mở terminal mới (giữ 2 terminal cũ: Go + Python):

```bash
# Test 1: Health check Python
curl http://localhost:8080/health
```

Kết quả:

```json
  "service": "python-gateway",
  "status": "healthy",
  "timestamp": "2026-01-25T15:41:00"
}
```

```bash
# Test 2: Test connectivity Python → Go
curl http://localhost:8080/api/test-connectivity
```

Kết quả:

```json
  "go_health": {
    "service": "go-ping-service",
    "status": "healthy",
    "time": "2026-01-25T15:42:00+07:00"
  },
  "message": "Python can reach Go service",
  "status": "connected"
}
```

```bash
# Test 3: Ping qua Python Gateway
curl -X POST http://localhost:8080/api/ping
```

Kết quả:

```json
  "gateway_timestamp": "2026-01-25T15:43:00",
  "go_response": {
    "message": "Pong",
    "success_count": 5,
    "timestamp": "2026-01-25T15:43:00+07:00"
  },
  "message": "Ping forwarded successfully",
  "status": "success"
}
```

```bash
# Test 4: Lấy stats qua Python
curl http://localhost:8080/api/stats
```

Kết quả:

```json
  "data": {
    "failed_count": 0,
    "last_ping_time": "2026-01-25T15:43:00+07:00",
    "success_count": 5
  },
  "retrieved_at": "2026-01-25T15:44:00",
  "status": "success"
}
```

### 3.7. Xử lý lỗi Python Service

#### **Lỗi 1: ModuleNotFoundError**
```
ModuleNotFoundError: No module named 'flask'
```

Giải pháp:

```bash
# Kiểm tra venv đã activate chưa
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Cài lại dependencies
pip install -r requirements.txt
```

#### **Lỗi 2: Port 8080 đã bị chiếm**
```
OSError: [Errno 48] Address already in use
```

Giải pháp:

```python
# Đổi port trong app.py:
app.run(host='0.0.0.0', port=8082, debug=True)
```

#### **Lỗi 3: Go service is not available**

```json
  "status": "error",
  "message": "Go service is not available"
}
```

**Nguyên nhân:** Go service chưa chạy hoặc sai URL

**Giải pháp:**

```bash
# Kiểm tra Go service có chạy không:
curl http://localhost:8081/health

# Nếu không, chạy lại Go service:
cd go-service
go run main.go
```

#### **Lỗi 4: CORS error từ browser**
```
Access-Control-Allow-Origin missing
Giải pháp: Đã được xử lý sẵn bằng Flask-CORS

🧪 PHẦN 4: TEST LUỒNG HOÀN CHỈNH
4.1. Kiểm tra 2 services đang chạy
bash# Terminal 1: Go service
cd go-service
go run main.go

# Terminal 2: Python service
cd python-service
source venv/bin/activate  # hoặc venv\Scripts\activate trên Windows
python app.py
```

### 4.2. Test flow: User → Python → Go → Python → User

```bash
# Ping trực tiếp Go (bypass Python)
curl -X POST http://localhost:8081/ping

# Ping qua Python Gateway
curl -X POST http://localhost:8080/api/ping

# So sánh 2 kết quả
```

**Quan sát:**

- Cả 2 đều tăng `success_count`
- Response từ Python có thêm `gateway_timestamp`

### 4.3. Test với Postman

**Collection:** TODO App Ping-Pong

**Request 1: Direct Go Ping**

- Method: POST
- URL: `http://localhost:8081/ping`
- Save & Send

**Request 2: Gateway Ping**

- Method: POST
- URL: `http://localhost:8080/api/ping`
- Save & Send

**Request 3: Gateway Stats**

- Method: GET
- URL: `http://localhost:8080/api/stats`
- Save & Send

### 4.4. Test scenario nâng cao

**Scenario 1: Tắt Go service, gọi Python**

```bash
# Tắt Go service (Ctrl+C trong terminal Go)

# Gọi Python
curl -X POST http://localhost:8080/api/ping
```

Kết quả mong đợi:

```json
  "status": "error",
  "message": "Go service is not available",
  "error": "Connection refused"
}
```

**Scenario 2: Restart Go service → dữ liệu mất**

```bash
# Lấy stats hiện tại
curl http://localhost:8080/api/stats
# success_count: 10

# Restart Go service (Ctrl+C rồi go run main.go lại)

# Lấy stats lại
curl http://localhost:8080/api/stats
# success_count: 0  ← DỮ LIỆU MẤT!
**Giải thích:** Dữ liệu lưu trong RAM → restart thì mất → Cần Volume (Giai đoạn 6)

📊 PHẦN 5: GIẢI THÍCH LUỒNG DỮ LIỆU
5.1. Sequence Diagram
User          Python Gateway         Go Service
 |                  |                      |
 |--- POST /api/ping --->                  |
 |                  |                      |
 |                  |--- POST /ping ------>|
 |                  |                      |
 |                  |                      |-- stats.SuccessCount++
 |                  |                      |
 |                  |<--- 200 + JSON ------|
 |                  |                      |
 |<-- 200 + JSON ---|                      |
 |                  |                      |
```

### 5.2. Phân tích từng bước

**Bước 1: User gửi POST request đến Python**

```
POST http://localhost:8080/api/ping
```

**Bước 2: Python nhận request, log**

```python
logger.info("Received ping request from user")
```

**Bước 3: Python forward sang Go**

```python
response = requests.post(f"{GO_SERVICE_URL}/ping", timeout=5)
```

**Bước 4: Go nhận request, xử lý**

```go
mutex.Lock()
stats.SuccessCount++
stats.LastPingTime = time.Now()
mutex.Unlock()
```

**Bước 5: Go trả response về Python**

```go
c.JSON(http.StatusOK, gin.H{"message": "Pong", ...})
```

**Bước 6: Python nhận response, parse JSON**

```python
go_data = response.json()
```

**Bước 7: Python trả về User**

```python
return jsonify({'go_response': go_data, ...}), 200
```

---

## 🎯 PHẦN 6: BÀI TẬP THỰC HÀNH

### Bài 1: Thêm Failed Count

**Yêu cầu:** Thêm tính năng đếm số lần ping thất bại

**Gợi ý:**

- Trong Go service, thêm logic kiểm tra (ví dụ: random fail 20%)
- Nếu fail, tăng `stats.FailedCount`, trả HTTP 500
- Python xử lý error, vẫn trả response cho user

**Code Go cần thêm:**

```go
import "math/rand"

func handlePing(c *gin.Context) {
    mutex.Lock()
    defer mutex.Unlock()
    
    // Random fail 20%
    if rand.Float32() < 0.2 {
        stats.FailedCount++
        c.JSON(http.StatusInternalServerError, gin.H{
            "message": "Ping failed",
            "failed_count": stats.FailedCount,
        })
        return
    }
    
    // Success
    stats.SuccessCount++
    stats.LastPingTime = time.Now()
    c.JSON(http.StatusOK, gin.H{
        "message": "Pong",
        "success_count": stats.SuccessCount,
    })
}
```

### Bài 2: Thêm Endpoint Reset

**Yêu cầu:** Thêm API để reset stats về 0

**Endpoint mới:**

- `POST /api/reset` (Python)
- `POST /reset` (Go)

**Code Go:**

```go
func resetStats(c *gin.Context) {
    mutex.Lock()
    defer mutex.Unlock()
    
    stats = Stats{} // Reset về zero value
    
    c.JSON(http.StatusOK, gin.H{
        "message": "Stats reset successfully",
    })
}

// Thêm vào main():
router.POST("/reset", resetStats)
```

**Code Python:**

```python
@app.route('/api/reset', methods=['POST'])
def reset_stats():
    try:
        response = requests.post(f"{GO_SERVICE_URL}/reset", timeout=5)
        response.raise_for_status()
        return jsonify({
            'status': 'success',
            'message': 'Stats reset successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500
```

### Bài 3: Thêm Request ID Tracing

**Yêu cầu:** Mỗi request có ID duy nhất để trace qua 2 services

**Gợi ý:**

- Python tạo UUID, gửi qua header sang Go
- Go log UUID, trả lại trong response
- Python log UUID khi nhận response

**Code Python:**

```python
import uuid

@app.route('/api/ping', methods=['POST'])
def ping():
    request_id = str(uuid.uuid4())
    logger.info(f"[{request_id}] Received ping request")
    
    response = requests.post(
        f"{GO_SERVICE_URL}/ping",
        headers={'X-Request-ID': request_id},
        timeout=5
    )
    
    logger.info(f"[{request_id}] Go responded")
    ...
```

---

## ✅ PHẦN 7: CHECKLIST HOÀN THÀNH GIAI ĐOẠN 2

- ☐ Go service chạy được trên port 8081
- ☐ Python service chạy được trên port 8080
- ☐ Health check của cả 2 services hoạt động
- ☐ Test connectivity Python ↔ Go thành công
- ☐ Ping qua Python gateway hoạt động
- ☐ Stats được cập nhật chính xác
- ☐ Hiểu được mutex và thread-safety
- ☐ Hiểu được cách gọi HTTP giữa các services
- ☐ Biết xử lý errors và logging
- ☐ Nhận ra vấn đề dữ liệu mất khi restart
- ☐ Làm được ít nhất 1 bài tập thực hành

---

## 🐛 PHẦN 8: TROUBLESHOOTING TỔNG HỢP

### Vấn đề 1: Connection Refused

**Triệu chứng:**

```json
  "error": "Connection refused",
  "message": "Go service is not available"
}
```

**Checklist:**

- ☐ Go service có đang chạy không? (`curl http://localhost:8081/health`)
- ☐ Port có đúng không? (8081 cho Go, 8080 cho Python)
- ☐ Firewall có chặn không?
- ☐ URL trong Python có đúng không? (`GO_SERVICE_URL`)

### Vấn đề 2: Dữ liệu không cập nhật

**Triệu chứng:** Ping nhiều lần nhưng `success_count` vẫn là 1

**Nguyên nhân:** Có thể gọi nhầm endpoint hoặc nhiều instance Go chạy

**Kiểm tra:**

```bash
# Kiểm tra có bao nhiêu process Go đang chạy
# Windows
tasklist | findstr go

# Linux/Mac
ps aux | grep "go run"
```

### Vấn đề 3: Import Error Python

**Triệu chứng:**
```
ImportError: cannot import name 'Flask' from 'flask'
```

Giải pháp:

```bash
# Xóa venv cũ
rm -rf venv

# Tạo lại
python -m venv venv
source venv/bin/activate  # hoặc venv\Scripts\activate

# Cài lại
pip install -r requirements.txt
```

---

## 📚 PHẦN 9: TÀI LIỆU THAM KHẢO

**Go:**

- Gin Framework: https://gin-gonic.com/docs/
- Go Concurrency (Mutex): https://go.dev/tour/concurrency/9
- HTTP Server: https://pkg.go.dev/net/http

**Python:**

- Flask Quickstart: https://flask.palletsprojects.com/quickstart/
- Requests Library: https://requests.readthedocs.io/
- Python Logging: https://docs.python.org/3/library/logging.html

**HTTP & APIs:**

- HTTP Methods: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
- HTTP Status Codes: https://httpstatuses.com/

---

## 🎊 KẾT LUẬN GIAI ĐOẠN 2

Chúc mừng! Bạn đã hoàn thành Giai đoạn 2. Bây giờ bạn đã:

✅ Xây dựng được 2 microservices hoàn chỉnh  
✅ Hiểu cách các services giao tiếp qua HTTP  
✅ Nắm vững cách xử lý request/response  
✅ Biết logging và error handling  
✅ Nhận ra vấn đề lưu trữ dữ liệu trong RAM
Vấn đề cần giải quyết tiếp:

❌ Dữ liệu mất khi restart
❌ Chưa có TODO functionality (chỉ có Ping-Pong)
❌ Chưa có giao diện web
❌ Chưa có database