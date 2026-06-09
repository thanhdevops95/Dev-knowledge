# 🎓 Auth & Middleware — JWT, OAuth2, CORS, Logging

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Prerequisites:** [Database với SQLModel](03_database-with-sqlmodel.md), [HTTP Headers](../../../../../05_networking/http-https/lessons/01_basic/03_http-headers.md)

> 🎯 *Hoàn chỉnh backend production: **password hash** (bcrypt), **JWT tokens**, **OAuth2 Password Flow**, **`Depends()` chain** cho `get_current_user`, **CORS** middleware, **custom middleware** (logging, request_id). Sau bài này backend bảo mật + production-ready.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hash password với **bcrypt** (KHÔNG plaintext!)
- [ ] Generate + verify **JWT** với `python-jose`
- [ ] Implement **OAuth2 Password Flow** (`/token` endpoint)
- [ ] Tạo dependency **`get_current_user`** chain
- [ ] Bảo vệ endpoint bằng `Depends(get_current_user)`
- [ ] Config **CORS** middleware đúng cách
- [ ] Viết **custom middleware** (logging, request_id, timing)
- [ ] Hiểu thứ tự middleware + dependency execution

---

## Tình huống — Bạn deploy backend xong, ai cũng vào được

Backend bạn bài 03 hoạt động ngon nhưng:
- 🔓 Mọi endpoint **public** — ai cũng vào.
- 🔑 Password lưu **cleartext** (`password_hash = "hashed-mypass"` demo).
- 🌐 Frontend React ở `localhost:3000` gọi → **CORS error**.
- 📊 Không có log request — debug khó.

Security audit:
- ❌ Password phải hash bằng **bcrypt** hoặc **argon2**.
- ❌ Cần **JWT** auth — client login lấy token, gửi token mỗi request.
- ❌ Cần config **CORS** cho frontend domain.
- ❌ Cần log request_id để trace.

Bạn ngơ:
- JWT là gì, khác cookie session sao?
- bcrypt cài đặt sao trong FastAPI?
- Middleware vs Dependency — khác sao?

→ Bài cuối cluster dạy đầy đủ.

---

## 1️⃣ Hash password — KHÔNG BAO GIỜ cleartext

### Cài

`passlib` là thư viện hash password chuẩn Python — wrap bcrypt/argon2/scrypt với API thống nhất. Cài kèm `[bcrypt]` extras để có thuật toán bcrypt sẵn:

```bash
pip install "passlib[bcrypt]"
```

### `app/core/security.py`

Module security cô lập 2 hàm core — `hash_password` (encrypt khi đăng ký) + `verify_password` (so sánh khi login). Đặt riêng trong `app/core/` để dễ test + reuse:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

### Dùng

2 endpoint chính dùng `hash_password` + `verify_password` — đăng ký (hash trước khi lưu DB) và login (verify khi authenticate). Đây là pattern bạn sẽ viết trong mọi auth system:

```python
# Đăng ký
db_user.password_hash = hash_password(user.password)

# Login
if not verify_password(input_password, db_user.password_hash):
    raise HTTPException(401, "Sai email/password")
```

→ bcrypt **slow** (~250ms 1 hash) — đó là feature. Chống brute force.

### Tại sao không SHA256/MD5?

Beginner hay nghĩ "hash là hash, SHA-256 nhanh hơn nên tốt hơn". Sai cho password — password hash phải **CHẬM** để chống brute force. So sánh 4 thuật toán:

| Hash | Tốc độ | An toàn cho password? |
|---|---|---|
| MD5 / SHA-256 | Rất nhanh (microsecond) | ❌ Brute force dễ |
| **bcrypt** | ~250ms (10 rounds default) | ✅ |
| **argon2** | ~250ms | ✅ Winner Password Hashing Competition 2015 |
| scrypt | ~250ms | ✅ |

→ Password hash phải **CHẬM**. Hash file dùng SHA-256 OK (cần nhanh, mục đích khác).

> ⚠️ Đừng **roll your own crypto**. Dùng `passlib` hoặc `argon2-cffi`. Lỗi nhỏ = catastrophic.

---

## 2️⃣ JWT là gì?

**JWT** = JSON Web Token — chuỗi string chứa **payload signed** bằng secret server.

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzE2NTU2MTAwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
└──── header ────┘.└──── payload ────┘.└──── signature ────┘
       base64                base64
