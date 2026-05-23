# ⚡ JavaScript cơ bản — Ngôn ngữ của Web

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Ngôn ngữ lập trình duy nhất chạy native trên browser

---

## Tại sao JavaScript?

- **Duy nhất** chạy trên mọi browser — không cần cài gì
- **Full-stack:** Frontend (React) + Backend (Node.js) + Mobile (React Native)
- **#1** ngôn ngữ trên GitHub, Stack Overflow

---

## 1. Variables & Types

```javascript
// let (có thể gán lại), const (không gán lại), var (cũ — tránh dùng)
let name = "An";
const PI = 3.14159;
// var old = "tránh dùng";  // function-scoped, hoisting bugs

// Primitive types
const str = "Hello";           // String
const num = 42;                // Number (int + float đều là Number)
const big = 9007199254740991n; // BigInt
const bool = true;             // Boolean
const nothing = null;          // Null (intentional empty)
const notDefined = undefined;  // Undefined (chưa gán giá trị)
const sym = Symbol("id");      // Symbol (unique identifier)

// typeof
typeof "hello"    // "string"
typeof 42         // "number"
typeof true       // "boolean"
typeof null       // "object" 😱 (bug lịch sử, không sửa được)
typeof undefined  // "undefined"
typeof []         // "object"
typeof {}         // "object"

// Kiểm tra chính xác
Array.isArray([1,2,3])  // true
```

---

## 2. Strings

```javascript
const name = "An";
const greeting = `Xin chào ${name}!`;  // Template literal ⭐

// Methods
"hello".toUpperCase()           // "HELLO"
"Hello World".split(" ")       // ["Hello", "World"]
"  hello  ".trim()             // "hello"
"hello".includes("ell")        // true
"hello".startsWith("he")       // true
"hello".slice(1, 3)            // "el"
"hello".replace("l", "r")     // "herro" (chỉ cái đầu)
"hello".replaceAll("l", "r")  // "herro" (tất cả)
"ha".repeat(3)                 // "hahaha"
"hello".padStart(10, "0")     // "00000hello"
```

---

## 3. Arrays

```javascript
const fruits = ["táo", "cam", "xoài"];

// Thêm/xóa
fruits.push("dưa");           // Thêm cuối → ["táo","cam","xoài","dưa"]
fruits.pop();                  // Xóa cuối → trả "dưa"
fruits.unshift("lê");         // Thêm đầu
fruits.shift();                // Xóa đầu
fruits.splice(1, 1, "bưởi");  // Xóa 1 tại index 1, thêm "bưởi"

// Tìm kiếm
fruits.includes("cam")        // true
fruits.indexOf("cam")         // 1
fruits.find(f => f.length > 3)  // "xoài" (phần tử đầu tiên thỏa)
fruits.findIndex(f => f === "cam")  // 1

// Transform (KHÔNG thay đổi mảng gốc!) ⭐
const nums = [1, 2, 3, 4, 5];

nums.map(n => n * 2)             // [2, 4, 6, 8, 10]
nums.filter(n => n > 2)          // [3, 4, 5]
nums.reduce((sum, n) => sum + n, 0)  // 15
nums.every(n => n > 0)           // true (tất cả > 0?)
nums.some(n => n > 4)            // true (có ít nhất 1 > 4?)
nums.flat()                      // Flatten nested arrays
nums.sort((a, b) => a - b)      // Sắp xếp tăng dần

// Chaining
const result = users
    .filter(u => u.age >= 18)
    .map(u => u.name)
    .sort();

// Destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];
// first = 1, second = 2, rest = [3, 4, 5]

// Spread
const merged = [...arr1, ...arr2];
const copy = [...original];
```

---

## 4. Objects

```javascript
const user = {
    name: "An",
    age: 25,
    skills: ["JS", "React"],
    address: {
        city: "Hồ Chí Minh",
    },
    greet() {
        return `Xin chào, tôi là ${this.name}`;
    },
};

// Truy cập
user.name               // "An"
user["name"]            // "An" (dynamic key)
user.address.city       // "Hồ Chí Minh"

// Optional chaining ⭐
user.phone?.number      // undefined (không lỗi!)
user.getAddress?.()     // undefined

// Nullish coalescing ⭐
const port = config.port ?? 3000;  // 3000 nếu port là null/undefined
// Khác ||: 0 ?? 3000 = 0, nhưng 0 || 3000 = 3000

// Destructuring
const { name, age, skills: [firstSkill] } = user;

// Spread
const updated = { ...user, age: 26, role: "admin" };

// Object methods
Object.keys(user)       // ["name", "age", "skills", "address", "greet"]
Object.values(user)     // ["An", 25, [...], {...}, fn]
Object.entries(user)    // [["name","An"], ["age",25], ...]
Object.assign({}, user) // Shallow copy
```

