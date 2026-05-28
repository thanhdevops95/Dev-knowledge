# TODO APP - LỘ TRÌNH DEVSECOPS TỪ CƠ BẢN ĐẾN CHUYÊN GIA

## 📋 MỤC LỤC

- [Tổng quan dự án](#tổng-quan-dự-án)
- [Lộ trình chi tiết](#lộ-trình-chi-tiết)
  - [Giai đoạn 1: Setup môi trường & Kiến thức nền tảng](#giai-đoạn-1-setup-môi-trường--kiến-thức-nền-tảng)
  - [Giai đoạn 2: Xây dựng App cơ bản - Bare Metal (Ping-Pong)](#giai-đoạn-2-xây-dựng-app-cơ-bản---bare-metal-ping-pong)
  - [Giai đoạn 3: Thêm chức năng TODO (vẫn lưu RAM)](#giai-đoạn-3-thêm-chức-năng-todo-vẫn-lưu-ram)
  - [Giai đoạn 4: Thêm NGINX - Web Interface](#giai-đoạn-4-thêm-nginx---web-interface)
  - [Giai đoạn 5: Docker - Containerization](#giai-đoạn-5-docker---containerization)
  - [Giai đoạn 6: Docker Volumes - Persistent Data](#giai-đoạn-6-docker-volumes---persistent-data)
  - [Giai đoạn 7: Docker Compose - Orchestration](#giai-đoạn-7-docker-compose---orchestration)
  - [Giai đoạn 8: Database - PostgreSQL](#giai-đoạn-8-database---postgresql)
  - [Giai đoạn 9: GitLab CI - Continuous Integration](#giai-đoạn-9-gitlab-ci---continuous-integration)
  - [Giai đoạn 10: GitLab CD - Continuous Deployment](#giai-đoạn-10-gitlab-cd---continuous-deployment)
  - [Giai đoạn 11: AWS Deployment & Scaling](#giai-đoạn-11-aws-deployment--scaling)
  - [Giai đoạn 12: Monitoring & Security (DevSecOps)](#giai-đoạn-12-monitoring--security-devsecops)

---

## 📖 TỔNG QUAN DỰ ÁN

### Mục tiêu

Xây dựng hệ thống TODO App hoàn chỉnh theo lộ trình thực chiến từ đơn giản nhất (curl) đến phức tạp (Production-ready DevSecOps), giúp học viên nắm vững toàn bộ quy trình phát triển, triển khai và vận hành một ứng dụng thực tế.

### Kiến trúc cơ bản

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
┌──────▼──────┐
│   NGINX     │ (Web Server + Reverse Proxy)
└──────┬──────┘
       │
┌──────▼──────────┐
│  Python (Flask) │ (Gateway/API)
└──────┬──────────┘
       │
┌──────▼──────┐
│  Go Service │ (Backend Logic)
└──────┬──────┘
       │
┌──────▼──────┐
│ PostgreSQL  │ (Database)
└─────────────┘
```

**Components:**

- **App 1 (Python - Flask)**: Gateway/API chính để người dùng tương tác
- **App 2 (Go)**: Backend xử lý logic TODO + đếm Ping/Pong
- **NGINX**: Web server & Reverse Proxy (giai đoạn sau)
- **PostgreSQL**: Database (giai đoạn sau)
- **Redis**: Cache (giai đoạn nâng cao)

---

## 🗺️ LỘ TRÌNH

### GIAI ĐOẠN 1: Setup môi trường & Kiến thức nền tảng

**Mục tiêu:** Chuẩn bị môi trường làm việc và hiểu các khái niệm cơ bản

**Nội dung:**

- ✅ Cài đặt Python 3.x, Go, Git, curl, Postman
- ✅ Kiểm tra version và test tools
- ✅ Giới thiệu HTTP Protocol, REST API, JSON
- ✅ Giới thiệu Microservices Architecture cơ bản

**Lỗi thường gặp:**

- ❌ Python/Go chưa thêm vào PATH
- ❌ Port bị chiếm (8080, 8081)
- ❌ Firewall chặn kết nối localhost

**Output:**

- ✅ Môi trường sẵn sàng
- ✅ Hiểu được cách 2 service giao tiếp qua HTTP

**[➡️ Xem chi tiết Giai đoạn 1](#giai-doan-1)**

---

### GIAI ĐOẠN 2: Xây dựng App cơ bản - Bare Metal (Ping-Pong)

**Mục tiêu:** Xây dựng 2 app đơn giản giao tiếp với nhau qua HTTP, dữ liệu lưu RAM

#### 2.1. App Go (Backend) - Ping Counter Service

**Chức năng:**

- API `/ping`: Nhận ping, đếm số lần thành công, trả về "Pong"
- API `/stats`: Trả về thống kê `{success: X, failed: Y}`
- Lưu trữ: Biến toàn cục trong RAM

**Test:**

```bash
curl http://localhost:8081/ping
curl http://localhost:8081/stats
```

#### 2.2. App Python (Gateway)

**Chức năng:**

- API `/api/ping`: Nhận request từ user, forward sang Go, trả kết quả
- API `/api/stats`: Lấy stats từ Go, trả về user

**Test:**

```bash
curl http://localhost:8080/api/ping
curl http://localhost:8080/api/stats
```

**Lỗi thường gặp:**

- ❌ Connection refused (app chưa chạy hoặc sai port)
- ❌ Import error (thiếu thư viện Flask/requests)
- ❌ CORS issues (giai đoạn sau khi thêm frontend)

**Output:**

- ✅ 2 app chạy được độc lập
- ✅ User → Python → Go → Python → User (luồng hoàn chỉnh)

**[➡️ Xem chi tiết Giai đoạn 2](#giai-doan-2)**

---

### GIAI ĐOẠN 3: Thêm chức năng TODO (vẫn lưu RAM)

**Mục tiêu:** Mở rộng từ Ping-Pong sang TODO App hoàn chỉnh

#### 3.1. Go Service - TODO Backend

**API mới:**

- `POST /todos`: Tạo TODO mới
- `GET /todos`: Lấy danh sách TODO
- `PUT /todos/:id`: Cập nhật TODO
- `DELETE /todos/:id`: Xóa TODO
- `GET /todos/:id`: Lấy chi tiết 1 TODO

**Cấu trúc dữ liệu (RAM):**

```go
type Todo struct {
    ID        string    `json:"id"`
    Title     string    `json:"title"`
    Completed bool      `json:"completed"`
    CreatedAt time.Time `json:"created_at"`
}
var todos = make(map[string]Todo) // Lưu trong RAM
```

#### 3.2. Python Gateway - TODO API

**API tương ứng:**

- `POST /api/todos`
- `GET /api/todos`
- `PUT /api/todos/:id`
- `DELETE /api/todos/:id`
- `GET /api/todos/:id`

**Test với curl:**

```bash
# Tạo TODO
curl -X POST http://localhost:8080/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Học Docker"}'

# Lấy danh sách
curl http://localhost:8080/api/todos
```

**Lỗi thường gặp:**

- ❌ JSON parsing error
- ❌ ID trùng lặp
- ❌ Dữ liệu mất khi restart app (đây là lý do cần Volume)

**[➡️ Xem chi tiết Giai đoạn 3](#giai-doan-3)**

---

### GIAI ĐOẠN 4: Thêm NGINX - Web Interface

**Mục tiêu:** Thêm giao diện web để người dùng thao tác trực quan

#### 4.1. Xây dựng Frontend (HTML/CSS/JS)

**Chức năng:**

- Form thêm TODO
- Danh sách TODO với checkbox (completed)
- Nút xóa, sửa
- Hiển thị stats (ping count)

**Cấu trúc file:**

```
frontend/
├── index.html
├── style.css
└── app.js
```

#### 4.2. Cài đặt & Cấu hình NGINX

**Vai trò:**

- Phục vụ static files (HTML/CSS/JS)
- Reverse proxy đến Python API

**Test:**

- Truy cập `http://localhost` → Hiển thị giao diện TODO
- Thêm/Xóa TODO qua giao diện

**Lỗi thường gặp:**

- ❌ NGINX không start (port 80 bị chiếm)
- ❌ CORS issues (cần config headers)
- ❌ 502 Bad Gateway (Python app chưa chạy)

**[➡️ Xem chi tiết Giai đoạn 4](#giai-doan-4)**

---

### GIAI ĐOẠN 5: Docker - Containerization

**Mục tiêu:** Đóng gói ứng dụng vào Docker containers

#### 5.1. Dockerfile cho Go Service

**Nội dung:**

- Multi-stage build
- Optimize image size
- Health check

#### 5.2. Dockerfile cho Python Service

#### 5.3. Dockerfile cho NGINX

#### 5.4. Docker Network

**Tạo network:**

```bash
docker network create todo-network
```

**Chạy containers:**

```bash
docker run -d --name go-service --network todo-network go-todo:latest
docker run -d --name py-service --network todo-network py-todo:latest
docker run -d --name nginx --network todo-network -p 80:80 nginx-todo:latest
```

**Lỗi thường gặp:**

- ❌ Build failed (thiếu dependencies)
- ❌ Container exit ngay lập tức (lỗi code)
- ❌ Network isolation (containers không thấy nhau)
- ❌ Port mapping sai

---

### GIAI ĐOẠN 6: Docker Volumes - Persistent Data

**Mục tiêu:** Giải quyết vấn đề mất dữ liệu khi restart container

#### 6.1. Lưu dữ liệu vào File (Go)

**Thay đổi:**

- Lưu TODO vào file JSON thay vì RAM
- Đọc file khi khởi động
- Ghi file mỗi khi có thay đổi

#### 6.2. Mount Volume

```bash
docker run -d \
  --name go-service \
  --network todo-network \
  -v todo-data:/app/data \
  go-todo:latest
```

#### 6.3. Docker Volume Commands

```bash
docker volume ls
docker volume inspect todo-data
```

**Lỗi thường gặp:**

- ❌ Permission denied (volume mount)
- ❌ File corruption (đồng thời ghi)
- ❌ Volume không persist (sai cấu hình)

---

### GIAI ĐOẠN 7: Docker Compose - Orchestration

**Mục tiêu:** Quản lý nhiều containers dễ dàng

#### 7.1. File docker-compose.yml

**Nội dung:**

- Định nghĩa 3 services (go, python, nginx)
- Network tự động
- Volume mapping
- Environment variables
- Depends_on, health checks

#### 7.2. Sử dụng Docker Compose

```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
docker-compose ps
```

**Lỗi thường gặp:**

- ❌ YAML syntax error
- ❌ Service dependency issues
- ❌ Port conflicts

---

### GIAI ĐOẠN 8: Database - PostgreSQL

**Mục tiêu:** Thay thế file storage bằng database thực tế

#### 8.1. Thêm PostgreSQL vào Docker Compose

#### 8.2. Cập nhật Go Service - Database Integration

**Thay đổi:**

- Kết nối PostgreSQL
- Migration script tạo table
- CRUD operations với database

#### 8.3. Connection Pooling & Error Handling

**Lỗi thường gặp:**

- ❌ Connection refused (DB chưa ready)
- ❌ SQL injection (cần dùng prepared statements)
- ❌ Migration failed

---

### GIAI ĐOẠN 9: GitLab CI - Continuous Integration

**Mục tiêu:** Tự động hóa build, test, scan

#### 9.1. Setup GitLab Repository

**Bước:**

- Tạo repo trên GitLab
- Push code lên
- Cấu trúc thư mục

#### 9.2. File .gitlab-ci.yml - Build Stage

**Nội dung:**

- Build Docker images
- Run unit tests
- Security scan (Trivy/Grype)
- Push images lên registry

#### 9.3. GitLab Runner Setup

**Lỗi thường gặp:**

- ❌ Runner không connect
- ❌ Build timeout
- ❌ Registry authentication failed

---

### GIAI ĐOẠN 10: GitLab CD - Continuous Deployment

**Mục tiêu:** Tự động deploy lên server

#### 10.1. Setup Deploy Server (AWS EC2)

**Bước:**

- Tạo EC2 instance
- Cài Docker, Docker Compose
- Setup SSH keys

#### 10.2. File .gitlab-ci.yml - Deploy Stage

**Nội dung:**

- SSH vào server
- Pull images mới
- Rolling update (zero-downtime)

#### 10.3. Environment Variables & Secrets

**Lỗi thường gặp:**

- ❌ SSH permission denied
- ❌ Environment mismatch
- ❌ Deployment rollback failed

---

### GIAI ĐOẠN 11: AWS Deployment & Scaling

**Mục tiêu:** Triển khai production trên AWS với khả năng scale

#### 11.1. Kiến trúc AWS

**Components:**

- ECS/EKS cho containers
- RDS PostgreSQL
- ElastiCache Redis
- Application Load Balancer
- Auto Scaling Group
- CloudWatch

#### 11.2. Terraform Infrastructure as Code

#### 11.3. Kubernetes Deployment (Nâng cao)

**Lỗi thường gặp:**

- ❌ IAM permission issues
- ❌ Security group misconfiguration
- ❌ Resource limits exceeded

---

### GIAI ĐOẠN 12: Monitoring & Security (DevSecOps)

**Mục tiêu:** Giám sát, bảo mật toàn diện

#### 12.1. Monitoring Stack

**Tools:**

- Prometheus (metrics)
- Grafana (visualization)
- ELK Stack (logs)
- Jaeger (tracing)

#### 12.2. Security Hardening

**Checklist:**

- ✅ HTTPS/TLS certificates
- ✅ Secrets management (Vault)
- ✅ Network policies
- ✅ RBAC
- ✅ OWASP Top 10 fixes
- ✅ Dependency scanning
- ✅ Runtime security (Falco)

#### 12.3. Performance Optimization

**Nội dung:**

- Caching strategy (Redis)
- Database indexing
- Connection pooling
- Horizontal scaling
- Load testing (k6)

**Lỗi thường gặp:**

- ❌ Certificate expiration
- ❌ Memory leaks
- ❌ Database connection exhaustion
- ❌ DDoS attacks

---

## 📝 CHI TIẾT CÁC GIAI ĐOẠN

<a id="giai-doan-1"></a>

# GIAI ĐOẠN 1: SETUP MÔI TRƯỜNG & KIẾN THỨC NỀN TẢNG

## 📌 MỤC TIÊU GIAI ĐOẠN 1

Sau khi hoàn thành giai đoạn này, bạn sẽ:

- ✅ Cài đặt đầy đủ các công cụ cần thiết
- ✅ Hiểu được kiến trúc Microservices cơ bản
- ✅ Nắm rõ cách HTTP hoạt động
- ✅ Biết cách test API với curl và Postman
- ✅ Sẵn sàng cho các giai đoạn tiếp theo

---

## 🛠️ PHẦN 1: CÀI ĐẶT CÔNG CỤ
### 1.1. Cài đặt Python 3.x
#### **Windows:**
**Bước 1:** Tải Python từ trang chủ

- Truy cập: https://www.python.org/downloads/
- Tải phiên bản Python 3.11 hoặc mới hơn

**Bước 2:** Chạy file cài đặt

- ✅ QUAN TRỌNG: Tích chọn "Add Python to PATH"
- Click "Install Now"
- Đợi quá trình cài đặt hoàn tất

**Bước 3:** Kiểm tra cài đặt

```bash
# Mở Command Prompt (Win + R, gõ cmd, Enter)
python --version
# Kết quả mong đợi: Python 3.11.x

pip --version
# Kết quả mong đợi: pip 23.x.x
```

**Xử lý lỗi thường gặp:**

❌ **Lỗi**: `'python' is not recognized as an internal or external command`

✅ **Giải pháp**:

1. Cài lại Python, nhớ tích "Add Python to PATH"
2. Hoặc thêm Python vào PATH thủ công:
    - Nhấn Win + Pause → Advanced system settings
    - Environment Variables → System variables → Path → Edit
    - Thêm: C:\Users\[TênMáy]\AppData\Local\Programs\Python\Python311
    - Thêm: C:\Users\[TênMáy]\AppData\Local\Programs\Python\Python311\Scripts
3. Khởi động lại Command Prompt

#### **macOS:**
**Bước 1:** Cài đặt Homebrew (nếu chưa có)

```bash
# Mở Terminal (Cmd + Space, gõ Terminal)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
**Bước 2:** Cài Python qua Homebrew

```bash
brew install python@3.11
```
**Bước 3:** Kiểm tra

```bash
python3 --version
pip3 --version
```

#### **Linux (Ubuntu/Debian):**
```bash
# Cập nhật package list
sudo apt update

# Cài Python và pip
sudo apt install python3 python3-pip -y

# Kiểm tra
python3 --version
pip3 --version
```

---

### 1.2. Cài đặt Go (Golang)

#### **Windows:**

**Bước 1:** Tải Go

- Truy cập: https://go.dev/dl/
- Tải file: go1.21.x.windows-amd64.msi

**Bước 2:** Cài đặt

- Chạy file .msi
- Giữ nguyên đường dẫn mặc định: C:\Program Files\Go
- Click "Next" → "Install"

**Bước 3:** Kiểm tra

```bash
# Mở Command Prompt MỚI
go version
# Kết quả mong đợi: go version go1.21.x windows/amd64
```
**Bước 4:** Setup GOPATH (quan trọng)

```bash
# Tạo thư mục workspace
mkdir %USERPROFILE%\go
mkdir %USERPROFILE%\go\src
mkdir %USERPROFILE%\go\bin

# Thêm vào Environment Variables:
# GOPATH = C:\Users\[TênMáy]\go
# Path thêm: %GOPATH%\bin
```

#### **macOS:**
```bash
# Cài qua Homebrew
brew install go

# Kiểm tra
go version

# Setup GOPATH (thêm vào ~/.zshrc hoặc ~/.bash_profile)
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
```
#### **Linux:**
```bash
# Tải Go
wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz

# Giải nén vào /usr/local
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz

# Thêm vào ~/.bashrc hoặc ~/.profile
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
echo 'export GOPATH=$HOME/go' >> ~/.bashrc
source ~/.bashrc

# Kiểm tra
go version
```

---

### 1.3. Cài đặt Git

#### **Windows:**
- Tải từ: https://git-scm.com/download/win
- Chạy file cài đặt, giữ nguyên các tùy chọn mặc định

```bash
# Kiểm tra:
bashgit --version
```
#### **macOS:**

```bash
# Cài qua Homebrew
brew install git
# Kiểm tra:
git --version
```
#### **Linux:**

```bash
# Cài qua Apt
sudo apt install git -y
# Kiểm tra:
git --version
```

**Cấu hình Git lần đầu:**

```bash
bashgit config --global user.name "Tên của bạn"
git config --global user.email "email@example.com"

# Kiểm tra
git config --list
```

### 1.4. Cài đặt curl
#### **Windows:**
curl đã được tích hợp sẵn từ Windows 10 build 1803.
```bash
# Kiểm tra
bashcurl --version
```

Nếu chưa có:
- Tải từ: https://curl.se/windows/
- Giải nén và thêm vào PATH

#### **macOS/Linux:**
curl thường có sẵn.

```bash
# Kiểm tra
curl --version
```
Nếu chưa có (Linux):
```bash
sudo apt install curl -y
```

---

### 1.5. Cài đặt Postman

#### **Tất cả hệ điều hành:**
1. Truy cập: https://www.postman.com/downloads/
2. Tải phiên bản phù hợp với hệ điều hành
3. Cài đặt và đăng ký tài khoản miễn phí (hoặc dùng không cần đăng nhập)

**Giải pháp thay thế nhẹ hơn:**
- **Insomnia**: https://insomnia.rest/download
- **Thunder Client** (VS Code Extension)
- Hoặc chỉ dùng curl (đủ cho khóa học này)

---

### 1.6. Cài đặt Code Editor

**Khuyến nghị: Visual Studio Code**

Tải từ: https://code.visualstudio.com/

**Extensions nên cài:**
- Python (Microsoft)
- Go (Go Team at Google)
- Docker (Microsoft)
- GitLens
- REST Client (để test API trong VS Code)

---

## 📚 PHẦN 2: KIẾN THỨC NỀN TẢNG

### 2.1. HTTP Protocol - Giao thức nền tảng của Web

#### **HTTP là gì?**

HTTP (HyperText Transfer Protocol) là giao thức truyền tải dữ liệu trên Internet. Mọi lần bạn:
- Mở website
- Gửi form
- Tải file
- Sử dụng app mobile

→ Đều sử dụng HTTP hoặc HTTPS (bản bảo mật của HTTP)

#### **Cấu trúc HTTP Request (Yêu cầu):**
```bash
GET /api/todos HTTP/1.1             ← REQUEST LINE (Phương thức + Đường dẫn + Phiên bản)
Host: localhost:8080                ← HEADERS (Thông tin bổ sung)
Content-Type: application/json
Authorization: Bearer abc123

{"title": "Học Docker"}             ← BODY (Dữ liệu gửi đi, không phải lúc nào cũng có)
```

**Giải thích từng phần:**

1. **REQUEST LINE:**
   - `GET`: Phương thức HTTP (xem bên dưới)
   - `/api/todos`: Đường dẫn resource (tài nguyên)
   - `HTTP/1.1`: Phiên bản giao thức

2. **HEADERS:**
   - `Host`: Server đích
   - `Content-Type`: Loại dữ liệu gửi đi (JSON, XML, Form...)
   - `Authorization`: Token xác thực (nếu cần)

3. **BODY:**
   - Dữ liệu thực tế (với POST, PUT, PATCH)
   - GET và DELETE thường không có body

#### **HTTP Response (Phản hồi):**
```bash
HTTP/1.1 200 OK                     ← STATUS LINE (Phiên bản + Mã trạng thái + Mô tả)
Content-Type: application/json
Content-Length: 156

{                                   ← BODY (Dữ liệu trả về)
  "id": "1",
  "title": "Học Docker",
  "completed": false
}
```

#### **Các phương thức HTTP quan trọng:**

| Phương thức | Mục đích | Ví dụ |
|-------------|----------|-------|
| **GET** | Lấy dữ liệu | Xem danh sách TODO |
| **POST** | Tạo mới | Thêm TODO mới |
| **PUT** | Cập nhật toàn bộ | Sửa TODO (cả title và completed) |
| **PATCH** | Cập nhật một phần | Chỉ đổi completed = true |
| **DELETE** | Xóa | Xóa TODO |

#### **Mã trạng thái HTTP (Status Codes):**

| Mã | Ý nghĩa | Ví dụ |
|----|---------|-------|
| **2xx** | **Thành công** | |
| 200 | OK | Lấy dữ liệu thành công |
| 201 | Created | Tạo TODO mới thành công |
| 204 | No Content | Xóa thành công, không trả về gì |
| **4xx** | **Lỗi từ Client** | |
| 400 | Bad Request | Gửi JSON sai format |
| 401 | Unauthorized | Thiếu token xác thực |
| 404 | Not Found | TODO ID không tồn tại |
| **5xx** | **Lỗi từ Server** | |
| 500 | Internal Server Error | Lỗi code backend |
| 503 | Service Unavailable | Server quá tải |

---

### 2.2. REST API - Chuẩn thiết kế API

#### **REST là gì?**

REST (Representational State Transfer) là một phong cách kiến trúc để thiết kế API. API theo chuẩn REST gọi là RESTful API.

#### **Nguyên tắc của REST:**

1. **Resource-based (Dựa trên tài nguyên):**
```
   /todos                               ← Tài nguyên là "todos" (danh từ số nhiều)
   /todos/123                           ← TODO cụ thể với ID = 123
```

2. **Sử dụng đúng HTTP Methods:**
```
   GET/todos                            → Lấy tất cả
   GET/todos/123                        → Lấy TODO ID 123
   POST   /todos                        → Tạo mới
   PUT/todos/123                        → Cập nhật toàn bộ TODO 123
   DELETE /todos/123                    → Xóa TODO 123

3. **Stateless (Không lưu trạng thái):**

- Mỗi request độc lập
- Server không nhớ request trước đó
- Mọi thông tin cần thiết phải gửi kèm trong request


4. **Trả về JSON:**

```json
{
 "id": "1",
 "title": "Học Docker",
 "completed": false,
 "created_at": "2026-01-25T10:30:00Z"
}
```

**Thiết kế RESTful API cho TODO App:**

| Hành động | Method | Endpoint | Body | Response |
|-----------|--------|----------|------|----------|
| Lấy tất cả TODO | GET | `/api/todos` | - | `[{...}, {...}]` |
| Lấy 1 TODO | GET | `/api/todos/:id` | - | `{id, title, ...}` |
| Tạo TODO | POST | `/api/todos` | `{title}` | `{id, title, ...}` |
| Cập nhật TODO | PUT | `/api/todos/:id` | `{title, completed}` | `{id, title, ...}` |
| Xóa TODO | DELETE | `/api/todos/:id` | - | `204 No Content` |

### 2.3. JSON - Định dạng dữ liệu
#### JSON là gì?
JSON (JavaScript Object Notation) là định dạng văn bản để trao đổi dữ liệu giữa client và server.
Cú pháp JSON:
```json
{
  "string": "Giá trị chuỗi",
  "number": 123,
  "float": 45.67,
  "boolean": true,
  "null_value": null,
  "array": [1, 2, 3, "a", "b"],
  "object": {
"nested_key": "nested_value"
  }
}
```

**Quy tắc:**

- Key phải trong dấu ngoặc kép "key"
- Giá trị string cũng dùng ngoặc kép
- Không có dấu phẩy sau phần tử cuối cùng
- Hỗ trợ: string, number, boolean, null, array, object

**Ví dụ TODO dạng JSON:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Học Docker từ cơ bản đến nâng cao",
  "completed": false,
  "created_at": "2026-01-25T14:30:00+07:00",
  "tags": ["docker", "devops", "container"]
}
```

---

### 2.4. Microservices Architecture - Kiến trúc vi dịch vụ

#### **Monolith vs Microservices:**

**Monolith (Nguyên khối):**
```
┌─────────────────────────────┐
│   TODO App (1 ứng dụng lớn)  │
│  │
│  - UI│
│  - Business Logic│
│  - Database Access   │
│  - Auth  │
└─────────────────────────────┘
```

**Ưu điểm:** Đơn giản, dễ phát triển ban đầu  
**Nhược điểm:** Khó scale, khó maintain khi lớn

**Microservices (Vi dịch vụ):**
```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Frontend│────▶│  TODO API│────▶│  Database│
│  Service │ │  Service │ │  Service │
└──────────────┘ └──────────────┘ └──────────────┘
│
▼
 ┌──────────────┐
 │  Auth│
 │  Service │
 └──────────────┘
```

**Ưu điểm:**
- Mỗi service độc lập, dễ scale từng phần
- Team khác nhau phát triển song song
- Dễ thay đổi công nghệ cho từng service

**Nhược điểm:**
- Phức tạp hơn
- Cần quản lý nhiều service
- Network latency

#### **Kiến trúc TODO App trong khóa học này:**
```
┌─────────────────┐
│   NGƯỜI DÙNG│
└────────┬────────┘
 │
┌────────▼────────┐
│   NGINX │  ← Web Server
│  (Port 80)  │
└────────┬────────┘
 │
┌────────▼────────┐
│  Python Gateway │  ← API Gateway
│  (Port 8080)│
└────────┬────────┘
 │
┌────────▼────────┐
│   Go Backend│  ← TODO Logic
│   (Port 8081)   │
└────────┬────────┘
 │
┌────────▼────────┐
│   PostgreSQL│  ← Database
│   (Port 5432)   │
└─────────────────┘
Luồng hoạt động:

User mở browser → truy cập http://localhost
NGINX phục vụ HTML/CSS/JS
JS gọi API → http://localhost/api/todos
NGINX forward request → Python (port 8080)
Python xử lý và gọi → Go (port 8081)
Go truy vấn → PostgreSQL
Kết quả trả ngược lại: PostgreSQL → Go → Python → NGINX → User


🧪 PHẦN 3: THỰC HÀNH TEST API VỚI CURL
3.1. Kiểm tra curl hoạt động
bash# Test curl cơ bản
curl https://api.github.com

# Kết quả mong đợi: JSON response với thông tin GitHub API
3.2. Các lệnh curl quan trọng
GET Request:
bash# Lấy dữ liệu
curl http://localhost:8080/api/todos

# Hiển thị headers
curl -i http://localhost:8080/api/todos

# Chỉ hiển thị status code
curl -o /dev/null -s -w "%{http_code}\n" http://localhost:8080/api/todos
Giải thích:

-i: Include headers trong output
-o /dev/null: Không hiển thị body
-s: Silent mode (không hiển thị progress)
-w "%{http_code}": Hiển thị HTTP status code

POST Request (Tạo TODO):
bashcurl -X POST http://localhost:8080/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Học Docker"}'
Giải thích:

-X POST: Chỉ định phương thức POST
-H: Thêm header (Header name: value)
-d: Dữ liệu gửi đi (data)

PUT Request (Cập nhật TODO):
bashcurl -X PUT http://localhost:8080/api/todos/123 \
  -H "Content-Type: application/json" \
  -d '{"title":"Học Docker nâng cao","completed":true}'
DELETE Request (Xóa TODO):
bashcurl -X DELETE http://localhost:8080/api/todos/123
Lưu response vào file:
bashcurl http://localhost:8080/api/todos -o todos.json

# Hoặc dùng redirect
curl http://localhost:8080/api/todos > todos.json

🧪 PHẦN 4: THỰC HÀNH VỚI POSTMAN
4.1. Tạo Collection mới

Mở Postman
Click "New" → "Collection"
Đặt tên: "TODO App - DevOps Course"

4.2. Thêm Request - GET All TODOs

Click "Add request" trong Collection
Đặt tên: "Get All TODOs"
Method: GET
URL: http://localhost:8080/api/todos
Click "Save"

4.3. Thêm Request - POST Create TODO

Tạo request mới: "Create TODO"
Method: POST
URL: http://localhost:8080/api/todos
Tab "Headers":

Key: Content-Type
Value: application/json


Tab "Body" → chọn "raw" → chọn "JSON":

json   {
 "title": "Học Kubernetes"
   }

Save

4.4. Thêm Request - PUT Update TODO

Tạo request: "Update TODO"
Method: PUT
URL: http://localhost:8080/api/todos/{{todo_id}}
Body:

json   {
 "title": "Học Kubernetes nâng cao",
 "completed": true
   }
Sử dụng Variables:

Tab "Variables" trong Collection
Thêm variable: todo_id = 123
Trong URL dùng: {{todo_id}}

4.5. Thêm Request - DELETE TODO

Tạo request: "Delete TODO"
Method: DELETE
URL: http://localhost:8080/api/todos/{{todo_id}}


✅ PHẦN 5: KIỂM TRA HOÀN THÀNH GIAI ĐOẠN 1
Checklist:

 Python đã cài đặt và chạy được python --version
 Go đã cài đặt và chạy được go version
 Git đã cài đặt và cấu hình user
 curl chạy được và test được API GitHub
 Postman/Insomnia đã cài đặt
 VS Code đã cài đặt với các extension
 Hiểu được HTTP Request/Response
 Hiểu được các phương thức HTTP
 Hiểu được REST API design
 Hiểu được JSON format
 Hiểu được kiến trúc Microservices cơ bản
 Biết dùng curl để test API
 Biết dùng Postman để test API


🎯 BÀI TẬP THỰC HÀNH
Bài 1: Test API công khai
Sử dụng curl để test API sau: https://jsonplaceholder.typicode.com
bash# 1. Lấy danh sách posts
curl https://jsonplaceholder.typicode.com/posts

# 2. Lấy post ID 1
curl https://jsonplaceholder.typicode.com/posts/1

# 3. Tạo post mới
curl -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","body":"Nội dung","userId":1}'

# 4. Cập nhật post
curl -X PUT https://jsonplaceholder.typicode.com/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated","body":"Nội dung mới","userId":1}'

# 5. Xóa post
curl -X DELETE https://jsonplaceholder.typicode.com/posts/1
```

**Yêu cầu:**
- Chạy 5 lệnh trên
- Quan sát response
- Ghi chú HTTP status code của mỗi request

### Bài 2: Tạo Postman Collection

1. Tạo Collection "JSONPlaceholder Tests"
2. Thêm 5 requests như bài 1
3. Export Collection ra file JSON
4. Share với mentor/giảng viên

### Bài 3: Phân tích HTTP Request

Phân tích request sau và giải thích từng phần:
```
POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
Accept: application/json
User-Agent: MyApp/1.0

{
  "username": "john_doe",
  "email": "john@example.com",
  "age": 25
}
```

**Trả lời:**
1. Phương thức HTTP là gì?
2. Endpoint là gì?
3. Header nào dùng để xác thực?
4. Dữ liệu gửi đi là gì?
5. Server sẽ trả về mã HTTP nào nếu thành công?

---

## 🐛 XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: Python không tìm thấy
```
'python' is not recognized as an internal or external command
```

**Nguyên nhân:** Python chưa được thêm vào PATH

**Giải pháp:**
1. Gỡ và cài lại Python, nhớ tích "Add Python to PATH"
2. Hoặc thêm thủ công vào Environment Variables

### Lỗi 2: Go command not found
```
go: command not found
Giải pháp:
bash# Kiểm tra Go đã cài chưa
which go  # Linux/Mac
where go  # Windows

# Nếu chưa có, cài lại theo hướng dẫn phần 1.2
```

### Lỗi 3: Port đã bị chiếm
```
Error: listen tcp :8080: bind: address already in use
```

**Giải pháp:**

**Windows:**

```bash
# Tìm process đang dùng port 8080
netstat -ano | findstr :8080

# Kill process (PID là số ở cột cuối)
taskkill /PID [số_PID] /F
```

**Linux/Mac:**

```bash
# Tìm process
lsof -i :8080

# Kill process
kill -9 [PID]
```

### Lỗi 4: curl SSL certificate error
```
curl: (60) SSL certificate problem: certificate verify failed
```

**Giải pháp tạm thời (chỉ dùng cho test):**

```bash
curl -k https://api.example.com
# -k: insecure, bỏ qua verify SSL
```

**Giải pháp lâu dài:** Cài đặt CA certificates

---

## 📖 TÀI LIỆU THAM KHẢO

**Tài liệu chính thức:**

- Python: https://docs.python.org/3/
- Go: https://go.dev/doc/
- HTTP: https://developer.mozilla.org/en-US/docs/Web/HTTP
- REST API: https://restfulapi.net/

**Công cụ online:**

- JSON Formatter: https://jsonformatter.org/
- HTTP Status Codes: https://httpstatuses.com/
- Postman Learning: https://learning.postman.com/

**Video tiếng Việt (khuyến nghị):**

- Python cơ bản: [tìm trên YouTube]
- Go tutorial: [tìm trên YouTube]
- HTTP & REST API: [tìm trên YouTube]

---

## 🎊 KẾT LUẬN GIAI ĐOẠN 1

Chúc mừng! Bạn đã hoàn thành Giai đoạn 1. Bây giờ bạn đã:

✅ Có đầy đủ công cụ để bắt đầu code  
✅ Hiểu được cách HTTP hoạt động  
✅ Biết thiết kế REST API  
✅ Thành thạo curl và Postman  
✅ Nắm được kiến trúc Microservices cơ bản

---

<a id="giai-doan-2"></a>

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

---

<a id="giai-doan-3"></a>

# GIAI ĐOẠN 3: THÊM CHỨC NĂNG TODO (VẪN LƯU RAM)

## 📌 MỤC TIÊU GIAI ĐOẠN 3
Sau khi hoàn thành giai đoạn này, bạn sẽ:

✅ Mở rộng từ Ping-Pong sang TODO App hoàn chỉnh  
✅ Xây dựng CRUD (Create, Read, Update, Delete) operations  
✅ Hiểu cách quản lý state phức tạp hơn  
✅ Thành thạo RESTful API design  
✅ Biết validate dữ liệu và xử lý edge cases  
✅ Sẵn sàng thêm giao diện web (Giai đoạn 4)

---

## 🗂️ PHẦN 1: PHÂN TÍCH YÊU CẦU TODO APP

### 1.1. User Stories

Là người dùng, tôi muốn:

- Tạo TODO mới với tiêu đề
- Xem danh sách tất cả TODO
- Xem chi tiết 1 TODO
- Đánh dấu TODO đã hoàn thành/chưa hoàn thành
- Chỉnh sửa tiêu đề TODO
- Xóa TODO

### 1.2. Data Model

**TODO Structure:**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Học Docker từ cơ bản",
  "completed": false,
  "created_at": "2026-01-25T10:30:00+07:00",
  "updated_at": "2026-01-25T10:30:00+07:00"
}
```

**Giải thích fields:**

- `id`: UUID (Universally Unique Identifier) - ID duy nhất
- `title`: Tiêu đề TODO (string, required)
- `completed`: Trạng thái hoàn thành (boolean, default: false)
- `created_at`: Thời gian tạo (timestamp)
- `updated_at`: Thời gian cập nhật cuối (timestamp)

### 1.3. API Endpoints Design

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/todos` | Lấy tất cả TODO | - | `[{todo}, {todo}]` |
| GET | `/todos/:id` | Lấy 1 TODO | - | `{todo}` |
| POST | `/todos` | Tạo TODO mới | `{title}` | `{todo}` |
| PUT | `/todos/:id` | Cập nhật TODO | `{title, completed}` | `{todo}` |
| DELETE | `/todos/:id` | Xóa TODO | - | `204 No Content` |

**Gateway Endpoints (Python):**

- Tương tự nhưng prefix `/api`: `/api/todos`, `/api/todos/:id`

---

## 🔧 PHẦN 2: XÂY DỰNG GO SERVICE - TODO BACKEND

### 2.1. Cập nhật main.go - Thêm TODO Structure

Mở file `go-service/main.go`, thay thế toàn bộ bằng code sau:

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
```

### 2.2. Cài đặt thư viện UUID

```bash
# Di chuyển vào thư mục go-service
cd go-service

# Cài thư viện UUID
go get github.com/google/uuid

# Cập nhật dependencies
go mod tidy
```

### 2.3. Giải thích chi tiết code Go mới

**UUID Generation:**

```go
import "github.com/google/uuid"

todo.ID = uuid.New().String()
```

- `uuid.New()`: Tạo UUID version 4 (random)
- `.String()`: Convert sang string format: `550e8400-e29b-41d4-a716-446655440000`

**Tại sao dùng UUID thay vì số đếm?**

- Tránh conflict khi có nhiều instance
- Bảo mật hơn (không đoán được)
- Dễ merge data từ nhiều nguồn

**Pointer trong UpdateTodoRequest:**

```go
type UpdateTodoRequest struct {
	Title     *string `json:"title"`
	Completed *bool   `json:"completed"`
}
```

**Vấn đề cần giải quyết:**

- User chỉ muốn cập nhật `completed`, không sửa `title`
- Nếu dùng `bool` thay vì `*bool`:
  - `completed: false` → không biết là "giữ nguyên" hay "set = false"
  - `completed` không gửi lên → Go nhận `false` (zero value)

**Giải pháp với pointer:**

```go
if req.Completed != nil {
    todo.Completed = *req.Completed
}
```

- `nil`: Field không được gửi lên → không cập nhật
- `*bool`: Field có giá trị → cập nhật

**Ví dụ:**

```json
// Chỉ cập nhật completed
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
```

**RWMutex vs Mutex:**

```go
var todosMutex sync.RWMutex
```

**RWMutex (Read-Write Mutex):**

- `RLock()`: Read lock - nhiều goroutine đọc cùng lúc
- `Lock()`: Write lock - chỉ 1 goroutine ghi, chặn tất cả đọc/ghi khác

**Khi nào dùng gì:**

- Đọc nhiều: `RLock()` (`getAllTodos`, `getTodoByID`)
- Ghi: `Lock()` (`createTodo`, `updateTodo`, `deleteTodo`)

**Lợi ích:**

- Performance tốt hơn khi có nhiều read operations
- Vẫn đảm bảo data consistency

**Map operations:**

```go
todos = make(map[string]Todo)
```

- **Map trong Go**: key-value store (như dictionary Python, object JS)
- `make()`: Khởi tạo map rỗng

**Các thao tác:**

```go
go// Thêm/Cập nhật
todos[id] = todo

// Đọc
todo, exists := todos[id]

// Xóa
delete(todos, id)

// Lấy số lượng
len(todos)
```

**Convert Map → Slice:**

```go
todoList := make([]Todo, 0, len(todos))
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
```

### 2.5. Test Go TODO API với curl

**Test 1: Lấy tất cả TODO (ban đầu rỗng)**

```bash
curl http://localhost:8081/todos
```

Kết quả:

```json
[]
```

**Test 2: Tạo TODO mới**

```bash
curl -X POST http://localhost:8081/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Học Docker"}'
```

Kết quả:

```json
{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "title": "Học Docker",
  "completed": false,
  "created_at": "2026-01-25T16:30:00+07:00",
  "updated_at": "2026-01-25T16:30:00+07:00"
}
```

**Lưu lại ID để test tiếp!**

**Test 3: Tạo thêm TODO**

```bash
curl -X POST http://localhost:8081/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Học Kubernetes"}'

curl -X POST http://localhost:8081/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Học GitLab CI/CD"}'
```

**Test 4: Lấy tất cả TODO (giờ có 3 items)**

```bash
curl http://localhost:8081/todos
```

Kết quả:

```json
[
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
```

**Test 5: Lấy 1 TODO theo ID**

```bash
# Thay YOUR_TODO_ID bằng ID thực tế từ kết quả trên
curl http://localhost:8081/todos/7c9e6679-7425-40de-944b-e07fc1f90ae7
```

Kết quả:

```json{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "title": "Học Docker",
  "completed": false,
  "created_at": "2026-01-25T16:30:00+07:00",
  "updated_at": "2026-01-25T16:30:00+07:00"
}
```

**Test 6: Cập nhật TODO - đánh dấu hoàn thành**

```bash
curl -X PUT http://localhost:8081/todos/7c9e6679-7425-40de-944b-e07fc1f90ae7 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
```

Kết quả:

```json{
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
```

**Test 9: Kiểm tra lại danh sách (TODO đã xóa)**

```bash
curl http://localhost:8081/todos
```

**Test 10: Test error cases**

```bash
# Lấy TODO không tồn tại
curl http://localhost:8081/todos/invalid-id

# Tạo TODO thiếu title
curl -X POST http://localhost:8081/todos \
  -H "Content-Type: application/json" \
  -d '{}'

# Tạo TODO với title rỗng
curl -X POST http://localhost:8081/todos \
  -H "Content-Type: application/json" \
  -d '{"title":""}'
```

---

## 🐍 PHẦN 3: CẬP NHẬT PYTHON SERVICE - TODO GATEWAY

### 3.1. Cập nhật app.py - Thêm TODO endpoints

Mở file `python-service/app.py`, thay thế toàn bộ bằng code sau:

```python
from flask import Flask, jsonify, request
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

---

<a id="giai-doan-4"></a>

# GIAI ĐOẠN 4: THÊM NGINX - WEB INTERFACE

## 📌 MỤC TIÊU GIAI ĐOẠN 4
Sau khi hoàn thành giai đoạn này, bạn sẽ:

✅ Xây dựng giao diện web đẹp cho TODO App  
✅ Hiểu cách NGINX hoạt động như web server  
✅ Cấu hình NGINX làm reverse proxy  
✅ Tích hợp Frontend → NGINX → Python → Go  
✅ Xử lý CORS và static files  
✅ Có ứng dụng hoàn chỉnh user có thể dùng được

---

## 🗂️ PHẦN 1: TỔNG QUAN KIẾN TRÚC

### 1.1. Kiến trúc hiện tại (Giai đoạn 3)

```
User (curl/Postman) → Python API → Go Service
```

**Vấn đề:**

- Không có giao diện trực quan
- Chỉ developer mới dùng được
- Khó demo cho người khác

### 1.2. Kiến trúc mới (Giai đoạn 4)

```
┌─────────────────────────────────────────────┐
│           User (Browser)                     │
└─────────────────┬───────────────────────────┘
                  │ HTTP
         ┌────────▼────────┐
         │  NGINX :80      │
         │  - Static files │
         │  - Reverse Proxy│
         └────────┬────────┘
                  │
         ┌────────▼────────────────┐
         │                         │
    Static Files          /api/* requests
    (HTML/CSS/JS)                 │
         │                        │
         │               ┌────────▼────────┐
         │               │ Python :8080    │
         │               │ (Gateway)       │
         │               └────────┬────────┘
         │                        │
         │               ┌────────▼────────┐
         │               │ Go :8081        │
         │               │ (Backend)       │
         │               └─────────────────┘
         │
    ┌────▼─────┐
    │ Browser  │
    │ renders  │
    └──────────┘
```

**Giải thích luồng:**

1. User mở `http://localhost` → NGINX
2. NGINX serve `index.html`, `style.css`, `app.js`
3. Browser render giao diện
4. User click "Add TODO" → JavaScript gọi API
5. AJAX request → `http://localhost/api/todos`
6. NGINX proxy → Python (port 8080)
7. Python forward → Go (port 8081)
8. Response ngược → Go → Python → NGINX → Browser
9. JavaScript update DOM

---

## 🎨 PHẦN 2: XÂY DỰNG FRONTEND

### 2.1. Tạo cấu trúc thư mục

```bash
# Di chuyển về thư mục gốc
cd todo-app-devsecops

# Tạo cấu trúc frontend
mkdir -p frontend/css
mkdir -p frontend/js
mkdir -p frontend/images
```

**Cấu trúc:**
```
frontend/
├── index.html       ← Trang chính
├── css/
│   └── style.css    ← Styles
├── js/
│   └── app.js       ← Logic JavaScript
└── images/          ← Hình ảnh (nếu có)
```

### 2.2. Tạo index.html

Tạo file `frontend/index.html`:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TODO App - DevSecOps Learning</title>
    <link rel="stylesheet" href="/css/style.css">
    <!-- Font Awesome cho icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <h1><i class="fas fa-tasks"></i> TODO App</h1>
            <p class="subtitle">DevSecOps Learning Project</p>
        </div>
    </header>

    <!-- Main Container -->
    <main class="container">
        <!-- Stats Section -->
        <section class="stats-section">
            <div class="stat-card">
                <i class="fas fa-list"></i>
                <div class="stat-info">
                    <span class="stat-number" id="total-count">0</span>
                    <span class="stat-label">Tổng số</span>
                </div>
            </div>
            <div class="stat-card">
                <i class="fas fa-check-circle" style="color: #10b981;"></i>
                <div class="stat-info">
                    <span class="stat-number" id="completed-count">0</span>
                    <span class="stat-label">Hoàn thành</span>
                </div>
            </div>
            <div class="stat-card">
                <i class="fas fa-clock" style="color: #f59e0b;"></i>
                <div class="stat-info">
                    <span class="stat-number" id="pending-count">0</span>
                    <span class="stat-label">Đang làm</span>
                </div>
            </div>
            <div class="stat-card">
                <i class="fas fa-server" style="color: #6366f1;"></i>
                <div class="stat-info">
                    <span class="stat-number" id="ping-count">0</span>
                    <span class="stat-label">Ping Count</span>
                </div>
            </div>
        </section>

        <!-- Add TODO Form -->
        <section class="add-todo-section">
            <form id="add-todo-form" class="add-todo-form">
                <input 
                    type="text" 
                    id="todo-input" 
                    placeholder="Thêm công việc mới..." 
                    required
                    autocomplete="off"
                >
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-plus"></i> Thêm
                </button>
            </form>
        </section>

        <!-- Filter Tabs -->
        <section class="filter-section">
            <div class="filter-tabs">
                <button class="filter-tab active" data-filter="all">
                    <i class="fas fa-list"></i> Tất cả
                </button>
                <button class="filter-tab" data-filter="active">
                    <i class="fas fa-clock"></i> Đang làm
                </button>
                <button class="filter-tab" data-filter="completed">
                    <i class="fas fa-check-circle"></i> Hoàn thành
                </button>
            </div>
        </section>

        <!-- TODO List -->
        <section class="todo-list-section">
            <!-- Loading Spinner -->
            <div id="loading" class="loading" style="display: none;">
                <i class="fas fa-spinner fa-spin"></i> Đang tải...
            </div>

            <!-- Error Message -->
            <div id="error-message" class="error-message" style="display: none;"></div>

            <!-- Empty State -->
            <div id="empty-state" class="empty-state" style="display: none;">
                <i class="fas fa-inbox"></i>
                <p>Chưa có công việc nào</p>
                <small>Thêm công việc đầu tiên của bạn!</small>
            </div>

            <!-- TODO List -->
            <ul id="todo-list" class="todo-list"></ul>
        </section>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>
                <i class="fas fa-code"></i> 
                Made with <i class="fas fa-heart" style="color: #ef4444;"></i> 
                for DevSecOps Learning
            </p>
            <div class="service-status">
                <span class="status-indicator" id="service-status">
                    <i class="fas fa-circle"></i> Kiểm tra kết nối...
                </span>
            </div>
        </div>
    </footer>

    <!-- Edit Modal -->
    <div id="edit-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2><i class="fas fa-edit"></i> Chỉnh sửa công việc</h2>
                <button class="modal-close" id="modal-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <input 
                    type="text" 
                    id="edit-todo-input" 
                    placeholder="Nhập tiêu đề mới..."
                >
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" id="cancel-edit">Hủy</button>
                <button class="btn btn-primary" id="save-edit">
                    <i class="fas fa-save"></i> Lưu
                </button>
            </div>
        </div>
    </div>

    <!-- JavaScript -->
    <script src="/js/app.js"></script>
</body>
</html>
```

### 2.3. Tạo style.css

Tạo file `frontend/css/style.css`:

```css
/* ==================== RESET & BASE ==================== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    /* Colors */
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --secondary: #8b5cf6;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --info: #3b82f6;
    
    /* Grays */
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-200: #e5e7eb;
    --gray-300: #d1d5db;
    --gray-400: #9ca3af;
    --gray-500: #6b7280;
    --gray-600: #4b5563;
    --gray-700: #374151;
    --gray-800: #1f2937;
    --gray-900: #111827;
    
    /* Spacing */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    --spacing-2xl: 3rem;
    
    /* Border Radius */
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    --radius-xl: 1rem;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: var(--gray-900);
    line-height: 1.6;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 var(--spacing-md);
}

/* ==================== HEADER ==================== */
.header {
    background: white;
    box-shadow: var(--shadow-md);
    padding: var(--spacing-xl) 0;
    margin-bottom: var(--spacing-2xl);
}

.header h1 {
    font-size: 2.5rem;
    color: var(--primary);
    margin-bottom: var(--spacing-sm);
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
}

.header h1 i {
    font-size: 2rem;
}

.subtitle {
    color: var(--gray-600);
    font-size: 1rem;
}

/* ==================== STATS SECTION ==================== */
.stats-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-xl);
}

.stat-card {
    background: white;
    padding: var(--spacing-lg);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.stat-card i {
    font-size: 2rem;
    color: var(--primary);
}

.stat-info {
    display: flex;
    flex-direction: column;
}

.stat-number {
    font-size: 1.75rem;
    font-weight: bold;
    color: var(--gray-900);
    line-height: 1;
}

.stat-label {
    font-size: 0.875rem;
    color: var(--gray-600);
}

/* ==================== ADD TODO FORM ==================== */
.add-todo-section {
    margin-bottom: var(--spacing-xl);
}

.add-todo-form {
    display: flex;
    gap: var(--spacing-md);
    background: white;
    padding: var(--spacing-md);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
}

.add-todo-form input {
    flex: 1;
    padding: var(--spacing-md);
    border: 2px solid var(--gray-200);
    border-radius: var(--radius-md);
    font-size: 1rem;
    transition: border-color 0.2s;
}

.add-todo-form input:focus {
    outline: none;
    border-color: var(--primary);
}

.add-todo-form input::placeholder {
    color: var(--gray-400);
}

/* ==================== BUTTONS ==================== */
.btn {
    padding: var(--spacing-md) var(--spacing-lg);
    border: none;
    border-radius: var(--radius-md);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-sm);
}

.btn:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

.btn:active {
    transform: translateY(0);
}

.btn-primary {
    background: var(--primary);
    color: white;
}

.btn-primary:hover {
    background: var(--primary-dark);
}

.btn-secondary {
    background: var(--gray-200);
    color: var(--gray-700);
}

.btn-secondary:hover {
    background: var(--gray-300);
}

.btn-success {
    background: var(--success);
    color: white;
}

.btn-danger {
    background: var(--danger);
    color: white;
}

.btn-sm {
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: 0.875rem;
}

/* ==================== FILTER TABS ==================== */
.filter-section {
    margin-bottom: var(--spacing-lg);
}

.filter-tabs {
    display: flex;
    gap: var(--spacing-sm);
    background: white;
    padding: var(--spacing-sm);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
}

.filter-tab {
    flex: 1;
    padding: var(--spacing-md);
    background: transparent;
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
    color: var(--gray-600);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-sm);
}

.filter-tab:hover {
    background: var(--gray-100);
    color: var(--gray-900);
}

.filter-tab.active {
    background: var(--primary);
    color: white;
}

/* ==================== TODO LIST ==================== */
.todo-list-section {
    background: white;
    padding: var(--spacing-lg);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    min-height: 300px;
}

.todo-list {
    list-style: none;
}

.todo-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
    border-bottom: 1px solid var(--gray-200);
    transition: background 0.2s;
}

.todo-item:last-child {
    border-bottom: none;
}

.todo-item:hover {
    background: var(--gray-50);
}

.todo-item.completed .todo-text {
    text-decoration: line-through;
    color: var(--gray-500);
}

.todo-checkbox {
    width: 24px;
    height: 24px;
    cursor: pointer;
}

.todo-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
}

.todo-text {
    font-size: 1.125rem;
    color: var(--gray-900);
    word-break: break-word;
}

.todo-meta {
    font-size: 0.75rem;
    color: var(--gray-500);
    display: flex;
    gap: var(--spacing-md);
}

.todo-actions {
    display: flex;
    gap: var(--spacing-sm);
}

.todo-actions button {
    padding: var(--spacing-sm) var(--spacing-md);
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.2s;
    font-size: 0.875rem;
}

.btn-edit {
    background: var(--info);
    color: white;
}

.btn-edit:hover {
    background: #2563eb;
}

.btn-delete {
    background: var(--danger);
    color: white;
}

.btn-delete:hover {
    background: #dc2626;
}

/* ==================== LOADING & STATES ==================== */
.loading {
    text-align: center;
    padding: var(--spacing-2xl);
    color: var(--gray-600);
    font-size: 1.125rem;
}

.loading i {
    font-size: 2rem;
    color: var(--primary);
}

.empty-state {
    text-align: center;
    padding: var(--spacing-2xl);
    color: var(--gray-500);
}

.empty-state i {
    font-size: 4rem;
    margin-bottom: var(--spacing-md);
    color: var(--gray-300);
}

.empty-state p {
    font-size: 1.25rem;
    margin-bottom: var(--spacing-sm);
}

.error-message {
    background: #fee2e2;
    border: 1px solid var(--danger);
    color: #991b1b;
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
    margin-bottom: var(--spacing-md);
}

/* ==================== MODAL ==================== */
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1000;
    align-items: center;
    justify-content: center;
}

.modal.active {
    display: flex;
}

.modal-content {
    background: white;
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-xl);
    max-width: 500px;
    width: 90%;
    max-height: 90vh;
    overflow: auto;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-lg);
    border-bottom: 1px solid var(--gray-200);
}

.modal-header h2 {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    color: var(--gray-900);
}

.modal-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--gray-600);
    padding: var(--spacing-sm);
    line-height: 1;
}

.modal-close:hover {
    color: var(--gray-900);
}

.modal-body {
    padding: var(--spacing-lg);
}

.modal-body input {
    width: 100%;
    padding: var(--spacing-md);
    border: 2px solid var(--gray-200);
    border-radius: var(--radius-md);
    font-size: 1rem;
}

.modal-body input:focus {
    outline: none;
    border-color: var(--primary);
}

.modal-footer {
    padding: var(--spacing-lg);
    border-top: 1px solid var(--gray-200);
    display: flex;
    justify-content: flex-end;
    gap: var(--spacing-md);
}

/* ==================== FOOTER ==================== */
.footer {
    background: white;
    margin-top: var(--spacing-2xl);
    padding: var(--spacing-xl) 0;
    text-align: center;
    box-shadow: var(--shadow-md);
}

.footer p {
    color: var(--gray-600);
    margin-bottom: var(--spacing-md);
}

.service-status {
    font-size: 0.875rem;
}

.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-md);
    background: var(--gray-100);
    border-radius: var(--radius-md);
}

.status-indicator.online {
    background: #d1fae5;
    color: #065f46;
}

.status-indicator.online i {
    color: var(--success);
}

.status-indicator.offline {
    background: #fee2e2;
    color: #991b1b;
}

.status-indicator.offline i {
    color: var(--danger);
}

/* ==================== ANIMATIONS ==================== */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.todo-item {
    animation: fadeIn 0.3s ease;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 768px) {
    .header h1 {
        font-size: 2rem;
    }
    
    .stats-section {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .filter-tabs {
        flex-direction: column;
    }
    
    .todo-item {
        flex-wrap: wrap;
    }
    
    .todo-actions {
        width: 100%;
        justify-content: flex-end;
    }
}
```

### 2.4. Tạo app.js

Tạo file `frontend/js/app.js`:

```javascript
// ==================== CONFIGURATION ====================
const API_BASE_URL = '/api'; // NGINX sẽ proxy /api/* sang Python

// ==================== STATE ====================
let todos = [];
let currentFilter = 'all'; // 'all', 'active', 'completed'
let editingTodoId = null;

// ==================== DOM ELEMENTS ====================
const elements = {
    todoList: document.getElementById('todo-list'),
    todoInput: document.getElementById('todo-input'),
    addTodoForm: document.getElementById('add-todo-form'),
    loading: document.getElementById('loading'),
    errorMessage: document.getElementById('error-message'),
    emptyState: document.getElementById('empty-state'),
    
    // Stats
    totalCount: document.getElementById('total-count'),
    completedCount: document.getElementById('completed-count'),
    pendingCount: document.getElementById('pending-count'),
    pingCount: document.getElementById('ping-count'),
    
    // Filters
    filterTabs: document.querySelectorAll('.filter-tab'),
    
    // Modal
    editModal: document.getElementById('edit-modal'),
    editTodoInput: document.getElementById('edit-todo-input'),
    modalClose: document.getElementById('modal-close'),
    cancelEdit: document.getElementById('cancel-edit'),
    saveEdit: document.getElementById('save-edit'),
    
    // Service status
    serviceStatus: document.getElementById('service-status')
};

// ==================== API FUNCTIONS ====================

/**
 * Generic fetch wrapper với error handling
 */
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        // Kiểm tra response
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.message || `HTTP ${response.status}`);
        }
        
        // DELETE thường trả 204 No Content
        if (response.status === 204) {
            return { success: true };
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Lấy tất cả TODO
 */
async function fetchTodos() {
    const data = await apiCall('/todos');
    return data.data || [];
}

/**
 * Tạo TODO mới
 */
async function createTodo(title) {
    const data = await apiCall('/todos', {
        method: 'POST',
        body: JSON.stringify({ title })
    });
    return data.data;
}

/**
 * Cập nhật TODO
 */
async function updateTodo(id, updates) {
    const data = await apiCall(`/todos/${id}`, {
        method: 'PUT',
        body: JSON.stringify(updates)
    });
    return data.data;
}

/**
 * Xóa TODO
 */
async function deleteTodo(id) {
    await apiCall(`/todos/${id}`, {
        method: 'DELETE'
    });
}

/**
 * Lấy ping stats
 */
async function fetchStats() {
    try {
        const data = await apiCall('/stats');
        return data.data || { success_count: 0 };
    } catch (error) {
        return { success_count: 0 };
    }
}

/**
 * Test ping
 */
async function pingService() {
    try {
        await apiCall('/ping', { method: 'POST' });
        return true;
    } catch (error) {
        return false;
    }
}

// ==================== UI FUNCTIONS ====================

/**
 * Hiển thị loading
 */
function showLoading() {
    elements.loading.style.display = 'block';
    elements.todoList.style.display = 'none';
    elements.emptyState.style.display = 'none';
    elements.errorMessage.style.display = 'none';
}

/**
 * Ẩn loading
 */
function hideLoading() {
    elements.loading.style.display = 'none';
}

/**
 * Hiển thị error
 */
function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorMessage.style.display = 'block';
    setTimeout(() => {
        elements.errorMessage.style.display = 'none';
    }, 5000);
}

