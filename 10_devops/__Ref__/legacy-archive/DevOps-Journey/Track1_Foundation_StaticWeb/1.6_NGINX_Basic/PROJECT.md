# 🎯 Project: NGINX Basic

> Mini project: **Production Web Server Setup**

---

## 📋 Project Overview

### Project Name: **NGINX Production Configuration**

Setup NGINX như production web server.

### Duration: 1-2 ngày

---

## 🎯 Requirements

### Features

1. **Static Website Hosting**
   - Serve HTML/CSS/JS files
   - Custom error pages (404, 500)
   - Directory indexing disabled

2. **Reverse Proxy**
   - Proxy to backend API
   - WebSocket support
   - Health check endpoint

3. **SSL/HTTPS**
   - Self-signed certificate
   - HTTP to HTTPS redirect
   - Security headers (HSTS, X-Frame-Options)

4. **Performance**
   - Gzip compression
   - Browser caching
   - Rate limiting

5. **Logging**
   - Custom log format
   - Separate access/error logs
   - Log rotation

---

## 📁 Project Structure

```
nginx-project/
├── nginx/
│   ├── nginx.conf
│   ├── sites-available/
│   │   └── mysite.conf
│   ├── ssl/
│   │   ├── cert.pem
│   │   └── key.pem
│   └── snippets/
│       ├── ssl-params.conf
│       └── proxy-params.conf
├── html/
│   ├── index.html
│   ├── 404.html
│   └── 50x.html
├── Dockerfile
└── docker-compose.yml
```

---

## 📊 Expected Configuration

```nginx
# Main features to implement:
server {
    listen 443 ssl http2;
    
    # SSL
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header Strict-Transport-Security "max-age=31536000";
    
    # Gzip
    gzip on;
    gzip_types text/plain application/json;
    
    # Static files
    location / {
        root /var/www/html;
        try_files $uri $uri/ =404;
    }
    
    # API proxy
    location /api/ {
        proxy_pass http://backend:3000/;
        include snippets/proxy-params.conf;
    }
    
    # Custom error pages
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
}
```

---

## ✅ Deliverables

- [ ] Complete nginx.conf
- [ ] SSL certificate generated
- [ ] All security headers
- [ ] Reverse proxy working
- [ ] Custom error pages
- [ ] Dockerized setup
- [ ] Documentation

---

**Good luck! 🚀**
