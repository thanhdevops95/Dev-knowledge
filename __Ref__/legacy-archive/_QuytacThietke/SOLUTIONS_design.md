# SOLUTIONS.md Design Specification

## 1. Purpose

- **Mục đích:** Cung cấp đáp án chi tiết cho các bài tập (Exercises) và dự án (Project) trong mỗi module.
- **Mục tiêu:** Giúp học viên kiểm tra, so sánh và hiểu cách giải quyết vấn đề một cách tối ưu.
- **Lưu ý:** File này là tài liệu tham khảo, học viên nên tự làm trước khi xem đáp án.

---

## 2. File Header (Metadata)

```yaml
---
module: "X.Y"
title: "<Tên Module> – Solutions"
track: "<Số Track>"
version: "1.0"
last_updated: "YYYY-MM-DD"
exercises_covered: [1, 2, 3]
---
```

---

## 3. Required Sections (theo thứ tự bắt buộc)

### 3.1. Header

```markdown
## MODULE X.Y – <Tên Module> Solutions
```

### 3.2. Important Notes (Lưu ý quan trọng)

- Khuyến cáo tự làm trước khi xem đáp án
- Có thể có nhiều cách giải đúng

### 3.3. Exercise Solutions (Đáp án bài tập)

Mỗi bài tập bao gồm:

- **Exercise ID & Title**
- **Problem Recap** (Tóm tắt lại yêu cầu)
- **Why This Solution? ⭐** (Tại sao chọn cách này?)
- **Solution Explanation** (Giải thích cách tiếp cận)
- **Step-by-Step Solution** (Từng bước giải)
- **Code Snippets** (Code mẫu)
- **Output Verification** (Kiểm tra kết quả)
- **Common Mistakes** (Lỗi thường gặp)
- **Alternative Solutions** (Cách giải khác - nếu có)

### 3.3.1. "Why This Solution?" Section ⭐ BẮT BUỘC

**Mục này giải thích TƯ DUY đằng sau giải pháp, không chỉ đưa code:**

```markdown
### 💡 Why This Solution? (Tại sao chọn cách này?)

| Quyết định | Lý do | So sánh |
|------------|-------|---------|
| Dùng `alpine` image | Giảm size từ 900MB xuống 50MB | `ubuntu:latest` = 900MB, `node:alpine` = 50MB |
| Multi-stage build | Loại bỏ devDependencies trong production | Single-stage = 500MB, Multi-stage = 100MB |
| `npm ci` thay vì `npm install` | Cài đặt chính xác theo lock file, nhanh hơn | `npm install` có thể update dependencies |

> 📝 **Ghi nhớ:** Trong production, luôn ưu tiên image nhỏ và security.
```

**Ví dụ thực tế:**

```markdown
### 💡 Why This Solution?

**Q: Tại sao dùng `node:18-alpine` thay vì `node:18`?**

- **`node:18`**: Base Debian, size ~900MB, chứa nhiều tool không cần thiết
- **`node:18-alpine`**: Base Alpine Linux, size ~50MB, minimal và secure

**Q: Tại sao dùng `COPY package*.json ./` trước `COPY . .`?**

- Docker cache mỗi layer riêng biệt
- Nếu source code thay đổi nhưng package.json không đổi → npm install được cache
- Tiết kiệm thời gian build đáng kể
```

### 3.4. Project Solution (Đáp án dự án)

- **Project Recap**
- **Architecture Overview**
- **Step-by-Step Implementation**
- **Final Verification**
- **Bonus Improvements**

### 3.5. References (Tham khảo)

- Link tới docs liên quan
- Tài liệu bổ sung

### 3.6. Navigation Footer ⭐ BẮT BUỘC

Cuối mỗi file phải có điều hướng:

```markdown
---

[⬅️ EXERCISES](./EXERCISES.md) | [📚 Mục lục](../../README.md) | [QUIZ ➡️](./QUIZ.md)
```

---

## 4. Formatting Rules

| Thành phần | Quy tắc |
|------------|---------|
| Tiêu đề | `##` cho chính, `###` cho mục con |
| Code | Block với ngôn ngữ phù hợp |
| Giải thích | Bullet points ngắn gọn |
| Diagram | Image hoặc ASCII art |
| Commands | Inline code cho lệnh đơn |

---

## 5. Style Guide

- **Giải thích rõ ràng:** Tại sao giải pháp này hoạt động
- **Comment trong code:** Giải thích từng bước
- **Output mẫu:** Hiển thị kết quả mong đợi
- **Lỗi phổ biến:** Liệt kê và cách tránh

---

## 6. Review Checklist

- [ ] Mỗi Exercise có đầy đủ: Explanation, Code, Verification
- [ ] Có mục "Why This Solution?" giải thích tư duy ⭐
- [ ] Code chạy được, không có lỗi cú pháp
- [ ] Có giải thích tại sao giải pháp hoạt động
- [ ] Liệt kê lỗi thường gặp
- [ ] Có alternative solutions (nếu có)
- [ ] **Có Navigation Footer cuối file** ⭐
- [ ] `last_updated` là ngày hiện tại

---

