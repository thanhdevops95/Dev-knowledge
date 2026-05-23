# 🟢 Node.js & Express — JavaScript Backend

> `[BEGINNER → INTERMEDIATE]` — Backend với ngôn ngữ JavaScript bạn đã biết

---

## Tại sao Node.js?

- **Cùng ngôn ngữ** với Frontend — JavaScript/TypeScript
- **Non-blocking I/O** — Xử lý nhiều connection đồng thời hiệu quả
- **Hệ sinh thái npm** — Hàng triệu packages
- **Realtime** — WebSockets, SSE rất tự nhiên
- **Express** — Minimal, linh hoạt, dễ học

---

## Setup với TypeScript

```bash
mkdir my-api && cd my-api
npm init -y
npm install express
npm install -D typescript ts-node @types/express @types/node nodemon

# TypeScript config
npx tsc --init
```

```json
// package.json scripts
{
  "scripts": {
    "dev": "nodemon --exec ts-node src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

---

## App cơ bản

```typescript
// src/index.ts
import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import { userRouter } from './routes/users'
import { errorHandler } from './middleware/errorHandler'

const app = express()
const PORT = process.env.PORT || 8000

// Middleware
app.use(helmet())                               // Security headers
app.use(cors({ origin: process.env.CORS_ORIGIN }))
app.use(express.json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true }))

// Request logging
app.use((req, res, next) => {
  const start = Date.now()
  res.on('finish', () => {
    const duration = Date.now() - start
    console.log(`${req.method} ${req.path} → ${res.statusCode} (${duration}ms)`)
  })
  next()
})

// Routes
app.get('/health', (req, res) => res.json({ status: 'ok' }))
app.use('/api/v1/users', userRouter)

// 404
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: { code: 'NOT_FOUND', message: `Route ${req.path} không tồn tại` }
  })
})

// Error handler (phải đặt cuối cùng)
app.use(errorHandler)

app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`)
})

export default app
```

---

## Router & Controllers

```typescript
// src/routes/users.ts
import { Router } from 'express'
import { authenticate, requireAdmin } from '../middleware/auth'
import * as userController from '../controllers/userController'
import { validateBody } from '../middleware/validate'
import { createUserSchema, updateUserSchema } from '../schemas/userSchema'

export const userRouter = Router()

userRouter.get('/', authenticate, userController.list)
userRouter.get('/:id', authenticate, userController.getById)
userRouter.post('/', validateBody(createUserSchema), userController.create)
userRouter.patch('/:id', authenticate, validateBody(updateUserSchema), userController.update)
userRouter.delete('/:id', authenticate, requireAdmin, userController.remove)
```

```typescript
// src/controllers/userController.ts
import { Request, Response, NextFunction } from 'express'
import * as userService from '../services/userService'
import { AppError } from '../utils/errors'

export async function list(req: Request, res: Response, next: NextFunction) {
  try {
    const { page = 1, limit = 20, search = '' } = req.query
    const result = await userService.findAll({
      page: Number(page),
      limit: Number(limit),
      search: String(search)
    })
    res.json({ success: true, ...result })
  } catch (err) {
    next(err)  // Chuyển lỗi sang errorHandler
  }
}

export async function getById(req: Request, res: Response, next: NextFunction) {
  try {
    const user = await userService.findById(req.params.id)
    if (!user) throw new AppError('NOT_FOUND', 'User không tồn tại', 404)
    res.json({ success: true, data: user })
  } catch (err) {
    next(err)
  }
}

export async function create(req: Request, res: Response, next: NextFunction) {
  try {
    const user = await userService.create(req.body)
    res.status(201).json({ success: true, data: user })
  } catch (err) {
    next(err)
  }
}
```

---

## Middleware

