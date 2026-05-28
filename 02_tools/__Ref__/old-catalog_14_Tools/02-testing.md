# 🧪 Testing — Unit, Integration & E2E

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Code không có test = code không hoàn chỉnh

---

## Testing Pyramid

```
           /  E2E  \        ← Ít nhất, chậm nhất, test user flows
          /──────────\         (Playwright, Cypress)
         /Integration \      ← Vừa phải, test APIs, services
        /──────────────\        (Supertest, Pytest)
       /   Unit Tests   \    ← Nhiều nhất, nhanh nhất, test functions
      /──────────────────\      (Jest/Vitest, Pytest)
```

---

## Unit Testing — JavaScript/TypeScript

### Vitest (Hiện đại, tích hợp với Vite)

```bash
npm install -D vitest @vitest/ui
```

```typescript
// src/utils/formatPrice.ts
export function formatPrice(amount: number, currency: string = "VND"): string {
  if (amount < 0) throw new Error("Amount không thể âm")
  return new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency
  }).format(amount)
}

// src/utils/formatPrice.test.ts
import { describe, it, expect } from 'vitest'
import { formatPrice } from './formatPrice'

describe('formatPrice', () => {
  it('formats VND correctly', () => {
    expect(formatPrice(100000)).toBe('100.000 ₫')
  })

  it('formats USD correctly', () => {
    expect(formatPrice(99.99, 'USD')).toContain('99')
  })

  it('throws error for negative amount', () => {
    expect(() => formatPrice(-100)).toThrow('Amount không thể âm')
  })

  it('handles zero', () => {
    expect(formatPrice(0)).toContain('0')
  })
})
```

```typescript
// Testing async functions
import { vi } from 'vitest'

describe('UserService', () => {
  // Mock dependencies
  const mockUserRepo = {
    findByEmail: vi.fn(),
    create: vi.fn()
  }
  const userService = new UserService(mockUserRepo)

  beforeEach(() => {
    vi.clearAllMocks()  // Reset mocks trước mỗi test
  })

  it('returns user when email exists', async () => {
    const fakeUser = { id: '1', email: 'test@example.com', name: 'Test' }
    mockUserRepo.findByEmail.mockResolvedValue(fakeUser)

    const result = await userService.findByEmail('test@example.com')

    expect(mockUserRepo.findByEmail).toHaveBeenCalledWith('test@example.com')
    expect(result).toEqual(fakeUser)
  })

  it('throws NotFoundError when user does not exist', async () => {
    mockUserRepo.findByEmail.mockResolvedValue(null)

    await expect(
      userService.findByEmail('nobody@example.com')
    ).rejects.toThrow('User không tồn tại')
  })
})
```

### Jest (Phổ biến nhất)

```typescript
// jest.config.ts
export default {
  preset: 'ts-jest',
  testEnvironment: 'node',
  coverageThreshold: {
    global: { lines: 80, functions: 80, branches: 70 }
  }
}

// Snapshot testing
it('renders UserCard correctly', () => {
  const { container } = render(<UserCard user={mockUser} />)
  expect(container).toMatchSnapshot()
})
```

---

## Unit Testing — Python

### Pytest

```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

```python
# tests/unit/test_price_utils.py
import pytest
from app.utils.price import calculate_discount, format_price

class TestCalculateDiscount:
    def test_percentage_discount(self):
        result = calculate_discount(price=100_000, discount_percent=10)
        assert result == 90_000

    def test_maximum_discount_capped(self):
        """Không được giảm quá 70%"""
        result = calculate_discount(price=100_000, discount_percent=80)
        assert result == 30_000  # Tối thiểu 30% của giá gốc

    def test_zero_discount(self):
        assert calculate_discount(price=100_000, discount_percent=0) == 100_000

    def test_negative_price_raises(self):
        with pytest.raises(ValueError, match="Price phải dương"):
            calculate_discount(price=-1000, discount_percent=10)

    @pytest.mark.parametrize("price,pct,expected", [
        (100_000, 10, 90_000),
        (200_000, 25, 150_000),
        (50_000, 50, 25_000),
    ])
    def test_various_discounts(self, price, pct, expected):
        assert calculate_discount(price, pct) == expected