## 7. Do's and Don'ts

### ✅ Nên làm

- Giải thích lý do lựa chọn giải pháp
- Thêm comment trong code
- Cung cấp output mẫu để verify
- Đề cập các cách giải khác

### ❌ Không nên làm

- Chỉ đưa code mà không giải thích
- Bỏ qua error handling
- Sử dụng lệnh nguy hiểm không cảnh báo
- Quên verify output

---

## 8. Example Template (Copy-Paste)

```markdown
---
module: "1.4"
title: "Docker Fundamentals – Solutions"
track: "1"
version: "1.0"
last_updated: "2025-12-27"
exercises_covered: [1, 2, 3]
---

## MODULE 1.4 – Docker Fundamentals Solutions

### ⚠️ Important Notes
> **Lưu ý:** Hãy tự làm bài tập trước khi xem đáp án. Có thể có nhiều cách giải đúng, solution dưới đây chỉ là một trong số đó.

---

## Exercise 1: Build Your First Docker Image

### Problem Recap
Tạo Docker image cho một ứng dụng Node.js đơn giản in ra "Hello from Docker!"

### Solution Explanation
Chúng ta cần:
1. Tạo file Node.js đơn giản
2. Viết Dockerfile với base image `node:18-alpine`
3. Build và chạy image

### Step-by-Step Solution

#### Bước 1: Tạo thư mục project
```bash
mkdir my-first-docker
cd my-first-docker
```

#### Bước 2: Tạo file app.js

```javascript
// app.js - Simple Node.js application
console.log("Hello from Docker!");
```

#### Bước 3: Tạo Dockerfile

```dockerfile
# Dockerfile
# Sử dụng Node.js Alpine image (nhẹ, ~50MB)
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy file app.js vào container
COPY app.js .

# Command chạy khi container start
CMD ["node", "app.js"]
```

#### Bước 4: Build image

```bash
# Build image với tên hello-docker, tag v1
docker build -t hello-docker:v1 .
```

**Output mong đợi:**

```
[+] Building 5.2s (8/8) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/node:18-alpine
 => [1/2] FROM docker.io/library/node:18-alpine
 => [2/2] COPY app.js .
 => exporting to image
 => => naming to docker.io/library/hello-docker:v1
```

#### Bước 5: Chạy container

```bash
docker run hello-docker:v1
```

**Output mong đợi:**

```
Hello from Docker!
```

### Output Verification

```bash
# Kiểm tra image đã được tạo
docker images | grep hello-docker

# Output:
# hello-docker   v1    abc123def456   10 seconds ago   178MB
```

```bash
# Kiểm tra image size (phải < 200MB)
docker images hello-docker:v1 --format "{{.Size}}"

# Output: 178MB ✅
```

### Common Mistakes

| Lỗi | Nguyên nhân | Cách sửa |
|-----|-------------|----------|
| `COPY failed: file not found` | File app.js không tồn tại | Đảm bảo app.js cùng thư mục với Dockerfile |
| `node: not found` | Base image sai | Dùng đúng `FROM node:18-alpine` |
| Container không exit | Dùng `node` thay vì `node app.js` | Đảm bảo CMD đúng cú pháp |

### Alternative Solutions

**Cách 2: Dùng ENTRYPOINT thay CMD**

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY app.js .
ENTRYPOINT ["node"]
CMD ["app.js"]
```

**Cách 3: Inline script**

```dockerfile
FROM node:18-alpine
CMD ["node", "-e", "console.log('Hello from Docker!')"]
```

---

## Exercise 2: Multi-container with Port Mapping

### Problem Recap

Chạy NGINX container với port mapping và volume mount để serve static files.

### Solution Explanation

Chúng ta cần:

1. Tạo file HTML
2. Chạy NGINX với `-v` (volume mount) và `-p` (port mapping)
3. Verify qua browser

### Step-by-Step Solution

#### Bước 1: Tạo thư mục và file HTML

```bash
mkdir nginx-exercise
cd nginx-exercise

# Tạo file index.html
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Docker Exercise</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; }
        h1 { color: #0066cc; }
    </style>
</head>
<body>
    <h1>🐳 Hello from NGINX in Docker!</h1>
    <p>This page is served from a Docker container.</p>
</body>
</html>
EOF
```

#### Bước 2: Chạy NGINX container

```bash
# Lấy đường dẫn tuyệt đối của thư mục hiện tại
CURRENT_DIR=$(pwd)

# Chạy container với volume mount và port mapping
docker run -d \
  --name nginx-exercise \
  -p 8080:80 \
  -v "$CURRENT_DIR:/usr/share/nginx/html:ro" \
  nginx:alpine
```

**Giải thích flags:**

- `-d`: Detached mode (chạy background)
- `--name`: Đặt tên container
- `-p 8080:80`: Map host port 8080 → container port 80
- `-v`: Mount volume (`:ro` = read-only)

#### Bước 3: Verify

```bash
# Kiểm tra container đang chạy
docker ps

# Output:
# CONTAINER ID   IMAGE          COMMAND                  PORTS                  NAMES
# abc123...      nginx:alpine   "/docker-entrypoint.…"   0.0.0.0:8080->80/tcp   nginx-exercise
```

