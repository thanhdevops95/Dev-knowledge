# 🔌 Nginx & Reverse Proxy — Web Server Production

> `[INTERMEDIATE]` — Phục vụ web, proxy, load balancing, SSL

---

## 1. Nginx là gì?

```
Client ──► Nginx (Reverse Proxy) ──► App Server (Node.js, Python...)
                    │
                    ├── Serve static files (HTML, CSS, JS, images)
                    ├── SSL termination (HTTPS)
                    ├── Load balancing (multiple backends)
                    ├── Compression (gzip/brotli)
                    ├── Rate limiting
                    └── Caching
```

---

## 2. Cấu hình cơ bản

```nginx
# /etc/nginx/sites-available/myapp.conf

# Upstream: danh sách backend servers
upstream app_servers {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
}

# HTTP → redirect HTTPS
server {
    listen 80;
    server_name myapp.com www.myapp.com;
    return 301 https://$host$request_uri;
}

# HTTPS
server {
    listen 443 ssl http2;
    server_name myapp.com www.myapp.com;

    # SSL
    ssl_certificate /etc/letsencrypt/live/myapp.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myapp.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript
               text/xml application/xml text/javascript image/svg+xml;

    # Static files
    location /static/ {
        alias /var/www/myapp/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # API → proxy to backend
    location /api/ {
        proxy_pass http://app_servers;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 5s;
        proxy_read_timeout 30s;
        proxy_send_timeout 30s;
    }

    # WebSocket
    location /ws/ {
        proxy_pass http://app_servers;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # SPA: fallback → index.html
    location / {
        root /var/www/myapp/dist;
        try_files $uri $uri/ /index.html;
    }

    # Block hidden files
    location ~ /\. {
        deny all;
    }
}
```

---

## 3. Load Balancing

```nginx
# Round Robin (default)
upstream backend {
    server 10.0.1.10:3000;
    server 10.0.1.11:3000;
    server 10.0.1.12:3000;
}

# Weighted
upstream backend {
    server 10.0.1.10:3000 weight=5;   # 5x traffic
    server 10.0.1.11:3000 weight=3;   # 3x traffic
    server 10.0.1.12:3000 weight=1;   # 1x traffic
}

# Least connections
upstream backend {
    least_conn;
    server 10.0.1.10:3000;
    server 10.0.1.11:3000;
}

# IP Hash (sticky sessions)
upstream backend {
    ip_hash;
    server 10.0.1.10:3000;
    server 10.0.1.11:3000;
}

# Health checks
upstream backend {
    server 10.0.1.10:3000 max_fails=3 fail_timeout=30s;
    server 10.0.1.11:3000 max_fails=3 fail_timeout=30s;
    server 10.0.1.12:3000 backup;     # Chỉ dùng khi servers khác chết
}
```

---

## 4. Rate Limiting

```nginx
# Định nghĩa zone: 10 requests/giây per IP
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;

server {
    # API: 10 req/s, burst 20 (queue thêm 20 requests)
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://app_servers;
    }

    # Login: 1 req/s, burst 5 (chống brute force)
    location /api/auth/login {
        limit_req zone=login burst=5;
        proxy_pass http://app_servers;
    }
}
```

---

## 5. Caching

```nginx
# Proxy cache
proxy_cache_path /tmp/nginx_cache levels=1:2 keys_zone=my_cache:10m
                 max_size=1g inactive=60m use_temp_path=off;

server {
    location /api/products {
        proxy_cache my_cache;
        proxy_cache_valid 200 10m;       # Cache 200 responses 10 phút
        proxy_cache_valid 404 1m;        # Cache 404 1 phút
        proxy_cache_key "$scheme$request_method$host$request_uri";
        add_header X-Cache-Status $upstream_cache_status;
        proxy_pass http://app_servers;
    }

    # Bypass cache khi cần
    location /api/users/me {
        proxy_cache off;                  # Không cache user-specific data!
        proxy_pass http://app_servers;
    }
}
```

---

## 6. SSL với Let's Encrypt

```bash
# Cài Certbot
sudo apt install certbot python3-certbot-nginx

# Lấy certificate (tự động config Nginx!)
sudo certbot --nginx -d myapp.com -d www.myapp.com

# Auto-renew (certbot tự thêm cron job)
sudo certbot renew --dry-run

# Kiểm tra SSL
curl -I https://myapp.com
# Strict-Transport-Security: max-age=31536000
```

---

## 7. Useful Commands

```bash
# Test config syntax
sudo nginx -t

# Reload config (không downtime!)
sudo nginx -s reload

# View logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Check status
sudo systemctl status nginx
```

---

## Nginx vs Caddy

| | Nginx | Caddy |
|---|---|---|
| **Config** | Phức tạp, nhiều options | Đơn giản, Caddyfile |
| **Auto HTTPS** | Cần Certbot | Tự động! |
| **Performance** | Nhanh nhất | Nhanh (Go) |
| **Modules** | C modules | Go plugins |
| **Khi nào** | Production, custom needs | Simple projects, dev |

```
# Caddyfile tương đương (đơn giản hơn nhiều!)
myapp.com {
    reverse_proxy localhost:3000
    encode gzip
    file_server /static/* {
        root /var/www/myapp
    }
}
# HTTPS tự động, không cần config SSL!
```

---

## Bài tập thực hành

- [ ] Reverse proxy: Nginx → Node.js app
- [ ] SSL: Let's Encrypt cho domain
- [ ] Load balancing: 3 backend instances
- [ ] Rate limiting: API + login endpoint

---

## Tài nguyên thêm

- [Nginx Docs](https://nginx.org/en/docs/) — Official
- [Nginx Config Generator](https://www.digitalocean.com/community/tools/nginx) — DigitalOcean
- [Caddy Docs](https://caddyserver.com/docs/) — Alternative
