# 🎯 GIAI ĐOẠN 1: BARE-METAL - HOÀN CHỈNH

## 📌 MÔ TẢ
Thư mục này chứa code hoàn chỉnh cho **Giai đoạn 1: Bare-metal**.
Hai service (Go và Python) chạy trực tiếp trên máy, giao tiếp qua `localhost`.

## 🏗️ CẤU TRÚC

```
Stage01_Complete/
├── go-service/
│   ├── main.go           # Go backend service
│   ├── go.mod            # Go dependencies
│   └── go.sum            # (sẽ tự tạo khi chạy go mod tidy)
├── python-service/
│   ├── app.py            # Python gateway service
│   └── requirements.txt  # Python dependencies
├── README.md             # File này
└── NOTES.md              # Ghi chú kết quả test
```

## 🚀 CÁCH CHẠY

### Bước 1: Cài đặt dependencies

**Go Service:**
```bash
cd go-service
go mod tidy
```

**Python Service:**
```bash
cd python-service
pip install -r requirements.txt
# Hoặc dùng venv (khuyến nghị)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### Bước 2: Chạy Go Service (Terminal 1)
```bash
cd go-service
go run main.go
```

**Output mong đợi:**
```
[GIN-debug] POST   /ping
[GIN-debug] GET    /todos
[GIN-debug] POST   /todos
[GIN-debug] DELETE /todos/:id
[GIN-debug] Listening and serving HTTP on :8081
```

### Bước 3: Chạy Python Service (Terminal 2)
```bash
cd python-service
python app.py
```

**Output mong đợi:**
```
INFO - Starting Python Gateway Service on port 8080
 * Running on http://0.0.0.0:8080
```

## 🧪 TESTING

### Test 1: Ping (Kiểm tra kết nối)
```bash
curl http://localhost:8080/ping
```

**Kết quả mong đợi:**
```json
{
  "backend_response": {
    "from": "Go Service",
    "message": "pong",
    "time": "2024-01-01T10:00:00Z"
  },
  "gateway_message": "Hello from Python Gateway"
}
```

### Test 2: Tạo TODO
```bash
curl -X POST http://localhost:8080/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Học DevOps Giai đoạn 1"}'
```

**Kết quả mong đợi:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Học DevOps Giai đoạn 1",
  "completed": false,
  "created_at": "2024-01-01T10:00:00Z"
}
```

### Test 3: Xem danh sách TODO
```bash
curl http://localhost:8080/api/todos
```

**Kết quả mong đợi:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Học DevOps Giai đoạn 1",
    "completed": false,
    "created_at": "2026-01-25T16:41:00+07:00"
  }
]
```

### Test 4: Xóa TODO
```bash
# Thay YOUR_TODO_ID bằng ID thực tế từ Test 2
curl -X DELETE http://localhost:8080/api/todos/YOUR_TODO_ID
```

**Kết quả mong đợi:** HTTP 204 No Content (không có body)

### Test 5: Kiểm tra mất dữ liệu (Quan trọng!)
1. Tạo 1 TODO (Test 2)
2. Kiểm tra danh sách (Test 3) → Thấy 1 TODO
3. **Tắt Go Service** (Ctrl+C ở Terminal 1)
4. **Bật lại Go Service** (`go run main.go`)
5. Kiểm tra lại danh sách (Test 3) → **Danh sách rỗng `[]`**

**Kết luận:** Dữ liệu lưu trong RAM → Restart thì mất.

## ✅ CHECKLIST HOÀN THÀNH

- [ ] Go service chạy được trên port 8081
- [ ] Python service chạy được trên port 8080
- [ ] Test Ping thành công
- [ ] Tạo TODO thành công
- [ ] Xem danh sách TODO thành công
- [ ] Xóa TODO thành công
- [ ] Đã kiểm chứng dữ liệu mất khi restart

## 🔍 ĐIỂM HỌC ĐƯỢC

1. ✅ Hiểu cách 2 service giao tiếp qua HTTP
2. ✅ Biết sự khác biệt giữa `localhost` trong context khác nhau
3. ✅ Nhận ra vấn đề của việc lưu dữ liệu trong RAM
4. ✅ Thành thạo cURL để test API

## 🚧 VẤN ĐỀ CẦN GIẢI QUYẾT Ở GIAI ĐOẠN SAU

- ❌ Dữ liệu mất khi restart → **Giai đoạn 3: Docker Volume**
- ❌ Phụ thuộc môi trường máy cá nhân → **Giai đoạn 2: Docker**
- ❌ Gõ lệnh thủ công phức tạp → **Giai đoạn 4: Docker Compose**

## 📝 GHI CHÚ

Xem file `NOTES.md` để biết kết quả test thực tế và các lỗi gặp phải (nếu có).
