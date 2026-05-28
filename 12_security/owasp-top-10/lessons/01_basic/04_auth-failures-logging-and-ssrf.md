# 🔑📜🌐 A07 Auth Failures + A09 Logging Failures + A10 SSRF

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 04/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~22 phút\
> **Prerequisites:** Bài [03_misconfig-vulnerable-components-supply-chain](03_misconfig-vulnerable-components-supply-chain.md) ✅

> 🎯 *Bài 04 (cuối basic). **A07 Identification and Authentication Failures** (password policy, MFA, session, OAuth2/OIDC) + **A09 Security Logging and Monitoring Failures** (audit log, SIEM, alerting) + **A10 Server-Side Request Forgery** (Capital One 2019 case, mitigation). Hands-on Acme Shop add MFA + audit log + SSRF protection. Đóng cluster OWASP basic.*

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

**A07 Auth**:
1. Password policy: minimum 6 chars, no MFA.
2. JWT no `exp` — token vĩnh viễn.
3. Session không rotation khi privilege change.
4. Account lockout: 5 attempts → lock 24h → attacker brute-force email = DoS.

**A09 Logging**:
5. No audit log cho admin action.
6. Log có nhưng không alert — pentest test 3 ngày trước, ops không phát hiện.
7. Login fail không log → brute force im lặng.

**A10 SSRF**:
8. `POST /api/import-from-url` — nhập URL → server fetch → có thể hit `http://169.254.169.254` (AWS metadata) → steal credential.

Bài này map fix từng cái. Cuối bài đóng cluster basic.

---

## 1️⃣ A07 — Identification and Authentication Failures

🪞 **Ẩn dụ**: *Authentication như **kiểm tra giấy tờ ở sân bay** — không chỉ check passport (password) mà cần boarding pass (token), check-in (session), security gate (MFA). Mỗi điểm yếu là 1 lỗ hổng.*

### Password policy — NIST 2024+ guidelines

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

### MFA — 3 generations

| Generation | Type | Pros | Cons |
|---|---|---|---|
| **SMS OTP** | SMS code | Universal | SIM swap, intercept |
| **TOTP** (Authenticator) | RFC 6238, 30s code | Free, offline | Phishing possible |
| **WebAuthn / Passkey** | Hardware-bound public key | Phishing-resistant, biometric UX | Newer; need device support |

→ **2026 best practice**: WebAuthn primary, TOTP fallback, SMS only for SMS-receiving-impossible.

### TOTP implementation

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

### WebAuthn implementation (sketch)

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

### Session management

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

### Credential stuffing protection

Credential stuffing = attacker dùng leaked credential từ breach khác → try login.

**Mitigation**:
- Check breach list (haveibeenpwned API).
- MFA mandatory (top defense).
- Behavioral analysis (impossible travel, new device).
- Cloudflare Turnstile / hCaptcha challenge.

### OAuth2 + OIDC flows

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

## 2️⃣ A09 — Security Logging and Monitoring Failures

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

### Log structure (JSON)

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

### Audit log specific

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

### Monitor + alert

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

### Tool stack 2026

| Layer | Tool option | Note |
|---|---|---|
| **Log collection** | Fluent Bit, Vector, Filebeat | Lightweight agent |
| **Log aggregation** | Loki (Grafana), Elasticsearch, Splunk | Centralize |
| **SIEM** | Splunk ES, Elastic Security, Microsoft Sentinel, Datadog Cloud SIEM | Correlate + detect |
| **Cloud-native** | AWS CloudWatch Logs + Security Hub, GCP Cloud Logging + SCC, Azure Monitor + Sentinel | Vendor |
| **Open-source SIEM** | Wazuh, Security Onion | Free |
| **Alerting** | PagerDuty, Opsgenie, Slack | On-call rotation |

### Time to detect — IBM Cost of Breach 2024

- **Average time to detect**: 204 days
- **Average time to contain**: 73 days
- **Cost reduction with breach < 200 days**: 23% less

→ Better logging + alert = faster detect = less damage.

---

## 3️⃣ A10 — Server-Side Request Forgery (SSRF)

🪞 **Ẩn dụ**: *SSRF như **lừa người gác cổng tự đi gọi điện thay bạn** — bạn không vào được nội bộ (intranet), nhưng nhờ server gọi giúp → server có access nội bộ → leak.*

