# 🎓 Routing & Context — Multi-page SPA + Global state

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Prerequisites:** [useEffect & Fetch](03_useeffect-and-fetch.md)

> 🎯 *Master **React Router v6** — multi-page SPA, route params, navigation. Plus **Context API** — global state without prop drilling. Plus glance **state management library** landscape (Zustand, Redux, Jotai). Sau bài này build SPA hoàn chỉnh nhiều trang.*

## 🎯 Sau bài này bạn sẽ

- [ ] Setup **React Router v6** + cấu trúc routes
- [ ] Dùng **`<Link>`**, **`<NavLink>`**, **`useNavigate`** thay `<a>`
- [ ] **Dynamic route params** + `useParams`
- [ ] **Nested routes** + `<Outlet>`
- [ ] **Protected routes** (auth guard)
- [ ] **Context API** — global state cho theme/user/cart
- [ ] Biết **state management** landscape: Context vs Zustand vs Redux
- [ ] Hiểu **client-side routing** vs **server-side**

---

## Tình huống — Bạn muốn shop có nhiều trang

Bạn có App.jsx 1 trang. Giờ cần:
- `/` — Home (product list)
- `/products/:id` — Detail
- `/cart` — Cart
- `/login` — Login
- `/admin` — Admin (chỉ logged-in user)

Plus:
- **Cart count** hiện trên header — mọi page thấy.
- **Current user** — header + admin page cần.

Bạn thử show/hide thủ công với `useState`:

```jsx
const [page, setPage] = useState('home');
// Render different content based on page
// Click logo → setPage('home')
// Click cart → setPage('cart')
```

→ Hoạt động nhưng:
- 😱 URL không đổi → back button broken, không bookmark được.
- 😱 Cart count phải pass qua 5 component (prop drilling).
- 😱 User info pass khắp nơi.

Senior chỉ:
> *"**React Router** cho multi-page SPA — URL ↔ component map. **Context API** cho global state (cart, user, theme) tránh prop drilling. 2 thứ này là backbone mọi React app production."*

→ Bài này dạy đầy đủ.

---

## 1️⃣ React Router — Setup

### Cài đặt

React core không có routing — phải cài thư viện riêng. **React Router** là default 2026 (~30M downloads/tuần). Một lệnh npm:

```bash
npm install react-router-dom
```

### `src/main.jsx`

Setup React Router cần **wrap App bằng `<BrowserRouter>`** ở entry point. Sau đó mọi component bên trong có thể dùng `<Link>`, `<Routes>`, `useNavigate`, ... Đây là pattern bootstrap chuẩn:

```jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>
);
```

→ `<BrowserRouter>` wrap app. Mọi component bên trong dùng routing được.

### `src/App.jsx`

Trong App, định nghĩa **map giữa URL pattern → component**. Mỗi `<Route>` 1 page. Dynamic param dùng `:name` (vd `/products/:id`). Catch-all `path="*"` cho 404:

```jsx
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import ProductDetail from './pages/ProductDetail';
import Cart from './pages/Cart';
import Login from './pages/Login';
import NotFound from './pages/NotFound';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/products/:id" element={<ProductDetail />} />
      <Route path="/cart" element={<Cart />} />
      <Route path="/login" element={<Login />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
```

→ `path="*"` catch-all 404.

### Pages folder structure

Convention: tách `pages/` (chứa top-level route components) khỏi `components/` (chứa shared components reusable). Structure này scale từ project nhỏ đến enterprise:

```
src/
├── pages/
│   ├── Home.jsx
│   ├── ProductDetail.jsx
│   ├── Cart.jsx
│   ├── Login.jsx
│   └── NotFound.jsx
├── components/
│   ├── Navbar.jsx
│   └── Footer.jsx
└── App.jsx
```

---

## 2️⃣ `<Link>` + `<NavLink>` — Navigate without reload

### `<Link>` — Replace `<a>` cho internal nav

