# Hướng Dẫn Xử Lý Lỗi: Sai Kiến Trúc CPU (Exec Format Error)

Đây là lỗi kinh điển khi bạn dùng máy Mac chip Apple Silicon (M1, M2, M3...) để build Docker Image và đem sang chạy trên máy chủ Linux thông thường (Intel/AMD).

## 1. Dấu hiệu nhận biết
Trên máy Mac chạy thì ngon lành. Nhưng khi đem Image sang máy Ubuntu (hoặc máy khác) chạy lệnh `docker run`, container chết ngay lập tức và log báo:
```text
exec /app/backend: exec format error
```
Hoặc:
```text
standard_init_linux.go:228: exec user process caused: exec format error
```

## 2. Nguyên nhân
- **Chip Apple (M1/M2/M3)** chạy kiến trúc **ARM64**. Khi bạn gõ `docker build`, mặc định nó tạo ra Image dành cho ARM64.
- **Máy chủ (Server/VPS)** thường chạy chip Intel/AMD, kiến trúc **AMD64 (x86_64)**.
- Image của ARM64 không thể chạy trên máy AMD64 (giống như cài app iPhone lên Windows vậy).

## 3. Cách Kiểm Tra (Diagnosis)
Kiểm tra kiến trúc của Image bạn vừa build:
```bash
docker inspect my-go-backend:v1 | grep Architecture
```
- Nếu thấy: `"Architecture": "arm64"` (trong khi server là amd64) => **Lệch rồi!**

## 4. Giải Pháp (Build Multi-Platform)

Khi build trên máy Mac M-series để đem đi deploy, bạn buộc phải chỉ định rõ kiến trúc đích là `linux/amd64`.

**Sửa lệnh Build:**
Thêm tham số `--platform linux/amd64` vào lệnh build.

```bash
# Build lại Go App cho Server
docker build --platform linux/amd64 -t my-go-backend:linux .

# Build lại Python App cho Server
docker build --platform linux/amd64 -t my-py-frontend:linux .
```

*Lưu ý:* Khi thêm cờ này, quá trình build trên Mac sẽ lâu hơn một chút (do phải giả lập chip Intel), nhưng image tạo ra sẽ chạy được trên mọi máy chủ Linux phổ biến.
