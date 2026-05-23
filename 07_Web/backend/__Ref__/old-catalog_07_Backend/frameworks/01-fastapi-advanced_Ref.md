# FastAPI Advanced — Dependency Injection, Auth, Background Tasks

> **Tags:** `fastapi` `python` `di` `jwt` `async` `celery` `websocket`
> **Level:** Intermediate | **Prerequisite:** `python/01-python-basics.md` `api-design/01-rest-api.md`

---

## 1. Dependency Injection System

```python
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from functools import lru_cache

app = FastAPI()

# Database session dependency
engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Repository pattern with DI
class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def find_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(UserModel).filter_by(id=user_id))
        return result.scalar_one_or_none()
    
    async def find_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(UserModel).filter_by(email=email))
        return result.scalar_one_or_none()
    
    async def create(self, data: CreateUserDto) -> User:
        user = UserModel(**data.model_dump())
        self.db.add(user)
        await self.db.flush()  # Get ID without committing
        return user

async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

# Service depending on repository
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    async def get_user(self, user_id: int) -> User:
        user = await self.repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    async def create_user(self, data: CreateUserDto) -> User:
        existing = await self.repo.find_by_email(data.email)
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")
        
        data.password = hash_password(data.password)
        return await self.repo.create(data)

async def get_user_service(
    repo: UserRepository = Depends(get_user_repo)
) -> UserService:
    return UserService(repo)

# Route using DI chain
@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
):
    return await service.get_user(user_id)
```

---

## 2. Authentication — JWT

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# JWT utilities
def create_access_token(user_id: int, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=60),
        "iat": datetime.utcnow(),
        "type": "access",
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def create_refresh_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=30),
        "type": "refresh",
    }
    return jwt.encode(payload, settings.JWT_REFRESH_SECRET, algorithm="HS256")

def decode_token(token: str, secret: str) -> dict:
    try:
        return jwt.decode(token, secret, algorithms=["HS256"])
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Current user dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    payload = decode_token(credentials.credentials, settings.JWT_SECRET)
    
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
    
    user_id = int(payload["sub"])
    user = await db.get(UserModel, user_id)
    
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    
    return user

# Role-based access control
def require_role(*roles: str):
    async def check_role(
        current_user: UserModel = Depends(get_current_user)
    ) -> UserModel:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {roles}"
            )
        return current_user
    return check_role

# Usage
@app.get("/admin/users")
async def list_all_users(
    admin: UserModel = Depends(require_role("admin", "superadmin")),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(UserModel))
    return result.scalars().all()

