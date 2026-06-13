# 🎓 Database với SQLModel — CRUD thực tế

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.2\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 13/06/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [Pydantic Models](02_pydantic-models.md) + [SQL Schema Design](../../../../../06_databases/sql-fundamentals/lessons/01_basic/05_schema-design-basics.md)

> 🎯 *Ghép FastAPI + database thật. Học **SQLModel** (Sebastián Ramírez, kết hợp SQLAlchemy + Pydantic), **Dependency Injection** (`Depends`), **session lifecycle**, viết CRUD đầy đủ với **PostgreSQL/SQLite**. Migration với **Alembic**.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **SQLModel** vs SQLAlchemy + raw SQL
- [ ] Setup **Postgres** local + **DATABASE_URL**
- [ ] Định nghĩa model bảng với `Field(primary_key=True)`
- [ ] Dùng **`Depends(get_session)`** đúng cách
- [ ] Viết CRUD đầy đủ: Create / Read list / Read one / Update / Delete
- [ ] Hiểu **session lifecycle** (open/commit/close)
- [ ] Quan hệ 1-N (User → Orders) với `Relationship()`
- [ ] Migration với **Alembic** (intro)

---

## Tình huống — Bạn cần data lưu thật, không in-memory list

Bài 01-02 bạn dùng `products_db: list[dict]` — **mất hết khi server restart**. Production cần:
- 🗄️ Lưu thật vào **PostgreSQL/SQLite**
- 🔄 Mỗi request **session độc lập** (DI)
- 🛡️ Migration **versioning schema** (Alembic)
- 🔗 **Relationship**: User có nhiều Orders

Bạn thử dùng SQLAlchemy raw — nhưng phải maintain **2 model** (Pydantic + SQLAlchemy) trùng nhau.

Senior chỉ:
> *"Dùng **SQLModel** — cùng tác giả FastAPI. 1 model làm cả Pydantic schema + SQLAlchemy table. Không trùng."*

→ Bài này dạy SQLModel + FastAPI CRUD đầy đủ.

---

## 1️⃣ SQLModel — best of both worlds

**SQLModel** = thư viện Sebastián Ramírez (2021) **gộp** SQLAlchemy + Pydantic thành **1 lớp duy nhất**.

| Cách cũ — 2 model | Cách mới — SQLModel |
|---|---|
| Pydantic `UserSchema(BaseModel)` + SQLAlchemy `User(Base)` | 1 class `User(SQLModel, table=True)` |
| Tự convert giữa 2 lớp | Tự convert (cùng class) |
| Trùng field, phải sync tay | 1 nguồn truth |

```python
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):       # ← table=True → tạo bảng DB
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    age: int | None = None
```

→ Vừa là **Pydantic model** (validate, OpenAPI) vừa là **SQLAlchemy table** (DB CRUD).

### Cài đặt

Cài SQLModel + driver phù hợp với DB. Dev local thường dùng SQLite (built-in Python, không cần extra), production dùng Postgres với `psycopg2-binary`. Một lệnh pip:

```bash
pip install "sqlmodel" "psycopg2-binary"        # Postgres
# Hoặc dùng SQLite (mặc định Python — không cần psycopg2)
```

---

## 2️⃣ Setup DB connection

### `app/db/database.py`

Module DB cô lập 3 thứ cốt lõi: `engine` (connection pool), `init_db()` (tạo bảng dev), `get_session()` (dependency factory). Pattern này tách connection management khỏi business logic:

```python
from sqlmodel import SQLModel, create_engine, Session

# DATABASE_URL từ env
import os
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./app.db"        # Default SQLite cho dev
    # "postgresql+psycopg2://user:pass@localhost:5432/mydb"   # Postgres production
)

engine = create_engine(
    DATABASE_URL,
    echo=True,                  # Log SQL queries — tắt production
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

def init_db():
    SQLModel.metadata.create_all(engine)        # Tạo mọi bảng (chỉ dùng dev, prod dùng Alembic)

def get_session():
    with Session(engine) as session:
        yield session
```

