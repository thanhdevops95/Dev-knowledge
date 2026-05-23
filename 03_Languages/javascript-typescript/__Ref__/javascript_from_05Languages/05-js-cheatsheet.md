# 📋 JavaScript Cheatsheet — Tra cứu Snippet nhanh

> `[BEGINNER → INTERMEDIATE]` — Prerequisite: `01-js-basics.md`
> Bảng tổng hợp cú pháp ES6+ & DOM Manipulation thường dùng.

---

## 1. Biến & Cơ chế Scoping

| Cú pháp | Scope | Khởi tạo lại | Gắn lại giá trị (Re-assign) | Hoisting |
|---|---|---|---|---|
| `var name = "js"` | Function | Có | Có | Có (`undefined`) |
| `let age = 10` | Block `{}` | Không | Có | ReferenceError |
| `const PI = 3.14` | Block `{}` | Không | Không | ReferenceError |

```javascript
/* Mẹo: LUÔN DÙNG const. Nếu biết trước biến sẽ thay đổi → dùng let.
   Trừ code legacy, BỎ HẲN việc sử dụng var. */

// Tuyệt chiêu const với Object/Array (Tham chiếu)
const user = { name: "An" };
user.name = "Bình"; // ✅ OK (Giá trị trong vùng nhớ thay đổi)
user = { name: "Chi" }; // ❌ LỖI TypeError (Không trỏ tới vùng nhớ khác được)
```

---

## 2. Functions (Hàm)

| Loại hàm | Cú pháp | Keyword `this` | Dùng làm Constructor (new) |
|---|---|---|---|
| Mặc định | `function add(a, b) { return a+b; }` | Global / Object gọi nó | ✅ Được |
| Gán biến | `const add = function(a, b) { ... }` | Như trên | ✅ Được |
| Arrow (ES6) | `const add = (a, b) => a + b;` | Keo chặt với Context CHA | ❌ Lỗi |

```javascript
// Function Default Parameters
const greet = (name = "Khách", time = "Sáng") => `Chào buổi ${time}, ${name}!`;

// IIFE (Kích hoạt chạy ngay)
(function() {
  console.log("Tôi chạy một lần duy nhất lúc Load trang");
})();

// Trả về Object siêu tốc bằng Arrow Function
const createUser = (id) => ({ id, name: "Newbie" }); 
```

---

## 3. Mảng (Arrays) & Thủ thuật Hữu ích

```javascript
const arr = [1, 2, 3, 4, 5]; // Dữ liệu mẫu

// Cắt / Slicing (KHÔNG thay đổi mảng gốc)
arr.slice(1, 3); // Lấy item vị trí 1 và 2 -> [2, 3]

// Cắt / Nối (LÀM BIẾN ĐỔI mảng gốc)
arr.splice(2, 1); // Xóa 1 phần tử từ vị trí index 2 -> [1, 2, 4, 5]

// MAP, FILTER, REDUCE (The Holy Trinity)
const doubled = arr.map(x => x * 2); // [2,4,8,10]
const evens = arr.filter(x => x % 2 === 0); // [2,4]
const sum = arr.reduce((acc, current) => acc + current, 0); // 12

// SOME & EVERY (Kiểm tra true/false)
arr.some(x => x > 4); // true (Chỉ cần 1 cái đúng là kết thúc)
arr.every(x => x > 0); // true (TẤT CẢ phải đúng)

// Tìm kiếm
arr.find(x => x === 4); // Trả về 4 (Trái sang phải, lấy thằng đầu tiên)
arr.findIndex(x => x === 4); // Trả về vị trí 2
arr.includes(4); // true

// San phẳng (Flatten) mảng đa chiều
const matrix = [[1, 2], [3, 4], 5];
matrix.flat(); // [1, 2, 3, 4, 5]
```

---

## 4. ES6+ Destructuring & Spread Operators

