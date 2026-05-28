# 🐳 Docker — Container hóa ứng dụng

> `[BEGINNER → INTERMEDIATE]` ⭐ `[MUST-KNOW]` — "Trên máy tôi chạy được" → "Ở đâu cũng chạy được"

---

## Tại sao cần Docker?

**Vấn đề kinh điển:**

```
Developer: "Trên máy tôi chạy OK mà!" 🤷
Ops:       "Trên server nó crash!" 💥

Lý do:
- Máy dev: Python 3.11, máy server: Python 3.8
- Dev dùng macOS, server dùng Ubuntu
- Dev có env vars khác server
- Thư viện system khác version
```

**Docker giải quyết:** Đóng gói app + dependencies + OS vào 1 **container** → chạy giống hệt ở mọi nơi.

---

## 1. Container vs VM

```
Virtual Machine:                    Container:
┌─────────────────────┐            ┌────────────────────┐
│ App A │ App B │ App C│            │ App A │ App B │App C│
├───────┼───────┼──────┤            ├───────┼───────┼─────┤
│Guest  │Guest  │Guest │            │ Bins/ │ Bins/ │Bins/│
│OS     │OS     │OS    │            │ Libs  │ Libs  │Libs │
├───────┴───────┴──────┤            ├───────┴───────┴─────┤
│     Hypervisor       │            │    Docker Engine     │
├──────────────────────┤            ├─────────────────────┤
│      Host OS         │            │      Host OS        │
├──────────────────────┤            ├─────────────────────┤
│     Hardware         │            │     Hardware        │
└──────────────────────┘            └─────────────────────┘
  Nặng (~GB), chậm khởi động         Nhẹ (~MB), khởi động <1s
```

| | VM | Container |
|---|---|---|
| **Kích thước** | GB | MB |
| **Khởi động** | Phút | Giây |
| **Isolation** | Mạnh (full OS) | Tốt (nhân OS chung) |
| **Performance** | ~5-10% overhead | Gần native |
| **Use case** | Chạy nhiều OS khác nhau | Deploy microservices |

---

## 2. Docker Image vs Container

```
Dockerfile → Image → Container(s)

Dockerfile: Công thức nấu ăn (recipe)
Image:      Đĩa CD (template, read-only)
Container:  Máy tính đang chạy CD đó (instance, read-write)

1 Image → Tạo nhiều Container (giống 1 class → nhiều objects)
```

---

## 3. Dockerfile — Viết "công thức"

```dockerfile
# Chọn base image
FROM node:20-alpine

# Metadata
LABEL maintainer="an@example.com"

# Thư mục làm việc trong container
WORKDIR /app

# Copy package files trước (tận dụng cache)
COPY package.json package-lock.json ./

# Cài dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Expose port (documentation)
EXPOSE 3000

# Biến môi trường
ENV NODE_ENV=production

# Lệnh chạy khi container start
CMD ["node", "server.js"]
```

### Multi-stage Build — Giảm kích thước image

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production (chỉ copy kết quả build)
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/server.js"]

# Image build: ~1GB → Production image: ~150MB
```

---

## 4. Lệnh Docker cơ bản

```bash
# === IMAGE ===
docker build -t myapp:1.0 .          # Build image từ Dockerfile
docker images                         # Liệt kê images
docker pull nginx:alpine              # Tải image từ Docker Hub
docker rmi myapp:1.0                  # Xóa image

# === CONTAINER ===
docker run -d --name web -p 3000:3000 myapp:1.0   # Chạy container
docker ps                              # Container đang chạy
docker ps -a                           # Tất cả container (kể cả stopped)
docker stop web                        # Dừng
docker start web                       # Chạy lại
docker rm web                          # Xóa container
docker logs web                        # Xem logs
docker exec -it web sh                 # Vào shell container

# === DOCKER COMPOSE ===
docker compose up -d                   # Chạy tất cả services
docker compose down                    # Dừng và xóa
docker compose logs -f                 # Xem logs real-time
```

---

## 5. Docker Compose — Chạy multi-container

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Web application
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    restart: unless-stopped

  # PostgreSQL database
  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    ports:
      - "5432:5432"

  # Redis cache
  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  # Nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app

volumes:
  postgres_data:
```

```bash
# Chạy toàn bộ stack
docker compose up -d

# Xem logs
docker compose logs app -f

# Scale service
docker compose up -d --scale app=3
```

---

## 6. Volumes — Persistent Storage

```bash
# Container bị xóa → dữ liệu mất!
# Volume lưu dữ liệu BÊN NGOÀI container

# Named volume (Docker quản lý)
docker run -v mydata:/var/lib/postgresql/data postgres

# Bind mount (gắn folder host → container)
docker run -v $(pwd)/src:/app/src myapp   # Hot reload dev!

# Trong Compose:
volumes:
  - ./src:/app/src          # Bind mount (dev)
  - postgres_data:/data     # Named volume (production)
```

---

## 7. Networking

```bash
# Docker tạo network riêng cho mỗi compose project
# Các container cùng network giao tiếp qua TÊN service

# app kết nối db:
DATABASE_URL=postgres://user:pass@db:5432/mydb
#                                  ↑ tên service, KHÔNG phải localhost!

# Các loại network:
# bridge (default): container trong cùng host giao tiếp
# host:   container dùng chung network host (không isolation)
# none:   không network
```

---

## 8. Best Practices

```dockerfile
# ✅ Dùng alpine image (nhỏ)
FROM node:20-alpine    # ~50MB thay vì ~1GB

# ✅ Non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# ✅ .dockerignore (giống .gitignore)
# .dockerignore:
node_modules
.git
.env
*.md

# ✅ Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:3000/health || exit 1

# ✅ Copy package.json trước source (layer caching)
COPY package*.json ./
RUN npm ci
COPY . .           # Source thay đổi → chỉ rebuild từ đây
```

---

## Các lỗi thường gặp

```
❌ Sai: Dùng latest tag → version không xác định
✅ Đúng: Pin version cụ thể — FROM node:20.11-alpine

❌ Sai: Chạy container as root
✅ Đúng: Tạo non-root user trong Dockerfile

❌ Sai: Lưu secrets trong image (ENV PASSWORD=123)
✅ Đúng: Dùng Docker secrets hoặc .env file (không commit!)

❌ Sai: Không dùng .dockerignore → image cực lớn
✅ Đúng: Exclude node_modules, .git, logs
```

---

## Bài tập thực hành

- [ ] Dockerize 1 Node.js/Python app — viết Dockerfile, build, run
- [ ] Tạo docker-compose.yml: app + database + redis
- [ ] Implement multi-stage build — so sánh kích thước image
- [ ] Dùng bind mount để hot-reload code trong development

---

## Tài nguyên thêm

- [Docker Official Docs](https://docs.docker.com/) — Tài liệu chính thức
- [Docker Curriculum](https://docker-curriculum.com/) — Beginner-friendly
- [Play with Docker](https://labs.play-with-docker.com/) — Thực hành online miễn phí
