# 📦 JS Modules Fundamentals — Module trong JavaScript

> `[BEGINNER → INTERMEDIATE]` — Prerequisite: hiểu cơ bản về JavaScript (`01-js-basics.md`).
> Tổng quan về cách JavaScript tổ chức mã nguồn (CJS, AMD, UMD, ESM).

---

## Tại sao cần Modules?

Trong những ngày đầu của web, mọi code JavaScript đều nằm trong các thẻ `<script>` và chia sẻ chung một **Global Scope** (phạm vi toàn cục). 

```html
<!-- KIỂU CŨ: Biến bị xung đột, thứ tự khai báo cực kỳ quan trọng -->
<script src="jquery.js"></script>
<script src="utils.js"></script>
<script src="app.js"></script> <!-- Nếu app.js gọi utils.js trước khi load, ứng dụng sập! -->
```

**Vấn đề giải quyết:**
1. **Tránh ô nhiễm Global Scope**: Mỗi module có một scope riêng biệt.
2. **Dependency Management**: Quản lý rõ ràng file nào phụ thuộc vào file nào.
3. **Reusability**: Đóng gói logic để tái sử dụng ở project khác.
4. **Maintainability**: Chia nhỏ file khổng lồ thành nhiều file nhỏ dễ quản lý.

---

## 1. Lịch sử các chuẩn Module trong JS

Trước khi JavaScript có tính năng module tích hợp sẵn (ES Modules - 2015), cộng đồng đã phải tự tạo ra các tiêu chuẩn:

| Tiêu chuẩn | Môi trường | Cú pháp chính | Đặc điểm |
|---|---|---|---|
| **IIFE** | Trình duyệt cũ | `(function(){ ... })()` | Dùng closure để giấu biến, tạo private scope. |
| **CommonJS (CJS)** | **Node.js** | `require()` / `module.exports` | Tải module **đồng bộ** (synchronous). Tốt cho Server. |
| **AMD** | Trình duyệt cũ | `define([...], function)` | Tải module **bất đồng bộ** (asynchronous). Dùng RequireJS. |
| **UMD** | Cả hai | `(function (root, factory)` | Chuẩn tương thích chéo (hoạt động với cả CJS, AMD và Global). |
| **ESM (ES6)** | **Hiện đại** (Cả 2) | `import` / `export` | Tiêu chuẩn chính thức của JavaScript. Hỗ trợ tĩnh (Static analysis). |

---

## 2. CommonJS (CJS) — Chuẩn của Node.js

Node.js sử dụng CommonJS làm chuẩn mặc định trong một thời gian dài. Việc loading file diễn ra theo kiểu **chặn đồng bộ (synchronous blocking)**, phù hợp cho server vì file đọc từ ổ cứng rất nhanh.

### Khai báo và xuất (Export)
```javascript
// math.js
const PI = 3.14159;

function add(a, b) {
  return a + b;
}

// Named export
exports.add = add;

// Default export (ghè đè toàn bộ module)
module.exports = {
  PI,
  add
};
```

### Nhập (Import)
```javascript
// app.js
const math = require('./math.js'); // Require trả về một object
console.log(math.add(2, 3));       // 5

// Có thể dùng destructuring
const { add, PI } = require('./math.js');
```

---

## 3. ES Modules (ESM) — Chuẩn hiện đại chuẩn hóa

ES Modules (ESM) được giới thiệu trong ES6 (2015). Đây là cách chính thức và được khuyến nghị cho cả Frontend (React, Vue) và Backend (Deno, modern Node.js). 

> **Khác biệt cốt lõi:** `import`/`export` là **static** (tĩnh). Parser của JS Engine biết file nào phụ thuộc file nào TRƯỚC khi thực thi code → Giúp Tree-shaking (loại bỏ code thừa) cực kỳ hiệu quả khi dùng Webpack/Rollup/Vite.

### Named Exports
Bạn có thể export nhiều giá trị từ một file.

```javascript
// utils.js
export const API_URL = "https://api.example.com";

export function formatDate(date) {
  return date.toISOString();
}

// Hoặc export cuối file
const a = 1, b = 2;
export { a, b };
```

