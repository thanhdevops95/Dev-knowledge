# 🎓 FastAPI là gì? — Web framework Python tốc độ + type-safe

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~15 phút\
> **Prerequisites:** Python cơ bản (variables, functions, decorators) + [HTTP là gì](../../../../05_Networking/http-https/lessons/01_basic/00_what-is-http.md) + [REST API concepts](../../../../05_Networking/http-https/lessons/01_basic/05_rest-api-concepts.md)

> 🎯 *Bài INTRO. Hiểu **FastAPI là gì**, **so sánh Flask/Django/FastAPI**, **vì sao type hints + Pydantic**, **OpenAPI auto-docs**, **sync vs async**, cài + chạy Hello World, mở Swagger UI.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **FastAPI** + lịch sử ngắn (Sebastián Ramírez, 2018)
- [ ] So sánh **FastAPI vs Flask vs Django** (3 framework lớn nhất 2026)
- [ ] Biết tại sao **type hints + Pydantic** là superpower
- [ ] Hiểu **OpenAPI auto-docs** — Swagger UI miễn phí
- [ ] Phân biệt **sync vs async** + khi nào dùng `async def`
- [ ] Cài FastAPI + uvicorn + chạy server đầu tiên
- [ ] Mở Swagger UI tại `/docs` và test endpoint
- [ ] Biết 3 trang docs: `/docs` Swagger, `/redoc` ReDoc, `/openapi.json` raw

---

## Tình huống — Bạn muốn build API đầu tiên

Bạn đã học HTTP + REST + SQL. Giờ cần **viết code backend**. Anh hỏi senior:

> *"Python web framework nào nên dùng 2026? Flask đọc nhiều... Django to quá... FastAPI nghe rần rộ?"*

Senior trả:
- **Flask** (2010) — minimalist, rất linh hoạt, nhưng phải tự ghép từng phần.
- **Django** (2005) — "battery included", admin/ORM/auth sẵn, nhưng nặng, monolith.
- **FastAPI** (2018) — modern, **async native**, **type-safe**, **auto OpenAPI**. Code ít, validate tự, docs tự sinh.

> *"Mới build API 2026? **FastAPI**. Hết suy nghĩ."*

Bạn ngơ:
- Sao FastAPI **nhanh hơn**?
- **Type hints** trong Python để làm gì?
- **OpenAPI auto-docs** = tự sinh Swagger? Khỏi viết tay?
- Khi nào `def` vs `async def`?

→ Bài này dạy bạn (và bạn) **FastAPI là gì** + setup + Hello World.

---

## 1️⃣ Vậy FastAPI là gì?

**FastAPI** = web framework Python **hiện đại**, **nhanh** (gần Node.js + Go), **type-safe** dựa trên type hints + Pydantic, **auto-generate OpenAPI docs**.

- Tạo bởi **Sebastián Ramírez** (Colombia, 2018).
- Build trên 2 thư viện:
  - **Starlette** — ASGI framework (async HTTP).
  - **Pydantic** — validation + serialization từ type hints.
- 2026: **~75k GitHub stars**, dùng bởi Microsoft, Netflix, Uber, Stripe.

### Các superpower

FastAPI hot vì kết hợp 6 feature mà framework cũ (Flask/Django) không có sẵn — đặc biệt **type hints + Pydantic** biến Python thành type-safe runtime. Đây là lý do startup mới 2026 mặc định pick FastAPI:

| Feature | Lợi ích |
|---|---|
| **Type hints native** | Validation tự + autocomplete IDE đầy đủ |
| **Pydantic** | Request/response model declaratively |
| **OpenAPI auto** | Swagger UI + ReDoc miễn phí ngay khi viết code |
| **Async native** | Concurrency cao, không cần thread |
| **Dependency Injection** | Code modular, test dễ |
| **Performance** | TechEmpower benchmark: top 5 web framework (gần Go) |

> 🧠 **Ẩn dụ — FastAPI như Tesla 2026:**
> - **Flask** = xe ô tô tự lắp (1995 style) — bạn ghép từng linh kiện.
> - **Django** = xe SUV gia đình (2005 style) — đầy đủ tính năng, nặng và to.
> - **FastAPI** = Tesla — modern, tự lái nhiều thứ (validation, docs), nhanh và đẹp.

