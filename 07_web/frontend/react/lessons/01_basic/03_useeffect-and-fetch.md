# 🎓 useEffect & Fetch — Side effects + Real data

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [State & Events](02_state-and-events.md), [Fetch API](../../../javascript-dom/lessons/01_basic/04_fetch-and-modules.md)

> 🎯 *Master **`useEffect`** — side effect lifecycle, **dependency array**, **cleanup**, **fetch data** từ FastAPI, **loading + error** states, **AbortController** cleanup, **custom hooks** intro. Sau bài này React app dùng data thật từ backend.*

## 🎯 Sau bài này bạn sẽ

- [ ] Dùng **`useEffect`** đúng cách
- [ ] Hiểu **dependency array** (3 patterns: `[]`, `[deps]`, không có)
- [ ] **Cleanup function** — unmount + before re-run
- [ ] **Fetch data** với loading/error state
- [ ] **AbortController** cleanup khi unmount
- [ ] **Custom hook** — extract reusable logic
- [ ] Hiểu **why `useEffect` runs twice** (StrictMode)
- [ ] Avoid **infinite loop** (common bug)

---

## Tình huống — bạn fetch FastAPI lần đầu trong React

Bạn muốn fetch products từ FastAPI hiển thị:

```jsx
function App() {
  const [products, setProducts] = useState([]);

  fetch('/api/products')
    .then(r => r.json())
    .then(setProducts);

  return <ul>{products.map(p => <li>{p.name}</li>)}</ul>;
}
```

→ **Vô tận**:
1. Render → fetch → setProducts → re-render.
2. Re-render → fetch lại → setProducts → re-render.
3. Loop... server crash.

Bạn ngơ:
- Sao fetch **mọi lần render**?
- Tại sao **infinite loop**?
- Loading state hiển thị thế nào?

Senior chỉ:
> *"Fetch là **side effect** — phải dùng **`useEffect`** với **dependency array**. Empty `[]` = chỉ fetch lúc mount. Plus handle loading/error đầy đủ."*

→ Bài này dạy useEffect + fetch đúng cách.

---

## 1️⃣ `useEffect` cơ bản

### Cú pháp

`useEffect` nhận **2 argument**: callback function (side effect) + dependency array. Array quyết định **khi nào** effect chạy. Đây là hook quan trọng thứ 2 sau `useState`:

```jsx
import { useEffect } from 'react';

useEffect(() => {
  // Side effect code
  console.log('Effect ran');
}, [dependencies]);    // ← Dependency array
```

### 3 patterns

Tùy dependency array, useEffect có **3 hành vi khác nhau** — không array, empty array, có deps. Hiểu để pick đúng — sai pattern là source bug "infinite re-render":

```jsx
// 1. KHÔNG có array — chạy SAU MỖI render
useEffect(() => {
  console.log('Every render');
});

// 2. Empty array [] — chạy 1 lần sau MOUNT
useEffect(() => {
  console.log('Once on mount');
}, []);

// 3. [deps] — chạy sau mount + khi deps đổi
useEffect(() => {
  console.log(`Count changed: ${count}`);
}, [count]);
```

### Khi nào dùng?

Bảng quick reference cho 4 use case phổ biến — pick đúng dependency array tránh bug. Quy tắc vàng: cứ value nào dùng trong effect → cho vào array (ESLint plugin `react-hooks` enforce):

| Use case | Dependency |
|---|---|
| Fetch data lúc mount | `[]` |
| Subscribe event/socket | `[]` + cleanup |
| Sync với prop/state | `[prop, state]` |
| Run after every render (rare) | (no array) |

→ **99% case** dùng `[]` hoặc `[deps]`. **Avoid no-array** (gây re-render loop).

---

## 2️⃣ Side effects là gì?

**Side effect** = action **ảnh hưởng bên ngoài** component:

- 📡 **Fetch API**
- 🔌 **Subscribe** (WebSocket, EventSource)
- ⏱️ **setTimeout/setInterval**
- 💾 **localStorage** read/write
- 📊 **Analytics** track
- 🎨 **DOM manipulation** (manual, hiếm)
- 📋 **Document.title** update

→ React render function phải **pure** (cùng input → cùng output, no side effect). Side effect → put trong `useEffect`.

```jsx
// ❌ Side effect trong render body
function App() {
  fetch('/api/data');                    // Lỗi
  document.title = 'New';                 // Lỗi
  localStorage.setItem('key', 'val');     // Lỗi
  return <div>...</div>;
}

// ✅ Side effect trong useEffect
function App() {
  useEffect(() => {
    document.title = 'New';
  }, []);
  return <div>...</div>;
}
```

