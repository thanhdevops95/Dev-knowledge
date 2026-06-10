# 🎓 DOM Manipulation — JS điều khiển HTML

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [Variables & Functions](01_variables-functions-types.md), [HTML Essentials](../../../html-css/lessons/01_basic/01_html-essentials.md)

> 🎯 *Master **DOM** — JS đại diện HTML trong memory. **`querySelector`** + family, **modify text/HTML/attribute/class**, **create + insert + remove element**, **`dataset`** (data-*), **forms**. Sau bài này JS làm trang động: add/remove/update element, không cần reload.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **DOM tree** — JS view của HTML
- [ ] Dùng **`querySelector` / `querySelectorAll`** chọn element
- [ ] Modify **text**, **HTML**, **attribute**, **classList**
- [ ] **Create + insert + remove** element (`createElement`, `append`)
- [ ] Đọc/ghi **form value** + **dataset** (data-*)
- [ ] Hiểu **NodeList vs HTMLCollection** + iterate
- [ ] Phân biệt **innerHTML** vs **textContent** (security)
- [ ] Templating với **`<template>`** tag

---

## Tình huống — Thêm sản phẩm vào giỏ hàng

Bạn muốn:
- Click button "+" → tăng số lượng trong giỏ hiển thị
- Click "Add" → thêm sản phẩm vào list giỏ + cập nhật total
- "Xóa" → remove khỏi list

Bạn thử jQuery cũ thấy nhiều site dùng:
```javascript
$('#cart-count').text(3);
$('.product').remove();
```

Senior chỉ:
> *"jQuery đã chết từ ~2018. Modern browser API thay thế hết. Không cần thư viện cho DOM cơ bản."*

Bạn ngơ:
- **Vanilla DOM API** modern thay jQuery thế nào?
- Sao **`querySelector`** đủ thay `$()`?
- **`innerHTML`** vs **`textContent`** chọn cái nào?
- `appendChild` vs `append` khác sao?

→ Bài này dạy DOM API hiện đại đầy đủ.

---

## 1️⃣ DOM là gì?

**DOM** = **Document Object Model** — biểu diễn HTML trong memory dưới dạng **cây** (tree) object. JS thao tác cây này để đổi UI.

```html
<html>
  <body>
    <h1>Title</h1>
    <p>Para</p>
  </body>
</html>
```

→ DOM tree:
```
document
└─ html
   └─ body
      ├─ h1
      │  └─ "Title"
      └─ p
         └─ "Para"
```

Mỗi node trong cây là 1 **object JS** với properties + methods.

### Anatomy node

Mỗi node DOM là **JS object** với hàng chục property + method. 8 cái dưới đây là phổ biến nhất — bạn sẽ gõ daily khi viết DOM code: tagName, textContent, innerHTML, classList, parent/children navigation, style:

```javascript
const h1 = document.querySelector('h1');

h1.tagName           // "H1"
h1.textContent        // "Title"
h1.innerHTML          // "Title"
h1.classList          // DOMTokenList
h1.parentElement      // <body>
h1.children           // HTMLCollection
h1.nextElementSibling // <p>
h1.style.color = 'red';   // Inline style
```

> 🧠 **Ẩn dụ — DOM như khung gia phả:**
> - HTML file = **certificate** dòng họ.
> - DOM = **gia phả thực sự** đang sống, JS đi thăm/sửa từng người.
> - Đổi DOM → browser tự re-render (paint pixel mới).

---

## 2️⃣ Chọn element — Query selectors

### `querySelector` + `querySelectorAll`

2 API hiện đại để **chọn element** từ DOM — syntax giống CSS selector (dễ nhớ). `querySelector` trả về **first match**, `querySelectorAll` trả về **NodeList** chứa tất cả matches:

```javascript
// Selector giống CSS
document.querySelector('h1')              // First <h1>
document.querySelector('.btn-primary')     // First class
document.querySelector('#main')             // ID
document.querySelector('article > p')       // Child combinator
document.querySelector('[data-id="42"]')    // Attribute
document.querySelector('button:disabled')   // Pseudo-class

document.querySelectorAll('p')              // ALL <p> → NodeList
document.querySelectorAll('.card')          // All matches
```