```typescript
// src/middleware/auth.ts
import { Request, Response, NextFunction } from 'express'
import jwt from 'jsonwebtoken'

export function authenticate(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({
      success: false,
      error: { code: 'UNAUTHORIZED', message: 'Yêu cầu đăng nhập' }
    })
  }

  const token = authHeader.slice(7)
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as JwtPayload
    req.user = payload  // Gắn user vào request
    next()
  } catch {
    res.status(401).json({
      success: false,
      error: { code: 'INVALID_TOKEN', message: 'Token không hợp lệ hoặc hết hạn' }
    })
  }
}

export function requireAdmin(req: Request, res: Response, next: NextFunction) {
  if (req.user?.role !== 'admin') {
    return res.status(403).json({
      success: false,
      error: { code: 'FORBIDDEN', message: 'Cần quyền Admin' }
    })
  }
  next()
}
```

```typescript
// src/middleware/validate.ts — Zod validation
import { Request, Response, NextFunction } from 'express'
import { ZodSchema } from 'zod'

export function validateBody(schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body)
    if (!result.success) {
      return res.status(422).json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Dữ liệu không hợp lệ',
          details: result.error.errors.map(e => ({
            field: e.path.join('.'),
            message: e.message
          }))
        }
      })
    }
    req.body = result.data
    next()
  }
}
```

```typescript
// src/middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express'
import { AppError } from '../utils/errors'

export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      success: false,
      error: { code: err.code, message: err.message }
    })
  }

  // Lỗi không mong đợi — log nhưng không expose details
  console.error('[Unhandled Error]', err)
  res.status(500).json({
    success: false,
    error: { code: 'INTERNAL_ERROR', message: 'Lỗi hệ thống, vui lòng thử lại' }
  })
}
```

---

## Validation với Zod

```typescript
// src/schemas/userSchema.ts
import { z } from 'zod'

export const createUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  password: z
    .string()
    .min(8)
    .regex(/[A-Z]/, 'Cần ít nhất 1 chữ hoa')
    .regex(/[0-9]/, 'Cần ít nhất 1 chữ số'),
  age: z.number().int().min(13).max(120)
})

export const updateUserSchema = z.object({
  name: z.string().min(2).max(100).optional(),
  bio: z.string().max(500).optional(),
  age: z.number().int().min(13).max(120).optional()
})

export type CreateUserDto = z.infer<typeof createUserSchema>
export type UpdateUserDto = z.infer<typeof updateUserSchema>
```

---

## Rate Limiting & Security

```typescript
import rateLimit from 'express-rate-limit'
import helmet from 'helmet'

// Rate limit chung
const generalLimiter = rateLimit({
  windowMs: 60 * 1000,   // 1 phút
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    success: false,
    error: { code: 'RATE_LIMIT', message: 'Quá nhiều request, thử lại sau 1 phút' }
  }
})

// Strict limit cho auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 phút
  max: 5,
  message: {
    success: false,
    error: { code: 'RATE_LIMIT', message: '5 lần thử tối đa mỗi 15 phút' }
  }
})

app.use('/api', generalLimiter)
app.use('/api/v1/auth/login', authLimiter)
```

---

## Cấu trúc project chuẩn

```
src/
├── index.ts              # Entry point
├── config.ts             # Environment config
│
├── routes/               # Route definitions
├── controllers/          # Request handlers
├── services/             # Business logic
├── repositories/         # Database queries
│
├── middleware/
│   ├── auth.ts
│   ├── validate.ts
│   └── errorHandler.ts
│
├── schemas/              # Zod schemas
├── models/               # Database models (Prisma/TypeORM)
├── utils/
│   ├── errors.ts
│   └── jwt.ts
│
└── tests/
```

---

## Bài tập thực hành

- [ ] Blog API: CRUD posts, comments, tags
- [ ] Auth system: JWT + refresh tokens
- [ ] File upload API với multer
- [ ] Real-time chat với Socket.io

---

## Tài nguyên thêm

- [Express.js Docs](https://expressjs.com/)
- [Fastify](https://fastify.dev/) — Thay thế nhanh hơn Express
- [NestJS](https://nestjs.com/) — Enterprise framework cho Node.js (TypeScript native)
- [Prisma](https://www.prisma.io/) — ORM TypeScript tốt nhất
