# 🚨 Tình huống Thực chiến - Docker

Đây là 5 tình huống thực tế mà DevOps Engineer thường gặp khi làm việc với Docker. Mỗi tình huống gồm:

- **Bối cảnh**: Chuyện gì xảy ra
- **Triệu chứng**: Bạn thấy gì
- **Điều tra**: Cách tìm nguyên nhân
- **Giải pháp**: Cách fix
- **Bài học**: Rút kinh nghiệm

---

## Scenario 1: Docker Image quá lớn (2GB+)

### 📋 Bối cảnh

Team bạn build một Docker image cho ứng dụng Python đơn giản. Khi push lên registry, mọi người phàn nàn:

- "Pull image mất 10 phút!"
- "CI/CD chậm kinh khủng"
- "Disk đầy liên tục"

### 🔍 Triệu chứng

```bash
docker images
# REPOSITORY    TAG       SIZE
# myapp         latest    2.1GB  ← Quá lớn cho app Python!
```

### 🕵️ Điều tra

```bash
# Xem các layers của image
docker history myapp:latest

# Output có thể thấy:
# 1.2GB - COPY . /app  ← Copy cả node_modules, __pycache__, .git
# 800MB - RUN pip install  ← Base image quá nặng
```

### 💡 Giải pháp

**1. Dùng .dockerignore:**

```dockerignore
# .dockerignore
__pycache__
*.pyc
.git
.gitignore
*.md
venv/
.env
tests/
```

**2. Dùng Alpine base image:**

```dockerfile
# Thay vì:
FROM python:3.11

# Dùng:
FROM python:3.11-alpine
# hoặc
FROM python:3.11-slim
```

**3. Multi-stage build:**

```dockerfile
# Build stage
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Production stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

**Kết quả:**

```bash
docker images
# REPOSITORY    TAG       SIZE
# myapp         latest    150MB  ← Giảm từ 2.1GB xuống 150MB!
```

### 🧠 Bài học

- **Luôn dùng .dockerignore** - Giống .gitignore cho Docker
- **Chọn base image phù hợp** - Alpine = nhẹ, Slim = cân bằng
- **Multi-stage build** - Tách build dependencies khỏi runtime
- **Check image size trước khi push** - Đặt limit trong CI/CD

---

## Scenario 2: Container chạy local nhưng fail trên production

### 📋 Bối cảnh

Developer chạy app trong Docker trên máy local: OK.
Deploy lên production server: CRASH.

> "Works on my machine!" - Câu nói đáng sợ nhất

### 🔍 Triệu chứng

```bash
# Local (Mac M1)
docker run myapp
# ✅ Running on port 5000

# Production (Linux x86_64)
docker run myapp
# ❌ exec format error
```

### 🕵️ Điều tra

```bash
# Kiểm tra platform của image
docker inspect myapp | grep Architecture
# "Architecture": "arm64"  ← Build trên Mac M1!

# Production là x86_64/amd64
uname -m
# x86_64
```

### 💡 Giải pháp

**1. Build multi-platform:**

```bash
# Dùng buildx để build cho nhiều platforms
docker buildx build --platform linux/amd64,linux/arm64 \
  -t myapp:latest --push .
```

**2. Chỉ định platform khi build:**

```bash
# Force build cho amd64 (production)
docker build --platform linux/amd64 -t myapp .
```

**3. Trong CI/CD, luôn chỉ định platform:**

```yaml
# .github/workflows/docker.yml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    platforms: linux/amd64
    push: true
    tags: myapp:latest
```

### 🧠 Bài học

- **Mac M1/M2 = ARM64** ≠ Production Linux = AMD64
- **CI/CD nên build image** - Không dùng image build từ laptop dev
- **Multi-platform builds** - Hỗ trợ cả ARM và x86

---

## Scenario 3: "Cannot connect to database" trong Docker Compose

### 📋 Bối cảnh

Bạn có docker-compose với app + database:

```yaml
services:
  app:
    build: .
    depends_on:
      - db
  db:
    image: postgres:15
```

App khởi động, cố connect database, và... CRASH.

### 🔍 Triệu chứng

```bash
docker-compose up
# db    | PostgreSQL starting...
# app   | Connecting to database...
# app   | Error: Connection refused
# app exited with code 1
```

### 🕵️ Điều tra

```bash
# Xem logs
docker-compose logs db
# PostgreSQL đang khởi động...
# ready to accept connections  ← Mất 20 giây để sẵn sàng

docker-compose logs app
# App cố connect ngay lập tức → Fail
```

**Nguyên nhân:** `depends_on` chỉ đợi container START, không đợi service READY.

### 💡 Giải pháp

**1. Health check + wait:**

```yaml
services:
  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  app:
    build: .
    depends_on:
      db:
        condition: service_healthy  # Đợi DB healthy!
```

**2. Retry trong app code:**

```python
import time
import psycopg2

def connect_with_retry(max_retries=10):
    for i in range(max_retries):
        try:
            return psycopg2.connect(DATABASE_URL)
        except psycopg2.OperationalError:
            print(f"DB not ready, retry {i+1}/{max_retries}")
            time.sleep(2)
    raise Exception("Cannot connect to database")