```javascript
// Gỡ Data cực mạnh với Array/Object (Destructuring)
const user = { id: 1, name: "A", detail: { age: 20 } };
const { id, name: fullName, detail: { age } } = user; // 'A' thành fullName

// Lấy tham số Array
const rgb = [255, 128, 0];
const [red, green, blue] = rgb;

// Rest Operator (Gom phần thừa)
const [first, ...rest] = [1, 2, 3, 4]; // first=1, rest=[2,3,4]
const { id, ...others } = user; // Lấy các thuôc tính còn lại của object

// Spread Operator (Dải nén)
const arr1 = [1, 2];
const arr2 = [3, 4];
const combined = [...arr1, ...arr2]; // [1, 2, 3, 4]

// Sao chép nhanh biến object (Shallow copy)
const copyUser = { ...user, isStudent: true }; 
```

---

## 5. Xử lý Bất đồng bộ (Promises & Async/Await)

| Callback (Cũ) | Promise (Tốt) | Async/Await (Tốt nhất) |
|---|---|---|
| Callback Hell (Tam giác tử thần) | Dùng `.then().catch()` | Như code Đồng Bộ (Sạch, dễ đọc) |
| Khó Error Handling | Dễ bắt lỗi | Dùng `try...catch` |

```javascript
// Bọc code cũ bằng Promise chuẩn 
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Async/Await (Hiện đại)
async function fetchUser(userId) {
  try {
    const response = await fetch(`https://api.com/users/${userId}`);
    if (!response.ok) throw new Error("Mạng có vấn đề");
    
    const user = await response.json();
    return user;
  } catch (error) {
    console.error("Lỗi:", error.message);
  }
}

// Chạy SONG SONG nhiều Promises thay vì tuần tự (CỰC KỲ TỐI ƯU)
const [users, posts] = await Promise.all([
    fetch('/users').then(res => res.json()),
    fetch('/posts').then(res => res.json())
]);

// Tranh cướp, ai xong trước thì lấy
const quickest = await Promise.race([req1, req2]);

// Đợi tất cả dù gặp Error (ES2020)
const results = await Promise.allSettled([req1, req2]);
```

---

## 6. DOM Query & Event (Dành riêng cho Browser)

```javascript
// Lấy phần tử (Nên ưu tiên dùng querySelector)
document.getElementById('m-btn');
document.querySelector('.container > p'); // Lấy 1 phần tử Tương thích CSS Selector
document.querySelectorAll('li.item'); // Lấy TẤT CẢ (Trả về NodeList, có thể loop bằng forEach)

// Edit Classes
const box = document.querySelector('#box');
box.classList.add('active');
box.classList.remove('hidden');
box.classList.toggle('dark-mode'); // Có thì gỡ, không có thì thêm
box.classList.contains('active'); // Trả về true/false

// Tạo mới Node 
const li = document.createElement('li');
li.textContent = "Chữ thuần túy an toàn bảo mật"; // An toàn trước XSS
li.innerHTML = "<strong>In đậm</strong>"; // Render thẻ HTML
box.appendChild(li); // Ném li xuống CUỐI box
box.insertAdjacentHTML('afterbegin', '<div>Đầu tiên</div>');

// Lắng nghe Sự Kiện (Events)
box.addEventListener('click', (e) => {
   e.preventDefault(); // Ngăn hành vi mặc định (Submit form, Mở link)
   e.stopPropagation(); // Cản sếp (Ngăn sự kiện lan bong bóng DOM lên cha)
   console.log(e.target); // Phần tử người dùng Click TRỰC TIẾP
   console.log(e.currentTarget); // Chỗ đặt Event Listener (Tức là thẻ #box)
});
```

---

## 7. Các Snippet bá đạo một dòng (One-liners)

```javascript
// Loại bỏ object trùng trong Mảng dựa theo khóa duy nhất `id`
const uniqueUsers = [...new Map(users.map(u => [u.id, u])).values()];

// Loại bỏ Element rỗng/Lỗi trong Mảng Array
const falsiesBuster = [1, null, "A", "", false].filter(Boolean); // [1, "A"]

// Tráo vị trí siêu cấp Tốc Độ (Toán tử Mảng Swap)
let a = 1, b = 2;
[a, b] = [b, a]; // a=2, b=1

// Chạy hàm tùy chọn RÀO LỖI Nhanh (Optional Chaining ES2020)
const userName = apiResponse?.data?.user?.name || "Khách Vô Danh";

// Đổi Object thành Chuỗi Cụm (Query Params) URL
const params = { id: 1, s: "js" };
const urlParams = new URLSearchParams(params).toString(); // "id=1&s=js"
```
