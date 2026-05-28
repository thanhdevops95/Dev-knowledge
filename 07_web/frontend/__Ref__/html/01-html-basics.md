# 🎨 HTML — Nền tảng của Web

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Xương sống của mọi trang web

---

## HTML là gì?

**HTML (HyperText Markup Language)** là ngôn ngữ đánh dấu để cấu trúc nội dung trên web. HTML **không phải** ngôn ngữ lập trình — nó mô tả *cấu trúc* và *ý nghĩa* của nội dung.

---

## Cấu trúc tài liệu HTML

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Mô tả trang web cho SEO">
    <title>Tiêu đề trang</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Nội dung trang -->
    <script src="main.js" defer></script>
</body>
</html>
```

---

## Semantic HTML ⭐

Dùng đúng tag để mô tả ý nghĩa nội dung (quan trọng cho SEO và Accessibility):

```html
<!-- ❌ Không semantic -->
<div class="header">
    <div class="nav">...</div>
</div>
<div class="main">
    <div class="article">...</div>
</div>

<!-- ✅ Semantic HTML -->
<header>
    <nav>
        <ul>
            <li><a href="/">Trang chủ</a></li>
            <li><a href="/about">Giới thiệu</a></li>
        </ul>
    </nav>
</header>

<main>
    <article>
        <h1>Tiêu đề bài viết</h1>
        <section>
            <h2>Phần 1</h2>
            <p>Nội dung...</p>
        </section>
    </article>
    
    <aside>
        <p>Nội dung phụ, sidebar</p>
    </aside>
</main>

<footer>
    <p>&copy; 2026 Dev-Knowledge</p>
</footer>
```

---

## Các thẻ quan trọng

### Heading & Text
```html
<h1>Tiêu đề lớn nhất (chỉ 1 cái/trang)</h1>
<h2>Tiêu đề phụ</h2>
<h3>Tiêu đề nhỏ hơn</h3>

<p>Đoạn văn</p>
<strong>Chữ đậm (quan trọng)</strong>
<em>Chữ nghiêng (nhấn mạnh)</em>
<code>inline code</code>
<pre><code>Block code</code></pre>
<blockquote>Trích dẫn</blockquote>
<mark>Đánh dấu highlight</mark>
<del>Gạch bỏ</del>
<br>    <!-- Xuống dòng -->
<hr>    <!-- Đường kẻ ngang -->
```

### Links & Images
```html
<!-- Link -->
<a href="https://example.com" target="_blank" rel="noopener noreferrer">
    Liên kết ngoài
</a>
<a href="/about">Liên kết trong</a>
<a href="#section-id">Liên kết anchor</a>
<a href="mailto:email@example.com">Email</a>

<!-- Image -->
<img
    src="photo.jpg"
    alt="Mô tả ảnh (quan trọng cho accessibility!)"
    width="800"
    height="600"
    loading="lazy"
>

<!-- Figure với caption -->
<figure>
    <img src="chart.png" alt="Biểu đồ doanh thu 2026">
    <figcaption>Hình 1: Biểu đồ doanh thu năm 2026</figcaption>
</figure>
```

### Lists
```html
<!-- Unordered list -->
<ul>
    <li>Item 1</li>
    <li>Item 2</li>
    <li>
        Item 3
        <ul>
            <li>Nested item</li>
        </ul>
    </li>
</ul>

<!-- Ordered list -->
<ol type="1">    <!-- 1, a, A, i, I -->
    <li>Bước 1</li>
    <li>Bước 2</li>
</ol>

<!-- Description list -->
<dl>
    <dt>HTML</dt>
    <dd>HyperText Markup Language</dd>
    <dt>CSS</dt>
    <dd>Cascading Style Sheets</dd>
