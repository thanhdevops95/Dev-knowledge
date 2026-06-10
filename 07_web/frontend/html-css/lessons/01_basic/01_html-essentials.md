# 🎓 HTML Essentials — Semantic tags, structure, common elements

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [HTML & CSS là gì](00_what-is-html-and-css.md)

> 🎯 *Master HTML thực sự: **document structure**, **20 common tag** thường gặp, **semantic tags** (`<header>`, `<article>`, `<nav>`...), **inline vs block**, **attributes** (id, class, data-), **embedding media** (img, video, iframe), **links + navigation**. Sau bài này viết được trang web đầy đủ structure.*

## 🎯 Sau bài này bạn sẽ

- [ ] Viết được **HTML5 document structure** đúng chuẩn
- [ ] Phân biệt **semantic** vs **non-semantic** tags
- [ ] Master **20 tag** phổ biến nhất
- [ ] Hiểu **block** vs **inline** vs **inline-block**
- [ ] Dùng **`id`** / **`class`** / **`data-*`** attributes đúng
- [ ] Embed **image** / **video** / **iframe** đúng cách
- [ ] Viết **navigation menu** + **link** trong/ngoài
- [ ] Validate HTML với W3C validator

---

## Tình huống — Bạn viết trang giới thiệu

Bạn muốn trang `about.html` cho Acme Shop. Bạn viết:

```html
<div>Acme Shop</div>
<div>Chúng tôi bán điện thoại.</div>
<div>
  <div>Trang chủ</div>
  <div>Sản phẩm</div>
  <div>Liên hệ</div>
</div>
<div>Copyright 2026</div>
```

→ Trang chạy được. Nhưng:
- 😱 **SEO** kém — Google không biết đâu là heading, navigation, footer.
- 😱 **Accessibility** kém — screen reader đọc "div div div" cho người mù.
- 😱 **Maintainability** kém — code đọc không hiểu đâu là gì.

Senior chê:
> *"Anh dùng `<div>` cho mọi thứ — đó là 2010 style. Modern HTML5 có **semantic tags**: `<header>`, `<nav>`, `<main>`, `<article>`, `<footer>`. Search engine + screen reader + dev sau bạn đều cảm ơn."*

Bạn ngơ:
- Semantic tag có gì khác?
- 20 tag thường dùng là gì?
- Khi nào `<section>` vs `<article>` vs `<div>`?

→ Bài này dạy đầy đủ.

---

## 1️⃣ HTML5 document structure đầy đủ

Trang HTML production-ready không chỉ có `<head>` + `<body>` tối thiểu — cần thêm **8 meta tag** cho SEO, social sharing (Open Graph, Twitter Card), mobile responsive, favicon. Đây là template chuẩn bạn có thể copy-paste vào project mới:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <!-- Encoding + viewport -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- SEO + social -->
  <title>Acme Shop — Điện thoại chính hãng</title>
  <meta name="description" content="Cửa hàng điện thoại uy tín tại Hà Nội">
  <meta name="keywords" content="iphone, samsung, xiaomi">

  <!-- Open Graph (Facebook, LinkedIn share preview) -->
  <meta property="og:title" content="Acme Shop">
  <meta property="og:description" content="Điện thoại chính hãng">
  <meta property="og:image" content="https://acmeshop.vn/og-image.jpg">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">

  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">

  <!-- CSS -->
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <!-- Content here -->

  <!-- JS đặt cuối body -->
  <script src="/app.js" defer></script>
</body>
</html>
```

### Vai trò các meta

6 nhóm meta tag trên có vai trò khác nhau — mỗi cái phục vụ 1 mục đích cụ thể từ encoding đến SEO. Hiểu vai trò giúp **không bao giờ quên** khi viết trang mới:

| Tag | Mục đích |
|---|---|
| `<meta charset="UTF-8">` | Encoding cho Unicode (tiếng Việt diacritics) |
| `<meta name="viewport">` | Mobile responsive |
| `<meta name="description">` | Snippet trong Google search result |
| `<meta property="og:*">` | Preview khi share lên Facebook/Slack/Discord |
| `<meta name="twitter:*">` | Preview khi share lên Twitter/X |
| `<link rel="icon">` | Favicon (icon tab) |

→ Mọi production page phải có đầy đủ. Tool check: [metatags.io](https://metatags.io).

---

## 2️⃣ Semantic tags — Bạn fix code cũ

### ❌ Cũ — `<div>` lung tung

Code HTML cũ (~2010 trở về trước) thường viết toàn `<div>` — máy không phân biệt được phần nào là header, nav, content, footer. Hậu quả: SEO kém, screen reader confused, code khó đọc:

```html
<div>Acme Shop</div>
<div>
  <div>Trang chủ</div>
  <div>Sản phẩm</div>
