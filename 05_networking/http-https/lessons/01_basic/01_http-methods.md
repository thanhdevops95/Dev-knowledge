# 🎓 HTTP Methods — GET / POST / PUT / PATCH / DELETE

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [00_what-is-http.md](./00_what-is-http.md)

> 🎯 *Tiếp bài intro HTTP: deep dive **5 methods** chính (GET/POST/PUT/PATCH/DELETE) + **idempotent** vs **safe** + khi nào dùng cái nào. Sau bài này bạn design REST API endpoint chuẩn convention + biết PUT vs PATCH khác nhau ra sao.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu 5 methods chính + use case mỗi cái
- [ ] Phân biệt **PUT** vs **PATCH** — câu hỏi interview kinh điển
- [ ] Hiểu **idempotent** vs **safe** + bảng so sánh 9 method
- [ ] Biết khi nào dùng **HEAD**, **OPTIONS**, **CONNECT**, **TRACE**
- [ ] Design REST endpoint chuẩn convention

---

## Tình huống — bạn design API endpoint đầu tiên

Bạn build CRUD API cho `users`. Cần endpoints:

- Lấy danh sách users → method gì?
- Lấy 1 user theo ID → method gì?
- Tạo user mới → method gì?
- Cập nhật email user → **PUT** hay **PATCH**?
- Xoá user → method gì?

Bạn gõ:
```
POST /getUsers
POST /getUserById
POST /createUser
POST /updateUser
POST /deleteUser
```

Sếp review: *"Sai convention. Đọc lại HTTP methods."*

→ Bạn ngơ. POST `/getUsers` chạy được mà. Sao "sai"?

**Lý do**: HTTP có **5 methods chính** với **semantics rõ ràng**. Dùng `POST /getUsers` là **technically OK** nhưng **anti-pattern** — vi phạm REST convention, làm cache/proxy hiểu sai, tool monitor không track đúng.

Bài này dạy bạn design API endpoint đúng convention từ đầu.

---

## 1️⃣ 5 methods chính — Tổng quan

HTTP định nghĩa nhiều method nhưng **5 cái dưới đây chiếm 99% case thực tế**. Mỗi method có 3 thuộc tính quan trọng — *có body không* (gửi data kèm request hay không), *idempotent* (lặp lại an toàn không), và *safe* (đổi state server không). Bảng dưới tóm tắt — phần kế tiếp giải thích chi tiết từng method:

| Method | Mục đích | Có body? | Idempotent? | Safe? |
|---|---|---|---|---|
| **GET** | Đọc resource | ❌ | ✅ | ✅ |
| **POST** | Tạo mới | ✅ | ❌ | ❌ |
| **PUT** | Update toàn bộ | ✅ | ✅ | ❌ |
| **PATCH** | Update 1 phần | ✅ | ❌ (tùy implement) | ❌ |
| **DELETE** | Xoá | Tuỳ | ✅ | ❌ |

### Giải thích "Idempotent" + "Safe"

🪞 **Idempotent** = "**làm 1 lần hay 100 lần kết quả giống nhau**". GET, PUT, DELETE → idempotent. POST, PATCH → KHÔNG.

🪞 **Safe** = "**không đổi state server**". Chỉ GET là safe (read-only). POST/PUT/PATCH/DELETE đều đổi state.

**Vì sao quan trọng?**

- **Proxy/CDN** cache GET (safe + idempotent) — request lại lấy từ cache, không hit backend
- **Browser retry** automatic GET/PUT khi network fail — vì idempotent
- **Browser KHÔNG retry POST** — vì POST không idempotent (có thể tạo dup record)

---

## 2️⃣ GET — Đọc resource

**Mục đích**: lấy data từ server. **KHÔNG đổi state** server.

### Convention URL

GET dùng URL để **chỉ định resource muốn đọc**. Convention REST đặt resource ở **path**, filter/sort/pagination ở **query string**:

```
GET /users            ← list all users
GET /users/123        ← get user by id 123
GET /users?role=admin ← list + filter qua query string
GET /users/123/posts  ← nested resource: posts của user 123
```

