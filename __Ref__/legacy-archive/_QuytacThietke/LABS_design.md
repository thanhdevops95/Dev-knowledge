# LABS.md Design Specification

## 1. Purpose

- **Mục đích:** Cung cấp hướng dẫn thực hành chi tiết, cho phép học viên copy-paste và chạy ngay các lệnh.
- **Mục tiêu:** Áp dụng kiến thức lý thuyết vào thực tế thông qua các bài lab có hướng dẫn từng bước.
- **Lưu ý:** Khác với Exercises (tự làm), Labs có hướng dẫn chi tiết và output mong đợi.

---

## 2. File Header (Metadata)

```yaml
---
module: "X.Y"
title: "<Tên Module> – Labs"
track: "<Số Track>"
version: "1.0"
last_updated: "YYYY-MM-DD"
total_labs: 3
estimated_time: "60-90 minutes"
difficulty: "Beginner | Intermediate | Advanced"
---
```

---

## 3. Required Sections (theo thứ tự bắt buộc)

### 3.1. Header

```markdown
## MODULE X.Y – <Tên Module> Labs
```

### 3.2. Overview (Tổng quan)

- Số lượng labs
- Thời gian ước tính
- Mức độ khó
- Yêu cầu hoàn thành

### 3.3. Prerequisites (Yêu cầu)

- Checklist công cụ cần cài đặt
- Kiến thức cần có
- Tài nguyên cần chuẩn bị

### 3.3.1. Environment Check ⭐ BẮT BUỘC (Kiểm tra môi trường)

**Mỗi Lab phải có mục này ngay đầu tiên:**

```markdown
### 🔍 Environment Check (Trước khi bắt đầu)

Chạy các lệnh sau để đảm bảo môi trường sẵn sàng:

| Kiểm tra | Lệnh | Kết quả mong đợi |
|----------|------|------------------|
| Docker đang chạy | `docker version` | Hiển thị version Client và Server |
| Port 8080 trống | `netstat -an | grep 8080` (Linux/Mac) hoặc `netstat -an | findstr 8080` (Windows) | Không có output |
| Git đã cài | `git --version` | `git version X.Y.Z` |

> ⚠️ **Nếu Docker không chạy:** Khởi động Docker Desktop và đợi 30 giây.
```

**Lý do:** Môi trường học viên rất đa dạng (Windows, Mac, Linux). Việc kiểm tra trước giúp tránh lỗi không đáng có.

### 3.4. Labs (Các bài thực hành)

Mỗi lab bao gồm:

- **Lab ID & Title**
- **Objective** (Mục tiêu)
- **Estimated Time** (Thời gian ước tính)
- **Environment Check** (Kiểm tra môi trường) ⭐
- **Step-by-Step Instructions** (Hướng dẫn từng bước)
- **Expected Output** (Kết quả mong đợi)
- **Verification** (Cách kiểm tra)
- **Troubleshooting** (Xử lý lỗi)

### 3.5. Cleanup (Dọn dẹp)

- Lệnh dọn dẹp tài nguyên sau khi hoàn thành
- Kiểm tra đã cleanup thành công

### 3.6. References (Tham khảo)

- Link tới docs liên quan
- Tài liệu bổ sung

### 3.7. Navigation Footer ⭐ BẮT BUỘC

Cuối mỗi file phải có điều hướng:

```markdown
---

[⬅️ CHEATSHEET](./CHEATSHEET.md) | [📚 Mục lục](../../README.md) | [EXERCISES ➡️](./EXERCISES.md)
```

---

## 4. Formatting Rules

| Thành phần | Quy tắc |
|------------|---------|
| Tiêu đề | `##` cho chính, `###` cho mục con |
| Bước | Đánh số: 1., 2., 3... |
| Code | Block với ngôn ngữ phù hợp |
| Output | Block với `text` hoặc `bash` |
| Lỗi | Table với Error, Cause, Solution |

---

## 5. Style Guide

