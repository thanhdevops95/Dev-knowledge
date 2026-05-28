# 📝 Functional Programming — Lập trình hàm

> `[INTERMEDIATE]` — Tư duy khác biệt, code ít bug hơn

---

## FP là gì?

**Xây dựng phần mềm bằng cách kết hợp các hàm thuần (pure functions)** — không side effects, không thay đổi state.

```javascript
// Imperative (mệnh lệnh) — NHƯ THẾ NÀO
const numbers = [1, 2, 3, 4, 5];
const result = [];
for (let i = 0; i < numbers.length; i++) {
    if (numbers[i] % 2 === 0) {
        result.push(numbers[i] * 2);
    }
}
// result = [4, 8]

// Declarative (khai báo/FP) — LÀM GÌ
const result = numbers
    .filter(n => n % 2 === 0)
    .map(n => n * 2);
// result = [4, 8]
```

---

## 1. Pure Functions — Hàm thuần

```javascript
// ❌ Impure: phụ thuộc/thay đổi state bên ngoài
let tax = 0.1;
function getPrice(price) {
    return price + (price * tax);  // Phụ thuộc biến tax bên ngoài!
}
tax = 0.2;
getPrice(100); // Kết quả khác dù cùng input!

// ✅ Pure: cùng input → luôn cùng output, không side effects
function getPrice(price, taxRate) {
    return price + (price * taxRate);
}
getPrice(100, 0.1); // Luôn = 110, bất kể gọi bao nhiêu lần

// Lợi ích: Dễ test, dễ debug, dễ cache (memoize), threadsafe
```

---

## 2. Immutability — Không thay đổi dữ liệu

```javascript
// ❌ Mutable: thay đổi object gốc
const user = { name: 'An', age: 25 };
user.age = 26;  // Sửa trực tiếp!

// ✅ Immutable: tạo bản mới
const updatedUser = { ...user, age: 26 };

// Array
const numbers = [1, 2, 3];
// ❌
numbers.push(4);         // Mutate!
numbers.sort();           // Mutate!

// ✅
const added = [...numbers, 4];               // New array
const sorted = [...numbers].sort();           // Copy rồi sort
const removed = numbers.filter(n => n !== 2); // New array

// Nested objects
const state = {
    user: { name: 'An', address: { city: 'HN' } },
    posts: [1, 2, 3],
};

// ✅ Immutable update (nested)
const newState = {
    ...state,
    user: {
        ...state.user,
        address: { ...state.user.address, city: 'HCM' },
    },
};
// Với Immer (library): produce(state, draft => { draft.user.address.city = 'HCM' })
```

---

## 3. Higher-Order Functions

```javascript
// Function nhận function làm argument hoặc trả về function
// map, filter, reduce là higher-order functions

// Custom HOF: withLogging
function withLogging(fn) {
    return function (...args) {
        console.log(`Calling ${fn.name} with:`, args);
        const result = fn(...args);
        console.log(`Result:`, result);
        return result;
    };
}

const add = (a, b) => a + b;
const loggedAdd = withLogging(add);
loggedAdd(2, 3);
// Calling add with: [2, 3]
// Result: 5

// Partial application
function multiply(a) {
    return function (b) {
        return a * b;
    };
}
const double = multiply(2);
const triple = multiply(3);

double(5);  // 10
triple(5);  // 15
```

---

## 4. Function Composition

```javascript
// pipe: chạy từ trái sang phải
const pipe = (...fns) => (x) => fns.reduce((v, fn) => fn(v), x);

// compose: chạy từ phải sang trái
const compose = (...fns) => (x) => fns.reduceRight((v, fn) => fn(v), x);

// Ví dụ: Process user input
const trim = (s) => s.trim();
const toLower = (s) => s.toLowerCase();
const split = (sep) => (s) => s.split(sep);
const join = (sep) => (arr) => arr.join(sep);
const capitalize = (s) => s[0].toUpperCase() + s.slice(1);

const slugify = pipe(
    trim,
    toLower,
    split(' '),
    join('-'),
);

slugify('  Hello World  '); // "hello-world"

// Data pipeline
const processUsers = pipe(
    users => users.filter(u => u.active),
    users => users.map(u => ({ ...u, name: u.name.toUpperCase() })),
    users => users.sort((a, b) => a.name.localeCompare(b.name)),
);
```

---

## 5. Reduce — Swiss Army Knife

```javascript
// Sum
[1, 2, 3, 4, 5].reduce((acc, n) => acc + n, 0);  // 15

// Group by
const users = [
    { name: 'An', dept: 'Dev' },
    { name: 'Bình', dept: 'Design' },
    { name: 'Cường', dept: 'Dev' },
];

const grouped = users.reduce((acc, user) => {
    const key = user.dept;
    acc[key] = acc[key] || [];
    acc[key].push(user);
    return acc;
}, {});
// { Dev: [{An}, {Cường}], Design: [{Bình}] }

// Flatten
[[1, 2], [3, 4], [5]].reduce((acc, arr) => [...acc, ...arr], []);
// [1, 2, 3, 4, 5]
// Hoặc: [].flat() trong ES2019

// Pipe implementation chính là reduce!
const pipe = (...fns) => (x) => fns.reduce((v, fn) => fn(v), x);

// Count occurrences
const words = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple'];
const counts = words.reduce((acc, word) => {
    acc[word] = (acc[word] || 0) + 1;
    return acc;
}, {});
// { apple: 3, banana: 2, cherry: 1 }
```

---

## 6. Currying — Chuyên biệt hóa function

```javascript
// Curry: chuyển f(a, b, c) → f(a)(b)(c)
const curry = (fn) => {
    const arity = fn.length;
    return function curried(...args) {
        if (args.length >= arity) return fn(...args);
        return (...moreArgs) => curried(...args, ...moreArgs);
    };
};

const add = curry((a, b, c) => a + b + c);
add(1)(2)(3);    // 6
add(1, 2)(3);    // 6
add(1)(2, 3);    // 6

// Ứng dụng: tạo specialized functions
const log = curry((level, date, message) =>
    `[${level}] ${date}: ${message}`
);

const errorLog = log('ERROR');
const todayErrorLog = errorLog(new Date().toISOString());

todayErrorLog('Server crashed');
// [ERROR] 2026-03-04T...: Server crashed
```

---

## FP vs OOP — Khi nào dùng gì?

| Tình huống | Nên dùng |
|---|---|
| Data transformation, pipeline | FP (map/filter/reduce) |
| Complex domain model | OOP (classes, inheritance) |
| State management (React) | FP (immutable state) |
| API services, middleware | Cả hai |
| Game logic, simulations | OOP (entities, components) |

---

## Bài tập thực hành

- [ ] Viết pipe() và compose() từ đầu
- [ ] Refactor imperative loop → map/filter/reduce
- [ ] Implement curry() function
- [ ] Data pipeline: đọc JSON → filter → transform → output

---

## Tài nguyên thêm

- [Mostly Adequate Guide to FP](https://mostly-adequate.gitbook.io/mostly-adequate-guide/) — Free book
- [JavaScript Allongé](https://leanpub.com/javascriptallongesix/read) — FP in JS
- [Ramda.js](https://ramdajs.com/) — FP utility library
