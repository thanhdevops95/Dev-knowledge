# 🔌 WebSocket — Giao tiếp hai chiều thời gian thực

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Hiểu cách chat, live notifications, game online hoạt động

---

## Tại sao cần WebSocket?

**HTTP** là giao thức **request-response**: client hỏi → server trả lời → xong.

Vấn đề: Nếu server có dữ liệu mới, **không thể chủ động** gửi cho client!

```
HTTP — Request/Response (pull):
Client: "Có tin nhắn mới không?" → Server: "Không"
Client: "Có tin nhắn mới không?" → Server: "Không"
Client: "Có tin nhắn mới không?" → Server: "Có! 1 tin nhắn"
→ Polling liên tục = lãng phí tài nguyên 😫

WebSocket — Full-duplex (push):
Client ◄═══════════════════► Server
    "Kết nối mở liên tục"
Server: "Có tin nhắn mới!" → Client nhận ngay!
Server: "User X online!" → Client nhận ngay!
→ Tiết kiệm, real-time ⚡
```

---

## 1. Cách WebSocket hoạt động

```
Phase 1: HTTP Upgrade (Handshake)
Client ──► GET /chat HTTP/1.1
           Upgrade: websocket
           Connection: Upgrade
           Sec-WebSocket-Key: x3JJHMbDL...

Server ◄── HTTP/1.1 101 Switching Protocols
           Upgrade: websocket
           Sec-WebSocket-Accept: HSmrc0sM...

Phase 2: Full-Duplex Communication
Client ◄═══════════════════► Server
         Frame: text/binary
         Ping/Pong (heartbeat)

Phase 3: Close
Client ──► Close Frame
Server ◄── Close Frame
           Connection closed
```

---

## 2. WebSocket Server (Node.js)

```javascript
const { WebSocketServer } = require('ws');

const wss = new WebSocketServer({ port: 8080 });

// Lưu tất cả clients đang kết nối
const clients = new Set();

wss.on('connection', (ws) => {
    clients.add(ws);
    console.log(`Client kết nối. Tổng: ${clients.size}`);

    // Nhận message từ client
    ws.on('message', (data) => {
        const message = JSON.parse(data);
        console.log('Nhận:', message);

        // Broadcast cho tất cả client khác
        clients.forEach(client => {
            if (client !== ws && client.readyState === 1) {
                client.send(JSON.stringify({
                    user: message.user,
                    text: message.text,
                    time: new Date().toISOString()
                }));
            }
        });
    });

    ws.on('close', () => {
        clients.delete(ws);
        console.log(`Client ngắt. Tổng: ${clients.size}`);
    });

    // Gửi welcome message
    ws.send(JSON.stringify({ text: 'Chào mừng đến phòng chat!' }));
});
```

---

## 3. WebSocket Client (Browser)

```javascript
const ws = new WebSocket('ws://localhost:8080');

ws.onopen = () => {
    console.log('Đã kết nối!');
    ws.send(JSON.stringify({ user: 'An', text: 'Xin chào mọi người!' }));
};

ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    console.log(`${message.user}: ${message.text}`);
};

ws.onclose = () => {
    console.log('Mất kết nối. Thử reconnect...');
    setTimeout(() => connectWebSocket(), 3000);  // Auto reconnect
};

ws.onerror = (error) => {
    console.error('Lỗi WebSocket:', error);
};
```

---

## 4. Socket.IO — WebSocket + fallbacks

**Socket.IO** = WebSocket + auto-reconnect + rooms + fallback to polling:

```javascript
// Server (Node.js)
const { Server } = require('socket.io');
const io = new Server(3000, { cors: { origin: '*' } });

io.on('connection', (socket) => {
    console.log('User connected:', socket.id);

    // Join room
    socket.on('join-room', (room) => {
        socket.join(room);
        socket.to(room).emit('user-joined', socket.id);
    });

    // Chat message
    socket.on('chat-message', ({ room, text }) => {
        io.to(room).emit('new-message', {
            user: socket.id,
            text,
            time: Date.now()
        });
    });

    socket.on('disconnect', () => {
        console.log('User disconnected:', socket.id);
    });
});

// Client
const socket = io('http://localhost:3000');
socket.emit('join-room', 'general');
socket.emit('chat-message', { room: 'general', text: 'Hello!' });
socket.on('new-message', (msg) => console.log(msg));
```

---

## 5. So sánh các giải pháp real-time

| | HTTP Polling | Long Polling | SSE | **WebSocket** |
|---|---|---|---|---|
| **Hướng** | Client → Server | Client → Server | Server → Client | **Hai chiều** |
| **Kết nối** | Mới mỗi request | Giữ đến có data | Giữ liên tục | Giữ liên tục |
| **Overhead** | Cao (headers lặp) | Trung bình | Thấp | **Thấp nhất** |
| **Use case** | Dashboard refresh | Notifications | News feed | **Chat, game, collab** |

### Server-Sent Events (SSE) — Khi chỉ cần server → client

```javascript
// Server (Node.js)
app.get('/events', (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');

    setInterval(() => {
        res.write(`data: ${JSON.stringify({ price: Math.random() * 100 })}\n\n`);
    }, 1000);
});

// Client
const source = new EventSource('/events');
source.onmessage = (event) => {
    console.log('Giá mới:', JSON.parse(event.data));
};
```

---

## 6. Best Practices

### Heartbeat / Ping-Pong

```javascript
// Server: Kiểm tra client còn sống
setInterval(() => {
    wss.clients.forEach(ws => {
        if (!ws.isAlive) {
            ws.terminate();
            return;
        }
        ws.isAlive = false;
        ws.ping();
    });
}, 30000);  // Mỗi 30 giây

// Client tự động pong (browser tự xử lý)
```

### Auto Reconnect với Exponential Backoff

```javascript
function connect() {
    const ws = new WebSocket('ws://localhost:8080');
    let retries = 0;

    ws.onopen = () => { retries = 0; };

    ws.onclose = () => {
        const delay = Math.min(1000 * 2 ** retries, 30000);
        console.log(`Reconnect trong ${delay}ms...`);
        setTimeout(connect, delay);
        retries++;
    };
}
```

---

## Các lỗi thường gặp

```
❌ Sai: Dùng WebSocket cho mọi thứ (kể cả REST API)
✅ Đúng: WebSocket cho real-time, REST cho CRUD thông thường

❌ Sai: Không xử lý reconnect → user mất kết nối vĩnh viễn
✅ Đúng: Auto reconnect với exponential backoff

❌ Sai: Broadcast raw strings → khó parse
✅ Đúng: Dùng JSON + message type: { type: "chat", data: {...} }
```

---

## Bài tập thực hành

- [ ] Xây chat room đơn giản: server + client, broadcast messages
- [ ] Thêm rooms (channels) vào chat app dùng Socket.IO
- [ ] Implement live stock ticker dùng SSE
- [ ] Xây collaborative text editor (nhiều người edit cùng lúc)

---

## Tài nguyên thêm

- [MDN — WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) — Official docs
- [Socket.IO Docs](https://socket.io/docs/v4/) — Library phổ biến nhất
- [WebSockets vs Long Polling](https://ably.com/blog/websockets-vs-long-polling) — So sánh chi tiết
