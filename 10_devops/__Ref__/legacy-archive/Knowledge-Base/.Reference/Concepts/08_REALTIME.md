# 08. Real-time Communication

[← APIs](07_APIS.md) | [Tiếp: Messaging →](09_MESSAGING.md)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Polling** | /ˈpəʊlɪŋ/ | Thăm dò - Client hỏi server định kỳ để kiểm tra dữ liệu mới |
| **Short Polling** | - | Thăm dò ngắn - Gửi request định kỳ (mỗi vài giây) |
| **Long Polling** | - | Thăm dò dài - Server giữ kết nối đến khi có dữ liệu mới |
| **WebSocket** | - | Giao thức kết nối hai chiều liên tục giữa client và server |
| **Full-duplex** | - | Song công - Cả hai bên có thể gửi/nhận đồng thời |
| **Half-duplex** | - | Bán song công - Chỉ một bên gửi tại một thời điểm |
| **SSE** | - | Server-Sent Events - Server đẩy dữ liệu một chiều đến client |
| **Push** | - | Đẩy - Server chủ động gửi dữ liệu đến client |
| **Pull** | - | Kéo - Client chủ động yêu cầu dữ liệu từ server |
| **Persistent Connection** | - | Kết nối liên tục - Không đóng sau mỗi request |
| **Handshake** | - | Bắt tay - Quá trình thiết lập kết nối WebSocket |

---

# 🤔 Tại sao DevOps cần biết Real-time Communication?

## Nỗi đau thực tế

> "Chat app cứ phải refresh mới thấy tin nhắn mới"

> "Dashboard monitoring không cập nhật real-time, mất 30 giây mới thấy alert"

> "Dùng polling mà server bị overwhelming với hàng ngàn requests/giây"

## Kiến thức này giúp bạn

| Tình huống | Cần biết |
|------------|----------|
| Build chat application | WebSocket |
| Live dashboard/monitoring | SSE hoặc WebSocket |
| Notification system | Long Polling hoặc SSE |
| Real-time collaboration | WebSocket |
| Giảm tải server từ polling | Chuyển sang WebSocket/SSE |

Hiểu real-time communication giúp bạn chọn đúng công nghệ cho từng use case, tránh lãng phí tài nguyên với polling không cần thiết.

---

# 🔄 Polling

## Short Polling

Client gửi request đến server **định kỳ** để kiểm tra dữ liệu mới.

```
┌─────────────────────────────────────────────────────────────┐
│                    SHORT POLLING                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Client                              Server                  │
│    │                                   │                     │
│    │──── GET /updates ────────────────►│                     │
│    │◄──── Response (no data) ──────────│                     │
│    │                                   │                     │
│    │      [wait 5 seconds]             │                     │
│    │                                   │                     │
│    │──── GET /updates ────────────────►│                     │
│    │◄──── Response (no data) ──────────│                     │
│    │                                   │                     │
│    │      [wait 5 seconds]             │                     │
│    │                                   │                     │
│    │──── GET /updates ────────────────►│                     │
│    │◄──── Response (has data!) ────────│                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Problems:**

- Wastes bandwidth
- High server load
- Not real-time

---

## Long Polling

Server **holds the request open** until data is available.

```
┌─────────────────────────────────────────────────────────────┐
│                     LONG POLLING                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Client                              Server                  │
│    │                                   │                     │
│    │──── GET /updates ────────────────►│                     │
│    │                                   │                     │
│    │     [Server holds connection]     │                     │
│    │     [waiting for data...]         │                     │
│    │                                   │                     │
│    │         [Data arrives!]           │                     │
│    │                                   │                     │
│    │◄──── Response (with data) ────────│                     │
│    │                                   │                     │
│    │──── GET /updates ────────────────►│  ← Immediately      │
│    │     [cycle repeats]               │    reconnect        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Better than short polling but:**

- Still creates new connections
- Timeout handling needed

---

# 🔌 WebSocket

## WebSocket là gì?

**WebSocket** provides **full-duplex communication** channel over a single TCP connection.

```
┌─────────────────────────────────────────────────────────────┐
│                      WEBSOCKET                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Client                              Server                  │
│    │                                   │                     │
│    │──── HTTP Upgrade Request ────────►│                     │
│    │      (Upgrade: websocket)         │                     │
│    │                                   │                     │
│    │◄──── 101 Switching Protocols ─────│                     │
│    │                                   │                     │
│    │◄════════════════════════════════►│                     │
│    │     Persistent bidirectional      │                     │
│    │     connection established        │                     │
│    │                                   │                     │
│    │──── Send message ────────────────►│                     │
│    │◄──── Push notification ───────────│                     │
│    │──── Send message ────────────────►│                     │
│    │◄──── Push notification ───────────│                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## WebSocket Handshake

```http
# Client Request
GET /chat HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13

# Server Response
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

---

## Use Cases

- **Chat applications** (Slack, Discord)
- **Live sports scores**
- **Real-time gaming**
- **Stock tickers**
- **Collaborative editing** (Google Docs)

---

# 📡 Server-Sent Events (SSE)

## SSE là gì?

**SSE** is **server-to-client only** streaming over HTTP.

```
┌─────────────────────────────────────────────────────────────┐
│                 SERVER-SENT EVENTS (SSE)                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Client                              Server                  │
│    │                                   │                     │
│    │──── GET /events ─────────────────►│                     │
│    │                                   │                     │
│    │◄─── data: Update 1 ───────────────│                     │
│    │◄─── data: Update 2 ───────────────│                     │
│    │◄─── data: Update 3 ───────────────│                     │
│    │                                   │                     │
│    │     (Server keeps pushing)        │                     │
│    │                                   │                     │
│    X     Only server→client            │                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

# 📊 Comparison Table

| Feature | Short Polling | Long Polling | WebSocket | SSE |
|---------|---------------|--------------|-----------|-----|
| **Direction** | Client→Server | Client→Server | Bidirectional | Server→Client |
| **Connection** | New each time | Held open | Persistent | Persistent |
| **Latency** | High | Medium | Low | Low |
| **Overhead** | High | Medium | Low | Low |
| **Browser** | ✅ All | ✅ All | ✅ All | ✅ Most |
| **Use case** | Simple status | Notifications | Chat, Games | Live feeds |

---

[← APIs](07_APIS.md) | [Tiếp: Messaging →](09_MESSAGING.md)
