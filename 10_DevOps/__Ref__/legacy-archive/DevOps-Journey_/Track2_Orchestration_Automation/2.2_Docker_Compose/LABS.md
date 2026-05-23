# 🔬 Labs: Docker Compose

> **Hands-on Labs for Docker Compose**
>
> *Bài thực hành Docker Compose.*

---

## 🔬 Lab 1: Basic Stack

### Objective

Deploy NGINX + Node.js + PostgreSQL stack.

### Steps

```yaml
# docker-compose.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api

  api:
    build: ./api
    environment:
      - DATABASE_URL=postgres://postgres:secret@db:5432/app
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: app
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

```bash
docker compose up -d
docker compose ps
docker compose logs api
```

---

## 🔬 Lab 2: Development Workflow

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev
```

```bash
# Hot reload development
docker compose up
# Edit code - changes reflect automatically
```

---

## 🔬 Lab 3: Multiple Environments

```yaml
# docker-compose.yml (base)
services:
  api:
    build: ./api

# docker-compose.dev.yml
services:
  api:
    volumes:
      - ./api:/app
    environment:
      - DEBUG=true

# docker-compose.prod.yml  
services:
  api:
    image: registry/api:${VERSION}
    restart: always
```

```bash
# Development
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
VERSION=1.0.0 docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 🔬 Lab 4: Networking

```yaml
version: '3.8'

services:
  frontend:
    image: nginx
    networks:
      - public

  api:
    build: ./api
    networks:
      - public
      - private

  db:
    image: postgres:15-alpine
    networks:
      - private

networks:
  public:
  private:
    internal: true
```

---

## 🔬 Lab 5: Health Checks

```yaml
services:
  api:
    build: ./api
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

---

## 🔬 Lab 6: Full Stack Application

```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - api

  api:
    build: ./api
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/app
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache

  db:
    image: postgres:15-alpine
    volumes:
      - db-data:/var/lib/postgresql/data

  cache:
    image: redis:7-alpine

  adminer:
    image: adminer
    ports:
      - "8080:8080"

volumes:
  db-data:
```

---

## ✅ Checklist

- [ ] Lab 1: Basic Stack
- [ ] Lab 2: Development Workflow
- [ ] Lab 3: Multiple Environments
- [ ] Lab 4: Networking
- [ ] Lab 5: Health Checks
- [ ] Lab 6: Full Stack

---

## ✅ General Verification (Kiểm chứng tổng quát)

Verify Docker Compose is working:

*(Xác nhận Docker Compose hoạt động:)*

```bash
# Check all services running (Kiểm tra tất cả services chạy)
docker compose ps

# Check logs for errors (Kiểm tra logs có lỗi)
docker compose logs --tail=20

# Test connectivity (Kiểm tra kết nối)
curl http://localhost:3000
curl http://localhost:8080

# Check networks (Kiểm tra networks)
docker network ls | grep compose
```

---

## 🔧 General Troubleshooting (Xử lý sự cố chung)

| Issue | Solution |
|-------|----------|
| `Service unhealthy` | Check health check command, increase start_period *(Kiểm tra lệnh health check)* |
| `Volume permission denied` | Check user ID matches, use `user:` directive *(Kiểm tra UID)* |
| `Port already in use` | Change host port or stop conflicting service *(Đổi port hoặc dừng service khác)* |
| `Cannot connect to database` | Wait for db healthy, check connection string *(Đợi db healthy)* |
| `Build failed` | Check Dockerfile, run `docker compose build --no-cache` *(Build lại từ đầu)* |

---

## 🧹 General Cleanup (Dọn dẹp tổng quát)

```bash
# Stop all services (Dừng tất cả services)
docker compose down

# Stop and remove volumes (Dừng và xóa volumes)
docker compose down -v

# Remove all including orphans (Xóa tất cả kể cả orphans)
docker compose down -v --remove-orphans

# Remove built images (Xóa images đã build)
docker compose down --rmi local

# Full cleanup (Dọn dẹp hoàn toàn)
docker compose down -v --rmi all --remove-orphans
```

---

**[← Back to README](./README.md)**