---

## 2️⃣ So sánh 3 framework Python lớn nhất 2026

3 framework cùng tồn tại với 3 triết lý khác nhau — FastAPI modern type-safe, Flask minimalist, Django all-in-one. Bảng so sánh 12 trục giúp pick cho project mới:

| Tiêu chí | **FastAPI** | **Flask** | **Django** |
|---|---|---|---|
| Năm ra đời | 2018 | 2010 | 2005 |
| Triết lý | Modern + async + type-safe | Minimalist | Battery-included |
| Async native | ✅ | 🟡 (Flask 2+ support) | 🟡 (Django 4+ async views) |
| Type hints | ✅ Built-in | ❌ (phải dùng Marshmallow extra) | ❌ |
| Auto docs | ✅ Swagger + ReDoc | ❌ (cần Flask-RESTX) | ❌ (cần DRF) |
| ORM | ❌ (chọn riêng: SQLAlchemy/SQLModel) | ❌ | ✅ Django ORM |
| Auth | ❌ (chọn riêng) | ❌ | ✅ Built-in |
| Admin | ❌ | ❌ | ✅ Built-in |
| Học khó | 🟢 Dễ | 🟢 Rất dễ | 🟡 Trung bình |
| Performance | 🟢 Top 5 | 🟡 Trung bình | 🟡 Trung bình |
| Production-ready | ✅ | ✅ | ✅ |
| Best for | **REST API**, microservice | API + freeform | Full-stack web (HTML server-side) |

### Chọn cái nào?

Không có "framework tốt nhất" — chỉ có framework phù hợp use case. Bảng decision tree cho 5 scenario phổ biến giúp pick nhanh:

| Use case | Chọn |
|---|---|
| REST API JSON (mobile + SPA frontend) 2026 | **FastAPI** |
| Quick prototype + Tinh tế kiểm soát | Flask |
| Full-stack server-rendered (CMS, admin panel) | Django |
| Microservice nhỏ, type-safe quan trọng | FastAPI |
| Có team Django cũ, không muốn đổi | Django |

→ **2026 reality**: 60-70% startup mới chọn FastAPI cho API. Django vẫn vua cho full-stack có admin. Flask còn dùng cho legacy + dev tool.

---

## 3️⃣ Type hints + Pydantic — superpower của FastAPI

### Python type hints (PEP 484, từ 2014)

Type hints là **annotation kiểu data** cho parameter + return — Python parser hiểu nhưng **không enforce** ở runtime. Mặc định chỉ giúp IDE autocomplete + type checker (mypy). Cú pháp đơn giản:

```python
def add(x: int, y: int) -> int:
    return x + y
```

→ `x: int` = "x là số nguyên". Python **không enforce** ở runtime (vẫn nhận `add("a", "b")` — sẽ lỗi sau).

### Pydantic — biến hint thành validation thực sự

Pydantic upgrade Python type hints thành **runtime validation** — sai kiểu là `ValidationError` ngay. Đây là **magic chính** của FastAPI: request body tự parse + validate + serialize JSON, không cần viết tay:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None

user = User(id=1, name="Nguyen Van A", email="nguyenvana@ex.com")
# OK

user = User(id="not-a-number", name="Nguyen Van A", email="x")
# ValidationError: id phải là int
```

→ Pydantic **validate ở runtime** từ type hints. Sai = `ValidationError` rõ ràng.

### FastAPI dùng Pydantic cho mọi thứ

```python
@app.post("/users")
def create_user(user: User):       # ← Pydantic model
    return user
```

Khi client POST JSON sai schema:
```json
{"id": "abc", "name": 123}
```

→ FastAPI tự trả **422 Unprocessable Entity** với chi tiết lỗi:
```json
{
  "detail": [
    {"loc": ["body", "id"], "msg": "value is not a valid integer", "type": "type_error.integer"},
    {"loc": ["body", "name"], "msg": "str type expected", "type": "type_error.str"}
  ]
}
```

→ Bạn viết 0 dòng validation code. FastAPI lo hết.

---

## 4️⃣ OpenAPI auto-docs — Swagger miễn phí

FastAPI đọc Pydantic models + decorator → tự sinh **OpenAPI spec** → render Swagger UI.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{id}")
def get_user(id: int):
    return {"id": id, "name": "bạn"}
```

