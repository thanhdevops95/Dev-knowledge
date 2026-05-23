# 🧪 Testing nâng cao — Integration, E2E, Mocking

> `[INTERMEDIATE → ADVANCED]` — Viết tests đáng tin cậy cho production

---

## 1. Testing Pyramid — Chiến lược

```
           /  E2E  \          ← Ít nhất, chậm nhất, đắt nhất
          /  Tests  \            (Playwright, Cypress)
         /───────────\
        / Integration \       ← Trung bình
       /    Tests      \        (Supertest, DB tests)
      /─────────────────\
     /    Unit Tests      \   ← Nhiều nhất, nhanh nhất, rẻ nhất
    /───────────────────────\   (Jest, Vitest, pytest)

Rule of thumb:
• Unit:        70% (logic, utils, pure functions)
• Integration: 20% (API endpoints, DB queries)
• E2E:         10% (critical user flows)
```

---

## 2. Integration Testing — API

```javascript
// Jest + Supertest — test Express API
import request from 'supertest';
import { app } from '../app';
import { db } from '../db';

beforeAll(async () => {
    await db.migrate.latest();     // Setup test DB
});

afterEach(async () => {
    await db('users').truncate();  // Clean between tests
});

afterAll(async () => {
    await db.destroy();            // Close connection
});

describe('POST /api/users', () => {
    it('should create user with valid data', async () => {
        const res = await request(app)
            .post('/api/users')
            .send({ name: 'An', email: 'an@mail.com' })
            .expect('Content-Type', /json/)
            .expect(201);

        expect(res.body.data).toMatchObject({
            name: 'An',
            email: 'an@mail.com',
        });
        expect(res.body.data.id).toBeDefined();

        // Verify in database
        const user = await db('users').where({ email: 'an@mail.com' }).first();
        expect(user).toBeTruthy();
    });

    it('should return 400 for invalid email', async () => {
        const res = await request(app)
            .post('/api/users')
            .send({ name: 'An', email: 'not-email' })
            .expect(400);

        expect(res.body.error).toContain('email');
    });

    it('should return 409 for duplicate email', async () => {
        await db('users').insert({ name: 'An', email: 'an@mail.com' });

        await request(app)
            .post('/api/users')
            .send({ name: 'Bình', email: 'an@mail.com' })
            .expect(409);
    });
});

describe('GET /api/users', () => {
    beforeEach(async () => {
        await db('users').insert([
            { name: 'An', email: 'an@mail.com' },
            { name: 'Bình', email: 'binh@mail.com' },
        ]);
    });

    it('should return paginated users', async () => {
        const res = await request(app)
            .get('/api/users?page=1&limit=10')
            .set('Authorization', `Bearer ${validToken}`)
            .expect(200);

        expect(res.body.data).toHaveLength(2);
        expect(res.body.meta.total).toBe(2);
    });

    it('should return 401 without auth', async () => {
        await request(app)
            .get('/api/users')
            .expect(401);
    });
});
```

---

## 3. Mocking — Isolate dependencies

```javascript
// Mock external services
import { jest } from '@jest/globals';

// Mock module
jest.mock('../services/emailService', () => ({
    sendEmail: jest.fn().mockResolvedValue({ messageId: 'abc123' }),
}));

import { sendEmail } from '../services/emailService';
import { registerUser } from '../services/userService';

describe('registerUser', () => {
    it('should send welcome email after registration', async () => {
        const user = await registerUser({
            name: 'An',
            email: 'an@mail.com',
            password: 'password123',
        });

        expect(sendEmail).toHaveBeenCalledWith({
            to: 'an@mail.com',
            subject: 'Welcome!',
            template: 'welcome',
        });
        expect(sendEmail).toHaveBeenCalledTimes(1);
    });

    it('should still create user if email fails', async () => {
        sendEmail.mockRejectedValueOnce(new Error('SMTP error'));

        const user = await registerUser({
            name: 'An',
            email: 'an@mail.com',
            password: 'password123',
        });

        expect(user).toBeDefined();  // User vẫn tạo OK
    });
});

// Spy — theo dõi mà không thay đổi behavior
const consoleSpy = jest.spyOn(console, 'log');
doSomething();
expect(consoleSpy).toHaveBeenCalledWith('Expected log');
consoleSpy.mockRestore();

// Mock Date
jest.useFakeTimers();
jest.setSystemTime(new Date('2026-01-01'));
// ... test time-dependent logic ...
jest.useRealTimers();
```

---

## 4. E2E Testing — Playwright

