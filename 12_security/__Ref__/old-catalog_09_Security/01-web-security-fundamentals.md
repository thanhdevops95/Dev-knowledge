# 🔐 Web Security Fundamentals

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Bảo mật phải được nghĩ từ đầu, không phải thêm vào sau

---

## OWASP Top 10 (2021)

Danh sách 10 lỗ hổng bảo mật nguy hiểm nhất theo OWASP:

| # | Tên | Mức độ |
|---|---|---|
| A01 | Broken Access Control | 🔴 Critical |
| A02 | Cryptographic Failures | 🔴 Critical |
| A03 | Injection (SQL, XSS, ...) | 🔴 Critical |
| A04 | Insecure Design | 🟠 High |
| A05 | Security Misconfiguration | 🟠 High |
| A06 | Vulnerable Components | 🟠 High |
| A07 | Identification & Auth Failures | 🟠 High |
| A08 | Software & Data Integrity Failures | 🟠 High |
| A09 | Security Logging Failures | 🟡 Medium |
| A10 | SSRF | 🟡 Medium |

---

## A03 — SQL Injection

```python
# ❌ VULNERABLE — KHÔNG BAO GIỜ làm thế này!
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    # Hacker nhập: ' OR '1'='1
    # Query trở thành: SELECT * FROM users WHERE username = '' OR '1'='1'
    return db.execute(query)

# ✅ SAFE — Dùng parameterized queries
def get_user(username: str):
    return db.execute(
        "SELECT * FROM users WHERE username = $1",
        [username]
    )

# ✅ SAFE — Với ORM
user = User.query.filter_by(username=username).first()
```

---

## A03 — XSS (Cross-Site Scripting)

```javascript
// ❌ VULNERABLE — inject HTML trực tiếp
element.innerHTML = userInput;
document.write(userInput);

// ✅ SAFE — dùng textContent
element.textContent = userInput;

// ✅ SAFE — Sanitize HTML nếu cần render
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);

// ✅ Content Security Policy (HTTP Header)
// Ngăn load script từ nguồn không tin cậy
Content-Security-Policy: 
    default-src 'self';
    script-src 'self' https://trusted-cdn.com;
    style-src 'self' 'unsafe-inline';
    img-src 'self' data: https:;
    font-src 'self' https://fonts.gstatic.com;
```

---

## A01 — Broken Access Control

```python
# ❌ Không kiểm tra quyền sở hữu
@app.route("/posts/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = db.get(Post, post_id)
    db.delete(post)  # Ai cũng xóa được!

# ✅ Kiểm tra ownership
@app.route("/posts/<post_id>", methods=["DELETE"])
@require_auth
def delete_post(post_id):
    post = db.get(Post, post_id)
    
    if not post:
        raise NotFoundError()
    
    if post.author_id != current_user.id and not current_user.is_admin:
        raise ForbiddenError("Không có quyền xóa bài viết này")
    
    db.delete(post)
    return "", 204
```

---

## Authentication — JWT

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "super-secret-key-from-env"
ALGORITHM = "HS256"

def create_tokens(user_id: str, role: str) -> dict:
    now = datetime.utcnow()
    
    # Access token — ngắn hạn (15 phút)
    access_payload = {
        "sub": user_id,
        "role": role,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=15)
    }
    
    # Refresh token — dài hạn (7 ngày), lưu trong DB
    refresh_payload = {
        "sub": user_id,
        "type": "refresh",
        "iat": now,
        "exp": now + timedelta(days=7)
    }
    
    return {
        "access_token": jwt.encode(access_payload, SECRET_KEY, ALGORITHM),
        "refresh_token": jwt.encode(refresh_payload, SECRET_KEY, ALGORITHM)
    }

def verify_token(token: str, token_type: str = "access") -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["type"] != token_type:
            raise ValueError("Sai loại token")
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("Token đã hết hạn")
    except jwt.InvalidTokenError:
        raise UnauthorizedError("Token không hợp lệ")
