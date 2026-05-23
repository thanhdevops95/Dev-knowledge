# Labs: Module 10 - FINAL PROJECT

> **Thực hành: Build Complete DevOps Portfolio Project**

---

## 🎯 PROJECT OVERVIEW

### Task Manager Application

**Features:**

- User authentication
- CRUD tasks
- REST API backend
- Responsive frontend

**DevOps Stack:**

- Docker containers
- Docker Compose
- GitHub Actions CI/CD
- NGINX reverse proxy
- SSL/HTTPS
- Health monitoring
- Zero-downtime deploy

---

## 📊 IMPLEMENTATION LABS

| Lab | Phase | Time |
|-----|-------|------|
| 01 | Project Setup | 30 min |
| 02 | Backend Development | 90 min |
| 03 | Frontend Development | 60 min |
| 04 | Docker Setup | 45 min |
| 05 | Docker Compose | 30 min |
| 06 | CI/CD Pipeline | 45 min |
| 07 | NGINX Configuration | 30 min |
| 08 | SSL Setup | 20 min |
| 09 | Monitoring | 30 min |
| 10 | Production Deploy | 45 min |

**Total:** 8-10 hours

---

## LAB 01: Project Setup

```bash
mkdir task-manager && cd task-manager
git init

mkdir -p app/{templates,static/{css,js}}
mkdir -p nginx .github/workflows

touch app/main.py app/requirements.txt
touch nginx/nginx.conf
touch docker-compose.yml Dockerfile
touch .github/workflows/ci.yml
```

---

## LAB 02: Backend (Flask)

```python
# app/main.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@db:5432/tasks'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/tasks', methods=['GET', 'POST'])
def tasks():
    # Implementation here
    pass
```

**requirements.txt:**

```
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
gunicorn==20.1.0
psycopg2-binary==2.9.6
```

---

## LAB 03-04: Frontend + Docker

Xem SOLUTIONS.md cho complete code.

---

## LAB 05: Docker Compose

```yaml
version: '3.8'

services:
  web:
    build: .
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://user:${DB_PASS}@db:5432/tasks
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: postgres:13-alpine
    restart: unless-stopped
    environment:
      POSTGRES_PASSWORD: ${DB_PASS}
      POSTGRES_DB: tasks
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web
    networks:
      - app-network

volumes:
  db-data:

networks:
  app-network:
```

---

## LAB 06: CI/CD Pipeline

```yaml
name: CI/CD

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install pytest && pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: docker/build-push-action@v4
        with:
          push: true
          tags: user/task-manager:latest
      
      - uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.HOST }}
          script: |
            cd /app
            docker-compose pull
            docker-compose up -d
```

---

## LAB 07-10: NGINX, SSL, Monitoring, Production

Xem SOLUTIONS.md cho complete implementation guide.

---

## 🎓 GRADING RUBRIC

| Criteria | Points |
|----------|--------|
| Working application | 25 |
| Docker setup | 20 |
| CI/CD pipeline | 20 |
| NGINX + SSL | 15 |
| Health monitoring | 10 |
| Documentation | 10 |
| **Total** | **100** |

---

**Complete project = Portfolio ready! 🚀**
