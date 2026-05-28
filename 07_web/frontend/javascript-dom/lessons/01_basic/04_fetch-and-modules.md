# 🎓 Fetch API & ES Modules — Gọi backend + Code modular

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~17 phút\
> **Prerequisites:** [Events & Async](03_events-and-async.md), [REST API](../../../../05_networking/http-https/lessons/01_basic/05_rest-api-concepts.md)

> 🎯 *Master **Fetch API** — GET/POST/PUT/DELETE, JSON body, headers, error handling, abort, retry. Plus **ES modules** — `import/export`, default vs named, dynamic import, tree-shaking. Sau bài này gọi FastAPI từ frontend hoàn chỉnh, code chia file modular.*

## 🎯 Sau bài này bạn sẽ

- [ ] Dùng **`fetch`** — GET / POST / PUT / DELETE
- [ ] Set **headers** + **JSON body**
- [ ] Handle **error đúng cách** (4xx/5xx + network)
- [ ] **Abort** fetch với AbortController + **timeout**
- [ ] **Retry** logic với exponential backoff
- [ ] **ES Modules** — `import` / `export` (default + named)
- [ ] **Dynamic import** — lazy load module
- [ ] Hiểu **tree-shaking** + bundle optimization

---

## Tình huống — bạn fetch FastAPI nhưng lỗi không hiển thị

Bạn viết code call FastAPI backend:

```javascript
fetch('http://localhost:8000/users/999')
  .then(res => res.json())
  .then(user => console.log(user));
// User 999 không tồn tại → backend trả 404
// → Console log: { detail: "User not found" }
// bạn tưởng SUCCESS
```

Bạn thử POST:
```javascript
fetch('/users', {
  method: 'POST',
  body: { name: 'bạn' }   // ← BUG: object không stringify
});
// → Backend nhận body lạ
```

Senior chỉ:
> *"`fetch` có gotcha: response 404/500 KHÔNG reject Promise — chỉ network error mới reject. Phải check `res.ok` thủ công. Plus body POST phải JSON.stringify. Plus headers Content-Type. Plus error handling đầy đủ."*

→ Bài này dạy fetch + modules đầy đủ.

---

## 1️⃣ `fetch` cơ bản — GET request

`fetch` là API hiện đại (2015+) để gọi HTTP request — thay thế `XMLHttpRequest` cũ. Trả về **Promise** → có thể dùng `.then()` chain hoặc `async/await`. GET request đơn giản nhất chỉ cần URL:

```javascript
fetch('https://api.acmeshop.vn/products')
  .then(res => res.json())
  .then(products => console.log(products));
```

### Với async/await (recommended)

`.then()` chain dễ thành "promise hell" khi nhiều bước. **`async/await`** (ES2017) viết được phẳng như code đồng bộ — đây là pattern chuẩn 2026:

```javascript
async function loadProducts() {
  const res = await fetch('https://api.acmeshop.vn/products');
  const products = await res.json();
  return products;
}
```

### `Response` object

`fetch` trả về `Response` object — không phải JSON ngay. Phải gọi method (`json()`, `text()`, `blob()`) để parse body. Object có nhiều property hữu ích: status, headers, url, ok flag:

```javascript
const res = await fetch(url);

res.ok                      // true nếu status 200-299
res.status                   // 200, 404, 500, ...
res.statusText               // "OK", "Not Found", ...
res.headers                  // Headers object
res.headers.get('content-type')

res.url                       // Final URL (after redirect)
res.redirected                 // true if redirected

// Body parsers (chỉ chạy 1 lần)
await res.json()              // → parsed JSON
await res.text()               // → string
await res.blob()               // → Blob (binary, image)
await res.arrayBuffer()        // → ArrayBuffer
await res.formData()           // → FormData
```

→ Body methods **consume stream** — chỉ gọi 1 lần.

---

## 2️⃣ Handle error đúng cách — **GOTCHA QUAN TRỌNG**

### ❌ `fetch` KHÔNG reject với 4xx/5xx

**Bug số 1** mọi beginner gặp với `fetch` — khác `axios` hay jQuery `$.ajax`, `fetch` KHÔNG throw cho HTTP error status (404/500). Phải tự check `res.ok`. Ví dụ "tưởng OK nhưng thực ra fail":

