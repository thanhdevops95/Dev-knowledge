# 🔔 Message Queues — Kafka & RabbitMQ

> `[INTERMEDIATE → ADVANCED]` — Giao tiếp async giữa các services

---

## Tại sao cần Message Queue?

**Vấn đề với synchronous communication:**
```
Service A ──── HTTP Call ────► Service B
   │
   ⌛ Phải chờ B xử lý xong mới tiếp tục
   💥 Nếu B down → A bị ảnh hưởng
   📈 B không đáp ứng kịp khi tải cao
```

**Giải pháp: Message Queue**
```
Service A ──── Publish ────► Queue ◄──── Consume ──── Service B
   │                                                       │
   ✅ Không chờ B                                         ✅ B xử lý theo tốc độ của mình
   ✅ B down → msg vẫn trong queue, xử lý sau             ✅ Scale consumers độc lập
   ✅ Decouple hoàn toàn
```

**Use cases:**
- Email/SMS/Push notification
- Payment processing
- Image/video processing (resize, transcode)
- Analytics event tracking
- Order fulfillment pipeline
- Microservices communication

---

## RabbitMQ — Traditional Message Broker

```bash
# Docker
docker run -d --name rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  -e RABBITMQ_DEFAULT_USER=admin \
  -e RABBITMQ_DEFAULT_PASS=password \
  rabbitmq:3-management

# Management UI: http://localhost:15672
```

### Python (pika)

```python
import pika
import json
from functools import wraps

# Connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        credentials=pika.PlainCredentials("admin", "password")
    )
)
channel = connection.channel()

# Declare exchange + queue (idempotent)
channel.exchange_declare(exchange="my_app", exchange_type="direct", durable=True)
channel.queue_declare(queue="emails", durable=True)  # Survive broker restart
channel.queue_bind(queue="emails", exchange="my_app", routing_key="email")

# PRODUCER — Publish message
def publish_event(event_type: str, payload: dict):
    channel.basic_publish(
        exchange="my_app",
        routing_key=event_type,
        body=json.dumps(payload),
        properties=pika.BasicProperties(
            content_type="application/json",
            delivery_mode=2,  # Make message persistent
        )
    )
    print(f"Published: {event_type} → {payload}")

publish_event("email", {
    "to": "user@example.com",
    "subject": "Xác nhận đơn hàng",
    "template": "order_confirmed",
    "order_id": "ord_123"
})

# CONSUMER — Process messages
def process_email(ch, method, properties, body):
    data = json.loads(body)
    try:
        # Gửi email thực tế
        send_email(data["to"], data["subject"], data["template"])
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge: xử lý xong
        print(f"Email sent to {data['to']}")
    except Exception as e:
        print(f"Failed: {e}")
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=True   # Đưa lại queue để retry
        )

channel.basic_qos(prefetch_count=1)  # Xử lý 1 message tại 1 thời điểm
channel.basic_consume(queue="emails", on_message_callback=process_email)
channel.start_consuming()
```

### Các loại Exchange

```
Direct Exchange   → Route theo routing_key chính xác
Topic Exchange    → Route theo pattern (order.* hoặc *.created)
Fanout Exchange   → Broadcast đến tất cả queues
Headers Exchange  → Route theo headers
```

---

## Apache Kafka — Distributed Event Streaming

Kafka mạnh hơn RabbitMQ cho:
- **Throughput cao** (millions msgs/sec)
- **Message retention** — Lưu messages (configurable, không xóa sau consume)
- **Replay** — Consumer đọc lại từ đầu bất kỳ lúc nào
- **Event sourcing, audit log**

```bash
# Docker Compose
version: '3'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    ports: ["9092:9092"]
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: 'true'
      KAFKA_LOG_RETENTION_HOURS: 168   # Giữ messages 7 ngày
```

### Python (kafka-python / confluent-kafka)

