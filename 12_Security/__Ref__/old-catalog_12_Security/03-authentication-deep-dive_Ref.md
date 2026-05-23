# 🔐 Authentication & Authorization nâng cao

> `[INTERMEDIATE → ADVANCED]` — Bảo mật user identity & access control

---

## Auth là gì?

**Authentication (AuthN):** "Bạn là AI?" → Xác minh danh tính  
**Authorization (AuthZ):** "Bạn được làm gì?" → Kiểm tra quyền

---

## 1. Session-based vs Token-based

```
Session-based:
Client ──POST /login──► Server tạo session → lưu DB/Redis
Client ◄──Set-Cookie: session_id=abc──
Client ──GET /api/me (Cookie: session_id=abc)──► Server lookup session
Client ◄── User data

Token-based (JWT):
Client ──POST /login──► Server tạo JWT
Client ◄──token: eyJhbG...──
Client ──GET /api/me (Authorization: Bearer eyJhbG...)──► Server verify JWT
Client ◄── User data
```

| | Session | JWT |
|---|---|---|
| **Lưu ở** | Server (DB/Redis) | Client (localStorage/cookie) |
| **Stateful** | ✅ Server nhớ session | ❌ Stateless |
| **Revoke** | ✅ Xóa session | ❌ Phải dùng blacklist |
| **Scale** | Cần shared session store | ✅ Không cần server state |
| **Size** | Cookie nhỏ (~20 bytes) | JWT lớn (~800+ bytes) |

---

## 2. JWT — Deep Dive

```
JWT = Header.Payload.Signature

Header:    { "alg": "HS256", "typ": "JWT" }
Payload:   { "sub": "123", "name": "An", "role": "admin", "exp": 1709500800 }
Signature: HMACSHA256(base64(header) + "." + base64(payload), secret)

eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.abc123signature

⚠️ Payload KHÔNG mã hóa! Ai cũng đọc được. KHÔNG lưu sensitive data.
```

```javascript
import jwt from 'jsonwebtoken';

// Tạo tokens
function generateTokens(user) {
    const accessToken = jwt.sign(
        { sub: user.id, role: user.role },
        process.env.JWT_SECRET,
        { expiresIn: '15m' }   // Ngắn!
    );

    const refreshToken = jwt.sign(
        { sub: user.id },
        process.env.JWT_REFRESH_SECRET,
        { expiresIn: '7d' }
    );

    return { accessToken, refreshToken };
}

// Verify middleware
function authMiddleware(req, res, next) {
    const token = req.headers.authorization?.replace('Bearer ', '');
    if (!token) return res.status(401).json({ error: 'No token' });

    try {
        req.user = jwt.verify(token, process.env.JWT_SECRET);
        next();
    } catch (err) {
        if (err.name === 'TokenExpiredError') {
            return res.status(401).json({ error: 'Token expired' });
        }
        return res.status(401).json({ error: 'Invalid token' });
    }
}

// Refresh token flow
app.post('/api/auth/refresh', async (req, res) => {
    const { refreshToken } = req.body;

    try {
        const payload = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET);
        const user = await db.users.findById(payload.sub);

        // Verify refresh token in DB (revocable)
        if (user.refreshToken !== refreshToken) {
            return res.status(401).json({ error: 'Invalid refresh token' });
        }

        const tokens = generateTokens(user);
        user.refreshToken = tokens.refreshToken;
        await user.save();

        res.json(tokens);
    } catch {
        res.status(401).json({ error: 'Invalid refresh token' });
    }
});
```

---

## 3. OAuth 2.0 — "Đăng nhập bằng Google"

```
┌──────┐     ┌──────────┐     ┌──────────┐
│ User │     │ Your App │     │  Google  │
└──┬───┘     └────┬─────┘     └────┬─────┘
   │              │                 │
   │──Click "Login with Google"──► │
   │              │──Redirect──────►│
   │              │                 │
   │◄─────── Google Login Page ─────│
   │──Enter credentials───────────►│
   │              │                 │
   │              │◄──Auth Code─────│
   │              │                 │
   │              │──Code + Secret─►│
   │              │◄──Access Token──│
   │              │                 │
   │              │──Get User Info─►│
   │              │◄──User Profile──│
   │              │                 │
   │◄──Login OK + JWT──────────────│
```

