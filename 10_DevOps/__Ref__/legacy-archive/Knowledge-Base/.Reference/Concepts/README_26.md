# 🎯 GIAI ĐOẠN 5: NGINX & WEB INTERFACE

## 📌 MÔ TẢ
Thư mục này chứa code từ **Giai đoạn 1-5**.
- **Giai đoạn 5: NGINX + Frontend (HTML/CSS/JS)** - Giao diện Web đẹp mắt!

Người dùng cuối giờ có thể dùng app qua trình duyệt, không cần cURL nữa!

## 🏗️ CẤU TRÚC

```
Stage05_Complete/
├── go-service/
├── python-service/
├── frontend/              # ← MỚI
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── nginx/                 # ← MỚI
│   └── conf.d/
│       └── default.conf
├── data/
├── docker-compose.yaml    # ← CẬP NHẬT: Thêm service 'web'
├── README.md
└── NOTES.md
```

## 🚀 CÁCH CHẠY

### Bước 1: Khởi động hệ thống
```bash
docker compose up -d
```

### Bước 2: Mở trình duyệt
Truy cập: **http://localhost**

Bạn sẽ thấy giao diện Web đẹp mắt với:
- ✅ Input để thêm TODO
- ✅ Danh sách TODO
- ✅ Nút xóa TODO
- ✅ Status indicator

## 🧪 TESTING

### Test 1: Giao diện Web
1. Mở http://localhost
2. Thấy giao diện màu tím gradient đẹp mắt
3. Status hiện "System Healthy ✅"

### Test 2: Thêm TODO qua Web
1. Gõ "Học DevOps Giai đoạn 5" vào ô input
2. Bấm nút "Thêm" (hoặc Enter)
3. TODO xuất hiện ngay lập tức trong danh sách

### Test 3: Xóa TODO
1. Bấm nút "🗑️" bên cạnh TODO
2. Confirm "Xóa công việc này?"
3. TODO biến mất

### Test 4: Kiểm tra API vẫn hoạt động
```bash
# Vẫn có thể dùng cURL
curl http://localhost/api/todos
```

### Test 5: Kiểm tra Reverse Proxy
```bash
# Request vào /api/ sẽ được NGINX chuyển sang Python
curl http://localhost/api/ping
```

### Test 6: F12 DevTools
1. Mở F12 → Network tab
2. Thêm TODO
3. Thấy request POST đến `/api/todos`
4. Response 201 Created

## 🏗️ KIẾN TRÚC 3-TIER

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP :80
┌──────▼──────┐
│    NGINX    │ ← Web Server + Reverse Proxy
└──────┬──────┘
       │
   ┌───┴────┐
   │        │
Static    /api/*
Files     │
   │      │
   │   ┌──▼──────┐
   │   │ Python  │ ← API Gateway
   │   └──┬──────┘
   │      │
   │   ┌──▼──────┐
   │   │   Go    │ ← Backend Logic
   │   └──┬──────┘
   │      │
   │   ┌──▼──────┐
   │   │  File   │ ← Data Storage
   │   └─────────┘
   │
┌──▼──────┐
│HTML/CSS │
│   /JS   │
└─────────┘
```

## 📊 LUỒNG HOẠT ĐỘNG

### 1. Load trang Web
```
Browser → http://localhost
  ↓
NGINX serve index.html
  ↓
Browser render HTML
  ↓
Browser load style.css, app.js
  ↓
app.js gọi fetch('/api/todos')
  ↓
(Tiếp luồng 2)
```

### 2. API Request
```
Browser → fetch('/api/todos')
  ↓
NGINX nhận request /api/todos
  ↓
NGINX proxy_pass → http://gateway:8080/api/todos
  ↓
Python nhận request
  ↓
Python gọi Go → http://backend:8081/todos
  ↓
Go trả data
  ↓
Python trả về Browser
  ↓
JavaScript update DOM
```

## ✅ CHECKLIST HOÀN THÀNH

- [ ] Tạo được frontend files (HTML/CSS/JS)
- [ ] Cấu hình được NGINX
- [ ] `docker compose up` chạy thành công
- [ ] Truy cập http://localhost thấy giao diện
- [ ] Thêm TODO qua Web thành công
- [ ] Xóa TODO thành công
- [ ] F12 thấy API calls
- [ ] Hiểu được Reverse Proxy

## 🔍 ĐIỂM HỌC ĐƯỢC

1. ✅ **NGINX Reverse Proxy:** Điều hướng request dựa trên path
2. ✅ **Static File Serving:** NGINX serve HTML/CSS/JS
3. ✅ **Frontend-Backend separation:** Frontend gọi API qua AJAX
4. ✅ **3-Tier Architecture:** Presentation - Logic - Data

## 🚧 VẤN ĐỀ CẦN GIẢI QUYẾT Ở GIAI ĐOẠN SAU

- ❌ File JSON không chuyên nghiệp → **Giai đoạn 6: MySQL**
- ❌ Deploy thủ công → **Giai đoạn 7-8: CI/CD**

## 📝 GHI CHÚ

Xem file `NOTES.md` để biết kết quả test thực tế.
