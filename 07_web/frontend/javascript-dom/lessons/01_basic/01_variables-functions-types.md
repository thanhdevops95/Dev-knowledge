# 🎓 Variables, Functions, Types — JS core syntax

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Prerequisites:** [What is JavaScript](00_what-is-javascript.md)

> 🎯 *Master core JS: **`let`/`const`/`var`** (chọn cái nào), **function** (regular vs arrow), **object** + **array** + **string** methods, **template literal**, **destructure + spread + rest**, **truthy/falsy**, **optional chaining `?.`** + **nullish `??`**. Sau bài này code JS hiện đại đúng chuẩn.*

## 🎯 Sau bài này bạn sẽ

- [ ] Khai báo biến với `let`/`const`/`var` đúng cách
- [ ] Hiểu **block scope** vs **function scope** + **hoisting**
- [ ] Viết **function** 4 cách + biết khi nào arrow vs regular
- [ ] Master **string** template literals + 10+ methods
- [ ] Master **array** + 15+ methods (`map`/`filter`/`reduce`/...)
- [ ] Master **object** + access + modify + iterate
- [ ] **Destructure** + **spread** + **rest** — modern JS
- [ ] **Truthy/falsy** + **`??`** + **`?.`** — bug-resistant code

---

## Tình huống — Bạn copy code Stack Overflow, dính bug

Bạn viết tính discount:

```javascript
var price = 100;
function calcDiscount(p) {
  if (p > 50) {
    var discount = 0.1;
  }
  return p * discount;    // ← UNDEFINED?
}
console.log(calcDiscount(60));    // 6
console.log(calcDiscount(40));    // NaN  ← BUG
```

Bạn ngơ:
- `var` thay vì `let` đâu khác?
- Sao truy cập `discount` ngoài `if` block được mà có giá trị undefined?
- **Hoisting** là gì?

Senior bảo:
> *"Bạn dính 3 bug đời JS cũ. Modern JS chỉ `let`/`const`, không bao giờ `var`. Plus chục technique nữa (destructure, arrow, optional chaining...) tăng productivity 10x."*

→ Bài này dạy đầy đủ core JS modern.

---

## 1️⃣ Variables — `let` / `const` / `var`

### Modern (ES6+) — chỉ dùng 2 cái

ES6 (2015) thêm `let` + `const` thay cho `var` legacy. Quy tắc đơn giản: **`const` default**, dùng `let` khi cần reassign, **không bao giờ `var`** nữa. Cú pháp đối xứng dễ nhớ:

```javascript
let count = 0;            // ← Mutable, block-scoped
const PI = 3.14;          // ← Immutable, block-scoped

count = 1;                 // OK
PI = 4;                    // TypeError: Assignment to constant
```

### `var` — legacy, **TRÁNH**

`var` từ thời JS 1995 — function-scoped (không phải block-scoped), hoisted với giá trị `undefined`, có thể re-declare silent. Đây là nguồn bug khó debug nhất. Khi đọc code cũ sẽ gặp, nhưng KHÔNG dùng cho code mới:

```javascript
var x = 5;                 // Function-scoped, hoisted
```

### So sánh

Bảng so sánh 3 keyword khai báo biến — 5 trục quan trọng nhất quyết định "khi nào dùng cái nào". `var` thua mọi trục → không dùng cho code mới:

| Aspect | `var` | `let` | `const` |
|---|---|---|---|
| Scope | Function | Block (`{}`) | Block |
| Reassign | ✅ | ✅ | ❌ |
| Re-declare | ✅ (silent) | ❌ | ❌ |
| Hoisted | ✅ (init `undefined`) | ✅ (TDZ) | ✅ (TDZ) |
| Use 2026 | ❌ | ✅ | ✅ |

→ **Quy tắc 2026**: **`const` default**, dùng `let` khi cần reassign. **KHÔNG bao giờ `var`**.

### Block scope vs Function scope

Đây là khác biệt **cốt lõi** giữa `var` và `let`/`const`. Block scope (`{}`) là chuẩn của hầu hết ngôn ngữ modern (Java, C, Python with). `var` leak ra ngoài block — bug khó debug:

