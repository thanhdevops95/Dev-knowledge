# 🎯 Project: Docker Advanced

> Mini project: **Production-Ready Docker Images**

---

## 📋 Project Overview

### Project Name: **Containerized Microservices Stack**

Xây dựng production-ready Docker images cho microservices.

### Duration: 3-4 ngày

---

## 🎯 Requirements

### Application Stack

- **API Gateway**: NGINX reverse proxy
- **Auth Service**: Node.js JWT authentication
- **User Service**: Python Flask API
- **Database**: PostgreSQL

### Docker Requirements

#### 1. All Services Must Have

- Multi-stage builds
- Non-root user
- Health checks
- Size-optimized (alpine/distroless)
- No secrets in image
- Proper .dockerignore

#### 2. Security Requirements

- Vulnerability scan (zero critical)
- Read-only filesystem where possible
- Minimal capabilities
- No privileged mode

#### 3. Operational Requirements

- Resource limits defined
- Proper logging
- Graceful shutdown

---

## 📁 Project Structure

```
microservices/
├── gateway/
│   ├── nginx.conf
│   └── Dockerfile
├── auth-service/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── user-service/
│   ├── app/
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
└── README.md
```

---

## 📊 Acceptance Criteria

| Service | Max Size | Health Check | Non-root |
|---------|----------|--------------|----------|
| Gateway | <30MB | ✓ | ✓ |
| Auth | <150MB | ✓ | ✓ |
| User | <100MB | ✓ | ✓ |
| DB | Default | ✓ | Default |

---

## ✅ Deliverables

- [ ] 4 optimized Dockerfiles
- [ ] docker-compose.yml với all configurations
- [ ] Vulnerability scan reports
- [ ] Size comparison documentation
- [ ] README với build/run instructions

---

**Good luck! 🚀**
