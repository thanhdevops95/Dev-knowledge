# 🐳 Docker — Advanced Topics

---

## 📋 Metadata

- **Parent Lesson:** [../README.md](../README.md)
- **Level:** `[ADVANCED]`
- **Prerequisites:** [Lesson 03: Dockerfile Basics](../03-Dockerfile-Basics/lesson.md)
- **Estimated Time:** 2-3 giờ
- **Last Updated:** 30/04/2026
- **Author:** Mr.Rom

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành, bạn sẽ có thể:

- [ ] Viết multi-stage Dockerfile tối ưu cho various languages (Node.js, Python, Go)
- [ ] Tối ưu layer caching và hiểu BuildKit
- [️ ] Viết Docker Compose với healthcheck, resource limits, logging
- [ ] Configure Docker networking (bridge, host, overlay)
- [ ] Quản lý volumes (named, bind, tmpfs, backup/restore)
- [ ] Apply security best practices (non-root, capabilities, read-only)
- [ ] Build multi-architecture images (amd64, arm64)
- [ ] Debug containers hiệu quả
- [ ] Thiết kế production-ready Dockerfile

---

## 📚 Nội Dung

### 1. Multi-Stage Builds Deep Dive

Multi-stage builds giảm image size bằng cách tách **build stage** và **runtime stage**.

#### Node.js Multi-Stage

```dockerfile
# Stage 1: Dependencies only (cacheable)
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Stage 2: Builder (if need build step)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json tsconfig.json ./
RUN npm ci
COPY src ./src
RUN npm run build

# Stage 3: Production (minimal)
FROM node:20-alpine AS runtime
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=deps --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
USER nextjs
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

#### Go Static Binary (Scratch Image)

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o server ./cmd/server

FROM scratch  # Empty image!
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/server /server
EXPOSE 8080
CMD ["/server"]
# Image size: ~8MB vs ~300MB for golang:alpine
```

#### Python with Virtual Environment

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir --target=/app/packages -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/packages /app/packages
ENV PYTHONPATH=/app/packages
COPY src/ ./src/
CMD ["python", "-m", "src.main"]
```

---

### 2. Layer Caching Optimization

**Rule:** Mỗi `RUN`, `COPY`, `ADD` tạo một layer. Docker cache theo layer.

```dockerfile
# ❌ BAD — Cache miss mỗi lần code thay đổi
FROM node:20-alpine
WORKDIR /app
COPY . .            # ← Changes invalidate cache
RUN npm install     # ← Re-runs every time!

# ✅ GOOD — Dependency files first, code last
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./    # ← Cache hit nếu package.json unchanged
RUN npm ci               # ← Cached!
COPY . .                 # ← Only invalidates subsequent layers
RUN npm run build
```

**.dockerignore** (critical for cache):

```
node_modules
.git
.github
dist
build
*.log
.env
.env.*
!.env.example
**/__pycache__/
*.pyc
.pytest_cache/
.DS_Store
README.md
docs/
tests/
```

---

### 3. Docker Compose Advanced

#### Full Production Example

```yaml
version: '3.9'

x-common-env: &common-env
  POSTGRES_DB: myapp
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: ${DB_PASSWORD}

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime     # Multi-stage target
      args:
        NODE_ENV: production
    image: myapp:${TAG:-latest}
    ports:
      - "${APP_PORT:-3000}:3000"
    environment:
      NODE_ENV: production
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@db:5432/myapp
      REDIS_URL: redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./uploads:/app/uploads         # Bind mount
      - app-logs:/app/logs             # Named volume
    networks:
      - backend
      - frontend
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:16-alpine
    environment:
      <<: *common-env    # YAML anchors — DRY
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
    networks:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - app
    networks:
      - frontend

volumes:
  postgres-data:
    driver: local
  redis-data:
  app-logs:

networks:
  backend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
  frontend:
    driver: bridge
```

#### Docker Compose Commands

```bash
# Development
docker compose up -d              # Start all services detached
docker compose up --build         # Rebuild images first
docker compose logs -f app        # Follow logs of specific service
docker compose exec app bash      # Shell into running container
docker compose ps                 # Status of services
docker compose down -v            # Stop + remove containers + volumes

# Scale
docker compose up --scale app=3   # Run 3 instances of app

# Override for development
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# View config
docker compose config             # Validate and view final config
```

#### docker-compose.dev.yml

```yaml
services:
  app:
    build:
      target: development   # Different stage in Dockerfile
    volumes:
      - .:/app              # Mount code for hot reload
      - /app/node_modules   # Anonymous volume (don't overwrite)
    environment:
      NODE_ENV: development
    command: npm run dev     # Override CMD
    ports:
      - "9229:9229"         # Node.js debugger
```

---

### 4. Networking Deep Dive

```bash
# Network types
docker network create --driver bridge mynet     # Isolated bridge (default)
docker network create --driver host mynet       # Share host network (Linux only)
docker network create --driver overlay mynet    # Docker Swarm multi-host

# Inspect
docker network ls
docker network inspect bridge | jq '.[0].Containers'
docker network inspect mynet