```

### 3 phần (cách nhau dấu `.`)

JWT là chuỗi text **3 phần ngăn cách dấu `.`** — mỗi phần base64-encoded. Header + Payload **decode được không cần secret** (base64), chỉ Signature là verify cần secret. Đây là lý do KHÔNG được lưu password trong payload:

| Phần | Nội dung |
|---|---|
| **Header** | `{"alg": "HS256", "typ": "JWT"}` |
| **Payload** | `{"sub": "1", "exp": 1716556100}` (claim — user_id, expiry) |
| **Signature** | HMAC-SHA256(header + payload, **SECRET_KEY**) |

→ Decode payload **không cần secret** (base64). **Verify** signature cần secret.

### Workflow

```
1. Client POST /token với email + password
2. Server verify → tạo JWT { "sub": user_id, "exp": now + 30min }
3. Server return { "access_token": "eyJ...", "token_type": "bearer" }
4. Client lưu token (localStorage / httpOnly cookie)
5. Mỗi request: Authorization: Bearer eyJ...
6. Server verify signature + expiry → biết user là ai
```

### JWT vs Cookie session

| Tiêu chí | JWT | Cookie session |
|---|---|---|
| State | Stateless (token tự chứa) | Stateful (server lưu) |
| Scale horizontal | ✅ Dễ (không share state) | 🟡 Cần Redis chia session |
| Revoke ngay | ❌ Khó (phải maintain blacklist) | ✅ Dễ (delete session) |
| Size | Lớn (~500-1000 byte) | Nhỏ (session_id ~32 byte) |
| Mobile / API | ✅ Default | 🟡 OK nhưng cookie phức tạp |
| XSS protection | 🟡 Nếu lưu localStorage thì rủi ro | ✅ httpOnly cookie |

→ **2026**: JWT phổ biến cho REST API (mobile + SPA). Session cookie phổ biến cho web traditional.

---

## 3️⃣ JWT trong FastAPI

### Cài

```bash
pip install "python-jose[cryptography]"
```

### `app/core/security.py` (mở rộng)

```python
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

SECRET_KEY = "your-very-long-random-secret-from-env"      # KHÔNG hardcode prod
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])      # raise JWTError nếu invalid
```

### Sinh SECRET_KEY production

```bash
openssl rand -hex 32
# eb2f3a8d4c5b6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f
```

→ Lưu vào `.env`, **không commit**. Đổi = invalidate mọi token cũ.

---

## 4️⃣ OAuth2 Password Flow — `/token` endpoint

FastAPI có sẵn `OAuth2PasswordBearer` + `OAuth2PasswordRequestForm` — chuẩn OAuth2 grant type "password".

### `app/api/auth.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.user import User
from app.core.security import verify_password, create_access_token

router = APIRouter(tags=["auth"])

@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    # OAuth2 spec: dùng "username" (có thể là email)
    user = session.exec(select(User).where(User.email == form_data.username)).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai email hoặc password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
```

Test:
```bash
curl -X POST http://localhost:8000/token \
  -d "username=nguyenvana@ex.com&password=mypass123" \
  -H "Content-Type: application/x-www-form-urlencoded"

# {"access_token":"eyJ...","token_type":"bearer"}
```

→ `OAuth2PasswordRequestForm` accept **form data** (`application/x-www-form-urlencoded`), không phải JSON — spec OAuth2.

---

## 5️⃣ `get_current_user` — Bảo vệ endpoint

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")     # ← URL endpoint login

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token không hợp lệ hoặc đã hết hạn",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.get(User, int(user_id))
    if user is None:
        raise credentials_exception
    return user
```

### Dùng trong endpoint

```python
@router.get("/users/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/orders")
def list_my_orders(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    statement = select(Order).where(Order.user_id == current_user.id)
    return session.exec(statement).all()
```

→ Mỗi request đến endpoint protected:
1. FastAPI lấy `Authorization: Bearer eyJ...` header.
2. Gọi `get_current_user` → decode JWT → fetch user từ DB.
3. Pass `current_user` vào endpoint.
4. Sai/expired token → 401 tự động.

### Swagger UI tự có nút "Authorize"

→ Mở `/docs`, click nút khóa 🔒 → Swagger UI hiển thị form login → tự test các endpoint protected.

---

## 6️⃣ Dependency chain — Permission roles

```python
def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(403, "Cần quyền admin")
    return current_user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.disabled:
        raise HTTPException(400, "Tài khoản bị disable")
    return current_user

# Dùng
@router.delete("/users/{id}")
def delete_user(id: int, admin: User = Depends(get_current_admin)):
    ...
```

→ **Dependency chain** = composable. `get_current_admin` dùng `get_current_user` — FastAPI auto resolve thứ tự + cache (1 request gọi `get_current_user` 1 lần, không gọi 2 lần dù bạn xài 2 chỗ).

---

## 7️⃣ CORS — Cho phép frontend origin khác gọi API

Frontend React ở `localhost:3000`, API ở `localhost:8000` → browser **block** vì khác origin (xem [HTTP headers CORS](../../../../../05_networking/http-https/lessons/01_basic/03_http-headers.md)).

