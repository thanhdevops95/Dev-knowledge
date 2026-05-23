# Clean Architecture

> **Tags:** `architecture` `clean-architecture` `ddd` `hexagonal` `solid` `di`
> **Level:** Advanced | **Prerequisite:** `architecture/patterns/02-design-patterns.md`

---

## 1. The Problem with Bad Architecture

```
Common pitfalls:
  - Business logic in database ORM models
  - HTTP handlers directly calling SQL queries
  - Tests require running the entire server + database
  - Changing one feature breaks unrelated features
  - Impossible to test business logic without infrastructure
  
Signs of spaghetti architecture:
  - import everywhere (controllers import models directly)
  - God classes/functions (UserService does everything user-related)
  - "It works, but don't touch it"
```

---

## 2. Clean Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frameworks & Drivers                     │
│    (Web, DB, UI, External Services — most volatile)              │
│ ┌────────────────────────────────────────────────────────────┐   │
│ │                    Interface Adapters                       │   │
│ │    (Controllers, Gateways, Presenters)                      │   │
│ │ ┌────────────────────────────────────────────────────┐    │   │
│ │ │              Application Business Rules             │   │   │
│ │ │    (Use Cases, Interactors)                          │   │   │
│ │ │ ┌──────────────────────────────────────────────┐   │   │   │
│ │ │ │          Enterprise Business Rules            │   │   │   │
│ │ │ │    (Entities, Core Domain — most stable)      │   │   │   │
│ │ │ └──────────────────────────────────────────────┘   │   │   │
│ │ └────────────────────────────────────────────────────┘    │   │
│ └────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

Dependency Rule: Dependencies only point INWARD.
  Outer layers know about inner layers, NEVER the reverse!
  
  Wrong: Order entity imports from database
  Right: Database module imports Order entity
```

---

## 3. Layers in Practice

### Layer 1: Entities (Domain Objects)
```python
# domain/entities/order.py
# Pure Python — NO imports from database, HTTP, or external services

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

class OrderStatus(Enum):
    PENDING   = "pending"
    CONFIRMED = "confirmed"
    SHIPPED   = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

@dataclass
class Money:
    amount: Decimal
    currency: str = "USD"
    
    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __mul__(self, factor: int | Decimal) -> 'Money':
        return Money(self.amount * Decimal(str(factor)), self.currency)

@dataclass
class OrderItem:
    product_id: str
    name: str
    quantity: int
    unit_price: Money
    
    @property
    def subtotal(self) -> Money:
        return self.unit_price * self.quantity

