# Microservices Architecture

> **Tags:** `microservices` `service-mesh` `api-gateway` `event-driven` `saga` `ddd`
> **Level:** Advanced | **Prerequisite:** `system-design/01-system-design.md`

---

## 1. Monolith vs Microservices

```
Monolith:                        Microservices:
┌────────────────────────┐        ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Web UI                 │        │  User   │ │  Order  │ │Payment  │
│ User Service           │        │ Service │ │ Service │ │ Service │
│ Order Service          │   →    └────┬────┘ └────┬────┘ └────┬────┘
│ Payment Service        │             │            │            │
│ Notification Service   │        ┌────▼────────────▼────────────▼────┐
│ Single Database        │        │         Message Bus / API Gateway  │
└────────────────────────┘        └────────────────────────────────────┘
```

### Khi nào dùng Microservices?

**Dùng Microservices khi:**
- Team lớn (Conway's Law: architecture mirrors team structure)
- Different services need different scaling (order service: 100x, payment: 10x)
- Different release cycles per service
- Different tech stacks needed per service
- Already has operational maturity (CI/CD, observability)

**Không nên dùng khi:**
- Team nhỏ (<20 engineers)
- Chưa hiểu domain rõ (tách boundary sai rất tốn kém)
- Không có DevOps culture/infrastructure
- Simple application

---

## 2. Domain-Driven Design (DDD)

DDD = methodology để xác định service boundaries dựa trên business domains:

### Bounded Context
```
E-commerce Domain:
  ┌──────────────────────┐  ┌──────────────────────┐
  │  Order Context       │  │  Catalog Context     │
  │  - Order (aggregate) │  │  - Product           │
  │  - OrderItem         │  │  - Category          │
  │  - OrderStatus       │  │  - Price             │
  │  "Product" = SKU     │  │  "Product" = listing │
  └──────────────────────┘  └──────────────────────┘
  
  Same word "Product" means DIFFERENT things in different contexts!
  → Each context has its own model, database, service
```

### Aggregates
```
Order (Aggregate Root)
  ├── OrderItem (Entity)  — cannot exist without Order
  ├── ShippingAddress (Value Object) — immutable, no identity
  └── OrderStatus (Value Object)

Rules:
  - Access entities only through Aggregate Root
  - Each aggregate has its own transaction boundary
  - Between aggregates: eventual consistency (events)
```

### Events (Domain Events)
```
When Order is placed:
  OrderPlaced event → 
    ├── InventoryService decrements stock
    ├── NotificationService sends confirmation email
    ├── PaymentService initiates payment
    └── AnalyticsService records sale
```

---

## 3. Service Communication Patterns

### Synchronous — REST/gRPC
```
Good for:
  - Queries (need immediate answer)
  - Operations requiring real-time response
  - Simple direct service-to-service calls

Bad for:
  - Long-running operations
  - Operations that don't need immediate response
  - High coupling between services
```

### Asynchronous — Message Queue
```
Good for:
  - Decoupling services
  - Long-running operations
  - Fan-out (1 event → many consumers)
  - Resilience (consumer can be down temporarily)

OrderService → [RabbitMQ/Kafka] → PaymentService
                                 → InventoryService
                                 → EmailService
```

### gRPC — High Performance RPC
```protobuf
// order.proto
syntax = "proto3";

service OrderService {
  rpc GetOrder(GetOrderRequest) returns (Order);
  rpc CreateOrder(CreateOrderRequest) returns (Order);
  rpc ListOrders(ListOrdersRequest) returns (stream Order);  // Server streaming
}

message Order {
  string id = 1;
  string user_id = 2;
  repeated OrderItem items = 3;
  double total = 4;
  string status = 5;
  google.protobuf.Timestamp created_at = 6;
}
```

---

## 4. API Gateway Pattern

```
Internet
    │
    ▼
┌─────────────────────────────────────┐
│             API Gateway             │
│  - Authentication/Authorization     │
│  - Rate Limiting                    │
│  - Request Routing                  │
│  - Load Balancing                   │
│  - Request/Response Transformation  │
│  - Circuit Breaking                 │
│  - SSL Termination                  │
│  - Caching                          │
│  - API Versioning                   │
└──┬──────────┬──────────┬────────────┘
   │          │          │
   ▼          ▼          ▼
User Svc  Order Svc  Payment Svc
```

### Kong Gateway Config
```yaml
# kong.yml
services:
  - name: user-service
    url: http://user-service:8080
    routes:
      - name: user-routes
        paths: ["/api/v1/users"]
        methods: ["GET", "POST", "PUT", "DELETE"]
    plugins:
      - name: jwt
      - name: rate-limiting
        config:
          minute: 100
          policy: local

  - name: order-service
    url: http://order-service:8080
    routes:
      - name: order-routes
        paths: ["/api/v1/orders"]
    plugins:
      - name: jwt
      - name: request-transformer
        config:
          add:
            headers: ["X-Service-Name: orders"]
```

---

## 5. Saga Pattern — Distributed Transactions

Problem: No single transaction across multiple services. **Saga** = sequence of local transactions coordinated by events or orchestration.

### Choreography Saga (Event-driven)
```
OrderService          InventoryService     PaymentService
     │                      │                   │
     │ PlaceOrder()          │                   │
     │─── OrderCreated ──────▶                   │
     │                       │ ReserveInventory()│
     │                       │── InventoryReserved─▶
     │                       │                   │ ProcessPayment()
     │                       │                   │ (success)
     │◀── PaymentProcessed ────────────────────────
     │ ConfirmOrder()        │                   │
     ▼                        ▼                   ▼

Compensating transactions (on failure):
PaymentFailed → InventoryService.ReleaseInventory() → OrderService.CancelOrder()
```

### Orchestration Saga (Central coordinator)
```python
class OrderSaga:
    """Orchestrator handles the entire saga"""
    
    def execute(self, order_id: str):
        try:
            # Step 1
            inventory_reserved = inventory_service.reserve(order_id)
            self.record_compensation(self.compensate_inventory, order_id)
            
            # Step 2
            payment_result = payment_service.charge(order_id)
            self.record_compensation(self.compensate_payment, payment_result.payment_id)
            
            # Step 3
            order_service.confirm(order_id)
            
        except InventoryError:
            self.rollback()   # No compensations needed yet
            
        except PaymentError:
            self.rollback()   # Runs compensate_inventory()
            
        except Exception:
            self.rollback()   # Runs all stored compensations in reverse
    
    def compensate_inventory(self, order_id):
        inventory_service.release(order_id)
    
    def compensate_payment(self, payment_id):
        payment_service.refund(payment_id)
```

---

## 6. Service Mesh — Istio

Service mesh = infrastructure layer for service-to-service communication, handles:
- mTLS (mutual TLS) automatically
- Circuit breaking
- Observability (traces, metrics)
- Traffic management (canary, A/B)
- Retries and timeouts

```yaml
# Traffic management: canary deployment (90% → v1, 10% → v2)
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: order-service
spec:
  hosts:
    - order-service
  http:
    - route:
        - destination:
            host: order-service
            subset: v1
          weight: 90
        - destination:
            host: order-service
            subset: v2
          weight: 10

---
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: order-service
spec:
  host: order-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: UPGRADE
    outlierDetection:            # Circuit breaking!
      consecutiveErrors: 5
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
```

---

## 7. Event-Driven Architecture with Kafka

```python
from kafka import KafkaProducer, KafkaConsumer
import json

# Producer (OrderService)
producer = KafkaProducer(
    bootstrap_servers=['kafka1:9092', 'kafka2:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',          # Wait for all replicas to acknowledge
    retries=3,
    max_in_flight_requests_per_connection=1  # Preserve order during retries
)

def publish_order_created(order: dict):
    producer.send(
        topic='order.created',
        key=str(order['id']).encode(),   # Key = partition key (orders by same user on same partition)
        value=order,
        headers=[
            ('event-type', b'OrderCreated'),
            ('correlation-id', correlation_id.encode()),
        ]
    )
    producer.flush()

# Consumer (InventoryService)
consumer = KafkaConsumer(
    'order.created',
    'order.cancelled',
    bootstrap_servers=['kafka1:9092', 'kafka2:9092'],
    group_id='inventory-service',           # Consumer group
    auto_offset_reset='earliest',
    enable_auto_commit=False,               # Manual commit!
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    try:
        topic = message.topic
        order = message.value
        
        if topic == 'order.created':
            reserve_inventory(order)
        elif topic == 'order.cancelled':
            release_inventory(order)
        
        # Commit only after successful processing
        consumer.commit()
        
    except Exception as e:
        # Don't commit → message will be reprocessed
        log.error(f"Failed to process message: {e}")
        send_to_dead_letter_queue(message)
        consumer.commit()  # Or not — depends on retry strategy
```

### Kafka Topics Design
```
Domain: orders
Topics:
  order.commands.create    ← Commands (request to do something)
  order.commands.cancel
  order.events.created     ← Events (something happened)
  order.events.confirmed
  order.events.cancelled
  order.events.shipped
  order.deadletter         ← Failed messages for inspection

Partitioning strategy:
  key = user_id → all orders for same user on same partition
  → Preserves ordering per user
```

---

## 8. Distributed Tracing

Every request gets a unique **trace ID** propagated across all services:

```python
# Using OpenTelemetry (standard)
from opentelemetry import trace
from opentelemetry.propagate import extract, inject
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup
provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4317")))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("order-service")

# FastAPI middleware (auto-instruments all requests)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
FastAPIInstrumentor.instrument_app(app)

# Manual spans
async def process_payment(order_id: str):
    with tracer.start_as_current_span("process-payment") as span:
        span.set_attributes({
            "order.id": order_id,
            "service.name": "payment-service",
        })
        
        try:
            result = await charge_card(order_id)
            span.set_attribute("payment.status", "success")
            return result
        except Exception as e:
            span.record_exception(e)
            span.set_status(StatusCode.ERROR)
            raise

# Propagate context to downstream service
async def call_inventory_service(order_id: str):
    headers = {}
    inject(headers)   # Adds traceparent header
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'http://inventory-service/reserve',
            json={'order_id': order_id},
            headers=headers    # traceparent propagated!
        )
```

**Visualization**: Jaeger, Zipkin, Grafana Tempo, AWS X-Ray

---

## 9. Health Checks & Graceful Shutdown

```python
# FastAPI health endpoints
@app.get("/health/live")
async def liveness():
    """Kubernetes liveness probe — am I alive? (not in deadlock)"""
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    """Kubernetes readiness probe — am I ready to serve traffic?"""
    # Check all dependencies
    checks = {}
    
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "error"
    
    try:
        redis.ping()
        checks["redis"] = "ok"
    except Exception:
        checks["redis"] = "error"
    
    all_healthy = all(v == "ok" for v in checks.values())
    status_code = 200 if all_healthy else 503
    
    return Response(
        content=json.dumps({"status": "ok" if all_healthy else "degraded", **checks}),
        status_code=status_code,
        media_type="application/json"
    )

# Graceful shutdown
import signal
import asyncio

shutdown_event = asyncio.Event()

def handle_shutdown(signum, frame):
    print("Graceful shutdown initiated...")
    shutdown_event.set()

signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

@app.on_event("shutdown")
async def shutdown():
    # 1. Stop accepting new requests (readiness probe fails → removed from load balancer)
    # 2. Wait for in-flight requests to complete
    # 3. Close connections (DB pool, Kafka consumer, etc.)
    await db_pool.close()
    await kafka_producer.stop()
    print("Graceful shutdown complete")
```

---

## 10. Microservices Checklist

| Concern | Solution |
|---|---|
| **Service discovery** | Kubernetes DNS, Consul, Eureka |
| **Configuration** | ConfigMap/Secrets, Vault, AWS SSM |
| **Authentication** | JWT at API Gateway, mTLS between services |
| **Circuit breaking** | Istio, Hystrix, Resilience4j |
| **Distributed tracing** | OpenTelemetry + Jaeger/Grafana |
| **Centralized logging** | EFK/ELK, Loki |
| **Metrics** | Prometheus + Grafana |
| **API gateway** | Kong, AWS API Gateway, Nginx |
| **Service mesh** | Istio, Linkerd |
| **Distributed transactions** | Saga pattern |
| **Caching** | Redis (per service) |
| **Testing** | Contract tests (Pact), end-to-end tests |

---

*Tài liệu liên quan: `system-design/01-system-design.md` | `system-design/05-distributed-systems.md` | `messaging/01-message-queues.md`*
