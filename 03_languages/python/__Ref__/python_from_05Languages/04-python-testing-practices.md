# 🧪 Python Testing — Kiểm thử trong Python

> `[INTERMEDIATE]` — Prerequisite: `01-python-basics.md`

---

## 1. pytest — Framework testing tiêu chuẩn

```python
# test_calculator.py
import pytest
from calculator import add, divide

# ── Basic test ──
def test_add():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, 1) == 0

# ── Exception testing ──
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

# ── Parametrize — nhiều test cases, 1 function ──
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (-1, 1, 0),
    (0, 0, 0),
    (100, -50, 50),
])
def test_add_parametrize(a, b, expected):
    assert add(a, b) == expected
```

### Fixtures — Setup/Teardown

```python
import pytest
from database import Database

@pytest.fixture
def db():
    """Setup: create DB, Teardown: close DB."""
    database = Database(":memory:")
    database.create_tables()
    yield database  # ← test runs here
    database.close()

@pytest.fixture
def sample_users(db):
    db.insert_user("Alice", "alice@test.com")
    db.insert_user("Bob", "bob@test.com")
    return db

def test_get_users(sample_users):
    users = sample_users.get_all_users()
    assert len(users) == 2
    assert users[0].name == "Alice"
```

### Mocking

```python
from unittest.mock import patch, MagicMock
from services import UserService

def test_create_user_sends_email():
    """Mock external dependency (email service)."""
    with patch('services.EmailClient') as mock_email:
        service = UserService()
        service.create_user("Alice", "alice@test.com")
        
        mock_email.return_value.send.assert_called_once_with(
            to="alice@test.com",
            subject="Welcome!"
        )

@patch('services.requests.get')
def test_fetch_api(mock_get):
    mock_get.return_value.json.return_value = {"status": "ok"}
    result = fetch_api("/health")
    assert result["status"] == "ok"
```

---

## 2. Coverage

```bash
pytest --cov=src --cov-report=html --cov-report=term-missing
# htmlcov/index.html → visual coverage report

# Target: 80%+ cho production code
# 100% coverage ≠ bug-free (nhưng < 60% = risky)
```

---

## 3. Test Types

| Type | Scope | Speed | Tools |
|---|---|---|---|
| **Unit** | Single function/class | ⚡ ms | pytest |
| **Integration** | Multiple components | 🔄 seconds | pytest + testcontainers |
| **E2E** | Full system | 🐌 seconds-mins | playwright, selenium |
| **Property-based** | Random inputs | 🔄 varies | hypothesis |

```python
# Property-based testing with Hypothesis
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_idempotent(lst):
    """Sorting a sorted list should be the same."""
    assert sorted(sorted(lst)) == sorted(lst)

@given(st.text())
def test_reverse_reverse(s):
    """Reversing twice = original."""
    assert s[::-1][::-1] == s
```

---

## Gotchas

| ❌ Sai | ✅ Đúng |
|--------|---------|
| Test implementation details | Test behavior/outcomes |
| Mock everything | Mock external deps only |
| Skip slow tests permanently | Use `@pytest.mark.slow` + run in CI |
| No test naming convention | `test_<function>_<scenario>_<expected>` |

---

## Tài nguyên

- [pytest Documentation](https://docs.pytest.org/) — Official docs
- [Effective Python Testing (Real Python)](https://realpython.com/pytest-python-testing/) — Tutorial
- [Python Testing with pytest (Okken)](https://pragprog.com/titles/bopytest2/) — Best book
