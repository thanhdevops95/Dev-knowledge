# 🎯 GIAI ĐOẠN 3: DOCKER VOLUME - PERSISTENCE

## 📌 MÔ TẢ
Thư mục này chứa code từ **Giai đoạn 1 + 2 + 3**.
- Giai đoạn 1-2: Code + Docker
- **Giai đoạn 3: File persistence + Docker Volume**

Dữ liệu giờ được lưu vào file JSON và mount ra ngoài host → **Không mất khi restart!**

## 🏗️ CẤU TRÚC

```
Stage03_Complete/
├── go-service/
│   ├── main.go           # ← CẬP NHẬT: Thêm loadTodos(), saveTodos()
│   ├── go.mod
│   ├── go.sum
│   └── Dockerfile
├── python-service/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── data/                 # ← MỚI: Thư mục lưu db.json
│   └── (db.json sẽ tự tạo)
├── README.md
└── NOTES.md
```

## 🚀 CÁCH CHẠY

### Bước 1: Build Images (nếu chưa có)

```bash
cd go-service
docker build -t todo-go:v2 .

cd ../python-service
docker build -t todo-python:v1 .
```

### Bước 2: Tạo Network

```bash
docker network create todo-net
```

### Bước 3: Chạy với Volume Mount

**Chạy Go Container (với Volume):**
```bash
docker run -d \
  --name go-app \
  --network todo-net \
  -v $(pwd)/data:/app/data \
  todo-go:v2
```

**Giải thích:**
- `-v $(pwd)/data:/app/data`: Mount thư mục `data` (host) vào `/app/data` (container)
- `$(pwd)`: Đường dẫn hiện tại (macOS/Linux)
- Windows PowerShell: dùng `${PWD}/data`
- Windows CMD: dùng đường dẫn tuyệt đối `C:\path\to\data`

**Chạy Python Container:**
```bash
docker run -d \
  --name python-app \
  --network todo-net \
  -p 5000:8080 \
  -e GO_HOST=go-app \
  todo-python:v1
```

## 🧪 TESTING - MAGIC MOMENT!

### Test 1: Tạo dữ liệu
```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Dữ liệu này BẤT TỬ!"}'
```

### Test 2: Kiểm tra file trên máy thật
```bash
# Xem file db.json đã xuất hiện
ls -la data/

# Xem nội dung
cat data/db.json
```

**Kết quả mong đợi:** Thấy file JSON chứa TODO vừa tạo! 🎉

### Test 3: HỦY DIỆT Container (Chaos Test)
```bash
# Xóa hoàn toàn container
docker rm -f go-app

# Kiểm tra file vẫn còn trên máy
cat data/db.json
# → Vẫn còn!
```

### Test 4: HỒI SINH (Resurrection)
```bash
# Chạy lại container mới (nhớ mount volume)
docker run -d \
  --name go-app \
  --network todo-net \
  -v $(pwd)/data:/app/data \
  todo-go:v2
```

### Test 5: Kiểm tra dữ liệu
```bash
curl http://localhost:5000/api/todos
```

**Kết quả:** ✅ Vẫn thấy "Dữ liệu này BẤT TỬ!" 

→ **THÀNH CÔNG!** Dữ liệu đã sống sót qua cái chết của container! 🎊

## 🔬 PHÂN TÍCH

### Luồng hoạt động

```
1. User tạo TODO
   ↓
2. Python forward → Go
   ↓
3. Go lưu vào RAM (map)
   ↓
4. Go gọi saveTodos()
   ↓
5. Ghi file /app/data/db.json (trong container)
   ↓
6. Docker Volume mount → File xuất hiện ở ./data/db.json (host)
   ↓
7. Container chết → File vẫn còn trên host
   ↓
8. Container mới khởi động → loadTodos() đọc file → Phục hồi dữ liệu
```

### So sánh Giai đoạn 2 vs 3

| Tiêu chí | Giai đoạn 2 | Giai đoạn 3 |
|----------|-------------|-------------|
| **Lưu trữ** | RAM only | RAM + File |
| **Restart** | Mất data | **Giữ data** ✅ |
| **Volume** | Không | Có (Bind Mount) |
| **File location** | Trong container | Host + Container |

## ✅ CHECKLIST HOÀN THÀNH

- [ ] Build được image v2 (có persistence code)
- [ ] Chạy container với volume mount
- [ ] Tạo TODO và thấy file db.json xuất hiện
- [ ] Xóa container và file vẫn còn
- [ ] Chạy container mới và dữ liệu phục hồi
- [ ] Hiểu được cơ chế Bind Mount

## 🔍 ĐIỂM HỌC ĐƯỢC

1. ✅ **Docker Volume (Bind Mount):** Ánh xạ thư mục host ↔ container
2. ✅ **Persistence:** Dữ liệu sống sót qua lifecycle của container
3. ✅ **File I/O trong Go:** `ioutil.ReadFile`, `WriteFile`, `json.Marshal`
4. ✅ **Startup logic:** Load data khi app khởi động

## 🚧 VẤN ĐỀ CẦN GIẢI QUYẾT Ở GIAI ĐOẠN SAU

- ❌ Lệnh docker run vẫn dài → **Giai đoạn 4: Docker Compose**
- ❌ File JSON không scale được → **Giai đoạn 6: MySQL**

## 📝 GHI CHÚ

Xem file `NOTES.md` để biết kết quả test thực tế.
