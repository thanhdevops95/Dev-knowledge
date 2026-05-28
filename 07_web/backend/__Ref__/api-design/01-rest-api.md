# 🏗️ Thiết kế API RESTful

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Nền tảng cho mọi Backend Developer

---

## REST là gì?

**REST (Representational State Transfer)** là một kiến trúc thiết kế API. API được gọi là "RESTful" khi tuân theo các nguyên tắc sau:

1. **Stateless** — Server không lưu state của client giữa các request
2. **Client-Server** — Frontend và backend tách biệt
3. **Uniform Interface** — URL nhất quán, dùng đúng HTTP methods
4. **Resource-based** — Mọi thứ đều là resource (`/users`, `/posts`)
5. **Cacheable** — Response có thể được cache

---

## URL Design

```
# ✅ Đúng
GET    /users              # Lấy danh sách users
GET    /users/123          # Lấy user cụ thể
POST   /users              # Tạo user mới
PUT    /users/123          # Cập nhật toàn bộ user
PATCH  /users/123          # Cập nhật một phần
DELETE /users/123          # Xóa user

# Nested resources (quan hệ có nghĩa)
GET    /users/123/posts          # Posts của user 123
POST   /users/123/posts          # Tạo post cho user 123
GET    /users/123/posts/456      # Post cụ thể của user

# ❌ Sai
GET    /getUsers                 # Verb trong URL
POST   /deleteUser               # Method không nhất quán
GET    /user/all                 # Không cần /all
```

---

## Request & Response

### Request Structure

```http
POST /api/v1/posts HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer eyJhbGc...
X-Request-ID: abc123

{
    "title": "My First Post",
    "content": "Hello World!",
    "tags": ["tech", "tutorial"],
    "status": "draft"
}
```

### Response Structure (Nhất quán)

```json
// ✅ Success Response
{
    "success": true,
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "My First Post",
        "status": "draft",
        "createdAt": "2026-02-19T13:00:00.000Z"
    },
    "meta": {
        "requestId": "abc123"
    }
}

// ✅ Error Response
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Dữ liệu không hợp lệ",
        "details": [
            { "field": "email", "message": "Email không đúng định dạng" },
            { "field": "age", "message": "Tuổi phải từ 18 trở lên" }
        ]
    },
    "meta": {
        "requestId": "abc123"
    }
}

// ✅ Paginated List Response
{
    "success": true,
    "data": [...],
    "pagination": {
        "page": 1,
        "limit": 20,
        "total": 150,
        "totalPages": 8,
        "hasNext": true,
        "hasPrev": false
    }
}
```

---

## Pagination

```
# Cursor-based (tốt nhất cho large datasets, realtime data)
GET /posts?cursor=eyJjcmVhdGVkQXQiOiIyMDI2In0&limit=20

# Offset-based (đơn giản, quen thuộc)
GET /posts?page=2&limit=20

# Keyset-based
GET /posts?after_id=550e8400&limit=20
```

---

## Filtering, Sorting, Search

```
# Filtering
GET /posts?status=published&authorId=123
GET /users?age[gte]=18&age[lte]=30
GET /products?price[gte]=100&category=electronics

# Sorting
GET /posts?sort=-createdAt          # Giảm dần
GET /posts?sort=title,-createdAt  # Nhiều field

# Field selection
GET /users?fields=id,name,email

# Search
GET /posts?q=machine+learning
GET /posts?search=machine learning

# Combining
GET /products?category=phone&price[gte]=500&sort=-rating&page=1&limit=20
```

---

## Versioning

```
# URL versioning (phổ biến nhất)
GET /api/v1/users
GET /api/v2/users

# Header versioning
GET /api/users
Accept: application/vnd.api+json; version=2

# Query param versioning
GET /api/users?version=2
```

---

## Authentication & Authorization

```http
# Bearer Token (JWT)
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# API Key (cho service-to-service)
X-API-Key: your-api-key
# hoặc
Authorization: ApiKey your-api-key

# Basic Auth (dùng cho internal tools)
Authorization: Basic base64(username:password)
```

---

## HTTP Status Codes đúng usage

```
200 OK              → GET, PUT, PATCH thành công
201 Created         → POST tạo resource mới thành công (kèm Location header)
204 No Content      → DELETE thành công, hoặc PUT/PATCH không trả data
400 Bad Request     → Dữ liệu sai cú pháp hoặc thiếu field bắt buộc
401 Unauthorized    → Chưa đăng nhập / token hết hạn
403 Forbidden       → Đã đăng nhập nhưng không có quyền
404 Not Found       → Resource không tồn tại
409 Conflict        → Trùng lặp (ví dụ: email đã tồn tại)
422 Unprocessable   → Cú pháp đúng nhưng logic sai (validation error)
429 Too Many Req    → Rate limit
500 Internal Error  → Lỗi server (nên log và ẩn chi tiết)
503 Unavailable     → Server đang bảo trì
```

---

## Rate Limiting

```http
# Response headers thông báo rate limit
X-Rate-Limit-Limit: 100
X-Rate-Limit-Remaining: 47
X-Rate-Limit-Reset: 1708344000

# Khi bị rate limit
HTTP/1.1 429 Too Many Requests
Retry-After: 60
{
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Quá nhiều request. Vui lòng thử lại sau 60 giây"
    }
}
```

---

## Idempotency

```
# Dùng Idempotency-Key để đảm bảo không duplicate (payment, order)
POST /payments
Idempotency-Key: a54c1670-f7e5-4b3a-9b2e-abc123def456

{
    "amount": 99.99,
    "currency": "USD"
}
# Gọi lại với cùng key → trả về kết quả cũ, không charge 2 lần
```

---

## OpenAPI / Swagger

```yaml
# openapi.yaml
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0

paths:
  /users:
    get:
      summary: Lấy danh sách users
      tags: [Users]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Thành công
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
    
    post:
      summary: Tạo user mới
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: Tạo thành công

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        email:
          type: string
          format: email
      required: [id, name, email]
    
    CreateUserRequest:
      type: object
      properties:
        name:
          type: string
          minLength: 2
          maxLength: 100
        email:
          type: string
          format: email
      required: [name, email]
  
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - BearerAuth: []
```

---

## Checklist thiết kế API

- [ ] URL dùng danh từ số nhiều (`/users`, không phải `/user`)
- [ ] Dùng đúng HTTP methods
- [ ] Response format nhất quán (success + error)
- [ ] Status codes đúng ngữ nghĩa
- [ ] Có versioning ngay từ đầu
- [ ] Implement pagination cho list endpoints
- [ ] Có filtering, sorting, field selection
- [ ] Rate limiting
- [ ] Authentication & Authorization rõ ràng
- [ ] Có OpenAPI documentation
- [ ] HTTPS bắt buộc
- [ ] Validate input kỹ lưỡng
- [ ] Không expose stack trace trong production

---

## Tài nguyên thêm

- [REST API Design Best Practices](https://www.freecodecamp.org/news/rest-api-best-practices-rest-endpoint-design-examples/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger Editor](https://editor.swagger.io/) — Viết API spec online
- [HTTP API Design Guide](https://github.com/interagent/http-api-design)
