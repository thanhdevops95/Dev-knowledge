# TLS / SSL Deep Dive

> **Tags:** `tls` `ssl` `https` `certificates` `encryption` `security`
> **Level:** Intermediate | **Prerequisite:** `networking/03-osi-tcp-ip.md`

---

## 1. TLS là gì?

**TLS** (Transport Layer Security) = giao thức mã hóa layer 4-5, kế thừa SSL (đã deprecated).

```
HTTP  = plain text  → ANYONE can read traffic
HTTPS = HTTP + TLS  → encrypted, authenticated

TLS cung cấp:
  ✅ Confidentiality  — mã hóa data (không ai đọc được)
  ✅ Integrity        — phát hiện data bị tamper (HMAC)
  ✅ Authentication   — xác thực server (certificates)
  Optional: mutual auth (mTLS) — xác thực cả client
```

---

## 2. TLS 1.3 Handshake (Simplified)

TLS 1.3 giảm từ 2 round-trips (TLS 1.2) xuống **1 round-trip**:

```
Client                              Server
  │── ClientHello ─────────────────▶│
  │   (TLS version, cipher suites,  │
  │    random, key_share: pub_key)   │
  │                                  │
  │◀─ ServerHello ──────────────────│
  │   (chosen cipher, key_share,    │
  │    Certificate, CertVerify,     │
  │    Finished)                    │
  │                                  │
  │── Finished ────────────────────▶│
  │── [Application Data] ──────────▶│   (Encrypted from here!)
  │◀─ [Application Data] ───────────│
```

### Key Exchange — ECDHE
- Client và Server đều generate **ephemeral** (tạm thời) key pairs
- Dùng **ECDH** (Elliptic Curve Diffie-Hellman) để derive **shared secret**
- Shared secret → dẫn xuất nhiều keys (handshake keys, application keys)
- **Perfect Forward Secrecy**: ephemeral keys không bao giờ lưu → compromise server's private key không decrypt được past sessions

```
ECDH Key Exchange:
  Client private: a    Client public: A = a*G
  Server private: b    Server public: B = b*G
  
  Client computes:  S = a * B = a * b * G
  Server computes:  S = b * A = b * a * G = a * b * G
  
  Same S! Without exchanging private keys!
```

---

## 3. TLS 1.2 vs TLS 1.3

| | TLS 1.2 | TLS 1.3 |
|---|---|---|
| Handshake RTT | 2 | **1** |
| 0-RTT (session resumption) | No | Yes (với risks) |
| Cipher negotiation | Client sends ALL supported | Optimistic key share |
| Forward Secrecy | Optional | **Mandatory** |
| RSA key exchange | Allowed | **Removed** |
| Weak ciphers | RC4, 3DES allowed | **Removed** |
| Handshake encryption | None | **Encrypted** |

---

## 4. Certificate Chain

```
Root CA (DigiCert, Let's Encrypt, etc.)
  └── Intermediate CA
        └── Leaf Certificate (your domain)
```

### Tại sao có Intermediate CA?
- Root CA phải được offline và cực kỳ bảo mật
- Intermediate CA có thể bị revoke mà không ảnh hưởng root
- Depth: thường 2-3 levels

### Certificate fields quan trọng
```
Subject:   CN=example.com, O=Acme Corp, C=US
Issuer:    CN=Let's Encrypt R3
Valid:     2024-01-01 to 2024-04-01  (Let's Encrypt: 90 days)
SANs:      example.com, www.example.com, api.example.com
Key:       EC 256-bit (P-256) or RSA 2048-bit
Signature: SHA256withRSA
```

### SAN (Subject Alternative Names)
- Modern TLS dùng **SAN** thay vì CN cho hostname matching
- 1 cert có thể cover nhiều domains:
```
SANs: example.com, www.example.com, api.example.com, *.example.com
```

### Wildcard Certificate
- `*.example.com` covers: `www.example.com`, `api.example.com`
- **KHÔNG** cover: `example.com` (cần add riêng), `sub.api.example.com` (chỉ 1 level)

---

## 5. Certificate Verification Process

Khi browser nhận certificate từ server:

```
1. Chain validation:
   Leaf cert signed by Intermediate CA?    ✅
   Intermediate cert signed by Root CA?     ✅
   Root CA trong browser's trust store?     ✅

2. Validity check:
   Current time inside notBefore/notAfter?  ✅

3. Hostname verification:
   Server hostname matches cert SAN/CN?     ✅

4. Revocation check (optional, browser dependent):
   OCSP (Online Certificate Status Protocol) — query CA
   CRL (Certificate Revocation List) — download list
   OCSP Stapling — server includes signed OCSP response

5. Key usage:
   Cert marked for TLS server auth?         ✅
```

---

## 6. Let's Encrypt & ACME Protocol

Let's Encrypt = free, automated CA. ACME = protocol để tự động issue/renew certs.

### Ownership Verification

**HTTP-01 Challenge**:
```bash
# ACME server: "Prove you control example.com"
# Place file at:
# http://example.com/.well-known/acme-challenge/TOKEN
# với content = TOKEN.KEY_AUTHORIZATION

# certbot tự động làm điều này:
certbot --nginx -d example.com -d www.example.com
certbot renew    # Tự động renew
```

**DNS-01 Challenge** (cho wildcard certs):
```bash
# ACME server yêu cầu thêm TXT record:
# _acme-challenge.example.com → "TOKEN_VALUE"

certbot certonly --manual --preferred-challenges=dns -d "*.example.com"
# Hoặc dùng DNS provider plugin (Cloudflare, Route53):
certbot certonly --dns-cloudflare -d "*.example.com"
```

