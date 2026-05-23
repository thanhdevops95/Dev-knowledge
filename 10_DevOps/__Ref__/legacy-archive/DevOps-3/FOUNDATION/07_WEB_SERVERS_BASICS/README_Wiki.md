# Module 07: WEB SERVERS BASICS - NGINX Mastery

> **Thời gian học:** 1-2 tuần
>
> **Prerequisite:** Module 03 (Networking), Module 04 (HTML/CSS/JS), Module 05 (Docker)
>
> **Difficulty:** ⭐⭐⭐☆☆

---

## 📋 Mục lục

1. [Web Servers là gì?](#1-web-servers-là-gì)
2. [NGINX Fundamentals](#2-nginx-fundamentals)
3. [Configuration Basics](#3-configuration-basics)
4. [Serving Static Files](#4-serving-static-files)
5. [Reverse Proxy](#5-reverse-proxy)
6. [Load Balancing](#6-load-balancing)
7. [HTTPS & SSL/TLS](#7-https--ssltls)
8. [Performance Tuning](#8-performance-tuning)
9. [Troubleshooting](#9-troubleshooting)

---

## 🎯 Learning Objectives

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu **Web Server vs Application Server**
- ✅ Nắm vững **NGINX architecture** và event-driven model
- ✅ Cấu hình NGINX serve **static files**
- ✅ Setup **reverse proxy** để forward requests đến backend
- ✅ Implement **load balancing** cho high availability
- ✅ Enable **HTTPS** với SSL/TLS certificates
- ✅ Optimize performance với **caching, compression**
- ✅ Debug common **NGINX issues**
- ✅ Deploy landing page từ modules trước với NGINX

---

## 1. Web Servers là gì?

### 1.1. HTTP Request-Response Cycle

**Basic web interaction:**

```
Browser (Client)              Web Server
     |                             |
     |---HTTP Request------------->|
     |  GET /index.html HTTP/1.1   |
     |  Host: example.com          |
     |                             |
     |<--HTTP Response-------------|
     |  HTTP/1.1 200 OK            |
     |  Content-Type: text/html    |
     |  <html>...</html>           |
     |                             |
```

**Web server tasks:**

1. **Listen** trên port (80 for HTTP, 443 for HTTPS)
2. **Accept** TCP connections từ clients
3. **Parse** HTTP requests
4. **Find** requested file hoặc forward đến application
5. **Send** HTTP response với content
6. **Log** request details
7. **Close** connection (hoặc keep-alive)

### 1.2. Web Server vs Application Server

**Web Server:**

- Serve **static content** (HTML, CSS, JS, images)
- Fast, efficient file serving
- Hiểu HTTP protocol
- Examples: NGINX, Apache, Caddy

**Application Server:**

- Execute **dynamic code** (Python, Java, NodeJS)
- Generate content on-the-fly
- Business logic processing
- Database interactions
- Examples: Node.js, Gunicorn, Tomcat, uWSGI

**Real-world architecture:**

```
Client Browser
     ↓
Internet
     ↓
Web Server (NGINX)
├── Serve static files (HTML, CSS, JS, images)
└── Forward dynamic requests to:
         ↓
    Application Server (NodeJS, Python)
    ├── Process business logic
    ├── Query database
    └── Generate HTML/JSON
```

**Why separate?**

- ✅ **Specialization** - Web server tốt ở static files, app server tốt ở logic
- ✅ **Security** - Web server là barrier, app server không expose trực tiếp
- ✅ **Scaling** - Có thể scale independently
- ✅ **Performance** - NGINX serve static files **10-100x faster** than NodeJS

**Example - Landing page:**

```
Request: https://example.com/about.html
→ NGINX: Serve file directly (fast!) ⚡

Request: https://example.com/api/users
→ NGINX: Forward to NodeJS backend
→ NodeJS: Query DB, return JSON
```

### 1.3. Popular Web Servers

**Market share (2024):**

| Server | Market Share | Pros | Cons |
|--------|-------------|------|------|
| **NGINX** | ~35% | Fast, low memory, reverse proxy | Complex config for beginners |
| **Apache** | ~30% | Mature, .htaccess, modules | Higher memory usage |
| **Cloudflare** | ~20% | CDN, DDoS protection, caching | Paid features, vendor lock-in |
| **Caddy** | ~2% | Auto HTTPS, simple config | Newer, smaller ecosystem |
| **IIS** | ~6% | Windows integration | Windows-only |

**Why NGINX for DevOps?**

- ✅ **Performance** - Event-driven, non-blocking I/O
- ✅ **Low resource** - ~1-2 MB RAM per worker
- ✅ **Reverse proxy** - Built-in, production-grade
- ✅ **Load balancing** - Multiple algorithms
- ✅ **Containerization** - Works great trong Docker
- ✅ **Community** - Huge ecosystem, tutorials

---

## 2. NGINX Fundamentals

### 2.1. Architecture

**Event-Driven, Asynchronous, Non-Blocking:**

```
Traditional (Apache):
Process-based model:
├── Request 1 → Process 1 (blocked đợi I/O)
├── Request 2 → Process 2 (blocked đợi I/O)
└── Request 3 → Process 3 (blocked đợi I/O)

Problem: Mỗi request cần 1 process → High memory
C10K problem (10,000 concurrent connections = impossible)

NGINX:
Event-driven model:
Master Process
└── Worker Processes (1 per CPU core)
    └── Event Loop
        ├── Request 1 (non-blocking)
        ├── Request 2 (non-blocking)
        ├── Request 3 (non-blocking)
        └── ... (10,000+ requests)

Each worker handle thousands of connections!
```

**Process model:**

```
Master Process (root)
├── Read & validate config
├── Bind to ports
├── Spawn worker processes
└── Control worker lifecycle

Worker Processes (www-data user)
├── Accept connections
├── Process requests
├── Serve files
└── Proxy to backends

Helper Processes
├── Cache loader
└── Cache manager
```

**Check processes:**

```bash
ps aux | grep nginx

# Output:
root     1234  nginx: master process
www-data 1235  nginx: worker process
www-data 1236  nginx: worker process
www-data 1237  nginx: worker process
```

### 2.2. Installation

**Ubuntu/Debian:**

```bash
# Update packages
sudo apt update

# Install NGINX
sudo apt install nginx -y

# Start NGINX
sudo systemctl start nginx

# Enable auto-start khi boot
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx

# Verify
curl http://localhost
# Should see "Welcome to nginx!" page
```

**NGINX version:**

```bash
nginx -v
# nginx version: nginx/1.24.0 (Ubuntu)

# Detailed info
nginx -V
```

**Docker:**

```bash
docker run -d -p 8080:80 --name nginx nginx:alpine

# Test
curl http://localhost:8080
```

### 2.3. File Structure

**Important files & directories:**

```
/etc/nginx/
├── nginx.conf              # Main config file
├── sites-available/        # Available site configs
│   └── default
├── sites-enabled/          # Enabled sites (symlinks)
│   └── default -> ../sites-available/default
├── conf.d/                 # Additional configs
├── snippets/               # Reusable config snippets
├── modules-enabled/        # Enabled modules
└── mime.types              # File type mappings

/var/log/nginx/
├── access.log              # Access logs
└── error.log               # Error logs

/var/www/html/              # Default web root
└── index.nginx-debian.html

/usr/share/nginx/html/      # Alternative web root (Docker default)
└── index.html
```

### 2.4. Basic Commands

```bash
# Test configuration syntax
sudo nginx -t

# Reload config (graceful, no downtime)
sudo nginx -s reload

# Or via systemctl
sudo systemctl reload nginx

# Stop NGINX
sudo systemctl stop nginx

# Start
sudo systemctl start nginx

# Restart (có downtime)
sudo systemctl restart nginx

# View logs real-time
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## 3. Configuration Basics

### 3.1. Configuration Structure

**Hierarchical structure:**

```nginx
# Global context
user www-data;
worker_processes auto;

# Events context
events {
    worker_connections 1024;
}

# HTTP context
http {
    include /etc/nginx/mime.types;
    
    # Server context
    server {
        listen 80;
        server_name example.com;
        
        # Location context
        location / {
            root /var/www/html;
        }
        
        location /api {
            proxy_pass http://backend;
        }
    }
}
```

**Context hierarchy:**

```
main (global)
├── events
└── http
    ├── server
    │   └── location
    └── upstream
```

**Directives:**

- **Simple directive:** `worker_processes 4;`
- **Block directive:** `server { ... }`

### 3.2. Minimal Configuration

**Simplest working config:**

```nginx
# /etc/nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        
        location / {
            root /var/www/html;
            index index.html;
        }
    }
}
```

**What it does:**

1. Listen trên port 80
2. Serve files từ `/var/www/html/`
3. Default file: `index.html`

**Test:**

```bash
# Create test file
echo "<h1>Hello NGINX!</h1>" | sudo tee /var/www/html/index.html

# Test config
sudo nginx -t

# Reload
sudo nginx -s reload

# Access
curl http://localhost
# Output: <h1>Hello NGINX!</h1>
```

### 3.3. Common Directives

**Server block directives:**

```nginx
server {
    # Listen port
    listen 80;
    listen [::]:80;  # IPv6
    
    # Server name (domain)
    server_name example.com www.example.com;
    
    # Document root
    root /var/www/example.com;
    
    # Default index files
    index index.html index.htm;
    
    # Access & error logs
    access_log /var/log/nginx/example.access.log;
    error_log /var/log/nginx/example.error.log;
    
    # Client body size limit
    client_max_body_size 10M;
}
```

**Location block directives:**

```nginx
location / {
    # Root directory
    root /var/www/html;
    
    # Try files in order
    try_files $uri $uri/ /index.html;
    
    # Autoindex (directory listing)
    autoindex on;
    
    # Add headers
    add_header X-Custom-Header "Value";
}
```

**Variables:**

```nginx
location / {
    # Built-in variables
    # $uri - Request URI (/index.html)
    # $request_uri - Full URI with query (/search?q=nginx)
    # $host - Hostname (example.com)
    # $remote_addr - Client IP
    # $request_method - GET, POST, etc.
    
    return 200 "URI: $uri\nHost: $host\n";
}
```

---

## 4. Serving Static Files

### 4.1. Basic Static Site

**Project structure:**

```
my-website/
├── index.html
├── about.html
├── css/
│   └── style.css
├── js/
│   └── app.js
└── images/
    └── logo.png
```

**NGINX config:**

```nginx
server {
    listen 80;
    server_name localhost;
    
    root /var/www/my-website;
    index index.html;
    
    # Main location
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Cache static assets
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**Deploy:**

```bash
# Copy files
sudo cp -r my-website /var/www/

# Set permissions
sudo chown -R www-data:www-data /var/www/my-website

# Test & reload
sudo nginx -t && sudo nginx -s reload
```

### 4.2. Location Matching

**Priority order:**

```nginx
server {
    # 1. Exact match (highest priority)
    location = /exact {
        return 200 "Exact match";
    }
    
    # 2. Preferential prefix match (^~)
    location ^~ /images/ {
        root /var/www;
    }
    
    # 3. Regex match (case-sensitive ~)
    location ~ \.php$ {
        # PHP handling
    }
    
    # 4. Regex match (case-insensitive ~*)
    location ~* \.(jpg|jpeg|png|gif)$ {
        root /var/www/images;
    }
    
    # 5. Prefix match (lowest priority)
    location / {
        root /var/www/html;
    }
}
```

**Examples:**

```
Request: /exact
→ Match #1 (exact)

Request: /images/logo.png
→ Match #2 (^~ prefix, stops regex checking)

Request: /test.php
→ Match #3 (~ regex)

Request: /photo.JPG
→ Match #4 (~* case-insensitive)

Request: /about.html
→ Match #5 (prefix)
```

### 4.3. SPA (Single Page Application)

**Problem:** React/Vue apps dùng client-side routing

```
User visits: https://example.com/about
Browser requests: /about
NGINX: File không tồn tại → 404 ❌
```

**Solution:** Redirect all requests về index.html

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/react-app/build;
    index index.html;
    
    location / {
        # Try file, then directory, then fallback to index.html
        try_files $uri $uri/ /index.html;
    }
    
    # Cache static assets (với hash trong filename)
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**How it works:**

```
Request: /about
1. Try /about file → Not found
2. Try /about/ directory → Not found
3. Serve /index.html → React router handles /about ✅
```

---

## 5. Reverse Proxy

### 5.1. Reverse Proxy là gì?

**Forward Proxy vs Reverse Proxy:**

```
FORWARD PROXY (client-side):
Client → Proxy → Internet
     (hide client IP)
Use case: VPN, corporate networks

REVERSE PROXY (server-side):
Client → Proxy → Backend Servers
     (hide backend servers)
Use case: Load balancing, caching, SSL termination
```

**Architecture:**

```
Internet
    ↓
NGINX (Reverse Proxy)
:80, :443
    ↓
[Routing logic]
    ↓
Backend Servers
├── App Server 1 (localhost:3000)
├── App Server 2 (localhost:3001)
└── API Server (localhost:4000)
```

**Benefits:**

- ✅ **Single entry point** - Clients chỉ biết NGINX, không biết backends
- ✅ **SSL termination** - NGINX handle HTTPS, backends dùng HTTP
- ✅ **Load balancing** - Distribute requests across servers
- ✅ **Caching** - NGINX cache responses, giảm load backends
- ✅ **Security** - NGINX filter malicious requests
- ✅ **Compression** - NGINX compress responses

### 5.2. Basic Reverse Proxy

**Backend server (NodeJS example):**

```javascript
// server.js
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Hello from backend!');
});

app.listen(3000, () => {
    console.log('Backend running on port 3000');
});
```

**NGINX config:**

```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        # Proxy to backend
        proxy_pass http://localhost:3000;
        
        # Forward original client info
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Flow:**

```
Client → https://example.com/
    ↓
NGINX :80
    ↓
proxy_pass to localhost:3000
    ↓
NodeJS app
    ↓
Response: "Hello from backend!"
    ↓
NGINX
    ↓
Client receives response
```

### 5.3. Multiple Backends

**Different paths → Different backends:**

```nginx
server {
    listen 80;
    server_name example.com;
    
    # Frontend (static files)
    location / {
        root /var/www/frontend;
        try_files $uri /index.html;
    }
    
    # API backend
    location /api/ {
        proxy_pass http://localhost:4000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Admin panel
    location /admin/ {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host $host;
    }
    
    # WebSocket server
    location /ws/ {
        proxy_pass http://localhost:6000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

**Routing:**

```
/              → Static files (React app)
/api/users     → Backend API :4000
/admin/        → Admin panel :5000
/ws/           → WebSocket :6000
```

### 5.4. Upstream Blocks

**Define backend servers:**

```nginx
# Define upstream
upstream backend_servers {
    server localhost:3000;
    server localhost:3001;
    server localhost:3002;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
    }
}
```

**Advanced upstream:**

```nginx
upstream api_backend {
    # Load balancing method (default: round-robin)
    least_conn;  # Or: ip_hash, hash $request_uri
    
    # Servers với weights
    server backend1.example.com:8080 weight=3;
    server backend2.example.com:8080 weight=2;
    server backup.example.com:8080 backup;
    
    # Health checks
    server backend3.example.com:8080 max_fails=3 fail_timeout=30s;
}
```

---

## 6. Load Balancing

### 6.1. Load Balancing Algorithms

**1. Round Robin (default):**

```nginx
upstream backend {
    server backend1;
    server backend2;
    server backend3;
}

# Requests distributed:
# Request 1 → backend1
# Request 2 → backend2
# Request 3 → backend3
# Request 4 → backend1
# ...
```

**2. Least Connections:**

```nginx
upstream backend {
    least_conn;
    server backend1;
    server backend2;
    server backend3;
}

# Request đến server có ít connections nhất
# Good for long-running requests
```

**3. IP Hash:**

```nginx
upstream backend {
    ip_hash;
    server backend1;
    server backend2;
    server backend3;
}

# Same client IP → always same backend
# Good for session persistence (sticky sessions)
```

**4. Generic Hash:**

```nginx
upstream backend {
    hash $request_uri consistent;
    server backend1;
    server backend2;
    server backend3;
}

# Hash based on URI
# Same URI → same backend (cache-friendly)
```

**5. Weighted:**

```nginx
upstream backend {
    server backend1 weight=3;  # 60% traffic
    server backend2 weight=2;  # 40% traffic
}

# Use khi servers có specs khác nhau
# Powerful server → higher weight
```

### 6.2. Health Checks

**Passive health checks:**

```nginx
upstream backend {
    server backend1 max_fails=3 fail_timeout=30s;
    server backend2 max_fails=3 fail_timeout=30s;
    server backup_server backup;
}

# Nếu backend1 fails 3 times trong 30s:
# → Mark as down for 30s
# → Use backup_server
```

**Parameters:**

- `max_fails=N` - Số failures trước khi mark down
- `fail_timeout=T` - Time window & down time
- `backup` - Only use khi primary servers down
- `down` - Permanently mark server down

**Example scenario:**

```nginx
upstream app {
    server app1:3000 max_fails=2 fail_timeout=10s;
    server app2:3000 max_fails=2 fail_timeout=10s;
    server app3:3000 backup;
}

# Timeline:
# 00:00 - app1 receives request → timeout (fail 1)
# 00:05 - app1 receives request → 500 error (fail 2)
# 00:05 - app1 marked down for 10s
# 00:05-00:15 - Requests to app2 only
# 00:15 - app1 back in rotation
```

### 6.3. Session Persistence

**Problem:**

```
User login → Session stored trên backend1
Next request → Load balancer sends to backend2
backend2: "Who are you?" (no session)
User: Logged out ❌
```

**Solution 1: IP Hash**

```nginx
upstream backend {
    ip_hash;
    server backend1;
    server backend2;
}
# Same IP → same backend
```

**Solution 2: Sticky Cookie (NGINX Plus)**

```nginx
upstream backend {
    server backend1;
    server backend2;
    sticky cookie srv_id expires=1h;
}
```

**Solution 3: Centralized Session Store (Best)**

```
Don't store session trên app servers!
Use Redis/Memcached:

Client → Any backend
Backend → Redis (get session)
```

---

## 7. HTTPS & SSL/TLS

### 7.1. Tại sao cần HTTPS?

**HTTP (unencrypted):**

```
Browser → Router → ISP → Server
         ↑
    Can see:
    - Passwords
    - Credit cards
    - Personal info
```

**HTTPS (encrypted):**

```
Browser → [Encrypted tunnel] → Server

Everyone in between sees:
- Destination IP only
- Cannot see: URL, data, passwords
```

**Benefits:**

- ✅ **Encryption** - Data không thể đọc được
- ✅ **Authentication** - Verify server identity (not phishing)
- ✅ **Integrity** - Data không bị tamper
- ✅ **SEO** - Google ranks HTTPS higher
- ✅ **Trust** - Browsers show padlock icon
- ✅ **Modern APIs** - Service Workers, HTTP/2, geolocation require HTTPS

### 7.2. SSL/TLS Certificates

**Certificate = Digital passport for your website**

**Contains:**

- Domain name (example.com)
- Organization info
- Public key
- Valid from/to dates
- Issuer (Certificate Authority)

**Certificate Authorities (CAs):**

- Let's Encrypt (Free! ✅)
- DigiCert
- Cloudflare
- Sectigo

**Types:**

| Type | Validation | Cost | Use case |
|------|-----------|------|----------|
| **DV** (Domain Validated) | Domain control only | Free-$50 | Personal sites, blogs |
| **OV** (Organization Validated) | Domain + org verification | $50-200 | Business sites |
| **EV** (Extended Validation) | Strict verification | $200-1000 | Banks, e-commerce |

### 7.3. Let's Encrypt với Certbot

**Install Certbot:**

```bash
# Ubuntu/Debian
sudo apt install certbot python3-certbot-nginx -y
```

**Obtain certificate:**

```bash
# Auto-configure NGINX
sudo certbot --nginx -d example.com -d www.example.com

# Manual (nếu muốn config tự tay)
sudo certbot certonly --nginx -d example.com
```

**Flow:**

```
1. Certbot connects to Let's Encrypt servers
2. Proves you control domain (HTTP challenge)
3. Let's Encrypt issues certificate (3 months validity)
4. Certbot installs certificate
5. NGINX config updated automatically
```

**Certificate files created:**

```
/etc/letsencrypt/live/example.com/
├── cert.pem          # Certificate
├── chain.pem         # Intermediate certificates
├── fullchain.pem     # cert.pem + chain.pem
└── privkey.pem       # Private key (keep secret!)
```

**Auto-renewal:**

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot installs cron job automatically:
# /etc/cron.d/certbot
# Runs twice daily, renews if < 30 days left
```

### 7.4. HTTPS Configuration

**NGINX HTTPS config:**

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    
    # Redirect HTTP → HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;
    
    # SSL certificate files
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    # SSL settings (Mozilla modern config)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers off;
    
    # SSL session cache
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    location / {
        root /var/www/html;
        index index.html;
    }
}
```

**Test HTTPS:**

```bash
# Check certificate
openssl s_client -connect example.com:443 -showcerts

# Test с curl
curl -I https://example.com

# SSL Labs test (detailed security analysis)
# Visit: https://www.ssllabs.com/ssltest/
```

---

## 8. Performance Tuning

### 8.1. Gzip Compression

**Config:**

```nginx
http {
    # Enable gzip
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;  # 1-9, higher = more CPU, better compression
    
    # File types to compress
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        image/svg+xml;
    
    # Don't compress images (already compressed)
    gzip_disable "msie6";
}
```

**Test:**

```bash
curl -I -H "Accept-Encoding: gzip" https://example.com

# Should see:
# Content-Encoding: gzip
```

**Impact:**

```
Without gzip:
HTML: 50 KB
CSS: 30 KB
JS: 200 KB
Total: 280 KB

With gzip:
HTML: 10 KB (80% smaller)
CSS: 6 KB
JS: 60 KB
Total: 76 KB (73% savings!)
```

### 8.2. Caching

**Browser caching:**

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

location ~* \.(html)$ {
    expires 1h;
    add_header Cache-Control "public, must-revalidate";
}
```

**Proxy caching:**

```nginx
# Define cache path
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

server {
    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 60m;
        proxy_cache_valid 404 1m;
        
        # Cache key
        proxy_cache_key "$scheme$request_method$host$request_uri";
        
        # Headers
        add_header X-Cache-Status $upstream_cache_status;
        
        proxy_pass http://backend;
    }
}
```

**Cache status:**

- `HIT` - Served từ cache ✅
- `MISS` - Not cached, fetch từ backend
- `BYPASS` - Not cacheable (POST request, etc.)
- `EXPIRED` - Cache expired, revalidate

### 8.3. Worker Optimization

```nginx
# Auto-detect CPU cores
worker_processes auto;

# Max connections per worker
events {
    worker_connections 4096;  # Default: 1024
    use epoll;  # Linux: efficient event method
}

# File descriptor limits
worker_rlimit_nofile 8192;
```

**Calculate max connections:**

```
Max clients = worker_processes × worker_connections
For proxy: Max clients = (worker_processes × worker_connections) / 2
  (vì mỗi proxy connection dùng 2 file descriptors)

Example:
4 workers × 4096 connections = 16,384 concurrent clients
```

---

## 9. Troubleshooting

### 9.1. Check Configuration

```bash
# Test syntax
sudo nginx -t

# Common errors:
# - Missing semicolon
# - Unclosed bracket
# - Invalid directive
# - Wrong context
```

### 9.2. Check Logs

```bash
# Access log (all requests)
sudo tail -f /var/log/nginx/access.log

# Error log (problems only)
sudo tail -f /var/log/nginx/error.log

# Search errors
sudo grep "error" /var/log/nginx/error.log

# Custom log format
log_format detailed '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

access_log /var/log/nginx/access.log detailed;
```

### 9.3. Common Issues

**Issue: 502 Bad Gateway**

```
Cause: Backend không response hoặc down

Fix:
1. Check backend running:
   systemctl status backend-service

2. Check backend reachable:
   curl http://localhost:3000

3. Check NGINX error log:
   sudo tail /var/log/nginx/error.log
   # "connect() failed (111: Connection refused)"

4. Verify proxy_pass URL correct
```

**Issue: 504 Gateway Timeout**

```
Cause: Backend response quá chậm

Fix:
# Increase timeout
location / {
    proxy_pass http://backend;
    proxy_read_timeout 300s;
    proxy_connect_timeout 300s;
}
```

**Issue: 413 Request Entity Too Large**

```
Cause: Upload file quá lớn

Fix:
http {
    client_max_body_size 100M;
}
```

---

## 📚 Tổng kết

### Key Takeaways

1. **NGINX** - Fast, event-driven web server
2. **Reverse Proxy** - Frontend cho backend services
3. **Load Balancing** - Distribute traffic, high availability
4. **HTTPS** - Essential for security, SEO, trust
5. **Performance** - Gzip, caching, optimization
6. **Configuration** - Block-based, contexts, directives

### Checklist

- [ ] Install & configure NGINX
- [ ] Serve static website
- [ ] Setup reverse proxy đến backend
- [ ] Configure load balancing
- [ ] Enable HTTPS với Let's Encrypt
- [ ] Optimize với compression & caching
- [ ] Debug common issues
- [ ] Deploy landing page với NGINX + Docker

### Next: Module 08 - DEPLOYMENT_BASICS

👉 Deploy apps lên production servers!

---

> **"NGINX: The duct tape of the Internet." - DevOps Engineers** 🚀
