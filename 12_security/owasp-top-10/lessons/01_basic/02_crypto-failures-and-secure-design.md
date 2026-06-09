# 🔐🏗️ A04 Cryptographic Failures + A06 Insecure Design

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 07/06/2026\
> **Level:** Basic (bài 02/5)\
> **Tags:** [MUST-KNOW]\
> **Prerequisites:** Bài [01_injection-and-access-control](01_injection-and-access-control.md) ✅, biết HTTPS cơ bản

> 🎯 *Bài 02. **A04 Cryptographic Failures** (OWASP Top 10:2025 — bản hiện hành; rename từ "Sensitive Data Exposure", từng đứng A02 ở 2021) — vuln về encryption, hashing, TLS. **A06 Insecure Design** (giới thiệu từ 2021, ở 2025 đứng A06) — flaw từ thiết kế chứ không phải implementation. Bài này dạy: symmetric vs asymmetric, password hashing (Argon2/bcrypt), TLS proper setup, JWT signing pitfalls, secure design patterns (threat-driven, secure by default), abuse case. Hands-on migrate Acme Shop password từ MD5 sang Argon2.*

> ⚠️ **Cập nhật chuẩn:** Bài đã chuyển sang **OWASP Top 10:2025** (final release). Trong bản này thứ tự thay đổi lớn: **A02 Security Misconfiguration** lên #2, **A03 Software Supply Chain Failures** là category MỚI (mở rộng từ "Vulnerable & Outdated Components"), **Injection** rớt xuống **A05**, **Insecure Design** xuống **A06**, **A10 Mishandling of Exceptional Conditions** là category MỚI, và **SSRF không còn category riêng — đã gộp vào A01 Broken Access Control**. Xem bảng mapping 2021↔2025 ở bài [00_what-is-owasp-and-application-security](00_what-is-owasp-and-application-security.md).

## 🎯 Sau bài này bạn sẽ

- [ ] Phân biệt **symmetric** (AES) vs **asymmetric** (RSA/ECDSA) — khi nào cái nào
- [ ] Hash password đúng: **Argon2id** (2026 default) hoặc **bcrypt** — không bao giờ MD5/SHA1/SHA256 raw
- [ ] Setup **TLS** đúng: 1.3 default, 1.2 minimum, cipher suite hardening
- [ ] **JWT** ký + verify đúng: HS256 vs RS256, `alg=none` pitfall, expiration
- [ ] **HSTS** + **Certificate Transparency** + **TLS pinning**
- [ ] Apply **secure design pattern**: fail closed, defense in depth, principle of least privilege from design
- [ ] Phân tích **abuse case** trong design phase
- [ ] Hands-on migrate Acme Shop hash từ MD5 sang Argon2

---

## Tình huống — Pen-test phát hiện crypto issue

Sếp tiếp tục pen-test report:

**Critical/High findings về crypto + design**:
1. User password hash bằng **MD5** trong DB (`password_hash` column).
2. JWT secret = `"acmeshop123"` trong code, ai có repo access đều biết.
3. HTTPS có nhưng cert path cấu hình expose `/api/internal/*` thẳng port 8080 không TLS.
4. "Forgot password" gửi password thật (plaintext) qua email.
5. Design flaw: feature "Refer-a-friend" cho ref code → attacker brute-force code → claim reward.

5 issue, mix giữa **crypto failures** (1-4) + **insecure design** (5). Bài này dạy fix.

---

## 1️⃣ A04 — Cryptographic Failures

🪞 **Ẩn dụ**: *Crypto như **két sắt ngân hàng** — chìa khóa (key) phải đủ chắc, ổ khóa (algorithm) không bị hỏng, két phải đặt đúng vị trí (in transit / at rest), người giữ chìa key phải đúng. Mỗi điểm yếu là 1 lỗi crypto.*

### 3 layer encryption