### Đặc trưng

GET có 5 đặc trưng quan trọng — nắm được sẽ giải thích được *vì sao GET cache được mà POST không*:

- **Không có body** (HTTP spec cho phép nhưng nhiều proxy ignore)
- **Filter qua query string** `?key=value&...`
- **Cache mạnh** — browser + CDN + proxy đều cache GET response (nếu headers cho phép)
- **Idempotent** — gọi 100 lần kết quả same (assume DB không thay đổi)
- **Safe** — read-only

### Ví dụ

4 dạng GET phổ biến qua `curl` — list, get-by-id, filter, sort. Mọi backend (FastAPI, Express, Rails, ...) đều handle 4 pattern này:

```bash
# 1. List users
curl https://api.example.com/users

# 2. Get user 123
curl https://api.example.com/users/123

# 3. Filter + pagination
curl "https://api.example.com/users?role=admin&page=2&limit=20"

# 4. Sort
curl "https://api.example.com/users?sort=created_at&order=desc"
```

### Response

Server trả về **status 200** + body JSON + headers cho phép cache. Đây là response chuẩn cho `GET /users`:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=60

[
  {"id": 1, "name": "Nguyen Van A"},
  {"id": 2, "name": "Le Van B"}
]
```

> 💡 **Anti-pattern**: `POST /getUsers`. Đúng: `GET /users`. Vì sao? Vì POST không cache được, không idempotent, làm proxy/monitor hiểu sai semantic.

---

## 3️⃣ POST — Tạo mới

**Mục đích**: tạo resource mới hoặc trigger action (vd send email, deploy, ...).

### Convention URL

```
POST /users              ← tạo user mới (body chứa data)
POST /users/123/posts    ← tạo post của user 123
POST /login              ← action: login (không phải tạo resource)
POST /deploy             ← action: deploy
```

### Đặc trưng

- **Có body** — chứa data tạo resource (JSON, form-data, ...)
- **KHÔNG idempotent** — gọi 2 lần tạo 2 record
- **KHÔNG safe** — đổi state
- **KHÔNG cache** mặc định
- **Browser KHÔNG retry** tự động khi network fail

### Ví dụ

```bash
# Tạo user mới
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nguyen Van A",
    "email": "nguyenvana@example.com",
    "role": "admin"
  }'
```

### Response

```http
HTTP/1.1 201 Created                        ← Note: 201, không phải 200
Content-Type: application/json
Location: /users/124                        ← Path resource mới tạo

{
  "id": 124,
  "name": "Nguyen Van A",
  "email": "nguyenvana@example.com",
  "role": "admin",
  "created_at": "2026-05-23T10:30:00Z"
}
```

### Idempotency keys — Hack để safe POST retry

POST không idempotent → retry có thể tạo dup. **Solution**: client gửi `Idempotency-Key` header với UUID unique:

```bash
curl -X POST https://api.stripe.com/v1/charges \
  -H "Idempotency-Key: 5a47e08f-1234-..." \
  -d '...'
```

Server cache response theo key 24h. Cùng key + same body → trả response cũ, không tạo charge mới.

→ Pattern phổ biến cho **payment API** (Stripe, PayPal). Không phải mọi API support.

---

## 4️⃣ PUT — Update toàn bộ

**Mục đích**: thay thế **TOÀN BỘ** resource bằng data trong body.

### Convention URL

```
PUT /users/123    ← thay user 123 hoàn toàn
```

### Đặc trưng

- **Có body** chứa **toàn bộ** representation mới
- **Idempotent** — gọi 100 lần kết quả same
- **KHÔNG safe** — đổi state
- **Field không gửi** = bị **reset về null/default**

### Ví dụ

```bash
# Update toàn bộ user 123
curl -X PUT https://api.example.com/users/123 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nguyen Van A (updated)",
    "email": "nguyenvana@example.com",
    "role": "admin",
    "age": 28
  }'
```

→ Sau call này, user 123 chỉ còn 4 fields trên. Nếu trước đó có `phone` mà không gửi trong body → `phone` bị **xoá** (set null hoặc default).

### Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 123,
  "name": "Nguyen Van A (updated)",
  "email": "nguyenvana@example.com",
  "role": "admin",
  "age": 28
}
```

