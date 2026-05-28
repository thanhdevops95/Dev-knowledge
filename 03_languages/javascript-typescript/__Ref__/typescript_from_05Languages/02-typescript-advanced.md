# 📘 TypeScript nâng cao — Generics, Utility Types & Patterns

> `[INTERMEDIATE → ADVANCED]` — Type system mạnh mẽ cho production

---

## 1. Generics — Tái sử dụng type

```typescript
// Generic function
function getFirst<T>(arr: T[]): T | undefined {
    return arr[0];
}

getFirst<number>([1, 2, 3]);     // number
getFirst(['a', 'b']);              // string (tự infer)

// Generic interface
interface ApiResponse<T> {
    data: T;
    status: number;
    message: string;
}

type UserResponse = ApiResponse<User>;
type PostResponse = ApiResponse<Post[]>;

// Generic class
class Repository<T extends { id: number }> {
    private items: T[] = [];

    add(item: T): void { this.items.push(item); }
    findById(id: number): T | undefined {
        return this.items.find(item => item.id === id);
    }
    getAll(): T[] { return [...this.items]; }
}

const userRepo = new Repository<User>();
userRepo.add({ id: 1, name: 'An' });

// Constrained generics
function merge<T extends object, U extends object>(a: T, b: U): T & U {
    return { ...a, ...b };
}
```

---

## 2. Utility Types

```typescript
interface User {
    id: number;
    name: string;
    email: string;
    password: string;
    role: 'admin' | 'user';
    createdAt: Date;
}

// Partial — tất cả fields optional
type UpdateUserInput = Partial<User>;  // { id?: number; name?: string; ... }

// Required — tất cả fields required
type StrictUser = Required<User>;

// Pick — chọn 1 số fields
type UserPreview = Pick<User, 'id' | 'name' | 'email'>;

// Omit — bỏ 1 số fields
type UserPublic = Omit<User, 'password'>;

// Record — key-value map
type UserMap = Record<string, User>;  // { [key: string]: User }

// ReturnType — lấy return type của function
function getUser() { return { id: 1, name: 'An' }; }
type UserFromFn = ReturnType<typeof getUser>;  // { id: number; name: string }

// Exclude / Extract — lọc union types
type Status = 'pending' | 'active' | 'blocked' | 'deleted';
type ActiveStatus = Extract<Status, 'active' | 'pending'>;  // 'active' | 'pending'
type RemovedStatus = Exclude<Status, 'active' | 'pending'>; // 'blocked' | 'deleted'
```

---

## 3. Template Literal Types

```typescript
type Color = 'red' | 'blue' | 'green';
type Size = 'sm' | 'md' | 'lg';

// Combine → 'red-sm' | 'red-md' | 'red-lg' | 'blue-sm' | ...
type ClassName = `${Color}-${Size}`;

// Event handler types
type EventName = 'click' | 'hover' | 'focus';
type HandlerName = `on${Capitalize<EventName>}`;
// 'onClick' | 'onHover' | 'onFocus'

// CSS unit types
type CSSUnit = `${number}${'px' | 'rem' | 'em' | '%' | 'vh' | 'vw'}`;

function setWidth(width: CSSUnit) {}
setWidth('100px');   // OK
setWidth('50%');     // OK
setWidth('hello');   // Error!
```

---

## 4. Conditional & Mapped Types

```typescript
// Conditional type
type IsArray<T> = T extends any[] ? true : false;
type A = IsArray<string[]>;  // true
type B = IsArray<string>;    // false

// Infer — extract type
type ElementType<T> = T extends (infer U)[] ? U : never;
type Item = ElementType<string[]>;   // string
type Item2 = ElementType<number[]>;  // number

// Mapped types — transform properties
type Readonly<T> = { readonly [K in keyof T]: T[K] };
type Optional<T> = { [K in keyof T]?: T[K] };

// Custom: make all string properties nullable
type Nullable<T> = {
    [K in keyof T]: T[K] extends string ? T[K] | null : T[K];
};
```

---

## 5. Discriminated Unions (Pattern Matching)

```typescript
// Mỗi variant có 1 field "type" khác nhau
type Shape =
    | { type: 'circle'; radius: number }
    | { type: 'rectangle'; width: number; height: number }
    | { type: 'triangle'; base: number; height: number };

function calculateArea(shape: Shape): number {
    switch (shape.type) {
        case 'circle':
            return Math.PI * shape.radius ** 2;  // TS biết shape.radius tồn tại!
        case 'rectangle':
            return shape.width * shape.height;    // TS biết width + height!
        case 'triangle':
            return (shape.base * shape.height) / 2;
    }
}

// API Response pattern
type Result<T> =
    | { success: true; data: T }
    | { success: false; error: string };

function handleResult(result: Result<User>) {
    if (result.success) {
        console.log(result.data.name);  // TS biết data tồn tại
    } else {
        console.error(result.error);     // TS biết error tồn tại
    }
}
```

---

## 6. Type Guards

```typescript
// typeof
function process(value: string | number) {
    if (typeof value === 'string') {
        return value.toUpperCase();  // TS biết là string
    }
    return value.toFixed(2);          // TS biết là number
}

// instanceof
function formatError(error: unknown) {
    if (error instanceof Error) {
        return error.message;
    }
    return String(error);
}

// Custom type guard (is keyword)
interface Fish { swim(): void; }
interface Bird { fly(): void; }

function isFish(animal: Fish | Bird): animal is Fish {
    return 'swim' in animal;
}

function move(animal: Fish | Bird) {
    if (isFish(animal)) {
        animal.swim();   // TS biết là Fish!
    } else {
        animal.fly();    // TS biết là Bird!
    }
}

// Assertion function
function assertNonNull<T>(value: T | null | undefined): asserts value is T {
    if (value == null) throw new Error('Value is null');
}
```

---

## 7. Zod — Runtime validation + Type inference

```typescript
import { z } from 'zod';

const UserSchema = z.object({
    name: z.string().min(2),
    email: z.string().email(),
    age: z.number().int().positive().optional(),
    role: z.enum(['admin', 'user']).default('user'),
});

// Infer TypeScript type TỪ schema — single source of truth!
type User = z.infer<typeof UserSchema>;
// { name: string; email: string; age?: number; role: 'admin' | 'user' }

// Validate runtime data
const result = UserSchema.safeParse(reqBody);
if (result.success) {
    const user: User = result.data;  // Type-safe!
} else {
    console.error(result.error.issues);
}
```

---

## Các lỗi thường gặp

```typescript
// ❌ Sai: any mọi nơi
function getData(): any { ... }

// ✅ Đúng: Dùng proper types hoặc unknown
function getData(): unknown { ... }
function getData(): User[] { ... }

// ❌ Sai: Type assertion không cần thiết
const user = data as User;  // Bypass type checking!

// ✅ Đúng: Type guard
if (isUser(data)) {
    // data is User — safe!
}
```

---

## Bài tập thực hành

- [ ] Viết generic `Result<T>` type + helper functions
- [ ] Tạo 5 utility types tùy chỉnh (DeepPartial, RequiredKeys...)
- [ ] Discriminated union cho API response handling
- [ ] Zod schema → infer TypeScript types cho REST API

---

## Tài nguyên thêm

- [TypeScript Docs](https://www.typescriptlang.org/docs/) — Official
- [Type Challenges](https://github.com/type-challenges/type-challenges) — Practice
- [Matt Pocock (Total TypeScript)](https://www.totaltypescript.com/) — Advanced
