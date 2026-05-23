# Module 08: DEPLOYMENT BASICS - Deploy lên Production

> **Thời gian học:** 1-2 tuần
>
> **Prerequisite:** Module 05 (Docker), Module 06 (CI/CD), Module 07 (NGINX)
>
> **Difficulty:** ⭐⭐⭐⭐☆

---

## 📋 Mục lục

1. [Deployment là gì?](#1-deployment-là-gì)
2. [Deployment Strategies](#2-deployment-strategies)
3. [Deploy Static Sites](#3-deploy-static-sites)
4. [Deploy với VPS](#4-deploy-với-vps)
5. [Container Deployment](#5-container-deployment)
6. [Environment Management](#6-environment-management)
7. [Rollback Strategies](#7-rollback-strategies)
8. [Monitoring After Deploy](#8-monitoring-after-deploy)
9. [Production Checklist](#9-production-checklist)

---

## 🎯 Learning Objectives

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu **deployment strategies** (Blue-Green, Canary, Rolling)
- ✅ Deploy **static sites** lên GitHub Pages, Netlify
- ✅ Deploy apps lên **VPS** (Virtual Private Server)
- ✅ Manage **environments** (dev, staging, production)
- ✅ Implement **zero-downtime deployments**
- ✅ Setup **rollback mechanisms**
- ✅ Monitor applications **post-deployment**
- ✅ Follow **production best practices**
- ✅ Deploy landing page từ modules trước lên production

---

## 1. Deployment là gì?

### 1.1. Deployment Definition

**Deployment (Triển khai):**
Process đưa code từ development environment lên production để users có thể sử dụng.

**Traditional deployment (manual):**

```
Developer laptop
     ↓ (git push)
Git repository
     ↓ (manual)
1. SSH vào server
2. git pull
3. Install dependencies
4. Build application
5. Restart server
6. Pray it works 🙏
```

**Problems:**

- ❌ Manual steps → Error-prone
- ❌ Downtime khi restart server
- ❌ Khó rollback nếu lỗi
- ❌ Không consistent (mỗi lần deploy khác nhau)
- ❌ Deploy vào production = stressful event

**Modern deployment (automated):**

```
Developer laptop
     ↓ (git push)
Git repository
     ↓ (webhook/trigger)
CI/CD Pipeline
├── Build
├── Test
├── Create artifacts
└── Deploy automatically
     ↓
Production (zero downtime)
     ↓
Monitor & Alert
```

**Benefits:**

- ✅ Automated → Consistent
- ✅ Zero/minimal downtime
- ✅ Easy rollback
- ✅ Fast feedback
- ✅ Deploy nhiều lần/ngày without fear

### 1.2. Deployment Pipeline

**Complete DevOps lifecycle:**

```
┌─────────────────────────────────────────────────────┐
│  PLAN → CODE → BUILD → TEST → RELEASE → DEPLOY     │
│    ↑                                          ↓     │
│    └──────────── MONITOR ←─── OPERATE ←──────┘     │
└─────────────────────────────────────────────────────┘
```

**Focus của module này: DEPLOY + OPERATE + MONITOR**

**Deployment pipeline stages:**

```
1. CODE COMMIT
   Developer: git push

2. CI PIPELINE (Module 06)
   ├── Checkout code
   ├── Run tests
   ├── Build Docker image
   └── Push to registry

3. DEPLOYMENT TRIGGER
   ├── Manual approval (CD)
   └── Auto deploy (CD)

4. DEPLOY TO ENVIRONMENT
   ├── Staging first (test)
   └── Production (real users)

5. POST-DEPLOY
   ├── Health checks
   ├── Smoke tests
   └── Monitor metrics

6. ROLLBACK (if needed)
   └── Revert to previous version
```

### 1.3. Environments

**Standard environments:**

```
┌────────────────────────────────────────┐
│  LOCAL (Developer laptop)              │
│  - Quick feedback                      │
│  - Mock data                           │
│  - Fast iteration                      │
└────────────────────────────────────────┘
            ↓
┌────────────────────────────────────────┐
│  DEV/DEVELOPMENT (Shared server)       │
│  - Latest code                         │
│  - Unstable                            │
│  - Auto-deploy on commit               │
└────────────────────────────────────────┘
            ↓
┌────────────────────────────────────────┐
│  STAGING/PRE-PRODUCTION                │
│  - Replica of production               │
│  - Real-like data                      │
│  - Final testing                       │
└────────────────────────────────────────┘
            ↓
┌────────────────────────────────────────┐
│  PRODUCTION                             │
│  - Real users                          │
│  - Real data                           │
│  - Stable, monitored                   │
└────────────────────────────────────────┘
```

**Why multiple environments?**

- ✅ **Isolate testing** từ production
- ✅ **Catch bugs** trước khi đến users
- ✅ **Test deploys** trên staging first
- ✅ **Parallel development** không conflict
- ✅ **Safe experiments** (A/B testing trên staging)

**Environment configs:**

| Aspect | Development | Staging | Production |
|--------|------------|---------|------------|
| **Data** | Mock/test data | Copy của prod data | Real user data |
| **Deploy frequency** | Mỗi commit | Daily/weekly | Weekly/monthly |
| **Stability** | Unstable, breaking OK | Stable-ish | Must be stable |
| **Monitoring** | Minimal | Moderate | Extensive |
| **Resources** | Minimal (1 small server) | Medium (similar to prod) | High (multiple servers) |
| **Access** | All developers | QA, senior devs | Restricted |

---

## 2. Deployment Strategies

### 2.1. Recreate (All-at-Once)

**How it works:**

```
v1 running
   ↓
Stop v1 (downtime starts)
   ↓
Deploy v2
   ↓
Start v2 (downtime ends)
```

**Timeline:**

```
00:00 - v1 serving users
00:01 - Stop v1 → Users see errors ❌
00:01-00:05 - Deploy v2 (4 minutes downtime)
00:05 - v2 starts → Users can access again ✅
```

**Pros:**

- ✅ Simple
- ✅ Same resources (không cần extra servers)
- ✅ Complete replacement

**Cons:**

- ❌ Downtime (seconds to minutes)
- ❌ Risky (if v2 broken, users affected)
- ❌ Slow rollback (need to redeploy v1)

**Use case:**

- Development/staging environments
- Maintenance windows (deploy lúc ít users)
- Small apps (downtime acceptable)

**Implementation:**

```bash
# Stop old version
docker stop myapp-v1
docker rm myapp-v1

# Deploy new version
docker pull myapp:v2
docker run -d -p 80:80 --name myapp-v2 myapp:v2

# Downtime: ~30 seconds
```

### 2.2. Rolling Deployment

**How it works:**

```
Servers: [v1] [v1] [v1]
    ↓
Step 1: [v2] [v1] [v1]  (1/3 updated)
    ↓
Step 2: [v2] [v2] [v1]  (2/3 updated)
    ↓
Step 3: [v2] [v2] [v2]  (all updated)
```

**Pros:**

- ✅ Zero downtime
- ✅ Gradual rollout
- ✅ Can pause if issues
- ✅ No extra resources

**Cons:**

- ❌ Slow (phải đợi health checks mỗi step)
- ❌ v1 và v2 running cùng lúc (compatibility issues)
- ❌ Rollback tricky nếu đã update nhiều servers

**Use case:**

- Production với multiple instances
- När resources limited
- Gradual updates OK

**Implementation (Docker Compose):**

```yaml
services:
  app:
    image: myapp:v2
    deploy:
      replicas: 3
      update_config:
        parallelism: 1  # Update 1 container at a time
        delay: 10s       # Wait 10s between updates
        failure_action: rollback
```

### 2.3. Blue-Green Deployment

**How it works:**

```
Blue (v1) - Currently serving traffic
Green (v2) - New version deployed, idle

Testing Green...
Green healthy? ✅

Switch traffic: Blue → Green
Green now serving traffic
Blue kept for rollback
```

**Visual:**

```
Load Balancer
     ↓
[Blue: v1] ← 100% traffic
[Green: v2] ← 0% traffic

↓ (switch)

Load Balancer
     ↓
[Blue: v1] ← 0% traffic (kept for rollback)
[Green: v2] ← 100% traffic
```

**Pros:**

- ✅ Instant cutover (zero downtime)
- ✅ Easy rollback (switch back to Blue)
- ✅ Green fully tested trước khi switch
- ✅ No version compatibility issues

**Cons:**

- ❌ Need double resources (2× servers/containers)
- ❌ Expensive
- ❌ Database migrations tricky

**Use case:**

- Critical production systems
- When rollback speed important
- Cloud environments (can spin up resources easily)

**Implementation (NGINX):**

```nginx
upstream backend {
    # Blue environment
    server blue-server:3000;
}

# To switch to Green:
upstream backend {
    # Green environment
    server green-server:3000;
}

# Reload NGINX: instant traffic switch!
```

**With health check:**

```bash
#!/bin/bash
# deploy-blue-green.sh

# Deploy green
docker run -d --name app-green myapp:v2

# Health check
while ! curl -f http://localhost:4000/health; do
    echo "Waiting for green to be healthy..."
    sleep 5
done

# Switch traffic (update NGINX config)
sed -i 's/app-blue:3000/app-green:3000/g' /etc/nginx/nginx.conf
nginx -s reload

echo "Switched to green. Blue is standby for rollback."
```

### 2.4. Canary Deployment

**How it works:**

```
v1 (stable) - 90% traffic
v2 (canary) - 10% traffic (test with small user base)

Monitor canary metrics...
Canary healthy? ✅

Gradually increase canary:
v1: 70%, v2: 30%
v1: 50%, v2: 50%
v1: 20%, v2: 80%
v1: 0%, v2: 100%
```

**Timeline:**

```
00:00 - v2 deployed, gets 5% traffic
00:30 - No errors, increase to 25%
01:00 - Still good, increase to 50%
01:30 - Metrics look great, 100% to v2!
```

**Pros:**

- ✅ Low risk (only small % users affected if broken)
- ✅ Real-world testing với actual users
- ✅ Gradual rollout → easy to stop
- ✅ A/B testing capability

**Cons:**

- ❌ Complex setup (need smart load balancer)
- ❌ Slow rollout
- ❌ Need robust monitoring

**Use case:**

- Large user base (millions)
- High-risk changes
- A/B testing features
- Real-world performance testing

**Implementation (NGINX):**

```nginx
split_clients "${remote_addr}" $backend {
    10%     canary;  # 10% to canary
    *       stable;  # 90% to stable
}

upstream stable {
    server app-v1:3000;
}

upstream canary {
    server app-v2:3000;
}

server {
    location / {
        proxy_pass http://$backend;
    }
}
```

---

## 3. Deploy Static Sites

### 3.1. GitHub Pages

**Free static hosting từ GitHub!**

**Setup:**

```bash
# 1. Create repo: username.github.io
# 2. Push HTML files to main branch

git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/username.github.io.git
git push -u origin main

# 3. Access: https://username.github.io
```

**Custom domain:**

```bash
# Add CNAME file
echo "example.com" > CNAME
git add CNAME
git commit -m "Add custom domain"
git push

# Configure DNS:
# CNAME record: www → username.github.io
# A record: @ → 185.199.108.153 (GitHub Pages IP)
```

**With build step (React, Vue):**

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - run: npm ci
      - run: npm run build
      
      - uses: actions/upload-pages-artifact@v2
        with:
          path: ./build
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v2
        id: deployment
```

### 3.2. Netlify

**Features:**

- ✅ Auto deploy từ Git
- ✅ Free SSL
- ✅ CDN global
- ✅ Form handling
- ✅ Serverless functions
- ✅ Branch previews

**Method 1: Drag & Drop**

```
1. Visit netlify.com
2. Drag build folder vào dashboard
3. Done! Got URL: random-name-123.netlify.app
```

**Method 2: Git Integration**

```
1. Connect GitHub repo
2. Configure build:
   - Build command: npm run build
   - Publish directory: dist/
3. Auto-deploy mỗi push!
```

**netlify.toml config:**

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"
```

**Custom domain:**

```
Netlify dashboard → Domain settings → Add custom domain
→ Configure DNS:
  CNAME: www → your-site.netlify.app
  A: @ → Netlify load balancer IP
```

### 3.3. Vercel

**Tương tự Netlify, optimized cho Next.js:**

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd my-project
vercel

# Production deploy
vercel --prod
```

**vercel.json:**

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "react",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

---

## 4. Deploy với VPS

### 4.1. What is VPS?

**VPS (Virtual Private Server):**

- Virtual machine trên cloud
- Full control (root access)
- Dedicated resources
- Cheaper than dedicated server

**Popular providers:**

| Provider | Starting Price | Locations | Notes |
|----------|---------------|-----------|-------|
| **DigitalOcean** | $5/month | Global | Beginner-friendly, great docs |
| **Linode** | $5/month | Global | Simple, reliable |
| **Vultr** | $2.50/month | Global | Cheap hourly billing |
| **AWS EC2** | $3.50/month | Global | Complex, free tier available |
| **Hetzner** | €4/month | Europe | Great price/performance |

**Typical $5/month VPS:**

- 1 CPU core
- 1 GB RAM
- 25 GB SSD
- 1 TB bandwidth

### 4.2. Initial Server Setup

**1. Create server:**

```
1. DigitalOcean dashboard → Create Droplet
2. Choose Ubuntu 22.04 LTS
3. $5/month plan
4. Add SSH key
5. Create
```

**2. SSH into server:**

```bash
ssh root@your-server-ip

# First time: Accept fingerprint
# Should see: root@server:~#
```

**3. Create non-root user:**

```bash
# Add user
adduser deploy

# Add to sudo group
usermod -aG sudo deploy

# Copy SSH keys
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy

# Test
ssh deploy@your-server-ip
```

**4. Harden security:**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Configure firewall
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Disable root SSH
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Install fail2ban (ban brute-force attacks)
sudo apt install fail2ban -y
```

### 4.3. Deploy NodeJS App

**Install dependencies:**

```bash
# NodeJS
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# PM2 (process manager)
sudo npm install -g pm2

# NGINX
sudo apt install nginx -y
```

**Clone app:**

```bash
cd /var/www
sudo git clone https://github.com/username/my-app.git
cd my-app
sudo npm install
```

**Create .env:**

```bash
sudo nano .env

# Add:
PORT=3000
NODE_ENV=production
DB_HOST=localhost
```

**Start với PM2:**

```bash
pm2 start server.js --name myapp

# Auto-start khi server reboot
pm2 startup systemd
pm2 save

# Monitor
pm2 status
pm2 logs myapp
```

**Configure NGINX reverse proxy:**

```nginx
# /etc/nginx/sites-available/myapp
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**Enable site:**

```bash
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**Setup SSL:**

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d example.com -d www.example.com
```

**Auto updates with webhook:**

```bash
# Install webhook
sudo apt install webhook -y

# Create deploy script
cat > /home/deploy/deploy.sh << 'EOF'
#!/bin/bash
cd /var/www/my-app
git pull origin main
npm install --production
pm2 restart myapp
EOF

chmod +x /home/deploy/deploy.sh

# Configure webhook
# /etc/webhook.conf
[
  {
    "id": "deploy",
    "execute-command": "/home/deploy/deploy.sh",
    "command-working-directory": "/home/deploy"
  }
]

# Start webhook
webhook -hooks /etc/webhook.conf -verbose
```

**GitHub webhook:**

```
GitHub repo → Settings → Webhooks → Add webhook
Payload URL: http://your-server-ip:9000/hooks/deploy
Content type: application/json
Secret: (optional)
```

---

## 5. Container Deployment

### 5.1. Docker Compose Deploy

**docker-compose.prod.yml:**

```yaml
version: '3.8'

services:
  app:
    image: username/myapp:latest
    restart: always
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=database
    env_file:
      - .env
    depends_on:
      - database
    networks:
      - app-network
  
  database:
    image: postgres:15-alpine
    restart: always
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    networks:
      - app-network
  
  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - certbot-webroot:/var/www/certbot
      - certbot-certs:/etc/letsencrypt
    depends_on:
      - app
    networks:
      - app-network

volumes:
  db-data:
  certbot-webroot:
  certbot-certs:

networks:
  app-network:
```

**Deploy:**

```bash
# On server
cd /opt/myapp
docker-compose -f docker-compose.prod.yml up -d

# Update
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

### 5.2. Docker Swarm (Basic Orchestration)

**Initialize swarm:**

```bash
docker swarm init
```

**Create stack:**

```yaml
# docker-stack.yml
version: '3.8'

services:
  app:
    image: username/myapp:latest
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
      update_config:
        parallelism: 1
        delay: 10s
    ports:
      - "3000:3000"
    networks:
      - app-net

networks:
  app-net:
```

**Deploy stack:**

```bash
docker stack deploy -c docker-stack.yml myapp

# List services
docker service ls

# Scale
docker service scale myapp_app=5

# Update image
docker service update --image username/myapp:v2 myapp_app
```

---

## 6. Environment Management

### 6.1. Environment Variables

**Never commit secrets!**

```bash
# ❌ BAD
# config.js
const DB_PASSWORD = "secret123";

# ✅ GOOD
# .env (gitignored)
DB_PASSWORD=secret123

# config.js
const DB_PASSWORD = process.env.DB_PASSWORD;
```

**.env.example (commit this):**

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=

# API Keys
API_KEY=
SECRET_KEY=
```

**Load .env:**

```javascript
// NodeJS
require('dotenv').config();

// Python
from dotenv import load_dotenv
load_dotenv()
```

### 6.2. Config per Environment

**Method 1: Multiple .env files**

```
.env.development
.env.staging
.env.production
```

```bash
# Load based on NODE_ENV
NODE_ENV=production node app.js
# Loads .env.production
```

**Method 2: Config service**

```javascript
// config/index.js
const environments = {
  development: {
    apiUrl: 'http://localhost:3000',
    dbHost: 'localhost'
  },
  production: {
    apiUrl: 'https://api.example.com',
    dbHost: 'prod-db.internal'
  }
};

module.exports = environments[process.env.NODE_ENV || 'development'];
```

---

## 7. Rollback Strategies

### 7.1. Version Tagging

**Always tag releases:**

```bash
# Tag version
git tag -a v1.2.3 -m "Release 1.2.3"
git push origin v1.2.3

# Build Docker image với tag
docker build -t myapp:v1.2.3 .
docker tag myapp:v1.2.3 myapp:latest
docker push myapp:v1.2.3
docker push myapp:latest
```

**Rollback:**

```bash
# Deploying v1.2.3 broke production

# Quick rollback to v1.2.2
docker pull myapp:v1.2.2
docker stop myapp-current
docker run -d --name myapp-current myapp:v1.2.2

# Or with Docker Compose
docker-compose down
docker-compose pull myapp:v1.2.2
docker-compose up -d
```

### 7.2. Database Rollback

**Challenge:** Code rollback easy, data rollback hard!

**Backward-compatible migrations:**

```sql
-- ✅ GOOD: Additive change
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
-- Rollback: Just ignore new column

-- ❌ BAD: Destructive change
ALTER TABLE users DROP COLUMN email;
-- Rollback: Data lost!
```

**Safe migration strategy:**

```
Deploy v1 → v2:
1. v1: Add new column (nullable)
2. Deploy code
3. Backfill data
4. Make column required
5. Remove old code

Rollback:
- Code rollback: v2 → v1
- DB stays (v1 ignores new column)
```

---

## 8. Monitoring After Deploy

### 8.1. Health Checks

**Endpoint:**

```javascript
// /health
app.get('/health', (req, res) => {
    // Check dependencies
    const dbConnected = checkDatabase();
    const redisConnected = checkRedis();
    
    if (dbConnected && redisConnected) {
        res.status(200).json({ status: 'healthy' });
    } else {
        res.status(503).json({ status: 'unhealthy' });
    }
});
```

**Monitor:**

```bash
# Simple check
curl https://example.com/health

# Uptime monitoring services (free tiers):
# - UptimeRobot
# - Pingdom
# - StatusCake
```

### 8.2. Logs

**Centralize logs:**

```bash
# PM2 logs
pm2 logs

# Docker logs
docker logs -f container-name

# System logs
sudo journalctl -u myapp -f
```

**Log levels:**

```javascript
logger.error('Critical error');  // Always log
logger.warn('Warning');          // Important
logger.info('User logged in');   // Normal ops
logger.debug('Variable value');  // Dev only
```

### 8.3. Metrics

**Key metrics:**

- **Response time:** Average, p95, p99
- **Error rate:** % của requests với errors
- **Throughput:** Requests per second
- **CPU/Memory:** Resource usage

**Tools sẽ học trong Module 09 (Monitoring Basics)**

---

## 9. Production Checklist

### 9.1. Pre-Deploy

- [ ] All tests pass locally
- [ ] Code reviewed và approved
- [ ] CI/CD pipeline green
- [ ] Staging tested successfully
- [ ] Database migrations tested
- [ ] Rollback plan documented
- [ ] Team notified (no surprise deploys!)

### 9.2. Deploy

- [ ] Use automation (not manual)
- [ ] Deploy during low-traffic hours (if possible)
- [ ] Monitor logs real-time
- [ ] Check health endpoints
- [ ] Verify critical user flows
- [ ] Monitor error rates

### 9.3. Post-Deploy

- [ ] Application healthy
- [ ] No spike in errors
- [ ] Response times normal
- [ ] Database connections stable
- [ ] User-reported issues monitored
- [ ] Rollback if needed

---

## 📚 Tổng kết

### Key Takeaways

1. **Deployment strategies** - Recreate, Rolling, Blue-Green, Canary
2. **Static sites** - GitHub Pages, Netlify, Vercel (easy!)
3. **VPS deployed** - Full control, NGINX + PM2
4. **Containers** - Docker Compose, Docker Swarm
5. **Environments** - Dev, Staging, Production
6. **Rollback** - Always have exit strategy
7. **Monitoring** - Health checks, logs, metrics

### Checklist

- [ ] Hiểu deployment strategies
- [ ] Deploy static site lên Netlify/GitHub Pages
- [ ] Setup VPS server properly
- [ ] Deploy NodeJS app với PM2
- [ ] Configure NGINX reverse proxy
- [ ] Setup HTTPS với Let's Encrypt
- [ ] Implement health checks
- [ ] Plan rollback strategy
- [ ] Monitor post-deployment

### Next: Module 09 - MONITORING_BASICS

👉 Monitor apps after deployment!

---

> **"Deploy early, deploy often, but deploy safe." - DevOps Wisdom** 🚀
