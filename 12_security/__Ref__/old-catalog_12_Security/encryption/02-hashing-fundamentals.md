# 🔑 Hashing — Băm mật mã

> `[INTERMEDIATE]` — Integrity, password storage, digital signatures

---

## Hashing là gì?

Hash function biến input **bất kỳ kích thước** thành output **kích thước cố định** (digest/hash). Quá trình này **1 chiều** — không thể tìm lại input từ hash.

```
Input (bất kỳ size)        Hash Function       Output (cố định size)
─────────────────          ─────────────       ─────────────────────
"hello"               →    SHA-256         →   2cf24dba5fb0a30e...  (64 hex chars)
"hello!"              →    SHA-256         →   ce06092fb948d9ff...  (64 hex chars)
War and Peace (3MB)   →    SHA-256         →   a1b2c3d4e5f6a7b8...  (64 hex chars)
```

**3 tính chất quan trọng:**

1. **Deterministic**: Cùng input → LUÔN cùng output
2. **Avalanche effect**: Thay đổi 1 bit input → output thay đổi ~50% bits
3. **Pre-image resistance**: Từ hash → KHÔNG thể tìm lại input

---

## 1. Ứng dụng của Hashing

### File Integrity — Kiểm tra file không bị sửa

Khi download phần mềm, website thường cung cấp checksum:

```bash
# Download file
curl -O https://example.com/app-v2.0.tar.gz

# Verify checksum
sha256sum app-v2.0.tar.gz
# Output: a1b2c3d4...  app-v2.0.tar.gz

# So sánh với checksum trên website
# Nếu khớp → file không bị sửa (man-in-the-middle attack)
```

### Git — Mỗi commit là 1 SHA-1 hash

```bash
git log --oneline
# a3f2d1b feat: add user profile
# 8e4c2a9 fix: null pointer in getUser
# ↑ đây là SHA-1 hash của commit content

# Thay đổi BẤT KỲ gì trong history → hash thay đổi → bị phát hiện!
```

### Data Deduplication — Tìm file trùng

```python
import hashlib
import os

def find_duplicates(directory):
    hashes = {}
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            with open(filepath, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            if file_hash in hashes:
                print(f"Duplicate: {filepath} == {hashes[file_hash]}")
            else:
                hashes[file_hash] = filepath
```

### HMAC — Xác thực message

HMAC (Hash-based Message Authentication Code) kết hợp hash + secret key → chứng minh message đến từ đúng nguồn:

```javascript
import crypto from 'crypto';

// Tạo HMAC signature
function signPayload(payload, secret) {
    return crypto
        .createHmac('sha256', secret)
        .update(JSON.stringify(payload))
        .digest('hex');
}

// Verify — dùng cho webhook, API authentication
function verifySignature(payload, signature, secret) {
    const expected = signPayload(payload, secret);
    // timing-safe comparison: chống timing attack!
    return crypto.timingSafeEqual(
        Buffer.from(signature, 'hex'),
        Buffer.from(expected, 'hex'),
    );
}

// Ứng dụng: Stripe webhook verification
app.post('/webhook/stripe', (req, res) => {
    const sig = req.headers['stripe-signature'];
    const valid = verifySignature(req.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
    if (!valid) return res.status(401).send('Invalid signature');
    // Process webhook...
});
```

---

## 2. So sánh Hash Algorithms

| Algorithm | Output | Speed | Security | Use case |
|---|---|---|---|---|
| **MD5** | 128 bits | Rất nhanh | ❌ Broken | ~~Không dùng~~ (legacy only) |
| **SHA-1** | 160 bits | Nhanh | ❌ Broken | ~~Không dùng~~ (Git đang migrate) |
| **SHA-256** | 256 bits | Nhanh | ✅ Secure | File integrity, blockchain, HMAC |
| **SHA-3** | 256 bits | Trung bình | ✅ Secure | Standard mới, backup cho SHA-2 |
| **bcrypt** | 184 bits | Chậm (by design) | ✅ | Password hashing |
| **Argon2** | Configurable | Chậm (by design) | ✅ Best | Password hashing (newest) |
| **BLAKE3** | 256 bits | Cực nhanh | ✅ | File hashing, high performance |

**Rule of thumb:**
- **Passwords** → bcrypt hoặc Argon2 (CHẬM = tốt)
- **Data integrity** → SHA-256 (nhanh, đủ secure)
- **HMAC** → SHA-256 + secret key
- **Performance-critical hashing** → BLAKE3

---

## 3. Tấn công & Phòng thủ

### Rainbow Table Attack

Attacker pre-compute hash cho hàng tỷ passwords phổ biến:

```
"password123" → ef92b778bafe771e89245b89ecbc08a4
"admin"       → 21232f297a57a5a743894a0e4a801fc3
...
(hàng tỷ entries)
```

Khi có DB leak → tra bảng → tìm password ngay!

**Phòng thủ: Salt** — thêm random string vào TRƯỚC khi hash:

```
Không salt:
  hash("password123") = ef92b778... (tra rainbow table → found!)

Có salt:
  hash("x7k9m2" + "password123") = 8a3f2d1b... (KHÔNG có trong rainbow table!)
  
  Mỗi user có salt KHÁC NHAU → attacker phải tính lại cho TỪNG user.
  bcrypt/Argon2 tự quản lý salt.
```

### Timing Attack

```javascript
// ❌ So sánh string thường → attacker đo thời gian từng ký tự
if (signature === expected) { ... }
// Ký tự đầu sai → return sớm (nhanh)
// 3 ký tự đầu đúng → return chậm hơn → attacker biết 3 ký tự

// ✅ Constant-time comparison → luôn mất cùng thời gian
crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b));
```

---

## Bài tập thực hành

- [ ] File checksum: verify downloaded file integrity
- [ ] HMAC: implement webhook signature verification
- [ ] Password: migrate từ MD5 → bcrypt (real scenario)
- [ ] Deduplication: tìm files trùng trong folder

---

## Tài nguyên thêm

- [Crypto101](https://www.crypto101.io/) — Free book
- [CrackStation](https://crackstation.net/) — Demo rainbow table (educational)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
