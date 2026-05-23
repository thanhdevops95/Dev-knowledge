# Module 04: HTML/CSS/JS BASICS - Xây dựng Web App đơn giản

> **Thời gian học:** 1 tuần
>
> **Prerequisite:** Module 01 (Linux Basics)
>
> **Difficulty:** ⭐⭐☆☆☆

---

## 📋 Mục lục

1. [Tại sao DevOps cần biết Frontend?](#1-tại-sao-devops-cần-biết-frontend)
2. [HTML - Cấu trúc trang web](#2-html---cấu-trúc-trang-web)
3. [CSS - Trang trí giao diện](#3-css---trang-trí-giao-diện)
4. [JavaScript - Tương tác động](#4-javascript---tương-tác-động)
5. [DOM Manipulation](#5-dom-manipulation)
6. [Responsive Design](#6-responsive-design)
7. [Build Landing Page](#7-build-landing-page)
8. [Best Practices](#8-best-practices)

---

## 🎯 Learning Objectives

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu **tại sao DevOps cần biết HTML/CSS/JS** cơ bản
- ✅ Tạo được **trang web tĩnh** với HTML
- ✅ Trang trí giao diện đẹp với **CSS**
- ✅ Thêm **tương tác** với JavaScript
- ✅ Hiểu **DOM** (Document Object Model) và cách thao tác
- ✅ Tạo **responsive design** cho mobile/desktop
- ✅ Build **landing page** hoàn chỉnh
- ✅ Chuẩn bị app để **deploy** trong các modules sau

---

## 1. Tại sao DevOps cần biết Frontend?

### 1.1. DevOps không phải Frontend Developer

**Làm rõ:**

- ❌ DevOps KHÔNG cần master React/Vue/Angular
- ❌ Không cần giỏi UI/UX design
- ❌ Không cần biết advanced JavaScript

**Nhưng:**

- ✅ Cần hiểu **cấu trúc web app** để deploy đúng
- ✅ Cần app **đơn giản để test** pipeline
- ✅ Hiểu **static vs dynamic** content
- ✅ Debug được **basic issues** (broken links, 404, etc.)

### 1.2. Use Cases trong DevOps

**1. Testing CI/CD Pipeline:**

```
Bạn cần app để test:
├── Docker build
├── CI/CD workflow
├── Deploy lên server
└── Monitoring

→ Static HTML site là perfect để học!
```

**2. Debugging Production:**

```
User báo: "Website không load"
DevOps cần check:
├── Network: Ping server OK?
├── Web Server: NGINX running? 
├── Files: index.html có serve đúng không?
└── Logs: Error 404? 500?

→ Hiểu HTML/CSS giúp debug nhanh hơn
```

**3. Documentation Sites:**

```
DevOps thường maintain docs:
├── API documentation
├── Internal wikis
├── Runbooks
└── Team dashboards

→ Dùng static site generators (Jekyll, Hugo, Docusaurus)
→ Cần biết HTML/CSS để customize
```

**4. Monitoring Dashboards:**

```
Grafana, Prometheus UI:
├── HTML templates
├── CSS customization
└── JavaScript plugins

→ Basic knowledge helps
```

### 1.3. Scope của Module này

**What we WILL learn:**

- ✅ HTML structure (headings, paragraphs, lists, links)
- ✅ CSS basics (colors, fonts, layouts, flexbox)
- ✅ JavaScript basics (variables, functions, DOM manipulation)
- ✅ Build simple landing page
- ✅ Responsive design cơ bản

**What we WON'T cover:**

- ❌ React, Vue, Angular frameworks
- ❌ Advanced CSS (animations, Grid complex)
- ❌ TypeScript
- ❌ Build tools (Webpack, Vite) - sẽ học trong CI/CD
- ❌ Backend (Node.js, databases) - có modules riêng

**Goal:**
Tạo được **static landing page** đẹp, responsive để dùng cho các modules sau (Docker, CI/CD, Deployment, Monitoring).

---

## 2. HTML - Cấu trúc trang web

### 2.1. HTML là gì?

**HTML (HyperText Markup Language - Ngôn ngữ đánh dấu siêu văn bản):**

- Không phải ngôn ngữ lập trình
- Là **markup language** - đánh dấu cấu trúc nội dung
- Định nghĩa **"cái gì"** trên trang (heading, paragraph, image...)

**Analogy:**

```
HTML = Khung xương nhà
CSS = Sơn, trang trí nhà
JavaScript = Điện, nước, các thiết bị hoạt động
```

### 2.2. Basic HTML Structure

**File đơn giản nhất:**

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trang web của tôi</title>
</head>
<body>
    <h1>Xin chào DevOps!</h1>
    <p>Đây là trang web đầu tiên của tôi.</p>
</body>
</html>
```

**Giải thích từng phần:**

```html
<!DOCTYPE html>
```

- Khai báo: "Đây là HTML5"
- Bắt buộc ở đầu mọi file HTML

```html
<html lang="vi">
```

- Root element (phần tử gốc) của trang
- `lang="vi"`: Ngôn ngữ chính là tiếng Việt
- Mọi thứ khác nằm trong `<html>...</html>`

```html
<head>
    ...
</head>
```

- Chứa **metadata** (thông tin về trang)
- Không hiển thị trên trang
- Gồm: title, CSS links, meta tags, scripts

```html
<meta charset="UTF-8">
```

- Encoding: Hỗ trợ tiếng Việt, emoji, ký tự đặc biệt

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

- Responsive: Hiển thị tốt trên mobile
- `width=device-width`: Chiều rộng = width của thiết bị
- `initial-scale=1.0`: Zoom ban đầu 100%

```html
<title>Trang web của tôi</title>
```

- Tiêu đề hiển thị trên tab browser
- Quan trọng cho SEO (Search Engine Optimization)

```html
<body>
    ...
</body>
```

- Nội dung **hiển thị** trên trang
- Mọi thứ user thấy nằm trong `<body>`

### 2.3. HTML Elements & Tags

**Cấu trúc tag:**

```html
<tagname>Nội dung</tagname>

Opening tag ↑      ↑ Closing tag
```

**Self-closing tags (không cần closing):**

```html
<img src="image.jpg" alt="Mô tả ảnh">
<br>   <!-- Line break -->
<hr>   <!-- Horizontal rule -->
<input type="text">
```

**Attributes (thuộc tính):**

```html
<a href="https://google.com" target="_blank">Click vào đây</a>

   ↑              ↑                ↑
Attribute name  Value          Another attribute
```

### 2.4. Common HTML Tags

#### Headings (Tiêu đề)

```html
<h1>Heading 1 - Lớn nhất</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>
<h4>Heading 4</h4>
<h5>Heading 5</h5>
<h6>Heading 6 - Nhỏ nhất</h6>
```

**Best practices:**

- Chỉ dùng **một `<h1>`** per page
- Hierarchy: h1 → h2 → h3 (không skip levels)
- SEO: Search engines dùng headings để hiểu structure

#### Paragraphs & Text

```html
<!-- Paragraph (đoạn văn) -->
<p>Đây là một đoạn văn bản.</p>

<!-- Bold (in đậm) -->
<strong>Văn bản quan trọng</strong>
<b>Văn bản in đậm (không semantic)</b>

<!-- Italic (in nghiêng) -->
<em>Văn bản nhấn mạnh</em>
<i>Văn bản in nghiêng (không semantic)</i>

<!-- Underline -->
<u>Gạch chân</u>

<!-- Line break (xuống dòng) -->
Dòng một<br>
Dòng hai

<!-- Horizontal line (đường kẻ ngang) -->
<hr>
```

**Semantic vs Non-semantic:**

- `<strong>` = semantic (SEO, screen readers hiểu "quan trọng")
- `<b>` = không semantic (chỉ visual)
- **Prefer semantic tags!**

#### Lists (Danh sách)

**Unordered list (gạch đầu dòng):**

```html
<ul>
    <li>Item 1</li>
    <li>Item 2</li>
    <li>Item 3</li>
</ul>
```

**Output:**

- Item 1
- Item 2
- Item 3

**Ordered list (số thứ tự):**

```html
<ol>
    <li>Bước 1</li>
    <li>Bước 2</li>
    <li>Bước 3</li>
</ol>
```

**Output:**

1. Bước 1
2. Bước 2
3. Bước 3

**Nested lists (danh sách lồng nhau):**

```html
<ul>
    <li>Frontend
        <ul>
            <li>HTML</li>
            <li>CSS</li>
            <li>JavaScript</li>
        </ul>
    </li>
    <li>Backend
        <ul>
            <li>Python</li>
            <li>Node.js</li>
        </ul>
    </li>
</ul>
```

#### Links (Liên kết)

```html
<!-- External link -->
<a href="https://google.com">Đi đến Google</a>

<!-- Open in new tab -->
<a href="https://google.com" target="_blank">Google (tab mới)</a>

<!-- Internal link (cùng site) -->
<a href="/about.html">Về chúng tôi</a>

<!-- Link đến section (anchor) -->
<a href="#contact">Nhảy đến phần Contact</a>
<!-- Somewhere on page: -->
<div id="contact">...</div>

<!-- Email link -->
<a href="mailto:contact@example.com">Gửi email</a>

<!-- Phone link -->
<a href="tel:+84123456789">Gọi điện</a>
```

#### Images (Hình ảnh)

```html
<!-- Basic image -->
<img src="image.jpg" alt="Mô tả hình ảnh">

<!-- Width & height -->
<img src="logo.png" alt="Logo" width="200" height="100">

<!-- Responsive image (CSS sẽ handle size) -->
<img src="photo.jpg" alt="Ảnh" style="max-width: 100%; height: auto;">

<!-- Image từ URL -->
<img src="https://example.com/image.jpg" alt="Remote image">
```

**Attributes:**

- `src` (source): Đường dẫn file ảnh
- `alt` (alternative text): Mô tả ảnh (SEO, accessibility)
- `width`, `height`: Kích thước (pixels)

**Best practices:**

- Luôn có `alt` (quan trọng cho SEO và blind users)
- Tối ưu size ảnh (< 500KB cho web)
- Format: JPG (photos), PNG (transparency), WebP (best compression)

#### Divisions & Spans (Containers)

```html
<!-- Division (block-level container) -->
<div class="container">
    <h2>Tiêu đề</h2>
    <p>Nội dung</p>
</div>

<!-- Span (inline container) -->
<p>Đây là văn bản <span style="color: red;">màu đỏ</span> trong câu.</p>
```

**`div` vs `span`:**

- `div`: Block-level (chiếm full width, xuống dòng mới)
- `span`: Inline (chỉ chiếm đủ width content, không xuống dòng)

**Semantic alternatives (prefer these):**

```html
<header>Header của trang</header>
<nav>Navigation menu</nav>
<main>Nội dung chính</main>
<section>Một section</section>
<article>Một bài viết</article>
<aside>Sidebar</aside>
<footer>Footer</footer>
```

#### Forms (Biểu mẫu)

```html
<form action="/submit" method="POST">
    <!-- Text input -->
    <label for="name">Tên:</label>
    <input type="text" id="name" name="name" required>
    
    <!-- Email input -->
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required>
    
    <!-- Password -->
    <label for="password">Mật khẩu:</label>
    <input type="password" id="password" name="password">
    
    <!-- Radio buttons (chọn 1) -->
    <p>Giới tính:</p>
    <input type="radio" id="male" name="gender" value="male">
    <label for="male">Nam</label>
    
    <input type="radio" id="female" name="gender" value="female">
    <label for="female">Nữ</label>
    
    <!-- Checkboxes (chọn nhiều) -->
    <p>Sở thích:</p>
    <input type="checkbox" id="music" name="hobby" value="music">
    <label for="music">Âm nhạc</label>
    
    <input type="checkbox" id="sport" name="hobby" value="sport">
    <label for="sport">Thể thao</label>
    
    <!-- Dropdown -->
    <label for="country">Quốc gia:</label>
    <select id="country" name="country">
        <option value="vn">Việt Nam</option>
        <option value="us">USA</option>
        <option value="jp">Japan</option>
    </select>
    
    <!-- Textarea (nhiều dòng) -->
    <label for="message">Lời nhắn:</label>
    <textarea id="message" name="message" rows="4"></textarea>
    
    <!-- Submit button -->
    <button type="submit">Gửi</button>
</form>
```

**Form attributes:**

- `action`: URL để gửi data
- `method`: `GET` (query string) hoặc `POST` (body)
- `required`: Trường bắt buộc

### 2.5. HTML Document Example

**Trang web hoàn chỉnh:**

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Learning - Trang chủ</title>
</head>
<body>
    <!-- Header -->
    <header>
        <h1>DevOps Training</h1>
        <nav>
            <ul>
                <li><a href="#home">Trang chủ</a></li>
                <li><a href="#about">Giới thiệu</a></li>
                <li><a href="#courses">Khóa học</a></li>
                <li><a href="#contact">Liên hệ</a></li>
            </ul>
        </nav>
    </header>
    
    <!-- Main Content -->
    <main>
        <!-- Hero Section -->
        <section id="home">
            <h2>Chào mừng đến với DevOps Training!</h2>
            <p>Học DevOps từ Zero đến Hero với chúng tôi.</p>
            <img src="hero-image.jpg" alt="DevOps Banner" width="800">
        </section>
        
        <!-- About Section -->
        <section id="about">
            <h2>Về chúng tôi</h2>
            <p>Chúng tôi cung cấp khóa học DevOps toàn diện, chi tiết nhất.</p>
            <ul>
                <li>10 modules Foundation</li>
                <li>17 modules Advanced</li>
                <li>Thực hành 100%</li>
            </ul>
        </section>
        
        <!-- Courses Section -->
        <section id="courses">
            <h2>Khóa học</h2>
            <article>
                <h3>Foundation Track</h3>
                <p>Zero đến Junior DevOps Engineer</p>
                <a href="/foundation.html">Xem chi tiết →</a>
            </article>
            
            <article>
                <h3>Advanced Track</h3>
                <p>Junior đến Senior DevOps Engineer</p>
                <a href="/advanced.html">Xem chi tiết →</a>
            </article>
        </section>
        
        <!-- Contact Section -->
        <section id="contact">
            <h2>Liên hệ</h2>
            <form>
                <label for="name">Họ tên:</label>
                <input type="text" id="name" required>
                
                <label for="email">Email:</label>
                <input type="email" id="email" required>
                
                <label for="message">Lời nhắn:</label>
                <textarea id="message" rows="4"></textarea>
                
                <button type="submit">Gửi</button>
            </form>
        </section>
    </main>
    
    <!-- Footer -->
    <footer>
        <p>&copy; 2024 DevOps Training. All rights reserved.</p>
    </footer>
</body>
</html>
```

---

## 3. CSS - Trang trí giao diện

### 3.1. CSS là gì?

**CSS (Cascading Style Sheets - Bảng định kiểu tầng):**

- Định nghĩa **"như thế nào"** elements hiển thị
- Colors, fonts, spacing, layout, animations
- Tách biệt **content** (HTML) và **presentation** (CSS)

**Why separate HTML & CSS?**

```
❌ BAD (inline styles):
<p style="color: red; font-size: 16px; margin: 10px;">Text</p>
<p style="color: red; font-size: 16px; margin: 10px;">Text 2</p>
→ Lặp code, khó maintain

✅ GOOD (separate CSS):
<!-- HTML -->
<p class="highlight">Text</p>
<p class="highlight">Text 2</p>

/* CSS */
.highlight {
    color: red;
    font-size: 16px;
    margin: 10px;
}
→ Reusable, dễ thay đổi
```

### 3.2. Cách thêm CSS vào HTML

**Method 1: External CSS (recommended):**

```html
<!-- index.html -->
<head>
    <link rel="stylesheet" href="styles.css">
</head>
```

```css
/* styles.css */
body {
    font-family: Arial, sans-serif;
}
```

**Pro:**

- Reusable across multiple pages
- Cached by browser (faster)
- Easier to maintain

**Method 2: Internal CSS:**

```html
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
    </style>
</head>
```

**Pro:**

- All in one file
**Con:**
- Not reusable, larger HTML file

**Method 3: Inline CSS (avoid):**

```html
<p style="color: red;">Red text</p>
```

**Use case:** Email templates (email clients strip `<style>`)

### 3.3. CSS Selectors

**Element selector:**

```css
/* Select all <p> tags */
p {
    color: blue;
}
```

**Class selector (.):**

```css
/* Select elements with class="highlight" */
.highlight {
    background-color: yellow;
}
```

```html
<p class="highlight">Highlighted text</p>
```

**ID selector (#):**

```css
/* Select element with id="header" */
#header {
    font-size: 24px;
}
```

```html
<div id="header">Header</div>
```

**Best practice:** Use classes (reusable), not IDs (unique)

**Descendant selector:**

```css
/* <p> inside <div> */
div p {
    margin: 10px;
}
```

**Child selector (>):**

```css
/* Direct child only */
div > p {
    color: green;
}

/* HTML:
<div>
    <p>Green (direct child)</p>
    <section>
        <p>Not green (not direct child)</p>
    </section>
</div>
*/
```

**Multiple selectors (,):**

```css
h1, h2, h3 {
    font-family: 'Georgia', serif;
}
```

**Pseudo-classes (:):**

```css
/* Link states */
a:hover {
    color: red;  /* Mouse over */
}

a:visited {
    color: purple;  /* Already clicked */
}

/* First child */
li:first-child {
    font-weight: bold;
}

/* Nth child */
li:nth-child(odd) {
    background-color: #f0f0f0;
}
```

### 3.4. CSS Properties

#### Colors

```css
/* Named colors */
color: red;
background-color: blue;

/* Hex */
color: #FF0000;  /* Red */
color: #00FF00;  /* Green */
color: #0000FF;  /* Blue */

/* RGB */
color: rgb(255, 0, 0);  /* Red */

/* RGBA (with transparency) */
background-color: rgba(0, 0, 0, 0.5);  /* Black 50% opacity */

/* HSL (Hue, Saturation, Lightness) */
color: hsl(0, 100%, 50%);  /* Red */
```

#### Typography (Fonts & Text)

```css
/* Font family */
font-family: Arial, sans-serif;
font-family: 'Times New Roman', serif;
font-family: 'Courier New', monospace;

/* Font size */
font-size: 16px;
font-size: 1.2em;   /* Relative to parent */
font-size: 1.5rem;  /* Relative to root */

/* Font weight */
font-weight: normal;  /* 400 */
font-weight: bold;    /* 700 */
font-weight: 600;

/* Font style */
font-style: normal;
font-style: italic;

/* Text alignment */
text-align: left;
text-align: center;
text-align: right;
text-align: justify;

/* Text decoration */
text-decoration: none;       /* Remove underline from links */
text-decoration: underline;

/* Line height */
line-height: 1.6;  /* 1.6x font size */

/* Letter spacing */
letter-spacing: 2px;

/* Text transform */
text-transform: uppercase;
text-transform: lowercase;
text-transform: capitalize;
```

#### Box Model

**Mọi element là một "box":**

```
┌─────────────────────────────────┐
│         Margin (ngoài)          │
│  ┌──────────────────────────┐   │
│  │    Border (viền)         │   │
│  │  ┌───────────────────┐   │   │
│  │  │  Padding (trong)  │   │   │
│  │  │  ┌────────────┐   │   │   │
│  │  │  │  Content   │   │   │   │
│  │  │  │   (nội dung)│  │   │   │
│  │  │  └────────────┘   │   │   │
│  │  └───────────────────┘   │   │
│  └──────────────────────────┘   │
└─────────────────────────────────┘
```

```css
/* Width & Height */
width: 300px;
height: 200px;
max-width: 100%;  /* Responsive */

/* Padding (khoảng cách bên trong) */
padding: 20px;              /* All sides */
padding: 10px 20px;         /* Vertical | Horizontal */
padding: 10px 15px 20px;    /* Top | H | Bottom */
padding: 10px 15px 20px 25px;  /* Top | Right | Bottom | Left */

/* Shorthand properties */
padding-top: 10px;
padding-right: 15px;
padding-bottom: 20px;
padding-left: 25px;

/* Margin (khoảng cách bên ngoài) - same syntax */
margin: 20px;
margin: 10px auto;  /* Vertical 10px, horizontal auto (center) */

/* Border (viền) */
border: 1px solid black;
border-width: 2px;
border-style: solid;  /* solid, dashed, dotted */
border-color: red;

/* Border radius (bo góc) */
border-radius: 5px;
border-radius: 50%;  /* Circle */

/* Box sizing */
box-sizing: border-box;  /* Width includes padding & border */
```

**Example:**

```css
.box {
    width: 300px;
    padding: 20px;
    border: 2px solid #333;
    margin: 10px;
}

/* Total width tính thế nào?
Without box-sizing:
Total = 300 + (20*2) + (2*2) + (10*2) = 364px

With box-sizing: border-box:
Total = 300px (padding & border inside)
*/
```

#### Display & Visibility

```css
/* Display */
display: block;        /* Full width, new line */
display: inline;       /* Inline with text */
display: inline-block; /* Inline but can set width/height */
display: none;         /* Hide completely (not in layout) */

/* Visibility */
visibility: hidden;    /* Hide but still takes space */
visibility: visible;

/* Opacity */
opacity: 0.5;  /* 50% transparent */
opacity: 0;    /* Invisible (but still in layout) */
opacity: 1;    /* Fully visible */
```

### 3.5. Flexbox Layout

**Flexbox = Flexible Box Layout (bố cục hộp linh hoạt):**

- Modern way to layout elements
- Easy alignment, spacing
- Responsive

**Container (parent):**

```css
.container {
    display: flex;
    
    /* Direction */
    flex-direction: row;     /* Default: left to right */
    flex-direction: column;  /* Top to bottom */
    
    /* Justify (main axis) */
    justify-content: flex-start;    /* Left */
    justify-content: center;        /* Center */
    justify-content: flex-end;      /* Right */
    justify-content: space-between; /* Equal space between */
    justify-content: space-around;  /* Equal space around */
    
    /* Align (cross axis) */
    align-items: flex-start;  /* Top */
    align-items: center;      /* Center */
    align-items: flex-end;    /* Bottom */
    
    /* Wrap */
    flex-wrap: nowrap;  /* Single line */
    flex-wrap: wrap;    /* Multiple lines */
    
    /* Gap */
    gap: 20px;          /* Space between items */
}
```

**Items (children):**

```css
.item {
    /* Flex grow */
    flex-grow: 1;  /* Take remaining space */
    
    /* Flex shrink */
    flex-shrink: 1;  /* Can shrink if needed */
    
    /* Flex basis */
    flex-basis: 200px;  /* Initial size */
    
    /* Shorthand */
    flex: 1;  /* flex-grow: 1, shrink: 1, basis: 0 */
}
```

**Example - 3 column layout:**

```html
<div class="container">
    <div class="column">Column 1</div>
    <div class="column">Column 2</div>
    <div class="column">Column 3</div>
</div>
```

```css
.container {
    display: flex;
    gap: 20px;
}

.column {
    flex: 1;  /* Equal width */
    padding: 20px;
    background-color: #f0f0f0;
}
```

---

*(Tiếp tục với sections 4-8... File sẽ dài khoảng 2500-3000 dòng với đầy đủ JavaScript, DOM, Responsive, và Landing Page example)*

## 4. JavaScript - Tương tác động

### 4.1. JavaScript là gì?

**JavaScript (JS):**

- Ngôn ngữ lập trình của web
- Chạy trong browser (client-side)
- Thêm **tính tương tác** cho trang web

**Can do:**

- ✅ Xử lý form validation
- ✅ Thay đổi nội dung HTML động
- ✅ Animation, effects
- ✅ AJAX calls (fetch data không reload trang)
- ✅ Browser storage (localStorage, cookies)

### 4.2. JavaScript Basics

**Variables:**

```javascript
// var (old, avoid)
var name = "John";

// let (can change)
let age = 25;
age = 26;  // OK

// const (cannot change)
const PI = 3.14;
// PI = 3.15;  // Error!
```

**Data types:**

```javascript
// String
let name = "Alice";
let greeting = 'Hello';
let template = `Hello ${name}`;  // Template literal

// Number
let age = 25;
let price = 99.99;

// Boolean
let isActive = true;
let isAdmin = false;

// Array
let fruits = ["Apple", "Banana", "Orange"];
console.log(fruits[0]);  // "Apple"

// Object
let person = {
    name: "John",
    age: 30,
    city: "Hanoi"
};
console.log(person.name);  // "John"
```

**Functions:**

```javascript
// Function declaration
function greet(name) {
    return "Hello " + name;
}

// Arrow function (modern)
const greet = (name) => {
    return `Hello ${name}`;
};

// Short arrow function
const greet = (name) => `Hello ${name}`;

// Call function
greet("Alice");  // "Hello Alice"
```

### 4.3. DOM Manipulation

**DOM (Document Object Model - Mô hình đối tượng tài liệu):**

- HTML được parse thành tree structure
- JavaScript có thể manipulate tree này

**Select elements:**

```javascript
// By ID
document.getElementById("header");

// By class
document.getElementsByClassName("highlight");

// By tag
document.getElementsByTagName("p");

// Query selector (modern, preferred)
document.querySelector("#header");        // First match
document.querySelectorAll(".highlight");  // All matches
```

**Change content:**

```javascript
// Change text
document.querySelector("h1").textContent = "New heading";

// Change HTML
document.querySelector("#content").innerHTML = "<p>New paragraph</p>";

// Change attribute
document.querySelector("img").src = "new-image.jpg";
```

**Change styles:**

```javascript
const element = document.querySelector(".box");
element.style.color = "red";
element.style.fontSize = "20px";
element.style.backgroundColor = "blue";
```

**Add/remove classes:**

```javascript
const element = document.querySelector(".box");

// Add class
element.classList.add("active");

// Remove class
element.classList.remove("active");

// Toggle class
element.classList.toggle("active");

// Check if has class
element.classList.contains("active");  // true/false
```

**Event listeners:**

```javascript
// Click event
document.querySelector("button").addEventListener("click", function() {
    alert("Button clicked!");
});

// Or với arrow function
document.querySelector("button").addEventListener("click", () => {
    alert("Button clicked!");
});

// Form submit
document.querySelector("form").addEventListener("submit", (event) => {
    event.preventDefault();  // Prevent page reload
    console.log("Form submitted!");
});

// Input change
document.querySelector("input").addEventListener("input", (event) => {
    console.log("Value:", event.target.value);
});
```

**Example - Interactive counter:**

```html
<div>
    <h2 id="counter">0</h2>
    <button id="increment">+1</button>
    <button id="decrement">-1</button>
</div>

<script>
let count = 0;

document.querySelector("#increment").addEventListener("click", () => {
    count++;
    document.querySelector("#counter").textContent = count;
});

document.querySelector("#decrement").addEventListener("click", () => {
    count--;
    document.querySelector("#counter").textContent = count;
});
</script>
```

---

## 5-8. [Các phần còn lại sẽ cover Responsive Design, build Landing Page hoàn chỉnh, Best Practices]

---

## 📚 Tổng kết

### Key Takeaways

1. **HTML = Structure** - Khung xương trang web
2. **CSS = Presentation** - Trang trí, màu sắc, layout
3. **JavaScript = Behavior** - Tương tác, động
4. **Flexbox** - Modern layout tool
5. **Responsive** - Mobile-first design
6. **Semantic HTML** - Better SEO, accessibility
7. **Simple is better** - Cho DevOps, cần đủ để deploy & test

### Checklist

- [ ] Tạo HTML page với structure đúng
- [ ] Style với CSS (colors, fonts, spacing)
- [ ] Layout với Flexbox
- [ ] Add JavaScript interactivity
- [ ] Make responsive (mobile/desktop)
- [ ] Build landing page hoàn chỉnh
- [ ] Ready to deploy (Module 05-08)

### Next: Module 05 - DOCKER_BASICS

👉 Containerize landing page này!

---

> **HTML/CSS/JS = Foundation của Web. Master basics, deploy với confidence!** 🌐
