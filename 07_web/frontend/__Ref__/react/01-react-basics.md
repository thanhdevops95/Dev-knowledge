# ⚛️ React — Library UI phổ biến nhất

> `[INTERMEDIATE]` — Component-based UI development

---

## React là gì?

**React** là JavaScript library để xây dựng UI theo kiểu **component-based**. Được tạo bởi Meta (Facebook), hiện là công nghệ frontend phổ biến nhất thế giới.

**Core concepts:**
- **Components** — Khối xây dựng UI, có thể tái sử dụng
- **JSX** — JavaScript + XML syntax
- **State** — Dữ liệu nội bộ của component, khi thay đổi → re-render
- **Props** — Dữ liệu truyền từ parent → child component
- **Virtual DOM** — React so sánh DOM ảo để cập nhật DOM thật hiệu quả

---

## Cài đặt

```bash
# Dùng Vite (nhanh nhất, khuyên dùng)
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install
npm run dev

# Hoặc Next.js (full-stack)
npx create-next-app@latest my-app
```

---

## JSX

```jsx
// JSX là syntactic sugar của React.createElement()
const element = <h1 className="title">Xin chào!</h1>;
// Tương đương:
const element = React.createElement("h1", { className: "title" }, "Xin chào!");

// Rules trong JSX:
// 1. Phải có 1 root element (hoặc dùng Fragment)
return (
    <>
        <h1>Title</h1>
        <p>Content</p>
    </>
);

// 2. className thay vì class
// 3. JavaScript trong {}
const name = "Jesse";
return <p>Xin chào, {name}!</p>;

// 4. Style là object
return <div style={{ color: "red", fontSize: "16px" }}>Text</div>;

// 5. Điều kiện render
return (
    <div>
        {isLoggedIn && <UserGreeting />}
        {isLoggedIn ? <UserGreeting /> : <GuestGreeting />}
        {items.length > 0 ? <List items={items} /> : <Empty />}
    </div>
);

// 6. Render list
return (
    <ul>
        {items.map(item => (
            <li key={item.id}>{item.name}</li>  // key là bắt buộc!
        ))}
    </ul>
);
```

---

## Components & Props

```tsx
// Function Component với TypeScript
interface ButtonProps {
    label: string;
    variant?: "primary" | "secondary" | "danger";
    disabled?: boolean;
    onClick?: () => void;
    children?: React.ReactNode;
}

export function Button({
    label,
    variant = "primary",
    disabled = false,
    onClick,
    children
}: ButtonProps) {
    return (
        <button
            className={`btn btn--${variant}`}
            disabled={disabled}
            onClick={onClick}
        >
            {children ?? label}
        </button>
    );
}

// Sử dụng
<Button label="Gửi" onClick={() => console.log("clicked")} />
<Button variant="danger" disabled>Xóa</Button>
```

---

## Hooks ⭐

### useState

```tsx
import { useState } from "react";

function Counter() {
    const [count, setCount] = useState(0);
    const [user, setUser] = useState<{ name: string } | null>(null);

    return (
        <div>
            <p>Đếm: {count}</p>
            <button onClick={() => setCount(c => c + 1)}>Tăng</button>
            <button onClick={() => setCount(0)}>Reset</button>
        </div>
    );
}
```

### useEffect

```tsx
import { useState, useEffect } from "react";

function UserProfile({ userId }: { userId: number }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Chạy sau mỗi render (nếu không có deps)
        // Chạy 1 lần khi mount (deps = [])
        // Chạy khi userId thay đổi (deps = [userId])
        
        let cancelled = false;
        
        setLoading(true);
        fetch(`/api/users/${userId}`)
            .then(r => r.json())
            .then(data => {
                if (!cancelled) {
                    setUser(data);
                    setLoading(false);
                }
            });

        return () => {
            cancelled = true;  // Cleanup
        };
    }, [userId]);

    if (loading) return <div>Loading...</div>;
    return <div>{user?.name}</div>;
}
```

