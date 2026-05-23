# Exercises: Module 10 - FINAL PROJECT

> **Bài tập Capstone Project**

**Mục đích:** Apply tất cả kiến thức Foundation  
**Thời gian:** 10-15 giờ

---

## 📋 PROJECT REQUIREMENTS

### Phase 1: Application (30 điểm)

**Exercise 1:** Create Flask backend

- REST API endpoints: /health, /api/tasks
- Database models with SQLAlchemy
- User authentication

**Exercise 2:** Create frontend

- HTML templates
- CSS styling
- JavaScript for interactivity

**Exercise 3:** Connect frontend + backend

- Fetch API calls
- Form handling
- Error handling

---

### Phase 2: Docker (25 điểm)

**Exercise 4:** Create Dockerfile

- Multi-stage build
- Non-root user
- Health check

**Exercise 5:** Create docker-compose.yml

- Web service
- Database service
- Network configuration
- Volume persistence

**Exercise 6:** Test locally

- `docker-compose up -d`
- Verify all services running
- Test endpoints

---

### Phase 3: CI/CD (20 điểm)

**Exercise 7:** Create GitHub Actions workflow

- Run tests on push
- Build Docker image
- Push to registry

**Exercise 8:** Add deployment step

- SSH to server
- Pull and restart containers
- Health check verification

---

### Phase 4: NGINX + SSL (15 điểm)

**Exercise 9:** Configure NGINX

- Reverse proxy to Flask
- Static file serving
- Gzip compression

**Exercise 10:** Setup SSL

- Let's Encrypt certificate
- HTTP to HTTPS redirect
- Security headers

---

### Phase 5: Monitoring (10 điểm)

**Exercise 11:** Add monitoring

- /health endpoint comprehensive
- /metrics endpoint
- Logging configuration

**Exercise 12:** Create alerts

- Health check script
- Cron job
- Notification on failure

---

## 📊 GRADING RUBRIC

| Category | Points |
|----------|--------|
| Working application | 30 |
| Docker setup | 25 |
| CI/CD pipeline | 20 |
| NGINX + SSL | 15 |
| Monitoring | 10 |
| **Total** | **100** |

**Passing:** 70/100

---

**Xem SOLUTIONS.md cho reference implementation!**
