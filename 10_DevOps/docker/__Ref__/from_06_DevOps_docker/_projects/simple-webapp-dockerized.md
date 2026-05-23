# 🐳 Docker — Mini Project: Dockerize a Web Application

---

## 📋 Metadata

- **Parent Lesson:** [../README.md](../README.md)
- **Type:** `[Mini-Project]`
- **Difficulty:** `[Medium]`
- **Estimated Time:** 2-3 giờ
- **Prerequisites:** Hoàn thành Lessons 01, 02, 03

---

## 🎯 Mục Tiêu

Build hoàn chỉnh Docker image cho một web application, bao gồm:
- Multi-stage Dockerfile
- `.dockerignore` optimization
- Docker Compose (optional — cho multi-container)
- Best practices (non-root user, layer caching,...)
- Push image lên Docker Hub (optional)

---

## 📝 Mô Tả Project

**Tên project:** "Simple Web App Dockerization"

**Mục tiêu:** Dockerize một Node.js/Python web app (bạn chọn) với đầy đủ best practices.

**Deliverables:**
- [ ] Working Dockerfile với multi-stage build
- [ ] `.dockerignore` file
- [ ] Built Docker image (<150MB cho Node.js, <100MB cho Python)
- [ ] Container running thành công
- [ ] README.md với build và run instructions
- [ ] (Optional) docker-compose.yml cho multi-service
- [ ] (Optional) Push image lên Docker Hub

---

## 🗂️ Project Structure

```
docker-webapp-project/
├── src/                    # Source code
│   ├── app.js (hoặc app.py)
│   ├── package.json (hoặc requirements.txt)
│   └── ...
├── Dockerfile              # Multi-stage Dockerfile
├── .dockerignore           # Exclude patterns
├── docker-compose.yml      # (Optional) Multi-container
├── README.md               # Project documentation
└── tests/                  # (Optional) Tests
```

---

## 🚀 Các Bước Thực Hiện

### Phase 1: Setup Project (30 phút)

1. **Chọn ngôn ngữ:** Node.js hoặc Python
2. **Tạo project structure** với files cơ bản:
   - `src/app.js` hoặc `src/app.py` — simple "Hello World" web app
   - `package.json` hoặc `requirements.txt`
3. **Test locally** (không dùng Docker):
   ```bash
   node src/app.js
   # hoặc
   python src/app.py
   ```
   Verify `http://localhost:3000` hoạt động.

---

### Phase 2: Viết Dockerfile — Single Stage (45 phút)

**Yêu cầu:**
- Base image: `node:18-alpine` hoặc `python:3.11-slim`
- Set `WORKDIR /app`
- Copy dependencies (`package*.json` hoặc `requirements.txt`)
- Install dependencies (`npm ci --only=production` hoặc `pip install --no-cache-dir -r requirements.txt`)
- Copy source code
- `EXPOSE 3000`
- `CMD ["node", "src/app.js"]` hoặc `CMD ["python", "src/app.py"]`

**Build & test:**
```bash
docker build -t myapp:single .
docker run -d -p 3000:3000 --name test-app myapp:single
```

Test: `http://localhost:3000`

**Check image size:**
```bash
docker images | grep myapp
```

---

### Phase 3: Multi-Stage Optimization (45 phút)

**Chuyển sang multi-stage build:**

```dockerfile
# Stage 1: Builder
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
# (nếu có build step: RUN npm run build)

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
COPY --from=builder /app/src ./src
# Copy --from=builder /app/dist ./dist  # nếu có build step

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

EXPOSE 3000
CMD ["node", "src/app.js"]
```

**Build và so sánh:**
```bash
docker build -t myapp:multi .
docker images | grep myapp
```

**Câu hỏi:**
- Image size giảm bao nhiêu %? ______
- Tại sao? (trả lời trong README)

---

### Phase 4: .dockerignore & Final Polish (30 phút)

**Tạo `.dockerignore`:**
```
node_modules
npm-debug.log
.git
.env
Dockerfile
.dockerignore
README.md
tests/
coverage/
dist/
```

**Rebuild và verify build context nhỏ hơn:**
```bash
docker build -t myapp:final .
```

---

### Phase 5: Documentation (30 phút)

**Viết `README.md` với nội dung:**

```markdown
# Dockerized Web App

## Overview

[Giải thích project là gì, dùng tech stack gì]

## Project Structure

```
docker-webapp-project/
├── src/
│   └── app.js
├── Dockerfile
├── .dockerignore
├── docker-compose.yml (nếu có)
└── README.md
```

## Build Image

```bash
docker build -t myapp:latest .
```

## Run Container

```bash
docker run -d -p 3000:3000 --name myapp myapp:latest
```

## Multi-stage vs Single-stage

Image size comparison:
- Single-stage: XXX MB
- Multi-stage: XXX MB
- Improvement: XX%

## Docker Compose (Optional)

```bash
docker-compose up -d
```

## Push to Docker Hub (Optional)

```bash
docker tag myapp:latest yourusername/myapp:latest
docker push yourusername/myapp:latest
```

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0
```

---

## ✅ Rubric Đánh Giá

| Tiêu chí | Weight | Pass (✓) | Excellent (⭐) |
|----------|--------|----------|---------------|
| **Functionality** | 30% | App chạy trong container | App chạy, expose port đúng, health check |
| **Dockerfile Quality** | 30% | Dockerfile cơ bản | Multi-stage, non-root user, best practices |
| **Image Size** | 20% | < 300MB | <150MB (Node) / <100MB (Python) |
| **Documentation** | 10% | README cơ bản | README chi tiết, có comparison, push instructions |
| **.dockerignore** | 10% | Có file | Exclude đầy đủ, build context nhỏ |

**Tổng:** /100  
**Pass:** 70 điểm  
**Excellent:** 90 điểm

---

## 🔗 Tài Nguyên

### Dockerfile Reference

- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

### Sample Projects

- [Node.js Docker Examples](https://github.com/nodejs/docker-node)
- [Python Docker Examples](https://github.com/docker-library/python)

---

## 🎓 After This Project

Sau khi hoàn thành, bạn có thể:

- ✅ Đưa project vào portfolio
- ✅ Viết Dockerfile cho bất kỳ app nào
- ✅ Tối ưu image size với multi-stage builds
- ✅ Push images lên Docker Hub/private registry
- ✅ Chuẩn bị cho các project phức tạp hơn (microservices với Docker Compose)

---

## 🤝 Feedback

Nếu bạn hoàn thành project này:

1. Share your Dockerfile và image size trong [Discussion](link-to-discussion)
2. Gửi feedback về bài học Docker series
3. Contribute improvements cho repo này!

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