```javascript
const res = await fetch('/users/999');
const data = await res.json();
console.log(data);    // { detail: "Not found" } — bạn tưởng OK
```

→ `fetch` chỉ reject khi **network fail** (CORS, offline, DNS). Status 404/500 vẫn resolve.

### ✅ Check `res.ok` explicit

Solution chuẩn: luôn check `res.ok` (true với 2xx) trước khi parse body. Throw error tự để code outer có thể catch. Đây là helper bạn nên wrap mọi fetch call:

```javascript
async function fetchUser(id) {
  const res = await fetch(`/users/${id}`);

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

// Use
try {
  const user = await fetchUser(999);
} catch (err) {
  console.error(err.message);    // "User not found"
}
```

### Phân biệt 3 loại lỗi

```javascript
try {
  const res = await fetch(url);

  if (!res.ok) {
    // HTTP error (4xx/5xx)
    if (res.status === 404) throw new NotFoundError();
    if (res.status === 401) throw new UnauthorizedError();
    if (res.status >= 500) throw new ServerError();
    throw new Error(`HTTP ${res.status}`);
  }

  return await res.json();
} catch (err) {
  if (err.name === 'TypeError') {
    // Network error (offline, CORS, DNS)
    console.error('Network failed:', err);
  } else if (err.name === 'SyntaxError') {
    // Response không phải JSON valid
    console.error('Invalid JSON');
  } else {
    // App error
    console.error(err);
  }
}
```

---

## 3️⃣ POST / PUT / PATCH — Gửi data

### JSON body

```javascript
async function createUser(data) {
  const res = await fetch('/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify(data)        // ← QUAN TRỌNG: stringify
  });
  if (!res.ok) throw new Error('Failed');
  return res.json();
}

// Use
const user = await createUser({
  name: 'bạn',
  email: 'nguyenvana@ex.com'
});
```

→ **Pitfall**: nếu để `body: data` (object), browser gửi `[object Object]`. **Luôn `JSON.stringify`**.

### Form data — multipart (file upload)

```javascript
const form = document.querySelector('form');
const formData = new FormData(form);

fetch('/upload', {
  method: 'POST',
  body: formData                   // ← KHÔNG set Content-Type — browser tự multipart/form-data với boundary
});
```

→ FormData auto handle multipart. **Đừng tự set `Content-Type`**.

### URL-encoded form (legacy)

```javascript
const params = new URLSearchParams({ key: 'value', x: 1 });

fetch('/api', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: params
});
```

→ Hiếm dùng. FastAPI OAuth2 `/token` endpoint cần dạng này ([bài auth FastAPI](../../../backend/python-fastapi/lessons/01_basic/04_auth-and-middleware.md)).

### PUT / PATCH / DELETE

```javascript
// PUT — replace
await fetch(`/users/${id}`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
});

// PATCH — partial update
await fetch(`/users/${id}`, {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'new@ex.com' })
});

// DELETE
const res = await fetch(`/users/${id}`, { method: 'DELETE' });
// Response thường không body (204 No Content)
```

---

## 4️⃣ Headers — Authentication

### Bearer token (JWT)

```javascript
async function authedFetch(url, options = {}) {
  const token = localStorage.getItem('access_token');

  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
    }
  });
}

// Use
const res = await authedFetch('/users/me');
```

### Custom headers

```javascript
fetch(url, {
  headers: {
    'X-Request-ID': crypto.randomUUID(),
    'Accept-Language': 'vi-VN',
    'Cache-Control': 'no-cache',
  }
});
```

→ Một số header **reserved** (Origin, Host, Cookie) browser tự set, KHÔNG cho override.

---

## 5️⃣ Abort + Timeout

### `AbortController` — Cancel fetch

```javascript
const controller = new AbortController();

const res = await fetch('/big-data', {
  signal: controller.signal
});

// Cancel from elsewhere
button.addEventListener('click', () => controller.abort());

// Handle abort
try {
  await fetch(url, { signal: controller.signal });
} catch (err) {
  if (err.name === 'AbortError') {
    console.log('Cancelled');
  }
}
```

### Timeout pattern