### Vulnerable pattern

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

### Capital One 2019 case study

- WAF misconfigured (A05) + SSRF (A10) → attacker:
  1. SSRF qua WAF endpoint.
  2. Hit EC2 metadata → steal IAM role credential.
  3. Use credential → access S3 → 106M records.
- Penalty: $80M fine, $190M settlement.

### SSRF target — Internal endpoint

| Target | Risk |
|---|---|
| `http://169.254.169.254` | AWS/GCP/Azure metadata service (IMDSv1) |
| `http://localhost:*` | Internal service (DB, admin panel) |
| `http://10.*` `http://192.168.*` | Private network |
| `http://[::1]` | IPv6 localhost |
| `file:///etc/passwd` | Local file (if scheme allowed) |
| `gopher://` `dict://` | Other protocols → exploit |

### Mitigation — 5 layer

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

### Safe SSRF pattern

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
@app.post("/api/login")
def login(data):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not ph.verify(user.password_hash, data.password):
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

### Re-pentest result

- 8 critical/high → 0.
- Mozilla Observatory: A+.
- SOC2 audit ready.

---

## 🏆 Cluster wrap-up — OWASP Top 10 basic ĐÓNG

Bạn đã đi qua:

| Bài | Coverage | Key takeaway |
|---|---|---|
| 00 | OWASP intro + STRIDE + DREAD + defense-in-depth | Security mindset shift-left |
| 01 | A01 + A03 | Parameterize query, RBAC/ABAC, CSP, SameSite |
| 02 | A02 + A04 | Argon2id, TLS 1.3, JWT pitfalls, abuse case |
| 03 | A05 + A06 + A08 | Security headers, dependency scan, cosign + SLSA |
| 04 | A07 + A09 + A10 | MFA WebAuthn/TOTP, audit log + SIEM, SSRF mitigation |

→ **5 bài, ~110p đọc, ~10-15h hands-on**. Output: app theo OWASP Top 10 best practice.

Next options:
- **Intermediate cluster**: hardening deep (CSP nonce SHA, OAuth2 advanced, Zero Trust deep).
- **Specialized clusters**: authentication/, authorization/, cryptography/, tls-ssl/ (sibling clusters in 12_security).
- **Career**: Security Engineer roadmap.

---

## ⚠️ Pitfalls

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

## 🎯 Self-check

- [ ] Password policy NIST 2024 — 5 thay đổi vs cũ?
- [ ] TOTP setup + verify code Python?
- [ ] Session management 6 property + recommend?
- [ ] OAuth2 + PKCE flow — vì sao PKCE quan trọng?
- [ ] Audit log 10 event must-log + 6 must-not-log?
- [ ] SSRF 5 mitigation layer?
- [ ] Capital One 2019 case — 2 vuln chain?
- [ ] WebAuthn vs TOTP vs SMS — chọn cho app financial?

---

## 📚 Glossary

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

### Trong cluster
- ↶ Trước: [03_misconfig-vulnerable-components-supply-chain](03_misconfig-vulnerable-components-supply-chain.md)
- ↑ Cluster OWASP: [OWASP README](../../README.md)
- ↑ Cluster 12_security: [12_security README](../../../README.md)

### Cross-reference
- 🔐 [Authentication cluster](../../../authentication/) — deep on OAuth/OIDC/MFA
- 🔑 [Authorization cluster](../../../authorization/) — RBAC/ABAC deep
- 🐍 [FastAPI auth JWT](../../../../07_web/backend/python-fastapi/lessons/01_basic/04_auth-and-middleware.md)
- 📊 [Observability SRE](../../../../10_devops/observability/lessons/02_intermediate/04_sre-practices.md)
- 🔒 [Secrets Management](../../../secrets-management/)

### Tài nguyên ngoài (2026)
- 📖 [OWASP A07](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
- 📖 [OWASP A09](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)
- 📖 [OWASP A10](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_(SSRF)/)
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

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 04 (cuối basic) OWASP. A07 (NIST 2024 password, TOTP/WebAuthn MFA, session mgmt, OAuth2+PKCE+OIDC) + A09 (audit log, WORM, SIEM, alert, MTTD) + A10 SSRF (Capital One 2019, 5 mitigation layer) + hands-on final hardening Acme Shop 8 findings + 8 pitfalls. **Đóng OWASP Top 10 basic cluster 5/5.**
