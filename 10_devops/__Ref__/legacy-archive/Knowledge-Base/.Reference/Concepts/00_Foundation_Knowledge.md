# 📚 KIẾN THỨC NỀN TẢNG - FOUNDATION KNOWLEDGE

## 📌 MỤC ĐÍCH FILE NÀY
Trước khi bắt đầu Giai đoạn 1, bạn cần hiểu một số khái niệm cơ bản về mạng máy tính, HTTP, và kiến trúc phần mềm. File này giải thích những khái niệm đó một cách dễ hiểu nhất.

---

## 🌐 PHẦN 1: HTTP PROTOCOL - GIAO THỨC NỀN TẢNG CỦA WEB

### 1.1. HTTP là gì?

**HTTP** (HyperText Transfer Protocol) là "ngôn ngữ" mà trình duyệt và server dùng để nói chuyện với nhau.

**Ví dụ thực tế:**
- Bạn gõ `facebook.com` vào trình duyệt
- Trình duyệt gửi **HTTP Request** đến server Facebook: "Cho tôi trang chủ"
- Server Facebook trả về **HTTP Response**: "Đây, file HTML của trang chủ"
- Trình duyệt hiển thị trang web

### 1.2. Cấu trúc HTTP Request

Một HTTP Request gồm 3 phần chính:

```
GET /api/todos HTTP/1.1              ← REQUEST LINE
Host: localhost:8080                 ← HEADERS
Content-Type: application/json
Authorization: Bearer abc123

{"title": "Học Docker"}              ← BODY (không phải lúc nào cũng có)
```

#### **1. Request Line**
- **Method** (GET, POST, PUT, DELETE): Bạn muốn làm gì?
- **Path** (/api/todos): Tài nguyên nào?
- **Version** (HTTP/1.1): Phiên bản giao thức

#### **2. Headers**
Thông tin bổ sung:
- `Host`: Server đích
- `Content-Type`: Loại dữ liệu (JSON, XML, HTML...)
- `Authorization`: Token xác thực
- `User-Agent`: Trình duyệt/App gì đang gọi

#### **3. Body**
Dữ liệu gửi lên (chỉ có với POST, PUT, PATCH).

### 1.3. HTTP Methods (Động từ)

| Method | Ý nghĩa | Ví dụ thực tế |
|--------|---------|---------------|
| **GET** | Lấy dữ liệu | Xem danh sách bài viết |
| **POST** | Tạo mới | Đăng bài viết mới |
| **PUT** | Cập nhật toàn bộ | Sửa toàn bộ thông tin bài viết |
| **PATCH** | Cập nhật một phần | Chỉ sửa tiêu đề bài viết |
| **DELETE** | Xóa | Xóa bài viết |

**Quy tắc vàng:**
- GET: Không có Body, chỉ lấy dữ liệu (an toàn, có thể cache)
- POST: Có Body, tạo mới (không an toàn, không cache)
- PUT/PATCH: Có Body, cập nhật
- DELETE: Không có Body, xóa

### 1.4. HTTP Response (Phản hồi)

```
HTTP/1.1 200 OK                      ← STATUS LINE
Content-Type: application/json
Content-Length: 156

{                                    ← BODY
  "id": "1",
  "title": "Học Docker",
  "completed": false
}
```

### 1.5. HTTP Status Codes (Mã trạng thái)

Mã 3 chữ số cho biết kết quả request:

#### **2xx - Thành công ✅**
- **200 OK**: Thành công, có dữ liệu trả về
- **201 Created**: Tạo mới thành công
- **204 No Content**: Thành công, không có dữ liệu (thường dùng cho DELETE)

#### **4xx - Lỗi từ Client ❌**
- **400 Bad Request**: Dữ liệu gửi lên sai format
- **401 Unauthorized**: Chưa đăng nhập
- **403 Forbidden**: Đã đăng nhập nhưng không có quyền
- **404 Not Found**: Không tìm thấy tài nguyên

