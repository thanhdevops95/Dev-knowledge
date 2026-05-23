# 🐳 Docker — Images & Containers

---

## 📋 Metadata

- **Parent Lesson:** [../README.md](../README.md)
- **Level:** `[BEGINNER]`
- **Prerequisites:** [Lesson 01: Installation & Setup](../01-Installation-Setup/lesson.md)
- **Estimated Time:** 1 giờ
- **Last Updated:** 30/04/2026
- **Author:** Mr.Rom

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ có thể:

- [ ] Phân biệt rõ Image vs Container
- [ ] Pull images từ Docker Hub
- [ ] Chạy, list, stop, remove containers với Docker CLI
- [ ] Hiểu container lifecycle
- [ ] Xem container logs và exec vào container
- [ ] Dùng Docker Commands một cách tự tin

---

## 📚 Nội Dung

### 1. Docker Images là gì?

**Image** là **read-only template** chứa:
- Application code
- Runtime (Node.js, Python, Java,...)
- Libraries
- Environment variables
- Configuration files

**Ảnh:** Docker image giống như **class** trong OOP — template để tạo objects.

**Ví dụ:** `nginx:latest`, `python:3.11-slim`, `node:18-alpine`

---

### 2. Docker Containers là gì?

**Container** là **running instance** của một image.

Khi bạn `docker run nginx`, Docker:
1. Tìm image `nginx` local (nếu không có → pull từ Docker Hub)
2. Tạo container từ image đó
3. Start container với process chính (ví dụ: `nginx -g 'daemon off;'`)

**Container có:**
- **Writable layer** (thay đổi trong runtime)
- **Isolated filesystem** (view từ `docker exec`)
- **Own network stack** (ports, IP)
- **Process space** (processes chạy bên trong)

**Ảnh:** Container giống như **object** trong OOP — instance của class (image).

---

### 3. Docker Registry

**Registry** là nơi lưu trữ và phân phối Docker images.

**Phổ biến:**
- **Docker Hub** (default): `docker.io` — public registry
- **GitHub Container Registry** (GHCR)
- **Google Container Registry** (GCR)
- **AWS ECR**
- **Private registry** (self-hosted với `docker registry`)

**Image naming:**
```
[registry/][username/]image[:tag|@digest]
```

Ví dụ:
- `nginx:latest` — từ Docker Hub, official image, tag `latest`
- `myusername/myapp:v1.0` — từ Docker Hub, user namespace
- `gcr.io/my-project/api:prod` — từ Google Container Registry

---

### 4. Essential Docker Commands

#### Images Commands

```bash
# List all local images
docker images

# Pull an image from registry
docker pull nginx:latest

# Remove an image
docker rmi nginx:latest

# Build image from Dockerfile (bài sau sẽ học)
docker build -t myapp:v1.0 .
```

#### Container Commands

```bash
# Run container (foreground)
docker run nginx:latest

# Run container (background)
docker run -d nginx:latest

# Run container với port mapping
docker run -d -p 8080:80 nginx:latest

# Run container với volume mount
docker run -d -v /host/path:/container/path nginx

# List running containers
docker ps

# List ALL containers (including stopped)
docker ps -a

# Stop container
docker stop <container_id_or_name>

# Start stopped container
docker start <container_id_or_name>

# Remove container
docker rm <container_id_or_name>

# View container logs
docker logs <container_id_or_name>
docker logs -f <container_id_or_name>  # follow logs (real-time)

# Exec into container shell
docker exec -it <container_id_or_name> /bin/bash
docker exec -it <container_id_or_name> sh  # Alpine images

# Inspect container details (JSON)
docker inspect <container_id_or_name>

# Stats: real-time resource usage
docker stats

# Stop ALL running containers
docker stop $(docker ps -q)

# Remove ALL stopped containers
docker rm $(docker ps -a -q)
```

---

### 5. Container Lifecycle

