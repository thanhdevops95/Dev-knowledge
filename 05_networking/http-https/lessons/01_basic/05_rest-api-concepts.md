# 🎓 REST API — Triết lý & cách thiết kế API đúng chuẩn

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [HTTP methods](01_http-methods.md), [HTTP status codes](02_http-status-codes.md), [HTTP headers](03_http-headers.md)

> 🎯 *Bài cuối HTTP basic. Học **REST là gì**, **6 ràng buộc Roy Fielding**, **cách design URL theo resource**, **HATEOAS** (sơ lược), **REST vs GraphQL vs gRPC**, **versioning**, và **best practices**. Sau bài này bạn design API không bị sếp phán "không RESTful".*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **REST** là gì + sự khác biệt với "API thông thường"
- [ ] Biết **6 ràng buộc** (constraints) của REST
- [ ] Design URL theo **resource** chứ không theo **verb**
- [ ] Map đúng **HTTP method ↔ CRUD operation**
- [ ] Hiểu **HATEOAS** + tại sao gây tranh cãi
- [ ] So sánh được **REST vs GraphQL vs gRPC vs SOAP**
- [ ] Biết 3 cách **versioning** API (`/v1`, header, query)
- [ ] Tránh được 5 anti-pattern phổ biến khi design REST

---

## Tình huống — Sếp bảo "phải RESTful"

Bạn viết xong backend đầu tiên. Endpoints như sau:

```
POST   /createUser
POST   /getUserById
POST   /updateUserEmail
POST   /deleteUserById
POST   /listAllUsers
POST   /searchUsers
GET    /api/get_user_orders?user_id=42&action=fetch
```

Sếp code review:

> *"API này **không RESTful**. Em sửa lại đi."*

Bạn ngơ:

- **REST** là cái gì?
- Sao toàn `POST` lại sai?
- "Resource-oriented" là sao? URL phải viết như thế nào?
- Có **chuẩn bắt buộc** không, hay chỉ là khuyên?
- **GraphQL** với **gRPC** mới hot, sao công ty vẫn xài REST?

→ Bài này dạy bạn **triết lý REST**, **cách design đúng resource**, **so sánh** REST với GraphQL/gRPC, và **versioning**. Sau bài bạn sẽ viết lại 7 endpoint kia thành **5 endpoint RESTful** ngắn gọn hơn nhiều.

---

## 1️⃣ Vậy REST là gì?

**REST** = **REpresentational State Transfer** — một **kiến trúc** (architectural style) thiết kế **API qua HTTP**, đề xuất bởi **Roy Fielding** trong luận án tiến sĩ năm **2000** (cùng người đồng-thiết-kế HTTP/1.1).

> 🧠 **Ẩn dụ — REST như nguyên tắc xây nhà:**
> - REST **KHÔNG phải framework** (như React).
> - REST **KHÔNG phải protocol** (như HTTP).
> - REST là **bộ nguyên tắc design** — giống "phong thủy xây nhà": ai làm theo thì nhà ổn, ai phá thì... vẫn ở được nhưng đời con cháu khổ.

### REST vs "API thường" (RPC-style)

Trước REST, API thường viết theo style **RPC** (Remote Procedure Call) — URL là **động từ** ("làm gì"), chỉ dùng POST cho mọi action. REST đảo ngược: URL là **danh từ** ("resource gì"), method báo "làm gì với nó". 5 trục khác biệt cốt lõi:

| Tiêu chí | REST | RPC (Remote Procedure Call) |
|---|---|---|
| **URL** mô tả | **Resource** (danh từ) | **Action** (động từ) |
| Ví dụ | `GET /users/42` | `POST /getUserById?id=42` |
| Method | GET/POST/PUT/PATCH/DELETE đầy đủ | Thường chỉ POST |
| Status code | Dùng đúng (404, 401, 409...) | Hay trả 200 + `{"error": "..."}` |
| Mindset | "Dữ liệu gì" | "Làm gì" |

### API "RESTful" và API "REST"

Phân biệt 2 thuật ngữ hay bị nhầm lẫn — đặc biệt khi interview hoặc đọc job description. **REST** là chuẩn nghiêm ngặt 6 ràng buộc của Roy Fielding (2000); **RESTful** là phiên bản "đủ dùng" công nghiệp dùng hằng ngày:

