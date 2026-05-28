# GIAI ĐOẠN 1: SETUP MÔI TRƯỜNG & KIẾN THỨC NỀN TẢNG

## 📌 MỤC TIÊU GIAI ĐOẠN 1
Sau khi hoàn thành giai đoạn này, bạn sẽ:

✅ Cài đặt đầy đủ các công cụ cần thiết
✅ Hiểu được kiến trúc Microservices cơ bản
✅ Nắm rõ cách HTTP hoạt động
✅ Biết cách test API với curl và Postman
✅ Sẵn sàng cho các giai đoạn tiếp theo


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

**Bước :** Kiểm tra

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
bashcurl --version
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

Thiết kế RESTful API cho TODO App:
|Hành động | Method | Endpoint | Body | Response |
|----|---------|-------|
|Lấy tất cả TODOGET/api/todos-[{...}, {...}] |
|Lấy 1 TODOGET/api/todos/:id-{id, title, ...} |
|Tạo TODOPOST/api/todos{title}{id, title, ...} |
|Cập nhật TODOPUT/api/todos/:id{title, completed}{id, title, ...} |
|Xóa TODODELETE/api/todos/:id-204 No Content |

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
Quy tắc:

- Key phải trong dấu ngoặc kép "key"
- Giá trị string cũng dùng ngoặc kép
- Không có dấu phẩy sau phần tử cuối cùng
- Hỗ trợ: string, number, boolean, null, array, object

Ví dụ TODO dạng JSON:
json{
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
Giải pháp:
Windows:
bash# Tìm process đang dùng port 8080
netstat -ano | findstr :8080

# Kill process (PID là số ở cột cuối)
taskkill /PID [số_PID] /F
Linux/Mac:
bash# Tìm process
lsof -i :8080

# Kill process
kill -9 [PID]
```

### Lỗi 4: curl SSL certificate error
```
curl: (60) SSL certificate problem: certificate verify failed
Giải pháp tạm thời (chỉ dùng cho test):
bashcurl -k https://api.example.com
# -k: insecure, bỏ qua verify SSL
Giải pháp lâu dài: Cài đặt CA certificates

📖 TÀI LIỆU THAM KHẢO
Tài liệu chính thức:

Python: https://docs.python.org/3/
Go: https://go.dev/doc/
HTTP: https://developer.mozilla.org/en-US/docs/Web/HTTP
REST API: https://restfulapi.net/

Công cụ online:

JSON Formatter: https://jsonformatter.org/
HTTP Status Codes: https://httpstatuses.com/
Postman Learning: https://learning.postman.com/

Video tiếng Việt (khuyến nghị):

Python cơ bản: [tìm trên YouTube]
Go tutorial: [tìm trên YouTube]
HTTP & REST API: [tìm trên YouTube]


🎊 KẾT LUẬN GIAI ĐOẠN 1
Chúc mừng! Bạn đã hoàn thành Giai đoạn 1. Bây giờ bạn đã:
✅ Có đầy đủ công cụ để bắt đầu code
✅ Hiểu được cách HTTP hoạt động
✅ Biết thiết kế REST API
✅ Thành thạo curl và Postman
✅ Nắm được kiến trúc Microservices cơ bản