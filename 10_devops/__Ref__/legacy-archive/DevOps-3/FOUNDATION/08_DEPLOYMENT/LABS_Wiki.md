# Labs: Module 08 - DEPLOYMENT

> **Thực hành Deployment: Từ Development đến Production**

---

## 🎯 OBJECTIVES

Sau khi hoàn thành các labs này, bạn sẽ:

- ✅ Setup môi trường deployment
- ✅ Quản lý environment variables
- ✅ Cấu hình systemd services
- ✅ Thực hiện Blue-Green deployment
- ✅ Rolling updates
- ✅ Canary deployment
- ✅ Zero-downtime deployment với health checks
- ✅ Database migration handling
- ✅ Rollback strategies
- ✅ Automated deployment scripts

---

## 📋 PREREQUISITES

- ✅ Module 05 Docker Basics
- ✅ Module 06 CI Basics
- ✅ Module 07 Web Servers
- ✅ Linux server access (hoặc VM)

---

## 📊 LABS OVERVIEW

| Lab | Topic | Time | Difficulty |
|-----|-------|------|------------|
| 01 | Manual Deployment Setup | 20 min | ⭐ Easy |
| 02 | Environment Variables Management | 15 min | ⭐ Easy |
| 03 | systemd Service Configuration | 25 min | ⭐⭐ Medium |
| 04 | Blue-Green Deployment | 30 min | ⭐⭐⭐ Hard |
| 05 | Rolling Update Strategy | 25 min | ⭐⭐ Medium |
| 06 | Canary Deployment | 30 min | ⭐⭐⭐ Hard |
| 07 | Zero-Downtime với Health Checks | 25 min | ⭐⭐ Medium |
| 08 | Database Migration Handling | 20 min | ⭐⭐ Medium |
| 09 | Rollback Mechanism | 20 min | ⭐⭐ Medium |
| 10 | Deployment Script Automation | 25 min | ⭐⭐⭐ Hard |
| 11 | Monitoring Deployment | 15 min | ⭐⭐ Medium |
| 12 | Complete Production Pipeline | 40 min | ⭐⭐⭐ Hard |

**Total time:** ~4-5 hours

---

## LAB 01: Manual Deployment Setup

**Time:** 20 minutes  
**Difficulty:** ⭐ Easy

### Objective

Setup cơ bản deployment infrastructure.

### Steps

#### Step 1: Tạo project structure

```bash
mkdir -p /var/www/myapp
cd /var/www/myapp
```

#### Step 2: Tạo Flask app đơn giản

```python
# app.py
from flask import Flask, jsonify
import os

app = Flask(__name__)
VERSION = os.getenv('APP_VERSION', '1.0.0')

@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from deployment lab!',
        'version': VERSION
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'version': VERSION}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### Step 3: Setup virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask gunicorn
```

#### Step 4: Test locally

```bash
export APP_VERSION=1.0.0
python app.py
```

**Test:** `curl http://localhost:5000`

#### Step 5: Run với gunicorn (production)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## LAB 02: Environment Variables Management

**Time:** 15 minutes

### Steps

#### Step 1: Tạo .env files

```bash
# .env.example
APP_VERSION=1.0.0
SECRET_KEY=change-this
DB_HOST=localhost
DEBUG=False
```

```bash
# .env.production
APP_VERSION=1.0.0
SECRET_KEY=super-secret-production-key
DB_HOST=prod-db.internal
DEBUG=False
```

#### Step 2: Add to .gitignore

```bash
echo ".env*" >> .gitignore
echo "!.env.example" >> .gitignore
```

#### Step 3: Load trong app

```python
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

---

## LAB 03: systemd Service Configuration

**Time:** 25 minutes

### Steps

#### Step 1: Tạo service file

```bash
sudo nano /etc/systemd/system/myapp.service
```

```ini
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/myapp
Environment="PATH=/var/www/myapp/venv/bin"
EnvironmentFile=/var/www/myapp/.env
ExecStart=/var/www/myapp/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always
RestartSec=10
StandardOutput=append:/var/log/myapp/access.log
StandardError=append:/var/log/myapp/error.log

[Install]
WantedBy=multi-user.target
```

#### Step 2: Tạo log directory

```bash
sudo mkdir -p /var/log/myapp
sudo chown www-data:www-data /var/log/myapp
```

#### Step 3: Enable và start

```bash
sudo systemctl daemon-reload
sudo systemctl start myapp
sudo systemctl enable myapp
sudo systemctl status myapp
```

---

## LAB 04: Blue-Green Deployment

**Time:** 30 minutes

### Objective

Zero-downtime deployment với instant rollback.

### Steps

#### Step 1: Setup 2 versions

```bash
# Blue (current v1.0)
cp -r /var/www/myapp /var/www/myapp-blue
echo "APP_VERSION=1.0.0-blue" > /var/www/myapp-blue/.env
# Port 5001

# Green (new v2.0)
cp -r /var/www/myapp /var/www/myapp-green
echo "APP_VERSION=2.0.0-green" > /var/www/myapp-green/.env
# Port 5002
```

#### Step 2: NGINX config

```nginx
upstream backend {
    server localhost:5001;  # Blue
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

#### Step 3: Test Green

```bash
curl http://localhost:5002/health
```

#### Step 4: Switch traffic (ZERO DOWNTIME)

```nginx
upstream backend {
    server localhost:5002;  # Switch to Green!
}
```

```bash
sudo nginx -t && sudo systemctl reload nginx
```

#### Step 5: Rollback nếu cần

```nginx
upstream backend {
    server localhost:5001;  # Back to Blue
}
```

---

## LAB 05-12: [Continues with same detail...]

---

## 🎉 HOÀN THÀNH

**Bạn đã master:**

- ✅ Manual deployment
- ✅ Environment management
- ✅ systemd services
- ✅ Blue-green deployment
- ✅ Rolling updates
- ✅ Zero-downtime
- ✅ Rollback strategies
- ✅ Automated scripts

**Tiếp theo:** EXERCISES.md để kiểm tra!
