# 🎓 HTTP Headers — Content-Type, Auth, Cache, CORS

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~15 phút\
> **Prerequisites:** [00_what-is-http.md](./00_what-is-http.md)

> 🎯 *Headers là **metadata** kèm theo HTTP request/response. Bài này dạy **4 nhóm headers** chính: Content (type/length/encoding), Auth (Bearer/Basic/JWT), Cache (Cache-Control/ETag), **CORS** (giải thích vì sao browser block cross-origin). Sau bài này bạn config CORS không cần Google nữa.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **Content-Type** + parse được `application/json` vs `multipart/form-data` vs `application/x-www-form-urlencoded`
- [ ] Phân biệt **Bearer token** (JWT) vs **Basic auth** vs **API key header**
- [ ] Config **Cache-Control** + **ETag** đúng cho static asset
- [ ] **CORS** — vì sao browser block + cách backend cho phép
- [ ] 10+ custom headers thường gặp (X-Request-ID, X-Forwarded-For, ...)

---

## Tình huống — bạn bị 5 CORS errors trong 1 ngày

Tuần đầu tiên integrate frontend (`localhost:3000`) với backend (`api.example.com`), bạn mở DevTools console và thấy error đỏ chót như đoạn dưới — quen thuộc với mọi frontend dev:

```
Access to fetch at 'https://api.example.com/users' from origin 'http://localhost:3000'
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
on the requested resource.
```

Bạn search Google → mấy chục bài CORS, đa số confused. Sửa backend thêm `Access-Control-Allow-Origin: *` → vẫn lỗi `Access-Control-Allow-Credentials`. Lại thêm header → lỗi `Access-Control-Allow-Methods`. Cứ thế.

→ CORS không tự nhiên hiểu được. Cần **hiểu HEADER là gì + cơ chế CORS** ở mức concept → fix 1 lần xong.

Bài này dạy headers tổng quát + CORS đầy đủ.

---

## 1️⃣ Header là gì?

**Header** = metadata key-value đi kèm HTTP request/response. Format:

```
Key: Value
```

- **Case-insensitive**: `Content-Type` = `content-type` = `CONTENT-TYPE`
- **Multiple values**: separate bằng `,` (vd `Accept: text/html, application/xml`)
- **Custom headers**: prefix `X-` (deprecated convention nhưng vẫn phổ biến)

### 4 nhóm chính

HTTP có ~100 header chính thức (RFC) + hàng nghìn custom. Đừng nhớ hết — chỉ cần nắm **4 nhóm theo mục đích** sau đây thì 90% case daily debug đã đủ:

| Nhóm | Mục đích | Ví dụ headers |
|---|---|---|
| **Content** | Format body | `Content-Type`, `Content-Length`, `Content-Encoding` |
| **Authentication** | Auth identity | `Authorization`, `Cookie`, `WWW-Authenticate` |
| **Cache** | Cache mechanism | `Cache-Control`, `ETag`, `Last-Modified`, `If-None-Match` |
| **CORS** | Cross-origin security | `Access-Control-*`, `Origin` |

🪞 **Ẩn dụ**: headers giống **nhãn dán trên bưu kiện**. Body là **đồ bên trong**. Nhãn ghi: "fragile" (Content-Type), "ship to ID #123" (Authorization), "express delivery" (Cache-Control). Postman không mở box vẫn biết cách handle qua nhãn.

---

## 2️⃣ Content headers — Body format

### Content-Type — Body là gì?

`Content-Type` báo cho receiver biết body **format gì** để parse đúng. Cùng URL nhưng `application/json` vs `text/html` → backend xử lý hoàn toàn khác. 6 dạng MIME phổ biến nhất bạn sẽ gặp daily:

```http
Content-Type: application/json
Content-Type: application/x-www-form-urlencoded
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
Content-Type: text/html; charset=utf-8
Content-Type: image/png
Content-Type: application/octet-stream
```

