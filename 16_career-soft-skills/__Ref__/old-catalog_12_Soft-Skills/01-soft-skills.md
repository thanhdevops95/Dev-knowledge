# 🧠 Kỹ năng mềm & Tư duy lập trình

> `[BEGINNER → ADVANCED]` — Thứ phân biệt Developer giỏi với Developer xuất sắc

---

## Code Review — Cho và nhận feedback

### Khi bạn là Reviewer

```
✅ Tốt:
"Hàm này có thể extract ra thành helper để tái sử dụng ở X và Y không?"
"Nếu input là null thì sẽ crash tại dòng 42, cần handle trường hợp này."
"Tôi thích cách bạn dùng Strategy pattern ở đây 👍"

❌ Không nên:
"Code tệ quá."
"Làm lại đi."
"Sao không làm theo cách của tôi?"
```

**Checklist khi review:**
- [ ] Logic có đúng không?
- [ ] Edge cases được xử lý chưa? (null, empty, negative, max)
- [ ] Performance ổn không? (N+1 query, unnecessary loops)
- [ ] Security: input validation, authorization
- [ ] Có test không?
- [ ] Code có tự giải thích không? (readable)
- [ ] DRY — Có đoạn code nào trùng lặp không?

### Khi bạn là Author

- **Viết PR description rõ ràng** — What, Why, How
- **PR nhỏ** — Tối đa 400 dòng, dễ review hơn
- **Self-review trước** — Đọc lại code của mình như của người khác
- **Không defensive** — Feedback là về code, không phải về bạn

---

## Clean Code Principles

### Đặt tên rõ ràng

```python
# ❌ Khó hiểu
def calc(d, r):
    return d * r * 0.01

x = 1704067200

# ✅ Tự giải thích
def calculate_discount_amount(price: float, discount_rate_percent: float) -> float:
    return price * discount_rate_percent / 100

JANUARY_1_2026_UNIX_TIMESTAMP = 1704067200
```

### Functions nhỏ, mỗi function 1 việc

```python
# ❌ Hàm làm quá nhiều thứ (God function)
def process_order(order_data):
    # Validate
    if not order_data.get("user_id"):
        raise ValueError("Missing user_id")
    # Tính giá
    total = sum(item["price"] * item["qty"] for item in order_data["items"])
    if order_data.get("coupon"):
        total *= 0.9
    # Lưu DB
    order = db.create(order_data, total=total)
    # Gửi email
    send_email(order_data["email"], f"Order #{order.id} confirmed")
    # Update inventory
    for item in order_data["items"]:
        db.update_stock(item["id"], -item["qty"])

# ✅ Tách ra từng function có trách nhiệm rõ
def validate_order(order_data: dict) -> None: ...
def calculate_order_total(items: list, coupon: str | None) -> Decimal: ...
def save_order(order_data: dict, total: Decimal) -> Order: ...
def notify_customer(order: Order) -> None: ...
def update_inventory(items: list) -> None: ...

def process_order(order_data: dict) -> Order:
    validate_order(order_data)
    total = calculate_order_total(order_data["items"], order_data.get("coupon"))
    order = save_order(order_data, total)
    notify_customer(order)
    update_inventory(order_data["items"])
    return order
```

### DRY — Don't Repeat Yourself

```python
# ❌ Logic trùng lặp
def get_user_discount(user):
    if user.plan == "premium":
        return 0.20
    elif user.plan == "basic":
        return 0.10
    else:
        return 0

def get_enterprise_discount(enterprise):
    if enterprise.plan == "premium":
        return 0.20
    elif enterprise.plan == "basic":
        return 0.10
    else:
        return 0

# ✅ Extract logic chung
DISCOUNT_RATES = {
    "premium": 0.20,
    "basic": 0.10,
    "free": 0
}

def get_discount_rate(plan: str) -> float:
    return DISCOUNT_RATES.get(plan, 0)
```

---

## Problem-Solving Approach

### Khi gặp bug hoặc vấn đề mới:

```
1. HIỂU vấn đề (không vội code ngay!)
   → Đọc lỗi kỹ, reproduce được không?
   → Viết ra input/output mong muốn

2. LẬP KẾ HOẠCH
   → Chia nhỏ vấn đề thành các bước
   → Pseudocode hoặc flow diagram

3. THỰC HIỆN
   → Code từng bước nhỏ
   → Test từng bước

4. REVIEW
   → Có edge cases nào bỏ sót không?
   → Code có thể đơn giản hơn không?
```