# tests/unit/test_user_service.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.fixture
def mock_user_repo():
    return AsyncMock()

@pytest.fixture
def user_service(mock_user_repo):
    return UserService(repo=mock_user_repo)

@pytest.mark.asyncio
async def test_create_user_success(user_service, mock_user_repo):
    mock_user_repo.find_by_email.return_value = None
    mock_user_repo.create.return_value = User(id="1", email="test@example.com")
    
    result = await user_service.create("Test", "test@example.com", "Pass123!")
    
    mock_user_repo.create.assert_called_once()
    assert result.email == "test@example.com"

@pytest.mark.asyncio
async def test_create_user_duplicate_email(user_service, mock_user_repo):
    mock_user_repo.find_by_email.return_value = User(id="existing")
    
    with pytest.raises(DuplicateEmailError):
        await user_service.create("Test", "existing@example.com", "Pass123!")
```

---

## Integration Testing — API Tests

### Python (FastAPI + httpx)

```python
# tests/integration/conftest.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5432/test_db"

@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db(test_engine):
    async with AsyncSession(test_engine) as session:
        yield session
        await session.rollback()  # Rollback sau mỗi test

@pytest.fixture
async def client(db):
    app.dependency_overrides[get_db] = lambda: db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def authenticated_client(client, db):
    """Client đã đăng nhập"""
    user = await create_test_user(db)
    token = create_access_token(str(user.id), user.role)
    client.headers["Authorization"] = f"Bearer {token}"
    yield client, user
```

```python
# tests/integration/test_posts_api.py
import pytest