- **REST** đầy đủ 6 ràng buộc → hiếm gặp ngoài đời (đặc biệt HATEOAS).
- **RESTful** = "theo phong cách REST" → đa số API thực tế chỉ ở **Level 2 Richardson Maturity Model** (HTTP methods + resource URL + status code đúng), không có HATEOAS. **Đó vẫn được gọi là REST trong công nghiệp.**

→ Khi sếp nói "RESTful", **không có nghĩa phải đủ 6 constraints** — chỉ cần resource URL + method đúng + status đúng là đủ trong 90% công ty.

---

## 2️⃣ 6 ràng buộc (constraints) của REST

Roy Fielding định nghĩa **6 constraints** mà 1 API phải tuân theo để gọi là REST đúng nghĩa:

| # | Constraint | Nghĩa | Bắt buộc? |
|---|---|---|---|
| 1 | **Client-Server** | Tách rời UI (client) và data (server) | ✅ Mandatory |
| 2 | **Stateless** | Server không lưu state giữa các request | ✅ Mandatory |
| 3 | **Cacheable** | Response phải nói rõ có cache được không | ✅ Mandatory |
| 4 | **Uniform Interface** | URL/method/format thống nhất | ✅ Mandatory |
| 5 | **Layered System** | Client không biết gì giữa nó và server (proxy, LB, CDN OK) | ✅ Mandatory |
| 6 | **Code on Demand** | Server có thể gửi code (JS) cho client chạy | 🔵 Optional |

### Diễn giải nhanh

**1. Client-Server** → Frontend (React) và Backend (API) phải **deploy độc lập**, đổi UI không cần đổi DB.

**2. Stateless** → Mỗi request phải **tự đủ thông tin** (Authorization header chẳng hạn). Server không "nhớ" "à user này vừa login phút trước". → Quan trọng cho **horizontal scaling** (3 server đứng sau LB, request nào đập server nào cũng xử lý được).

**3. Cacheable** → Response phải có `Cache-Control` (xem [bài headers](03_http-headers.md)). API trả "list 100 sản phẩm hot" mà không cho cache → server đập 1000 RPS chết.

**4. Uniform Interface** → 4 sub-rule:
   - **Resource-based URL** (`/users/42`, không phải `/getUser?id=42`)
   - **Manipulation through representation** (client gửi JSON đại diện resource, không thao tác DB trực tiếp)
   - **Self-descriptive messages** (mỗi request đủ `Content-Type`, `Accept`...)
   - **HATEOAS** (response chứa link tới action kế tiếp — xem §4)

**5. Layered System** → Giữa client và server có thể có **CDN**, **reverse proxy**, **load balancer**, **API gateway** — client không cần biết.

**6. Code on Demand** → Server gửi JavaScript về client thực thi. Hầu hết API hiện đại **không dùng** (vì không safe).

→ **Trong thực tế**, 90% API gọi là "REST" chỉ tuân **#1, #2, #4 (3 sub-rule đầu)**. Đó vẫn được chấp nhận.

---

## 3️⃣ Resource design — Linh hồn của REST

### Quy tắc 1 — URL là **danh từ**, không phải **động từ**

Quy tắc đầu tiên — và là cái dễ nhận biết "API có RESTful hay không": URL chỉ chứa **danh từ** (resource), không chứa **động từ** (action). Động từ là vai trò của HTTP method. So sánh 5 cặp anti-pattern thường gặp vs version REST đúng:

| ❌ Sai (RPC-style) | ✅ Đúng (REST) |
|---|---|
| `POST /createUser` | `POST /users` |
| `GET /getUserById?id=42` | `GET /users/42` |
| `POST /updateUserEmail` | `PATCH /users/42` |
| `POST /deleteUserById` | `DELETE /users/42` |
| `GET /listAllUsers` | `GET /users` |

**Mindset:** URL trả lời câu hỏi *"resource nào?"*, method trả lời câu hỏi *"làm gì với nó?"*.

### Quy tắc 2 — Resource là **danh từ số nhiều**