```javascript
// var = function-scoped
function f() {
  if (true) {
    var x = 5;
  }
  console.log(x);   // 5 — leak ra ngoài block
}

// let = block-scoped
function f() {
  if (true) {
    let x = 5;
  }
  console.log(x);   // ReferenceError — x không tồn tại
}
```

### Hoisting — Tại sao `var` confuse

JS có cơ chế **hoisting** — declaration được "kéo lên đầu function". Với `var`, biến tồn tại nhưng giá trị `undefined` trước khi assign. Với `let`/`const`, vào "TDZ" → access trước declare = `ReferenceError`:

```javascript
console.log(x);      // undefined (KHÔNG error)
var x = 5;

// Tương đương:
var x;               // Declaration hoisted
console.log(x);      // undefined
x = 5;
```

→ `var` declaration **moved to top of function**, value gán tại chỗ. `let`/`const` cũng hoist nhưng trong **TDZ** (Temporal Dead Zone) → access trước declare = `ReferenceError`.

```javascript
console.log(y);      // ReferenceError: Cannot access 'y' before initialization
let y = 5;
```

→ TDZ = safer behavior.

### Const với object — vẫn mutable!

```javascript
const obj = { name: "Nguyen Van A" };
obj.name = "Le Van B";    // OK — chỉ binding immutable, không phải value
obj.age = 28;        // OK

obj = {};            // ❌ TypeError — đổi binding
```

→ `const` cho **reference object** = tham chiếu cố định, nội dung object vẫn đổi được. Để thực sự immutable: `Object.freeze(obj)`.

### Bạn fix bug

```javascript
const PRICE = 100;
function calcDiscount(p) {
  const discount = p > 50 ? 0.1 : 0;    // ← ternary, không if-block
  return p * discount;
}
console.log(calcDiscount(60));    // 6
console.log(calcDiscount(40));    // 0 ← ĐÚNG
```

---

## 2️⃣ Functions — 4 cách viết

### 1. Function declaration

```javascript
function add(a, b) {
  return a + b;
}
add(1, 2);    // 3
```

→ **Hoisted toàn bộ** — gọi trước khi declare OK.

### 2. Function expression

```javascript
const add = function(a, b) {
  return a + b;
};
```

→ Variable `add` hoisted (TDZ), function value gán runtime.

### 3. Arrow function (ES6) — **modern default**

```javascript
const add = (a, b) => a + b;             // Implicit return
const square = x => x * x;                // 1 param không cần ()
const greet = () => console.log("hi");    // No param

// Multi-line
const calc = (a, b) => {
  const sum = a + b;
  return sum * 2;
};

// Trả object cần wrap ()
const make = (name, age) => ({ name, age });
```

### 4. Method shorthand (object/class)

```javascript
const user = {
  name: "Nguyen Van A",
  greet() {
    return `Hi, ${this.name}`;
  }
};
```

### Arrow vs Regular — Khác biệt QUAN TRỌNG

| Aspect | Regular `function` | Arrow `=>` |
|---|---|---|
| `this` | Own `this` (depend caller) | **Inherit** từ scope ngoài |
| `arguments` | Có | Không (dùng `...rest`) |
| Constructor (`new`) | OK | ❌ Error |
| Hoisted | ✅ (declaration) | ❌ (expression) |
| Method trong object | OK | `this` sẽ là outer scope (gotcha) |

### `this` gotcha — Khi nào arrow, khi nào regular?

```javascript
const user = {
  name: "Nguyen Van A",

  greetRegular: function() {
    console.log(this.name);    // "Nguyen Van A" — this = user
  },

  greetArrow: () => {
    console.log(this.name);    // undefined — this = window/global
  }
};
```

→ **Quy tắc**:
- **Method trong object/class** → `function` (regular) để có `this`.
- **Callback** (event handler, setTimeout, map) → `arrow` (tránh `this` lẫn).

```javascript
class Counter {
  constructor() {
    this.count = 0;
  }

  // ✅ Arrow callback giữ this
  start() {
    setInterval(() => {
      this.count++;     // this = Counter instance
      console.log(this.count);
    }, 1000);
  }

  // ❌ Regular function → this = undefined trong setInterval
  startBad() {
    setInterval(function() {
      this.count++;     // this = global, count = NaN
    }, 1000);
  }
}
```

