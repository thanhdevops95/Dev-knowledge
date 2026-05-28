# 🎓 State & Events — useState, event handlers, controlled forms

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~17 phút\
> **Prerequisites:** [Components & Props](01_components-and-props.md)

> 🎯 *Master **`useState`** — state lifecycle, **event handlers**, **controlled inputs** (form with state), **lifting state up** (share between siblings), **immutable update** (đừng mutate). Sau bài này build cart/form/counter — interactive React app.*

## 🎯 Sau bài này bạn sẽ

- [ ] Dùng **`useState`** đúng cách
- [ ] **Update state immutably** — array + object
- [ ] **Event handlers** (onClick, onChange, onSubmit)
- [ ] **Controlled inputs** — value + onChange
- [ ] **Lifting state up** — share state giữa 2 child component
- [ ] Hiểu **state batching** + **functional updater**
- [ ] **Form submit** + reset
- [ ] Khi nào **multiple state** vs **1 object state**

---

## Tình huống — bạn thêm cart logic

Bài 01 bạn có ProductList. Giờ muốn:
- Click "Add" → product vào cart.
- Cart count hiển thị trên header.
- Form input số lượng có 2-way binding.

Bạn thử:

```jsx
let cart = [];
function App() {
  return (
    <div>
      <p>Cart: {cart.length}</p>
      <button onClick={() => cart.push({id:1})}>Add</button>
    </div>
  );
}
```

→ Click → `cart` đổi nhưng **UI không re-render**. Bạn ngơ.

Senior chỉ:
> *"Variable thường KHÔNG trigger re-render. Phải dùng **state** qua `useState` hook. Plus mutate array (`push`) là anti-pattern — luôn tạo array mới."*

→ Bài này dạy state đầy đủ.

---

## 1️⃣ `useState` — Basic

### Cú pháp

`useState(initialValue)` là hook đầu tiên cần master — trả về **mảng 2 phần tử** dùng destructuring: `[value hiện tại, hàm setter]`. Gọi setter là React re-render component:

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);    // ← [value, setter] = useState(initial)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}
```

→ `useState(initial)` returns `[currentValue, setterFunction]`.
→ Click button → `setCount` → React **re-render component** với value mới.

### Quy tắc Hooks

React Hooks có **2 quy tắc cứng** — vi phạm là crash app. ESLint plugin `react-hooks` sẽ warn nhưng tốt nhất hiểu lý do: React track hook theo **thứ tự gọi**, không theo tên:

```jsx
// ✅ Top-level của component
function App() {
  const [a, setA] = useState(0);
  const [b, setB] = useState('');
  return ...;
}

// ❌ Trong condition / loop / nested function
function App() {
  if (something) {
    const [a, setA] = useState(0);   // Lỗi!
  }
}
```

→ Hooks **phải gọi ở top-level**, **cùng thứ tự mỗi render**. ESLint plugin `react-hooks` catch.

### Multiple state

Với component nhiều giá trị độc lập (form login có email/password/remember), pattern khuyến nghị là **nhiều `useState`** riêng biệt — KHÔNG gom vào 1 object như Vue/Svelte:

```jsx
function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [remember, setRemember] = useState(false);

  return (...);
}
```

→ **OK** nhiều `useState`. Modern React khuyên multiple useState cho independent values.

### Initial value lazy

Khi initial value đến từ **computation tốn** (parse JSON lớn, query localStorage, ...), pass **function** thay vì giá trị — React chỉ gọi 1 lần khi mount, không chạy mỗi render:

```jsx
// ❌ Function chạy mỗi render (expensive)
const [data, setData] = useState(loadFromLocalStorage());