/**
 * Format timestamp
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    
    // Dưới 1 phút
    if (diff < 60000) {
        return 'Vừa xong';
    }
    
    // Dưới 1 giờ
    if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return `${minutes} phút trước`;
    }
    
    // Dưới 1 ngày
    if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours} giờ trước`;
    }
    
    // Ngày cụ thể
    return date.toLocaleDateString('vi-VN');
}

/**
 * Render 1 TODO item
 */
function renderTodoItem(todo) {
    const li = document.createElement('li');
    li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
    li.dataset.id = todo.id;
    
    li.innerHTML = `
        <input 
            type="checkbox" 
            class="todo-checkbox" 
            ${todo.completed ? 'checked'tiếp tục : ''}
data-id="${todo.id}"
>
<div class="todo-content">
<div class="todo-text">${escapeHtml(todo.title)}</div>
<div class="todo-meta">
<span><i class="fas fa-clock"></i> ${formatDate(todo.created_at)}</span>
${todo.completed ? '<span><i class="fas fa-check"></i> Hoàn thành</span>' : ''}
</div>
</div>
<div class="todo-actions">
<button class="btn-edit" data-id="${todo.id}">
<i class="fas fa-edit"></i> Sửa
</button>
<button class="btn-delete" data-id="${todo.id}">
<i class="fas fa-trash"></i> Xóa
</button>
</div>
`;
return li;
}
/**

Escape HTML để tránh XSS
*/
function escapeHtml(text) {
const div = document.createElement('div');
div.textContent = text;
return div.innerHTML;
}