Mở browser **`http://localhost:8000/docs`**:

```
┌─────────────────────────────────────────┐
│ My API           v1.0.0   /openapi.json │
├─────────────────────────────────────────┤
│ GET  /users/{id}        Get User    ▼   │
│ ┌───────────────────────────────────┐   │
│ │ Parameters:                       │   │
│ │   id  integer  required           │   │
│ │ [Try it out]                      │   │
│ └───────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

→ Có "Try it out" để **test ngay trong browser**. Cũ là Postman riêng — giờ tích hợp.

### 3 trang docs miễn phí

| URL | Tool |
|---|---|
| `/docs` | **Swagger UI** — interactive, "Try it out" |
| `/redoc` | **ReDoc** — đẹp, đọc tài liệu (read-only) |
| `/openapi.json` | **Raw OpenAPI spec** — feed vào Postman/code generator |

> 💡 OpenAPI = chuẩn ngành mô tả API ([bài REST](../../../../05_Networking/http-https/lessons/01_basic/05_rest-api-concepts.md#7️⃣-best-practices--long-apply)). FastAPI cho free.

---

## 5️⃣ Sync vs Async — khi nào `async def`?

Python có 2 cách viết function:

```python
# Sync (thông thường)
def get_user_sync():
    user = db.fetch_user(1)        # Block 50ms
    posts = api.fetch_posts(1)     # Block 100ms
    return user, posts             # Total 150ms

# Async
async def get_user_async():
    user = await db.fetch_user(1)
    posts = await api.fetch_posts(1)
    return user, posts
```

### Khi nào `def`, khi nào `async def`?

| Tình huống | Dùng |
|---|---|
| **I/O wait** (DB, HTTP call, file) + có library async | `async def` |
| **CPU-bound** (compute, parse) | `def` (sync) — Python GIL không tận dụng async |
| **Library cũ sync only** | `def` — FastAPI tự chạy trong thread pool |
| **Mixed** — không chắc | `async def` an toàn |

### FastAPI thông minh

```python
# Cả 2 đều OK
@app.get("/sync")
def sync_handler():       # FastAPI chạy thread pool
    return {"ok": True}

@app.get("/async")
async def async_handler():   # FastAPI chạy event loop
    return {"ok": True}
```

→ Bạn không cần biết hết về asyncio để dùng FastAPI. Bắt đầu với `def` cũng được.

### Async ROI thực tế

- **App I/O-heavy** (mọi API call DB/external) → async tăng throughput 5-20x.
- **App CPU-heavy** (image processing) → async **không giúp** — cần multi-process.
- Beginner: bắt đầu `def` đơn giản, async sau khi cần.

---

## 6️⃣ Cài + chạy Hello World

### Cài đặt

```bash
# Tạo venv (always!)
python3 -m venv venv
source venv/bin/activate          # Mac/Linux
# venv\Scripts\activate            # Windows

# Cài FastAPI + uvicorn (ASGI server)
pip install "fastapi[standard]"
# Hoặc cụ thể: pip install fastapi uvicorn[standard]
```

### Hello World — file `main.py`

```python
from fastapi import FastAPI

app = FastAPI(
    title="My First API",
    version="1.0.0",
    description="bạn's first FastAPI server"
)

