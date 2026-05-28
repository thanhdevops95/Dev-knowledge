# 🔌 WebSockets & SSE — Real-time Communication

> `[INTERMEDIATE]` — Prerequisite: hiểu HTTP cơ bản
> Push data từ server → client without polling.

---

## Tại sao cần Real-time?

HTTP truyền thống: client **hỏi** → server **trả lời** (request-response). Nhưng nhiều ứng dụng cần server **chủ động gửi** data cho client ngay khi có:
- Chat messages
- Live notifications
- Stock prices
- Collaborative editing (Google Docs)
- Gaming
- Live dashboards

---

## 1. Short Polling → Long Polling → SSE → WebSockets

```
Polling (Cũ):
  Client: "Có tin mới không?" → Server: "Chưa"  (lặp lại mỗi 2s)
  Client: "Có tin mới không?" → Server: "Chưa"
  Client: "Có tin mới không?" → Server: "CÓ!"
  → Lãng phí bandwidth và server resources

Long Polling:
  Client: "Có tin mới không?" → Server: (giữ kết nối, đợi...)
  ... 30 giây sau ... → Server: "CÓ!" → Client reconnect
  → Tốt hơn, nhưng vẫn overhead reconnection

SSE (Server-Sent Events):
  Client ──HTTP request──→ Server
  Server ──event stream──→ Client (1 chiều, persistent)
  → Đơn giản, tự reconnect, dùng HTTP

WebSocket:
  Client ←──bi-directional──→ Server (2 chiều, persistent)
  → Full-duplex, low latency, nhưng phức tạp hơn
```

---

## 2. WebSocket Protocol

### Handshake — HTTP Upgrade

```http
# Client request (HTTP Upgrade)
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13

# Server response (101 Switching Protocols)
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=

# Sau handshake → WebSocket connection established
# Giao tiếp bằng frames (binary), không phải HTTP
```

### Server Implementation (Python)

```python
# pip install websockets
import asyncio
import websockets
import json

connected_clients = set()

async def handler(ws, path):
    connected_clients.add(ws)
    try:
        async for message in ws:
            data = json.loads(message)
            # Broadcast to all connected clients
            broadcast_msg = json.dumps({
                "user": data.get("user", "Anonymous"),
                "message": data.get("message", ""),
                "timestamp": datetime.now().isoformat()
            })
            websockets.broadcast(connected_clients, broadcast_msg)
    finally:
        connected_clients.remove(ws)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever

asyncio.run(main())
```

### Client Implementation

```javascript
// Browser WebSocket API
const ws = new WebSocket('wss://server.example.com/chat');

ws.onopen = () => {
    console.log('Connected');
    ws.send(JSON.stringify({ user: 'An', message: 'Hello!' }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(`${data.user}: ${data.message}`);
};

ws.onclose = (event) => {
    console.log(`Disconnected: ${event.code}`);
    // Reconnect logic
    setTimeout(() => connectWS(), 3000);
};

ws.onerror = (error) => console.error('WS Error:', error);
```

---

## 3. Server-Sent Events (SSE)

**SSE** đơn giản hơn WebSocket: server gửi events **1 chiều** qua HTTP. Browser tự reconnect.

### Server (Node.js)

```javascript
// Express SSE endpoint
app.get('/events', (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    
    // Send event every 2 seconds
    const interval = setInterval(() => {
        const data = { price: Math.random() * 100, time: new Date() };
        res.write(`event: stock-update\n`);
        res.write(`data: ${JSON.stringify(data)}\n\n`);
    }, 2000);
    
    req.on('close', () => clearInterval(interval));
});
```

### Client

```javascript
// Browser EventSource API
const source = new EventSource('/events');

source.addEventListener('stock-update', (event) => {
    const data = JSON.parse(event.data);
    console.log(`Stock: $${data.price.toFixed(2)}`);
});

source.onerror = () => {
    console.log('Connection lost, auto-reconnecting...');
    // EventSource tự reconnect!
};
```

---

## 4. So sánh — Khi nào dùng gì?

| | WebSocket | SSE | Long Polling |
|---|---|---|---|
| **Direction** | Bi-directional ↔ | Server → Client → | Client ↔ Server |
| **Protocol** | WS/WSS | HTTP | HTTP |
| **Auto-reconnect** | ❌ Manual | ✅ Built-in | ❌ Manual |
| **Binary data** | ✅ | ❌ (text only) | ❌ |
| **Overhead** | Low (frames) | Low (HTTP stream) | High (new connections) |
| **Browser support** | ✅ All | ✅ All (except IE) | ✅ All |
| **Through proxies** | ⚠️ May need config | ✅ Standard HTTP | ✅ Standard HTTP |

### Khi nào dùng gì?

```
Chat app, multiplayer game, collaborative editing?
  → WebSocket (bidirectional, low latency)

Live feed, notifications, stock prices?
  → SSE (server push, simpler, auto-reconnect)

Legacy systems, firewall restrictions?
  → Long Polling (works everywhere)

One-time data fetch?
  → Regular HTTP (don't over-engineer!)
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | WebSocket cho mọi real-time | SSE đủ cho server→client | SSE đơn giản hơn, auto-reconnect |
| 2 | Không handle reconnection | Implement exponential backoff reconnect | Network interruptions xảy ra thường xuyên |
| 3 | Quên heartbeat/ping | Gửi ping/pong mỗi 30s | Detect dead connections, prevent timeout |
| 4 | WebSocket không qua Nginx | Config `proxy_set_header Upgrade $http_upgrade` | Nginx cần biết để forward WS |

---

## Bài tập thực hành

- [ ] **Bài 1 (Trung bình):** Build chat app đơn giản với WebSocket (2+ users)
- [ ] **Bài 2 (Trung bình):** Build live stock ticker dùng SSE
- [ ] **Bài 3 (Khó):** So sánh performance: WebSocket vs SSE vs Long Polling với 1000 clients

---

## Tài nguyên thêm

- [MDN — WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) — Browser API docs
- [MDN — SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) — EventSource docs
- [Socket.IO](https://socket.io/) — WebSocket library with fallbacks
- [WebSockets Deep Dive (Hussein Nasser)](https://www.youtube.com/watch?v=2Nt-ZrNP22A) — YouTube
