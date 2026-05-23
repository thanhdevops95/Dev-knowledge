# Hướng dẫn Web Development Cơ bản

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Tổng hợp kiến thức HTML, CSS, JavaScript cơ bản để xây dựng trang web.

---

## 🏗️**HTML CƠ BẢN**

### Cấu trúc HTML

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tiêu đề trang</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>Header</header>
    <main>Nội dung chính</main>
    <footer>Footer</footer>
    
    <script src="script.js"></script>
</body>
</html>
```

### Thẻ thường dùng

| Thẻ | Mô tả |
|-----|-------|
| `<h1>` - `<h6>` | Tiêu đề |
| `<p>` | Đoạn văn |
| `<a href="">` | Link |
| `<img src="">` | Hình ảnh |
| `<div>` | Container block |
| `<span>` | Container inline |
| `<ul>`, `<ol>`, `<li>` | Danh sách |
| `<table>`, `<tr>`, `<td>` | Bảng |
| `<form>`, `<input>`, `<button>` | Form |
| `<header>`, `<nav>`, `<main>`, `<footer>` | Semantic |

### Form cơ bản

```html
<form action="/submit" method="POST">
    <label for="name">Tên:</label>
    <input type="text" id="name" name="name" required>
    
    <label for="email">Email:</label>
    <input type="email" id="email" name="email">
    
    <label for="password">Mật khẩu:</label>
    <input type="password" id="password" name="password">
    
    <label for="message">Tin nhắn:</label>
    <textarea id="message" name="message"></textarea>
    
    <select name="country">
        <option value="vn">Việt Nam</option>
        <option value="us">USA</option>
    </select>
    
    <input type="checkbox" id="agree" name="agree">
    <label for="agree">Đồng ý điều khoản</label>
    
    <button type="submit">Gửi</button>
</form>
```

---

## 🎨**CSS CƠ BẢN**

### Cú pháp

```css
selector {
    property: value;
}

/* Ví dụ */
h1 {
    color: blue;
    font-size: 24px;
}
```

### Selectors

```css
/* Element */
p { color: black; }

/* Class */
.container { width: 100%; }

/* ID */
#header { background: #333; }

/* Descendant */
.container p { margin: 10px; }

/* Child */
.container > p { padding: 5px; }

