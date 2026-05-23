# 🔄 API nâng cao — Design & Patterns

> `[INTERMEDIATE → ADVANCED]` — Thiết kế API production-grade

---

## 1. API Versioning

```
Strategies:
1. URL Path:     /api/v1/users, /api/v2/users     ← Phổ biến nhất
2. Header:       Accept: application/vnd.api.v2+json
3. Query param:  /api/users?version=2

Ví dụ v1 → v2 migration:
v1: GET /api/v1/users → { "name": "An Ng" }
v2: GET /api/v2/users → { "firstName": "An", "lastName": "Ng" }

// Cả 2 chạy song song → clients migrate dần → sunset v1
```

---

## 2. Pagination — 3 cách

### Offset-based (đơn giản, phổ biến)

```
GET /api/posts?page=3&limit=20

Response:
{
    "data": [...],
    "meta": {
        "page": 3,
        "limit": 20,
        "total": 1500,
        "totalPages": 75
    }
}

SQL: SELECT * FROM posts ORDER BY id LIMIT 20 OFFSET 40;
❌ Vấn đề: OFFSET 10000 → scan 10000 rows → chậm!
```

### Cursor-based (hiệu năng tốt) ⭐

```
GET /api/posts?cursor=eyJpZCI6MTAwfQ&limit=20

Response:
{
    "data": [...],
    "meta": {
        "nextCursor": "eyJpZCI6MTIwfQ",
        "hasMore": true
    }
}

SQL: SELECT * FROM posts WHERE id > 100 ORDER BY id LIMIT 20;
✅ Luôn nhanh, dùng index
✅ Real-time safe (không bị trùng/mất khi data thay đổi)
```

```javascript
// Cursor implementation
function encodeCursor(id) {
    return Buffer.from(JSON.stringify({ id })).toString('base64');
}

function decodeCursor(cursor) {
    return JSON.parse(Buffer.from(cursor, 'base64').toString());
}

app.get('/api/posts', async (req, res) => {
    const { cursor, limit = 20 } = req.query;
    const where = cursor ? { id: { $gt: decodeCursor(cursor).id } } : {};

    const posts = await Post.find(where).sort({ id: 1 }).limit(Number(limit) + 1);
    const hasMore = posts.length > limit;
    if (hasMore) posts.pop();

    res.json({
        data: posts,
        meta: {
            nextCursor: hasMore ? encodeCursor(posts[posts.length - 1].id) : null,
            hasMore,
        },
    });
});
```

---

## 3. Error Handling — Standard Format

```javascript
// RFC 7807 Problem Details
app.use((err, req, res, next) => {
    const status = err.status || 500;

    res.status(status).json({
        type: `https://api.example.com/errors/${err.code || 'internal'}`,
        title: err.title || 'Internal Server Error',
        status,
        detail: err.message,
        instance: req.originalUrl,
        timestamp: new Date().toISOString(),
        requestId: req.id,
        ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
    });
});

// Custom error classes
class AppError extends Error {
    constructor(message, status, code) {
        super(message);
        this.status = status;
        this.code = code;
    }
}

class NotFoundError extends AppError {
    constructor(resource, id) {
        super(`${resource} with id ${id} not found`, 404, 'NOT_FOUND');
    }
}

class ValidationError extends AppError {
    constructor(errors) {
        super('Validation failed', 400, 'VALIDATION_ERROR');
        this.errors = errors;
    }
}

// Sử dụng
app.get('/api/users/:id', async (req, res) => {
    const user = await User.findById(req.params.id);
    if (!user) throw new NotFoundError('User', req.params.id);
    res.json({ data: user });
});
```

---

## 4. Input Validation — Zod

```javascript
import { z } from 'zod';

const createUserSchema = z.object({
    name: z.string().min(2).max(100),
    email: z.string().email(),
    age: z.number().int().min(0).max(150).optional(),
    role: z.enum(['user', 'admin']).default('user'),
    address: z.object({
        city: z.string(),
        country: z.string().length(2),
    }).optional(),
    tags: z.array(z.string()).max(10).default([]),
});