```javascript
// playwright.config.js
export default {
    testDir: './e2e',
    use: {
        baseURL: 'http://localhost:3000',
        screenshot: 'only-on-failure',
        video: 'retain-on-failure',
    },
    webServer: {
        command: 'npm run dev',
        port: 3000,
    },
};

// e2e/auth.spec.js
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
    test('should register new user', async ({ page }) => {
        await page.goto('/register');

        await page.fill('[name="name"]', 'An');
        await page.fill('[name="email"]', 'an@test.com');
        await page.fill('[name="password"]', 'password123');
        await page.click('button[type="submit"]');

        await expect(page).toHaveURL('/dashboard');
        await expect(page.locator('text=Welcome, An')).toBeVisible();
    });

    test('should login and see dashboard', async ({ page }) => {
        await page.goto('/login');
        await page.fill('[name="email"]', 'an@test.com');
        await page.fill('[name="password"]', 'password123');
        await page.click('button[type="submit"]');

        await expect(page).toHaveURL('/dashboard');
        await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
    });

    test('should show error for invalid credentials', async ({ page }) => {
        await page.goto('/login');
        await page.fill('[name="email"]', 'wrong@test.com');
        await page.fill('[name="password"]', 'wrongpass');
        await page.click('button[type="submit"]');

        await expect(page.locator('.error-message')).toContainText('Invalid');
        await expect(page).toHaveURL('/login');
    });
});

// API testing với Playwright
test('API: should create and fetch user', async ({ request }) => {
    const createRes = await request.post('/api/users', {
        data: { name: 'An', email: 'an@test.com' },
    });
    expect(createRes.ok()).toBeTruthy();

    const user = await createRes.json();
    expect(user.data.name).toBe('An');

    const getRes = await request.get(`/api/users/${user.data.id}`);
    expect(getRes.ok()).toBeTruthy();
});
```

---

## 5. Test Patterns & Best Practices

### Arrange-Act-Assert (AAA)

```javascript
test('should calculate total with discount', () => {
    // Arrange — setup
    const cart = new Cart();
    cart.addItem({ name: 'Shirt', price: 100000 });
    cart.addItem({ name: 'Pants', price: 200000 });
    cart.applyDiscount(10);  // 10%

    // Act — execute
    const total = cart.getTotal();

    // Assert — verify
    expect(total).toBe(270000);  // 300000 * 0.9
});
```

### Test Data Builders

```javascript
// Factory function cho test data
function createUser(overrides = {}) {
    return {
        name: 'Test User',
        email: `test-${Date.now()}@mail.com`,
        role: 'user',
        ...overrides,
    };
}

test('admin can delete users', async () => {
    const admin = createUser({ role: 'admin' });
    const user = createUser({ role: 'user' });
    // ...
});
```

### Table-Driven Tests

```javascript
describe('calculateShipping', () => {
    const cases = [
        { weight: 0.5, distance: 10, expected: 15000 },
        { weight: 1.0, distance: 10, expected: 20000 },
        { weight: 5.0, distance: 50, expected: 80000 },
        { weight: 10,  distance: 100, expected: 150000 },
    ];

    test.each(cases)(
        'weight=$weight, distance=$distance → $expected',
        ({ weight, distance, expected }) => {
            expect(calculateShipping(weight, distance)).toBe(expected);
        }
    );
});
```

---

## 6. Code Coverage

```bash
# Jest
npx jest --coverage

# Vitest
npx vitest --coverage

# Output:
# ----------|---------|----------|---------|---------|
# File      |  % Stmts|  % Branch|  % Funcs|  % Lines|
# ----------|---------|----------|---------|---------|
# cart.js   |   95.00 |    85.00 |   100.0 |   95.00 |
# users.js  |   80.00 |    70.00 |    90.0 |   82.00 |
# ----------|---------|----------|---------|---------|
```

```
Coverage thresholds:
• 80%+ overall → tốt cho hầu hết projects
• 90%+ cho critical code (payment, auth)
• 100% → không thực tế, ROI thấp

Quan trọng: Coverage CAO ≠ Tests TỐT
  ❌ Test chỉ gọi function mà không assert gì
  ✅ Test cases thực tế: edge cases, error paths
```

---

## Khi nào Mock, khi nào không?

| Mock | Không Mock |
|---|---|
| External APIs (Stripe, Google) | Pure functions |
| Email/SMS services | Business logic |
| File system (đôi khi) | Database (integration test) |
| Time (Date.now) | HTTP endpoints (supertest) |
| Random (Math.random) | |

---

## Bài tập thực hành

- [ ] Unit tests: viết 10 tests cho utility functions (Jest/Vitest)
- [ ] Integration: test 5 API endpoints với Supertest
- [ ] E2E: Playwright test cho login → dashboard flow
- [ ] Mock: test service gọi external API (email, payment)

---

## Tài nguyên thêm

- [Testing JavaScript](https://testingjavascript.com/) — Kent C. Dodds
- [Playwright Docs](https://playwright.dev/) — E2E testing
- [Jest Docs](https://jestjs.io/) — Unit testing