/**

Filter todos theo trạng thái
*/
function getFilteredTodos() {
switch (currentFilter) {
case 'active':
return todos.filter(t => !t.completed);
case 'completed':
return todos.filter(t => t.completed);
default:
return todos;
}
}

/**

Render danh sách TODO
*/
function renderTodoList() {
const filteredTodos = getFilteredTodos();
// Clear list
elements.todoList.innerHTML = '';
// Kiểm tra empty
if (filteredTodos.length === 0) {
elements.todoList.style.display = 'none';
elements.emptyState.style.display = 'block';
return;
}
// Hiển thị list
elements.todoList.style.display = 'block';
elements.emptyState.style.display = 'none';
// Render items
filteredTodos.forEach(todo => {
const li = renderTodoItem(todo);
elements.todoList.appendChild(li);
});
// Update stats
updateStats();
}

/**

Update statistics
*/
function updateStats() {
const total = todos.length;
const completed = todos.filter(t => t.completed).length;
const pending = total - completed;
elements.totalCount.textContent = total;
elements.completedCount.textContent = completed;
elements.pendingCount.textContent = pending;
}

/**

Load todos từ server
*/
async function loadTodos() {
showLoading();
try {
todos = await fetchTodos();
renderTodoList();
} catch (error) {
showError('Không thể tải danh sách TODO. Vui lòng kiểm tra kết nối.');
console.error('Load todos error:', error);
} finally {
hideLoading();
}
}

