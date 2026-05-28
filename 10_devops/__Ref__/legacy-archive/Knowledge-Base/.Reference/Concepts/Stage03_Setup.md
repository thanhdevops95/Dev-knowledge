# 🛠️ GIAI ĐOẠN 3: CHUẨN BỊ THƯ MỤC DỮ LIỆU (VOLUME)

## 📌 MỤC TIÊU
Trong giai đoạn này, chúng ta sẽ map (ánh xạ) một thư mục từ máy thật vào trong Docker Container để lưu giữ dữ liệu. Vì vậy, ta cần chuẩn bị sẵn thư mục đó.

---

## 1. TẠO THƯ MỤC DATA

Tại thư mục gốc của dự án `Todo-App-DevOps`, chạy các lệnh sau:

### 🪟 Windows / 🍎 macOS / 🐧 Linux
```bash
# Đảm bảo bạn đang ở thư mục gốc của dự án
cd Todo-App-DevOps

# Tạo thư mục data
mkdir data

# Kiểm tra
ls -F
# Thấy folder data/ là ok
```

## 2. KIỂM TRA QUYỀN TRUY CẬP (LINUX/MAC)
Nếu bạn dùng Linux, đôi khi Docker container không có quyền ghi vào thư mục của user. Hãy cấp quyền "thoải mái" một chút cho folder này (chỉ cho môi trường học tập dev).

```bash
chmod 777 data
```

---

## ✅ CHECKLIST
- Đã có thư mục `Todo-App-DevOps/data/`.
- Thư mục này hiện tại **đang rỗng**.

Sẵn sàng sang Giai đoạn 3 để cứu dữ liệu!
