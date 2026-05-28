# 📋 NGINX - Cheatsheet

> **Quick Reference for NGINX Configuration**
>
> *Tra cứu nhanh cấu hình NGINX*

---

## 🔧 Basic Commands (Lệnh cơ bản)

```bash
nginx -t              # Test configuration (Kiểm tra cấu hình)
nginx -s reload       # Reload configuration (Tải lại cấu hình)
nginx -s stop         # Stop NGINX (Dừng NGINX)
nginx -s quit         # Graceful stop (Dừng an toàn)
systemctl status nginx  # Check status (Kiểm tra trạng thái)
```

---

## 📝 Basic Server Block

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/html;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

---

## 🔄 Reverse Proxy

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## ⚖️ Load Balancing

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

## 📁 Common Locations (Vị trí phổ biến)

| Path | Description (Mô tả) |
|------|---------------------|
| `/etc/nginx/nginx.conf` | Main config (File cấu hình chính) |
| `/etc/nginx/sites-available/` | Available sites (Sites có sẵn) |
| `/etc/nginx/sites-enabled/` | Enabled sites (Sites đang bật) |
| `/var/log/nginx/access.log` | Access log |
| `/var/log/nginx/error.log` | Error log |
| `/var/www/html/` | Default web root |

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
