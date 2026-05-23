# Module 08: DEPLOYMENT - Production Deployment Strategies

> **"Ship code confidently to production!"**

---

## 📚 MỤC LỤC

1. [Giới thiệu](#1-giới-thiệu)
2. [Deployment Strategies](#2-deployment-strategies)
3. [Environment Management](#3-environment-management)
4. [Process Management](#4-process-management)
5. [Zero-Downtime Deployment](#5-zero-downtime-deployment)
6. [Rollback Strategies](#6-rollback-strategies)
7. [Monitoring Deployments](#7-monitoring-deployments)
8. [Tổng kết](#8-tổng-kết)

---

## 1. Giới thiệu

### Câu chuyện mở đầu

> **2021**, deploy update lên production Friday afternoon.
>
> ```bash
> # On server
> git pull
> pip install -r requirements.txt
> killall python
> python app.py &
> ```
>
> **5 minutes later:**
>
> - Website down ❌
> - Database migration failed ❌  
> - Users seeing errors ❌
> - Boss calling 📞😱
>
> **Scramble to fix:**
>
> - Rollback code
> - Fix database
> - Restart app
> - 2 hours downtime
> - Lost customers
> - Team works until midnight
>
> **Senior DevOps:** "Cần deployment process đúng!"
>
> **New process:**
>
> ```
> 1. Deploy to staging ✅
> 2. Run tests ✅
> 3. Blue-green deployment ✅
> 4. Health checks ✅
> 5. Auto-rollback if fails ✅
> ```
>
> **Result:** Zero-downtime deployments 10x per day!

---

## 2. Deployment Strategies

### 2.1. Manual Deploy (DON'T!)

**❌ Bad practice:**

```bash
ssh server
git pull
pip install -r requirements.txt
systemctl restart app
# Hope it works! 🤞
```

**Problems:**

- Downtime during restart
- No rollback plan
- Manual errors
- No testing

### 2.2. Blue-Green Deployment

**Concept:** Two identical environments.

```
Blue (Current production)
Green (New version)

Deploy to Green → Test → Switch traffic → Blue becomes backup
```

**Implementation:**

```bash
# Deploy to green
ssh green-server "git pull && docker-compose up -d"

# Test green
curl http://green-server/health

# Switch load balancer
# green-server becomes primary
# blue-server becomes backup

# If issues → Switch back instantly!
```

### 2.3. Rolling Deployment

**Concept:** Update servers one by one.

```
3 servers running v1:
Server 1: v1 → v2 (others still v1)
Server 2: v1 → v2 (Server 1 done)
Server 3: v1 → v2 (Server 2 done)

All servers now v2, zero downtime!
```

### 2.4. Canary Deployment

**Concept:** Route small % traffic to new version first.

```
Deploy v2
Route 5% traffic → v2
Route 95% traffic → v1

If v2 OK → 50% to v2
If v2 OK → 100% to v2

If v2 BAD → Back to 100% v1
```

---

## 3. Environment Management

### 3.1. Environment Variables

**Don't hardcode:**

```python
# ❌ Bad
DB_HOST = "production-db.example.com"
API_KEY = "sk-1234567890"
```

**Use environment variables:**

```python
# ✅ Good
import os
DB_HOST = os.getenv('DB_HOST')
API_KEY = os.getenv('API_KEY')
```

**Set variables:**

```bash
# System-wide
export DB_HOST=localhost
export API_KEY=secret

# With systemd
# /etc/systemd/system/myapp.service
[Service]
Environment="DB_HOST=localhost"
Environment="API_KEY=secret"

# With Docker
docker run -e DB_HOST=localhost -e API_KEY=secret myapp

# With docker-compose
# docker-compose.yml
environment:
  - DB_HOST=localhost
  - API_KEY=secret
```

### 3.2. .env Files

**.env (local development):**

```
DB_HOST=localhost
DB_USER=devuser
DB_PASSWORD=devpass
DEBUG=True
```

**Load in app:**

```python
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
```

**⚠️ Never commit .env to Git!**

**.gitignore:**

```
.env
.env.production
```

---

## 4. Process Management

### 4.1. systemd Service

**Create service file:**

**/etc/systemd/system/myapp.service:**

```ini
[Unit]
Description=My Flask App
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/myapp
Environment="PATH=/var/www/myapp/venv/bin"
Environment="DB_HOST=localhost"
ExecStart=/var/www/myapp/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Manage service:**

```bash
# Enable (start on boot)
sudo systemctl enable myapp

# Start
sudo systemctl start myapp

# Stop
sudo systemctl stop myapp

# Restart
sudo systemctl restart myapp

# View logs
sudo journalctl -u myapp -f

# Status
sudo systemctl status myapp
```

### 4.2. Docker Compose for Production

**docker-compose.prod.yml:**

```yaml
version: '3.8'

services:
  web:
    image: myapp:${VERSION}
    restart: always
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=${DB_HOST}
      - DB_PASSWORD=${DB_PASSWORD}
    depends_on:
      - db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  db:
    image: postgres:13
    restart: always
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}

volumes:
  db-data:
```

**Deploy:**

```bash
export VERSION=1.2.0
export DB_PASSWORD=secret
docker-compose -f docker-compose.prod.yml up -d
```

---

## 5. Zero-Downtime Deployment

### 5.1. Health Checks

**Add health endpoint:**

```python
@app.route('/health')
def health():
    # Check database connection
    try:
        db.execute('SELECT 1')
        return {'status': 'healthy'}, 200
    except:
        return {'status': 'unhealthy'}, 500
```

**Use in deployment:**

```bash
# Deploy new version
docker-compose up -d

# Wait for healthy
while ! curl -f http://localhost:5000/health; do
    sleep 1
done

# Switch traffic
sudo systemctl reload nginx
```

### 5.2. Graceful Shutdown

**Handle SIGTERM properly:**

```python
import signal
import sys

def signal_handler(sig, frame):
    print('Gracefully shutting down...')
    # Finish current requests
    # Close database connections
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
```

**systemd will wait for graceful shutdown:**

```ini
[Service]
TimeoutStopSec=30
KillMode=mixed
```

---

## 6. Rollback Strategies

### 6.1. Keep Previous Version

**Docker tags:**

```bash
# Deploy new version
docker pull myapp:1.2.0
docker tag myapp:1.2.0 myapp:current

# If issues, rollback
docker tag myapp:1.1.0 myapp:current
docker-compose up -d
```

**Git tags:**

```bash
# Tag releases
git tag v1.2.0
git push --tags

# Rollback
git checkout v1.1.0
./deploy.sh
```

### 6.2. Database Migrations

**Always compatible both ways:**

**❌ Bad migration:**

```sql
-- Removes column immediately
ALTER TABLE users DROP COLUMN old_field;
```

**✅ Good migration (two-step):**

```sql
-- Step 1: Deploy code that doesn't use old_field
-- (old_field still exists)

-- Step 2 (later): Remove column
ALTER TABLE users DROP COLUMN old_field;
```

**Allows rollback without data loss!**

---

## 7. Monitoring Deployments

### 7.1. Deployment Checklist

```yaml
Pre-Deployment:
  - [ ] Tests pass in CI/CD
  - [ ] Staging tested
  - [ ] Database backed up
  - [ ] Rollback plan ready

During Deployment:
  - [ ] Health checks passing
  - [ ] Logs show no errors
  - [ ] Response times normal
  - [ ] Error rate not increased

Post-Deployment:
  - [ ] Smoke tests run
  - [ ] Monitor for 30 minutes
  - [ ] Alert team of success
```

### 7.2. Monitoring Metrics

**Track during deployment:**

```
- Response time
  Before: 200ms average
  After: Should be similar

- Error rate
  Before: 0.1%
  After: Should not increase

- Memory usage
  Before: 500MB
  After: Should not spike

- CPU usage
  Before: 30%
  After: Should be similar
```

**Auto-rollback if metrics bad:**

```bash
#!/bin/bash
# Deploy
./deploy.sh v1.2.0

# Monitor for 5 minutes
sleep 300

# Check error rate
ERROR_RATE=$(curl http://metrics/error_rate)
if [ "$ERROR_RATE" -gt "1" ]; then
    echo "High error rate! Rolling back..."
    ./deploy.sh v1.1.0
fi
```

---

## 8. Tổng kết

### ✅ Bạn đã học

**Deployment Strategies:**

- ✅ Blue-green deployment
- ✅ Rolling updates
- ✅ Canary releases

**Production Skills:**

- ✅ Environment management
- ✅ Process management (systemd)
- ✅ Zero-downtime deployments
- ✅ Rollback strategies

**Monitoring:**

- ✅ Health checks
- ✅ Deployment metrics
- ✅ Auto-rollback

### 📚 Next Module

**Module 09: MONITORING_BASICS** - Observability & alerting

### 🎓 Self-Assessment

Can you:

- [ ] Deploy without downtime?
- [ ] Manage environment variables?
- [ ] Rollback quickly if needed?
- [ ] Setup health checks?
- [ ] Monitor deployments?

**If YES → Production DevOps engineer! 🎉**

---

<div align="center">

**Safe deployments = Happy customers! 🚀✅**

</div>