→ `get_session()` là **dependency** — mỗi request 1 session độc lập, auto close.

### `app/main.py`

`main.py` setup FastAPI app + lifespan hook (chạy `init_db()` khi server start). Modern FastAPI dùng `lifespan` thay `@app.on_event("startup")` cũ (deprecated 2024):

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()                # Run khi server start
    yield
    # cleanup khi shutdown (nếu cần)

app = FastAPI(lifespan=lifespan)
```

→ FastAPI **lifespan** thay cho `@app.on_event("startup")` cũ (đã deprecated từ 2024).

---

## 3️⃣ Tách model: Database vs API

### Pattern khuyên dùng

Tách **4 model class** từ chung `UserBase` — Base (fields shared), Table (cho DB), Create/Read/Update (cho API). Pattern này tránh leak password ra response + cho phép validate khác nhau cho từng use case:

```python
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

# --- Base — fields chung ---
class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    name: str
    age: int | None = None

# --- DB table ---
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    password_hash: str                        # ← chỉ ở DB
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# --- API Request (Create) ---
class UserCreate(UserBase):
    password: str                              # ← client gửi plaintext, server hash

# --- API Request (Update) ---
class UserUpdate(SQLModel):
    email: str | None = None
    name: str | None = None
    age: int | None = None

# --- API Response (Read) ---
class UserRead(UserBase):
    id: int
    created_at: datetime
    # KHÔNG có password_hash!
```

→ Vẫn pattern 3-model của [bài 02](02_pydantic-models.md), nhưng giờ chia chuẩn cho ORM.

---

## 4️⃣ CRUD endpoint đầy đủ

### `app/api/users.py`

CRUD endpoints với SQLModel — pattern repetitive cho 5 method: POST/GET-list/GET-one/PATCH/DELETE. Tất cả đều inject `session` qua dependency `Depends(get_session)`:

```python
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from app.db.database import get_session
from app.models import User, UserCreate, UserRead, UserUpdate
from app.core.security import hash_password   # bcrypt/argon2 (bài 04)

router = APIRouter(prefix="/users", tags=["users"])

# --- CREATE ---
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(
        email=user.email,
        name=user.name,
        age=user.age,
        password_hash=hash_password(user.password)
    )
    session.add(db_user)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(409, "Email đã tồn tại")
    session.refresh(db_user)        # Load id auto-generated
    return db_user

# --- LIST ---
@router.get("/", response_model=list[UserRead])
def list_users(
    skip: int = 0,
    limit: int = 20,
    session: Session = Depends(get_session)
):
    statement = select(User).offset(skip).limit(limit).order_by(User.id)
    users = session.exec(statement).all()
    return users

# --- GET ONE ---
@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User không tồn tại")
    return user

# --- UPDATE ---
@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    update_data: UserUpdate,
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404)

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# --- DELETE ---
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404)
    session.delete(user)
    session.commit()
```

→ 5 endpoint chuẩn REST, dùng DB thật, session độc lập mỗi request, transaction handle đúng (commit/rollback).

Khái niệm trừu tượng nhất ở đây là **chuỗi biến đổi data** — từ HTTP request qua session/ORM xuống SQL rồi quay ngược lại thành JSON:

```mermaid
flowchart LR
    C["Client request"] --> E["Endpoint"]
    D["Depends(get_session)"] -.->|"inject Session"| E
    E -->|"select() / get()"| S["SQLModel (ORM)"]
    S -->|"SQL"| PG[("Postgres / SQLite")]
    PG -->|"rows"| S
    S -->|"ORM object"| E
    E -->|"response_model → JSON"| C