### Debugging Checklist

```
1. Đọc lỗi kỹ — Error message, stack trace
2. Reproduce — Tái hiện lỗi nhất quán
3. Isolate — Thu hẹp đến dòng code gây lỗi
4. Hypothesize — Giả thuyết nguyên nhân
5. Verify — Test từng giả thuyết
6. Fix — Sửa và verify lại
7. Document — Ghi chú để không mắc lại
```

---

## Git Workflow trong Team

### Quy trình chuẩn

```bash
# 1. Tạo branch mới từ main
git checkout main
git pull origin main
git checkout -b feature/add-user-profile

# 2. Code và commit thường xuyên
git add .
git commit -m "feat(profile): add avatar upload endpoint"

# 3. Push và tạo PR
git push origin feature/add-user-profile
# Tạo Pull Request trên GitHub/GitLab

# 4. Sau khi PR được merge
git checkout main
git pull origin main
git branch -d feature/add-user-profile
```

### Quy tắc branch naming

```
feature/  → Tính năng mới
bug/      → Sửa bug
hotfix/   → Fix khẩn cấp trên production
chore/    → Cập nhật dependency, config
refactor/ → Refactoring
docs/     → Tài liệu

Ví dụ:
feature/user-authentication
bug/fix-login-redirect
hotfix/payment-crash-v1.2.1
```

---

## Agile & Scrum cơ bản

### Các ceremonires (cuộc họp) trong Scrum

| Ceremony | Mục đích |
|---|---|
| **Sprint Planning** | Chọn task cho sprint tới (1-2 tuần) |
| **Daily Standup** | 15 phút: Hôm qua làm gì? Hôm nay làm gì? Blocker? |
| **Sprint Review** | Demo kết quả cho stakeholders |
| **Retrospective** | Team tự cải thiện process |

### User Story

```
AS A [role]
I WANT [feature]
SO THAT [benefit]

Ví dụ:
AS A registered user
I WANT to reset my password via email
SO THAT I can regain access to my account if I forget my password

Acceptance Criteria:
- Given: User nhấn "Forgot password" và nhập email hợp lệ
- When: Hệ thống gửi email với link reset
- Then: Link có hiệu lực 1 giờ, click vào có thể đặt password mới
- And: Password cũ không còn hiệu lực sau khi đổi
```

---

## Communication khi làm việc team

### Báo cáo tiến độ rõ ràng

```
❌ "Đang làm task"
❌ "Sắp xong rồi"

✅ "Tôi đã hoàn thành phần X và Y.
    Đang làm Z (ước tính xong tối nay).
    Có blockers: cần API spec từ BE team để hoàn thiện form."
```

### Khi cần giúp đỡ

```
Cung cấp đủ context:
1. Tôi đang cố làm gì?
2. Tôi đã thử gì rồi?
3. Kết quả thực tế là gì?
4. Kết quả mong đợi là gì?

Ví dụ:
"Tôi đang cố kết nối đến PostgreSQL từ Docker container.
Đã thử: dùng localhost:5432 và 127.0.0.1:5432
Lỗi: Connection refused
Mong đợi: Connect thành công
Đây là docker-compose.yml của tôi: [code]"
```

---

## Continuous Learning Mindset

### Thói quen tốt

- **Newsletter** — Subscribe: TLDR Tech, Bytes.dev, JavaScript Weekly
- **Podcast** — Syntax.fm, Backend Banter, Lex Fridman
- **Blog / Articles** — Medium, Dev.to, HackerNews
- **Mở source code** — Đọc code của thư viện bạn dùng
- **Side projects** — Xây dựng thứ gì đó thực sự
- **Contribute open source** — Dù chỉ sửa typo trong docs

### Track học tập

```markdown
## Learning Log — [Tháng/Năm]

### Đã học:
- [ ] Docker multi-stage builds
- [ ] PostgreSQL Window Functions
- [ ] React Server Components

### Đang học:
- Kubernetes networking

### Muốn học:
- Rust
- WebAssembly

### Projects:
- Side project: CLI tool với Go
- Contributed: Fix bug #1234 trong fastapi repo
```

---

## Tài nguyên thêm

- [Clean Code (book)](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) — Robert C. Martin
- [The Pragmatic Programmer (book)](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) — Kinh điển
- [A Philosophy of Software Design (book)](https://www.amazon.com/Philosophy-Software-Design-2nd/dp/173210221X) — Về complexity
- [StaffEng](https://staffeng.com/) — Becoming a senior/staff engineer