</dl>
```

---

## Forms ⭐

```html
<form action="/submit" method="POST" novalidate>
    <!-- Text input -->
    <label for="email">Email:</label>
    <input
        type="email"
        id="email"
        name="email"
        placeholder="jesse@example.com"
        required
        autocomplete="email"
    >

    <!-- Password -->
    <input type="password" name="password" minlength="8" required>

    <!-- Number -->
    <input type="number" name="age" min="18" max="100">

    <!-- Checkbox -->
    <label>
        <input type="checkbox" name="agree" value="yes" required>
        Tôi đồng ý với điều khoản
    </label>

    <!-- Radio -->
    <fieldset>
        <legend>Giới tính:</legend>
        <label><input type="radio" name="gender" value="male"> Nam</label>
        <label><input type="radio" name="gender" value="female"> Nữ</label>
    </fieldset>

    <!-- Select -->
    <select name="country">
        <option value="">-- Chọn quốc gia --</option>
        <option value="vn" selected>Việt Nam</option>
        <option value="us">United States</option>
    </select>

    <!-- Textarea -->
    <textarea name="message" rows="5" cols="40" maxlength="500"></textarea>

    <!-- File upload -->
    <input type="file" name="avatar" accept="image/*">

    <!-- Date & Time -->
    <input type="date" name="birthday">
    <input type="time" name="meeting">
    <input type="datetime-local" name="event">

    <!-- Range slider -->
    <input type="range" name="volume" min="0" max="100" step="5">

    <!-- Submit -->
    <button type="submit">Gửi</button>
    <button type="reset">Xóa</button>
    <button type="button" onclick="handleClick()">Custom</button>
</form>
```

---

## Tables

```html
<table>
    <caption>Bảng điểm học sinh</caption>
    <thead>
        <tr>
            <th scope="col">Họ tên</th>
            <th scope="col">Toán</th>
            <th scope="col">Văn</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Nguyễn Văn A</td>
            <td>9.5</td>
            <td>8.0</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td>Trung bình</td>
            <td>8.8</td>
            <td>7.5</td>
        </tr>
    </tfoot>
</table>
```

---

## Multimedia

```html
<!-- Video -->
<video controls width="640" height="360" poster="thumbnail.jpg">
    <source src="video.mp4" type="video/mp4">
    <source src="video.webm" type="video/webm">
    <p>Trình duyệt không hỗ trợ video.</p>
</video>

<!-- Audio -->
<audio controls>
    <source src="audio.mp3" type="audio/mpeg">
    <source src="audio.ogg" type="audio/ogg">
</audio>

<!-- Embed iframe -->
<iframe
    src="https://www.youtube.com/embed/VIDEO_ID"
    width="560"
    height="315"
    loading="lazy"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media"
    allowfullscreen
></iframe>
```

---

## Meta Tags cho SEO

```html
<head>
    <!-- Basic SEO -->
    <title>Tên trang | Tên website</title>
    <meta name="description" content="Mô tả trang, khoảng 150-160 ký tự">
    <meta name="keywords" content="từ khóa1, từ khóa2">
    <link rel="canonical" href="https://example.com/page">

    <!-- Open Graph (Facebook, LinkedIn) -->
    <meta property="og:title" content="Tiêu đề khi share">
    <meta property="og:description" content="Mô tả khi share">
    <meta property="og:image" content="https://example.com/image.jpg">
    <meta property="og:url" content="https://example.com/page">
    <meta property="og:type" content="website">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Tiêu đề">
    <meta name="twitter:description" content="Mô tả">
    <meta name="twitter:image" content="https://example.com/image.jpg">
</head>
```

---

## Accessibility (a11y) cơ bản

```html
<!-- 1. Luôn có alt cho img -->
<img src="logo.png" alt="Logo công ty">
<img src="decoration.png" alt="" role="presentation">  <!-- ảnh trang trí -->

<!-- 2. Label cho form inputs -->
<label for="username">Tên đăng nhập:</label>
<input type="text" id="username" name="username">

<!-- 3. ARIA labels khi không có text visible -->
<button aria-label="Đóng menu">✕</button>
<nav aria-label="Menu chính"></nav>

<!-- 4. Skip navigation link -->
<a href="#main-content" class="skip-link">Bỏ qua phần điều hướng</a>

<!-- 5. Role và landmark -->
<div role="alert">Thông báo quan trọng!</div>
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title"></div>

<!-- 6. Keyboard accessible -->
<div tabindex="0" role="button" onkeypress="handleKey(event)">
    Có thể focus bằng Tab
</div>
```

---

## Bài tập thực hành

- [ ] Tạo trang portfolio cá nhân chỉ dùng HTML (chưa cần CSS)
- [ ] Validate HTML với [W3C Validator](https://validator.w3.org/)
- [ ] Kiểm tra Accessibility với axe DevTools extension
- [ ] Clone structure của 1 trang web thật (chỉ HTML, không CSS)

---

## Tài nguyên thêm

- [MDN HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) — Tài liệu đầy đủ nhất
- [HTML Reference](https://htmlreference.io/) — Tham khảo visual
- [The A11Y Project](https://www.a11yproject.com/) — Accessibility checklist