Convention REST là **luôn dùng plural form** (`/users` chứ không `/user`) cho cả collection và single resource. Lý do: 1 đường URL pattern nhất quán cho cả 2 case — `/users` (list) và `/users/42` (1 record), không cần switch giữa singular/plural khi viết route:

```
✅ /users        ← collection (danh sách)
✅ /users/42     ← single (1 user cụ thể)
❌ /user         ← inconsistent
❌ /user/42      ← inconsistent
```

### Quy tắc 3 — Map đúng method ↔ CRUD

REST mapping 1-1 giữa **HTTP method** và **CRUD operation** (Create/Read/Update/Delete). Cùng URL `/users/42` nhưng GET = đọc, PUT = thay toàn bộ, PATCH = sửa 1 phần, DELETE = xoá. Đây là pattern chuẩn mọi REST API tuân theo:

| HTTP Method | CRUD | URL ví dụ | Mô tả |
|---|---|---|---|
| **GET** `/users` | Read (list) | `/users` | Lấy tất cả |
| **GET** `/users/42` | Read (one) | `/users/42` | Lấy 1 user |
| **POST** `/users` | Create | `/users` | Tạo mới (server gán ID) |
| **PUT** `/users/42` | Update (toàn bộ) | `/users/42` | Thay thế toàn bộ user 42 |
| **PATCH** `/users/42` | Update (1 phần) | `/users/42` | Chỉ đổi 1-2 field |
| **DELETE** `/users/42` | Delete | `/users/42` | Xóa user 42 |

→ Chi tiết method idempotent/safe xem [bài 01](01_http-methods.md).

### Quy tắc 4 — Nested resource cho quan hệ

```
GET    /users/42/orders          ← danh sách order của user 42
GET    /users/42/orders/100      ← order #100 của user 42
POST   /users/42/orders          ← user 42 đặt order mới
DELETE /users/42/orders/100      ← user 42 hủy order 100
```

**Nguyên tắc:** Không nest quá **2 level**. Quá nest → URL khó nhớ, khó test.

```
❌ /users/42/orders/100/items/5/reviews/77   ← quá nest
✅ /reviews/77                                ← flat hơn, dễ dùng
```

### Quy tắc 5 — Query string cho filter/sort/paginate

```
GET /users?role=admin              ← filter
GET /users?sort=created_at:desc    ← sort
GET /users?page=2&limit=20         ← paginate
GET /users?q=nguyen&fields=id,email  ← search + sparse fieldset
```

→ Query string KHÔNG dùng cho action (`?action=delete` ❌).

### Viết lại 7 endpoint thành RESTful

**Trước (bị sếp chê):**
```
POST /createUser
POST /getUserById
POST /updateUserEmail
POST /deleteUserById
POST /listAllUsers
POST /searchUsers
POST /get_user_orders
```

**Sau (RESTful):**
```
POST   /users                        ← create
GET    /users/{id}                   ← get one
PATCH  /users/{id}                   ← update email (partial)
DELETE /users/{id}                   ← delete
GET    /users                        ← list all
GET    /users?q=nguyen               ← search
GET    /users/{id}/orders            ← list orders of user
```

→ **5 endpoint** thay vì 7. Method tự nói "làm gì". URL tự nói "với cái gì". Sếp gật đầu.

---

## 4️⃣ HATEOAS — Constraint gây tranh cãi nhất

**HATEOAS** = **Hypermedia As The Engine Of Application State**.

**Ý tưởng:** Response không chỉ chứa data, mà còn chứa **link** tới action kế tiếp client có thể làm.

```jsonc
// GET /users/42
{
  "id": 42,
  "name": "Nguyen Van A",
  "email": "nguyenvana@example.com",
  "_links": {
    "self":    { "href": "/users/42" },
    "orders":  { "href": "/users/42/orders" },
    "update":  { "href": "/users/42", "method": "PATCH" },
    "delete":  { "href": "/users/42", "method": "DELETE" }
  }
}
```

→ Client **không cần hardcode URL** — nó đi theo link như browser đi theo `<a href>`. Đó là gốc "Hypermedia" — y như HTML.

### Tại sao gây tranh cãi?

