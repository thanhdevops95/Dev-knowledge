# React Advanced Patterns

> **Tags:** `react` `hooks` `context` `performance` `patterns` `compound-components`
> **Level:** Advanced | **Prerequisite:** `react/01-react-basics.md`

---

## 1. Custom Hooks

Tách logic ra khỏi UI, tạo reusable units of behavior:

```typescript
// useLocalStorage — sync state with localStorage
import { useState, useEffect, useCallback } from 'react';

function useLocalStorage<T>(key: string, initialValue: T) {
    const [storedValue, setStoredValue] = useState<T>(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            return initialValue;
        }
    });

    const setValue = useCallback((value: T | ((prev: T) => T)) => {
        try {
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            setStoredValue(valueToStore);
            window.localStorage.setItem(key, JSON.stringify(valueToStore));
        } catch (error) {
            console.error(error);
        }
    }, [key, storedValue]);

    return [storedValue, setValue] as const;
}

// useDebounce — delay value update
function useDebounce<T>(value: T, delay: number): T {
    const [debouncedValue, setDebouncedValue] = useState<T>(value);

    useEffect(() => {
        const handler = setTimeout(() => setDebouncedValue(value), delay);
        return () => clearTimeout(handler);
    }, [value, delay]);

    return debouncedValue;
}

// useFetch — data fetching with loading/error states
function useFetch<T>(url: string) {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        const controller = new AbortController();
        
        async function fetchData() {
            try {
                setLoading(true);
                const response = await fetch(url, { signal: controller.signal });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const json = await response.json();
                setData(json);
                setError(null);
            } catch (err) {
                if (err instanceof Error && err.name !== 'AbortError') {
                    setError(err);
                }
            } finally {
                setLoading(false);
            }
        }

        fetchData();
        return () => controller.abort();   // Cleanup: cancel pending request
    }, [url]);

    return { data, loading, error };
}

// Usage
function SearchPage() {
    const [query, setQuery] = useState('');
    const debouncedQuery = useDebounce(query, 300);
    const { data, loading, error } = useFetch<User[]>(`/api/users?q=${debouncedQuery}`);
    
    return (
        <div>
            <input value={query} onChange={e => setQuery(e.target.value)} />
            {loading && <Spinner />}
            {error && <ErrorMessage error={error} />}
            {data?.map(user => <UserCard key={user.id} user={user} />)}
        </div>
    );
}
```

---

## 2. Context + useReducer — State Management

```typescript
// Full-featured context with useReducer
type User = { id: number; name: string; email: string; role: 'admin' | 'user' };

type AuthState = {
    user: User | null;
    token: string | null;
    loading: boolean;
};

type AuthAction =
    | { type: 'LOGIN_START' }
    | { type: 'LOGIN_SUCCESS'; user: User; token: string }
    | { type: 'LOGIN_FAILURE' }
    | { type: 'LOGOUT' };

function authReducer(state: AuthState, action: AuthAction): AuthState {
    switch (action.type) {
        case 'LOGIN_START':
            return { ...state, loading: true };
        case 'LOGIN_SUCCESS':
            return { user: action.user, token: action.token, loading: false };
        case 'LOGIN_FAILURE':
            return { ...state, loading: false };
        case 'LOGOUT':
            return { user: null, token: null, loading: false };
        default:
            return state;
    }
}

// Context
const AuthContext = createContext<{
    state: AuthState;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
} | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [state, dispatch] = useReducer(authReducer, {
        user: null,
        token: localStorage.getItem('token'),
        loading: false,
    });

    const login = async (email: string, password: string) => {
        dispatch({ type: 'LOGIN_START' });
        try {
            const res = await api.post('/auth/login', { email, password });
            localStorage.setItem('token', res.data.token);
            dispatch({ type: 'LOGIN_SUCCESS', user: res.data.user, token: res.data.token });
        } catch {
            dispatch({ type: 'LOGIN_FAILURE' });
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        dispatch({ type: 'LOGOUT' });
    };

    return (
        <AuthContext.Provider value={{ state, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

// Custom hook for consuming context
export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) throw new Error('useAuth must be used within AuthProvider');
    return context;
}
```

---

## 3. Compound Components Pattern

Flexible component API — hide complexity, allow customization:

