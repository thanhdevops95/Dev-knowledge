# Module 07: Docker

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Docker** | /ˈdɒkər/ | Nền tảng container hóa ứng dụng |
| **Container** | - | Đơn vị đóng gói ứng dụng + dependencies chạy độc lập |
| **Image** | - | Template để tạo container (như khuôn bánh) |
| **Dockerfile** | - | File định nghĩa cách build image |
| **Registry** | - | Kho lưu trữ images (Docker Hub, ECR) |
| **Docker Hub** | - | Registry công cộng của Docker |
| **Volume** | - | Nơi lưu dữ liệu persistent cho container |
| **Network** | - | Mạng cho phép containers giao tiếp |
| **Docker Compose** | - | Tool chạy nhiều containers cùng lúc |
| **Layer** | - | Lớp trong Docker image, được cache để build nhanh |
| **Port Mapping** | - | Ánh xạ port từ host vào container (-p 8080:80) |
| **Environment Variable** | - | Biến môi trường truyền vào container |
| **Build Context** | - | Thư mục chứa Dockerfile và source code |
| **Multi-stage Build** | - | Kỹ thuật tạo image nhỏ gọn hơn |

---

## 🎬 Câu chuyện mở đầu

Developer gửi code cho bạn deploy:

> "Chạy bằng `npm start`, cần Node.js v18, Redis, và 5 environment variables."

Bạn setup trên server production, chạy lệnh... và nhận:

```
Error: Cannot find module 'express'
```

Developer trả lời: **"Works on my machine!"** 🤷

Vấn đề này xảy ra vì:

- Node.js version khác nhau
- Dependencies không đầy đủ
- Config môi trường khác nhau

**Docker giải quyết vấn đề này.** Code chạy được ở máy dev → chạy được ở production.

---

## 📖 Docker là gì?

### Trước hết: Container là gì? (Định nghĩa từ gốc)

Để hiểu Docker, bạn cần hiểu **Container** là gì từ góc nhìn hệ điều hành.

**Bắt đầu từ Process:**

Khi bạn chạy một chương trình (ví dụ: `python app.py`), hệ điều hành tạo ra một **process**. Process này:

- Có bộ nhớ riêng
- Có thể đọc/ghi files trên disk
- Có thể mở network connections
- **Nhưng:** có thể "thấy" và bị ảnh hưởng bởi các process khác trên cùng máy

**Vấn đề thực tế:**

| Vấn đề | Ví dụ |
|--------|-------|
| **Conflict dependencies** | App A cần Python 2.7, App B cần Python 3.11 |
| **Khác biệt môi trường** | Dev dùng macOS, server dùng Ubuntu, config khác nhau |
| **Isolation yếu** | App A crash có thể ảnh hưởng App B |

**Container giải quyết bằng cách:**

> **Container = Process chạy trong môi trường cô lập và đóng gói sẵn**

Cụ thể, container là một (hoặc nhiều) process được **cô lập** khỏi phần còn lại của hệ thống:

- **Filesystem riêng:** Container có thư mục `/`, `/home`, `/etc` của riêng nó
- **Network riêng:** Container có IP riêng, không thấy network của host
- **Process space riêng:** Container không thấy các process khác
- **User space riêng:** Root trong container ≠ root trên host

**Và quan trọng nhất:** Toàn bộ môi trường (code, thư viện, config) được **đóng gói sẵn** vào một **Image**.

```
Process thông thường:              Container:
┌─────────────────────┐           ┌─────────────────────┐
│     Máy vật lý      │           │     Máy vật lý      │
│                     │           │                     │
│  App A    App B     │           │  ┌─────────────┐   │
│    │        │       │           │  │  Container  │   │
│    │        │       │           │  │ ┌─────────┐ │   │
│    │        │       │           │  │ │  App A  │ │   │
│    └────────┴───────│           │  │ │ +Python │ │   │
│          │          │           │  │ │ +libs   │ │   │
│   Chung filesystem  │           │  │ │ +config │ │   │
│   Chung network     │           │  │ └─────────┘ │   │
│   Có thể conflict   │           │  └──────┬──────┘   │
└─────────────────────┘           │     Cô lập        │
                                  └─────────────────────┘
```

**Docker là gì trong bức tranh này?**