# Login endpoint
@app.post("/auth/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(UserModel).filter_by(email=data.email))
    user = user.scalar_one_or_none()
    
    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    return {
        "access_token": create_access_token(user.id, user.role),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }

@app.post("/auth/refresh")
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    payload = decode_token(credentials.credentials, settings.JWT_REFRESH_SECRET)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Not a refresh token")
    
    user = await db.get(UserModel, int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return { "access_token": create_access_token(user.id, user.role) }
```

---

## 3. Request Validation & Response Models

```python
from pydantic import BaseModel, EmailStr, field_validator, model_validator, Field
from typing import Optional, Annotated

# Input models
class CreateUserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
    age: Optional[int] = Field(None, ge=0, le=120)
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Name cannot be empty")
        return stripped
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v
    
    @model_validator(mode='before')
    @classmethod
    def strip_whitespace(cls, values: dict) -> dict:
        return {k: v.strip() if isinstance(v, str) else v for k, v in values.items()}

# Response models (never expose sensitive fields)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime
    
    model_config = {"from_attributes": True}  # Allow from ORM objects

class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

class ErrorResponse(BaseModel):
    detail: str
    code: str | None = None

# Annotated types for reuse
UserID = Annotated[int, Field(gt=0, description="User ID")]
PageNumber = Annotated[int, Field(default=1, ge=1)]
PageSize = Annotated[int, Field(default=20, ge=1, le=100)]

@app.get(
    "/users",
    response_model=UserListResponse,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    }
)
async def list_users(
    page: PageNumber = 1,
    per_page: PageSize = 20,
    search: Optional[str] = None,
    role: Optional[str] = None,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(UserModel)
    
    if search:
        query = query.filter(
            or_(UserModel.name.ilike(f"%{search}%"),
                UserModel.email.ilike(f"%{search}%"))
        )
    if role:
        query = query.filter(UserModel.role == role)
    
    # Count total
    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar()
    
    # Paginate
    result = await db.execute(
        query.offset((page - 1) * per_page).limit(per_page)
    )
    items = result.scalars().all()
    
    return UserListResponse(
        items=[UserResponse.model_validate(u) for u in items],
        total=total,
        page=page,
        per_page=per_page,
        total_pages=(total + per_page - 1) // per_page,
    )
```

---

## 4. Background Tasks & Celery

```python
# Built-in FastAPI background tasks (simple, in-process)
from fastapi import BackgroundTasks

def send_welcome_email(email: str, name: str):
    # Runs after response is sent
    email_client.send(to=email, subject="Welcome!", body=f"Hi {name}!")

@app.post("/users")
async def create_user(
    data: CreateUserRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    user = await create_user_in_db(db, data)
    
    # Schedule background task (non-blocking)
    background_tasks.add_task(send_welcome_email, user.email, user.name)
    background_tasks.add_task(index_user_in_search, user.id)
    
    return {"id": user.id}  # Returned immediately!

# Celery (for heavy tasks, retry, scheduling, distributed)
from celery import Celery

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

@celery.task(
    bind=True,
    max_retries=3,
    acks_late=True,        # Acknowledge only after task completes
    autoretry_for=(Exception,),
    retry_backoff=True,    # Exponential backoff
)
def send_email(self, user_id: int, template: str):
    try:
        user = get_user(user_id)
        email_service.send(user.email, template)
    except EmailError as exc:
        raise self.retry(exc=exc, countdown=60)  # Retry in 60s

@celery.task
def process_upload(file_key: str, user_id: int):
    """Heavy image processing task"""
    image = s3.download(file_key)
    thumbnail = generate_thumbnail(image)
    s3.upload(f"thumbnails/{file_key}", thumbnail)
    db.update_user_avatar(user_id, f"thumbnails/{file_key}")

# Trigger from FastAPI
@app.post("/upload")
async def upload_file(file: UploadFile, current_user: UserModel = Depends(get_current_user)):
    key = f"uploads/{uuid4()}/{file.filename}"
    await s3_client.upload(file, key)
    
    # Enqueue Celery task (immediately returns task ID)
    task = process_upload.delay(key, current_user.id)
    
    return {"task_id": task.id, "status": "processing"}

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    result = celery.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }
```

---

## 5. WebSockets

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, WebSocket] = {}
        self.rooms: Dict[str, set[str]] = {}
    
    async def connect(self, room: str, user_id: str, ws: WebSocket):
        await ws.accept()
        self.active[user_id] = ws
        self.rooms.setdefault(room, set()).add(user_id)
    
    def disconnect(self, room: str, user_id: str):
        self.active.pop(user_id, None)
        if room in self.rooms:
            self.rooms[room].discard(user_id)
    
    async def send_to_user(self, user_id: str, data: dict):
        if ws := self.active.get(user_id):
            await ws.send_json(data)
    
    async def broadcast_to_room(self, room: str, data: dict, exclude: str = None):
        user_ids = self.rooms.get(room, set())
        for uid in user_ids:
            if uid != exclude and (ws := self.active.get(uid)):
                try:
                    await ws.send_json(data)
                except Exception:
                    self.disconnect(room, uid)

manager = ConnectionManager()

@app.websocket("/ws/chat/{room_id}")
async def websocket_chat(
    websocket: WebSocket,
    room_id: str,
    token: str,  # Auth via query param
):
    # Authenticate
    try:
        payload = decode_token(token, settings.JWT_SECRET)
        user_id = payload["sub"]
    except HTTPException:
        await websocket.close(code=4001, reason="Unauthorized")
        return
    
    await manager.connect(room_id, user_id, websocket)
    
    try:
        # Notify others
        await manager.broadcast_to_room(
            room_id,
            {"type": "user_joined", "userId": user_id},
            exclude=user_id
        )
        
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "message":
                await manager.broadcast_to_room(
                    room_id,
                    {
                        "type": "message",
                        "userId": user_id,
                        "content": data["content"],
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )
            elif data["type"] == "ping":
                await websocket.send_json({"type": "pong"})
    
    except WebSocketDisconnect:
        manager.disconnect(room_id, user_id)
        await manager.broadcast_to_room(
            room_id,
            {"type": "user_left", "userId": user_id}
        )
```

---

## 6. Middleware & Exception Handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time

# Request logging middleware
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        request_id = str(uuid4())
        
        # Add request ID to state
        request.state.request_id = request_id
        
        response = await call_next(request)
        
        duration = time.time() - start
        logger.info("request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration * 1000, 2),
            request_id=request_id,
        )
        
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        
        return response

# CORS
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com", "https://staging.myapp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting middleware
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.rpm = requests_per_minute
        self.cache: Dict[str, list] = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        window_start = now - 60
        
        requests = [t for t in self.cache.get(client_ip, []) if t > window_start]
        
        if len(requests) >= self.rpm:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"},
                headers={"Retry-After": "60"},
            )
        
        requests.append(now)
        self.cache[client_ip] = requests
        
        return await call_next(request)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)

# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "request_id": getattr(request.state, "request_id", None),
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception",
        error=str(exc),
        request_id=getattr(request.state, "request_id", None),
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

---

## 7. Testing FastAPI

```python
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Override dependencies in tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
test_engine = create_async_engine(TEST_DATABASE_URL)
TestSessionFactory = async_sessionmaker(test_engine, expire_on_commit=False)

async def override_get_db():
    async with TestSessionFactory() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest.fixture
async def auth_headers(client: AsyncClient):
    # Create user and login
    await client.post("/users", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "Password123",
    })
    response = await client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "Password123",
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# Tests
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/users", json={
        "name": "Alice",
        "email": "alice@example.com",
        "password": "Password123",
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert "password" not in data  # Never return password!

@pytest.mark.asyncio
async def test_get_users_requires_auth(client: AsyncClient):
    response = await client.get("/users")
    assert response.status_code == 403  # No token

@pytest.mark.asyncio
async def test_get_users_with_auth(client: AsyncClient, auth_headers: dict):
    response = await client.get("/users", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
```

---

*Tài liệu liên quan: `python/02-python-advanced.md` | `api-design/01-rest-api.md` | `security/03-owasp-top10.md`*
