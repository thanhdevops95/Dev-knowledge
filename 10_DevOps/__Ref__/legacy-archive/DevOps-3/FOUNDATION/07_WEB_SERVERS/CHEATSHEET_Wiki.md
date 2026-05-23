# Web Servers - Cheatsheet

> **NGINX essentials for production deployment**

---

## 🌐 NGINX BASICS

### Installation & Service

```bash
# Install (Ubuntu/Debian)
sudo apt update
sudo apt install nginx

# Service management
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx         # No downtime
sudo systemctl status nginx
sudo systemctl enable nginx         # Auto-start on boot

# Test configuration
sudo nginx -t

# View version
nginx -v
nginx -V                            # With compile options
```

---

## 📁 FILE STRUCTURE

```
/etc/nginx/
├── nginx.conf                  # Main config
├── sites-available/            # All site configs
│   ├── default
│   └── mysite.conf
├── sites-enabled/              # Active sites (symlinks)
│   └── default -> ../sites-available/default
├── conf.d/                     # Additional configs
└── snippets/                   # Reusable config snippets
```

### Enable/Disable Sites

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/mysite.conf /etc/nginx/sites-enabled/

# Disable site
sudo rm /etc/nginx/sites-enabled/mysite.conf

# Always test after changes
sudo nginx -t
sudo systemctl reload nginx
```

---

## 📝 BASIC CONFIGURATION

### Static Website

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    
    root /var/www/mysite;
    index index.html index.htm;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Reverse Proxy

```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Static Files + Proxy

```nginx
server {
    listen 80;
    server_name example.com;
    
    # Serve static files directly
    location /static {
        alias /var/www/myapp/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Proxy dynamic requests
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
    }
}
```

---

## 🔄 LOAD BALANCING

### Upstream Block

```nginx
upstream backend {
    least_conn;                      # Algorithm
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
    }
}
```

### Load Balancing Methods

```nginx
# Round robin (default)
upstream backend {
    server app1:5000;
    server app2:5000;
}

# Least connections
upstream backend {
    least_conn;
    server app1:5000;
    server app2:5000;
}

# IP hash (sticky sessions)
upstream backend {
    ip_hash;
    server app1:5000;
    server app2:5000;
}

# Weighted
upstream backend {
    server app1:5000 weight=3;      # Gets 3x traffic
    server app2:5000 weight=1;
}
```

---

## 🔐 SSL/TLS (HTTPS)

### Let's Encrypt (Free SSL)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate (auto-configures NGINX)
sudo certbot --nginx -d example.com -d www.example.com

# Renew (automatic via cron)
sudo certbot renew --dry-run

# List certificates
sudo certbot certificates
```

### Manual SSL Configuration

```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
```

---

## 🛡️ SECURITY HEADERS

```nginx
server {
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self'" always;
    
    # HSTS (HTTPS only)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

---

## 🚀 PERFORMANCE OPTIMIZATION

### Gzip Compression

```nginx
# In nginx.conf or server block
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript 
           application/x-javascript application/xml+rss 
           application/json application/javascript;
```

### Browser Caching

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

location /static {
    expires 30d;
    add_header Cache-Control "public";
}
```

### Client Body Size

```nginx
# Increase upload limit
client_max_body_size 50M;
```

### Timeouts

```nginx
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;
```

---

## 📋 COMMON LOCATIONS

```nginx
# Exact match
location = /favicon.ico {
    access_log off;
    log_not_found off;
}

# Prefix match
location /admin {
    # Matches /admin, /admin/page, etc.
}

# Regex match (case-sensitive)
location ~ \.php$ {
    # PHP files
}

# Regex match (case-insensitive)
location ~* \.(gif|jpg|jpeg|png)$ {
    # Image files
}

# Priority order:
# 1. Exact match (=)
# 2. Prefix match (^~)
# 3. Regex (~, ~*)
# 4. Standard prefix
```

---

## 📊 LOGGING

### Access & Error Logs

```nginx
# In server block
access_log /var/log/nginx/mysite_access.log;
error_log /var/log/nginx/mysite_error.log;

# Disable access log
access_log off;

# Custom log format
log_format main '$remote_addr - $remote_user [$time_local] '
                '"$request" $status $body_bytes_sent '
                '"$http_referer" "$http_user_agent"';
access_log /var/log/nginx/access.log main;
```

### View Logs

```bash
# Real-time access log
sudo tail -f /var/log/nginx/access.log

# Real-time error log
sudo tail -f /var/log/nginx/error.log

# Last 100 lines
sudo tail -100 /var/log/nginx/access.log

# Search for errors
sudo grep "error" /var/log/nginx/error.log
```

---

## 🔧 COMMON TASKS

### Redirect HTTP to HTTPS

```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### Redirect www to non-www

```nginx
server {
    listen 80;
    server_name www.example.com;
    return 301 http://example.com$request_uri;
}
```

### Basic Auth

```bash
# Create password file
sudo htpasswd -c /etc/nginx/.htpasswd username
```

```nginx
location /admin {
    auth_basic "Restricted";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```

### Rate Limiting

```nginx
# Define rate limit zone
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;

server {
    location /api {
        limit_req zone=mylimit burst=20;
        proxy_pass http://backend;
    }
}
```

---

## 🐛 DEBUGGING

### Test Configuration

```bash
# Test syntax
sudo nginx -t

# Test and show config
sudo nginx -T

# Check what's using port 80
sudo netstat -tulpn | grep :80
sudo lsof -i :80
```

### Common Errors

**502 Bad Gateway:**

```
- Backend app not running
- Wrong proxy_pass address
- Firewall blocking connection
```

**403 Forbidden:**

```
- File permissions wrong
- SELinux blocking (if enabled)
- Index file missing
```

**404 Not Found:**

```
- Wrong root directory
- File doesn't exist
- Location block not matching
```

---

## 📝 PRODUCTION CONFIG

```nginx
# /etc/nginx/sites-available/myapp
upstream app_servers {
    least_conn;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;
    
    # SSL
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";
    
    # Logging
    access_log /var/log/nginx/myapp_access.log;
    error_log /var/log/nginx/myapp_error.log;
    
    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    
    # Static files
    location /static {
        alias /var/www/myapp/static;
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

<div align="center">

**NGINX = Production gateway! 🌐⚡**

**Master it for reliable deployments! 💪**

</div>
