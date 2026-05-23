# Hướng Dẫn Xử Lý Lỗi: Không thể kết nối Docker Daemon

## 1. Dấu hiệu nhận biết
Bạn gõ bất kỳ lệnh docker nào cũng nhận được thông báo:
```text
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

## 2. Nguyên nhân
- **Docker chưa được bật**: Bạn mới chỉ cài đặt nhưng chưa mở ứng dụng Docker Desktop (hoặc OrbStack) lên.
- **Vấn đề về quyền (Permission)**: Ở Linux, socket của Docker thường được sở hữu bởi `root`. User thường không có quyền truy cập.

## 3. Giải Pháp

### Trên macOS
1. Nhìn lên thanh Menu Bar (góc trên bên phải), tìm biểu tượng con cá voi (Docker) hoặc hình tròn đen (OrbStack).
2. Nếu không thấy, nhấn `Cmd + Space` (Spotlight) gõ "Docker" và mở nó lên.
3. Đợi vài giây đến khi biểu tượng đứng yên (Docker is running).

### Trên Linux (Ubuntu Server)
1. Kiểm tra trạng thái service:
   ```bash
   sudo systemctl status docker
   ```
2. Nếu nó đang tắt (inactive), hãy bật lên:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker  # Để tự bật khi khởi động lại máy
   ```
3. Nếu service đang chạy (active) mà vẫn lỗi "Permission denied":
   - Thêm user vào nhóm docker:
     ```bash
     sudo usermod -aG docker $USER
     ```
   - **Quan trọng:** Bạn cần Logout khỏi SSH và Login lại thì group mới mới được cập nhật. Hoặc gõ lệnh tạm thời: `newgrp docker`.
