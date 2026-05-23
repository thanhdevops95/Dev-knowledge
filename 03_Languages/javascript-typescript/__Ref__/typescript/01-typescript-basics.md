# 🔷 TypeScript — JavaScript có kiểu dữ liệu

> `[INTERMEDIATE]` ⭐ `[MUST-KNOW]` — Bắt buộc trong mọi dự án JS lớn

---

## TypeScript là gì?

TypeScript = JavaScript + Static Types. TypeScript được **compile** thành JavaScript trước khi chạy.

**Lợi ích:**
- Phát hiện lỗi **ngay lúc viết code**, không phải lúc chạy
- Autocomplete và gợi ý code tốt hơn trong IDE
- Dễ đọc, dễ maintain cho team lớn
- Refactoring an toàn hơn

---

## Cài đặt

```bash
npm install -g typescript
tsc --version

# Khởi tạo project
tsc --init       # Tạo tsconfig.json

# Dùng với Vite (khuyên dùng)
npm create vite@latest my-app -- --template react-ts
```

---

## Kiểu dữ liệu cơ bản

```typescript
// Primitive types
let name: string = "Jesse";
let age: number = 25;
let isActive: boolean = true;
let nothing: null = null;
let notYet: undefined = undefined;

// Arrays
let fruits: string[] = ["apple", "banana"];
let numbers: Array<number> = [1, 2, 3];

// Tuple — mảng với độ dài và kiểu cố định
let point: [number, number] = [10, 20];
let rgb: [number, number, number] = [255, 128, 0];

// Union types — có thể là nhiều kiểu
let id: string | number;
id = "abc123";
id = 123;

// Literal types
let direction: "north" | "south" | "east" | "west";
let status: 200 | 400 | 404 | 500;

// any — tránh dùng!
let anything: any = "hello";

// unknown — an toàn hơn any
let value: unknown = getData();
if (typeof value === "string") {
    console.log(value.toUpperCase());  // OK, đã kiểm tra kiểu
}
```

---

## Interface & Type

```typescript
// Interface — định nghĩa cấu trúc object
interface User {
    id: number;
    name: string;
    email: string;
    age?: number;           // Optional
    readonly createdAt: Date;  // Không thể thay đổi sau khi tạo
}

// Extends interface
interface Admin extends User {
    role: "admin" | "superadmin";
    permissions: string[];
}

// Type alias — linh hoạt hơn interface
type ID = string | number;

type ApiResponse<T> = {
    data: T;
    error: string | null;
    status: number;
};

// Sử dụng Generic
const response: ApiResponse<User[]> = {
    data: [],
    error: null,
    status: 200
};

// Intersection types
type AdminUser = User & { role: string };
```

---

## Functions với TypeScript

```typescript
// Khai báo kiểu cho function
function add(a: number, b: number): number {
    return a + b;
}

// Arrow function
const multiply = (a: number, b: number): number => a * b;

// Optional và default params
function greet(name: string, greeting?: string): string {
    return `${greeting ?? "Hello"}, ${name}!`;
}

// Overloads
function format(value: string): string;
function format(value: number, decimals: number): string;
function format(value: string | number, decimals?: number): string {
    if (typeof value === "string") return value.trim();
    return value.toFixed(decimals ?? 2);
}

// Generic functions
function first<T>(array: T[]): T | undefined {
    return array[0];
}

first([1, 2, 3])        // type: number | undefined
first(["a", "b"])       // type: string | undefined
```

---

## Classes

```typescript
class Repository<T extends { id: number }> {
    private items: T[] = [];

    add(item: T): void {
        this.items.push(item);
    }

    findById(id: number): T | undefined {
        return this.items.find(item => item.id === id);
    }

    getAll(): readonly T[] {
        return this.items;
    }
}

class UserRepository extends Repository<User> {
    findByEmail(email: string): User | undefined {
        return this.getAll().find(u => u.email === email);
    }
}
```

---

## Utility Types (rất hữu ích)

```typescript
interface User {
    id: number;
    name: string;
    email: string;
    password: string;
    age: number;
}

// Partial — tất cả fields trở thành optional
type UserUpdate = Partial<User>;

// Required — tất cả fields bắt buộc
type StrictUser = Required<User>;

// Pick — chọn một số fields
type UserPublic = Pick<User, "id" | "name" | "email">;

// Omit — bỏ một số fields
type UserWithoutPassword = Omit<User, "password">;

// Record — tạo object type
type UserMap = Record<string, User>;

// Readonly — không thể thay đổi
type ReadonlyUser = Readonly<User>;

// ReturnType — lấy kiểu trả về của function
type GetUserReturn = ReturnType<typeof getUser>;
```

---

## Bài tập thực hành

- [ ] Chuyển đổi 1 project JavaScript sang TypeScript
- [ ] Viết generic `useLocalStorage<T>` hook với TypeScript
- [ ] Tạo type-safe API client với `fetch` và generics

---

## Tài nguyên thêm

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/) — Tài liệu chính thức
- [Total TypeScript](https://www.totaltypescript.com/) — Khoá học nâng cao miễn phí
- [Type Challenges](https://github.com/type-challenges/type-challenges) — Bài tập TypeScript