```javascript
function fetchWithTimeout(url, ms = 5000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), ms);

  return fetch(url, { signal: controller.signal })
    .finally(() => clearTimeout(timeoutId));
}

// Use
try {
  const res = await fetchWithTimeout('/slow-api', 3000);
} catch (err) {
  if (err.name === 'AbortError') {
    console.log('Timed out');
  }
}
```

→ Modern (2024+): `AbortSignal.timeout(ms)`:
```javascript
fetch(url, { signal: AbortSignal.timeout(5000) });
```

---

## 6️⃣ Retry với exponential backoff

```javascript
async function fetchRetry(url, options = {}, retries = 3) {
  for (let i = 0; i <= retries; i++) {
    try {
      const res = await fetch(url, options);
      if (res.ok) return res;
      if (res.status >= 500 && i < retries) {
        // Server error — retry
        await sleep(2 ** i * 1000);    // 1s, 2s, 4s
        continue;
      }
      throw new Error(`HTTP ${res.status}`);
    } catch (err) {
      if (i === retries) throw err;
      await sleep(2 ** i * 1000);
    }
  }
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}
```

→ Retry chỉ với:
- **Network error** (TypeError).
- **5xx** (server fault).
- **NOT** 4xx (client fault, retry vô nghĩa).

---

## 7️⃣ ES Modules — `import` / `export`

### Cũ — Mọi script global scope

```html
<script src="utils.js"></script>     <!-- Define global fn -->
<script src="app.js"></script>        <!-- Use global -->
```

→ **Pollute global** namespace. Conflict tên. Khó manage dependencies.

### Modern — ES Modules

```html
<script type="module" src="app.js"></script>
```

```javascript
// utils.js — EXPORT
export function add(a, b) { return a + b; }
export const PI = 3.14;
export default function main() { ... }    // default export

// app.js — IMPORT
import main, { add, PI } from './utils.js';
//      ↑     ↑ named
//      default

console.log(add(1, 2));    // 3
main();
```

→ Mỗi module **scope riêng**. Chỉ export được dùng ngoài.

### Export styles

```javascript
// Named export — multiple per file
export const x = 5;
export function f() {}
export class C {}

// Default export — 1 per file
export default function main() {}
// OR
function main() {}
export default main;

// Re-export
export { foo } from './foo.js';
export * from './bar.js';
```

### Import styles

```javascript
import default_thing from './file.js';
import { named1, named2 } from './file.js';
import default_thing, { named1 } from './file.js';
import * as everything from './file.js';      // namespace
import { named1 as alias } from './file.js';   // rename

// Side-effect only (load module, no import)
import './styles.js';
```

### Naming convention

| Export | File name | Import |
|---|---|---|
| `export default Button` | `Button.js` (PascalCase) | `import Button from './Button.js'` |
| `export const formatDate` | `utils.js` | `import { formatDate } from './utils.js'` |

→ Convention: default cho **main thing** (1 component, 1 class). Named cho utilities (nhiều helpers).

### File extension

```javascript
import './utils.js'       // ✅ Browser require explicit `.js`
import './utils'           // ❌ Browser fail (Node has loose resolve)
```

→ **Browser bắt buộc `.js`** trong path. Node + bundlers thường nới lỏng.

---

## 8️⃣ Dynamic import — Lazy load

```javascript
// Static — load lúc parse
import { heavy } from './heavy.js';

// Dynamic — load on-demand
async function lazyLoad() {
  const module = await import('./heavy.js');
  module.heavy();
}

button.addEventListener('click', lazyLoad);
```

→ Use case:
- **Route-based code splitting** (chỉ load page user mở).
- **Heavy library** chỉ load khi click feature.
- **Conditional dependency** (chỉ load nếu cần).

```javascript
// Conditional import
if (user.isAdmin) {
  const adminTools = await import('./admin.js');
  adminTools.init();
}
```

---

## 9️⃣ Tree-shaking + Bundle optimization

### Tree-shaking — Loại bỏ unused export

```javascript
// utils.js
export function used() { ... }
export function unused() { ... }

// app.js
import { used } from './utils.js';
used();
```

→ Bundler (Vite/Webpack) **detect** `unused` không được import → loại bỏ khỏi bundle.

### Default vs Named export — Impact

```javascript
// ❌ Default export khó tree-shake
export default { used, unused };

// ✅ Named exports — better tree-shaking
export { used, unused };
```