| MIME Type | Khi nào |
|---|---|
| `application/json` ⭐ | REST API, đa số modern app |
| `application/x-www-form-urlencoded` | HTML form `<form>` default |
| `multipart/form-data` | Upload file qua form |
| `text/html` | HTML page response |
| `text/plain` | Plain text |
| `application/xml` | SOAP, RSS, sitemap |
| `image/png` / `image/jpeg` | Image |
| `application/pdf` | PDF document |
| `application/octet-stream` | Binary unknown (fallback) |

### Ví dụ Content-Type matters

Thiếu hoặc sai `Content-Type` là **nguyên nhân #1** của bug `400 Bad Request` khi test API. So sánh 2 lệnh curl bên dưới — chỉ khác 1 header, kết quả 200 vs 400:

```bash
# Backend expect JSON
curl -X POST /api/users -H "Content-Type: application/json" -d '{"name":"Nguyen Van A"}'
→ 200 OK

# Quên Content-Type → server parse fail
curl -X POST /api/users -d '{"name":"Nguyen Van A"}'
→ 400 Bad Request (nhiều framework default parse là form-urlencoded)
```

→ **Luôn set Content-Type** khi gửi body. Đa số bug "400 với JSON" là quên header này.

### Multipart upload file

Upload file (image, video, document) qua HTML form dùng `multipart/form-data` — format đặc biệt: nhiều "part" tách nhau bằng **boundary** string random. Mỗi part có headers riêng + content riêng. Đây là raw request khi user submit form có file upload:

```http
POST /upload HTTP/1.1
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="title"

My Photo
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="photo.jpg"
Content-Type: image/jpeg

<binary data>
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

→ Upload file → backend dùng library parse multipart (vd `multer` Node, `python-multipart` Python).

### Content-Length, Content-Encoding

```http
Content-Length: 1234              ← Body bao nhiêu bytes
Content-Encoding: gzip            ← Compressed bằng gzip
Content-Language: en-US           ← Ngôn ngữ
```

`gzip` thường save 70-80% bandwidth cho text. Mọi web server modern enable mặc định.

---

## 3️⃣ Authentication headers

### Bearer token (JWT) — Most common 2026

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NSJ9.SflKxwRJ
```

- **Bearer** = "ai cầm token này được xem là chủ"
- Token thường là **JWT** (JSON Web Token) — 3 phần `header.payload.signature` encode base64
- Stateless — server verify signature, không cần lookup DB

```javascript
// Client gửi
fetch('/api/users', {
  headers: {
    'Authorization': 'Bearer ' + token
  }
})

// Server verify (Express + jsonwebtoken)
const token = req.headers.authorization.replace('Bearer ', '');
const decoded = jwt.verify(token, SECRET);
const userId = decoded.sub;
```

### Basic auth — Legacy

```http
Authorization: Basic bG9uZzpwYXNzMTIz
```

- `Basic <base64(username:password)>`
- KHÔNG encrypt — base64 dễ decode. **CHỈ dùng qua HTTPS**.
- Hiện chỉ dùng cho:
  - Internal admin panel đơn giản
  - Quick test API protected
  - Public webhook endpoint (vd Stripe gửi Basic auth confirm họ là Stripe)

### API key header

```http
X-API-Key: sk_test_abc123xyz
# Hoặc:
Authorization: ApiKey sk_test_abc123xyz
```

→ Không chuẩn HTTP, phụ thuộc service. Stripe dùng Bearer, AWS dùng signed request, ...

### Cookie auth — Session-based

```http
Cookie: session_id=abc123; theme=dark
```

- Server set qua `Set-Cookie` response header
- Browser tự đính kèm mỗi request cùng domain
- **Pros**: simple, secure (HttpOnly flag), no JS access
- **Cons**: cross-domain khó (cần CORS + credentials), không scale stateless

### WWW-Authenticate (response challenge)

