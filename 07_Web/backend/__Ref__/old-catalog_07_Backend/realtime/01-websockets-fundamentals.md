# 🔄 WebSockets & Realtime

> `[INTERMEDIATE]` — Khi HTTP không đủ — push data từ server về client

---

## HTTP vs WebSocket vs SSE

```
HTTP (Request/Response):
  Client ──► Server: "Có tin nhắn mới không?"
  Server ──► Client: "Không"
  ...lặp lại mỗi vài giây (polling) → Rất tốn tài nguyên

WebSocket (Bidirectional):
  Client ←──────────────→ Server (1 connection liên tục)
  Server chủ động push data về client
  → Chat, game, collaboration editors

Server-Sent Events / SSE (One-way push):
  Client ←──────────── Server (1 connection, server push)
  → Notifications, live feeds, AI streaming responses
```

---

## WebSocket — Protocol cơ bản

```
1. HTTP Handshake:
   GET /ws HTTP/1.1
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Key: ...

2. Server đồng ý:
   HTTP/1.1 101 Switching Protocols
   Upgrade: websocket

3. TCP connection giữ nguyên → gửi nhận frames
```

---

## WebSocket Server — Python (FastAPI)

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json

app = FastAPI()

class ConnectionManager:
    """Quản lý tất cả WebSocket connections"""
    
    def __init__(self):
        # room_id → set of websockets
        self.rooms: Dict[str, Set[WebSocket]] = {}
        # websocket → user info
        self.users: Dict[WebSocket, dict] = {}
    
    async def connect(self, websocket: WebSocket, room_id: str, user: dict):
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        self.rooms[room_id].add(websocket)
        self.users[websocket] = {"room_id": room_id, **user}
        
        # Thông báo cho room có người mới join
        await self.broadcast_to_room(room_id, {
            "type": "user_joined",
            "user": user,
            "online_count": len(self.rooms[room_id])
        }, exclude=websocket)
    
    def disconnect(self, websocket: WebSocket):
        user_info = self.users.pop(websocket, {})
        room_id = user_info.get("room_id")
        if room_id and room_id in self.rooms:
            self.rooms[room_id].discard(websocket)
            if not self.rooms[room_id]:
                del self.rooms[room_id]
        return user_info
    
    async def send_to_user(self, websocket: WebSocket, message: dict):
        try:
            await websocket.send_json(message)
        except Exception:
            pass
    
    async def broadcast_to_room(
        self, room_id: str, message: dict, exclude: WebSocket | None = None
    ):
        if room_id not in self.rooms:
            return
        dead_connections = set()
        for ws in self.rooms[room_id].copy():
            if ws == exclude:
                continue
            try:
                await ws.send_json(message)
            except Exception:
                dead_connections.add(ws)
        # Cleanup dead connections
        for ws in dead_connections:
            self.disconnect(ws)

manager = ConnectionManager()

@app.websocket("/ws/chat/{room_id}")
async def chat_websocket(
    websocket: WebSocket,
    room_id: str,
    token: str  # Lấy từ query param
):
    # Verify token
    try:
        payload = verify_token(token)
        user = {"id": payload["sub"], "name": payload["name"]}
    except ValueError:
        await websocket.close(code=4001, reason="Unauthorized")
        return
    
    await manager.connect(websocket, room_id, user)
    
    try:
        while True:
            # Nhận message từ client
            data = await websocket.receive_json()
            
            match data.get("type"):
                case "message":
                    message_content = data.get("content", "").strip()
                    if not message_content:
                        continue
                    
                    # Lưu vào database
                    msg = await save_message(room_id, user["id"], message_content)
                    
                    # Broadcast cho cả room
                    await manager.broadcast_to_room(room_id, {
                        "type": "message",
                        "id": str(msg.id),
                        "content": message_content,
                        "author": user,
                        "timestamp": msg.created_at.isoformat()
                    })
                
                case "typing":
                    # Thông báo đang gõ cho người khác
                    await manager.broadcast_to_room(room_id, {
                        "type": "typing",
                        "user": user
                    }, exclude=websocket)
    
    except WebSocketDisconnect:
        user_info = manager.disconnect(websocket)
        await manager.broadcast_to_room(room_id, {
            "type": "user_left",
            "user": user,
            "online_count": len(manager.rooms.get(room_id, set()))
        })
```

---

## WebSocket Client — JavaScript

```typescript
class ChatClient {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnects = 5
  private listeners: Map<string, Function[]> = new Map()

  constructor(
    private roomId: string,
    private token: string
  ) {}

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      const url = `wss://api.example.com/ws/chat/${this.roomId}?token=${this.token}`
      this.ws = new WebSocket(url)