</div>
<div>Bài viết...</div>
<div>Copyright</div>
```

### ✅ Mới — Semantic HTML5

HTML5 (2014) thêm **8 tag semantic** thay thế `<div>` lung tung. Cùng 1 trang nhưng dùng đúng tag → SEO tốt hơn, accessibility chuẩn, code self-documenting:

```html
<header>
  <h1>Acme Shop</h1>
</header>

<nav>
  <ul>
    <li><a href="/">Trang chủ</a></li>
    <li><a href="/products">Sản phẩm</a></li>
    <li><a href="/contact">Liên hệ</a></li>
  </ul>
</nav>

<main>
  <article>
    <h2>iPhone 15 review</h2>
    <p>Bài viết...</p>
  </article>

  <aside>
    <h3>Sản phẩm liên quan</h3>
    <ul>...</ul>
  </aside>
</main>

<footer>
  <p>&copy; 2026 Acme Shop</p>
</footer>
```

### Bảng semantic tags

8 tag semantic chính + 3 trục cần nhớ — mục đích, bao nhiêu trên 1 trang, anti-pattern hay gặp. `<main>` chỉ **1 duy nhất**, các tag khác có thể nhiều:

| Tag | Mục đích | Bao nhiêu / trang |
|---|---|---|
| `<header>` | Đầu trang/section — logo, title | Nhiều (mỗi section có header riêng) |
| `<nav>` | Navigation menu | Thường 1, có thể nhiều (main nav + footer nav) |
| `<main>` | Content chính | **1 duy nhất** mỗi trang |
| `<article>` | Nội dung độc lập (blog post, news) | Nhiều |
| `<section>` | Group content liên quan (chapter) | Nhiều |
| `<aside>` | Sidebar, related, ads | Nhiều |
| `<footer>` | Cuối trang/section | Nhiều |
| `<figure>` + `<figcaption>` | Image + caption | Nhiều |

### `<section>` vs `<article>` vs `<div>`

| Tag | Khi nào |
|---|---|
| **`<article>`** | Nội dung **độc lập** — đứng một mình vẫn nghĩa (blog post, product card, comment) |
| **`<section>`** | Nhóm nội dung **có heading + liên quan** (chapter của trang) |
| **`<div>`** | **Không semantic** — chỉ để wrap cho styling/JS |

→ **Quy tắc**: nếu có heading → thường là `<section>` hoặc `<article>`. Wrap cho CSS → `<div>`.

---

## 3️⃣ 20 tag phổ biến nhất — phải thuộc

### Heading

```html
<h1>Heading lớn nhất — 1 per page</h1>
<h2>Heading section</h2>
<h3>Heading sub-section</h3>
<!-- ... đến h6 -->
```

→ **Quy tắc**: dùng **theo thứ tự**, không skip (h1 → h3 lỗi a11y). 1 trang **1 `<h1>` duy nhất**.

### Text

```html
<p>Paragraph — đoạn văn.</p>
<strong>Quan trọng (bold + semantic)</strong>
<em>Nhấn mạnh (italic + semantic)</em>
<b>Bold không semantic</b>
<i>Italic không semantic</i>
<u>Underline</u>
<small>Text nhỏ (vd disclaimer)</small>
<mark>Highlight</mark>
<code>Inline code</code>
<pre><code>Block code (preserve whitespace)</code></pre>
<blockquote cite="https://...">Trích dẫn</blockquote>
<hr>  <!-- Horizontal rule -->
<br>  <!-- Line break -->
```

→ `<strong>` vs `<b>`: cả 2 bold. `<strong>` có **nghĩa semantic** (quan trọng), `<b>` chỉ visual. Modern: prefer `<strong>` / `<em>`.

### List

```html
<!-- Unordered -->
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>

<!-- Ordered -->
<ol start="3">
  <li>Item 3</li>
  <li>Item 4</li>
</ol>

<!-- Definition list -->
<dl>
  <dt>Term</dt>
  <dd>Definition</dd>
</dl>
```

### Links

```html
<a href="/products">Internal link</a>
<a href="https://google.com">External link</a>
<a href="https://x.com" target="_blank" rel="noopener noreferrer">
  External tab mới
