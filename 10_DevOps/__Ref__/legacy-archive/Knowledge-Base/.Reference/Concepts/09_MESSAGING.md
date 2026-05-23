# 09. Message Queues & Pub/Sub

[← Real-time](08_REALTIME.md) | [Tiếp: Architecture →](10_ARCHITECTURE.md)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Message Queue** | - | Hàng đợi tin nhắn - Nơi lưu trữ message chờ xử lý |
| **Pub/Sub** | - | Publish/Subscribe - Mô hình gửi tin nhắn đến nhiều subscriber |
| **Producer** | - | Bên gửi - Service tạo và gửi message |
| **Consumer** | - | Bên nhận - Service nhận và xử lý message |
| **Broker** | - | Trung gian - Hệ thống quản lý và định tuyến message |
| **Topic** | - | Chủ đề - Kênh để phân loại message trong Pub/Sub |
| **Partition** | - | Phân vùng - Chia topic thành nhiều phần để xử lý song song |
| **FIFO** | - | First In First Out - Xử lý theo thứ tự vào trước ra trước |
| **RabbitMQ** | - | Hệ thống message queue phổ biến |
| **Kafka** | - | Nền tảng streaming sự kiện phân tán |
| **Exchange** | - | Thành phần trong RabbitMQ định tuyến message đến queue |
| **Consumer Group** | - | Nhóm consumer cùng xử lý message từ một topic |

---

# 🤔 Tại sao DevOps cần biết Message Queues?

## Nỗi đau thực tế

> "Request POST order mất 30 giây vì phải gửi email, update inventory, notify..."

> "Service A gọi Service B, B chết → A cũng chết theo"

> "Flash sale: đơn hàng đổ về quá nhanh, database không xử lý kịp"

## Kiến thức này giúp bạn

| Tình huống | Cần biết |
|------------|----------|
| Tách biệt các service | Pub/Sub decoupling |
| Xử lý background jobs | Message Queue, workers |
| Handle traffic spikes | Queue buffering |
| Event-driven architecture | Kafka, event streaming |
| Đảm bảo tin nhắn không mất | Message persistence, acknowledgment |

Message Queues là xương sống của microservices architecture và event-driven systems. Hiểu về chúng giúp bạn xây dựng hệ thống loose-coupled và resilient.

---

# 🔄 Asynchronous Communication

## Sync vs Async

```
Synchronous:
Client ──request──► Service ──wait──► Response
                    (blocking)

Asynchronous:
Client ──message──► Queue ──► Consumer processes later
       (non-blocking)        (decoupled)
```

---

## Tại sao cần Async?

| Benefit | Mô tả |
|---------|-------|
| **Decoupling** | Services không cần biết về nhau |
| **Resilience** | Queue buffers khi downstream slow |
| **Scalability** | Scale consumers independently |
| **Peak handling** | Absorb traffic spikes |

---

# 📦 Message Queues

## Message Queue là gì?

**Message Queue** chứa và delivers messages giữa producers và consumers theo **point-to-point** model.

```
┌─────────────────────────────────────────────────────────────┐
│                    MESSAGE QUEUE                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Producers            Queue               Consumers          │
│                                                              │
│  ┌───────┐         ┌─────────────┐       ┌───────────┐      │
│  │ App 1 │──msg───►│ [M1][M2][M3]│──────►│ Consumer 1│      │
│  └───────┘         │             │       └───────────┘      │
│                    │   FIFO      │                           │
│  ┌───────┐         │   Queue     │       ┌───────────┐      │
│  │ App 2 │──msg───►│             │──────►│ Consumer 2│      │
│  └───────┘         └─────────────┘       └───────────┘      │
│                                                              │
│  ⚠️ Each message delivered to ONE consumer only             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## RabbitMQ

**RabbitMQ** là popular open-source message broker implementing AMQP protocol.

### Key Concepts

```
Producer → Exchange → Binding → Queue → Consumer
```

| Concept | Mô tả |
|---------|-------|
| **Exchange** | Receives messages, routes to queues |
| **Queue** | Stores messages |
| **Binding** | Rules connecting exchange to queue |
| **Consumer** | Receives and processes messages |

### Use Cases

- Task queues (background jobs)
- RPC (Remote Procedure Call)
- Notifications

---

# 📢 Publish-Subscribe (Pub/Sub)

## Pub/Sub là gì?

Publishers gửi messages đến **topics**, và **all subscribers** của topic đó nhận message.

```
┌─────────────────────────────────────────────────────────────┐
│                      PUBLISH-SUBSCRIBE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Publishers            Topic              Subscribers        │
│                                                              │
│  ┌───────┐         ┌─────────────┐       ┌───────────┐      │
│  │Pub 1  │──msg───►│             │──────►│   Sub 1   │      │
│  └───────┘         │   "orders"  │       └───────────┘      │
│                    │    Topic    │                           │
│  ┌───────┐         │             │──────►┌───────────┐      │
│  │Pub 2  │──msg───►│             │       │   Sub 2   │      │
│  └───────┘         └─────────────┘       └───────────┘      │
│                          │                                   │
│                          └──────►┌───────────┐              │
│                                  │   Sub 3   │              │
│                                  └───────────┘              │
│                                                              │
│  ⚠️ Each message delivered to ALL subscribers               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Apache Kafka

**Kafka** là distributed event streaming platform.

### Key Concepts

```
┌─────────────────────────────────────────────────────────────┐
│                       KAFKA                                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Topic: "orders"                                             │
│  ┌─────────────────────────────────────────┐                │
│  │ Partition 0: [msg1][msg2][msg3][msg4]   │                │
│  │ Partition 1: [msg5][msg6][msg7]         │                │
│  │ Partition 2: [msg8][msg9]               │                │
│  └─────────────────────────────────────────┘                │
│                                                              │
│  Consumer Group A:                                           │
│    Consumer 1 ← reads Partition 0                           │
│    Consumer 2 ← reads Partition 1, 2                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Features

| Feature | Mô tả |
|---------|-------|
| **Durable** | Messages persisted to disk |
| **Scalable** | Partitioning for parallelism |
| **Replayable** | Consumers can re-read messages |
| **High throughput** | Millions of messages/sec |

---

# 📊 Message Queue vs Pub/Sub

| Aspect | Message Queue | Pub/Sub |
|--------|---------------|---------|
| **Delivery** | One consumer | All subscribers |
| **Pattern** | Point-to-point | Broadcast |
| **Coupling** | Tighter | Looser |
| **Example** | RabbitMQ | Kafka |
| **Use case** | Task distribution | Event notification |

---

[← Real-time](08_REALTIME.md) | [Tiếp: Architecture →](10_ARCHITECTURE.md)
