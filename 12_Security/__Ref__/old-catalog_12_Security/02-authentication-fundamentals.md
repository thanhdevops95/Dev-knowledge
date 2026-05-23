# 🔐 Authentication & Authorization

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Ai bạn là? Bạn được làm gì?

---

## Authentication vs Authorization

```
Authentication (AuthN) — "Bạn là ai?"
  → Xác minh danh tính
  → Login bằng mật khẩu, token, biometrics

Authorization (AuthZ) — "Bạn được làm gì?"
  → Xác định quyền hạn sau khi đã xác thực
  → RBAC, ABAC, permissions

Thứ tự: AuthN trước → AuthZ sau
```

---

## JWT — JSON Web Token

```
Structure: header.payload.signature

Header: {"alg": "HS256", "typ": "JWT"}
Payload: {"sub": "usr_123", "role": "admin", "exp": 1708344000}
Signature: HMACSHA256(base64(header) + "." + base64(payload), secret)
```

```python
import jwt
from datetime import datetime, timedelta, timezone
from uuid import uuid4

SECRET_KEY = "your-256-bit-secret-from-env"
ALGORITHM = "HS256"

def create_access_token(user_id: str, role: str) -> str:
    payload = {
        "sub": user_id,        # Subject
        "role": role,
        "type": "access",
        "jti": str(uuid4()),   # JWT ID — phòng replay attack
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "type": "refresh",
        "jti": str(uuid4()),
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, expected_type: str = "access") -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != expected_type:
            raise ValueError("Sai loại token")
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token đã hết hạn")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Token không hợp lệ: {e}")
```

### Token Rotation Pattern

```python
# Khi access token hết hạn:
# 1. Client gửi refresh token
# 2. Server verify, tạo access + refresh token MỚI
# 3. Invalidate refresh token cũ (lưu vào blacklist trong Redis)

async def refresh_tokens(refresh_token: str, redis: Redis) -> dict:
    payload = verify_token(refresh_token, expected_type="refresh")
    
    # Kiểm tra refresh token chưa bị revoke
    jti = payload["jti"]
    if await redis.exists(f"revoked:token:{jti}"):
        raise ValueError("Token đã bị thu hồi")
    
    user_id = payload["sub"]
    user = await user_repo.get(user_id)
    if not user or not user.is_active:
        raise ValueError("User không tồn tại")
    
    # Revoke token cũ
    ttl = int(payload["exp"] - datetime.now(timezone.utc).timestamp())
    await redis.setex(f"revoked:token:{jti}", ttl, "1")
    
    return {
        "access_token": create_access_token(user_id, user.role),
        "refresh_token": create_refresh_token(user_id)
    }
```

---

## OAuth 2.0 & OpenID Connect

**OAuth 2.0** — Authorization protocol (cho phép app third-party access resource)
**OpenID Connect (OIDC)** — Authentication layer trên OAuth 2.0

### Authorization Code Flow (Phổ biến nhất)

```
User                  App                    Auth Server (Google)
 │── Click "Login" ──►│                             │
 │                    │── Redirect ─────────────────►│
 │                    │   ?response_type=code        │
 │                    │   &client_id=...             │
 │                    │   &redirect_uri=...          │
 │                    │   &scope=email profile       │
 │                    │   &state=random_string       │
 │◄─────────────────────── Google Login Page ────────│
 │── Enter creds ─────────────────────────────────── ►│
 │                    │◄─────── Redirect ─────────────│
 │                    │   ?code=AUTH_CODE             │
 │                    │   &state=random_string        │
 │                    │                             │
 │                    │── POST /token ──────────────►│
 │                    │   code + client_secret       │
 │                    │◄── access_token + id_token ──│
 │                    │                             │
 │                    │── GET /userinfo ────────────►│
 │                    │◄── {email, name, picture} ───│
 │◄─── Logged in ─────│                             │
```

```python
# Python với authlib
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"}
)

# FastAPI routes
@router.get("/auth/google")
async def login_google(request: Request):
    redirect_uri = request.url_for("auth_google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def auth_google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    
    # Tìm hoặc tạo user
    user = await user_service.find_or_create_by_email(
        email=user_info["email"],
        name=user_info["name"],
        avatar=user_info.get("picture"),
        provider="google"
    )
    
    access_token = create_access_token(str(user.id), user.role)
    refresh_token = create_refresh_token(str(user.id))
    
    # Redirect về frontend với tokens
    return RedirectResponse(
        f"https://myapp.com/auth/callback"
        f"?access_token={access_token}"
        f"&refresh_token={refresh_token}"
    )
```