### useRef

```tsx
import { useRef } from "react";

function VideoPlayer() {
    const videoRef = useRef<HTMLVideoElement>(null);

    const play = () => videoRef.current?.play();
    const pause = () => videoRef.current?.pause();

    return (
        <>
            <video ref={videoRef} src="video.mp4" />
            <button onClick={play}>Play</button>
            <button onClick={pause}>Pause</button>
        </>
    );
}
```

### useContext

```tsx
import { createContext, useContext, useState } from "react";

interface ThemeContextType {
    theme: "light" | "dark";
    toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
    const [theme, setTheme] = useState<"light" | "dark">("dark");
    
    return (
        <ThemeContext.Provider value={{
            theme,
            toggleTheme: () => setTheme(t => t === "light" ? "dark" : "light")
        }}>
            {children}
        </ThemeContext.Provider>
    );
}

export function useTheme() {
    const ctx = useContext(ThemeContext);
    if (!ctx) throw new Error("useTheme phải dùng trong ThemeProvider");
    return ctx;
}

// Sử dụng trong component bất kỳ
function Header() {
    const { theme, toggleTheme } = useTheme();
    return <button onClick={toggleTheme}>Theme: {theme}</button>;
}
```

### useMemo & useCallback

```tsx
import { useMemo, useCallback } from "react";

function ProductList({ products, filter }: Props) {
    // useMemo — cache giá trị tính toán
    const filtered = useMemo(
        () => products.filter(p => p.category === filter),
        [products, filter]  // Chỉ tính lại khi thay đổi
    );

    // useCallback — cache function reference (dùng khi truyền vào child)
    const handleClick = useCallback((id: number) => {
        console.log("Clicked:", id);
    }, []);  // Không dependencies → không bao giờ tạo lại

    return (
        <ul>
            {filtered.map(p => (
                <ProductItem key={p.id} product={p} onClick={handleClick} />
            ))}
        </ul>
    );
}
```

---

## Custom Hooks

```tsx
// Tách logic có thể tái sử dụng
function useFetch<T>(url: string) {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        let cancelled = false;
        setLoading(true);

        fetch(url)
            .then(r => {
                if (!r.ok) throw new Error(`HTTP ${r.status}`);
                return r.json();
            })
            .then(data => { if (!cancelled) { setData(data); setLoading(false); } })
            .catch(err => { if (!cancelled) { setError(err); setLoading(false); } });

        return () => { cancelled = true; };
    }, [url]);

    return { data, loading, error };
}

// Sử dụng
function UserList() {
    const { data, loading, error } = useFetch<User[]>("/api/users");

    if (loading) return <Spinner />;
    if (error) return <Error message={error.message} />;
    return <ul>{data?.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

---

## Patterns phổ biến

```tsx
// Compound Components
<Select>
    <Select.Trigger>Chọn một</Select.Trigger>
    <Select.Options>
        <Select.Option value="1">Option 1</Select.Option>
        <Select.Option value="2">Option 2</Select.Option>
    </Select.Options>
</Select>

// Render Props
<Mouse render={(mouse) => <Cat position={mouse} />} />

// HOC (Higher-Order Component)
const withAuth = (Component) => (props) => {
    const { user } = useAuth();
    if (!user) return <Redirect to="/login" />;
    return <Component {...props} user={user} />;
};
```

---

## Bài tập thực hành

- [ ] **Todo App** với useState, filter, localStorage persistence
- [ ] **Data Dashboard** — Fetch API, loading states, error handling
- [ ] **Auth flow** — Login form, protected routes, token management
- [ ] **Custom Hook** — `useDebounce`, `useLocalStorage`, `useMediaQuery`

---

## Tài nguyên thêm

- [React Docs (react.dev)](https://react.dev/) — Official docs mới nhất
- [Epic React](https://epicreact.dev/) — Khoá học nâng cao của Kent C. Dodds
- [React Query](https://tanstack.com/query) — Server state management tốt nhất