</a>
<a href="mailto:nguyenvana@ex.com">Email</a>
<a href="tel:+84901234567">Phone (mobile)</a>
<a href="#section1">Anchor cùng trang</a>
<a href="/file.pdf" download>Download file</a>
```

→ `target="_blank"` luôn kèm `rel="noopener noreferrer"` (security + performance).

### Image

```html
<!-- Basic -->
<img src="photo.jpg" alt="Lập trình viên đang code" width="800" height="600">

<!-- Responsive — modern -->
<picture>
  <source media="(min-width: 800px)" srcset="large.jpg">
  <source media="(min-width: 400px)" srcset="medium.jpg">
  <img src="small.jpg" alt="Ảnh sản phẩm" loading="lazy">
</picture>

<!-- Lazy load (browser tự defer load) -->
<img src="hero.jpg" alt="Hero" loading="lazy">

<!-- With caption -->
<figure>
  <img src="diagram.png" alt="Architecture diagram">
  <figcaption>Hình 1 — Sơ đồ kiến trúc</figcaption>
</figure>
```

→ **`alt`** bắt buộc cho a11y + SEO. Image trang trí dùng `alt=""`.

### Table

```html
<table>
  <thead>
    <tr>
      <th>Tên</th>
      <th>Tuổi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Nguyen Van A</td>
      <td>28</td>
    </tr>
  </tbody>
  <tfoot>
    <tr><td colspan="2">Total: 1</td></tr>
  </tfoot>
</table>
```

→ Dùng cho **data tabular** (Excel-like). KHÔNG dùng cho layout (đó là CSS Grid/Flex).

### Media

```html
<video src="video.mp4" controls width="640"></video>

<audio src="song.mp3" controls></audio>

<iframe src="https://youtube.com/embed/xxx" width="560" height="315"></iframe>
```

---

## 4️⃣ Block vs Inline vs Inline-block

```html
<!-- BLOCK: chiếm toàn width, xuống dòng -->
<div>Block</div>      <!-- ─────────────────────── -->
<div>Block</div>      <!-- ─────────────────────── -->

<!-- INLINE: chiếm width content, nối dòng -->
<span>Inline</span><span>Inline</span>     <!-- ─── ─── -->
```

| Loại | Tag tiêu biểu | Đặc điểm |
|---|---|---|
| **Block** | `<div>`, `<p>`, `<h1-6>`, `<section>`, `<header>`, `<ul>`, `<table>` | Full width, ngắt dòng |
| **Inline** | `<span>`, `<a>`, `<strong>`, `<em>`, `<img>`, `<code>` | Width = content, không ngắt |
| **Inline-block** | Set qua CSS | Inline nhưng có `width`/`height` |

→ CSS `display: block | inline | inline-block | flex | grid | none` đổi behavior. Học chi tiết [bài 03 CSS](03_css-fundamentals.md).

---

## 5️⃣ Attributes — `id`, `class`, `data-*`

### `id` — Định danh duy nhất

```html
<h1 id="page-title">Hello</h1>
```

- Mỗi `id` **unique** trong trang.
- Dùng cho **anchor link** (`<a href="#page-title">`).
- Dùng cho JS `document.getElementById("page-title")`.
- Hiếm dùng cho CSS (specificity cao quá).

### `class` — Định danh nhóm

```html
<button class="btn btn-primary">Click</button>
<button class="btn btn-secondary">Cancel</button>
```

- Nhiều element có thể cùng class.
- 1 element có nhiều class (space-separated).
- Dùng chủ yếu cho **CSS** và **JS query**.

### `data-*` — Custom data attribute

```html
<button data-user-id="42" data-role="admin">Edit</button>

<script>
  const btn = document.querySelector('button');
  console.log(btn.dataset.userId);     // "42"
  console.log(btn.dataset.role);        // "admin"
</script>
```

→ Hữu ích pass data từ HTML → JS không cần ID/class. **Convention**: tên prefix `data-`, kebab-case trong HTML, camelCase trong JS (`dataset.userId`).

### Boolean attributes

```html
<input type="text" required disabled readonly>
<input type="checkbox" checked>
<button hidden>Won't show</button>
<details open>...</details>
```

→ Boolean = present = true. Không cần `=""`.

---

## 6️⃣ HTML entities — Ký tự đặc biệt

```html
&lt;       →  <
&gt;       →  >
&amp;      →  &
&quot;     →  "
&apos;     →  '
&nbsp;     →  non-breaking space
&copy;     →  ©
&trade;    →  ™
&hellip;   →  …
&mdash;    →  —
&#x1F60A;  →  😊 (Unicode point)
```

→ Khi nội dung có `<`, `>`, `&` → escape thành entity (tránh browser hiểu nhầm).

---

## 7️⃣ Comments

```html
<!-- Đây là comment, không hiển thị -->
<!--
  Multi-line comment
  cũng OK