      this.ws.onopen = () => {
        console.log('Connected!')
        this.reconnectAttempts = 0
        resolve()
      }

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        this.emit(data.type, data)
      }

      this.ws.onclose = (event) => {
        console.log('Disconnected:', event.code, event.reason)
        if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnects) {
          this.scheduleReconnect()
        }
      }

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        reject(error)
      }
    })
  }

  private scheduleReconnect() {
    const delay = Math.min(1000 * 2 ** this.reconnectAttempts, 30000)
    this.reconnectAttempts++
    console.log(`Reconnecting in ${delay}ms...`)
    setTimeout(() => this.connect(), delay)
  }

  sendMessage(content: string) {
    this.send({ type: 'message', content })
  }

  startTyping() {
    this.send({ type: 'typing' })
  }

  private send(data: object) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data))
    }
  }

  on(eventType: string, handler: Function) {
    if (!this.listeners.has(eventType)) {
      this.listeners.set(eventType, [])
    }
    this.listeners.get(eventType)!.push(handler)
  }

  private emit(eventType: string, data: object) {
    this.listeners.get(eventType)?.forEach(handler => handler(data))
  }

  disconnect() {
    this.ws?.close(1000, 'User disconnected')
  }
}

// Dùng
const chat = new ChatClient('room-123', userToken)
await chat.connect()

chat.on('message', (data) => {
  addMessageToUI(data)
})

chat.on('typing', (data) => {
  showTypingIndicator(data.user.name)
})

chat.on('user_joined', (data) => {
  showNotification(`${data.user.name} đã tham gia`)
})

sendButton.onclick = () => {
  chat.sendMessage(messageInput.value)
  messageInput.value = ''
}
```

---

## React Hook cho WebSocket

```typescript
// hooks/useWebSocket.ts
import { useEffect, useRef, useCallback, useState } from 'react'

interface UseWebSocketOptions {
  onMessage: (data: any) => void
  onConnect?: () => void
  onDisconnect?: () => void
}

export function useWebSocket(url: string, options: UseWebSocketOptions) {
  const wsRef = useRef<WebSocket | null>(null)
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    const ws = new WebSocket(url)
    wsRef.current = ws

    ws.onopen = () => {
      setConnected(true)
      options.onConnect?.()
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      options.onMessage(data)
    }

    ws.onclose = () => {
      setConnected(false)
      options.onDisconnect?.()
    }

    return () => ws.close()
  }, [url])

  const send = useCallback((data: object) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data))
    }
  }, [])

  return { send, connected }
}
```

---

## Server-Sent Events (SSE) — AI Streaming

```python
# FastAPI SSE — phù hợp cho AI streaming
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

@app.get("/api/ai/stream")
async def stream_ai_response(prompt: str):
    async def generate():
        async for chunk in call_openai_stream(prompt):
            # SSE format: "data: {json}\n\n"
            yield f"data: {json.dumps({'token': chunk})}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )
```

```typescript
// Client — đọc SSE stream
async function streamAIResponse(prompt: string, onToken: (token: string) => void) {
  const response = await fetch('/api/ai/stream?prompt=' + encodeURIComponent(prompt))
  const reader = response.body!.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const chunk = decoder.decode(value)
    const lines = chunk.split('\n').filter(l => l.startsWith('data: '))
    
    for (const line of lines) {
      const data = line.slice(6)
      if (data === '[DONE]') return
      const { token } = JSON.parse(data)
      onToken(token)
    }
  }
}

// Dùng
let fullResponse = ''
await streamAIResponse(prompt, (token) => {
  fullResponse += token
  updateUI(fullResponse)
})
```

---

## Khi nào dùng gì?

| | WebSocket | SSE | Long Polling |
|---|---|---|---|
| **Hướng** | Hai chiều | Server → Client | Server → Client |
| **Use case** | Chat, game | Notifications, AI stream | Simple updates |
| **Complexity** | Cao | Thấp | Thấp |
| **Scale** | Cần Redis Pub/Sub | Dễ hơn | Dễ nhất |
| **Proxy/Firewall** | Đôi khi bị block | HTTP, ít vấn đề | HTTP, ít vấn đề |

---

## Scale WebSocket với Redis Pub/Sub

```python
# Vấn đề: user A kết nối server 1, user B kết nối server 2
# → Cần Redis để sync messages giữa các servers

import redis.asyncio as aioredis

redis_client = aioredis.from_url("redis://localhost")

@app.websocket("/ws/chat/{room_id}")
async def chat_ws(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id, user)
    
    # Subscribe Redis channel cho room này
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(f"room:{room_id}")
    
    async def listen_redis():
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                await manager.broadcast_to_room(room_id, data)
    
    asyncio.create_task(listen_redis())
    
    try:
        while True:
            data = await websocket.receive_json()
            # Publish lên Redis → tất cả servers nhận
            await redis_client.publish(f"room:{room_id}", json.dumps(data))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await pubsub.unsubscribe(f"room:{room_id}")
```

---

## Bài tập thực hành

- [ ] Build chat app đơn giản (1 room, nhiều users)
- [ ] Thêm typing indicator và online user count
- [ ] Implement reconnect logic với exponential backoff
- [ ] Scale với Redis Pub/Sub (2 server instances)

---

## Tài nguyên thêm

- [FastAPI WebSocket Docs](https://fastapi.tiangolo.com/advanced/websockets/)
- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [Socket.io](https://socket.io/) — Thư viện WebSocket phổ biến (Node.js)
- [Ably](https://ably.com/) — Managed WebSocket service
