# 🌐 REST API — Thiết kế API chuẩn

> `[BEGINNER → INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Giao thức giao tiếp phổ biến nhất giữa client và server

---

## Tại sao cần học REST?

**REST** (Representational State Transfer) là kiến trúc API được **90%+ web services** sử dụng. Mọi app bạn dùng (Facebook, GitHub, Spotify) đều giao tiếp qua REST API.

---

## 1. HTTP Methods — Ngữ nghĩa rõ ràng

| Method | Mục đích | Idempotent? | Safe? | Ví dụ |
|---|---|---|---|---|
| **GET** | Đọc dữ liệu | ✅ | ✅ | Lấy danh sách users |
| **POST** | Tạo mới | ❌ | ❌ | Tạo user mới |
| **PUT** | Cập nhật toàn bộ | ✅ | ❌ | Thay thế user |
| **PATCH** | Cập nhật 1 phần | ✅ | ❌ | Sửa email user |
| **DELETE** | Xóa | ✅ | ❌ | Xóa user |

> **Idempotent:** Gọi 1 lần hay 100 lần → kết quả giống nhau  
> **Safe:** Không thay đổi dữ liệu trên server

---

## 2. URL Design — Naming Convention

```bash
# ✅ ĐÚNG: Danh từ số nhiều, lowercase, dùng kebab-case
GET    /api/v1/users              # Danh sách users
GET    /api/v1/users/123          # User cụ thể
POST   /api/v1/users              # Tạo user
PUT    /api/v1/users/123          # Cập nhật user 123
DELETE /api/v1/users/123          # Xóa user 123

GET    /api/v1/users/123/orders   # Orders của user 123
GET    /api/v1/users/123/orders/456  # Order cụ thể

# Filtering, Sorting, Pagination qua query params
GET /api/v1/users?status=active&sort=name&page=2&limit=20

# ❌ SAI — Tránh những lỗi sau:
GET /api/getUsers              # Dùng động từ
GET /api/v1/user               # Số ít
GET /api/v1/Users              # PascalCase
GET /api/v1/users/123/delete   # Động từ trong URL
POST /api/v1/users/create      # Thừa — POST đã ngầm "create"
```

---

## 3. Status Codes — Trả về đúng mã

```
2xx — Thành công
┌─────┬──────────────────────────────────┐
│ 200 │ OK — Request thành công          │
│ 201 │ Created — Tạo resource mới       │
│ 204 │ No Content — Xóa thành công      │
└─────┴──────────────────────────────────┘

4xx — Lỗi do client
┌─────┬──────────────────────────────────┐
│ 400 │ Bad Request — Dữ liệu không hợp lệ │
│ 401 │ Unauthorized — Chưa đăng nhập    │
│ 403 │ Forbidden — Không có quyền       │
│ 404 │ Not Found — Resource không tồn tại│
│ 409 │ Conflict — Xung đột (email trùng) │
│ 422 │ Unprocessable — Validation failed │
│ 429 │ Too Many Requests — Rate limited  │
└─────┴──────────────────────────────────┘

5xx — Lỗi do server
┌─────┬──────────────────────────────────┐
│ 500 │ Internal Server Error            │
│ 502 │ Bad Gateway — Upstream lỗi       │
│ 503 │ Service Unavailable — Server quá tải │
│ 504 │ Gateway Timeout                  │
└─────┴──────────────────────────────────┘
```

---

## 4. Request & Response Format

### Request

```http
POST /api/v1/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOi...

{
  "name": "Nguyễn Văn An",
  "email": "an@example.com",
  "role": "admin"
}
```

### Response — Cấu trúc chuẩn

```json
// Thành công
{
  "status": "success",
  "data": {
    "id": 123,
    "name": "Nguyễn Văn An",
    "email": "an@example.com",
    "created_at": "2026-03-03T10:00:00Z"
  }
}

// Lỗi
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email không hợp lệ",
    "details": [
      { "field": "email", "message": "Định dạng email sai" }
    ]
  }
}

