# 🟢 Node.js cơ bản — JavaScript trên Server

> `[BEGINNER → INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Backend phổ biến nhất cho web developers

---

## Tại sao Node.js?

- **1 ngôn ngữ** (JavaScript) cho cả frontend + backend
- **Non-blocking I/O** — xử lý hàng ngàn connections đồng thời
- **npm** — ecosystem package lớn nhất thế giới (2M+ packages)
- Dùng bởi: Netflix, PayPal, LinkedIn, Uber

---

## 1. Event Loop — Core concept

```
Node.js = Single-threaded + Event Loop + Non-blocking I/O

Truyền thống (Java, PHP):
Request 1 ──► Thread 1 ──► Query DB (đợi...) ──► Response
Request 2 ──► Thread 2 ──► Query DB (đợi...) ──► Response
Request 3 ──► Thread 3 ──► Query DB (đợi...) ──► Response
  (1000 requests = 1000 threads → tốn RAM)

Node.js:
Request 1 ──► Event Loop ──► Query DB (không đợi!) ──► Callback
Request 2 ──┤                                          
Request 3 ──┘              
  (1000 requests = 1 thread → ít RAM, nhanh hơn cho I/O)
```

> ⚠️ Node.js **KHÔNG** phù hợp cho CPU-intensive tasks (video encoding, ML). Dùng Worker Threads hoặc chọn Go/Python cho tasks đó.

---

## 2. Modules

```javascript
// ES Modules (hiện đại, khuyến khích)
// math.js
export function add(a, b) { return a + b; }
export function multiply(a, b) { return a * b; }
export default class Calculator { /* ... */ }

// app.js
import Calculator, { add, multiply } from './math.js';

// CommonJS (cũ, nhưng vẫn phổ biến)
// utils.js
module.exports = { add, multiply };

// app.js
const { add, multiply } = require('./utils');

// Built-in modules
import fs from 'fs/promises';
import path from 'path';
import { createServer } from 'http';
import crypto from 'crypto';
```

---

## 3. Express.js — Web Framework

```javascript
import express from 'express';
import cors from 'cors';

const app = express();

// Middleware
app.use(cors());
app.use(express.json());                    // Parse JSON body
app.use(express.urlencoded({ extended: true }));

// Logging middleware
app.use((req, res, next) => {
    console.log(`${req.method} ${req.url}`);
    next();  // Chuyển tiếp cho middleware tiếp theo
});

