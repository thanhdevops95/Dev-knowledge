# Hướng dẫn Security Basics

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Tổng hợp các kiến thức bảo mật cơ bản cho developers.

---

## 🔐**MẬT KHẨU & AUTHENTICATION**

### Hash mật khẩu (Python)

```python
# KHÔNG BAO GIỜ LƯU MẬT KHẨU PLAINTEXT!

# Sử dụng bcrypt
import bcrypt

# Hash password
password = "mypassword123"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode(), salt)

# Verify password
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)
```

### Quy tắc mật khẩu

| Yêu cầu | Tối thiểu |
|---------|-----------|
| Độ dài | 8 ký tự (khuyến nghị 12+) |
| Chữ hoa | Ít nhất 1 |
| Chữ thường | Ít nhất 1 |
| Số | Ít nhất 1 |
| Ký tự đặc biệt | Ít nhất 1 |

### JWT (JSON Web Token)

```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key-here"

# Tạo token
def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Verify token
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token hết hạn
    except jwt.InvalidTokenError:
        return None  # Token không hợp lệ
```

---

## 🛡️**SQL INJECTION**

### Vấn đề

```python
# NGUY HIỂM - KHÔNG LÀM THẾ NÀY!
query = f"SELECT * FROM users WHERE username = '{username}'"
# Input: admin' OR '1'='1
# Query: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
```

### Giải pháp: Parameterized Queries

```python
# SQLite
cursor.execute(
    "SELECT * FROM users WHERE username = ?",
    (username,)
)

# PostgreSQL (psycopg2)
cursor.execute(
    "SELECT * FROM users WHERE username = %s",
    (username,)
)

# SQLAlchemy ORM
user = session.query(User).filter(User.username == username).first()
```

---

## 🔒**XSS (Cross-Site Scripting)**

### Vấn đề

```html
<!-- User input được render trực tiếp -->
<div>{{ user_comment }}</div>

<!-- Input: <script>alert('XSS')</script> -->
<!-- Kết quả: Script chạy trên browser! -->
```

### Giải pháp

```python
# Python - Escape HTML
from markupsafe import escape

safe_text = escape(user_input)

# Jinja2 - Auto-escape (mặc định bật)
{{ user_comment }}  # Tự động escape

# Nếu cần render HTML (CẨN THẬN!)
{{ user_comment | safe }}  # Chỉ dùng khi tin tưởng source
```

```javascript
// JavaScript - Dùng textContent thay vì innerHTML
element.textContent = userInput;  // An toàn
element.innerHTML = userInput;    // NGUY HIỂM!
```

---

## 🔐**CSRF (Cross-Site Request Forgery)**

### Vấn đề

```html
<!-- Trang độc hại có thể gửi request đến trang của bạn -->
<img src="https://bank.com/transfer?to=hacker&amount=1000">
```

### Giải pháp: CSRF Token

```python
# Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
```

```html
<!-- Template -->
<form method="POST">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    ...
</form>
```

---

## 📁**FILE UPLOAD**

### Kiểm tra file

```python
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    if file.content_length > MAX_FILE_SIZE:
        raise ValueError("File too large")
    
    if not allowed_file(file.filename):
        raise ValueError("File type not allowed")
    
    # Làm sạch filename
    filename = secure_filename(file.filename)
    
    # Tạo tên unique
    unique_filename = f"{uuid.uuid4()}_{filename}"
    
    file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
```

---

## 🌐**HTTPS**

### Tại sao cần HTTPS?

| HTTP | HTTPS |
|------|-------|
| Không mã hóa | Mã hóa SSL/TLS |
| Dữ liệu có thể bị đọc | Dữ liệu được bảo vệ |
| Không xác thực server | Xác thực bằng certificate |

### Bắt buộc HTTPS

```python
# Flask
from flask_talisman import Talisman

Talisman(app)
```

```nginx
# Nginx - Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 🔑**QUẢN LÝ SECRETS**

### KHÔNG commit secrets!

```gitignore
# .gitignore
.env
*.key
*.pem
config.local.json
secrets.json
```

### Sử dụng Environment Variables

```python
import os

# Đọc từ environment
API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Với giá trị mặc định
DEBUG = os.getenv("DEBUG", "False") == "True"
```

### File .env

```bash
# .env (KHÔNG commit file này!)
API_KEY=your-secret-api-key
DATABASE_URL=postgres://user:pass@localhost/db
SECRET_KEY=your-secret-key
```

```python
# Đọc .env với python-dotenv
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
```

---

## 📋**SECURITY HEADERS**

```python
# Flask với Talisman
from flask_talisman import Talisman

csp = {
    'default-src': "'self'",
    'script-src': "'self'",
    'style-src': "'self'",
}

Talisman(
    app,
    content_security_policy=csp,
    force_https=True
)
```

### Headers quan trọng

| Header | Mục đích |
|--------|----------|
| `Content-Security-Policy` | Chống XSS |
| `X-Content-Type-Options` | Chống MIME sniffing |
| `X-Frame-Options` | Chống Clickjacking |
| `X-XSS-Protection` | XSS filter (cũ) |
| `Strict-Transport-Security` | Bắt buộc HTTPS |

---

## 🔍**INPUT VALIDATION**

```python
import re
from pydantic import BaseModel, validator, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    @validator('username')
    def username_valid(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', v):
            raise ValueError('Invalid username')
        return v
    
    @validator('password')
    def password_strong(cls, v):
        if len(v) < 8:
            raise ValueError('Password too short')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password needs uppercase')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password needs number')
        return v
```

---

## 📝**LOGGING (Không log sensitive data!)**

```python
import logging

logger = logging.getLogger(__name__)

# Tốt
logger.info(f"User {user.id} logged in")

# KHÔNG TỐT - Log password!
logger.info(f"User {username} with password {password}")

# KHÔNG TỐT - Log full credit card
logger.info(f"Payment with card {card_number}")

# Tốt - Mask sensitive data
logger.info(f"Payment with card ****{card_number[-4:]}")
```

---

## ✅**CHECKLIST BẢO MẬT**

### Authentication
- [ ] Hash passwords với bcrypt/argon2
- [ ] Implement rate limiting cho login
- [ ] Sử dụng HTTPS
- [ ] Secure session cookies

### Data Protection
- [ ] Parameterized queries (chống SQL injection)
- [ ] Escape output (chống XSS)
- [ ] CSRF tokens
- [ ] Validate tất cả input

### Secrets
- [ ] Không commit secrets vào git
- [ ] Sử dụng environment variables
- [ ] Rotate secrets định kỳ

### Infrastructure
- [ ] Cập nhật dependencies thường xuyên
- [ ] Sử dụng security headers
- [ ] Enable CORS đúng cách
- [ ] Log và monitor

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