@app.get("/")
def root():
    return {"message": "Hello FastAPI!"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": f"User #{user_id}"}
```

### Chạy server

```bash
fastapi dev main.py
# Hoặc cách cũ:
# uvicorn main:app --reload --port 8000
```

→ Output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started reloader process
INFO:     Application startup complete.
```

### Test

```bash
# Terminal khác
curl http://localhost:8000/
# {"message":"Hello FastAPI!"}

curl http://localhost:8000/users/42
# {"user_id":42,"name":"User #42"}

curl http://localhost:8000/users/abc
# 422 — id không phải int
```

### Mở `/docs`

→ Browser: [http://localhost:8000/docs](http://localhost:8000/docs)

```
GET /           Root
GET /users/{user_id}  Get User
   Parameters:
     user_id  integer  required
   [Try it out]
```

→ Click "Try it out" → nhập `user_id = 42` → "Execute" → thấy response.

→ Đẹp như Stripe API docs. Bạn viết 5 dòng Python.

---

## 7️⃣ FastAPI app structure cơ bản

```
myproject/
├── venv/                    # Virtual env
├── main.py                  # FastAPI app entry
├── requirements.txt         # Deps
└── .env                     # Secrets (KHÔNG commit)
```

### Production cấu trúc nâng cao

```
myproject/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI() instance + middleware
│   ├── api/                 # Routes
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── orders.py
│   ├── models/              # Pydantic + DB models
│   │   └── user.py
│   ├── db/                  # DB connection + session
│   │   └── database.py
│   ├── core/                # Config + auth + security
│   │   ├── config.py
│   │   └── security.py
│   └── dependencies.py      # Shared DI
├── tests/
├── requirements.txt
└── .env
```

→ Tổ chức như vậy khi project lớn. Beginner: bắt đầu `main.py` 1 file.

---

## 8️⃣ Bạn viết app đầu tiên — sản phẩm

```python
from fastapi import FastAPI

app = FastAPI(title="bạn Shop API", version="0.1.0")

products = [
    {"id": 1, "name": "iPhone", "price": 25000000},
    {"id": 2, "name": "AirPods", "price": 5000000},
]

@app.get("/products")
def list_products():
    return products

@app.get("/products/{id}")
def get_product(id: int):
    for p in products:
        if p["id"] == id:
            return p
    return {"error": "Not found"}
```

→ Chạy `fastapi dev main.py`. Mở `/docs`. Test "list" + "get" trong browser. **Hết 5 phút có API thực sự**.

→ Bài kế tiếp dạy **path/query/body params** chuẩn + return status code đúng.

---

## ⚠️ 5 pitfall hay vướng

1. **Quên virtual env** → cài global → conflict versions. Mỗi project 1 venv.
2. **Đổi code không reload** → quên `--reload` flag hoặc `fastapi dev`. Production dùng `fastapi run` (no reload).
3. **`async def` mà bên trong gọi sync DB** → block event loop. Hoặc tất cả `await`, hoặc tất cả sync.
4. **Tin docs auto sinh là đủ** → docs nói **có endpoint**, không nói **business logic đúng**. Vẫn cần test.
5. **Port 8000 đã dùng** → đổi: `fastapi dev main.py --port 8001`. Hoặc `lsof -i :8000` tìm process kill.

---

## ✅ Self-check

1. So sánh **FastAPI** với **Flask** + **Django** trên 3 tiêu chí.
2. **Type hints** và **Pydantic** giúp gì cho dev FastAPI?
3. Tại sao OpenAPI **auto-generated** là deal-breaker?
4. Khi nào dùng `def` vs `async def`?
5. Truy cập 3 trang docs khi server đã chạy?

<details>
<summary>Gợi ý đáp án</summary>

1. **Sync/async**: FastAPI native async, Flask 2+ có, Django 4+ có (kém native hơn). **Auto docs**: FastAPI ✅, Flask/Django ❌ phải thêm extension. **Type hints**: FastAPI built-in, 2 cái còn lại không. **Best for**: FastAPI = REST API, Flask = freeform, Django = full-stack có admin.

2. **Type hints** = annotation `x: int`. **Pydantic** = validation runtime từ hint. FastAPI **combine** chúng: declare schema bằng class Pydantic → tự validate request, tự generate OpenAPI, IDE autocomplete đầy đủ. Code ít, đảm bảo nhiều.

3. **OpenAPI** là chuẩn ngành mô tả API. **Auto-generated**: bạn không tốn thời gian viết+update docs tay. Mỗi sửa code = docs cập nhật theo. Khách hàng có Swagger để test. Postman tự import. Code generator (SDK client) tự sinh.

4. **`async def`**: khi có **I/O wait** + library async (DB driver, HTTP client). **`def`**: khi sync only hoặc CPU-bound. Mixed/không chắc: dùng `def` an toàn (FastAPI tự thread pool).

5. `/docs` (Swagger UI), `/redoc` (ReDoc đẹp đọc), `/openapi.json` (raw spec). VD: `http://localhost:8000/docs`.
</details>

---

## ⚡ Cheatsheet

### Cài đặt 1 dòng

```bash
python3 -m venv venv && source venv/bin/activate
pip install "fastapi[standard]"
```

### File `main.py` template

```python
from fastapi import FastAPI

app = FastAPI(title="My API", version="1.0.0")

@app.get("/")
def root():
    return {"hello": "world"}
```

### Run

```bash
fastapi dev main.py              # Dev (auto-reload)
fastapi dev main.py --port 8001  # Custom port
fastapi run main.py              # Production (no reload)
```

### Test

```bash
curl http://localhost:8000/
http://localhost:8000/docs       # Swagger UI
http://localhost:8000/redoc      # ReDoc
http://localhost:8000/openapi.json
```

### Decorator HTTP method

```python
@app.get("/path")     # GET
@app.post("/path")    # POST
@app.put("/path")     # PUT
@app.patch("/path")   # PATCH
@app.delete("/path")  # DELETE
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **FastAPI** | Modern Python web framework — async, type-safe, OpenAPI auto |
| **Starlette** | ASGI framework FastAPI built on top of |
| **Pydantic** | Validation + serialization library (v1 2017, v2 2023) |
| **ASGI** | Async Server Gateway Interface — successor của WSGI |
| **WSGI** | Web Server Gateway Interface — chuẩn cũ sync Python web |
| **uvicorn** | ASGI server phổ biến cho FastAPI |
| **OpenAPI** | Spec chuẩn mô tả REST API (tên cũ: Swagger) |
| **Swagger UI** | Web UI interactive cho OpenAPI |
| **ReDoc** | Web UI đẹp cho OpenAPI (read-only docs) |
| **Type hint** | Python annotation `x: int`, `def f() -> str:` |
| **Decorator** | `@app.get("/path")` — biến function thành route handler |
| **Async/await** | Python coroutine — concurrency không cần thread |
| **Dependency Injection** | Truyền dependency vào function tự động (FastAPI `Depends()`) |

---

## 🔗 Links

### Trong cluster
- → Tiếp: [Routes & Parameters](01_routes-and-parameters.md)
- ↑ Cluster: [python-fastapi README](../../README.md)

### Cross-reference
- [HTTP methods](../../../../05_Networking/http-https/lessons/01_basic/01_http-methods.md) — FastAPI decorator dùng đúng method
- [HTTP status codes](../../../../05_Networking/http-https/lessons/01_basic/02_http-status-codes.md) — return đúng code (201, 204, 400, ...)
- [REST API concepts](../../../../05_Networking/http-https/lessons/01_basic/05_rest-api-concepts.md) — FastAPI design RESTful
- [SQL fundamentals](../../../../06_Databases/sql-fundamentals/) — bài 03 sẽ tích hợp DB

### External
- 📖 [FastAPI official docs](https://fastapi.tiangolo.com/) — tutorial dài, chất lượng cao nhất
- 📖 [FastAPI source code](https://github.com/tiangolo/fastapi)
- 📖 [Pydantic docs](https://docs.pydantic.dev/)
- 📖 [Starlette docs](https://www.starlette.io/)
- 📖 [TechEmpower benchmark](https://www.techempower.com/benchmarks/) — Python framework performance
- 📖 [Awesome FastAPI](https://github.com/mjhea0/awesome-fastapi) — curated list

---

> 🎯 *Sau bài này bạn có FastAPI Hello World chạy + hiểu Swagger UI tự động. Bài kế tiếp dạy **path/query/body params** + **status codes** + **response models**.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in 2-3 câu trước §1 Superpower + §2 So sánh framework + Chọn cái nào + §3 Python type hints + Pydantic. Fix residue `"bạn"` (name placeholder) → `"Nguyen Van A"`. Thêm Changelog section.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `python-fastapi/` lesson 1/5. Cover: FastAPI là gì + 6 superpower (type hints, Pydantic, OpenAPI, async, DI, performance) + so sánh FastAPI vs Flask vs Django + Pydantic validation + setup uvicorn + Swagger UI tự động.