# Connect/disconnect
docker network connect mynet container1
docker network disconnect mynet container1

# Container DNS
# Containers on same bridge network can reach each other by container name
# docker-compose services can reach each other by service name
curl http://app:3000       # Works from any container on same network!
curl http://db:5432        # Reaches PostgreSQL container
```

**iptables rules (what Docker does automatically):**
```bash
# Docker adds iptables rules:
# MASQUERADE: outbound traffic NATed from container IP to host IP
# DNAT: port forwarding from host to container
iptables -t nat -L DOCKER --line-numbers
```

---

### 5. Volumes & Storage

```bash
# Types of mounts

# 1. Bind mount: host path → container path
docker run -v /host/data:/container/data nginx
docker run --mount type=bind,source=/host/data,target=/container/data nginx

# 2. Named volume: Docker-managed
docker volume create mydata
docker run -v mydata:/data nginx
docker run --mount type=volume,source=mydata,target=/data nginx

# 3. tmpfs: In-memory, not persisted
docker run --mount type=tmpfs,target=/tmp nginx
docker run --tmpfs /tmp nginx

# Volume commands
docker volume ls
docker volume inspect mydata
docker volume rm mydata
docker volume prune    # Remove unused volumes

# Backup volume
docker run --rm \
  -v mydata:/source:ro \
  -v $(pwd):/backup \
  alpine tar czf /backup/mydata-backup.tar.gz -C /source .

# Restore
docker run --rm \
  -v mydata:/target \
  -v $(pwd):/backup \
  alpine tar xzf /backup/mydata-backup.tar.gz -C /target
```

---

### 6. Security Best Practices

```dockerfile
# 1. Use specific image tags (never :latest in production)
FROM node:20.11.0-alpine3.19

# 2. Non-root user
RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs --ingroup nodejs
USER nextjs

# 3. Read-only filesystem where possible
# docker run --read-only -v /tmp ...

# 4. No new privileges
# docker run --security-opt no-new-privileges

# 5. Drop capabilities
# docker run --cap-drop ALL --cap-add NET_BIND_SERVICE

# 6. Secrets via environment (NOT in image)
# ENV DB_PASSWORD=secret  ← NEVER (visible in docker history + logs)
# Use: docker secrets, Vault, env file via --env-file (gitignored)

# 7. Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 8. COPY vs ADD — use COPY
COPY ./src ./src    # Transparent
# ADD can extract tarballs and fetch URLs — avoid unless needed
```

**Run with security constraints:**
```bash
docker run \
  --read-only \
  --tmpfs /tmp \
  --security-opt no-new-privileges \
  --cap-drop ALL \
  --cap-add NET_BIND_SERVICE \
  --user 1001:1001 \
  --memory 512m \
  --cpus 0.5 \
  myimage:latest
```

**Scan for vulnerabilities:**
```bash
docker scout cves myimage:latest
trivy image myimage:latest
snyk container test myimage:latest
```

---

### 7. BuildKit & Advanced Caching

```bash
# Enable BuildKit (default in Docker 23+)
DOCKER_BUILDKIT=1 docker build .
# Or in daemon.json: { "features": { "buildkit": true } }

# Remote cache (push/pull layer cache from registry)
docker buildx build \
  --cache-from type=registry,ref=registry.example.com/myapp:cache \
  --cache-to type=registry,ref=registry.example.com/myapp:cache,mode=max \
  -t myapp:latest .

# GitHub Actions cache
docker buildx build \
  --cache-from type=gha \
  --cache-to type=gha,mode=max \
  -t myapp:latest .
```

**Dockerfile with BuildKit cache mounts:**
```dockerfile
# Persist pip/npm cache between builds
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# npm cache
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# apt cache
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y curl git
```

---

### 8. Multi-Architecture Builds

Build for multiple architectures (arm64 for Apple Silicon, amd64 for servers):

```bash
# Setup buildx
docker buildx create --use --name multiarch
docker buildx inspect --bootstrap

# Build and push multi-arch
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t registry.example.com/myapp:latest .

# Check manifest
docker manifest inspect registry.example.com/myapp:latest
```

---

### 9. Production Dockerfile Template

```dockerfile
# ===== Node.js Production =====
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json tsconfig.json ./
RUN npm ci
COPY src ./src
RUN npm run build

FROM node:20-alpine
RUN apk add --no-cache dumb-init     # Proper signal handling
WORKDIR /app
RUN addgroup --gid 1001 nodejs && adduser --uid 1001 --gid 1001 -D nextjs
COPY --from=deps --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
USER nextjs
EXPOSE 3000
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
```

**Key points:**
- `dumb-init` để proper signal handling (PID 1)
- Non-root user
- Multi-stage: deps + builder + runtime
- Specific tags (not `latest`)
- Healthcheck (add it!)

---

### 10. Debugging Containers

```bash
# Inspect running container
docker inspect container_name
docker stats container_name       # Live CPU/memory
docker top container_name         # Processes inside container

# Execute commands
docker exec -it container_name sh          # Shell
docker exec container_name env             # View environment
docker exec container_name cat /etc/hosts  # View files

