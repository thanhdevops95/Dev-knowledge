# CHEATSHEET.md Design Specification

## 1. Purpose

- **Mục đích:** Cung cấp bảng tra cứu nhanh các lệnh (Commands), cấu hình mẫu (Snippets) và tham chiếu hữu ích.
- **Sử dụng:** Học viên có thể copy-paste nhanh vào terminal hoặc file cấu hình mà không phải tìm kiếm lại.

---

## 2. File Header (Metadata)

```yaml
---
module: "X.Y"
title: "<Tên Module> – Cheatsheet"
track: "<Số Track>"
version: "1.0"
last_updated: "YYYY-MM-DD"
---
```

---

## 3. Required Sections (theo thứ tự bắt buộc)

### 3.1. Header

```markdown
## MODULE X.Y – <Tên Module> Cheatsheet
```

### 3.2. Quick Reference (Tham chiếu nhanh)

- Tóm tắt 3-5 điểm quan trọng nhất của module
- Dạng bullet points ngắn gọn

### 3.3. Common Commands (Các lệnh thường dùng)

- Bảng với 3 cột: Command | Description | Example
- Sắp xếp theo nhóm chức năng hoặc theo thứ tự sử dụng thường xuyên

### 3.4. Snippets / Config Samples (Cấu hình mẫu)

- Các đoạn code/config có thể copy-paste trực tiếp
- Mỗi snippet có tiêu đề và mô tả ngắn

### 3.5. Common Errors & Fixes (Lỗi thường gặp)

- Bảng với 3 cột: Error | Cause | Solution
- Liệt kê 3-5 lỗi phổ biến nhất

### 3.6. References (Tham khảo)

- Link tới docs chính thức
- Link tới các resources hữu ích

### 3.7. Navigation Footer ⭐ BẮT BUỘC

Cuối mỗi file phải có điều hướng:

```markdown
---

[⬅️ README](./README.md) | [📚 Mục lục](../../README.md) | [LABS ➡️](./LABS.md)
```

---

## 4. Formatting Rules

| Thành phần | Quy tắc |
|------------|---------|
| Tiêu đề | `##` cho chính, `###` cho mục con |
| Bảng | Markdown tables, căn chỉnh bằng `:` |
| Code | Inline: `` `code` ``, Block: 3 backticks + ngôn ngữ |
| Lệnh | Dùng `monospace` font |

---

## 5. Style Guide

- **Ngắn gọn:** Mỗi mô tả ≤ 15 từ
- **Rõ ràng:** Tránh viết tắt không giải thích
- **Thực tế:** Ví dụ phải chạy được

---

## 6. Review Checklist

- [ ] Header đúng định dạng
- [ ] Tất cả lệnh đã được kiểm tra trên môi trường thực
- [ ] Ví dụ rõ ràng, copy-paste được
- [ ] Bảng lỗi thường gặp đầy đủ
- [ ] Link tham khảo hoạt động
- [ ] **Có Navigation Footer cuối file** ⭐
- [ ] `last_updated` là ngày hiện tại

---

## 7. Do's and Don'ts

### ✅ Nên làm

- Kiểm tra lệnh trên môi trường thực trước khi đưa vào
- Sắp xếp theo nhóm chức năng logic
- Ghi chú các tùy chọn quan trọng
- Thêm comment trong code snippets

### ❌ Không nên làm

- Sử dụng lệnh deprecated
- Bỏ qua việc giải thích tham số
- Để ví dụ không chạy được

---

## 8. Example Template (Copy-Paste)

```markdown
---
module: "1.4"
title: "Docker Fundamentals – Cheatsheet"
track: "1"
version: "1.0"
last_updated: "2025-12-27"
---

## MODULE 1.4 – Docker Fundamentals Cheatsheet

### Quick Reference
- **Image:** Template read-only để tạo container
- **Container:** Instance đang chạy của image
- **Dockerfile:** File text chứa lệnh build image
- **Registry:** Nơi lưu trữ và phân phối images (Docker Hub)

---

### Common Commands

#### Image Management

| Command | Description | Example |
|---------|-------------|---------|
| `docker images` | Liệt kê tất cả images | `docker images` |
| `docker pull <image>` | Tải image từ registry | `docker pull nginx:alpine` |
| `docker build -t <name> .` | Build image từ Dockerfile | `docker build -t myapp:v1 .` |
| `docker rmi <image>` | Xóa image | `docker rmi myapp:v1` |
| `docker tag <src> <dst>` | Đặt tag cho image | `docker tag myapp:v1 myapp:latest` |

#### Container Management

| Command | Description | Example |
|---------|-------------|---------|
| `docker run -d <image>` | Chạy container background | `docker run -d nginx` |
| `docker run -p <host>:<container>` | Map port | `docker run -p 8080:80 nginx` |
| `docker ps` | Liệt kê containers đang chạy | `docker ps` |
| `docker ps -a` | Liệt kê tất cả containers | `docker ps -a` |
| `docker stop <id>` | Dừng container | `docker stop abc123` |
| `docker rm <id>` | Xóa container | `docker rm abc123` |
| `docker logs <id>` | Xem logs | `docker logs -f abc123` |
| `docker exec -it <id> sh` | Truy cập shell container | `docker exec -it abc123 /bin/sh` |

#### Volume & Network

| Command | Description | Example |
|---------|-------------|---------|
| `docker volume create` | Tạo volume | `docker volume create mydata` |
| `docker run -v <vol>:<path>` | Mount volume | `docker run -v mydata:/data nginx` |
| `docker network ls` | Liệt kê networks | `docker network ls` |
| `docker network create` | Tạo network | `docker network create mynet` |

---

### Snippets / Config Samples

#### Basic Dockerfile (Node.js App)

```dockerfile
# Dockerfile cho Node.js application
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

#### Multi-stage Build (Optimized)

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
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

#### Docker Compose (Web + DB)

```yaml
# docker-compose.yml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "8080:3000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
  
  db:
    image: postgres:15-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb

volumes:
  pgdata:
```

---

### Common Errors & Fixes

| Error | Cause | Solution |
|-------|-------|----------|
| `docker: command not found` | Docker chưa cài đặt | Cài Docker Desktop và restart terminal |
| `Cannot connect to Docker daemon` | Docker daemon không chạy | Start Docker Desktop hoặc `sudo systemctl start docker` |
| `port is already allocated` | Port đã được sử dụng | Đổi port hoặc stop container đang dùng port đó |
| `no space left on device` | Hết dung lượng disk | `docker system prune -a` để dọn dẹp |
| `permission denied` | Không có quyền Docker | Thêm user vào group docker: `sudo usermod -aG docker $USER` |

---

### References

- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Docker Hub](https://hub.docker.com/)
- [GLOSSARY](../../resources/GLOSSARY.md)

---

[⬅️ README](./README.md) | [📚 Mục lục](../../README.md) | [LABS ➡️](./LABS.md)

```

---

*File này là chuẩn mẫu cho mọi `CHEATSHEET.md` trong khoá học DevOps.*