/**

Load ping stats
*/
async function loadPingStats() {
try {
const stats = await fetchStats();
elements.pingCount.textContent = stats.success_count || 0;
} catch (error) {
console.error('Load stats error:', error);
}
}

/**

Check service status
*/
async function checkServiceStatus() {
const isOnline = await pingService();
const status = elements.serviceStatus;
if (isOnline) {
status.className = 'status-indicator online';
status.innerHTML = '<i class="fas fa-circle"></i> Dịch vụ hoạt động';
await loadPingStats();
} else {
status.className = 'status-indicator offline';
status.innerHTML = '<i class="fas fa-circle"></i> Mất kết nối';
}
}

// ==================== EVENT HANDLERS ====================
/**

Handle add TODO
*/
async function handleAddTodo(e) {
e.preventDefault();
const title = elements.todoInput.value.trim();
if (!title) return;
try {
const newTodo = await createTodo(title);
todos.push(newTodo);
renderTodoList();
elements.todoInput.value = '';
elements.todoInput.focus();
} catch (error) {
showError('Không thể thêm TODO. Vui lòng thử lại.');
console.error('Create todo error:', error);
}
}

/**

Handle toggle checkbox
*/
async function handleToggleTodo(id, completed) {
try {
const updatedTodo = await updateTodo(id, { completed: !completed });
const index = todos.findIndex(t => t.id === id);
if (index !== -1) {
todos[index] = updatedTodo;
renderTodoList();
}
} catch (error) {
showError('Không thể cập nhật TODO.');
console.error('Toggle todo error:', error);
}
}