// ✅ Lazy — function chạy 1 lần khi mount
const [data, setData] = useState(() => loadFromLocalStorage());
```

→ Dùng lazy khi initial computation tốn.

---

## 2️⃣ Event handlers

### onClick

React event handler **dùng camelCase** (`onClick`, không `onclick`) và pass **function reference** (không phải string). Pattern phổ biến nhất — định nghĩa handler ngoài JSX cho code clean:

```jsx
function App() {
  const handleClick = () => {
    console.log('Clicked');
  };

  return (
    <>
      {/* Pattern 1: pass function reference */}
      <button onClick={handleClick}>Click</button>

      {/* Pattern 2: inline arrow */}
      <button onClick={() => console.log('Hi')}>Hi</button>

      {/* Pattern 3: pass with args */}
      <button onClick={() => deleteUser(42)}>Delete user 42</button>
    </>
  );
}
```

### ⚠️ Pitfall — Call vs Pass

```jsx
// ❌ Gọi function ngay khi render
<button onClick={handleClick()}>X</button>
// = onClick={returnValueOfHandleClick}  ← Không phải function nữa

// ✅ Pass reference
<button onClick={handleClick}>X</button>

// ✅ Hoặc wrap arrow nếu cần arg
<button onClick={() => handleClick(42)}>X</button>
```

### Event object

```jsx
function App() {
  const handleClick = (event) => {
    console.log(event.target);          // Button element
    console.log(event.type);              // "click"
    event.preventDefault();                // Cancel default
  };

  return <button onClick={handleClick}>Click</button>;
}
```

### Common events

```jsx
<button onClick={fn}>
<input onChange={fn}>
<input onBlur={fn}>
<input onFocus={fn}>
<input onKeyDown={fn}>
<form onSubmit={fn}>
<div onMouseEnter={fn}>
<div onMouseLeave={fn}>
<div onContextMenu={fn}>     // right-click
```

→ All camelCase. React's **synthetic events** wrap native (cross-browser consistent).

---

## 3️⃣ Update state — **IMMUTABLY**

### Number / String / Boolean — Easy

```jsx
const [count, setCount] = useState(0);

setCount(count + 1);
setCount(0);

const [name, setName] = useState('');
setName('bạn');

const [open, setOpen] = useState(false);
setOpen(!open);
setOpen(true);
```

### Array — KHÔNG mutate

```jsx
const [items, setItems] = useState([]);

// ❌ Mutate (no re-render)
items.push({ id: 1, name: 'A' });
items[0].done = true;

// ✅ Tạo array mới
// Add
setItems([...items, newItem]);
setItems(prev => [...prev, newItem]);    // ← functional updater (safer)

// Remove by index
setItems(items.filter((_, i) => i !== indexToRemove));

// Remove by ID
setItems(items.filter(item => item.id !== id));

// Update item
setItems(items.map(item =>
  item.id === id ? { ...item, done: true } : item
));

// Insert at position
setItems([...items.slice(0, i), newItem, ...items.slice(i)]);

// Reorder
setItems([...items].sort((a, b) => a.name.localeCompare(b.name)));
```

### Object — KHÔNG mutate

```jsx
const [user, setUser] = useState({ name: '', email: '', age: 0 });

// ❌ Mutate
user.name = 'bạn';

// ✅ Tạo object mới (spread)
setUser({ ...user, name: 'bạn' });
setUser(prev => ({ ...prev, name: 'bạn' }));

// Update nested
setUser({
  ...user,
  address: { ...user.address, city: 'HN' }
});

// Reset
setUser({ name: '', email: '', age: 0 });
```

### Functional updater — Why important

```jsx
// ❌ Race condition khi update nhanh
setCount(count + 1);
setCount(count + 1);
setCount(count + 1);
// Cả 3 dùng cùng `count`, end = count + 1, không phải count + 3