```

---

## Password Hashing

```python
# ❌ KHÔNG BAO GIỜ lưu password dạng plain text hoặc MD5/SHA
password_hash = md5(password)  # ❌

# ✅ Dùng bcrypt hoặc Argon2
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Argon2 (tốt hơn bcrypt)
from argon2 import PasswordHasher
ph = PasswordHasher()

hashed = ph.hash("my_password")
ph.verify(hashed, "my_password")  # True
```

---

## HTTPS & Security Headers

```nginx
# Nginx config
server {
    listen 443 ssl http2;
    
    # TLS
    ssl_certificate /etc/ssl/certs/certificate.crt;
    ssl_certificate_key /etc/ssl/private/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
    
    # CSP
    add_header Content-Security-Policy "default-src 'self'; ..." always;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    return 301 https://$host$request_uri;
}
```

---

## Rate Limiting

```python
from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

@app.post("/auth/login")
@limiter.limit("5/minute")  # 5 lần/phút cho login
async def login(request: Request, credentials: LoginRequest):
    ...

@app.get("/api/search")
@limiter.limit("100/minute")  # 100 lần/phút cho search
async def search(request: Request, q: str):
    ...
```

---

## Input Validation

```python
from pydantic import BaseModel, EmailStr, validator
import re

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    age: int

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Mật khẩu tối thiểu 8 ký tự")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Cần ít nhất 1 chữ hoa")
        if not re.search(r"\d", v):
            raise ValueError("Cần ít nhất 1 chữ số")
        return v

    @validator("age")
    def validate_age(cls, v):
        if not 13 <= v <= 120:
            raise ValueError("Tuổi không hợp lệ")
        return v

    @validator("name")
    def validate_name(cls, v):
        # Strip và kiểm tra ký tự đặc biệt
        v = v.strip()
        if len(v) < 2 or len(v) > 100:
            raise ValueError("Tên phải từ 2-100 ký tự")
        return v
```

---

## Environment Variables & Secrets

```python
# ❌ KHÔNG hardcode secrets trong code
DATABASE_URL = "postgresql://admin:password@prod-db:5432/mydb"
SECRET_KEY = "my-secret-key"

# ✅ Dùng environment variables
import os
from dotenv import load_dotenv

load_dotenv()  # Đọc từ .env (chỉ local, không commit lên git!)

DATABASE_URL = os.environ["DATABASE_URL"]  # Bắt buộc phải có
SECRET_KEY = os.getenv("SECRET_KEY", "default-for-dev-only")
```

```bash
# .env (KHÔNG commit lên git!)
DATABASE_URL=postgresql://...
SECRET_KEY=super-random-secret-key
JWT_PRIVATE_KEY=...

# .env.example (commit, không có values thật)
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=your-secret-key-here
JWT_PRIVATE_KEY=your-private-key-here
```

---

## Security Checklist

- [ ] HTTPS everywhere, redirect HTTP → HTTPS
- [ ] Set security headers (HSTS, CSP, X-Frame-Options...)
- [ ] Hash passwords với bcrypt/Argon2
- [ ] Parameterized queries (chống SQL injection)
- [ ] Sanitize user input (chống XSS)
- [ ] Kiểm tra authorization trên mọi endpoint
- [ ] Rate limiting cho auth endpoints
- [ ] JWT expiry ngắn (15-30 phút)
- [ ] Không log sensitive data (password, token, PII)
- [ ] Dependency updates thường xuyên (`npm audit`, `pip audit`)
- [ ] `.env` trong `.gitignore`
- [ ] Secrets trong secret manager (AWS Secrets Manager, Vault)

---

## Tài nguyên thêm

- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — Chính thức
- [PortSwigger Web Security Academy](https://portswigger.net/web-security) — Labs miễn phí
- [Securityheaders.com](https://securityheaders.com/) — Kiểm tra security headers
- [HaveIBeenPwned](https://haveibeenpwned.com/API/v3) — Check email breach