→ **Modern default**. CSS selector syntax — dễ nhớ.

### Legacy methods (vẫn dùng được)

Trước thời `querySelector` (~2010), JS có **3 method legacy** riêng cho ID/class/tag. Vẫn còn dùng được và `getElementById` thực ra **nhanh nhất** cho lookup theo ID:

```javascript
document.getElementById('main')              // ID only
document.getElementsByClassName('btn')        // HTMLCollection (live)
document.getElementsByTagName('p')             // HTMLCollection
```

| Method | Return | Live? |
|---|---|---|
| `querySelector` | First match Element / null | — |
| `querySelectorAll` | **NodeList** (static snapshot) | ❌ |
| `getElementById` | Element / null | — |
| `getElementsByClassName` | **HTMLCollection** (live) | ✅ |
| `getElementsByTagName` | HTMLCollection (live) | ✅ |

→ **"Live"** = collection tự update khi DOM đổi. **Static** = snapshot tại moment query.

→ **2026 default**: `querySelector` / `querySelectorAll`. `getElementById` còn nhanh nhất cho ID.

### Query trong element con

Không phải lúc nào cũng query toàn `document` — đôi khi cần **scope** vào 1 element cụ thể. Mọi element đều có method `querySelector` riêng, chỉ tìm trong descendant của nó:

```javascript
const article = document.querySelector('article');
const para = article.querySelector('p');         // Chỉ tìm trong article
const links = article.querySelectorAll('a');
```

### Iterate NodeList

`querySelectorAll` trả về `NodeList` — **không phải Array** nhưng có `forEach`. Cần dùng method array khác (`map`, `filter`) → convert qua `Array.from()` hoặc spread `[...]`:

```javascript
const items = document.querySelectorAll('.item');

// forEach (NodeList có)
items.forEach(item => item.classList.add('active'));

// for-of
for (const item of items) {
  console.log(item.textContent);
}

// Convert sang Array nếu cần map/filter/reduce
const arr = [...items];
const visible = arr.filter(item => !item.hidden);
```

→ NodeList có `forEach` nhưng KHÔNG có `map`/`filter`/`reduce`. Convert qua spread.

---

## 3️⃣ Modify content — text, HTML, attribute

### `textContent` — Plain text (safe)

```javascript
const h1 = document.querySelector('h1');
h1.textContent = "New title";

console.log(h1.textContent);      // "New title"
```

→ **Recommended cho user input**. Browser KHÔNG parse HTML → an toàn (chống XSS).

### `innerHTML` — Parse HTML (nguy hiểm với user input)

```javascript
const div = document.querySelector('#content');
div.innerHTML = '<strong>Hello</strong>';     // Render bold

// ❌ NGUY HIỂM với user input
const userInput = '<img src=x onerror=alert(1)>';
div.innerHTML = userInput;        // → XSS attack
```

→ **Quy tắc**:
- Plain text → `textContent`.
- HTML structure cố định → `innerHTML` OK.
- User input → **textContent** hoặc sanitize (DOMPurify) trước.

### Attributes — Standard vs `data-*`

```javascript
const link = document.querySelector('a');

// Standard attribute
link.href                              // "https://..."
link.href = "/new";
link.getAttribute('href')              // alternative
link.setAttribute('href', '/new');
link.removeAttribute('disabled');

// data-* (custom)
const btn = document.querySelector('button');
// HTML: <button data-user-id="42" data-action="delete">

btn.dataset.userId                     // "42"  (camelCase)
btn.dataset.action                      // "delete"
btn.dataset.newField = "value";        // Set new data-new-field
```

→ `dataset` is the **idiomatic** way for custom data.

### Boolean attributes

```javascript
input.disabled = true;                 // Direct property
input.checked = true;
button.hidden = false;

// Hoặc qua setAttribute (more verbose)
input.setAttribute('disabled', '');
```

---

## 4️⃣ `classList` — Modify class

