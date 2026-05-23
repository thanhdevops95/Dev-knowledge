# PROJECT.md Design Specification

## 1. Purpose

- **Mục đích:** Cung cấp dự án mini (Capstone/Mini Project) để học viên tổng hợp và áp dụng toàn bộ kiến thức đã học trong module.
- **Mục tiêu:** Xây dựng một sản phẩm hoàn chỉnh, có thể demo và đưa vào portfolio.
- **Thời gian:** 2-4 giờ (tùy độ phức tạp của module)

---

## 2. File Header (Metadata)

```yaml
---
module: "X.Y"
title: "<Tên Module> – Project"
track: "<Số Track>"
version: "1.0"
last_updated: "YYYY-MM-DD"
difficulty: "Beginner | Intermediate | Advanced"
estimated_time: "2-4 hours"
technologies: ["Docker", "NGINX", "Git"]
---
```

---

## 3. Required Sections (theo thứ tự bắt buộc)

### 3.1. Header

```markdown
## MODULE X.Y – <Tên Module> Project
### 🚀 <Tên Dự Án>
```

### 3.2. Project Overview (Tổng quan dự án)

- Mô tả ngắn gọn về dự án
- Tại sao dự án này quan trọng
- Sản phẩm cuối cùng là gì

### 3.3. Learning Objectives (Mục tiêu học tập)

- Checklist các kỹ năng sẽ được áp dụng
- Liên kết với các module đã học

### 3.4. Prerequisites (Yêu cầu)

- Checklist kiến thức cần có
- Công cụ cần cài đặt
- Tài nguyên cần chuẩn bị

### 3.5. Architecture Diagram (Sơ đồ kiến trúc)

- Diagram tổng quan hệ thống
- Mô tả các thành phần
- Luồng dữ liệu

### 3.6. Project Requirements (Yêu cầu dự án)

- **Functional Requirements:** Chức năng bắt buộc
- **Non-functional Requirements:** Hiệu năng, bảo mật, khả năng mở rộng
- **Bonus Features:** Tính năng nâng cao (không bắt buộc)

### 3.7. Step-by-Step Implementation (Hướng dẫn từng bước)

- Các milestone chính
- Hướng dẫn chi tiết cho mỗi bước
- Checkpoint để verify

### 3.8. Expected Deliverables (Sản phẩm cần nộp)

- Danh sách files/folders
- Format yêu cầu
- Documentation cần có

### 3.9. Evaluation Criteria (Tiêu chí đánh giá)

- Bảng điểm chi tiết
- Điểm pass
- Điểm bonus

### 3.10. Submission Guidelines (Hướng dẫn nộp bài)

- Cách đặt tên
- Format nén
- Nơi nộp

### 3.11. References (Tham khảo)

- Tài liệu liên quan
- Ví dụ tham khảo

### 3.12. Navigation Footer ⭐ BẮT BUỘC

Cuối mỗi file phải có điều hướng:

```markdown
---

[⬅️ QUIZ](./QUIZ.md) | [📚 Mục lục](../../README.md) | [Bài tiếp ➡️](../X.Y+1_Folder/README.md)
```

---

## 4. Formatting Rules

| Thành phần | Quy tắc |
|------------|---------|
| Tiêu đề | `##` cho chính, `###` cho mục con |
| Diagram | Image hoặc ASCII art |
| Code | Block với ngôn ngữ phù hợp |
| Checklist | `- [ ]` format |
| Milestone | Đánh số: Phase 1, Phase 2... |

---

## 5. Style Guide

- **Thực tế:** Dự án gắn với công việc thực tế
- **Hoàn chỉnh:** Có thể demo được
- **Portfolio-worthy:** Có thể đưa vào CV
- **Scalable:** Có thể mở rộng thêm

---

## 6. Review Checklist

- [ ] Có đầy đủ 12 sections bắt buộc
- [ ] Architecture diagram rõ ràng (sử dụng Mermaid.js nếu có thể)
- [ ] Requirements cụ thể, có thể kiểm tra
- [ ] Step-by-step đủ chi tiết để follow
- [ ] Evaluation criteria công bằng
- [ ] **Có Navigation Footer cuối file** ⭐
- [ ] `last_updated` là ngày hiện tại

