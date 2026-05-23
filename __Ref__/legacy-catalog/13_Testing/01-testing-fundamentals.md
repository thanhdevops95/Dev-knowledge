# Testing Fundamentals — Pytest, Jest, E2E

> **Tags:** `testing` `pytest` `jest` `vitest` `playwright` `tdd` `mocking` `coverage`
> **Level:** Intermediate | **Prerequisite:** `python/01-python-basics.md` or `javascript/01-js-basics.md`

---

## 1. Testing Pyramid

```
        /\
       /e2e\         Few (slow, expensive, high confidence)
      /------\
     / integr\       More (test multiple units together)
    /----------\
   / unit tests \    Many (fast, isolated, cheap)
  /--------------\
  
Unit tests:        Test a single function/class in isolation
Integration:       Test multiple components working together (API + DB)
E2E:               Test entire flow from user's perspective (browser)
```

---

## 2. Pytest — Python Testing

```python
# conftest.py — shared fixtures across test files
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import Base, get_db

# ─── Database fixtures ────────────────────────────────────────────
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    """Use shared event loop for all async tests"""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()

@pytest.fixture(autouse=True)  # Runs for EVERY test automatically
async def clean_db(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db(test_engine) -> AsyncSession:
    session_factory = async_sessionmaker(test_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session

@pytest.fixture
async def client(db) -> AsyncClient:
    """HTTP client with overridden DB dependency"""
    async def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        yield client
    
    app.dependency_overrides.clear()

# ─── Factory fixtures ─────────────────────────────────────────────
@pytest.fixture
async def create_user(db):
    """Factory fixture — return function to create test users"""
    async def _create(name="Test User", email="test@example.com", role="user", **kwargs):
        from app.models import User
        from app.auth import hash_password
        
        user = User(name=name, email=email, role=role,
                    hashed_password=hash_password("Password123"), **kwargs)
        db.add(user)
        await db.flush()
        return user
    
    return _create

@pytest.fixture
async def auth_client(client, create_user):
    """Authenticated HTTP client"""
    user = await create_user(email="auth@example.com")
    
    resp = await client.post("/auth/login", json={
        "email": "auth@example.com",
        "password": "Password123",
    })
    token = resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    client.state = type("State", (), {"user": user})()
    return client
```

```python
# tests/test_users.py
import pytest
from httpx import AsyncClient

# Basic test
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/users", json={
        "name": "Alice",
        "email": "alice@example.com",
        "password": "Password123",
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["name"] == "Alice"
    assert "password" not in data         # Never expose password!
    assert "id" in data

# Parametrize — run same test with multiple inputs
@pytest.mark.parametrize("email,expected_status", [
    ("valid@example.com", 201),
    ("invalid-email", 422),         # Pydantic validation error
    ("", 422),                       # Empty email
    ("a" * 256 + "@example.com", 422),  # Too long
])
@pytest.mark.asyncio
async def test_create_user_email_validation(client: AsyncClient, email: str, expected_status: int):
    response = await client.post("/users", json={
        "name": "Test",
        "email": email,
        "password": "Password123",
    })
    assert response.status_code == expected_status

# Test with factory fixture
@pytest.mark.asyncio
async def test_cannot_login_wrong_password(client: AsyncClient, create_user):
    await create_user(email="bob@example.com")
    
    response = await client.post("/auth/login", json={
        "email": "bob@example.com",
        "password": "WrongPassword",
    })
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

# Test requiring auth
@pytest.mark.asyncio
async def test_get_profile_requires_auth(client: AsyncClient):
    response = await client.get("/users/me")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_profile(auth_client: AsyncClient):
    response = await auth_client.get("/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "auth@example.com"

# Unit test — no HTTP
def test_password_hashing():
    from app.auth import hash_password, verify_password
    
    hashed = hash_password("MyPassword123")
    
    assert hashed != "MyPassword123"       # Not stored plain!
    assert verify_password("MyPassword123", hashed)
    assert not verify_password("WrongPassword", hashed)

# Test with mocking
@pytest.mark.asyncio
async def test_send_welcome_email(auth_client: AsyncClient, mocker):
    mock_email = mocker.patch("app.services.email.send_email")
    
    response = await auth_client.post("/users", json={
        "name": "Carol",
        "email": "carol@example.com",
        "password": "Password123",
    })
    
    assert response.status_code == 201
    mock_email.assert_called_once_with(
        to="carol@example.com",
        subject="Welcome!",
        body=mocker.ANY,  # Don't care about exact body
    )
```

