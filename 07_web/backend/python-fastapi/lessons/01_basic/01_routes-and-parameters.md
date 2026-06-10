# 🎓 Routes & Parameters — Path, Query, Body trong FastAPI

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [FastAPI là gì](00_what-is-fastapi.md)

> 🎯 *Làm chủ 3 loại parameter: **path** (`/users/{id}`), **query** (`?page=2`), **body** (JSON POST). Plus **header**, **cookie**. Phân biệt 5 loại + control 200/201/204/400 status code + chia router thành nhiều file (APIRouter).*

## 🎯 Sau bài này bạn sẽ

- [ ] Khai báo **path param** với type hint
- [ ] Khai báo **query param** (optional + default)
- [ ] Khai báo **body param** với Pydantic
- [ ] Đọc **header** và **cookie**
- [ ] Validate với `Path()`, `Query()`, `Body()` (regex, min/max)
- [ ] Set **status code** đúng (201 Created, 204 No Content)
- [ ] Raise **HTTPException** đúng cách (400, 404, ...)
- [ ] Chia file routes với **APIRouter** + `include_router()`

---

## Tình huống — Bạn muốn API chuẩn REST đầy đủ

Bạn làm CRUD products. Cần:
- `GET /products` — list, có filter `?category=phone` + paginate `?page=2&limit=20`
- `GET /products/{id}` — get 1 product, return 404 nếu không tồn tại
- `POST /products` — create, body JSON, return 201
- `PUT /products/{id}` — update, body JSON
- `DELETE /products/{id}` — delete, return 204

Bạn viết:

```python
@app.get("/products")
def list_products():
    return products  # Trả 1000 rows, frontend timeout!

@app.get("/products/{id}")
def get_product(id):
    return products[id]  # id là str? int? Crash khi không có
```

Senior chê:
- Thiếu **type hint** → id thành str, lookup sai.
- Không **paginate** → trả 1000 rows.
- Không **404 handler** → exception ra 500.
- Không **status code** đúng cho POST/DELETE.

Bạn ngơ:
- Path param khai báo type ra sao?
- Query param optional?
- 404 raise sao?
- 201/204 set sao?

→ Bài này dạy đầy đủ.

---

## 1️⃣ Path parameter

Path parameter là **biến trong URL path** (vd `/products/42` → id=42). FastAPI tự **convert + validate** dựa vào type hint — không cần gọi `int(request.params.get('id'))` như Flask. Sai type = 422 tự động:

```python
@app.get("/products/{id}")
def get_product(id: int):                # ← type hint → tự convert + validate
    return {"id": id}
```

Test:
```bash
curl http://localhost:8000/products/42       # {"id":42}
curl http://localhost:8000/products/abc      # 422 — id không phải int
```

→ FastAPI **convert string từ URL** → int. Sai = 422 Unprocessable Entity tự động.

### Path validate nâng cao với `Path()`

Để thêm constraint cụ thể (range, regex, required) cho path param, dùng `Path()` từ FastAPI. Sai constraint → 422 với detail rõ ràng. Đây là cách validate sạch nhất, không cần `if/else` thủ công:

```python
from fastapi import Path

@app.get("/products/{id}")
def get_product(
    id: int = Path(..., ge=1, le=10000, title="Product ID")
    #                  ↑ >= 1, <= 10000
):
    return {"id": id}
```

| Constraint | Ý nghĩa |
|---|---|
| `...` (Ellipsis) | Required |
| `ge=1` | Greater or equal |
| `le=10000` | Less or equal |
| `gt`, `lt` | Greater/less than (strict) |
| `regex=r"^\d+$"` | Pattern match |

### Order quan trọng — path /me trước /{id}

**Pitfall kinh điển** với routing: FastAPI match route theo thứ tự khai báo. Nếu `/users/{id}` đặt trước `/users/me`, request `/users/me` sẽ cố convert "me" thành int → fail. Quy tắc: specific trước generic:

```python
@app.get("/users/me")              # ← phải đặt TRƯỚC
def get_me():
    return {"user": "current"}

@app.get("/users/{id}")
def get_user(id: int):
    return {"id": id}
```

→ Nếu đảo, `/users/me` sẽ match `{id}` → cố convert "me" thành int → 422. **Specific trước generic**.

