# 🎯 Project: Docker Fundamentals

> Mini project: **Containerized Web Application**

---

## 📋 Project Overview

### Project Name: **Full Stack App Containerization**

Containerize một full-stack application.

### Duration: 2-3 ngày

---

## 🎯 Requirements

### Application Stack

- **Frontend**: React/Vue/Static HTML
- **Backend**: Node.js/Python API
- **Database**: PostgreSQL/MySQL

### Docker Requirements

#### 1. Frontend Container

```dockerfile
# Requirements:
# - Multi-stage build
# - Serve với nginx
# - < 30MB final image
# - Non-root user
```

#### 2. Backend Container

```dockerfile
# Requirements:
# - Proper layering
# - Health check
# - Environment variables
# - Non-root user
```

#### 3. Database Container

```yaml
# Requirements:
# - Persistent volume
# - Init scripts
# - Secure credentials
```

---

## 📁 Project Structure

```
fullstack-app/
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── nginx.conf
├── backend/
│   ├── src/
│   ├── Dockerfile
│   └── .dockerignore
├── database/
│   └── init.sql
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 📊 Expected Output

```bash
$ docker compose up -d

$ docker ps
CONTAINER ID   IMAGE          STATUS         PORTS
abc123         frontend       Up (healthy)   0.0.0.0:80->80/tcp
def456         backend        Up (healthy)   0.0.0.0:3000->3000/tcp
ghi789         postgres:15    Up (healthy)   5432/tcp

$ docker images
REPOSITORY   TAG       SIZE
frontend     latest    25MB
backend      latest    150MB
```

---

## ✅ Deliverables

- [ ] 3 Dockerfiles (frontend, backend, database)
- [ ] docker-compose.yml
- [ ] .dockerignore files
- [ ] Environment configuration
- [ ] Health checks implemented
- [ ] README với instructions
- [ ] All containers running và communicating

---

## 📊 Evaluation

| Criteria | Points |
|----------|--------|
| Working containers | 40 |
| Image optimization | 20 |
| Security (non-root) | 15 |
| Health checks | 10 |
| Documentation | 15 |

---

**Good luck! 🚀**