| Layer | What | Tool |
|---|---|---|
| **In transit** | Data trên đường truyền network | TLS 1.3 |
| **At rest** | Data trên đĩa (DB, file, backup) | AES-256-GCM, KMS |
| **In use** | Data trong memory | Confidential Computing (Intel SGX, AMD SEV) — niche |

### Symmetric vs Asymmetric

| Aspect | Symmetric | Asymmetric |
|---|---|---|
| Same key encrypt + decrypt? | Yes | No (public/private pair) |
| Speed | Fast (10-100x) | Slow |
| Algorithm | AES, ChaCha20 | RSA, ECDSA, Ed25519 |
| Use case | Encrypt large data | Key exchange, signature, identity |
| Key distribution challenge | Yes (must share securely) | No (publish public freely) |

→ Real-world: dùng **cả 2**. Asymmetric để exchange symmetric key (TLS handshake), rồi symmetric để encrypt payload.

### Algorithm chọn 2026

**Encryption (symmetric)**:
- ✅ **AES-256-GCM** (default 2026)
- ✅ **ChaCha20-Poly1305** (mobile, faster ARM)
- ❌ **AES-CBC** (padding oracle vuln nếu không có HMAC)
- ❌ **AES-ECB** (deterministic, leaks pattern)
- ❌ **DES, 3DES, RC4** (broken)

**Encryption (asymmetric)**:
- ✅ **RSA-3072+** (2026 minimum)
- ✅ **Ed25519** (modern signature)
- ✅ **ECDSA-P256/P384** (signature)
- ❌ **RSA-1024** (broken)

**Hashing (general)**:
- ✅ **SHA-256, SHA-3** (general purpose)
- ✅ **BLAKE3** (faster, modern)
- ❌ **MD5, SHA1** (collision broken — vẫn dùng được cho non-security checksum)

**Password hashing** (slow on purpose):
- ✅ **Argon2id** (2026 default — winner Password Hashing Competition 2015)
- ✅ **bcrypt** (mature, OK)
- ✅ **scrypt**
- ❌ **PBKDF2** (legacy compliance only — không offer GPU resistance)
- ❌ **SHA-256/MD5 raw** (cực kỳ tệ — GPU crack billion/s)

### Password hashing thực hành

```python
# ❌ Anti-pattern: MD5/SHA hash trực tiếp
import hashlib
hash = hashlib.md5(password.encode()).hexdigest()
# GPU crack 10 ký tự < 1 giờ

# ❌ Anti-pattern: SHA-256 raw
hash = hashlib.sha256(password.encode()).hexdigest()

# ✅ Pattern: Argon2id
from argon2 import PasswordHasher
ph = PasswordHasher(
    time_cost=3,        # iteration
    memory_cost=65536,  # 64 MB
    parallelism=4,
)
hash = ph.hash(password)
# → "$argon2id$v=19$m=65536,t=3,p=4$..."

# Verify
try:
    ph.verify(stored_hash, user_input)
    if ph.check_needs_rehash(stored_hash):
        new_hash = ph.hash(user_input)  # rehash với param mới
except VerifyMismatchError:
    raise HTTPException(401)
```

### Migrate hash legacy

```python
# DB: column password_hash + hash_algo
def verify_password(user_input: str, stored: str, algo: str) -> tuple[bool, str|None]:
    if algo == "md5":
        if hashlib.md5(user_input.encode()).hexdigest() == stored:
            # Rehash với Argon2id, return new hash
            return True, ph.hash(user_input)
        return False, None
    elif algo == "argon2":
        try:
            ph.verify(stored, user_input)
            return True, None
        except VerifyMismatchError:
            return False, None

# Login flow
ok, new_hash = verify_password(input_pw, user.password_hash, user.hash_algo)
if ok:
    if new_hash:
        user.password_hash = new_hash
        user.hash_algo = "argon2"
        db.commit()
    return token
```

→ Gradual migration mà không force user reset.

### Encryption at rest