```
┌─────────────┐
│   Created   │ ← docker create (not started yet)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Running   │ ← docker start / docker run
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Paused     │ ← docker pause (freeze processes)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Stopped    │ ← docker stop (graceful shutdown)
└─────────────┘
```

**Note:** Container là **ephemeral** — data bên trong mất khi container bị remove (trừ khi dùng volumes).

---

## 💻 Docker Commands Quick Reference

### Images

```bash
docker images                    # List all local images
docker pull <image>:<tag>       # Pull image from registry
docker rmi <image>:<tag>        # Remove image
docker build -t myapp:v1.0 .    # Build image from Dockerfile (bài sau)
docker tag <src> <dest>         # Tag image
docker push <image>:<tag>       # Push to registry
```

### Containers

```bash
docker run <image>                      # Create & start (foreground)
docker run -d <image>                   # Run detached (background)
docker run -p 8080:80 <image>           # Port mapping (host:container)
docker run -v /host/path:/container/path <image>   # Mount volume
docker run --name my-container <image>  # Assign name

docker ps                               # List running containers
docker ps -a                            # List all containers (running + stopped)
docker stop <container>                 # Stop (graceful, SIGTERM)
docker start <container>                # Start stopped container
docker restart <container>
docker rm <container>                   # Remove (must be stopped)
docker rm -f <container>                # Force remove (even if running)

docker logs <container>                 # View logs
docker logs -f <container>              # Follow logs (real-time)
docker exec -it <container> /bin/bash   # Exec shell into container
docker exec -it <container> sh          # For Alpine images
docker inspect <container>              # JSON metadata
docker stats                            # Real-time CPU/RAM for all containers

# Bulk operations
docker stop $(docker ps -q)             # Stop all running
docker rm $(docker ps -a -q)            # Remove all stopped
```

---

### 7. Practical Examples

#### Example 1: Pull and Run Nginx

```bash
# Pull Nginx image
docker pull nginx:latest

# Run Nginx với port mapping
docker run -d --name my-nginx -p 8080:80 nginx:latest

# Verify it's running
docker ps
# Output:
# CONTAINER ID   IMAGE    COMMAND                  CREATED        STATUS        PORTS
# abc123def456   nginx    "/docker-entrypoint.…"   5 seconds ago  Up 4 seconds 0.0.0.0:8080->80/tcp

# Test: Mở browser -> http://localhost:8080
# Bạn thấy trang "Welcome to nginx!"

# View logs
docker logs my-nginx

# Exec vào container để xem filesystem
docker exec -it my-nginx /bin/bash
# Bạn đang ở bên trong container!
# Thử: `ls -la /usr/share/nginx/html`

# Stop container
docker stop my-nginx

# Remove container
docker rm my-nginx

# (Optional) Remove image
docker rmi nginx:latest
```

#### Example 2: Run PostgreSQL Database

```bash
# Run PostgreSQL với environment variables và volume
docker run -d \
  --name my-postgres \
  -e POSTGRES_PASSWORD=secret123 \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15-alpine

# Check logs (đợi DB sẵn sàng)
docker logs -f my-postgres

# Connect from host (using psql)
# psql -h localhost -U postgres -d mydb

# Stop & remove
docker stop my-postgres
docker rm my-postgres
```

**Note:** Volume `postgres_data` là named volume — Docker quản lý, dù container bị xóa thì data vẫn còn.

---

### 7. Common Issues & Troubleshooting

#### Issue 1: "Error response from daemon: port is already allocated"

**Lỗi:** Port bạn muốn map (ví dụ 8080) đã được sử dụng bởi process khác

**Kiểm tra:**
```bash
# macOS/Linux
lsof -i :8080

# Windows (PowerShell)
netstat -ano | findstr :8080
```

**Giải pháp:**
- Dùng port khác: `-p 8081:80`
- Stop process đang dùng port 8080
- Stop container cũ đang dùng port đó: `docker ps` → `docker stop <container>`

---

#### Issue 2: Container chạy rồi tắt ngay

**Nguyên nhân:** Container process kết thúc (ví dụ bạn chạy `docker run ubuntu bash -c "echo hello"` — nó in hello rồi exit)

