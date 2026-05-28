# 📬 Message Brokers — Kafka vs RabbitMQ

> `[INTERMEDIATE → ADVANCED]` — Giao tiếp giữa services bằng messages

---

## Tại sao cần Message Broker?

Trong monolith, các module gọi nhau bằng function calls — đơn giản, nhanh. Nhưng trong **microservices**, mỗi service là 1 process riêng trên server riêng. Gọi nhau bằng HTTP có vấn đề:

**Vấn đề 1: Tight coupling.** Order Service gọi trực tiếp Inventory Service, Email Service, Analytics Service... Nếu 1 service chết → request fail → order fail → user giận.

```
❌ Synchronous (tight coupling):
  Order Service → Inventory Service (500ms)
                → Email Service (TIMEOUT! 😫) → ORDER FAILS!
                → Analytics Service (200ms)
  
  Nếu Email Service chết → toàn bộ order flow fail.
  Nếu thêm Notification Service → phải sửa Order Service code!
```

**Vấn đề 2: Traffic spikes.** Black Friday: 10x orders → downstream services overwhelm → cascade failure.

**Message Broker giải quyết** bằng cách đặt "bưu điện" ở giữa:

```
✅ Asynchronous via Message Broker:
  Order Service → Message Broker → Inventory Service (consume khi sẵn sàng)
                                 → Email Service (consume khi sẵn sàng)
                                 → Analytics Service (consume khi sẵn sàng)
  
  Email Service chết? Messages chờ trong queue.
  Email Service sống lại? Process tất cả pending messages.
  Thêm Notification Service? Subscribe thôi, không sửa Order Service!
```

---

## 1. Hai mô hình chính

### Message Queue — Point-to-Point

Mỗi message được **1 consumer duy nhất** nhận. Giống bưu điện: thư gửi cho 1 người.

```
Producer ──message──► Queue ──message──► Consumer 1
                                   ──► Consumer 2 (load balanced)
                                   ──► Consumer 3 (load balanced)

Message "Order #123" → chỉ 1 trong 3 consumers nhận và xử lý.
Các consumers khác nhận messages KHÁC.
→ Dùng cho: task distribution, background jobs
```

### Pub/Sub — Publish/Subscribe

Mỗi message được **TẤT CẢ subscribers** nhận. Giống radio: ai tune vào đều nghe.

```
Publisher ──event──► Topic/Exchange ──event──► Subscriber 1 (Inventory)
                                   ──event──► Subscriber 2 (Email)
                                   ──event──► Subscriber 3 (Analytics)

Event "OrderCreated" → TẤT CẢ 3 subscribers đều nhận và xử lý.
→ Dùng cho: event broadcasting, notifications, analytics
```

---

## 2. RabbitMQ — "Smart broker, dumb consumers"

RabbitMQ là message broker truyền thống. Nó quản lý routing logic, đảm bảo delivery, và xóa messages sau khi consumed.

### Architecture

```
Producer → Exchange → Binding → Queue → Consumer

Exchange types:
  Direct:   Route theo exact routing key   (key="order.created" → queue1)
  Topic:    Route theo pattern             (key="order.*" → queue1, key="*.created" → queue2)
  Fanout:   Broadcast tất cả queues        (pub/sub)
  Headers:  Route theo message headers     (ít dùng)
```

### Node.js Implementation

```typescript
import amqp from 'amqplib';

// PRODUCER: gửi messages
async function publishOrder(order) {
    const connection = await amqp.connect('amqp://localhost');
    const channel = await connection.createChannel();
    
    // Declare exchange (tạo nếu chưa có)
    await channel.assertExchange('orders', 'topic', { durable: true });
    
    // Publish message
    channel.publish(
        'orders',                                 // Exchange name
        'order.created',                          // Routing key
        Buffer.from(JSON.stringify(order)),        // Message body
        {
            persistent: true,                     // Survive broker restart
            contentType: 'application/json',
            messageId: generateUUID(),            // Idempotency
            timestamp: Date.now(),
        },
    );
    
    console.log(`Published order ${order.id}`);
}

// CONSUMER: nhận messages
async function startInventoryConsumer() {
    const connection = await amqp.connect('amqp://localhost');
    const channel = await connection.createChannel();
    
    // Declare queue
    await channel.assertQueue('inventory-updates', { durable: true });
    
    // Bind queue to exchange with routing pattern
    await channel.bindQueue('inventory-updates', 'orders', 'order.*');
    // → Nhận mọi message có routing key bắt đầu bằng "order."
    
    // Prefetch: xử lý 1 message tại 1 thời điểm
    // (không overwhelm consumer — back-pressure)
    channel.prefetch(1);
    
    // Consume messages
    channel.consume('inventory-updates', async (msg) => {
        if (!msg) return;
        
        try {
            const order = JSON.parse(msg.content.toString());
            console.log('Processing order:', order.id);
            
            await updateInventory(order);
            
            // ACK: message xử lý thành công → xóa khỏi queue
            channel.ack(msg);
        } catch (error) {
            console.error('Failed to process:', error);
            // NACK: xử lý thất bại
            // requeue: true → đưa lại queue (retry)
            // requeue: false → gửi vào Dead Letter Queue
            channel.nack(msg, false, false);
        }
    });
}
```