```typescript
// Compound component: Select/Option
interface SelectContextValue {
    selected: string;
    onSelect: (value: string) => void;
    isOpen: boolean;
    setIsOpen: (open: boolean) => void;
}

const SelectContext = createContext<SelectContextValue | undefined>(undefined);

function useSelectContext() {
    const ctx = useContext(SelectContext);
    if (!ctx) throw new Error('Must be used inside <Select>');
    return ctx;
}

// Main Select component
function Select({ children, value, onChange }: {
    children: React.ReactNode;
    value: string;
    onChange: (value: string) => void;
}) {
    const [isOpen, setIsOpen] = useState(false);
    
    return (
        <SelectContext.Provider value={{ selected: value, onSelect: onChange, isOpen, setIsOpen }}>
            <div className="select-container">
                {children}
            </div>
        </SelectContext.Provider>
    );
}

// Sub-components
Select.Trigger = function SelectTrigger({ children }: { children: React.ReactNode }) {
    const { selected, isOpen, setIsOpen } = useSelectContext();
    return (
        <button onClick={() => setIsOpen(!isOpen)}>
            {selected || children}
            <ChevronIcon rotated={isOpen} />
        </button>
    );
};

Select.List = function SelectList({ children }: { children: React.ReactNode }) {
    const { isOpen } = useSelectContext();
    return isOpen ? <ul className="select-list">{children}</ul> : null;
};

Select.Option = function SelectOption({ value, children }: { value: string; children: React.ReactNode }) {
    const { selected, onSelect, setIsOpen } = useSelectContext();
    return (
        <li
            className={selected === value ? 'selected' : ''}
            onClick={() => { onSelect(value); setIsOpen(false); }}
        >
            {children}
        </li>
    );
};

// Usage — extremely composable
<Select value={country} onChange={setCountry}>
    <Select.Trigger>Select country</Select.Trigger>
    <Select.List>
        <Select.Option value="us">United States</Select.Option>
        <Select.Option value="vn">Vietnam</Select.Option>
        <Select.Option value="jp">Japan</Select.Option>
    </Select.List>
</Select>
```

---

## 4. Render Props Pattern (Legacy but still relevant)

```typescript
// Render prop: pass render function as prop
interface MousePosition {
    x: number;
    y: number;
}

function MouseTracker({ render }: { render: (pos: MousePosition) => React.ReactNode }) {
    const [position, setPosition] = useState<MousePosition>({ x: 0, y: 0 });

    const handleMouseMove = (e: React.MouseEvent) => {
        setPosition({ x: e.clientX, y: e.clientY });
    };

    return <div onMouseMove={handleMouseMove} style={{ width: '100%', height: '100vh' }}>
        {render(position)}
    </div>;
}

// Usage
<MouseTracker
    render={({ x, y }) => (
        <div>Mouse is at ({x}, {y})</div>
    )}
/>

// Modern equivalent: custom hook
function useMousePosition() {
    const [position, setPosition] = useState({ x: 0, y: 0 });
    useEffect(() => {
        const handleMouseMove = (e: MouseEvent) => setPosition({ x: e.clientX, y: e.clientY });
        document.addEventListener('mousemove', handleMouseMove);
        return () => document.removeEventListener('mousemove', handleMouseMove);
    }, []);
    return position;
}
```

---

## 5. Performance Optimization

```typescript
// React.memo — skip re-render if props unchanged
const UserCard = React.memo(function UserCard({ user, onSelect }: {
    user: User;
    onSelect: (id: number) => void;
}) {
    return <div onClick={() => onSelect(user.id)}>{user.name}</div>;
}, (prevProps, nextProps) => {
    // Custom comparison — return true to SKIP re-render
    return prevProps.user.id === nextProps.user.id && 
           prevProps.user.name === nextProps.user.name;
});

// useMemo — memoize expensive computation
function UserList({ users, filter }: { users: User[]; filter: string }) {
    // Only recomputes when users or filter changes
    const filteredUsers = useMemo(() => {
        return users.filter(u => u.name.toLowerCase().includes(filter.toLowerCase()));
    }, [users, filter]);

    const stats = useMemo(() => ({
        total: filteredUsers.length,
        admins: filteredUsers.filter(u => u.role === 'admin').length,
    }), [filteredUsers]);

    return <div>...</div>;
}

// useCallback — stable function reference
function SearchPage() {
    const [query, setQuery] = useState('');

    // Without useCallback: new function reference on every render → ProductList re-renders
    // With useCallback: same reference if deps unchanged → ProductList doesn't re-render
    const handleSelect = useCallback((id: number) => {
        console.log('Selected:', id);
    }, []);    // No deps → stable forever

    return (
        <>
            <input value={query} onChange={e => setQuery(e.target.value)} />
            <ProductList onSelect={handleSelect} />  {/* Won't re-render on query change */}
        </>
    );
}
```

### Code Splitting
```typescript
// Lazy load routes
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Profile = lazy(() => import('./pages/Profile'));
const Admin = lazy(() => import('./pages/Admin'));

function App() {
    return (
        <Router>
            <Suspense fallback={<PageSpinner />}>
                <Routes>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/profile" element={<Profile />} />
                    <Route path="/admin" element={<Admin />} />
                </Routes>
            </Suspense>
        </Router>
    );
}

// Lazy load heavy components
const RichEditor = lazy(() => import('./components/RichEditor'));
const Chart = lazy(() => import('./components/Chart'));
```

---

## 6. Error Boundaries

```typescript
interface ErrorBoundaryState {
    hasError: boolean;
    error: Error | null;
}

class ErrorBoundary extends React.Component<
    { children: React.ReactNode; fallback?: React.ComponentType<{ error: Error }> },
    ErrorBoundaryState
> {
    constructor(props: any) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error: Error) {
        return { hasError: true, error };
    }

    componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
        // Log to error tracking service
        console.error('Error caught by boundary:', error, errorInfo);
        // Sentry.captureException(error, { extra: errorInfo });
    }

    render() {
        if (this.state.hasError && this.state.error) {
            const Fallback = this.props.fallback;
            return Fallback ? <Fallback error={this.state.error} /> : <DefaultErrorUI />;
        }
        return this.props.children;
    }
}

// Usage
<ErrorBoundary fallback={({ error }) => <ErrorPage message={error.message} />}>
    <UserDashboard />
</ErrorBoundary>
```

