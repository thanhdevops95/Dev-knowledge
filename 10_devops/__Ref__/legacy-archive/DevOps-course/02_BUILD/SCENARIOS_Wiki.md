# 🚨 MODULE 02: SCENARIOS - Tình huống Docker & Git

## Scenario 1: Docker Image Quá Lớn (2GB)

### 🚨 Bối cảnh

Image counter-app build xong nặng 2GB, push lên Docker Hub mất 30 phút, pull về production mất 20 phút.

### 🕵️ Điều tra

```bash
docker images counter-app
# SIZE: 2.1GB

docker history counter-app:v1.0
# Thấy layer chứa build tools, cache, temp files
```

### 💡 Giải pháp

**1. Dùng Alpine base image**

```dockerfile
❌ FROM python:3.11  # 900MB
✅ FROM python:3.11-alpine  # 50MB
```

**2. Multi-stage build**

```dockerfile
# Build stage
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-alpine
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY app.py /app/
WORKDIR /app
CMD ["python", "app.py"]
```

**3. .dockerignore**

```
__pycache__
*.pyc
.git
.venv
tests/
docs/
```

**Kết quả:** Image từ 2GB → 200MB (giảm 90%)

### 🧠 Bài học

- Alpine images nhẹ hơn nhiều
- Multi-stage build loại bỏ build dependencies
- .dockerignore quan trọng như .gitignore

---

## Scenario 2: Container Exit Ngay Sau Khi Start

### 🚨 Bối cảnh

```bash
docker run -d counter-app:v1.0
docker ps  # Không thấy container
docker ps -a  # Status: Exited (1)
```

### 🕵️ Điều tra

```bash
docker logs <container-id>
# Output: ModuleNotFoundError: No module named 'flask'
```

### 💡 Giải pháp

**Nguyên nhân:** requirements.txt không được install

**Sửa Dockerfile:**

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt  # ← Thiếu dòng này
COPY app.py .
```

**Debug tips:**

```bash
# Run interactive mode để debug
docker run -it counter-app:v1.0 sh

# Check bên trong container
ls /app
python -c "import flask"
```

### 🧠 Bài học

- Luôn check logs khi container exit
- Test image locally trước khi deploy
- Sử dụng `docker run -it` để debug

---

## Scenario 3: Data Mất Khi Restart Container

### 🚨 Bối cảnh

Counter đếm được 100, restart container → Counter về 0.

### 🕵️ Điều tra

Redis không có volume → Data lưu trong container → Restart = mất data

### 💡 Giải pháp

**docker-compose.yml:**

```yaml
services:
  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data  # ← Thêm volume
    command: redis-server --appendonly yes  # Enable persistence

volumes:
  redis-data:  # Named volume
```

**Test:**

```bash
docker-compose up -d
# Counter = 50
docker-compose restart
# Counter vẫn = 50 ✅
```

### 🧠 Bài học

- Container = ephemeral (tạm thời)
- Volumes cho persistent dataDocker volumes persist data across restarts
- Named volumes tốt hơn bind mounts cho production

---

## Scenario 4: Containers Không Communicate Được

### 🚨 Bối cảnh

Flask app không connect được Redis:

```
Error: Redis connection failed at redis:6379
```

### 🕵️ Điều tra

```bash
docker network ls
# Flask và Redis ở 2 networks khác nhau!
```

### 💡 Giải pháp

**Option 1: Docker Compose (tự động tạo network)**

```yaml
services:
  web:
    ...
  redis:
    ...
# Compose tự tạo network chung
```

**Option 2: Manual network**

```bash
# Tạo network
docker network create app-network

# Run containers trên cùng network
docker run -d --network app-network --name redis redis:7-alpine
docker run -d --network app-network --name web \
  -e REDIS_HOST=redis counter-app:v1.0
```

### 🧠 Bài học

- Containers cần cùng network mới communicate
- Docker Compose tự động handle networking
- Dùng service name làm hostname (redis, web)

---

## Scenario 5: Git Commit Nhầm Sensitive Data

### 🚨 Bối cảnh

Developer commit nhầm file `.env` chứa passwords:

```env
REDIS_PASSWORD=super_secret_123
AWS_KEY=AKIA...
```

Đã push lên GitHub → Bảo mật bị lộ!

### 🕵️ Điều tra

```bash
git log --all -- .env
# Thấy commit a1b2c3d chứa .env
```

### 💡 Giải pháp

**1. Xóa file khỏi Git history (git-filter-repo)**

```bash
# Cài tool
pip install git-filter-repo

# Xóa file khỏi toàn bộ history
git filter-repo --path .env --invert-paths

# Force push (nguy hiểm!)
git push origin --force --all
```

**2. Rotate credentials ngay lập tức**

- Đổi Redis password
- Revoke AWS keys
- Generate credentials mới

**3. Thêm .gitignore**

```
# .gitignore
.env
*.key
secrets/
config/local.py
```

**4. Prevention: Pre-commit hook**

```bash
# .git/hooks/pre-commit
#!/bin/sh
if git diff --cached --name-only | grep -E '\.env$|\.key$'; then
    echo "❌ Error: Trying to commit sensitive files!"
    exit 1
fi
```

**5. Scan với git-secrets**

```bash
# Cài git-secrets
brew install git-secrets

# Scan repo
git secrets --scan
```

### 🧠 Bài học

- Không bao giờ commit credentials
- .gitignore từ đầu dự án
- Dùng pre-commit hooks để prevent
- Rotate keys ngay khi bị leak
- Dùng tools như git-secrets, trufflehog

---

## 🎯 Tổng kết Module 02

| Scenario | Vấn đề | Giải pháp | Tool |
|----------|--------|-----------|------|
| **1** | Image quá lớn | Alpine + Multi-stage | Dockerfile optimization |
| **2** | Container exit | Check logs + Debug | `docker logs`, `docker run -it` |
| **3** | Data mất | Volumes | Docker volumes |
| **4** | Network issues | Custom/Compose network | `docker network` |
| **5** | Sensitive data leak | git-filter-repo + Rotate | git-secrets, .gitignore |

---

## ✅ Checklist

- [ ] Hiểu cách optimize Docker image
- [ ] Biết debug container exit
- [ ] Sử dụng volumes cho persistence
- [ ] Cấu hình networking đúng
- [ ] Bảo vệ sensitive data trong Git

**Next:** Module 03 - CI/CD! 🚀
