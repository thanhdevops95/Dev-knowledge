# Docker Errors & Troubleshooting

> Các lỗi Docker thường gặp và cách xử lý

## 📋 Mục lục

- [Container Issues](#container-issues)
- [Image Issues](#image-issues)
- [Network Issues](#network-issues)
- [Volume Issues](#volume-issues)
- [Permission Issues](#permission-issues)
- [Resource Issues](#resource-issues)

## Container Issues

### Error: "Container already exists"

**Lỗi:**
```
Error response from daemon: Conflict. The container name "/mycontainer" is already in use
```

**Nguyên nhân:** Container với tên này đã tồn tại (có thể đã stopped)

**Giải pháp:**
```bash
# Xem tất cả containers
docker ps -a

# Xóa container cũ
docker rm mycontainer

# Hoặc force remove nếu đang chạy
docker rm -f mycontainer

# Hoặc dùng tên khác
docker run --name mycontainer2 nginx
```

### Error: "Port already allocated"

**Lỗi:**
```
Error starting userland proxy: listen tcp 0.0.0.0:8080: bind: address already in use
```

**Nguyên nhân:** Port đã được sử dụng bởi process khác

**Giải pháp:**
```bash
# Tìm process đang dùng port
lsof -i :8080
# hoặc
netstat -tulpn | grep 8080

# Kill process đó
kill -9 <PID>

# Hoặc dùng port khác
docker run -p 8081:80 nginx

# Hoặc stop container đang dùng port
docker ps | grep 8080
docker stop <container_id>
```

### Error: "Container exits immediately"

**Lỗi:** Container start rồi exit ngay lập tức

**Nguyên nhân:** 
- Không có foreground process
- Lỗi trong application
- Missing dependencies

**Giải pháp:**
```bash
# Xem logs để tìm lỗi
docker logs container_name

# Xem exit code
docker ps -a
# Exit code 0: normal exit
# Exit code 1: application error
# Exit code 137: killed (OOM)
# Exit code 139: segmentation fault

# Run interactive để debug
docker run -it image_name /bin/bash

# Check Dockerfile CMD/ENTRYPOINT
docker inspect image_name | grep -A 5 "Cmd\|Entrypoint"
```

## Image Issues

### Error: "No such image"

**Lỗi:**
```
Error: No such image: myimage:latest
```

**Nguyên nhân:** Image không tồn tại locally

**Giải pháp:**
```bash
# Pull image từ registry
docker pull myimage:latest

# Hoặc build image
docker build -t myimage:latest .

# List images để kiểm tra
docker images
```

### Error: "Failed to build image"

**Lỗi:**
```
ERROR [internal] load metadata for docker.io/library/node:16
```

**Nguyên nhân:** 
- Network issues
- Base image không tồn tại
- Syntax error trong Dockerfile

**Giải pháp:**
```bash
# Check network connectivity
ping docker.io

# Verify base image exists
docker pull node:16

# Build với verbose output
docker build --progress=plain -t myimage .

# Build without cache
docker build --no-cache -t myimage .

# Check Dockerfile syntax
cat Dockerfile
```

## Network Issues

### Error: "Cannot connect to Docker daemon"

**Lỗi:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Nguyên nhân:** Docker daemon không chạy hoặc permission issues

**Giải pháp:**
```bash
# Start Docker daemon (Linux)
sudo systemctl start docker

# Check Docker status
sudo systemctl status docker

# Add user to docker group (Linux)
sudo usermod -aG docker $USER
# Logout and login again

# macOS: Start Docker Desktop

# Verify
docker version
```

### Error: "Network not found"

**Lỗi:**
```
Error response from daemon: network mynetwork not found
```

**Nguyên nhân:** Network không tồn tại

**Giải pháp:**
```bash
# List networks
docker network ls

# Create network
docker network create mynetwork

# Or use existing network
docker network ls
docker run --network existing_network myimage
```

### Error: "Cannot connect between containers"

**Nguyên nhân:** Containers không cùng network

**Giải pháp:**
```bash
# Create custom network
docker network create myapp-network

# Run containers on same network
docker run -d --name db --network myapp-network postgres
docker run -d --name web --network myapp-network nginx

# Connect existing container to network
docker network connect myapp-network existing_container

# Test connectivity
docker exec web ping db
```

## Volume Issues

### Error: "Volume not found"

**Lỗi:**
```
Error response from daemon: volume myvolume not found
```

**Giải pháp:**
```bash
# List volumes
docker volume ls

# Create volume
docker volume create myvolume

# Use volume
docker run -v myvolume:/data nginx
```

### Error: "Permission denied" in volume

**Lỗi:**
```
Permission denied: '/data/file.txt'
```

**Nguyên nhân:** User trong container không có quyền truy cập

**Giải pháp:**
```bash
# Run as specific user
docker run -u $(id -u):$(id -g) -v /host:/container myimage

# Change ownership on host
sudo chown -R $USER:$USER /host/path

# In Dockerfile, create user with matching UID
RUN useradd -u 1000 appuser
USER appuser
```

## Permission Issues

### Error: "Permission denied" running Docker

**Lỗi:**
```
Got permission denied while trying to connect to the Docker daemon socket
```

**Giải pháp:**
```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER

# Logout and login again
# Or run new shell
newgrp docker

# Verify
docker ps

# Temporary fix (not recommended)
sudo docker ps
```

## Resource Issues

### Error: "Out of memory"

**Lỗi:** Container bị kill với exit code 137

**Giải pháp:**
```bash
# Check container memory usage
docker stats

# Run with memory limit
docker run -m 512m myimage

# Increase Docker Desktop memory (macOS/Windows)
# Docker Desktop → Preferences → Resources → Memory

# Check system memory
free -h
```

### Error: "No space left on device"

**Lỗi:**
```
Error: No space left on device
```

**Giải pháp:**
```bash
# Check disk usage
df -h
docker system df

# Clean up
docker system prune -a          # Remove all unused data
docker image prune -a           # Remove unused images
docker container prune          # Remove stopped containers
docker volume prune             # Remove unused volumes

# Remove specific items
docker rm $(docker ps -a -q)    # All containers
docker rmi $(docker images -q)  # All images
```

## Docker Compose Issues

### Error: "Service 'xxx' failed to build"

**Giải pháp:**
```bash
# Build with verbose output
docker-compose build --no-cache --progress=plain

# Check docker-compose.yml syntax
docker-compose config

# Build specific service
docker-compose build service_name
```

### Error: "Network has active endpoints"

**Lỗi:**
```
Error response from daemon: network xxx has active endpoints
```

**Giải pháp:**
```bash
# Stop all containers
docker-compose down

# Force remove
docker-compose down -v

# Remove network manually
docker network rm network_name
```

## Best Practices để tránh lỗi

### 1. Always check logs
```bash
docker logs container_name
docker logs -f container_name  # Follow logs
docker-compose logs -f
```

### 2. Use health checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
```

### 3. Clean up regularly
```bash
# Weekly cleanup
docker system prune -a --volumes

# Remove old images
docker image prune -a --filter "until=24h"
```

### 4. Monitor resources
```bash
docker stats
docker system df
```

### 5. Use .dockerignore
```
node_modules
.git
*.log
.env
```

---

