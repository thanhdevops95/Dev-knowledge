# 🎓 Forms & Accessibility — Input đúng cách + a11y basic

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~16 phút\
> **Prerequisites:** [HTML Essentials](01_html-essentials.md)

> 🎯 *Master **form** trong HTML: 15+ input types, **validation tự động** browser, **label** + accessibility, **submit/GET vs POST**, **ARIA attributes**, **a11y checklist**. Sau bài này viết được form login/signup/checkout đúng chuẩn — keyboard navigate được, screen reader đọc được.*

## 🎯 Sau bài này bạn sẽ

- [ ] Viết **`<form>`** với GET/POST gửi đến backend
- [ ] Dùng **15+ input types** (text, email, password, number, date, file, range...)
- [ ] **Validation tự động** browser (`required`, `pattern`, `min`/`max`)
- [ ] **Label** đúng cách (`<label for>` hoặc bọc trong)
- [ ] **Fieldset + Legend** group inputs
- [ ] **`<select>`**, **`<textarea>`**, **`<button>`** đúng cách
- [ ] **ARIA** attributes cơ bản (`aria-label`, `aria-describedby`)
- [ ] Test a11y với keyboard (Tab) + screen reader
- [ ] **WCAG 2.2** levels (A / AA / AAA) — biết apply level nào

---

## Tình huống — Bạn viết form login, đồng nghiệp mù bẩm sinh không dùng được

Bạn viết form login đầu tiên:

```html
<div>Email</div>
<input type="text">

<div>Password</div>
<input type="text">

<div onclick="login()">Login</div>
```

→ Trông OK trên Chrome. Đồng nghiệp (developer mù) test bằng screen reader (NVDA):
- "Edit text" — không biết là field gì.
- Tab keyboard → focus nhảy lung tung.
- Click "Login" qua bàn phím — không submit (vì là `<div>` không phải `<button>`).
- Password hiển thị plaintext.

Họ bảo:
> *"Anh viết form như anh là user duy nhất. **15% dân số** có disability — mù, mất tay, dyslexia. Nếu form không accessible = không bán được cho 15% khách hàng. Plus, accessibility = SEO bonus + UX cho **mọi** user."*

Bạn ngơ:
- **`<input type>`** thực ra có nhiều loại?
- **`<label>`** thực sự để làm gì?
- **ARIA** là gì?
- A11y là **đạo đức** hay **luật** (GDPR/ADA)?

→ Bài này dạy form + a11y đầy đủ.

---

## 1️⃣ Form cơ bản

Form là **cách chính** để user gửi data lên server — login, signup, search, upload. HTML form skeleton gồm 3 phần: `<form>` wrapper với action/method, các `<input>` với `<label>` đi kèm, và `<button type="submit">`. Ví dụ form login đầy đủ:

```html
<form action="/login" method="POST">
  <label for="email">Email</label>
  <input type="email" id="email" name="email" required>

  <label for="password">Mật khẩu</label>
  <input type="password" id="password" name="password" required minlength="8">

  <button type="submit">Đăng nhập</button>
</form>
```

### Anatomy `<form>`

5 attribute chính của `<form>` — `action` URL submit tới, `method` GET/POST, `enctype` cho upload file, `autocomplete` tắt autocomplete browser, `novalidate` để JS tự validate. Hiểu để cấu hình đúng:

| Attribute | Mục đích |
|---|---|
| `action="/login"` | URL gửi data tới (backend endpoint) |
| `method="POST"` | HTTP method (GET hoặc POST) |
| `enctype="multipart/form-data"` | Khi upload file |
| `autocomplete="off"` | Browser không suggest |
| `novalidate` | Disable browser validation (do JS tự lo) |

### GET vs POST

Form có 2 method chính — GET đẩy data vào URL (visible, cache được, idempotent), POST đẩy vào body (không visible). Pick đúng theo nature của action:

| Method | Khi nào |
|---|---|
| **GET** | Search, filter (data đi vào URL: `?q=phone&page=2`) |
| **POST** | Submit data (login, signup, create) — body request |

