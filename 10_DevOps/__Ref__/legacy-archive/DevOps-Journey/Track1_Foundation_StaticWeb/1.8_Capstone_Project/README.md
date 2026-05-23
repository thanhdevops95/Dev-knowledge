# 🏆 Module 1.8: Capstone Project

> **Static Website with Full CI/CD Pipeline** - Integrate all Track 1 knowledge.
>
> *Website tĩnh với Full CI/CD Pipeline - Tích hợp toàn bộ kiến thức Track 1.*

---

## 🔀 Platform Options (Lựa chọn nền tảng)

| Platform (Nền tảng) | Status (Trạng thái) | Notes (Ghi chú) |
|----------|--------|-------|
| **GitLab CI/CD** | ⭐ Primary (Chính) | This guide uses GitLab (Hướng dẫn này sử dụng GitLab) |
| GitHub Actions | Alternative (Thay thế) | See [1.7 CI/CD GitHub guide](../1.7_CICD_Basic/README_GITHUB_ACTIONS.md) (Xem hướng dẫn GitHub Actions 1.7) |

---

## 🎯 Project Overview (Tổng quan dự án)

Build a **static portfolio website** with (Xây dựng portfolio website tĩnh với):

- ✅ Source code managed with Git (Quản lý bằng Git)
- ✅ Static website with HTML/CSS/JS (Website tĩnh với HTML/CSS/JS)
- ✅ Containerized with Docker + NGINX (Container hóa với Docker + NGINX)
- ✅ CI/CD pipeline with **GitLab CI/CD** (Pipeline với GitLab CI/CD)
- ✅ Auto deploy when pushing code (Tự động deploy khi push code)

---

## 📐 Project Requirements (Yêu cầu dự án)

### 1. Functional Requirements (Yêu cầu chức năng)

| # | Requirement (Yêu cầu) | Description (Mô tả) |
|---|-------------|-------------|
| FR-01 | Homepage | Introduction page (Trang giới thiệu) |
| FR-02 | About page | Skills & experience details (Chi tiết kỹ năng & kinh nghiệm) |
| FR-03 | Projects page | Showcase projects (Trưng bày dự án) |
| FR-04 | Contact form | Contact form - UI only (Form liên hệ - chỉ UI) |
| FR-05 | Responsive | Display well on mobile/tablet/desktop (Hiển thị tốt trên di động/tablet/desktop) |

### 2. Technical Requirements (Yêu cầu kỹ thuật)

| # | Requirement (Yêu cầu) | Description (Mô tả) |
|---|-------------|-------------|
| TR-01 | Git | Manage code with Git, .gitignore (Quản lý code với Git) |
| TR-02 | Docker | Dockerfile to build image (File Docker để build image) |
| TR-03 | NGINX | Serve static files with NGINX (Cung cấp file tĩnh với NGINX) |
| TR-04 | CI | **GitLab CI** pipeline for lint/build (Pipeline với GitLab CI/CD cho lint/build) |
| TR-05 | CD | Auto deploy on push to main branch (Tự động deploy khi push code lên main branch) |
| TR-06 | Registry | Push image to **GitLab Container Registry** (Push image lên **GitLab Container Registry**)|

---

## 📁 Project Structure (Cấu trúc dự án)

```
devops-portfolio/
│
├── .gitlab-ci.yml                  # GitLab CI/CD pipeline (File CI/CD chính)
│
├── src/                            # Source code (Mã nguồn)
│   ├── index.html
│   ├── about.html
│   ├── projects.html
│   ├── contact.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── profile.jpg
│
├── nginx/
│   └── nginx.conf                  # NGINX configuration (Cấu hình NGINX)
│
├── Dockerfile                      # Docker build file (File Docker để build image)
├── .dockerignore                   # Docker ignore (Docker ignore)
├── .gitignore                      # Git ignore (Git ignore)
├── README.md                       # Project documentation (Giới thiệu dự án)
└── LICENSE                         # License file (File license)
```

---

## 📝 Step-by-Step Guide

### Step 1: Create Project (Tạo dự án) 📂

```bash
# 1. Create project directory (Tạo thư mục dự án)
mkdir devops-portfolio
cd devops-portfolio

# 2. Initialize Git (Khởi tạo Git)
git init

# 3. Create directory structure (Tạo cấu trúc thư mục)
mkdir -p src/{css,js,images}
mkdir -p nginx

# 4. Create .gitignore (Tạo .gitignore)
cat > .gitignore << 'EOF'
# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Node modules (nếu dùng build tools)
node_modules/

# Logs
*.log

# Environment files
.env
.env.local
EOF
```