---

## 5️⃣ PATCH — Update 1 phần

**Mục đích**: update **chỉ 1 hoặc vài fields**, giữ nguyên còn lại.

### Convention URL

```
PATCH /users/123    ← update chỉ field gửi
```

### Đặc trưng

- **Có body** chứa **chỉ fields cần đổi**
- **KHÔNG idempotent** strict (tuỳ implement — vd `PATCH /counter +1` không idempotent)
- **KHÔNG safe**
- **Field không gửi** = giữ nguyên

### Ví dụ

```bash
# Chỉ update email, các field khác giữ nguyên
curl -X PATCH https://api.example.com/users/123 \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com"
  }'
```

### Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 123,
  "name": "Nguyen Van A",                  ← giữ nguyên
  "email": "newemail@example.com", ← updated
  "role": "admin",                 ← giữ nguyên
  "age": 28                        ← giữ nguyên
}
```

### PUT vs PATCH — Bảng so sánh

| | **PUT** | **PATCH** |
|---|---|---|
| Mục đích | Replace toàn bộ | Update 1 phần |
| Body | TOÀN BỘ fields | CHỈ fields cần đổi |
| Field thiếu trong body | Reset null/default | Giữ nguyên |
| Idempotent | ✅ | Tuỳ (`+1` thì không) |
| Real-world dùng nhiều | Ít hơn | **Phổ biến hơn** |

→ **Trong thực tế**, PATCH dùng **nhiều hơn PUT** vì client thường chỉ đổi vài field.

> 💡 Anti-pattern: dùng PUT mà chỉ gửi 1 field → resource bị reset các field khác. Phải PATCH.

---

## 6️⃣ DELETE — Xoá resource

**Mục đích**: xoá resource.

### Convention URL

```
DELETE /users/123    ← xoá user 123
DELETE /users        ← xoá tất cả users (hiếm + nguy hiểm)
```

### Đặc trưng

- **Body tuỳ chọn** — đa số không có
- **Idempotent** — xoá 1 record đã xoá vẫn OK (trả 204 No Content)
- **KHÔNG safe**

### Ví dụ

```bash
curl -X DELETE https://api.example.com/users/123
```

### Response

```http
HTTP/1.1 204 No Content       ← 204: success, không body
```

Hoặc:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"message": "User 123 deleted", "deleted_at": "2026-05-23T..."}
```

### Soft delete vs Hard delete

| | Hard delete | Soft delete |
|---|---|---|
| DB action | `DELETE FROM users WHERE id=123` | `UPDATE users SET deleted_at=NOW() WHERE id=123` |
| Data mất? | ✅ Mất vĩnh viễn | ❌ Vẫn còn |
| Restore? | ❌ (trừ khi backup) | ✅ |
| Compliance (GDPR) | ⭐ Tốt cho "right to be forgotten" | Cần handle riêng |
| Recommend | Khi data thực sự không cần | **Mặc định** cho user-facing data |

→ Đa số production app dùng **soft delete** + cron job hard delete sau N ngày.

---

## 7️⃣ Methods khác — HEAD, OPTIONS, CONNECT, TRACE

### HEAD — GET nhưng chỉ headers

```bash
curl -I https://example.com
# HTTP/1.1 200 OK
# Content-Type: text/html
# Content-Length: 1234
# (KHÔNG body)
```

**Use case**:
- Check file exist mà không tải về
- Lấy `Content-Length` trước khi quyết tải
- Health check (rẻ hơn GET)

### OPTIONS — Xem methods supported + CORS preflight

```bash
curl -X OPTIONS https://api.example.com/users -v
# < Access-Control-Allow-Methods: GET, POST, PUT, DELETE
# < Access-Control-Allow-Origin: *
```

**Use case chính**: **CORS preflight** — browser tự gửi OPTIONS trước cross-origin request không simple (PUT/DELETE/custom headers) để check server có cho phép không.

→ Chi tiết CORS → [03_http-headers.md](./03_http-headers.md) §5 CORS.