// Routes
app.get('/api/users', async (req, res) => {
    try {
        const { page = 1, limit = 20 } = req.query;
        const users = await User.find()
            .skip((page - 1) * limit)
            .limit(Number(limit));
        res.json({ data: users, meta: { page, limit } });
    } catch (error) {
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.get('/api/users/:id', async (req, res) => {
    const user = await User.findById(req.params.id);
    if (!user) return res.status(404).json({ error: 'User not found' });
    res.json({ data: user });
});

app.post('/api/users', async (req, res) => {
    const { name, email } = req.body;

    if (!name || !email) {
        return res.status(400).json({ error: 'name and email required' });
    }

    const user = await User.create({ name, email });
    res.status(201).json({ data: user });
});

// Error handling middleware (phải có 4 params!)
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

---

## 4. Middleware Pattern

```
Request ──► Middleware 1 ──► Middleware 2 ──► Route Handler ──► Response
            (CORS)          (Auth)           (Business Logic)

Middleware = function(req, res, next)
  • Thêm/sửa req (req.user = decoded JWT)
  • Chặn request (401 nếu chưa auth)
  • next() → chuyển tiếp
  • res.json() → dừng, trả response
```

```javascript
// Auth middleware
function authMiddleware(req, res, next) {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: 'No token' });

    try {
        req.user = jwt.verify(token, process.env.JWT_SECRET);
        next();
    } catch {
        res.status(401).json({ error: 'Invalid token' });
    }
}

// Rate limiting middleware
function rateLimit(maxRequests, windowMs) {
    const requests = new Map();

    return (req, res, next) => {
        const key = req.ip;
        const now = Date.now();
        const windowStart = now - windowMs;

        const userRequests = requests.get(key) || [];
        const recent = userRequests.filter(t => t > windowStart);

        if (recent.length >= maxRequests) {
            return res.status(429).json({ error: 'Too many requests' });
        }

        recent.push(now);
        requests.set(key, recent);
        next();
    };
}

// Sử dụng
app.use('/api', rateLimit(100, 60000));  // 100 req/phút
app.use('/api/admin', authMiddleware);
```

---

## 5. File System & Streams

```javascript
import fs from 'fs/promises';
import { createReadStream, createWriteStream } from 'fs';

// Đọc/ghi file
const data = await fs.readFile('config.json', 'utf-8');
await fs.writeFile('output.txt', 'Hello World');
await fs.appendFile('log.txt', `${new Date()}: Event\n`);

// Kiểm tra file tồn tại
try {
    await fs.access('file.txt');
    console.log('File exists');
} catch {
    console.log('File not found');
}

// Streams — xử lý file lớn (không load toàn bộ vào RAM)
const readStream = createReadStream('big-file.csv');
const writeStream = createWriteStream('output.csv');

readStream
    .pipe(transformStream)  // Xử lý dữ liệu
    .pipe(writeStream);     // Ghi ra file
```

---

## 6. Environment & Config

```bash
# .env
PORT=3000
DATABASE_URL=postgres://user:pass@localhost:5432/mydb
JWT_SECRET=super-secret-key
NODE_ENV=development
```

```javascript
// Dùng dotenv hoặc Node.js 20+ built-in
import 'dotenv/config';

const config = {
    port: process.env.PORT || 3000,
    dbUrl: process.env.DATABASE_URL,
    jwtSecret: process.env.JWT_SECRET,
    isProduction: process.env.NODE_ENV === 'production',
};
```

---

## 7. Project Structure

```
src/
├── server.js              # Entry point
├── config/
│   └── index.js           # Environment config
├── routes/
│   ├── users.js           # /api/users routes
│   └── posts.js           # /api/posts routes
├── controllers/
│   ├── userController.js  # Request handling
│   └── postController.js
├── services/
│   ├── userService.js     # Business logic
│   └── postService.js
├── models/
│   ├── User.js            # Database model
│   └── Post.js
├── middleware/
│   ├── auth.js            # Authentication
│   ├── validate.js        # Input validation
│   └── errorHandler.js    # Global error handler
└── utils/
    └── helpers.js
```

---

## Express vs Fastify vs NestJS

| | Express | Fastify | NestJS |
|---|---|---|---|
| **Tốc độ** | Tốt | ⚡ Nhanh hơn 2x | Tốt (dùng Express/Fastify) |
| **Style** | Minimal, flexible | Performance-first | Full framework (Angular-like) |
| **TypeScript** | Manual setup | Built-in | ⭐ First-class |
| **Learning** | Dễ nhất | Dễ | Trung bình (DI, decorators) |
| **Khi nào** | Prototype, small apps | High-performance API | Enterprise, large teams |

---

## Các lỗi thường gặp

```
❌ Sai: Blocking Event Loop (CPU-heavy task trong main thread)
   app.get('/api/hash', (req, res) => {
       const hash = heavyCrypto(data);  // Block!
   });
✅ Đúng: Dùng Worker Threads hoặc offload sang queue

❌ Sai: Không handle unhandled promise rejections
✅ Đúng: 
   process.on('unhandledRejection', (err) => {
       console.error('Unhandled:', err);
       process.exit(1);
   });

❌ Sai: Commit .env file
✅ Đúng: .env trong .gitignore, dùng .env.example
```

---

## Bài tập thực hành

- [ ] Tạo REST API với Express: CRUD users + validation
- [ ] Thêm JWT authentication middleware
- [ ] Kết nối MongoDB/PostgreSQL
- [ ] Viết integration tests cho API endpoints

---

## Tài nguyên thêm

- [Node.js Docs](https://nodejs.org/docs/) — Official
- [Express.js Guide](https://expressjs.com/en/guide/) — Getting started
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices) — GitHub 100k+ ⭐