→ Chi tiết [bài HTTP methods](../../../../05_networking/http-https/lessons/01_basic/01_http-methods.md).

### Submit flow

Khi user click submit, browser thực thi **5 bước** — collect data, validate, format encoding, gửi request, hoặc highlight lỗi nếu validation fail. Flow này là default behavior, không cần JS:

```
User click submit / Enter trong input
   ↓
Browser collect form data
   ↓
Browser run validation (required, pattern, ...)
   ↓
Pass → POST /login  với body: email=nguyenvana@ex.com&password=secret
                       (URL-encoded form data)
Fail → highlight input lỗi, không gửi
```

---

## 2️⃣ 15+ input types — modern HTML5

HTML5 mở rộng `<input>` thành **15+ type** đặc biệt — không chỉ là `text` nữa. Mỗi type bật **validation tự + UI riêng + mobile keyboard phù hợp**. Đây là superpower miễn phí của browser:

```html
<input type="text">              <!-- Free text -->
<input type="email">             <!-- Email validate -->
<input type="password">          <!-- Hidden chars -->
<input type="number" min="0" max="100" step="1">
<input type="tel">               <!-- Phone (mobile keyboard số) -->
<input type="url">               <!-- URL validate -->
<input type="search">            <!-- Search box (X clear) -->
<input type="date">              <!-- Date picker -->
<input type="time">              <!-- Time picker -->
<input type="datetime-local">    <!-- Date + time -->
<input type="month">             <!-- Month picker -->
<input type="week">              <!-- Week picker -->
<input type="color">             <!-- Color picker -->
<input type="range" min="0" max="100">   <!-- Slider -->
<input type="file" accept="image/*" multiple>   <!-- File upload -->
<input type="checkbox">          <!-- ☐ -->
<input type="radio" name="gender" value="m">   <!-- ⚪ -->
<input type="hidden" name="csrf" value="...">  <!-- Server pass-through -->
```

### Bonus mobile keyboards

Choosing right `type` → **mobile keyboard tự đổi**:
- `email` → bàn phím có `@`.
- `tel` → bàn phím số.
- `number` → bàn phím số.
- `url` → bàn phím có `.com`.

→ UX bonus quan trọng mà nhiều dev không biết.

### Attributes phổ biến

```html
<input type="text"
       name="username"
       id="username"
       placeholder="Nhập username"
       required
       minlength="3"
       maxlength="20"
       pattern="[a-zA-Z0-9_]+"
       autocomplete="username"
       autocapitalize="off"
       autocorrect="off"
       spellcheck="false"
       readonly
       disabled
       value="default">
```

| Attribute | Mục đích |
|---|---|
| `name` | Key gửi lên backend (`username=nguyenvana`) |
| `id` | Liên kết với `<label for>` |
| `placeholder` | Gợi ý mờ trong input (KHÔNG thay label!) |
| `required` | Bắt buộc nhập |
| `min`/`max`/`minlength`/`maxlength` | Validate |
| `pattern` | Regex validate |
| `autocomplete` | Browser suggest (`name`, `email`, `current-password`, ...) |
| `readonly` | Không sửa được nhưng vẫn submit |
| `disabled` | Không sửa + KHÔNG submit |

---

## 3️⃣ `<label>` — accessibility quan trọng nhất

### ❌ Sai (không label)

```html
<input type="email" placeholder="Email">
```

→ Screen reader đọc "Edit text" — user mù không biết là gì.

### ✅ Đúng — `<label for>` link `id`

```html
<label for="email">Email</label>
<input type="email" id="email" name="email">
```

### ✅ Hoặc bọc input trong label

```html
<label>
  Email
  <input type="email" name="email">
</label>
```

→ Cả 2 cách đều OK. **Quy tắc 2026**: ưu tiên `for/id` (clearer + cho phép label/input không cạnh nhau).

### Bonus — click label → focus input

```
Click "Email" label → cursor tự vào input
```