### CONNECT — Tunnel qua proxy

Dùng cho **HTTPS qua HTTP proxy**. Client gửi `CONNECT api.example.com:443` → proxy mở TCP tunnel → traffic HTTPS chạy qua.

→ Đa số dev không tự dùng CONNECT — browser/curl tự xử lý khi config proxy.

### TRACE — Debug

Echo lại request server nhận. Hiếm dùng, **đa số production disable** vì security risk (XSS via TRACE).

---

## 8️⃣ REST endpoint design — Convention chuẩn

Áp dụng 5 methods để design endpoint:

| Action | Method + URL | Status response thường |
|---|---|---|
| List users | `GET /users` | 200 OK |
| List với filter | `GET /users?role=admin` | 200 OK |
| Get 1 user | `GET /users/:id` | 200 OK / 404 Not Found |
| Create user | `POST /users` | 201 Created |
| Replace user | `PUT /users/:id` | 200 OK / 204 No Content |
| Update user | `PATCH /users/:id` | 200 OK |
| Delete user | `DELETE /users/:id` | 204 No Content |
| List user's posts | `GET /users/:id/posts` | 200 OK |
| Create user's post | `POST /users/:id/posts` | 201 Created |

### Quy tắc URL design

1. **Plural noun** cho collection: `/users` không `/user`
2. **ID trong path**: `/users/123` không `/users?id=123`
3. **Filter qua query**: `/users?role=admin&page=2`
4. **Action qua method**: `GET` để đọc, không `POST /getUsers`
5. **Nested cho relationship**: `/users/:id/posts` (1-N)
6. **kebab-case** trong URL: `/user-profiles` không `/userProfiles` hay `/user_profiles`

### Anti-pattern phổ biến

```
❌ POST /getUsers       → ✓ GET /users
❌ GET /deleteUser/123  → ✓ DELETE /users/123
❌ POST /users/update   → ✓ PATCH /users/:id
❌ POST /api?action=create  → ✓ POST /users
```

→ Câu hỏi: *"Em viết được API hoạt động đấy"*. Đáp: **OK chạy thôi** chưa đủ — phải đúng convention để team đọc + tool monitor + cache hiểu đúng.

---

## 💡 Cạm bẫy thường gặp & Best practice

### ❌ Cạm bẫy: Dùng GET với body

```bash
curl -X GET https://api.example.com/users -d '{"filter": "active"}'
```

- **Lý do sai**: spec cho phép nhưng **nhiều proxy/CDN ignore body của GET**. Backend có thể không nhận data.
- **Cách fix**: dùng query string hoặc POST search endpoint:
  ```bash
  curl https://api.example.com/users?filter=active
  curl -X POST https://api.example.com/users/search -d '{"filter":"active"}'
  ```

### ❌ Cạm bẫy: PUT mà gửi 1 field

```bash
curl -X PUT https://api.example.com/users/123 -d '{"email":"new@example.com"}'
```

- **Hậu quả**: backend reset MỌI field khác về null/default → user mất name, role, ... 😱
- **Cách fix**: dùng PATCH cho partial update.

### ❌ Cạm bẫy: POST trùng do retry

Client gửi POST → network timeout → client retry → server đã nhận lần đầu + nhận lần 2 → **tạo 2 record duplicate**.

- **Cách fix**: dùng `Idempotency-Key` header (cần backend support) hoặc kiểm tra duplicate (vd unique constraint trên email).

### ❌ Cạm bẫy: DELETE nhưng không idempotent (trả 404 lần 2)

```bash
DELETE /users/123 → 204 No Content (xoá thành công)
DELETE /users/123 → 404 Not Found (vì đã xoá)
```

- **Lý do**: 404 lần 2 có thể fail client retry logic. Strict idempotent phải trả `204` cả lần 2.
- **Cách fix**: backend trả 204 nếu resource không tồn tại (xoá-able state = xoá-rồi state).

### ❌ Cạm bẫy: POST cho mọi action (RPC-style)

```
POST /api/getUsers
POST /api/createUser
POST /api/updateUserEmail
POST /api/deleteUser
```

