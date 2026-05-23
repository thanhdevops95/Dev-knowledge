# Docker Advanced

> **Tags:** `docker` `dockerfile` `compose` `networking` `volumes` `multi-stage` `security`
> **Level:** Intermediate | **Prerequisite:** `docker/01-docker-basics.md`

---

## 1. Multi-Stage Builds

Reduce final image size drastically by separating build from runtime:

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app

# Copy only dependency files first (layer caching)
COPY package*.json ./
RUN npm ci --only=production

COPY tsconfig.json ./
COPY src/ ./src/
RUN npm run build

# Stage 2: Runtime (much smaller)
FROM node:20-alpine AS runtime
WORKDIR /app

# Only what's needed to run
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules

# Non-root user
RUN addgroup -g 1001 -S nodejs \
    && adduser -S nextjs -u 1001
USER nextjs

EXPOSE 3000
CMD ["node", "dist/server.js"]
```

```dockerfile
# Go: even better — static binary, scratch image
FROM golang:1.22-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o server ./cmd/server

# Final: scratch (empty) image
FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/server /server

EXPOSE 8080
CMD ["/server"]
# Image size: ~8MB vs ~300MB for golang:alpine
```

```dockerfile
# Python with venv
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

## 2. Layer Caching Optimization

Docker builds each instruction as a layer. **Order matters!**

```dockerfile
# BAD: code copy before dependency install → cache miss on every code change
FROM node:20-alpine
WORKDIR /app
COPY . .                     # ← Invalidates cache if ANY file changes
RUN npm install              # ← Re-runs every time!

# GOOD: dependency files first, then code
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./        # ← Only changes when deps change
RUN npm ci                   # ← Cached if package.json unchanged!
COPY . .                     # ← Only code invalidates this
RUN npm run build
```

### .dockerignore (critical)
```
# .dockerignore
node_modules/
.git/
.github/
dist/
build/
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
tests/      # Unless running tests in Docker
```

---

## 3. Docker Compose Advanced

```yaml
# docker-compose.yml
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
        condition: service_healthy    # Wait for health check
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

### Docker Compose Commands
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
```

```yaml
# docker-compose.dev.yml — overrides for development
services:
  app:
    build:
      target: development   # Different stage
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

## 4. Networking Deep Dive

```bash
# Network types
docker network create --driver bridge mynet     # Isolated bridge
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

### iptables rules (what Docker does)
```bash
# Docker adds iptables rules automatically:
# MASQUERADE: outbound traffic NATed from container IP to host IP
# DNAT: port forwarding from host to container
iptables -t nat -L DOCKER --line-numbers
```

---

## 5. Volumes & Storage

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

## 6. Security Best Practices

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

# 6. Secrets via environment (not in image)
# ENV DB_PASSWORD=secret  ← NEVER DO THIS (visible in docker history + logs)
# Use: docker secrets, Vault, env file via --env-file (gitignored file)

# 7. Scan for vulnerabilities
# docker scout cves myimage:latest
# trivy image myimage:latest
# snyk container test myimage:latest

# 8. COPY vs ADD
COPY ./src ./src    # Preferred: transparent
# ADD can extract tarballs and fetch URLs — avoid unless needed
```

```bash
# Run with security constraints
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

---

## 7. Build Cache with BuildKit

```bash
# Enable BuildKit (default in Docker 23+, enable explicitly if needed)
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

### Dockerfile with mount cache
```dockerfile
# BuildKit cache mount — persist pip/npm cache between builds
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

## 8. Multi-Architecture Builds

```bash
# Build for multiple architectures (arm64 for Apple Silicon, amd64 for servers)
docker buildx create --use --name multiarch
docker buildx inspect --bootstrap

docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t registry.example.com/myapp:latest .

# Check image manifest
docker manifest inspect registry.example.com/myapp:latest
```

---

## 9. Production Dockerfile Templates

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

---

## 10. Debugging Containers

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

*Tài liệu liên quan: `docker/01-docker-basics.md` | `kubernetes/01-kubernetes-basics.md` | `cicd/01-github-actions.md`*