→ Tăng click target (mobile UX). User mù → screen reader đọc "Email, edit, email type".

---

## 4️⃣ `<select>` / `<textarea>` / `<button>`

### `<select>` — dropdown

```html
<label for="country">Quốc gia</label>
<select id="country" name="country" required>
  <option value="">-- Chọn --</option>
  <option value="vn">Việt Nam</option>
  <option value="us">USA</option>
  <option value="jp" selected>Japan</option>
</select>

<!-- Multi-select -->
<select name="hobbies" multiple size="5">
  <option>Music</option>
  <option>Sports</option>
</select>

<!-- Group -->
<select name="city">
  <optgroup label="Miền Bắc">
    <option>Hà Nội</option>
    <option>Hải Phòng</option>
  </optgroup>
  <optgroup label="Miền Nam">
    <option>TP. HCM</option>
  </optgroup>
</select>
```

### `<textarea>` — multi-line text

```html
<label for="bio">Tiểu sử</label>
<textarea id="bio" name="bio" rows="5" cols="50" maxlength="500"
          placeholder="Viết về bạn..."></textarea>
```

### `<button>` — KHÔNG dùng `<div onclick>`

```html
<button type="submit">Gửi</button>           <!-- Submit form -->
<button type="reset">Reset</button>           <!-- Clear form -->
<button type="button" onclick="hi()">Hi</button>   <!-- Action JS, không submit -->
```

| `type` | Hành vi |
|---|---|
| `submit` (default trong form) | Submit form |
| `reset` | Clear form |
| `button` | Chỉ event JS, không submit |

→ **Quy tắc**: button trong form đặt `type="button"` rõ ràng (tránh submit nhầm).

### ❌ Lý do KHÔNG dùng `<div onclick>`

```html
<div onclick="login()">Login</div>
```

- Không focusable bằng keyboard (Tab không vào).
- Screen reader không đọc là button.
- Không có default style "clickable" (cursor).
- Không submit form.

→ **Dùng `<button>` cho mọi click action**. CSS thì style giống `<div>` được.

---

## 5️⃣ `<fieldset>` + `<legend>` — group inputs

```html
<form>
  <fieldset>
    <legend>Thông tin cá nhân</legend>

    <label for="name">Họ tên</label>
    <input id="name" name="name">

    <label for="dob">Ngày sinh</label>
    <input type="date" id="dob" name="dob">
  </fieldset>

  <fieldset>
    <legend>Địa chỉ</legend>

    <label for="city">Thành phố</label>
    <input id="city" name="city">
  </fieldset>

  <button type="submit">Lưu</button>
</form>
```

→ Browser tự vẽ border + heading. Screen reader đọc legend trước mỗi field group → context tốt hơn.

---

## 6️⃣ Validation tự động — browser miễn phí

```html
<input type="email" required>
<input type="number" min="18" max="100" required>
<input type="text" pattern="\d{10}" title="10 số" required>
<input type="password" minlength="8" required>
```

### Khi user submit invalid → browser tự:

- Highlight input đỏ
- Hiển thị message ("Please fill out this field")
- Block submit

### Custom message

```html
<input type="email" required
       oninvalid="this.setCustomValidity('Vui lòng nhập email hợp lệ')"
       oninput="this.setCustomValidity('')">
```

### Pseudo-class CSS

```css
input:invalid { border-color: red; }
input:valid   { border-color: green; }
input:required { ... }
input:optional { ... }
input:focus    { outline: 2px solid blue; }
```

> ⚠️ **Đừng dựa hoàn toàn validation browser**. Backend PHẢI validate lại — user bypass HTML dễ (DevTools edit). Browser validation = UX, backend validation = security.

---

## 7️⃣ ARIA — Accessible Rich Internet Applications

**ARIA** = bộ attribute thêm context cho a11y khi HTML semantic không đủ.

### `aria-label` — gán nhãn khi không có text

```html
<button aria-label="Đóng dialog">×</button>

<!-- Search icon button -->
<button aria-label="Search">
  <svg>...</svg>
</button>
```