- **Hậu quả**: làm CDN/proxy không cache được, monitoring tool không phân biệt action, code khó đọc.
- **Cách fix**: REST-ful với 5 methods + URL chuẩn.

### ✅ Best practice: Methods + Status code đi đôi

| Method | Status thường |
|---|---|
| GET | 200 (found) / 404 (not found) |
| POST | 201 Created / 200 OK (action) |
| PUT | 200 (updated) / 204 (success no body) |
| PATCH | 200 (updated) |
| DELETE | 204 (deleted) / 200 (with body) |

→ Tuân để client + tool predict đúng response.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** Khi nào dùng PUT vs PATCH?

<details>
<summary>💡 Đáp án</summary>

- **PUT** — replace **toàn bộ** resource. Body chứa MỌI field. Field thiếu trong body bị **reset null/default**.
- **PATCH** — update **1 phần**. Body chỉ chứa field cần đổi. Field khác giữ nguyên.

**Trong thực tế**:
- **PATCH** dùng **nhiều hơn** vì client thường đổi 1-2 field, không phải toàn bộ resource
- PUT dùng khi thực sự cần replace full (vd config file)

→ Câu hỏi interview kinh điển. Nhớ: **PUT replace, PATCH update**.

</details>

**Q2.** Vì sao "Idempotent" quan trọng?

<details>
<summary>💡 Đáp án</summary>

**Idempotent** = gọi 1 lần hay N lần kết quả same.

**Quan trọng vì**:

1. **Browser retry tự động** trên idempotent methods (GET/PUT/DELETE) khi network fail. POST không retry → tránh tạo dup.
2. **CDN/Proxy cache** GET (safe + idempotent) — request lại lấy cache, không hit backend.
3. **Client side resilience** — biết method nào safe retry: GET/PUT/DELETE OK retry, POST/PATCH cần idempotency key.
4. **Distributed systems** — same operation lặp do network partition không gây inconsistency.

**Bảng nhanh**:
- ✅ Idempotent: GET, PUT, DELETE, HEAD, OPTIONS
- ❌ Không: POST, PATCH (tuỳ)

</details>

**Q3.** `POST /getUsers` chạy được. Sao "anti-pattern"?

<details>
<summary>💡 Đáp án</summary>

**Technically chạy**, nhưng **vi phạm convention**:

1. **POST = đổi state**, nhưng `/getUsers` là **đọc** (không đổi). Semantic sai.
2. **POST không cache** → mỗi lần gọi hit backend, tốn resource. GET có thể cache CDN/browser.
3. **POST không safe** → tool monitor / log treat như "write" → metric sai.
4. **Browser không retry POST** → client logic phức tạp thêm.
5. **Team confused** — đọc code thấy POST tưởng "tạo gì đó", thực ra read.

**Đúng**: `GET /users` — semantic rõ ràng, cache được, idempotent, tool hiểu đúng.

→ "OK chạy" ≠ "OK design". REST convention không phải décor — nó cho phép infra tự optimize (cache/retry/scale).

</details>

**Q4.** Soft delete vs Hard delete — chọn cái nào?

<details>
<summary>💡 Đáp án</summary>

**Mặc định** dùng **soft delete** cho user-facing data — set `deleted_at = NOW()` thay xoá record.

**Lý do**:
- **Restore được** nếu user lỡ tay
- **Audit log** giữ history
- **Compliance** (vd accounting cần keep record 7 năm)
- **Reference integrity** không break (FK vẫn trỏ tới record cũ)

**Khi nào hard delete**:
- Data thực sự không cần (vd temp cache, log expired)
- **GDPR right to be forgotten** (user yêu cầu xoá hoàn toàn)
- Performance (table quá lớn vì keep soft-deleted)

**Best of both**: soft delete + cron job hard delete sau N ngày/tháng (vd 30 days bin + 6 month full delete).

</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Methods table

