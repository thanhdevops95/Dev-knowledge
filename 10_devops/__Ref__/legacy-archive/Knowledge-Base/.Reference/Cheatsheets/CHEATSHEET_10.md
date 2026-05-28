# Final Project - Cheatsheet

> **Quick reference for building & deploying full-stack DevOps project**

---

## 🎯 PROJECT CHECKLIST

### Initial Setup

```markdown
- [ ] Repository created on GitHub
- [ ] README.md with project description
- [ ] .gitignore configured
- [ ] Project structure created
- [ ] Development environment setup
```

### Application Development

```markdown
- [ ] Backend API implemented
- [ ] Frontend UI created
- [ ] Database models defined
- [ ] Authentication working
- [ ] CRUD operations functional
- [ ] Error handling implemented
- [ ] Health check endpoint added
```

### Docker & Containers

```markdown
- [ ] Dockerfile optimized
- [ ] docker-compose.yml for local dev
- [ ] docker-compose.prod.yml for production
- [ ] Environment variables configured
- [ ] Volumes for data persistence
- [ ] Networks configured
```

### CI/CD Pipeline

```markdown
- [ ] GitHub Actions workflow created
- [ ] Auto-tests on push
- [ ] Auto-build Docker images
- [ ] Auto-deploy to server
- [ ] Secrets configured properly
```

### Production Deployment

```markdown
- [ ] Server provisioned
- [ ] NGINX configured
- [ ] SSL certificate installed
- [ ] Application deployed
- [ ] Health checks passing
- [ ] Monitoring active
```

---

## 🐍 FLASK APPLICATION BOILERPLATE

### app/main.py

```python
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Health check
@app.route('/health')
def health():
    try:
        db.session.execute('SELECT 1')
        return {'status': 'healthy', 'database': True}, 200
    except:
        return {'status': 'unhealthy', 'database': False}, 500

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoints
@app.route('/api/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        # Create task
        data = request.json
        task = Task(title=data['title'], user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        return jsonify({'id': task.id}), 201
    
    # Get tasks
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([t.to_dict() for t in tasks])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### app/models.py

```python
from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    tasks = db.relationship('Task', backref='owner', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }
```

---

## 🐳 DOCKER CONFIGURATION

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Dependencies first (caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY app/ ./app/
COPY run.py .

# Non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

### docker-compose.yml (Development)

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/devdb
      - REDIS_URL=redis://redis:6379
      - FLASK_ENV=development
    volumes:
      - ./app:/app/app  # Hot reload
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: devdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### docker-compose.prod.yml (Production)

```yaml
version: '3.8'

services:
  web:
    image: username/myapp:${VERSION}
    restart: always
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:13
    restart: always
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    restart: always

volumes:
  postgres_data:
```

---

## ⚙️ GITHUB ACTIONS WORKFLOW

### .github/workflows/ci-cd.yml

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: pytest --cov=app tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: |
            username/myapp:latest
            username/myapp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd /var/www/myapp
            export VERSION=latest
            docker-compose pull
            docker-compose up -d
            
            # Wait for health check
            sleep 10
            curl -f http://localhost:5000/health || exit 1
```

---

## 🌐 NGINX CONFIGURATION

### /etc/nginx/sites-available/myapp

```nginx
upstream app_servers {
    least_conn;
    server localhost:5000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    server_name myapp.com www.myapp.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name myapp.com www.myapp.com;
    
    # SSL
    ssl_certificate /etc/letsencrypt/live/myapp.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myapp.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000" always;
    
    # Logging
    access_log /var/log/nginx/myapp_access.log;
    error_log /var/log/nginx/myapp_error.log;
    
    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    
    # Static files
    location /static {
        alias /var/www/myapp/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Application
    location / {
        proxy_pass http://app_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

---

## 📊 DEPLOYMENT COMMANDS

### Initial Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose

# Install NGINX
sudo apt install nginx

# Install Certbot
sudo apt install certbot python3-certbot-nginx
```

### Deploy Application

```bash
# Clone repository
cd /var/www
git clone https://github.com/username/myapp.git
cd myapp

# Setup environment
cp .env.example .env
nano .env  # Edit with production values

# Start application
docker-compose -f docker-compose.prod.yml up -d

# Setup NGINX
sudo cp nginx.conf /etc/nginx/sites-available/myapp
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Get SSL certificate
sudo certbot --nginx -d myapp.com -d www.myapp.com
```

### Update Application

```bash
cd /var/www/myapp
git pull
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🧪 TESTING

### Unit Tests (tests/test_app.py)

```python
import pytest
from app import create_app, db
from app.models import User, Task

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_create_task(client):
    # Login first
    client.post('/api/login', json={
        'username': 'test',
        'password': 'test123'
    })
    
    # Create task
    response = client.post('/api/tasks', json={
        'title': 'Test task'
    })
    assert response.status_code == 201
```

---

## 📝 .env.example

```bash
# Database
DATABASE_URL=postgresql://user:password@db:5432/mydb

# Redis
REDIS_URL=redis://redis:6379

# Application
SECRET_KEY=change-this-in-production
FLASK_ENV=production

# Email (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your@email.com
MAIL_PASSWORD=your-password
```

---

## 🚀 QUICK START

### Local Development

```bash
# Clone
git clone https://github.com/username/myapp.git
cd myapp

# Environment
cp .env.example .env

# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Access
# http://localhost:5000
```

### Production Deployment

```bash
# On server
cd /var/www
git clone https://github.com/username/myapp.git
cd myapp

# Configure
cp .env.example .env
nano .env

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# NGINX + SSL
sudo cp nginx.conf /etc/nginx/sites-available/myapp
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo certbot --nginx -d myapp.com
```

---

<div align="center">

**Build → Test → Deploy → Monitor! 🚀**

**Complete DevOps lifecycle! 🔄**

</div>