```

→ Endpoint không bao giờ chạm SQL trực tiếp — SQLModel dịch 2 chiều (Python ↔ SQL), còn session do DI cấp riêng cho từng request rồi tự đóng.

---

## 5️⃣ `select()` query — SQL Pythonic

SQLModel dùng SQLAlchemy 2.0 syntax — sạch hơn ORM cũ.

### Basic

```python
statement = select(User).where(User.email == "nguyenvana@ex.com")
user = session.exec(statement).first()      # 1 row hoặc None
```

### Filter nhiều điều kiện

```python
statement = (
    select(User)
    .where(User.age >= 25)
    .where(User.name.like("L%"))
    .order_by(User.created_at.desc())
    .limit(10)
)
users = session.exec(statement).all()
```

### Aggregations

```python
from sqlmodel import func

statement = select(func.count(User.id)).where(User.age > 30)
count = session.exec(statement).one()
```

### JOIN (preview, advanced ở intermediate)

```python
statement = (
    select(Order, User)
    .join(User, Order.user_id == User.id)
    .where(User.status == "active")
)
results = session.exec(statement).all()
```

→ Pattern + syntax: gần với SQL ở [bài 03 JOINs SQL fundamentals](../../../../../06_databases/sql-fundamentals/lessons/01_basic/03_joins.md).

---

## 6️⃣ Relationship — 1-N (User → Orders)

```python
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    # back-ref: User.orders trả về list[Order]
    orders: list["Order"] = Relationship(back_populates="user")

class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: int
    user_id: int | None = Field(default=None, foreign_key="user.id", index=True)

    # forward: Order.user trả về User
    user: User | None = Relationship(back_populates="orders")
```

### Query relationship

```python
user = session.get(User, 1)
print(user.orders)             # ← list[Order] tự load (lazy)

order = session.get(Order, 100)
print(order.user)              # ← User của order
```

### Nest relationship trong Response

```python
class OrderRead(SQLModel):
    id: int
    amount: int

class UserReadWithOrders(UserRead):
    orders: list[OrderRead] = []

@app.get("/users/{id}/full", response_model=UserReadWithOrders)
def get_user_full(id: int, session: Session = Depends(get_session)):
    return session.get(User, id)        # Pydantic tự include orders
```

---

## 7️⃣ Session lifecycle — quan trọng phải hiểu

```python
def get_session():
    with Session(engine) as session:
        yield session
        # Sau yield: __exit__ tự rollback uncommit + close
```

| Bước | Khi nào |
|---|---|
| `Session(engine)` | Mỗi request — instance mới |
| `yield session` | Truyền vào endpoint qua Depends |
| `session.commit()` | Trong endpoint — save changes |
| `session.rollback()` | Trong endpoint khi exception |
| `session.close()` | Tự khi context manager exit |

→ **1 request = 1 session = 1 transaction** (thường). Đừng share session giữa request.

### Async session (option)

```python
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine("postgresql+asyncpg://...")

async def get_session():
    async with AsyncSession(engine) as session:
        yield session

# Endpoint
@router.get("/users/{id}")
async def get_user(id: int, session: AsyncSession = Depends(get_session)):
    return await session.get(User, id)
```

→ Cần thiết khi DB driver async (asyncpg). Performance tốt hơn cho I/O-bound.

---

## 8️⃣ Migration với Alembic — versioning schema

`init_db()` chỉ tạo bảng **lần đầu**. Sau khi đã có data, đổi schema (thêm cột, đổi type) phải qua **migration**.

### Setup

```bash
pip install alembic
alembic init alembic
# Edit alembic/env.py để dùng metadata SQLModel + DATABASE_URL từ env
```

### Workflow

```bash
# Tự sinh migration từ diff giữa model và DB
alembic revision --autogenerate -m "add user.age column"

# Apply
alembic upgrade head