```javascript
const el = document.querySelector('.card');

el.classList.add('active');                          // Thêm
el.classList.remove('hidden');                        // Xóa
el.classList.toggle('open');                          // Toggle on/off
el.classList.toggle('open', condition);                // Force on/off
el.classList.contains('active')                        // true/false
el.classList.replace('old', 'new');                    // Replace

// Multiple
el.classList.add('a', 'b', 'c');
el.classList.remove('a', 'b');
```

→ Don't manipulate `className` directly (`el.className = 'a b'`) — overwrite all classes.

---

## 5️⃣ Inline style

```javascript
const el = document.querySelector('.box');

el.style.color = 'red';
el.style.backgroundColor = '#fff';        // camelCase (CSS: background-color)
el.style.padding = '10px';

// Multiple
Object.assign(el.style, {
  color: 'blue',
  fontSize: '20px',
  marginTop: '10px'
});

// CSS variable
el.style.setProperty('--my-var', '#f00');

// Get computed (after CSS apply)
const computed = window.getComputedStyle(el);
computed.color;        // "rgb(255, 0, 0)"
```

→ **Best practice**: prefer `classList` (CSS in stylesheet) over inline `style`. Inline = specificity cao, khó maintain.

---

## 6️⃣ Create + Insert + Remove element

### Create

```javascript
const div = document.createElement('div');
div.classList.add('card');
div.textContent = 'New card';

const img = document.createElement('img');
img.src = '/photo.jpg';
img.alt = 'Photo';
```

### Insert — modern methods

```javascript
const parent = document.querySelector('#container');
const newEl = document.createElement('p');
newEl.textContent = 'Hello';

parent.append(newEl);          // Append cuối (modern, returns nothing)
parent.prepend(newEl);          // Insert đầu
parent.appendChild(newEl);      // Legacy (returns the node)

// Insert relative to sibling
const ref = parent.firstChild;
ref.before(newEl);              // Insert before
ref.after(newEl);                // Insert after

// Replace
ref.replaceWith(newEl);
```

### Insert HTML string

```javascript
// insertAdjacentHTML — fast, no re-parse parent
parent.insertAdjacentHTML('beforeend', '<p>New</p>');
parent.insertAdjacentHTML('afterbegin', '<h2>Title</h2>');

// Positions:
// "beforebegin" | "afterbegin" | "beforeend" | "afterend"
//
//   parent
//   <!-- beforebegin -->
//   <parent>
//     <!-- afterbegin -->
//     existing children
//     <!-- beforeend -->
//   </parent>
//   <!-- afterend -->
```

### Remove

```javascript
const el = document.querySelector('.card');
el.remove();                        // Modern (recommended)

// Legacy
el.parentElement.removeChild(el);
```

### Clone

```javascript
const el = document.querySelector('.card');
const clone = el.cloneNode(true);     // true = deep clone (children)
parent.append(clone);
```

---

## 7️⃣ Forms — Đọc/ghi value

```html
<form id="login">
  <input id="email" type="email" name="email">
  <input id="pwd" type="password" name="password">
  <input type="checkbox" name="remember">
  <select name="country">
    <option value="vn">VN</option>
    <option value="us">US</option>
  </select>
  <button type="submit">Login</button>
</form>
```

```javascript
const form = document.querySelector('#login');

// Direct
const email = form.email.value;          // input by name
const pwd = form.querySelector('#pwd').value;

// FormData — modern, recommended
const formData = new FormData(form);
formData.get('email');                    // "nguyenvana@ex.com"
formData.get('remember');                  // "on" if checked, null if not
formData.entries();                         // iterate all

// Set value
form.email.value = 'nguyenvana@ex.com';
form.querySelector('input[type=checkbox]').checked = true;

// Submit programmatically
form.requestSubmit();                      // Modern (triggers validation)
form.submit();                              // Skip validation
```

### Quan trọng: serialize form

```javascript
const formData = new FormData(form);
const obj = Object.fromEntries(formData);
// { email: "nguyenvana@ex.com", password: "...", country: "vn" }

// For fetch
fetch('/api/login', {
  method: 'POST',
  body: formData                   // multipart/form-data
});

// Or as JSON
fetch('/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(obj)
});
```

---

## 8️⃣ Templating với `<template>`