→ Screen reader đọc "Đóng dialog button" thay vì "Multiplication sign button".

### `aria-describedby` — gán mô tả

```html
<label for="pwd">Password</label>
<input id="pwd" type="password" aria-describedby="pwd-help">
<p id="pwd-help">Tối thiểu 8 ký tự, 1 số, 1 hoa.</p>
```

### `aria-current` — chỉ phần tử "đang ở"

```html
<nav>
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/about" aria-current="page">About</a></li>
    <li><a href="/contact">Contact</a></li>
  </ul>
</nav>
```

→ Screen reader đọc "About, current page". CSS có thể style `[aria-current="page"]`.

### `aria-hidden` — ẩn khỏi screen reader

```html
<button>
  <span aria-hidden="true">📞</span>
  Gọi
</button>
```

→ Emoji không có nghĩa cho screen reader → hide. Button text "Gọi" mới được đọc.

### `role` — gán role khi semantic không có

```html
<div role="alert">Lỗi: email đã tồn tại</div>
<div role="dialog" aria-modal="true">...</div>
<div role="status">Loading...</div>
```

→ **Quy tắc**: ưu tiên **semantic HTML** trước. Chỉ dùng ARIA khi semantic không đủ. **No ARIA tốt hơn ARIA sai** (sai = worse UX).

---

## 8️⃣ A11y checklist — test bao gồm

### 1. Keyboard navigation

- Tab qua **mọi interactive element** (link, button, input).
- Enter/Space activate.
- Esc đóng dialog/menu.
- Arrow keys trong menu/list.

→ Test: bỏ chuột, chỉ dùng Tab → có thể hoàn thành mọi task?

### 2. Screen reader

- Mac: **VoiceOver** (`Cmd + F5`)
- Win: **NVDA** (free) hoặc **JAWS** (commercial)
- Linux: **Orca**

→ Test: nhắm mắt, dùng screen reader → biết đang đâu, làm gì?

### 3. Color contrast

