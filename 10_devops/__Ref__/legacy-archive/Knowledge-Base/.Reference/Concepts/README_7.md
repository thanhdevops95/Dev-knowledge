# 🎯 GIAI ĐOẠN 2: DOCKER HÓA - HOÀN CHỈNH

## 📌 MÔ TẢ
Thư mục này chứa code từ **Giai đoạn 1 + Giai đoạn 2**.
- Giai đoạn 1: Code Go & Python (bare-metal)
- **Giai đoạn 2: Dockerfiles + Docker Network**

Hai service giờ chạy trong Container, giao tiếp qua Docker Network.

## 🏗️ CẤU TRÚC

```
Stage02_Complete/
├── go-service/
│   ├── main.go
│   ├── go.mod
│   ├── go.sum
│   └── Dockerfile        # ← MỚI
├── python-service/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile        # ← MỚI
├── README.md
└── NOTES.md
```

## 🚀 CÁCH CHẠY

### Bước 1: Build Docker Images

**Build Go Image:**
```bash
cd go-service
docker build -t todo-go:v1 .
```

**Build Python Image:**
```bash
cd python-service
docker build -t todo-python:v1 .
```

**Kiểm tra images:**
```bash
docker images | grep todo
```

### Bước 2: Tạo Docker Network

```bash
docker network create todo-net
```

### Bước 3: Chạy Containers

**Chạy Go Container:**
```bash
docker run -d \
  --name go-app \
  --network todo-net \
  todo-go:v1
```

**Chạy Python Container:**
```bash
docker run -d \
  --name python-app \
  --network todo-net \
  -p 5000:8080 \
  -e GO_HOST=go-app \
  todo-python:v1
```

**Giải thích:**
- `--network todo-net`: Cắm vào mạng chung
- `-p 5000:8080`: Map port 5000 (host) → 8080 (container)
- `-e GO_HOST=go-app`: Python sẽ gọi `http://go-app:8081` (DNS)

### Bước 4: Kiểm tra

```bash
# Xem containers đang chạy
docker ps

# Xem log
docker logs python-app
docker logs go-app
```

## 🧪 TESTING

### Test 1: Ping
```bash
curl http://localhost:5000/ping
```

### Test 2: Tạo TODO
```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Docker hóa thành công!"}'
```

### Test 3: Xem TODO
```bash
curl http://localhost:5000/api/todos
```

### Test 4: DNS Resolution (Kiểm tra Python gọi Go qua tên)
```bash
# Vào trong Python container
docker exec -it python-app sh

# Trong container, ping go-app
ping go-app
# Kết quả: Thấy IP của go-app container

# Hoặc curl trực tiếp
curl http://go-app:8081/ping

exit
```

### Test 5: Restart & Mất dữ liệu
```bash
# Tạo TODO
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Test data"}'

# Restart Go container
docker restart go-app

# Kiểm tra lại
curl http://localhost:5000/api/todos
# Kết quả: [] (rỗng) - Vẫn mất dữ liệu!
```

## 🧹 DỌN DẸP

```bash
# Dừng và xóa containers
docker rm -f go-app python-app

# Xóa network
docker network rm todo-net

# Xóa images (nếu muốn)
docker rmi todo-go:v1 todo-python:v1
```

## ✅ CHECKLIST HOÀN THÀNH

- [ ] Build được Go image
- [ ] Build được Python image
- [ ] Tạo được Docker network
- [ ] Chạy được cả 2 containers
- [ ] Test Ping thành công
- [ ] CRUD operations hoạt động
- [ ] DNS resolution hoạt động (Python gọi Go bằng tên)
- [ ] Hiểu được dữ liệu vẫn mất khi restart

## 🔍 ĐIỂM HỌC ĐƯỢC

1. ✅ Multi-stage build để giảm kích thước image
2. ✅ Docker Network cho phép containers "nhìn thấy nhau" bằng tên
3. ✅ Port mapping (-p) để expose ra ngoài
4. ✅ Environment variables (-e) để config
5. ✅ Container là ephemeral (vô thường) - restart là mất data

## 🚧 VẤN ĐỀ CẦN GIẢI QUYẾT Ở GIAI ĐOẠN SAU

- ❌ Dữ liệu vẫn mất khi restart → **Giai đoạn 3: Docker Volume**
- ❌ Lệnh docker run dài quá → **Giai đoạn 4: Docker Compose**

## 📝 GHI CHÚ

Xem file `NOTES.md` để biết kết quả test thực tế.