```bash
# Test bằng curl
curl http://localhost:8080
```

**Hoặc mở browser:** `http://localhost:8080`

#### Bước 4: Xem logs

```bash
# Xem logs
docker logs nginx-exercise

# Follow logs realtime
docker logs -f nginx-exercise
```

#### Bước 5: Cleanup

```bash
# Stop container
docker stop nginx-exercise

# Remove container
docker rm nginx-exercise
```

### Output Verification

```bash
# Kiểm tra port đang listen
curl -I http://localhost:8080

# Output:
# HTTP/1.1 200 OK
# Server: nginx/1.25.3
# Content-Type: text/html
```

### Common Mistakes

| Lỗi | Nguyên nhân | Cách sửa |
|-----|-------------|----------|
| `port is already allocated` | Port 8080 đã được dùng | Đổi sang port khác: `-p 8081:80` |
| `403 Forbidden` | Không có index.html | Đảm bảo file tồn tại trong thư mục mount |
| Volume không update | Cache browser | Hard refresh (Ctrl+F5) hoặc clear cache |

---

## Exercise 3: Docker Compose Multi-service

### Problem Recap

Tạo docker-compose.yml với 3 services: frontend (NGINX), backend (Node.js), database (PostgreSQL).

### Solution Explanation

Chúng ta cần:

1. Tạo cấu trúc thư mục
2. Viết docker-compose.yml với 3 services
3. Cấu hình networks, volumes, depends_on
4. Start và verify

### Step-by-Step Solution

#### Bước 1: Tạo cấu trúc thư mục

```bash
mkdir fullstack-app
cd fullstack-app

# Tạo thư mục cho mỗi service
mkdir frontend backend
```

#### Bước 2: Tạo Backend (Node.js)

**backend/package.json:**

```json
{
  "name": "backend",
  "version": "1.0.0",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.3"
  }
}
```

**backend/server.js:**

```javascript
const express = require('express');
const app = express();
const PORT = 3000;

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date() });
});

app.get('/api', (req, res) => {
  res.json({ message: 'Hello from Backend!' });
});

app.listen(PORT, () => {
  console.log(`Backend running on port ${PORT}`);
});
```

**backend/Dockerfile:**

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

#### Bước 3: Tạo Frontend (NGINX)

**frontend/index.html:**

```html
<!DOCTYPE html>
<html>
<head><title>Fullstack App</title></head>
<body>
    <h1>Frontend</h1>
    <p>Connected to Backend API</p>
</body>
</html>
```

**frontend/nginx.conf:**

```nginx
server {
    listen 80;
    location / {
        root /usr/share/nginx/html;
        index index.html;
    }
    location /api {
        proxy_pass http://backend:3000;
    }
}
```

#### Bước 4: Tạo docker-compose.yml

```yaml
# docker-compose.yml
version: "3.8"

services:
  # Frontend - NGINX
  frontend:
    image: nginx:alpine
    container_name: frontend
    ports:
      - "80:80"
    volumes:
      - ./frontend/index.html:/usr/share/nginx/html/index.html:ro
      - ./frontend/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - backend
    networks:
      - app-network

  # Backend - Node.js
  backend:
    build: ./backend
    container_name: backend
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://user:password@db:5432/mydb
      - NODE_ENV=development
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    networks:
      - app-network

  # Database - PostgreSQL
  db:
    image: postgres:15-alpine
    container_name: db
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  pgdata:
```

#### Bước 5: Start services

```bash
# Build và start tất cả services
docker-compose up -d --build

# Xem logs
docker-compose logs -f
```

#### Bước 6: Verify

```bash
# Kiểm tra tất cả services đang chạy
docker-compose ps

# Output:
# NAME       SERVICE    STATUS    PORTS
# backend    backend    running   0.0.0.0:3000->3000/tcp
# db         db         running   0.0.0.0:5432->5432/tcp
# frontend   frontend   running   0.0.0.0:80->80/tcp
```

```bash
# Test backend health
curl http://localhost:3000/health

# Test frontend
curl http://localhost:80
```

### Output Verification

```bash
# Kiểm tra networks
docker network ls | grep fullstack

# Kiểm tra volumes
docker volume ls | grep pgdata
```

### Common Mistakes

| Lỗi | Nguyên nhân | Cách sửa |
|-----|-------------|----------|
| Backend không connect được DB | DB chưa ready | Dùng `depends_on` với `condition: service_healthy` |
| NGINX 502 Bad Gateway | Backend chưa start | Kiểm tra backend logs, đợi healthcheck pass |
| Data mất khi restart | Chưa dùng volume | Thêm volume cho PostgreSQL |

---

## References

- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [NGINX Docker Image](https://hub.docker.com/_/nginx)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [GLOSSARY](../../resources/GLOSSARY.md)

---

[⬅️ EXERCISES](./EXERCISES.md) | [📚 Mục lục](../../README.md) | [QUIZ ➡️](./QUIZ.md)

```

---

*File này là chuẩn mẫu cho mọi `SOLUTIONS.md` trong khoá học DevOps.*