Server trả 401 kèm:

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="api"
```

→ Báo client "phải gửi Bearer token".

---

## 4️⃣ Cache headers

### Cache-Control — Master cache directive

```http
Cache-Control: max-age=3600                        ← Cache 1 giờ
Cache-Control: no-cache                            ← Validate trước khi dùng cache
Cache-Control: no-store                            ← KHÔNG cache (sensitive data)
Cache-Control: public, max-age=86400, immutable    ← CDN cache 1 ngày, không validate
Cache-Control: private, max-age=600                ← Browser cache only, không CDN
```

| Directive | Tác dụng |
|---|---|
| `max-age=N` | Cache N seconds |
| `no-cache` | Phải validate (ETag) trước khi dùng |
| `no-store` | KHÔNG cache (cho sensitive data) |
| `public` | Bất kỳ cache (browser + CDN) |
| `private` | Chỉ browser cache (không CDN — vì có data user) |
| `immutable` | Resource không bao giờ đổi (static asset có hash trong filename) |
| `stale-while-revalidate=N` | Dùng stale cache trong khi revalidate background |

### ETag + If-None-Match — Validation

```mermaid
sequenceDiagram
    Client->>Server: GET /image.png (first time)
    Server->>Client: 200 OK<br/>ETag: "abc123"<br/>(image bytes)
    Note over Client: Cache image + ETag

    Client->>Server: GET /image.png<br/>If-None-Match: "abc123"
    Note over Server: ETag match → unchanged
    Server->>Client: 304 Not Modified<br/>(no body — dùng cache)
```

→ Save bandwidth: ETag match → 304 → client dùng cache local thay tải lại.

### Last-Modified + If-Modified-Since — Alternative

```http
HTTP/1.1 200 OK
Last-Modified: Wed, 21 Oct 2025 07:28:00 GMT

# Lần sau:
GET /file.png
If-Modified-Since: Wed, 21 Oct 2025 07:28:00 GMT

→ 304 nếu chưa modify từ lúc đó
```

→ ETag chính xác hơn (hash content). Last-Modified phụ thuộc timestamp (file system precision sec, không millisec).

### Best practice cache cho static asset

```http
# HTML (đổi thường)
Cache-Control: no-cache

# CSS/JS có hash trong filename (vd app.a3b7c.css)
Cache-Control: public, max-age=31536000, immutable

# Image
Cache-Control: public, max-age=86400

# API JSON (user data)
Cache-Control: private, max-age=60
```

---

## 5️⃣ CORS — Cross-Origin Resource Sharing

### Vì sao có CORS?

**Same-Origin Policy** (SOP) — browser **block** JavaScript từ origin A gọi resource từ origin B (cross-origin) **vì security**:

- Tránh `evil.com` script gọi `bank.com/transfer` với cookie của user
- Cookie + auth tự đính kèm mỗi cross-origin call → nguy hiểm nếu unprotected

**Origin** = `<protocol>://<host>:<port>`. Khác 1 trong 3 = cross-origin:

```
http://localhost:3000   vs  http://localhost:5000   → CROSS (port khác)
http://example.com      vs  https://example.com    → CROSS (protocol khác)
http://example.com      vs  http://api.example.com → CROSS (host khác)
```

### Vấn đề + Giải pháp

Browser block. Nhưng **modern web** cần FE gọi API khác domain. Giải pháp: **CORS** — backend explicit cho phép qua headers.

### Simple request

Browser tự gửi (không preflight) nếu request:
- Method là `GET`, `POST`, `HEAD`
- Không có custom header (chỉ vài header "safe": `Accept`, `Content-Type=form-urlencoded|text|multipart`)