// Danh sách + Pagination
{
  "status": "success",
  "data": [...],
  "meta": {
    "page": 2,
    "limit": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

---

## 5. Versioning — Quản lý phiên bản

```bash
# Cách 1: URL versioning (phổ biến nhất)
GET /api/v1/users
GET /api/v2/users

# Cách 2: Header versioning
GET /api/users
Accept: application/vnd.example.v2+json

# Cách 3: Query parameter
GET /api/users?version=2
```

---

## 6. Authentication — Xác thực

### Bearer Token (JWT)

```
Client → POST /api/auth/login { email, password }
Server → { token: "eyJhbGciOi..." }

Client → GET /api/users
          Authorization: Bearer eyJhbGciOi...
Server → { data: [...] }
```

### API Key

```
GET /api/data?api_key=sk_live_abc123
# hoặc
GET /api/data
X-API-Key: sk_live_abc123
```

---

## 7. Pagination — Phân trang

```bash
# Offset-based (đơn giản, phổ biến)
GET /api/users?page=3&limit=20
# Vấn đề: Nếu thêm/xóa item → page bị lệch

# Cursor-based (tốt cho infinite scroll)
GET /api/users?cursor=abc123&limit=20
# Response: { data: [...], next_cursor: "def456" }
```

---

## 8. Rate Limiting — Giới hạn request

```
Response headers:
X-RateLimit-Limit: 100        # Max 100 requests
X-RateLimit-Remaining: 45     # Còn 45 requests
X-RateLimit-Reset: 1614556800 # Reset lúc nào (UNIX timestamp)

Khi vượt limit:
HTTP 429 Too Many Requests
Retry-After: 60               # Thử lại sau 60 giây
```

---

## 9. HATEOAS — Self-describing API

```json
{
  "data": {
    "id": 123,
    "name": "Nguyễn Văn An",
    "links": {
      "self": "/api/users/123",
      "orders": "/api/users/123/orders",
      "avatar": "/api/users/123/avatar"
    }
  }
}
```

---

## Ví dụ thực tế — Express.js

```javascript
const express = require('express');
const app = express();
app.use(express.json());

let users = [];
let nextId = 1;

// GET /api/users — Danh sách
app.get('/api/users', (req, res) => {
    const { page = 1, limit = 20, status } = req.query;
    let result = users;
    if (status) result = result.filter(u => u.status === status);

    const start = (page - 1) * limit;
    const paginated = result.slice(start, start + Number(limit));

    res.json({
        status: 'success',
        data: paginated,
        meta: { page: Number(page), limit: Number(limit), total: result.length }
    });
});

// POST /api/users — Tạo mới
app.post('/api/users', (req, res) => {
    const { name, email } = req.body;
    if (!name || !email) {
        return res.status(400).json({
            status: 'error',
            error: { message: 'name và email bắt buộc' }
        });
    }
    const user = { id: nextId++, name, email, created_at: new Date() };
    users.push(user);
    res.status(201).json({ status: 'success', data: user });
});

// DELETE /api/users/:id — Xóa
app.delete('/api/users/:id', (req, res) => {
    const idx = users.findIndex(u => u.id === Number(req.params.id));
    if (idx === -1) {
        return res.status(404).json({
            status: 'error',
            error: { message: 'User không tồn tại' }
        });
    }
    users.splice(idx, 1);
    res.status(204).send();
});

app.listen(3000);
```

---

## Các lỗi thường gặp

```
❌ Sai: POST /api/users/delete/123
✅ Đúng: DELETE /api/users/123

❌ Sai: Trả 200 cho mọi thứ kể cả lỗi
✅ Đúng: Dùng đúng status code (400, 401, 404, 500...)

❌ Sai: Trả về toàn bộ user kèm password hash
✅ Đúng: Chỉ trả fields cần thiết, KHÔNG BAO GIỜ trả password

❌ Sai: GET /api/users → trả 10,000 users
✅ Đúng: Pagination bắt buộc cho list endpoints
```

---

## Bài tập thực hành

- [ ] Thiết kế REST API cho todo app: CRUD tasks + filter by status
- [ ] Implement API với Express.js / FastAPI — có validation + error handling
- [ ] Thêm pagination (offset + cursor) cho list endpoint
- [ ] Dùng Postman/Insomnia test tất cả endpoints

---

## Tài nguyên thêm

- [RESTful API Design Best Practices](https://restfulapi.net/) — Tổng hợp chuẩn
- [HTTP Status Codes](https://httpstatuses.com/) — Mọi status code
- [JSON:API Specification](https://jsonapi.org/) — Spec chuẩn cho JSON response