Nhập Named Export (Yêu cầu phải viết đúng tên, nằm trong ngoặc nhọn `{}`):

```javascript
// app.js
import { API_URL, formatDate } from './utils.js';
import { a as firstItem } from './utils.js'; // Đổi tên khi import
```

### Default Exports
Mỗi file chỉ được phép có **1 Default Export duy nhất**. Thường dùng khi một module chỉ đại diện cho một class, một component, hoặc một hàm duy nhất.

```javascript
// User.js
export default class User {
  constructor(name) {
    this.name = name;
  }
}
```

Nhập Default Export (Có thể tự do đặt tên bất kỳ):
```javascript
// app.js
import MyCustomUser from './User.js'; // Không cần dấu {}
const user = new MyCustomUser("Aki");
```

### Kết hợp cả hai
```javascript
// react.js (minh họa)
export const useState = () => {};
export const useEffect = () => {};
export default function React() {};

// Khi import
import React, { useState, useEffect } from 'react';
```

---

## 4. Bật ESM trong Node.js

Mặc định Node.js coi mọi file `.js` là CommonJS. Để chạy ESM trong Node:

**Cách 1: Sửa package.json**
```json
// package.json
{
  "type": "module" 
}
```
*Lưu ý: Khi set `type: "module"`, để dùng CommonJS, bạn phải đổi đuôi file thành `.cjs`.*

**Cách 2: Đổi đuôi file**
Đổi đuôi file ESM của bạn thành `.mjs` (viết tắt của Module JS). Nó sẽ tự động được chạy dưới dạng ESM.

---

## 5. Dynamic Imports (Import động)

Khác với `import` tĩnh luôn phải để ở đầu file, `import()` động trả về một **Promise**. Dùng để Code Splitting, tải file khi được yêu cầu (như click vào nút).

```javascript
button.addEventListener('click', async () => {
    // Chỉ tải module auth.js khi user click login
    try {
        const authPlugin = await import('/modules/auth.js');
        authPlugin.login();
    } catch (err) {
        console.error("Lỗi khi tải module", err);
    }
});
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Cú pháp Sai | ✅ Cú pháp Đúng | Giải thích / Hậu quả |
|---|--------|---------|------------|
| 1 | `require` file ESM | Dùng `import()` tĩnh/động | CommonJS không thể đọc file ESM trực tiếp thông qua `require()`. |
| 2 | `<script src="app.js">` | `<script type="module" src="app.js">`| Browser sẽ văng lỗi `SyntaxError: Cannot use import statement outside a module` nếu thiếu `type="module"`. |
| 3 | `import add from './math'` (bị quên `Default`) | `import { add } from './math'` | Nhập hàm Named (được export bằng `export function`) nhưng lại dùng cú pháp của Default Import. |
| 4 | `import ... from 'file.js'` (đặt trong `if`) | Dùng Dynamic Import: `import('file.js')` | `import` tĩnh TRUYỀN THỐNG phải ở root (đầu file), không được đặt trong `if, for, function`. |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** Tạo 2 file `math.js` và `app.js`. Triển khai các hàm `add, subtract` bằng Export/Import của ESM chạy trên trình duyệt.
- [ ] **Bài 2 (Trung bình):** Setup một package Node.js có `"type": "module"`. Import thử thư viện `fs/promises` của Node.js.
- [ ] **Bài 3 (Khó):** Tạo nút HTML, viết mã bắt sự kiện click và sử dụng cú pháp Dynamic Import (`await import`) để render nội dung động từ 1 JS file khác.

---

## Tài nguyên thêm
- [MDN — JavaScript modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) - Tài liệu chuẩn từ Mozilla.
- [Node.js Docs - Modules: ECMAScript modules](https://nodejs.org/api/esm.html) - Setup ESM trong môi trường Node.
- [JavaScript Modules: A Beginner's Guide](https://www.freecodecamp.org/news/javascript-modules-a-beginner-s-guide-783f7d7a5fcc/) - Lịch sử cặn kẽ về module hóa trong JS.