Backend trả thêm:

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: http://localhost:3000
(hoặc *)
```

→ Browser cho JS đọc response. Nếu thiếu header này → block.

### Preflight request

Request không-simple (PUT/DELETE/PATCH, custom header, Content-Type JSON) → browser **tự** gửi OPTIONS trước **preflight**:

```mermaid
sequenceDiagram
    Note over Browser: JS gọi: fetch('https://api.example.com', {method:'DELETE'})
    Browser->>API: OPTIONS /resource<br/>Origin: http://localhost:3000<br/>Access-Control-Request-Method: DELETE
    API->>Browser: 204 No Content<br/>Access-Control-Allow-Origin: http://localhost:3000<br/>Access-Control-Allow-Methods: GET, POST, DELETE<br/>Access-Control-Allow-Headers: Authorization
    Note over Browser: Preflight OK → gửi actual request
    Browser->>API: DELETE /resource<br/>Authorization: Bearer ...
    API->>Browser: 200 OK<br/>Access-Control-Allow-Origin: http://localhost:3000
```

→ 2 round-trips. Browser cache preflight (`Access-Control-Max-Age: 86400`) để đỡ overhead.

### Server cần trả gì?

```http
# Cho phép origin cụ thể (recommend)
Access-Control-Allow-Origin: http://localhost:3000

# Hoặc cho phép mọi origin (DANGEROUS nếu API có cookie/auth)
Access-Control-Allow-Origin: *

# Cho phép cookie/credential cross-origin (cần origin specific, KHÔNG * được)
Access-Control-Allow-Credentials: true
Access-Control-Allow-Origin: http://localhost:3000

# Cho phép methods (preflight)
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH

# Cho phép headers (preflight)
Access-Control-Allow-Headers: Content-Type, Authorization, X-Custom-Header

