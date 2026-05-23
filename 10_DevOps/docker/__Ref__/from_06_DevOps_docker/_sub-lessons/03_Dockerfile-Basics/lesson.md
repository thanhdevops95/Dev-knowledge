# 🐳 Docker — Dockerfile Basics

---

## 📋 Metadata

- **Parent Lesson:** [../README.md](../README.md)
- **Level:** `[INTERMEDIATE]`
- **Prerequisites:** [Lesson 02](../02-Images-Containers/lesson.md)
- **Estimated Time:** 1.5 giờ
- **Last Updated:** 30/04/2026
- **Author:** Mr.Rom

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành, bạn sẽ có thể:

- [ ] Viết Dockerfile cơ bản với các directives (FROM, RUN, COPY, CMD, ENV,...)
- [ ] Build custom Docker image với `docker build`
- [ ] Hiểu Docker layer caching và cách tối ưu build
- [ ] Dùng `.dockerignore` để exclude files
- [ ] Viết multi-stage Dockerfile để minimize image size
- [ ] Áp dụng Dockerfile best practices

---

## 📚 Nội Dung

### 1. Dockerfile là gì?

**Dockerfile** là text file chứa instructions để build Docker image.

**Ví dụ đơn giản:**

```dockerfile
# Dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y nginx
COPY index.html /var/www/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Build và run:
```bash
docker build -t my-nginx:latest .
docker run -d -p 8080:80 my-nginx:latest
```

---

### 2. Dockerfile Instructions

#### `FROM` — Base Image

```dockerfile
FROM <image>:<tag>
```

**Ví dụ:**
```dockerfile
FROM ubuntu:22.04
FROM node:18-alpine
FROM python:3.11-slim
FROM golang:1.21-alpine AS builder  # Multi-stage
```

**Best practice:** Dùng official images từ Docker Hub (hoặc trusted sources). Chọn tag cụ thể (không dùng `latest` trong production).

---

#### `RUN` — Execute Commands During Build

**2 forms:**
1. **Shell form:** `RUN <command>` (chạy trong shell `/bin/sh -c`)
2. **Exec form:** `RUN ["executable", "param1", "param2"]`

```dockerfile
# Shell form
RUN apt-get update && apt-get install -y nginx