> **Docker = Công cụ để tạo, chạy và quản lý containers**

Docker không phát minh ra container (Linux có từ 2008 với LXC). Docker làm cho việc sử dụng container trở nên **dễ dàng** thông qua:

- **Dockerfile:** Định nghĩa môi trường bằng code
- **Image:** Đóng gói môi trường thành file có thể share
- **Docker Hub:** Nơi chia sẻ images
- **Docker CLI:** Lệnh đơn giản để quản lý

---

### Container vs Virtual Machine

Bây giờ bạn đã hiểu Container là gì, hãy so sánh với **Virtual Machine (VM)** - một cách cô lập khác.

**Sự khác biệt cốt lõi:**

- **VM:** Mỗi VM có **một hệ điều hành riêng** chạy trên hypervisor
- **Container:** Tất cả containers **share kernel** của host OS, chỉ cô lập ở user space

```
┌──────────────────────────────────────────────────────────────┐
│                    VIRTUAL MACHINES                           │
├──────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐             │
│  │    App 1    │ │    App 2    │ │    App 3    │             │
│  ├─────────────┤ ├─────────────┤ ├─────────────┤             │
│  │  Libraries  │ │  Libraries  │ │  Libraries  │             │
│  ├─────────────┤ ├─────────────┤ ├─────────────┤             │
│  │  Guest OS   │ │  Guest OS   │ │  Guest OS   │  ← 3 OS!    │
│  │  (Ubuntu)   │ │  (CentOS)   │ │  (Debian)   │     riêng   │
│  └─────────────┘ └─────────────┘ └─────────────┘             │
│  ├──────────────────────────────────────────────┤            │
│  │              Hypervisor (VMware)              │            │
│  ├──────────────────────────────────────────────┤            │
│  │                   Host OS                     │            │
│  ├──────────────────────────────────────────────┤            │
│  │                  Hardware                     │            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                      CONTAINERS                               │
├──────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐             │
│  │    App 1    │ │    App 2    │ │    App 3    │             │
│  ├─────────────┤ ├─────────────┤ ├─────────────┤             │
│  │  Libraries  │ │  Libraries  │ │  Libraries  │             │
│  └─────────────┘ └─────────────┘ └─────────────┘             │
│  ├──────────────────────────────────────────────┤            │
│  │              Docker Engine                    │  ← Share   │
│  ├──────────────────────────────────────────────┤    1 OS!   │
│  │                   Host OS                     │            │
│  ├──────────────────────────────────────────────┤            │
│  │                  Hardware                     │            │
└──────────────────────────────────────────────────────────────┘
```

### So sánh trực tiếp

| Đặc điểm | VM | Container |
|----------|----|-----------|
| **Khởi động** | Phút (boot cả OS) | Giây (chỉ start process) |
| **Dung lượng** | GB (toàn bộ OS) | MB (chỉ app + libs) |
| **Isolation** | Hoàn toàn (OS riêng) | Cấp process (share kernel) |
| **Resource overhead** | Cao (mỗi VM cần RAM cho OS) | Thấp (chỉ RAM cho app) |
| **Số lượng trên 1 host** | 10-20 VMs | 100+ containers |
| **Use case** | Cần OS khác nhau, isolation cao | Microservices, CI/CD, dev env |

**Khi nào dùng gì?**

| Chọn VM khi... | Chọn Container khi... |
|----------------|----------------------|
| Cần chạy Windows trên Linux host | Deploy microservices |
| Cần isolation cấp OS (multi-tenant) | CI/CD pipelines |
| Legacy apps cần OS cụ thể | Development environments |
| Compliance yêu cầu VM | Cần scale nhanh (100+ instances) |

---

## 🏗️ Kiến trúc Docker

Trước khi bắt đầu dùng Docker, bạn cần hiểu **4 thành phần cốt lõi** và cách chúng liên quan với nhau. Đây là nền tảng để bạn không bị "mù" khi gặp lỗi.

### Các thành phần chính