/**

Handle edit TODO
*/
function handleEditClick(id) {
const todo = todos.find(t => t.id === id);
if (!todo) return;
editingTodoId = id;
elements.editTodoInput.value = todo.title;
elements.editModal.classList.add('active');
elements.editTodoInput.focus();
}

/**

Handle save edit
*/
async function handleSaveEdit() {
const newTitle = elements.editTodoInput.value.trim();
if (!newTitle || !editingTodoId) return;
try {
const updatedTodo = await updateTodo(editingTodoId, { title: newTitle });
const index = todos.findIndex(t => t.id === editingTodoId);
if (index !== -1) {
todos[index] = updatedTodo;
renderTodoList();
}
closeEditModal();
} catch (error) {
showError('Không thể cập nhật TODO.');
console.error('Update todo error:', error);
}
}

/**

Close edit modal
*/
function closeEditModal() {
elements.editModal.classList.remove('active');
editingTodoId = null;
elements.editTodoInput.value = '';
}

/**

Handle delete TODO
*/
async function handleDeleteTodo(id) {
if (!confirm('Bạn có chắc muốn xóa TODO này?')) return;
try {
await deleteTodo(id);
todos = todos.filter(t => t.id !== id);
renderTodoList();
} catch (error) {
showError('Không thể xóa TODO.');
console.error('Delete todo error:', error);
}
}

