# ✅ Solutions: NGINX Basic

> **Solutions for Exercises. Try to solve it yourself first!**
>
> *Đáp án cho Exercises. Hãy thử tự giải trước!*

---

## Exercise 1: Static Site

```bash
# 1. Install NGINX
sudo apt update && sudo apt install nginx -y

# 2. Create site directory
sudo mkdir -p /var/www/mysite
sudo chown -R $USER:$USER /var/www/mysite

# Create HTML page
cat << 'EOF' > /var/www/mysite/index.html
<!DOCTYPE html>
<html>
<head><title>My Site</title></head>
<body><h1>Welcome to My Site!</h1></body>
</html>
EOF
```

```nginx
# 3. /etc/nginx/sites-available/mysite
server {
    listen 80;
    server_name mysite.local;
    
    root /var/www/mysite;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

```bash
# 4. Enable and reload
sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 5. Test
curl http://localhost
```

---

## Exercise 2: Virtual Hosts

```nginx
# /etc/nginx/sites-available/site1
server {
    listen 80;
    server_name site1.local;
    root /var/www/site1;
    index index.html;
}

# /etc/nginx/sites-available/site2
server {
    listen 80;
    server_name site2.local;
    root /var/www/site2;
    index index.html;
}
```

```bash
# Create directories and files
sudo mkdir -p /var/www/site{1,2}
echo "<h1>Site 1</h1>" | sudo tee /var/www/site1/index.html
echo "<h1>Site 2</h1>" | sudo tee /var/www/site2/index.html

# Enable sites
sudo ln -s /etc/nginx/sites-available/site1 /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/site2 /etc/nginx/sites-enabled/
sudo systemctl reload nginx

# Add to /etc/hosts
echo "127.0.0.1 site1.local site2.local" | sudo tee -a /etc/hosts

# Test
curl http://site1.local
curl http://site2.local
```

---

## Exercise 3: Reverse Proxy

```nginx
# /etc/nginx/sites-available/api-proxy
server {
    listen 80;
    server_name api.local;
    
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

---

## Exercise 4: Load Balancing

```nginx
upstream backend {
    # Round-robin (default)
    server localhost:3001;
    server localhost:3002;
    server localhost:3003;
    
    # Or weighted:
    # server localhost:3001 weight=3;
    # server localhost:3002 weight=2;
    # server localhost:3003 weight=1;
    
    # Health check
    keepalive 32;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend;
        proxy_next_upstream error timeout http_500;
    }
    
    location /health {
        access_log off;
        return 200 "healthy";
    }
}
```

---

## Exercise 5: SSL/HTTPS

```bash
# 1. Generate self-signed certificate
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/server.key \
    -out /etc/nginx/ssl/server.crt \
    -subj "/C=US/ST=State/L=City/O=Org/CN=localhost"
```

```nginx
# 2-4. HTTPS configuration
server {
    listen 80;
    server_name localhost;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name localhost;
    
    # SSL
    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;
    
    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    root /var/www/html;
    index index.html;
}
```

---

## Exercise 6: Caching & Optimization

```nginx
# Gzip
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_proxied any;
gzip_comp_level 6;
gzip_types
    text/plain
    text/css
    text/xml
    text/javascript
    application/json
    application/javascript
    application/xml
    application/rss+xml
    image/svg+xml;

# Browser caching
location ~* \.(jpg|jpeg|png|gif|ico|css|js|pdf|woff2)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}

# Connection settings
keepalive_timeout 65;
keepalive_requests 100;

# Buffers
client_body_buffer_size 16k;
client_max_body_size 10m;
```

---

**[← Back to Exercises](./EXERCISES.md)** | **[Back to README →](./README.md)**