```
┌──────────────────────────────────────────────────────────────┐
│                    DOCKER ARCHITECTURE                        │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Dockerfile ──build──▶ Image ──run──▶ Container              │
│                          │                                    │
│  (Recipe)             (Template)        (Running app)         │
│                          │                                    │
│                          ▼                                    │
│                    Docker Registry                            │
│                   (Docker Hub, ECR)                           │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

**Giải thích từng thành phần:**

| Thành phần | Giải thích | Ví dụ thực tế |
|------------|------------|---------------|
| **Dockerfile** | File text chứa các lệnh để build image. Giống như công thức nấu ăn - liệt kê từng bước. | `FROM node:18`, `COPY . .`, `RUN npm install` |
| **Image** | Kết quả của việc build Dockerfile. Đây là "template" bất biến, có thể chạy ở bất kỳ đâu. | `nginx:1.25`, `node:18-alpine`, `myapp:v1.0` |
| **Container** | Instance đang chạy của Image. Bạn có thể chạy nhiều containers từ cùng một image. | Một container nginx đang serve website |
| **Registry** | Nơi lưu trữ và chia sẻ images. Giống như GitHub cho code, nhưng cho Docker images. | Docker Hub, AWS ECR, Google GCR |

**Ẩn dụ dễ nhớ:**

- **Dockerfile** = Công thức nấu ăn (các bước cụ thể)
- **Image** = Bánh đã nướng xong, đóng hộp (sẵn sàng dùng)
- **Container** = Một miếng bánh đang được ăn (đang chạy)
- **Registry** = Siêu thị bán bánh (nơi lưu trữ và chia sẻ)

> 💡 **Điểm quan trọng:** Image là **bất biến (immutable)**. Khi container chạy và tạo dữ liệu mới, dữ liệu đó nằm trong container, không phải image. Đây là lý do bạn cần **volumes** để lưu dữ liệu persistent.

---

## 🚀 Docker Commands

Sau đây là các lệnh Docker bạn sẽ dùng **hàng ngày**. Tôi chia theo workflow thực tế: chạy → quản lý → debug → images.

> 💡 **Mẹo:** Bạn không cần nhớ hết. Bookmark trang này và dùng `docker --help` hoặc `docker <command> --help` khi cần.

### Chạy container

**Đây là lệnh quan trọng nhất.** `docker run` kết hợp nhiều bước: pull image (nếu chưa có) → tạo container → start container.

```bash
# Chạy container từ image
docker run nginx

# Chạy ở background (-d = detached)
docker run -d nginx

# Chạy với port mapping
docker run -d -p 8080:80 nginx
# Host:8080 → Container:80

# Chạy với tên cụ thể
docker run -d --name my-nginx -p 8080:80 nginx

# Chạy và xóa khi stop
docker run --rm nginx

# Chạy với environment variables
docker run -d -e "DB_HOST=localhost" myapp
```

### Quản lý containers

**Sau khi chạy container, bạn cần biết cách kiểm tra, dừng, xóa.** Đây là các lệnh bạn dùng khi debug hoặc clean up.

```bash
# Liệt kê containers đang chạy
docker ps

# Liệt kê tất cả (kể cả stopped)
docker ps -a

# Stop container
docker stop my-nginx

# Start container đã stop
docker start my-nginx

# Restart
docker restart my-nginx

# Xóa container
docker rm my-nginx

# Force remove (đang chạy)
docker rm -f my-nginx

# Xóa tất cả stopped containers
docker container prune
```

### Xem thông tin container

**Khi container có vấn đề, đây là các lệnh giúp bạn debug.** Logs là nơi đầu tiên bạn nên xem khi có lỗi.

```bash
# Logs
docker logs my-nginx
docker logs -f my-nginx  # Follow

# Exec command trong container
docker exec my-nginx ls /etc/nginx
docker exec -it my-nginx bash  # Interactive shell

# Inspect (chi tiết)
docker inspect my-nginx

# Stats (resource usage)
docker stats
```

### Quản lý images

**Images chiếm dung lượng disk.** Theo thời gian, bạn sẽ có nhiều images cũ, unused. Các lệnh sau giúp bạn quản lý.

```bash
# Liệt kê images
docker images

# Pull image từ registry
docker pull nginx:1.25

# Remove image
docker rmi nginx:1.25