# Exec form (không chạy qua shell)
RUN ["apt-get", "update"]
```

**Tips:**
- Chain multiple commands với `&&` để giảm số layers
- Clean up trong cùng RUN (ví dụ: `apt-get clean && rm -rf /var/lib/apt/lists/*`)

---

#### `COPY` vs `ADD`

**`COPY <src> <dest>`** — Copy files từ build context vào image

```dockerfile
COPY app.js /app/
COPY . /app  # Copy tất cả files từ current directory
```

**`ADD`** — Tương tự COPY nhưng có thêm features:
- Tự unpack compressed files (tar, gzip)
- Support remote URLs (download files)

**Best practice:** **Dùng `COPY` trừ khi cần `ADD` features** (unpack tarball). `ADD` không rõ ràng, khó predict.

---

#### `CMD` — Default Command When Container Starts

**3 forms:**
1. **Exec form (recommended):** `CMD ["executable","param1","param2"]`
2. **Shell form:** `CMD command param1 param2`
3. **Params for ENTRYPOINT:** `CMD ["param1","param2"]`

```dockerfile
# Exec form (preferred)
CMD ["nginx", "-g", "daemon off;"]

# Shell form
CMD python app.py

# With ENTRYPOINT (rare)
ENTRYPOINT ["python"]
CMD ["app.py"]  # params passed to ENTRYPOINT
```

**Chỉ có 1 CMD trong Dockerfile** (nếu có nhiều, chỉ lệnh cuối được dùng).

---

#### `ENTRYPOINT` — Configure Container as Executable

`ENTRYPOINT` thiết lập container chạy như một executable.

```dockerfile
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]  # Default args
```

Khi run: `docker run <image> <args>` → args passed as CMD.

**Use case:** `ENTRYPOINT` cho container wrapper script, `CMD` cho default args.

---

#### `ENV` — Environment Variables

```dockerfile
ENV NODE_ENV=production
ENV PORT=8080
# Multiple in one line
ENV APP_NAME="MyApp" APP_VERSION="1.0.0"
```

Dùng trong RUN, CMD, và trong container runtime:

```dockerfile
RUN echo "Environment is $NODE_ENV"
```

---

#### `EXPOSE` — Document Ports

```dockerfile
EXPOSE 80
EXPOSE 8080 443
```

**Lưu ý:** `EXPOSE` chỉ là **documentation**. Port không được publish ra host trừ khi dùng `-p` khi run:

```bash
docker run -p 8080:80 myimage  # Map host 8080 → container 80
```

---

#### `VOLUME` — Create Mount Points

```dockerfile
VOLUME ["/data"]
VOLUME /var/log/nginx
```

Tạo mount point cho persistent data (volumes hoặc bind mounts).

---

#### `WORKDIR` — Set Working Directory

```dockerfile
WORKDIR /app
COPY . .
RUN npm install  # Chạy trong /app
```

Nếu `WORKDIR` không tồn tại, Docker tự tạo.

---

#### `USER` — Set User/Root

```dockerfile
USER nginx
USER 1000  # UID
USER appuser:group  # user:group
```

**Best practice:** Run container với non-root user (security). Sau `USER`, tất cả RUN, CMD, ENTRYPOINT chạy với user đó.

---

#### `LABEL` — Metadata

```dockerfile
LABEL maintainer="Mr.Rom <rom@example.com>"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.source="https://github.com/..."
```

Dùng để add metadata cho image (hiển thị trong `docker inspect`).

---

### 3. Docker Build Process

**Command:**
```bash
docker build -t myapp:v1.0 .
```

**Process:**

1. Docker đọc Dockerfile
2. Mỗi instruction tạo một **layer** (cacheable)
3. Build context (files trong current directory) được tar và gửi cho daemon
4. Thực thi từng step, tạo layer mới
5. Final image = tổng hợp tất cả layers

**Layer caching:**

Nếu bạn build lại với Dockerfile không đổi và build context không đổi → Docker dùng cache, build nhanh.

**Nếu một step thay đổi → tất cả steps sau rebuild.**

**Ví dụ:**

```dockerfile
FROM node:18-alpine           # Layer 1 (cache if unchanged)
WORKDIR /app                  # Layer 2
COPY package.json .           # Layer 3 — chỉ rebuild khi package.json đổi
RUN npm install               # Layer 4 — rebuild nếu Layer 3 đổi
COPY . .                      # Layer 5 — rebuild mỗi lần code thay đổi
CMD ["node", "server.js"]     # Layer 6
```

**Optimization:** Order steps sao cho cache hit nhiều nhất. Copy `package.json` riêng trước, rồi `npm install`, rồi mới copy toàn bộ source code.

---

### 4. .dockerignore File

Giống `.gitignore` — exclude files từ build context.

**Ví dụ `.dockerignore`:**
```
node_modules
npm-debug.log
.git
.env
*.md
dist/
coverage/
```

**Tại sao cần?**
- Giảm build context size (build nhanh hơn)
- Không đưa sensitive files (`.env`, `secrets`) vào image
- Không đưa unnecessary files (`node_modules`, `*.log`)

---

### 5. Multi-Stage Builds

**Problem:** Image cuối cùng lớn vì chứa build dependencies (compilers, dev packages).

**Solution:** Multi-stage builds — dùng nhiều `FROM` trong 1 Dockerfile, copy artifacts giữa các stage.

**Ví dụ: Node.js app**

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

**Kết quả:** Production image chỉ chứa runtime + built code, không có dev dependencies, npm cache, source maps,...

**Ưu điểm:**
- ✅ Image size nhỏ hơn
- ✅ Attack surface nhỏ hơn
- ✅ Không có build tools trong production image

---

### 6. Dockerfile Best Practices

#### ✅ DOs

✅ **Dùng official base images** (`node:18-alpine`, `python:3.11-slim`)  
✅ **Dùng specific tags** (không dùng `latest` trong production)  
✅ **Multi-stage builds** để minimize image size  
✅ **Combine RUN commands** để giảm số layers  
✅ **Clean up trong cùng RUN** (ví dụ: `apt-get clean`)  
✅ **Dùng `.dockerignore`** để exclude unnecessary files  
✅ **Run as non-root user** (`USER` directive)  
✅ **Pin versions** trong `RUN apt-get install package=version`  
✅ **Label images** với maintainer, version, source  
✅ **EXPOSE ports** để document  

#### ❌ DON'Ts

❌ **Không dùng `ADD`** trừ khi cần unpack tarball  
❌ **Không chạy process như root** (security risk)  
❌ **Không store credentials** trong image (dùng Docker secrets hoặc environment variables lúc run)  
❌ **Không commit built images** vào Git (dùng registry)  
❌ **Không ignore `.dockerignore`** (build context lớn, slow)  
❌ **Không dùng `latest` tag** trong production (không reproducible)  

---

### 7. Practical Example: Full Dockerfile

**Node.js + Express app với multi-stage build:**

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app

# Copy dependencies
COPY package*.json ./
RUN npm ci

# Copy source và build
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy từ builder stage
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./package.json

# Switch to non-root user
USER nodejs

EXPOSE 3000
CMD ["node", "dist/server.js"]
```

---

## 💻 Hands-On Exercises

### Exercise 1: Simple Dockerfile

**Task:** Viết Dockerfile cho Python Flask app

**Structure:**
```
my-flask-app/
├── app.py
├── requirements.txt
└── Dockerfile
```

**app.py:**
```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Docker!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

**requirements.txt:**
```
Flask==2.3.3
```

**Yêu cầu Dockerfile:**
1. Base image: `python:3.11-slim`
2. Set working directory `/app`
3. Copy `requirements.txt` và `pip install`
4. Copy toàn bộ source code
5. Expose port 5000
6. CMD: `["python", "app.py"]`

**Build & run:**
```bash
docker build -t my-flask-app .
docker run -d -p 5000:5000 my-flask-app
```

Test: `http://localhost:5000`

---

### Exercise 2: Multi-stage Build

**Task:** Tối ưu Dockerfile từ Exercise 1 bằng multi-stage build

**Yêu cầu:**
1. Stage 1 (`builder`): Install dependencies, copy source
2. Stage 2 (production): Copy only necessary files từ builder (không copy `requirements.txt`, không cần pip install lại)
3. Dùng non-root user (ví dụ: UID 1000)

**So sánh image size:**
```bash
docker images | grep my-flask-app
```

Giải thích tại sao multi-stage image nhỏ hơn?

---

### Exercise 3: .dockerignore

**Task:** Tạo `.dockerignore` file trong `my-flask-app/`

**Yêu cầu:** Exclude:
- `__pycache__/`
- `*.pyc`
- `.git/`
- `.venv/` hoặc `venv/`
- `*.log`
- `node_modules/` (nếu có)

**Test:** Rebuild image và xem build context size (Docker logs show "Sending build context").

---

## ✅ Kiểm Tra & Đánh Giá

### Self-Check Questions

1. **`COPY` vs `ADD` — khi nào dùng cái nào?**
   ```
   [Trả lời]
   ```

2. **CMD exec form vs shell form?**
   ```
   [Trả lời]
   ```

3. **Multi-stage build dùng để làm gì?**
   ```
   [Trả lời]
   ```

4. **Tại sao nên dùng specific tag thay vì `latest`?**
   ```
   [Trả lời]
   ```

---

### Checklist Tự Đánh Giá

- [ ] Tôi biết cách viết Dockerfile cơ bản (FROM, RUN, COPY, CMD, EXPOSE)
- [ ] Tôi biết cách build image: `docker build -t name .`
- [ ] Tôi hiểu layer caching và cách tối ưu Dockerfile
- [ ] Tôi biết dùng `.dockerignore`
- [ ] Tôi biết viết multi-stage Dockerfile
- [ ] Tôi hiểu và áp dụng best practices (non-root user, specific tags,...)
- [ ] Tôi có thể viết Dockerfile cho simple app (Node.js, Python, Go,...)

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