---

## 3. Jest / Vitest — JavaScript Testing

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,           // describe/it/expect without imports
    environment: 'node',     // or 'jsdom' for browser-like tests
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      thresholds: { lines: 80, branches: 80 },
    },
  },
});

// src/test/setup.ts
import { beforeEach, afterEach } from 'vitest';
import { mockReset } from 'vitest-mock-extended';

// Reset mocks between tests
beforeEach(() => {
  vi.clearAllMocks();
});
```

```typescript
// src/services/user.service.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserService } from './user.service';

// Mock the whole module
vi.mock('../repositories/user.repository');
vi.mock('../services/email.service');

import { UserRepository } from '../repositories/user.repository';
import { EmailService } from '../services/email.service';

describe('UserService', () => {
  let userService: UserService;
  let mockRepo: vi.Mocked<UserRepository>;
  let mockEmail: vi.Mocked<EmailService>;

  beforeEach(() => {
    mockRepo = new UserRepository() as vi.Mocked<UserRepository>;
    mockEmail = new EmailService() as vi.Mocked<EmailService>;
    userService = new UserService(mockRepo, mockEmail);
  });

  describe('createUser', () => {
    it('creates user and sends welcome email', async () => {
      const userData = { name: 'Alice', email: 'alice@example.com', password: 'Pass123!' };
      const savedUser = { id: 1, ...userData, createdAt: new Date() };
      
      mockRepo.create.mockResolvedValue(savedUser);
      mockEmail.sendWelcome.mockResolvedValue(undefined);

      const result = await userService.createUser(userData);

      expect(result).toMatchObject({ id: 1, name: 'Alice' });
      expect(mockRepo.create).toHaveBeenCalledWith(
        expect.objectContaining({ email: 'alice@example.com' })
      );
      expect(mockEmail.sendWelcome).toHaveBeenCalledWith('alice@example.com', 'Alice');
    });

    it('throws if email already exists', async () => {
      mockRepo.findByEmail.mockResolvedValue({ id: 99 } as any);

      await expect(userService.createUser({
        name: 'Bob', email: 'exists@example.com', password: 'Pass123!'
      })).rejects.toThrow('Email already registered');
      
      expect(mockRepo.create).not.toHaveBeenCalled();
    });

    it.each([
      ['short password', 'ab'],
      ['no uppercase', 'password123'],
      ['no digit', 'Password!'],
    ])('validates password: %s', async (_, password) => {
      await expect(userService.createUser({
        name: 'Test', email: 'test@example.com', password
      })).rejects.toThrow();
    });
  });
});