@pytest.mark.asyncio
async def test_create_post(authenticated_client):
    client, user = authenticated_client
    
    response = await client.post("/api/v1/posts", json={
        "title": "My Test Post",
        "content": "Some content here",
        "tags": ["python", "testing"]
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "My Test Post"
    assert data["data"]["authorId"] == str(user.id)
    assert "password" not in data["data"]  # Không leak sensitive data

@pytest.mark.asyncio
async def test_list_posts_pagination(authenticated_client, db):
    client, _ = authenticated_client
    # Tạo 15 posts
    for i in range(15):
        await create_test_post(db, title=f"Post {i}")
    
    response = await client.get("/api/v1/posts?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 10
    assert data["pagination"]["total"] >= 15
    assert data["pagination"]["hasNext"] is True

@pytest.mark.asyncio
async def test_delete_post_forbidden(authenticated_client, db):
    """User không thể xóa post của người khác"""
    client, current_user = authenticated_client
    other_post = await create_test_post(db, author_id="other-user-id")
    
    response = await client.delete(f"/api/v1/posts/{other_post.id}")
    assert response.status_code == 403
```

### Node.js (Supertest)

```typescript
import request from 'supertest'
import app from '../src/index'

describe('POST /api/v1/users', () => {
  it('creates a new user successfully', async () => {
    const res = await request(app)
      .post('/api/v1/users')
      .send({
        name: 'Jesse',
        email: 'jesse@example.com',
        password: 'Password123!',
        age: 25
      })
      .expect(201)

    expect(res.body.success).toBe(true)
    expect(res.body.data.email).toBe('jesse@example.com')
    expect(res.body.data).not.toHaveProperty('password')
  })

  it('returns 409 for duplicate email', async () => {
    await createTestUser({ email: 'existing@example.com' })
    
    const res = await request(app)
      .post('/api/v1/users')
      .send({ email: 'existing@example.com', ... })
      .expect(409)

    expect(res.body.error.code).toBe('DUPLICATE_EMAIL')
  })
})
```

---

## E2E Testing — Playwright

```bash
npm install -D @playwright/test
npx playwright install
```

```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Authentication Flow', () => {
  test('user can register and login', async ({ page }) => {
    // Register
    await page.goto('/register')
    await page.fill('[data-testid="name-input"]', 'Jesse')
    await page.fill('[data-testid="email-input"]', 'jesse@example.com')
    await page.fill('[data-testid="password-input"]', 'Password123!')
    await page.click('[data-testid="register-btn"]')
    
    // Redirect after register
    await expect(page).toHaveURL('/dashboard')
    await expect(page.getByText('Xin chào, Jesse')).toBeVisible()
    
    // Logout
    await page.click('[data-testid="logout-btn"]')
    await expect(page).toHaveURL('/login')
    
    // Login
    await page.fill('[data-testid="email-input"]', 'jesse@example.com')
    await page.fill('[data-testid="password-input"]', 'Password123!')
    await page.click('[data-testid="login-btn"]')
    
    await expect(page).toHaveURL('/dashboard')
  })

  test('shows error for wrong credentials', async ({ page }) => {
    await page.goto('/login')
    await page.fill('[data-testid="email-input"]', 'wrong@example.com')
    await page.fill('[data-testid="password-input"]', 'wrongpassword')
    await page.click('[data-testid="login-btn"]')
    
    await expect(page.getByText('Email hoặc mật khẩu không đúng')).toBeVisible()
  })
})

// tests/e2e/checkout.spec.ts
test('complete checkout flow', async ({ page }) => {
  await loginAs(page, 'customer@example.com')
  
  await page.goto('/products')
  await page.click('[data-testid="product-1"] .add-to-cart')
  await page.click('[data-testid="cart-icon"]')
  await page.click('[data-testid="checkout-btn"]')
  
  await page.fill('[data-testid="card-number"]', '4242 4242 4242 4242')
  await page.fill('[data-testid="card-expiry"]', '12/28')
  await page.fill('[data-testid="card-cvc"]', '123')
  await page.click('[data-testid="pay-btn"]')
  
  await expect(page.getByText('Đặt hàng thành công')).toBeVisible({ timeout: 10000 })
  await expect(page).toHaveURL(/\/orders\/\d+/)
})
```

---

## Test Data & Fixtures

```python
# tests/factories.py — dùng factory_boy
import factory
from app.models import User, Post

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    id = factory.LazyFunction(lambda: str(uuid4()))
    name = factory.Faker("name", locale="vi_VN")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password_hash = factory.LazyFunction(lambda: hash_password("Password123!"))
    is_active = True
    role = "user"

class PostFactory(factory.Factory):
    class Meta:
        model = Post
    
    title = factory.Faker("sentence", nb_words=5)
    content = factory.Faker("paragraph", nb_sentences=5)
    author = factory.SubFactory(UserFactory)

# Dùng trong tests
user = UserFactory()
admin = UserFactory(role="admin")
posts = PostFactory.create_batch(10, author=user)
```

---

## CI — Chạy tests tự động

```yaml
# .github/workflows/test.yml
- name: Run tests with coverage
  run: |
    pytest tests/ -v \
      --cov=app \
      --cov-report=term-missing \
      --cov-fail-under=80 \
      -p no:warnings

# Fail nếu coverage < 80%
```

---

## Bài tập thực hành

- [ ] Viết unit tests cho tất cả utility functions
- [ ] Integration tests cho CRUD API (create, read, update, delete)
- [ ] E2E test flow đăng ký → đăng nhập → đặt hàng
- [ ] Setup coverage minimum 80% trong CI

---

## Tài nguyên thêm

- [Vitest Docs](https://vitest.dev/)
- [Pytest Docs](https://docs.pytest.org/)
- [Playwright Docs](https://playwright.dev/)
- [Testing Library](https://testing-library.com/) — Test React components