### Key Concepts giải thích

**Acknowledgment (ACK):** Consumer phải **confirm** đã xử lý xong message. Nếu consumer crash trước khi ACK → RabbitMQ gửi lại message cho consumer khác. Đây là cách RabbitMQ đảm bảo **at-least-once delivery**.

**Prefetch:** Giới hạn số messages consumer nhận cùng lúc. Prefetch=1 → consumer nhận 1 message, xử lý xong mới nhận tiếp. Tránh consumer bị overwhelm.

**Persistent messages:** Lưu messages trên disk. Broker restart → messages không mất. Trade-off: chậm hơn in-memory.

---

## 3. Apache Kafka — "Dumb broker, smart consumers"

Kafka không phải message queue — nó là **distributed event log**. Khác biệt quan trọng:

- RabbitMQ: Message **xóa** sau khi consumed
- Kafka: Message **giữ lại** theo retention policy (7 ngày default). Consumers đọc bằng offset.

### Architecture

```
Topic: "orders" 
├── Partition 0: [msg0] [msg1] [msg2] [msg3] ──────────►
├── Partition 1: [msg0] [msg1] [msg2] ──────────────────►
└── Partition 2: [msg0] [msg1] [msg2] [msg3] [msg4] ───►
                                                     offset

Consumer Group A (Inventory Service):
  Consumer A1 → reads Partition 0
  Consumer A2 → reads Partition 1 + 2
  → Mỗi partition chỉ được 1 consumer trong group đọc!

Consumer Group B (Analytics Service):
  Consumer B1 → reads Partition 0 + 1 + 2
  → Consumer groups KHÔNG ảnh hưởng nhau (mỗi group có offset riêng)
```

**Tại sao partitions?** Scale horizontally. 1 partition = 1 consumer max. 10 partitions → 10 consumers đọc song song → 10x throughput.

### Node.js Implementation

```typescript
import { Kafka, Partitioners } from 'kafkajs';

const kafka = new Kafka({
    clientId: 'order-service',
    brokers: ['localhost:9092'],
});

// PRODUCER
const producer = kafka.producer({
    createPartitioner: Partitioners.DefaultPartitioner,
});

async function publishOrderEvent(order) {
    await producer.connect();
    
    await producer.send({
        topic: 'orders',
        messages: [
            {
                key: order.userId,    // Cùng userId → cùng partition → đảm bảo ORDER
                value: JSON.stringify({
                    eventType: 'ORDER_CREATED',
                    data: order,
                    timestamp: Date.now(),
                    eventId: generateUUID(),
                }),
                headers: {
                    'event-type': 'ORDER_CREATED',
                    'source': 'order-service',
                },
            },
        ],
    });
}

// CONSUMER
const consumer = kafka.consumer({ groupId: 'inventory-service' });

async function startConsumer() {
    await consumer.connect();
    await consumer.subscribe({ topic: 'orders', fromBeginning: false });
    
    await consumer.run({
        // eachMessage: xử lý từng message
        eachMessage: async ({ topic, partition, message }) => {
            const event = JSON.parse(message.value.toString());
            console.log(`
                Topic: ${topic}
                Partition: ${partition}
                Offset: ${message.offset}
                Event: ${event.eventType}
                Order: ${event.data.id}
            `);
            
            switch (event.eventType) {
                case 'ORDER_CREATED':
                    await reserveInventory(event.data);
                    break;
                case 'ORDER_CANCELLED':
                    await releaseInventory(event.data);
                    break;
            }
            
            // KafkaJS auto-commits offset sau khi eachMessage return
            // → Nếu crash trước return → message được re-process
        },
    });
}
```

