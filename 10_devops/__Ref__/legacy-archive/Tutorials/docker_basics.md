# Hướng dẫn Docker Cơ bản

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Docker là công cụ đóng gói ứng dụng cùng với môi trường chạy vào một "container", giúp ứng dụng chạy nhất quán trên mọi máy.

### Tại sao cần Docker?

| Vấn đề | Docker giải quyết |
|--------|-------------------|
| "Máy tôi chạy được mà!" | Container chạy giống nhau mọi nơi |
| Cài đặt môi trường phức tạp | Dockerfile định nghĩa môi trường |
| Xung đột phiên bản | Mỗi container có môi trường riêng |
| Deploy khó khăn | Build image → Push → Pull → Run |

---

## 🔧**CÀI ĐẶT DOCKER**

### Windows

1. Tải [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Cài đặt và khởi động
3. Kiểm tra:
```powershell
docker --version
docker run hello-world
```

### macOS

```bash
brew install --cask docker
```

### Linux (Ubuntu)

```bash
# Cài đặt
sudo apt update
sudo apt install docker.io docker-compose

# Thêm user vào group docker (không cần sudo)
sudo usermod -aG docker $USER

# Khởi động
sudo systemctl start docker
sudo systemctl enable docker
```

---

## 📦**KHÁI NIỆM CƠ BẢN**

| Khái niệm | Giải thích |
|-----------|------------|
| **Image** | Bản thiết kế (template) của container |
| **Container** | Instance đang chạy của image |
| **Dockerfile** | File định nghĩa cách build image |
| **Registry** | Nơi lưu trữ images (Docker Hub) |
| **Volume** | Lưu trữ dữ liệu persistent |
| **Network** | Kết nối giữa các containers |

---

## 🔨**LỆNH DOCKER CƠ BẢN**

### Images

```bash
# Tải image từ Docker Hub
docker pull python:3.11

# Liệt kê images
docker images

# Xóa image
docker rmi python:3.11

# Xóa tất cả images không dùng
docker image prune -a
```

### Containers

```bash
# Chạy container
docker run python:3.11

# Chạy container với interactive terminal
docker run -it python:3.11 bash

# Chạy container nền (detached)
docker run -d --name my-container python:3.11

# Chạy với port mapping
docker run -d -p 8080:80 nginx

# Chạy với volume
docker run -d -v /host/path:/container/path nginx

# Liệt kê containers đang chạy
docker ps

# Liệt kê tất cả containers
docker ps -a

# Dừng container
docker stop my-container

# Khởi động lại container
docker start my-container

# Xóa container
docker rm my-container

# Xóa tất cả containers dừng
docker container prune
```

### Logs & Debug

```bash
# Xem logs
docker logs my-container

# Xem logs realtime
docker logs -f my-container

# Chạy lệnh trong container đang chạy
docker exec -it my-container bash

# Xem thông tin container
docker inspect my-container
```

---

## 📄**DOCKERFILE**

### Cấu trúc cơ bản

```dockerfile
# Base image
FROM python:3.11-slim

# Thông tin maintainer (optional)
LABEL maintainer="your@email.com"

# Set working directory
WORKDIR /app

# Copy requirements first (tận dụng cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Environment variables
ENV PYTHONUNBUFFERED=1

# Command to run
CMD ["python", "main.py"]
```

### Dockerfile cho Python Flask

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
```

### Dockerfile cho Node.js

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "index.js"]
```

### Dockerfile Instructions

| Instruction | Mô tả |
|-------------|-------|
| `FROM` | Base image |
| `WORKDIR` | Set working directory |
| `COPY` | Copy files từ host vào image |
| `ADD` | Giống COPY + hỗ trợ URL, extract tar |
| `RUN` | Chạy lệnh khi build |
| `CMD` | Lệnh mặc định khi container chạy |
| `ENTRYPOINT` | Lệnh chính (không bị override) |
| `ENV` | Set environment variables |
| `EXPOSE` | Khai báo port |
| `VOLUME` | Tạo mount point |
| `ARG` | Build-time variables |

---

## 🏗️**BUILD & RUN**

### Build image

```bash
# Build với tag
docker build -t my-app:1.0 .

# Build với Dockerfile ở vị trí khác
docker build -t my-app:1.0 -f Dockerfile.prod .

# Build không cache
docker build --no-cache -t my-app:1.0 .
```

### Run container

```bash
# Chạy cơ bản
docker run my-app:1.0

# Chạy với options đầy đủ
docker run -d \
  --name my-app \
  -p 8080:8000 \
  -v $(pwd)/data:/app/data \
  -e DATABASE_URL=postgres://... \
  my-app:1.0
```

---

## 📦**DOCKER COMPOSE**

File `docker-compose.yml` để quản lý multi-container.

### docker-compose.yml cơ bản

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=1
    depends_on:
      - db

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password

volumes:
  postgres_data:
```

### Lệnh Docker Compose

```bash
# Khởi động services
docker-compose up

# Khởi động nền
docker-compose up -d

# Build lại và khởi động
docker-compose up --build

# Dừng services
docker-compose down

# Dừng và xóa volumes
docker-compose down -v

# Xem logs
docker-compose logs -f

# Chạy lệnh trong service
docker-compose exec web bash

# Scale service
docker-compose up -d --scale web=3
```

---

## 🔒**VOLUMES**

Volumes để lưu trữ dữ liệu persist (không mất khi container xóa).

### Tạo và sử dụng volume

```bash
# Tạo volume
docker volume create my-volume

# Liệt kê volumes
docker volume ls

# Chạy container với volume
docker run -d -v my-volume:/app/data my-app

# Xóa volume
docker volume rm my-volume
```

### Bind mount vs Volume

```bash
# Bind mount (mount folder từ host)
docker run -v /host/path:/container/path my-app

# Named volume
docker run -v my-volume:/container/path my-app
```

---

## 🌐**NETWORKING**

### Tạo network

```bash
# Tạo network
docker network create my-network

# Chạy container trong network
docker run -d --network my-network --name web my-web-app
docker run -d --network my-network --name db postgres

# Container "web" có thể kết nối "db" bằng hostname "db"
```

### Port mapping

```bash
# Map port 8080 host → 80 container
docker run -p 8080:80 nginx

# Map port random
docker run -P nginx

# Map chỉ localhost
docker run -p 127.0.0.1:8080:80 nginx
```

---

## 🏷️**DOCKER HUB**

### Push image lên Docker Hub

```bash
# Login
docker login

# Tag image
docker tag my-app:1.0 username/my-app:1.0

# Push
docker push username/my-app:1.0
```

### Pull image

```bash
docker pull username/my-app:1.0
```

---

## 🧹**DỌN DẸP**

```bash
# Xóa containers dừng
docker container prune

# Xóa images không dùng
docker image prune

# Xóa volumes không dùng
docker volume prune

# Xóa tất cả không dùng (containers, images, networks, cache)
docker system prune -a

# Xem dung lượng Docker đang dùng
docker system df
```

---

## 📋**.DOCKERIGNORE**

File `.dockerignore` để bỏ qua files khi COPY:

```dockerignore
# Python
__pycache__
*.pyc
venv
.env

# Node
node_modules
npm-debug.log

# Git
.git
.gitignore

# IDE
.vscode
.idea

# Docker
Dockerfile*
docker-compose*
.dockerignore

# Docs
*.md
docs/

# Tests
tests/
```

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