/**

Handle filter change
*/
function handleFilterChange(filter) {
currentFilter = filter;
// Update active tab
elements.filterTabs.forEach(tab => {
if (tab.dataset.filter === filter) {
tab.classList.add('active');
} else {
tab.classList.remove('active');
}
});
renderTodoList();
}

// ==================== EVENT LISTENERS ====================
// Form submit
elements.addTodoForm.addEventListener('submit', handleAddTodo);
// Todo list delegation
elements.todoList.addEventListener('click', (e) => {
const target = e.target;
// Checkbox toggle
if (target.classList.contains('todo-checkbox')) {
    const id = target.dataset.id;
    const todo = todos.find(t => t.id === id);
    if (todo) {
        handleToggleTodo(id, todo.completed);
    }
}

// Edit button
if (target.classList.contains('btn-edit') || target.parentElement.classList.contains('btn-edit')) {
    const btn = target.classList.contains('btn-edit') ? target : target.parentElement;
    handleEditClick(btn.dataset.id);
}

// Delete button
if (target.classList.contains('btn-delete') || target.parentElement.classList.contains('btn-delete')) {
    const btn = target.classList.contains('btn-delete') ? target : target.parentElement;
    handleDeleteTodo(btn.dataset.id);
}
});
// Filter tabs
elements.filterTabs.forEach(tab => {
tab.addEventListener('click', () => {
handleFilterChange(tab.dataset.filter);
});
});
// Modal events
elements.modalClose.addEventListener('click', closeEditModal);
elements.cancelEdit.addEventListener('click', closeEditModal);
elements.saveEdit.addEventListener('click', handleSaveEdit);
// Close modal khi click outside
elements.editModal.addEventListener('click', (e) => {
if (e.target === elements.editModal) {
closeEditModal();
}
});
// Enter key trong edit modal
elements.editTodoInput.addEventListener('keypress', (e) => {
if (e.key === 'Enter') {
handleSaveEdit();
}
});
// ==================== INITIALIZATION ====================
/**

Initialize app
*/
async function init() {
console.log('TODO App initializing...');
// Check service status
await checkServiceStatus();
// Load initial data
await loadTodos();
// Auto refresh ping stats mỗi 30s
setInterval(loadPingStats, 30000);
// Auto check service status mỗi 10s
setInterval(checkServiceStatus, 10000);
console.log('TODO App ready!');
}

