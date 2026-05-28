# Solutions: Module 07 - WEB SERVERS

> **Đáp Án NGINX Complete**

---

## EXERCISES SOLUTIONS

### Phần A: Trắc Nghiệm

1. **A** - Web server và reverse proxy
2. **C** - Port 80 cho HTTP
3. **B** - nginx -t test syntax
4. **A** - systemctl reload nginx
5. **C** - proxy_pass directive
6. **B** - upstream {} block
7. **A** - certbot (Let's Encrypt)
8. **C** - gzip on
9. **B** - limit_req zone
10. **A** - add_header

### Phần B: Thực Hành

**Câu 11: Install NGINX**

```bash
sudo apt update
sudo apt install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
curl http://localhost
```

**Câu 12: Virtual Host**

```nginx
server {
    listen 80;
    server_name mysite.com;
    
    root /var/www/mysite;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

**Câu 13: Reverse Proxy**

```nginx
server {
    listen 80;
    server_name api.mysite.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**Câu 14: Load Balancer**

```nginx
upstream backend {
    least_conn;
    server 127.0.0.1:5001 weight=3;
    server 127.0.0.1:5002 weight=2;
    server 127.0.0.1:5003 backup;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

**Câu 15: SSL với Let's Encrypt**

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d mysite.com -d www.mysite.com
sudo certbot renew --dry-run
```

**Câu 16: Security Headers**

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000" always;
```

**Câu 17: Gzip Compression**

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1000;
gzip_types text/plain text/css application/json application/javascript;
```

**Câu 18: Troubleshoot 502**

```bash
# 1. Check backend running
sudo systemctl status myapp

# 2. Check backend port
curl http://localhost:5000

# 3. Check NGINX logs
sudo tail -f /var/log/nginx/error.log

# 4. Fix: Start backend
sudo systemctl start myapp
```

---

## SCENARIOS SOLUTIONS

| Scenario | Solution |
|----------|----------|
| 502 Bad Gateway | Start backend service |
| SSL errors | certbot renew |
| Config syntax error | nginx -t shows line |
| Port conflict | lsof -i :80 |
| Load balance fail | Fix upstream syntax |

---

## KEY CONFIGURATIONS

**Complete Production Config:**

```nginx
upstream backend {
    least_conn;
    server localhost:5000;
}

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
    
    # Security
    add_header X-Frame-Options "SAMEORIGIN" always;
    
    # Compression
    gzip on;
    gzip_types text/plain text/css application/json;
    
    location /static/ {
        alias /var/www/static/;
        expires 1y;
    }
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

**Master NGINX = Master web infrastructure! 🌐**
