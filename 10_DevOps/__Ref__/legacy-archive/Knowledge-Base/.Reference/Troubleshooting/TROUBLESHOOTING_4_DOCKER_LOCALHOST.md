# Hướng Dẫn Xử Lý Lỗi: Kết Nối Bị Từ Chối (Connection Refused) do hiểu sai Localhost

Đây là lỗi tư duy phổ biến nhất khi mới làm quen với Docker.

## 1. Dấu hiệu nhận biết
Python App báo lỗi không thể kết nối tới Backend, dù bạn chắc chắn cả 2 đều đang chạy.
```json
{
  "error": "HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded... Connection refused"
}
```

## 2. Nguyên nhân
Trong code Python, bạn cấu hình URL backend là `http://localhost:8080`.
- Khi chạy trực tiếp trên máy Mac (không Docker): `localhost` chính là máy Mac. Go App chạy ở đó => Kết nối OK.
- **Khi chạy trong Docker (Container):**
  - `localhost` của container Python nghĩa là **chính cái container Python đó**.
  - Go App đang nằm ở một container khác (hoặc ở máy Host), không nằm trong container Python.
  - Python tìm Go ở trong bụng nó (localhost) -> Không thấy -> Lỗi.

## 3. Giải Pháp

### Cách 1: Dùng Docker Network (Chuẩn nhất)
Khi chạy 2 container trong cùng 1 Docker Network, chúng gọi nhau bằng **Tên Container** (Service Name).
- Code/Biến môi trường sửa thành: `http://go-container:8080`
- `go-container` là tên bạn đặt lúc `docker run --name go-container`.

### Cách 2: Gọi ra máy Host (Dùng host.docker.internal)
Nếu bạn muốn container Python chạy trong Docker gọi ra Go App chạy ở ngoài máy Mac (chưa đóng gói Docker).
- Docker cung cấp một tên miền đặc biệt: `host.docker.internal`.
- Code/Biến môi trường sửa thành: `http://host.docker.internal:8080`.
- Lúc này container sẽ đi "cửa sau" ra ngoài máy chủ để tìm cổng 8080.

### Tóm tắt quy tắc
1. **Container gọi Container (cùng network):** Dùng Tên Container.
2. **Container gọi Máy Host:** Dùng `host.docker.internal`.
3. **Máy Host gọi Container:** Dùng `localhost:PORT` (với điều kiện đã map port `-p`).