---

## 7. React 18 Features

### useTransition — Mark Updates as Non-Urgent
```typescript
import { useTransition, useState } from 'react';

function SearchPage() {
    const [isPending, startTransition] = useTransition();
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setQuery(e.target.value);  // Urgent: update input immediately
        
        startTransition(() => {
            // Non-urgent: can be interrupted by more urgent updates
            setResults(searchProducts(e.target.value));
        });
    };

    return (
        <div>
            <input onChange={handleChange} />
            {isPending ? <Spinner /> : null}
            {results.map(r => <Result key={r.id} {...r} />)}
        </div>
    );
}
```

### useDeferredValue
```typescript
function ProductList({ query }: { query: string }) {
    // Defer heavy computation — shows stale list while computing new one
    const deferredQuery = useDeferredValue(query);
    const isStale = query !== deferredQuery;
    
    const results = useMemo(() => 
        filterProducts(products, deferredQuery),
    [deferredQuery]);

    return (
        <div style={{ opacity: isStale ? 0.6 : 1 }}>
            {results.map(p => <ProductCard key={p.id} product={p} />)}
        </div>
    );
}
```

### use() hook (React 19)
```typescript
// New way to read from Promises and Contexts
async function getUser(id: number): Promise<User> {
    const res = await fetch(`/api/users/${id}`);
    return res.json();
}

function UserProfile({ id }: { id: number }) {
    // use() can be called conditionally!
    const user = use(getUser(id));   // Suspense-aware
    const theme = use(ThemeContext); // Context reading
    
    return <div>{user.name}</div>;
}
```

---

## 8. Refs Advanced

```typescript
// useImperativeHandle — expose custom API via ref
interface ModalHandle {
    open: () => void;
    close: () => void;
    isOpen: () => boolean;
}

const Modal = forwardRef<ModalHandle, { children: React.ReactNode }>(
    ({ children }, ref) => {
        const [isOpen, setIsOpen] = useState(false);

        useImperativeHandle(ref, () => ({
            open: () => setIsOpen(true),
            close: () => setIsOpen(false),
            isOpen: () => isOpen,
        }), [isOpen]);

        return isOpen ? (
            <div className="modal-overlay">
                <div className="modal">{children}</div>
            </div>
        ) : null;
    }
);

// Usage
function App() {
    const modalRef = useRef<ModalHandle>(null);

    return (
        <>
            <button onClick={() => modalRef.current?.open()}>Open Modal</button>
            <Modal ref={modalRef}>
                <button onClick={() => modalRef.current?.close()}>Close</button>
            </Modal>
        </>
    );
}
```

---

## 9. Testing React Components

```typescript
// Vitest + @testing-library/react
import { render, screen, userEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';

describe('UserCard', () => {
    it('renders user name and email', () => {
        const user = { id: 1, name: 'Alice', email: 'alice@example.com' };
        render(<UserCard user={user} onSelect={vi.fn()} />);
        
        expect(screen.getByText('Alice')).toBeInTheDocument();
        expect(screen.getByText('alice@example.com')).toBeInTheDocument();
    });

    it('calls onSelect when clicked', async () => {
        const user = { id: 1, name: 'Alice', email: 'alice@example.com' };
        const handleSelect = vi.fn();
        render(<UserCard user={user} onSelect={handleSelect} />);
        
        await userEvent.click(screen.getByRole('button', { name: 'Alice' }));
        
        expect(handleSelect).toHaveBeenCalledWith(1);
    });
});

// Testing async components
describe('UserList with API', () => {
    it('shows loading state then users', async () => {
        vi.mocked(fetch).mockResolvedValueOnce(new Response(
            JSON.stringify([{ id: 1, name: 'Alice' }])
        ));

        render(<UserList />);
        
        expect(screen.getByRole('progressbar')).toBeInTheDocument();
        
        await waitFor(() => {
            expect(screen.getByText('Alice')).toBeInTheDocument();
        });
        
        expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });
});
```

---

## 10. Bài tập

1. **Custom hook**: Tạo `useUndo<T>()` hook — track state history, support undo/redo.
2. **Compound component**: Tạo `<Tabs>` với `<Tabs.List>`, `<Tabs.Tab>`, `<Tabs.Panel>`.
3. **Performance audit**: Dùng React DevTools Profiler, identify và fix re-renders thừa trong app của bạn.
4. **Error boundary**: Tạo error boundary với "Report Bug" button và error logging.
5. **Suspense**: Convert existing data-fetching component sang Suspense-based với React Query.

---

*Tài liệu liên quan: `react/01-react-basics.md` | `react/03-react-state-management.md` | `typescript/02-typescript-advanced.md`*