### Default parameters + rest

```javascript
function greet(name = "World", greeting = "Hello") {
  return `${greeting}, ${name}!`;
}
greet();              // "Hello, World!"
greet("Nguyen Van A");        // "Hello, Nguyen Van A!"

// Rest parameter
function sum(...nums) {
  return nums.reduce((a, b) => a + b, 0);
}
sum(1, 2, 3, 4);      // 10
```

---

## 3️⃣ Strings + Template literals

### Concat cũ

```javascript
const name = "Nguyen Van A";
const greeting = "Hello, " + name + "!";
```

### Template literal (ES6) — backtick `` ` ``

```javascript
const name = "Nguyen Van A";
const greeting = `Hello, ${name}!`;            // Interpolation

const html = `
  <div>
    <h1>${name}</h1>
    <p>Welcome ${name}!</p>
  </div>
`;                                              // Multi-line
```

→ **Default 2026**. Sạch hơn concat `+`.

### String methods top

```javascript
"Hello World".length              // 11
"Hello".toUpperCase()              // "HELLO"
"Hello".toLowerCase()              // "hello"
"  hi  ".trim()                     // "hi"
"a,b,c".split(",")                  // ["a", "b", "c"]
["a","b"].join("-")                 // "a-b"
"Hello".includes("ell")             // true
"Hello".startsWith("He")            // true
"Hello".endsWith("lo")              // true
"Hello".replace("l", "L")           // "HeLlo" (1st match)
"Hello".replaceAll("l", "L")        // "HeLLo"
"Hello".slice(1, 4)                 // "ell"
"Hello".indexOf("l")                // 2
"abc".repeat(3)                     // "abcabcabc"
"5".padStart(3, "0")                // "005"
```

### String to number

```javascript
Number("42")           // 42
parseInt("42px", 10)    // 42 — base 10
parseFloat("3.14")      // 3.14
+"42"                    // 42 (unary)

(42).toString()         // "42"
(42).toFixed(2)         // "42.00"
```

---

## 4️⃣ Arrays — Master 15+ methods

### Create + access

```javascript
const arr = [1, 2, 3];
arr[0]                 // 1
arr.length             // 3
arr[arr.length - 1]    // 3 (last)
arr.at(-1)             // 3 (modern, negative index)
```

### Mutate methods

```javascript
arr.push(4)            // Add cuối → [1,2,3,4]
arr.pop()              // Remove cuối → returns 4, arr = [1,2,3]
arr.unshift(0)         // Add đầu → [0,1,2,3]
arr.shift()            // Remove đầu → returns 0
arr.splice(1, 1)       // Remove 1 element at index 1
arr.splice(1, 0, 5)    // Insert 5 at index 1
arr.reverse()          // Mutate reverse
arr.sort()              // Mutate sort
```

### **Immutable methods (recommended)** — return new array

```javascript
const nums = [1, 2, 3, 4, 5];

// map — transform each
nums.map(x => x * 2)              // [2, 4, 6, 8, 10]

// filter — keep matching
nums.filter(x => x > 2)            // [3, 4, 5]

// reduce — fold to single value
nums.reduce((acc, x) => acc + x, 0)    // 15 (sum)

// find — first match
nums.find(x => x > 2)              // 3

// findIndex
nums.findIndex(x => x > 2)         // 2

// some / every
nums.some(x => x > 4)              // true (ít nhất 1)
nums.every(x => x > 0)             // true (tất cả)

// includes
nums.includes(3)                    // true

// flat / flatMap
[[1,2],[3,4]].flat()                // [1,2,3,4]
nums.flatMap(x => [x, x*2])         // [1,2,2,4,3,6,4,8,5,10]

// Chain
nums.filter(x => x > 2)
    .map(x => x * 10)
    .reduce((a, b) => a + b, 0)     // 120

// Immutable sort + reverse (ES2023)
nums.toSorted()                      // new array sorted
nums.toReversed()                    // new array reversed
```