---

## 7. Do's and Don'ts

### ✅ Nên làm

- Thiết kế dự án có thể đưa vào portfolio
- Cung cấp starter code nếu cần
- Có nhiều mức độ hoàn thành (basic → advanced)
- Guide từng bước nhưng không đưa đáp án hoàn chỉnh

### ❌ Không nên làm

- Dự án quá đơn giản, không có giá trị
- Yêu cầu mơ hồ, không verify được
- Bỏ qua bonus features
- Thiếu architecture diagram

---

## 8. Example Template (Copy-Paste)

```markdown
---
module: "1.4"
title: "Docker Fundamentals – Project"
track: "1"
version: "1.0"
last_updated: "2025-12-27"
difficulty: "Intermediate"
estimated_time: "3-4 hours"
technologies: ["Docker", "Docker Compose", "NGINX", "Node.js", "PostgreSQL"]
---

## MODULE 1.4 – Docker Fundamentals Project

### 🚀 DevBlog - Containerized Blog Platform

---

## 1. Project Overview

### Mô tả
Bạn sẽ xây dựng **DevBlog** - một nền tảng blog đơn giản được containerize hoàn toàn bằng Docker. Dự án bao gồm:
- **Frontend:** Static HTML/CSS served by NGINX
- **Backend API:** Node.js Express server
- **Database:** PostgreSQL để lưu trữ bài viết

### Tại sao dự án này quan trọng?
- Áp dụng tất cả kiến thức Docker đã học
- Thực hành multi-container application
- Có sản phẩm hoàn chỉnh để demo

### Sản phẩm cuối cùng
Một blog platform có thể:
- Hiển thị danh sách bài viết
- Xem chi tiết bài viết
- Thêm bài viết mới (qua API)

---

## 2. Learning Objectives

Sau khi hoàn thành dự án, bạn sẽ:
- [ ] Viết được Dockerfile cho Node.js application
- [ ] Sử dụng Docker Compose để quản lý multi-container
- [ ] Cấu hình NGINX làm reverse proxy
- [ ] Persist data với Docker volumes
- [ ] Troubleshoot container issues

---

## 3. Prerequisites

### Kiến thức
- [ ] Đã hoàn thành MODULE 1.4 - Docker Fundamentals
- [ ] Hiểu cơ bản về Node.js và Express
- [ ] Biết cơ bản về SQL

### Công cụ
- [ ] Docker Desktop đã cài đặt
- [ ] Docker Compose (bundled with Docker Desktop)
- [ ] Text editor (VS Code recommended)
- [ ] Terminal/Command Line
- [ ] Git

### Tài nguyên
- [ ] Tài khoản Docker Hub (optional)
- [ ] Starter code (link below)

---

## 4. Architecture Diagram

```

┌─────────────────────────────────────────────────────────────┐
│                        DevBlog Architecture                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │   Browser    │    │   NGINX      │    │   Backend    │   │
│  │              │───▶│   (Frontend) │───▶│   (API)      │   │
│  │  Port: 80    │    │   Port: 80   │    │   Port: 3000 │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│                                                 │            │
│                                                 │            │
│                                                 ▼            │
│                                          ┌──────────────┐   │
│                                          │  PostgreSQL  │   │
│                                          │  Port: 5432  │   │
│                                          │  (with Vol)  │   │
│                                          └──────────────┘   │
│                                                              │
│  ────────────────────────────────────────────────────────── │
│  Docker Network: devblog-network                             │
│  Volume: pgdata                                              │
└─────────────────────────────────────────────────────────────┘

