# 🗺️ ROADMAP: FOUNDATION TRACK

> **Mục tiêu:** Từ Zero đến Junior DevOps Engineer
>
> **Thời gian:** Linh hoạt (tự học với AI hỗ trợ)
>
> **Kết quả:** Có khả năng deploy & monitor ứng dụng web đơn giản lên production

---

## 📊 TỔNG QUAN (OVERVIEW)

### Cấu trúc Track

**Foundation Track** bao gồm:

- ✅ **10 Modules cốt lõi** (00 → 09)
- ✅ **7 Integration Projects** (tích hợp kiến thức dần dần)
- ✅ **1 Final Project** (tổng hợp toàn bộ)

### Learning Path

```
00_SETUP → 01_LINUX → 02_GIT → 03_NETWORK → 04_HTML/CSS/JS
    ↓
05_DOCKER → 06_CI → 07_WEB_SERVERS → 08_DEPLOYMENT → 09_MONITORING
    ↓
INTEGRATION PROJECTS (01-07) → FINAL PROJECT
```

---

## 🎯 MODULE ROADMAP

### Module 00: SETUP - Chuẩn bị môi trường

**Mục tiêu:** Setup môi trường DevOps trên Windows/macOS/Linux

**Bạn sẽ học:**

- Tại sao DevOps cần Linux
- WSL2 là gì? Cách cài đặt
- VS Code, Terminal, Git basics
- Tạo tài khoản GitHub, Docker Hub

**Mini Project:** Environment Verification Script

**Thời lượng nội dung:** ~460 trang

---

### Module 01: LINUX_BASICS - Làm chủ dòng lệnh

**Mục tiêu:** Thành thạo Linux command line & file system

**Bạn sẽ học:**

- Lịch sử Unix/Linux
- File System Hierarchy (FHS)
- Navigation, File operations
- Permissions (chmod, chown)
- Process management

**Mini Project:** System Info Script

**Thời lượng nội dung:** ~570 trang

---

### Module 02: GIT_GITHUB - Version Control

**Mục tiêu:** Hiểu sâu Git internals & GitHub workflow

**Bạn sẽ học:**

- VCS: Centralized vs Distributed
- Git Internals: .git folder, objects, refs
- Branching, Merge vs Rebase
- Pull Request workflow

**Mini Project:** Learning Journal Repository

**Integration Project 01:** LEARNING_JOURNAL

- Tạo repo ghi chú học tập hàng ngày
- Practice: Daily commits, markdown

**Thời lượng nội dung:** ~520 trang

---

### Module 03: NETWORKING_INTRO - Mạng cơ bản

**Mục tiêu:** Hiểu cách máy tính communicate

**Bạn sẽ học:**

- OSI & TCP/IP models
- IP, Ports, DNS
- HTTP/HTTPS, SSH
- Basic troubleshooting

**Mini Project:** Network Diagnostic Tool

**Thời lượng nội dung:** ~490 trang

---

### Module 04: HTML_CSS_JS_BASICS - Frontend basics

**Mục tiêu:** Hiểu web app để test DevOps pipeline

**Bạn sẽ học:**

- HTML structure
- CSS styling (responsive)
- JavaScript basics (DOM manipulation)

**Mini Project:** Personal Landing Page

**Integration Project 02:** LANDING_PAGE

- Tạo landing page cá nhân
- HTML/CSS/JS thuần
- Responsive design

**Thời lượng nội dung:** ~470 trang

---

### Module 05: DOCKER_BASICS - Containerization

**Mục tiêu:** Đóng gói app vào containers

**Bạn sẽ học:**

- VM vs Container
- Docker Architecture
- Dockerfile, Images, Layers
- Docker Compose
- Multi-stage builds

**Mini Project:** Containerize Landing Page

**Integration Project 03:** DOCKERIZE_APP

- Containerize landing page từ Module 04
- Optimize image size < 50MB
- docker-compose cho local dev

**Thời lượng nội dung:** ~590 trang

---

### Module 06: CI_BASICS - Continuous Integration

**Mục tiêu:** Tự động build & test với GitHub Actions

**Bạn sẽ học:**

- CI/CD concepts
- GitHub Actions architecture
- YAML syntax
- Workflows: build, test, push

**Mini Project:** Auto-build Docker Image

**Integration Project 04:** CI_PIPELINE

- Setup GitHub Actions
- Auto-build on push
- Push image to Docker Hub

**Thời lượng nội dung:** ~460 trang

---

### Module 07: WEB_SERVERS_BASICS - NGINX

**Mục tiêu:** Serve app với NGINX

**Bạn sẽ học:**

- Web Server vs App Server
- NGINX architecture
- Configuration syntax
- Reverse Proxy
- HTTPS/SSL basics

**Mini Project:** NGINX Configuration

**Integration Project 05:** NGINX_DEPLOY

