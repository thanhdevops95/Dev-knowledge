# Hướng dẫn NGINX

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

NGINX là web server và reverse proxy phổ biến, được sử dụng để:
- Serve static files
- Reverse proxy
- Load balancing
- SSL/TLS termination
- Caching

---

## 🔧**CÀI ĐẶT**

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install nginx

# Khởi động
sudo systemctl start nginx
sudo systemctl enable nginx

# Kiểm tra
sudo systemctl status nginx
curl http://localhost
```

### CentOS/RHEL

```bash
sudo yum install epel-release
sudo yum install nginx
```

### Docker

```bash
docker run -d -p 80:80 nginx
```

---

## 📁**CẤU TRÚC THƯ MỤC**

```
/etc/nginx/
├── nginx.conf           # Config chính
├── sites-available/     # Các site configs
├── sites-enabled/       # Symlinks đến sites-available
├── conf.d/              # Additional configs
├── snippets/            # Reusable snippets
└── mime.types           # MIME types

/var/www/html/           # Default web root
/var/log/nginx/          # Logs
```

---

## ⚙️**CẤU HÌNH CƠ BẢN**

### nginx.conf

```nginx
# /etc/nginx/nginx.conf
user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    # Basic settings
    sendfile on;
    tcp_nopush on;
    types_hash_max_size 2048;
    
    # MIME types
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    
    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    
    # Virtual hosts
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

---

## 🌐**STATIC WEBSITE**

### Site config

```nginx
# /etc/nginx/sites-available/mysite
server {
    listen 80;
    server_name example.com www.example.com;
    
    root /var/www/mysite;
    index index.html index.htm;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Cache static files
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Enable site

```bash
# Tạo symlink
sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Reload
sudo systemctl reload nginx
```

---

## 🔄**REVERSE PROXY**

### Proxy đến application

```nginx
server {
    listen 80;
    server_name api.example.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### WebSocket support

```nginx
location /ws {
    proxy_pass http://localhost:8080;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 86400;
}
```

---

## ⚖️**LOAD BALANCING**

### Round Robin (default)

```nginx
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend;
    }
}
```

### Weighted

```nginx
upstream backend {
    server 192.168.1.10:8080 weight=5;
    server 192.168.1.11:8080 weight=3;
    server 192.168.1.12:8080 weight=2;
}
```

### Least Connections

```nginx
upstream backend {
    least_conn;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}
```

### IP Hash (sticky sessions)

```nginx
upstream backend {
    ip_hash;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}
```

### Health checks

```nginx
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080 backup;  # Backup server
    server 192.168.1.12:8080 down;    # Tạm offline
}
```

---

## 🔐**SSL/HTTPS**

### Self-signed certificate (dev)

```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/server.key \
    -out /etc/nginx/ssl/server.crt
```

### Let's Encrypt (production)

```bash
# Cài Certbot
sudo apt install certbot python3-certbot-nginx

# Lấy certificate
sudo certbot --nginx -d example.com -d www.example.com

# Auto-renew
sudo certbot renew --dry-run
```

### SSL config

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000" always;
    
    root /var/www/mysite;
    index index.html;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 📊**LOCATION BLOCKS**

### Prefix match

```nginx
location /images/ {
    # Match: /images/photo.jpg, /images/icons/icon.png
}
```

### Exact match

```nginx
location = /favicon.ico {
    # Match only exact /favicon.ico
}
```

### Regex match

```nginx
location ~ \.php$ {
    # Case-sensitive regex: .php files
}

location ~* \.(jpg|jpeg|png)$ {
    # Case-insensitive regex: image files
}
```

### Priority

1. `=` (exact match)
2. `^~` (preferential prefix)
3. `~` và `~*` (regex)
4. Không có modifier (prefix)

---

## 🔧**CẤU HÌNH PHỔ BIẾN**

### PHP-FPM

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.php index.html;
    
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

### React/Vue SPA

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/app/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:3000;
    }
}
```

### Security headers

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'" always;
```

### Rate limiting

```nginx
http {
    limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;
    
    server {
        location /api/ {
            limit_req zone=mylimit burst=20 nodelay;
            proxy_pass http://backend;
        }
    }
}
```

### Gzip compression

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_proxied any;
gzip_comp_level 6;
gzip_types
    text/plain
    text/css
    text/xml
    application/json
    application/javascript
    application/xml+rss
    image/svg+xml;
```

---

## 📋**COMMANDS**

```bash
# Test config
sudo nginx -t

# Reload (không downtime)
sudo systemctl reload nginx

# Restart
sudo systemctl restart nginx

# Stop/Start
sudo systemctl stop nginx
sudo systemctl start nginx

# Xem logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
