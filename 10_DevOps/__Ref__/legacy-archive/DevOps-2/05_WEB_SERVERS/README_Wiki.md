# Module 05: Web Servers (Nginx)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Web Server** | - | Phần mềm nhận HTTP requests và trả về responses |
| **Nginx** | /ˈɛndʒɪnˌeks/ | Web server phổ biến nhất, kiêm reverse proxy |
| **Apache** | - | Web server truyền thống, flexible nhưng chậm hơn |
| **Reverse Proxy** | - | Proxy ngược - Đứng trước backend servers |
| **Load Balancer** | - | Cân bằng tải - Phân phối traffic đến nhiều servers |
| **Upstream** | - | Nhóm backend servers trong Nginx config |
| **Virtual Host** | - | Chạy nhiều websites trên một server |
| **HTTPS** | - | HTTP + SSL/TLS - Giao thức web mã hóa |
| **SSL Termination** | - | Nginx xử lý SSL, forward HTTP đến backend |
| **Static Files** | - | Files không thay đổi (HTML, CSS, JS, images) |
| **Port** | - | Cổng mạng (80 = HTTP, 443 = HTTPS) |
| **Location** | - | Block config cho URL pattern trong Nginx |
| **Certbot** | - | Tool tự động lấy SSL certificate từ Let's Encrypt |

---

## 📖 Web Server là gì? (Định nghĩa từ gốc)

### Trước hết: HTTP Request/Response là gì?

Khi bạn mở browser và gõ `google.com`:

1. **Browser gửi HTTP Request** → "Cho tôi trang chủ Google"
2. **Server nhận request, xử lý**
3. **Server trả HTTP Response** → HTML của trang chủ
4. **Browser render HTML** → Bạn thấy trang web

```
Bạn (Browser)              Server
    │                        │
    │── GET / ─────────────►│  "Cho tôi trang chủ"
    │                        │
    │◄── 200 OK + HTML ──────│  "Đây, trang chủ của bạn"
    │                        │
```

### Web Server = Phần mềm xử lý HTTP

> **Web Server = Chương trình lắng nghe HTTP requests và trả về responses**

Cụ thể, web server:

- **Lắng nghe** trên port (80 cho HTTP, 443 cho HTTPS)
- **Nhận** HTTP request từ client
- **Xử lý** request (serve file, forward đến app, etc.)
- **Trả về** HTTP response

### Tại sao không dùng App Server trực tiếp?

Khi bạn chạy `npm start` hoặc `python app.py`, app có **built-in server**. Tại sao cần thêm Web Server?

| App's Built-in Server | Web Server (Nginx) |
|----------------------|-------------------|
| Xử lý 1-10 requests đồng thời | Xử lý 10,000+ requests đồng thời |
| Không có HTTPS | HTTPS với SSL/TLS |
| Không có caching | Cache static files |
| Không có load balancing | Phân tải nhiều servers |
| Crash = phải restart thủ công | Tự động recovery |
| Chỉ serve app | Serve static files + proxy app |

**Ẩn dụ:**

```
App Server = Đầu bếp trong nhà
             Nấu được, nhưng phục vụ 1-2 người

Web Server = Nhà hàng chuyên nghiệp
             Reception, phục vụ, bếp chuyên biệt
             Phục vụ hàng trăm khách
```

---

## 🎬 Câu chuyện thực tế

Bạn viết xong một web app tuyệt đẹp. Chạy `npm start` hoặc `python app.py`, mở browser thấy website hoạt động.

Nhưng đây chỉ là **development server**. Nó:

- Chậm dưới load cao
- Không có HTTPS (không bảo mật)
- Crash khi có 100+ users cùng lúc
- Không serve static files hiệu quả

Để chạy **production**, bạn cần một **Web Server** thực thụ như **Nginx** hoặc **Apache**.

---

## 🌐 Nginx - Web Server phổ biến nhất

```
Browser          Web Server              App
   │                 │                    │
   │── GET /api ────►│                    │
   │                 │── Forward ────────►│
   │                 │◄── Response ───────│
   │◄─── HTML/JSON ──│                    │
```

### Tại sao cần Web Server?

| Development Server | Web Server (Nginx) |
|-------------------|-------------------|
| 1 request/time | 10,000+ concurrent |
| HTTP only | HTTPS với SSL |
| Crash = manual restart | Auto-restart |
| No caching | Static file caching |
| No load balancing | Multiple backends |

---

## 🌐 Nginx - Web Server phổ biến nhất

### Tại sao Nginx?

```
Apache vs Nginx market share:
├── Nginx: 34%+ (đang tăng)
├── Apache: 31%
└── Others: 35%

Netflix, Cloudflare, GitHub dùng Nginx.
```