- Deploy app với NGINX
- Reverse proxy setup
- HTTPS configuration

**Thời lượng nội dung:** ~460 trang

---

### Module 08: DEPLOYMENT_BASICS - Deploy lên Internet

**Mục tiêu:** Deploy app lên production

**Bạn sẽ học:**

- Deployment strategies
- GitHub Pages
- Netlify
- VPS deployment với SSH

**Mini Project:** Deploy Portfolio to Netlify

**Integration Project 06:** PRODUCTION_DEPLOY

- Deploy landing page to Netlify/GitHub Pages
- Custom domain (optional)
- CI/CD auto-deployment

**Thời lượng nội dung:** ~460 trang

---

### Module 09: MONITORING_BASICS - Giám sát app

**Mục tiêu:** Monitor app sau khi deploy

**Bạn sẽ học:**

- Tại sao cần monitoring?
- Docker logs, tail -f
- Health check endpoints
- Basic metrics (CPU, Memory)
- Simple alerting

**Mini Project:** Health Check Dashboard

**Integration Project 07:** ADD_MONITORING

- Thêm /health endpoint
- Structured logging
- Basic uptime monitoring

**Thời lượng nội dung:** ~465 trang

---

### FINAL PROJECT: Portfolio Website Full Production

**Mục tiêu:** Tổng hợp TẤT CẢ kiến thức Foundation

**Yêu cầu:**

- ✅ Responsive Portfolio Website (HTML/CSS/JS)
- ✅ Dockerized với multi-stage build
- ✅ CI/CD với GitHub Actions
- ✅ Deployed to production (Netlify hoặc VPS)
- ✅ NGINX reverse proxy (nếu VPS)
- ✅ HTTPS enabled
- ✅ Health check endpoint
- ✅ Monitoring setup
- ✅ Full documentation

**Thời lượng:** ~100 trang hướng dẫn

---

## 📚 LEARNING RESOURCES

### Mỗi Module có

1. **README.md** - Lý thuyết chuyên sâu (WHY → HOW)
2. **LABS.md** - Hướng dẫn thực hành step-by-step
3. **EXERCISES.md** - Bài tập tự làm
4. **SOLUTIONS.md** - Đáp án chi tiết
5. **SCENARIOS.md** - Tình huống thực tế
6. **QUIZ.md** - Trắc nghiệm
7. **CHEATSHEET.md** - Tổng hợp lệnh
8. **MINI_PROJECT.md** - Project nhỏ áp dụng kiến thức

### Integration Projects

7 projects tích hợp, mỗi project có:

- README.md - Hướng dẫn
- REQUIREMENTS.md - Yêu cầu kỹ thuật
- STARTER_TEMPLATE/ - Code mẫu khởi đầu
- EXAMPLE/ - Bài giải tham khảo

---

## 🎓 LEARNING METHODOLOGY

### Progressive Learning

```
Module → Mini Project → (Integration Project) → Next Module
```

**Ví dụ:**

```
Module 04 (HTML/CSS/JS)
    → Mini Project: Simple Page
    → Integration 02: LANDING_PAGE
    → Module 05 (Docker)
    → Mini Project: Containerize Simple App
    → Integration 03: DOCKERIZE_APP (dùng lại Landing Page)
```

### WHY before HOW

Mỗi concept đều giải thích:

1. **WHY:** Tại sao cần? Vấn đề nó giải quyết?
2. **HOW:** Cách sử dụng, commands, best practices
3. **ALTERNATIVES:** So sánh với các giải pháp khác

---

## ✅ COMPLETION CHECKLIST

Sau khi hoàn thành Foundation Track, bạn có thể:

- [ ] Setup môi trường DevOps trên bất kỳ OS nào
- [ ] Thành thạo Linux command line
- [ ] Quản lý code với Git & GitHub
- [ ] Hiểu cơ bản về networking
- [ ] Tạo web app đơn giản với HTML/CSS/JS
- [ ] Containerize app với Docker
- [ ] Setup CI/CD pipeline với GitHub Actions
- [ ] Configure NGINX web server
- [ ] Deploy app lên production
- [ ] Monitor app với logs & health checks

**🎯 Mục tiêu cuối cùng:**
> Deploy một Portfolio Website hoàn chỉnh lên production với full CI/CD & monitoring!

---

## 🚀 NEXT STEPS

Sau khi hoàn thành Foundation:

- **Advanced Track:** 17 modules chuyên sâu (Kubernetes, Terraform, Ansible, Cloud...)
- **Certifications:** AWS, CKA, CKAD
- **Real Projects:** Contribute to open source

---

> **Lời khuyên:**
>
> - Làm từng module một cách tuần tự
> - Đừng skip bài tập
> - Integration Projects rất quan trọng - đây là lúc bạn thực sự "hiểu"
> - Final Project là cơ hội showcase skills
