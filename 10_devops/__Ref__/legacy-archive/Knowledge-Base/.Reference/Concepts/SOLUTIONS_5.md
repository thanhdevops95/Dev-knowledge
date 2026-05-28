# Solutions: Module 04 - HTML/CSS/JS BASICS

> **Đáp Án Frontend Exercises**

---

## PHẦN A: TRẮC NGHIỆM

1. **A** - h1 là heading lớn nhất
2. **B** - .classname cho CSS class selector
3. **C** - const declare constant
4. **A** - link rel="stylesheet" để link CSS
5. **B** - addEventListener syntax đúng
6. **C** - getElementById select by ID
7. **A** - margin: 0 auto center block element
8. **B** - () => {} là arrow function
9. **C** - response.json() parse JSON
10. **B** - console.log() để debug

---

## PHẦN B: CODE SOLUTIONS

**Câu 11: HTML Semantic Structure**

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Page</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <a href="/">Home</a>
            <a href="/about">About</a>
        </nav>
    </header>
    <main>
        <article>
            <h1>Main Content</h1>
            <p>Paragraph here.</p>
        </article>
    </main>
    <footer>
        <p>&copy; 2025</p>
    </footer>
    <script src="app.js"></script>
</body>
</html>
```

**Câu 12: CSS Flexbox Layout**

```css
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    gap: 1rem;
}

.card {
    flex: 1;
    max-width: 300px;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
```

**Câu 13: JavaScript Event Handler**

```javascript
const button = document.getElementById('submitBtn');

button.addEventListener('click', (event) => {
    event.preventDefault();
    const input = document.getElementById('nameInput').value;
    console.log(`Hello, ${input}!`);
    alert(`Welcome, ${input}!`);
});
```

**Câu 14: Fetch API**

```javascript
async function fetchData() {
    try {
        const response = await fetch('/api/tasks');
        if (!response.ok) throw new Error('Network error');
        const data = await response.json();
        console.log(data);
        displayTasks(data);
    } catch (error) {
        console.error('Error:', error);
    }
}

fetchData();
```

---

## PHẦN C: THỰC HÀNH

**Câu 15: DevTools Debug**

- F12 mở DevTools
- Console tab xem errors
- Network tab check requests
- Elements tab inspect DOM

**Câu 16: Deploy Static Site**

```nginx
server {
    listen 80;
    server_name mysite.com;
    root /var/www/mysite;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

**Câu 17: Asset Optimization**

- Minify CSS/JS
- Compress images
- Enable gzip
- Cache headers

---

## KEY CONCEPTS

**HTML:**

- Semantic elements: header, main, footer, nav, article, section
- Forms: input, button, label
- Meta tags for SEO

**CSS:**

- Box model: margin, padding, border
- Flexbox: display: flex, justify-content, align-items
- Grid: display: grid, grid-template-columns

**JavaScript:**

- DOM: getElementById, querySelector
- Events: addEventListener
- Fetch: async/await, .json()

---

**Frontend knowledge = Better DevOps! 🎨**