# Rollback 1 step
alembic downgrade -1
```

→ Mỗi migration là 1 file Python `versions/xxxxx_add_user_age_column.py` — version control được, deploy được.

> ⚠️ **Production rule**: KHÔNG dùng `SQLModel.metadata.create_all(engine)` ở production. Mọi schema change qua Alembic.

→ Alembic chi tiết là cluster riêng. Beginner: biết tồn tại, bắt đầu khi project lên production.

---

## 9️⃣ Connect Postgres thực tế

### Setup Postgres local (Docker)

```bash
docker run --name pg-dev \
  -e POSTGRES_USER=myapp \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=myapp \
  -p 5432:5432 \
  -d postgres:16
```

### `.env`

```env
DATABASE_URL=postgresql+psycopg2://myapp:secret@localhost:5432/myapp
```

### Connect

```python
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False, pool_size=10, max_overflow=20)
```

→ **Connection pool** với `pool_size=10` = giữ 10 connection ready (tránh re-connect mỗi request).

---

## 1️⃣0️⃣ Ghép tất cả — cấu trúc project hoàn chỉnh

```
myapp/
├── app/
│   ├── main.py              # FastAPI + lifespan
│   ├── db/
│   │   └── database.py      # engine + get_session()
│   ├── models/
│   │   ├── user.py          # User + UserCreate + UserRead + UserUpdate
│   │   └── order.py
│   ├── api/
│   │   ├── users.py         # router users
│   │   └── orders.py
│   └── core/
│       └── security.py      # hash_password + verify_password (bài 04)
├── alembic/                  # Migration files
├── .env
└── requirements.txt
```

→ Bạn bây giờ có **backend production-ready** với DB persistent. Bài cuối cluster sẽ thêm **auth (JWT) + CORS + middleware**.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Share session global** → race condition, transaction lẫn. **1 request = 1 session** qua DI.
2. **Quên `session.commit()`** → DB rollback khi request kết thúc, data bị mất.
3. **Quên `session.refresh(obj)` sau commit** → `obj.id` vẫn `None`. Refresh để load fields auto-generated.
4. **`create_all` ở production** → conflict với data thật, schema không versioning. Dùng Alembic.
5. **Connection leak** — không dùng `with Session(...)` hoặc DI → connection pool cạn.

---

## 🧠 Tự kiểm tra (Self-check)

1. SQLModel khác gì SQLAlchemy + Pydantic riêng?
2. `Depends(get_session)` làm gì?
3. Sau `session.commit()`, vì sao cần `session.refresh(obj)`?
4. Relationship `User.orders` trong SQLModel cần config gì?
5. Vì sao không dùng `SQLModel.metadata.create_all()` ở production?

<details>
<summary>Gợi ý đáp án</summary>

1. SQLModel **gộp** Pydantic (validation, OpenAPI) + SQLAlchemy (ORM, DB). 1 class duy nhất `User(SQLModel, table=True)` thay vì 2 class trùng nhau. Cùng tác giả FastAPI (Sebastián Ramírez).

2. `Depends(get_session)` = **dependency injection**. Mỗi request, FastAPI gọi `get_session()` → tạo session mới → inject vào endpoint. Sau endpoint xong, context manager tự close session. Không leak, không share.

3. `session.refresh(obj)` **fetch lại** values từ DB. Cần khi `id` được DB auto-generate (`primary_key`) hoặc `default_factory=lambda: datetime.now(timezone.utc)` server-side. Trước refresh, `obj.id` là None.

4. Cả 2 phía: `User.orders: list["Order"] = Relationship(back_populates="user")` + `Order.user: User | None = Relationship(back_populates="orders")` + `Order.user_id: int | None = Field(foreign_key="user.id")`. `back_populates` link 2 phía để SQLModel biết là 1-N (không phải 2 relationship độc lập).

5. (a) Tạo bảng **không versioning** — không track ai thay đổi gì. (b) Conflict khi schema thay đổi mà data đã có. (c) Không rollback được. Production dùng **Alembic** — migration file Python, version control git, deploy như code.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Setup nhanh

```python
from sqlmodel import SQLModel, Field, Session, create_engine, select