### Auto-renewal
```bash
# Crontab
0 12 * * * /usr/bin/certbot renew --quiet

# Systemd timer (modern)
systemctl enable certbot.timer
systemctl start certbot.timer

# Kiểm tra renewal
certbot renew --dry-run
```

---

## 7. mTLS — Mutual TLS

Trong TLS thông thường, chỉ CLIENT xác thực SERVER. mTLS = **cả hai bên xác thực nhau**:

```
Client ─── ClientHello ──▶ Server
Client ◀── ServerHello ─── Server
Client ◀── Certificate ─── Server    (server cert)
Client ──▶ Certificate ──▶ Server    (client cert)  ← mTLS thêm bước này
Client  ─── Finished ──────▶ Server
```

### Use cases
- **Service-to-service auth** trong microservices (Istio/Linkerd tự động mTLS)
- **API authentication** thay vì API keys
- **Zero trust networking**

```python
# Python server với mTLS
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('server.crt', 'server.key')
context.load_verify_locations('client-ca.crt')
context.verify_mode = ssl.CERT_REQUIRED  # Require client cert!

# Python client với mTLS
import requests

response = requests.get(
    'https://api.example.com',
    cert=('client.crt', 'client.key'),  # Client certificate
    verify='server-ca.crt'              # Server CA to verify against
)
```

---

## 8. Self-Signed Certificates

Cho development/internal use:

```bash
# Generate CA key + cert
openssl genrsa -out ca.key 4096
openssl req -x509 -new -nodes -key ca.key -sha256 -days 1825 \
  -out ca.crt \
  -subj "/C=US/ST=CA/O=MyOrg CA/CN=MyOrg Root CA"

# Generate server key + CSR
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr \
  -subj "/C=US/ST=CA/O=MyOrg/CN=localhost"

# Sign CSR with CA (create cert)
cat > server.ext << EOF
subjectAltName = DNS:localhost, DNS:*.localhost, IP:127.0.0.1
EOF

openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out server.crt -days 825 -sha256 \
  -extfile server.ext

# Verify
openssl verify -CAfile ca.crt server.crt
openssl x509 -in server.crt -text -noout
```

### Dùng mkcert (đơn giản hơn cho dev)
```bash
brew install mkcert
mkcert -install             # Thêm CA vào system trust store
mkcert localhost 127.0.0.1  # Tạo cert cho localhost
# Tạo: localhost+1.pem và localhost+1-key.pem
```

---

## 9. Certificate Pinning

**Cert pinning** = hardcode cert/public key fingerprint trong app. Chống MITM ngay cả khi attacker có CA cert.

```python
import hashlib, ssl, socket

# Lấy cert fingerprint của server
def get_cert_fingerprint(hostname, port=443):
    ctx = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert_der = ssock.getpeercert(binary_form=True)
            return hashlib.sha256(cert_der).hexdigest()

# Pin: hardcode expected fingerprint
EXPECTED_FP = "abc123..."

actual_fp = get_cert_fingerprint("api.example.com")
if actual_fp != EXPECTED_FP:
    raise SecurityError("Certificate doesn't match pinned value!")
```

**Nhược điểm pinning**: khi cert renew → phải update app → deploy.
**Giải pháp**: pin **public key** (thay đổi ít hơn cert) hoặc dùng **backup pins**.

---

## 10. OCSP Stapling

Thay vì client phải query OCSP responder (slow, privacy issue), server "staples" OCSP response vào TLS handshake:

```nginx
# Nginx config
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /path/to/chain.crt;
resolver 8.8.8.8 8.8.4.4 valid=300s;

# Kiểm tra
openssl s_client -connect example.com:443 -status 2>/dev/null | grep -A 10 "OCSP Response"
```

---

## 11. Debug TLS Issues

```bash
# Xem cert của server
openssl s_client -connect example.com:443 -servername example.com

# Xem chi tiết cert
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -text

# Check expiry
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# Test specific TLS version
openssl s_client -connect example.com:443 -tls1_2
openssl s_client -connect example.com:443 -tls1_3

# Test with curl
curl -v --tlsv1.3 https://example.com     # Force TLS 1.3
curl -v --insecure https://example.com    # Skip verification (testing only!)
curl --cacert custom-ca.crt https://internal.example.com

# SSL Labs: Test your server
# https://www.ssllabs.com/ssltest/analyze.html?d=example.com
```

---

## 12. Common TLS Errors

| Error | Cause | Fix |
|---|---|---|
| `certificate has expired` | Cert past notAfter | Renew cert |
| `certificate is not trusted` | Self-signed or unknown CA | Add CA to trust store |
| `hostname mismatch` | CN/SAN doesn't match domain | Fix cert or use correct hostname |
| `CERTIFICATE_VERIFY_FAILED` | Chain broken or wrong CA | Check full chain |
| `ssl.SSLError: [SSL: WRONG_VERSION_NUMBER]` | Non-TLS server | Wrong port or HTTP on HTTPS port |
| `SSLV3_ALERT_HANDSHAKE_FAILURE` | No common cipher | Update client/server TLS version |

---

*Tài liệu liên quan: `encryption/01-encryption-basics.md` | `encryption/03-pki-certificates.md` | `networking/03-osi-tcp-ip.md`*