// Start app khi DOM loaded
if (document.readyState === 'loading') {
document.addEventListener('DOMContentLoaded', init);
} else {
init();
}
```

---

## 🔧 PHẦN 3: CÀI ĐẶT VÀ CẤU HÌNH NGINX

### 3.1. Cài đặt NGINX

#### **Windows:**
```bash
# Tải NGINX
# Truy cập: http://nginx.org/en/download.html
# Tải phiên bản Windows (nginx-1.24.0.zip)

# Giải nén vào thư mục
# Ví dụ: C:\nginx
```

#### **macOS:**
```bash
# Cài qua Homebrew
brew install nginx

# Kiểm tra
nginx -v
```

#### **Linux (Ubuntu/Debian):**
```bash
# Cập nhật package list
sudo apt update

# Cài NGINX
sudo apt install nginx -y

# Kiểm tra
nginx -v

# Start NGINX
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 3.2. Tạo cấu hình NGINX cho TODO App

**Tạo thư mục nginx config:**
```bash
# Di chuyển về thư mục gốc
cd todo-app-devsecops

# Tạo thư mục nginx
mkdir nginx
```

**Tạo file `nginx/nginx.conf`:**
```nginx
# ==================== NGINX CONFIGURATION FOR TODO APP ====================

# Chạy NGINX với user hiện tại (development mode)
# Production nên dùng user nginx hoặc www-data
user nginx;

# Số worker processes (= số CPU cores)
worker_processes auto;

# Error log
error_log /var/log/nginx/error.log warn;

# PID file
pid /var/run/nginx.pid;

events {
    # Số connections mỗi worker có thể xử lý
    worker_connections 1024;
}

http {
    # ==================== MIME TYPES ====================
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # ==================== LOGGING ====================
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    # ==================== PERFORMANCE ====================
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # ==================== GZIP COMPRESSION ====================
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss;

    # ==================== SERVER BLOCK ====================
    server {
        listen 80;
        server_name localhost;

        # Root directory cho static files
        root /usr/share/nginx/html;
        index index.html;

        # ==================== STATIC FILES ====================
        # Serve HTML, CSS, JS từ frontend folder
        location / {
            try_files $uri $uri/ /index.html;
            
            # Cache static files
            location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
                expires 1y;
                add_header Cache-Control "public, immutable";
            }
        }

        # ==================== API PROXY ====================
        # Proxy tất cả /api/* requests sang Python service
        location /api/ {
            # Python service đang chạy trên port 8080
            proxy_pass http://localhost:8080;
            
            # Headers để preserve thông tin request gốc
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeout settings
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
            
            # Buffer settings
            proxy_buffering off;
            proxy_request_buffering off;
            
            # CORS headers (nếu cần)
            add_header Access-Control-Allow-Origin * always;
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
            add_header Access-Control-Allow-Headers "Content-Type, Authorization" always;
            
            # Handle OPTIONS preflight
            if ($request_method = 'OPTIONS') {
                add_header Access-Control-Allow-Origin * always;
                add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
                add_header Access-Control-Allow-Headers "Content-Type, Authorization" always;
                add_header Content-Length 0;
                add_header Content-Type text/plain;
                return 204;
            }
        }

        # ==================== HEALTH CHECK ====================
        location /nginx-health {
            access_log off;
            return 200 "NGINX is healthy\n";
            add_header Content-Type text/plain;
        }

        # ==================== ERROR PAGES ====================
        error_page 404 /404.html;
        location = /404.html {
            internal;
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            internal;
        }
    }
}
```

