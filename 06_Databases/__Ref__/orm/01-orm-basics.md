# 🗄️ ORM — SQLAlchemy & Prisma

> `[INTERMEDIATE]` — Làm việc với database mà không viết SQL thô

---

## ORM là gì?

**ORM (Object-Relational Mapper)** = Lớp trung gian ánh xạ giữa **objects trong code** và **rows trong database**.

```
Python/JS Object  ←──── ORM ────→  Database Row
                   (translate)
user.name = "Jesse"  →  UPDATE users SET name='Jesse' WHERE id=1
```

**Lợi ích:**
- Không cần viết SQL thủ công (ít bug, dễ đọc)
- Database abstraction — đổi DB không cần sửa nhiều code
- Validation ở model level
- Migration tự động

**Khi nào vẫn cần SQL thuần:**
- Query phức tạp (window functions, CTEs)
- Performance critical paths
- Bulk operations

---

## SQLAlchemy 2.0 (Python)

```bash
pip install sqlalchemy asyncpg alembic
```

### Định nghĩa Models

```python
# models/base.py
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import uuid

class Base(DeclarativeBase):
    pass

# models/user.py
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    # Relationship
    author: Mapped[User] = relationship("User", back_populates="posts")
```

### Async Session & CRUD

```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/mydb"
engine = create_async_engine(DATABASE_URL, echo=False, pool_size=10)
SessionFactory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with SessionFactory() as session:
        yield session
```

```python
# repositories/user_repo.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from models.user import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_by_id(self, user_id: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def find_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def find_all(
        self,
        page: int,
        limit: int,
        search: str = ""
    ) -> tuple[list[User], int]:
        query = select(User)
        count_query = select(func.count(User.id))

        if search:
            query = query.where(User.name.ilike(f"%{search}%"))
            count_query = count_query.where(User.name.ilike(f"%{search}%"))

        query = query.offset((page - 1) * limit).limit(limit)

        result = await self.db.execute(query)
        count = await self.db.execute(count_query)

        return result.scalars().all(), count.scalar()

    async def create(self, name: str, email: str, password_hash: str) -> User:
        user = User(name=name, email=email, password_hash=password_hash)
        self.db.add(user)
        await self.db.flush()  # Ghi vào DB trong transaction hiện tại
        await self.db.refresh(user)  # Load lại giá trị từ DB
        return user

    async def update(self, user_id: str, **fields) -> User | None:
        await self.db.execute(
            update(User).where(User.id == user_id).values(**fields)
        )
        return await self.find_by_id(user_id)

    async def delete(self, user_id: str) -> None:
        await self.db.execute(delete(User).where(User.id == user_id))
```

### Alembic — Migrations

```bash
# Khởi tạo
alembic init alembic

# Tạo migration
alembic revision --autogenerate -m "create users table"

# Chạy migrations
alembic upgrade head

# Rollback 1 bước
alembic downgrade -1

# Xem history
alembic history
```

---

## Prisma (Node.js / TypeScript)

```bash
npm install prisma @prisma/client
npx prisma init  # Tạo prisma/schema.prisma
```

### Schema định nghĩa

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  name      String
  email     String   @unique
  password  String
  role      Role     @default(USER)
  isActive  Boolean  @default(true)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  posts    Post[]
  comments Comment[]

  @@map("users")
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String
  published Boolean  @default(false)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  author   User   @relation(fields: [authorId], references: [id])
  authorId String

  tags     Tag[]
  comments Comment[]

  @@index([authorId])
  @@map("posts")
}

model Comment {
  id        Int      @id @default(autoincrement())
  content   String
  createdAt DateTime @default(now())

  author   User   @relation(fields: [authorId], references: [id])
  authorId String

  post   Post @relation(fields: [postId], references: [id])
  postId Int

  @@map("comments")
}

model Tag {
  id    Int    @id @default(autoincrement())
  name  String @unique
  posts Post[]

  @@map("tags")
}

enum Role {
  USER
  MODERATOR
  ADMIN
}
```

### Migrations

```bash
# Tạo và apply migration
npx prisma migrate dev --name "create_users_table"

# Apply lên production
npx prisma migrate deploy

# Xem database trong browser
npx prisma studio

# Generate types sau khi thay đổi schema
npx prisma generate
```

### Prisma Client — CRUD

```typescript
import { PrismaClient, Prisma } from '@prisma/client'

const prisma = new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query'] : []
})

// Create
const user = await prisma.user.create({
  data: {
    name: 'Jesse',
    email: 'jesse@example.com',
    password: hashedPassword,
    posts: {
      create: [{ title: 'First Post', content: 'Hello!' }]
    }
  },
  include: { posts: true }
})

// Read
const user = await prisma.user.findUnique({
  where: { email: 'jesse@example.com' },
  include: {
    posts: {
      where: { published: true },
      orderBy: { createdAt: 'desc' },
      take: 10
    }
  }
})

// List với pagination và filtering
const [users, total] = await prisma.$transaction([
  prisma.user.findMany({
    where: {
      isActive: true,
      name: { contains: search, mode: 'insensitive' }
    },
    orderBy: { createdAt: 'desc' },
    skip: (page - 1) * limit,
    take: limit,
    select: {
      id: true,
      name: true,
      email: true,
      role: true,
      createdAt: true
      // Không select password!
    }
  }),
  prisma.user.count({
    where: { isActive: true }
  })
])

// Update
const updated = await prisma.user.update({
  where: { id: userId },
  data: { name: 'New Name', updatedAt: new Date() }
})

// Delete
await prisma.user.delete({ where: { id: userId } })

// Transaction
await prisma.$transaction(async (tx) => {
  const order = await tx.order.create({ data: orderData })
  await tx.product.updateMany({
    where: { id: { in: items.map(i => i.productId) } },
    data: { stock: { decrement: 1 } }
  })
  return order
})
```

---

## So sánh ORM

| | Prisma | SQLAlchemy | TypeORM | GORM (Go) |
|---|---|---|---|---|
| **Language** | Node.js/TS | Python | Node.js/TS | Go |
| **Type-safety** | ✅ Xuất sắc | ✅ Tốt | 🟡 Ổn | 🟡 Ổn |
| **Migration** | ✅ Prisma Migrate | ✅ Alembic | 🟡 Ổn | ✅ Auto |
| **Schema** | Schema file | Python models | Decorators | Go structs |
| **Khuyên dùng** | Dự án TypeScript mới | Python apps | Legacy | Go |

---

## Bài tập thực hành

- [ ] Định nghĩa schema Blog (User, Post, Comment, Tag) với Prisma
- [ ] Implement CRUD repository với SQLAlchemy async
- [ ] Tạo migration khi thêm field mới
- [ ] N+1 query problem: detect và fix với `include`

---

## Tài nguyên thêm

- [Prisma Docs](https://www.prisma.io/docs) — Rất chi tiết
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/en/20/)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
