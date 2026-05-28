# TypeScript Advanced

> **Tags:** `typescript` `generics` `conditional-types` `mapped-types` `template-literal` `utility-types`
> **Level:** Advanced | **Prerequisite:** `typescript/01-typescript-basics.md`

---

## 1. Generics Deep Dive

```typescript
// Basic generic
function identity<T>(arg: T): T {
  return arg;
}

// Generic with constraints
function getLength<T extends { length: number }>(arg: T): number {
  return arg.length;
}

// Multiple type params
function zip<T, U>(arr1: T[], arr2: U[]): [T, U][] {
  return arr1.map((item, i) => [item, arr2[i]]);
}

// Generic with default
interface ApiResponse<T = unknown> {
  data: T;
  status: number;
  message: string;
}

// Generic class
class Repository<T extends { id: number }> {
  private items: Map<number, T> = new Map();

  add(item: T): void {
    this.items.set(item.id, item);
  }

  findById(id: number): T | undefined {
    return this.items.get(id);
  }

  findAll(): T[] {
    return [...this.items.values()];
  }
}

interface User { id: number; name: string }
const userRepo = new Repository<User>();
userRepo.add({ id: 1, name: "Alice" });
```

---

## 2. Conditional Types

```typescript
// Basic conditional type
type IsArray<T> = T extends any[] ? true : false;
type A = IsArray<string[]>;  // true
type B = IsArray<string>;    // false

// Infer — extract types from patterns
type UnwrapArray<T> = T extends (infer U)[] ? U : T;
type C = UnwrapArray<string[]>;   // string
type D = UnwrapArray<number>;     // number (not array, return as-is)

// Unwrap Promise
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;
// (này đã có sẵn trong TypeScript 4.5+)
type E = Awaited<Promise<Promise<string>>>;  // string

// Extract return type
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
// (đã có sẵn)
type F = ReturnType<() => Promise<number>>;  // Promise<number>

// Extract parameter types  
type Parameters<T> = T extends (...args: infer P) => any ? P : never;
// (đã có sẵn)
type G = Parameters<(x: number, y: string) => void>;  // [x: number, y: string]

// Distributive conditional types
type ToArray<T> = T extends any ? T[] : never;
type H = ToArray<string | number>;  // string[] | number[]
// NOTE: T extends any distributes over union!

// Non-distributive (wrap in tuple)
type ToArrayNonDistributive<T> = [T] extends [any] ? T[] : never;
type I = ToArrayNonDistributive<string | number>;  // (string | number)[]
```

---

## 3. Mapped Types

```typescript
// Basic mapped type
type Readonly<T> = {
  readonly [K in keyof T]: T[K];
};

type Partial<T> = {
  [K in keyof T]?: T[K];
};

type Required<T> = {
  [K in keyof T]-?: T[K];  // -? removes optionality
};

// Mapped type with remapping (TypeScript 4.1+)
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface User {
  name: string;
  age: number;
}

type UserGetters = Getters<User>;
// { getName: () => string; getAge: () => number; }

// Filter properties by type
type PickByType<T, Value> = {
  [K in keyof T as T[K] extends Value ? K : never]: T[K];
};

interface Mixed {
  name: string;
  age: number;
  active: boolean;
  score: number;
}

type OnlyStrings = PickByType<Mixed, string>;    // { name: string }
type OnlyNumbers = PickByType<Mixed, number>;    // { age: number; score: number }

// DeepReadonly
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

// DeepPartial
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};
```

---

## 4. Template Literal Types

```typescript
// String manipulation types (TypeScript 4.1+)
type EventName = `on${Capitalize<string>}`;
type greeting = `Hello, ${string}!`;

// Practical: API route types
type HTTPMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
type Endpoint = "/users" | "/posts" | "/comments";
type Route = `${HTTPMethod} ${Endpoint}`;
// "GET /users" | "POST /users" | "GET /posts" | ... (15 combinations)

// Object with event handlers
type Events = {
  click: MouseEvent;
  keydown: KeyboardEvent;
  focus: FocusEvent;
};

type EventHandlers = {
  [K in keyof Events as `on${Capitalize<string & K>}`]: (e: Events[K]) => void;
};
// { onClick: (e: MouseEvent) => void; onKeydown: ... }

// CSS property builder
type CSSUnit = "px" | "em" | "rem" | "%";
type CSSValue = `${number}${CSSUnit}`;
// "16px", "1.5em", "100%" etc.

// Extracting parts from string types
type ExtractRoute<T extends string> =
  T extends `${infer Method} ${infer Path}` ? { method: Method; path: Path } : never;

type Parsed = ExtractRoute<"GET /users/123">;
// { method: "GET"; path: "/users/123" }
```

---

## 5. Discriminated Unions

```typescript
// Pattern: common "type" field for exhaustive checking
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;  // shape is { kind: "circle"; radius: number }
    case "rectangle":
      return shape.width * shape.height;
    case "triangle":
      return (shape.base * shape.height) / 2;
    default:
      // TypeScript ensures exhaustiveness!
      const _exhaustive: never = shape;
      throw new Error(`Unhandled shape: ${_exhaustive}`);
  }
}

// Result type pattern (Railway-Oriented Programming)
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

async function fetchUser(id: number): Promise<Result<User>> {
  try {
    const user = await db.findUser(id);
    return { success: true, data: user };
  } catch (error) {
    return { success: false, error: error as Error };
  }
}

const result = await fetchUser(1);
if (result.success) {
  console.log(result.data.name);    // TypeScript knows: result.data is User
} else {
  console.error(result.error.message); // TypeScript knows: result.error is Error
}
```

---