// Middleware
function validate(schema) {
    return (req, res, next) => {
        try {
            req.body = schema.parse(req.body);
            next();
        } catch (err) {
            res.status(400).json({
                error: 'Validation Error',
                details: err.errors.map(e => ({
                    field: e.path.join('.'),
                    message: e.message,
                })),
            });
        }
    };
}

app.post('/api/users', validate(createUserSchema), createUser);
```

---

## 5. Rate Limiting — Nhiều tầng

```javascript
import rateLimit from 'express-rate-limit';

// Global: 1000 req/15 phút
app.use(rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 1000,
    standardHeaders: true,
    legacyHeaders: false,
}));

// Login: 5 req/15 phút (strict)
app.use('/api/auth/login', rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 5,
    message: { error: 'Too many login attempts. Try again in 15 minutes.' },
}));

// API key-based: per user
app.use('/api', rateLimit({
    windowMs: 60 * 1000,  // 1 phút
    max: 100,
    keyGenerator: (req) => req.user?.id || req.ip,
}));
```

---

## 6. Idempotency — An toàn khi retry

```
Idempotent: Gọi N lần = kết quả giống nhau

GET  /users/123      → Idempotent ✅ (luôn trả cùng user)
PUT  /users/123      → Idempotent ✅ (set cùng data)
DELETE /users/123    → Idempotent ✅ (đã xóa rồi thì vẫn xóa)
POST /users          → NOT Idempotent ❌ (tạo nhiều users!)
```

```javascript
// Idempotency key cho POST
app.post('/api/payments', async (req, res) => {
    const idempotencyKey = req.headers['idempotency-key'];
    if (!idempotencyKey) {
        return res.status(400).json({ error: 'Idempotency-Key header required' });
    }

    // Check đã xử lý chưa
    const existing = await cache.get(`idem:${idempotencyKey}`);
    if (existing) {
        return res.status(200).json(JSON.parse(existing));
    }

    // Xử lý payment
    const result = await processPayment(req.body);

    // Lưu kết quả 24h
    await cache.set(`idem:${idempotencyKey}`, JSON.stringify(result), 'EX', 86400);
    res.status(201).json(result);
});
```

---

## 7. API Documentation — OpenAPI

```yaml
# openapi.yaml
openapi: 3.0.3
info:
  title: My API
  version: 1.0.0

paths:
  /api/users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema: { type: integer, default: 1 }
        - name: limit
          in: query
          schema: { type: integer, default: 20, maximum: 100 }
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items: { $ref: '#/components/schemas/User' }
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/CreateUser' }
      responses:
        '201': { description: Created }
        '400': { description: Validation Error }

components:
  schemas:
    User:
      type: object
      properties:
        id: { type: integer }
        name: { type: string }
        email: { type: string, format: email }
```

---

## 8. API Response Conventions

```javascript
// Consistent response format
// Success
{
    "data": { ... },
    "meta": { "page": 1, "total": 100 }
}

// Error
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Email is required",
        "details": [{ "field": "email", "message": "Required" }]
    }
}

// Empty
{
    "data": [],
    "meta": { "total": 0 }
}
```

---

## Các lỗi thường gặp

```
❌ Sai: POST /api/getUsers → verb trong URL
✅ Đúng: GET /api/users → URL = noun, HTTP method = verb

❌ Sai: Trả 200 cho mọi response (lỗi trong body)
✅ Đúng: Dùng đúng status codes: 201, 400, 401, 403, 404, 409, 500

❌ Sai: API không có rate limiting → DDoS/abuse
✅ Đúng: Rate limit mọi endpoint, strict hơn cho auth endpoints
```

---

## Bài tập thực hành

- [ ] Implement cursor-based pagination cho posts API
- [ ] Tạo error handling middleware với custom error classes
- [ ] Thêm Zod validation cho tất cả endpoints
- [ ] Viết OpenAPI spec → generate Swagger UI

---

## Tài nguyên thêm

- [REST API Tutorial](https://restfulapi.net/) — Comprehensive
- [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/) — Enterprise-grade
- [HTTPie](https://httpie.io/) — Modern HTTP client
