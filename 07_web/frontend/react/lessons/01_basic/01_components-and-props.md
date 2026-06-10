# 🎓 Components & Props — Building block của React

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [What is React](00_what-is-react.md)

> 🎯 *Master **function component**, **JSX rules** sâu, **props** (pass data, destructure, default), **children prop**, **conditional render** (`&&`, ternary), **list render** + **key**, **composition pattern**. Sau bài này chia UI thành component reusable.*

## 🎯 Sau bài này bạn sẽ

- [ ] Viết **function component** đúng chuẩn
- [ ] Master **JSX expression** + **conditional** + **list**
- [ ] Pass **props** + destructure + default value
- [ ] Dùng **`children`** prop cho composition
- [ ] **Key** trong list — sao cần, dùng đúng
- [ ] Pass **function** as prop (callback)
- [ ] **Spread props** `<Comp {...props} />`
- [ ] **Container vs Presentational** pattern

---

## Tình huống — Bạn copy-paste card UI 10 lần

Bạn viết product page có 10 product card:

```jsx
function App() {
  return (
    <div>
      <div className="card">
        <img src="iphone.jpg" alt="iPhone" />
        <h3>iPhone 15</h3>
        <p>25,000,000đ</p>
        <button>Mua</button>
      </div>
      <div className="card">
        <img src="airpods.jpg" alt="AirPods" />
        <h3>AirPods Pro</h3>
        <p>5,000,000đ</p>
        <button>Mua</button>
      </div>
      {/* ... 8 lần nữa */}
    </div>
  );
}
```

→ Hard to maintain. Đổi 1 chỗ → đổi 10 chỗ.

Senior chỉ:
> *"Component là **DRY** cho UI. Tách `<ProductCard>`, pass `product` prop. 10 dòng JSX → 1 dòng `<ProductCard product={p} />`."*

→ Bài này dạy component + props đầy đủ.

---

## 1️⃣ Function component

### Cú pháp cơ bản

React 2026 dùng **function component** (không phải class) — đơn giản như function thường, return JSX. Có 3 dạng cú pháp tương đương: function declaration, arrow function, arrow với body block:

```jsx
function Greeting() {
  return <h1>Hello!</h1>;
}

// Arrow alternative
const Greeting = () => <h1>Hello!</h1>;

// Multi-line — wrap ()
const Card = () => (
  <div className="card">
    <h2>Title</h2>
    <p>Body</p>
  </div>
);

// With logic
function Counter() {
  const count = 5;
  const doubled = count * 2;
  return (
    <div>
      <p>Count: {count}</p>
      <p>Doubled: {doubled}</p>
    </div>
  );
}
```

### Quy tắc đặt tên

**Quy tắc cứng**: component tên phải **PascalCase** (chữ đầu viết hoa). Lý do: JSX phân biệt component vs HTML tag qua chữ đầu — `<ProductCard />` = component, `<productcard />` = HTML tag không tồn tại:

```jsx
// ✅ Component — PascalCase
function ProductCard() { ... }
function UserProfile() { ... }
function MyApp() { ... }

// ❌ camelCase — React coi là HTML tag (lowercase)
function productCard() { ... }   // <productCard /> không phải component!
```

→ **PascalCase bắt buộc** cho component. Lowercase = HTML tag.

### File structure

Convention React project: mỗi component **1 file riêng** trong `components/`. Tên file = tên component + `.jsx`. Export default → import dễ. Đây là structure scale từ project nhỏ đến lớn:

```
src/
├── components/
│   ├── ProductCard.jsx       ← Component thường tách file riêng
│   ├── Button.jsx
│   └── Navbar.jsx
├── App.jsx
└── main.jsx
```

```jsx
// src/components/ProductCard.jsx
function ProductCard() {
  return <div className="card">...</div>;
}
export default ProductCard;

// src/App.jsx
import ProductCard from './components/ProductCard';

function App() {
  return <ProductCard />;
}
```

---

## 2️⃣ Props — Data parent → child

### Pass props