```javascript
// Passport.js — OAuth strategy
const passport = require('passport');
const GoogleStrategy = require('passport-google-oauth20').Strategy;

passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: '/auth/google/callback',
}, async (accessToken, refreshToken, profile, done) => {
    let user = await User.findOne({ googleId: profile.id });
    if (!user) {
        user = await User.create({
            googleId: profile.id,
            name: profile.displayName,
            email: profile.emails[0].value,
            avatar: profile.photos[0].value,
        });
    }
    done(null, user);
}));

app.get('/auth/google', passport.authenticate('google', {
    scope: ['profile', 'email']
}));

app.get('/auth/google/callback',
    passport.authenticate('google', { session: false }),
    (req, res) => {
        const tokens = generateTokens(req.user);
        res.redirect(`/login/success?token=${tokens.accessToken}`);
    }
);
```

---

## 4. RBAC — Role-Based Access Control

```javascript
// Roles & Permissions
const PERMISSIONS = {
    admin:     ['read', 'write', 'delete', 'manage_users'],
    editor:    ['read', 'write'],
    viewer:    ['read'],
};

function authorize(...requiredPermissions) {
    return (req, res, next) => {
        const userPermissions = PERMISSIONS[req.user.role] || [];
        const hasPermission = requiredPermissions.every(p =>
            userPermissions.includes(p)
        );

        if (!hasPermission) {
            return res.status(403).json({ error: 'Forbidden' });
        }
        next();
    };
}

// Routes
app.get('/api/posts', authMiddleware, authorize('read'), getPosts);
app.post('/api/posts', authMiddleware, authorize('write'), createPost);
app.delete('/api/posts/:id', authMiddleware, authorize('delete'), deletePost);
app.get('/api/admin/users', authMiddleware, authorize('manage_users'), getUsers);
```

---

## 5. Password Security

```javascript
import bcrypt from 'bcrypt';

// Hash password (registration)
const hashedPassword = await bcrypt.hash(password, 12);
// $2b$12$LJ3m4ys.hDGey2JVHx0wbO... (60 chars, includes salt)

// Verify password (login)
const isValid = await bcrypt.compare(inputPassword, hashedPassword);

// ⚠️ KHÔNG BAO GIỜ:
// - Lưu plaintext password
// - Dùng MD5/SHA256 (quá nhanh → brute force dễ)
// - Tự implement crypto
```

---

## 6. Security Best Practices

```javascript
// 1. Rate limit login attempts
const rateLimit = require('express-rate-limit');
app.use('/api/auth/login', rateLimit({
    windowMs: 15 * 60 * 1000,  // 15 phút
    max: 5,                     // 5 lần thử
    message: 'Too many login attempts',
}));

// 2. CSRF Protection
app.use(csurf({ cookie: true }));

// 3. Secure cookies
res.cookie('token', jwt, {
    httpOnly: true,    // JS không đọc được
    secure: true,      // Chỉ HTTPS
    sameSite: 'strict', // Chống CSRF
    maxAge: 900000,    // 15 phút
});

// 4. Security headers
app.use(helmet());

// 5. Input validation
const { z } = require('zod');
const loginSchema = z.object({
    email: z.string().email(),
    password: z.string().min(8).max(128),
});
```

---

## Các lỗi thường gặp

```
❌ Sai: Lưu JWT trong localStorage → XSS có thể đánh cắp
✅ Đúng: Lưu trong httpOnly cookie

❌ Sai: Access token expire 30 ngày
✅ Đúng: Access token 15 phút, Refresh token 7 ngày

❌ Sai: Không hash password trước khi lưu DB
✅ Đúng: bcrypt với cost factor ≥ 12
```

---

## Bài tập thực hành

- [ ] Implement JWT auth: register, login, refresh token, logout
- [ ] Thêm OAuth: "Login with Google" bằng Passport.js
- [ ] RBAC: admin, editor, viewer với middleware authorize()
- [ ] Security: rate limiting, httpOnly cookies, input validation

---

## Tài nguyên thêm

- [OWASP Auth Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [JWT.io](https://jwt.io/) — Decode JWT online
- [OAuth 2.0 Simplified](https://www.oauth.com/) — Free book
