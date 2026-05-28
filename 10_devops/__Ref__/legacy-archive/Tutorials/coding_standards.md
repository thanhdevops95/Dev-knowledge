# Hướng dẫn Coding Standards

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Tài liệu này định nghĩa các chuẩn về trình bày code, chú thích và tổ chức dự án.

---

## 📝**FILE HEADER TEMPLATE**

### Python

```python
"""
================================================================
[TÊN ỨNG DỤNG] v[VERSION] - [MÔ TẢ NGẮN]
================================================================
Version: X.X.X
Author: [Tên tác giả]
License: MIT
Created: [YYYY-MM-DD]
Last Modified: [YYYY-MM-DD]
================================================================

MÔ TẢ:
----------------------------------------------------------------
[Mô tả chi tiết về mục đích và chức năng của file/module này]

DEPENDENCIES:
----------------------------------------------------------------
- library1: Mô tả
- library2: Mô tả

USAGE:
----------------------------------------------------------------
python main.py [options]

CHANGELOG:
----------------------------------------------------------------
- v1.0.0: Initial release
================================================================
"""
```

### JavaScript/TypeScript

```javascript
/**
 * ================================================================
 * [TÊN ỨNG DỤNG] v[VERSION] - [MÔ TẢ NGẮN]
 * ================================================================
 * @version     X.X.X
 * @author      [Tên tác giả]
 * @license     MIT
 * @created     [YYYY-MM-DD]
 * @modified    [YYYY-MM-DD]
 * ================================================================
 * 
 * @description
 * [Mô tả chi tiết về mục đích và chức năng]
 * 
 * @example
 * import { myFunction } from './module';
 * myFunction();
 * ================================================================
 */
```

### HTML

```html
<!--
================================================================
[TÊN TRANG] - [MÔ TẢ NGẮN]
================================================================
Version: X.X.X
Author: [Tên tác giả]
Created: [YYYY-MM-DD]
================================================================
-->
<!DOCTYPE html>
<html lang="vi">
...
</html>
```

### CSS

```css
/**
 * ================================================================
 * [TÊN FILE] - [MÔ TẢ NGẮN]
 * ================================================================
 * Version: X.X.X
 * Author: [Tên tác giả]
 * Created: [YYYY-MM-DD]
 * ================================================================
 * 
 * TABLE OF CONTENTS:
 * 1. Variables
 * 2. Reset/Base
 * 3. Layout
 * 4. Components
 * 5. Utilities
 * ================================================================
 */
```

---

## 💬**CHÚ THÍCH CODE (COMMENTS)**

### Python Docstrings

```python
def calculate_total(items: list, tax_rate: float = 0.1) -> float:
    """
    Tính tổng tiền bao gồm thuế.
    
    Hàm này tính tổng giá trị các items và cộng thêm thuế
    theo tỷ lệ được chỉ định.
    
    Args:
        items (list): Danh sách các items, mỗi item có 'price' và 'quantity'
        tax_rate (float, optional): Tỷ lệ thuế. Mặc định 0.1 (10%)
    
    Returns:
        float: Tổng tiền sau thuế
    
    Raises:
        ValueError: Nếu items rỗng hoặc tax_rate âm
    
    Example:
        >>> items = [{'price': 100, 'quantity': 2}]
        >>> calculate_total(items, 0.1)
        220.0
    
    Note:
        Tax rate phải từ 0 đến 1 (0% - 100%)
    """
    if not items:
        raise ValueError("Items cannot be empty")
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")
    
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    return subtotal * (1 + tax_rate)
```

### Class Docstring

```python
class UserService:
    """
    Service xử lý các thao tác liên quan đến User.
    
    Class này cung cấp các phương thức để tạo, đọc, cập nhật
    và xóa users trong hệ thống.
    
    Attributes:
        db_connection: Kết nối database
        cache: Cache instance (optional)
    
    Example:
        >>> service = UserService(db)
        >>> user = service.get_by_id(123)
        >>> print(user.name)
    
    Note:
        Sử dụng context manager cho transaction:
        >>> with service.transaction():
        ...     service.create(user_data)
    """
    
    def __init__(self, db_connection, cache=None):
        """
        Khởi tạo UserService.
        
        Args:
            db_connection: Database connection object
            cache: Optional cache instance for performance
        """
        self.db = db_connection
        self.cache = cache
```