---

## Session-based Auth (Traditional)

```python
# Cookie + Server-side session
from fastapi import Cookie, Response
import secrets

# Login
@router.post("/auth/login")
async def login(body: LoginRequest, response: Response, redis: Redis):
    user = await authenticate_user(body.email, body.password)
    
    session_id = secrets.token_urlsafe(32)
    session_data = {"user_id": str(user.id), "role": user.role}
    
    # Lưu session trong Redis
    await redis.setex(f"session:{session_id}", 3600 * 24, json.dumps(session_data))
    
    # Set HTTP-only cookie
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,     # Không accessible từ JavaScript
        secure=True,       # HTTPS only
        samesite="strict", # CSRF protection
        max_age=3600 * 24
    )
    return {"message": "Đăng nhập thành công"}

# Middleware kiểm tra session
async def get_session_user(
    session_id: str | None = Cookie(None),
    redis: Redis = Depends(get_redis)
) -> User:
    if not session_id:
        raise HTTPException(401, "Chưa đăng nhập")
    
    session_data = await redis.get(f"session:{session_id}")
    if not session_data:
        raise HTTPException(401, "Session hết hạn")
    
    data = json.loads(session_data)
    return await user_repo.get(data["user_id"])
```

---

## RBAC — Role Based Access Control

```python
from enum import Enum
from functools import wraps

class Role(str, Enum):
    USER      = "user"
    MODERATOR = "moderator"
    ADMIN     = "admin"

# Permission matrix
PERMISSIONS = {
    "post:read":   [Role.USER, Role.MODERATOR, Role.ADMIN],
    "post:create": [Role.USER, Role.MODERATOR, Role.ADMIN],
    "post:delete": [Role.MODERATOR, Role.ADMIN],
    "user:ban":    [Role.MODERATOR, Role.ADMIN],
    "user:delete": [Role.ADMIN],
    "admin:panel": [Role.ADMIN],
}

def require_permission(permission: str):
    """Decorator kiểm tra permission"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            allowed_roles = PERMISSIONS.get(permission, [])
            if Role(current_user.role) not in allowed_roles:
                raise HTTPException(
                    status_code=403,
                    detail=f"Không có quyền: {permission}"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Dùng trong routes
@router.delete("/posts/{post_id}")
@require_permission("post:delete")
async def delete_post(post_id: str, current_user: User = Depends(get_current_user)):
    await post_service.delete(post_id, current_user)
```

---

## MFA — Multi-Factor Authentication

```python
import pyotp
import qrcode

# TOTP (Time-based OTP — Google Authenticator)
def setup_mfa(user_id: str, user_email: str) -> dict:
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    
    # URI để tạo QR code
    provisioning_uri = totp.provisioning_uri(
        name=user_email,
        issuer_name="MyApp"
    )
    
    # Tạo QR code
    img = qrcode.make(provisioning_uri)
    img.save(f"qr_{user_id}.png")
    
    # Lưu secret (mã hóa) vào DB
    await user_repo.save_mfa_secret(user_id, encrypt(secret))
    
    return {"qr_uri": provisioning_uri, "backup_codes": generate_backup_codes()}

def verify_totp(user_id: str, otp_code: str) -> bool:
    encrypted_secret = await user_repo.get_mfa_secret(user_id)
    secret = decrypt(encrypted_secret)
    totp = pyotp.TOTP(secret)
    return totp.verify(otp_code, valid_window=1)  # +/- 30s tolerance
```

---

## Security Checklist Authentication

- [ ] HTTPS only — Không gửi credentials qua HTTP
- [ ] Hash passwords với bcrypt/Argon2 (cost factor ≥ 12)
- [ ] JWT secret dài (256-bit), rotate định kỳ
- [ ] Access token TTL ngắn (15 phút)
- [ ] Refresh token rotation (mỗi lần dùng = token mới)
- [ ] Lưu refresh tokens trong Redis với khả năng revoke
- [ ] HTTP-only, Secure, SameSite cookies
- [ ] Rate limit login endpoints (5 lần/15 phút)
- [ ] Log failed login attempts
- [ ] PKCE cho OAuth flows
- [ ] Validate `state` parameter trong OAuth

---

## Tài nguyên thêm

- [JWT.io](https://jwt.io/) — Debug JWT tokens
- [OAuth 2.0 Simplified](https://www.oauth.com/) — Giải thích dễ hiểu
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Authlib](https://authlib.org/) — Python OAuth library
- [Lucia Auth](https://lucia-auth.com/) — Auth library cho Node.js
