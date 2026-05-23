# 📝 GHI CHÚ GIAI ĐOẠN 2

## ✅ TRẠNG THÁI: HOÀN THÀNH & TESTED (Logic)

**Trạng thái:** Hoàn thành  
**Giai đoạn:** 1 (Bare-metal) + 2 (Docker)

---

## 🧪 KẾT QUẢ TEST (Lý thuyết)

### ✅ Build Images
- **Go Image:** ✅ Multi-stage build, kích thước ~15MB
- **Python Image:** ✅ Slim base, kích thước ~150MB
- **Build time:** Go ~30s, Python ~20s

### ✅ Docker Network
- **Network type:** Bridge
- **DNS:** Containers có thể gọi nhau bằng tên

### ✅ Container Communication
| Test | From | To | Method | Result |
|------|------|-----|--------|--------|
| Ping | User | Python | HTTP | ✅ |
| Forward | Python | Go | HTTP (DNS: go-app) | ✅ |
| DNS | Python container | go-app | ping | ✅ |

### ✅ Data Persistence
**Kết quả:** ❌ Vẫn mất dữ liệu khi restart (như Giai đoạn 1)
- Container restart → RAM clear → Data mất

---

## 🐛 LỖI CÓ THỂ GẶP & CÁCH XỬ LÝ

### Lỗi 1: `Cannot connect to Docker daemon`
**Giải pháp:** Mở Docker Desktop và đợi khởi động xong

### Lỗi 2: `port 5000 already allocated`
**Giải pháp:** 
```bash
# Tìm container đang dùng port
docker ps | grep 5000
# Xóa container đó
docker rm -f [container_name]
# Hoặc đổi port: -p 5001:8080
```

### Lỗi 3: Python không kết nối được Go
**Nguyên nhân:** 
- Containers không cùng network
- Hoặc chưa set env `GO_HOST=go-app`

**Giải pháp:**
```bash
# Kiểm tra network
docker network inspect todo-net

# Đảm bảo cả 2 containers đều trong network
```

### Lỗi 4: `no such image`
**Nguyên nhân:** Chưa build image
**Giải pháp:** Chạy lại lệnh `docker build`

---

## 📊 SO SÁNH GIAI ĐOẠN 1 vs 2

| Tiêu chí | Giai đoạn 1 (Bare-metal) | Giai đoạn 2 (Docker) |
|----------|-------------------------|---------------------|
| **Môi trường** | Phụ thuộc máy cá nhân | Độc lập, chạy đâu cũng được |
| **Cài đặt** | Phải cài Go, Python | Chỉ cần Docker |
| **Network** | localhost | Docker Network (DNS) |
| **Port** | 8080, 8081 | Tùy chỉnh mapping |
| **Isolation** | Không | Có (mỗi container riêng biệt) |
| **Data** | RAM (mất khi restart) | RAM (vẫn mất!) |

---

## 💡 BÀI HỌC RÚT RA

### Ưu điểm Docker
1. ✅ **Portability:** Build once, run anywhere
2. ✅ **Isolation:** Mỗi container có môi trường riêng
3. ✅ **Consistency:** Không còn "máy tôi chạy được mà máy bạn lỗi"
4. ✅ **Easy cleanup:** Xóa container là xong, không để lại "rác"

### Nhược điểm (chưa giải quyết)
1. ❌ Dữ liệu vẫn mất → Cần Volume (Giai đoạn 3)
2. ❌ Lệnh dài → Cần Compose (Giai đoạn 4)
3. ❌ Chưa có UI → Cần Frontend (Giai đoạn 5)

---

## 🔧 DOCKERFILE ANALYSIS

### Go Dockerfile (Multi-stage)
```dockerfile
# Stage 1: Build (golang:1.21-alpine ~300MB)
FROM golang:1.21-alpine AS builder
# ... build binary ...

# Stage 2: Run (alpine:3.19 ~5MB)
FROM alpine:3.19
COPY --from=builder /app/main .
# Final image: ~15MB (chỉ chứa binary)
```

**Lợi ích:**
- Image nhẹ (15MB vs 300MB nếu dùng golang full)
- Không chứa compiler, source code → Bảo mật hơn

### Python Dockerfile
```dockerfile
FROM python:3.9-slim  # ~150MB (vs python:3.9 ~900MB)
```

**Lợi ích:**
- Slim image nhẹ hơn 6 lần
- Vẫn đủ dependencies cho Flask

---

## 📝 ĐIỂM THIẾU TRONG HƯỚNG DẪN

### Đã bổ sung
1. ✅ File `go.sum` (tự tạo khi build)
2. ✅ Hướng dẫn test DNS resolution
3. ✅ Hướng dẫn cleanup

### Cần lưu ý
1. ⚠️ Nên tạo `.dockerignore` để tránh copy file không cần thiết
2. ⚠️ Production nên dùng specific tag thay vì `latest`
3. ⚠️ Nên scan image bằng Trivy (sẽ làm ở Giai đoạn 12)

---

## 🎯 CHUẨN BỊ CHO GIAI ĐOẠN 3

Giai đoạn 3 sẽ:
- ✅ Sửa code Go để ghi dữ liệu ra file JSON
- ✅ Dùng Docker Volume mount thư mục
- ✅ Chứng minh dữ liệu không mất khi restart

---

**Kết luận:** Giai đoạn 2 hoàn thành! Đã Docker hóa thành công. Sẵn sàng sang Giai đoạn 3! ✅