#### **5xx - Lỗi từ Server 💥**
- **500 Internal Server Error**: Lỗi code backend
- **502 Bad Gateway**: Gateway/Proxy không kết nối được backend
- **503 Service Unavailable**: Server quá tải hoặc đang bảo trì

---

## 🏗️ PHẦN 2: REST API - CHUẨN THIẾT KẾ API

### 2.1. REST là gì?

**REST** (Representational State Transfer) là một phong cách thiết kế API. API theo chuẩn REST gọi là **RESTful API**.

### 2.2. Nguyên tắc REST

#### **1. Resource-based (Dựa trên tài nguyên)**
Mọi thứ đều là "tài nguyên" (Resource) và có URL riêng.

```
/users              ← Tài nguyên "users" (danh từ số nhiều)
/users/123          ← User cụ thể với ID = 123
/users/123/posts    ← Các bài viết của user 123
```

**Sai:** `/getUsers`, `/createUser` (dùng động từ)
**Đúng:** `GET /users`, `POST /users` (dùng HTTP Method làm động từ)

#### **2. Sử dụng đúng HTTP Methods**

| Hành động | Method | URL | Body | Response |
|-----------|--------|-----|------|----------|
| Lấy tất cả | GET | `/todos` | - | `[{...}, {...}]` |
| Lấy 1 cái | GET | `/todos/123` | - | `{id: 123, ...}` |
| Tạo mới | POST | `/todos` | `{title: "..."}` | `{id: 456, ...}` |
| Cập nhật | PUT | `/todos/123` | `{title: "...", completed: true}` | `{id: 123, ...}` |
| Xóa | DELETE | `/todos/123` | - | `204 No Content` |

#### **3. Stateless (Không lưu trạng thái)**
Mỗi request phải độc lập, chứa đầy đủ thông tin cần thiết.

**Sai:**
```
Request 1: POST /login {username, password}
Request 2: GET /profile  ← Server nhớ user đã login ở Request 1
```

**Đúng:**
```
Request 1: POST /login {username, password} → Trả về Token
Request 2: GET /profile 
           Header: Authorization: Bearer <token>  ← Mỗi request tự mang token
```

#### **4. Trả về JSON**
Dữ liệu trả về nên là JSON (dễ đọc, dễ parse).

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Học Docker từ cơ bản",
  "completed": false,
  "created_at": "2026-01-25T10:30:00+07:00"
}
```

### 2.3. Ví dụ thiết kế RESTful API cho TODO App

```
GET    /api/todos           → Lấy tất cả TODO
GET    /api/todos/:id       → Lấy 1 TODO
POST   /api/todos           → Tạo TODO mới
PUT    /api/todos/:id       → Cập nhật TODO
DELETE /api/todos/:id       → Xóa TODO
```

---

## 📦 PHẦN 3: JSON - ĐỊNH DẠNG DỮ LIỆU

### 3.1. JSON là gì?

**JSON** (JavaScript Object Notation) là định dạng văn bản để trao đổi dữ liệu.

### 3.2. Cú pháp JSON

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
- Key phải trong dấu ngoặc kép `"key"`
- String cũng dùng ngoặc kép `"value"`
- Không có dấu phẩy sau phần tử cuối cùng
- Hỗ trợ: string, number, boolean, null, array, object

### 3.3. Ví dụ TODO dạng JSON

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Học Docker từ cơ bản đến nâng cao",
  "completed": false,
  "created_at": "2026-01-25T14:30:00+07:00",
  "tags": ["docker", "devops", "container"],
  "priority": {
    "level": "high",
    "score": 9
  }
}
```

---

## 🏛️ PHẦN 4: KIẾN TRÚC PHẦN MỀM

### 4.1. Monolith vs Microservices

#### **Monolith (Nguyên khối)**
Tất cả tính năng trong 1 ứng dụng lớn.