### 3.3. Copy frontend files vào NGINX directory

#### **Linux/macOS:**
```bash
# Tạo symbolic link
sudo ln -s $(pwd)/frontend /usr/share/nginx/html

# Hoặc copy trực tiếp
sudo cp -r frontend/* /usr/share/nginx/html/
```

#### **Windows:**

**Nếu NGINX cài tại `C:\nginx`:**
```bash
# Copy frontend vào nginx html folder
xcopy /E /I frontend C:\nginx\html
```

### 3.4. Test cấu hình NGINX
```bash
# Linux/macOS
sudo nginx -t

# Windows (chạy từ thư mục nginx)
nginx.exe -t
```

**Output mong đợi:**
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

### 3.5. Chạy NGINX

#### **Linux/macOS:**
```bash
# Start NGINX
sudo systemctl start nginx

# Hoặc
sudo nginx

# Reload config (nếu đã chạy)
sudo systemctl reload nginx

# Hoặc
sudo nginx -s reload

# Kiểm tra status
sudo systemctl status nginx
```

#### **Windows:**
```bash
# Di chuyển vào thư mục NGINX
cd C:\nginx

# Start NGINX
start nginx.exe

# Reload (nếu thay đổi config)
nginx.exe -s reload

# Stop NGINX
nginx.exe -s stop
```

---

## 🧪 PHẦN 4: TEST TOÀN BỘ HỆ THỐNG

### 4.1. Checklist trước khi test

- [ ] Go service đang chạy (port 8081)
- [ ] Python service đang chạy (port 8080)
- [ ] NGINX đang chạy (port 80)
- [ ] Frontend files đã copy vào nginx/html

### 4.2. Test từng layer

**Test 1: NGINX Health Check**
```bash
curl http://localhost/nginx-health
```

**Kết quả:**
NGINX is healthy

**Test 2: Static Files**
```bash
# Mở browser
http://localhost

# Hoặc dùng curl
curl http://localhost
# Phải trả về HTML của index.html
```

**Test 3: API Proxy**
```bash
curl http://localhost/api/todos
```

**Kết quả:**
```json
{
  "count": 0,
  "data": [],
  "retrieved_at": "...",
  "status": "success"
}
```

### 4.3. Test giao diện web

1. **Mở browser:** `http://localhost`
2. **Kiểm tra giao diện hiển thị đúng**
3. **Thêm TODO mới:**
   - Nhập "Học Docker"
   - Click "Thêm"
   - TODO xuất hiện trong danh sách
4. **Đánh dấu hoàn thành:**
   - Click checkbox
   - TODO có gạch ngang
5. **Chỉnh sửa:**
   - Click "Sửa"
   - Modal hiện ra
   - Đổi tiêu đề → "Lưu"
6. **Xóa TODO:**
   - Click "Xóa"
   - Confirm → TODO biến mất
7. **Filter:**
   - Click "Đang làm" → Chỉ hiện TODO chưa xong
   - Click "Hoàn thành" → Chỉ hiện TODO đã xong
   - Click "Tất cả" → Hiện hết

### 4.4. Test luồng hoàn chỉnh
Browser → NGINX (port 80)
↓ GET /
NGINX serve index.html
↓
Browser render giao diện
↓ User click "Thêm TODO"
JavaScript → POST /api/todos
↓
NGINX proxy → Python (port 8080)
↓
Python forward → Go (port 8081)
↓
Go lưu vào RAM → trả response
↓
Response: Go → Python → NGINX → Browser
↓
JavaScript update DOM → TODO xuất hiện

---

## 🐛 PHẦN 5: XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: NGINX không start

**Triệu chứng:**
nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)

**Nguyên nhân:** Port 80 bị chiếm

**Giải pháp:**
```bash
# Linux/macOS - Tìm process
sudo lsof -i :80

# Kill process
sudo kill -9 [PID]

# Hoặc đổi port trong nginx.conf
listen 8000;  # Thay vì 80
```

### Lỗi 2: 502 Bad Gateway

**Triệu chứng:** Browser hiển thị "502 Bad Gateway"

**Nguyên nhân:** Python service không chạy hoặc sai port

**Kiểm tra:**
```bash
# Test Python có chạy không
curl http://localhost:8080/health

# Nếu không, start Python
cd python-service
python app.py
```

### Lỗi 3: Static files không load

**Triệu chứng:** Giao diện không có CSS, JavaScript không chạy

**Nguyên nhân:** Sai đường dẫn trong nginx.conf

**Kiểm tra:**
```bash
# Xem nginx log
sudo tail -f /var/log/nginx/error.log

# Kiểm tra file có tồn tại
ls -la /usr/share/nginx/html/
```

### Lỗi 4: CORS error

**Triệu chứng:** Console browser báo CORS policy error

**Giải pháp:** Đã được xử lý trong nginx.conf với:
```nginx
add_header Access-Control-Allow-Origin * always;
```

### Lỗi 5: API trả về HTML thay vì JSON

**Nguyên nhân:** NGINX đang serve static file thay vì proxy

**Kiểm tra nginx.conf:**
```nginx
# Đảm bảo location /api/ đứng TRƯỚC location /
location /api/ {
    proxy_pass http://localhost:8080;
}

location / {
    try_files $uri $uri/ /index.html;
}
```

---

## 🎯 PHẦN 6: BÀI TẬP THỰC HÀNH

### Bài 1: Thêm Due Date cho TODO

**Yêu cầu:**
1. Thêm field `due_date` vào TODO struct (Go)
2. Thêm input date trong form
3. Hiển thị due date trong danh sách
4. Highlight TODO quá hạn (màu đỏ)

### Bài 2: Thêm Dark Mode

**Yêu cầu:**
1. Thêm toggle button dark/light mode
2. Lưu preference vào localStorage
3. Apply dark theme CSS

**Gợi ý CSS:**
```css
body.dark-mode {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
}

.dark-mode .todo-item {
    background: #1f2937;
    color: #f3f4f6;
}
```

### Bài 3: Thêm Search

**Yêu cầu:**
1. Thêm search box
2. Filter TODO theo title real-time
3. Highlight từ khóa tìm kiếm

### Bài 4: Export/Import JSON

**Yêu cầu:**
1. Button "Export" → download todos.json
2. Button "Import" → upload JSON file
3. Parse và bulk create TODOs

---

## ✅ PHẦN 7: CHECKLIST HOÀN THÀNH GIAI ĐOẠN 4

- [ ] NGINX đã cài đặt và chạy được
- [ ] Frontend files đã copy vào nginx directory
- [ ] Giao diện web hiển thị đúng
- [ ] Có thể thêm TODO qua giao diện
- [ ] Có thể đánh dấu hoàn thành
- [ ] Có thể chỉnh sửa TODO
- [ ] Có thể xóa TODO
- [ ] Filter hoạt động (All/Active/Completed)
- [ ] Stats hiển thị đúng
- [ ] Service status hiển thị đúng
- [ ] Responsive trên mobile
- [ ] Không có lỗi CORS
- [ ] Hiểu được vai trò của NGINX (web server + reverse proxy)
- [ ] Hiểu được luồng: Browser → NGINX → Python → Go

---

## 📚 PHẦN 8: TÀI LIỆU THAM KHẢO

### NGINX:
- Official docs: https://nginx.org/en/docs/
- Reverse proxy: https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/
- Configuration: https://www.nginx.com/resources/wiki/start/topics/examples/full/

### Frontend:
- Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- DOM Manipulation: https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model
- CSS Grid: https://css-tricks.com/snippets/css/complete-guide-grid/

---

## 🎊 KẾT LUẬN GIAI ĐOẠN 4

Chúc mừng! Bạn đã hoàn thành Giai đoạn 4 - TODO App với giao diện web hoàn chỉnh!

**Đã đạt được:**
✅ Giao diện web đẹp, responsive  
✅ NGINX làm web server + reverse proxy  
✅ Full CRUD operations qua UI  
✅ Real-time stats  
✅ Service health monitoring  
✅ Professional UX/UI  

**Vấn đề cần giải quyết tiếp:**
❌ Dữ liệu vẫn lưu RAM (mất khi restart)  
❌ Chưa containerize (Docker)  
❌ Deploy thủ công (chưa có CI/CD)  
❌ Chưa có monitoring

---

_(Copy nội dung từ file 5.md vào đây)_

---

_(Copy nội dung từ file 6.md vào đây)_

---

_(Copy nội dung từ file 7.md vào đây)_

---

_(Copy nội dung từ file 8.md vào đây)_

---

_(Copy nội dung từ file 9.md vào đây)_

---

_(Copy nội dung từ file 10.md vào đây)_

---

_(Copy nội dung từ file 11.md vào đây)_

---

_(Copy nội dung từ file 12.md vào đây)_

---

## 🎯 KẾT LUẬN

Sau khi hoàn thành toàn bộ 12 giai đoạn, bạn sẽ:

✅ Thành thạo xây dựng Microservices với Go và Python  
✅ Nắm vững Docker và Container Orchestration  
✅ Hiểu rõ CI/CD pipeline với GitLab  
✅ Biết deploy và scale trên AWS  
✅ Áp dụng được DevSecOps best practices  
✅ Sẵn sàng làm việc với hệ thống Production-ready

---

**Chúc bạn học tập hiệu quả! 🚀**