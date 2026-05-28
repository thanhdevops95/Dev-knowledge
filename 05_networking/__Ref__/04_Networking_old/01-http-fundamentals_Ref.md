# 🌐 Mạng máy tính & HTTP

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Hiểu nền tảng để làm Web

---

## Cách Internet hoạt động

Khi bạn gõ `https://google.com` vào trình duyệt:

```
1. DNS Lookup      → Dịch "google.com" → IP address (142.250.x.x)
2. TCP Handshake   → Thiết lập kết nối với server
3. TLS Handshake   → Mã hóa kết nối (HTTPS)
4. HTTP Request    → Trình duyệt gửi yêu cầu GET /
5. HTTP Response   → Server trả về HTML
6. Render          → Trình duyệt hiển thị trang
```

---

## DNS (Domain Name System)

DNS hoạt động như "danh bạ điện thoại" của Internet:

```
Bạn gõ: google.com
    ↓
DNS Resolver (ISP hoặc 8.8.8.8)
    ↓
Root Nameserver → .com Nameserver → google.com Nameserver
    ↓
IP: 142.250.185.46
```

**Các loại DNS record phổ biến:**

| Record | Dùng để |
|---|---|
| `A` | Trỏ domain → IPv4 |
| `AAAA` | Trỏ domain → IPv6 |
| `CNAME` | Alias của domain khác |
| `MX` | Mail server |
| `TXT` | Xác thực, SPF, DKIM |
| `NS` | Nameserver của domain |

---

## HTTP — HyperText Transfer Protocol

### HTTP Methods

| Method | Dùng để | Idempotent? |
|---|---|---|
| `GET` | Lấy dữ liệu | ✅ |
| `POST` | Tạo mới | ❌ |
| `PUT` | Cập nhật toàn bộ | ✅ |
| `PATCH` | Cập nhật một phần | ❌ |
| `DELETE` | Xóa | ✅ |
| `OPTIONS` | Kiểm tra CORS | ✅ |
| `HEAD` | Như GET nhưng không có body | ✅ |

### HTTP Status Codes

| Code | Ý nghĩa |
|---|---|
| `200 OK` | Thành công |
| `201 Created` | Tạo mới thành công |
| `204 No Content` | Thành công, không có nội dung trả về |
| `301 Moved Permanently` | Chuyển hướng vĩnh viễn |
| `302 Found` | Chuyển hướng tạm thời |
| `400 Bad Request` | Request sai cú pháp |
| `401 Unauthorized` | Chưa xác thực |
| `403 Forbidden` | Không có quyền truy cập |
| `404 Not Found` | Không tìm thấy |
| `409 Conflict` | Xung đột dữ liệu |
| `422 Unprocessable Entity` | Validation error |
| `429 Too Many Requests` | Rate limit |
| `500 Internal Server Error` | Lỗi phía server |
| `502 Bad Gateway` | Proxy/load balancer lỗi |
| `503 Service Unavailable` | Server quá tải hoặc bảo trì |

### HTTP Headers

```http
# Request Headers
GET /api/users HTTP/1.1
Host: api.example.com
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
Accept-Language: vi-VN

# Response Headers
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=3600
X-Rate-Limit-Remaining: 99
```

---

## HTTPS & TLS

**HTTPS = HTTP + TLS (Transport Layer Security)**

TLS Handshake (đơn giản hóa):
```
Client                          Server
  │── ClientHello ────────────────►│
  │◄─ ServerHello + Certificate ──│
  │── Kiểm tra Certificate ────────│
  │── PreMasterSecret (mã hóa) ──►│
  │◄─────── Mã hóa bắt đầu ───────│
  │◄──── Application Data ────────│
```

---

## TCP vs UDP

| | TCP | UDP |
|---|---|---|
| **Kết nối** | Có (3-way handshake) | Không |
| **Độ tin cậy** | Đảm bảo gói tin đến | Không đảm bảo |
| **Thứ tự** | Đúng thứ tự | Có thể lộn xộn |
| **Tốc độ** | Chậm hơn | Nhanh hơn |
| **Dùng cho** | HTTP, email, file transfer | Video streaming, gaming, DNS |

---

## API Concepts

### REST API
```
Resource:  /users
GET    /users          → Lấy danh sách user
POST   /users          → Tạo user mới
GET    /users/123      → Lấy user cụ thể
PUT    /users/123      → Cập nhật user
DELETE /users/123      → Xóa user
```

### WebSocket
- HTTP: Client hỏi → Server trả lời (one-way per request)
- WebSocket: Kết nối liên tục, 2 chiều (realtime: chat, game, live update)

```javascript
const ws = new WebSocket('wss://api.example.com/ws');
ws.onmessage = (event) => console.log(event.data);
ws.send(JSON.stringify({ type: 'message', content: 'Hello' }));
```

---

## CORS (Cross-Origin Resource Sharing)

Khi frontend (`localhost:3000`) gọi API backend (`localhost:8000`) → **CORS error**.

```
Origin A (localhost:3000) ──GET──► Origin B (localhost:8000)
                          ◄─ OK ──  (nếu cho phép)
                          ◄─ CORS ─ (nếu không cấu hình)
```

Server cần trả về header:
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
```

---

## Bài tập thực hành

- [ ] Dùng `curl` gọi một public API (ví dụ: `https://api.github.com/users/octocat`)
- [ ] Mở DevTools → Network tab → xem HTTP requests khi load một trang web
- [ ] Dùng `dig` hoặc `nslookup` để tra DNS của một domain

---

## Tài nguyên thêm

- [HTTP MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP) — Tài liệu HTTP đầy đủ
- [How HTTPS works](https://howhttps.works/) — Comic giải thích HTTPS trực quan
- [High Performance Browser Networking](https://hpbn.co/) — Free book về networking
