# 🛡️ API Security — Bảo mật API Production

> `[INTERMEDIATE → ADVANCED]` — Chống các cuộc tấn công phổ biến nhất

---

## Tại sao API Security quan trọng?

APIs là **cửa ngõ duy nhất** vào logic và data của bạn. Mọi cuộc tấn công đều nhắm vào API. OWASP API Security Top 10 (2023) cho thấy các lỗi phổ biến nhất đều... rất đơn giản và **hoàn toàn phòng tránh được**.

---

## 1. Authentication — "Bạn là ai?"

### JWT Best Practices

```typescript
import jwt from 'jsonwebtoken';

// ✅ Short-lived access token + long-lived refresh token
function generateTokenPair(user) {
    const accessToken = jwt.sign(
        { userId: user.id, role: user.role },
        process.env.JWT_SECRET,
        { expiresIn: '15m' },  // Ngắn! Nếu bị steal → chỉ valid 15 phút
    );

    const refreshToken = jwt.sign(
        { userId: user.id, tokenVersion: user.tokenVersion },
        process.env.REFRESH_SECRET,
        { expiresIn: '7d' },
    );

    return { accessToken, refreshToken };
}

// Middleware: verify access token
function authenticate(req, res, next) {
    const authHeader = req.headers.authorization;
    if (!authHeader?.startsWith('Bearer ')) {
        return res.status(401).json({ error: 'Missing token' });
    }

    try {
        const token = authHeader.split(' ')[1];
        const payload = jwt.verify(token, process.env.JWT_SECRET);
        req.user = payload;
        next();
    } catch (err) {
        if (err.name === 'TokenExpiredError') {
            return res.status(401).json({ error: 'Token expired', code: 'TOKEN_EXPIRED' });
        }
        return res.status(401).json({ error: 'Invalid token' });
    }
}
```

### Token Storage

```
❌ localStorage: XSS attack → đọc được token
❌ sessionStorage: Cũng XSS vulnerable

✅ httpOnly cookie (cho web apps):
   Browser tự gửi, JS KHÔNG đọc được → immune to XSS
   + SameSite=Strict: chống CSRF
   + Secure: chỉ gửi qua HTTPS

✅ Memory (cho SPA):
   Lưu trong variable/state → mất khi refresh
   Dùng refresh token (httpOnly cookie) để lấy lại
```

---

## 2. Authorization — "Bạn được quyền gì?"

Lỗi phổ biến nhất theo OWASP: **Broken Object Level Authorization (BOLA)** — user access resource của user khác.

```typescript
// ❌ BOLA vulnerability: KHÔNG check ownership
app.get('/api/orders/:id', authenticate, async (req, res) => {
    const order = await db.orders.findById(req.params.id);
    res.json(order);
    // User A xem order của User B bằng cách đổi ID! 😱
});

// ✅ Check ownership
app.get('/api/orders/:id', authenticate, async (req, res) => {
    const order = await db.orders.findById(req.params.id);
    if (!order) return res.status(404).json({ error: 'Not found' });

    // KIỂM TRA: order này thuộc về user đang logged in?
    if (order.userId !== req.user.userId && req.user.role !== 'admin') {
        return res.status(403).json({ error: 'Forbidden' });
    }

    res.json(order);
});

// ✅ Better: query trực tiếp với user filter
app.get('/api/orders/:id', authenticate, async (req, res) => {
    const order = await db.orders.findOne({
        id: req.params.id,
        userId: req.user.userId,  // Chỉ tìm order CỦA user này
    });
    if (!order) return res.status(404).json({ error: 'Not found' });
    res.json(order);
});
```

---

## 3. Input Validation — Không tin bất kỳ input nào

```typescript
import { z } from 'zod';

// Zod schema: define CHÍNH XÁC shape của input
const CreateUserSchema = z.object({
    name: z.string()
        .min(2, 'Tên ít nhất 2 ký tự')
        .max(100, 'Tên tối đa 100 ký tự')
        .trim(),
    email: z.string()
        .email('Email không hợp lệ')
        .toLowerCase(),
    age: z.number()
        .int()
        .min(13, 'Phải từ 13 tuổi')
        .max(150)
        .optional(),
    role: z.enum(['user', 'editor']),  // KHÔNG cho phép 'admin'!
});

// Middleware: validate request body
function validate(schema) {
    return (req, res, next) => {
        const result = schema.safeParse(req.body);
        if (!result.success) {
            return res.status(400).json({
                error: 'Validation failed',
                details: result.error.issues,
            });
        }
        req.body = result.data;  // Dùng parsed data (đã sanitize!)
        next();
    };
}

app.post('/api/users', authenticate, validate(CreateUserSchema), createUser);
```

