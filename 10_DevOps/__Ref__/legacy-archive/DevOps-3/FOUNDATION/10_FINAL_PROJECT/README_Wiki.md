# Module 10: DỰ ÁN TỐT NGHIỆP - DevOps Portfolio

> **"Áp dụng mọi thứ đã học - Xây dựng ứng dụng production-ready!"**

---

## 📚 MỤC LỤC

1. [Tổng quan dự án](#1-tổng-quan-dự-án)
2. [Yêu cầu](#2-yêu-cầu)
3. [Kiến trúc hệ thống](#3-kiến-trúc-hệ-thống)
4. [Các bước triển khai](#4-các-bước-triển-khai)
5. [Sản phẩm bàn giao](#5-sản-phẩm-bàn-giao)
6. [Thang điểm đánh giá](#6-thang-điểm-đánh-giá)
7. [Nâng cao thêm](#7-nâng-cao-thêm)
8. [Tổng kết](#8-tổng-kết)

---

## 1. Tổng Quan Dự Án

### **Xây dựng & Triển khai: Task Manager Full-Stack**

**Bạn sẽ xây dựng:**

- Ứng dụng web hoàn chỉnh (frontend + backend)
- Đóng gói trong Docker containers
- Tự động triển khai qua CI/CD pipeline
- Phục vụ thông qua NGINX reverse proxy
- Có giám sát (monitoring) và ghi log (logging)
- Sẵn sàng cho production!

**Công nghệ sử dụng:**

| Thành phần | Công nghệ |
|------------|-----------|
| Backend | Python Flask hoặc Node.js Express |
| Frontend | HTML/CSS/JavaScript |
| Cơ sở dữ liệu | PostgreSQL |
| Cache | Redis |
| Web Server | NGINX |
| Container | Docker & Docker Compose |
| CI/CD | GitHub Actions |
| Triển khai | VPS hoặc Cloud server |

---

## 2. Yêu Cầu

### 2.1. Yêu cầu chức năng (Functional Requirements)

**Tính năng ứng dụng:**

1. ✅ Xác thực người dùng (đăng nhập/đăng ký)
2. ✅ Tạo/Xem/Sửa/Xóa task (CRUD operations)
3. ✅ Đánh dấu task hoàn thành/chưa hoàn thành
4. ✅ Lọc task (tất cả/đang làm/hoàn thành)
5. ✅ REST API endpoints đầy đủ
6. ✅ Giao diện responsive trên mọi thiết bị

**Yêu cầu kỹ thuật:**

1. ✅ Đóng gói bằng Docker
2. ✅ Multi-container setup (app, db, redis, nginx)
3. ✅ Quản lý biến môi trường (environment variables)
4. ✅ Health check endpoints
5. ✅ Logging được triển khai
6. ✅ CI/CD pipeline hoạt động
7. ✅ Zero-downtime deployment
8. ✅ HTTPS đã bật

### 2.2. Yêu cầu DevOps

**Bắt buộc phải có:**

- [x] Version control với Git
- [x] Dockerfile được tối ưu
- [x] docker-compose.yml cho development
- [x] docker-compose.prod.yml cho production
- [x] GitHub Actions CI/CD
- [x] NGINX reverse proxy
- [x] SSL certificate (Let's Encrypt)
- [x] Health monitoring
- [x] Logging vào file
- [x] Dùng environment variables (không hardcode secrets!)

---

## 3. Kiến Trúc Hệ Thống

### 3.1. Sơ đồ kiến trúc

```
Internet (Người dùng)
         ↓
    HTTPS (port 443)
         ↓
    NGINX (reverse proxy + SSL termination)
         ↓
┌─────────────────────────────────────┐
│      Docker Compose Network         │
│                                     │
│  ┌──────────────┐   ┌───────────┐  │
│  │   Flask App  │   │   Redis   │  │
│  │   (port 5000)│←→ │   Cache   │  │
│  └──────┬───────┘   └───────────┘  │
│         │                           │
│         ↓                           │
│  ┌──────────────┐                  │
│  │  PostgreSQL  │                  │
│  │  (port 5432) │                  │
│  └──────────────┘                  │
└─────────────────────────────────────┘
```

**Giải thích:**

1. **Người dùng** truy cập qua HTTPS
2. **NGINX** nhận request, xử lý SSL, forward tới Flask
3. **Flask App** xử lý logic, lưu data vào PostgreSQL
4. **Redis** cache để tăng tốc
5. Tất cả chạy trong **Docker network** riêng

### 3.2. Cấu trúc thư mục dự án

```
task-manager/
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # Pipeline CI/CD
├── app/
│   ├── main.py                 # Ứng dụng Flask chính
│   ├── models.py               # Database models
│   ├── templates/              # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   └── login.html
│   ├── static/                 # CSS, JS, images
│   │   ├── style.css
│   │   └── app.js
│   └── requirements.txt        # Python dependencies
├── nginx/
│   └── nginx.conf              # Cấu hình NGINX
├── Dockerfile                  # Build image cho app
├── docker-compose.yml          # Chạy local development
├── docker-compose.prod.yml     # Chạy production
├── .env.example                # Template biến môi trường
├── .gitignore
└── README.md                   # Tài liệu dự án
```

---

## 4. Các Bước Triển Khai

### Bước 1: Phát triển ứng dụng Flask

**Tạo file `app/main.py`:**

```python
# app/main.py - Ứng dụng Flask chính
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Lấy cấu hình từ environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')

db = SQLAlchemy(app)

# Model cho Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

# Trang chủ
@app.route('/')
def index():
    return render_template('index.html')

# API endpoints
@app.route('/api/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        # Tạo task mới
        data = request.json
        task = Task(title=data['title'])
        db.session.add(task)
        db.session.commit()
        return jsonify({'id': task.id, 'message': 'Đã tạo task!'}), 201
    
    # Lấy danh sách tasks
    tasks = Task.query.all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'completed': t.completed
    } for t in tasks])

# Health check endpoint - rất quan trọng cho DevOps!
@app.route('/health')
def health():
    try:
        # Kiểm tra kết nối database
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**Giải thích code:**

- `os.getenv()` = Lấy biến môi trường, không hardcode
- `Task` model = Bảng trong database
- `/api/tasks` = RESTful API endpoint
- `/health` = DevOps dùng để kiểm tra app còn sống không

---

### Bước 2: Đóng gói Docker

**Tạo `Dockerfile`:**

```dockerfile
# Sử dụng Python image nhỏ gọn
FROM python:3.9-slim

# Thư mục làm việc trong container
WORKDIR /app

# Copy và cài dependencies trước (tận dụng Docker cache)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app/ .

# Không chạy với root user (bảo mật!)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Port mà app lắng nghe
EXPOSE 5000

# Health check tự động
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

# Lệnh khởi động với Gunicorn (production-ready)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
```

**Giải thích:**

- `FROM python:3.9-slim` = Base image nhỏ (~40MB thay vì 900MB)
- Copy `requirements.txt` trước = Tận dụng cache, build nhanh hơn
- `USER appuser` = Không chạy root, bảo mật hơn
- `HEALTHCHECK` = Docker tự kiểm tra container có healthy

---

### Bước 3: Docker Compose cho Development

**Tạo `docker-compose.yml`:**

```yaml
version: '3.8'

services:
  # Ứng dụng chính
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/taskdb
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=dev-secret-key
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app  # Hot reload khi dev
    networks:
      - app-network

  # PostgreSQL Database
  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: taskdb
    volumes:
      - db-data:/var/lib/postgresql/data  # Persist data
    networks:
      - app-network

  # Redis Cache
  redis:
    image: redis:6-alpine
    networks:
      - app-network

# Lưu trữ persistent
volumes:
  db-data:

# Network riêng cho các services
networks:
  app-network:
```

**Chạy development:**

```bash
# Khởi động tất cả services
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng
docker-compose down
```

---

### Bước 4: CI/CD Pipeline

**Tạo `.github/workflows/ci-cd.yml`:**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  # Job 1: Chạy tests
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Cài dependencies
        run: |
          pip install -r app/requirements.txt
          pip install pytest
      
      - name: Chạy tests
        run: pytest tests/

  # Job 2: Build Docker image
  build:
    needs: test  # Chỉ chạy nếu test pass
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t task-manager:${{ github.sha }} .
      
      - name: Đăng nhập Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Push lên Docker Hub
        run: |
          docker tag task-manager:${{ github.sha }} ${{ secrets.DOCKER_USERNAME }}/task-manager:latest
          docker push ${{ secrets.DOCKER_USERNAME }}/task-manager:latest

  # Job 3: Deploy lên server
  deploy:
    needs: build  # Chỉ chạy nếu build thành công
    if: github.ref == 'refs/heads/main'  # Chỉ deploy từ main branch
    runs-on: ubuntu-latest
    steps:
      - name: Deploy qua SSH
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /var/www/task-manager
            docker-compose pull
            docker-compose down
            docker-compose up -d
            
            # Đợi rồi kiểm tra health
            sleep 10
            curl -f http://localhost/health || exit 1
            echo "Deploy thành công!"
```

**Giải thích pipeline:**

1. **Test** → Nếu fail thì dừng ngay
2. **Build** → Tạo Docker image, push lên registry
3. **Deploy** → SSH vào server, pull và restart containers

---

### Bước 5: Cấu hình NGINX

**Tạo `nginx/nginx.conf`:**

```nginx
# Cấu hình NGINX cho production

# HTTP → Redirect sang HTTPS
server {
    listen 80;
    server_name taskmanager.yourname.com;
    
    # Redirect tất cả HTTP sang HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS server chính
server {
    listen 443 ssl http2;
    server_name taskmanager.yourname.com;
    
    # SSL certificates từ Let's Encrypt
    ssl_certificate /etc/letsencrypt/live/taskmanager.yourname.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/taskmanager.yourname.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Serve static files trực tiếp (nhanh hơn!)
    location /static {
        alias /var/www/task-manager/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Proxy tới Flask app
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Health check endpoint
    location /health {
        proxy_pass http://127.0.0.1:5000/health;
    }
}
```

---

### Bước 6: Triển khai Production

**Trên server VPS:**

```bash
# 1. Clone repository
git clone https://github.com/yourname/task-manager.git
cd task-manager

# 2. Tạo file .env từ template
cp .env.example .env
nano .env  # Điền các giá trị production

# 3. Khởi động containers
docker-compose -f docker-compose.prod.yml up -d

# 4. Cài đặt NGINX
sudo cp nginx/nginx.conf /etc/nginx/sites-available/taskmanager
sudo ln -s /etc/nginx/sites-available/taskmanager /etc/nginx/sites-enabled/
sudo nginx -t  # Kiểm tra syntax
sudo systemctl reload nginx

# 5. Lấy SSL certificate miễn phí
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d taskmanager.yourname.com

# 6. Verify
curl https://taskmanager.yourname.com/health
```

---

## 5. Sản Phẩm Bàn Giao

### 5.1. Repository trên GitHub

**Bắt buộc có:**

- ✅ Source code hoàn chỉnh
- ✅ Dockerfile đã tối ưu
- ✅ docker-compose files (dev + prod)
- ✅ CI/CD configuration
- ✅ README.md tài liệu đầy đủ

### 5.2. Ứng dụng đang chạy

**URL:** `https://taskmanager.yourname.com`

**Kiểm tra:**

- ✅ Truy cập được qua HTTPS
- ✅ Tất cả chức năng hoạt động
- ✅ Response time nhanh (< 500ms)
- ✅ Không có lỗi trong console

### 5.3. Tài liệu README.md

**Phải bao gồm:**

1. Mô tả dự án
2. Công nghệ sử dụng
3. Sơ đồ kiến trúc
4. Hướng dẫn cài đặt local
5. Hướng dẫn triển khai
6. API documentation
7. Screenshots
8. Các thách thức gặp phải và cách giải quyết

---

## 6. Thang Điểm Đánh Giá

**Tổng: 100 điểm**

### Ứng dụng (30 điểm)

| Tiêu chí | Điểm |
|----------|------|
| CRUD hoạt động đầy đủ | 10 |
| Xác thực người dùng | 10 |
| Giao diện responsive | 5 |
| Xử lý lỗi tốt | 5 |

### Docker & Compose (20 điểm)

| Tiêu chí | Điểm |
|----------|------|
| Dockerfile tối ưu | 5 |
| Multi-container setup | 10 |
| Volume management | 5 |

### CI/CD (20 điểm)

| Tiêu chí | Điểm |
|----------|------|
| Automated tests | 5 |
| Automated build | 5 |
| Automated deployment | 10 |

### Production Setup (20 điểm)

| Tiêu chí | Điểm |
|----------|------|
| NGINX cấu hình đúng | 5 |
| HTTPS hoạt động | 5 |
| Environment variables | 5 |
| Health checks | 5 |

### Tài liệu (10 điểm)

| Tiêu chí | Điểm |
|----------|------|
| README rõ ràng | 5 |
| Sơ đồ kiến trúc | 3 |
| API documentation | 2 |

**Đạt:** ≥ 70/100 điểm

---

## 7. Nâng Cao Thêm

**Các tính năng tùy chọn để điểm cộng:**

- [ ] JWT authentication
- [ ] Real-time updates (WebSockets)
- [ ] Monitoring dashboard (Prometheus + Grafana)
- [ ] Auto-scaling
- [ ] Kubernetes deployment
- [ ] Automated database backups
- [ ] Performance testing
- [ ] Security scanning (vulnerability check)

---

## 8. Tổng Kết

### 🎉 CHÚC MỪNG BẠN

**Bạn đã hoàn thành Foundation Track!**

**Kỹ năng đã master:**

- ✅ Linux command line
- ✅ Git & GitHub
- ✅ Networking cơ bản
- ✅ HTML/CSS/JavaScript
- ✅ Docker containerization
- ✅ CI/CD automation
- ✅ Web servers (NGINX)
- ✅ Production deployment
- ✅ Monitoring & logging

### 📚 Tiếp theo là gì?

**Advanced Track sẽ dạy:**

- Kubernetes orchestration
- Infrastructure as Code (Terraform)
- CI/CD nâng cao (Jenkins, ArgoCD, GitOps)
- Cloud platforms (AWS, Azure, GCP)
- Observability (Prometheus, Grafana, ELK)
- Security & DevSecOps

### 🎓 Bạn giờ là

**Junior DevOps Engineer** - Sẵn sàng cho các vị trí entry-level! 🚀

---

<div align="center">

# 🎉 FOUNDATION TRACK HOÀN THÀNH! 🎉

**Bạn đã làm được! Từ zero đến DevOps trong 10 modules!**

**Giờ hãy build project và bắt đầu sự nghiệp! 💪**

**Hành trình DevOps tiếp tục ở ADVANCED track!**

</div>