### Nginx làm được gì?

1. **Static file server** - Serve HTML, CSS, JS, images
2. **Reverse proxy** - Route requests đến backend apps
3. **Load balancer** - Chia traffic cho nhiều servers
4. **SSL termination** - Handle HTTPS
5. **Caching** - Cache responses

---

## 🏗️ Cấu trúc Nginx

### Hierarchy

```
nginx.conf
├── http { }
│   ├── server { }      ← Virtual host 1 (domain 1)
│   │   ├── listen 80
│   │   ├── server_name example.com
│   │   └── location / { }
│   │
│   └── server { }      ← Virtual host 2 (domain 2)
│       ├── listen 80
│       ├── server_name api.example.com
│       └── location / { }
│
└── events { }
```

### Config file locations

```bash
/etc/nginx/
├── nginx.conf              # Main config
├── sites-available/        # Available sites
│   ├── default
│   └── myapp.conf
├── sites-enabled/          # Enabled sites (symlinks)
│   └── myapp.conf -> ../sites-available/myapp.conf
├── conf.d/                 # Additional configs
└── mime.types              # MIME type mappings
```

---

## 📄 Static File Server

### Config cơ bản

```nginx
# /etc/nginx/sites-available/mysite
server {
    listen 80;
    server_name example.com;
    
    # Root directory cho static files
    root /var/www/mysite;
    index index.html;
    
    # Serve static files
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Optimize static file serving
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Giải thích

- `listen 80` - Lắng nghe port 80 (HTTP)
- `server_name` - Domain name
- `root` - Thư mục chứa files
- `try_files` - Thử serve file, nếu không có → 404
- `expires` - Browser cache 30 ngày

---

## 🔄 Reverse Proxy

### Khi nào cần?

Khi bạn có app chạy trên port 3000 (Node), 8000 (Python), cần:

- Users truy cập qua port 80/443
- HTTPS
- Load balancing

```
User → Nginx (80/443) → App (3000)
```

### Config Reverse Proxy

```nginx
server {
    listen 80;
    server_name api.example.com;
    
    location / {
        proxy_pass http://localhost:3000;
        
        # Forward headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### Giải thích headers

| Header | Mục đích |
|--------|----------|
| `Host` | Domain gốc của request |
| `X-Real-IP` | IP thật của client |
| `X-Forwarded-For` | Chain of IPs (nếu qua nhiều proxies) |
| `X-Forwarded-Proto` | HTTP hay HTTPS |

---

## ⚖️ Load Balancing

### Khi app cần scale

```
                    ┌─→ App Server 1 (3000)
User → Nginx ──────┼─→ App Server 2 (3001)
                    └─→ App Server 3 (3002)
```

### Config Load Balancer

```nginx
# Define upstream (backend servers)
upstream myapp {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
}

server {
    listen 80;
    server_name app.example.com;
    
    location / {
        proxy_pass http://myapp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Load balancing methods

```nginx
upstream myapp {
    # Round Robin (default)
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    
    # Least connections
    least_conn;
    
    # IP Hash (sticky sessions)
    ip_hash;
    
    # Weighted
    server 127.0.0.1:3000 weight=3;
    server 127.0.0.1:3001 weight=1;
    
    # Backup server
    server 127.0.0.1:3002 backup;
}
```

---

## 🔐 HTTPS với SSL/TLS

### Tại sao cần HTTPS?

- **Encryption** - Dữ liệu được mã hóa
- **Authentication** - Chứng minh bạn là bạn
- **SEO** - Google ranking cao hơn
- **Browser trust** - Không bị cảnh báo "Not Secure"

### Free SSL với Let's Encrypt

```bash
# Cài Certbot
sudo apt install certbot python3-certbot-nginx

# Lấy certificate (tự động config Nginx)
sudo certbot --nginx -d example.com -d www.example.com

# Certificate được lưu ở:
# /etc/letsencrypt/live/example.com/fullchain.pem
# /etc/letsencrypt/live/example.com/privkey.pem
```

### Config HTTPS thủ công

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # SSL certificates
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

## 🛠️ Commands thường dùng

```bash
# Test config syntax
sudo nginx -t

# Reload config (không downtime)
sudo systemctl reload nginx

# Restart nginx
sudo systemctl restart nginx

# Xem status
sudo systemctl status nginx

# Xem logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## 📝 Tổng kết Module 05

### Bạn đã học

✅ Web server là gì và tại sao cần  
✅ Nginx config structure  
✅ Static file serving  
✅ Reverse proxy  
✅ Load balancing  
✅ SSL/HTTPS setup  

---

## ⏭️ Tiếp theo

👉 **[LABS.md - Thực hành Nginx](LABS.md)**