- **Copy-paste friendly:** Lệnh có thể copy và chạy ngay
- **Output rõ ràng:** Hiển thị output mong đợi
- **Checkpoint:** Có verification sau mỗi bước quan trọng
- **Troubleshooting:** Liệt kê lỗi phổ biến

---

## 6. Review Checklist

- [ ] Mỗi lab có đầy đủ: Objective, Steps, Output, Verification
- [ ] Có Environment Check ở đầu mỗi lab ⭐
- [ ] Lệnh trong code block đúng cú pháp và chạy được
- [ ] Output mong đợi chính xác
- [ ] Troubleshooting bao gồm lỗi phổ biến
- [ ] Có phần Cleanup
- [ ] **Có Navigation Footer cuối file** ⭐
- [ ] `last_updated` là ngày hiện tại

---

## 7. Do's and Don'ts

### ✅ Nên làm

- Test từng bước trên môi trường thực
- Cung cấp output mẫu để verify
- Comment trong code giải thích
- Checkpoint sau mỗi milestone

### ❌ Không nên làm

- Lệnh không chạy được
- Thiếu output verification
- Sử dụng lệnh nguy hiểm không cảnh báo
- Bỏ qua cleanup

---

## 8. Example Template (Copy-Paste)

```markdown
---
module: "1.4"
title: "Docker Fundamentals – Labs"
track: "1"
version: "1.0"
last_updated: "2025-12-27"
total_labs: 3
estimated_time: "60-90 minutes"
difficulty: "Beginner"
---

## MODULE 1.4 – Docker Fundamentals Labs

### Overview
- **Số lượng labs:** 3 bài
- **Thời gian ước tính:** 60-90 phút
- **Mức độ khó:** Beginner
- **Yêu cầu:** Hoàn thành tất cả 3 labs

---

### Prerequisites

#### Công cụ
- [ ] Docker Desktop đã cài đặt và đang chạy
- [ ] Terminal/Command Line
- [ ] Text editor (VS Code recommended)

#### Kiểm tra môi trường
```bash
# Kiểm tra Docker version
docker --version
# Output mong đợi: Docker version 24.x.x

# Kiểm tra Docker đang chạy
docker info
# Nếu thấy "Server: Docker Desktop" là OK
```

---

## Lab 1: Your First Container

### Objective

Chạy container đầu tiên và hiểu các lệnh Docker cơ bản.

### Estimated Time

15 phút

---

### Step 1: Pull image từ Docker Hub

```bash
# Pull image nginx (web server phổ biến)
docker pull nginx:alpine
```

**Expected Output:**

```
alpine: Pulling from library/nginx
a387a0fe20ea: Pull complete
...
Status: Downloaded newer image for nginx:alpine
docker.io/library/nginx:alpine
```

**Verification:**

```bash
# Kiểm tra image đã được pull
docker images nginx

# Output:
# REPOSITORY   TAG       IMAGE ID       SIZE
# nginx        alpine    abc123def      41.1MB
```

---

### Step 2: Run container

```bash
# Chạy nginx container ở background
docker run -d --name my-nginx -p 8080:80 nginx:alpine
```

**Giải thích flags:**

| Flag | Ý nghĩa |
|------|---------|
| `-d` | Detached mode (chạy background) |
| `--name my-nginx` | Đặt tên container |
| `-p 8080:80` | Map host port 8080 → container port 80 |

**Expected Output:**

```
a1b2c3d4e5f6789...  (container ID)
```

**Verification:**

```bash
# Kiểm tra container đang chạy
docker ps

# Output:
# CONTAINER ID   IMAGE          PORTS                  NAMES
# a1b2c3d4e5f6   nginx:alpine   0.0.0.0:8080->80/tcp   my-nginx
```

---

### Step 3: Access ứng dụng

**Cách 1: Dùng curl**

```bash
curl http://localhost:8080
```

**Expected Output:**

```html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
```

**Cách 2: Mở browser**

- Truy cập: `http://localhost:8080`
- Kết quả: Trang welcome của NGINX