```

### Mô tả các thành phần

| Component | Image | Port | Mô tả |
|-----------|-------|------|-------|
| Frontend | nginx:alpine | 80 | Serve static files + reverse proxy |
| Backend | node:18-alpine | 3000 | REST API server |
| Database | postgres:15-alpine | 5432 | Data storage |

---

## 5. Project Requirements

### 5.1 Functional Requirements (Bắt buộc)

| ID | Requirement | Mô tả |
|----|-------------|-------|
| FR1 | Container Setup | Tạo Dockerfile cho backend |
| FR2 | Docker Compose | Định nghĩa 3 services trong docker-compose.yml |
| FR3 | Networking | Tất cả containers trong cùng network |
| FR4 | Volume | PostgreSQL data được persist |
| FR5 | Reverse Proxy | NGINX proxy `/api` requests tới backend |
| FR6 | Homepage | Hiển thị danh sách bài viết |
| FR7 | API Endpoints | GET /api/posts, POST /api/posts |

### 5.2 Non-functional Requirements

| ID | Requirement | Mô tả |
|----|-------------|-------|
| NFR1 | Image Size | Backend image < 300MB |
| NFR2 | Startup Time | Toàn bộ stack start < 60s |
| NFR3 | Health Check | Backend có healthcheck endpoint |
| NFR4 | Logging | Logs có thể xem qua `docker-compose logs` |

### 5.3 Bonus Features (Không bắt buộc)

| ID | Feature | Điểm bonus |
|----|---------|------------|
| B1 | Multi-stage build | +5 |
| B2 | Environment variables file (.env) | +5 |
| B3 | Database initialization script | +5 |
| B4 | README with setup instructions | +5 |
| B5 | Docker image pushed to Docker Hub | +10 |

---

## 6. Step-by-Step Implementation

### Phase 1: Project Setup (30 mins)

#### 1.1 Tạo cấu trúc thư mục

```bash
mkdir devblog
cd devblog

# Tạo thư mục cho mỗi service
mkdir frontend backend database

# Tạo các file cần thiết
touch docker-compose.yml
touch .env
touch README.md
```

**Cấu trúc cuối cùng:**

```
devblog/
├── docker-compose.yml
├── .env
├── README.md
├── frontend/
│   ├── index.html
│   └── nginx.conf
├── backend/
│   ├── Dockerfile
│   ├── package.json
│   ├── server.js
│   └── ...
└── database/
    └── init.sql
```

#### 1.2 Checkpoint

- [ ] Thư mục đã được tạo
- [ ] Cấu trúc đúng như trên

---

### Phase 2: Backend Development (45 mins)

#### 2.1 Tạo backend/package.json

```json
{
  "name": "devblog-api",
  "version": "1.0.0",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.3",
    "cors": "^2.8.5"
  }
}
```

#### 2.2 Tạo backend/server.js

Yêu cầu:

- Express server on port 3000
- GET /health - health check
- GET /api/posts - list all posts
- POST /api/posts - create new post
- Connect to PostgreSQL

**Gợi ý:**

```javascript
// Cấu trúc cơ bản
const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// TODO: Implement routes

app.listen(3000, () => console.log('API running on port 3000'));
```

#### 2.3 Tạo backend/Dockerfile

Yêu cầu:

- Base: node:18-alpine
- WORKDIR: /app
- Install dependencies
- EXPOSE 3000
- CMD npm start

#### 2.4 Checkpoint

- [ ] package.json đúng dependencies
- [ ] server.js có đầy đủ endpoints
- [ ] Dockerfile đúng syntax

---

### Phase 3: Frontend Development (30 mins)

#### 3.1 Tạo frontend/index.html

- HTML page hiển thị blog posts
- Fetch data từ /api/posts
- Form để add new post

#### 3.2 Tạo frontend/nginx.conf

Yêu cầu:

- Serve static files từ /usr/share/nginx/html
- Proxy /api/* tới backend:3000

#### 3.3 Checkpoint

- [ ] index.html hiển thị đúng
- [ ] nginx.conf có reverse proxy config

---

### Phase 4: Database Setup (20 mins)

#### 4.1 Tạo database/init.sql

```sql
-- Create posts table
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO posts (title, content) VALUES
    ('Hello Docker', 'This is my first containerized blog post!'),
    ('Learning DevOps', 'Docker makes deployment so much easier.');