### Config

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://acmeshop.vn"
    ],
    allow_credentials=True,         # Cho gửi cookie
    allow_methods=["*"],             # Hoặc liệt kê: ["GET", "POST", ...]
    allow_headers=["*"],
)
```

### Cạm bẫy

```python
# ❌ NGUY HIỂM production
allow_origins=["*"]
allow_credentials=True
# CORS spec cấm combo này — browser sẽ từ chối
```

→ Production: liệt kê **chính xác** origin domains. Wildcard `*` chỉ cho API public hoàn toàn (không auth).

---

## 8️⃣ Custom middleware — Logging + request_id + timing

```python
import time
import uuid
from fastapi import Request

@app.middleware("http")
async def add_request_id_and_log(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start = time.time()

    # Pre-request: gắn request_id để log handlers dùng
    request.state.request_id = request_id

    response = await call_next(request)

    # Post-request: log
    duration_ms = (time.time() - start) * 1000
    print(f"[{request_id}] {request.method} {request.url.path} {response.status_code} {duration_ms:.0f}ms")

    response.headers["X-Request-ID"] = request_id
    return response
```

→ Mỗi request: log method + path + status + thời gian. Thêm `X-Request-ID` cho trace cross-service.

### Output

```
[abc-123] GET /users/42 200 12ms
[def-456] POST /users 422 8ms
[ghi-789] GET /orders 200 156ms
```

---

## 9️⃣ Thứ tự execution

Khi 1 request đến:

```
1. Middleware (mọi @app.middleware đã đăng ký)
   ↓
2. Route handler (find URL match)
   ↓
3. Dependencies (Depends chain) — chạy outside-in
   ↓
4. Path operation function (endpoint code)
   ↓
5. Response → quay ngược lại
   ↓
6. Middleware (post-processing)
   ↓
7. Trả về client
```

### Middleware order quan trọng

```python
app.add_middleware(CustomLoggingMiddleware)     # ← chạy NGOÀI cùng
app.add_middleware(CORSMiddleware, ...)          # ← chạy giữa
# request → Logging → CORS → endpoint → CORS → Logging → response
```

→ Add **outer middleware sau cùng** trong code (FastAPI add ngược thứ tự — LIFO).

---

## 1️⃣0️⃣ Ghép full stack production-ready

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time, uuid

from app.db.database import init_db
from app.api import users, orders, auth

@asynccontextmanager
async def lifespan(app):
    init_db()
    yield

app = FastAPI(title="Acme Shop API", version="1.0.0", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://acmeshop.vn"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    rid = str(uuid.uuid4())[:8]
    start = time.time()
    response = await call_next(request)
    print(f"[{rid}] {request.method} {request.url.path} → {response.status_code} ({(time.time()-start)*1000:.0f}ms)")
    response.headers["X-Request-ID"] = rid
    return response

# Routes
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
```

→ Backend bạn giờ:
- ✅ DB persistent (SQLModel + Postgres)
- ✅ Password hash bcrypt
- ✅ JWT auth với `/token` + `get_current_user`
- ✅ Permission `get_current_admin`
- ✅ CORS cho frontend domains
- ✅ Logging với request_id
- ✅ Auto OpenAPI docs
- ✅ Schema migration với Alembic

→ Backend **production-ready**. Deploy lên VPS bằng Docker (xem cluster Docker đã viết).

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **SECRET_KEY hardcode trong code** → push lên git = mọi token bị giả mạo. Luôn từ env, sinh bằng `openssl rand`.
2. **`allow_origins=["*"]` + `allow_credentials=True`** → spec CORS cấm combo này. Browser block.
3. **JWT không expire** → lộ 1 token = vĩnh viễn. Luôn có `exp`. Refresh token pattern cho session dài.
4. **Lưu JWT trong `localStorage`** → XSS attack đọc được. Best practice: **httpOnly cookie** (nhưng phức tạp CORS). Hoặc localStorage + chặn XSS bằng CSP.
5. **Quên hash khi seed test data** → password cleartext trong DB. Validate test data luôn qua `hash_password()`.

---

## 🧠 Tự kiểm tra (Self-check)

1. Sao password phải hash **chậm**? Tool nào (2026 default)?
2. JWT có **3 phần**, viết ra. Verify cần gì?
3. Khác biệt **Middleware** vs **Dependency**?
4. `OAuth2PasswordBearer(tokenUrl="token")` làm gì?
5. CORS `allow_origins=["*"]` + `allow_credentials=True` — vì sao spec cấm?

<details>
<summary>Gợi ý đáp án</summary>

1. Password hash **chậm** để brute force tốn năm thay vì giây. Default 2026: **bcrypt** (rounds 10-12, ~250ms) hoặc **argon2** (winner PHC 2015). Đừng SHA256/MD5 — quá nhanh.

2. JWT = `header.payload.signature` (cách nhau `.`). Header có alg+typ, payload có claim (sub, exp, ...). Signature = HMAC(header+payload, SECRET). Verify cần **SECRET_KEY** — decode chỉ cần base64 (không cần secret).

3. **Middleware** = chạy **mọi request** (logging, CORS, auth global). **Dependency** = chạy với endpoint **chỉ định** (`Depends()`). Middleware ngoài, dependency trong. Middleware không return value, dependency return value inject vào endpoint.

4. Đăng ký **OAuth2 scheme** với FastAPI — Swagger UI hiển thị nút "Authorize", `oauth2_scheme` lấy token từ `Authorization: Bearer ...` header. `tokenUrl="token"` chỉ Swagger biết endpoint login (`POST /token`) để render form login.

5. Spec CORS quy định **`*` không cho phép gửi credential** (cookie, Authorization header) — vì origin không xác định = nguy hiểm. Browser sẽ từ chối preflight. Phải liệt kê origin cụ thể nếu `allow_credentials=True`.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Hash password

```python
from passlib.context import CryptContext
ctx = CryptContext(schemes=["bcrypt"])
ctx.hash("plaintext")               # → hash
ctx.verify("plain", "hash")          # → True/False
```

### JWT

```python
from jose import jwt
token = jwt.encode({"sub": "1", "exp": ...}, SECRET, "HS256")
payload = jwt.decode(token, SECRET, algorithms=["HS256"])
```

### Auth setup

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = jwt.decode(token, SECRET, ...)
    return session.get(User, int(payload["sub"]))

@app.get("/me")
def me(user: User = Depends(get_current_user)):
    return user
```

### CORS

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Logging middleware

```python
@app.middleware("http")
async def log_requests(req, call_next):
    response = await call_next(req)
    print(f"{req.method} {req.url.path} {response.status_code}")
    return response
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **bcrypt / argon2** | Password hash chậm, an toàn |
| **JWT** | JSON Web Token — chuỗi signed payload |
| **Claim** | Field trong JWT payload (`sub`, `exp`, `iat`, ...) |
| **HS256 / RS256** | Symmetric (1 secret) / Asymmetric (key pair) signing |
| **OAuth2 Password Flow** | Grant type: client gửi `username`+`password` → nhận token |
| **`OAuth2PasswordBearer`** | FastAPI helper extract Bearer token |
| **Middleware** | Function wrap mọi request |
| **Dependency** | Function chạy cho endpoint chỉ định qua `Depends()` |
| **CORS** | Cross-Origin Resource Sharing — header browser policy |
| **`X-Request-ID`** | Header trace request qua các service |
| **httpOnly cookie** | Cookie JS không đọc được — chống XSS |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [Database với SQLModel — CRUD thực tế](03_database-with-sqlmodel.md)
- ↑ **Về cụm:** [python-fastapi README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [HTTP Headers — Auth + CORS](../../../../../05_networking/http-https/lessons/01_basic/03_http-headers.md)
- [HTTPS & TLS](../../../../../05_networking/http-https/lessons/01_basic/04_https-tls.md) — JWT nên dùng qua HTTPS

### 🌐 Tài nguyên tham khảo khác
- 📖 [FastAPI Security — OAuth2 with Password](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- 📖 [JWT.io debugger](https://jwt.io/) — decode + verify JWT online
- 📖 [OWASP — Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- 📖 [Argon2 paper](https://www.password-hashing.net/)
- 📖 [FastAPI Middleware docs](https://fastapi.tiangolo.com/tutorial/middleware/)

---

> 🎯 *Cluster FastAPI basic 5/5 đóng. Backend bạn giờ production-ready: DB + Auth + CORS + logging + auto docs. Bài kế tiếp có thể vào **02_intermediate** (background tasks, WebSocket, file upload, testing) hoặc nhảy sang cluster khác (Docker deploy, K8s, Postgres specific).*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `python-fastapi/` lesson 5/5. Cover: hash password bcrypt + JWT (3 phần + workflow + vs cookie session) + OAuth2PasswordBearer + dependency `get_current_user` + CORS middleware + custom middleware (logging, rate limit) + production checklist (HTTPS, refresh token, secret rotation).
- **v1.1.0 (25/05/2026)** — Bổ sung câu dẫn nhập cho §1 Cài passlib + `app/core/security.py` + Dùng hash/verify + Tại sao không SHA256, §2 JWT 3 phần. Chuẩn hóa placeholder tên trong code mẫu. Thêm mục Changelog.