@dataclass
class Order:
    id: str
    customer_id: str
    items: list[OrderItem]
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    # Domain logic lives HERE (not in services or controllers)
    @property
    def total(self) -> Money:
        if not self.items:
            return Money(Decimal("0"))
        total = self.items[0].unit_price * 0  # Zero in correct currency
        for item in self.items:
            total = Money(total.amount + item.subtotal.amount, total.currency)
        return total
    
    def confirm(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise ValueError(f"Can only confirm pending orders, current: {self.status}")
        self.status = OrderStatus.CONFIRMED
    
    def cancel(self, reason: str = "") -> None:
        if self.status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            raise ValueError(f"Cannot cancel shipped/delivered orders")
        self.status = OrderStatus.CANCELLED
    
    def add_item(self, item: OrderItem) -> None:
        if self.status != OrderStatus.PENDING:
            raise ValueError("Can only modify pending orders")
        self.items.append(item)
    
    def is_cancellable(self) -> bool:
        return self.status not in (OrderStatus.SHIPPED, OrderStatus.DELIVERED, OrderStatus.CANCELLED)
```

### Layer 2: Use Cases (Application Business Rules)
```python
# application/use_cases/create_order.py
from dataclasses import dataclass
from typing import Protocol

# Ports (interfaces) — defined in application layer
class OrderRepository(Protocol):
    async def save(self, order: Order) -> None: ...
    async def find_by_id(self, order_id: str) -> Order | None: ...
    async def find_by_customer(self, customer_id: str) -> list[Order]: ...

class ProductCatalog(Protocol):
    async def get_product(self, product_id: str) -> Product | None: ...

class PaymentGateway(Protocol):
    async def charge(self, order: Order, payment_token: str) -> PaymentResult: ...

class EventPublisher(Protocol):
    async def publish(self, event: DomainEvent) -> None: ...

# INPUT (DTO)
@dataclass
class CreateOrderCommand:
    customer_id: str
    items: list[dict]   # [{product_id, quantity}]
    payment_token: str

# OUTPUT (DTO)
@dataclass
class OrderResult:
    order_id: str
    total: Decimal
    status: str

# USE CASE — contains APPLICATION-level business logic
class CreateOrderUseCase:
    def __init__(
        self,
        order_repo: OrderRepository,
        product_catalog: ProductCatalog,
        payment_gateway: PaymentGateway,
        event_publisher: EventPublisher,
    ):
        self.order_repo = order_repo
        self.product_catalog = product_catalog
        self.payment_gateway = payment_gateway
        self.event_publisher = event_publisher
    
    async def execute(self, command: CreateOrderCommand) -> OrderResult:
        # 1. Validate and build items
        order_items = []
        for item_data in command.items:
            product = await self.product_catalog.get_product(item_data["product_id"])
            if not product:
                raise ValueError(f"Product {item_data['product_id']} not found")
            
            order_items.append(OrderItem(
                product_id=product.id,
                name=product.name,
                quantity=item_data["quantity"],
                unit_price=Money(product.price),
            ))
        
        # 2. Create order (domain object handles validation)
        order = Order(
            id=generate_id(),
            customer_id=command.customer_id,
            items=order_items,
        )
        
        # 3. Process payment (external side effect)
        payment_result = await self.payment_gateway.charge(order, command.payment_token)
        if not payment_result.success:
            raise PaymentError(payment_result.error_message)
        
        # 4. Confirm order (domain logic)
        order.confirm()
        
        # 5. Persist
        await self.order_repo.save(order)
        
        # 6. Publish domain event
        await self.event_publisher.publish(OrderCreatedEvent(
            order_id=order.id,
            customer_id=order.customer_id,
            total=order.total.amount,
        ))
        
        return OrderResult(
            order_id=order.id,
            total=order.total.amount,
            status=order.status.value,
        )
```

### Layer 3: Interface Adapters
```python
# adapters/api/order_controller.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/orders", tags=["orders"])

# HTTP request/response models (NOT same as domain entities!)
class CreateOrderRequest(BaseModel):
    items: list[dict]
    payment_token: str

class OrderResponse(BaseModel):
    order_id: str
    total: float
    status: str

@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    request: CreateOrderRequest,
    current_user=Depends(get_current_user),
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
):
    try:
        result = await use_case.execute(CreateOrderCommand(
            customer_id=current_user.id,
            items=request.items,
            payment_token=request.payment_token,
        ))
        return OrderResponse(
            order_id=result.order_id,
            total=float(result.total),
            status=result.status,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PaymentError as e:
        raise HTTPException(status_code=402, detail=str(e))
```

### Layer 4: Infrastructure (Database, HTTP, etc.)
```python
# infrastructure/repositories/sqlalchemy_order_repo.py
from sqlalchemy.ext.asyncio import AsyncSession
from application.ports import OrderRepository

class SQLAlchemyOrderRepository:
    """Concrete implementation of OrderRepository using SQLAlchemy"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, order: Order) -> None:
        # Map domain entity to ORM model
        db_order = OrderModel(
            id=order.id,
            customer_id=order.customer_id,
            status=order.status.value,
            created_at=order.created_at,
        )
        
        for item in order.items:
            db_item = OrderItemModel(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=float(item.unit_price.amount),
            )
            db_order.items.append(db_item)
        
        self.session.add(db_order)
        await self.session.flush()
    
    async def find_by_id(self, order_id: str) -> Order | None:
        result = await self.session.execute(
            select(OrderModel).options(selectinload(OrderModel.items))
            .filter(OrderModel.id == order_id)
        )
        db_order = result.scalar_one_or_none()
        
        if not db_order:
            return None
        
        # Map ORM model back to domain entity
        return self._to_domain(db_order)
    
    def _to_domain(self, db_order: OrderModel) -> Order:
        return Order(
            id=db_order.id,
            customer_id=db_order.customer_id,
            status=OrderStatus(db_order.status),
            items=[
                OrderItem(
                    product_id=item.product_id,
                    name=item.name,
                    quantity=item.quantity,
                    unit_price=Money(Decimal(str(item.unit_price))),
                )
                for item in db_order.items
            ],
            created_at=db_order.created_at,
        )
```

---

## 4. Dependency Injection Container

```python
# infrastructure/container.py
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession

class Container:
    """Wires all dependencies together"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    @lru_cache
    def order_repository(self) -> OrderRepository:
        return SQLAlchemyOrderRepository(self.db)
    
    @lru_cache
    def product_catalog(self) -> ProductCatalog:
        return HttpProductCatalog(settings.CATALOG_URL)
    
    @lru_cache  
    def payment_gateway(self) -> PaymentGateway:
        return StripePaymentGateway(settings.STRIPE_SECRET_KEY)
    
    @lru_cache
    def event_publisher(self) -> EventPublisher:
        return KafkaEventPublisher(settings.KAFKA_URL)
    
    @lru_cache
    def create_order_use_case(self) -> CreateOrderUseCase:
        return CreateOrderUseCase(
            order_repo=self.order_repository(),
            product_catalog=self.product_catalog(),
            payment_gateway=self.payment_gateway(),
            event_publisher=self.event_publisher(),
        )

# FastAPI DI
async def get_container(db: AsyncSession = Depends(get_db)) -> Container:
    return Container(db)

async def get_create_order_use_case(
    container: Container = Depends(get_container)
) -> CreateOrderUseCase:
    return container.create_order_use_case()
```

---

## 5. Testing — The Benefit

```python
# Test use cases without any framework, database, or HTTP!
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_create_order_success():
    # Arrange: mock all external dependencies
    product = MagicMock(id="prod-1", name="Widget", price=Decimal("29.99"))
    
    mock_catalog = AsyncMock()
    mock_catalog.get_product.return_value = product
    
    mock_payment = AsyncMock()
    mock_payment.charge.return_value = MagicMock(success=True)
    
    mock_repo = AsyncMock()
    mock_publisher = AsyncMock()
    
    use_case = CreateOrderUseCase(mock_repo, mock_catalog, mock_payment, mock_publisher)
    
    # Act
    result = await use_case.execute(CreateOrderCommand(
        customer_id="cust-123",
        items=[{"product_id": "prod-1", "quantity": 2}],
        payment_token="tok_test_123",
    ))
    
    # Assert
    assert result.total == Decimal("59.98")
    assert result.status == "confirmed"
    mock_repo.save.assert_called_once()
    mock_publisher.publish.assert_called_once()

@pytest.mark.asyncio
async def test_create_order_with_invalid_product():
    mock_catalog = AsyncMock()
    mock_catalog.get_product.return_value = None  # Product not found!
    
    use_case = CreateOrderUseCase(mock_catalog, AsyncMock(), AsyncMock(), AsyncMock())
    
    with pytest.raises(ValueError, match="Product prod-1 not found"):
        await use_case.execute(CreateOrderCommand(
            customer_id="cust-123",
            items=[{"product_id": "prod-1", "quantity": 1}],
            payment_token="tok_test",
        ))

def test_order_cannot_confirm_non_pending_order():
    # Test domain entity logic — pure Python, no mocking needed
    order = Order(id="ord-1", customer_id="cust-1", items=[...])
    order.status = OrderStatus.SHIPPED
    
    with pytest.raises(ValueError, match="Can only confirm pending orders"):
        order.confirm()
```

---

## 6. Folder Structure

```
src/
├── domain/                  # Layer 1: Entities & Domain Logic
│   ├── entities/
│   │   ├── order.py
│   │   ├── user.py
│   │   └── product.py
│   ├── events/
│   │   ├── order_events.py
│   │   └── user_events.py
│   └── value_objects/
│       └── money.py
│
├── application/             # Layer 2: Use Cases
│   ├── use_cases/
│   │   ├── create_order.py
│   │   ├── cancel_order.py
│   │   └── get_user_orders.py
│   └── ports/               # Interfaces for external dependencies
│       ├── repositories.py  # Abstract repository interfaces
│       ├── event_publisher.py
│       └── payment.py
│
├── adapters/                # Layer 3: Interface Adapters
│   ├── api/
│   │   ├── order_controller.py
│   │   └── user_controller.py
│   └── cli/
│       └── admin_commands.py
│
├── infrastructure/          # Layer 4: Frameworks & Drivers
│   ├── database/
│   │   ├── models.py        # ORM models
│   │   └── repositories.py  # Concrete implementations
│   ├── http/
│   │   ├── product_catalog_client.py
│   │   └── payment_gateway.py
│   ├── messaging/
│   │   └── kafka_publisher.py
│   └── container.py         # DI wiring
│
└── tests/
    ├── unit/                # Test entities + use cases (fast, no infra)
    ├── integration/         # Test repositories + external services
    └── e2e/                 # Test full HTTP flows
```

---

## 7. Hexagonal Architecture (Ports & Adapters)

```
                    ┌─────────────────────────┐
                    │    Application Core      │
        ┌──────────▶│   (Domain + Use Cases)  │◀──────────┐
        │           │                          │            │
        │           └─────────────────────────┘            │
        │                    Port (Interface)               │
        │                        ▼                          │
    Adapter                 Application                 Adapter
  (HTTP REST)             uses ports only           (SQLAlchemy)
    Adapter                                           Adapter
    (CLI)                                            (Kafka)
    Adapter                                           Adapter
    (GraphQL)                                       (S3 Storage)

"Driving" adapters (left): trigger use cases (HTTP, CLI, Tests)
"Driven" adapters (right): called by use cases (DB, Email, Payment)
```

---

*Tài liệu liên quan: `architecture/patterns/02-design-patterns.md` | `testing/01-testing-fundamentals.md` | `fastapi/02-fastapi-advanced.md`*
