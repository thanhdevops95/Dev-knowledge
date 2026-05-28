# ⚡ FastAPI — Python Backend Framework

> `[INTERMEDIATE]` ⭐ — API nhanh nhất Python, tự sinh docs

---

## Tại sao dùng FastAPI?

- **Nhanh nhất** trong các Python framework (ngang NodeJS/Go)
- **Tự sinh OpenAPI docs** — Swagger UI & ReDoc tự động
- **Type hints** — Validation input/output qua Pydantic
- **Async native** — `async/await` từ đầu
- **Dễ học** — Ít boilerplate nhất

---

## Cài đặt & Khởi động

```bash
pip install fastapi uvicorn[standard] pydantic-settings

# Chạy dev server
uvicorn main:app --reload --port 8000
```

---

## App cơ bản

```python
# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db.connect()
    yield
    # Shutdown
    await db.disconnect()

app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}
```

---

## Pydantic Models — Request & Response

```python
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(ge=13, le=120)

class UserCreate(UserBase):
    password: str = Field(min_length=8)

    @validator("password")
    def password_must_be_strong(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Cần ít nhất 1 chữ hoa")
        if not any(c.isdigit() for c in v):
            raise ValueError("Cần ít nhất 1 chữ số")
        return v

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True  # Cho phép đọc từ ORM objects

class PaginatedResponse(BaseModel):
    data: list[UserResponse]
    total: int
    page: int
    limit: int
    total_pages: int

# Standard API response
class ApiResponse(BaseModel):
    success: bool = True
    data: dict | list | None = None
    message: str = ""
```

---

## Routing & Path Operations

```python
from fastapi import APIRouter, Path, Query, Depends, HTTPException, status
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: str = Query("", max_length=100),
    is_active: bool | None = None,
    db: AsyncSession = Depends(get_db)
):
    """Lấy danh sách users với pagination và filtering"""
    users, total = await user_service.list(db, page, limit, search, is_active)
    return PaginatedResponse(
        data=users,
        total=total,
        page=page,
        limit=limit,
        total_pages=(total + limit - 1) // limit
    )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID = Path(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = await user_service.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} không tồn tại"
        )
    return user

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    body: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    existing = await user_service.get_by_email(db, body.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email đã được sử dụng"
        )
    return await user_service.create(db, body)

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    body: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Không có quyền")
    return await user_service.update(db, user_id, body)

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    await user_service.delete(db, user_id)
```

---

## Dependency Injection

```python
from fastapi import Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def get_db():
    """Database session dependency"""
    async with AsyncSession(engine) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Verify JWT token và trả về user hiện tại"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError()
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Token không hợp lệ hoặc đã hết hạn"
        )
    
    user = await user_service.get_by_id(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User không tồn tại")
    return user

def require_admin(current_user: User = Depends(get_current_user)):
    """Chỉ cho phép admin"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Cần quyền Admin")
    return current_user

# Dùng trong route
@app.get("/admin/stats")
async def admin_stats(admin: User = Depends(require_admin)):
    return {"users_count": 100}
```

---

## Middleware

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import time
import uuid

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start_time = time.perf_counter()
    
    response = await call_next(request)
    
    duration_ms = (time.perf_counter() - start_time) * 1000
    print(f"[{request_id}] {request.method} {request.url.path} → {response.status_code} ({duration_ms:.1f}ms)")
    
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{duration_ms:.1f}ms"
    return response
```

---

## Exception Handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Dữ liệu không hợp lệ",
                "details": [
                    {
                        "field": ".".join(str(x) for x in err["loc"][1:]),
                        "message": err["msg"]
                    }
                    for err in exc.errors()
                ]
            }
        }
    )
```

---

## Cấu trúc project chuẩn

```
my-api/
├── main.py                  # FastAPI app, middleware, routers
├── config.py               # Settings với pydantic-settings
├── dependencies.py         # Shared dependencies (db, auth)
│
├── routers/
│   ├── users.py
│   ├── posts.py
│   └── auth.py
│
├── models/                 # SQLAlchemy models
│   ├── base.py
│   ├── user.py
│   └── post.py
│
├── schemas/                # Pydantic schemas
│   ├── user.py
│   └── post.py
│
├── services/               # Business logic
│   ├── user_service.py
│   └── post_service.py
│
├── repositories/           # Database queries
│   └── user_repo.py
│
├── tests/
│   ├── conftest.py
│   └── test_users.py
│
└── pyproject.toml
```

---

## Testing

```python
# tests/test_users.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient):
    response = await async_client.post(
        "/users",
        json={
            "name": "Jesse",
            "email": "jesse@example.com",
            "age": 25,
            "password": "Password123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "jesse@example.com"
    assert "id" in data
    assert "password" not in data  # Không được trả về password!

@pytest.mark.asyncio
async def test_get_user_not_found(authenticated_client: AsyncClient):
    response = await authenticated_client.get("/users/nonexistent-id")
    assert response.status_code == 404
```

---

## Bài tập thực hành

- [ ] CRUD API cho Blog (posts, comments)
- [ ] Authentication đầy đủ: register, login, refresh token
- [ ] Upload file với FastAPI (ảnh avatar)
- [ ] Background tasks với FastAPI + Celery

---

## Tài nguyên thêm

- [FastAPI Docs](https://fastapi.tiangolo.com/) — Xuất sắc, có nhiều ví dụ
- [SQLAlchemy + FastAPI](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Awesome FastAPI](https://github.com/mjhea0/awesome-fastapi)