# Xóa unused images
docker image prune
```

---

## 📄 Dockerfile

**Dockerfile là trái tim của Docker.** Đây là file bạn viết để định nghĩa cách build image. Mỗi dòng trong Dockerfile tạo ra một **layer** trong image.

> 💡 **Quan trọng:** Thứ tự các lệnh trong Dockerfile ảnh hưởng đến **cache** và **tốc độ build**. Những thứ ít thay đổi (như cài OS packages) nên đặt trước, code thay đổi thường xuyên nên đặt sau.

### Anatomy of Dockerfile

**Dưới đây là Dockerfile hoàn chỉnh cho một Node.js app.** Tôi sẽ giải thích từng dòng:

```dockerfile
# Base image
FROM node:18-alpine

# Metadata
LABEL maintainer="you@example.com"

# Set working directory
WORKDIR /app

# Copy package files first (for caching)
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy source code
COPY . .

# Environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/health || exit 1

# Command to run
CMD ["node", "server.js"]
```

**Giải thích từng lệnh Dockerfile:**

| Lệnh | Ý nghĩa |
|------|--------|
| `FROM node:18-alpine` | Bắt đầu từ image có sẵn. `alpine` là version nhỏ gọn (~5MB thay vì ~900MB). |
| `WORKDIR /app` | Tạo thư mục `/app` và cd vào đó. Tất cả lệnh sau sẽ chạy trong `/app`. |
| `COPY package*.json ./` | Copy `package.json` và `package-lock.json` vào container trước. |
| `RUN npm install` | Chạy lệnh cài dependencies. Kết quả được lưu vào layer. |
| `COPY . .` | Copy toàn bộ source code vào container. |
| `ENV NODE_ENV=production` | Set biến môi trường. App sẽ thấy biến này khi chạy. |
| `EXPOSE 3000` | Khai báo container sẽ lắng nghe port 3000. (Đây chỉ là documentation, không tự mở port) |
| `HEALTHCHECK` | Docker sẽ kiểm tra container có healthy không theo interval. |
| `CMD ["node", "server.js"]` | Lệnh chạy khi container start. Dùng dạng exec (array) thay vì shell. |

### Layer caching

**Tại sao cần hiểu layer caching?** Vì nó quyết định tốc độ build. Nếu bạn sắp xếp Dockerfile đúng, build lần 2 chỉ mất vài giây thay vì vài phút.

**Nguyên tắc:** Mỗi lệnh trong Dockerfile tạo một layer. Docker cache layer nếu không có thay đổi. Nhưng nếu một layer thay đổi, tất cả layers sau nó cũng bị invalidate.

```dockerfile
# Layer 1: Base image (cached)
FROM node:18-alpine

# Layer 2: Install OS deps (cached if not changed)
RUN apk add --no-cache python3 make g++

# Layer 3: Copy package files (cached if not changed)
COPY package*.json ./

# Layer 4: Install deps (cached if packages unchanged)
RUN npm install

# Layer 5: Copy source (ALWAYS changes → invalidates cache)
COPY . .

# Tip: Put frequently changing stuff at the end!
```

### Multi-stage builds

**Vấn đề:** Image build thường rất lớn vì chứa cả build tools (gcc, npm dev dependencies...). Nhưng production chỉ cần code đã build.

**Giải pháp:** Multi-stage builds cho phép bạn dùng một image để build, rồi copy kết quả sang image nhỏ hơn cho production.

**Kết quả:** Image production có thể nhỏ hơn **10x** so với image build.

```dockerfile
# Stage 1: Build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Production (smaller image)
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/server.js"]
```

### Build image

```bash
# Build với tag
docker build -t myapp:v1.0 .

# Build với Dockerfile khác
docker build -f Dockerfile.prod -t myapp:prod .

# Build với build args
docker build --build-arg NODE_ENV=production -t myapp .
```

---

## 📦 Docker Compose

**Docker Compose** giải quyết vấn đề: "Tôi cần chạy nhiều containers cùng lúc và chúng cần nói chuyện với nhau".

Thay vì chạy 5 lệnh `docker run` riêng rẽ, bạn định nghĩa tất cả trong một file YAML và chạy `docker-compose up`.

### Khi nào cần Docker Compose?

| Tình huống | Dùng Docker Compose |
|-----------|---------------------|
| App + Database + Cache | ✅ Có |
| Microservices local development | ✅ Có |
| Một container đơn giản | ❌ Chỉ cần `docker run` |
| Production Kubernetes | ❌ Dùng K8s manifests |

### docker-compose.yml

**Dưới đây là ví dụ thực tế:** Web app (Node.js) + Database (PostgreSQL) + Cache (Redis). Tôi sẽ giải thích từng phần:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - REDIS_URL=redis://redis:6379
      - DB_URL=postgres://user:pass@db:5432/app
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Compose commands

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d web

# Stop all
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs -f web

# Rebuild
docker-compose up -d --build

# Scale
docker-compose up -d --scale web=3
```