Trong SPA, **KHÔNG dùng `<a href="">`** cho internal nav — sẽ trigger full page reload. React Router cung cấp `<Link>` chỉ update URL + render component mới, no reload:

```jsx
import { Link } from 'react-router-dom';

<Link to="/products">Products</Link>
<Link to="/products/42">Product 42</Link>
<Link to={`/products/${id}`}>View</Link>
```

→ ❌ **KHÔNG dùng** `<a href="/products">` — gây page reload. `<Link>` SPA-friendly.

### `<NavLink>` — Active state

```jsx
import { NavLink } from 'react-router-dom';

<NavLink to="/products" className={({isActive}) => isActive ? 'active' : ''}>
  Products
</NavLink>
```

→ Khi URL match → tự thêm class `active`. Hữu ích navbar highlight current page.

### `useNavigate` — Programmatic navigation

```jsx
import { useNavigate } from 'react-router-dom';

function LoginForm() {
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    await login();
    navigate('/');                        // Redirect home
    // navigate('/cart', { replace: true });  // No back to login
    // navigate(-1);                          // Back
  };
}
```

---

## 3️⃣ Dynamic route params — `useParams`

### Route definition

```jsx
<Route path="/products/:id" element={<ProductDetail />} />
<Route path="/users/:userId/orders/:orderId" element={<Order />} />
```

### Read in component

```jsx
import { useParams } from 'react-router-dom';

function ProductDetail() {
  const { id } = useParams();    // ← from URL /products/42 → id="42"

  const { data: product, loading } = useFetch(`/api/products/${id}`);

  if (loading) return <p>Loading...</p>;
  return <h1>{product.name}</h1>;
}
```

### Query string — `useSearchParams`

```jsx
import { useSearchParams } from 'react-router-dom';

function Search() {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get('q') || '';
  const page = searchParams.get('page') || '1';

  const handleSearch = (newQuery) => {
    setSearchParams({ q: newQuery, page: '1' });
  };

  return (
    <div>
      <input value={query} onChange={e => handleSearch(e.target.value)} />
      <p>Page: {page}</p>
    </div>
  );
}
```

→ URL: `/search?q=phone&page=2`.

---

## 4️⃣ Nested routes + `<Outlet>`

### Use case — Shared layout

```
/products              → ProductList
/products/:id          → ProductDetail
                         + Header + Sidebar (shared)
/products/:id/reviews  → Reviews
                         + ProductDetail layout (shared)
```

### Setup

```jsx
function App() {
  return (
    <Routes>
      {/* Parent layout */}
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Home />} />              {/* / */}
        <Route path="products" element={<ProductLayout />}>
          <Route index element={<ProductList />} />        {/* /products */}
          <Route path=":id" element={<ProductDetail />} /> {/* /products/:id */}
        </Route>
        <Route path="cart" element={<Cart />} />
      </Route>

      <Route path="/login" element={<Login />} />          {/* Bên ngoài layout */}
    </Routes>
  );
}

function MainLayout() {
  return (
    <>
      <Navbar />
      <main>
        <Outlet />              {/* ← Child route render ở đây */}
      </main>
      <Footer />
    </>
  );
}
```

→ `<Outlet>` = nơi child route render. DRY layout.

---

## 5️⃣ Protected route — Auth guard

```jsx
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';

function ProtectedRoute({ children }) {
  const { user } = useAuth();
  const location = useLocation();

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}

// Use
<Route path="/admin" element={
  <ProtectedRoute>
    <AdminPage />
  </ProtectedRoute>
} />
```

### Redirect back after login

```jsx
function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || '/';

  const handleLogin = async () => {
    await login();
    navigate(from, { replace: true });   // Back to original page
  };
}
```

→ Pattern phổ biến: user vào `/admin` chưa login → redirect `/login` → login xong → back về `/admin`.

---

## 6️⃣ Context API — Global state

### Vấn đề — Prop drilling

