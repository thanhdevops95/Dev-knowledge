# 🔐 Encryption & Hashing — Mật mã học cho Developer

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Bảo vệ data in transit & at rest

---

## Encryption vs Hashing — Khác nhau thế nào?

Đây là 2 concepts **hoàn toàn khác nhau** mà nhiều developer nhầm lẫn:

```
Encryption (Mã hóa):
  Plaintext → 🔑 Key → Ciphertext → 🔑 Key → Plaintext
  CÓ THỂ giải mã ngược. Dùng khi CẦN đọc lại data gốc.
  Ví dụ: Tin nhắn, file, API keys, thẻ tín dụng.

Hashing (Băm):
  Input → Hash Function → Hash value
  KHÔNG THỂ giải ngược. Dùng khi KHÔNG CẦN đọc data gốc.
  Ví dụ: Passwords, file integrity, checksums.
```

Một cách dễ nhớ:
- **Encryption** = khóa tủ (mở được bằng chìa khóa)
- **Hashing** = xay thịt (không thể biến thịt xay thành miếng thịt)

---

## 1. Hashing — Mật khẩu & Integrity

### Tại sao không lưu plaintext password?

Nếu database bị hack, tất cả passwords lộ. Năm 2012, LinkedIn bị hack 6.5 triệu passwords vì lưu hash yếu (SHA-1 không salt). Bạn **PHẢI** hash passwords.

### Chọn đúng hash algorithm

```
❌ MD5      → Broken. Collision attacks dễ dàng. KHÔNG BAO GIỜ dùng.
❌ SHA-1    → Broken. Google chứng minh collision năm 2017.
❌ SHA-256  → Nhanh quá! GPU crack 10 tỷ hashes/giây → brute force dễ.

✅ bcrypt   → Chậm BY DESIGN. Có salt tự động. Standard hiện tại.
✅ Argon2   → Winner Password Hashing Competition 2015. Chống GPU attack.
✅ scrypt   → Memory-hard. Tốn RAM để compute → GPU không hiệu quả.
```

**Tại sao cần "chậm"?** Vì password hash chỉ cần compute 1 lần (khi login). Nhưng attacker phải compute hàng tỷ lần (brute force). Hash nhanh (SHA-256) giúp attacker, hash chậm (bcrypt) giúp bạn.

### Bcrypt implementation

```typescript
import bcrypt from 'bcryptjs';

// Salt rounds = "cost factor". Mỗi +1 → chậm gấp đôi.
// 10 = ~100ms, 12 = ~300ms, 14 = ~1s
const SALT_ROUNDS = 12;

// Hash password (khi register)
async function hashPassword(password: string): Promise<string> {
    // bcrypt tự generate random salt + embed vào hash
    return bcrypt.hash(password, SALT_ROUNDS);
}

// Verify password (khi login)
async function verifyPassword(password: string, hash: string): Promise<boolean> {
    return bcrypt.compare(password, hash);
    // bcrypt extract salt từ hash → hash input password → compare
}

// Kết quả hash format:
// $2b$12$LJ3m4ys3Lk0TDbGA4MNZweYMfOJGXJGsPKdfrJfax3VDJv/sJINy.
// $2b  = algorithm (bcrypt)
// $12  = cost factor (12 rounds)
// $LJ3m4ys3Lk0TDbGA4MNZwe = salt (22 chars)
// YMfOJGXJGsPKdfrJfax3VDJv/sJINy. = hash (31 chars)
```

### Data Integrity — SHA-256

```javascript
import crypto from 'crypto';

// File checksum — kiểm tra file không bị sửa
function fileChecksum(filePath) {
    const hash = crypto.createHash('sha256');
    const stream = fs.createReadStream(filePath);
    return new Promise((resolve) => {
        stream.on('data', (chunk) => hash.update(chunk));
        stream.on('end', () => resolve(hash.digest('hex')));
    });
}

// API webhook verification — chứng minh request từ đúng nguồn
function verifyWebhook(payload, signature, secret) {
    const expected = crypto
        .createHmac('sha256', secret)
        .update(payload)
        .digest('hex');
    return crypto.timingSafeEqual(
        Buffer.from(signature),
        Buffer.from(expected),
    );
    // timingSafeEqual: chống timing attack
}
```

---

## 2. Symmetric Encryption — 1 key cho encrypt & decrypt

**Cùng 1 chìa khóa** để khóa và mở. Nhanh, dùng cho large data.

Vấn đề: Làm sao chia sẻ key an toàn?

```
Alice ──key──► Bob     Nếu Eve chặn key trên đường → game over!
```

### AES-256-GCM (Standard hiện tại)

