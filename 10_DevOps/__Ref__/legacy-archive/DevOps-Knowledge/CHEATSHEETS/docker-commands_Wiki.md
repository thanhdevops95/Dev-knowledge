# Docker Commands Cheatsheet (Quick Reference -- Tra cứu Nhanh)

> Commonly used Docker commands for quick reference -- Các lệnh Docker thường dùng để tra cứu nhanh

## 📋 Table of Contents -- Mục lục

- [Images](#images) -- Images
- [Containers](#containers) -- Containers
- [Docker Compose](#docker-compose) -- Docker Compose
- [Networks](#networks) -- Networks
- [Volumes](#volumes) -- Volumes
- [System](#system) -- System
- [Registry](#registry) -- Registry
- [Dockerfile Best Practices](#dockerfile-best-practices) -- Dockerfile Best Practices
- [Common Patterns](#common-patterns) -- Patterns Thường dùng

## <a id="images"></a> Images

```bash
# List images -- Liệt kê images
docker images                    # List all images -- Liệt kê tất cả images
docker images -a                 # Include intermediate images -- Bao gồm intermediate images
docker image ls                  # Alternative syntax -- Cú pháp thay thế

# Pull images -- Pull images
docker pull nginx                # Pull latest -- Pull phiên bản mới nhất
docker pull nginx:1.21           # Pull specific version -- Pull phiên bản cụ thể
docker pull nginx:alpine         # Pull specific tag -- Pull tag cụ thể

# Build images -- Build images
docker build -t myapp:1.0 .                    # Build from Dockerfile -- Build từ Dockerfile
docker build -t myapp:1.0 -f Dockerfile.prod . # Use specific Dockerfile -- Dùng Dockerfile cụ thể
docker build --no-cache -t myapp:1.0 .         # Build without cache -- Build không dùng cache

# Tag images -- Tag images
docker tag myapp:1.0 myapp:latest              # Create tag -- Tạo tag
docker tag myapp:1.0 myregistry.com/myapp:1.0  # Tag for registry -- Tag cho registry

# Remove images -- Xóa images
docker rmi image_name            # Remove image -- Xóa image
docker rmi -f image_name         # Force remove -- Xóa cưỡng chế
docker image prune               # Remove dangling images -- Xóa dangling images
docker image prune -a            # Remove all unused images -- Xóa tất cả images không dùng

# Inspect -- Kiểm tra
docker inspect image_name        # Detailed image info -- Thông tin chi tiết image
docker history image_name        # Image layers history -- Lịch sử các layers
```

## <a id="containers"></a> Containers

```bash
# Run containers -- Chạy containers
docker run nginx                              # Run container -- Chạy container
docker run -d nginx                           # Run in background (detached) -- Chạy nền
docker run -d -p 8080:80 nginx               # Map port -- Map cổng
docker run -d -p 8080:80 --name web nginx    # With custom name -- Với tên tùy chỉnh
docker run -d -e ENV_VAR=value nginx         # Set environment variable -- Đặt biến môi trường
docker run -d -v /host:/container nginx      # Mount volume -- Gắn volume
docker run -it ubuntu bash                   # Interactive with terminal -- Tương tác với terminal
docker run --rm nginx                        # Remove after stop -- Xóa sau khi dừng
docker run -d --restart=always nginx         # Auto-restart -- Tự động khởi động lại

# List containers -- Liệt kê containers
docker ps                        # Running containers -- Containers đang chạy
docker ps -a                     # All containers -- Tất cả containers
docker ps -q                     # Only container IDs -- Chỉ IDs
docker ps -a --filter "status=exited"  # Filter by status -- Lọc theo trạng thái

# Container lifecycle -- Vòng đời container
docker start container_name      # Start stopped container -- Khởi động container đã dừng
docker stop container_name       # Stop running container -- Dừng container đang chạy
docker restart container_name    # Restart container -- Khởi động lại container
docker pause container_name      # Pause container -- Tạm dừng container
docker unpause container_name    # Unpause container -- Tiếp tục container
docker kill container_name       # Force stop -- Dừng cưỡng chế

# Remove containers -- Xóa containers
docker rm container_name         # Remove stopped container -- Xóa container đã dừng
docker rm -f container_name      # Force remove running container -- Xóa cưỡng chế container đang chạy
docker container prune           # Remove all stopped containers -- Xóa tất cả containers đã dừng

# Execute commands -- Thực thi lệnh
docker exec container_name ls    # Run command in container -- Chạy lệnh trong container
docker exec -it container_name bash  # Interactive shell -- Shell tương tác
docker exec -u root container_name bash  # As root user -- Với quyền root

# Logs
docker logs container_name       # View logs -- Xem logs
docker logs -f container_name    # Follow logs -- Theo dõi logs
docker logs --tail 100 container_name  # Last 100 lines -- 100 dòng cuối
docker logs --since 10m container_name # Last 10 minutes -- 10 phút gần nhất

# Copy files -- Sao chép files
docker cp container_name:/path/file /host/path  # From container -- Từ container
docker cp /host/path container_name:/path       # To container -- Đến container

# Stats & Info -- Thống kê & Thông tin
docker stats                     # Resource usage (all) -- Sử dụng tài nguyên (tất cả)
docker stats container_name      # Specific container -- Container cụ thể
docker top container_name        # Running processes -- Tiến trình đang chạy
docker inspect container_name    # Detailed info -- Thông tin chi tiết
docker port container_name       # Port mappings -- Ánh xạ cổng
```

## <a id="docker-compose"></a> Docker Compose

```bash
# Start services -- Khởi động services
docker-compose up                # Start in foreground -- Khởi động ở foreground
docker-compose up -d             # Start in background -- Khởi động ở background
docker-compose up --build        # Rebuild and start -- Rebuild và khởi động
docker-compose up -d service_name  # Start specific service -- Khởi động service cụ thể

# Stop services -- Dừng services
docker-compose down              # Stop and remove containers -- Dừng và xóa containers
docker-compose down -v           # Also remove volumes -- Cũng xóa volumes
docker-compose stop              # Stop without removing -- Dừng không xóa
docker-compose stop service_name # Stop specific service -- Dừng service cụ thể

# View status -- Xem trạng thái
docker-compose ps                # List containers -- Liệt kê containers
docker-compose logs              # View logs -- Xem logs
docker-compose logs -f           # Follow logs -- Theo dõi logs
docker-compose logs service_name # Logs for specific service -- Logs cho service cụ thể

# Execute commands -- Thực thi lệnh
docker-compose exec service_name bash  # Shell into service -- Shell vào service
docker-compose run service_name command  # Run one-off command -- Chạy lệnh một lần

# Build
docker-compose build             # Build all services -- Build tất cả services
docker-compose build service_name  # Build specific service -- Build service cụ thể
docker-compose build --no-cache  # Build without cache -- Build không dùng cache

# Scale -- Mở rộng
docker-compose up -d --scale web=3  # Scale service to 3 instances -- Mở rộng service lên 3 instances

# Config -- Cấu hình
docker-compose config            # Validate and view config -- Kiểm tra và xem cấu hình
docker-compose config --services # List services -- Liệt kê services
```

## <a id="networks"></a> Networks

```bash
# List networks -- Liệt kê networks
docker network ls                # List all networks -- Liệt kê tất cả networks

# Create network -- Tạo network
docker network create mynetwork  # Create bridge network -- Tạo bridge network
docker network create --driver bridge mynetwork
docker network create --subnet=172.18.0.0/16 mynetwork

# Connect/Disconnect -- Kết nối/Ngắt kết nối
docker network connect mynetwork container_name    # Connect -- Kết nối
docker network disconnect mynetwork container_name # Disconnect -- Ngắt kết nối

# Inspect -- Kiểm tra
docker network inspect mynetwork # Network details -- Chi tiết network

# Remove -- Xóa
docker network rm mynetwork      # Remove network -- Xóa network
docker network prune             # Remove unused networks -- Xóa networks không dùng
```

## <a id="volumes"></a> Volumes

```bash
# List volumes -- Liệt kê volumes
docker volume ls                 # List all volumes -- Liệt kê tất cả volumes

# Create volume -- Tạo volume
docker volume create myvolume    # Create named volume -- Tạo named volume

# Inspect -- Kiểm tra
docker volume inspect myvolume   # Volume details -- Chi tiết volume

# Remove -- Xóa
docker volume rm myvolume        # Remove volume -- Xóa volume
docker volume prune              # Remove unused volumes -- Xóa volumes không dùng

# Use volumes -- Sử dụng volumes
docker run -v myvolume:/data nginx           # Named volume -- Named volume
docker run -v /host/path:/container/path nginx  # Bind mount -- Bind mount
docker run -v /container/path nginx          # Anonymous volume -- Anonymous volume
```

## <a id="system"></a> System

```bash
# System info -- Thông tin hệ thống
docker version               # Docker version -- Phiên bản Docker
docker info                  # System information -- Thông tin hệ thống

# Clean up -- Dọn dẹp
docker system prune          # Remove unused data -- Xóa dữ liệu không dùng
docker system prune -a       # Remove all unused data -- Xóa tất cả dữ liệu không dùng
docker system prune -a --volumes  # Include volumes -- Bao gồm volumes
docker system df             # Disk usage -- Sử dụng đĩa

# Events -- Sự kiện
docker events                # Real-time events -- Sự kiện real-time
docker events --since 1h     # Events from last hour -- Sự kiện từ 1 giờ trước
```

## <a id="registry"></a> Registry

```bash
# Login/Logout -- Đăng nhập/Đăng xuất
docker login                 # Login to Docker Hub -- Đăng nhập Docker Hub
docker login myregistry.com  # Login to private registry -- Đăng nhập registry riêng
docker logout                # Logout -- Đăng xuất

# Push images -- Push images
docker push myimage:tag      # Push to registry -- Push lên registry
docker push myregistry.com/myimage:tag  # Push to private registry -- Push lên registry riêng

# Search -- Tìm kiếm
docker search nginx          # Search Docker Hub -- Tìm kiếm trên Docker Hub
```

## <a id="dockerfile-best-practices"></a> Dockerfile Best Practices

```dockerfile
# Use specific base image version -- Dùng phiên bản base image cụ thể
FROM node:16-alpine

# Set working directory -- Đặt thư mục làm việc
WORKDIR /app

# Copy dependency files first (better caching) -- Copy files dependencies trước (cache tốt hơn)
COPY package*.json ./

# Install dependencies -- Cài đặt dependencies
RUN npm ci --only=production

# Copy application code -- Copy code ứng dụng
COPY . .

# Expose port -- Expose cổng
EXPOSE 3000

# Use non-root user -- Dùng non-root user
USER node

# Start application -- Khởi động ứng dụng
CMD ["node", "server.js"]
```

## <a id="common-patterns"></a> Common Patterns -- Patterns Thường dùng

```bash
# Remove all stopped containers -- Xóa tất cả containers đã dừng
docker rm $(docker ps -a -q)

# Remove all images -- Xóa tất cả images
docker rmi $(docker images -q)

# Stop all running containers -- Dừng tất cả containers đang chạy
docker stop $(docker ps -q)

# Remove all containers (force) -- Xóa tất cả containers (cưỡng chế)
docker rm -f $(docker ps -a -q)

# View logs of all containers -- Xem logs của tất cả containers
docker-compose logs -f

# Rebuild and restart specific service -- Rebuild và khởi động lại service cụ thể
docker-compose up -d --build service_name

# Shell into running container -- Shell vào container đang chạy
docker exec -it $(docker ps -q -f name=container_name) bash
```

---
