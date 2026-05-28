# ⚡ HTTP/3 & QUIC — Tương lai của Web

> `[ADVANCED]` — Prerequisite: `04-http-fundamentals.md`, `11-tcp-deep-dive.md`
> QUIC transport + HTTP/3: nhanh hơn, bảo mật hơn, phù hợp mạng mobile.

---

## 1. Vấn đề của HTTP/2 over TCP

HTTP/2 đã cải thiện rất nhiều so với HTTP/1.1 (multiplexing, header compression, server push). Nhưng vẫn dùng **TCP** → vấn đề cố hữu:

```
HTTP/2 over TCP — Head-of-Line (HOL) Blocking:

Stream 1: [DATA]───[DATA]───────────[DATA]
Stream 2: [DATA]───[DATA]──[LOST]──────── ← 1 packet lost
Stream 3: [DATA]───[DATA]───────────[DATA]

TCP layer: phải retransmit lost packet → 
           TOÀN BỘ streams bị block chờ! 💀

QUIC giải quyết: multiplexing ở transport layer
Stream 1: [DATA]───[DATA]───────────[DATA] ← không bị ảnh hưởng
Stream 2: [DATA]───[DATA]──[LOST]──[retransmit]
Stream 3: [DATA]───[DATA]───────────[DATA] ← không bị ảnh hưởng
→ Chỉ stream bị mất packet phải chờ, streams khác vẫn chạy!
```

```
TCP Handshake overhead:

HTTP/2 over TLS 1.3 (TCP):
  Round 1: TCP SYN → SYN+ACK → ACK        (1 RTT)
  Round 2: TLS ClientHello → ServerHello    (1 RTT)
  Round 3: Data transfer
  Total: 2 RTT trước khi gửi data

QUIC (HTTP/3):
  Round 1: QUIC handshake + TLS integrated  (1 RTT)
  Round 2: Data transfer
  Total: 1 RTT! 

0-RTT resumption (trở lại server đã connect):
  QUIC: Gửi data NGAY LẬP TỨC (0 RTT)! 🚀
```

---

## 2. QUIC Transport Protocol

### QUIC Architecture

```
┌─────────────────────────────────┐
│         HTTP/3                  │  Application layer
├─────────────────────────────────┤
│         QUIC                    │  Transport layer
│  ┌─────────┐  ┌──────────────┐ │
│  │ Streams  │  │  TLS 1.3    │ │  ← TLS built-in!
│  │ (mux)    │  │  (encrypted) │ │
│  └─────────┘  └──────────────┘ │
├─────────────────────────────────┤
│         UDP                     │  ← Dựa trên UDP
├─────────────────────────────────┤
│         IP                      │
└─────────────────────────────────┘

So sánh:
HTTP/2:  HTTP/2 → TLS 1.3 → TCP → IP (4 layers, 2+ RTT)
HTTP/3:  HTTP/3 → QUIC(+TLS) → UDP → IP (3 layers, 1 RTT)
```

### QUIC Key Features

| Feature | Mô tả |
|---|---|
| **Built-in encryption** | TLS 1.3 tích hợp, KHÔNG có plaintext |
| **Stream multiplexing** | Nhiều streams độc lập, no HOL blocking |
| **0-RTT connection** | Resume session cũ, gửi data ngay |
| **Connection migration** | Chuyển WiFi → 4G không mất connection |
| **Improved loss recovery** | Mỗi packet có unique number, detect loss chính xác hơn |
| **Flow control** | Per-stream + per-connection flow control |

### Connection Migration

```
TCP: connection = (src_ip, src_port, dst_ip, dst_port)
  Khi chuyển WiFi → 4G: IP thay đổi → connection MẤT
  → Phải reconnect (3-way handshake + TLS lại)

QUIC: connection = Connection ID (random, không phụ thuộc IP)
  Khi chuyển WiFi → 4G: IP thay đổi nhưng Connection ID giữ nguyên
  → Connection TIẾP TỤC! Không mất data, không delay

→ Tuyệt vời cho mobile (di chuyển, đổi network liên tục)
```

---

## 3. HTTP/3 — HTTP over QUIC

