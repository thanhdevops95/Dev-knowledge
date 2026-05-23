# Scenarios: Module 05 - DOCKER BASICS

> **8 Tình huống thực tế với Docker trong Production**

---

## 🎬 Scenario 1: "Container Không Khởi Động"

### Tình huống

Sáng thứ Hai, 9 giờ. Đồng nghiệp deploy version mới cuối tuần.

```bash
docker ps -a
```

```
CONTAINER ID   IMAGE       STATUS
abc123         myapp:2.0   Exited (1) 10 seconds ago
```

Container liên tục crash. Users không access được app.

### Điều tra

**Bước 1: Check logs**

```bash
docker logs abc123
```

```
Traceback (most recent call last):
  File "app.py", line 3, in <module>
    import redis
ModuleNotFoundError: No module named 'redis'
```

**Bước 2: Check Dockerfile**

```dockerfile
FROM python:3.9
COPY app.py .
CMD ["python", "app.py"]
```

**Vấn đề:** Dependencies không được install!

### Giải pháp

**Sửa Dockerfile:**

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

**Rebuild và deploy:**

```bash
docker build -t myapp:2.1 .
docker run -d -p 5000:5000 myapp:2.1
```

### Phòng tránh

✅ Luôn install dependencies trước khi copy app  
✅ Test builds locally trước khi deploy  
✅ Sử dụng health checks  

---

## 🌐 Scenario 2: "Network Mystery"

### Tình huống

Microservices app có 3 containers: web, api, database. Web không connect được API.

```bash
docker-compose logs web
```

```
Error: Failed to connect to api:8000
ConnectionRefusedError
```

### Điều tra

**Check containers:**

```bash
docker-compose ps
# Tất cả đều Up
```

**Check docker-compose.yml:**

```yaml
services:
  web:
    image: nginx
  api:
    image: myapi
  database:
    image: postgres
```

**Vấn đề:** Không có network định nghĩa!

### Giải pháp

```yaml
services:
  web:
    networks:
      - app-network
  api:
    networks:
      - app-network
  database:
    networks:
      - app-network

networks:
  app-network:
```

---

## 💾 Scenario 3: "Data Biến Mất"

### Tình huống

Database container crash. Restart → **Tất cả data mất!** 😱

### Nguyên nhân

```bash
docker inspect db | grep -A 10 Mounts
# "Mounts": []
```

**Không có volume!** Data trong container filesystem = mất khi container bị xóa.

### Giải pháp (cho tương lai)

```yaml
services:
  db:
    image: postgres:13
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

**Backup strategy:**

```bash
docker exec db pg_dump -U postgres mydb > backup.sql
```

---

## 🔥 Scenario 4: "Memory Explosion"

### Tình huống

Server unresponsive. Memory 100%.

```bash
docker stats --no-stream
```

```
CONTAINER    MEM USAGE
web-app      4.5GiB
background   12GiB   ← Vấn đề!
db           1.2GiB
```

### Giải pháp

**Ngay lập tức:**

```bash
docker restart background
docker update --memory="2g" background
```

**Lâu dài:**

```yaml
services:
  background:
    deploy:
      resources:
        limits:
          memory: 2G
```

---

## ⚡ Scenario 5: "Build Quá Chậm"

### Tình huống

Docker build mất 15 phút. Mỗi code change = 15 phút chờ!

### Nguyên nhân

```dockerfile
# BAD
COPY . .                    # ← Copy tất cả trước
RUN npm install             # ← Install mỗi lần
```

### Giải pháp

```dockerfile
# GOOD
COPY package*.json ./       # ← Package files trước
RUN npm install             # ← Cached!
COPY . .                    # ← Source code sau
```

**Kết quả:** Build giảm từ 15 phút → 8 giây (cached)!

---

## 🔐 Scenario 6: "Security Breach"

### Tình huống

Security audit flagged Dockerfile.

```dockerfile
FROM ubuntu:latest       # ← latest tag
COPY .env .              # ← Secrets trong image!
# Running as root        # ← Nguy hiểm!
```

### Giải pháp

```dockerfile
FROM python:3.9-alpine   # ← Specific version
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
RUN adduser -D appuser
USER appuser             # ← Non-root
CMD ["python", "app.py"]
# .env passed at runtime via -e flag
```

---

## 🚀 Scenario 7: "Zero-Downtime Deploy"

### Tình huống

Deploy version mới không được có downtime.

### Giải pháp: Blue-Green

```nginx
upstream backend {
    server localhost:5001;  # Blue (current)
}
```

```bash
# Deploy Green (new version) on different port
docker run -d -p 5002:5000 myapp:2.0

# Test Green
curl http://localhost:5002/health

# Switch traffic
# Update nginx: server localhost:5002;
nginx -s reload

# Instant rollback if issues
```

---

## 📦 Scenario 8: "Compose Chaos"

### Tình huống

Team's docker-compose.yml là mess. Services fail randomly.

### Giải pháp: Production-Ready Compose

```yaml
version: '3.8'

services:
  web:
    image: myapp:${VERSION:-latest}
    restart: unless-stopped
    depends_on:
      - db
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s

  db:
    image: postgres:13-alpine
    restart: unless-stopped
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-network

volumes:
  db-data:

networks:
  app-network:
```

---

## 🎓 KEY LESSONS

1. **Luôn có volumes** cho persistent data
2. **Set resource limits**
3. **Optimize Dockerfile** layer order
4. **Non-root user** cho security
5. **Explicit networks** trong compose
6. **Health checks** cho zero-downtime
7. **Test trước deploy**