→ **Quy tắc 2026**: prefer **immutable** methods (`map`/`filter`/`reduce`) — functional style, dễ debug.

### Iterate

```javascript
// for-of (modern)
for (const x of nums) {
  console.log(x);
}

// forEach (callback)
nums.forEach((x, i) => console.log(i, x));

// for-in — ❌ avoid for array (iterate keys, slow)
```

---

## 5️⃣ Objects — Key-value store

### Create + access

```javascript
const user = {
  name: "An",
  age: 28,
  "full name": "Nguyen Van A",
};

user.name              // "An" — dot notation
user["full name"]      // "Nguyen Van A" — bracket (key có space)
user.email              // undefined (chưa có)
```

### Modify

```javascript
user.age = 29;          // Update
user.city = "Hanoi";    // Add new
delete user.city;       // Remove
```

### Method shorthand

```javascript
const obj = {
  name: "Nguyen Van A",
  greet() {              // ← shorthand for greet: function() {...}
    return `Hi ${this.name}`;
  }
};
```

### Computed property name

```javascript
const key = "age";
const obj = {
  name: "Nguyen Van A",
  [key]: 28,              // → { name: "Nguyen Van A", age: 28 }
};
```

### Shorthand property

```javascript
const name = "Nguyen Van A";
const age = 28;
const user = { name, age };    // ← Same as { name: name, age: age }
```

### Iterate

```javascript
const user = { name: "Nguyen Van A", age: 28 };

Object.keys(user)              // ["name", "age"]
Object.values(user)             // ["Nguyen Van A", 28]
Object.entries(user)            // [["name","Nguyen Van A"], ["age",28]]

for (const [key, value] of Object.entries(user)) {
  console.log(key, value);
}
```

### Spread / merge

```javascript
const base = { a: 1, b: 2 };
const extra = { b: 99, c: 3 };

const merged = { ...base, ...extra };
// → { a: 1, b: 99, c: 3 }    (extra override base)

const clone = { ...base };      // Shallow copy
```

---

## 6️⃣ Destructure + Spread + Rest

### Array destructure

```javascript
const [a, b, c] = [1, 2, 3];          // a=1, b=2, c=3
const [first, , third] = [1, 2, 3];   // skip element

// Default value
const [x = 10] = [];                   // x=10

// Rest
const [head, ...tail] = [1, 2, 3, 4];
// head=1, tail=[2,3,4]

// Swap
let m = 1, n = 2;
[m, n] = [n, m];                       // m=2, n=1
```

### Object destructure

```javascript
const user = { name: "Nguyen Van A", age: 28, city: "Hanoi" };

const { name, age } = user;
// name="Nguyen Van A", age=28

// Rename
const { name: userName } = user;
// userName="Nguyen Van A"

// Default
const { email = "no@email.com" } = user;
// email="no@email.com"

// Rest
const { name, ...rest } = user;
// name="Nguyen Van A", rest={age: 28, city: "Hanoi"}

// Function param destructure (very common)
function greet({ name, age = 0 }) {
  return `Hi ${name}, ${age}`;
}
greet({ name: "Nguyen Van A" });          // "Hi Nguyen Van A, 0"
```

### Spread operator

```javascript
// Array
const a = [1, 2];
const b = [3, 4];
const combined = [...a, ...b];          // [1,2,3,4]
const clone = [...a];                    // shallow copy

// Object
const base = { x: 1 };
const extended = { ...base, y: 2 };      // { x:1, y:2 }

// Function args
const max = Math.max(...[1, 2, 3, 4]);   // 4 (spread array → args)
```

### Rest parameter

```javascript
function sum(...nums) {
  return nums.reduce((a, b) => a + b, 0);
}
sum(1, 2, 3, 4);        // 10
```

→ Spread + rest cùng dùng `...`, khác context:
- **Rest** (function param) — gom nhiều arg thành array.
- **Spread** (call site) — phun array thành nhiều arg.

---

## 7️⃣ Truthy/Falsy + Modern operators

### 6 falsy values trong JS

