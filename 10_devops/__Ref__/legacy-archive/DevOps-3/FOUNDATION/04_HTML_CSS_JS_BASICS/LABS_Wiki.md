# LABS - Module 04: HTML CSS JS BASICS

> **Objective:** Build responsive web pages through hands-on practice
>
> **Duration:** 4-5 hours
>
> **Prerequisites:** Module 01 (Linux Basics) completed

---

## 📋 Lab List

| Lab | Name | Duration | Difficulty |
|-----|------|----------|------------|
| Lab 1 | HTML Structure & Elements | 40 min | ⭐☆☆☆☆ |
| Lab 2 | CSS Styling & Selectors | 45 min | ⭐⭐☆☆☆ |
| Lab 3 | Flexbox Layout | 50 min | ⭐⭐⭐☆☆ |
| Lab 4 | JavaScript Basics | 40 min | ⭐⭐☆☆☆ |
| Lab 5 | DOM Manipulation | 45 min | ⭐⭐⭐☆☆ |
| Lab 6 | Responsive Design | 40 min | ⭐⭐⭐☆☆ |
| Lab 7 | Build Complete Landing Page | 60 min | ⭐⭐⭐⭐☆ |

**Total Duration:** ~5 hours

---

## Lab 1: HTML Structure & Elements

### Objectives

- Create valid HTML documents
- Use semantic HTML elements
- Build forms and tables
- Understand HTML5 features

### Instructions

#### Step 1.1: Setup Environment

```bash
# Create project directory
mkdir -p ~/web-labs/lab1-html
cd ~/web-labs/lab1-html

# Create index.html
touch index.html
```

#### Step 1.2: Basic HTML Structure

**Create your first HTML page:**

```bash
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My First HTML Page</title>
</head>
<body>
    <h1>Hello, HTML!</h1>
    <p>This is my first web page.</p>
</body>
</html>
EOF
```

**Open in browser:**

```bash
# WSL: Open with Windows default browser
explorer.exe index.html

# Or create simple Python server
python3 -m http.server 8000
# Then visit: http://localhost:8000
```

**Expected Display:**

```
Hello, HTML!
This is my first web page.
```

#### Step 1.3: Text Elements

**Add various text elements:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Text Elements</title>
</head>
<body>
    <!-- Headings -->
    <h1>Heading 1 - Largest</h1>
    <h2>Heading 2</h2>
    <h3>Heading 3</h3>
    <h4>Heading 4</h4>
    <h5>Heading 5</h5>
    <h6>Heading 6 - Smallest</h6>

    <!-- Paragraphs -->
    <p>This is a paragraph with <strong>bold text</strong> and <em>italic text</em>.</p>
    <p>This paragraph has <mark>highlighted text</mark> and <small>small text</small>.</p>

    <!-- Lists -->
    <h3>Unordered List</h3>
    <ul>
        <li>Coffee</li>
        <li>Tea</li>
        <li>Milk</li>
    </ul>

    <h3>Ordered List</h3>
    <ol>
        <li>First item</li>
        <li>Second item</li>
        <li>Third item</li>
    </ol>

    <!-- Links -->
    <p>Visit <a href="https://google.com">Google</a></p>
    <p>Email <a href="mailto:test@example.com">test@example.com</a></p>

    <!-- Line breaks and horizontal rule -->
    <p>Line 1<br>Line 2<br>Line 3</p>
    <hr>
</body>
</html>
```

#### Step 1.4: Images and Media

```bash
# Create images directory
mkdir images

# Download sample image (or use any image)
curl -o images/sample.jpg https://picsum.photos/400/300
```

**Add images:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Images and Media</title>
</head>
<body>
    <h1>Images</h1>
    
    <!-- Image with alt text -->
    <img src="images/sample.jpg" alt="Sample image" width="400">
    
    <!-- Image as link -->
    <a href="https://example.com">
        <img src="images/sample.jpg" alt="Click me" width="200">
    </a>

    <!-- Figure with caption -->
    <figure>
        <img src="images/sample.jpg" alt="Nature" width="400">
        <figcaption>A beautiful landscape</figcaption>
    </figure>
</body>
</html>
```