Khi cần tạo nhiều element cùng kiểu, dùng `<template>` thay vì string concat.

```html
<template id="card-tpl">
  <article class="card">
    <h3 class="title"></h3>
    <p class="price"></p>
    <button class="buy">Mua</button>
  </article>
</template>

<div id="cards"></div>
```

```javascript
const tpl = document.querySelector('#card-tpl');
const cards = document.querySelector('#cards');

const products = [
  { name: 'iPhone', price: '25M' },
  { name: 'AirPods', price: '5M' },
];

products.forEach(p => {
  const clone = tpl.content.cloneNode(true);
  clone.querySelector('.title').textContent = p.name;
  clone.querySelector('.price').textContent = p.price;
  cards.append(clone);
});
```

→ **Performance** + **safe** (no innerHTML XSS). Modern preferred cho dynamic list.

---

## 9️⃣ Bạn viết shopping cart đơn giản

### HTML

```html
<div id="cart">
  <h2>Giỏ hàng <span id="count">0</span></h2>
  <ul id="items"></ul>
  <p>Tổng: <span id="total">0</span>đ</p>
</div>

<button data-id="1" data-name="iPhone" data-price="25000000" class="add">+ iPhone</button>
<button data-id="2" data-name="AirPods" data-price="5000000" class="add">+ AirPods</button>

<template id="item-tpl">
  <li>
    <span class="name"></span>
    <span class="price"></span>
    <button class="remove">x</button>
  </li>
</template>

<script src="cart.js" defer></script>
```

### `cart.js`

```javascript
const cart = [];

const itemsEl = document.querySelector('#items');
const countEl = document.querySelector('#count');
const totalEl = document.querySelector('#total');
const itemTpl = document.querySelector('#item-tpl');

function render() {
  itemsEl.innerHTML = '';
  cart.forEach((item, index) => {
    const clone = itemTpl.content.cloneNode(true);
    clone.querySelector('.name').textContent = item.name;
    clone.querySelector('.price').textContent = item.price.toLocaleString() + 'đ';
    const removeBtn = clone.querySelector('.remove');
    removeBtn.addEventListener('click', () => {
      cart.splice(index, 1);
      render();
    });
    itemsEl.append(clone);
  });

  countEl.textContent = cart.length;
  totalEl.textContent = cart.reduce((s, i) => s + i.price, 0).toLocaleString();
}

document.querySelectorAll('.add').forEach(btn => {
  btn.addEventListener('click', () => {
    cart.push({
      id: btn.dataset.id,
      name: btn.dataset.name,
      price: parseInt(btn.dataset.price)
    });
    render();
  });
});

render();
```

→ Full cart logic ~30 dòng. Vanilla JS, không framework. Modern API.

→ Chi tiết `addEventListener` ở [bài 03](03_events-and-async.md).

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **`innerHTML = userInput`** → XSS attack. Dùng `textContent` cho user input.
2. **NodeList không có `map`** → spread `[...nodeList].map(...)`.
3. **`getElementsByClassName` LIVE** → loop `for (let i = 0; i < els.length; i++)` mà remove element trong loop → vô tận / skip. Dùng `querySelectorAll` (static).
4. **`appendChild` legacy returns node, `append` modern returns nothing** → check nếu cần.
5. **Modify `className` thay `classList`** → overwrite mọi class khác.

---

## 🧠 Tự kiểm tra (Self-check)

1. Khác **`querySelector`** và **`querySelectorAll`**?
2. **`textContent`** vs **`innerHTML`** — chọn cái nào với user input?
3. **Live** collection vs **static** — khác sao? Cái nào safer?
4. Đọc value của `<input id="email">` — 2 cách?
5. Tạo `<li>Hello</li>` và append vào `#list` — code?

<details>
<summary>Gợi ý đáp án</summary>

1. **`querySelector(sel)`** = first match Element, return `null` nếu không có. **`querySelectorAll(sel)`** = NodeList tất cả match, return empty NodeList nếu không có. Cả 2 dùng CSS selector syntax.

