# 🔑📜🌐 A07 Authentication Failures + A09 Logging & Alerting Failures + SSRF (gộp A01)

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.1\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 11/06/2026\
> **Level:** Basic (bài 04/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** Bài [03_misconfig-vulnerable-components-supply-chain](03_misconfig-vulnerable-components-supply-chain.md) ✅

> 🎯 *Bài 04 (cuối basic), chuẩn **OWASP Top 10:2025** (bản hiện hành). **A07:2025 Authentication Failures** (password policy, MFA, session, OAuth2/OIDC) + **A09:2025 Security Logging and Alerting Failures** (audit log, SIEM, alerting) + **Server-Side Request Forgery (SSRF)** — ở bản 2025, SSRF không còn là category riêng mà **gộp vào A01:2025 Broken Access Control** (Capital One 2019 case, mitigation). Hands-on Acme Shop add MFA + audit log + SSRF protection. Đóng cluster OWASP basic.*

> ℹ️ **Lưu ý chuẩn 2025:** bài này theo OWASP Top 10:2025 (bản final, đợt thứ 8). So với 2021: **A05 Security Misconfiguration → A02:2025**, **A06 Vulnerable & Outdated Components → mở rộng thành A03:2025 Software Supply Chain Failures (mới)**, **Injection → A05:2025**, **Insecure Design → A06:2025**, và xuất hiện category mới **A10:2025 Mishandling of Exceptional Conditions**. Riêng **SSRF (A10:2021) đã bị gộp vào A01:2025 Broken Access Control** — không còn category độc lập. Trong bài, mình vẫn dạy SSRF như một kỹ thuật tấn công riêng biệt vì kiến thức kỹ thuật không đổi; chỉ vị trí trong bảng xếp hạng thay đổi.

## 🎯 Sau bài này bạn sẽ

- [ ] Implement **password policy** đúng NIST 2024+ (length > complexity)
- [ ] Setup **MFA**: TOTP (Authenticator), WebAuthn (passkey), SMS (legacy)
- [ ] Quản lý **session**: rotation, idle timeout, absolute timeout, concurrent limit
- [ ] OAuth2 + **OIDC** flow đúng: Authorization Code + PKCE, không Implicit
- [ ] **Account lockout vs rate limit** — tránh DoS lockout
- [ ] **Audit log** đầy đủ: actor, action, resource, time, IP, success/fail
- [ ] Setup **SIEM/alert** cho security event (Datadog, Splunk, ELK)
- [ ] Hiểu **SSRF** + Capital One 2019 case + 5 mitigation layer
- [ ] Đóng cluster OWASP Top 10 basic

---

## Tình huống — Final pentest findings + post-incident

Sếp tổng kết pentest:

**A07:2025 Authentication Failures**:
1. Password policy: minimum 6 chars, no MFA.
2. JWT no `exp` — token vĩnh viễn.
3. Session không rotation khi privilege change.
4. Account lockout: 5 attempts → lock 24h → attacker brute-force email = DoS.

**A09:2025 Security Logging and Alerting Failures**:
5. No audit log cho admin action.
6. Log có nhưng không alert — pentest test 3 ngày trước, ops không phát hiện.
7. Login fail không log → brute force im lặng.

**SSRF (thuộc A01:2025 Broken Access Control)**:
8. `POST /api/import-from-url` — nhập URL → server fetch → có thể hit `http://169.254.169.254` (AWS metadata) → steal credential.

Bài này map fix từng cái. Cuối bài đóng cluster basic.

---

## 1️⃣ A07:2025 — Authentication Failures

> 📝 *Bản 2021 gọi là "Identification and Authentication Failures"; bản 2025 rút gọn tên thành "Authentication Failures", vị trí vẫn ở A07.*

🪞 **Ẩn dụ**: *Authentication như **kiểm tra giấy tờ ở sân bay** — không chỉ check passport (password) mà cần boarding pass (token), check-in (session), security gate (MFA). Mỗi điểm yếu là 1 lỗ hổng.*

### Password policy — Hướng dẫn NIST 2024+

| Old practice | New (NIST SP 800-63B) |
|---|---|
| Minimum 6-8 chars | **Minimum 8, recommend 15** |
| Mix upper/lower/digit/symbol | **No composition rule** (length > complexity) |
| Force change every 90 days | **Don't force periodic change** (chỉ on suspected compromise) |
| Allow common password | **Block top 10k common passwords** + breached list |
| Password hint Q&A | **Remove security questions** (researchable) |

```python
# Verify policy
from password_strength import PasswordPolicy
import pwnedpasswords  # haveibeenpwned API

policy = PasswordPolicy.from_names(
    length=8,           # min 8
    # no uppercase/special required — modern guideline
)

def validate_password(pw: str):
    if policy.test(pw):
        raise ValueError("Password too weak")
    # Check breach
    count = pwnedpasswords.check(pw)
    if count > 0:
        raise ValueError(f"Password leaked in {count} breach. Choose another.")
```

### MFA — 3 thế hệ

| Generation | Type | Pros | Cons |
|---|---|---|---|
| **SMS OTP** | SMS code | Universal | SIM swap, intercept |
| **TOTP** (Authenticator) | RFC 6238, 30s code | Free, offline | Phishing possible |
| **WebAuthn / Passkey** | Hardware-bound public key | Phishing-resistant, biometric UX | Newer; need device support |

→ **2026 best practice**: WebAuthn primary, TOTP fallback, SMS only for SMS-receiving-impossible.

### Triển khai TOTP

```python
import pyotp
import qrcode

# Setup phase
def enable_totp(user: User):
    secret = pyotp.random_base32()
    user.totp_secret = secret  # encrypt in DB
    uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.email,
        issuer_name="Acme Shop",
    )
    qr = qrcode.make(uri)
    return qr  # show to user to scan with Google Authenticator

# Verify phase
def verify_totp(user: User, code: str) -> bool:
    totp = pyotp.TOTP(user.totp_secret)
    return totp.verify(code, valid_window=1)  # ±30s tolerance
```

### Triển khai WebAuthn (phác thảo)

```python
# Library: python-fido2 or webauthn
from webauthn import generate_registration_options, verify_registration_response

# Registration
options = generate_registration_options(
    rp_id="acmeshop.vn",
    rp_name="Acme Shop",
    user_id=user.id,
    user_name=user.email,
)
# → Frontend uses navigator.credentials.create() with options
# → Send response back
result = verify_registration_response(credential_data, expected_challenge=..., expected_rp_id=...)
user.webauthn_credentials.append(result.credential_id)
```

### Quản lý session

| Property | Recommendation 2026 |
|---|---|
| **Session ID** | Cryptographic random (≥ 128-bit entropy) |
| **Storage** | Server-side (Redis), not client-side |
| **Cookie attr** | `httponly`, `secure`, `samesite=strict` |
| **Idle timeout** | 15-30 phút (sensitive); 1-7 days (consumer) |
| **Absolute timeout** | 8-24 hours |
| **Rotation** | After login, after privilege change (admin, password change) |
| **Concurrent limit** | Optional: 1-3 device per account |

```python
# Rotate session on privilege change
@app.post("/change-password")
def change_password(...):
    # ... validate + update password
    old_session = request.session.get("id")
    new_session_id = secrets.token_urlsafe(32)
    redis.delete(f"session:{old_session}")
    redis.set(f"session:{new_session_id}", user.id, ex=3600)
    response.set_cookie("session_id", new_session_id, ...)
```

### Account lockout vs rate limit

**Account lockout** (bad):
- 5 fail → lock account 24h.
- Attacker: enumerate email, lock everyone → DoS.

**Rate limit per IP + per account** (good):
- 5 fail/account/hour → CAPTCHA challenge (not lock).
- Or progressive delay: 1s, 2s, 4s, 8s, 16s, ...
- Notify user on suspicious pattern.

```python
# Per-IP + per-account
from limits import storage, strategies, parse

limiter = strategies.FixedWindowRateLimiter(storage.RedisStorage(...))

@app.post("/login")
def login(...):
    ip_limit = parse("5/minute")
    if not limiter.hit(ip_limit, "login_ip", request.client.host):
        raise HTTPException(429)
    account_limit = parse("10/hour")
    if not limiter.hit(account_limit, "login_account", email):
        raise HTTPException(429)
    # ... actual login
```

### Phòng chống credential stuffing

Credential stuffing = attacker dùng leaked credential từ breach khác → try login.

**Mitigation**:
- Check breach list (haveibeenpwned API).
- MFA mandatory (top defense).
- Behavioral analysis (impossible travel, new device).
- Cloudflare Turnstile / hCaptcha challenge.

### Các flow OAuth2 + OIDC

| Flow | When to use | Recommend 2026 |
|---|---|---|
| **Authorization Code + PKCE** | Web app, mobile, SPA | ✅ Default |
| **Client Credentials** | Server-to-server | ✅ M2M |
| **Device Code** | Smart TV, CLI tool | ✅ |
| **Implicit** | Old SPA | ❌ Deprecated 2024 |
| **Password (ROPC)** | Legacy | ❌ Avoid (gives password to client) |

```python
# Authorization Code + PKCE flow (sketch)
# 1. Frontend generate code_verifier (random) + code_challenge = SHA256(code_verifier)
# 2. Redirect user to OAuth provider with code_challenge
# 3. User approves, provider redirects back with authorization_code
# 4. Frontend POST code + code_verifier to token endpoint
# 5. Provider verify challenge matches → issue access_token + refresh_token
```

### OIDC = OAuth2 + Identity layer

OIDC adds:
- **ID Token** (JWT) — encode identity (sub, email, name).
- **`/userinfo`** endpoint.
- **Standard scopes**: `openid`, `profile`, `email`.

```python
# Verify ID token
from authlib.jose import jwt
claims = jwt.decode(id_token, jwks_uri="https://issuer.com/.well-known/jwks.json")
claims.validate()
assert claims["iss"] == "https://issuer.com"
assert claims["aud"] == client_id
user_id = claims["sub"]
```

---

## 2️⃣ A09:2025 — Security Logging and Alerting Failures

> 📝 *Bản 2021 gọi là "Security Logging and Monitoring Failures"; bản 2025 đổi "Monitoring" → "Alerting" để nhấn mạnh: có log + có theo dõi vẫn chưa đủ, phải **trigger cảnh báo (alert)** kịp thời. Vị trí vẫn ở A09.*

🪞 **Ẩn dụ**: *Logging + monitoring như **camera an ninh** — không có camera = không biết ai vào ra; có camera nhưng không xem = vô dụng; xem nhưng không trigger alarm khi có bất thường = chậm.*

### Phải log gì

| Event category | Log? | Example |
|---|---|---|
| **Authentication** | ✅ Always | Login success/fail, logout, MFA challenge |
| **Authorization** | ✅ Always | Permission denied, role change |
| **Account changes** | ✅ | Password change, email change, MFA setup/remove |
| **Admin action** | ✅ Always | User promote, data export, config change |
| **Data access (sensitive)** | ✅ | Read PII, financial record |
| **Input validation fail** | ✅ | SQL injection attempt, XSS attempt |
| **Resource access** | ✅ For audit | Order view, file download |
| **System event** | ✅ | Service restart, deploy, scale |

### Cấu trúc log (JSON)

```json
{
    "timestamp": "2026-05-24T14:30:00Z",
    "level": "INFO",
    "event": "user.login",
    "outcome": "success",
    "actor": {
        "user_id": "u_12345",
        "email": "thien.le@acmeshop.vn",
        "ip": "203.0.113.42",
        "user_agent": "Mozilla/5.0..."
    },
    "resource": null,
    "trace_id": "abc123",
    "session_id": "s_xyz789"
}
```

→ Structured JSON → grep/filter dễ; SIEM tự parse.

### KHÔNG log

| Field | Why not |
|---|---|
| Password (plaintext or hashed) | Never |
| Session token / JWT | Token in log = token leak |
| API key | Same |
| Full credit card | PCI compliance |
| Full PII (passport, SSN) | Privacy law |
| OAuth refresh token | Token leak |

→ Sanitize trước log; tool: `pii-detector`, manual review log schema.

### Audit log chuyên biệt

Cho action critical (admin, financial, data export), log **immutable append-only**:

- Lưu kèm signature/hash chain (blockchain-style).
- Storage: dedicated bucket WORM (Write Once Read Many) — S3 Object Lock, GCS Retention Policy.
- Retention: 1-7 năm (theo compliance SOC2/PCI/HIPAA/GDPR).

```python
import hashlib

def audit(actor, action, resource, outcome, prev_hash=""):
    entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "actor": actor,
        "action": action,
        "resource": resource,
        "outcome": outcome,
        "prev_hash": prev_hash,
    }
    entry["hash"] = hashlib.sha256(json.dumps(entry, sort_keys=True).encode()).hexdigest()
    s3.put_object(Bucket="audit-bucket", Key=f"{date}/{entry['hash']}.json", Body=json.dumps(entry))
    return entry["hash"]
```

### Giám sát + cảnh báo

| Signal | Alert? | Threshold |
|---|---|---|
| Login fail spike | ✅ | > 100/min from same IP |
| Login from new country | ⚠️ Warn | After geolocation lookup |
| Admin action outside business hours | ✅ | Anomaly |
| MFA disable | ✅ Critical | Always |
| Data export volume | ✅ | > X MB / X records |
| API 401/403 spike | ✅ | > N% requests |
| Session count spike per user | ✅ | > 10 |
| Failed SQL injection attempt | ⚠️ | Pattern detect |

### Bộ công cụ (tool stack) 2026

| Layer | Tool option | Note |
|---|---|---|
| **Log collection** | Fluent Bit, Vector, Filebeat | Lightweight agent |
| **Log aggregation** | Loki (Grafana), Elasticsearch, Splunk | Centralize |
| **SIEM** | Splunk ES, Elastic Security, Microsoft Sentinel, Datadog Cloud SIEM | Correlate + detect |
| **Cloud-native** | AWS CloudWatch Logs + Security Hub, GCP Cloud Logging + SCC, Azure Monitor + Sentinel | Vendor |
| **Open-source SIEM** | Wazuh, Security Onion | Free |
| **Alerting** | PagerDuty, Opsgenie, Slack | On-call rotation |

### Thời gian phát hiện — IBM Cost of a Data Breach 2024

- **Average time to identify**: 194 days
- **Average time to contain**: 64 days
- **Tổng breach lifecycle**: 258 days (mức thấp nhất trong 7 năm)
- **Chi phí**: breach có lifecycle **< 200 ngày** rẻ hơn trung bình **~$1.39M** so với breach kéo dài hơn

→ Better logging + alert = faster detect = less damage. Nguồn: IBM Cost of a Data Breach Report 2024.

---

## 3️⃣ SSRF — Server-Side Request Forgery (thuộc A01:2025 Broken Access Control)

> 📝 *Ở bản 2021, SSRF là một category độc lập (A10:2021). Bản **2025 đã gộp SSRF vào A01:2025 Broken Access Control** — vì bản chất SSRF là server bị ép truy cập tài nguyên ngoài phạm vi cho phép (một dạng broken access control). Kiến thức kỹ thuật và cách phòng thủ dưới đây không thay đổi; chỉ vị trí trong Top 10 thay đổi.*

🪞 **Ẩn dụ**: *SSRF như **lừa người gác cổng tự đi gọi điện thay bạn** — bạn không vào được nội bộ (intranet), nhưng nhờ server gọi giúp → server có access nội bộ → leak.*

### Pattern dễ bị tấn công

```python
# Anti-pattern
@app.post("/api/import-from-url")
def import_url(url: str):
    response = requests.get(url, timeout=10)
    return response.text
```

Attacker:
```
url=http://169.254.169.254/latest/meta-data/iam/security-credentials/role-name
```

→ AWS EC2 metadata endpoint → leak IAM role credentials → attacker assume role → access S3/RDS.

### Case study Capital One 2019

- WAF misconfigured (A02:2025 Security Misconfiguration) + SSRF (thuộc A01:2025 Broken Access Control) → attacker:
  1. SSRF qua WAF endpoint.
  2. Hit EC2 metadata → steal IAM role credential.
  3. Use credential → access S3 → 106M records.
- Penalty: $80M fine, $190M settlement.

### Mục tiêu SSRF — Endpoint nội bộ

| Target | Risk |
|---|---|
| `http://169.254.169.254` | AWS/GCP/Azure metadata service (IMDSv1) |
| `http://localhost:*` | Internal service (DB, admin panel) |
| `http://10.*` `http://192.168.*` | Private network |
| `http://[::1]` | IPv6 localhost |
| `file:///etc/passwd` | Local file (if scheme allowed) |
| `gopher://` `dict://` | Other protocols → exploit |

### Cách phòng chống — 5 lớp

**Layer 1 — Disable IMDSv1** (cloud metadata):
```bash
# AWS: enforce IMDSv2 (require token)
aws ec2 modify-instance-metadata-options \
    --instance-id i-12345 \
    --http-tokens required \
    --http-put-response-hop-limit 1
```

**Layer 2 — Allowlist destination**:
```python
ALLOWED_HOSTS = {"api.acmeshop.vn", "cdn.acmeshop.vn"}

def validate_url(url: str):
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP(S) allowed")
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"Host not in allowlist")
```

**Layer 3 — Block private IP**:
```python
import ipaddress
import socket

def resolve_and_validate(url: str):
    host = urlparse(url).hostname
    ip = socket.gethostbyname(host)
    addr = ipaddress.ip_address(ip)
    if addr.is_private or addr.is_loopback or addr.is_link_local:
        raise ValueError("Internal IP not allowed")
    return ip
```

⚠️ **Race condition**: DNS resolution lúc validate khác lúc fetch (DNS rebinding). Mitigation: resolve once, use IP for fetch.

**Layer 4 — Network ACL**:
- Egress firewall: app server không có route to internal metadata IP.
- VPC endpoint policy.
- K8s NetworkPolicy block egress to `169.254.0.0/16`.

**Layer 5 — Use library safe**:
```python
# Library safer SSRF (Python)
import safeurl
safeurl.fetch("http://example.com")  # blocks private IP by default
```

### Pattern SSRF an toàn

```python
@app.post("/api/import-from-url")
def import_url(url: str):
    # 1. Validate allowlist
    if not is_allowed_host(url):
        raise HTTPException(400, "Host not in allowlist")
    # 2. Resolve + block private IP
    ip = resolve_and_validate(url)
    # 3. Set timeout + redirect limit
    response = requests.get(
        url,
        timeout=10,
        allow_redirects=False,  # ⚠️ redirect can bypass allowlist
        proxies={"http": "http://egress-proxy"},  # via egress proxy
    )
    return response.text
```

---

## 🛠️ Hands-on — Acme Shop full hardening

### Mục tiêu

Address final 8 pentest findings từ section "Tình huống".

### Fix 1-4 — Auth

```python
# 1. Password policy + breach check
def set_password(user, pw):
    validate_password(pw)  # NIST + breach check
    user.password_hash = ph.hash(pw)

# 2. JWT exp
token = jwt.encode({
    "sub": user.id, "exp": time.time() + 900, "iat": time.time(),
}, SECRET, algorithm="HS256")

# 3. Session rotation
@app.post("/change-password")
def change_pw(...):
    rotate_session(user)

# 4. Replace lockout with rate limit
# (xem section 1)
```

### Fix MFA setup

```python
@app.post("/api/mfa/enable-totp")
def enable_totp(user: User = Depends(current_user)):
    secret = pyotp.random_base32()
    user.totp_secret_encrypted = encrypt_with_kms(secret)  # encrypt at rest
    db.commit()
    uri = pyotp.totp.TOTP(secret).provisioning_uri(user.email, "Acme Shop")
    return {"uri": uri}  # frontend render QR

@app.post("/api/login/verify-totp")
def verify_totp(code: str, user: User):
    secret = decrypt_with_kms(user.totp_secret_encrypted)
    if not pyotp.TOTP(secret).verify(code, valid_window=1):
        audit(user.id, "mfa.fail", outcome="fail")
        raise HTTPException(401)
    audit(user.id, "mfa.success", outcome="success")
    return create_session(user)
```

### Fix 5-7 — Logging

```python
# 5+6 — Audit middleware
@app.middleware("http")
async def audit_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    # Log every request (sample if too verbose)
    log.info(json.dumps({
        "ts": datetime.utcnow().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration_ms": int(duration * 1000),
        "ip": request.client.host,
        "user_id": getattr(request.state, "user_id", None),
        "trace_id": request.headers.get("x-trace-id"),
    }))
    return response

# 7 — Login fail explicit log
from argon2.exceptions import VerifyMismatchError, InvalidHashError

@app.post("/api/login")
def login(data):
    user = db.query(User).filter(User.email == data.email).first()
    # argon2-cffi: ph.verify() trả True khi đúng, RAISE VerifyMismatchError khi sai
    # (không trả False) → phải bọc try/except, không dùng `not ph.verify(...)`
    login_ok = False
    if user:
        try:
            ph.verify(user.password_hash, data.password)
            login_ok = True
        except (VerifyMismatchError, InvalidHashError):
            login_ok = False
    if not login_ok:
        log.warning(json.dumps({
            "event": "login.fail",
            "email": data.email,  # email OK to log (not secret)
            "ip": request.client.host,
            "ts": datetime.utcnow().isoformat(),
        }))
        raise HTTPException(401)
    ...

# Alert setup (example with Datadog)
# Metric: login.fail rate > 50/min → alert PagerDuty
```

### Fix 8 — SSRF

```python
@app.post("/api/import-from-url")
def import_url(data: ImportIn, user: User = Depends(require_role("editor"))):
    url = data.url
    # Validate
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(400)
    if parsed.hostname not in ALLOWED_IMPORT_HOSTS:
        raise HTTPException(400, "Host not in allowlist")

    # Resolve, block private
    ip = socket.gethostbyname(parsed.hostname)
    if ipaddress.ip_address(ip).is_private:
        raise HTTPException(400, "Private IP not allowed")

    # Fetch via egress proxy
    response = requests.get(
        url,
        timeout=10,
        allow_redirects=False,
        proxies={"http": EGRESS_PROXY, "https": EGRESS_PROXY},
    )
    if response.status_code != 200:
        raise HTTPException(502)
    return {"content": response.text[:10000]}  # limit size
```

### Kết quả pen-test lại

- 8 critical/high → 0.
- Mozilla Observatory: A+.
- SOC2 audit ready.

---

## 🏆 Cluster wrap-up — OWASP Top 10:2025 basic ĐÓNG

Bạn đã đi qua (numbering theo **OWASP Top 10:2025**):

| Bài | Coverage (2025) | Key takeaway |
|---|---|---|
| 00 | OWASP intro + STRIDE + DREAD + defense-in-depth | Security mindset shift-left |
| 01 | A01:2025 Broken Access Control (gồm SSRF) + A05:2025 Injection | Parameterize query, RBAC/ABAC, CSP, SameSite |
| 02 | A04:2025 Cryptographic Failures + A02:2025 Security Misconfiguration | Argon2id, TLS 1.3, JWT pitfalls, abuse case |
| 03 | A03:2025 Software Supply Chain Failures (mới) + A06:2025 Insecure Design + A08:2025 Software or Data Integrity Failures | Security headers, dependency scan, cosign + SLSA |
| 04 | A07:2025 Authentication Failures + A09:2025 Logging & Alerting Failures + SSRF (A01) | MFA WebAuthn/TOTP, audit log + SIEM, SSRF mitigation |

> ℹ️ **2 category mới ở bản 2025** mà cluster có chạm tới: **A03:2025 Software Supply Chain Failures** (mở rộng từ "Vulnerable & Outdated Components" 2021 — bài 03) và **A10:2025 Mishandling of Exceptional Conditions** (xử lý lỗi/điều kiện ngoại lệ sai cách — sẽ đào sâu ở cluster intermediate). Ngoài ra **SSRF không còn là category riêng**, đã gộp vào A01:2025.

→ **5 bài, ~110p đọc, ~10-15h hands-on**. Output: app theo OWASP Top 10:2025 best practice.

Next options:
- **Intermediate cluster**: hardening deep (CSP nonce SHA, OAuth2 advanced, Zero Trust deep).
- **Specialized clusters**: authentication/, authorization/, cryptography/, tls-ssl/ (sibling clusters in 12_security).
- **Career**: Security Engineer roadmap.

---

## 💡 Cạm bẫy thường gặp & Best practice

### 1. Account lockout = DoS amplifier

**Fix**: Rate limit + CAPTCHA, không lock.

### 2. SMS MFA only

**Fix**: TOTP/WebAuthn primary, SMS fallback only.

### 3. Audit log có nhưng không alert

**Fix**: SIEM rule + on-call escalation.

### 4. Log password / token

**Fix**: Sanitize log schema review.

### 5. SSRF allowlist nhưng follow redirect

**Fix**: `allow_redirects=False` hoặc validate sau redirect.

### 6. Session never rotates

**Fix**: Rotate sau login + privilege change + password change.

### 7. JWT no exp

**Fix**: Always set `exp` ≤ 15 phút cho access token.

### 8. Trust client-side IP detection

**Fix**: `X-Forwarded-For` from trusted proxy only; otherwise use connection IP.

---

## 🧠 Tự kiểm tra (Self-check)

- [ ] Password policy NIST 2024 — 5 thay đổi vs cũ?
- [ ] TOTP setup + verify code Python?
- [ ] Session management 6 property + recommend?
- [ ] OAuth2 + PKCE flow — vì sao PKCE quan trọng?
- [ ] Audit log 10 event must-log + 6 must-not-log?
- [ ] SSRF 5 mitigation layer?
- [ ] Capital One 2019 case — 2 vuln chain?
- [ ] WebAuthn vs TOTP vs SMS — chọn cho app financial?

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Term | Vietnamese / Explanation |
|---|---|
| **MFA** | Multi-Factor Authentication |
| **2FA** | Two-Factor (subset of MFA) |
| **TOTP** | Time-based One-Time Password (RFC 6238) |
| **HOTP** | HMAC-based OTP |
| **WebAuthn** | Web Authentication API (FIDO2) — phishing-resistant |
| **Passkey** | Branded WebAuthn (Apple/Google) |
| **OIDC** | OpenID Connect — identity layer on OAuth2 |
| **PKCE** | Proof Key for Code Exchange |
| **JWT** | JSON Web Token |
| **Session ID** | Server-side session reference |
| **Credential stuffing** | Use leaked credentials to try login |
| **Account lockout** | Disable account after N fail (anti-pattern alone) |
| **Audit log** | Immutable record of action |
| **WORM storage** | Write Once Read Many (compliance) |
| **SIEM** | Security Information and Event Management |
| **MTTD** | Mean Time To Detect |
| **MTTC** | Mean Time To Contain |
| **SSRF** | Server-Side Request Forgery |
| **IMDSv1/v2** | AWS Instance Metadata Service (v2 require token) |
| **DNS rebinding** | Attack changing DNS response between resolve and fetch |
| **NIST SP 800-63B** | Digital identity guidelines (2024) |
| **haveibeenpwned** | Breach DB API |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [A03:2025 Software Supply Chain Failures + A06:2025 Insecure Design + A08:2025 Software or Data Integrity Failures](03_misconfig-vulnerable-components-supply-chain.md)
- ↑ **Về cụm:** [OWASP README](../../README.md)
- ↑ **Về cụm:** [12_security README](../../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- ↑ **Về cụm:** [Authentication cluster](../../../authentication/) — deep on OAuth/OIDC/MFA
- ↑ **Về cụm:** [Authorization cluster](../../../authorization/) — RBAC/ABAC deep
- 🐍 [FastAPI auth JWT](../../../../07_web/backend/python-fastapi/lessons/01_basic/04_auth-and-middleware.md)
- 📊 [Observability SRE](../../../../10_devops/observability/lessons/02_intermediate/04_sre-practices.md)
- 🔒 [Secrets Management](../../../secrets-management/)

### Tài nguyên ngoài (2026)
- 📖 [OWASP Top 10:2025 (bản hiện hành)](https://owasp.org/Top10/2025/)
- 📖 [OWASP A07:2025 — Authentication Failures](https://owasp.org/Top10/2025/)
- 📖 [OWASP A09:2025 — Security Logging and Alerting Failures](https://owasp.org/Top10/2025/)
- 📖 [OWASP A01:2025 — Broken Access Control (gồm SSRF)](https://owasp.org/Top10/2025/)
- 📖 [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- 📖 [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- 📖 [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- 📖 [OWASP SSRF Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- 📖 [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html)
- 📖 [haveibeenpwned API](https://haveibeenpwned.com/API/v3)
- 📖 [WebAuthn Guide](https://webauthn.guide/)
- 📖 [Passkeys.io](https://www.passkeys.io/)
- 📖 [OAuth 2.1 draft](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1)
- 📖 [IBM Cost of Data Breach Report](https://www.ibm.com/reports/data-breach)
- 📖 [Capital One Postmortem](https://krebsonsecurity.com/2019/08/what-we-can-learn-from-the-capital-one-hack/)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 04 (cuối basic) OWASP. A07 (NIST 2024 password, TOTP/WebAuthn MFA, session mgmt, OAuth2+PKCE+OIDC) + A09 (audit log, WORM, SIEM, alert, MTTD) + A10 SSRF (Capital One 2019, 5 mitigation layer) + hands-on final hardening Acme Shop 8 findings + 8 pitfalls. **Đóng OWASP Top 10 basic cluster 5/5.**
- **v2.0.1 (11/06/2026)** — Việt hoá heading nội dung mô tả sang tiếng Việt (giữ thuật ngữ/brand/param) theo Vietnamese-first.
- **v2.0.0 (07/06/2026)** — Cập nhật sang **OWASP Top 10:2025** (bản hiện hành, final release). A07 đổi tên "Identification and Authentication Failures" → "Authentication Failures"; A09 đổi "Monitoring" → "Alerting"; SSRF (A10:2021) **gộp vào A01:2025 Broken Access Control** — không còn category riêng. Cluster wrap-up + tham chiếu chéo cập nhật theo numbering 2025, nêu rõ 2 category mới (A03 Software Supply Chain Failures, A10 Mishandling of Exceptional Conditions). Sửa lỗi: số liệu IBM Cost of a Data Breach 2024 (identify 194 ngày, contain 64 ngày, lifecycle 258 ngày, breach <200 ngày rẻ hơn ~$1.39M) thay cho 204/73 ngày + "23% less"; bọc `ph.verify()` của argon2-cffi trong try/except bắt `VerifyMismatchError` (verify RAISE chứ không trả False). Map Capital One case sang A02:2025 + A01:2025. Link OWASP trỏ về bản 2025.