### JavaScript JSDoc

```javascript
/**
 * Tính tổng tiền bao gồm thuế.
 * 
 * @param {Array<Object>} items - Danh sách items
 * @param {number} items[].price - Giá mỗi item
 * @param {number} items[].quantity - Số lượng
 * @param {number} [taxRate=0.1] - Tỷ lệ thuế (mặc định 10%)
 * @returns {number} Tổng tiền sau thuế
 * @throws {Error} Nếu items rỗng
 * 
 * @example
 * const items = [{ price: 100, quantity: 2 }];
 * const total = calculateTotal(items, 0.1);
 * console.log(total); // 220
 */
function calculateTotal(items, taxRate = 0.1) {
    if (!items.length) {
        throw new Error('Items cannot be empty');
    }
    
    const subtotal = items.reduce((sum, item) => 
        sum + (item.price * item.quantity), 0);
    
    return subtotal * (1 + taxRate);
}
```

### Inline Comments

```python
# ===== GOOD COMMENTS =====

# Tính discount dựa trên số lượng (bulk pricing)
# Mua 10+: giảm 10%, Mua 50+: giảm 20%
if quantity >= 50:
    discount = 0.2
elif quantity >= 10:
    discount = 0.1

# FIXME: Cần xử lý case user chưa verify email
# TODO: Thêm logging cho debug
# HACK: Workaround cho bug #123, cần refactor sau
# NOTE: API này sẽ deprecated trong v2.0

# ===== BAD COMMENTS (TRÁNH) =====

# Cộng 1 vào i (comment không cần thiết)
i = i + 1

# Gọi hàm calculate
calculate()  # comment thừa
```

---

## 📛**NAMING CONVENTIONS**

### Python (PEP 8)

```python
# Constants - UPPER_SNAKE_CASE
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"

# Variables và Functions - snake_case
user_name = "John"
total_amount = 0

def calculate_total_price(items, tax_rate):
    pass

def get_user_by_id(user_id):
    pass

# Classes - PascalCase
class UserService:
    pass

class DatabaseConnection:
    pass

# Private (convention) - prefix underscore
_internal_cache = {}

def _helper_function():
    pass

class MyClass:
    def __init__(self):
        self._private_var = 10
        self.__very_private = 20  # Name mangling
```

### JavaScript

```javascript
// Constants - UPPER_SNAKE_CASE
const MAX_RETRIES = 3;
const API_URL = 'https://api.example.com';

// Variables và Functions - camelCase
let userName = 'John';
let totalAmount = 0;

function calculateTotalPrice(items, taxRate) {
    // ...
}

const getUserById = (userId) => {
    // ...
};

// Classes - PascalCase
class UserService {
    constructor() {
        this.#privateField = 10;  // Private field (ES2022)
    }
}

// Components (React) - PascalCase
function UserProfile({ user }) {
    return <div>{user.name}</div>;
}
```

### Files và Folders

| Loại | Convention | Ví dụ |
|------|------------|-------|
| Python modules | snake_case | `user_service.py` |
| Python packages | snake_case | `my_package/` |
| JS/TS files | camelCase hoặc kebab-case | `userService.js`, `user-service.js` |
| React components | PascalCase | `UserProfile.jsx` |
| CSS files | kebab-case | `main-styles.css` |
| Config files | lowercase | `config.json`, `.env` |

---

## 📁**CẤU TRÚC FILE**

### Python File Structure

```python
"""
Module docstring - mô tả file
"""

# ================================================================
# IMPORTS
# ================================================================
# Standard library
import os
import sys
from datetime import datetime

# Third-party
import requests
import pandas as pd

# Local
from .utils import helper
from .models import User

# ================================================================
# CONSTANTS
# ================================================================
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
API_URL = "https://api.example.com"

# ================================================================
# CLASSES
# ================================================================
class MyClass:
    """Class description."""
    
    def __init__(self):
        pass
    
    def public_method(self):
        """Public method description."""
        pass
    
    def _private_method(self):
        """Private method description."""
        pass

# ================================================================
# FUNCTIONS
# ================================================================
def main():
    """Main function."""
    pass

def helper_function():
    """Helper function description."""
    pass

# ================================================================
# ENTRY POINT
# ================================================================
if __name__ == "__main__":
    main()
```

### JavaScript File Structure

