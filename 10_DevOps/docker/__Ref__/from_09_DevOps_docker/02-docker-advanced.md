# 🐳 Docker nâng cao — Tối ưu hóa và Best Practices

> `[INTERMEDIATE]` — Viết Dockerfile xịn, Build nhanh, Chạy bảo mật

---

## 1. Multi-stage Builds (Tối ưu Image Size)

Vấn đề: Cài Node.js, `npm install`, TypeScript compiler... xong image nặng 1GB, nhưng lúc chạy chỉ cần thư mục `dist/` thả vào Nginx (bỏ đi source code, `node_modules`).

Giải pháp: **Multi-stage builds** — Dùng nhiều `FROM` trong 1 Dockerfile. Chỉ copy file cần thiết từ stage trước sang stage cuối.

```dockerfile
# Stage 1: Build (Tên stage là 'builder')
FROM node:18-alpine AS builder
WORKDIR /app

# Khai thác Layer Caching: Copy package.json trước
COPY package*.json ./
RUN npm ci

# Copy source code và build
COPY . .
RUN npm run build

# Stage 2: Production (Image cuối cùng)
FROM nginx:alpine
# Copy thư mục dist/ từ stage 'builder' sang thư mục chứa web của Nginx
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# KẾT QUẢ: Image build xong chỉ nặng ~20MB (Nginx + HTML/JS/CSS), bỏ đi hoàn toàn đống node_modules 1GB rác!
```

---

## 2. Layer Caching (Tăng tốc độ Build)

Mỗi chỉ thị `RUN`, `COPY`, `ADD` tạo ra một "Layer". Docker sẽ cache các layer này. Nó chỉ build lại từ layer bị thay đổi trở đi.

```dockerfile
# ❌ SAI:
COPY . .
RUN npm install
# Mỗi khi sửa code (app.js thay đổi) -> Layer COPY thay đổi -> `npm install` phải chạy lại từ đầu (Rất lâu!)

# ✅ ĐÚNG:
COPY package*.json ./
RUN npm install
COPY . .
# Sửa code (app.js) -> Chỉ build lại từ lệnh COPY . . trở đi. `npm install` lấy từ Cache (Chớp mắt là xong!)
```

---

## 3. Quản lý Dữ liệu (Volumes & Bind Mounts)

Docker containers là stateless (chết là mất hết). Cần lưu Database ra ngoài.

### Bind Mounts (Map thư mục máy host)
Tiện cho dev (Sửa file trên VSCode -> Update vào Docker tức thì).
```bash
docker run -v /Users/thanh/project:/app node npm start
```

### Docker Volumes (Docker tự quản lý)
Tiện cho Production Database. An toàn, không sợ lỡ tay xóa.
```bash
# Tạo volume
docker volume create my-db-data

# Dùng
docker run -v my-db-data:/var/lib/postgresql/data postgres
```

---

## 4. Docker Compose chuyên sâu

Chạy cùng lúc Frontend, Backend, Redis, DB.

```yaml
# docker-compose.yml
version: '3.8'

services:
  # 1. Frontend Server
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend  # Đợi backend start lên mới chạy

  # 2. Backend API
  backend:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      - DB_HOST=database   # Lấy tên service làm domain kết nối (DNS nội bộ Mạng Compose)
      - REDIS_HOST=cache
    env_file:
      - .env               # Đọc file bí mật từ máy host

  # 3. Cache
  cache:
    image: redis:alpine
    ports:
      - "6379:6379"

  # 4. Database (Lưu dữ liệu ra Volume để không mất khi docker-compose down)
  database:
    image: postgres:14-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data

# Khai báo Volumes dùng chung
volumes:
  pgdata:
```

```bash
# Lệnh hay dùng
docker-compose up -d --build   # Build lại image và chạy ngầm (Detached)
docker-compose down -v         # Tắt tất cả và Xóa luôn Volumes (Xóa sạch Data)
```

---

## 5. Security Best Practices (Bảo mật)

```dockerfile
# 1. Dùng base image Alpine (Siêu nhỏ bé ~5MB) để giảm Attack Surface (Càng ít package càng khó bị hack).
FROM node:18-alpine

# 2. Không chạy bằng user root! (Mặc định Docker chạy root).
# Tạo user thường
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# 3. Quét lỗ hổng Image trước khi đẩy lên Hub
# docker scan my-image:latest
```

---

## Các lỗi thường gặp

```
❌ Sai: Lưu config, mật khẩu trực tiếp trong Dockerfile (Ai pull image về đều đọc được).
✅ Đúng: Dùng biến môi trường (ENV) hoặc file `.env` khi chạy runtime. Giữ Image sạch sẽ 100%.

❌ Sai: Cài `curl`, `vim` vào Image Production để debug cho tiện.
✅ Đúng: Image Production chỉ chứa đúng thứ cần để CHẠY App. Đừng biến nó thành một máy ảo Ubuntu thu nhỏ.
```

---

## Bài tập thực hành

- [ ] Tạo Multi-stage build cho 1 dự án Webpack/Vite (Stage 1 xài Node để run build. Stage 2 xài Nginx chỉ bốc thư mục dist sang).
- [ ] Chỉnh sửa Dockerfile thêm một user `non-root` rồi kiểm tra xem user đang chạy có phải ID 1000 không.
- [ ] Soạn `docker-compose.yml` có Network riêng cho Frontend và Backend. Chỉ backend mới được gọi Database.

---

## Tài nguyên thêm
- [Dockerfile Best Practices Official](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- Vọc thêm lệnh: `docker system prune -a` (Dọn dẹp hàng chục GB rác của Image/Container/Volume cũ mèm trên máy tính bạn).
