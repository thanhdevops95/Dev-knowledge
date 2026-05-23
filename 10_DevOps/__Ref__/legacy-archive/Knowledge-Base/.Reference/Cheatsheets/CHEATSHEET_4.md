# HTML/CSS/JS Basics - Cheatsheet

> **Quick reference cho frontend essentials**

---

## 📄 HTML BASICS

### Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Content here -->
    <script src="app.js"></script>
</body>
</html>
```

### Common Tags

```html
<!-- Headings -->
<h1>Heading 1</h1>
<h2>Heading 2</h2>
<h3>Heading 3</h3>

<!-- Text -->
<p>Paragraph</p>
<strong>Bold</strong>
<em>Italic</em>
<br>              <!-- Line break -->
<hr>              <!-- Horizontal rule -->

<!-- Links & Images -->
<a href="url">Link text</a>
<img src="image.jpg" alt="Description">

<!-- Lists -->
<ul>              <!-- Unordered -->
  <li>Item</li>
</ul>

<ol>              <!-- Ordered -->
  <li>First</li>
</ol>

<!-- Containers -->
<div>Block container</div>
<span>Inline container</span>

<!-- Forms -->
<form action="/submit" method="POST">
  <input type="text" name="username" placeholder="Username">
  <input type="password" name="password">
  <input type="email" name="email">
  <textarea name="message"></textarea>
  <button type="submit">Submit</button>
</form>

<!-- Semantic HTML -->
<header>Page header</header>
<nav>Navigation</nav>
<main>Main content</main>
<article>Article</article>
<section>Section</section>
<footer>Page footer</footer>
```

### File Paths

```html
<!-- Relative (same directory) -->
<img src="logo.png">
<link href="style.css">

<!-- Relative (subdirectory) -->
<img src="images/logo.png">
<script src="js/app.js"></script>

<!-- Relative (parent) -->
<img src="../logo.png">

<!-- Absolute (from root) -->
<img src="/images/logo.png">

<!-- External URL -->
<img src="https://example.com/logo.png">
```

---

## 🎨 CSS BASICS

### Adding CSS

```html
<!-- External (best practice) -->
<link rel="stylesheet" href="style.css">

<!-- Internal -->
<style>
  p { color: blue; }
</style>

<!-- Inline -->
<p style="color: red;">Text</p>
```

### Selectors

```css
/* Element */
p { color: blue; }

/* Class */
.highlight { background: yellow; }

/* ID */
#header { font-size: 24px; }

/* Multiple */
h1, h2, h3 { font-family: Arial; }

/* Descendant */
div p { color: red; }

/* Child */
div > p { color: blue; }

/* Pseudo-classes */
a:hover { color: red; }
input:focus { border: 2px solid blue; }
```

### Common Properties

```css
/* Text */
color: #333;
font-size: 16px;
font-weight: bold;
font-family: Arial, sans-serif;
text-align: center;
line-height: 1.5;

/* Box Model */
width: 300px;
height: 200px;
padding: 20px;           /* Inside */
margin: 10px;            /* Outside */
border: 1px solid black;

/* Background */
background-color: #f0f0f0;
background-image: url('bg.jpg');
background-size: cover;

/* Display */
display: block;          /* Full width */
display: inline;         /* Inline */
display: inline-block;   /* Inline but can have width/height */
display: none;           /* Hidden */
display: flex;           /* Flexbox */

/* Positioning */
position: static;        /* Default */
position: relative;      /* Relative to normal position */
position: absolute;      /* Relative to parent */
position: fixed;         /* Relative to viewport */

/* Flexbox */
display: flex;
justify-content: center; /* Horizontal */
align-items: center;     /* Vertical */
flex-direction: row;     /* or column */
```

### Layout Examples

```css
/* Center a div */
.center {
  width: 300px;
  margin: 0 auto;
}

/* Flexbox centering */
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    width: 100%;
  }
}
```

---

## 💻 JAVASCRIPT BASICS

### Variables

```javascript
// Modern (use these)
let name = "John";       // Can change
const age = 25;          // Cannot change

// String interpolation
const greeting = `Hello, ${name}!`;
```

### Data Types

```javascript
// Primitives
let str = "text";        // String
let num = 42;            // Number
let bool = true;         // Boolean
let nothing = null;      // Null
let undef = undefined;   // Undefined

// Objects
let obj = { key: "value" };
let arr = [1, 2, 3];
```

### Functions

```javascript
// Function declaration
function greet(name) {
  return `Hello, ${name}`;
}

// Arrow function
const greet = (name) => {
  return `Hello, ${name}`;
};

// Short arrow
const greet = name => `Hello, ${name}`;

// Usage
greet("DevOps");  // "Hello, DevOps"
```

### Conditionals

```javascript
// If/else
if (age >= 18) {
  console.log("Adult");
} else {
  console.log("Minor");
}

// Ternary
const status = age >= 18 ? "Adult" : "Minor";

// Switch
switch (role) {
  case "admin":
    console.log("Admin access");
    break;
  case "user":
    console.log("User access");
    break;
  default:
    console.log("No access");
}
```

### Loops

```javascript
// For loop
for (let i = 0; i < 5; i++) {
  console.log(i);
}

// For...of (arrays)
for (const item of items) {
  console.log(item);
}

// forEach
items.forEach(item => {
  console.log(item);
});

// While
while (condition) {
  // code
}
```

### Arrays

```javascript
const arr = [1, 2, 3, 4, 5];

// Access
arr[0];              // 1