| Phe ủng hộ | Phe phản đối |
|---|---|
| API tự khám phá được (discoverable) | Tăng kích thước payload 30-50% |
| Client decouple khỏi URL hardcoded | Frontend SPA thường hardcode URL vẫn OK |
| Phù hợp với spirit nguyên gốc của Fielding | Hầu hết library client (axios, fetch) không khai thác |

→ **Thực tế 2026**: ~90% "REST API" công nghiệp **không có HATEOAS**. Chỉ một số framework như **Spring HATEOAS** (Java), **HAL/JSON:API spec** mới đầy đủ.

→ Khi sếp nói "RESTful", **không bao gồm HATEOAS** trong 99% trường hợp.

---

## 5️⃣ REST vs GraphQL vs gRPC vs SOAP

| Tiêu chí | **REST** | **GraphQL** | **gRPC** | **SOAP** |
|---|---|---|---|---|
| **Năm ra đời** | 2000 | 2015 (Facebook) | 2016 (Google) | 1998 |
| **Transport** | HTTP | HTTP | HTTP/2 | HTTP/SMTP |
| **Format** | JSON (thường) | JSON | Protobuf (binary) | XML |
| **Schema** | OpenAPI (optional) | Schema-first (bắt buộc) | `.proto` (bắt buộc) | WSDL (bắt buộc) |
| **Endpoint** | Nhiều (1 per resource) | **1 endpoint duy nhất** | RPC-style (methods) | 1 endpoint + SOAP envelope |
| **Over/under-fetch** | Có (trả thừa hoặc gọi nhiều lần) | Không (client query đúng field cần) | Không (schema chặt) | Có |
| **Type safety** | Yếu (JSON tự do) | Mạnh (schema) | **Rất mạnh** (Protobuf) | Mạnh (WSDL) |
| **Realtime** | Không (cần WebSocket riêng) | Subscription | Streaming native | Không |
| **Dùng cho** | Public API, web/mobile | Mobile app, complex frontend | Microservices internal | Legacy enterprise |
| **Cache (HTTP)** | ✅ Native (qua URL) | ❌ Khó (1 endpoint) | ❌ | ❌ |

### Khi nào chọn gì?

| Use case | Chọn |
|---|---|
| **Public API** cho 3rd-party dev | **REST** — phổ thông, docs dễ, ai cũng biết |
| **Mobile app** + cần linh hoạt field | **GraphQL** — giảm bandwidth, 1 endpoint |
| **Microservice ↔ microservice** trong cùng cluster | **gRPC** — binary nhanh, type-safe, streaming |
| **Enterprise legacy** (bank, gov) | **SOAP** — đã tồn tại, không nên thay |
| **Realtime chat/notification** | **WebSocket / SSE** (không phải bộ trên) |

→ **2026 reality:** 70% API trong công nghiệp vẫn là **REST**. GraphQL và gRPC tăng nhưng chưa thay thế. SOAP đang chết dần (trừ banking/insurance).

---

## 6️⃣ API Versioning

Khi API có người dùng (mobile app đã deploy), **đổi API breaking** = đập app cũ. Cần versioning để app v1 (cũ) vẫn chạy khi server đã có v2 (mới).

### 3 cách versioning phổ biến

#### Cách 1 — URL path (phổ biến nhất)

```
GET /v1/users/42
GET /v2/users/42
```

✅ Dễ test bằng browser, copy-paste, cache theo URL\
❌ "Không thuần REST" (URL nên là resource, không phải version)

→ **Stripe, GitHub, Twitter** đều dùng cách này.

#### Cách 2 — Custom header

```http
GET /users/42 HTTP/1.1
Accept-Version: v2
```

✅ URL sạch (resource-only)\
❌ Khó test (phải set header), khó cache theo version

→ **Stripe** kết hợp: URL `/v1` + header `Stripe-Version: 2024-04-10` (date-based).

#### Cách 3 — Query string

```
GET /users/42?version=2
```

✅ Dễ test\
❌ Query string nên cho filter, không phải metadata. Ít dùng nhất.

### Khi nào bump version?

| Thay đổi | Bump version? |
|---|---|
| Thêm field optional vào response | ❌ Không (backward compat) |
| Thêm endpoint mới | ❌ Không |
| Bỏ field khỏi response | ✅ Có (breaking) |
| Đổi kiểu field (`int` → `string`) | ✅ Có (breaking) |
| Đổi semantic 1 endpoint | ✅ Có |

