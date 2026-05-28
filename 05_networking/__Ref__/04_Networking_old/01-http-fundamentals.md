# 🌐 HTTP — Giao thức nền tảng của web

> `[BEGINNER → INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Mọi request trên web đều là HTTP

---

## Tại sao cần hiểu HTTP?

Mỗi khi bạn mở trang web, gọi API, download file — **HTTP** đang làm việc phía sau. Hiểu HTTP = debug nhanh, thiết kế API tốt, tối ưu performance.

---

## 1. HTTP Request & Response

```
CLIENT (Browser/App)                    SERVER
    │                                      │
    │── HTTP Request ──────────────────►   │
    │   POST /api/users HTTP/1.1           │
    │   Host: api.example.com              │
    │   Content-Type: application/json     │
    │   Authorization: Bearer eyJ...       │
    │                                      │
    │   {"name": "An", "email": "..."}     │
    │                                      │
    │◄── HTTP Response ────────────────    │
    │   HTTP/1.1 201 Created               │
    │   Content-Type: application/json     │
    │   Cache-Control: no-cache            │
    │                                      │
    │   {"id": 1, "name": "An"}            │
    │                                      │
```

### Request structure

```
[Method] [Path] HTTP/[Version]    ← Request line
[Headers]                          ← Metadata
                                   ← Blank line
[Body]                             ← Data (optional)

Ví dụ:
POST /api/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer eyJhbGciOi...
Content-Length: 45

{"name": "An", "email": "an@mail.com"}
```

### Response structure

```
HTTP/[Version] [Status Code] [Reason]   ← Status line
[Headers]                                ← Metadata
                                         ← Blank line
[Body]                                   ← Data

Ví dụ:
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=3600
X-Request-Id: abc-123

{"data": [...]}
```

---

## 2. HTTP Headers quan trọng

### Request Headers

| Header | Mục đích | Ví dụ |
|---|---|---|
| `Host` | Domain server | `api.example.com` |
| `Content-Type` | Kiểu dữ liệu gửi | `application/json` |
| `Authorization` | Xác thực | `Bearer eyJ...` |
| `Accept` | Kiểu dữ liệu muốn nhận | `application/json` |
| `User-Agent` | Client info | `Mozilla/5.0...` |
| `Cookie` | Session data | `session=abc123` |
| `Accept-Language` | Ngôn ngữ ưu tiên | `vi-VN,en-US` |
| `If-None-Match` | Conditional (ETag) | `"abc123"` |

### Response Headers

| Header | Mục đích | Ví dụ |
|---|---|---|
| `Content-Type` | Kiểu dữ liệu trả | `application/json; charset=utf-8` |
| `Cache-Control` | Caching policy | `max-age=3600, public` |
| `Set-Cookie` | Đặt cookie | `session=abc; HttpOnly; Secure` |
| `ETag` | Version identifier | `"abc123"` |
| `Access-Control-*` | CORS | `Access-Control-Allow-Origin: *` |
| `Location` | Redirect URL | `https://example.com/new-page` |

---

## 3. CORS — Cross-Origin Resource Sharing

```
Problem: Browser chặn request từ domain khác (Same-Origin Policy)

frontend.com ──► api.example.com  → ❌ Blocked by CORS!

Solution: Server cho phép qua headers

Server response:
Access-Control-Allow-Origin: https://frontend.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400
```

```
Preflight Request (OPTIONS) — trước mỗi "complex" request:

Browser ──► OPTIONS /api/users
            Origin: https://frontend.com
            Access-Control-Request-Method: POST

Server  ◄── 204 No Content
            Access-Control-Allow-Origin: https://frontend.com
            Access-Control-Allow-Methods: POST

Browser ──► POST /api/users   ← Bây giờ mới gửi request thật
```

```javascript
// Express.js CORS setup
const cors = require('cors');

app.use(cors({
    origin: ['https://frontend.com', 'https://admin.com'],
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    credentials: true,  // Cho phép cookies
}));
```

---

## 4. Caching — Tăng tốc

