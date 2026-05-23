# 🧪 Testing Methodologies — TDD, BDD & Patterns

> `[INTERMEDIATE]` — Chiến lược test cho code chất lượng

---

## 1. Test Pyramid

```
         ╱  E2E Tests  ╲          Chậm, đắt, ít
        ╱  (Playwright)  ╲        Test flows end-to-end
       ╱─────────────────────╲
      ╱  Integration Tests    ╲   API, DB, services
     ╱  (Supertest, Testcontainers)╲
    ╱──────────────────────────────╲
   ╱       Unit Tests               ╲  Nhanh, rẻ, nhiều
  ╱     (Jest, Vitest, pytest)       ╲  Test functions/classes
 ╱────────────────────────────────────╲

Rule: 70% Unit, 20% Integration, 10% E2E
```

---

## 2. TDD — Test-Driven Development

```
RED → GREEN → REFACTOR (lặp lại!)

RED:      Viết test TRƯỚC → test FAIL (chưa có code!)
GREEN:    Viết code TỐI THIỂU để test PASS
REFACTOR: Cải thiện code, test vẫn PASS
```

```typescript
// RED: Viết test trước
describe('calculateDiscount', () => {
    test('10% for orders over 500k', () => {
        expect(calculateDiscount(600_000)).toBe(60_000);
    });

    test('no discount for orders under 500k', () => {
        expect(calculateDiscount(400_000)).toBe(0);
    });

    test('20% for orders over 1M', () => {
        expect(calculateDiscount(1_200_000)).toBe(240_000);
    });
});

// GREEN: Viết code tối thiểu
function calculateDiscount(amount: number): number {
    if (amount >= 1_000_000) return amount * 0.2;
    if (amount >= 500_000) return amount * 0.1;
    return 0;
}

// REFACTOR: Cải thiện
const DISCOUNT_TIERS = [
    { threshold: 1_000_000, rate: 0.2 },
    { threshold: 500_000, rate: 0.1 },
];

function calculateDiscount(amount: number): number {
    const tier = DISCOUNT_TIERS.find(t => amount >= t.threshold);
    return tier ? amount * tier.rate : 0;
}
// Tests vẫn PASS → refactor thành công!
```

---

## 3. AAA Pattern — Arrange, Act, Assert

```typescript
describe('UserService', () => {
    test('create user with valid data', async () => {
        // ARRANGE — Setup
        const userData = { name: 'An', email: 'an@test.com', password: 'Pass123!' };
        const mockRepo = { save: jest.fn().mockResolvedValue({ id: '1', ...userData }) };
        const service = new UserService(mockRepo);

        // ACT — Execute
        const result = await service.create(userData);

        // ASSERT — Verify
        expect(result.id).toBeDefined();
        expect(result.name).toBe('An');
        expect(mockRepo.save).toHaveBeenCalledWith(
            expect.objectContaining({ name: 'An', email: 'an@test.com' }),
        );
    });
});
```

---

## 4. Mocking — Giả lập dependencies

```typescript
import { jest } from '@jest/globals';

// Mock module
jest.mock('./emailService');

// Mock specific function
const sendEmail = jest.fn().mockResolvedValue({ success: true });

// Mock implementation
const mockDB = {
    users: {
        findById: jest.fn(),
        create: jest.fn(),
        update: jest.fn(),
    },
};

describe('OrderService', () => {
    beforeEach(() => {
        jest.clearAllMocks();  // Reset mocks mỗi test!
    });

    test('send confirmation email after order', async () => {
        // Arrange
        mockDB.users.findById.mockResolvedValue({ id: '1', email: 'an@test.com' });
        const service = new OrderService(mockDB, sendEmail);

        // Act
        await service.createOrder({ userId: '1', items: [{ productId: 'p1', qty: 2 }] });

        // Assert
        expect(sendEmail).toHaveBeenCalledWith(
            'an@test.com',
            expect.stringContaining('Xác nhận đơn hàng'),
        );
    });

    test('throw error when user not found', async () => {
        mockDB.users.findById.mockResolvedValue(null);
        const service = new OrderService(mockDB, sendEmail);

        await expect(service.createOrder({ userId: '999', items: [] }))
            .rejects.toThrow('User not found');

        expect(sendEmail).not.toHaveBeenCalled();
    });
});
```

---

## 5. Integration Testing — Supertest

```typescript
import request from 'supertest';
import { app } from '../src/app';

describe('POST /api/users', () => {
    test('create user successfully', async () => {
        const res = await request(app)
            .post('/api/users')
            .send({ name: 'An', email: 'an@test.com', password: 'Pass123!' })
            .expect('Content-Type', /json/)
            .expect(201);

        expect(res.body.data).toMatchObject({
            name: 'An',
            email: 'an@test.com',
        });
        expect(res.body.data.password).toBeUndefined();  // Không trả password!
    });

    test('reject invalid email', async () => {
        const res = await request(app)
            .post('/api/users')
            .send({ name: 'An', email: 'invalid', password: 'Pass123!' })
            .expect(400);

        expect(res.body.error).toBeDefined();
    });

    test('reject duplicate email', async () => {
        // First create
        await request(app)
            .post('/api/users')
            .send({ name: 'An', email: 'dup@test.com', password: 'Pass123!' });

        // Second create → conflict
        const res = await request(app)
            .post('/api/users')
            .send({ name: 'Bình', email: 'dup@test.com', password: 'Pass123!' })
            .expect(409);
    });
});
```

---

## 6. Test Data Builders

```typescript
// Factory pattern cho test data
class UserBuilder {
    private data: Partial<User> = {
        name: 'Default User',
        email: 'default@test.com',
        role: 'user',
        active: true,
    };

    withName(name: string) { this.data.name = name; return this; }
    withEmail(email: string) { this.data.email = email; return this; }
    withRole(role: string) { this.data.role = role; return this; }
    inactive() { this.data.active = false; return this; }

    build(): User {
        return { id: randomUUID(), ...this.data } as User;
    }
}

// Sử dụng — đọc dễ hiểu!
const admin = new UserBuilder().withName('Admin An').withRole('admin').build();
const inactiveUser = new UserBuilder().withEmail('old@test.com').inactive().build();
```

---

## 7. Code Coverage

```json
// jest.config.ts
{
    "collectCoverage": true,
    "coverageThreshold": {
        "global": {
            "branches": 80,
            "functions": 80,
            "lines": 80,
            "statements": 80
        }
    },
    "coveragePathIgnorePatterns": [
        "/node_modules/",
        "/__tests__/",
        "/dist/"
    ]
}
```

```
Loại coverage:
  Lines:      % dòng code được chạy
  Branches:   % nhánh if/else được test
  Functions:  % functions được gọi
  Statements: % statements được thực thi

⚠️ 100% coverage ≠ bug-free!
   Coverage chỉ đo "code được chạy", không đo "code đúng logic"
```

---

## Bài tập thực hành

- [ ] TDD: Viết test TRƯỚC cho calculator service
- [ ] Mocking: test OrderService với mocked DB + email
- [ ] Integration: Supertest cho CRUD API endpoints
- [ ] Coverage: đạt 80% cho 1 module

---

## Tài nguyên thêm

- [Jest Docs](https://jestjs.io/docs/getting-started) — Official
- [Vitest](https://vitest.dev/) — Vite-native testing
- [Testing JavaScript (Kent C. Dodds)](https://testingjavascript.com/)