// ✅ Functional — pass previous value
setCount(prev => prev + 1);
setCount(prev => prev + 1);
setCount(prev => prev + 1);
// Final = count + 3
```

→ **Quy tắc**: nếu **new value depends on previous**, dùng functional updater `setX(prev => ...)`.

---

## 4️⃣ Controlled input — 2-way binding

### Pattern

```jsx
function NameInput() {
  const [name, setName] = useState('');

  return (
    <input
      value={name}                         // ← React quản lý value
      onChange={e => setName(e.target.value)}    // ← Update state khi user gõ
    />
  );
}
```

→ **Controlled** = value của input ← state. React = single source of truth.

### Form đầy đủ

```jsx
function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [remember, setRemember] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log({ email, password, remember });
    // API call here
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        required
      />
      <label>
        <input
          type="checkbox"
          checked={remember}
          onChange={e => setRemember(e.target.checked)}
        />
        Remember me
      </label>
      <button type="submit">Login</button>
    </form>
  );
}
```

| Input type | Read value |
|---|---|
| `text`/`email`/`password`/`textarea` | `e.target.value` |
| `checkbox` | `e.target.checked` |
| `radio` | `e.target.value` (multiple radios) |
| `file` | `e.target.files[0]` |
| `select` | `e.target.value` |

### Generic handler cho nhiều fields

```jsx
function Form() {
  const [form, setForm] = useState({ name: '', email: '', age: 0 });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  return (
    <form>
      <input name="name" value={form.name} onChange={handleChange} />
      <input name="email" value={form.email} onChange={handleChange} />
      <input name="age" type="number" value={form.age} onChange={handleChange} />
    </form>
  );
}
```

→ 1 handler cho mọi input — DRY.

### Uncontrolled — `useRef`

```jsx
import { useRef } from 'react';

function NameInput() {
  const inputRef = useRef(null);

  const handleSubmit = () => {
    console.log(inputRef.current.value);    // Read direct
  };

  return (
    <>
      <input ref={inputRef} defaultValue="bạn" />
      <button onClick={handleSubmit}>Submit</button>
    </>
  );
}
```

→ **Uncontrolled** = browser tự quản lý input value. Read khi cần (refs). Useful cho:
- File input.
- Performance critical (large form, không re-render mỗi keystroke).
- Integrate non-React lib.

→ **Default 2026**: controlled. Uncontrolled niche.

---

## 5️⃣ Lifting state up — Share state giữa siblings

### Problem

```jsx
function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count+1)}>+</button>;
}

function Display() {
  // Làm sao access count?
  return <p>Count: ???</p>;
}

function App() {
  return (
    <>
      <Counter />
      <Display />
    </>
  );
}
```

### Solution — Lift state to nearest common parent

```jsx
function Counter({ count, onIncrement }) {
  return <button onClick={onIncrement}>+ ({count})</button>;
}

function Display({ count }) {
  return <p>Count: {count}</p>;
}

function App() {
  const [count, setCount] = useState(0);    // ← Lift here

  return (
    <>
      <Counter count={count} onIncrement={() => setCount(count + 1)} />
      <Display count={count} />
    </>
  );
}
```

→ **State trong parent**, **pass xuống children** qua props. Children muốn update → callback prop.

### Data flow React = "Top-down"

```
       App (owns count state)
       │
       ├──► count + onIncrement ──► Counter
       │
       └──► count ──────────────► Display
```

→ **One-way data flow**: parent → child. Child không direct modify parent state — chỉ qua callback.

### Khi nhiều level — Context API (bài 04)

Pass props qua nhiều level = **prop drilling**. Solution: **Context** (bài 04).

---

## 6️⃣ State batching

React **gom nhiều setState** trong cùng event handler:

```jsx
function App() {
  const [a, setA] = useState(0);
  const [b, setB] = useState(0);

  const handleClick = () => {
    setA(a + 1);          // ← Schedule update
    setB(b + 1);          // ← Schedule update
    // → React batch → 1 re-render
  };

  console.log('render');     // Chỉ log 1 lần per click
}
```

→ React 18+ **auto batch** mọi update (kể cả async). Optimizes performance.

---

## 7️⃣ Multiple state vs Object state

### Multiple — Recommended cho independent values

```jsx
const [name, setName] = useState('');
const [email, setEmail] = useState('');
const [age, setAge] = useState(0);
```

→ Pros: simpler, partial update easy.

### Object state — Khi values related + thường update cùng

```jsx
const [form, setForm] = useState({
  name: '',
  email: '',
  age: 0,
  errors: {},
  isSubmitting: false
});

setForm(prev => ({ ...prev, name: 'bạn' }));
```

→ Pros: 1 reset, batch update related fields.

### `useReducer` — Khi state phức tạp

```jsx
import { useReducer } from 'react';

