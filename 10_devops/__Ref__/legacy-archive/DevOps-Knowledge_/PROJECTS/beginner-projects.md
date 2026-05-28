# Beginner DevOps Projects

> Dự án thực hành cho người mới bắt đầu

## 📋 Danh sách dự án

### 1. Static Website with Docker

**Mục tiêu:** Học cách containerize một website tĩnh

**Yêu cầu:**
- HTML/CSS website đơn giản
- Dockerfile để build image
- Chạy container locally
- Push image lên Docker Hub

**Kỹ năng học được:**
- Docker basics
- Dockerfile
- Container management
- Docker Hub

**Hướng dẫn:**
```bash
# 1. Tạo HTML file
echo "<h1>Hello DevOps!</h1>" > index.html

# 2. Tạo Dockerfile
cat > Dockerfile << EOF
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF

# 3. Build image
docker build -t my-website:1.0 .

# 4. Run container
docker run -d -p 8080:80 my-website:1.0

# 5. Test
curl http://localhost:8080
```

---

### 2. Simple Bash Automation Script

**Mục tiêu:** Tự động hóa task đơn giản với Bash

**Yêu cầu:**
- Script backup files
- Tự động cleanup old files
- Logging
- Cron job để chạy định kỳ

**Kỹ năng học được:**
- Bash scripting
- Cron jobs
- File management
- Logging

---

### 3. Git Workflow Practice

**Mục tiêu:** Thực hành Git workflow cơ bản

**Yêu cầu:**
- Tạo repository
- Feature branch workflow
- Pull requests
- Merge conflicts resolution

**Kỹ năng học được:**
- Git basics
- Branching strategy
- Collaboration workflow
- Conflict resolution

---

### 4. Docker Compose Multi-Container App

**Mục tiêu:** Chạy multi-container application

**Yêu cầu:**
- Web app (Node.js/Python)
- Database (PostgreSQL/MySQL)
- docker-compose.yml
- Environment variables

**Kỹ năng học được:**
- Docker Compose
- Multi-container apps
- Networking
- Environment configuration

---

### 5. Linux Server Setup

**Mục tiêu:** Setup và configure Linux server

**Yêu cầu:**
- Install Ubuntu Server (VM hoặc Cloud)
- Configure SSH
- Setup firewall (ufw)
- Install và configure web server (Nginx)
- Deploy simple website

**Kỹ năng học được:**
- Linux administration
- SSH configuration
- Firewall setup
- Web server configuration

---

### 6. Simple CI Pipeline

**Mục tiêu:** Tạo CI pipeline đơn giản

**Yêu cầu:**
- GitHub repository
- GitHub Actions workflow
- Automated tests
- Build Docker image

**Kỹ năng học được:**
- CI/CD basics
- GitHub Actions
- Automated testing
- Docker build automation

**Example workflow:**
```yaml
name: CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -t myapp:${{ github.sha }} .
    
    - name: Run tests
      run: docker run myapp:${{ github.sha }} npm test
```

---

### 7. Monitoring with Prometheus & Grafana

**Mục tiêu:** Setup basic monitoring

**Yêu cầu:**
- Docker Compose với Prometheus & Grafana
- Monitor Docker containers
- Create simple dashboard
- Setup alerts

**Kỹ năng học được:**
- Monitoring basics
- Prometheus
- Grafana
- Alerting

---

### 8. Infrastructure as Code với Terraform

**Mục tiêu:** Tạo infrastructure với code

**Yêu cầu:**
- Terraform configuration
- Create AWS EC2 instance (Free tier)
- Variables và outputs
- State management

**Kỹ năng học được:**
- IaC basics
- Terraform
- Cloud resources
- State management

---

## 💡 Tips

### Bắt đầu như thế nào?

1. **Chọn 1 project** - Đừng làm nhiều cùng lúc
2. **Đọc kỹ requirements** - Hiểu rõ mục tiêu
3. **Research** - Google, documentation, tutorials
4. **Làm từng bước nhỏ** - Đừng vội
5. **Document** - Ghi lại những gì học được
6. **Push lên GitHub** - Xây dựng portfolio

### Khi gặp khó khăn

- Đọc error messages kỹ
- Google error message
- Check documentation
- Hỏi trong communities (Reddit, Discord, Stack Overflow)
- Xem tutorials trên YouTube

### Best Practices

- ✅ Commit thường xuyên với clear messages
- ✅ Write README cho mỗi project
- ✅ Add comments trong code
- ✅ Test thoroughly
- ✅ Clean up resources sau khi xong

---