// Testing with timers
describe('RateLimiter', () => {
  beforeEach(() => {
    vi.useFakeTimers();   // Control time!
  });
  
  afterEach(() => {
    vi.useRealTimers();
  });

  it('resets counter after window expires', async () => {
    const limiter = new RateLimiter({ max: 3, windowMs: 60_000 });
    
    limiter.check('user-1');
    limiter.check('user-1');
    limiter.check('user-1');
    expect(() => limiter.check('user-1')).toThrow(RateLimitExceeded);
    
    // Fast-forward 1 minute
    vi.advanceTimersByTime(60_000);
    
    // Should work again
    expect(() => limiter.check('user-1')).not.toThrow();
  });
});
```

---

## 4. React Testing Library

```typescript
// components/LoginForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    mockOnSubmit.mockReset();
  });

  it('renders email and password fields', () => {
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /log in/i })).toBeInTheDocument();
  });

  it('shows validation errors on empty submit', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    await user.click(screen.getByRole('button', { name: /log in/i }));
    
    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/password is required/i)).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('calls onSubmit with credentials on valid input', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={mockOnSubmit} />);
    
    await user.type(screen.getByLabelText(/email/i), 'alice@example.com');
    await user.type(screen.getByLabelText(/password/i), 'Password123');
    await user.click(screen.getByRole('button', { name: /log in/i }));
    
    expect(mockOnSubmit).toHaveBeenCalledWith({
      email: 'alice@example.com',
      password: 'Password123',
    });
  });

  it('shows loading state during submission', async () => {
    mockOnSubmit.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));
    const user = userEvent.setup();
    
    render(<LoginForm onSubmit={mockOnSubmit} />);
    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'Password123');
    
    await user.click(screen.getByRole('button', { name: /log in/i }));
    
    expect(screen.getByRole('button', { name: /logging in/i })).toBeDisabled();
    
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /log in/i })).not.toBeDisabled();
    });
  });
});
```

---

## 5. Playwright — E2E Testing

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  baseURL: 'http://localhost:3000',
  use: {
    trace: 'on-first-retry',    // Capture trace on retry for debugging
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'mobile-safari', use: { ...devices['iPhone 13'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});

// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('user can login and see dashboard', async ({ page }) => {
    await page.goto('/login');
    
    // Fill form
    await page.getByLabel('Email').fill('alice@example.com');
    await page.getByLabel('Password').fill('Password123');
    await page.getByRole('button', { name: 'Log In' }).click();
    
    // Should redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
  });

  test('shows error on invalid credentials', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Email').fill('wrong@example.com');
    await page.getByLabel('Password').fill('WrongPass');
    await page.getByRole('button', { name: 'Log In' }).click();
    
    await expect(page.getByText('Invalid credentials')).toBeVisible();
    await expect(page).toHaveURL('/login');  // Stay on login page
  });
});

// Page Object Model (POM) — organize E2E tests
class LoginPage {
  constructor(private page: Page) {}
  
  async goto() { await this.page.goto('/login'); }
  async login(email: string, password: string) {
    await this.page.getByLabel('Email').fill(email);
    await this.page.getByLabel('Password').fill(password);
    await this.page.getByRole('button', { name: 'Log In' }).click();
  }
  async getErrorMessage() {
    return this.page.getByRole('alert').textContent();
  }
}

// Fixtures for shared state
test.describe('Order Flow', () => {
  test.use({ storageState: 'playwright/.auth/user.json' });  // Pre-authenticated!
  
  test('user can add to cart and checkout', async ({ page }) => {
    const cartPage = new CartPage(page);
    
    await page.goto('/products');
    await page.getByTestId('product-1').getByRole('button', { name: 'Add to Cart' }).click();
    
    await cartPage.goto();
    await expect(cartPage.getItemCount()).resolves.toBe(1);
    
    await cartPage.checkout();
    await expect(page).toHaveURL('/order-confirmation');
  });
});
```

---

## 6. TDD — Red-Green-Refactor

```
1. RED:    Write a FAILING test first (test the desired behavior)
2. GREEN:  Write MINIMUM code to make test pass
3. REFACTOR: Clean up code while tests stay green

Example — TDD for password validator:
```

```python
# Step 1: RED — Write test first
def test_password_requires_uppercase():
    with pytest.raises(ValueError, match="uppercase"):
        validate_password("password123")

def test_password_requires_digit():
    with pytest.raises(ValueError, match="digit"):
        validate_password("Password!!")

def test_password_minimum_length():
    with pytest.raises(ValueError, match="8 characters"):
        validate_password("Pass1")

def test_valid_password_passes():
    # Should not raise
    validate_password("Password123")

# Step 2: GREEN — Minimal implementation
def validate_password(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Must be at least 8 characters")
    if not any(c.isupper() for c in password):
        raise ValueError("Must contain at least one uppercase letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Must contain at least one digit")
    return password

# Step 3: REFACTOR — Improve code quality
from dataclasses import dataclass

@dataclass
class PasswordRule:
    check: callable
    error: str

PASSWORD_RULES = [
    PasswordRule(lambda p: len(p) >= 8, "Must be at least 8 characters"),
    PasswordRule(lambda p: any(c.isupper() for c in p), "Must contain at least one uppercase letter"),
    PasswordRule(lambda p: any(c.isdigit() for c in p), "Must contain at least one digit"),
]

def validate_password(password: str) -> str:
    for rule in PASSWORD_RULES:
        if not rule.check(password):
            raise ValueError(rule.error)
    return password
# Tests still pass! ✅
```

---

## 7. Code Coverage

```bash
# Python — pytest-cov
pytest --cov=app --cov-report=html --cov-report=term-missing
pytest --cov=app --cov-fail-under=80   # Fail if < 80% coverage

# JavaScript — Vitest
vitest run --coverage

# Playwright — built-in
npx playwright test --reporter=html

# What coverage measures:
# Line:     Was this line executed?
# Branch:   Was both if/else branches hit?
# Function: Was each function called?
# Statement: Was each statement executed?

# Important: 100% coverage ≠ bug-free code!
# Coverage shows what's NOT tested, not that what IS tested is correct.
# Aim for 80%+ line coverage, focus on branch coverage for critical logic.
```

---

*Tài liệu liên quan: `python/04-python-testing.md` | `javascript/02-js-advanced.md` | `fastapi/02-fastapi-advanced.md`*
