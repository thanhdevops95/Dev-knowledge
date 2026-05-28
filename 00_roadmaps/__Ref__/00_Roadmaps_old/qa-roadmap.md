# 🧪 Lộ trình QA / Test Engineer

> `[BEGINNER → ADVANCED]` — Xem trước [Tổng quan Lộ trình](./00-overview.md)

---

## Tại sao QA?

QA Engineer giống như "hàng rào cuối cùng" trước khi sản phẩm đến tay người dùng. Một bug nhỏ ở production có thể gây thiệt hại hàng triệu đô — QA ngăn chặn điều đó. **Phòng bug luôn rẻ hơn chữa bug**: fix bug ở giai đoạn design rẻ hơn 100x so với fix ở production.

QA không chỉ là "click và tìm bug". QA hiện đại viết automation, thiết kế test strategy, phân tích risk, và tích hợp testing vào CI/CD pipeline. Đây là vai trò đòi hỏi tư duy hệ thống và kỹ năng kỹ thuật cao.

---

## Sơ đồ lộ trình

```
Testing Fundamentals
    │
    ▼
Manual Testing (Test cases, Bug reports)
    │
    ▼
Automation ──► Playwright / Cypress (E2E)
    │
    ├──► API Testing (Postman, REST Assured)
    │
    ├──► Unit Testing (Jest, pytest)
    │
    ├──► Performance Testing (k6, JMeter)
    │
    ├──► Security Testing (OWASP ZAP)
    │
    └──► CI Integration + TDD/BDD
```

---

## Giai đoạn 1 — Testing Fundamentals

- [ ] Khái niệm QA vs QC vs Testing → [../13-Testing/01-testing-fundamentals.md](../13-Testing/01-testing-fundamentals.md)
- [ ] Test pyramid (Unit → Integration → E2E)
- [ ] Black-box vs White-box testing
- [ ] Equivalence partitioning, Boundary value analysis

---

## Giai đoạn 2 — Manual Testing

- [ ] Viết Test Cases & Test Plans
- [ ] Bug Report hiệu quả (steps to reproduce, severity, priority)
- [ ] Exploratory Testing
- [ ] Regression Testing workflow

---

## Giai đoạn 3 — Test Automation (E2E)

- [ ] Playwright cơ bản → [../13-Testing/e2e-testing/01-playwright-basics.md](../13-Testing/e2e-testing/01-playwright-basics.md)
- [ ] Cypress cơ bản → [../13-Testing/e2e-testing/02-cypress-basics.md](../13-Testing/e2e-testing/02-cypress-basics.md)
- [ ] Page Object Model pattern
- [ ] Data-driven testing

---

## Giai đoạn 4 — API Testing

- [ ] API Testing cơ bản → [../13-Testing/integration-testing/01-api-testing-basics.md](../13-Testing/integration-testing/01-api-testing-basics.md)
- [ ] Postman / Newman cho automation
- [ ] REST API validation (status codes, schemas, contracts)

---

## Giai đoạn 5 — Unit Testing

- [ ] Jest (JavaScript/TypeScript) → [../13-Testing/unit-testing/](../13-Testing/unit-testing/)
- [ ] pytest (Python) → [../13-Testing/unit-testing/](../13-Testing/unit-testing/)
- [ ] Mocking, Stubbing, Test Doubles
- [ ] Code Coverage (Istanbul, Coverage.py)

---

## Giai đoạn 6 — Performance Testing

- [ ] k6 cơ bản → [../13-Testing/performance-testing/01-k6-basics.md](../13-Testing/performance-testing/01-k6-basics.md)
- [ ] Load testing, Stress testing, Spike testing
- [ ] Performance metrics: latency, throughput, error rate

---

## Giai đoạn 7 — Security Testing

- [ ] OWASP ZAP cơ bản → [../13-Testing/security-testing/01-owasp-zap-basics.md](../13-Testing/security-testing/01-owasp-zap-basics.md)
- [ ] SQL Injection, XSS, CSRF detection
- [ ] Dependency vulnerability scanning

---

## Giai đoạn 8 — CI Integration & Methodologies

- [ ] Tích hợp tests vào CI/CD pipeline (GitHub Actions)
- [ ] TDD (Test-Driven Development) → [../13-Testing/methodologies/](../13-Testing/methodologies/)
- [ ] BDD (Behavior-Driven Development) với Cucumber/Gherkin
- [ ] Shift-left testing strategy

---

## 📦 Project thực hành

| Giai đoạn | Project |
|---|---|
| Sau Manual | Viết test plan hoàn chỉnh cho 1 web app |
| Sau Playwright | Automation suite cho e-commerce site (login, cart, checkout) |
| Sau API Testing | Test toàn bộ REST API của 1 backend project |
| Sau Performance | Load test 1 API và tạo report phân tích bottleneck |
| Nâng cao | CI pipeline chạy unit + E2E + performance tests tự động |

---

## 📚 Tài nguyên

- [ISTQB Foundation Syllabus](https://www.istqb.org/) — Chứng chỉ QA quốc tế
- [Playwright Docs](https://playwright.dev/docs/intro) — Framework E2E testing hiện đại
- [Ministry of Testing](https://www.ministryoftesting.com/) — Cộng đồng QA lớn nhất
- [Test Automation University](https://testautomationu.applitools.com/) — Khóa học miễn phí
- [k6 Docs](https://grafana.com/docs/k6/latest/) — Performance testing tool
