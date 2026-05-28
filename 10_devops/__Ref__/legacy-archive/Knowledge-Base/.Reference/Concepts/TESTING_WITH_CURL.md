# Hướng Dẫn Kiểm Thử Bằng Lệnh Curl (Client URL)

`curl` là công cụ dòng lệnh mạnh mẽ giúp bạn gửi request HTTP mà không cần mở trình duyệt. Nó vô cùng hữu ích khi làm việc với server không có giao diện (headless) hoặc khi muốn xem chi tiết response.

Bạn nên mở một tab Terminal mới (Terminal thứ 3) để gõ các lệnh này, trong khi vẫn giữ 2 terminal kia chạy ứng dụng.

## 1. Test Python App (Frontend)
Đây là cách người dùng bình thường (hoặc Frontend App khác) sẽ gọi vào hệ thống của bạn.

`python-app` đang chạy ở cổng **5001**.
```bash
curl http://localhost:5001/do-ping
```
**Kết quả kỳ vọng:**
```json
{"backend_response":"Pong! Total pings: 1","backend_url":"http://localhost:8080","message":"Ping successful"}
```
- Nếu thấy JSON này, tức là:
  1. Bạn gọi thành công vào Python App.
  2. Python App đã gọi thành công sang Go App.
  3. Go App đã trả lời "Pong".

### Xem chi tiết (Verbose)
Thêm cờ `-v` để xem toàn bộ quá trình bắt tay, gửi header:
```bash
curl -v http://localhost:5001/do-ping
```
Bạn sẽ thấy các dòng bắt đầu bằng `>` (Gửi đi) và `<` (Nhận về), rất hữu ích để debug Header.

---

## 2. Test Go App (Backend)
Bạn cũng có thể gọi trực tiếp vào Backend để kiểm tra xem nó có sống không, bỏ qua vai trò của Python.

`go-app` đang chạy ở cổng **8080**.

### Test API Ping
```bash
curl http://localhost:8080/ping
```
**Kết quả:**
```text
Pong! Total pings: 2
```

### Test API Stats (Không qua cơ chế đếm)
```bash
curl http://localhost:8080/stats
```
**Kết quả:**
```json
{"pings": 2}
```

---

## 3. Test Kịch bản Lỗi (Khi tắt Go App)
Hãy thử tắt Terminal đang chạy Go App (Ctrl+C), nhưng vẫn để Python App chạy.

Sau đó gọi lại lệnh curl vào Python:
```bash
curl http://localhost:5001/do-ping
```
**Kết quả kỳ vọng (Lỗi được xử lý):**
```json
{
  "error": "HTTPConnectionPool(host='localhost', port=8080): Max retries exceeded...",
  "url": "http://localhost:8080"
}
```
Lúc này bạn sẽ biết ngay là kết nối giữa 2 container bị đứt (hoặc backend chết), trong khi Frontend vẫn sống.
