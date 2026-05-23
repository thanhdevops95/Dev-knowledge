# 🐳 Docker — Container hóa ứng dụng

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Bắt buộc trong mọi dự án hiện đại

---

## Docker là gì?

**Docker** đóng gói ứng dụng và toàn bộ dependencies vào **container** — một môi trường độc lập, chạy nhất quán ở mọi nơi.

**Tại sao cần Docker?**
- **Works on my machine!** → Với Docker: "Works everywhere!"
- **Isolation** — App A không ảnh hưởng App B
- **Dễ deploy** — 1 lệnh deploy lên bất kỳ server nào
- **Microservices** — Mỗi service 1 container
- **CI/CD** — Pipeline test và build nhất quán

---

## Khái niệm cốt lõi

| Khái niệm | Giải thích |
|---|---|
| **Image** | Template read-only, như "bản thiết kế" |
| **Container** | Instance đang chạy của Image |
| **Dockerfile** | File định nghĩa cách build Image |
| **Registry** | Kho lưu Images (Docker Hub, ECR...) |
| **Volume** | Lưu trữ data bền vững |
| **Network** | Mạng riêng cho containers giao tiếp |

---

## Cài đặt

```bash
# macOS
brew install --cask docker

# Kiểm tra
docker --version
docker compose version
```

---

## Lệnh cơ bản

```bash
# Images
docker images                          # Liệt kê images
docker pull nginx                      # Tải image từ Docker Hub
docker rmi nginx:latest                # Xóa image
docker build -t my-app:1.0 .          # Build image từ Dockerfile
docker tag my-app:1.0 registry/my-app:1.0

# Containers
docker run nginx                       # Chạy container
docker run -d nginx                    # Chạy detached (background)
docker run -p 8080:80 nginx           # Map port host:container
docker run -v /data:/app/data nginx   # Mount volume
docker run --name my-nginx nginx       # Đặt tên container

docker ps                              # Containers đang chạy
docker ps -a                           # Tất cả containers
docker stop my-nginx                   # Dừng container
docker start my-nginx                  # Khởi động lại
docker restart my-nginx
docker rm my-nginx                     # Xóa container
docker rm -f my-nginx                  # Force xóa kể cả đang chạy

# Xem thông tin
docker logs my-nginx                   # Xem logs
docker logs -f my-nginx                # Follow logs realtime
docker exec -it my-nginx bash         # SSH vào container
docker inspect my-nginx                # Thông tin chi tiết
docker stats                           # Monitor CPU/RAM realtime
```

---

## Dockerfile

```dockerfile
# ─── Python App ────────────────────────────────────
FROM python:3.12-slim

# Tạo user không phải root (security best practice)
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy dependencies trước (tận dụng layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# ─── Node.js App (Multi-stage build) ───────────────
# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Stage 2: Production (image nhỏ hơn nhiều)
FROM node:20-alpine AS production

WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000
CMD ["node", "dist/index.js"]
```

```dockerfile
# ─── React/Vite App ─────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Dùng nginx để serve static files
FROM nginx:alpine AS production
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## .dockerignore

```
node_modules/
.git/
.env
.env.local
dist/
build/
*.log
Dockerfile
docker-compose.yml
README.md
.DS_Store
```

---

## Docker Compose ⭐

```yaml
# docker-compose.yml
version: '3.9'

services:
  # ── API Backend ──────────────────────────────
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: my-api
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:secret@db:5432/mydb
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=${JWT_SECRET}     # Từ .env file
    volumes:
      - ./api:/app                   # Dev: hot reload
      - /app/.venv                   # Giữ .venv trong container
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - app-network

  # ── Frontend ─────────────────────────────────
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - api
    networks:
      - app-network

  # ── PostgreSQL ───────────────────────────────
  db:
    image: postgres:16-alpine
    container_name: my-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # ── Redis ───────────────────────────────────
  redis:
    image: redis:7-alpine
    container_name: my-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - app-network

  # ── Adminer (DB GUI) ─────────────────────────
  adminer:
    image: adminer:latest
    ports:
      - "8080:8080"
    depends_on:
      - db
    networks:
      - app-network

volumes:
  postgres-data:
  redis-data:

networks:
  app-network:
    driver: bridge
```

```bash
# Lệnh Docker Compose
docker compose up -d               # Start all services detached
docker compose up --build          # Rebuild và start
docker compose down                # Stop và remove containers
docker compose down -v             # + Xóa volumes
docker compose logs -f api         # Follow logs của service
docker compose exec api bash       # Vào container
docker compose ps                  # Xem trạng thái
docker compose restart api         # Restart 1 service
docker compose scale api=3         # Scale service (3 instances)
```

---

## Docker Networking

```bash
# Liệt kê networks
docker network ls

# Tạo network
docker network create my-network

# Connect container vào network
docker network connect my-network my-container

# Trong cùng network: containers giao tiếp qua NAME
# api container có thể gọi: http://db:5432 (không phải localhost!)
```

---

## Best Practices

```dockerfile
# ✅ 1. Dùng image cụ thể, không dùng :latest
FROM python:3.12.0-slim

# ✅ 2. Một RUN = một layer, dùng && để gộp
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# ✅ 3. Copy package files trước, code sau (tận dụng cache)
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ✅ 4. Dùng .dockerignore
# ✅ 5. Không chạy với root user
# ✅ 6. Multi-stage build để giảm size
# ✅ 7. Healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8000/health || exit 1
```

---

## Bài tập thực hành

- [ ] Dockerize một app Python/Node.js của bạn
- [ ] Tạo docker-compose.yml với App + Database + Redis
- [ ] Viết multi-stage Dockerfile, so sánh kích thước image
- [ ] Setup hot reload cho development với volumes

---

## Tài nguyên thêm

- [Docker Docs](https://docs.docker.com/) — Tài liệu chính thức
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dive](https://github.com/wagoodman/dive) — Tool phân tích Docker image layers