```

#### 4.2 Checkpoint

- [ ] SQL syntax đúng
- [ ] Có sample data

---

### Phase 5: Docker Compose (45 mins)

#### 5.1 Tạo .env file

```env
POSTGRES_USER=devblog
POSTGRES_PASSWORD=secret123
POSTGRES_DB=devblog
```

#### 5.2 Tạo docker-compose.yml

Yêu cầu:

- Version: "3.8"
- 3 services: frontend, backend, db
- Network: devblog-network
- Volume: pgdata cho PostgreSQL
- Backend depends_on db với healthcheck
- Frontend depends_on backend

#### 5.3 Build và Test

```bash
# Build và start
docker-compose up -d --build

# Xem logs
docker-compose logs -f

# Test endpoints
curl http://localhost:80
curl http://localhost:80/api/posts
```

#### 5.4 Checkpoint

- [ ] `docker-compose ps` shows 3 healthy containers
- [ ] Frontend accessible at port 80
- [ ] API returns posts

---

### Phase 6: Documentation (20 mins)

#### 6.1 Tạo README.md

Bao gồm:

- Project description
- Prerequisites
- How to run
- API documentation
- Screenshots

---

## 7. Expected Deliverables

### Files cần nộp

```
devblog/
├── docker-compose.yml          ✅ Required
├── .env                        ✅ Required
├── README.md                   ✅ Required
├── frontend/
│   ├── index.html              ✅ Required
│   └── nginx.conf              ✅ Required
├── backend/
│   ├── Dockerfile              ✅ Required
│   ├── package.json            ✅ Required
│   ├── server.js               ✅ Required
│   └── ...
├── database/
│   └── init.sql                ✅ Required
└── screenshots/
    ├── homepage.png            ✅ Required
    ├── api-response.png        ✅ Required
    └── docker-ps.png           ✅ Required
```

### Screenshots cần có

1. Homepage hiển thị posts
2. API response từ /api/posts
3. Output của `docker-compose ps`

---

## 8. Evaluation Criteria

| Tiêu chí | Điểm | Mô tả |
|----------|------|-------|
| **Docker Setup** | 25 | Dockerfile, docker-compose.yml đúng |
| **Functionality** | 25 | API hoạt động, data persist |
| **Architecture** | 15 | Networking, volumes đúng |
| **Code Quality** | 15 | Clean code, comments |
| **Documentation** | 10 | README rõ ràng |
| **Screenshots** | 10 | Đầy đủ và rõ ràng |
| **Bonus Features** | +30 | Xem bảng bonus ở trên |
| **Tổng** | **100 (+30)** | |

### Thang điểm

- **90-100+:** Xuất sắc ⭐⭐⭐
- **80-89:** Tốt ⭐⭐
- **70-79:** Pass ⭐
- **< 70:** Cần làm lại

---

## 9. Submission Guidelines

1. **Tên folder:** `<HọTên>_Module1.4_Project`
2. **Format:** Nén thành file `.zip`
3. **Bao gồm:** Tất cả files + screenshots + README
4. **Không bao gồm:** node_modules, .git, volumes data
5. **Nộp qua:** [Link nộp bài]

---

## 10. References

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [NGINX as Reverse Proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Node.js with PostgreSQL](https://node-postgres.com/)

---

## 11. Starter Code (Optional)

Nếu cần starter code, download từ: [link-to-starter-code]

---

### 💡 Tips

1. **Test từng service riêng lẻ** trước khi combine
2. **Đọc logs** khi gặp lỗi: `docker-compose logs <service>`
3. **Rebuild** khi thay đổi code: `docker-compose up -d --build`
4. **Clean up** khi cần reset: `docker-compose down -v`

---

### 🎯 Good Luck

Hãy nhớ: Mục tiêu không chỉ là hoàn thành dự án, mà còn là hiểu sâu về Docker và containerization!

---

[⬅️ QUIZ](./QUIZ.md) | [📚 Mục lục](../../README.md) | [Bài tiếp ➡️](../1.5_NGINX_Basic/README.md)

```

---

*File này là chuẩn mẫu cho mọi `PROJECT.md` trong khoá học DevOps.*
