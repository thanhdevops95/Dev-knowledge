# CHEATSHEET - Modules 02-09

Quick reference for all Foundation track modules.

---

## Module 02: GIT & GITHUB

### Basic Commands

```bash
git init                      # Initialize repo
git clone url                 # Clone repository
git status                    # Check status
git add file                  # Stage file
git add .                     # Stage all
git commit -m "message"       # Commit
git push                      # Push to remote
git pull                      # Pull from remote
git log --oneline             # View history
```

### Branching

```bash
git branch                    # List branches
git branch name               # Create branch
git checkout name             # Switch branch
git checkout -b name          # Create and switch
git merge branch              # Merge branch
git branch -d name            # Delete branch
git push origin --delete name # Delete remote branch
```

### Undoing

```bash
git restore file              # Discard changes
git restore --staged file     # Unstage
git reset HEAD~1              # Undo last commit
git revert commit-hash        # Revert commit
git stash                     # Stash changes
git stash pop                 # Apply stash
```

### Remote

```bash
git remote -v                 # Show remotes
git remote add origin url     # Add remote
git fetch                     # Fetch updates
git pull origin main          # Pull from main
git push -u origin main       # Push and set upstream
```

---

## Module 03: NETWORKING

### IP & DNS

```bash
ip addr                       # Show IP
ip route                      # Show routes
dig domain.com                # DNS lookup
nslookup domain.com           # DNS query
host domain.com               # Simple DNS lookup
ping -c 4 host                # Test connectivity
traceroute host               # Trace route
```

### Network Testing

```bash
curl http://example.com       # HTTP request
curl -I url                   # Headers only
wget url                      # Download file
nc -zv host port              # Test port
telnet host port              # Connect to port
netstat -tuln                 # Listening ports
ss -tuln                      # Socket stats
```

### Subnetting Quick Reference

```
/24 = 255.255.255.0   = 256 IPs (254 usable)
/25 = 255.255.255.128 = 128 IPs (126 usable)
/26 = 255.255.255.192 = 64 IPs (62 usable)
/27 = 255.255.255.224 = 32 IPs (30 usable)
/28 = 255.255.255.240 = 16 IPs (14 usable)
/29 = 255.255.255.248 = 8 IPs (6 usable)
/30 = 255.255.255.252 = 4 IPs (2 usable)
```

---

## Module 04: HTML/CSS/JS

### HTML Basics

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>Heading</h1>
    <p>Paragraph</p>
</body>
</html>
```

### CSS Common

```css
/* Selectors */
element { }
.class { }
#id { }
element.class { }

/* Box Model */
padding: 10px;
margin: 10px;
border: 1px solid black;

/* Flexbox */
display: flex;
justify-content: center;
align-items: center;
gap: 10px;
```

### JavaScript Essentials

```javascript
// Variables
let name = 'value';
const API = 'url';

// Functions
function greet(name) {
    return `Hello ${name}`;
}

// Arrow function
const add = (a, b) => a + b;

// DOM
document.querySelector('.class');
document.getElementById('id');
element.addEventListener('click', () => {});
```

---

## Module 05: DOCKER

### Images

```bash
docker pull image:tag         # Pull image
docker images                 # List images
docker build -t name .        # Build image
docker tag image user/image   # Tag image
docker push user/image        # Push image
docker rmi image              # Remove image
```

### Containers

```bash
docker run image              # Run container
docker run -d image           # Run detached
docker run -p 80:80 image     # Port mapping
docker run -v vol:/data image # Volume mount
docker ps                     # Running containers
docker ps -a                  # All containers
docker stop container         # Stop
docker rm container           # Remove
docker exec -it container sh  # Enter container
docker logs container         # View logs
docker logs -f container      # Follow logs
```

### Dockerfile

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### Docker Compose

```yaml
version: '3'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
    environment:
      - NODE_ENV=development
```

```bash
docker-compose up             # Start services
docker-compose up -d          # Start detached
docker-compose down           # Stop and remove
docker-compose logs -f        # Follow logs
docker-compose ps             # List services
```

---

## Module 06: CI/CD (GitHub Actions)

### Workflow Basics

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test
```

### Common Actions

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
  with:
    node-version: '18'
- uses: docker/build-push-action@v5
```

### Secrets

```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
```

---

## Module 07: NGINX

### Basic Config

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Reverse Proxy

```nginx
location / {
    proxy_pass http://localhost:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### SSL

```nginx
server {
    listen 443 ssl;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
}
```

### Commands

```bash
sudo nginx -t                 # Test config
sudo nginx -s reload          # Reload
sudo systemctl restart nginx  # Restart
sudo systemctl status nginx   # Status
```

---

## Module 08: DEPLOYMENT

### PM2 (Node.js)

```bash
pm2 start app.js              # Start app
pm2 list                      # List apps
pm2 logs                      # View logs
pm2 restart app               # Restart
pm2 stop app                  # Stop
pm2 delete app                # Remove
pm2 startup                   # Auto-start
pm2 save                      # Save config
```

### Deployment Commands

```bash
# Pull latest code
git pull origin main

# Install dependencies
npm install --production

# Build
npm run build

# Restart
pm2 restart app

# Or with Docker
docker-compose up -d --build
```

---

## Module 09: MONITORING

### Logs

```bash
# System logs
sudo journalctl -f
sudo tail -f /var/log/syslog

# NGINX logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Docker logs
docker logs -f container
```

### System Monitoring

```bash
# CPU & Memory
top
htop
free -h

# Disk
df -h
du -sh /path

# Network
netstat -an
ss -tuln

# Processes
ps aux
ps aux --sort=-%cpu | head
ps aux --sort=-%mem | head
```

### Health Checks

```bash
# HTTP endpoint
curl http://localhost/health

# Service status
systemctl status service

# Docker container
docker ps
docker inspect container
```

---

## 🔥 Most Used Commands (Top 20)

```bash
# 1. List files
ls -la

# 2. Change directory
cd /path

# 3. Git status
git status

# 4. Git add all
git add .

# 5. Git commit
git commit -m "message"

# 6. Git push
git push

# 7. Docker run
docker run -d -p 80:80 nginx

# 8. Docker ps
docker ps

# 9. Docker logs
docker logs -f container

# 10. View file
cat file.txt

# 11. Search in files
grep -r "pattern" .

# 12. Check port
netstat -tuln | grep 3000

# 13. Curl test
curl http://localhost

# 14. Disk space
df -h

# 15. Memory
free -h

# 16. Processes
ps aux

# 17. Kill process
kill -9 PID

# 18. NGINX reload
sudo nginx -s reload

# 19. PM2 restart
pm2 restart app

# 20. System status
systemctl status service
```

---

> **Master these commands → DevOps efficiency!** ⚡