**DB column-level**:
```python
# Encrypt PII với app-level key (key trong KMS)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
key = get_key_from_kms()  # AWS KMS / GCP KMS / Vault
aesgcm = AESGCM(key)
nonce = os.urandom(12)
ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), associated_data=None)
# Store: nonce + ciphertext (base64)
```

**Disk-level**:
- AWS EBS encryption (auto with KMS key).
- GCP Persistent Disk encryption (default).
- Azure Managed Disks SSE.

**Backup**:
- S3 Server-Side Encryption (SSE-S3, SSE-KMS, SSE-C).
- Encrypted snapshot.

### Encryption in transit (TLS proper)

```nginx
# nginx — TLS 1.3 only + strong cipher
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.acmeshop.vn;

    ssl_protocols TLSv1.3 TLSv1.2;  # TLS 1.3 preferred; 1.2 fallback
    ssl_ciphers "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256";
    ssl_prefer_server_ciphers off;  # TLS 1.3 ignores anyway
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;

    # HSTS — force HTTPS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # ...
}
```

**HSTS**: HTTP Strict Transport Security — browser refuse HTTP cho domain (after first visit).

Submit domain `acmeshop.vn` lên [HSTS Preload List](https://hstspreload.org/) → browser ship sẵn HSTS, không cần first visit.

### Certificate Transparency + TLS pinning

- **CT logs**: mọi cert phải log vào CT log (Chrome enforce). Bạn monitor CT log cho domain — phát hiện cert lạ được issue.
- **TLS pinning** (mobile app): app hardcode public key/cert fingerprint → reject cert khác. Trade-off: cert rotation phức tạp.

### Tool: Mozilla SSL Config Generator

[ssl-config.mozilla.org](https://ssl-config.mozilla.org/) generate nginx/apache/haproxy config theo profile (Modern/Intermediate/Old).

### Test TLS

```bash
# SSL Labs API (ngoài) hoặc tool offline
testssl.sh api.acmeshop.vn

# Quick check
openssl s_client -connect api.acmeshop.vn:443 -tls1_3
```

→ Test SSL Labs giả lập SSL Labs scan: grade A+ là target.

---

## 2️⃣ JWT — Common pitfalls

🪞 **Ẩn dụ**: *JWT như **vé concert có đóng dấu hologram** — server cấp vé, attacker không thể giả; nhưng nếu hologram giả được (alg=none), hoặc concert kết thúc rồi vé vẫn dùng (no expiration), hoặc 1 vé dùng được mọi show (no audience claim), thì vô dụng.*

### JWT cấu trúc

```
header.payload.signature
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.abc123
```

- **Header**: `{"alg": "HS256", "typ": "JWT"}` — algorithm + type.
- **Payload**: claims (sub, exp, iat, iss, aud, custom).
- **Signature**: HMAC/RSA signature.

### Cạm bẫy 1 — `alg=none` attack

**Vuln**: Library accept `alg=none` → no signature verify → attacker tạo JWT bất kỳ.

```
header = {"alg": "none"}
payload = {"sub": "admin", "exp": 9999999999}
token = base64(header) + "." + base64(payload) + "."  # empty signature
```

**Fix**: Explicit reject `alg=none`:
```python
import jwt
try:
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])  # ✅ explicit
except jwt.InvalidTokenError:
    raise HTTPException(401)
```

### Cạm bẫy 2 — HMAC vs RSA confusion

**Vuln**: Server expects RS256 (public key verify), attacker switch to HS256 và dùng **public key as HMAC secret** → server tự verify đúng.

**Fix**: Same — explicit `algorithms=` list.

### Cạm bẫy 3 — Weak secret HS256

**Vuln**: Secret = `"secret"` → brute-force JWT crack online.

**Fix**: Secret ≥ 256-bit random:
```python
import secrets
SECRET = secrets.token_urlsafe(32)  # store env / Vault
```

### Cạm bẫy 4 — Expiration missing

**Vuln**: Token không có `exp` → valid forever; leak = permanent compromise.

**Fix**:
```python
payload = {
    "sub": user.id,
    "iat": int(time.time()),
    "exp": int(time.time()) + 900,  # 15 phút
    "iss": "acmeshop.vn",
    "aud": "acmeshop-mobile",
}
```

Pattern: short access token + refresh token (long, opaque, stored DB) — revocation possible.

### Cạm bẫy 5 — Sensitive data trong payload

**Vuln**: JWT payload base64 encoded **không phải** encrypted → ai có token đọc được.

**Fix**: Không put password, full PII, secret vào claims. Dùng `JWE` (encrypted JWT) nếu thực sự cần.

### Cạm bẫy 6 — JWT in localStorage

**Vuln**: XSS → `document.localStorage` → token stolen.

**Fix**: httpOnly cookie thay localStorage; SameSite Strict.

---

## 3️⃣ A06 — Insecure Design

🪞 **Ẩn dụ**: *Insecure Design như **xây nhà cửa sổ hướng ra phố đông đúc** — không phải lỗi thợ xây (implementation), mà lỗi kiến trúc sư (design). Phải xem lại bản vẽ, không phải fix gạch.*

### Phân biệt với security misconfig

| Vuln type | Khi nào sinh | Fix ở đâu |
|---|---|---|
| Implementation (A05 Injection) | Code | Code |
| Misconfig (A02) | Deploy/config | Config |
| **Insecure Design (A06)** | **Architecture/Design** | **Architecture (re-design)** |

### Examples thực tế

**Example 1 — Refer-a-friend brute force**:

```
Acme Shop: User invite friend qua ref code 6-digit → friend nhập code → cả 2 nhận $10.
Design flaw: Ref code = 6 digit → 1M combination → bot brute force → claim mọi reward.
```

Implementation đúng 100% nhưng **design flaw**.

**Fix design**:
- Code 16-char random + user-specific.
- Rate limit per IP / per account / per code.
- Cap reward count per code.
- Anti-abuse: machine learning detect pattern.

**Example 2 — Password reset token đoán được**:

Design: token = `md5(email + timestamp)` → attacker biết email + đoán timestamp ±10s → token guess.

**Fix**: token = `secrets.token_urlsafe(32)` (cryptographically random).

**Example 3 — "Forgot password" gửi password thật**:

Design: System lưu password plaintext / reversible encrypt để có thể email lại.

**Fix**: Hash password (one-way). "Forgot password" → reset link với token, không email password.

**Example 4 — Subscription cancel ngay = free**:

User register monthly subscription → access 30 days → cancel ngay → vẫn dùng đến hết 30 days. Attacker register + cancel ngay → free 30 days mãi.

**Fix design**: Charge upfront non-refundable; or grace 7 days only.

**Example 5 — Voucher single-use bypass**:

Design: Check voucher trong code, but không lock concurrent.

```python
# Anti-pattern
voucher = db.query(Voucher).get(code)
if voucher.used:
    raise HTTPException(400)
voucher.used = True
db.commit()  # ❌ race: 100 request đồng thời all pass
```

**Fix**: Atomic update.
```python
result = db.execute(
    "UPDATE vouchers SET used=true WHERE code=:c AND used=false",
    {"c": code},
)
if result.rowcount == 0:
    raise HTTPException(400)
```

### Secure design patterns

| Pattern | Mô tả |
|---|---|
| **Fail closed** | Khi lỗi/uncertain → deny access (không allow) |
| **Defense in depth** | Multi-layer protection (xem bài 00) |
| **Least privilege** | Default no permission; explicit grant |
| **Separation of duties** | Critical action cần 2+ người |
| **Complete mediation** | Mỗi access check, không cache decision |
| **Secure by default** | Default config = secure, opt-in cho insecure |
| **Open design** | Security qua design, không obscurity |
| **Don't trust user input** | Validate at boundary, escape at output |
| **Zero trust** | Verify identity + context mỗi request |

### Abuse case analysis

Trong design phase, ngoài "happy path" + "edge case", thêm **abuse case**:

> *"Nếu tôi là attacker, tôi sẽ lợi dụng feature này thế nào?"*

| Feature | Use case | Abuse case |
|---|---|---|
| Forgot password | User quên → reset | Attacker enumerate email; spam reset email; brute-force token |
| Login | User login | Brute force password; credential stuffing; account lockout DoS |
| File upload | User upload avatar | Upload malware; XSS via SVG; oversized file DoS |
| API rate limit per user | Prevent abuse | Forge user → distribute across many account |
| Referral code | Invite friend | Brute-force code; self-referral abuse |
| Free trial | New user thử | Multi-account abuse |

### Tool: STRIDE per feature + Misuse case diagram

Trong design doc, thêm section "Misuse cases" — list 3-5 abuse case + mitigation cho mỗi feature.

---

## 4️⃣ Threat-driven design

### Workflow

```
1. Design feature (happy + edge case)
2. Apply STRIDE per data flow (bài 00)
3. Identify abuse cases
4. Add controls trong design (rate limit, validation, audit log)
5. Document threat model trong design doc
6. Code review check threat coverage
7. Pen-test verify
8. Monitor production for abuse signal
```

### Acme Shop "Refer-a-friend" — Threat-driven redesign

**Original design** (insecure):
- Ref code 6-digit.
- User input code → both receive $10.
- No rate limit.

**STRIDE analysis**:
- **S**poof: Attacker generate fake account, claim reward.
- **T**amper: Modify code in request to claim.
- **I**nfo: Enumerate codes → find valid.
- **D**oS: Spam request → exhaust reward pool.
- **E**lev: Self-referral (refer own alt account).

**Redesigned**:
- Code = 16-char random + user_id binding.
- Rate limit 5 attempts/hour per IP.
- Server validates: claimer_id ≠ referrer_id.
- Reward cap: 10 referral per referrer per month.
- Audit log every claim.
- Anti-abuse ML score: flag suspicious pattern.

→ Design **trước khi code** = rẻ. Fix sau prod = đắt + lộ data.

---

## 🛠️ Hands-on — Migrate Acme Shop password to Argon2

### Mục tiêu

DB hiện có 100k user `password_hash` = MD5. Migrate sang Argon2id gradual (không force reset).

### Bước 1 — Schema

```sql
ALTER TABLE users ADD COLUMN hash_algo VARCHAR(20) DEFAULT 'md5';
```

### Bước 2 — Helper

```python
from argon2 import PasswordHasher, exceptions
import hashlib

ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)

def verify_and_upgrade(user_input: str, stored_hash: str, algo: str):
    if algo == "md5":
        if hashlib.md5(user_input.encode()).hexdigest() == stored_hash:
            return True, ph.hash(user_input), "argon2"
        return False, None, None
    elif algo == "argon2":
        try:
            ph.verify(stored_hash, user_input)
            if ph.check_needs_rehash(stored_hash):
                return True, ph.hash(user_input), "argon2"
            return True, None, None
        except exceptions.VerifyMismatchError:
            return False, None, None
    raise ValueError(f"Unknown algo: {algo}")
```

### Bước 3 — Login flow

```python
@app.post("/api/login")
def login(data: LoginIn):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(401)

    ok, new_hash, new_algo = verify_and_upgrade(data.password, user.password_hash, user.hash_algo)
    if not ok:
        raise HTTPException(401)

    if new_hash:
        user.password_hash = new_hash
        user.hash_algo = new_algo
        db.commit()
        log.info(f"Rehashed password for user_id={user.id}")

    return {"token": create_token(user)}
```

### Bước 4 — Verify

- Login user cũ → password verify MD5 OK → DB updated to Argon2.
- Next login → verify Argon2.
- Sau 6 tháng → run report: bao nhiêu user còn MD5 (= inactive). Force reset hoặc deprecate.

### Bước 5 — JWT secret rotation

```bash
# Move secret to env / Vault
export JWT_SECRET=$(python -c 'import secrets; print(secrets.token_urlsafe(64))')

# Code
SECRET = os.environ["JWT_SECRET"]
if not SECRET or len(SECRET) < 32:
    raise RuntimeError("JWT_SECRET too short or missing")
```

→ Rotate secret quarterly + after any leak suspicion.

### Bước 6 — TLS config + HSTS

Apply Mozilla SSL Config Modern profile + HSTS preload submit.

---

## 💡 Cạm bẫy thường gặp & Best practice

### 1. "Encryption = security"

**Bẫy**: Encrypt mọi thứ → tưởng safe.

**Thực tế**: Key management quan trọng hơn algorithm. Hardcoded key = encryption vô nghĩa.

**Fix**: Key trong KMS/HSM, rotation, audit.

### 2. Roll-your-own crypto

**Bẫy**: Tự viết hash function "improved".

**Fix**: Dùng library standard (libsodium, AES from `cryptography`).

### 3. ECB mode

**Bẫy**: AES-ECB encrypt image → outline image visible trong ciphertext.

**Fix**: AES-GCM (authenticated encryption) — không bao giờ ECB.

### 4. Nonce reuse

**Bẫy**: Reuse nonce với AES-GCM → break security.

**Fix**: Random nonce mỗi encryption; hoặc counter unique.

### 5. PBKDF2 với low iteration

**Bẫy**: PBKDF2 với 1000 iteration → modern GPU break.

**Fix**: Argon2id; nếu buộc dùng PBKDF2 (compliance), iteration ≥ **600.000** (khuyến nghị **OWASP** Password Storage Cheat Sheet cho PBKDF2-HMAC-SHA256, ngữ cảnh FIPS-140).
> 📝 *Đừng gán nhầm con số này cho NIST. NIST SP 800-63B chỉ yêu cầu iteration tối thiểu 10.000, "chọn càng cao càng tốt theo hiệu năng" — không nêu con số 600k. 600k là của OWASP.*

### 6. JWT trong URL

**Bẫy**: `?token=xxx` trong URL → logged everywhere (proxy, browser history, referrer).

**Fix**: Header `Authorization: Bearer` hoặc httpOnly cookie.

### 7. "Forgot password" → email password thật

**Bẫy**: Lưu password plaintext / reversible để có thể recover.

**Fix**: Reset link với token, không recover password (one-way hash).

### 8. Cert pinning + cert rotation conflict

**Bẫy**: Pin cert trong mobile app → cert rotation = app broken.

**Fix**: Pin public key của intermediate CA (rotation hiếm), không leaf cert; hoặc backup pin.

---

## 🧠 Tự kiểm tra (Self-check)

- [ ] Symmetric vs Asymmetric — chọn cho 3 use case?
- [ ] Tại sao Argon2id > bcrypt > PBKDF2 > SHA-256?
- [ ] TLS 1.3 cipher suite tối thiểu cho 2026?
- [ ] HSTS header complete với preload?
- [ ] JWT 4 pitfall + fix mỗi cái?
- [ ] Insecure Design vs Misconfig — phân biệt?
- [ ] Threat-driven design workflow 8 bước?
- [ ] Abuse case 3 ví dụ + mitigation?

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Term | Vietnamese / Explanation |
|---|---|
| **Symmetric encryption** | Same key encrypt + decrypt (AES) |
| **Asymmetric encryption** | Public/private key pair (RSA, ECDSA) |
| **AES-GCM** | Authenticated encryption với associated data |
| **Argon2id** | Password hashing winner PHC 2015 — 2026 default |
| **bcrypt** | Older password hash, mature |
| **PBKDF2** | Legacy compliance; weak vs GPU |
| **HKDF** | Key derivation function (extract + expand) |
| **TLS** | Transport Layer Security — replace SSL |
| **HSTS** | HTTP Strict Transport Security header |
| **HSTS Preload** | Browser ship list domain force HTTPS |
| **CT log** | Certificate Transparency — public log mọi cert |
| **TLS pinning** | App hardcode cert/key fingerprint |
| **JWT** | JSON Web Token — token format |
| **JWE** | JSON Web Encryption — encrypted JWT |
| **JWS** | JSON Web Signature — signed JWT |
| **Insecure Design** | Vuln từ design, không phải code bug |
| **Abuse case** | Use case từ góc nhìn attacker |
| **Fail closed** | Default deny khi uncertain |
| **Secure by default** | Default config = secure |
| **KMS** | Key Management Service |
| **HSM** | Hardware Security Module |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [A01 Broken Access Control (gồm SSRF) + A05 Injection](01_injection-and-access-control.md)
- ➡️ **Bài tiếp theo:** [A02 Misconfig + A03 Software Supply Chain Failures](03_misconfig-vulnerable-components-supply-chain.md) *(sắp viết)*
- ↑ **Về cụm:** [OWASP README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- 🔒 [Cryptography](../../../cryptography/) — deep
- 📡 [TLS/SSL](../../../tls-ssl/)
- 🌐 [HTTPS lesson](../../../../05_networking/http-https/lessons/01_basic/04_https-tls.md)
- 🐍 [FastAPI auth JWT](../../../../07_web/backend/python-fastapi/lessons/01_basic/04_auth-and-middleware.md)
- ↑ **Về cụm:** [Authentication cluster](../../../authentication/)

### Tài nguyên ngoài (2026)
- 📖 [OWASP Top 10:2025 (bản hiện hành)](https://owasp.org/Top10/2025/)
- 📖 [OWASP A04:2025 — Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/)
- 📖 [OWASP A06:2025 — Insecure Design](https://owasp.org/Top10/2025/A06_2025-Insecure_Design/)
- 📖 [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- 📖 [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- 📖 [OWASP Transport Layer Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)
- 📖 [Mozilla SSL Config Generator](https://ssl-config.mozilla.org/)
- 📖 [HSTS Preload List](https://hstspreload.org/)
- 📖 [SSL Labs SSL Test](https://www.ssllabs.com/ssltest/)
- 📖 [testssl.sh](https://testssl.sh/)
- 📖 [Argon2 spec](https://github.com/P-H-C/phc-winner-argon2)
- 📖 [libsodium](https://doc.libsodium.org/) — modern crypto library
- 📖 [NIST SP 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html) — digital identity guidelines
- 📖 [JWT.io](https://jwt.io/) — JWT debugger

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 02 OWASP basic. A02 Crypto Failures (symmetric/asymmetric, algorithm 2026, password hashing Argon2id, TLS proper, HSTS, JWT pitfalls) + A04 Insecure Design (threat-driven design, abuse cases, secure patterns) + hands-on migrate MD5→Argon2 Acme Shop + 8 pitfalls.
- **v2.0.0 (07/06/2026)** — Cập nhật sang **OWASP Top 10:2025** (final release). Đổi numbering: Cryptographic Failures A02→**A04**, Insecure Design A04→**A06**; bảng phân biệt vuln type dùng số hiệu 2025 (Injection A05, Misconfig A02). Thêm ghi chú thay đổi chuẩn (A02 Misconfig lên #2, A03 Software Supply Chain mới, A10 Mishandling mới, SSRF gộp A01) + link bài 00 cho mapping 2021↔2025. Sửa nav bài trước/sau theo numbering 2025. Cập nhật link tài nguyên OWASP sang URL 2025. Sửa attribution sai: PBKDF2 ≥ 600.000 iteration là khuyến nghị **OWASP** (không phải NIST) — bổ sung làm rõ NIST SP 800-63B chỉ yêu cầu tối thiểu 10.000.