## 6. Utility Types Deep Dive

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  age?: number;
  role: "admin" | "user" | "guest";
}

// Pick — chỉ lấy các keys cụ thể
type UserPreview = Pick<User, "id" | "name">;
// { id: number; name: string }

// Omit — loại bỏ keys
type UserWithoutId = Omit<User, "id">;
// { name: string; email: string; age?: number; role: ... }

// Exclude — loại bỏ từ union type
type NonAdmin = Exclude<User["role"], "admin">;
// "user" | "guest"

// Extract — chỉ giữ matching từ union
type AdminOrUser = Extract<User["role"], "admin" | "user">;
// "admin" | "user"

// Record
type UserMap = Record<string, User>;
// { [key: string]: User }

type RolePermissions = Record<User["role"], string[]>;
// { admin: string[]; user: string[]; guest: string[] }

// NonNullable
type MaybeUser = User | null | undefined;
type DefiniteUser = NonNullable<MaybeUser>;  // User

// ReturnType + Parameters
function createUser(name: string, email: string): User { ... }
type CreateUserReturn = ReturnType<typeof createUser>;    // User  
type CreateUserParams = Parameters<typeof createUser>;   // [name: string, email: string]

// ConstructorParameters + InstanceType
class MyService {
  constructor(private db: Database, private cache: Cache) {}
}
type ServiceParams = ConstructorParameters<typeof MyService>;  // [Database, Cache]
type ServiceInstance = InstanceType<typeof MyService>;         // MyService

// Awaited (TypeScript 4.5+)
type AsyncResult = Promise<Promise<User>>;
type FinalResult = Awaited<AsyncResult>;  // User
```

---

## 7. Type Guards & Narrowing

```typescript
// typeof guard
function processInput(input: string | number): string {
  if (typeof input === "string") {
    return input.toUpperCase();  // TypeScript knows: input is string
  }
  return input.toFixed(2);      // TypeScript knows: input is number
}

// instanceof guard
function formatError(error: Error | string): string {
  if (error instanceof Error) {
    return `${error.name}: ${error.message}`;
  }
  return error;
}

// User-defined type guard (is keyword)
interface Cat { meow(): void }
interface Dog { bark(): void }

function isCat(animal: Cat | Dog): animal is Cat {
  return (animal as Cat).meow !== undefined;
}

function makeSound(animal: Cat | Dog): void {
  if (isCat(animal)) {
    animal.meow();  // TypeScript knows: animal is Cat
  } else {
    animal.bark();  // TypeScript knows: animal is Dog
  }
}

// Assertion function
function assertIsDefined<T>(val: T): asserts val is NonNullable<T> {
  if (val === undefined || val === null) {
    throw new Error(`Expected defined value, got ${val}`);
  }
}

let user: User | null = getUser();
assertIsDefined(user);
console.log(user.name);  // TypeScript knows: user is User (not null)
```

---

## 8. Declaration Merging & Module Augmentation

```typescript
// Interface merging — useful for extending third-party types
interface Window {
  myApp: { version: string };
}
// Now TypeScript knows window.myApp exists

// Module augmentation — extend existing modules
declare module 'express' {
  interface Request {
    user?: User;       // Add user to Express Request
    traceId?: string;
  }
}

// Global augmentation
declare global {
  interface Array<T> {
    first(): T | undefined;
    last(): T | undefined;
  }
}

Array.prototype.first = function() { return this[0]; };
Array.prototype.last = function() { return this[this.length - 1]; };
```

---

## 9. satisfies Operator (TypeScript 4.9+)

```typescript
// Problem with 'as': loses type narrowing
const config = {
  port: 3000,
  host: "localhost",
} as Record<string, unknown>;   // All values become 'unknown'

config.port.toFixed(2);  // Error: Object is of type 'unknown'

// Solution: satisfies — validates type but keeps inferred type
const config2 = {
  port: 3000,
  host: "localhost",
} satisfies Record<string, unknown>;

config2.port.toFixed(2);  // OK! TypeScript knows port is number
config2.host.toUpperCase();  // OK! TypeScript knows host is string

// Practical: palette with both constraint AND specificity
const palette = {
  red: [255, 0, 0],
  green: "#00ff00",
  blue: [0, 0, 255],
} satisfies Record<string, string | number[]>;

palette.red.map(...)     // OK! TypeScript knows red is number[], not string | number[]
palette.green.toUpperCase()  // OK! TypeScript knows green is string
```

---

## 10. Advanced tsconfig Patterns

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,          // Enables all strict checks
    "noUncheckedIndexedAccess": true,  // arr[i] is T | undefined
    "exactOptionalPropertyTypes": true, // ?prop !== prop: T | undefined
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "verbatimModuleSyntax": true,  // Enforce type-only imports

    // Path aliases
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"]
    },

    // Output
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,     // Generate .d.ts files
    "sourceMap": true
  }
}
```

---

## 11. Bài tập

1. **Generic Builder**: Tạo `QueryBuilder<T>` generic class hỗ trợ `.where()`, `.select()`, `.orderBy()` với types an toàn.
2. **Mapped types**: Tạo `FormState<T>` từ type `T` — mỗi field có `value`, `error`, `touched`.
3. **Discriminated union**: Tạo Redux-like action system hoàn toàn type-safe.
4. **Template literal**: Tạo CSS-in-JS helper có type `css(prop: CSSProperty, value: string)`.
5. **Type guard**: Tạo runtime validator cho API responses — input `unknown`, output typed hoặc error.

---

*Tài liệu liên quan: `typescript/01-typescript-basics.md` | `javascript/02-js-advanced.md` | `react/02-react-advanced.md`*