```javascript
if (value) { ... }       // value falsy → skip

// Falsy:
false
0
0n             // bigint zero
""             // empty string
null
undefined
NaN

// Mọi thứ khác = truthy (kể cả [], {}, "0", "false")
```

### `||` OR — fallback (truthy)

```javascript
const name = userName || "Anonymous";
// Nếu userName falsy → "Anonymous"

const port = process.env.PORT || 3000;
```

→ Vấn đề: `0`, `""` cũng fallback (có thể không muốn).

### `??` Nullish coalescing (ES2020)

```javascript
const port = process.env.PORT ?? 3000;
// Chỉ fallback nếu null/undefined

const count = userCount ?? 0;     // 0 OK, "" OK, chỉ null/undefined fallback
```

→ **Modern preference**: `??` cho default value khi 0/"" hợp lệ.

### `?.` Optional chaining (ES2020)

```javascript
const user = { name: "Nguyen Van A", address: null };

user.address.city           // ❌ TypeError
user.address?.city          // ✅ undefined (safe access)
user.profile?.image?.url    // ✅ chain
user.greet?.()              // ✅ call function chỉ nếu tồn tại
user.items?.[0]              // ✅ array access
```

→ Default 2026 cho mọi nested access uncertain.

### `&&` AND

```javascript
const isLoggedIn = true;
const user = isLoggedIn && getCurrentUser();
// Nếu isLoggedIn truthy → user = getCurrentUser(), else = false
```

→ Hữu ích short-circuit. JSX dùng nhiều.

### Compound assignment

```javascript
x ||= "default";       // Same: x = x || "default"
x ??= "default";       // Same: x = x ?? "default"
x &&= newValue;         // Same: x = x && newValue
```

---

## 8️⃣ Bạn viết lại code modern

```javascript
// Modern JS — discount calculator
const PRODUCTS = [
  { id: 1, name: "iPhone", price: 25_000_000 },
  { id: 2, name: "AirPods", price: 5_000_000 },
  { id: 3, name: "Cable", price: 200_000 },
];

const calcDiscount = (price, threshold = 50_000_000) =>
  price > threshold ? 0.1 : 0;

const applyDiscount = product => ({
  ...product,
  discount: calcDiscount(product.price),
  final: product.price * (1 - calcDiscount(product.price)),
});

const final = PRODUCTS.map(applyDiscount);

// Total
const total = final.reduce((sum, p) => sum + p.final, 0);

console.log(`Total: ${total.toLocaleString()}đ`);
```

→ Modern style: `const`, arrow, immutable, spread, destructure, template, optional fallback.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **`var`** — function-scoped + hoist = bug. Modern: `const` default, `let` khi cần.
2. **Arrow trong method object** — `this` không phải object. Method dùng `function`/shorthand.
3. **Mutate array gốc** — `arr.sort()` mutate. Trong React/Redux gây bug. Dùng `arr.toSorted()` hoặc `[...arr].sort()`.
4. **`||` cho default khi 0/"" hợp lệ** — `count || 10` returns 10 khi count=0. Dùng `??`.
5. **`==` thay `===`** — type coercion bug. Luôn `===`.

---

## 🧠 Tự kiểm tra (Self-check)

1. Khác `const` và `let`? Khi nào dùng cái nào?
2. Method object dùng arrow vs regular — chọn cái nào, vì sao?
3. Viết function: input array number, output sum (immutable, modern).
4. `arr.map()` vs `arr.forEach()` — khác sao?
5. `0 || "default"` vs `0 ?? "default"` — kết quả?

<details>
<summary>Gợi ý đáp án</summary>

1. **`const`** = immutable binding (không reassign), block-scoped. **`let`** = mutable binding, block-scoped. Quy tắc: **`const` default**, `let` khi value sẽ đổi (counter, loop variable). Lưu ý: `const` cho object vẫn cho mutate nội dung.

2. **Method** trong object/class → dùng **regular function** hoặc method shorthand `greet() {...}`. Lý do: `this` phải là object instance. **Arrow** trong method → `this` là outer scope (thường `undefined`/`window`).

3. ```javascript
   const sum = nums => nums.reduce((a, b) => a + b, 0);
   ```