```typescript
import crypto from 'crypto';

// GCM = Galois/Counter Mode: encrypt + authenticate (detect tampering)
function encrypt(plaintext: string, key: Buffer): { encrypted: string; iv: string; tag: string } {
    const iv = crypto.randomBytes(12);  // Initialization Vector: PHẢI random mỗi lần!
    const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);

    let encrypted = cipher.update(plaintext, 'utf8', 'hex');
    encrypted += cipher.final('hex');

    return {
        encrypted,
        iv: iv.toString('hex'),
        tag: cipher.getAuthTag().toString('hex'),  // Authentication tag
    };
}

function decrypt(data: { encrypted: string; iv: string; tag: string }, key: Buffer): string {
    const decipher = crypto.createDecipheriv(
        'aes-256-gcm',
        key,
        Buffer.from(data.iv, 'hex'),
    );
    decipher.setAuthTag(Buffer.from(data.tag, 'hex'));

    let decrypted = decipher.update(data.encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
}

// Usage
const key = crypto.randomBytes(32);  // 256 bits
const result = encrypt('Thông tin mật', key);
const original = decrypt(result, key);  // 'Thông tin mật'
```

---

## 3. Asymmetric Encryption — 2 keys (Public + Private)

**2 chìa khóa khác nhau**: public key (ai cũng có) để encrypt, private key (chỉ bạn) để decrypt. Giải quyết vấn đề chia sẻ key.

```
Bob muốn gửi tin mật cho Alice:
  1. Alice publish public key (ai cũng thấy)
  2. Bob encrypt message bằng Alice's PUBLIC key
  3. Gửi qua internet (Eve thấy ciphertext nhưng KHÔNG decrypt được)
  4. Alice decrypt bằng PRIVATE key (chỉ mình Alice có)
```

```typescript
import crypto from 'crypto';

// Generate key pair
const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
    modulusLength: 2048,
    publicKeyEncoding: { type: 'spki', format: 'pem' },
    privateKeyEncoding: { type: 'pkcs8', format: 'pem' },
});

// Encrypt với public key (bất kỳ ai)
const encrypted = crypto.publicEncrypt(publicKey, Buffer.from('Secret message'));

// Decrypt với private key (chỉ owner)
const decrypted = crypto.privateDecrypt(privateKey, encrypted);
console.log(decrypted.toString());  // 'Secret message'
```

**Thực tế**: Asymmetric chậm hơn symmetric ~1000x → dùng kết hợp:
1. Asymmetric: trao đổi symmetric key an toàn
2. Symmetric (AES): encrypt data thực

Đây chính là cách **TLS/HTTPS** hoạt động!

---

## 4. TLS/HTTPS — Encryption in Transit

```
TLS Handshake (đơn giản hóa):

Client                              Server
  │                                    │
  ├── ClientHello (supported ciphers) ─►│
  │◄── ServerHello + Certificate ──────│
  │                                    │
  │  Verify certificate (trust chain)  │
  │  Generate session key              │
  │  Encrypt key với server's public key│
  ├── Encrypted session key ───────────►│
  │                                    │  Decrypt session key
  │                                    │  với private key
  │◄── Encrypted data (AES) ──────────►│
  │     cùng session key              │
```

---

## 5. Encryption at Rest — Dữ liệu lưu trữ

```
Encrypt TRƯỚC khi lưu DB. Decrypt KHI đọc.

Approaches:
1. Application-level: App encrypt → lưu ciphertext vào DB
   ✅ Control hoàn toàn
   ❌ Phải tự quản lý keys

2. Database-level: PostgreSQL pgcrypto, MongoDB CSFLE
   ✅ Transparent cho app
   ❌ DB admin có thể access

3. Disk-level: AWS EBS encryption, LUKS
   ✅ Dễ setup
   ❌ Không bảo vệ nếu DB bị SQL injection

Ví dụ: PII (Personally Identifiable Information)
  email: "user@example.com"  → Encrypt!
  phone: "0912345678"        → Encrypt!
  password: (hashed, not encrypted)
  name: tuỳ compliance requirement
```

---

## Checklist bảo mật

```
✅ Passwords: bcrypt/Argon2 (NEVER md5/sha256)
✅ Sensitive data: AES-256-GCM encryption at rest
✅ In transit: TLS 1.2+ everywhere (HTTPS)
✅ API keys/secrets: env variables hoặc Vault (NEVER in code!)
✅ Key management: rotate keys định kỳ
✅ IV/Nonce: PHẢI random mỗi lần encrypt (NEVER reuse!)
✅ Timing-safe comparison: crypto.timingSafeEqual (NEVER ===)
```

---

## Bài tập thực hành

- [ ] Implement bcrypt password hashing cho login system
- [ ] AES-256-GCM: encrypt/decrypt sensitive user data
- [ ] Webhook verification: HMAC-SHA256 signature
- [ ] Audit: tìm plaintext secrets trong codebase (git history!)

---

## Tài nguyên thêm

- [Crypto101](https://www.crypto101.io/) — Free book, giải thích rõ ràng
- [OWASP Cryptographic Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [Let's Encrypt](https://letsencrypt.org/) — Free TLS certificates