---

## 4. Rate Limiting — Chống abuse

```typescript
import rateLimit from 'express-rate-limit';

// Global: 100 requests / 15 phút per IP
const globalLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 100,
    standardHeaders: true,  // RateLimit-* headers
    message: { error: 'Too many requests, try again later' },
});

// Login: 5 attempts / 15 phút (chống brute force)
const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 5,
    skipSuccessfulRequests: true,  // Chỉ count failed attempts
});

// Expensive endpoints: 10 / giờ
const reportLimiter = rateLimit({
    windowMs: 60 * 60 * 1000,
    max: 10,
});

app.use(globalLimiter);
app.post('/api/auth/login', loginLimiter, loginHandler);
app.post('/api/reports', reportLimiter, reportHandler);
```

---

## 5. Security Headers & CORS

```typescript
import helmet from 'helmet';
import cors from 'cors';

// Helmet: set security headers tự động
app.use(helmet());
// X-Content-Type-Options: nosniff
// X-Frame-Options: DENY
// Strict-Transport-Security: max-age=31536000
// Content-Security-Policy: ...

// CORS: chỉ cho phép specific origins
app.use(cors({
    origin: ['https://myapp.com', 'https://admin.myapp.com'],
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true,  // Cho phép cookies
    maxAge: 86400,       // Preflight cache 24h
}));

// ❌ NEVER: cors({ origin: '*' }) + credentials!
```

---

## 6. SQL Injection & Data Exposure

```typescript
// ❌ SQL Injection: user input trực tiếp vào query
const user = await db.query(`SELECT * FROM users WHERE id = '${req.params.id}'`);
// req.params.id = "1' OR '1'='1" → SELECT * FROM users (trả TẤT CẢ users!)

// ✅ Parameterized queries
const user = await db.query('SELECT * FROM users WHERE id = $1', [req.params.id]);

// ✅ ORM (Prisma, Sequelize) — auto-parameterized
const user = await prisma.user.findUnique({ where: { id: req.params.id } });

// ❌ Data exposure: trả toàn bộ user object (kể cả password!)
app.get('/api/users/:id', async (req, res) => {
    const user = await db.users.findById(req.params.id);
    res.json(user);  // { id, name, email, passwordHash, ssn, ... } 😱
});

// ✅ Select chỉ fields cần thiết
app.get('/api/users/:id', async (req, res) => {
    const user = await prisma.user.findUnique({
        where: { id: req.params.id },
        select: { id: true, name: true, email: true, avatar: true },
    });
    res.json(user);
});
```

---

## Security Checklist

```
Authentication:
  ✅ JWT short-lived (15m access + 7d refresh)
  ✅ httpOnly cookies cho web (chống XSS)
  ✅ Password: bcrypt, minimum strength requirements

Authorization:
  ✅ Check resource ownership TRÊN MỌI endpoint
  ✅ Role-based + resource-level permissions
  ✅ Không expose internal IDs nếu có thể (dùng UUID)

Input:
  ✅ Validate MỌI input (Zod, Joi, class-validator)
  ✅ Parameterized queries (KHÔNG string interpolation!)
  ✅ Sanitize HTML output (chống XSS)

Infrastructure:
  ✅ HTTPS everywhere (TLS 1.2+)
  ✅ Rate limiting (global + per-endpoint)
  ✅ Security headers (Helmet)
  ✅ CORS whitelist (KHÔNG origin: '*')
  ✅ Secrets in env vars / Vault (KHÔNG in code!)
  ✅ Dependency audit (npm audit) trong CI
```

---

## Bài tập thực hành

- [ ] JWT: access + refresh token system
- [ ] BOLA fix: audit existing endpoints cho ownership check
- [ ] Rate limiting: global + login-specific
- [ ] Input validation: Zod schemas cho tất cả endpoints

---

## Tài nguyên thêm

- [OWASP API Security Top 10](https://owasp.org/API-Security/) — Must read
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) — Practical guides
- [Helmet.js](https://helmetjs.github.io/) — Security headers