-->
```

→ ⚠️ Comment **vẫn được gửi đến client** (visible khi view source). Không lưu secret trong comment.

---

## 8️⃣ Bạn viết lại trang `about.html` chuẩn

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Về chúng tôi — Acme Shop</title>
  <meta name="description" content="Acme Shop — cửa hàng điện thoại uy tín tại Hà Nội từ 2024">
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <header>
    <a href="/" class="logo">
      <img src="/logo.svg" alt="Acme Shop logo" width="120" height="40">
    </a>
    <nav>
      <ul>
        <li><a href="/">Trang chủ</a></li>
        <li><a href="/products">Sản phẩm</a></li>
        <li><a href="/about" aria-current="page">Về chúng tôi</a></li>
        <li><a href="/contact">Liên hệ</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <article>
      <h1>Câu chuyện Acme Shop</h1>

      <section>
        <h2>Khởi đầu</h2>
        <p>Acme Shop ra đời năm 2024 tại Hà Nội với sứ mệnh
           <strong>cung cấp điện thoại chính hãng</strong> giá hợp lý.</p>
      </section>

      <section>
        <h2>Đội ngũ</h2>
        <figure>
          <img src="/team.jpg" alt="Đội ngũ Acme Shop" loading="lazy">
          <figcaption>Đội ngũ 10 người tận tâm.</figcaption>
        </figure>
      </section>
    </article>

    <aside>
      <h2>Tin tức mới</h2>
      <ul>
        <li><a href="/news/iphone16">iPhone 16 review</a></li>
        <li><a href="/news/sale">Black Friday 2026</a></li>
      </ul>
    </aside>
  </main>

  <footer>
    <p>&copy; 2026 Acme Shop. <a href="/privacy">Privacy</a></p>
    <p>📞 <a href="tel:+84901234567">090-123-4567</a></p>
  </footer>
</body>
</html>
```

→ Đầy đủ semantic, SEO-friendly, accessible. Senior gật đầu.

---

## 9️⃣ Validate HTML

### W3C Validator