```

**3. wait-for-it script:**

```dockerfile
# Dockerfile
COPY wait-for-it.sh /wait-for-it.sh
CMD ["/wait-for-it.sh", "db:5432", "--", "python", "app.py"]
```

### 🧠 Bài học

- **`depends_on` ≠ "service is ready"** - Chỉ là container started
- **Luôn có retry logic** - Network có thể unstable
- **Health checks** - Để Compose biết khi nào service thực sự ready

---

## Scenario 4: "No space left on device" - Disk đầy

### 📋 Bối cảnh

Server production chạy Docker, đột nhiên mọi thứ fail:

> "Cannot create container: no space left on device"

Kiểm tra disk: 100% used.

### 🔍 Triệu chứng

```bash
df -h /var/lib/docker
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1       50G   50G     0  100%  /

docker system df
# TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
# Images          45        5         30GB      25GB (83%)
# Containers      100       3         5GB       4.8GB (96%)
# Build Cache     -         -         10GB      10GB (100%)
```

### 🕵️ Điều tra

**Nguyên nhân thường gặp:**

1. **Images cũ** không được xóa
2. **Containers stopped** vẫn còn
3. **Build cache** tích lũy
4. **Logs container** quá lớn

```bash
# Kiểm tra logs của containers
docker ps -q | xargs docker inspect --format='{{.LogPath}}' | xargs ls -lh
# Có thể thấy log files hàng GB!
```

### 💡 Giải pháp

**1. Cleanup ngay:**

```bash
# Xóa containers đã stop
docker container prune

# Xóa images không dùng
docker image prune -a

# Xóa volumes không dùng
docker volume prune

# Xóa tất cả (CẢNH BÁO: aggressive!)
docker system prune -a --volumes
```

**2. Giới hạn log size:**

```yaml
# docker-compose.yml
services:
  app:
    image: myapp
    logging:
      driver: "json-file"
      options:
        max-size: "10m"    # Max 10MB per log file
        max-file: "3"      # Keep 3 files
```

**3. Scheduled cleanup (cron):**

```bash
# /etc/cron.daily/docker-cleanup
#!/bin/bash
docker system prune -af --filter "until=168h"  # Xóa resources > 7 ngày
```

**4. Monitoring disk:**

```bash
# Alert khi disk > 80%
df -h /var/lib/docker | awk 'NR==2 {print $5}' | sed 's/%//'
```

### 🧠 Bài học

- **Docker không tự cleanup** - Phải chủ động dọn dẹp
- **Log rotation là bắt buộc** - Logs có thể grow vô hạn
- **Monitoring disk** - Alert trước khi 100%
- **Scheduled cleanup** - Cron job hàng ngày/tuần

---

## Scenario 5: Secrets bị lộ trong Docker Image

### 📋 Bối cảnh

Security audit phát hiện: Password database có thể extract từ Docker image!

> "Ai đã commit password vào Dockerfile?!"

### 🔍 Triệu chứng

```bash
# Hacker có thể:
docker pull yourcompany/app:latest
docker history yourcompany/app:latest
# Thấy: ENV DB_PASSWORD=supersecret123

# Hoặc:
docker run yourcompany/app cat /app/.env
# DB_PASSWORD=supersecret123
```

### 🕵️ Điều tra

**Cách secrets thường bị lộ:**

```dockerfile
# ❌ SAI: Hardcode password
ENV DB_PASSWORD=supersecret123

# ❌ SAI: Copy .env file
COPY .env /app/.env

# ❌ SAI: Clone private repo với token
RUN git clone https://token:x-oauth@github.com/company/private-repo
```

### 💡 Giải pháp

**1. KHÔNG bao giờ hardcode secrets trong Dockerfile:**

```dockerfile
# ✅ ĐÚNG: Truyền khi run container
# Dockerfile không có secrets
ENV DB_PASSWORD=""

# docker run -e DB_PASSWORD=xxx myapp
```

**2. Dùng Docker secrets (Swarm) hoặc K8s secrets:**

```bash
# Docker Swarm
echo "supersecret" | docker secret create db_password -

# Compose
services:
  app:
    secrets:
      - db_password

secrets:
  db_password:
    external: true
```

**3. Multi-stage build cho private repos:**

```dockerfile
# Build stage - có credentials
FROM alpine AS builder
ARG GITHUB_TOKEN
RUN git clone https://${GITHUB_TOKEN}@github.com/company/repo

# Production stage - không có credentials  
FROM alpine
COPY --from=builder /repo/app /app
# GITHUB_TOKEN không có trong final image!
```

**4. .dockerignore cho sensitive files:**

```dockerignore
.env
*.pem
*.key
secrets/
credentials.json
```

### 🧠 Bài học

- **Image layers lưu mọi thứ** - Ngay cả khi bạn xóa file sau đó
- **Secrets qua environment** - Truyền khi run, không build
- **Scan images** - Dùng tools như Trivy, Snyk
- **Private registries** - Không push sensitive images lên Docker Hub public

---

## 📝 Checklist Trước khi Deploy Docker

- [ ] Image size < 500MB (hoặc có lý do hợp lý)
- [ ] Không có secrets trong image
- [ ] .dockerignore đầy đủ
- [ ] Health check configured
- [ ] Log rotation enabled
- [ ] Multi-platform nếu cần
- [ ] Security scan passed