```
HTTP/3 changes so với HTTP/2:

✅ Giữ nguyên:
  - Multiplexing (nhiều requests trên 1 connection)
  - Header compression (QPACK thay HPACK)
  - Server push (ít dùng, có thể bỏ)
  - Binary framing
  - Semantics: GET, POST, headers, status codes

✅ Cải thiện:
  - NO Head-of-Line blocking (stream-level)
  - Faster connection setup (1-RTT, 0-RTT)
  - Connection migration
  - Better loss recovery

❌ Bỏ:
  - TCP (dùng QUIC/UDP thay)
  - HPACK (dùng QPACK — phù hợp QUIC)
  - HTTP/2 priority scheme (có scheme mới)
```

---

## 4. QUIC Internals — Cách hoạt động bên trong

### Packet Structure

```
QUIC Packet:
┌──────────────────────────────────────┐
│ Header (unencrypted)                 │
│  - Connection ID                     │
│  - Packet Number                     │
├──────────────────────────────────────┤
│ Payload (encrypted)                  │
│  - STREAM frames (data)             │
│  - ACK frames                        │
│  - CRYPTO frames (handshake)        │
│  - PADDING frames                    │
│  - RESET_STREAM frames              │
└──────────────────────────────────────┘

Mọi payload đều encrypted! Chỉ Connection ID visible.
```

### QPACK vs HPACK

```
HPACK (HTTP/2):       QPACK (HTTP/3):
  Sequential         Independent per stream
  Đơn giản hơn       Phức tạp hơn, nhưng no HOL blocking
  
HPACK problem: encoder/decoder state phải synchronized
  → 1 stream block → tất cả header decoding block

QPACK solution: 2 unidirectional streams cho table updates
  → Streams decode headers independently
```

---

## 5. HTTP/3 Adoption — Ai đang dùng?

```
2024+ Adoption:
  ✅ Google (YouTube, Search, Gmail)     — ~30% global traffic
  ✅ Facebook/Meta                       — All services
  ✅ Cloudflare (CDN)                    — Default enabled
  ✅ Fastly (CDN)                        — Supported
  ✅ Chrome, Firefox, Safari, Edge       — All support
  ⚠️ Nginx                              — Experimental
  ⚠️ Apache                             — Limited
  ✅ Caddy                               — Full support
  ✅ LiteSpeed                           — Full support
```

### Cách enable HTTP/3

```nginx
# Nginx (1.25.0+ with quic module)
server {
    listen 443 quic reuseport;    # HTTP/3
    listen 443 ssl http2;          # HTTP/2 fallback
    
    ssl_certificate /cert.pem;
    ssl_certificate_key /key.pem;
    
    add_header Alt-Svc 'h3=":443"; ma=86400';  # Advertise HTTP/3
}
```

```
# Caddy (built-in HTTP/3)
example.com {
    # HTTP/3 enabled by default!
    reverse_proxy localhost:8080
}
```

---

## 6. Khi nào dùng HTTP/3?

```
✅ Nên dùng HTTP/3:
  - High latency networks (mobile, satellite)
  - Lossy networks (packet loss > 1%)
  - Mobile apps (connection migration!)
  - CDN/edge serving
  - Video streaming

⚠️ Chưa cần HTTP/3:
  - Internal/LAN services (latency đã thấp)
  - Legacy systems chưa support
  - UDP bị firewall block (một số corporate networks)
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | "QUIC dùng UDP → unreliable" | QUIC tự implement reliability trên UDP | QUIC reliable như TCP nhưng nhanh hơn |
| 2 | HTTP/3 thay thế HTTP/2 ngay | HTTP/2 vẫn fallback, gradual adoption | `Alt-Svc` header cho phép upgrade dần |
| 3 | "Bật HTTP/3 → tự động nhanh hơn" | HTTP/3 nhanh hơn chủ yếu trên high-latency/lossy networks | LAN: khác biệt minimal |
| 4 | UDP blocked bởi firewall | Cần mở UDP port 443 | Một số networks block UDP → fallback TCP |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** Kiểm tra website dùng HTTP/3 bằng Chrome DevTools (Protocol column)
- [ ] **Bài 2 (Trung bình):** Setup Caddy server với HTTP/3 enabled, verify bằng `curl --http3`
- [ ] **Bài 3 (Khó):** So sánh performance HTTP/2 vs HTTP/3 trên lossy network (dùng `tc` simulate packet loss)

---

## Tài nguyên thêm

- [QUIC RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html) — Official spec
- [HTTP/3 explained (Daniel Stenberg)](https://http3-explained.haxx.se/) — curl author, free book ⭐
- [Cloudflare QUIC blog](https://blog.cloudflare.com/tag/quic/) — Practical QUIC insights
- [Can I Use HTTP/3?](https://caniuse.com/http3) — Browser support