[validator.w3.org](https://validator.w3.org/) — paste HTML hoặc URL → list lỗi syntax.

Lỗi thường gặp:
- Tag không đóng (`<p>` quên `</p>`).
- Tag bằng kiểu HTML4 (`<center>`, `<font>`).
- Attribute deprecated (`<table bgcolor="...">`).
- Skip heading level (h1 → h3).

### Editor support

- VS Code: extension "HTMLHint", "WebHint".
- Format đẹp: Prettier (`shift+option+F`).

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **`<div>` cho mọi thứ** → 2010 style. Semantic tag cho SEO + a11y.
2. **Nhiều `<h1>` 1 trang** → SEO confuse. **1 `<h1>` duy nhất**.
3. **`alt=""` thiếu** trên image content → screen reader bỏ qua. Image trang trí dùng `alt=""`, image nội dung dùng `alt="Mô tả"`.
4. **`target="_blank"` không kèm `rel="noopener"`** → security risk (tab mở có thể đọc `window.opener`).
5. **Comment chứa secret** → visible khi view source. KHÔNG comment API key.

---

## 🧠 Tự kiểm tra (Self-check)

1. Khác **`<section>`** vs **`<article>`** vs **`<div>`**?
2. **`<strong>`** vs **`<b>`** — chọn cái nào, lý do?
3. Bao nhiêu **`<h1>`** trên 1 trang?
4. `target="_blank"` cần kèm attribute gì? Vì sao?
5. Viết HTML5 minimal có header + nav + main + footer.

<details>
<summary>Gợi ý đáp án</summary>

1. **`<article>`** = nội dung **độc lập** (blog post, comment) — đứng riêng vẫn nghĩa. **`<section>`** = nhóm content có **heading + liên quan** (chapter trong trang). **`<div>`** = **non-semantic** — chỉ wrap cho CSS/JS.

2. **`<strong>`** — semantic "quan trọng" + bold visual. **`<b>`** chỉ bold visual không nghĩa. Modern HTML5 prefer `<strong>` / `<em>` — accessible cho screen reader + SEO.

3. **1 duy nhất** — `<h1>` = title trang. Multiple h1 confuse SEO + a11y. Sub-heading dùng `<h2>` trở xuống.

4. `rel="noopener noreferrer"`. Lý do: `noopener` chặn tab mới đọc `window.opener` (security XSS). `noreferrer` không gửi referrer header (privacy).

5. ```html
   <!DOCTYPE html>
   <html lang="vi">
   <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>Demo</title>
   </head>
   <body>
     <header><h1>My Site</h1></header>
     <nav><ul><li><a href="/">Home</a></li></ul></nav>
     <main>
       <article><h2>Welcome</h2><p>Hello!</p></article>
     </main>
     <footer>&copy; 2026</footer>
   </body>
   </html>
   ```
</details>

---

## ⚡ Cheatsheet

### HTML5 boilerplate

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Title</title>
  <meta name="description" content="...">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>...</header>
  <nav>...</nav>
  <main>
    <article>...</article>
  </main>
  <footer>...</footer>
  <script src="app.js" defer></script>
</body>
</html>
```

### Semantic tags quick

```
<header> <nav> <main> <article> <section> <aside> <footer>
<figure> <figcaption>
<h1>-<h6>  <p>  <strong>  <em>  <code>  <pre>
<ul>/<ol> + <li>   <dl> + <dt> + <dd>
<a href> <img alt> <video> <audio> <iframe>
<table> <thead> <tbody> <tfoot> <tr> <th> <td>
```

### Attributes

```
id="unique"
class="btn primary"
data-user-id="42"
required, disabled, checked, hidden
target="_blank" rel="noopener noreferrer"
loading="lazy" (image)
defer / async (script)
```

### HTML entities top

```
&lt;  &gt;  &amp;  &quot;
&nbsp;  &copy;  &mdash;  &hellip;
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **HTML element** | Tag + content + closing tag (`<p>hello</p>`) |
| **Tag** | `<tagname>` / `</tagname>` |
| **Attribute** | Key-value trong tag (`id="x"`, `class="y"`) |
| **Semantic tag** | Tag có nghĩa (`<header>`, `<article>`) |
| **Non-semantic** | `<div>`, `<span>` — không nghĩa |
| **Self-closing tag** | `<img>`, `<br>`, `<hr>` — không có `</...>` |
| **Block element** | Full width, ngắt dòng (`<div>`, `<p>`) |
| **Inline element** | Width = content, không ngắt (`<span>`, `<a>`) |
| **DOCTYPE** | Khai báo HTML version |
| **Meta tag** | Metadata trong `<head>` (charset, viewport, OG, ...) |
| **a11y** | Accessibility (a + 11 letters + y) |
| **`alt` text** | Description ảnh — bắt buộc cho a11y |
| **Open Graph (OG)** | Meta tag cho preview Facebook/Slack |
| **W3C Validator** | Tool check HTML syntax |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [HTML & CSS là gì? — Nền tảng frontend web](00_what-is-html-and-css.md)
- ➡️ **Bài tiếp theo:** [Forms & Accessibility — Input đúng cách + a11y basic](02_forms-and-accessibility.md)
- ↑ **Về cụm:** [html-css README](../../README.md)

### 🌐 Tài nguyên tham khảo khác
- 📖 [MDN — HTML elements reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Element)
- 📖 [HTML Living Standard](https://html.spec.whatwg.org/) — spec
- 📖 [W3C Markup Validator](https://validator.w3.org/)
- 📖 [HTML5 Doctor](http://html5doctor.com/) — semantic deep dive
- 📖 [Can I use](https://caniuse.com/) — browser support

---

> 🎯 *Sau bài này bạn viết trang HTML5 đầy đủ structure. Bài kế tiếp dạy **forms + accessibility** — interactive web phải đẹp + dùng được cho mọi user.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `html-css/` lesson 2/5. Cover: HTML5 structure đầy đủ (8 meta cho SEO + social + viewport) + semantic tags (header/nav/main/article/section/aside/footer) + common tags (heading/list/link/image/table) + form basics + best practices (alt text, lang attr).
- **v1.1.0 (25/05/2026)** — Bổ sung lời dẫn trước các mục HTML5 structure, Vai trò meta, Anti-pattern div, Semantic HTML5, Bảng semantic tags. Chuẩn hoá tên thương hiệu ví dụ thành `Acme Shop`. Thêm mục Changelog.
