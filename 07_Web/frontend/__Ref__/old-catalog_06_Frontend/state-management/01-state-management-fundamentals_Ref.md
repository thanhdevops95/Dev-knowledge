# ⚛️ State Management — Quản lý trạng thái ứng dụng

> `[INTERMEDIATE]` — Từ React state đến global stores

---

## Tại sao State Management phức tạp?

**State** = data thay đổi theo thời gian. Khi app lớn, bạn gặp 3 vấn đề:

**Vấn đề 1: Prop Drilling** — Truyền state qua 5+ tầng components. Components ở giữa nhận props mà chúng không cần.

**Vấn đề 2: Shared State** — Cart ở Sidebar và Header cùng cần `cartItems`. Mỗi component giữ state riêng → out of sync.

**Vấn đề 3: Server vs Client State** — Data từ API cần caching, loading, error, refetch... khác biệt hoàn toàn với UI state (tabs, modals, forms).

---

## 1. Local State — Đủ cho 80% cases

```tsx
// ✅ Local state
function SearchInput() {
    const [query, setQuery] = useState('');
    return <input value={query} onChange={e => setQuery(e.target.value)} />;
}

// ✅ Lifting state up: di chuyển state lên parent chung
function ProductPage() {
    const [selectedSize, setSelectedSize] = useState('M');
    return (
        <>
            <SizeSelector selected={selectedSize} onChange={setSelectedSize} />
            <AddToCartButton size={selectedSize} />
        </>
    );
}

// ✅ Composition: truyền component thay vì data → giảm prop drilling
function App() {
    const user = useAuth();
    return (
        <Layout>
            <Header avatar={<Avatar user={user} />} />
        </Layout>
    );
}
```

### React Context — Data thay đổi ít (theme, locale, auth)

```tsx
const ThemeContext = createContext(null);

function ThemeProvider({ children }) {
    const [theme, setTheme] = useState('light');
    const value = useMemo(() => ({ theme, toggle: () => setTheme(t => t === 'light' ? 'dark' : 'light') }), [theme]);
    return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

// Dùng ở bất kỳ đâu (không cần prop drilling!)
function ThemeToggle() {
    const { theme, toggle } = useContext(ThemeContext);
    return <button onClick={toggle}>Current: {theme}</button>;
}
```

**⚠️ Context caveat:** Khi context value thay đổi, TẤT CẢ consumers re-render. Cart items thay đổi thường xuyên trong context → toàn bộ subtree re-render → dùng Zustand/Redux thay.

---

## 2. Zustand — Lightweight, đơn giản nhất

Zustand = state manager **nhẹ nhất** cho React. Không boilerplate, không providers.

```tsx
import { create } from 'zustand';

const useCartStore = create((set) => ({
    items: [],
    totalItems: 0,
    
    addItem: (product) => set((state) => {
        const existing = state.items.find(i => i.id === product.id);
        if (existing) {
            return {
                items: state.items.map(i =>
                    i.id === product.id ? { ...i, quantity: i.quantity + 1 } : i
                ),
                totalItems: state.totalItems + 1,
            };
        }
        return {
            items: [...state.items, { ...product, quantity: 1 }],
            totalItems: state.totalItems + 1,
        };
    }),
    
    removeItem: (id) => set((state) => ({
        items: state.items.filter(i => i.id !== id),
        totalItems: state.items.reduce((sum, i) => i.id !== id ? sum + i.quantity : sum, 0),
    })),
    
    clearCart: () => set({ items: [], totalItems: 0 }),
}));

// Selector: component CHỈ re-render khi portion cần thay đổi
function CartIcon() {
    const totalItems = useCartStore((s) => s.totalItems);
    return <span>🛒 ({totalItems})</span>;
}

function ProductCard({ product }) {
    const addItem = useCartStore((s) => s.addItem);
    return <button onClick={() => addItem(product)}>Add to cart</button>;
}
// → Tất cả components tự đồng bộ! Không cần prop drilling.
```

---

## 3. Redux Toolkit — Cho apps lớn, predictable

Mọi state change qua **action → reducer** → dễ debug, time-travel debugging.

```tsx
import { configureStore, createSlice } from '@reduxjs/toolkit';

const cartSlice = createSlice({
    name: 'cart',
    initialState: { items: [], total: 0 },
    reducers: {
        addItem: (state, action) => {
            // Immer: "mutate" trực tiếp (thực tế tạo immutable copy)
            const existing = state.items.find(i => i.id === action.payload.id);
            if (existing) existing.quantity += 1;
            else state.items.push({ ...action.payload, quantity: 1 });
            state.total = state.items.reduce((sum, i) => sum + i.quantity, 0);
        },
    },
});

const store = configureStore({ reducer: { cart: cartSlice.reducer } });

// Component
function CartIcon() {
    const total = useSelector((state) => state.cart.total);
    return <span>🛒 ({total})</span>;
}
```

---

## 4. TanStack Query — Server State (API data)

Data từ API KHÔNG NÊN quản lý bằng Redux/Zustand. Nó có lifecycle riêng: caching, loading, error, refetching, stale detection...

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// GET: fetch + cache + auto-refetch
function UserList() {
    const { data, isLoading, error } = useQuery({
        queryKey: ['users'],
        queryFn: () => fetch('/api/users').then(r => r.json()),
        staleTime: 5 * 60 * 1000,        // Fresh 5 phút
        refetchOnWindowFocus: true,        // Refetch khi quay lại tab
    });
    
    if (isLoading) return <Skeleton />;
    if (error) return <ErrorMessage error={error} />;
    return <ul>{data.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

// POST: mutation + invalidate cache
function CreateUserForm() {
    const queryClient = useQueryClient();
    
    const mutation = useMutation({
        mutationFn: (newUser) => fetch('/api/users', {
            method: 'POST', body: JSON.stringify(newUser),
        }).then(r => r.json()),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['users'] }); // Auto refetch
        },
    });
    
    return <form onSubmit={(e) => {
        e.preventDefault();
        mutation.mutate({ name: 'An' });
    }}>...</form>;
}
```

---

## 5. Khi nào dùng gì?

| State Type | Tool | Khi nào |
|---|---|---|
| Local component | `useState` | Form input, toggle |
| Shared shallow | React Context | Theme, locale, auth |
| Complex shared UI | **Zustand** | Cart, notifications |
| Large app, strict patterns | Redux Toolkit | Enterprise, team lớn |
| Server data (API) | **TanStack Query** | CRUD, pagination, caching |

**Lời khuyên thực tế:**
- Bắt đầu: `useState` + `useContext` (đừng over-engineer)
- Cần global state: **Zustand** (90% cases)
- Cần server state: **TanStack Query** (100% cases với API)
- Team lớn, time-travel debug: Redux Toolkit

---

## Bài tập thực hành

- [ ] Zustand: shopping cart — 3 components subscribe cùng store
- [ ] TanStack Query: CRUD users với caching + optimistic updates
- [ ] So sánh: Context vs Zustand — đo re-renders bằng React DevTools

---

## Tài nguyên thêm

- [Zustand](https://github.com/pmndrs/zustand) — GitHub
- [TanStack Query](https://tanstack.com/query/latest) — Official
- [Redux Toolkit](https://redux-toolkit.js.org/) — Official