Props là **input** của component — pass từ parent xuống child qua **attributes JSX**. Cú pháp: string dùng `"..."`, expression (number/bool/object/function) dùng `{...}`. Component nhận qua first parameter (`props`):

```jsx
function App() {
  return (
    <Greeting name="Nguyen Van A" age={28} isAdmin={true} />
  );
}

function Greeting(props) {
  return (
    <h1>Hello, {props.name}! Age: {props.age}</h1>
  );
}
```

### Destructure props (recommended)

Code clean hơn khi **destructure** ngay ở parameter — không phải gõ `props.name`, `props.age` mỗi lần. Pattern này là default modern React + dễ thêm default value:

```jsx
function Greeting({ name, age, isAdmin }) {
  return (
    <div>
      <h1>Hello, {name}!</h1>
      <p>Age: {age}</p>
      {isAdmin && <p>Admin user</p>}
    </div>
  );
}
```

### Default value

```jsx
function Greeting({ name, age = 0, role = 'guest' }) {
  return <h1>{name} ({role}, {age})</h1>;
}

<Greeting name="Nguyen Van A" />               // age=0, role='guest'
<Greeting name="Nguyen Van A" age={28} />       // age=28, role='guest'
```

### Rest props

```jsx
function Card({ title, ...rest }) {
  console.log(rest);    // { description, image, ... }
  return <div>{title}</div>;
}

<Card title="Hi" description="Body" image="/x.jpg" />
```

### Spread props — Pass through

```jsx
function App() {
  const productProps = { id: 1, name: 'iPhone', price: 25000000 };
  return <ProductCard {...productProps} />;
  // Same as <ProductCard id={1} name="iPhone" price={25000000} />
}
```

→ Useful khi forward many props (e.g., `<Button {...props} />`).

---

## 3️⃣ JSX expressions chi tiết

### Text + variable

```jsx
const name = 'Nguyen Van A';
<h1>Hello, {name}</h1>
<p>Today is {new Date().toLocaleDateString()}</p>
```

### Conditional — Ternary

```jsx
<p>{isLoggedIn ? `Hi ${user.name}` : 'Please login'}</p>
```

### Conditional — `&&` short-circuit

```jsx
{isAdmin && <button>Delete</button>}
{items.length > 0 && <ul>...</ul>}

// ⚠️ Pitfall: 0 render thành "0"
{count && <p>Has count</p>}    // count=0 → renders "0"!

// Fix:
{count > 0 && <p>Has count</p>}
```

### Conditional — Variable

```jsx
function Greeting({ isLoggedIn, user }) {
  let content;
  if (isLoggedIn) {
    content = <p>Welcome, {user.name}</p>;
  } else {
    content = <p>Please login</p>;
  }
  return <div>{content}</div>;
}
```

### Conditional — Early return

```jsx
function Greeting({ isLoggedIn, user }) {
  if (!isLoggedIn) {
    return <p>Please login</p>;
  }
  return <p>Welcome, {user.name}</p>;
}
```

### Conditional — Multiple branches

```jsx
function StatusBadge({ status }) {
  const styles = {
    active: { color: 'green' },
    inactive: { color: 'gray' },
    banned: { color: 'red' },
  };
  return <span style={styles[status]}>{status}</span>;
}
```

---

## 4️⃣ List render với `.map()` + key

### Cơ bản

```jsx
function ProductList({ products }) {
  return (
    <ul>
      {products.map(product => (
        <li key={product.id}>
          {product.name}
        </li>
      ))}
    </ul>
  );
}

const products = [
  { id: 1, name: 'iPhone' },
  { id: 2, name: 'AirPods' },
];
<ProductList products={products} />
```

### **Key prop** — Quan trọng nhất

```jsx
{items.map(item => <li key={item.id}>...</li>)}
```

| Why key? |
|---|
| React dùng `key` để **track items** giữa renders |
| Không key → React giả định order — vỡ khi reorder/filter |
| Performance: re-render chỉ items đổi |

### Quy tắc key

