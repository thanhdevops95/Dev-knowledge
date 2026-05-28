# 🔬 Labs: Docker Fundamentals

> **Hands-on Labs for Docker Basics**
>
> *Bài thực hành Docker cơ bản.*

---

## 🔬 Lab 1: Docker Basics

```bash
# Check Docker
docker --version
docker info

# Run first container
docker run hello-world

# Run interactive container
docker run -it ubuntu bash

# Inside container
apt update && apt install -y curl
exit
```

---

## 🔬 Lab 2: Container Management

```bash
# Run nginx in background
docker run -d --name web nginx

# List containers
docker ps
docker ps -a

# Container logs
docker logs web
docker logs -f web

# Execute in container
docker exec -it web bash

# Stop and remove
docker stop web
docker rm web

# Remove all stopped
docker container prune
```

---

## 🔬 Lab 3: Images

```bash
# List images
docker images

# Pull image
docker pull nginx:alpine

# Search images
docker search nginx

# Image history
docker history nginx

# Remove image
docker rmi nginx:alpine

# Remove unused
docker image prune
```

---

## 🔬 Lab 4: Dockerfile

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

```bash
# Build image
docker build -t my-app:v1 .

# Run container
docker run -d -p 3000:3000 my-app:v1
```

---

## 🔬 Lab 5: Volumes

```bash
# Named volume
docker volume create mydata
docker run -d -v mydata:/data nginx

# Bind mount
docker run -d -v $(pwd)/html:/usr/share/nginx/html nginx

# List volumes
docker volume ls

# Inspect volume
docker volume inspect mydata
```

---

## 🔬 Lab 6: Networking

```bash
# List networks
docker network ls

# Create network
docker network create mynet

# Run with network
docker run -d --name web --network mynet nginx
docker run -d --name db --network mynet postgres

# Containers can communicate by name
docker exec web curl http://db:5432

# Inspect network
docker network inspect mynet
```

---

## 🔬 Lab 7: Multi-stage Build

```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
```

```bash
docker build -t my-app:optimized .
```

---

## 🔬 Lab 8: Docker Hub

```bash
# Login
docker login

# Tag image
docker tag my-app:v1 username/my-app:v1

# Push
docker push username/my-app:v1

# Pull
docker pull username/my-app:v1
```

---

## ✅ Checklist

- [ ] Lab 1: Docker Basics
- [ ] Lab 2: Container Management
- [ ] Lab 3: Images
- [ ] Lab 4: Dockerfile
- [ ] Lab 5: Volumes
- [ ] Lab 6: Networking
- [ ] Lab 7: Multi-stage
- [ ] Lab 8: Docker Hub

---

## ✅ General Verification (Kiểm chứng tổng quát)

Verify Docker is working and you've completed labs:

*(Xác nhận Docker hoạt động và bạn đã hoàn thành labs:)*

```bash
# Check Docker is running (Kiểm tra Docker đang chạy)
docker info | head -20

# List all containers (Liệt kê tất cả containers)
docker ps -a

# List images (Liệt kê images)
docker images

# List volumes and networks (Liệt kê volumes và networks)
docker volume ls
docker network ls
```

---

## 🔧 General Troubleshooting (Xử lý sự cố chung)

| Issue | Solution |
|-------|----------|
| `Cannot connect to the Docker daemon` | Start Docker Desktop or `sudo systemctl start docker` *(Khởi động Docker)* |
| `permission denied` | Add user to docker group: `sudo usermod -aG docker $USER` *(Thêm user vào docker group)* |
| `port is already allocated` | Stop conflicting container or use different port *(Dừng container hoặc dùng port khác)* |
| `no space left on device` | Run `docker system prune -a` *(Dọn dẹp Docker)* |
| `image not found` | Check image name/tag, try `docker pull` first *(Kiểm tra tên image)* |
| `COPY failed: file not found` | Check file path relative to Dockerfile *(Kiểm tra đường dẫn file)* |

---

## 🧹 General Cleanup (Dọn dẹp tổng quát)

```bash
# Stop all containers (Dừng tất cả containers)
docker stop $(docker ps -q) 2>/dev/null

# Remove all containers (Xóa tất cả containers)
docker rm $(docker ps -aq) 2>/dev/null

# Remove lab images (Xóa images lab)
docker rmi my-app:v1 my-app:optimized 2>/dev/null

# Remove volumes and networks (Xóa volumes và networks)
docker volume rm mydata 2>/dev/null
docker network rm mynet 2>/dev/null

# Full cleanup (use with caution!) (Dọn dẹp hoàn toàn - cẩn thận!)
# docker system prune -a --volumes
```

> ⚠️ **Warning:** `docker system prune -a` removes ALL unused data!
>
> *Cảnh báo: Lệnh này xóa TẤT CẢ dữ liệu không sử dụng!*

---

**[← Back to README](./README.md)**

