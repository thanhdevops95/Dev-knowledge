# 🎯 GIAI ĐOẠN 4: DOCKER COMPOSE - ORCHESTRATION

## 📌 MÔ TẢ
Thư mục này chứa code từ **Giai đoạn 1-4**.
- **Giai đoạn 4: docker-compose.yaml** - Quản lý toàn bộ hệ thống bằng 1 file!

Không cần gõ lệnh `docker run` dài nữa. Chỉ cần `docker compose up`!

## 🏗️ CẤU TRÚC

```
Stage04_Complete/
├── go-service/
├── python-service/
├── data/
├── docker-compose.yaml   # ← MỚI: File "nhạc trưởng"
├── README.md
└── NOTES.md
```

## 🚀 CÁCH CHẠY

### Cách cũ (Giai đoạn 3) - Phức tạp:
```bash
docker network create todo-net
docker build -t todo-go:v2 ./go-service
docker build -t todo-python:v1 ./python-service
docker run -d --name go-app --network todo-net -v $(pwd)/data:/app/data todo-go:v2
docker run -d --name python-app --network todo-net -p 5000:8080 -e GO_HOST=go-app todo-python:v1
```

### Cách mới (Giai đoạn 4) - Đơn giản:
```bash
docker compose up -d
```

**Chỉ 1 lệnh!** Compose sẽ tự động:
- ✅ Tạo network
- ✅ Build images (nếu chưa có)
- ✅ Chạy containers theo thứ tự (depends_on)
- ✅ Mount volumes
- ✅ Set environment variables

## 🧪 TESTING

### Test 1: Khởi động hệ thống
```bash
docker compose up -d
```

**Output:**
```
[+] Running 3/3
 ✔ Network stage04_complete_app-network  Created
 ✔ Container go-app                      Started
 ✔ Container python-app                  Started
```

### Test 2: Kiểm tra trạng thái
```bash
docker compose ps
```

**Kết quả mong đợi:**
```
NAME         IMAGE            STATUS    PORTS
go-app       todo-go:v2       Up        
python-app   todo-python:v1   Up        0.0.0.0:5000->8080/tcp
```

### Test 3: Xem logs
```bash
# Tất cả services
docker compose logs

# Chỉ 1 service
docker compose logs backend

# Realtime
docker compose logs -f
```

### Test 4: CRUD Operations (như cũ)
```bash
# Tạo TODO
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Docker Compose rất tiện!"}'

# Xem TODO
curl http://localhost:5000/api/todos
```

### Test 5: Restart & Persistence
```bash
# Tắt hệ thống
docker compose down

# Bật lại
docker compose up -d

# Kiểm tra data
curl http://localhost:5000/api/todos
# → Vẫn còn! (nhờ volume)
```

### Test 6: Rebuild khi code thay đổi
```bash
# Sửa code (ví dụ: đổi message trong ping)
# Rồi rebuild và restart
docker compose up -d --build
```

## 🔧 CÁC LỆNH COMPOSE HỮU ÍCH

```bash
# Khởi động (detached)
docker compose up -d

# Khởi động và xem log
docker compose up

# Dừng (giữ containers)
docker compose stop

# Dừng và xóa containers
docker compose down

# Dừng, xóa containers + volumes
docker compose down -v

# Rebuild images
docker compose build

# Pull images mới
docker compose pull

# Restart 1 service
docker compose restart backend

# Chạy lệnh trong service
docker compose exec backend sh

# Xem config đã parse
docker compose config
```

## 📊 PHÂN TÍCH DOCKER-COMPOSE.YAML

```yaml
version: '3.8'  # Phiên bản format

services:
  backend:
    container_name: go-app      # Tên container cố định
    build: ./go-service         # Tự build nếu chưa có image
    image: todo-go:v2           # Tên image sau khi build
    volumes:
      - ./data:/app/data        # Bind mount
    networks:
      - app-network             # Kết nối vào network
    restart: always             # Tự restart nếu crash

  gateway:
    depends_on:
      - backend                 # Chờ backend start trước
    environment:
      - GO_HOST=backend         # Biến môi trường
    ports:
      - "5000:8080"             # Port mapping

networks:
  app-network:
    driver: bridge              # Network type
```

## ✅ CHECKLIST HOÀN THÀNH

- [ ] Tạo được file docker-compose.yaml
- [ ] `docker compose up -d` chạy thành công
- [ ] Cả 2 services đều Up
- [ ] CRUD operations hoạt động
- [ ] Data vẫn còn sau khi `down` và `up` lại
- [ ] Hiểu được cách Compose hoạt động

## 🔍 ĐIỂM HỌC ĐƯỢC

1. ✅ **Infrastructure as Code:** Toàn bộ hệ thống trong 1 file YAML
2. ✅ **Dependency management:** `depends_on` kiểm soát thứ tự
3. ✅ **Service discovery:** Gọi nhau bằng tên service
4. ✅ **Declarative:** Khai báo "muốn gì", không phải "làm thế nào"

## 🚧 VẤN ĐỀ CẦN GIẢI QUYẾT Ở GIAI ĐOẠN SAU

- ❌ Chưa có giao diện Web → **Giai đoạn 5: NGINX + Frontend**
- ❌ File JSON không chuyên nghiệp → **Giai đoạn 6: MySQL**

## 📝 GHI CHÚ

Xem file `NOTES.md` để biết kết quả test thực tế.