---

## 🔗 Networking

### Network types

```bash
# Bridge (default) - isolated network
docker network create mynetwork

# List networks
docker network ls

# Run container on network
docker run -d --network mynetwork --name app myapp

# Containers on same network can communicate by name
# From app container: curl http://db:5432
```

### Docker Compose networking

```yaml
services:
  web:
    # Can reach db as "db" hostname
    environment:
      - DB_HOST=db
  db:
    # ...
```

---

## 💾 Volumes

### Types

```
┌─────────────────────────────────────────────────────────────┐
│                     VOLUME TYPES                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Named Volume (managed by Docker)                         │
│     docker run -v mydata:/app/data myapp                     │
│                                                              │
│  2. Bind Mount (host directory)                              │
│     docker run -v /host/path:/container/path myapp           │
│                                                              │
│  3. tmpfs (memory only)                                      │
│     docker run --tmpfs /app/cache myapp                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Commands

```bash
# Create volume
docker volume create mydata

# List volumes
docker volume ls

# Inspect
docker volume inspect mydata

# Remove unused
docker volume prune
```

---

## 🚨 Lỗi thường gặp khi học Docker

### 1. "Cannot connect to the Docker daemon"

**Triệu chứng:**

```bash
docker ps
# Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Nguyên nhân:** Docker daemon chưa chạy hoặc user không có quyền.

**Cách fix:**

```bash
# Trên Linux - khởi động Docker
sudo systemctl start docker

# Thêm user vào group docker (không cần sudo mỗi lần)
sudo usermod -aG docker $USER
# Logout và login lại
```

---

### 2. "Port already in use"

**Triệu chứng:**

```bash
docker run -p 80:80 nginx
# Error: bind: address already in use
```

**Nguyên nhân:** Port 80 đã có service khác đang dùng.

**Cách fix:**

```bash
# Tìm process đang dùng port
sudo lsof -i :80  # Linux/Mac
netstat -ano | findstr :80  # Windows

# Dùng port khác
docker run -p 8080:80 nginx
```

---

### 3. "No space left on device"

**Triệu chứng:** Build hoặc run fails với lỗi disk space.

**Nguyên nhân:** Docker images, containers, volumes cũ chiếm nhiều disk.

**Cách fix:**

```bash
# Xem disk usage của Docker
docker system df

# Xóa tất cả không dùng (CẢNH BÁO: xóa sạch!)
docker system prune -a --volumes

# Xóa từng loại
docker container prune  # Containers đã stop
docker image prune -a   # Images không dùng
docker volume prune     # Volumes không dùng
```

---

### 4. Container chạy rồi exit ngay

**Triệu chứng:**

```bash
docker run ubuntu
docker ps  # Không thấy container
docker ps -a  # Container đã exited
```

**Nguyên nhân:** Container chạy command xong thì exit. Ubuntu image chỉ chạy `/bin/bash` rồi thoát.

**Cách fix:**

```bash
# Chạy interactive mode
docker run -it ubuntu bash

# Hoặc chạy background với process luôn chạy
docker run -d ubuntu sleep infinity
```

---

### 5. "COPY failed: file not found"

**Triệu chứng:** Dockerfile build fails khi COPY file.

**Nguyên nhân:** File không nằm trong build context, hoặc bị .dockerignore loại bỏ.

**Cách fix:**

```bash
# Kiểm tra file có trong thư mục build không
ls -la

# Kiểm tra .dockerignore
cat .dockerignore

# Build với context đúng (. = thư mục hiện tại)
docker build -t myapp .
```

---

## 📝 Tổng kết Module 07

### Bạn đã học

✅ Docker vs VMs  
✅ Images, Containers, Registries  
✅ Docker commands  
✅ Dockerfile và best practices  
✅ Docker Compose  
✅ Networking và Volumes  

---

## ⏭️ Tiếp theo

👉 **[LABS.md - Thực hành Docker](LABS.md)**
