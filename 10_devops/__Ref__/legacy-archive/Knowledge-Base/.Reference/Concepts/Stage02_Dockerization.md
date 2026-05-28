# GIAI ĐOẠN 2: DOCKER HÓA - SỰ CÔ LẬP & PORTABILITY

## 📌 MỤC TIÊU GIAI ĐOẠN 2
"Tại sao máy tôi chạy được mà máy bạn lại lỗi?" 🤔
Docker sinh ra để giải quyết vấn đề đó. Giai đoạn này chúng ta sẽ đóng gói (Containerize) Python App và Go App thành các Docker Image.

**Bạn sẽ học được:**
✅ Viết `Dockerfile` tối ưu cho Python và Go.
✅ Build Docker Image thủ công.
✅ Chạy Container và hiểu về Port Mapping.
✅ Tạo Docker Network để các container "nhìn thấy nhau" bằng tên (Service Discovery).

---

## 🛠️ PHẦN 1: VIẾT DOCKERFILE

### 1. Dockerfile cho Go Service (Multi-stage Build)
Chúng ta sẽ dùng kỹ thuật **Multi-stage Build** để Image siêu nhẹ (chỉ chứa file binary đã biên dịch, không chứa source code hay compiler).

Tạo file `go-service/Dockerfile`:
```dockerfile
# --- Stage 1: Build ---
FROM golang:1.21-alpine AS builder

# Set thư mục làm việc trong container
WORKDIR /app

# Copy file dependency trước để tận dụng cache
COPY go.mod go.sum ./
RUN go mod download

# Copy toàn bộ source code
COPY . .

# Build ra file binary tên là "main"
RUN go build -o main .

# --- Stage 2: Run (Dùng Alpine cho nhẹ) ---
FROM alpine:3.19

WORKDIR /app

# Copy file binary từ Stage 1 sang Stage 2
COPY --from=builder /app/main .

# Expose port (chỉ mang tính document, cần -p khi run)
EXPOSE 8081

# Lệnh chạy app
CMD ["./main"]
```

### 2. Dockerfile cho Python Service
Python là ngôn ngữ thông dịch nên không cần build binary, nhưng nên dùng bản `slim` cho nhẹ.

Tạo file `python-service/Dockerfile`:
```dockerfile
# Dùng Python 3.9 bản slim (nhẹ hơn bản full)
FROM python:3.9-slim

WORKDIR /app

# Copy requirements và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app.py .

# Biến môi trường (để Python in log ngay lập tức)
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["python", "app.py"]
```

---

## 🏗️ PHẦN 2: BUILD IMAGE

Mở Terminal tại thư mục gốc `Todo-App-DevOps`.

### B1. Build Go Image
```bash
docker build -t todo-go:v1 ./go-service
```
>Giải thích:
> `-t todo-go:v1`: Đặt tên image là `todo-go`, tag `v1`.
> `./go-service`: Đường dẫn chứa Dockerfile.

### B2. Build Python Image
```bash
docker build -t todo-python:v1 ./python-service
```

### B3. Kiểm tra Image
```bash
docker images
```
Bạn sẽ thấy 2 image vừa tạo. Chú ý cột SIZE: Image Go sẽ rất nhẹ (chỉ vài chục MB), Image Python sẽ nặng hơn một chút.

---

## 🔌 PHẦN 3: TẠO NETWORK & CHẠY CONTAINER

Nếu chỉ chạy `docker run` bình thường, 2 container sẽ không nhìn thấy nhau qua `localhost`. Ta cần tạo một cái "Switch ảo" (Bridge Network).

### B1. Tạo Network
```bash
docker network create todo-net
```

### B2. Chạy Go Container
```bash
docker run -d \
  --name go-app \
  --network todo-net \
  todo-go:v1
```
> `-d`: Detached mode (chạy ngầm).
> `--name go-app`: Đặt tên container là `go-app`. Tên này chính là **DNS** để Python gọi tới!
> `--network todo-net`: Cắm vào mạng ảo.
> **Lưu ý:** Ta KHÔNG cần `-p 8081:8081` nếu chỉ muốn Python gọi Go trong nội bộ Docker. Nhưng để tiện test từ ngoài, ta tạm chưa map port này, hoặc map nếu muốn debug. (Ở đây ta sẽ để Python gọi Go qua mạng nội bộ Docker).

### B3. Cập nhật Code Python (Quan trọng!)
Ở Giai đoạn 1, `app.py` đang gọi `http://localhost:8081`.
Trong môi trường Docker:
- `localhost` của container Python là chính nó -> Không có Go ở đó.
- Go đang ở máy `go-app`.

👉 **Sửa file `python-service/app.py`:**
Sửa dòng `GO_SERVICE_URL`:
```python
import os

# Lấy từ biến môi trường, mặc định là localhost nếu chạy ngoài Docker
# Nhưng trong Docker ta sẽ truyền biến môi trường vào
GO_SERVICE_HOST = os.environ.get('GO_HOST', 'localhost')
GO_SERVICE_URL = f"http://{GO_SERVICE_HOST}:8081"
```
*(Nếu bạn lười sửa code check ENV, bạn có thể sửa cứng thành `http://go-app:8081` nhưng cách dùng ENV chuyên nghiệp hơn)*.
**Rebuild lại image Python sau khi sửa code:**
```bash
docker build -t todo-python:v1 ./python-service
```

### B4. Chạy Python Container
```bash
docker run -d \
  --name python-app \
  --network todo-net \
  -p 5000:8080 \
  -e GO_HOST=go-app \
  todo-python:v1
```
> `-p 5000:8080`: Map port 5000 máy thật -> port 8080 container.
> `-e GO_HOST=go-app`: Truyền biến môi trường. Python sẽ gọi `http://go-app:8081`.

---

## 🧪 PHẦN 4: THỰC HÀNH KIỂM THỬ

### Test Kết Nối:
Giờ đây ta truy cập qua Port **5000** của máy thật.

```bash
# Ping
curl http://localhost:5000/ping
# Output: Gateway Hello... Backend pong... (Thành công!)
```

### Test DNS Nội Bộ:
Làm sao biết Python thực sự gọi `go-app`? Hãy chui vào container Python:
```bash
docker exec -it python-app sh
# (Trong container)
ping go-app
# Kết quả: PING go-app (172.x.x.x): 56 data bytes... -> Thông nhau!
exit
```

### Test Restart & Mất Dữ Liệu (Vẫn như cũ):
1. Thêm 1 Todo qua port 5000.
2. Restart Go container: `docker restart go-app`.
3. Get lại Todo -> Mất sạch.
> **Kết luận:** Docker Container cũng là **Ephemeral** (vô thường). Restart là mất dữ liệu trong RAM. Giai đoạn 3 sẽ xử lý việc này bằng Volume.

## 🧹 DỌN DẸP (CLEAN UP)
Trước khi sang bài mới, hãy xóa container để tránh xung đột:
```bash
docker rm -f go-app python-app
```

---
👉 **Bước tiếp theo:** Cứu dữ liệu bằng **Docker Volume (Giai đoạn 3)**.