→ **2026 preference**: named exports cho utility/library files.

### Bundle size analysis

```bash
npx vite-bundle-visualizer        # Visualize bundle
npx source-map-explorer dist/**/*.js
```

→ Detect "tại sao bundle nặng 2MB" — thường là 1 lib import full namespace.

```javascript
// ❌ Tải toàn Lodash (~70KB)
import _ from 'lodash';
_.debounce(...);

// ✅ Chỉ debounce (~3KB)
import debounce from 'lodash/debounce';
```

---

## 1️⃣0️⃣ bạn ghép full app — Frontend gọi FastAPI

### `api.js`

```javascript
// API client module
const BASE_URL = 'http://localhost:8000';

async function request(path, options = {}) {
  const token = localStorage.getItem('access_token');

  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }

  return res.status === 204 ? null : res.json();
}

export const api = {
  // Auth
  login: (email, password) => {
    const form = new URLSearchParams({ username: email, password });
    return fetch(`${BASE_URL}/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form,
    }).then(r => r.json());
  },

  // Users
  getMe: () => request('/users/me'),
  getUsers: () => request('/users'),
  getUser: id => request(`/users/${id}`),
  createUser: data => request('/users', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  updateUser: (id, data) => request(`/users/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(data),
  }),
  deleteUser: id => request(`/users/${id}`, { method: 'DELETE' }),

  // Products
  getProducts: () => request('/products'),
};
```

### `app.js`

```javascript
import { api } from './api.js';

const list = document.querySelector('#products');
const form = document.querySelector('#login');
const search = document.querySelector('#search');

// Login
form.addEventListener('submit', async e => {
  e.preventDefault();
  const fd = new FormData(form);
  try {
    const { access_token } = await api.login(fd.get('email'), fd.get('password'));
    localStorage.setItem('access_token', access_token);
    alert('Logged in!');
  } catch (err) {
    alert('Login failed: ' + err.message);
  }
});

// Load products
async function loadProducts() {
  list.textContent = 'Loading...';
  try {
    const products = await api.getProducts();
    list.innerHTML = products.map(p =>
      `<li>${p.name} — ${p.price.toLocaleString()}đ</li>`
    ).join('');
  } catch (err) {
    list.textContent = `Error: ${err.message}`;
  }
}

// Debounce search
const debouncedSearch = debounce(async query => {
  // ... call api.getProducts(query)
}, 300);

search.addEventListener('input', e => debouncedSearch(e.target.value));

function debounce(fn, ms) {
  let id;
  return (...args) => {
    clearTimeout(id);
    id = setTimeout(() => fn(...args), ms);
  };
}

loadProducts();
```

### `index.html`

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>bạn Shop</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <form id="login">
    <input name="email" type="email" required>
    <input name="password" type="password" required>
    <button>Login</button>
  </form>

  <input id="search" placeholder="Search...">
  <ul id="products"></ul>

  <script type="module" src="./app.js"></script>
</body>
</html>
```

→ Full-stack hoàn chỉnh! Frontend (HTML+CSS+JS) gọi FastAPI backend Bạn viết. Modular code, proper error handle.

---

## ⚠️ 5 pitfall hay vướng

1. **`fetch` không reject 4xx/5xx** — must check `res.ok`. 90% beginner lỗi này.
2. **POST không `JSON.stringify`** — gửi `[object Object]`. Always stringify object body.
3. **Set Content-Type cho FormData** — browser muốn tự handle boundary. Để browser tự.
4. **Default export everywhere** → khó tree-shake + named import inconsistent. Use named cho utility.
5. **Static import file lớn** → bundle bloat. Dynamic import cho heavy code.

---

## ✅ Self-check

1. `fetch('/missing')` trả 404 — `.then()` chạy hay `.catch()`?
2. POST JSON body — 2 thứ phải có?
3. Cancel fetch khi user click hủy — pattern?
4. Khác **named export** và **default export**?
5. Khi nào dùng **dynamic import** thay static?

<details>
<summary>Gợi ý đáp án</summary>

1. **`.then()` chạy** — `fetch` chỉ reject khi network error. 404/500 = Response object với `res.ok = false`. Phải check `res.ok` thủ công + throw.

2. (a) **`'Content-Type': 'application/json'`** header. (b) **`body: JSON.stringify(data)`** — không stringify thì gửi `[object Object]`.

3. **`AbortController`**:
   ```javascript
   const controller = new AbortController();
   fetch(url, { signal: controller.signal });
   cancelBtn.onclick = () => controller.abort();
   ```

4. **Named** = nhiều exports/file (`export const a, b, c`), import explicit `{ a, b }`. **Default** = 1 per file (`export default Btn`), import `Btn`. Named tốt cho tree-shake. Default cho "main thing" của file.

5. Khi: (a) **Route-based** — load page chỉ khi navigate đến. (b) **Heavy lib** — chỉ load khi click feature. (c) **Conditional** — chỉ admin cần load admin tools. Static = mọi file load lúc parse.
</details>

---

## ⚡ Cheatsheet

### Fetch

```javascript
// GET
const res = await fetch(url);
if (!res.ok) throw new Error(`HTTP ${res.status}`);
const data = await res.json();

// POST JSON
fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
});