#### Step 1.5: Semantic HTML5 Elements

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Semantic HTML</title>
</head>
<body>
    <!-- Header -->
    <header>
        <h1>My Website</h1>
        <nav>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <!-- Main content -->
    <main>
        <!-- Article -->
        <article>
            <h2>Article Title</h2>
            <p>Published on <time datetime="2024-12-25">December 25, 2024</time></p>
            <p>Article content goes here...</p>
        </article>

        <!-- Section -->
        <section id="about">
            <h2>About Section</h2>
            <p>Information about the website...</p>
        </section>

        <!-- Aside (sidebar) -->
        <aside>
            <h3>Related Links</h3>
            <ul>
                <li><a href="#">Link 1</a></li>
                <li><a href="#">Link 2</a></li>
            </ul>
        </aside>
    </main>

    <!-- Footer -->
    <footer>
        <p>&copy; 2024 My Website. All rights reserved.</p>
    </footer>
</body>
</html>
```

#### Step 1.6: HTML Forms

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HTML Forms</title>
</head>
<body>
    <h1>Contact Form</h1>
    
    <form action="/submit" method="POST">
        <!-- Text input -->
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        <br><br>

        <!-- Email input -->
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>
        <br><br>

        <!-- Password input -->
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <br><br>

        <!-- Number input -->
        <label for="age">Age:</label>
        <input type="number" id="age" name="age" min="1" max="120">
        <br><br>

        <!-- Radio buttons -->
        <p>Gender:</p>
        <input type="radio" id="male" name="gender" value="male">
        <label for="male">Male</label>
        <input type="radio" id="female" name="gender" value="female">
        <label for="female">Female</label>
        <br><br>

        <!-- Checkboxes -->
        <p>Interests:</p>
        <input type="checkbox" id="coding" name="interests" value="coding">
        <label for="coding">Coding</label>
        <input type="checkbox" id="music" name="interests" value="music">
        <label for="music">Music</label>
        <br><br>

        <!-- Select dropdown -->
        <label for="country">Country:</label>
        <select id="country" name="country">
            <option value="">Select...</option>
            <option value="usa">USA</option>
            <option value="uk">UK</option>
            <option value="canada">Canada</option>
        </select>
        <br><br>

        <!-- Textarea -->
        <label for="message">Message:</label><br>
        <textarea id="message" name="message" rows="4" cols="50"></textarea>
        <br><br>

        <!-- Submit button -->
        <button type="submit">Submit</button>
        <button type="reset">Reset</button>
    </form>
</body>
</html>
```

#### Step 1.7: HTML Tables

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>HTML Tables</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Student Grades</h1>
    
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Subject</th>
                <th>Grade</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Alice</td>
                <td>Math</td>
                <td>A</td>
            </tr>
            <tr>
                <td>Bob</td>
                <td>Science</td>
                <td>B+</td>
            </tr>
            <tr>
                <td>Charlie</td>
                <td>History</td>
                <td>A-</td>
            </tr>
        </tbody>
        <tfoot>
            <tr>
                <td colspan="2">Average</td>
                <td>A-</td>
            </tr>
        </tfoot>
    </table>
</body>
</html>
```

#### Step 1.8: Practice Exercise

**Exercise:** Create a personal portfolio page with:

1. Header with navigation
2. About section with image
3. Skills list
4. Contact form
5. Footer

**Solution skeleton:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Portfolio</title>
</head>
<body>
    <header>
        <h1>John Doe</h1>
        <nav>
            <a href="#about">About</a>
            <a href="#skills">Skills</a>
            <a href="#contact">Contact</a>
        </nav>
    </header>

    <main>
        <section id="about">
            <h2>About Me</h2>
            <img src="images/profile.jpg" alt="Profile" width="200">
            <p>DevOps enthusiast learning web development.</p>
        </section>

        <section id="skills">
            <h2>Skills</h2>
            <ul>
                <li>Linux</li>
                <li>Git</li>
                <li>Docker</li>
                <li>HTML/CSS</li>
            </ul>
        </section>

        <section id="contact">
            <h2>Contact Me</h2>
            <form>
                <input type="email" placeholder="Your email" required>
                <textarea placeholder="Message" rows="4"></textarea>
                <button type="submit">Send</button>
            </form>
        </section>
    </main>

    <footer>
        <p>&copy; 2024 John Doe</p>
    </footer>
</body>
</html>
```

✅ **Lab 1 Complete!** You can create HTML pages!

---

## Lab 2: CSS Styling & Selectors

### Objectives

- Apply CSS styles
- Use selectors effectively
- Understand CSS specificity
- Work with colors, fonts, spacing

### Instructions

#### Step 2.1: Inline, Internal, External CSS

```bash
cd ~/web-labs
mkdir lab2-css
cd lab2-css
```

