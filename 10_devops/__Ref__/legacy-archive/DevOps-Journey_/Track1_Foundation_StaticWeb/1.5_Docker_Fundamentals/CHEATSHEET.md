# 📋 Docker Fundamentals - Cheatsheet

> **Quick Reference for Docker Commands**
>
> *Tra cứu nhanh các lệnh Docker*

---

## 🐳 Images

```bash
docker images               # List images (Liệt kê images)
docker pull nginx           # Pull image (Tải image)
docker build -t myapp .     # Build image (Build image)
docker rmi image_name       # Remove image (Xóa image)
docker image prune          # Remove unused (Xóa không dùng)
```

---

## 📦 Containers

```bash
docker ps                   # Running containers (Containers đang chạy)
docker ps -a                # All containers (Tất cả containers)
docker run -d -p 80:80 nginx  # Run container (Chạy container)
docker stop container_id    # Stop container (Dừng container)
docker rm container_id      # Remove container (Xóa container)
docker exec -it container bash  # Enter container (Vào container)
docker logs container_id    # View logs (Xem logs)
docker logs -f container_id # Follow logs (Theo dõi logs)
```

---

## 📝 Dockerfile

```dockerfile
FROM nginx:alpine           # Base image (Image gốc)
WORKDIR /app                # Working directory (Thư mục làm việc)
COPY . .                    # Copy files (Sao chép files)
RUN npm install             # Run command (Chạy lệnh)
EXPOSE 80                   # Expose port (Mở port)
CMD ["nginx", "-g", "daemon off;"]  # Start command
```

---

## 🔧 Useful Commands (Lệnh hữu ích)

```bash
docker inspect container    # Container details (Chi tiết container)
docker stats                # Resource usage (Sử dụng tài nguyên)
docker top container        # Processes in container (Tiến trình)
docker cp file container:/path  # Copy to container (Sao chép vào)
docker commit container new_image  # Save container as image
```

---

## 🧹 Cleanup (Dọn dẹp)

```bash
docker system prune         # Remove unused (Xóa không dùng)
docker system prune -a      # Remove all unused (Xóa tất cả không dùng)
docker volume prune         # Remove unused volumes (Xóa volumes)
docker container prune      # Remove stopped containers (Xóa containers đã dừng)
```

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