```jsx
function App() {
  const [user, setUser] = useState(null);
  return <Layout user={user} setUser={setUser} />;
}

function Layout({ user, setUser }) {
  return <Header user={user} setUser={setUser} />;
}

function Header({ user, setUser }) {
  return <UserBadge user={user} setUser={setUser} />;
}

function UserBadge({ user, setUser }) {
  return <p>{user?.name}</p>;
}
```

→ Pass `user` qua 4 level. **Prop drilling**.

### Solution — Context

```jsx
// src/contexts/UserContext.jsx
import { createContext, useContext, useState } from 'react';

const UserContext = createContext(null);

export function UserProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = async (email, password) => {
    const res = await fetch('/api/login', { /* ... */ });
    const data = await res.json();
    setUser(data.user);
  };

  const logout = () => setUser(null);

  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const ctx = useContext(UserContext);
  if (!ctx) throw new Error('useUser must be inside UserProvider');
  return ctx;
}
```

### Wrap app

```jsx
// src/main.jsx
<BrowserRouter>
  <UserProvider>
    <App />
  </UserProvider>
</BrowserRouter>
```

### Use anywhere

```jsx
// src/components/UserBadge.jsx
import { useUser } from '../contexts/UserContext';

function UserBadge() {
  const { user, logout } = useUser();
  if (!user) return null;
  return (
    <>
      <p>{user.name}</p>
      <button onClick={logout}>Logout</button>
    </>
  );
}
```

→ Không prop drilling. Mọi component anywhere truy cập user.

### Multiple contexts

```jsx
<UserProvider>
  <CartProvider>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </CartProvider>
</UserProvider>
```

→ Pattern: 1 context per concern. Tránh "1 context to rule them all" (re-render thừa).

---

## 7️⃣ Context pitfalls + State libraries

### Context pitfall — Re-render

```jsx
const AppContext = createContext({});

function AppProvider({ children }) {
  const [user, setUser] = useState(null);
  const [cart, setCart] = useState([]);
  const [theme, setTheme] = useState('light');

  return (
    <AppContext.Provider value={{ user, setUser, cart, setCart, theme, setTheme }}>
      {children}
    </AppContext.Provider>
  );
}
```

→ `theme` change → mọi component dùng context **re-render** (kể cả không dùng theme).

### Fix — Tách contexts

```jsx
<UserContext.Provider value={{user, setUser}}>
  <CartContext.Provider value={{cart, setCart}}>
    <ThemeContext.Provider value={{theme, setTheme}}>
```

### Khi nào nên dùng state library?

| Need | Tool |
|---|---|
| Local component state | `useState` |
| Few global states (user, theme) | **Context** |
| Many global states + complex updates | **Zustand** (recommended) |
| Time-travel debug, large team | **Redux Toolkit** |
| Atomic state (per-key reactivity) | **Jotai** |
| Server state (cache, refetch) | **TanStack Query** (separate, see [bài 03](03_useeffect-and-fetch.md)) |

### State library landscape 2026

| Library | Year | Bundle | Pros |
|---|---|---|---|
| **Context API** | Built-in | 0 | Native, OK cho 1-2 contexts |
| **Zustand** | 2019 | ~1KB | Tiny + simple + perf — **#1 modern choice** |
| **Redux Toolkit** | 2019 (modernized) | ~12KB | DevTools, time-travel, enterprise |
| **Jotai** | 2020 | ~3KB | Atomic, fine-grained |
| **Recoil** | 2020 (Meta) | ~14KB | Atomic, async — đã dead 2024 |
| **MobX** | 2015 | ~50KB | Reactive, OOP |

→ **2026 default**: **Zustand** cho client state, **TanStack Query** cho server state.

### Glance Zustand

