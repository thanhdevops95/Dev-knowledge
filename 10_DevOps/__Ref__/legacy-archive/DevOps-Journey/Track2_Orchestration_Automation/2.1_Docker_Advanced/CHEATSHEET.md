# 📋 Docker Advanced - Cheatsheet

> **Quick Reference for Advanced Docker**
>
> *Tra cứu nhanh Docker nâng cao*

---

## 🏗️ Multi-stage Build

```dockerfile
# Build stage (Giai đoạn build)
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage (Giai đoạn production)
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## 🔒 Security Best Practices (Bảo mật)

```dockerfile
# Non-root user (Không dùng root)
FROM node:18-alpine
RUN addgroup -g 1001 appgroup && \
    adduser -u 1001 -G appgroup -s /bin/sh -D appuser
USER appuser

# Read-only filesystem (Filesystem chỉ đọc)
docker run --read-only nginx

# Drop capabilities (Loại bỏ capabilities)
docker run --cap-drop=ALL nginx
```

---

## 📦 Image Optimization (Tối ưu Image)

```dockerfile
# Use alpine (Dùng alpine)
FROM python:3.11-alpine

# Combine RUN commands (Gộp lệnh RUN)
RUN apk add --no-cache curl && \
    pip install --no-cache-dir requirements.txt && \
    rm -rf /var/cache/apk/*

# .dockerignore
node_modules
.git
*.md
```

---

## 🏥 Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1
```

```bash
docker inspect --format='{{.State.Health.Status}}' container
```

---

## 🔍 Debugging Commands (Lệnh debug)

```bash
docker logs -f container           # Follow logs (Theo dõi logs)
docker exec -it container sh       # Enter container (Vào container)
docker inspect container           # Container details (Chi tiết)
docker stats                       # Resource usage (Sử dụng tài nguyên)
docker top container               # Processes (Tiến trình)
docker diff container              # File changes (Thay đổi file)
docker history image               # Image layers (Layers của image)
```

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