```
┌─────────────────────────────┐
│   TODO App (1 cục to)       │
│                             │
│  - UI (Giao diện)           │
│  - Business Logic           │
│  - Database Access          │
│  - Authentication           │
│  - Notification             │
└─────────────────────────────┘
```

**Ưu điểm:**
- Đơn giản, dễ phát triển ban đầu
- Deploy một lần là xong

**Nhược điểm:**
- Khó scale (phải scale cả cục)
- Một chỗ lỗi → Cả hệ thống chết
- Team lớn làm chung code → Xung đột

#### **Microservices (Vi dịch vụ)**
Chia nhỏ thành nhiều service độc lập.

```
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Frontend │──▶│ TODO API │──▶│ Database │
│ Service  │   │ Service  │   │ Service  │
└──────────┘   └──────────┘   └──────────┘
                     │
                     ▼
               ┌──────────┐
               │   Auth   │
               │ Service  │
               └──────────┘
```

**Ưu điểm:**
- Mỗi service scale độc lập
- Team khác nhau phát triển song song
- Dễ thay đổi công nghệ (Service A dùng Python, Service B dùng Go)

**Nhược điểm:**
- Phức tạp hơn (cần quản lý nhiều service)
- Network latency (gọi qua mạng chậm hơn gọi trong process)

### 4.2. Kiến trúc TODO App trong khóa học này

```
┌─────────────────┐
│   NGƯỜI DÙNG    │
└────────┬────────┘
         │ HTTP
┌────────▼────────┐
│   NGINX :80     │  ← Web Server + Reverse Proxy
└────────┬────────┘
         │
┌────────▼────────┐
│ Python :8080    │  ← API Gateway (Điều phối)
└────────┬────────┘
         │
┌────────▼────────┐
│   Go :8081      │  ← Backend (Xử lý logic)
└────────┬────────┘
         │
┌────────▼────────┐
│  MySQL :3306    │  ← Database (Lưu trữ)
└─────────────────┘
```

**Luồng hoạt động:**
1. User mở browser → `http://localhost`
2. NGINX phục vụ HTML/CSS/JS
3. JS gọi API → `http://localhost/api/todos`
4. NGINX forward → Python (port 8080)
5. Python xử lý và gọi → Go (port 8081)
6. Go truy vấn → MySQL
7. Kết quả trả ngược: MySQL → Go → Python → NGINX → User

---

## 🔌 PHẦN 5: NETWORK BASICS

### 5.1. IP Address & Port

**IP Address:** Địa chỉ của máy tính trong mạng.
- `127.0.0.1` hoặc `localhost`: Chính máy bạn
- `192.168.1.100`: Máy khác trong mạng LAN
- `8.8.8.8`: Máy ở Internet (Google DNS)

**Port:** "Cổng" của ứng dụng trên máy.
- Một máy có 65535 port (0-65535)
- Port 80: HTTP
- Port 443: HTTPS
- Port 3306: MySQL
- Port 8080, 8081: Thường dùng cho app tự viết

**Ví dụ:**
- `http://localhost:8080` = Máy bạn, port 8080
- `http://192.168.1.100:5000` = Máy khác trong LAN, port 5000

### 5.2. DNS (Domain Name System)

Chuyển đổi tên miền → IP.

```
facebook.com → 157.240.2.35
```

Trong Docker/Kubernetes, container có DNS riêng:
```
Container tên "go-app" → Có thể gọi bằng http://go-app:8081
```

---

## 🎯 TỔNG KẾT

Sau khi đọc file này, bạn đã hiểu:
- ✅ HTTP Request/Response hoạt động như thế nào
- ✅ REST API thiết kế ra sao
- ✅ JSON là gì
- ✅ Sự khác biệt Monolith vs Microservices
- ✅ IP, Port, DNS cơ bản

👉 **Bước tiếp theo:** Vào `Stage01_Setup.md` để cài đặt công cụ và bắt đầu code!