```
Không cache:    Client ──► Server ──► DB (mỗi request)
Có cache:       Client ──► Cache HIT! → Trả ngay (không qua server)

Cache-Control header:
• no-store:          Không cache gì cả (sensitive data)
• no-cache:          Cache nhưng LUÔN validate với server
• max-age=3600:      Cache 1 giờ, không cần hỏi server
• public:            CDN có thể cache
• private:           Chỉ browser cache (user-specific data)
• must-revalidate:   Hết hạn → phải hỏi server
```

```
ETag — Conditional Request:

Request 1:
GET /api/users → 200 OK, ETag: "v1"

Request 2:
GET /api/users
If-None-Match: "v1"
→ Server: Data chưa đổi → 304 Not Modified (không gửi body → nhanh!)
→ Server: Data đã đổi  → 200 OK + data mới + ETag: "v2"
```

---

## 5. HTTP/1.1 vs HTTP/2 vs HTTP/3

```
HTTP/1.1 (1997):
┌────┐ ┌────┐ ┌────┐
│ R1 │→│ R2 │→│ R3 │  ← Tuần tự (head-of-line blocking)
└────┘ └────┘ └────┘
  Mỗi request phải đợi response trước mới gửi tiếp

HTTP/2 (2015):
┌────┐
│ R1 │──┐
│ R2 │──┼── Multiplexing (song song trên 1 TCP connection)
│ R3 │──┘
└────┘
  + Header compression (HPACK)
  + Server Push

HTTP/3 (2022):
  Dùng QUIC (UDP) thay TCP
  + Không head-of-line blocking
  + Faster connection setup (0-RTT)
  + Better on unstable networks (mobile)
```

---

## 6. Cookies vs LocalStorage vs SessionStorage

| | Cookies | LocalStorage | SessionStorage |
|---|---|---|---|
| **Kích thước** | ~4KB | ~5-10MB | ~5-10MB |
| **Gửi server?** | ✅ Mỗi request | ❌ | ❌ |
| **Hết hạn** | Set expires | Vĩnh viễn | Đóng tab |
| **Truy cập** | Server + Client | Client only | Client only |
| **Use case** | Auth, sessions | User preferences | Cart, form draft |

```javascript
// Cookies
document.cookie = "theme=dark; max-age=86400; path=/; SameSite=Strict";

// LocalStorage
localStorage.setItem("language", "vi");
const lang = localStorage.getItem("language");  // "vi"
localStorage.removeItem("language");

// SessionStorage
sessionStorage.setItem("cartId", "abc123");
```

---

## 7. HTTPS & TLS

```
HTTP:  Plaintext → Ai cũng đọc được
HTTPS: HTTP + TLS encryption → Chỉ 2 bên đọc được

TLS Handshake (simplified):
Client ──► ClientHello (supported cipher suites)
Server ◄── ServerHello (chosen cipher) + Certificate
Client ──► Verify certificate + Key Exchange
           ← Encrypted connection established →
Client ◄═══════════ HTTPS ══════════► Server
```

---

## Các lỗi thường gặp

```
❌ Sai: CORS: Allow-Origin: * cho production → bảo mật kém
✅ Đúng: Chỉ allow domains cụ thể

❌ Sai: Cache sensitive data (user profile) với public cache
✅ Đúng: Cache-Control: private, no-store cho data nhạy cảm

❌ Sai: Gửi JWT trong URL query string → lộ trong logs
✅ Đúng: Gửi trong Authorization header
```

---

## Bài tập thực hành

- [ ] Dùng browser DevTools → Network tab xem request/response headers
- [ ] Implement CORS middleware cho Express.js API
- [ ] Setup Cache-Control cho static assets (images, CSS, JS)
- [ ] Dùng curl gửi HTTP request: GET, POST, với headers

---

## Tài nguyên thêm

- [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) — Reference đầy đủ nhất
- [HTTP/2 Explained](https://http2-explained.haxx.se/) — Free book
- [High Performance Browser Networking](https://hpbn.co/) — Free book by Ilya Grigorik