| Practice | OK? |
|---|---|
| **Unique ID stable** (DB id) | ✅ Best |
| **String unique** (slug, email) | ✅ |
| **`key={index}`** | ⚠️ Chỉ khi list **không reorder/insert/delete** |
| **`key={Math.random()}`** | ❌ Mỗi render = key mới → React re-create everything |

```jsx
// ❌ Index key + reorder bug
{items.map((item, i) => <li key={i}>{item.name}</li>)}
// Reorder: item.name đổi nhưng state internal (vd <input>) không follow đúng item

// ✅ Stable ID
{items.map(item => <li key={item.id}>{item.name}</li>)}
```

### Complex list render — Tách thành sub-component

```jsx
// ❌ Inline lớn
function App({ products }) {
  return (
    <div>
      {products.map(p => (
        <div key={p.id} className="card">
          <img src={p.image} alt={p.name} />
          <h3>{p.name}</h3>
          <p>{p.price.toLocaleString()}đ</p>
          <button>Mua</button>
        </div>
      ))}
    </div>
  );
}

// ✅ Tách
function ProductCard({ product }) {
  return (
    <div className="card">
      <img src={product.image} alt={product.name} />
      <h3>{product.name}</h3>
      <p>{product.price.toLocaleString()}đ</p>
      <button>Mua</button>
    </div>
  );
}

function App({ products }) {
  return (
    <div>
      {products.map(p => <ProductCard key={p.id} product={p} />)}
    </div>
  );
}
```

→ Bạn fix 10 product card 10 dòng → tách `ProductCard` component → tái sử dụng.

---

## 5️⃣ `children` prop — Composition

### Pass JSX as children

```jsx
function Card({ children }) {
  return <div className="card">{children}</div>;
}

<Card>
  <h2>Title</h2>
  <p>Body</p>
</Card>

// Same as:
<Card children={<><h2>Title</h2><p>Body</p></>} />
```

### Use cases

```jsx
// Modal
function Modal({ onClose, children }) {
  return (
    <div className="modal-backdrop">
      <div className="modal">
        <button onClick={onClose}>×</button>
        {children}
      </div>
    </div>
  );
}

<Modal onClose={() => setOpen(false)}>
  <h2>Login</h2>
  <LoginForm />
</Modal>

// Layout wrapper
function PageLayout({ title, children }) {
  return (
    <>
      <header><h1>{title}</h1></header>
      <main>{children}</main>
      <footer>© 2026</footer>
    </>
  );
}

<PageLayout title="Acme Shop">
  <ProductList />
</PageLayout>
```

→ **Composition** = key React philosophy. Layout/wrapper component nhận `children` cực phổ thông.

---

## 6️⃣ Pass function as prop (callback)

```jsx
function Button({ onClick, children }) {
  return <button onClick={onClick}>{children}</button>;
}

function App() {
  const handleClick = () => alert('Clicked');

  return (
    <Button onClick={handleClick}>
      Click me
    </Button>
  );
}
```

### Pass data with function

```jsx
function ProductCard({ product, onAddToCart }) {
  return (
    <div>
      <h3>{product.name}</h3>
      <button onClick={() => onAddToCart(product)}>
        Add to cart
      </button>
    </div>
  );
}

function App() {
  const handleAdd = (product) => {
    console.log('Added:', product);
  };

  return <ProductCard product={p} onAddToCart={handleAdd} />;
}
```

### Naming convention

```
onClick    onSubmit    onChange       (DOM events)
onAdd      onRemove    onEdit         (custom — start with "on")
```

→ Quy ước: callback prop bắt đầu với **`on*`** (giống native events).

---

## 7️⃣ Props.children variations

### Single child

```jsx
function Card({ children }) {
  return <div>{children}</div>;
}

<Card>Single text</Card>
<Card><Button /></Card>
```

### Multiple children

```jsx
<Card>
  <h2>Title</h2>
  <p>Body</p>
</Card>

// children là array của 2 element
```

### Render prop pattern

