# GIAI ĐOẠN 4: DOCKER COMPOSE - NHẠC TRƯỞNG (ORCHESTRATION)

## 📌 MỤC TIÊU GIAI ĐOẠN 4
Thay vì nhớ một tràng lệnh `docker run` với hàng tá tham số (`--network`, `-v`, `-e`, `-p`...), chúng ta dùng một file `docker-compose.yaml` để khai báo toàn bộ hệ thống "Infrastructure as Code".

**Lợi ích:**
✅ Chỉ cần 1 lệnh `up` để bật cả hệ thống.
✅ Chỉ cần 1 lệnh `down` để tắt sạch sẽ.
✅ Dễ dàng chia sẻ file cấu hình cho đồng đội.

---

## 🛠️ PHẦN 1: VIẾT DOCKER COMPOSE FILE

Tạo file có tên `docker-compose.yaml` (hoặc `.yml`) ngay tại thư mục gốc dự án `Todo-App-DevOps/`.

Nội dung file:

```yaml
version: '3.8'  # Phiên bản format

services:
  # --- Service 1: Go Backend ---
  backend:
    container_name: go-app      # Đặt tên cố định cho dễ nhớ
    image: todo-go:v2           # Dùng image đã build ở Giai đoạn 3
    build: ./go-service         # (Optional) Tự build nếu chưa có image
    volumes:
      - ./data:/app/data        # Map volume cứu dữ liệu
    networks:
      - app-network             # Cắm vào mạng chung
    restart: always             # Tự khởi động lại nếu crash

  # --- Service 2: Python Gateway ---
  gateway:
    container_name: python-app
    image: todo-python:v1
    build: ./python-service
    ports:
      - "5000:8080"             # Map port ra máy thật
    environment:
      - GO_HOST=backend         # Trỏ tới tên service 'backend' (DNS)
    depends_on:
      - backend                 # Chờ backend chạy trước rồi mới chạy gateway
    networks:
      - app-network

# --- Định nghĩa Network ---
networks:
  app-network:
    driver: bridge
```

### 🧐 Phân tích kỹ:
1. **services**: Định nghĩa các "máy con". Ở đây có `backend` và `gateway`.
2. **DNS Magic**: Trong mạng Compose, tên service chính là hostname.
   - Python config `GO_HOST=backend` -> Nó sẽ gọi `http://backend:8081`. (Lưu ý: trong file yaml mình đặt tên service là `backend`, container_name là `go-app`. Compose cho phép dùng tên service làm DNS. Tốt nhất nên dùng tên service).
3. **depends_on**: Giúp kiểm soát thứ tự khởi động (tuy nhiên không chờ app *sẵn sàng* thực sự, chỉ chờ container chạy).

---

## 🚀 PHẦN 2: CHẠY (DEPLOY)

### B1. Khởi động (Up)
Tại thư mục chứa file yaml:
```bash
docker compose up -d
```
> `-d`: Detached (chạy ngầm).
> Nếu bạn chưa có image, Compose sẽ tự động chạy lệnh build (nhờ dòng `build: ./...`).

### B2. Kiểm tra trạng thái (PS)
```bash
docker compose ps
```
Bạn sẽ thấy 2 container đang `Up`.

### B3. Xem Log (Logs)
Nếu muốn biết chuyện gì đang xảy ra bên trong:
```bash
docker compose logs -f
```
*(Bấm Ctrl+C để thoát xem log)*

---

## 🧪 PHẦN 3: TEST (VẪN NHƯ CŨ)

Hệ thống hoạt động y hệt Giai đoạn 3, nhưng quy trình vận hành sướng hơn nhiều.

1. **Test Ping:** `curl http://localhost:5000/ping`
2. **Test Data:** `curl http://localhost:5000/api/todos` -> Nên thấy dữ liệu cũ (từ Giai đoạn 3) vì ta vẫn map vào folder `./data`.

---

## 🧹 PHẦN 4: CÁC LỆNH HỮU ÍCH

### Tắt hệ thống (Stop & Remove Containers/Networks)
```bash
docker compose down
```

### Tắt và xóa luôn cả Volume (Cẩn thận!)
```bash
docker compose down -v
```
*(Lưu ý: Lệnh này thường chỉ xóa Named Volume, còn Bind Mount `./data` của mình thì file vẫn còn trên máy).*

### Rebuild lại code mới
Nếu bạn sửa code, chỉ cần:
```bash
docker compose up -d --build
```
Compose sẽ phát hiện thay đổi, build lại image và restart container.

---

## 📝 TỔNG KẾT
Docker Compose là công cụ "bất ly thân" của Developer. Nó thu gọn quy trình triển khai phức tạp vào 1 file duy nhất.

👉 **Bước tiếp theo:** Người dùng không thích dùng `curl`. Họ cần giao diện Web đẹp. Giai đoạn 5 sẽ thêm **NGINX** và **Frontend HTML/JS**.