→ **Nguyên tắc:** thêm = OK, **xóa/đổi semantic** = bump.

---

## 7️⃣ Best practices — bạn apply

### ✅ DO

1. **Plural noun cho resource** → `/users`, không phải `/user`.
2. **Status code chính xác** → 201 cho create, 204 cho delete-không-body, 400 vs 401 vs 403 vs 404 (xem [bài status](02_http-status-codes.md)).
3. **JSON snake_case hoặc camelCase, thống nhất** trong cả API.
4. **Đầy đủ pagination** (`?page=` + `?limit=`) cho list lớn → tránh trả 10,000 record.
5. **Filter qua query** → `?status=active`, không phải `/activeUsers`.
6. **Versioning từ ngày đầu** → `/v1/...` ngay v1, không chờ tới khi cần v2 mới thêm.
7. **HTTPS bắt buộc** (xem [bài 04](04_https-tls.md)).
8. **Document bằng OpenAPI (Swagger)** → 1 file YAML/JSON tả toàn bộ endpoint.

### ❌ DON'T (5 anti-pattern phổ biến)

1. **Verb trong URL** — `POST /createUser` thay vì `POST /users`.
2. **Trả 200 + `{"error": "..."}`** — phải dùng đúng 4xx/5xx, status code là phần response.
3. **POST cho mọi thứ** — mất idempotency, mất cache, mất semantic.
4. **Field naming không nhất quán** — `user_name` ở endpoint A, `userName` ở endpoint B.
5. **Quên pagination** → `/users` trả 50,000 record, mobile app crash.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Tưởng REST = HTTP** → REST là **kiến trúc**, có thể chạy qua non-HTTP (hiếm). HTTP là **protocol**.
2. **Tưởng "không HATEOAS = không REST"** → 99% công ty xài Level 2 Richardson maturity vẫn gọi REST.
3. **Dùng PUT để partial update** → PUT là **replace toàn bộ** (idempotent). Partial dùng **PATCH**.
4. **Versioning sau khi đã có user** → Bumping v1→v2 lúc đã có 100k app đã deploy = đập app cũ. Versioning từ ngày đầu.
5. **Pluralize sai tiếng Anh** → `/people` ✅, `/persons` ❌. `/children` ✅, `/childs` ❌. Khi đặt tên resource hơi rủi ro thì xài generic: `/items`, `/posts`.

---

## 🧠 Tự kiểm tra (Self-check)

1. URL `POST /deleteUser?id=42` có RESTful không? Sửa lại.
2. Khác biệt giữa `PUT /users/42` và `PATCH /users/42`?
3. 4 cách versioning API là gì? Cách nào phổ biến nhất?
4. Khi nào chọn GraphQL thay vì REST?
5. HATEOAS là gì, vì sao 99% API không dùng?

<details>
<summary>Gợi ý đáp án</summary>

1. Không. `POST` dùng cho create, không phải delete. URL chứa verb (`deleteUser`) là RPC-style. Fix: `DELETE /users/42`.
2. `PUT` replace **toàn bộ** resource (gửi đủ field, field thiếu sẽ thành null). `PATCH` chỉ đổi field gửi lên (partial update).
3. 3 cách: URL path (`/v1/...`), custom header (`Accept-Version: v2`), query (`?version=2`). **URL path** phổ biến nhất (Stripe, GitHub, Twitter).
4. Khi client (đặc biệt mobile) **cần linh hoạt chọn field** — giảm over-fetch + giảm round-trip. REST bắt client gọi nhiều endpoint hoặc nhận thừa field.
5. HATEOAS = response chứa link tới action kế tiếp (như HTML `<a href>`). 99% không dùng vì: tăng payload size, library client không khai thác, frontend SPA hardcode URL vẫn OK.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

| Thao tác | URL + Method |
|---|---|
| Tạo user | `POST /users` |
| Lấy user 42 | `GET /users/42` |
| Đổi email user 42 | `PATCH /users/42` |
| Xóa user 42 | `DELETE /users/42` |
| List all users | `GET /users` |
| Filter user admin | `GET /users?role=admin` |
| Paginate | `GET /users?page=2&limit=20` |
| Sort by date desc | `GET /users?sort=created_at:desc` |
| Order của user 42 | `GET /users/42/orders` |
| Tạo order cho user 42 | `POST /users/42/orders` |
| Versioning | `/v1/users/42` |