---

### Step 2: Create Website (Tạo website) 🌐

#### index.html

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Portfolio</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <nav>
            <div class="logo">🚀 DevOps Journey</div>
            <ul class="nav-links">
                <li><a href="index.html" class="active">Home</a></li>
                <li><a href="about.html">About</a></li>
                <li><a href="projects.html">Projects</a></li>
                <li><a href="contact.html">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section class="hero">
            <h1>Hi, I'm a DevOps Engineer 👋</h1>
            <p>Building reliable, scalable infrastructure</p>
            <a href="projects.html" class="btn">View My Projects</a>
        </section>

        <section class="skills">
            <h2>Skills</h2>
            <div class="skill-cards">
                <div class="card">
                    <span class="icon">🐧</span>
                    <h3>Linux</h3>
                </div>
                <div class="card">
                    <span class="icon">🐳</span>
                    <h3>Docker</h3>
                </div>
                <div class="card">
                    <span class="icon">⚙️</span>
                    <h3>CI/CD</h3>
                </div>
                <div class="card">
                    <span class="icon">☸️</span>
                    <h3>Kubernetes</h3>
                </div>
            </div>
        </section>
    </main>

    <footer>
        <p>© 2025 DevOps Journey. Built with 💙</p>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>
```

#### css/style.css

```css
/* Reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

/* Header */
header {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 1rem 2rem;
    position: sticky;
    top: 0;
    z-index: 100;
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-links a {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    transition: background 0.3s;
}

.nav-links a:hover,
.nav-links a.active {
    background: rgba(255, 255, 255, 0.2);
}

/* Hero */
.hero {
    text-align: center;
    padding: 100px 20px;
    color: white;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.5rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.btn {
    display: inline-block;
    padding: 1rem 2rem;
    background: white;
    color: #667eea;
    text-decoration: none;
    border-radius: 50px;
    font-weight: bold;
    transition: transform 0.3s, box-shadow 0.3s;
}

.btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

/* Skills */
.skills {
    background: white;
    padding: 80px 20px;
    text-align: center;
}

.skills h2 {
    font-size: 2.5rem;
    margin-bottom: 3rem;
    color: #333;
}

.skill-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    max-width: 1000px;
    margin: 0 auto;
}

.card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    transition: transform 0.3s;
}

.card:hover {
    transform: translateY(-10px);
}

.card .icon {
    font-size: 3rem;
    display: block;
    margin-bottom: 1rem;
}

.card h3 {
    font-size: 1.3rem;
}

/* Footer */
footer {
    text-align: center;
    padding: 2rem;
    color: white;
    background: rgba(0, 0, 0, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
    .nav-links {
        display: none;
    }
    
    .hero h1 {
        font-size: 2rem;
    }
    
    .hero p {
        font-size: 1.2rem;
    }
}
```

#### js/main.js

```javascript
// Simple interactivity (Tương tác đơn giản)
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DevOps Portfolio loaded!');
    
    // Add animation on scroll (Thêm hiệu ứng khi cuộn)
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
});
```

---

### Step 3: Create Docker Configuration (Tạo Docker Configuration) 🐳

#### Dockerfile

```dockerfile
# Build stage (optional, for future use with build tools)
FROM nginx:alpine

# Labels
LABEL maintainer="yourname@example.com"
LABEL version="1.0"
LABEL description="DevOps Portfolio Website"

# Copy NGINX config
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy website files
COPY src/ /usr/share/nginx/html/

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]
```

#### nginx/nginx.conf

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/javascript application/javascript application/json;

    # Serve static files
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Custom error pages
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
}
```

#### .dockerignore

```
.git
.github
.gitignore
README.md
LICENSE
*.md
.DS_Store
Thumbs.db
```

---

### Step 4: Test Local (Kiểm tra cục bộ) 🧪

```bash
# Build Docker image
docker build -t devops-portfolio:dev .

# Run container
docker run -d -p 8080:80 --name portfolio devops-portfolio:dev

# Test
curl http://localhost:8080
# Mở browser: http://localhost:8080

# View logs
docker logs portfolio

# Stop and clean up
docker stop portfolio
docker rm portfolio
```

---

### Step 5: CI/CD Pipeline ⚙️

#### .gitlab-ci.yml

