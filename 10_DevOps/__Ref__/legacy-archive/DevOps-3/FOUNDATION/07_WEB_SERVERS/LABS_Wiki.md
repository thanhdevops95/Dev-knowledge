# Labs: Module 07 - WEB SERVERS

> **Thực hành NGINX Production**

---

## 🎯 OBJECTIVES

- ✅ Install và configure NGINX
- ✅ Serve static files
- ✅ Setup reverse proxy
- ✅ Load balancing
- ✅ SSL với Let's Encrypt
- ✅ Security headers

---

## 📊 LABS

| Lab | Topic | Time |
|-----|-------|------|
| 01 | Installation | 10 min |
| 02 | Static Hosting | 15 min |
| 03 | Reverse Proxy | 20 min |
| 04 | Load Balancing | 25 min |
| 05 | SSL/TLS | 20 min |
| 06 | Security Headers | 15 min |
| 07 | Gzip Compression | 10 min |
| 08 | Rate Limiting | 15 min |
| 09 | Logging | 10 min |
| 10 | Production Config | 25 min |

---

## LAB 01: Installation

```bash
sudo apt update
sudo apt install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
curl http://localhost
```

---

## LAB 02: Static Hosting

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

---

## LAB 03: Reverse Proxy

```nginx
server {
    listen 80;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## LAB 04: Load Balancing

```nginx
upstream backend {
    least_conn;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

---

## LAB 05: SSL với Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com
sudo certbot renew --dry-run
```

---

## LAB 06-10: [Continues...]

---

**Tiếp: EXERCISES.md**