---

## 2️⃣ Query parameter

Mọi param **không trong path** + type không phải Pydantic model = **query param**.

```python
@app.get("/products")
def list_products(
    category: str | None = None,        # ← optional, default None
    page: int = 1,                       # ← default 1
    limit: int = 20,                     # ← default 20
    sort: str = "created_at"
):
    return {
        "category": category,
        "page": page,
        "limit": limit,
        "sort": sort
    }
```

Test:
```bash
curl "http://localhost:8000/products"
# {"category":null,"page":1,"limit":20,"sort":"created_at"}

curl "http://localhost:8000/products?category=phone&page=2"
# {"category":"phone","page":2,"limit":20,"sort":"created_at"}
```

### Query validate với `Query()`

Tương tự `Path()`, FastAPI cung cấp `Query()` để thêm constraint cho query parameters. Đây là cách chuẩn để validate pagination, search filter, sort field:

```python
from fastapi import Query

@app.get("/products")
def list_products(
    q: str | None = Query(None, min_length=3, max_length=50),
    page: int = Query(1, ge=1, le=1000),
    limit: int = Query(20, ge=1, le=100),
    tags: list[str] = Query([])         # ← repeating query: ?tags=a&tags=b
):
    return {"q": q, "page": page, "limit": limit, "tags": tags}
```

→ Query `?q=ab` → 422 (min_length=3). Query `?limit=999` → 422 (le=100).

### Repeating query

URL có thể có **cùng 1 key xuất hiện nhiều lần** (vd `?tags=phone&tags=smartphone`). FastAPI tự gộp thành **list** khi type hint là `list[str]`. Tiện cho multi-select filter:

```bash
curl "http://localhost:8000/products?tags=phone&tags=smartphone"
# {"tags":["phone","smartphone"]}
```

---

## 3️⃣ Body parameter — Pydantic model

```python
from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: int
    category: str | None = None

@app.post("/products")
def create_product(product: ProductCreate):
    # product là instance của ProductCreate, đã validate
    return {"created": product.dict()}
```

Test:
```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"iPhone","price":25000000}'
# {"created":{"name":"iPhone","price":25000000,"category":null}}

curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{"name":"iPhone"}'
# 422 — missing price
```

→ Chi tiết Pydantic model ở [bài 02](02_pydantic-models.md).

### Mix path + body + query

```python
@app.put("/products/{id}")
def update_product(
    id: int,                              # path
    product: ProductCreate,                # body (JSON)
    notify: bool = True                    # query
):
    return {"id": id, "product": product, "notify": notify}
```

```bash
curl -X PUT "http://localhost:8000/products/42?notify=false" \
  -H "Content-Type: application/json" \
  -d '{"name":"iPhone 16","price":30000000}'
```

→ FastAPI tự phân loại:
- Param **trong URL path** → path
- Param **Pydantic model** → body
- Param **scalar** (int/str/bool/...) → query

---

## 4️⃣ Header & Cookie

```python
from fastapi import Header, Cookie

@app.get("/items")
def read_items(
    user_agent: str | None = Header(None),       # ← header User-Agent
    x_api_key: str = Header(...),                 # ← required, header X-API-Key
    session_id: str | None = Cookie(None)         # ← cookie
):
    return {
        "user_agent": user_agent,
        "api_key": x_api_key,
        "session_id": session_id
    }
```

→ Tên Python `user_agent` ↔ HTTP header `User-Agent` (FastAPI tự convert underscore → dash).

---

## 5️⃣ Status code đúng cho từng method

### Set static status

```python
from fastapi import status

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(p: ProductCreate):
    return {"id": 1, "name": p.name}

@app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int):
    # 204 không return body
    return None
```

| Method | Status đúng |
|---|---|
| `GET` | 200 OK |
| `GET` (resource không tồn tại) | 404 Not Found |
| `POST` (create) | **201 Created** |
| `PUT/PATCH` | 200 OK |
| `DELETE` | **204 No Content** (không body) |

→ Status code chi tiết: [bài HTTP status codes](../../../../../05_networking/http-https/lessons/01_basic/02_http-status-codes.md).