```javascript
/**
 * @fileoverview Module description
 */

// ================================================================
// IMPORTS
// ================================================================
import React from 'react';
import { useState, useEffect } from 'react';

import { apiClient } from '@/services/api';
import { formatDate } from '@/utils/date';

import styles from './styles.module.css';

// ================================================================
// CONSTANTS
// ================================================================
const MAX_ITEMS = 100;
const DEFAULT_PAGE_SIZE = 20;

// ================================================================
// TYPES (TypeScript)
// ================================================================
interface User {
    id: number;
    name: string;
    email: string;
}

// ================================================================
// COMPONENT / MAIN FUNCTION
// ================================================================
function UserList({ initialUsers }) {
    // State
    const [users, setUsers] = useState(initialUsers);
    const [loading, setLoading] = useState(false);
    
    // Effects
    useEffect(() => {
        // ...
    }, []);
    
    // Handlers
    const handleClick = () => {
        // ...
    };
    
    // Render
    return (
        <div>...</div>
    );
}

// ================================================================
// HELPER FUNCTIONS
// ================================================================
function formatUser(user) {
    // ...
}

// ================================================================
// EXPORTS
// ================================================================
export default UserList;
export { formatUser };
```

---

## 📏**CODE STYLE RULES**

### Line Length

```python
# Tối đa 80-120 ký tự mỗi dòng
# Nếu dài hơn, xuống dòng:

# Method chaining
result = (
    df.filter(lambda x: x > 0)
    .map(lambda x: x * 2)
    .reduce(lambda a, b: a + b)
)

# Function arguments
def very_long_function_name(
    argument_one,
    argument_two,
    argument_three,
    argument_four
):
    pass

# Dictionary
config = {
    "database": "postgresql",
    "host": "localhost",
    "port": 5432,
    "username": "admin",
}
```

### Spacing

```python
# ===== Operators =====
# Good
x = 1 + 2
y = x * 3
if x == y:
    pass

# Bad
x=1+2
y=x*3

# ===== After comma =====
# Good
func(a, b, c)
my_list = [1, 2, 3]

# Bad
func(a,b,c)

# ===== Blank lines =====
# 2 blank lines giữa top-level definitions
class MyClass:
    pass


def my_function():
    pass


# 1 blank line giữa methods trong class
class MyClass:
    def method_one(self):
        pass
    
    def method_two(self):
        pass
```

### Imports

```python
# ===== Order =====
# 1. Standard library
import os
import sys

# 2. Third-party
import numpy as np
import pandas as pd

# 3. Local
from myapp import utils
from myapp.models import User

# ===== Style =====
# Good - một import mỗi dòng
import os
import sys

# Good - nhiều items từ cùng module
from datetime import datetime, timedelta, timezone

# Bad - wildcard import
from module import *

# Bad - quá dài
from mymodule import func1, func2, func3, func4, func5, func6

# Good - xuống dòng nếu nhiều
from mymodule import (
    func1,
    func2,
    func3,
    func4,
)
```

---

## ✅**CHECKLIST CODE REVIEW**

### Trước khi Commit

- [ ] Code có comments đầy đủ
- [ ] Functions có docstrings
- [ ] Naming conventions đúng
- [ ] Không có magic numbers (dùng constants)
- [ ] Không có code duplicate
- [ ] Error handling đầy đủ
- [ ] Tests pass

### Code Quality

```python
# ===== BAD =====
def calc(d, r):
    return d * r * 0.1

# ===== GOOD =====
TAX_RATE = 0.1

def calculate_tax(amount: float, rate: float = TAX_RATE) -> float:
    """
    Calculate tax for given amount.
    
    Args:
        amount: Base amount
        rate: Tax rate (default: 10%)
    
    Returns:
        Tax amount
    """
    return amount * rate
```

---

## 🔧**TOOLS**

### Python

```bash
# Formatter
pip install black
black .

# Linter
pip install flake8
flake8 .

# Import sorter
pip install isort
isort .

# Type checker
pip install mypy
mypy .
```

### JavaScript

```bash
# Formatter
npm install -D prettier
npx prettier --write .

# Linter
npm install -D eslint
npx eslint .
```

### Config files

```json
// .prettierrc
{
    "semi": true,
    "singleQuote": true,
    "tabWidth": 4,
    "printWidth": 100
}
```

```ini
# pyproject.toml
[tool.black]
line-length = 100
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 100
```

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