### Kafka Key Concepts giải thích

**Consumer Group:** Mỗi group đọc **tất cả messages** nhưng share partitions giữa consumers trong group. 2 groups khác nhau đều đọc **tất cả** messages (không ảnh hưởng nhau). Đây là cách Kafka hỗ trợ cả Point-to-Point và Pub/Sub.

**Offset:** Vị trí đọc của consumer trong partition. Consumer track offset → biết đã đọc đến đâu. Restart? Tiếp tục từ last committed offset.

**Retention:** Messages giữ trong Kafka theo retention policy (7 ngày default, hoặc unlimited). Consumer mới? Có thể đọc lại TẤT CẢ events từ đầu (`fromBeginning: true`) — cực kỳ hữu ích cho event sourcing/replay.

---

## 4. RabbitMQ vs Kafka — Khi nào dùng gì?

| | RabbitMQ | Kafka |
|---|---|---|
| **Model** | Message Queue (smart broker) | Event Log (smart consumers) |
| **Message fate** | Xóa sau khi consumed | Giữ lại (retention) |
| **Throughput** | ~50K msg/s (single node) | ~1M msg/s (clustered) |
| **Ordering** | Per queue | Per partition |
| **Replay** | ❌ Không thể | ✅ Đọc lại bất kỳ lúc nào |
| **Routing** | Flexible (exchanges, patterns) | Simple (topics, partitions) |
| **Use case** | Task queues, RPC, complex routing | Event streaming, logs, analytics |
| **Complexity** | Trung bình | Cao (ZooKeeper/KRaft, partitions) |
| **Delay/Schedule** | ✅ Native plugin | ❌ Cần workaround |
| **Memory** | Thấp | Cao (depends on retention) |

**Decision framework:**

```
Cần task queue (background jobs)?           → RabbitMQ
Cần complex routing (topic/header-based)?   → RabbitMQ
Cần message replay / event sourcing?        → Kafka
Cần high throughput (>100K msg/s)?          → Kafka
Cần real-time streaming / analytics?        → Kafka
Cần delayed/scheduled messages?             → RabbitMQ
Team nhỏ, setup đơn giản?                  → RabbitMQ
Nhưng nếu không chắc?                      → RabbitMQ (đơn giản hơn để bắt đầu)
```

---

## 5. Best Practices

### Idempotent Consumers

Messages có thể gửi **nhiều lần** (network issues, retry). Consumer PHẢI idempotent:

```typescript
async function processOrder(event) {
    const { eventId, data } = event;
    
    // Check: đã xử lý event này chưa?
    const processed = await db.processedEvents.findOne({ eventId });
    if (processed) {
        console.log(`Event ${eventId} already processed, skipping`);
        return;
    }
    
    // Process
    await updateInventory(data);
    
    // Mark as processed
    await db.processedEvents.create({ eventId, processedAt: new Date() });
}
```

### Dead Letter Queue (DLQ)

Messages fail sau N retries → chuyển vào DLQ để review thủ công, không block queue chính:

```
Main Queue → Consumer → Fail → Retry (3x) → DLQ
                                              ↓
                                        Manual review
                                        Fix & reprocess
```

### Schema Evolution

Khi message format thay đổi, old consumers phải vẫn hoạt động:

```typescript
// v1: { orderId: "123", total: 100 }
// v2: { orderId: "123", total: 100, currency: "VND" }  ← thêm field

// Consumer phải handle cả v1 và v2
function processOrder(event) {
    const currency = event.data.currency || 'VND';  // Default cho v1
    // ...
}
```

---

## Bài tập thực hành

- [ ] RabbitMQ: pub/sub — order event → email + inventory consumers
- [ ] Kafka: setup local (Docker), produce/consume events
- [ ] Idempotency: demo duplicate messages + idempotent consumer
- [ ] DLQ: configure dead letter queue, verify failed messages go to DLQ

---

## Tài nguyên thêm

- [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials) — Official (interactive!)
- [Kafka Documentation](https://kafka.apache.org/documentation/) — Official
- [KafkaJS](https://kafka.js.org/) — Node.js client
- [CloudAMQP](https://www.cloudamqp.com/) — Managed RabbitMQ (free tier)