---

## 3️⃣ Fetch data trong React

### Pattern đầy đủ

Fetch data trong React cần handle **3 state** đồng thời — loading, error, data. Đây là pattern chuẩn 2026 bạn sẽ viết hàng ngày. Try/catch + finally đảm bảo loading luôn được clear:

```jsx
import { useState, useEffect } from 'react';

function ProductList() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchProducts() {
      try {
        setLoading(true);
        setError(null);

        const res = await fetch('/api/products');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setProducts(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchProducts();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <ul>
      {products.map(p => <li key={p.id}>{p.name}</li>)}
    </ul>
  );
}
```

### 3 states quan trọng

Mọi fetch-data component đều phải handle **3 state** này — bỏ sót cái nào là UX kém. Production-grade app coi đây là minimum, không phải nice-to-have:

| State | Khi |
|---|---|
| **Loading** | Đang fetch — show spinner |
| **Error** | Fetch fail — show error message |
| **Success** | Có data — render list |

→ Always handle cả 3. Production app không phép skip loading/error.

### Lỗi thường — async trong useEffect

```jsx
// ❌ useEffect callback KHÔNG được async
useEffect(async () => {
  const res = await fetch('/api');
  // ...
}, []);
// React expect return cleanup function, không phải Promise

// ✅ Wrap async function bên trong
useEffect(() => {
  async function load() {
    const res = await fetch('/api');
    // ...
  }
  load();
}, []);

// ✅ Hoặc IIFE
useEffect(() => {
  (async () => {
    const res = await fetch('/api');
  })();
}, []);
```

---

## 4️⃣ Cleanup function — Quan trọng

useEffect callback có thể return **cleanup function**. Chạy:
1. Trước effect re-run (deps đổi).
2. Khi component unmount.

```jsx
useEffect(() => {
  // Setup
  const id = setInterval(() => {
    console.log('Tick');
  }, 1000);

  // Cleanup
  return () => clearInterval(id);
}, []);
```

→ Without cleanup: component unmount → interval vẫn chạy → **memory leak + bug**.

### Subscribe event với cleanup

```jsx
useEffect(() => {
  const handler = () => {
    console.log('Resize:', window.innerWidth);
  };
  window.addEventListener('resize', handler);

  return () => window.removeEventListener('resize', handler);
}, []);
```

### Subscribe WebSocket

```jsx
useEffect(() => {
  const ws = new WebSocket('wss://api.example.com');
  ws.onmessage = (e) => setMessages(prev => [...prev, e.data]);

  return () => ws.close();
}, []);
```

### Fetch cancel với AbortController

```jsx
useEffect(() => {
  const controller = new AbortController();

  async function load() {
    try {
      const res = await fetch('/api/data', {
        signal: controller.signal
      });
      const data = await res.json();
      setData(data);
    } catch (err) {
      if (err.name !== 'AbortError') {
        setError(err.message);
      }
    }
  }
  load();

  return () => controller.abort();    // Cancel khi unmount/re-run
}, []);
```

→ Production cần cancel — tránh race condition (user navigate away khi response chưa về → setState trên unmounted → warning + bug).

---

## 5️⃣ Dependency array — Common pitfalls

### Missing deps

```jsx
function Search({ query }) {
  const [results, setResults] = useState([]);

  useEffect(() => {
    fetch(`/search?q=${query}`).then(r => r.json()).then(setResults);
  }, []);    // ❌ Missing `query` — chỉ fetch 1 lần, không refetch khi query đổi
}
```

→ Fix: `[query]`. ESLint plugin `react-hooks/exhaustive-deps` catch.

### Object/function deps — re-create mỗi render

```jsx
function App() {
  const config = { url: '/api' };    // ← New object mỗi render

  useEffect(() => {
    fetch(config.url);
  }, [config]);    // ❌ config !== previous config → fetch lại mỗi render!
}
```

→ Fix:
- Move `config` ngoài component (constant).
- Hoặc primitive deps: `[config.url]`.
- Hoặc `useMemo`/`useCallback` (advanced).

### Infinite loop

```jsx
const [items, setItems] = useState([]);

useEffect(() => {
  setItems([...items, 'new']);    // ❌ items change → effect re-run → setItems → loop
}, [items]);
```

→ Fix: dùng functional updater hoặc đổi pattern logic.

---

## 6️⃣ Multiple effects — Tách concern

