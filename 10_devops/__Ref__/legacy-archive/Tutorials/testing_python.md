# Hướng dẫn Testing Python

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Hướng dẫn viết test cho Python với pytest, unittest và các best practices.

---

## 🧪**PYTEST**

### Cài đặt

```bash
pip install pytest pytest-cov
```

### Cấu trúc project

```
my-project/
├── src/
│   └── calculator.py
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   └── conftest.py
├── pytest.ini
└── requirements.txt
```

### Test đơn giản

```python
# src/calculator.py
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

```python
# tests/test_calculator.py
from src.calculator import add, divide
import pytest

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_divide():
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

### Chạy tests

```bash
# Chạy tất cả tests
pytest

# Chạy file cụ thể
pytest tests/test_calculator.py

# Chạy test cụ thể
pytest tests/test_calculator.py::test_add

# Verbose output
pytest -v

# Hiển thị print statements
pytest -s

# Dừng ở lỗi đầu tiên
pytest -x

# Chạy tests failed lần trước
pytest --lf

# Coverage report
pytest --cov=src --cov-report=html
```

### Fixtures

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_data():
    return {"name": "John", "age": 25}

@pytest.fixture
def db_connection():
    # Setup
    conn = create_connection()
    yield conn
    # Teardown
    conn.close()

@pytest.fixture(scope="module")
def expensive_resource():
    # Chỉ chạy 1 lần cho cả module
    return load_big_data()
```

```python
# tests/test_user.py
def test_user_name(sample_data):
    assert sample_data["name"] == "John"

def test_database(db_connection):
    result = db_connection.query("SELECT 1")
    assert result is not None
```

### Parametrize

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
    (-2, 4),
])
def test_square(input, expected):
    assert input ** 2 == expected

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

### Markers

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    # Test chạy lâu
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_feature():
    pass

@pytest.mark.xfail(reason="Known bug")
def test_known_bug():
    assert False
```

```bash
# Chạy tests có marker
pytest -m slow

# Bỏ qua tests slow
pytest -m "not slow"
```

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
```

---

## 🔬**UNITTEST**

### Test cơ bản

```python
import unittest
from src.calculator import add, divide

class TestCalculator(unittest.TestCase):
    
    def setUp(self):
        """Chạy trước mỗi test"""
        self.data = [1, 2, 3]
    
    def tearDown(self):
        """Chạy sau mỗi test"""
        self.data = None
    
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
    
    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)

if __name__ == '__main__':
    unittest.main()
```

### Assertions

```python
# Bằng
self.assertEqual(a, b)
self.assertNotEqual(a, b)

# True/False
self.assertTrue(x)
self.assertFalse(x)

# None
self.assertIsNone(x)
self.assertIsNotNone(x)

# Is (identity)
self.assertIs(a, b)
self.assertIsNot(a, b)

# In
self.assertIn(a, b)
self.assertNotIn(a, b)

# Instance
self.assertIsInstance(a, type)

# Gần bằng (số thực)
self.assertAlmostEqual(a, b, places=7)

# Regex
self.assertRegex(text, pattern)

# Exception
with self.assertRaises(ValueError):
    raise ValueError()
```

### Chạy unittest

```bash
# Chạy file
python -m unittest tests/test_calculator.py

# Chạy tất cả tests
python -m unittest discover

# Chạy với verbose
python -m unittest -v tests/test_calculator.py
```

---

## 🎭**MOCKING**

### unittest.mock

```python
from unittest.mock import Mock, patch, MagicMock

# Mock đơn giản
mock = Mock()
mock.return_value = 42
assert mock() == 42

# Mock method
mock.some_method.return_value = "hello"
assert mock.some_method() == "hello"

# Side effect
mock.side_effect = ValueError("Error!")
# mock() will raise ValueError

# Side effect với function
mock.side_effect = lambda x: x * 2
assert mock(5) == 10
```

### Patch decorator

```python
from unittest.mock import patch

# Patch function
@patch('module.function_name')
def test_something(mock_func):
    mock_func.return_value = "mocked"
    result = module.function_name()
    assert result == "mocked"

# Patch object
@patch.object(MyClass, 'method_name')
def test_method(mock_method):
    mock_method.return_value = 42
    obj = MyClass()
    assert obj.method_name() == 42
```

### Patch context manager

```python
def test_api_call():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "test"}
        
        result = my_function_that_calls_api()
        
        mock_get.assert_called_once_with("https://api.example.com")
        assert result == {"data": "test"}
```

### pytest-mock

```python
# Sử dụng với pytest
def test_with_mocker(mocker):
    mock_func = mocker.patch('module.function')
    mock_func.return_value = "mocked"
    
    result = call_function()
    
    assert result == "mocked"
    mock_func.assert_called_once()
```

---

## 📊**CODE COVERAGE**

### Cài đặt

```bash
pip install pytest-cov coverage
```

### Chạy coverage

```bash
# Với pytest
pytest --cov=src tests/

# Report chi tiết
pytest --cov=src --cov-report=html tests/

# Missing lines
pytest --cov=src --cov-report=term-missing tests/
```

### .coveragerc

```ini
[run]
source = src
omit = 
    */tests/*
    */__pycache__/*
    */venv/*

[report]
exclude_lines =
    pragma: no cover
    if __name__ == .__main__.:
    raise NotImplementedError

[html]
directory = htmlcov
```

---

## ✅**BEST PRACTICES**

### 1. Đặt tên test

```python
# Tốt: Mô tả rõ ràng
def test_add_returns_sum_of_two_positive_numbers():
    pass

def test_divide_raises_error_when_dividing_by_zero():
    pass

# Không tốt: Quá ngắn
def test_add():
    pass
```

### 2. Arrange - Act - Assert (AAA)

```python
def test_user_creation():
    # Arrange - Chuẩn bị dữ liệu
    name = "John"
    email = "john@example.com"
    
    # Act - Thực hiện action
    user = User(name=name, email=email)
    
    # Assert - Kiểm tra kết quả
    assert user.name == name
    assert user.email == email
```

### 3. Một assertion mỗi test (nếu có thể)

```python
# Tốt: Tách riêng
def test_user_has_correct_name():
    user = User(name="John")
    assert user.name == "John"

def test_user_has_correct_email():
    user = User(email="john@test.com")
    assert user.email == "john@test.com"
```

### 4. Sử dụng fixtures để tránh lặp

```python
@pytest.fixture
def user():
    return User(name="John", email="john@test.com")

def test_user_name(user):
    assert user.name == "John"

def test_user_email(user):
    assert user.email == "john@test.com"
```

### 5. Test edge cases

```python
def test_empty_list():
    assert process([]) == []

def test_single_item():
    assert process([1]) == [1]

def test_negative_numbers():
    assert process([-1, -2]) == [-1, -2]

def test_none_input():
    with pytest.raises(TypeError):
        process(None)
```

---

## 📁**CẤU TRÚC THƯ MỤC**

```
project/
├── src/
│   ├── __init__.py
│   ├── module1.py
│   └── module2.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   ├── test_module1.py
│   ├── test_module2.py
│   └── integration/
│       └── test_api.py
├── pytest.ini
├── .coveragerc
└── requirements-dev.txt
```

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