```jsx
function DataFetcher({ url, render }) {
  const data = useFetch(url);    // hypothetical hook
  return render(data);
}

<DataFetcher
  url="/api/users"
  render={data => (
    <ul>{data.map(u => <li key={u.id}>{u.name}</li>)}</ul>
  )}
/>
```

→ Render prop = pass function as child. Flexible but hooks (bài 02) thay thế nhiều.

---

## 8️⃣ Container vs Presentational pattern

### Presentational — Dumb component (chỉ UI)

```jsx
// Pure UI, không fetch, không state — re-usable
function ProductCard({ product, onAddToCart }) {
  return (
    <div className="card">
      <img src={product.image} alt={product.name} />
      <h3>{product.name}</h3>
      <p>{product.price.toLocaleString()}đ</p>
      <button onClick={() => onAddToCart(product)}>Add</button>
    </div>
  );
}
```

### Container — Smart component (data + logic)

```jsx
// Fetch + manage state
function ProductsContainer() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);

  useEffect(() => {
    fetch('/api/products').then(r => r.json()).then(setProducts);
  }, []);

  const handleAdd = product => setCart([...cart, product]);

  return (
    <div>
      {products.map(p => (
        <ProductCard key={p.id} product={p} onAddToCart={handleAdd} />
      ))}
      <p>Cart: {cart.length} items</p>
    </div>
  );
}
```

→ **Separation of concerns**: presentational reusable + container có logic. 2026 pattern này ít chặt chẽ (hooks blur ranh giới), nhưng vẫn là **mental model tốt**.

---

## 9️⃣ Bạn viết product list đúng React

### `src/components/ProductCard.jsx`

```jsx
function ProductCard({ product, onAddToCart }) {
  return (
    <div className="card">
      <img src={product.image} alt={product.name} />
      <h3>{product.name}</h3>
      <p className="price">{product.price.toLocaleString()}đ</p>
      <button onClick={() => onAddToCart(product)}>
        Mua
      </button>
    </div>
  );
}

export default ProductCard;
```

### `src/components/ProductList.jsx`

```jsx
import ProductCard from './ProductCard';

function ProductList({ products, onAddToCart }) {
  if (products.length === 0) {
    return <p>Không có sản phẩm.</p>;
  }

  return (
    <div className="grid">
      {products.map(product => (
        <ProductCard
          key={product.id}
          product={product}
          onAddToCart={onAddToCart}
        />
      ))}
    </div>
  );
}

export default ProductList;
```

### `src/App.jsx`

```jsx
import ProductList from './components/ProductList';

const products = [
  { id: 1, name: 'iPhone 15', price: 25000000, image: '/iphone.jpg' },
  { id: 2, name: 'AirPods Pro', price: 5000000, image: '/airpods.jpg' },
  { id: 3, name: 'MacBook Air', price: 28000000, image: '/macbook.jpg' },
];

function App() {
  const handleAddToCart = product => {
    alert(`Added ${product.name}`);
  };

  return (
    <div>
      <h1>Acme Shop</h1>
      <ProductList products={products} onAddToCart={handleAddToCart} />
    </div>
  );
}

export default App;
```

→ 3 component, separation clean, mỗi component <30 dòng. Add product mới = thêm 1 object. Re-design card = sửa 1 file. **DRY achieved**.

→ Bài kế tiếp dạy `useState` + event để cart thực sự lưu items.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Component lowercase** → React thấy như HTML tag `<productCard />` → render fail. PascalCase.
2. **Quên `key` trong `.map()`** → React warning + bug khi reorder. Always stable ID.
3. **`{count && <p>...</p>}`** với count=0 → render "0" (number falsy nhưng vẫn render). Dùng `count > 0 && ...`.
4. **Mutate props** → React props **immutable**. Tạo state mới nếu muốn modify (bài 02).
5. **Tách component quá sớm** — `<Title>` cho 1 dòng h1 không cần. Tách khi reuse 2+ lần hoặc logic phức tạp.

---

## 🧠 Tự kiểm tra (Self-check)