2. **`textContent`** safer — browser KHÔNG parse HTML → chống XSS (user gõ `<script>` → render plain text). **`innerHTML`** parse HTML → render bold/img etc. nhưng nguy hiểm với user input. Quy tắc: user input → `textContent` (hoặc sanitize trước).

3. **Live**: HTMLCollection (từ `getElementsByClassName`) tự update khi DOM đổi → loop + modify = bug. **Static**: NodeList (từ `querySelectorAll`) = snapshot at query time → loop safe. **Static safer**.

4. (a) `document.querySelector('#email').value`. (b) `document.getElementById('email').value`. Bonus: trong form → `form.email.value` (by name).

5. ```javascript
   const li = document.createElement('li');
   li.textContent = 'Hello';
   document.querySelector('#list').append(li);
   ```
</details>

---

## ⚡ Cheatsheet

### Query

```javascript
document.querySelector('selector')
document.querySelectorAll('selector')
document.getElementById('id')
parent.querySelector('child-selector')
```

### Modify

```javascript
el.textContent = "..."       // safe text
el.innerHTML = "<b>...</b>"   // HTML (careful)
el.setAttribute('data-x', '1')
el.dataset.userId             // data-*
el.classList.add/remove/toggle/contains('cls')
el.style.color = 'red'
```

### Create + insert

```javascript
const el = document.createElement('div');
parent.append(child)                        // cuối
parent.prepend(child)                       // đầu
ref.before(newEl) / ref.after(newEl)
el.remove()
el.cloneNode(true)
parent.insertAdjacentHTML('beforeend', '<p>...</p>')
```

### Form

```javascript
const fd = new FormData(form);
const obj = Object.fromEntries(fd);
form.requestSubmit()
form.elementName.value
input.checked
```

### `<template>`

```javascript
const tpl = document.querySelector('#tpl');
const clone = tpl.content.cloneNode(true);
clone.querySelector('.x').textContent = '...';
parent.append(clone);
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **DOM** | Document Object Model — JS tree of HTML |
| **Node** | Generic — Element, Text, Comment |
| **Element** | HTML element node (`<div>`, `<p>`, ...) |
| **`querySelector`** | Modern CSS-style query |
| **NodeList** | Static collection from `querySelectorAll` |
| **HTMLCollection** | Live collection from `getElementsByClassName` |
| **`textContent`** | Plain text (safe) |
| **`innerHTML`** | Parsed HTML (potential XSS) |
| **`classList`** | DOMTokenList for class manipulation |
| **`dataset`** | `data-*` attributes as object |
| **`FormData`** | Form serialization object |
| **`<template>`** | Reusable HTML template, JS clone |
| **XSS** | Cross-Site Scripting — inject HTML/JS |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [Variables, Functions, Types — JS core syntax](01_variables-functions-types.md)
- ➡️ **Bài tiếp theo:** [Events & Async — Click, Promise, async/await](03_events-and-async.md)
- ↑ **Về cụm:** [javascript-dom README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [HTML Essentials](../../../html-css/lessons/01_basic/01_html-essentials.md) — HTML mà JS modify
- [Forms & a11y](../../../html-css/lessons/01_basic/02_forms-and-accessibility.md) — form HTML JS đọc

### 🌐 Tài nguyên tham khảo khác
- 📖 [MDN — DOM introduction](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction)
- 📖 [javascript.info — DOM tree](https://javascript.info/dom-nodes)
- 📖 [Modern API — You Don't Need jQuery](https://github.com/nefe/You-Dont-Need-jQuery)
- 📖 [DOMPurify](https://github.com/cure53/DOMPurify) — sanitize HTML

---

> 🎯 *Sau bài này JS bạn modify DOM thuần thục. Bài kế tiếp dạy **events + async** — interactivity thực sự + Promise/async-await.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `javascript-dom/` lesson 3/5. Cover: DOM tree concept + node anatomy + query selectors (modern vs legacy) + traverse (parent/children/siblings) + modify (textContent/innerHTML/classList/style) + create + insert + remove + clone elements.
- **v1.1.0 (25/05/2026)** — Bổ sung lời dẫn trước các mục Anatomy node, querySelector, Legacy methods, Query trong element con, Iterate NodeList. Thêm mục Changelog.