```jsx
import { create } from 'zustand';

const useCartStore = create((set) => ({
  items: [],
  addItem: (item) => set((state) => ({ items: [...state.items, item] })),
  removeItem: (id) => set((state) => ({ items: state.items.filter(i => i.id !== id) })),
  clear: () => set({ items: [] }),
}));

// Use anywhere
function CartBadge() {
  const items = useCartStore(state => state.items);
  return <p>Cart: {items.length}</p>;
}

function AddButton({ product }) {
  const addItem = useCartStore(state => state.addItem);
  return <button onClick={() => addItem(product)}>Add</button>;
}
```

→ No Provider, no boilerplate. Selective subscription (chỉ re-render khi field dùng đổi).

---

## 8️⃣ Bạn viết full SPA shop

```jsx
// src/main.jsx
import { BrowserRouter } from 'react-router-dom';
import { UserProvider } from './contexts/UserContext';
import { CartProvider } from './contexts/CartContext';

createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <UserProvider>
      <CartProvider>
        <App />
      </CartProvider>
    </UserProvider>
  </BrowserRouter>
);
```

```jsx
// src/App.jsx
import { Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="products/:id" element={<ProductDetail />} />
        <Route path="cart" element={<Cart />} />
        <Route path="admin" element={
          <ProtectedRoute>
            <AdminPage />
          </ProtectedRoute>
        } />
      </Route>
      <Route path="/login" element={<Login />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
```

```jsx
// src/components/Layout.jsx
import { Outlet, Link, NavLink } from 'react-router-dom';
import { useUser } from '../contexts/UserContext';
import { useCart } from '../contexts/CartContext';

function Layout() {
  const { user } = useUser();
  const { items } = useCart();

  return (
    <>
      <header>
        <Link to="/">🛒 bạn Shop</Link>
        <nav>
          <NavLink to="/">Home</NavLink>
          <NavLink to="/cart">Cart ({items.length})</NavLink>
          {user?.isAdmin && <NavLink to="/admin">Admin</NavLink>}
          {user ? <span>Hi {user.name}</span> : <Link to="/login">Login</Link>}
        </nav>
      </header>

      <main>
        <Outlet />
      </main>

      <footer>© 2026 bạn Shop</footer>
    </>
  );
}
```

→ Full SPA với routing + context + layout. Production-grade architecture.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **`<a href="/products">`** thay `<Link to="/products">` → page reload, mất state. Always `<Link>`.
2. **Context với mọi state** → re-render thừa. Tách multiple contexts theo concern.
3. **`useContext` ngoài Provider** → returns null/default → bug khó debug. Wrap throw error trong custom hook.
4. **Forget cleanup khi navigate away** → memory leak. Use AbortController trong useEffect.
5. **Tưởng Context = state management** → Context **chỉ pass data**, không optimize re-render. Heavy state → Zustand/Redux.

---

## 🧠 Tự kiểm tra (Self-check)

1. Khác `<a>` và `<Link>` trong React Router?
2. Đọc URL param `/products/42` — code?
3. Khi nào dùng **Context API** vs **Zustand/Redux**?
4. Pattern **Protected Route** — auth guard?
5. `<Outlet>` để làm gì?

<details>
<summary>Gợi ý đáp án</summary>

1. **`<a href>`** — full page reload, mất state SPA, slow. **`<Link to>`** — client-side navigation, URL đổi (history API), không reload, state giữ. **Always `<Link>`** cho internal navigation.

2. ```jsx
   import { useParams } from 'react-router-dom';
   const { id } = useParams();        // "42" (string)
   ```
   Route: `<Route path="/products/:id" element={<ProductDetail />} />`.

3. **Context** OK cho ít global state (user, theme, language). **Zustand/Redux** khi: nhiều state, complex updates, performance critical, time-travel debug. Quy tắc 2026: start Context, migrate Zustand khi đụng pain. **TanStack Query** cho server state (cache fetch).

4. Component wrap:
   ```jsx
   function ProtectedRoute({ children }) {
     const { user } = useAuth();
     const loc = useLocation();
     if (!user) return <Navigate to="/login" state={{from: loc}} replace />;
     return children;
   }
   ```
   Login xong navigate về `loc.state.from`.

