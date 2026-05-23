# 🎭 Playwright — E2E Testing hiện đại

> `[INTERMEDIATE]` — Test ứng dụng web từ góc nhìn người dùng

---

## 1. Setup & Cấu trúc

```bash
npm init playwright@latest
# Tạo: playwright.config.ts, tests/, .github/workflows/playwright.yml
```

```
tests/
├── auth.spec.ts          ← Authentication tests
├── dashboard.spec.ts     ← Dashboard features
├── checkout.spec.ts      ← E-commerce checkout flow
├── fixtures/
│   └── auth.fixture.ts   ← Custom fixtures (logged-in user)
└── helpers/
    └── api.helper.ts     ← API helpers
```

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
    testDir: './tests',
    timeout: 30_000,
    retries: process.env.CI ? 2 : 0,
    workers: process.env.CI ? 1 : undefined,
    reporter: [
        ['html'],
        ['junit', { outputFile: 'results.xml' }],
    ],
    use: {
        baseURL: 'http://localhost:3000',
        screenshot: 'only-on-failure',
        video: 'retain-on-failure',
        trace: 'on-first-retry',
    },
    projects: [
        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
        { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
        { name: 'mobile', use: { ...devices['iPhone 14'] } },
    ],
    webServer: {
        command: 'npm run dev',
        port: 3000,
        reuseExistingServer: !process.env.CI,
    },
});
```

---

## 2. Viết Tests

```typescript
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
    test('login successfully', async ({ page }) => {
        await page.goto('/login');

        // Fill form
        await page.getByLabel('Email').fill('user@example.com');
        await page.getByLabel('Password').fill('password123');
        await page.getByRole('button', { name: 'Đăng nhập' }).click();

        // Verify redirect
        await expect(page).toHaveURL('/dashboard');
        await expect(page.getByText('Chào mừng')).toBeVisible();
    });

    test('show error for invalid credentials', async ({ page }) => {
        await page.goto('/login');

        await page.getByLabel('Email').fill('wrong@email.com');
        await page.getByLabel('Password').fill('wrongpassword');
        await page.getByRole('button', { name: 'Đăng nhập' }).click();

        await expect(page.getByText('Email hoặc mật khẩu không đúng')).toBeVisible();
        await expect(page).toHaveURL('/login');  // Không redirect
    });
});

test.describe('Shopping Cart', () => {
    test('add product and checkout', async ({ page }) => {
        await page.goto('/products');

        // Add to cart
        await page.getByTestId('product-card').first().click();
        await page.getByRole('button', { name: 'Thêm vào giỏ' }).click();

        // Verify cart badge
        await expect(page.getByTestId('cart-badge')).toHaveText('1');

        // Go to cart
        await page.getByTestId('cart-icon').click();
        await expect(page).toHaveURL('/cart');

        // Checkout
        await page.getByRole('button', { name: 'Thanh toán' }).click();
        await page.getByLabel('Địa chỉ').fill('123 Lê Lợi, Q1, HCM');
        await page.getByRole('button', { name: 'Đặt hàng' }).click();

        await expect(page.getByText('Đặt hàng thành công')).toBeVisible();
    });
});
```

---

## 3. Locators — Cách tìm elements

```typescript
// ✅ Best practices (resilient, user-facing)
page.getByRole('button', { name: 'Submit' });   // ARIA role
page.getByLabel('Email');                         // Form label
page.getByPlaceholder('Search...');               // Placeholder
page.getByText('Welcome');                        // Text content
page.getByTestId('submit-btn');                   // data-testid

// ⚠️ OK khi cần thiết
page.locator('.card:first-child');                // CSS selector
page.locator('//div[@class="card"]');             // XPath

// ❌ Fragile — tránh!
page.locator('#btn-123');                         // Random ID
page.locator('.css-abc123');                       // Generated class
page.locator('div > div > span:nth-child(3)');    // Deep nesting

// Chaining & Filtering
page.getByRole('listitem')
    .filter({ hasText: 'MacBook' })
    .getByRole('button', { name: 'Buy' });
```

---

## 4. Page Object Model (POM)

```typescript
// pages/LoginPage.ts
export class LoginPage {
    constructor(private page: Page) {}

    readonly emailInput = this.page.getByLabel('Email');
    readonly passwordInput = this.page.getByLabel('Password');
    readonly submitButton = this.page.getByRole('button', { name: 'Đăng nhập' });
    readonly errorMessage = this.page.getByTestId('error-message');

    async goto() {
        await this.page.goto('/login');
    }

    async login(email: string, password: string) {
        await this.emailInput.fill(email);
        await this.passwordInput.fill(password);
        await this.submitButton.click();
    }
}

// tests/auth.spec.ts
import { LoginPage } from '../pages/LoginPage';

test('login flow', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@test.com', 'pass123');
    await expect(page).toHaveURL('/dashboard');
});
```

---

## 5. API Testing & Mocking

```typescript
// Mock API response
test('show products from API', async ({ page }) => {
    await page.route('**/api/products', async (route) => {
        await route.fulfill({
            status: 200,
            contentType: 'application/json',
            body: JSON.stringify([
                { id: 1, name: 'Mock Product', price: 100 },
            ]),
        });
    });

    await page.goto('/products');
    await expect(page.getByText('Mock Product')).toBeVisible();
});

// API testing trực tiếp (không cần browser!)
test('API: create user', async ({ request }) => {
    const response = await request.post('/api/users', {
        data: { name: 'Test User', email: 'test@test.com' },
    });

    expect(response.status()).toBe(201);
    const user = await response.json();
    expect(user.name).toBe('Test User');
});
```

---

## 6. Visual Regression Testing

```typescript
// Screenshot comparison
test('homepage visual', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage.png', {
        maxDiffPixelRatio: 0.01,  // Cho phép 1% khác biệt
    });
});

// Component screenshot
test('button states', async ({ page }) => {
    await page.goto('/components/button');
    const button = page.getByRole('button', { name: 'Primary' });

    await expect(button).toHaveScreenshot('button-default.png');

    await button.hover();
    await expect(button).toHaveScreenshot('button-hover.png');
});
```

---

## Commands

```bash
npx playwright test                    # Chạy tất cả tests
npx playwright test --headed           # Hiện browser
npx playwright test --ui               # Interactive UI mode
npx playwright test auth.spec.ts       # Chạy 1 file
npx playwright test --grep "login"     # Chạy tests matching pattern
npx playwright show-report             # Xem HTML report
npx playwright codegen localhost:3000  # Record & generate code!
```

---

## Bài tập thực hành

- [ ] Viết E2E test cho login + registration flow
- [ ] Page Object Model cho 3 pages
- [ ] Mock API response: test error states
- [ ] Visual regression: homepage + key components

---

## Tài nguyên thêm

- [Playwright Docs](https://playwright.dev/docs/intro) — Official
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