```yaml
# .gitlab-ci.yml - GitLab CI/CD Pipeline (Pipeline CI/CD GitLab)

stages:
  - lint
  - build
  - deploy

variables:
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

# Cache for faster builds (Cache để build nhanh hơn)
cache:
  paths:
    - node_modules/

# Job 1: Lint and Test (Kiểm tra và test)
lint:
  stage: lint
  image: alpine:latest
  script:
    - echo "Checking required files... (Kiểm tra files cần thiết...)"
    - test -f src/index.html && echo "✅ index.html exists"
    - test -f src/css/style.css && echo "✅ style.css exists"
    - test -f Dockerfile && echo "✅ Dockerfile exists"

# Job 2: Build Docker Image (Build Docker image)
build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE_TAG .
    - docker build -t $CI_REGISTRY_IMAGE:latest .
    - docker push $IMAGE_TAG
    - docker push $CI_REGISTRY_IMAGE:latest
  only:
    - main
    - develop

# Job 3: Deploy to Staging - auto (Triển khai staging - tự động)
deploy-staging:
  stage: deploy
  image: alpine:latest
  script:
    - echo "Deploying $IMAGE_TAG to staging..."
    # Add your deployment commands here (Thêm lệnh triển khai ở đây)
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

# Job 4: Deploy to Production - manual (Triển khai production - thủ công)
deploy-production:
  stage: deploy
  image: alpine:latest
  script:
    - echo "Deploying $IMAGE_TAG to production..."
    # Add your deployment commands here (Thêm lệnh triển khai ở đây)
  environment:
    name: production
    url: https://example.com
  when: manual  # Requires manual approval (Cần phê duyệt thủ công)
  only:
    - main
```

> 💡 **GitHub Users:** If using GitHub, see [GitHub Actions workflow example](../1.7_CICD_Basic/README_GITHUB_ACTIONS.md).
>
> *Nếu dùng GitHub, xem ví dụ GitHub Actions workflow.*

---

### Step 6: Push to GitLab (Push lên GitLab) 🚀

```bash
# Add remote (Thêm remote)
git remote add origin https://gitlab.com/YOUR_USERNAME/devops-portfolio.git

# Commit all (Commit tất cả)
git add .
git commit -m "Initial commit: DevOps Portfolio with CI/CD"

# Push
git push -u origin main
```

> 💡 **GitHub Users:** Replace `gitlab.com` with `github.com` if using GitHub.
>
> *Nếu dùng GitHub, thay `gitlab.com` bằng `github.com`.*

---

## ✅ Assessment Criteria (Tiêu chí đánh giá)

| # | Criteria (Tiêu chí) | Points (Điểm) | Description (Mô tả) |
|---|----------|--------|-------------|
| 1 | **Website** | 20% | HTML/CSS standards, responsive (Chuẩn HTML/CSS, thích ứng tốt) |
| 2 | **Git** | 10% | Clear commit messages, .gitignore (Thông điệp commit rõ ràng, có .gitignore) |
| 3 | **Dockerfile** | 20% | Builds successfully, optimized layers (Build thành công, tối ưu layers) |
| 4 | **NGINX** | 15% | Correct config, security headers (Cấu hình đúng, có headers bảo mật) |
| 5 | **CI/CD** | 25% | Pipeline runs successfully (Pipeline chạy thành công) |
| 6 | **README** | 10% | Complete documentation (Tài liệu đầy đủ) |

---

## 🎯 Bonus Challenges

After completing the basic requirements, try the following challenges (Sau khi hoàn thành yêu cầu cơ bản, thử các challenges sau):

### Challenge 1: Multi-stage Build (Xây dựng nhiều giai đoạn) ⭐

Add build step for CSS/JS minification (Thêm bước build để tối ưu hóa CSS/JS)

### Challenge 2: Custom Domain (Tên miền tùy chỉnh) ⭐⭐

Configure a custom domain for your GitHub Page (Cấu hình miền tùy chỉnh cho Trang GitHub)

### Challenge 3: SSL/HTTPS (Máy chủ SSL/HTTPS) ⭐⭐

Configure HTTPS with Let's Encrypt (Cấu hình HTTPS với Let's Encrypt)

### Challenge 4: Monitoring (Theo dõi) ⭐⭐⭐

Add uptime monitoring with UptimeRobot (Thêm tính năng giám sát thời gian hoạt động với UptimeRobot)

---

## 📚 Resources

- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [NGINX Documentation](https://nginx.org/en/docs/)

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [1.7 CI/CD](../1.7_CICD_Basic/) | **1.8 Capstone** | [Track 2](../../Track2_Orchestration_Automation/) |

---

**🎉 Congratulations! You completed Track 1!**

*Chúc mừng! Bạn đã hoàn thành Track 1!*

</div>
