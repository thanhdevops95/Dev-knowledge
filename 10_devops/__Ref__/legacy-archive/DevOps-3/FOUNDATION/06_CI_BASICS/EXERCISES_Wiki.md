# Exercises: Module 06 - CI BASICS

> **Bài tập CI/CD**

**Điểm:** 100 | **Thời gian:** 50 phút

---

## PHẦN A: TRẮC NGHIỆM (25 điểm)

1. CI là gì? - **B) Continuous Integration**
2. Workflow file location? - **C) .github/workflows/**
3. Run on push to main? - **B) on: push: branches: [main]**
4. Checkout action? - **A) actions/checkout@v3**
5. Secret syntax? - **C) ${{ secrets.NAME }}**
6. Matrix test? - **B) strategy: matrix:**
7. Cache deps? - **A) actions/cache**
8. Manual trigger? - **C) workflow_dispatch**
9. Run if condition? - **B) if: github.ref == 'refs/heads/main'**
10. Deploy after test? - **A) needs: test**

---

## PHẦN B: THỰC HÀNH (75 điểm)

1. Tạo workflow chạy tests on push
2. Add Docker build step
3. Setup secrets cho DockerHub
4. Deploy to server via SSH
5. Add matrix testing (Python 3.8, 3.9, 3.10)
6. Cache pip dependencies
7. Add manual trigger option
8. Conditional deploy (only on main)

---

**Xem SOLUTIONS.md cho đáp án!**
