# 🔌 WebSocket & SSE — Giao tiếp thời gian thực

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Hiểu và triển khai real-time communication

---

## Tại sao cần Real-time?

Trong web truyền thống, client phải **hỏi đi hỏi lại** (polling) server để biết có gì mới không. Giống như bạn cứ 5 giây lại mở hộp thư xem có thư mới — rất tốn năng lượng và chậm.

**Real-time** giải quyết vấn đề này: server **chủ động đẩy** data xuống client ngay khi có update. Giống như người giao thư gõ cửa nhà bạn khi có thư mới.

Có 3 cách phổ biến:

| Kỹ thuật | Chiều giao tiếp | Kết nối | Use case |
|---|---|---|---|
| **Polling** | Client → Server (lặp lại) | HTTP mới mỗi lần | Dashboard refresh mỗi 30s |
| **SSE** | Server → Client (1 chiều) | HTTP persistent | Live feed, notifications |
| **WebSocket** | Hai chiều ↔ | TCP persistent | Chat, game, collaboration |

Cách chọn phụ thuộc vào **bạn có cần client gửi data liên tục không**:
- Chỉ server push? → **SSE** (đơn giản hơn nhiều)
- Hai chiều, tần suất cao? → **WebSocket**
- Đơn giản, không cần real-time? → **Polling** (đừng over-engineer!)

---

## 1. Server-Sent Events (SSE) — Đơn giản nhất

### Tại sao SSE?

SSE được tích hợp sẵn trong trình duyệt qua `EventSource` API — không cần thư viện. Nó hoạt động trên HTTP thường, tự động reconnect khi mất kết nối, và hỗ trợ qua proxy/CDN dễ dàng hơn WebSocket.

**Điểm mạnh:** Đơn giản. Nếu bạn chỉ cần server đẩy data xuống (notifications, live feed, stock prices), SSE là lựa chọn tốt nhất.

**Điểm yếu:** Client không gửi ngược lên được (phải dùng fetch/POST riêng). Giới hạn 6 connections đồng thời per domain (HTTP/1.1).

### Server (Node.js)

```javascript
// SSE endpoint — giữ kết nối mở, gửi events liên tục
app.get('/api/events', (req, res) => {
    // Headers đặc biệt cho SSE
    res.writeHead(200, {
        'Content-Type': 'text/event-stream',   // Bắt buộc!
        'Cache-Control': 'no-cache',            // Không cache
        'Connection': 'keep-alive',             // Giữ kết nối
    });

    // Gửi event mỗi 3 giây
    const intervalId = setInterval(() => {
        const data = {
            time: new Date().toISOString(),
            temperature: (20 + Math.random() * 10).toFixed(1),
        };
        // Format SSE: "data: ..." kết thúc bằng 2 newlines
        res.write(`data: ${JSON.stringify(data)}\n\n`);
    }, 3000);

    // Client disconnect → cleanup
    req.on('close', () => {
        clearInterval(intervalId);
        console.log('Client disconnected');
    });
});
```

### Client (Browser)

```javascript
// EventSource — built-in, tự reconnect!
const source = new EventSource('/api/events');

source.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(`Nhiệt độ: ${data.temperature}°C`);
    // Update UI...
};

source.onerror = (err) => {
    console.error('SSE error:', err);
    // EventSource tự reconnect! Không cần code thêm.
};

// Cleanup khi component unmount (React)
// source.close();
```

### Ứng dụng thực tế của SSE

- **ChatGPT streaming**: Text được stream từng token qua SSE
- **Live notifications**: New order, new message
- **Dashboard metrics**: Real-time charts
- **CI/CD logs**: Build logs streaming

---

## 2. WebSocket — Giao tiếp hai chiều

### Tại sao WebSocket?

WebSocket tạo kết nối TCP liên tục giữa client và server. Sau handshake ban đầu (upgrade từ HTTP), cả hai bên có thể gửi data **bất kỳ lúc nào** mà không cần request/response. 

Điều này quan trọng khi:
- **Chat**: Cả 2 bên gửi tin nhắn
- **Collaborative editing**: Google Docs, Figma
- **Multiplayer game**: Input + state sync liên tục
- **Trading**: Real-time order book + place orders

**Trade-off so với SSE**: WebSocket mạnh hơn nhưng phức tạp hơn — cần quản lý connections, heartbeat, reconnect, và khó scale hơn (stateful).

### Server (Socket.io)

Socket.io là thư viện phổ biến nhất, cung cấp reconnect, rooms, namespaces, và fallback sang polling nếu WebSocket bị chặn.

```javascript
import { Server } from 'socket.io';
import { createServer } from 'http';

const httpServer = createServer(app);
const io = new Server(httpServer, {
    cors: { origin: 'http://localhost:3000' },
    // Tự fallback sang polling nếu WS bị chặn (corporate firewall)
});

// Middleware — xác thực trước khi cho connect
io.use((socket, next) => {
    const token = socket.handshake.auth.token;
    try {
        const user = verifyJWT(token);
        socket.data.user = user;  // Gắn user info vào socket
        next();
    } catch {
        next(new Error('Authentication failed'));
    }
});

io.on('connection', (socket) => {
    const user = socket.data.user;
    console.log(`${user.name} connected (${socket.id})`);

    // Join room theo userId → gửi message targeted
    socket.join(`user:${user.id}`);

    // Lắng nghe event từ client
    socket.on('chat:message', async (data) => {
        // data = { roomId: "room_1", text: "Hello!" }

        // Lưu DB
        const message = await db.messages.create({
            userId: user.id,
            roomId: data.roomId,
            text: data.text,
        });

        // Broadcast đến TẤT CẢ users trong room (trừ sender)
        socket.to(data.roomId).emit('chat:message', {
            id: message.id,
            userId: user.id,
            userName: user.name,
            text: data.text,
            createdAt: message.createdAt,
        });
    });

    // Typing indicator
    socket.on('chat:typing', (data) => {
        socket.to(data.roomId).emit('chat:typing', {
            userId: user.id,
            userName: user.name,
        });
    });

    // Join/leave rooms
    socket.on('room:join', (roomId) => {
        socket.join(roomId);
        socket.to(roomId).emit('room:user-joined', { userId: user.id });
    });

    socket.on('disconnect', (reason) => {
        console.log(`${user.name} disconnected: ${reason}`);
    });
});

httpServer.listen(3001);
```