---

### Step 4: Xem logs

```bash
# Xem logs của container
docker logs my-nginx

# Follow logs (realtime)
docker logs -f my-nginx
# Nhấn Ctrl+C để thoát
```

**Expected Output:**

```
/docker-entrypoint.sh: Configuration complete; ready for start up
2025/12/27 10:00:00 [notice] 1#1: nginx/1.25.3
```

---

### Step 5: Truy cập shell bên trong container

```bash
# Mở shell trong container
docker exec -it my-nginx /bin/sh

# Bên trong container, thử các lệnh:
ls -la /usr/share/nginx/html/
cat /etc/nginx/nginx.conf
exit
```

**Verification:**

```bash
# Sau khi exit, container vẫn chạy
docker ps | grep my-nginx
```

---

### Step 6: Stop và restart container

```bash
# Stop container
docker stop my-nginx

# Kiểm tra - không còn trong ps
docker ps

# Nhưng vẫn còn trong ps -a
docker ps -a | grep my-nginx

# Restart container
docker start my-nginx

# Kiểm tra lại
docker ps
```

---

### Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `port is already allocated` | Port 8080 đã được dùng | Đổi port: `-p 8081:80` |
| `Cannot connect to Docker daemon` | Docker không chạy | Start Docker Desktop |
| `name already in use` | Container name trùng | `docker rm my-nginx` hoặc đổi tên |
| `connection refused` | Container không chạy | `docker start my-nginx` |

---

## Lab 2: Build Custom Image

### Objective

Viết Dockerfile và build custom Docker image.

### Estimated Time

25 phút

---

### Step 1: Tạo project folder

```bash
mkdir my-web-app
cd my-web-app
```

---

### Step 2: Tạo file HTML

```bash
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Docker App</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            text-align: center;
            padding: 40px;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        h1 { font-size: 3em; margin-bottom: 10px; }
        p { font-size: 1.2em; opacity: 0.9; }
        .emoji { font-size: 4em; }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">🐳</div>
        <h1>Hello from Docker!</h1>
        <p>Đây là web app đầu tiên của tôi được containerize.</p>
        <p>Build time: <span id="time"></span></p>
    </div>
    <script>
        document.getElementById('time').textContent = new Date().toLocaleString('vi-VN');
    </script>
</body>
</html>
EOF
```

---

### Step 3: Tạo Dockerfile

```bash
cat > Dockerfile << 'EOF'
# Dockerfile for my-web-app
# Base image: NGINX Alpine (lightweight)
FROM nginx:alpine

# Maintainer info
LABEL maintainer="your-email@example.com"
LABEL version="1.0"
LABEL description="My first custom Docker image"

# Copy HTML file to NGINX default location
COPY index.html /usr/share/nginx/html/index.html

# Expose port 80
EXPOSE 80

# NGINX runs automatically (inherited from base image)
EOF
```

**Verification:**

```bash
# Kiểm tra files đã tạo
ls -la

# Output:
# Dockerfile
# index.html
```

---

### Step 4: Build image

```bash
# Build với tag my-web-app:v1
docker build -t my-web-app:v1 .
```

**Expected Output:**

```
[+] Building 2.5s (7/7) FINISHED
 => [internal] load build definition from Dockerfile
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/nginx:alpine
 => [1/2] FROM docker.io/library/nginx:alpine
 => [2/2] COPY index.html /usr/share/nginx/html/index.html
 => exporting to image
 => => naming to docker.io/library/my-web-app:v1
```

**Verification:**

```bash
# Kiểm tra image
docker images my-web-app

# Output:
# REPOSITORY    TAG   IMAGE ID       SIZE
# my-web-app    v1    xyz789abc      41.5MB
```

---

### Step 5: Run container từ custom image

```bash
# Chạy container
docker run -d --name my-app -p 9000:80 my-web-app:v1

# Kiểm tra
docker ps
```