function reducer(state, action) {
  switch (action.type) {
    case 'INCREMENT': return { count: state.count + 1 };
    case 'DECREMENT': return { count: state.count - 1 };
    case 'RESET': return { count: 0 };
    default: return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });

  return (
    <>
      <p>{state.count}</p>
      <button onClick={() => dispatch({ type: 'INCREMENT' })}>+</button>
      <button onClick={() => dispatch({ type: 'DECREMENT' })}>-</button>
      <button onClick={() => dispatch({ type: 'RESET' })}>Reset</button>
    </>
  );
}
```

→ `useReducer` = Redux-style trong component. Use khi:
- Complex state transitions.
- Multiple related state pieces.
- Test logic riêng (reducer pure function).

---

## 8️⃣ Bạn viết Cart đầy đủ

```jsx
import { useState } from 'react';
import ProductCard from './components/ProductCard';

const PRODUCTS = [
  { id: 1, name: 'iPhone 15', price: 25000000 },
  { id: 2, name: 'AirPods Pro', price: 5000000 },
  { id: 3, name: 'MacBook Air', price: 28000000 },
];

function App() {
  const [cart, setCart] = useState([]);

  const addToCart = (product) => {
    setCart(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item =>
          item.id === product.id
            ? { ...item, qty: item.qty + 1 }
            : item
        );
      }
      return [...prev, { ...product, qty: 1 }];
    });
  };

  const removeFromCart = (id) => {
    setCart(prev => prev.filter(item => item.id !== id));
  };

  const updateQty = (id, qty) => {
    if (qty <= 0) {
      removeFromCart(id);
      return;
    }
    setCart(prev => prev.map(item =>
      item.id === id ? { ...item, qty } : item
    ));
  };

  const total = cart.reduce((sum, item) => sum + item.price * item.qty, 0);

  return (
    <div>
      <header>
        <h1>bạn Shop</h1>
        <p>🛒 Cart: {cart.length} items — Tổng: {total.toLocaleString()}đ</p>
      </header>

      <main>
        <h2>Sản phẩm</h2>
        <div className="grid">
          {PRODUCTS.map(p => (
            <ProductCard key={p.id} product={p} onAddToCart={addToCart} />
          ))}
        </div>

        <h2>Giỏ hàng</h2>
        {cart.length === 0 ? (
          <p>Chưa có sản phẩm.</p>
        ) : (
          <ul>
            {cart.map(item => (
              <li key={item.id}>
                {item.name} ×
                <input
                  type="number"
                  value={item.qty}
                  onChange={e => updateQty(item.id, parseInt(e.target.value))}
                  min="0"
                  style={{ width: 60 }}
                />
                = {(item.price * item.qty).toLocaleString()}đ
                <button onClick={() => removeFromCart(item.id)}>×</button>
              </li>
            ))}
          </ul>
        )}
      </main>
    </div>
  );
}

export default App;
```

→ Full shopping cart logic ~50 dòng. Immutable updates, controlled input, lifted state. **Real React app**.

→ Bài kế tiếp dạy `useEffect` + fetch FastAPI cho data thật.

---

## ⚠️ 5 pitfall hay vướng

1. **Mutate state** → `arr.push(x)` không trigger re-render. **Always tạo new value**.
2. **`onClick={fn()}`** thay `onClick={fn}` → call ngay render thay vì on click.
3. **`setCount(count + 1)` 3 lần** → batch dùng `count` cũ → +1 thay +3. Functional updater `setCount(prev => prev + 1)`.
4. **Quên `e.preventDefault()` trong onSubmit** → page reload, mất state. Always trong form handler.
5. **State trong loop / condition** → ESLint catch + bug ordering hooks. Always top-level.

---

## ✅ Self-check

1. `useState(0)` returns gì?
2. Update array state — 2 methods chính (add, remove by ID)?
3. Tại sao **functional updater** quan trọng?
4. Controlled input — pattern code?
5. **Lifting state up** giải quyết vấn đề gì?

<details>
<summary>Gợi ý đáp án</summary>

1. `useState(initial)` returns **array `[value, setter]`**. Destructure: `const [count, setCount] = useState(0)`. `value` = current state, `setter` = function update state.

2. **Add**: `setItems([...items, newItem])` hoặc `setItems(prev => [...prev, newItem])`. **Remove by ID**: `setItems(items.filter(i => i.id !== targetId))`. Always tạo array mới (immutable).

3. **Race condition** khi multiple `setState` cùng tick: cả 3 dùng cùng `prevValue` → end = prev+1 (not prev+3). **Functional updater** `setX(prev => prev + 1)` luôn dùng latest value → batch đúng. Use khi new value depends on old.

4. ```jsx
   const [val, setVal] = useState('');
   <input value={val} onChange={e => setVal(e.target.value)} />
   ```
   `value` ← state, `onChange` → update state. 2-way binding.

5. **Share state giữa 2 sibling components**. Sibling A & B đều cần count — đặt state ở **nearest common parent**, pass down qua props (data + callback). One-way data flow React: parent owns state, children request update qua callback.
</details>

---

## ⚡ Cheatsheet

### useState

```jsx
const [value, setValue] = useState(initial);
setValue(newValue);
setValue(prev => newValueFromPrev);