### Client (React + Socket.io)

```javascript
import { io } from 'socket.io-client';
import { useEffect, useState, useCallback } from 'react';

// Custom hook — tái sử dụng cho nhiều components
function useSocket(url, token) {
    const [socket, setSocket] = useState(null);
    const [connected, setConnected] = useState(false);

    useEffect(() => {
        const s = io(url, {
            auth: { token },
            reconnection: true,          // Tự reconnect
            reconnectionDelay: 1000,     // Chờ 1s trước khi retry
            reconnectionAttempts: 10,    // Thử 10 lần
        });

        s.on('connect', () => setConnected(true));
        s.on('disconnect', () => setConnected(false));

        setSocket(s);
        return () => s.disconnect();     // Cleanup on unmount
    }, [url, token]);

    return { socket, connected };
}

// Chat component
function ChatRoom({ roomId }) {
    const { socket, connected } = useSocket('http://localhost:3001', authToken);
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        if (!socket) return;

        socket.emit('room:join', roomId);

        // Lắng nghe tin nhắn mới
        socket.on('chat:message', (msg) => {
            setMessages(prev => [...prev, msg]);
        });

        return () => {
            socket.off('chat:message');
        };
    }, [socket, roomId]);

    const sendMessage = useCallback((text) => {
        socket?.emit('chat:message', { roomId, text });
    }, [socket, roomId]);

    return (
        <div>
            <div>{connected ? '🟢 Online' : '🔴 Offline'}</div>
            {messages.map(m => <Message key={m.id} message={m} />)}
            <ChatInput onSend={sendMessage} />
        </div>
    );
}
```

---

## 3. Scaling WebSocket — Thách thức production

### Vấn đề: Stateful connections

WebSocket là **stateful** — mỗi client gắn với 1 server instance. Khi scale ra nhiều servers, user A kết nối server 1, user B kết nối server 2 → họ không thấy messages của nhau!

```
Vấn đề:
  User A ──WS──► Server 1    User A gửi "Hello"
  User B ──WS──► Server 2    User B KHÔNG nhận được!

Giải pháp: Redis Adapter
  User A ──WS──► Server 1 ──pub──► Redis ──sub──► Server 2 ──WS──► User B
                                       (Message broker)
```

```javascript
// Socket.io Redis adapter — giải quyết multi-server
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';

const pubClient = createClient({ url: 'redis://localhost:6379' });
const subClient = pubClient.duplicate();

await Promise.all([pubClient.connect(), subClient.connect()]);

io.adapter(createAdapter(pubClient, subClient));
// Giờ tất cả servers đều nhận events qua Redis!
```

### Heartbeat & Connection Management

Trong production, connections có thể "chết ngầm" (client mất mạng nhưng server không biết). Cần heartbeat:

```javascript
const io = new Server(httpServer, {
    pingInterval: 25000,   // Gửi ping mỗi 25s
    pingTimeout: 5000,     // Chờ pong 5s, không có → disconnect
});
```

---

## 4. Khi nào dùng gì?

| Tình huống | Chọn | Lý do |
|---|---|---|
| Notifications, live feed | **SSE** | Server push đơn giản, auto-reconnect |
| AI text streaming | **SSE** | OpenAI, ChatGPT đều dùng SSE |
| Chat, messaging | **WebSocket** | Hai chiều, low latency |
| Real-time game | **WebSocket** | Input + state sync liên tục |
| Dashboard refresh mỗi 30s | **Polling** | Đơn giản, không cần real-time |
| Collaborative editing | **WebSocket + CRDT** | Conflict resolution cần |
| IoT sensor data | **MQTT** (not WS) | Lightweight protocol cho embedded |

---

## Các lỗi thường gặp

**1. Không handle reconnection** — Mạng không ổn định. Luôn implement reconnect logic với exponential backoff.

**2. Memory leak** — Quên remove event listeners khi component unmount → events stack up.

**3. Dùng WebSocket khi SSE đủ** — Over-engineering. Nếu chỉ cần server push, SSE đơn giản và đáng tin cậy hơn.

**4. Không scale được** — WebSocket stateful. Production cần Redis adapter hoặc message broker.

**5. Gửi quá nhiều data** — Throttle/debounce events. Không gửi mouse position 60fps qua WebSocket!

---

## Bài tập thực hành

- [ ] SSE: Build live notification feed
- [ ] WebSocket: Build chat room với Socket.io (join/leave, typing indicator)
- [ ] Scale: Redis adapter cho multi-server Socket.io
- [ ] Compare: Implement cùng feature với cả SSE và WebSocket, so sánh

---

## Tài nguyên thêm

- [Socket.io Docs](https://socket.io/docs/v4/) — Official
- [MDN: Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [WebSockets vs SSE (web.dev)](https://web.dev/articles/eventsource-basics)