**Verification:**

```bash
# Test trong terminal
curl http://localhost:9000

# Hoặc mở browser: http://localhost:9000
```

---

### Step 6: Update và rebuild

```bash
# Sửa file HTML
sed -i 's/Hello from Docker!/Hello from Docker v2!/' index.html

# Rebuild với tag mới
docker build -t my-web-app:v2 .

# Chạy container mới
docker run -d --name my-app-v2 -p 9001:80 my-web-app:v2
```

---

### Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `COPY failed: file not found` | File không tồn tại | Kiểm tra file có trong thư mục |
| `invalid reference format` | Tag sai format | Dùng lowercase, không có space |
| `build context too large` | Thư mục quá lớn | Tạo .dockerignore |

---

## Lab 3: Docker Volumes

### Objective

Hiểu và sử dụng Docker volumes để persist data.

### Estimated Time

20 phút

---

### Step 1: Tạo volume

```bash
# Tạo named volume
docker volume create mydata

# Kiểm tra
docker volume ls
```

**Expected Output:**

```
DRIVER    VOLUME NAME
local     mydata
```

---

### Step 2: Run container với volume

```bash
# Chạy container và mount volume
docker run -d --name data-container \
  -v mydata:/data \
  nginx:alpine

# Tạo file trong volume
docker exec data-container sh -c "echo 'Hello Volume!' > /data/test.txt"

# Kiểm tra file
docker exec data-container cat /data/test.txt
```

**Expected Output:**

```
Hello Volume!
```

---

### Step 3: Verify data persistence

```bash
# Stop và remove container
docker stop data-container
docker rm data-container

# Chạy container mới với cùng volume
docker run -d --name new-container \
  -v mydata:/data \
  nginx:alpine

# Kiểm tra file vẫn còn
docker exec new-container cat /data/test.txt
```

**Expected Output:**

```
Hello Volume!
```

Data vẫn còn nguyên! 🎉

---

### Step 4: Bind mount (mount thư mục local)

```bash
# Tạo thư mục local
mkdir ~/docker-data
echo "Local file content" > ~/docker-data/local.txt

# Mount thư mục local vào container
docker run -d --name bind-container \
  -v ~/docker-data:/app/data \
  nginx:alpine

# Kiểm tra
docker exec bind-container cat /app/data/local.txt
```

---

### Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `volume not found` | Volume chưa tạo | `docker volume create <name>` |
| `permission denied` | Quyền thư mục | Kiểm tra permissions |
| `mount path must be absolute` | Đường dẫn không tuyệt đối | Dùng full path |

---

## Cleanup

Sau khi hoàn thành tất cả labs:

```bash
# Stop tất cả containers của labs này
docker stop my-nginx my-app my-app-v2 data-container new-container bind-container 2>/dev/null

# Remove containers
docker rm my-nginx my-app my-app-v2 data-container new-container bind-container 2>/dev/null

# Remove images
docker rmi my-web-app:v1 my-web-app:v2 2>/dev/null

# Remove volume
docker volume rm mydata 2>/dev/null

# Cleanup thư mục
rm -rf my-web-app ~/docker-data

# Kiểm tra cleanup
docker ps -a
docker images
docker volume ls
```

---

## Summary

Sau khi hoàn thành 3 labs, bạn đã biết:

- ✅ Pull và run container từ Docker Hub
- ✅ Xem logs và truy cập shell container
- ✅ Viết Dockerfile và build custom image
- ✅ Sử dụng volumes để persist data
- ✅ Cleanup resources sau khi xong

---

## References

- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Volumes](https://docs.docker.com/storage/volumes/)
- [GLOSSARY](../../resources/GLOSSARY.md)

---

[⬅️ CHEATSHEET](./CHEATSHEET.md) | [📚 Mục lục](../../README.md) | [EXERCISES ➡️](./EXERCISES.md)

```

---

*File này là chuẩn mẫu cho mọi `LABS.md` trong khoá học DevOps.*
