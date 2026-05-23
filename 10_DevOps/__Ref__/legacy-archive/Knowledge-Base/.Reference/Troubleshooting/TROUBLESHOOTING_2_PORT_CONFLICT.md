# Hướng Dẫn Xử Lý Lỗi: Xung Đột Cổng 5000 (Port Conflict)

Lỗi này rất hay gặp khi lập trình Web (Flask/NodeJS) trên macOS, vì cấu hình mặc định của hệ điều hành.

## 1. Dấu hiệu nhận biết
Khi bạn chạy ứng dụng (ví dụ Flask):
```bash
python3 app.py
```
Bạn nhận được thông báo lỗi đỏ rực:
```text
OSError: [Errno 48] Address already in use
```
Hoặc:
```text
Error: Listen EADDRINUSE: address already in use :::5000
```

## 2. Nguyên nhân
- Bạn đang cố gắng khởi động Web Server ở cổng **5000**.
- Trên macOS, tính năng **"AirPlay Receiver"** (cho phép truyền màn hình iPhone lên Mac) mặc định chạy ngầm và **chiếm giữ đúng cổng 5000**.
- Hai ứng dụng không thể cùng nghe ở một cổng => Lỗi.

## 3. Cách Kiểm Tra (Diagnosis)
Để biết chính xác "kẻ nào" đang chiếm cổng 5000, hãy dùng lệnh `lsof` (List Open Files):

```bash
# -i :5000  => Tìm các tiến trình mạng ở cổng 5000
lsof -i :5000
```

**Kết quả thường thấy:**
```text
COMMAND      PID USER   TYPE             DEVICE SIZE/OFF NODE NAME
ControlCe  12345 elsa   IPv4 ...         0t0  TCP *:commplex-main (LISTEN)
```
- `ControlCe`: Viết tắt của **Control Center**. Đây chính là tiến trình của macOS (AirPlay).

## 4. Giải Pháp

### Cách 1: Đổi cổng cho ứng dụng của bạn (Khuyên dùng)
Chúng ta tránh cổng 5000 ra.
- Sửa trong Code (`app.py`):
  ```python
  app.run(port=5001)
  ```
- Sửa trong Dockerfile:
  ```dockerfile
  EXPOSE 5001
  ```
- Khi chạy Docker map port:
  ```bash
  docker run -p 5001:5001 ...
  ```

### Cách 2: Tắt AirPlay Receiver
Nếu bạn kiên quyết muốn dùng cổng 5000.
1. Mở **System Settings** (Cài đặt hệ thống).
2. Vào **General** -> **AirDrop & Handoff**.
3. Tìm mục **AirPlay Receiver** và gạt nút tắt.
4. Bây giờ cổng 5000 đã được giải phóng.

### Cách 3: Kill tiến trình đang chiếm (Chỉ dùng khi bị treo)
Nếu cổng bị chiếm bởi một ứng dụng cũ của chính bạn bị treo (không phải System), bạn có thể "giết" nó:
```bash
# Tìm PID
lsof -i :5000
# Kill PID (ví dụ PID là 9999)
kill -9 9999
```
*Cảnh báo: Đừng kill ControlCenter của Mac, nó sẽ tự khởi động lại thôi.*
