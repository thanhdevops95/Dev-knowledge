# ✅ Solutions: Docker Advanced

> **Solutions for Exercises. Try to solve it yourself first!**
>
> *Đáp án cho Exercises. Hãy thử tự giải trước!*

---

## Exercise 1: Multi-stage Optimization

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:18-alpine

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copy only necessary files
COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --chown=appuser:appgroup server.js ./

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "server.js"]
```

---

## Exercise 3: Security Audit - Fixed

```dockerfile
# ✅ Fixed Dockerfile
FROM node:18-alpine

# Create non-root user
RUN addgroup -S app && adduser -S app -G app

WORKDIR /app

# Copy package files first
COPY --chown=app:app package*.json ./
RUN npm ci --only=production

# Copy source
COPY --chown=app:app . .

# No secrets in image - use runtime injection
# ENV API_KEY removed

USER app

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -q --spider http://localhost:3000/health || exit 1

CMD ["npm", "start"]
```

**Security Issues Fixed:**

1. ❌ `ubuntu:latest` → ✅ `node:18-alpine` (smaller, fewer CVEs)
2. ❌ Running as root → ✅ Non-root user
3. ❌ API_KEY in ENV → ✅ Removed (use runtime)
4. ❌ No health check → ✅ Added HEALTHCHECK

---

## Exercise 4: Minimal Go Image

```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY main.go .

# Build static binary
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o app main.go

# Final stage - scratch (empty image)
FROM scratch

COPY --from=builder /app/app /app

ENTRYPOINT ["/app"]
```

```bash
docker build -t go-app .
docker images go-app
# SIZE: ~2MB
```

---

## Exercise 6: Resource Management

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  api:
    build: ./api
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 256M
        reservations:
          cpus: '0.25'
          memory: 128M
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:15-alpine
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - db-data:/var/lib/postgresql/data

  cache:
    image: redis:7-alpine
    deploy:
      resources:
        limits:
          cpus: '0.25'
          memory: 128M
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  db-data:
```

---

**[← Back to Exercises](./EXERCISES.md)** | **[Back to README →](./README.md)**
