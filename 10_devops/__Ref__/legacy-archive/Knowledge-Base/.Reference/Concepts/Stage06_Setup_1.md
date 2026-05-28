# 🛠️ GIAI ĐOẠN 6: CHUẨN BỊ MYSQL CLIENT

## 📌 MỤC TIÊU
Trong giai đoạn này, chúng ta thay hệ thống lưu file bằng Database MySQL. Để kiểm tra dữ liệu trong DB, bạn cần cài một tool quản lý DB.

---

## 1. CÀI ĐẶT DB CLIENT (DBEAVER)

**DBeaver** là công cụ miễn phí, mạnh mẽ, hỗ trợ mọi loại DB.

### Tải và cài đặt
- Truy cập: [dbeaver.io/download](https://dbeaver.io/download/)
- Tải phiên bản **Community Edition**.
- Cài đặt như phần mềm bình thường.

### (Alternative) VS Code Extensions
Nếu lười cài app riêng, bạn có thể cài extension **"MySQL"** hoặc **"Database Client"** ngay trong VS Code.

---

## 2. CHUẨN BỊ THƯ MỤC DB
Chúng ta cần một chỗ để MySQL lưu dữ liệu của nó (để khi container MySQL restart không bị mất data).

```bash
cd Todo-App-DevOps
mkdir -p mysql-data
```

## ✅ CHECKLIST
- Đã có DBeaver (hoặc tool tương đương).
- Đã có folder `mysql-data/`.

Sẵn sàng "chuyên nghiệp hóa" hệ thống lưu trữ!