### Method ↔ CRUD ↔ Status code

| Method | CRUD | Success status | Idempotent |
|---|---|---|---|
| GET | Read | 200 | ✅ |
| POST | Create | 201 | ❌ |
| PUT | Replace | 200/204 | ✅ |
| PATCH | Partial update | 200/204 | ❌ |
| DELETE | Delete | 204 | ✅ |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **REST** | REpresentational State Transfer — kiến trúc API qua HTTP (Roy Fielding, 2000) |
| **RESTful** | "Theo phong cách REST" — không bắt buộc đủ 6 constraints |
| **Resource** | Đối tượng API quản lý (user, order, post...) — biểu diễn bằng URL danh từ số nhiều |
| **CRUD** | Create / Read / Update / Delete — 4 thao tác cơ bản, map vào POST/GET/PUT-PATCH/DELETE |
| **Idempotent** | Gọi N lần = gọi 1 lần về kết quả (GET, PUT, DELETE) |
| **HATEOAS** | Hypermedia As The Engine Of App State — response chứa link tới action kế tiếp |
| **Richardson Maturity Model** | Thang 0-3 đo "mức RESTful": L0 = 1 endpoint, L1 = resource, L2 = HTTP method + status, L3 = HATEOAS |
| **OpenAPI / Swagger** | Spec mô tả API (YAML/JSON) — auto-gen docs, client SDK |
| **GraphQL** | Query language API (Facebook 2015) — 1 endpoint, client chọn field |
| **gRPC** | RPC framework Google — Protobuf binary + HTTP/2 + streaming |
| **Versioning** | Cơ chế đánh dấu phiên bản API để client cũ vẫn chạy (`/v1/...`, header, query) |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [HTTPS + TLS — Cert, Handshake, Let's Encrypt](04_https-tls.md)
- ↑ **Về cụm:** [http-https README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [HTTP methods](01_http-methods.md) — base cho REST CRUD mapping
- [HTTP status codes](02_http-status-codes.md) — REST dùng status code đúng nghĩa
- [HTTP headers](03_http-headers.md) — `Content-Type`, `Accept`, versioning header

### 🌐 Tài nguyên tham khảo khác
- 📖 [Roy Fielding's dissertation (2000)](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm) — bản gốc REST
- 📖 [Richardson Maturity Model — Martin Fowler](https://martinfowler.com/articles/richardsonMaturityModel.html)
- 📖 [REST API Tutorial — restfulapi.net](https://restfulapi.net/)
- 📖 [OpenAPI Specification](https://swagger.io/specification/)
- 📖 [JSON:API spec](https://jsonapi.org/) — chuẩn cho REST + HATEOAS
- 📖 [GraphQL vs REST — Apollo blog](https://www.apollographql.com/blog/graphql-vs-rest)
- 📖 [gRPC docs](https://grpc.io/docs/)

---

> 🎯 *Sau bài này bạn design được API RESTful không bị sếp chê. Cluster HTTP basic kết thúc ở đây — tổng 6 bài đủ cover **HTTP là gì → methods → status → headers → HTTPS → REST**. Bài sau bạn sẽ vào **02_intermediate** (CORS, JWT, caching nâng cao) hoặc nhảy sang cluster khác (DNS, TCP-IP).*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `http-https/` lesson 5/6. Cover: REST 6 constraints + Richardson Maturity Model + Resource design (5 quy tắc) + Status code + Versioning (URL/header) + Pagination + Filtering/Sorting + HATEOAS overview + REST vs GraphQL vs gRPC comparison.
- **v1.1.0 (25/05/2026)** — Bổ sung lead-in trước các bảng ở §1 (REST vs RPC, phân biệt RESTful/REST) và §3 (Quy tắc 1 URL danh từ, Quy tắc 2 plural, Quy tắc 3 method↔CRUD). Thêm Changelog section. Nội dung kỹ thuật giữ nguyên.
