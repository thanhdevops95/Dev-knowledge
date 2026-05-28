# 🎯 GIAI ĐOẠN 6: MYSQL DATABASE

## 📌 MÔ TẢ
Thư mục này chứa code từ **Giai đoạn 1-6**.
- **Giai đoạn 6: MySQL Database** - Thay file JSON bằng Database thực thụ!

Dữ liệu giờ được lưu trong MySQL, chuyên nghiệp và có thể scale.

## 🏗️ CẤU TRÚC MỚI

```
Stage06_Complete/
├── go-service/
│   ├── main.go           # ← CẬP NHẬT: SQL queries thay vì file I/O
│   ├── go.mod            # ← CẬP NHẬT: Thêm mysql driver
│   └── Dockerfile
├── python-service/
├── frontend/
├── nginx/
├── mysql-data/           # ← MỚI: MySQL data volume
├── docker-compose.yaml   # ← CẬP NHẬT: Thêm service 'db'
├── README.md
└── NOTES.md
```

## 🚀 CÁCH CHẠY

### Bước 1: Khởi động (MySQL cần 10-20s)
```bash
docker compose up -d
```

### Bước 2: Xem log MySQL khởi động
```bash
docker compose logs -f db
# Đợi thấy "ready for connections"
```

### Bước 3: Truy cập Web
http://localhost

## 🧪 TESTING

### Test 1: Kiểm tra MySQL
```bash
# Vào MySQL container
docker exec -it mysql-db mysql -u root -psecret

# Trong MySQL shell
USE todo_db;
SHOW TABLES;
# Thấy bảng 'todos'

SELECT * FROM todos;
# Ban đầu rỗng

EXIT;
```

### Test 2: Tạo TODO qua Web
1. Mở http://localhost
2. Thêm TODO: "MySQL hoạt động!"
3. Vào MySQL kiểm tra:
```bash
docker exec -it mysql-db mysql -u root -psecret -e "SELECT * FROM todo_db.todos;"
```
→ Thấy dữ liệu trong database!

### Test 3: Persistence Test (Quan trọng!)
```bash
# Tạo vài TODO
# Sau đó restart toàn bộ hệ thống
docker compose down
docker compose up -d

# Kiểm tra lại
curl http://localhost/api/todos
```
→ ✅ Dữ liệu vẫn còn! (Nhờ MySQL volume)

### Test 4: So sánh với Giai đoạn 3
| Tiêu chí | Giai đoạn 3 (File JSON) | Giai đoạn 6 (MySQL) |
|----------|------------------------|---------------------|
| **Lưu trữ** | File JSON | MySQL Database |
| **Concurrency** | ❌ Race condition | ✅ ACID transactions |
| **Query** | ❌ Load toàn bộ file | ✅ SQL queries |
| **Scale** | ❌ Không scale | ✅ Scale được |
| **Backup** | Copy file | MySQL dump |

## 📊 KIẾN TRÚC 4-TIER

```
Browser
   ↓
NGINX (Web + Proxy)
   ↓
Python (Gateway)
   ↓
Go (Business Logic)
   ↓
MySQL (Data Storage) ← MỚI
```

## ✅ CHECKLIST

- [ ] MySQL container chạy thành công
- [ ] Go kết nối được MySQL
- [ ] Tạo TODO và thấy trong database
- [ ] Restart hệ thống và data vẫn còn
- [ ] Hiểu được lợi ích của Database

## 🔍 ĐIỂM HỌC ĐƯỢC

1. ✅ **MySQL trong Docker:** Dễ dàng setup database
2. ✅ **SQL Driver trong Go:** `database/sql` package
3. ✅ **Connection Retry:** Xử lý MySQL khởi động chậm
4. ✅ **Health Check:** `depends_on` với `condition`
5. ✅ **Volume cho Database:** Persistent data

## 🚧 TIẾP THEO

- Giai đoạn 7-8: **CI/CD** - Tự động build & deploy
- Giai đoạn 9: **Kubernetes** - Orchestration quy mô lớn

## 📝 GHI CHÚ

Xem file `NOTES.md` để biết chi tiết.