// Lazy initial
useState(() => expensiveCompute());
```

### Immutable updates

```javascript
// Array
[...arr, newItem]                  // add
arr.filter(i => i.id !== id)        // remove
arr.map(i => i.id === id ? {...i, ...changes} : i)   // update
[...arr].sort(...)                   // sort (clone first)

// Object
{...obj, key: value}                // update
const {removed, ...rest} = obj      // remove key
{...obj, nested: {...obj.nested, key: value}}        // nested
```

### Controlled input

```jsx
<input value={state} onChange={e => setState(e.target.value)} />
<input type="checkbox" checked={state} onChange={e => setState(e.target.checked)} />
```

### Event

```jsx
<button onClick={handler}>          // ✅ Pass ref
<button onClick={() => handler(arg)}>   // With arg
<form onSubmit={e => { e.preventDefault(); ... }}>
```

### useReducer

```jsx
const [state, dispatch] = useReducer(reducer, initial);
dispatch({ type: 'ACTION', payload });
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **State** | Component internal data — đổi → re-render |
| **`useState`** | Hook khai báo state |
| **Setter function** | `setState` — update state value |
| **Functional updater** | `setX(prev => ...)` — safe khi depend on prev |
| **Immutable update** | Tạo value mới thay vì mutate |
| **Event handler** | Function chạy khi event fire |
| **Synthetic event** | React's cross-browser event wrapper |
| **Controlled input** | Value managed by React state |
| **Uncontrolled input** | Browser manages, read via ref |
| **Lifting state up** | Move state to nearest common parent |
| **State batching** | React gom multiple setState → 1 re-render |
| **`useReducer`** | Hook cho complex state, Redux-style |
| **`useRef`** | Hook for DOM ref / mutable value not triggering re-render |

---

## 🔗 Links

### Trong cluster
- ← Trước: [Components & Props](01_components-and-props.md)
- → Tiếp: [useEffect & Fetch](03_useeffect-and-fetch.md)
- ↑ Cluster: [react README](../../README.md)

### External
- 📖 [React docs — State: A Component's Memory](https://react.dev/learn/state-a-components-memory)
- 📖 [React docs — Updating Arrays in State](https://react.dev/learn/updating-arrays-in-state)
- 📖 [React docs — Sharing State Between Components](https://react.dev/learn/sharing-state-between-components)
- 📖 [Why React batches state updates](https://github.com/reactwg/react-18/discussions/21)

---

> 🎯 *Sau bài này React app interactive đầy đủ. Bài kế tiếp dạy **useEffect + fetch** — đến với data thật từ FastAPI.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in 2-3 câu trước §1 useState Cú pháp + Quy tắc Hooks + Multiple state + Initial lazy + §2 onClick handler. Thêm Changelog section.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `react/` lesson 3/5. Cover: useState hook (cú pháp + 2 rules + multiple + lazy init) + event handlers (onClick/onChange/onSubmit/onKeyDown) + controlled vs uncontrolled inputs + form pattern + synthetic events.