# Cache preflight response
Access-Control-Max-Age: 86400
```

### Setup CORS — Code

**Express (Node.js)**:

```javascript
const cors = require('cors');
app.use(cors({
  origin: ['http://localhost:3000', 'https://myapp.com'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

**FastAPI (Python)**:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Nginx (proxy layer)**:

```nginx
add_header 'Access-Control-Allow-Origin' 'http://localhost:3000' always;
add_header 'Access-Control-Allow-Credentials' 'true' always;
```

### Common CORS pitfalls

| Pitfall | Cách fix |
|---|---|
| `Allow-Origin: *` + `Allow-Credentials: true` | KHÔNG được combine. Phải dùng origin specific với credentials. |
| Backend không handle OPTIONS preflight | Middleware CORS phải catch OPTIONS, trả 200/204 với headers. |
| Trả CORS header nhưng status 500 | Browser vẫn block. Phải success 2xx HOẶC ít nhất gửi đúng headers ở error. |
| Cookie không gửi cross-origin | Client phải set `credentials: 'include'` trong fetch. Server phải `Allow-Credentials: true`. |

---

## 6️⃣ Custom headers (X-...)

| Header | Mục đích |
|---|---|
| `X-Request-ID` | Trace ID cho 1 request qua nhiều service (microservices) |
| `X-Forwarded-For` | Real IP client (khi qua proxy/CDN) |
| `X-Forwarded-Proto` | HTTP hoặc HTTPS original |
| `X-Real-IP` | Real IP (Nginx convention) |
| `X-RateLimit-Limit` | Tổng request cho phép |
| `X-RateLimit-Remaining` | Còn lại |
| `X-RateLimit-Reset` | Khi reset (Unix timestamp) |
| `X-Frame-Options` | Anti-clickjacking (`DENY` / `SAMEORIGIN`) |
| `X-Content-Type-Options: nosniff` | Disable MIME sniffing |
| `X-Request-Method` | Override method (tunneling khi proxy chặn DELETE) |

> 💡 **`X-` prefix deprecated** từ RFC 6648 (2012). Nhưng đa số dev vẫn dùng vì convention. Modern API: dùng custom name không prefix (vd `Request-ID`).

### Security headers (response)

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains   ← Force HTTPS
Content-Security-Policy: default-src 'self'                      ← Anti-XSS
X-Frame-Options: DENY                                            ← Anti-clickjacking
X-Content-Type-Options: nosniff                                  ← Anti MIME sniff
Referrer-Policy: no-referrer-when-downgrade
Permissions-Policy: geolocation=(), camera=()
```

→ Modern web app phải gửi đủ. Tool kiểm tra: [securityheaders.com](https://securityheaders.com).

---

## 💡 Pitfall thường gặp

### ❌ Pitfall: Quên `Content-Type: application/json`

```bash
curl -X POST /api/users -d '{"name":"bạn"}'
→ 400 (server parse JSON fail vì Content-Type default form-urlencoded)
```

**Fix**: luôn set khi gửi JSON.

### ❌ Pitfall: CORS `*` + `credentials: true`

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
→ Browser BLOCK (combo invalid theo spec)
```

**Fix**: dùng origin cụ thể với credentials.

### ❌ Pitfall: Cache static asset không có hash filename

```html
<link rel="stylesheet" href="/app.css">       ← KHÔNG hash
```

→ Update `app.css` → user vẫn dùng cache cũ 1 năm (`max-age=31536000`).

**Fix**: dùng filename có hash từ build tool:

```html
<link rel="stylesheet" href="/app.a3b7c2.css">  ← Đổi name = browser load mới
```

### ❌ Pitfall: Lưu JWT trong localStorage

```javascript
localStorage.setItem('token', jwt);    // ❌ XSS attack đọc được
```

**Fix**: dùng cookie `HttpOnly + Secure + SameSite=Strict`:

```http
Set-Cookie: token=...; HttpOnly; Secure; SameSite=Strict
```

→ JS không read được (HttpOnly), chỉ HTTPS (Secure), không cross-site (SameSite).

### ❌ Pitfall: Trust `X-Forwarded-For` blindly

Client có thể fake header này. Backend trust → log IP sai → bị bypass IP-based rate limit.

**Fix**: chỉ trust `X-Forwarded-For` từ **trusted proxy** (Nginx/Cloudflare). Set whitelist IP của proxy.

### ✅ Best practice: Header naming consistent

```
✓ X-Request-ID (UPPERCASE-DASH)
✗ x-request-id (lowercase OK nhưng inconsistent)
✗ x_request_id (underscore — Nginx có thể block!)
```

→ Nginx default drop underscore headers (`underscores_in_headers off` mặc định).

---

## 🧠 Self-check

**Q1.** `Content-Type` vs `Accept` khác nhau?

<details>
<summary>💡 Đáp án</summary>

- **`Content-Type`** (trên request) = "body tôi GỬI có format gì". VD: `application/json` → server parse JSON.
- **`Accept`** (trên request) = "tôi MUỐN response format gì". VD: `Accept: application/xml` → server (nếu support) trả XML thay JSON.

Cả 2 đều có thể có trên request:

```http
POST /users HTTP/1.1
Content-Type: application/json        ← body tôi gửi là JSON
Accept: application/json              ← muốn nhận JSON response

{"name": "bạn"}
```

Response có `Content-Type` riêng:

```http
HTTP/1.1 201 Created
Content-Type: application/json        ← response body là JSON
```

</details>

**Q2.** CORS — vì sao có? Backend cần làm gì?

<details>
<summary>💡 Đáp án</summary>

**Vì sao có**: browser **Same-Origin Policy** block JS từ origin A gọi origin B (security — tránh evil site dùng cookie user gọi bank site).

**Modern web cần cross-origin** (FE `localhost:3000` gọi API `api.example.com`). CORS = mechanism backend **explicit cho phép** qua headers.

**Backend cần gửi headers**:

```http
Access-Control-Allow-Origin: http://localhost:3000     ← cho phép FE origin này
Access-Control-Allow-Credentials: true                 ← cho gửi cookie (KHÔNG dùng với *)
Access-Control-Allow-Methods: GET, POST, PUT, DELETE   ← cho preflight
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400                          ← cache preflight 1 ngày
```

**Và handle preflight OPTIONS** trước actual request (PUT/DELETE hoặc Content-Type JSON).

→ Frameworks (Express/FastAPI/Spring) có middleware CORS plug-and-play.

</details>

**Q3.** Vì sao KHÔNG lưu JWT trong `localStorage`?

<details>
<summary>💡 Đáp án</summary>

**Lý do**: localStorage **đọc được bằng JS**. Nếu site bị **XSS** (vd 1 dependency npm bị compromise inject script), script đọc được token → impersonate user.

**Alternative an toàn**: **HttpOnly Cookie**

```http
Set-Cookie: token=...; HttpOnly; Secure; SameSite=Strict
```

- **HttpOnly** = JS KHÔNG read được (chỉ browser auto-attach mỗi request)
- **Secure** = chỉ gửi qua HTTPS
- **SameSite=Strict** = không gửi cross-site → chặn CSRF

**Trade-off**: cookie cần handle CSRF (vì auto-attach). LocalStorage cần handle XSS. Pick poison.

**Best of both**: cookie HttpOnly + CSRF token trong header.

</details>

---

## ⚡ Cheatsheet

### Common request headers

```http
Host: example.com
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
User-Agent: Mozilla/5.0 ...
Cookie: session=abc123
Origin: http://localhost:3000
```

### Common response headers

```http
Content-Type: application/json
Content-Length: 1234
Cache-Control: max-age=3600
ETag: "abc123"
Set-Cookie: session=...; HttpOnly; Secure
Access-Control-Allow-Origin: ...
```

### CORS quick setup (Express)

```javascript
app.use(cors({
  origin: ['http://localhost:3000'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Header | (giữ EN) | Key-value metadata trong request/response |
| MIME Type | (giữ EN) | Format identifier (`application/json`, `image/png`) |
| Bearer | (giữ EN) | "Người cầm" — auth scheme dùng token |
| JWT | (giữ EN) | JSON Web Token (header.payload.signature) |
| Origin | (giữ EN) | `protocol://host:port` |
| CORS | (giữ EN) | Cross-Origin Resource Sharing |
| Same-Origin Policy | (giữ EN) | Browser security block cross-origin |
| Preflight | (giữ EN) | OPTIONS request browser gửi trước actual request |
| ETag | (giữ EN) | Hash content cho cache validation |
| HttpOnly | (giữ EN) | Cookie flag không cho JS đọc |

---

## 🔗 Liên kết & Tài nguyên

### Trong kho

| Hướng | Bài |
|---|---|
| ⬅️ Bài trước | [02_http-status-codes.md](./02_http-status-codes.md) |
| ➡️ Bài tiếp | [04_https-tls.md](./04_https-tls.md) (chưa có) — HTTPS + TLS |

### Tài nguyên ngoài

- [MDN HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) — chính thức
- [MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) — đầy đủ về CORS
- [JWT.io](https://jwt.io/) — debug JWT token
- [securityheaders.com](https://securityheaders.com) — scan security headers
- [Mozilla Observatory](https://observatory.mozilla.org/) — security audit site

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6 (Header→Code anti-pattern fix): thêm lead-in 2-3 câu trước Tình huống CORS error block, §1 bảng "4 nhóm chính", §2 Content-Type MIME list + "Content-Type matters" example + Multipart upload block. Fix placeholder `"name":"bạn"` → `"name":"Nguyen Van A"` (Blueprint v0.5.7 §3.5). Nội dung kỹ thuật giữ nguyên.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `http-https/` lesson 4/6. Cover: tình huống bạn 5 CORS errors → §1 Header concept + 4 nhóm → §2 Content (Content-Type 9 MIME + multipart upload) → §3 Auth (Bearer/Basic/API key/Cookie) → §4 Cache (Cache-Control directives + ETag mermaid + static asset best practice) → §5 **CORS** (SOP, simple vs preflight với mermaid, server config code 3 framework, 4 pitfalls) → §6 Custom headers + security headers. 5 pitfall + 3 self-check.