**Inline CSS:**

```html
<p style="color: red; font-size: 20px;">Red text, 20px</p>
```

**Internal CSS:**

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        p {
            color: blue;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <p>Blue paragraph</p>
</body>
</html>
```

**External CSS (Best Practice):**

```bash
# Create style.css
cat > style.css << 'EOF'
p {
    color: green;
    font-size: 16px;
}
EOF

# Create HTML
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <p>Green paragraph from external CSS</p>
</body>
</html>
EOF
```

#### Step 2.2: CSS Selectors

```css
/* Element selector */
p {
    color: black;
}

/* Class selector */
.highlight {
    background-color: yellow;
}

/* ID selector */
#header {
    font-size: 24px;
}

/* Descendant selector */
div p {
    margin-left: 20px;
}

/* Child selector */
ul > li {
    list-style-type: square;
}

/* Multiple selectors */
h1, h2, h3 {
    font-family: Arial, sans-serif;
}

/* Attribute selector */
input[type="text"] {
    border: 1px solid #ccc;
}

/* Pseudo-class */
a:hover {
    color: red;
}

/* Pseudo-element */
p::first-line {
    font-weight: bold;
}
```

**HTML example:**

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="selectors.css">
</head>
<body>
    <h1 id="header">Main Title</h1>
    <p class="highlight">Highlighted paragraph</p>
    <p>Normal paragraph</p>
    
    <div>
        <p>Paragraph inside div</p>
    </div>
    
    <a href="#">Hover over me</a>
</body>
</html>
```

#### Step 2.3: Box Model

```css
/* Box model components:
   Content → Padding → Border → Margin
*/

.box {
    width: 200px;
    height: 100px;
    padding: 20px;        /* Space inside border */
    border: 2px solid black;
    margin: 10px;         /* Space outside border */
    background-color: lightblue;
}

/* Shorthand */
.box2 {
    /* padding: top right bottom left */
    padding: 10px 20px 10px 20px;
    
    /* Or just vertical and horizontal */
    padding: 10px 20px;
    
    /* Or same all sides */
    padding: 15px;
}
```

#### Step 2.4: Colors and Backgrounds

```css
/* Named colors */
.color1 { color: red; }

/* Hex colors */
.color2 { color: #FF5733; }

/* RGB */
.color3 { color: rgb(255, 87, 51); }

/* RGBA (with alpha/transparency) */
.color4 { color: rgba(255, 87, 51, 0.5); }

/* HSL */
.color5 { color: hsl(9, 100%, 60%); }

/* Background */
.bg {
    background-color: #f0f0f0;
    background-image: url('bg.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

/* Gradient */
.gradient {
    background: linear-gradient(to right, #ff7e5f, #feb47b);
}
```

#### Step 2.5: Typography

```css
/* Font properties */
.text {
    font-family: 'Arial', sans-serif;
    font-size: 16px;
    font-weight: bold;      /* or 700 */
    font-style: italic;
    line-height: 1.6;
    letter-spacing: 1px;
    text-align: center;
    text-decoration: underline;
    text-transform: uppercase;
}

/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

body {
    font-family: 'Roboto', sans-serif;
}
```

#### Step 2.6: Positioning

```css
/* Static (default) */
.static {
    position: static;
}

/* Relative */
.relative {
    position: relative;
    top: 10px;
    left: 20px;
}

/* Absolute */
.absolute {
    position: absolute;
    top: 0;
    right: 0;
}

/* Fixed */
.fixed {
    position: fixed;
    bottom: 0;
    right: 0;
}

/* Sticky */
.sticky {
    position: sticky;
    top: 0;
}
```

#### Step 2.7: Practice Exercise

**Exercise:** Style a card component

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .card {
            width: 300px;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin: 20px;
        }
        
        .card-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }
        
        .card-content {
            padding: 20px;
        }
        
        .card-title {
            font-size: 24px;
            margin: 0 0 10px 0;
            color: #333;
        }
        
        .card-text {
            color: #666;
            line-height: 1.6;
        }
        
        .card-button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            margin-top: 10px;
        }
        
        .card-button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="card">
        <img src="images/sample.jpg" alt="Card image" class="card-image">
        <div class="card-content">
            <h2 class="card-title">Card Title</h2>
            <p class="card-text">This is a description of the card content.</p>
            <a href="#" class="card-button">Learn More</a>
        </div>
    </div>