1. Component đặt tên `productCard` được không? Vì sao?
2. Pass `user` (object) làm prop, child component access `user.name` thế nào?
3. Tại sao cần `key` trong list? `key={index}` OK chưa?
4. `children` prop để làm gì? Use case?
5. Khác **Container** và **Presentational** component?

<details>
<summary>Gợi ý đáp án</summary>

1. **Không** — JSX dùng PascalCase cho component (`<ProductCard />`), lowercase = HTML tag (`<productcard />` → DOM element không tồn tại). Đặt `ProductCard`.

2. Pass: `<UserCard user={userData} />`. Child: `function UserCard({ user }) { return <p>{user.name}</p>; }` (destructure props). Hoặc `props.user.name` (no destructure).

3. **Key** giúp React track item identity giữa renders → diff/patch chính xác. **`key={index}`** OK chỉ khi list **không reorder/insert/delete** (static list). Reorder + index key = state internal (input value) gắn nhầm item. Always stable ID.

4. **`children`** = JSX bên trong `<Component>...</Component>`. Use case: layout wrapper (Modal, Card, PageLayout), composition (slot pattern). React API ngầm — không cần khai báo, chỉ destructure `{ children }`.

5. **Presentational** = pure UI, props in / JSX out, không fetch/state (Button, Card). **Container** = data + logic (fetch, manage state, pass to presentational). Pattern này 2026 ít chặt (hooks blur), nhưng mental model: tách presentation khỏi business logic.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Component

```jsx
function Comp({ prop1, prop2 = 'default', ...rest }) {
  return <div>{prop1}</div>;
}
export default Comp;
```

### JSX patterns

```jsx
{variable}                        // Interpolate
{cond ? <A/> : <B/>}              // Ternary
{cond && <A/>}                    // Short-circuit
{items.map(i => <X key={i.id} item={i}/>)}   // List
<>{multiple} {root}</>            // Fragment
```

### Props patterns

```jsx
<Comp prop="text" num={5} bool flag={false} />
<Comp {...obj} />                 // Spread
<Comp onClick={() => fn(arg)} />   // Callback
```

### Children

```jsx
function Layout({ children }) {
  return <main>{children}</main>;
}
<Layout><Page /></Layout>
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Function component** | Function trả về JSX |
| **Props** | Data từ parent → child (immutable) |
| **`children`** | Special prop — JSX bên trong tag |
| **PascalCase** | `ComponentName` (component, file) |
| **Destructure** | `{ name, age }` extract props |
| **Spread props** | `<C {...obj} />` |
| **Key prop** | Unique ID cho list item |
| **Composition** | Combine component qua children |
| **Container / Presentational** | Smart (logic) / Dumb (UI) pattern |
| **Callback prop** | Function pass từ parent (vd `onClick`) |
| **Render prop** | Function as child — flexible render |
| **Fragment** | `<>...</>` — wrap multi root no extra div |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [React là gì? — Component framework #1 cho frontend](00_what-is-react.md)
- ➡️ **Bài tiếp theo:** [State & Events — useState, event handlers, controlled forms](02_state-and-events.md)
- ↑ **Về cụm:** [react README](../../README.md)

### 🌐 Tài nguyên tham khảo khác
- 📖 [React docs — Your First Component](https://react.dev/learn/your-first-component)
- 📖 [React docs — Passing Props](https://react.dev/learn/passing-props-to-a-component)
- 📖 [React docs — Rendering Lists](https://react.dev/learn/rendering-lists)
- 📖 [Patterns.dev — Composition pattern](https://www.patterns.dev/posts/compound-pattern/)

---

> 🎯 *Sau bài này bạn chia UI thành component. Bài kế tiếp dạy **state + events** — interactive components.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `react/` lesson 2/5. Cover: function component + PascalCase rule + file structure + props (pass + destructure + default value + spread) + children prop + composition pattern + container/presentational.
- **v1.1.0 (25/05/2026)** — Bổ sung lời dẫn trước các mục Cú pháp function component, Quy tắc đặt tên, File structure, Pass props, Destructure props. Chuẩn hoá giá trị ví dụ trong code thành placeholder. Thêm mục Changelog.