**Cách debug:**
```bash
# Xem logs
docker logs <container_id>

# Chạy lại với interactive mode
docker run -it ubuntu /bin/bash
```

---

#### Issue 3: "No space left on device"

**Nguyên nhân:** Docker disk đầy (images, containers, volumes chiếm quá nhiều space)

**Giải pháp:**
```bash
# Xem disk usage
docker system df

# Clean up unused resources
docker system prune -a  # XÓA TẤT CẢ images, containers, networks không dùng

# Chỉ xem trước (không xóa)
docker system prune --dry-run
```

---

## 💻 Hands-On Exercises

### Exercise 1: Pull and Explore Images

**Tasks:**
1. Pull image `alpine:latest` (image nhẹ, ~5MB)
   ```bash
   docker pull alpine:latest
   ```
2. List local images với `docker images`. Ghi ra:
   - Repository: ________ Tag: ________ Size: ________
3. Pull `python:3.11-slim` và `node:18-alpine`
4. Run `docker images` lần nữa. Có bao nhiêu images? _____

---

### Exercise 2: Run Containers

**Tasks:**
1. Chạy container `alpine` với command `echo "Hello Docker"`:
   ```bash
   docker run alpine echo "Hello Docker"
   ```
2. Chạy container `alpine` với interactive shell:
   ```bash
   docker run -it alpine /bin/sh
   ```
   Bên trong container:
   - Chạy `ls -la /`
   - Chạy `uname -a`
   - Thoát: `exit`
3. Chạy container `nginx` trong background với port mapping:
   ```bash
   docker run -d --name web -p 8080:80 nginx:latest
   ```
4. Verify: `docker ps` — bạn thấy container `web` không? _____

---

### Exercise 3: Container Lifecycle

**Tasks:**
1. Chạy container `redis:alpine` với tên `my-redis`:
   ```bash
   docker run -d --name my-redis redis:alpine
   ```
2. Stop container: `docker stop my-redis`
3. Start lại: `docker start my-redis`
4. Xem logs: `docker logs my-redis`
5. Exec vào container:
   ```bash
   docker exec -it my-redis redis-cli
   ```
   Bên trong Redis CLI:
   - `SET test hello`
   - `GET test`
   - `exit`
6. Remove container: `docker rm my-redis`

---

### Exercise 4: Docker Stats & Inspect

**Tasks:**
1. Chạy 2 containers: `nginx` và `postgres` (như ví dụ ở trên)
2. Xem real-time stats của tất cả containers:
   ```bash
   docker stats
   ```
   Ghi lại:
   - Container nào dùng CPU nhiều nhất? ____
   - Container nào dùng Memory nhiều nhất? ____
3. Inspect container `nginx`:
   ```bash
   docker inspect <nginx_container_id>
   ```
   Tìm và ghi ra:
   - IP address: ____
   - Port mappings: ____
   - Mounts (nếu có): ____

---

## ✅ Kiểm Tra & Đánh Giá

### Self-Check Questions

1. **Sự khác biệt chính giữa Image và Container?**
   ```
   [Trả lời của bạn]
   ```

2. **Command nào để chạy container trong background?**
   ```
   [Trả lời]
   ```

3. **Làm thế nào để xem logs của container đã stop?**
   ```
   [Trả lời]
   ```

4. **`docker ps` và `docker ps -a` khác nhau thế nào?**
   ```
   [Trả lời]
   ```

---

### Checklist Tự Đánh Giá

- [ ] Tôi phân biệt được Image vs Container
- [ ] Tôi biết cách pull images từ Docker Hub
- [ ] Tôi biết cách run container (foreground & background)
- [ ] Tôi biết cách list, stop, start, remove containers
- [ ] Tôi biết cách xem container logs
- [ ] Tôi biết cách exec vào container shell
- [ ] Tôi hiểu container lifecycle
- [ ] Tôi biết cách troubleshoot basic issues (port already allocated, container exit early)

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
