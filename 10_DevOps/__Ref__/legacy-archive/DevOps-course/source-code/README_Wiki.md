# The Counter App - README

## 📖 Giới thiệu

**The Counter App** là ứng dụng demo đơn giản dùng xuyên suốt khóa học DevOps Zero to Hero.

### Công nghệ sử dụng

- **Backend**: Flask (Python Web Framework)
- **Database**: Redis (In-memory key-value store)
- **Container**: Docker + Docker Compose

---

## 🚀 Cách chạy

### Option 1: Chạy local (cần Python + Redis)

```bash
# Cài dependencies
pip install -r requirements.txt

# Chạy Redis (terminal riêng)
redis-server

# Chạy Flask app
python app.py
```

Truy cập: <http://localhost:5000>

### Option 2: Chạy bằng Docker Compose (Khuyến nghị)

```bash
# Build và start tất cả services
docker-compose up --build

# Hoặc chạy ở background
docker-compose up -d --build
```

Truy cập: <http://localhost:5000>

### Dừng ứng dụng

```bash
docker-compose down

# Xóa cả volumes (mất data)
docker-compose down -v
```

---

## 🧪 Testing

### Kiểm tra Sức khỏe Hệ thống

```bash
curl http://localhost:5000/health
```

Kết quả mong đợi:

```json
{
  "status": "healthy",
  "redis": "connected"
}
```

### Test chức năng

1. Mở <http://localhost:5000>
2. Click "➕ Tăng" → Số đếm tăng lên
3. Click "🔄 Reset" → Số đếm về 0
4. Restart container → Data vẫn còn (nhờ volume)

---

## 📁 Cấu trúc Files

```
source-code/
├── app.py                 # Flask application chính
├── Dockerfile             # Hướng dẫn build Docker image
├── docker-compose.yml     # Orchestration file
├── requirements.txt       # Python dependencies
└── README.md              # File này
```

---

## 🔧 Biến môi trường

| Tên biến | Mặc định | Mô tả |
|----------|----------|-------|
| `REDIS_HOST` | `localhost` | Hostname của Redis server |
| `REDIS_PORT` | `6379` | Port của Redis |

---

## 🎯 Mục đích học tập

Ứng dụng này sẽ được dùng để thực hành:

- **Module 01 (PLAN)**: Thiết kế kiến trúc, requirements
- **Module 02 (BUILD)**: Đóng gói với Docker, Git
- **Module 03 (CI)**: Tự động test & build với GitHub Actions
- **Module 04 (CD)**: Deploy lên Kubernetes
- **Module 05 (OPERATE)**: Quản lý infrastructure với Terraform
- **Module 06 (MONITOR)**: Theo dõi metrics với Prometheus/Grafana
- **Module 07 (FEEDBACK)**: Alerting & Incident Response

---

## 📝 Notes

- App dùng Redis để persist data (không lưu trong memory)
- Có health check endpoint `/health` cho monitoring
- UI responsive, có animation đơn giản
- Code có comment chi tiết để dễ hiểu

---

**Happy Learning! 🚀**