- Text vs background ≥ **4.5:1** (WCAG AA)
- Text lớn (18px+) ≥ **3:1**
- Tool: [WebAIM contrast checker](https://webaim.org/resources/contrastchecker/)

### 4. Focus visible

```css
/* ❌ Đừng làm thế này */
:focus { outline: none; }

/* ✅ Custom focus đẹp */
:focus { outline: 2px solid blue; outline-offset: 2px; }
:focus-visible { outline: 2px solid blue; }   /* Chỉ khi keyboard */
```

→ User keyboard cần thấy focus đang ở đâu.

### 5. Alt text

```html
<img src="phone.jpg" alt="iPhone 15 Pro Max đen">   <!-- Content -->
<img src="divider.svg" alt="">                       <!-- Decorative -->
```

### 6. Heading hierarchy

```html
<h1>Page title</h1>
  <h2>Section 1</h2>
    <h3>Sub 1.1</h3>
    <h3>Sub 1.2</h3>
  <h2>Section 2</h2>
```

→ Không skip level (h1 → h3 sai).

### 7. Form labels — đã cover §3.

### 8. Tool audit tự động

- Chrome DevTools → **Lighthouse** → "Accessibility" → score 90+
- [axe DevTools](https://www.deque.com/axe/devtools/) extension
- [WAVE](https://wave.webaim.org/) — paste URL

---

## 9️⃣ WCAG 2.2 — Web Content Accessibility Guidelines

| Level | Mức | Áp dụng |
|---|---|---|
| **A** | Tối thiểu | Mọi site |
| **AA** | Khuyến nghị | **Default 2026** — luật yêu cầu (US ADA, EU EAA) |
| **AAA** | Tối đa | Banking, healthcare, gov |

### POUR principles

WCAG 2.2 dựa trên 4 nguyên tắc:

| P | Nguyên tắc | Ví dụ |
|---|---|---|
| **P** | Perceivable | Alt text, captions video, contrast |
| **O** | Operable | Keyboard, đủ time, không flash gây co giật |
| **U** | Understandable | Label rõ, error message hữu ích, ngôn ngữ đúng |
| **R** | Robust | HTML valid, ARIA đúng, work với mọi tech |

### Luật bắt buộc 2026

- **🇺🇸 USA**: ADA (Title III) — kiện hàng nghìn site mỗi năm.
- **🇪🇺 EU**: European Accessibility Act (EAA) — bắt buộc từ 28/06/2025 cho mọi public service + e-commerce > €2M revenue.
- **🇻🇳 VN**: Chưa enforce luật, nhưng quốc tế bán hàng cần đáp ứng.

→ A11y không phải tùy chọn — là **luật + đạo đức + ROI** (15% market share).

---

## 1️⃣0️⃣ Bạn viết form login chuẩn

```html
<form action="/login" method="POST">
  <h2>Đăng nhập</h2>

  <div class="field">
    <label for="email">Email</label>
    <input
      type="email"
      id="email"
      name="email"
      autocomplete="email"
      required
      aria-describedby="email-help">
    <small id="email-help">Email bạn đã đăng ký.</small>
  </div>

  <div class="field">
    <label for="password">Mật khẩu</label>
    <input
      type="password"
      id="password"
      name="password"
      autocomplete="current-password"
      required
      minlength="8"
      aria-describedby="pwd-help">
    <small id="pwd-help">Tối thiểu 8 ký tự.</small>
  </div>

  <div class="field">
    <label>
      <input type="checkbox" name="remember">
      Ghi nhớ đăng nhập
    </label>
  </div>

  <button type="submit">Đăng nhập</button>

  <p>
    <a href="/forgot-password">Quên mật khẩu?</a>
  </p>
</form>
```

→ Form này: label đúng, validation tự, autocomplete tốt, keyboard navigate được, screen reader đọc đầy đủ.

---

## ⚠️ 5 pitfall hay vướng

1. **`<div onclick>`** thay button → keyboard không vào, screen reader bỏ qua. Dùng `<button>`.
2. **Placeholder thay label** → khi user gõ, mất context. Luôn có `<label>`.
3. **`outline: none` cho :focus** → user keyboard mất hướng. Custom focus style đẹp thay vì xoá.
4. **Validation chỉ frontend** → bypass dễ via DevTools. Backend BẮT BUỘC validate.
5. **`color` mà không text alternative** → user mù màu (8% nam) không phân biệt. "Red = error" thì kèm icon ⚠️ hoặc text "Error".

---

## ✅ Self-check

1. Sao `<input type="email">` tốt hơn `<input type="text">` cho email?
2. Cách kết hợp `<label>` + `<input>` — 2 cách?
3. Tại sao **không** dùng `<div onclick>` cho click?
4. `<button type="button">` khác `<button type="submit">` sao?
5. Tại sao a11y là **luật** chứ không chỉ "nice to have"?

<details>
<summary>Gợi ý đáp án</summary>

1. (a) **Mobile keyboard tự đổi**: có `@`, không có shift. (b) **Validation tự động**: browser check format. (c) **Autofill tốt hơn**: browser biết là email field. (d) **Semantic**: screen reader đọc "email field". (e) **CSS hooks**: `input[type=email]:invalid` style được.

2. (a) `<label for="x">Foo</label><input id="x">` — link qua `for/id`. (b) `<label>Foo <input></label>` — bọc input. Recommend (a) clearer.

3. (a) Keyboard Tab **không focus** `<div>` (trừ khi `tabindex="0"`). (b) Screen reader **không announce** là button. (c) Enter/Space không activate. (d) Trong form, `<div>` không submit. **Dùng `<button>` cho mọi click action**.

4. **`type="submit"`** (default trong form) submit form khi click hoặc Enter. **`type="button"`** chỉ chạy JS handler, không submit. Quan trọng: nếu có nhiều button trong form mà bạn không muốn submit nhầm → `type="button"` explicitly.

5. **USA ADA Title III** kiện thousands sites mỗi năm — không accessible = bị fines. **EU EAA** bắt buộc 28/06/2025 cho public + e-commerce >€2M. Domino's Pizza thua kiện 2019 vì site không accessible cho user mù. Plus ethically: 15% dân số có disability — exclude = bias.
</details>

---

## ⚡ Cheatsheet

### Form template

```html
<form action="/api/login" method="POST">
  <label for="email">Email</label>
  <input type="email" id="email" name="email" required autocomplete="email">

  <label for="pwd">Password</label>
  <input type="password" id="pwd" name="password" required minlength="8" autocomplete="current-password">

  <button type="submit">Submit</button>
</form>
```

### Input types

```
text  email  password  number  tel  url  search
date  time  datetime-local  month  week
color  range  file  checkbox  radio  hidden
```

### Validation attributes

```
required  minlength="N"  maxlength="N"
min="N"  max="N"  step="N"  pattern="regex"
```

### ARIA top

```html
aria-label="..."        khi không có text
aria-describedby="id"   link mô tả
aria-current="page"     chỉ "đang ở đây"
aria-hidden="true"      hide khỏi screen reader
role="alert"            khi cần dynamic announce
```

### A11y test

```
[ ] Tab navigate qua mọi interactive
[ ] Enter/Space activate
[ ] Esc đóng dialog
[ ] Screen reader đọc đủ context
[ ] Color contrast 4.5:1
[ ] Focus visible
[ ] Alt text cho image
[ ] Lighthouse A11y score 90+
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **`<form>`** | Container submit data |
| **`<label>`** | Gán nhãn cho input |
| **`<input>`** | Field nhập data, 15+ types |
| **`<button>`** | Click action |
| **`<select>` / `<option>`** | Dropdown |
| **`<textarea>`** | Multi-line input |
| **`<fieldset>` / `<legend>`** | Group inputs với heading |
| **`autocomplete`** | Browser suggest |
| **a11y** | Accessibility (a + 11 letters + y) |
| **ARIA** | Accessible Rich Internet Applications |
| **WCAG** | Web Content Accessibility Guidelines |
| **POUR** | Perceivable / Operable / Understandable / Robust |
| **WCAG levels A/AA/AAA** | Min / Default / Max |
| **Screen reader** | NVDA, JAWS, VoiceOver, Orca |
| **Lighthouse** | Chrome DevTools audit tool |

---

## 🔗 Links

### Trong cluster
- ← Trước: [HTML Essentials](01_html-essentials.md)
- → Tiếp: [CSS Fundamentals](03_css-fundamentals.md)
- ↑ Cluster: [html-css README](../../README.md)

### Cross-reference
- [HTTP methods (GET vs POST)](../../../../05_networking/http-https/lessons/01_basic/01_http-methods.md)
- [FastAPI form handling](../../../backend/python-fastapi/lessons/01_basic/01_routes-and-parameters.md)

### External
- 📖 [MDN — HTML Forms guide](https://developer.mozilla.org/en-US/docs/Learn/Forms)
- 📖 [WCAG 2.2 quickref](https://www.w3.org/WAI/WCAG22/quickref/)
- 📖 [WebAIM contrast checker](https://webaim.org/resources/contrastchecker/)
- 📖 [The A11y Project](https://www.a11yproject.com/) — checklist + resources
- 📖 [Inclusive Components — Heydon Pickering](https://inclusive-components.design/)

---

> 🎯 *Sau bài này form bạn viết accessible cho mọi user. Bài kế tiếp dạy **CSS fundamentals** — selectors, box model, units — bắt đầu style.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in 2-3 câu trước §1 Form cơ bản + Anatomy form + GET vs POST + Submit flow + §2 15+ input types. Fix `username=bạn` residue → `username=nguyenvana`. Thêm Changelog section.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `html-css/` lesson 3/5. Cover: form anatomy + GET vs POST + 15+ input types + mobile keyboard auto + label association + validation HTML5 + accessibility (ARIA, WCAG, screen reader, keyboard nav) + form best practices.
