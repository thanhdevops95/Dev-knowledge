# Deployment - Cheatsheet

> **Production deployment strategies & best practices**

---

## 🚀 DEPLOYMENT STRATEGIES

### Blue-Green Deployment

```bash
# Setup
# Blue: Current production (v1.0)
# Green: New version (v1.1)

# Deploy to green
ssh green-server
git pull
docker-compose up -d

# Test green
curl http://green-server/health

# Switch traffic (load balancer)
# green becomes primary
# blue becomes backup

# If issues → switch back instantly!
```

### Rolling Deployment

```bash
# Update servers one by one

# Server 1
ssh server1
docker pull myapp:1.1
docker-compose up -d
# Wait for health check

# Server 2
ssh server2
docker pull myapp:1.1
docker-compose up -d
# Wait for health check

# Server 3
ssh server3
docker pull myapp:1.1
docker-compose up -d

# All servers updated, zero downtime!
```

### Canary Deployment

```bash
# Route small % to new version

# 5% to v1.1, 95% to v1.0
# Monitor metrics
# If good → 50% to v1.1
# If good → 100% to v1.1
# If bad → 0% to v1.1 (rollback)
```

---

## 🔧 ENVIRONMENT VARIABLES

### .env File

```bash
# .env
DB_HOST=localhost
DB_USER=appuser
DB_PASSWORD=secretpassword
API_KEY=sk-1234567890
DEBUG=False
```

### Load in Application

```python
# Python
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
API_KEY = os.getenv('API_KEY')
```

```javascript
// Node.js
require('dotenv').config();

const dbHost = process.env.DB_HOST;
const apiKey = process.env.API_KEY;
```

### .gitignore

```
.env
.env.production
.env.local
*.key
*.pem
```

---

## 🐳 DOCKER DEPLOYMENT

### Build & Tag

```bash
# Build image
docker build -t myapp:1.0.0 .

# Tag for registry
docker tag myapp:1.0.0 username/myapp:1.0.0
docker tag myapp:1.0.0 username/myapp:latest

# Push to registry
docker push username/myapp:1.0.0
docker push username/myapp:latest
```

### Pull & Run on Server

```bash
# On production server
docker pull username/myapp:1.0.0

# Stop old version
docker stop myapp-old

# Run new version
docker run -d \
  --name myapp \
  -p 5000:5000 \
  --restart=always \
  -e DB_PASSWORD=$DB_PASSWORD \
  username/myapp:1.0.0

# Remove old container
docker rm myapp-old
```

### Docker Compose Deployment

```bash
# On server
cd /var/www/myapp

# Pull latest images
docker-compose pull

# Update (zero downtime with multiple instances)
docker-compose up -d --no-deps --scale web=3 --no-recreate web

# Or simple update (brief downtime)
docker-compose up -d
```

---

## 🔄 SYSTEMD SERVICE

### Create Service File

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/myapp
Environment="PATH=/var/www/myapp/venv/bin"
Environment="DB_HOST=localhost"
EnvironmentFile=/var/www/myapp/.env
ExecStart=/var/www/myapp/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Manage Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable (start on boot)
sudo systemctl enable myapp

# Start
sudo systemctl start myapp

# Stop
sudo systemctl stop myapp

# Restart
sudo systemctl restart myapp

# Status
sudo systemctl status myapp

# View logs
sudo journalctl -u myapp -f
sudo journalctl -u myapp --since "1 hour ago"
```

---

## 🏥 HEALTH CHECKS

### Application Health Endpoint

```python
# Python Flask
@app.route('/health')
def health():
    try:
        # Check database
        db.execute('SELECT 1')
        db_healthy = True
    except:
        db_healthy = False
    
    try:
        # Check Redis
        redis.ping()
        redis_healthy = True
    except:
        redis_healthy = False
    
    if db_healthy and redis_healthy:
        return {'status': 'healthy'}, 200
    else:
        return {
            'status': 'unhealthy',
            'database': db_healthy,
            'redis': redis_healthy
        }, 500
```

### Check Health Script

```bash
#!/bin/bash
# check-health.sh

HEALTH_URL="http://localhost:5000/health"

if curl -f $HEALTH_URL > /dev/null 2>&1; then
    echo "✅ Application healthy"
    exit 0
else
    echo "❌ Application unhealthy"
    exit 1
fi
```

### Wait for Health After Deploy

```bash
# deploy.sh

# Deploy new version
docker-compose up -d

# Wait for healthy
echo "Waiting for application to be healthy..."
for i in {1..30}; do
    if curl -f http://localhost:5000/health > /dev/null 2>&1; then
        echo "✅ Application healthy!"
        break
    fi
    echo "Waiting... ($i/30)"
    sleep 2
done
```

---

## 🔙 ROLLBACK STRATEGIES

### Docker Rollback

```bash
# Keep previous version tagged
docker tag myapp:1.0.0 myapp:previous

# Deploy new version
docker tag myapp:1.1.0 myapp:current
docker-compose up -d

# If issues → Rollback
docker tag myapp:previous myapp:current
docker-compose up -d
```

### Git Tag Rollback

```bash
# Tag releases
git tag v1.0.0
git tag v1.1.0
git push --tags