engine = create_engine("sqlite:///./app.db")

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str

SQLModel.metadata.create_all(engine)
```

### DI session

```python
def get_session():
    with Session(engine) as session:
        yield session

@app.get("/users/{id}")
def get_user(id: int, session: Session = Depends(get_session)):
    return session.get(User, id)
```

### CRUD 1-liner

```python
# Create
user = User(email="x@y.com", name="Nguyen Van A")
session.add(user); session.commit(); session.refresh(user)

# Get by ID
user = session.get(User, 1)

# List
users = session.exec(select(User).limit(20)).all()

# Filter
users = session.exec(select(User).where(User.age >= 25)).all()

# Update
user.name = "Le Van B"; session.add(user); session.commit()

# Delete
session.delete(user); session.commit()
```

### Migration commands

```bash
alembic revision --autogenerate -m "msg"
alembic upgrade head
alembic downgrade -1
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **ORM** | Object-Relational Mapper — code object ↔ table |
| **SQLAlchemy** | ORM Python phổ biến nhất |
| **SQLModel** | Gộp SQLAlchemy + Pydantic, do tác giả FastAPI |
| **`Field()`** | Annotation cho column (primary_key, index, ...) |
| **`Relationship()`** | Quan hệ 1-1 / 1-N / M-N giữa model |
| **`Session`** | Context query DB, 1 transaction |
| **`engine`** | Connection pool tới DB |
| **`Depends()`** | FastAPI dependency injection |
| **`select()`** | Build query SQL Pythonic |
| **Alembic** | Migration tool versioning DB schema |
| **Lifespan** | FastAPI event startup/shutdown |
| **Connection pool** | Reuse DB connection cho nhiều request |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [Pydantic Models — Validation + Serialization của FastAPI](02_pydantic-models.md)
- ➡️ **Bài tiếp theo:** [Auth & Middleware — JWT, OAuth2, CORS, Logging](04_auth-and-middleware.md)
- ↑ **Về cụm:** [python-fastapi README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [SQL Schema Design](../../../../../06_databases/sql-fundamentals/lessons/01_basic/05_schema-design-basics.md) — concept PK/FK/index từ SQL fundamentals
- [SQL INSERT/UPDATE/DELETE](../../../../../06_databases/sql-fundamentals/lessons/01_basic/04_insert-update-delete.md) — transaction + soft delete

### 🌐 Tài nguyên tham khảo khác
- 📖 [SQLModel docs](https://sqlmodel.tiangolo.com/) — tutorial chính thức
- 📖 [SQLAlchemy 2.0 docs](https://docs.sqlalchemy.org/)
- 📖 [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- 📖 [FastAPI — SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)

---

> 🎯 *Sau bài này backend bạn lưu data thật, CRUD đầy đủ, schema versioning. Bài cuối cluster dạy **auth JWT + CORS + middleware** — biến backend từ "open" sang "secure".*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `python-fastapi/` lesson 4/5. Cover: SQLModel (Pydantic + SQLAlchemy gộp) + engine setup + Session dependency + lifespan startup + 4-model pattern (Base/Table/Create/Read) + CRUD endpoints + Alembic migration intro.
- **v1.1.0 (25/05/2026)** — Bổ sung câu dẫn nhập cho §1 Cài SQLModel, §2 database.py + main.py, §3 Pattern khuyên dùng, §4 users.py API. Chuẩn hóa placeholder tên trong code mẫu. Thêm mục Changelog.
- **v1.1.1 (11/06/2026)** — Bổ sung sơ đồ luồng request → session → SQLModel → SQL → JSON cho trực quan.
- **v1.1.2 (13/06/2026)** — Sửa lỗi factual: `default_factory=datetime.utcnow` → `lambda: datetime.now(timezone.utc)` (`utcnow` deprecated từ Python 3.12).