// Methods
arr.push(6);         // Add to end
arr.pop();           // Remove from end
arr.length;          // 5
arr.includes(3);     // true

// Higher order functions
arr.map(x => x * 2);           // [2, 4, 6, 8, 10]
arr.filter(x => x > 2);        // [3, 4, 5]
arr.find(x => x > 2);          // 3
arr.reduce((sum, x) => sum + x, 0);  // 15
```

### Objects

```javascript
const user = {
  name: "John",
  age: 25,
  greet() {
    return `Hello, ${this.name}`;
  }
};

// Access
user.name;           // "John"
user['age'];         // 25
user.greet();        // "Hello, John"

// Destructuring
const { name, age } = user;
```

---

## 🌐 DOM MANIPULATION

### Selecting Elements

```javascript
// By ID
document.getElementById('myId');

// By class (returns array-like)
document.getElementsByClassName('myClass');

// By tag
document.getElementsByTagName('div');

// CSS selector (modern, best)
document.querySelector('.myClass');        // First match
document.querySelectorAll('.myClass');     // All matches
```

### Changing Content

```javascript
// Text content
element.textContent = 'New text';

// HTML content
element.innerHTML = '<strong>Bold</strong>';

// Attributes
element.getAttribute('href');
element.setAttribute('href', 'newurl.html');
element.removeAttribute('disabled');

// Classes
element.classList.add('active');
element.classList.remove('hidden');
element.classList.toggle('visible');
element.classList.contains('active');    // true/false

// Styles
element.style.color = 'red';
element.style.backgroundColor = 'blue';
```

### Creating & Adding Elements

```javascript
// Create
const div = document.createElement('div');
div.textContent = 'Hello';
div.className = 'box';

// Add to DOM
parent.appendChild(div);           // At end
parent.insertBefore(div, child);   // Before child
parent.removeChild(child);         // Remove
```

### Events

```javascript
// Click
button.addEventListener('click', () => {
  console.log('Clicked!');
});

// Form submit
form.addEventListener('submit', (e) => {
  e.preventDefault();  // Prevent page reload
  console.log('Submitted');
});

// Input change
input.addEventListener('input', (e) => {
  console.log(e.target.value);
});

// Mouse events
element.addEventListener('mouseenter', () => {});
element.addEventListener('mouseleave', () => {});

// Keyboard
document.addEventListener('keydown', (e) => {
  console.log(e.key);
});
```

---

## 🌍 FETCH API

### GET Request

```javascript
fetch('https://api.example.com/data')
  .then(response => response.json())
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error('Error:', error);
  });

// Async/await (modern)
async function getData() {
  try {
    const response = await fetch('https://api.example.com/data');
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error('Error:', error);
  }
}
```

### POST Request

```javascript
fetch('https://api.example.com/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'John',
    email: 'john@example.com'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### With Headers

```javascript
fetch('https://api.example.com/data', {
  headers: {
    'Authorization': 'Bearer TOKEN',
    'Content-Type': 'application/json'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

---

## 🛠️ DEBUGGING

### Console Methods

```javascript
console.log('Message');              // General
console.error('Error message');      // Red error
console.warn('Warning');             // Yellow warning
console.table([{a: 1}, {a: 2}]);    // Table format
console.time('label');               // Start timer
console.timeEnd('label');            // End timer
```

### Error Handling

```javascript
try {
  // Risky code
  JSON.parse(badData);
} catch (error) {
  console.error('Error:', error.message);
} finally {
  // Always runs
  console.log('Cleanup');
}
```

### Chrome DevTools

```
F12 or Ctrl+Shift+I     Open DevTools
Ctrl+Shift+C            Inspect element
Ctrl+Shift+J            Console
Ctrl+Shift+Delete       Clear cache
```

**DevTools Tabs:**

- **Elements:** Inspect HTML/CSS
- **Console:** JavaScript output & errors
- **Network:** HTTP requests
- **Application:** Storage, cookies, cache

---

## 🚨 COMMON ISSUES (DevOps)

### Files Not Loading

```javascript
// Check paths
<script src="app.js"></script>     // Same folder
<script src="/js/app.js"></script> // From root
<script src="js/app.js"></script>  // Subfolder

// Check console for 404 errors
// F12 → Console → Look for red errors
```

### CORS Errors

```
Error: CORS policy blocked

Solution (backend):
res.setHeader('Access-Control-Allow-Origin', '*');

Or use proxy in dev:
// package.json
"proxy": "http://localhost:5000"
```

### JavaScript Not Running

```javascript
// Ensure script loads after DOM
<body>
  <!-- HTML content -->
  <script src="app.js"></script>  <!-- At end of body -->
</body>

// Or use DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  // Code runs after DOM loads
});
```

### Cache Issues

```
Browser caches CSS/JS!

Solutions:
1. Hard refresh: Ctrl+Shift+R
2. Version query: style.css?v=2
3. Disable cache in DevTools (Network tab)
```

---

## 📦 DEPLOYMENT CHECKLIST

```bash
# File structure
index.html
style.css
app.js
images/
  logo.png
  bg.jpg

# Server deployment
sudo cp -r myapp/ /var/www/html/
sudo chown -R www-data:www-data /var/www/html/myapp
sudo chmod -R 755 /var/www/html/myapp

# File permissions
chmod 644 *.html *.css *.js    # Files
chmod 755 images/              # Directories

# Test locally first
python3 -m http.server 8000
# Visit: http://localhost:8000
```

---

<div align="center">

**Frontend basics mastered! 🎨💻**

**Deploy with confidence! 🚀**

</div>