5. **`<Outlet>`** = placeholder cho **child route content** trong layout component. Parent route `<MainLayout>` render header/footer + `<Outlet>`. Child routes render vào `<Outlet>` đó. DRY layout shared.
</details>

---

## ⚡ Cheatsheet

### Routing setup

```jsx
import { BrowserRouter, Routes, Route, Link, NavLink, useNavigate, useParams } from 'react-router-dom';

<BrowserRouter>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/users/:id" element={<UserDetail />} />
    <Route path="*" element={<NotFound />} />
  </Routes>
</BrowserRouter>
```

### Hooks

```jsx
const navigate = useNavigate();
navigate('/path');
navigate(-1);                                // back

const { id } = useParams();
const [params, setParams] = useSearchParams();
const location = useLocation();
```

### Nested + protect

```jsx
<Route path="/" element={<Layout />}>          // has <Outlet />
  <Route index element={<Home />} />
  <Route path="cart" element={<Cart />} />
</Route>
<Route path="/admin" element={
  <ProtectedRoute><Admin /></ProtectedRoute>
} />
```

### Context

```jsx
const Ctx = createContext(null);

function Provider({ children }) {
  const [state, setState] = useState();
  return <Ctx.Provider value={{state, setState}}>{children}</Ctx.Provider>;
}

function useThing() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('useThing must be inside Provider');
  return ctx;
}
```

### Zustand

```jsx
const useStore = create((set) => ({
  count: 0,
  inc: () => set(s => ({ count: s.count + 1 })),
}));

const count = useStore(s => s.count);
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **React Router** | Routing library cho React (v6 2021) |
| **SPA** | Single Page Application — JS render frontend |
| **`<BrowserRouter>`** | Wrap app, dùng History API |
| **`<Link>` / `<NavLink>`** | Internal navigation (SPA, no reload) |
| **`useNavigate`** | Programmatic navigation |
| **`useParams`** | Read URL params |
| **`useSearchParams`** | Read query string |
| **`<Outlet>`** | Child route placeholder |
| **Nested routes** | Routes có parent layout share |
| **Protected route** | Wrap component check auth |
| **Context API** | Built-in global state mechanism |
| **`createContext` / `useContext`** | API |
| **Provider** | Component wrap để children dùng context |
| **Prop drilling** | Pass props qua nhiều level (giải bằng context) |
| **Zustand / Redux / Jotai** | State management libraries |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [useEffect & Fetch — Side effects + Real data](03_useeffect-and-fetch.md)
- ↑ **Về cụm:** [react README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [FastAPI auth](../../../../backend/python-fastapi/lessons/01_basic/04_auth-and-middleware.md) — JWT auth backend
- [HTTP headers — CORS](../../../../../05_networking/http-https/lessons/01_basic/03_http-headers.md)

### 🌐 Tài nguyên tham khảo khác
- 📖 [React Router docs](https://reactrouter.com/)
- 📖 [React docs — Passing Data Deeply with Context](https://react.dev/learn/passing-data-deeply-with-context)
- 📖 [Zustand docs](https://zustand-demo.pmnd.rs/)
- 📖 [Redux Toolkit docs](https://redux-toolkit.js.org/)
- 📖 [TanStack Query docs](https://tanstack.com/query)

---

> 🎯 *Cluster React basic 5/5 đóng. Bạn build SPA fullstack: React frontend + FastAPI backend. Bài kế tiếp ngoài cluster: build tools (Vite deep), state management deep, hoặc framework khác.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in 2-3 câu trước §1 React Router Setup (Cài + main.jsx + App.jsx + Pages structure) + §2 Link/NavLink. Thêm Changelog section.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `react/` lesson 5/5. Cover: React Router setup + Routes/Route + dynamic params + Link/NavLink + useNavigate + useParams + nested routes + Context API (createContext + Provider + useContext) + Cart context example.