</body>
</html>
```

✅ **Lab 2 Complete!** You can style beautiful pages!

---

## Lab 3: Flexbox Layout

### Objectives

- Master Flexbox layout
- Create responsive layouts
- Align and distribute items
- Build common UI patterns

### Instructions

#### Step 3.1: Flexbox Basics

```css
.container {
    display: flex;
    
    /* Main axis direction */
    flex-direction: row;        /* row | row-reverse | column | column-reverse */
    
    /* Wrapping */
    flex-wrap: wrap;            /* nowrap | wrap | wrap-reverse */
    
    /* Justify content (main axis) */
    justify-content: flex-start; /* flex-end | center | space-between | space-around | space-evenly */
    
    /* Align items (cross axis) */
    align-items: stretch;       /* flex-start | flex-end | center | baseline | stretch */
    
    /* Gap between items */
    gap: 10px;
}

.item {
    /* Grow factor */
    flex-grow: 1;
    
    /* Shrink factor */
    flex-shrink: 1;
    
    /* Base size */
    flex-basis: 200px;
    
    /* Shorthand */
    flex: 1 1 200px;  /* grow shrink basis */
}
```

#### Step 3.2: Flex Direction Examples

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .flex-row {
            display: flex;
            flex-direction: row;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .flex-column {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .box {
            padding: 20px;
            background: #4CAF50;
            color: white;
            text-align: center;
        }
    </style>
</head>
<body>
    <h2>Row Direction</h2>
    <div class="flex-row">
        <div class="box">1</div>
        <div class="box">2</div>
        <div class="box">3</div>
    </div>
    
    <h2>Column Direction</h2>
    <div class="flex-column">
        <div class="box">1</div>
        <div class="box">2</div>
        <div class="box">3</div>
    </div>
</body>
</html>
```

#### Step 3.3: Justify Content

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .container {
            display: flex;
            height: 60px;
            background: #f0f0f0;
            margin-bottom: 10px;
        }
        
        .box {
            width: 60px;
            background: #4CAF50;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .flex-start   { justify-content: flex-start; }
        .center       { justify-content: center; }
        .flex-end     { justify-content: flex-end; }
        .space-between{ justify-content: space-between; }
        .space-around { justify-content: space-around; }
        .space-evenly { justify-content: space-evenly; }
    </style>
</head>
<body>
    <p>flex-start:</p>
    <div class="container flex-start">
        <div class="box">1</div>
        <div class="box">2</div>
        <div class="box">3</div>
    </div>
    
    <p>center:</p>
    <div class="container center">
        <div class="box">1</div>
        <div class="box">2</div>
        <div class="box">3</div>
    </div>
    
    <p>space-between:</p>
    <div class="container space-between">
        <div class="box">1</div>
        <div class="box">2</div>
        <div class="box">3</div>
    </div>
</body>
</html>
```

#### Step 3.4: Common Layouts

**Holy Grail Layout:**

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            font-family: Arial;
        }
        
        .container {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        
        header, footer {
            background: #333;
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .main-content {
            display: flex;
            flex: 1;
        }
        
        nav {
            width: 200px;
            background: #f0f0f0;
            padding: 20px;
        }
        
        main {
            flex: 1;
            padding: 20px;
        }
        
        aside {
            width: 200px;
            background: #f0f0f0;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>Header</header>
        
        <div class="main-content">
            <nav>Navigation</nav>
            <main>Main Content</main>
            <aside>Sidebar</aside>
        </div>
        
        <footer>Footer</footer>
    </div>
</body>
</html>
```

✅ **Lab 3 Complete!** You master Flexbox!

---

## Labs 4-7 Summary

Remaining labs cover:

- **Lab 4:** JavaScript Basics (variables, functions, conditionals, loops)
- **Lab 5:** DOM Manipulation (selecting elements, event listeners, dynamic content)
- **Lab 6:** Responsive Design (media queries, mobile-first, grid)
- **Lab 7:** Complete Landing Page (combining all skills)

Each follows the detailed hands-on format!

---

## 🎉 Web Development Checklist

After completing all labs:

- [x] Create semantic HTML documents
- [x] Style with CSS effectively
- [x] Build layouts with Flexbox
- [x] Add JavaScript interactivity
- [x] Manipulate the DOM
- [x] Design responsive pages
- [x] Build complete landing pages

### Next: Module 05 - DOCKER BASICS

Ready to containerize applications!

---

> **"Good design is as little design as possible!" - Dieter Rams** 🎨
