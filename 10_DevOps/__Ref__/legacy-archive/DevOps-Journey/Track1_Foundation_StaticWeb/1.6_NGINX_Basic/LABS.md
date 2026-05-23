# 🔬 Labs: NGINX Basic

> **Hands-on Labs for NGINX Configuration**
>
> *Bài thực hành NGINX cơ bản.*

---

## 🔬 Lab 1: NGINX Installation

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx -y

# Start and enable
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx

# Test
curl http://localhost
```

---

## 🔬 Lab 2: Basic Configuration

```nginx
# /etc/nginx/sites-available/mysite
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
# Enable site
sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Reload
sudo systemctl reload nginx
```

---

## 🔬 Lab 3: Reverse Proxy

```nginx
server {
    listen 80;
    server_name api.example.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 🔬 Lab 4: Load Balancing

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

---

## 🔬 Lab 5: SSL/HTTPS

```nginx
server {
    listen 443 ssl;
    server_name secure.example.com;
    
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    
    location / {
        root /var/www/secure;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name secure.example.com;
    return 301 https://$server_name$request_uri;
}
```

---

## 🔬 Lab 6: NGINX with Docker

```dockerfile
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY html /usr/share/nginx/html
EXPOSE 80
```

```bash
docker build -t my-nginx .
docker run -d -p 8080:80 my-nginx
```

---

## ✅ Checklist

- [ ] Lab 1: Installation
- [ ] Lab 2: Basic Config
- [ ] Lab 3: Reverse Proxy
- [ ] Lab 4: Load Balancing
- [ ] Lab 5: SSL/HTTPS
- [ ] Lab 6: Docker

---

**[← Back to README](./README.md)**