# Rollback to previous version
git checkout v1.0.0
./deploy.sh
```

### Database Migration Rollback

```bash
# Forward-compatible migrations

# Bad: DROP COLUMN immediately
ALTER TABLE users DROP COLUMN old_field;

# Good: Two-step process
# Step 1: Deploy code that doesn't use old_field
# Step 2 (later): DROP COLUMN
```

---

## 📊 DEPLOYMENT CHECKLIST

### Pre-Deployment

```markdown
- [ ] All tests pass in CI/CD
- [ ] Code reviewed and approved
- [ ] Staging environment tested
- [ ] Database backup completed
- [ ] Rollback plan documented
- [ ] Team notified of deployment
```

### During Deployment

```markdown
- [ ] Health checks passing
- [ ] No errors in logs
- [ ] Response times normal
- [ ] Error rate not increased
- [ ] Database migrations successful
```

### Post-Deployment

```markdown
- [ ] Smoke tests completed
- [ ] Monitoring for 30 minutes
- [ ] Error rates checked
- [ ] Performance metrics normal
- [ ] Team notified of completion
```

---

## 🔐 SECRETS MANAGEMENT

### Never Commit Secrets

```bash
# ❌ Bad
DB_PASSWORD = "mysecretpassword"

# ✅ Good
DB_PASSWORD = os.getenv('DB_PASSWORD')
```

### Environment Files

```bash
# Production server
# /var/www/myapp/.env
DB_HOST=prod-db.internal
DB_PASSWORD=prod-secret-123
API_KEY=sk-prod-key
```

### Docker Secrets (Swarm)

```bash
# Create secret
echo "mysecret" | docker secret create db_password -

# Use in service
docker service create \
  --secret db_password \
  myapp
```

---

## 📝 DEPLOYMENT SCRIPTS

### Simple Deploy Script

```bash
#!/bin/bash
# deploy.sh

set -e  # Exit on error

echo "🚀 Starting deployment..."

# Pull latest code
git pull origin main

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application
sudo systemctl restart myapp

# Wait for healthy
sleep 5
if curl -f http://localhost:5000/health; then
    echo "✅ Deployment successful!"
else
    echo "❌ Health check failed!"
    exit 1
fi
```

### Docker Deploy Script

```bash
#!/bin/bash
# docker-deploy.sh

set -e

VERSION=$1

echo "🚀 Deploying version $VERSION..."

# Pull image
docker pull username/myapp:$VERSION

# Tag as current
docker tag username/myapp:$VERSION username/myapp:current

# Update docker-compose
docker-compose up -d

# Wait for healthy
for i in {1..30}; do
    if curl -f http://localhost:5000/health > /dev/null 2>&1; then
        echo "✅ Deployment successful!"
        exit 0
    fi
    sleep 2
done

echo "❌ Health check failed, rolling back..."
docker tag username/myapp:previous username/myapp:current
docker-compose up -d
exit 1
```

---

## 🌐 SERVER SETUP

### Initial Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essentials
sudo apt install -y git python3 python3-pip docker.io

# Create app user
sudo useradd -m -s /bin/bash appuser
sudo usermod -aG docker appuser

# Setup app directory
sudo mkdir -p /var/www/myapp
sudo chown appuser:appuser /var/www/myapp

# Setup firewall
sudo ufw allow 22      # SSH
sudo ufw allow 80      # HTTP
sudo ufw allow 443     # HTTPS
sudo ufw enable
```

### Clone & Setup App

```bash
# As appuser
cd /var/www
git clone https://github.com/username/myapp.git
cd myapp

# Setup environment
cp .env.example .env
nano .env  # Edit with production values

# Install dependencies
pip3 install -r requirements.txt

# Setup systemd service
sudo cp myapp.service /etc/systemd/system/
sudo systemctl enable myapp
sudo systemctl start myapp
```

---

## 📈 MONITORING DEPLOYMENT

### Log Deployment Events

```python
import logging

logger = logging.getLogger(__name__)

def deploy():
    logger.info("Deployment started", extra={
        'version': '1.1.0',
        'user': 'deployer',
        'timestamp': datetime.now()
    })
    
    # Deploy steps...
    
    logger.info("Deployment completed", extra={
        'duration': '2m 30s',
        'status': 'success'
    })
```

### Metrics to Track

```
Before deployment:
- Response time: 200ms average
- Error rate: 0.1%
- Memory: 500MB
- CPU: 30%

After deployment:
- Response time: Should be similar
- Error rate: Should not increase
- Memory: Should not spike
- CPU: Should be similar

If metrics acceptable for 30 min → Success!
```

---

## 🆘 EMERGENCY ROLLBACK

```bash
#!/bin/bash
# emergency-rollback.sh

echo "🚨 EMERGENCY ROLLBACK!"

# Stop current version
docker-compose down

# Switch to previous version
docker tag myapp:previous myapp:current

# Start previous version
docker-compose up -d

# Notify team
curl -X POST $SLACK_WEBHOOK \
  -d '{"text":"🚨 Emergency rollback performed!"}'

echo "✅ Rollback complete"
```

---

<div align="center">

**Deploy with confidence! 🚀✅**

**Always have a rollback plan! 🔙**

</div>