# Logs
docker logs container_name           # All logs
docker logs -f --tail 100 container_name  # Follow + last 100 lines
docker logs --since 1h container_name     # Last hour

# Copy files
docker cp container_name:/app/logs ./logs/  # Container → host
docker cp ./config.json container_name:/app/config.json

# Debug distroless/scratch images (no shell!)
docker run --rm -it \
  --pid container:myapp \
  --network container:myapp \
  --volumes-from myapp \
  ubuntu:22.04 \
  bash    # Use Ubuntu as debug side-car

# Or use kubectl debug pattern:
docker run --rm \
  -v /proc/$(docker inspect -f '{{.State.Pid}}' myapp):/proc/1 \
  nicolaka/netshoot nsenter -t 1 -n ss -tuln
```

---

## 💻 Hands-On Exercises

### Exercise 1: Multi-Stage Build Comparison

**Task:** Viết Dockerfile đơn stage và multi-stage cho Node.js app, so sánh image size.

**Yêu cầu:**
1. Single-stage Dockerfile (copy toàn bộ source, npm install)
2. Multi-stage Dockerfile (deps + builder + runtime)
3. Build cả 2: `docker build -t app:single .` và `docker build -t app:multi .`
4. Compare: `docker images | grep app`
5. Ghi lại: Single-stage: ___ MB, Multi-stage: ___ MB, Improvement: ___

---

### Exercise 2: Docker Compose với Healthcheck

**Task:** Tạo `docker-compose.yml` với API + PostgreSQL + Redis, có healthcheck và depends_on condition.

**Yêu cầu:**
- API service với healthcheck `/health`
- PostgreSQL với healthcheck `pg_isready`
- Redis với healthcheck `redis-cli ping`
- API `depends_on` chờ DB healthy trước
- Resource limits (CPU 0.5, Memory 512M)
- Logging rotation (max-size 10m, max-file 3)

**Commands:**
```bash
docker compose up -d
docker compose ps  # Check status
docker compose logs -f api
```

---

### Exercise 3: Networking — Containers Communicate by Name

**Task:** Tạo 2 containers (app + db) trong custom network, verify app có thể kết nối db bằng container name.

**Steps:**
```bash
docker network create myapp-net
docker run -d --name postgres --network myapp-net -e POSTGRES_PASSWORD=secret postgres:15-alpine
docker run -d --name app --network myapp-net -e DATABASE_URL=postgres://postgres:secret@postgres:5432/mydb your-app-image
docker exec app curl http://postgres:5432  # Should connect
```

---

### Exercise 4: Volumes — Backup & Restore

**Task:** Backup PostgreSQL data volume và restore.

**Steps:**
```bash
# Create volume and run PostgreSQL
docker volume create pgdata
docker run -d --name pg -v pgdata:/var/lib/postgresql/data -e POSTGRES_PASSWORD=secret postgres:15-alpine

# Backup
docker run --rm -v pgdata:/source:ro -v $(pwd):/backup alpine tar czf /backup/pgdata-backup.tar.gz -C /source .

# Stop & remove container (data still in volume)
docker stop pg && docker rm pg

# Restore
docker run -d --name pg-restored -v pgdata:/var/lib/postgresql/data -e POSTGRES_PASSWORD=secret postgres:15-alpine
# Data should be there!

# Cleanup
docker stop pg-restored && docker rm pg-restored
docker volume rm pgdata
```

---

### Exercise 5: Security Scan

**Task:** Scan một Docker image với Trivy.

**Steps:**
```bash
# Install trivy (https://aquasecurity.github.io/trivy/)
# Then scan:
trivy image nginx:latest
trivy image --severity HIGH,CRITICAL your-image:latest

# Ghi lại:
# - Số vulnerabilities found: ___
# - Critical: ___, High: ___
```

---

## ✅ Kiểm Tra & Đánh Giá

### Self-Check Questions

1. **Multi-stage build advantage là gì?**
   ```
   [Trả lời]
   ```

2. **Tại sao nên copy package*.json trước, code sau?**
   ```
   [Trả lời]
   ```

3. **Docker Compose `depends_on` với `condition: service_healthy` làm gì?**
   ```
   [Trả lời]
   ```

4. **3 types of mounts trong Docker là gì?**
   ```
   [Trả lời]
   ```

5. **Làm thế nào để scan vulnerabilities trong image?**
   ```
   [Trả lời]
   ```

---

### Checklist Tự Đánh Giá

- [ ] Tôi viết được multi-stage Dockerfile cho Node.js/Python/Go
- [ ] Tôi hiểu layer caching và tối ưu Dockerfile order
- [ ] Tôi viết được docker-compose.yml với healthcheck, resource limits
- [ ] Tôi biết cách dùng Docker networks (create, inspect, connect)
- [ ] Tôi biết 3 types of mounts và khi nào dùng cái nào
- [ ] Tôi apply security best practices (non-root, capabilities, read-only)
- [ ] Tôi scan images với Trivy/`docker scout`
- [ ] Tôi biết cách backup/restore volumes
- [ ] Tôi debug container với `docker exec`, `docker logs`, `docker inspect`
- [ ] Tôi build multi-arch images với `docker buildx`

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