```jsx
function App() {
  // Effect 1: fetch data
  useEffect(() => {
    fetchData();
  }, []);

  // Effect 2: subscribe WebSocket
  useEffect(() => {
    const ws = new WebSocket(...);
    return () => ws.close();
  }, []);

  // Effect 3: update document title
  useEffect(() => {
    document.title = `${user.name} - App`;
  }, [user.name]);
}
```

→ **Tách multiple effects** thay vì 1 effect lớn. Mỗi effect = 1 concern, dep array riêng.

---

## 7️⃣ Tại sao `useEffect` chạy 2 lần dev?

```jsx
useEffect(() => {
  console.log('Effect');
  return () => console.log('Cleanup');
}, []);

// Console (dev mode, StrictMode):
// Effect
// Cleanup
// Effect       ← Chạy lần 2
```

→ Vì `<StrictMode>` (default Vite/CRA dev) — React **purposely mount/unmount/remount** để **detect bug cleanup**. Production build chạy 1 lần.

### Hệ quả

```jsx
useEffect(() => {
  fetch('/api/data');    // Fetch 2 lần dev (1 lần prod)
}, []);
```

→ Không phải bug. Nếu API expensive/non-idempotent, ensure cleanup hoặc fetch idempotent. Tools:
- TanStack Query (auto cache + dedupe).
- SWR.
- Custom abort controller.

---

## 8️⃣ Custom Hooks — Extract logic

Khi nhiều component dùng cùng logic (fetch, subscribe, ...) → extract custom hook.

### Pattern

```jsx
// hooks/useFetch.js
import { useState, useEffect } from 'react';

function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      try {
        setLoading(true);
        setError(null);
        const res = await fetch(url, { signal: controller.signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();
        setData(json);
      } catch (err) {
        if (err.name !== 'AbortError') setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    load();

    return () => controller.abort();
  }, [url]);

  return { data, loading, error };
}

export default useFetch;
```

### Use

```jsx
import useFetch from './hooks/useFetch';

function ProductList() {
  const { data: products, loading, error } = useFetch('/api/products');

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <ul>
      {products?.map(p => <li key={p.id}>{p.name}</li>)}
    </ul>
  );
}

function UserProfile({ id }) {
  const { data: user, loading } = useFetch(`/api/users/${id}`);
  if (loading) return <p>Loading...</p>;
  return <h2>{user.name}</h2>;
}
```

→ DRY logic across components. **Modern pattern 2026**.

### Quy tắc custom hooks

| Rule | Why |
|---|---|
| **Tên bắt đầu `use*`** | ESLint detect hook rules |
| **Gọi từ component hoặc hook khác** | Hook rules — không từ regular function |
| **Top-level** | Same as built-in hooks |

---

## 9️⃣ bạn fetch FastAPI products

```jsx
// src/hooks/useFetch.js — như §8

// src/App.jsx
import { useState } from 'react';
import useFetch from './hooks/useFetch';

const API_BASE = 'http://localhost:8000';

function ProductList() {
  const { data: products, loading, error } = useFetch(`${API_BASE}/products`);
  const [cart, setCart] = useState([]);

  if (loading) return <p>Đang tải sản phẩm...</p>;
  if (error) return <p style={{color:'red'}}>Lỗi: {error}</p>;

  const addToCart = (p) => setCart(prev => [...prev, p]);

  return (
    <div>
      <h1>🛒 Cart: {cart.length}</h1>
      <ul>
        {products.map(p => (
          <li key={p.id}>
            <h3>{p.name}</h3>
            <p>{p.price.toLocaleString()}đ</p>
            <button onClick={() => addToCart(p)}>Add</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProductList;
```

→ Frontend React gọi FastAPI Bạn viết. Loading/error/success đầy đủ. Custom hook reuse.

### Production tip — TanStack Query

```jsx
import { useQuery } from '@tanstack/react-query';

function ProductList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['products'],
    queryFn: () => fetch('/api/products').then(r => r.json()),
  });
  // Auto cache, dedupe, refetch, stale-while-revalidate
}
```

→ **TanStack Query** = thư viện fetch + cache mạnh nhất 2026. Nhiều startup default.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Fetch trong render body** → infinite loop. Always trong `useEffect`.
2. **Missing dependency** → stale value. Trust ESLint warning. Fix với `[deps]` đúng.
3. **`async` directly trên useEffect callback** → return Promise. Wrap async function bên trong.
4. **No cleanup cho subscribe** → memory leak. Always return cleanup function.
5. **StrictMode 2x effect dev** → tưởng bug. Production 1x. Đảm bảo cleanup idempotent.

---