// POST FormData (file upload)
fetch(url, { method: 'POST', body: formData });   // No Content-Type!

// Auth header
fetch(url, { headers: { Authorization: `Bearer ${token}` } });

// Abort
const ctrl = new AbortController();
fetch(url, { signal: ctrl.signal });
ctrl.abort();

// Timeout (modern)
fetch(url, { signal: AbortSignal.timeout(5000) });
```

### Modules

```javascript
// Named
export const x = 5;
export function f() {}
import { x, f } from './file.js';

// Default
export default Component;
import Component from './file.js';

// Combine
import Default, { named } from './file.js';

// Re-export
export { foo } from './a.js';
export * from './b.js';

// Dynamic
const mod = await import('./heavy.js');
```

### Error handling

```javascript
try {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return await res.json();
} catch (err) {
  if (err.name === 'AbortError') ...
  if (err.name === 'TypeError') ...   // network
  console.error(err);
}
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **`fetch`** | Modern API gửi HTTP request |
| **`Response`** | Object trả từ fetch — `.ok`/`.status`/`.json()`/... |
| **`AbortController`** | Cancel fetch / event listener |
| **`AbortSignal.timeout(ms)`** | Modern timeout (2024+) |
| **`FormData`** | Multipart form serialization |
| **`URLSearchParams`** | URL-encoded form |
| **ES Module** | `<script type="module">` — `import/export` scoped |
| **Named export** | Multiple per file |
| **Default export** | 1 per file |
| **Dynamic import** | `await import(...)` lazy load |
| **Tree-shaking** | Bundler remove unused exports |
| **Code splitting** | Bundle thành nhiều chunks, load on-demand |

---

## 🔗 Links

### Trong cluster
- ← Trước: [Events & Async](03_events-and-async.md)
- ↑ Cluster: [javascript-dom README](../../README.md)

### Cross-reference
- [REST API concepts](../../../../05_networking/http-https/lessons/01_basic/05_rest-api-concepts.md) — backend Bạn gọi
- [HTTP methods](../../../../05_networking/http-https/lessons/01_basic/01_http-methods.md)
- [HTTP headers](../../../../05_networking/http-https/lessons/01_basic/03_http-headers.md) — CORS, Auth
- [FastAPI auth](../../../backend/python-fastapi/lessons/01_basic/04_auth-and-middleware.md)

### External
- 📖 [MDN — Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- 📖 [MDN — ES Modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
- 📖 [javascript.info — Fetch](https://javascript.info/fetch)
- 📖 [Bundlephobia](https://bundlephobia.com/) — check npm package size

---

> 🎯 *Cluster javascript-dom basic 5/5 đóng. Bạn build full-stack app vanilla JS + FastAPI. Bài kế tiếp ngoài cluster: **React** (`react/`) — component-based + state management.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in 2-3 câu trước §1 fetch GET + async/await + Response object + §2 fetch không reject 4xx + Check res.ok. Thêm Changelog section.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `javascript-dom/` lesson 5/5. Cover: fetch API (GET/POST/PUT/DELETE) + async/await + Response object + error handling (gotcha 4xx/5xx) + JSON body + FormData + AbortController cancel + ES modules (import/export) + tree-shaking.