| Method | Body | Idempotent | Safe | Cache | Use case |
|---|---|---|---|---|---|
| GET | ❌ | ✅ | ✅ | ✅ | Read |
| HEAD | ❌ | ✅ | ✅ | ✅ | Headers only |
| OPTIONS | ❌ | ✅ | ✅ | ❌ | CORS preflight |
| POST | ✅ | ❌ | ❌ | ❌ | Create / Action |
| PUT | ✅ | ✅ | ❌ | ❌ | Replace full |
| PATCH | ✅ | Tuỳ | ❌ | ❌ | Update partial |
| DELETE | Tuỳ | ✅ | ❌ | ❌ | Delete |

### REST endpoint patterns

```
GET    /users               # list
GET    /users/:id           # get one
GET    /users?role=admin    # filter
POST   /users               # create (201)
PUT    /users/:id           # replace full
PATCH  /users/:id           # update partial
DELETE /users/:id           # delete (204)

GET    /users/:id/posts     # nested list
POST   /users/:id/posts     # nested create

POST   /login               # action (not resource)
POST   /deploy              # action
```

### `curl` cho mỗi method

```bash
curl URL                                 # GET
curl -I URL                              # HEAD
curl -X OPTIONS URL                      # OPTIONS
curl -X POST URL -d '{}'                 # POST
curl -X PUT URL -d '{...full...}'        # PUT
curl -X PATCH URL -d '{...partial...}'   # PATCH
curl -X DELETE URL                       # DELETE
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| EN | VN | Giải thích |
|---|---|---|
| Method | (giữ EN) | Loại HTTP request (GET/POST/...) |
| Idempotent | (giữ EN) | Gọi N lần kết quả same |
| Safe | An toàn | Không đổi state server |
| Resource | Tài nguyên | Object backend quản (user, post, ...) |
| Collection | Tập hợp | List nhiều resource (`/users`) |
| RESTful | (giữ EN) | Tuân theo REST convention |
| Endpoint | Điểm cuối | Method + URL pattern (vd `GET /users/:id`) |
| Idempotency key | (giữ EN) | UUID client gửi để safe POST retry |
| Soft delete | Xoá mềm | Set `deleted_at` thay DROP record |
| Hard delete | Xoá cứng | DELETE record khỏi DB |
| RPC-style | (giữ EN) | API anti-pattern — POST cho mọi action |

---

## 🔗 Liên kết & Tài nguyên

### Trong kho

| Hướng | Bài |
|---|---|
| ⬅️ Bài trước | [00_what-is-http.md](./00_what-is-http.md) — Intro HTTP |
| ➡️ Bài tiếp | [02_http-status-codes.md](./02_http-status-codes.md) — 5 nhóm status |
| 📚 REST design | [05_rest-api-concepts.md](./05_rest-api-concepts.md) |
| 🛠️ Test API | [02_tools/api-clients/](../../../../02_tools/api-clients/) — Postman/curl |

### 🌐 Tài nguyên tham khảo khác

- [MDN HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) — chính thức
- [RFC 9110 §9 Methods](https://www.rfc-editor.org/rfc/rfc9110#section-9) — spec đầy đủ
- [HTTP Method Cheat Sheet](https://restfulapi.net/http-methods/) — quick ref
- [Stripe Idempotency](https://stripe.com/docs/api/idempotent_requests) — real-world idempotency key
- [REST API Tutorial](https://restfulapi.net/) — design REST chuẩn

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `http-https/` lesson 2/6. Cover: tình huống bạn design API anti-pattern `POST /getUsers` → §1 bảng 5 methods + idempotent/safe → §2 GET (URL + cache + safe) → §3 POST (Idempotency-Key Stripe pattern) → §4 PUT replace toàn bộ → §5 PATCH partial + so sánh PUT vs PATCH → §6 DELETE + soft vs hard → §7 HEAD/OPTIONS/CONNECT/TRACE → §8 REST endpoint design + 4 anti-pattern. 5 pitfall + 4 self-check + cheatsheet.
- **v1.1.0 (25/05/2026)** — Bổ sung lead-in trước bảng 5 methods (§1) và các mục §2 (Convention URL / Đặc trưng / Ví dụ / Response). Chuẩn hoá ví dụ placeholder `"name": "Nguyen Van A"`.