## 🧠 Tự kiểm tra (Self-check)

1. 3 pattern dependency array — khi nào dùng cái nào?
2. Tại sao fetch trong render body gây infinite loop?
3. Cleanup function chạy khi nào?
4. Sao `useEffect` chạy 2 lần ở dev?
5. Custom hook — quy tắc đặt tên?

<details>
<summary>Gợi ý đáp án</summary>

1. **No array** — chạy sau mỗi render (hiếm dùng, gây re-render loop). **`[]`** — chỉ chạy 1 lần sau mount (fetch initial, subscribe). **`[deps]`** — chạy sau mount + khi deps đổi (sync với prop/state).

2. Render → effect (no useEffect) → setState → re-render → effect chạy lại → setState... infinite. `useEffect` với `[]` chỉ chạy 1 lần mount → break loop.

3. (a) **Trước effect re-run** khi deps đổi. (b) **Khi component unmount**. Use case: clearInterval, removeEventListener, ws.close(), abortController.abort().

4. **StrictMode** (default Vite/CRA dev) **purposely mount/unmount/remount** component để detect bug cleanup. Production chạy 1x. Đảm bảo cleanup function đúng = mọi thứ work cả 2 mode.

5. **`use*`** prefix bắt buộc (ESLint detect hook rules). Plus chỉ gọi từ component/hook khác (không từ regular function). Plus top-level (không condition/loop). Examples: `useFetch`, `useAuth`, `useDebounce`.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### useEffect patterns

```jsx
useEffect(() => { ... });           // every render
useEffect(() => { ... }, []);        // mount only
useEffect(() => { ... }, [dep]);     // mount + dep change

useEffect(() => {
  // setup
  return () => { ... };                // cleanup
}, [deps]);
```

### Fetch with all states

```jsx
const [data, setData] = useState(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
  const ctrl = new AbortController();
  (async () => {
    try {
      setLoading(true);
      const res = await fetch(url, { signal: ctrl.signal });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setData(await res.json());
    } catch (e) {
      if (e.name !== 'AbortError') setError(e.message);
    } finally {
      setLoading(false);
    }
  })();
  return () => ctrl.abort();
}, [url]);
```

### Subscribe

```jsx
useEffect(() => {
  const id = setInterval(fn, 1000);
  return () => clearInterval(id);
}, []);

useEffect(() => {
  window.addEventListener('resize', handler);
  return () => window.removeEventListener('resize', handler);
}, []);
```

### Custom hook

```jsx
function useThing(arg) {
  const [state, setState] = useState();
  useEffect(() => { ... }, [arg]);
  return { state, ... };
}
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **`useEffect`** | Hook for side effects |
| **Side effect** | Action ngoài component (fetch, subscribe, DOM) |
| **Dependency array** | `[deps]` — when effect re-runs |
| **Cleanup function** | Return từ effect, runs before re-run + unmount |
| **AbortController** | Cancel fetch/subscribe |
| **Custom hook** | Reusable hook function `use*` |
| **StrictMode** | Dev wrapper — extra runtime check, double-invoke |
| **TanStack Query / SWR** | Data fetching libraries (cache, dedupe, refetch) |
| **`useRef`** | Hook for DOM ref / mutable value |
| **`useLayoutEffect`** | Like useEffect but sync before paint (rare) |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [State & Events — useState, event handlers, controlled forms](02_state-and-events.md)
- ➡️ **Bài tiếp theo:** [Routing & Context — Multi-page SPA + Global state](04_routing-and-context.md)
- ↑ **Về cụm:** [react README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [Fetch API](../../../javascript-dom/lessons/01_basic/04_fetch-and-modules.md)
- [FastAPI](../../../../backend/python-fastapi/) — backend Bạn gọi

### 🌐 Tài nguyên tham khảo khác
- 📖 [React docs — Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects)
- 📖 [React docs — You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect)
- 📖 [TanStack Query docs](https://tanstack.com/query) — recommended for fetch
- 📖 [SWR docs](https://swr.vercel.app/) — alternative

---

> 🎯 *Sau bài này React bạn dùng data thật từ FastAPI. Bài cuối cluster dạy **routing + context** — multi-page SPA + global state.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `react/` lesson 4/5. Cover: useEffect hook (3 patterns dependency array) + side effects + fetch data pattern (loading/error/success) + cleanup function + race condition + abort controller + custom hooks intro.
- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in 2-3 câu trước §1 useEffect cú pháp + 3 patterns + Khi nào dùng + §3 Pattern đầy đủ + 3 states. Thêm Changelog section.
