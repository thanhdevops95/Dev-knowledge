# 🔐 Authentication nâng cao — JWT, OAuth2, Sessions

> `[INTERMEDIATE → ADVANCED]` — Xác thực người dùng production-grade

---

## 1. JWT — JSON Web Token

### Cấu trúc

```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIxMjMiLCJyb2xlIjoiYWRtaW4ifQ.signature
       HEADER                    PAYLOAD                     SIGNATURE

Header:  { "alg": "HS256", "typ": "JWT" }
Payload: { "userId": "123", "role": "admin", "exp": 1709553600 }
Signature: HMAC-SHA256(header + "." + payload, SECRET_KEY)
```

### Access Token + Refresh Token

```typescript
import jwt from 'jsonwebtoken';

const ACCESS_SECRET = process.env.ACCESS_SECRET!;
const REFRESH_SECRET = process.env.REFRESH_SECRET!;

function generateTokens(user: User) {
    const accessToken = jwt.sign(
        { userId: user.id, role: user.role },
        ACCESS_SECRET,
        { expiresIn: '15m' },  // Ngắn hạn!
    );

    const refreshToken = jwt.sign(
        { userId: user.id, tokenVersion: user.tokenVersion },
        REFRESH_SECRET,
        { expiresIn: '7d' },   // Dài hạn
    );

    return { accessToken, refreshToken };
}

// Login flow
app.post('/api/auth/login', async (req, res) => {
    const { email, password } = req.body;

    const user = await db.users.findByEmail(email);
    if (!user || !await bcrypt.compare(password, user.password)) {
        return res.status(401).json({ error: 'Invalid credentials' });
    }

    const { accessToken, refreshToken } = generateTokens(user);

    // Refresh token trong httpOnly cookie (XSS-safe)
    res.cookie('refreshToken', refreshToken, {
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60 * 1000,
    });

    res.json({ accessToken });
});

// Refresh flow
app.post('/api/auth/refresh', async (req, res) => {
    const token = req.cookies.refreshToken;
    if (!token) return res.status(401).json({ error: 'No refresh token' });

    try {
        const payload = jwt.verify(token, REFRESH_SECRET) as any;
        const user = await db.users.findById(payload.userId);

        // Check token version (revoke cũ khi logout/password change)
        if (!user || user.tokenVersion !== payload.tokenVersion) {
            return res.status(401).json({ error: 'Token revoked' });
        }

        const { accessToken, refreshToken: newRefresh } = generateTokens(user);

        res.cookie('refreshToken', newRefresh, { /* same options */ });
        res.json({ accessToken });
    } catch {
        res.status(401).json({ error: 'Invalid refresh token' });
    }
});

// Auth middleware
function authenticate(req, res, next) {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: 'No token' });

    try {
        req.user = jwt.verify(token, ACCESS_SECRET);
        next();
    } catch {
        res.status(401).json({ error: 'Invalid token' });
    }
}
```

---

## 2. OAuth 2.0 — "Login with Google/GitHub"

```
OAuth2 Authorization Code Flow:

1. User clicks "Login with Google"
2. Redirect → Google authorization page
3. User authorizes → Google redirects back with CODE
4. Your server exchanges CODE → ACCESS TOKEN (server-to-server)
5. Use access token to get user profile from Google

┌────────┐          ┌──────────┐          ┌──────────┐
│ Client │──1. Login──►│  Your    │──2. Redirect──►│ Google  │
│(Browser│          │  Server  │          │ OAuth    │
│        │◄─5. JWT──│          │◄─3. Code─│          │
│        │          │          │──4. Code──►│          │
│        │          │          │◄─Token───│          │
└────────┘          └──────────┘          └──────────┘
```

