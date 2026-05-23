# 🐳 Docker — Dockerfile Basics — Bài Tập Thực Hành

---

## 📋 Metadata

- **Parent Lesson:** [../lesson.md](../lesson.md)
- **Type:** `[Exercise/Project]`
- **Difficulty:** `[Medium]`
- **Estimated Time:** 1.5-2 giờ
- **Prerequisites:** [Lesson 02](../02-Images-Containers/lesson.md)

---

## 🎯 Mục Tiêu

Thực hành viết Dockerfile với multi-stage build, .dockerignore, và best practices.

---

## 📝 Bài Tập

### Bài 1: Simple Dockerfile — Node.js App

**Task:** Viết Dockerfile cho Node.js Express app

**Project structure:**
```
node-app/
├── server.js
├── package.json
├── package-lock.json
└── Dockerfile
```

**server.js:**
```javascript
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('Hello from Dockerized Node.js App!');
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

**package.json:**
```json
{
  "name": "node-docker-app",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  }
}
```

**Yêu cầu Dockerfile:**

```dockerfile
# Base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Run as non-root (optional but recommended)
# USER node

CMD ["npm", "start"]
```

**Tasks:**
1. Tạo project structure với các files trên
2. Viết Dockerfile theo yêu cầu
3. Build image: `docker build -t node-app:v1 .`
4. Run container: `docker run -d -p 3000:3000 --name my-node-app node-app:v1`
5. Test: `http://localhost:3000`
6. Check logs: `docker logs my-node-app`

**Ghi lại:**
- Image size: ______
- Container logs output: ______

---

### Bài 2: Multi-stage Build — Reduce Image Size

**Task:** Tối ưu Dockerfile từ Bài 1 với multi-stage build

**Yêu cầu:**
```dockerfile
# Stage 1: Builder
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build  # Giả sử có build step (hoặc bỏ qua nếu không có)

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
# Copy từ builder (chỉ cần dist/ và node_modules)
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

**So sánh:**
```bash
# Image từ Bài 1 (single-stage)
docker images | grep node-app

# Image từ Bài 2 (multi-stage)
docker images | grep node-app-multi  # Đổi tên image khác
```

**Câu hỏi:**
1. Image size giảm bao nhiêu %? ______
2. Tại sao multi-stage nhỏ hơn? ___________________

---

### Bài 3: .dockerignore

**Task:** Tạo `.dockerignore` file với nội dung:

```
node_modules
npm-debug.log
.git
.env
Dockerfile
.dockerignore
README.md
dist/
coverage/
```

**Test:**
```bash
# Xem build context size
docker build -t node-app:test .

# Output sẽ show "Sending build context" — có thể thấy context size giảm
```

---

### Bài 4: Python Flask App (Optional Challenge)

**Task:** Viết Dockerfile cho Python Flask app (đã có code trong Exercise 1 của Lesson 03)

**Yêu cầu:**
1. Base image: `python:3.11-slim`
2. Install system dependencies (nếu cần)
3. Copy `requirements.txt`, `pip install --no-cache-dir`
4. Copy source code
5. Expose port 5000
6. Multi-stage build (optional) — thử giảm size
7. Run as non-root user

**Bonus:** Thêm `LABEL` metadata:
```dockerfile
LABEL maintainer="Your Name <email@example.com>"
LABEL org.opencontainers.image.version="1.0.0"
```

---

## 💡 Hints

### Hint 1: Layer Caching Order

Đặt steps ít thay đổi ở trên, thay đổi thường xuyên ở dưới:

```dockerfile
# Tốt:
COPY package*.json ./  # Ít thay đổi
RUN npm install        # Rebuild khi package.json đổi
COPY . .               # Thay đổi thường xuyên (source code)

# Không tốt:
COPY . .               # Rebuild mọi lần vì source thay đổi
COPY package*.json ./
RUN npm install
```

---

### Hint 2: Reduce Layers

Combine RUN commands:

```dockerfile
# Tốt (1 layer):
RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Không tối ưu (3 layers):
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y python3
```

---

## ✅ Success Criteria

**Pass:**
- ✅ Hoàn thành Bài 1 (simple Dockerfile, image chạy được)
- ✅ Hoàn thành Bài 2 (multi-stage, image size giảm ≥30%)
- ✅ Hoàn thành Bài 3 (.dockerignore)
- ✅ Hiểu layer caching và áp dụng vào Dockerfile optimization

**Excellent:**
- ⭐ Hoàn thành Bài 4 (Python Flask multi-stage)
- ⭐ Image size tối ưu (Python app <100MB, Node app <150MB)
- ⭐ Dockerfile clean, readable, có comments
- ⭐ Follow best practices (non-root user, specific tags, cleanup,...)

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