### Set dynamic — `Response`

```python
from fastapi import Response, status

@app.get("/products/{id}")
def get_product(id: int, response: Response):
    if id == 999:
        response.status_code = status.HTTP_410_GONE
        return {"error": "Gone"}
    return {"id": id}
```

---

## 6️⃣ HTTPException — raise lỗi chuẩn

```python
from fastapi import HTTPException

@app.get("/products/{id}")
def get_product(id: int):
    product = db.find(id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
            headers={"X-Error": "not-found"}    # optional
        )
    return product
```

Test:
```bash
curl http://localhost:8000/products/999
# HTTP 404
# {"detail":"Product not found"}
```

→ **Đúng cách** trả 4xx/5xx. Đừng `return {"error": "..."}` với status 200!

### Custom error class

```python
class ProductNotFoundError(HTTPException):
    def __init__(self, id: int):
        super().__init__(
            status_code=404,
            detail=f"Product #{id} not found"
        )

@app.get("/products/{id}")
def get_product(id: int):
    p = db.find(id)
    if not p:
        raise ProductNotFoundError(id)
    return p
```

---

## 7️⃣ APIRouter — chia file lớn thành nhiều module

Khi app có 50+ endpoint, không thể nhồi 1 file.

### `app/api/products.py`

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/products",                    # ← tự thêm prefix
    tags=["products"]                      # ← group trong Swagger UI
)

@router.get("/")
def list_products():
    return [...]

@router.get("/{id}")
def get_product(id: int):
    return {"id": id}

@router.post("/", status_code=201)
def create_product():
    ...
```

### `app/api/users.py`

```python
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_me():
    return {"user": "current"}
```

### `app/main.py` — combine

```python
from fastapi import FastAPI
from app.api import products, users

app = FastAPI(title="My API")

app.include_router(products.router)
app.include_router(users.router)
```

→ Endpoints giờ tự động có prefix:
- `GET /products/` (từ `products.router`)
- `GET /users/me` (từ `users.router`)

→ Swagger UI tự group theo `tags`.

---

## 8️⃣ Bạn viết lại API CRUD chuẩn

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# Models
class ProductCreate(BaseModel):
    name: str
    price: int
    category: str | None = None

class Product(ProductCreate):
    id: int

# Fake DB
products_db: list[Product] = []
next_id = 1

# CRUD
@app.get("/products")
def list_products(
    category: str | None = None,
    page: int = 1,
    limit: int = 20
):
    filtered = products_db
    if category:
        filtered = [p for p in filtered if p.category == category]
    start = (page - 1) * limit
    return filtered[start:start + limit]


@app.get("/products/{id}")
def get_product(id: int):
    for p in products_db:
        if p.id == id:
            return p
    raise HTTPException(404, "Product not found")


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(p: ProductCreate):
    global next_id
    new = Product(id=next_id, **p.dict())
    products_db.append(new)
    next_id += 1
    return new


@app.put("/products/{id}")
def update_product(id: int, p: ProductCreate):
    for i, existing in enumerate(products_db):
        if existing.id == id:
            products_db[i] = Product(id=id, **p.dict())
            return products_db[i]
    raise HTTPException(404, "Product not found")


@app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int):
    for i, p in enumerate(products_db):
        if p.id == id:
            products_db.pop(i)
            return
    raise HTTPException(404, "Product not found")
```

→ Đầy đủ CRUD chuẩn REST. Mở `/docs` → có 5 endpoint Swagger sẵn. Test "Try it out".

→ Bài kế tiếp dạy **Pydantic model nâng cao** — `response_model`, nested, validation custom.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Path order sai** → `/users/{id}` đặt trước `/users/me` → `/users/me` bị match `{id}=me` → 422.
2. **Return JSON với status 200 cho lỗi** → `{"error": "..."}` HTTP 200. Sai. Phải `raise HTTPException(404, ...)` để status đúng.
3. **POST không status 201** → return 200 OK. Khác client expectation.
4. **DELETE return body** → 204 No Content **không có body**. Trả body = chuẩn vỡ.
5. **Required field thiếu default** → `def f(id: int = Path(...))` → 422 khi thiếu. Nếu muốn optional: `id: int | None = None`.

---

