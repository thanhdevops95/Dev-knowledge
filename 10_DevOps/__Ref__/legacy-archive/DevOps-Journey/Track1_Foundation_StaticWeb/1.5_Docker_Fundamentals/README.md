# 🐳 Module 1.5: Docker Fundamentals

[![Duration](https://img.shields.io/badge/Duration-12--15%20hours-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Beginner--Intermediate-orange?style=flat-square)](.)

> **Containerization** - Package applications consistently.
>
> *Container hóa - Đóng gói ứng dụng một cách nhất quán.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Understand containers and how they differ from VMs (Hiểu Container khác VM như thế nào)
- ✅ Learn Docker architecture - daemon, client, registry (Hiểu kiến trúc Docker)
- ✅ Write Dockerfiles to build images (Viết Dockerfile để build images)
- ✅ Run and manage containers (Chạy và quản lý containers)
- ✅ Use Docker volumes and networks (Sử dụng ổ đĩa và mạng Docker)
- ✅ Push images to Docker Hub (Đẩy images lên Docker Hub)

---

## 📚 Content (Nội dung)

### 1. Introduction to Docker & Containers (Giới thiệu về Docker & Containers) - 1 hour

#### 1.1 What is Docker? (Docker là gì?)

**Docker** is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly.

*Docker là một nền tảng mở để phát triển, vận chuyển và chạy các ứng dụng. Docker cho phép bạn tách biệt ứng dụng khỏi hạ tầng để chuyển giao phần mềm nhanh chóng.*

#### 1.2 Virtual Machine

```
┌─────────────────────────────────────────────────────────────┐
│                    VIRTUAL MACHINES                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │    App A    │  │    App B    │  │    App C    │         │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤         │
│  │   Bins/Libs │  │   Bins/Libs │  │   Bins/Libs │         │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤         │
│  │  Guest OS   │  │  Guest OS   │  │  Guest OS   │ ← Heavy!│
│  │  (Ubuntu)   │  │  (CentOS)   │  │  (Debian)   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                      HYPERVISOR                              │
├─────────────────────────────────────────────────────────────┤
│                      HOST OS                                 │
├─────────────────────────────────────────────────────────────┤
│                    INFRASTRUCTURE                            │
└─────────────────────────────────────────────────────────────┘
```

**VM Characteristics (Đặc điểm VM):**

- ✅ Complete isolation (Cách ly hoàn toàn)
- ❌ Heavy - GBs per VM (Nặng - GB mỗi VM)
- ❌ Slow startup - minutes (Khởi động chậm - hằng phút)
- ❌ Resource intensive (Tốn tài nguyên)

#### 1.3 Container

```
┌─────────────────────────────────────────────────────────────┐
│                      CONTAINERS                              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │    App A    │  │    App B    │  │    App C    │         │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤         │
│  │   Bins/Libs │  │   Bins/Libs │  │   Bins/Libs │ ← Light!│
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                    DOCKER ENGINE                             │
├─────────────────────────────────────────────────────────────┤
│                      HOST OS                                 │
├─────────────────────────────────────────────────────────────┤
│                    INFRASTRUCTURE                            │
└─────────────────────────────────────────────────────────────┘
```

**Container Characteristics (Đặc điểm Container):**

- ✅ Lightweight - MBs (Nhẹ - MB)
- ✅ Fast startup - seconds (Khởi động nhanh - giây)
- ✅ Share kernel with host (Chia sẻ kernel với host)
- ✅ Portable - runs anywhere (Chạy ở đâu cũng được)

#### 1.4 Comparison (So sánh)

| Criteria | VM | Container |
|----------|-----|-----------|
| **Size** | GB | MB |
| **Startup** | Minutes (Hằng phút) | Seconds (Hằng giây) |
| **Isolation** | Complete (Hoàn toàn) | Process level (Mức tiến trình) |
| **OS** | Separate (OS riêng biệt) | Shared kernel (Chia sẻ kernel) |
| **Density** | Few VMs/host | Many containers/host |
| **Use case** | Multi-tenant, legacy | Microservices, CI/CD |

---

### 2. Docker Architecture (Kiến trúc Docker) - 1 hour

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCKER ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐                                       │
│  │   Docker Client  │  docker build, run, pull...          │
│  │   (CLI / API)    │                                       │
│  └────────┬─────────┘                                       │
│           │ REST API                                         │
│           ▼                                                  │
│  ┌──────────────────┐                                       │
│  │   Docker Daemon  │  dockerd                              │
│  │   (Docker Host)  │                                       │
│  ├──────────────────┤                                       │
│  │  ┌────────────┐  │                                       │
│  │  │  Images    │  │  ← Blueprints                        │
│  │  └────────────┘  │                                       │
│  │  ┌────────────┐  │                                       │
│  │  │ Containers │  │  ← Running instances                 │
│  │  └────────────┘  │                                       │
│  │  ┌────────────┐  │                                       │
│  │  │  Volumes   │  │  ← Persistent data                   │
│  │  └────────────┘  │                                       │
│  │  ┌────────────┐  │                                       │
│  │  │  Networks  │  │  ← Container communication           │
│  │  └────────────┘  │                                       │
│  └──────────────────┘                                       │
│           │                                                  │
│           ▼                                                  │
│  ┌──────────────────┐                                       │
│  │  Docker Registry │  Docker Hub, ECR, GCR...             │
│  │  (Image storage) │                                       │
│  └──────────────────┘                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Main Components (Các thành phần chính)

| Component | Description |
|-----------|-------------|
| **Docker Client** | CLI you use - `docker run`, `docker build` (Giao diện dòng lệnh bạn dùng) |
| **Docker Daemon** | Background service managing containers (Dịch vụ nền quản lý container) |
| **Docker Image** | Read-only template with app + dependencies (Bản mẫu chỉ đọc chứa app và thư viện) |
| **Docker Container** | Running instance of an image (Bản thể đang chạy của image) |
| **Docker Registry** | Image storage - Docker Hub, etc. (Nơi lưu trữ image) |

---

### 3. Docker Images - 2 hours

#### 3.1 Image Concept (Khái niệm Image)

**Image** = Read-only template containing (Template read-only chứa):

- Base OS (Alpine, Ubuntu, Debian...)
- Application code (Mã ứng dụng)
- Dependencies (libs, packages)
- Configuration (Cấu hình)

```
┌─────────────────────────────────────────┐
│           Docker Image Layers           │
├─────────────────────────────────────────┤
│  Layer 5: COPY app.js /app/             │ ← Your code
├─────────────────────────────────────────┤
│  Layer 4: RUN npm install               │ ← Dependencies
├─────────────────────────────────────────┤
│  Layer 3: WORKDIR /app                  │
├─────────────────────────────────────────┤
│  Layer 2: RUN apt-get update            │
├─────────────────────────────────────────┤
│  Layer 1: FROM node:18-alpine           │ ← Base image
└─────────────────────────────────────────┘
```

#### 3.2 Image Naming Convention (Quy ước đặt tên)

```
[registry/]repository[:tag]

Examples (Ví dụ):
nginx                          # Docker Hub, latest tag
nginx:alpine                   # Docker Hub, alpine tag
nginx:1.25.3                   # Specific version
myuser/myapp:v1.0              # User repository
gcr.io/project/app:latest      # Google Container Registry
123456789.dkr.ecr.region.amazonaws.com/app:v1  # AWS ECR
```

#### 3.3 Pull Images (Tải images)

```bash
# Pull image from Docker Hub (Tải image từ Docker Hub)
docker pull nginx
docker pull nginx:alpine
docker pull nginx:1.25.3

# View pulled images (Xem images đã tải)
docker images
docker image ls

# View image details (Xem chi tiết image)
docker image inspect nginx

# View history/layers (Xem lịch sử/layers)
docker history nginx
```

#### 3.4 Remove Images (Xóa images)

```bash
# Remove one image (Xóa 1 image)
docker rmi nginx
docker image rm nginx

# Remove multiple images (Xóa nhiều images)
docker rmi nginx redis mysql

# Remove all unused images (Xóa tất cả images không dùng)
docker image prune

# Remove all images - DANGEROUS! (Xóa tất cả - NGUY HIỂM!)
docker rmi $(docker images -q)
```

---

### 4. Docker Containers - 3 hours

#### 4.1 Running Containers (Chạy container)

```bash
# Run simple container (Chạy container đơn giản)
docker run nginx

# Run in background/detached (Chạy trong background)
docker run -d nginx

# Name the container (Đặt tên cho container)
docker run -d --name my-nginx nginx

# Map port (host:container)
docker run -d -p 8080:80 nginx
# Access: http://localhost:8080 (Truy cập)

# Map multiple ports (Map nhiều ports)
docker run -d -p 8080:80 -p 8443:443 nginx

# Run with environment variables (Chạy với biến môi trường)
docker run -d -e MYSQL_ROOT_PASSWORD=secret mysql

# Auto-remove when stopped (Tự động xóa khi dừng)
docker run --rm -it alpine sh
```

#### 4.2 Managing Containers (Quản lý containers)

```bash
# List running containers (Liệt kê containers đang chạy)
docker ps

# List all - including stopped (Liệt kê tất cả - kể cả đã dừng)
docker ps -a

# Stop container (Dừng container)
docker stop my-nginx
docker stop container_id

# Start stopped container (Start container đã dừng)
docker start my-nginx

# Restart container
docker restart my-nginx

# Remove container - must stop first (Xóa container - phải stop trước)
docker rm my-nginx

# Force remove - running (Force xóa - đang chạy)
docker rm -f my-nginx

# Remove all stopped containers (Xóa tất cả containers đã dừng)
docker container prune
```

#### 4.3 Interacting with Containers (Tương tác với container)

```bash
# View logs (Xem logs)
docker logs my-nginx
docker logs -f my-nginx         # Follow mode
docker logs --tail 100 my-nginx # Last 100 lines (100 dòng cuối)

# Enter container terminal (Vào terminal của container)
docker exec -it my-nginx bash
docker exec -it my-nginx sh     # If no bash (Nếu không có bash)

# Run command in container (Chạy lệnh trong container)
docker exec my-nginx cat /etc/nginx/nginx.conf

# Copy files (Sao chép files)
docker cp local_file.txt my-nginx:/path/in/container/
docker cp my-nginx:/path/in/container/file.txt ./local/

# View stats - CPU, Memory (Xem thống kê)
docker stats
docker stats my-nginx
```

#### 4.4 Container Lifecycle (Vòng đời Container)

```
┌─────────────────────────────────────────────────────────────┐
│                CONTAINER LIFECYCLE                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│       docker create                                          │
│            │                                                 │
│            ▼                                                 │
│     ┌──────────────┐                                        │
│     │   CREATED    │                                        │
│     └──────┬───────┘                                        │
│            │ docker start                                    │
│            ▼                                                 │
│     ┌──────────────┐  docker pause   ┌──────────────┐      │
│     │   RUNNING    │ ──────────────► │    PAUSED    │      │
│     └──────┬───────┘ ◄────────────── └──────────────┘      │
│            │          docker unpause                         │
│            │ docker stop                                     │
│            ▼                                                 │
│     ┌──────────────┐                                        │
│     │   STOPPED    │                                        │
│     └──────┬───────┘                                        │
│            │ docker rm                                       │
│            ▼                                                 │
│     ┌──────────────┐                                        │
│     │   DELETED    │                                        │
│     └──────────────┘                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### 5. Dockerfile - 3 hours

#### 5.1 What is Dockerfile? (Dockerfile là gì?)

**Dockerfile** = Text file containing instructions to build Docker image

*File text chứa các instructions để build Docker image*

#### 5.2 Basic Structure (Cấu trúc cơ bản)

```dockerfile
# Syntax (Cú pháp)
# INSTRUCTION arguments

# Comments start with # (Comment bắt đầu bằng #)

FROM base_image          # Base image (REQUIRED - BẮT BUỘC)
WORKDIR /app             # Set working directory (Đặt thư mục làm việc)
COPY source dest         # Copy files from host to image
RUN command              # Run command during build (Chạy lệnh khi build)
EXPOSE port              # Document port - doesn't open port (Không mở port)
ENV KEY=value            # Set environment variable (Đặt biến môi trường)
CMD ["executable"]       # Default command when run (Lệnh mặc định khi chạy)
```

#### 5.3 Important Instructions (Các instructions quan trọng)

| Instruction | Description | Example |
|-------------|-------------|---------|
| `FROM` | Base image (Image nển) | `FROM node:18-alpine` |
| `WORKDIR` | Set working directory (Thiết lập thư mục làm việc) | `WORKDIR /app` |
| `COPY` | Copy files from host (Chép file từ máy chủ) | `COPY . .` |
| `ADD` | Copy + extract archives (Chép + giải nén) | `ADD app.tar.gz /app` |
| `RUN` | Run command in build time (Chạy lệnh khi build) | `RUN npm install` |
| `CMD` | Default command in run time (Lệnh mặc định khi chạy) | `CMD ["node", "app.js"]` |
| `ENTRYPOINT` | Fixed command (Lệnh cố định) | `ENTRYPOINT ["python"]` |
| `EXPOSE` | Document port (Khai báo cổng) | `EXPOSE 3000` |
| `ENV` | Environment variable (Biến môi trường) | `ENV NODE_ENV=production` |
| `ARG` | Build-time variable (Biến khi build) | `ARG VERSION=1.0` |
| `VOLUME` | Mount point (Điểm gắn kết ổ đĩa) | `VOLUME /data` |
| `USER` | Set user (Thiết lập người dùng) | `USER node` |

#### 5.4 Ví dụ: Node.js Application

**Cấu trúc project:**

```
my-app/
├── Dockerfile
├── package.json
├── package-lock.json
└── src/
    └── app.js
```

**Dockerfile:**

```dockerfile
# 1. Base image
FROM node:18-alpine

# 2. Set working directory
WORKDIR /app

# 3. Copy package files first (cache optimization)
COPY package*.json ./

# 4. Install dependencies
RUN npm ci --only=production

# 5. Copy source code
COPY src/ ./src/

# 6. Expose port (documentation)
EXPOSE 3000

# 7. Set non-root user (security)
USER node

# 8. Default command
CMD ["node", "src/app.js"]
```

**Build và run:**

```bash
# Build image
docker build -t my-node-app .
docker build -t my-node-app:v1.0 .

# Run container
docker run -d -p 3000:3000 --name app my-node-app
```

#### 5.5 Ví dụ: Python Application

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

EXPOSE 5000

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

#### 5.6 Ví dụ: Static Website với NGINX

```dockerfile
FROM nginx:alpine

# Copy static files
COPY ./html /usr/share/nginx/html

# Copy custom config (optional)
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

# nginx runs as daemon by default
CMD ["nginx", "-g", "daemon off;"]
```

#### 5.7 Best Practices

```dockerfile
# ❌ BAD - Mỗi RUN tạo 1 layer
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get clean

# ✅ GOOD - Gộp lại 1 layer
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

```dockerfile
# ❌ BAD - Copy all rồi mới install
COPY . .
RUN npm install

# ✅ GOOD - Copy package.json trước để tận dụng cache
COPY package*.json ./
RUN npm install
COPY . .
```

```dockerfile
# ✅ GOOD - Sử dụng .dockerignore
# File: .dockerignore
node_modules
.git
*.log
.env
Dockerfile
.dockerignore
```

---

### 6. Docker Volumes - 2 hours

#### 6.1 The Problem: Data in Containers (Vấn đề: Data trong container)

- Container deleted → Data lost (Container bị xóa → Data mất)
- Need persistent data (Cần lưu data bền vững)

#### 6.2 Mount Types (Các loại mounts)

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCKER STORAGE                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. VOLUMES (Docker managed)                                 │
│     /var/lib/docker/volumes/my-vol/_data                    │
│                                                              │
│  2. BIND MOUNTS (Host path)                                  │
│     /home/user/data → /app/data                             │
│                                                              │
│  3. TMPFS (Memory only) (Chỉ RAM)                            │
│     RAM → /app/cache                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 6.3 Volumes

```bash
# Create volume (Tạo volume)
docker volume create my-data

# List volumes (Liệt kê volumes)
docker volume ls

# Inspect volume (Xem chi tiết volume)
docker volume inspect my-data

# Use volume (Sử dụng volume)
docker run -d \
    -v my-data:/var/lib/mysql \
    --name mysql \
    mysql

# Remove volume (Xóa volume)
docker volume rm my-data

# Remove unused volumes (Xóa volumes không dùng)
docker volume prune
```

#### 6.4 Bind Mounts

```bash
# Mount folder from host (Mount folder từ host)
docker run -d \
    -v $(pwd)/data:/app/data \
    --name app \
    my-app

# Windows PowerShell
docker run -d `
    -v ${PWD}/data:/app/data `
    --name app `
    my-app

# Read-only mount (Mount chỉ đọc)
docker run -d \
    -v $(pwd)/config:/app/config:ro \
    my-app
```

#### 6.5 Use Cases (Trường hợp sử dụng)

| Use case | Mount type | Example |
|----------|------------|---------|
| Database data | Volume | MySQL, PostgreSQL data (Dữ liệu DB) |
| Development | Bind mount | Live reload code (Tự động tải lại code) |
| Config files | Bind mount (ro) | nginx.conf (Cấu hình máy chủ) |
| Logs | Volume or Bind | Application logs (Nhật ký ứng dụng) |
| Secrets | tmpfs | Passwords, tokens (Mật khẩu, tokens) |

---

### 7. Docker Networks (Mạng Docker) - 2 hours

#### 7.1 Network Types (Các loại Network)

| Driver | Description | Use case |
|--------|-------------|----------|
| **bridge** | Default, isolated network (Mặc định, mạng cô lập) | Single host, dev (Máy đơn, phát triển) |
| **host** | Use host network directly (Dùng trực tiếp mạng host) | Performance (Hiệu suất cao) |
| **none** | No networking (Không kết nối mạng) | Security (Bảo mật tối đa) |
| **overlay** | Multi-host network (Mạng đa máy chủ) | Swarm, K8s (Hệ thống phân tán) |

#### 7.2 Bridge Network (Default)

```bash
# Create network (Tạo network)
docker network create my-network

# List networks (Liệt kê networks)
docker network ls

# Inspect network (Xem chi tiết network)
docker network inspect my-network

# Run container in network (Chạy container trong network)
docker run -d --name web --network my-network nginx
docker run -d --name api --network my-network my-api

# Containers can call each other by name (Containers có thể gọi nhau bằng tên)
# From web: curl http://api:3000

# Remove network (Xóa network)
docker network rm my-network
```

#### 7.3 Container Communication (Giao tiếp Container)

```bash
# Example: Web + API + Database (Ví dụ: Web + API + Database)

# 1. Create network (Tạo network)
docker network create app-network

# 2. Database
docker run -d \
    --name db \
    --network app-network \
    -e POSTGRES_PASSWORD=secret \
    postgres

# 3. API (connect to db)
docker run -d \
    --name api \
    --network app-network \
    -e DATABASE_URL=postgresql://postgres:secret@db:5432/app \
    my-api

# 4. Web (connect to api)
docker run -d \
    --name web \
    --network app-network \
    -p 80:80 \
    -e API_URL=http://api:3000 \
    my-web
```

---

### 8. Docker Hub - 1 hour

#### 8.1 Login (Đăng nhập)

```bash
docker login
# Enter username and password (Nhập username và password)
```

#### 8.2 Push Image (Push image)

```bash
# Tag image with username (Tag image với username)
docker tag my-app:v1.0 username/my-app:v1.0

# Push
docker push username/my-app:v1.0

# Push latest
docker tag my-app:v1.0 username/my-app:latest
docker push username/my-app:latest
```

#### 8.3 Pull Image (Pull image)

```bash
docker pull username/my-app:v1.0
```

---

### 9. Practice: Deploy Static Website (Thực hành: Deploy Website)

#### Project Structure (Cấu trúc dự án)

```
my-website/
├── Dockerfile
├── nginx.conf
└── html/
    ├── index.html
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

#### index.html

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Journey</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <h1>🚀 Welcome to DevOps Journey!</h1>
    <p>This website is running in a Docker container.</p>
    <p id="time"></p>
    <script src="js/app.js"></script>
</body>
</html>
```

#### Dockerfile

```dockerfile
FROM nginx:alpine

# Copy website files (Sao chép files website)
COPY html/ /usr/share/nginx/html/

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

#### Build and Run (Build và Chạy)

- Run the following commands to build and run the container (Chạy các lệnh sau để build và chạy container):

```bash
# Build
docker build -t my-website:v1.0 .

# Run (Chạy)
docker run -d -p 8080:80 --name website my-website:v1.0

# Access (Truy cập): http://localhost:8080
```

---

## 📝 Module Files (Các file trong Module)

| File | Description |
|------|-------------|
| [CHEATSHEET.md](./CHEATSHEET.md) | Quick reference (Tra cứu nhanh) |
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Exercises (Bài tập) |
| [PROJECT.md](./PROJECT.md) | Mini project (Dự án nhỏ) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Solutions (Đáp án) |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [1.4 Git](../1.4_Git_GitLab/) | **1.5 Docker** | [1.6 NGINX](../1.6_NGINX_Basic/) |

---

**Master Docker fundamentals! 🐳**

*Thành thạo Docker cơ bản!*

</div>