```python
from confluent_kafka import Producer, Consumer
import json

# PRODUCER
producer = Producer({'bootstrap.servers': 'localhost:9092'})

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()}[{msg.partition()}] offset {msg.offset()}")

def publish_event(topic: str, key: str, payload: dict):
    producer.produce(
        topic=topic,
        key=key.encode(),
        value=json.dumps(payload).encode(),
        callback=delivery_report
    )
    producer.flush()

# Publish events
publish_event("user-events", "user.created", {
    "event": "user.created",
    "user_id": "usr_123",
    "email": "jesse@example.com",
    "timestamp": "2026-02-19T14:00:00Z"
})

publish_event("order-events", "order.placed", {
    "event": "order.placed",
    "order_id": "ord_456",
    "user_id": "usr_123",
    "amount": 99000,
    "items": [{"product_id": "p1", "qty": 2}]
})
```

```python
# CONSUMER
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'email-service',  # Consumer group
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,   # Manual commit cho exactly-once
})

consumer.subscribe(['user-events', 'order-events'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        event = json.loads(msg.value().decode())
        print(f"Received [{msg.topic()}]: {event['event']}")

        # Process event
        match event.get('event'):
            case 'user.created':
                send_welcome_email(event['email'])
            case 'order.placed':
                send_order_confirmation(event['user_id'], event['order_id'])

        # Commit sau khi xử lý thành công
        consumer.commit(asynchronous=False)

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
```

### Kafka Concepts

```
Topic        = Danh mục messages (như queue nhưng persistent)
Partition    = Topic được chia thành partitions để parallel processing
Consumer Group = Nhiều consumers chia nhau đọc messages
Offset       = Vị trí của message trong partition
```

---

## Celery — Task Queue (Python)

```bash
pip install celery redis flower
```

```python
# celery_app.py
from celery import Celery

app = Celery(
    "my_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

app.conf.update(
    task_serializer="json",
    result_expires=3600,
    timezone="Asia/Ho_Chi_Minh",
    task_routes={
        "tasks.email.*": {"queue": "emails"},
        "tasks.image.*": {"queue": "images"},
    }
)

# tasks/email.py
from celery_app import app
from sendgrid import SendGridAPIClient

@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_task(self, to: str, subject: str, body: str):
    try:
        client = SendGridAPIClient(api_key=SENDGRID_KEY)
        client.send(to=to, subject=subject, body=body)
    except Exception as exc:
        raise self.retry(exc=exc)

@app.task
def process_image_task(image_path: str, sizes: list[int]):
    from PIL import Image
    img = Image.open(image_path)
    for size in sizes:
        img.resize((size, size)).save(f"{image_path}_{size}x{size}.webp")
```

```python
# Dispatch tasks từ API
from tasks.email import send_email_task
from tasks.image import process_image_task

# Async (fire & forget)
send_email_task.delay("user@example.com", "Subject", "Body")

# Với countdown (sau 5 phút)
send_email_task.apply_async(
    args=["user@example.com", "Follow-up", "..."],
    countdown=300
)

# Chained tasks
from celery import chain
chain(
    upload_to_s3.s(file_path),
    process_image_task.s([100, 200, 400]),
    send_notification.s(user_id)
).apply_async()
```

```bash
# Chạy worker
celery -A celery_app worker --loglevel=info -Q emails,images

# Flower UI — Monitor tasks
celery -A celery_app flower --port=5555
# http://localhost:5555
```

---

## Khi nào dùng cái nào?

| | RabbitMQ | Kafka | Celery |
|---|---|---|---|
| **Use case** | Task queue, RPC | Event streaming | Python task queue |
| **Message retention** | Xóa sau consume | Giữ N ngày | Xóa sau consume |
| **Throughput** | Cao | Rất cao | Trung bình |
| **Ordering** | Per-queue | Per-partition | Không |
| **Replay** | ❌ | ✅ | ❌ |
| **Độ khó** | Dễ | Phức tạp hơn | Rất dễ (Python) |
| **Dùng khi** | Event-driven services | Audit log, analytics | Python jobs |

---

## Bài tập thực hành

- [ ] Build email notification system với Celery + Redis
- [ ] Order pipeline: place order → inventory → payment → ship (Kafka)
- [ ] Dead letter queue – xử lý messages thất bại
- [ ] Consumer group load test với Kafka

---

## Tài nguyên thêm

- [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials)
- [Kafka: The Definitive Guide (free e-book)](https://www.confluent.io/resources/kafka-the-definitive-guide/)
- [Celery Docs](https://docs.celeryq.dev/)
