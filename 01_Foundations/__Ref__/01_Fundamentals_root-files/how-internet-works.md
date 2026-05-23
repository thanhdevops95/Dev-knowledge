# 🌐 Cách Internet hoạt động

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Hiểu nền tảng trước khi xây dựng bất cứ thứ gì trên web

---

## Khi bạn gõ URL vào trình duyệt, điều gì xảy ra?

Hãy theo dõi hành trình của request `https://github.com`:

```
Bạn gõ: https://github.com
              │
    ┌─────────▼──────────┐
    │   DNS Resolution    │  "github.com" → 140.82.114.4
    └─────────┬──────────┘
              │ IP address
    ┌─────────▼──────────┐
    │  TCP Handshake     │  Thiết lập kết nối tin cậy (3-way)
    └─────────┬──────────┘
              │ Connected
    ┌─────────▼──────────┐
    │  TLS Handshake     │  Mã hóa kết nối (HTTPS)
    └─────────┬──────────┘
              │ Encrypted channel
    ┌─────────▼──────────┐
    │  HTTP Request      │  GET / HTTP/2
    └─────────┬──────────┘
              │ → Server
    ┌─────────▼──────────┐
    │  HTTP Response     │  200 OK + HTML
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │  Browser Render    │  Parse HTML → CSS → JS → Hiển thị
    └────────────────────┘
```

---

## 1. DNS — Dịch tên miền thành IP

**Domain Name System** hoạt động như danh bạ điện thoại của Internet:

```
Bạn gõ: github.com
    │
    ├── Kiểm tra cache trình duyệt
    ├── Kiểm tra /etc/hosts (hệ điều hành)
    ├── Hỏi DNS Resolver của ISP (hoặc 8.8.8.8, 1.1.1.1)
    │       │
    │       ├── Root Nameserver (.) → biết .com ở đâu
    │       ├── TLD Nameserver (.com) → biết github.com ở đâu
    │       └── Authoritative Nameserver (github.com) → IP: 140.82.114.4
    │
    └── Trả về: 140.82.114.4
```

**Kiểm tra DNS trên terminal:**
```bash
dig github.com          # Chi tiết
nslookup github.com     # Đơn giản hơn
host github.com         # Ngắn gọn
```

---

## 2. TCP — Kết nối tin cậy

**TCP (Transmission Control Protocol)** đảm bảo dữ liệu đến đúng và đủ.

**3-Way Handshake:**
```
Client                  Server
  │──── SYN ──────────►│  "Tôi muốn kết nối"
  │◄─── SYN + ACK ─────│  "OK, tôi sẵn sàng"
  │──── ACK ──────────►│  "Đã nhận, bắt đầu thôi"
  │                     │
  │◄══ Data flows ═════►│  (Kết nối đã thiết lập)
```

**Kết thúc kết nối (4-Way):**
```
Client                  Server
  │──── FIN ──────────►│
  │◄─── ACK ───────────│
  │◄─── FIN ───────────│
  │──── ACK ──────────►│
```

---

## 3. TLS/SSL — Bảo mật kết nối

**HTTPS = HTTP + TLS**. TLS mã hóa toàn bộ dữ liệu truyền đi.

```
Client                          Server
  │── ClientHello ─────────────►│  (TLS version, cipher suites)
  │◄─ ServerHello + Cert ───────│  (Server gửi certificate)
  │── Verify certificate ────────│  (Client kiểm tra cert với CA)
  │── Key Exchange ─────────────►│  (Trao đổi khóa mã hóa)
  │◄──────── Encrypted data ────►│  (Từ đây toàn bộ mã hóa)
```

**Certificate Authority (CA):** Tổ chức bên thứ 3 (DigiCert, Let's Encrypt...) xác nhận "github.com thực sự là GitHub".

---

## 4. HTTP — Giao thức ứng dụng

**HTTP/1.1 → HTTP/2 → HTTP/3**

| | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---|---|---|---|
| **Transport** | TCP | TCP | UDP (QUIC) |
| **Multiplexing** | ❌ | ✅ | ✅ |
| **Header Compression** | ❌ | ✅ (HPACK) | ✅ (QPACK) |
| **Server Push** | ❌ | ✅ | ✅ |
| **0-RTT** | ❌ | ❌ | ✅ |

---

## 5. Rendering — Trình duyệt hiển thị trang

```
HTML received
    │
    ▼
Parse HTML → DOM Tree
    │
    ▼
Parse CSS → CSSOM Tree
    │
    ▼
DOM + CSSOM → Render Tree
    │
    ▼
Layout (tính vị trí, kích thước)
    │
    ▼
Paint (vẽ pixels)
    │
    ▼
Compositing (kết hợp layers)
    │
    ▼
Display!
```

**Critical Rendering Path** — Những gì block render:
- CSS block rendering (phải tải xong mới render)
- JavaScript block parsing (phải xử lý xong mới tiếp tục parse HTML)
- Dùng `defer` và `async` cho script để không block

```html
<script src="app.js" defer></script>   <!-- Tải song song, chạy sau khi parse xong -->
<script src="app.js" async></script>   <!-- Tải song song, chạy ngay khi tải xong -->
```

---

## Các giao thức và khái niệm khác

### IP Addresses

```
IPv4: 192.168.1.1      (32-bit, ~4.3 tỷ địa chỉ — đã hết!)
IPv6: 2001:db8::1      (128-bit, gần như vô hạn)

Private (LAN):
  10.0.0.0/8           (10.x.x.x)
  172.16.0.0/12        (172.16.x.x - 172.31.x.x)
  192.168.0.0/16       (192.168.x.x)

Loopback: 127.0.0.1    (localhost — máy tự trỏ đến chính nó)
```

### Ports

```
Port = cổng vào cho từng dịch vụ trên cùng 1 máy

22    → SSH
25    → SMTP (email)
53    → DNS
80    → HTTP
443   → HTTPS
3306  → MySQL
5432  → PostgreSQL
6379  → Redis
8080  → HTTP alternative (dev)
27017 → MongoDB
```

### Load Balancer

```
             ┌─── Server 1 (app instance)
Client ──►   Load ──► Server 2 (app instance)
Balancer     └─── Server 3 (app instance)
```

**Các thuật toán:**
- **Round Robin** — Lần lượt từng server
- **Least Connections** — Server ít kết nối nhất
- **IP Hash** — Cùng IP → cùng server (session sticky)

### CDN (Content Delivery Network)

```
User ở Việt Nam
    │
    ▼
CDN Edge Server (Singapore)  ← nhanh hơn!
    │ (cache miss)
    ▼
Origin Server (US)
```

CDN cache static assets (ảnh, JS, CSS, video) gần người dùng nhất để giảm latency.

---

## Bài tập thực hành

- [ ] Mở DevTools → Network tab → xem từng request/response khi load trang web
- [ ] Chạy `traceroute google.com` — xem packet đi qua những hop nào
- [ ] Xem certificate của một trang HTTPS bằng cách click vào ổ khóa
- [ ] Thử `curl -v https://api.github.com` — xem TLS handshake và headers

---

## Tài nguyên thêm

- [How DNS Works (comic)](https://howdns.works/) — Visual dễ hiểu
- [How HTTPS Works (comic)](https://howhttps.works/) — TLS giải thích qua truyện tranh
- [HTTP/2 explained](https://http2-explained.haxx.se/) — Free book