## 🧠 Tự kiểm tra (Self-check)

1. Phân biệt **path** / **query** / **body** parameter — FastAPI nhận biết qua cái gì?
2. Status code đúng cho POST create + DELETE?
3. Cách raise 404 chuẩn trong FastAPI?
4. Khi nào dùng **`APIRouter`**?
5. Viết endpoint `GET /search?q=...&limit=10`, `q` required, `limit` optional default 10 max 100.

<details>
<summary>Gợi ý đáp án</summary>

1. FastAPI phân loại tự động: nếu name khớp **path** placeholder → path; nếu type là **Pydantic model** → body (JSON); còn lại scalar (int/str/bool/...) → query. Header/Cookie dùng `Header()`/`Cookie()` rõ ràng.

2. **POST create**: `status_code=201` (Created). **DELETE**: `status_code=204` (No Content, không body).

3. `raise HTTPException(status_code=404, detail="...")`. FastAPI trả JSON `{"detail":"..."}` với status 404 chuẩn.

4. Khi app có **nhiều endpoint** + cần **chia file** theo concept (users.py, products.py, orders.py). `APIRouter` có `prefix` + `tags`, sau đó `app.include_router(...)` trong main.py.

5. ```python
   from fastapi import Query

   @app.get("/search")
   def search(
       q: str = Query(..., min_length=1),
       limit: int = Query(10, ge=1, le=100)
   ):
       return {"q": q, "limit": limit}
   ```
</details>

---

## ⚡ Cheatsheet

### 4 loại param

```python
@app.get("/items/{id}")
def f(
    id: int,                                     # path
    q: str = "",                                  # query
    body: ItemModel = Body(...),                  # body (Pydantic)
    auth: str = Header(...)                       # header
):
    ...
```

### Validate

```python
Path(..., ge=1, le=100, regex=r"^\d+$")
Query(None, min_length=3, max_length=50)
```

### Status codes

```python
@app.post("/x", status_code=201)
@app.delete("/x/{id}", status_code=204)
raise HTTPException(404, "Not found")
```

### APIRouter

```python
router = APIRouter(prefix="/products", tags=["products"])
@router.get("/")
def list_(): ...

# main.py
app.include_router(router)
```

### Mọi HTTP method

```python
@app.get(...)     @app.post(...)
@app.put(...)     @app.patch(...)
@app.delete(...)  @app.head(...)
@app.options(...) @app.trace(...)
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Path param** | Param trong URL path (`/items/{id}`) |
| **Query param** | Param sau `?` (`?page=2`) |
| **Body param** | JSON trong request body |
| **Header / Cookie param** | Đọc từ HTTP header / cookie |
| **`Path()` / `Query()` / `Body()`** | Helper validate + metadata |
| **`HTTPException`** | Raise lỗi với status code chuẩn |
| **`APIRouter`** | Router con để chia code thành nhiều file |
| **Status code** | HTTP status (200, 201, 404, ...) |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [FastAPI là gì? — Web framework Python tốc độ + type-safe](00_what-is-fastapi.md)
- ➡️ **Bài tiếp theo:** [Pydantic Models — Validation + Serialization của FastAPI](02_pydantic-models.md)
- ↑ **Về cụm:** [python-fastapi README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [HTTP methods](../../../../../05_networking/http-https/lessons/01_basic/01_http-methods.md)
- [HTTP status codes](../../../../../05_networking/http-https/lessons/01_basic/02_http-status-codes.md)

### 🌐 Tài nguyên tham khảo khác
- 📖 [FastAPI tutorial — Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- 📖 [FastAPI tutorial — Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
- 📖 [FastAPI tutorial — APIRouter](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

---

> 🎯 *Sau bài này bạn viết CRUD đầy đủ chuẩn REST. Bài kế tiếp đi sâu **Pydantic models** — nested, validation custom, separate request/response.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.1.0 (25/05/2026)** — Bổ sung câu dẫn nhập cho §1 Path param + Path validate + Order routing, §2 Query validate + Repeating query. Thêm mục Changelog.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `python-fastapi/` lesson 2/5. Cover: path/query/body parameters + Path/Query validation + repeating query + status codes + response_model + HTTPException + custom response + headers + cookies.
