# 📝 GHI CHÚ GIAI ĐOẠN 1

## ✅ TRẠNG THÁI: HOÀN THÀNH & TESTED

**Môi trường:** macOS/Windows/Linux

---

## 🧪 KẾT QUẢ TEST

### ✅ Test 1: Khởi động services
- **Go Service:** ✅ Chạy thành công trên port 8081
- **Python Service:** ✅ Chạy thành công trên port 8080
- **Thời gian khởi động:** < 2 giây

### ✅ Test 2: Ping connectivity
```bash
$ curl http://localhost:8080/ping
```
**Kết quả:** ✅ PASS
- Python nhận request
- Python gọi được Go qua `localhost:8081`
- Nhận được response từ Go

### ✅ Test 3: CRUD Operations
| Operation | Endpoint | Status | Note |
|-----------|----------|--------|------|
| Create TODO | POST /api/todos | ✅ 201 | UUID tự động tạo |
| Get All | GET /api/todos | ✅ 200 | Trả về array |
| Delete TODO | DELETE /api/todos/:id | ✅ 204 | No content |
| Get non-exist | GET /api/todos/invalid | ✅ 404 | Error handling OK |

### ✅ Test 4: Data Persistence (RAM)
**Kịch bản:**
1. Tạo 3 TODO items
2. Verify có 3 items
3. Restart Go service
4. Check lại → **Kết quả: `[]` (rỗng)**

**Kết luận:** ✅ Đã chứng minh dữ liệu lưu RAM sẽ mất khi restart.

---

## 🐛 LỖI GẶP PHẢI & CÁCH XỬ LÝ

### Lỗi 1: `go: command not found`
**Nguyên nhân:** Go chưa cài hoặc chưa có trong PATH  
**Giải pháp:** Cài Go theo `Course_Content/Stage01_Setup.md`

### Lỗi 2: `ModuleNotFoundError: No module named 'flask'`
**Nguyên nhân:** Chưa cài Flask  
**Giải pháp:** `pip install -r requirements.txt`

### Lỗi 3: `port 8080 already in use`
**Nguyên nhân:** Có process khác đang dùng port  
**Giải pháp:**
```bash
# macOS/Linux
lsof -i :8080
kill -9 [PID]

# Windows
netstat -ano | findstr :8080
taskkill /PID [PID] /F
```

### Lỗi 4: `Connection refused` khi Python gọi Go
**Nguyên nhân:** Go service chưa chạy  
**Giải pháp:** Đảm bảo Go service đã chạy trước khi start Python

---

## 📊 METRICS

- **Tổng số files:** 5
- **Lines of Code:**
  - Go: ~150 lines
  - Python: ~180 lines
- **Dependencies:**
  - Go: 3 packages (gin, cors, uuid)
  - Python: 3 packages (flask, flask-cors, requests)
- **API Endpoints:** 4 (ping, get todos, create todo, delete todo)

---

## 💡 BÀI HỌC RÚT RA

### 1. Ưu điểm của Bare-metal
- ✅ Đơn giản, dễ debug
- ✅ Không cần cài Docker
- ✅ Phù hợp cho học tập ban đầu

### 2. Nhược điểm
- ❌ Phụ thuộc môi trường (Python/Go version khác nhau)
- ❌ Dữ liệu mất khi restart
- ❌ Khó triển khai lên nhiều máy
- ❌ Conflict port dễ xảy ra

### 3. Điểm cần cải thiện ở giai đoạn sau
- 🔄 Containerize để "chạy đâu cũng được" (Giai đoạn 2)
- 💾 Persistent storage (Giai đoạn 3)
- 🎼 Orchestration dễ dàng hơn (Giai đoạn 4)

---

## 🔗 LIÊN KẾT

- **Hướng dẫn:** `Course_Content/Stage01_BareMetal.md`
- **Setup:** `Course_Content/Stage01_Setup.md`
- **Troubleshooting:** `Course_Content/Troubleshooting_Guide.md`

---

## ✏️ GHI CHÚ BỔ SUNG

### Điểm thiếu trong hướng dẫn (cần bổ sung)
1. ⚠️ Chưa có hướng dẫn tạo file `go.sum` (cần chạy `go mod tidy`)
2. ⚠️ Chưa đề cập đến việc dùng Virtual Environment cho Python
3. ✅ Đã có đầy đủ error handling
4. ✅ Code đã có comment chi tiết

### Đề xuất cải tiến
- [ ] Thêm endpoint GET /todos/:id (lấy 1 TODO cụ thể)
- [ ] Thêm endpoint PUT /todos/:id (update TODO)
- [ ] Thêm validation chi tiết hơn (title max length, etc.)
- [ ] Thêm logging vào file thay vì chỉ console

---

**Kết luận:** Giai đoạn 1 hoàn thành tốt, code chạy ổn định, sẵn sàng chuyển sang Giai đoạn 2! ✅
