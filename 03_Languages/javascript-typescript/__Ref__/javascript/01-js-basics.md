# ⚡ JavaScript — Ngôn ngữ của Web

> `[BEGINNER]` — Ngôn ngữ duy nhất chạy được trên trình duyệt

---

## JavaScript là gì?

- **Ngôn ngữ của web** — Chạy trực tiếp trên trình duyệt (không cần compile)
- **Đa năng** — Frontend, Backend (Node.js), Mobile (React Native), Desktop (Electron)
- **Động** (dynamically typed) — Không cần khai báo kiểu dữ liệu
- **Event-driven & Async** — Xử lý tốt các tác vụ bất đồng bộ

---

## Biến & Kiểu dữ liệu

```javascript
// Khai báo biến (dùng const và let, KHÔNG dùng var)
const PI = 3.14;          // Hằng số, không thể gán lại
let count = 0;             // Biến, có thể thay đổi

// Primitive types
let name = "Jesse";            // string
let age = 25;                  // number
let price = 9.99;              // number (không phân biệt int/float)
let isActive = true;           // boolean
let empty = null;              // null
let notDefined = undefined;    // undefined
let id = Symbol("id");         // Symbol (ES6)
let bigNum = 9007199254740993n; // BigInt

// Kiểm tra kiểu
typeof "hello"      // "string"
typeof 42           // "number"
typeof null         // "object" ← bug nổi tiếng của JS!
typeof undefined    // "undefined"
```

---

## Objects & Arrays

```javascript
// Object
const user = {
    name: "Jesse",
    age: 25,
    address: {
        city: "Hà Nội",
        country: "Việt Nam"
    },
    greet() {
        return `Xin chào, tôi là ${this.name}`;
    }
};

user.name           // "Jesse"
user["name"]        // "Jesse"
user.address.city   // "Hà Nội"

// Destructuring
const { name, age } = user;
const { address: { city } } = user;

// Spread operator
const updated = { ...user, age: 26 };

// Array
const fruits = ["apple", "banana", "cherry"];
fruits[0]               // "apple"
fruits.length           // 3
fruits.push("mango")    // Thêm vào cuối
fruits.pop()            // Xóa ở cuối
fruits.shift()          // Xóa ở đầu
fruits.unshift("kiwi")  // Thêm vào đầu

// Array Methods (QUAN TRỌNG!)
const numbers = [1, 2, 3, 4, 5];

numbers.map(n => n * 2)           // [2, 4, 6, 8, 10]
numbers.filter(n => n % 2 === 0)  // [2, 4]
numbers.reduce((sum, n) => sum + n, 0)  // 15
numbers.find(n => n > 3)          // 4
numbers.every(n => n > 0)         // true
numbers.some(n => n > 4)          // true
numbers.includes(3)               // true
numbers.slice(1, 3)               // [2, 3]
numbers.flat()                    // (dẹt mảng lồng nhau)
[...numbers, ...numbers]          // [1,2,3,4,5,1,2,3,4,5]
```

---

## Functions

```javascript
// Function declaration
function add(a, b) {
    return a + b;
}

// Arrow function (ES6)
const add = (a, b) => a + b;
const square = x => x ** 2;
const getUser = () => ({ name: "Jesse" });  // Trả về object

// Default parameters
function greet(name = "World") {
    return `Hello, ${name}!`;
}

// Rest parameters
function sum(...numbers) {
    return numbers.reduce((a, b) => a + b, 0);
}
sum(1, 2, 3, 4)  // 10

// Closures
function makeCounter() {
    let count = 0;
    return () => ++count;  // Truy cập được biến bên ngoài
}
const counter = makeCounter();
counter()  // 1
counter()  // 2
```

---

## Async JavaScript ⭐

```javascript
// Callback (cũ, dễ gây "callback hell")
fetchData(url, (error, data) => {
    if (error) handleError(error);
    else processData(data);
});

// Promise
fetch("https://api.example.com/users")
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error))
    .finally(() => console.log("Done"));

// Async/Await (hiện đại nhất, dễ đọc nhất)
async function getUser(id) {
    try {
        const response = await fetch(`/api/users/${id}`);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const user = await response.json();
        return user;
    } catch (error) {
        console.error("Lỗi:", error);
        throw error;
    }
}

// Chạy song song
const [users, posts] = await Promise.all([
    fetch("/api/users").then(r => r.json()),
    fetch("/api/posts").then(r => r.json())
]);

// Promise.allSettled — Không bị fail toàn bộ nếu 1 cái lỗi
const results = await Promise.allSettled([...]);
```

---

## ES6+ Features quan trọng

```javascript
// Template literals
const msg = `Xin chào ${name}, bạn ${age} tuổi`;

// Destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];
const { a, b, ...others } = { a: 1, b: 2, c: 3, d: 4 };

// Optional chaining (?.)
const city = user?.address?.city;      // Không bị lỗi nếu undefined
const len = arr?.length ?? 0;          // Nullish coalescing

// Modules
// math.js
export const PI = 3.14;
export function add(a, b) { return a + b; }
export default class Calculator { ... }

// main.js
import Calculator, { PI, add } from "./math.js";
import * as math from "./math.js";
```

---

## DOM Manipulation

```javascript
// Chọn element
const btn = document.getElementById("my-btn");
const title = document.querySelector("h1");
const items = document.querySelectorAll(".item");

// Thay đổi nội dung
title.textContent = "Tiêu đề mới";       // Text only
title.innerHTML = "<strong>Bold</strong>"; // HTML (cẩn thận XSS!)

// Thay đổi style
btn.classList.add("active");
btn.classList.remove("disabled");
btn.classList.toggle("highlight");
btn.style.color = "red";

// Events
btn.addEventListener("click", (event) => {
    event.preventDefault();       // Ngăn hành động mặc định
    event.stopPropagation();      // Ngăn event bubble lên
    console.log("Clicked!", event.target);
});

// Tạo và thêm element
const div = document.createElement("div");
div.className = "card";
div.textContent = "Nội dung";
document.body.appendChild(div);
```

---

## Bài tập thực hành

- [ ] **Todo App** — Thêm/xóa/đánh dấu task, lưu vào `localStorage`
- [ ] **Weather App** — Gọi API thời tiết hiển thị nhiệt độ, icon
- [ ] **Image Gallery** — Fetch ảnh từ API, hiển thị và filter
- [ ] **Quiz App** — Câu hỏi trắc nghiệm, đếm điểm, timer

---

## Tài nguyên thêm

- [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide) — Tài liệu chính thức
- [javascript.info](https://javascript.info/) — Hướng dẫn đầy đủ, rõ ràng nhất
- [Eloquent JavaScript (free)](https://eloquentjavascript.net/) — Sách học JS hay
- [33 JS Concepts](https://github.com/leonardomso/33-js-concepts) — 33 khái niệm cần biết