4. **`map`** return **new array** với value đã transform — functional, chain được. **`forEach`** chỉ iterate side-effect, **return undefined** — không chain. Modern prefer `map` khi transform, `forEach` khi pure side-effect (log).

5. **`0 || "default"`** → `"default"` (0 là falsy → fallback). **`0 ?? "default"`** → `0` (0 không null/undefined → giữ). Nên dùng `??` khi 0 là valid value.
</details>

---

## ⚡ Cheatsheet

### Variables

```javascript
const x = 5;        // immutable binding
let y = 5;          // mutable
// ❌ Never: var
```

### Functions

```javascript
function add(a, b) { return a + b; }            // declaration
const add = (a, b) => a + b;                     // arrow
const obj = { greet() { return "hi"; } };        // method shorthand
function f(a = 1, ...rest) { ... }                // default + rest
```

### Array methods

```javascript
arr.map(fn)        arr.filter(fn)      arr.reduce(fn, init)
arr.find(fn)       arr.findIndex(fn)    arr.some(fn)  arr.every(fn)
arr.includes(x)    arr.flat()           arr.flatMap(fn)
arr.toSorted()      arr.toReversed()
```

### Object

```javascript
Object.keys(obj)    Object.values(obj)    Object.entries(obj)
const merged = { ...a, ...b }
const { name, age } = obj
```

### Destructure + spread

```javascript
const [a, b, ...rest] = arr
const { name, age = 0, ...rest } = obj
const newArr = [...arr1, ...arr2]
const newObj = { ...obj, override: 1 }
```

### Modern operators

```javascript
x?.y?.z           // optional chain
x ?? "default"    // nullish fallback
x ||= "default"    // assign if falsy
x ??= "default"    // assign if nullish
```

### Truthy/Falsy

```
Falsy: false  0  ""  null  undefined  NaN
Truthy: everything else (including [], {}, "0")
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **`let` / `const`** | Block-scoped declaration (ES6+) |
| **`var`** | Legacy function-scoped (avoid) |
| **Block scope** | `{}` boundary |
| **Hoisting** | Declaration moved to top |
| **TDZ** | Temporal Dead Zone — let/const access before declare = error |
| **Arrow function** | `() => ...` — không own `this` |
| **Template literal** | `` `Hello ${name}` `` |
| **Destructure** | `const {a, b} = obj` |
| **Spread (`...`)** | Phun array/object thành elements |
| **Rest (`...`)** | Gom args/elements thành array |
| **`??` nullish coalescing** | Default only when null/undefined |
| **`?.` optional chaining** | Safe access nested property |
| **Truthy/Falsy** | Implicit boolean conversion |
| **`map`/`filter`/`reduce`** | Immutable array transform |
| **Method shorthand** | `obj = { greet() {...} }` |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [JavaScript là gì? — Ngôn ngữ chính của browser](00_what-is-javascript.md)
- ➡️ **Bài tiếp theo:** [DOM Manipulation — JS điều khiển HTML](02_dom-manipulation.md)
- ↑ **Về cụm:** [javascript-dom README](../../README.md)

### 🌐 Tài nguyên tham khảo khác
- 📖 [MDN — Grammar and types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types)
- 📖 [javascript.info — Variables](https://javascript.info/variables)
- 📖 [Array methods chart](https://doesitmutate.xyz/) — mutate vs not
- 📖 [Modern JS Tutorial](https://javascript.info/) — comprehensive
- 📖 [Wes Bos: ES6 for everyone](https://es6.io/) — paid course

---

> 🎯 *Sau bài này bạn viết JS modern đúng chuẩn. Bài kế tiếp dạy **DOM manipulation** — JS modify HTML thực tế.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Bổ sung lời dẫn trước các mục Modern let/const, var legacy, So sánh, Block scope, Hoisting. Chuẩn hoá giá trị ví dụ trong code thành placeholder. Thêm mục Changelog.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `javascript-dom/` lesson 2/5. Cover: var vs let vs const + scope (function vs block) + hoisting + TDZ + functions (declaration vs expression vs arrow) + parameters (default/rest/destructure) + types (primitive vs reference) + closure intro.