---

## 5. Functions

```javascript
// Function declaration (hoisted)
function add(a, b) {
    return a + b;
}

// Arrow function ⭐ (không hoisted)
const multiply = (a, b) => a * b;
const square = x => x * x;         // 1 param: không cần ()
const getUser = () => ({ name: "An" }); // Return object: wrap ()

// Default params
function greet(name = "World") {
    return `Hello, ${name}!`;
}

// Rest params
function sum(...numbers) {
    return numbers.reduce((a, b) => a + b, 0);
}
sum(1, 2, 3, 4)  // 10

// Closure — hàm "nhớ" biến bên ngoài
function counter() {
    let count = 0;
    return {
        increment: () => ++count,
        getCount: () => count,
    };
}
const c = counter();
c.increment();    // 1
c.increment();    // 2
c.getCount();     // 2
```

---

## 6. Async/Await — Bất đồng bộ

```javascript
// Promise
function fetchUser(id) {
    return fetch(`/api/users/${id}`)
        .then(res => res.json())
        .catch(err => console.error(err));
}

// Async/Await ⭐ (đọc dễ hơn)
async function fetchUser(id) {
    try {
        const res = await fetch(`/api/users/${id}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (error) {
        console.error("Fetch failed:", error);
    }
}

// Song song
const [users, posts] = await Promise.all([
    fetch("/api/users").then(r => r.json()),
    fetch("/api/posts").then(r => r.json()),
]);

// Promise.allSettled — không fail nếu 1 promise reject
const results = await Promise.allSettled([
    fetch("/api/users"),
    fetch("/api/broken"),  // Lỗi nhưng không ảnh hưởng users
]);
```

---

## 7. ES6+ Modern Features

```javascript
// Destructuring
const { name, ...rest } = user;
const [first, ...others] = array;

// Spread & Rest
const merged = { ...obj1, ...obj2 };
const newArr = [...arr1, newItem, ...arr2];

// Optional chaining & Nullish coalescing
const city = user?.address?.city ?? "Unknown";

// Map & Set
const map = new Map();
map.set("key", "value");
map.get("key");     // "value"
map.has("key");     // true

const set = new Set([1, 2, 2, 3]);  // {1, 2, 3}

// for...of (iterables), for...in (object keys)
for (const item of array) { ... }
for (const key in object) { ... }

// Modules
export function add(a, b) { return a + b; }
export default class App {}
import App, { add } from './app.js';

// Classes
class Animal {
    #name;  // Private field (ES2022)

    constructor(name) {
        this.#name = name;
    }

    speak() {
        return `${this.#name} makes a sound`;
    }
}

class Dog extends Animal {
    speak() {
        return `${super.speak()} — Woof!`;
    }
}
```

---

## Các lỗi thường gặp

```javascript
// ❌ == vs ===
0 == ""       // true  😱 (type coercion!)
0 === ""      // false ✅ (strict equality)
null == undefined  // true
null === undefined // false
// ✅ LUÔN dùng ===

// ❌ this trong arrow function
const obj = {
    name: "An",
    greet: () => console.log(this.name),  // this = window, không phải obj!
};
// ✅ Dùng regular function cho methods
const obj = {
    name: "An",
    greet() { console.log(this.name); },  // this = obj ✅
};

// ❌ Floating point
0.1 + 0.2 === 0.3   // false! (0.30000000000000004)
// ✅ So sánh: Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON
```

---

## Bài tập thực hành

- [ ] Implement `debounce(fn, delay)` và `throttle(fn, delay)`
- [ ] Viết `deepClone(obj)` — clone sâu object lồng nhau
- [ ] Fetch API: lấy users từ JSONPlaceholder → hiển thị danh sách
- [ ] Implement simple Promise từ đầu (resolve, then, catch)

---

## Tài nguyên thêm

- [MDN JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) — Reference #1
- [JavaScript.info](https://javascript.info/) — Modern tutorial
- [You Don't Know JS](https://github.com/getify/You-Dont-Know-JS) — Deep understanding