/* Attribute */
input[type="text"] { border: 1px solid #ccc; }

/* Pseudo-class */
a:hover { color: red; }
button:active { background: blue; }
li:first-child { font-weight: bold; }
li:nth-child(2n) { background: #f0f0f0; }

/* Pseudo-element */
p::first-line { font-weight: bold; }
p::before { content: "→ "; }
```

### Box Model

```css
.box {
    /* Content */
    width: 200px;
    height: 100px;
    
    /* Padding (trong) */
    padding: 10px;
    padding: 10px 20px;           /* top-bottom | left-right */
    padding: 10px 20px 30px 40px; /* top | right | bottom | left */
    
    /* Border */
    border: 1px solid #ccc;
    border-radius: 5px;
    
    /* Margin (ngoài) */
    margin: 20px;
    margin: 0 auto; /* Center horizontally */
    
    /* Box-sizing */
    box-sizing: border-box; /* Width bao gồm padding + border */
}
```

### Flexbox

```css
.container {
    display: flex;
    
    /* Hướng */
    flex-direction: row;        /* default: ngang */
    flex-direction: column;     /* dọc */
    
    /* Căn theo trục chính */
    justify-content: flex-start;
    justify-content: center;
    justify-content: flex-end;
    justify-content: space-between;
    justify-content: space-around;
    
    /* Căn theo trục phụ */
    align-items: stretch;       /* default */
    align-items: flex-start;
    align-items: center;
    align-items: flex-end;
    
    /* Wrap */
    flex-wrap: wrap;
    
    /* Gap */
    gap: 10px;
}

.item {
    flex: 1;          /* Chia đều */
    flex-grow: 1;     /* Mở rộng */
    flex-shrink: 0;   /* Không co lại */
    flex-basis: 200px; /* Kích thước ban đầu */
}
```

### Grid

```css
.container {
    display: grid;
    
    /* Định nghĩa columns */
    grid-template-columns: 200px 1fr 200px;
    grid-template-columns: repeat(3, 1fr);
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    
    /* Định nghĩa rows */
    grid-template-rows: 100px auto 50px;
    
    /* Gap */
    gap: 20px;
    row-gap: 10px;
    column-gap: 20px;
}

.item {
    grid-column: 1 / 3;  /* Span từ cột 1 đến 3 */
    grid-row: 1 / 2;
}
```

### Responsive

```css
/* Mobile first */
.container {
    width: 100%;
}

/* Tablet */
@media (min-width: 768px) {
    .container {
        width: 750px;
    }
}

/* Desktop */
@media (min-width: 1024px) {
    .container {
        width: 960px;
    }
}

/* Large Desktop */
@media (min-width: 1200px) {
    .container {
        width: 1140px;
    }
}
```

---

## ⚡**JAVASCRIPT CƠ BẢN**

### Biến và kiểu dữ liệu

```javascript
// Biến
let name = "John";        // Có thể thay đổi
const PI = 3.14;          // Không thay đổi
var oldWay = "deprecated"; // Cách cũ

// Kiểu dữ liệu
let string = "Hello";
let number = 42;
let boolean = true;
let array = [1, 2, 3];
let object = { name: "John", age: 25 };
let nothing = null;
let notDefined = undefined;
```

### Functions

```javascript
// Function declaration
function greet(name) {
    return `Hello, ${name}!`;
}

// Arrow function
const greet = (name) => `Hello, ${name}!`;

// Arrow function nhiều dòng
const calculate = (a, b) => {
    const sum = a + b;
    return sum;
};
```

### Arrays

```javascript
const arr = [1, 2, 3, 4, 5];

// Thêm/xóa
arr.push(6);         // Thêm cuối
arr.pop();           // Xóa cuối
arr.unshift(0);      // Thêm đầu
arr.shift();         // Xóa đầu

// Duyệt
arr.forEach(item => console.log(item));

// Map - tạo array mới
const doubled = arr.map(x => x * 2);

// Filter - lọc
const even = arr.filter(x => x % 2 === 0);

// Find - tìm 1 phần tử
const found = arr.find(x => x > 3);

// Reduce - gộp
const sum = arr.reduce((acc, x) => acc + x, 0);

// Sort
arr.sort((a, b) => a - b);
```

### Objects

```javascript
const person = {
    name: "John",
    age: 25,
    greet() {
        return `Hello, I'm ${this.name}`;
    }
};

// Truy cập
console.log(person.name);
console.log(person["age"]);

// Destructuring
const { name, age } = person;

// Spread
const newPerson = { ...person, city: "HCM" };
```

### DOM Manipulation

```javascript
// Lấy element
const element = document.getElementById("myId");
const elements = document.getElementsByClassName("myClass");
const first = document.querySelector(".myClass");
const all = document.querySelectorAll(".myClass");

// Thay đổi nội dung
element.textContent = "New text";
element.innerHTML = "<strong>Bold</strong>";

// Thay đổi style
element.style.color = "red";
element.style.backgroundColor = "blue";

// Thay đổi class
element.classList.add("active");
element.classList.remove("active");
element.classList.toggle("active");

// Thay đổi attribute
element.setAttribute("data-id", "123");
element.getAttribute("data-id");

// Tạo element
const div = document.createElement("div");
div.textContent = "New div";
document.body.appendChild(div);
```

### Events

```javascript
// Event listener
button.addEventListener("click", function(event) {
    console.log("Clicked!");
});

// Arrow function
button.addEventListener("click", (e) => {
    e.preventDefault();  // Ngăn hành vi mặc định
    console.log(e.target);
});

// Events phổ biến
// click, dblclick, mouseenter, mouseleave
// keydown, keyup, keypress
// submit, change, input, focus, blur
// load, scroll, resize
```

### Async/Await

```javascript
// Fetch API
async function fetchData() {
    try {
        const response = await fetch('https://api.example.com/data');
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error('Error:', error);
    }
}

// POST request
async function postData() {
    const response = await fetch('https://api.example.com/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: 'John' })
    });
    return response.json();
}
```

---

## 📁**CẤU TRÚC PROJECT**

```
my-website/
├── index.html
├── about.html
├── contact.html
├── css/
│   ├── style.css
│   ├── reset.css
│   └── responsive.css
├── js/
│   ├── main.js
│   └── utils.js
├── images/
│   ├── logo.png
│   └── banner.jpg
└── fonts/
```

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