```typescript
import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';

passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    callbackURL: '/api/auth/google/callback',
}, async (accessToken, refreshToken, profile, done) => {
    // Tìm hoặc tạo user
    let user = await db.users.findByGoogleId(profile.id);
    if (!user) {
        user = await db.users.create({
            googleId: profile.id,
            name: profile.displayName,
            email: profile.emails?.[0]?.value,
            avatar: profile.photos?.[0]?.value,
        });
    }
    done(null, user);
}));

// Routes
app.get('/api/auth/google', passport.authenticate('google', {
    scope: ['profile', 'email'],
}));

app.get('/api/auth/google/callback',
    passport.authenticate('google', { session: false }),
    (req, res) => {
        const { accessToken, refreshToken } = generateTokens(req.user);
        res.cookie('refreshToken', refreshToken, { httpOnly: true, secure: true });
        res.redirect(`${FRONTEND_URL}?token=${accessToken}`);
    },
);
```

---

## 3. Session-based Auth — Khi nào dùng?

```
JWT (Stateless):
  ✅ Microservices (không shared state)
  ✅ Mobile apps
  ✅ API cho third-party
  ❌ Không revoke được ngay (phải chờ expire)
  ❌ Token size lớn

Sessions (Stateful):
  ✅ Server-rendered apps (SSR)
  ✅ Revoke ngay lập tức
  ✅ Cookie nhỏ (chỉ session ID)
  ❌ Cần shared session store (Redis) cho multi-server
  ❌ Không hợp mobile apps
```

---

## 4. Password Hashing

```typescript
import bcrypt from 'bcryptjs';

// ❌ KHÔNG BAO GIỜ:
// - Lưu plaintext password
// - Dùng MD5/SHA256 (quá nhanh → brute force dễ!)
// - Tự viết hash function

// ✅ Dùng bcrypt (hoặc Argon2)
const SALT_ROUNDS = 12;  // Cost factor: 2^12 iterations

async function hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(password: string, hash: string): Promise<boolean> {
    return bcrypt.compare(password, hash);
}

// Password validation
function validatePassword(password: string): string[] {
    const errors: string[] = [];
    if (password.length < 8) errors.push('Tối thiểu 8 ký tự');
    if (!/[A-Z]/.test(password)) errors.push('Cần ít nhất 1 chữ hoa');
    if (!/[0-9]/.test(password)) errors.push('Cần ít nhất 1 số');
    if (!/[!@#$%^&*]/.test(password)) errors.push('Cần ít nhất 1 ký tự đặc biệt');
    return errors;
}
```

---

## 5. RBAC — Role-Based Access Control

```typescript
// Roles & Permissions
const PERMISSIONS = {
    admin: ['read', 'write', 'delete', 'manage_users'],
    editor: ['read', 'write'],
    viewer: ['read'],
} as const;

// Authorization middleware
function authorize(...requiredPermissions: string[]) {
    return (req, res, next) => {
        const userRole = req.user.role;
        const userPermissions = PERMISSIONS[userRole] || [];

        const hasPermission = requiredPermissions.every(
            perm => userPermissions.includes(perm),
        );

        if (!hasPermission) {
            return res.status(403).json({ error: 'Forbidden' });
        }
        next();
    };
}

// Sử dụng
app.get('/api/users', authenticate, authorize('read'), getUsers);
app.post('/api/users', authenticate, authorize('write'), createUser);
app.delete('/api/users/:id', authenticate, authorize('delete'), deleteUser);
```

---

## Security Checklist

```
✅ Passwords: bcrypt/Argon2, salt rounds ≥ 12
✅ JWT: short-lived access (15m), httpOnly refresh cookie
✅ HTTPS: everywhere, HSTS header
✅ CORS: whitelist origins, credentials: true
✅ Rate limiting: login attempts (5/min per IP)
✅ CSRF: SameSite cookies hoặc CSRF token
✅ Input validation: email format, password strength
✅ Account lockout: sau 5 failed attempts
✅ Audit log: login, password change, role change
```

---

## Bài tập thực hành

- [ ] JWT auth: login, register, refresh token flow
- [ ] OAuth2: "Login with Google" integration
- [ ] RBAC: admin/editor/viewer permissions
- [ ] Security: rate limit, account lockout, audit log

---

## Tài nguyên thêm

- [OWASP Authentication Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [JWT.io](https://jwt.io/) — Debugger
- [OAuth 2.0 Simplified](https://www.oauth.com/) — Aaron Parecki
