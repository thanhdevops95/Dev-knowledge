# 🌐 Module 1.6: NGINX Basic

[![Duration](https://img.shields.io/badge/Duration-6--8%20hours-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Beginner-green?style=flat-square)](.)

> **Web Server and Reverse Proxy** - Serve static content and route traffic.
>
> *Web Server và Reverse Proxy - Serve nội dung tĩnh và điều hướng traffic.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Understand what NGINX is and its use cases (Hiểu NGINX là gì và use cases)
- ✅ Configure NGINX to serve static files (Cấu hình NGINX serve static files)
- ✅ Understand NGINX config file structure (Hiểu cấu trúc file config)
- ✅ Configure virtual hosts - server blocks (Cấu hình virtual hosts)
- ✅ Understand Reverse Proxy concept (Hiểu khái niệm Reverse Proxy)
- ✅ Deploy NGINX with Docker (Deploy NGINX với Docker)

---

## 📚 Content (Nội dung)

### 1. What is NGINX? (NGINX là gì?) - 30 min

#### 1.1 Introduction (Giới thiệu)

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> You've built a beautiful website. Now users need to access it. But your Node.js/Python app can only handle 100 concurrent connections and crashes under load. How do major websites serve millions of users?
>
> *Bạn đã xây dựng một website đẹp. Giờ người dùng cần truy cập. Nhưng app Node.js/Python của bạn chỉ xử lý được 100 kết nối đồng thời và crash khi quá tải. Làm sao các website lớn phục vụ hàng triệu người dùng?*
>
> **NGINX sits in front:** It handles 10,000+ concurrent connections, serves static files lightning-fast, and distributes traffic to multiple backend servers. That's why Netflix, Dropbox, and Airbnb all use NGINX!
>
> *NGINX đứng trước: Nó xử lý 10,000+ kết nối đồng thời, serve file tĩnh cực nhanh, và phân phối traffic đến nhiều backend servers. Đó là lý do Netflix, Dropbox, Airbnb đều dùng NGINX!*

**NGINX** (pronounced "engine-x") is a high-performance HTTP web server, reverse proxy, content cache, load balancer, TCP/UDP proxy server, and mail proxy server.

*NGINX (đọc là "engine-x") là một HTTP web server hiệu năng cao, kiêm reverse proxy, content cache, cân bằng tải, TCP/UDP proxy server, và mail proxy server.*

**Key capabilities (Các tính năng chính):**

- 🌐 **Web Server**: Serve static files (HTML, CSS, JS, images) with high concurrency (Phục vụ file tĩnh với khả năng xử lý đồng thời cao).
- 🔄 **Reverse Proxy**: Route requests to application backends (Node.js, Python, Go...) (Điều hướng requests tới backend ứng dụng).
- ⚖️ **Load Balancer**: Distribute traffic efficiently across multiple servers (Phân phối tải hiệu quả giữa các server).
- 📦 **Cache**: Improve performance by caching responses (Tăng tốc độ bằng cách lưu đệm phản hồi).

#### 1.2 NGINX vs Apache

| Criteria | NGINX | Apache |
|----------|-------|--------|
| **Architecture** | Event-driven, async (Hướng sự kiện, bất đồng bộ) | Process/Thread per request (Process/Thread mỗi request) |
| **Static content** | ✅ Very fast (Rất nhanh) | Slower (Chậm hơn) |
| **Memory** | ✅ Low RAM (Tốn ít RAM) | More RAM (Tốn nhiều RAM) |
| **Concurrent connections** | ✅ High (10k+) (Cao, 10k+) | Limited (Hạn chế) |
| **Config** | Simpler (Đơn giản hơn) | .htaccess flexible (Linh hoạt với .htaccess) |
| **Modules** | Compile time (Khi biên dịch) | Runtime (Khi chạy) |

#### 1.3 Common Use Cases (Use cases phổ biến)

```ini
┌─────────────────────────────────────────────────────────────┐
│                    NGINX USE CASES                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. STATIC WEB SERVER                                        │
│     Browser → NGINX → HTML/CSS/JS/Images                    │
│                                                              │
│  2. REVERSE PROXY                                            │
│     Browser → NGINX → Backend (Node.js, Python, etc.)       │
│                                                              │
│  3. LOAD BALANCER                                            │
│     Browser → NGINX → Server1, Server2, Server3...          │
│                                                              │
│  4. SSL TERMINATION                                          │
│     Browser ─HTTPS→ NGINX ─HTTP→ Backend                    │
│                                                              │
│  5. API GATEWAY                                              │
│     Browser → NGINX → /api → API Server                     │
│                      → /    → Frontend Server               │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

---

### 2. Installing and Running NGINX (Cài đặt và Chạy NGINX) - 1 hour

#### 2.1 Run with Docker - Recommended (Chạy với Docker - Khuyến nghị)

We will use **Docker** to run NGINX. This avoids installing software directly on your machine and allows you to easily switch versions or configurations.

*Chúng ta sẽ sử dụng **Docker** để chạy NGINX. Việc này tránh cài đặt phần mềm trực tiếp lên máy và cho phép bạn dễ dàng thay đổi phiên bản hoặc cấu hình.*

**Run the following command (Chạy lệnh sau):**

```bash
docker run -d -p 80:80 --name nginx nginx:alpine
```

**Command Explanation (Giải thích lệnh):**

- `docker run`: The command to create and start a new container (Lệnh tạo và chạy container mới).
- `-d` (Detached): Runs the container in the background (Chạy ngầm).
- `-p 80:80`: Maps port 80 of the host (laptop) to port 80 of the container (Ánh xạ cổng 80 của máy sang cổng 80 của container).
- `--name nginx`: Assigns the name "nginx" to the container for easy reference (Đặt tên container là "nginx" để dễ quản lý).
- `nginx:alpine`: Uses the lightweight Alpine Linux version of the NGINX image (Dùng bản NGINX siêu nhẹ trên nền Alpine Linux).

**Verify the setup (Kiểm tra cài đặt):**

```bash
curl http://localhost
# Or open browser (Hoặc mở browser): http://localhost
```

**You should see:** "Welcome to nginx!" HTML page.

**Manage the container (Quản lý container):**

```bash
docker logs nginx       # View server logs (Xem logs của server)
docker exec -it nginx sh # Enter the container shell (Vào trong container)
docker stop nginx       # Stop the server (Dừng server)
docker rm nginx         # Remove the container (Xóa container)
```

#### 2.2 Install Directly - Optional (Cài đặt trực tiếp - Tùy chọn)

- For Ubuntu/Debian (Cho Ubuntu/Debian):

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Check status (Kiểm tra status)
sudo systemctl status nginx

- For macOS with Homebrew (Cho macOS với Homebrew):
brew install nginx
brew services start nginx

```

#### 2.3 Verify Installation (Kiểm tra cài đặt)

- Run the following commands to verify (Chạy các lệnh sau để kiểm tra)

```bash
# Check version (Kiểm tra version)
nginx -v

# Check config syntax (Kiểm tra cú pháp config)
nginx -t

# View current config (Xem config đang dùng)
nginx -T

```

---

### 3. NGINX Directory Structure (Cấu trúc thư mục NGINX) - 30 min

#### 3.1 Important Directories (Thư mục quan trọng)

```ini
/etc/nginx/                    # Config directory (Thư mục cấu hình)
├── nginx.conf                 # Main config file (File config chính)
├── conf.d/                    # Additional configs (Configs bổ sung)
│   └── default.conf           # Default server block (Khối server mặc định)
├── sites-available/           # Available site configs (Debian) (Cấu hình site có sẵn)
├── sites-enabled/             # Enabled sites (symlinks) (Site đang bật)
├── snippets/                  # Reusable config snippets (Đoạn config tái sử dụng)
└── mime.types                 # MIME type mappings (Ánh xạ loại MIME)

/var/log/nginx/                # Logs (Nhật ký)
├── access.log                 # Access logs (Nhật ký truy cập)
└── error.log                  # Error logs (Nhật ký lỗi)

/usr/share/nginx/html/         # Default document root
└── index.html                 # Default welcome page

```

#### 3.2 In Docker Alpine (Trong Docker Alpine)

```bash
docker exec -it nginx sh

# Config (Cấu hình)
cat /etc/nginx/nginx.conf
ls /etc/nginx/conf.d/

# Web root (Thư mục web)
ls /usr/share/nginx/html/

# Logs (Nhật ký)
ls /var/log/nginx/

```

---

### 4. Basic NGINX Configuration (Cấu hình NGINX cơ bản) - 2 hours

#### 4.1 Config File Structure (Cấu trúc file config)

The main configuration file is `nginx.conf`. It controls the global behavior of the server. Let's analyze a standard configuration.

*File cấu hình chính là `nginx.conf`. Nó kiểm soát hành vi toàn cục của server. Hãy phân tích một cấu hình tiêu chuẩn.*

```nginx
# nginx.conf - Main config file (File config chính)

# 1. Global context (Ngữ cảnh toàn cục)
# Defines user and worker processes matching CPU cores
# (Định nghĩa user và số process worker khớp với số core CPU)
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

# 2. Events context (Ngữ cảnh sự kiện)
# Handles connections (Xử lý kết nối)
events {
    worker_connections 1024; # Max connections per worker (Tối đa kết nối mỗi worker)
}

# 3. HTTP context (Ngữ cảnh HTTP)
# Defines how to handle HTTP traffic (Định nghĩa cách xử lý traffic HTTP)
http {
    include /etc/nginx/mime.types; # Load file types (CSS, JS, Images...)
    default_type application/octet-stream;

    # Logging format (Định dạng log)
    log_format main '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';

    access_log /var/log/nginx/access.log main;

    # Optimization (Tối ưu hóa)
    sendfile on;      # Efficient file transfer (Truyền file hiệu quả)
    keepalive_timeout 65; # Keep connection open (Giữ kết nối mở)

    # Include server blocks (Bao gồm các server block từ thư mục con)
    # This keeps the main config clean (Giúp file config chính gọn gàng)
    include /etc/nginx/conf.d/*.conf;
}
```

**Key Components (Thành phần chính):**

- **worker_processes**: Should match number of CPU cores for max performance (Nên bằng số core CPU để đạt hiệu năng tối đa).
- **worker_connections**: Total concurrent connections = workers * connections (Tổng kết nối đồng thời).
- **include**: Imports other config files, allowing modular configuration (Import file config khác, giúp cấu hình dạng module).

#### 4.2 Server Block (Virtual Host)

A `server` block defines a virtual host, allowing NGINX to handle multiple domains or applications on a single server. Each `server` block listens on specific ports and responds to requests for defined `server_name`s.

*Một khối `server` định nghĩa một virtual host, cho phép NGINX xử lý nhiều domain hoặc ứng dụng trên một server duy nhất. Mỗi khối `server` lắng nghe trên các cổng cụ thể và phản hồi các yêu cầu cho các `server_name` đã định nghĩa.*

```nginx
# /etc/nginx/conf.d/default.conf

server {
    # Listen port (Lắng nghe port)
    listen 80;
    listen [::]:80;

    # Server name - domain (Tên server - domain)
    server_name localhost example.com www.example.com;

    # Document root (Thư mục gốc)
    root /usr/share/nginx/html;
    
    # Default file (File mặc định)
    index index.html index.htm;

    # Location block (Khối location)
    location / {
        try_files $uri $uri/ =404;
    }
}

```

#### 4.3 Important Directives (Các directives quan trọng)

| Directive | Description | Example |
|-----------|-------------|---------|
| `listen` | Port to listen on (Port lắng nghe) | `listen 80;` |
| `server_name` | Domain name (Tên miền) | `server_name example.com;` |
| `root` | Document root (Thư mục gốc tài liệu) | `root /var/www/html;` |
| `index` | Default files (Files mặc định) | `index index.html;` |
| `location` | URL pattern matching (Khớp mẫu URL) | `location /api { }` |
| `try_files` | Try multiple files (Thử nhiều files) | `try_files $uri $uri/ =404;` |
| `error_page` | Custom error pages (Trang lỗi tùy chỉnh) | `error_page 404 /404.html;` |

---

### 5. Serving Static Files (Phục vụ Static Files) - 1 hour

#### 5.1 Basic Static Website

**Project structure (Cấu trúc project):**

```ini
my-website/
├── docker-compose.yml
├── nginx.conf
└── html/
    ├── index.html
    ├── about.html
    ├── css/
    │   └── style.css
    ├── js/
    │   └── app.js
    └── images/
        └── logo.png

```

**nginx.conf:**

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Serve static files
    location / {
        try_files $uri $uri/ =404;
    }

    # Cache static assets
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Custom 404 page
    error_page 404 /404.html;
    location = /404.html {
        internal;
    }
}

```

**Dockerfile:**

```dockerfile
FROM nginx:alpine

# Copy custom config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy website files
COPY html/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

```

#### 5.2 Gzip Compression

```nginx
http {
    # Enable gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/plain text/css text/xml text/javascript 
               application/x-javascript application/xml 
               application/javascript application/json;
    gzip_disable "MSIE [1-6]\.";
}

```

---

### 6. Reverse Proxy (Proxy ngược) - 1.5 hours

#### 6.1 Concept (Khái niệm)

```ini
┌─────────────────────────────────────────────────────────────┐
│                    REVERSE PROXY                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Client                                                     │
│     │                                                        │
│     ▼                                                        │
│  ┌─────────────────┐                                        │
│  │     NGINX       │  ← Proxy Server                        │
│  │  (Port 80/443)  │                                        │
│  └────────┬────────┘                                        │
│           │                                                  │
│     ┌─────┴─────┐                                           │
│     │           │                                           │
│     ▼           ▼                                           │
│  ┌──────┐   ┌──────┐                                        │
│  │ API  │   │ Web  │  ← Backend Servers                     │
│  │:3000 │   │:8080 │                                        │
│  └──────┘   └──────┘                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘

```

#### 6.2 Basic Reverse Proxy (Cấu hình Reverse Proxy cơ bản)

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://backend:3000;
        
        # Important headers (Headers quan trọng)
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```

#### 6.3 Multiple Backends (Nhiều Backend servers)

```nginx
server {
    listen 80;
    server_name example.com;

    # Frontend - Static files (Serve file tĩnh)
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # API - Proxy to backend (Chuyển tiếp API)
    location /api/ {
        proxy_pass http://api-server:3000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket support (Hỗ trợ WebSocket)
    location /ws/ {
        proxy_pass http://ws-server:8080/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

```

---

### 7. Load Balancing Basics (Cân bằng tải cơ bản) - 1 hour

#### 7.1 Round Robin - Default (Luân phiên - Mặc định)

```nginx
upstream backend {
    server backend1:3000;
    server backend2:3000;
    server backend3:3000;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend;
    }
}

```

#### 7.2 Weighted Load Balancing (Phân tải theo trọng số)

```nginx
upstream backend {
    server backend1:3000 weight=3;  # 3x traffic
    server backend2:3000 weight=1;  # 1x traffic
    server backend3:3000 weight=1;  # 1x traffic
}

```

#### 7.3 Health Checks (Kiểm tra sức khỏe server)

```nginx
upstream backend {
    server backend1:3000;
    server backend2:3000;
    server backend3:3000 backup;  # Only if others fail (Chỉ dùng khi các server khác fail)
    
    # Passive health check (Kiểm tra sức khỏe thụ động)
    server backend4:3000 max_fails=3 fail_timeout=30s;
}

```

---

### 8. NGINX with Docker Compose (NGINX với Docker Compose) - 1 hour

#### 8.1 Full Stack Example (Ví dụ Full Stack)

- Create `docker-compose.yml` (Tạo file `docker-compose.yml`):

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./html:/usr/share/nginx/html:ro
    depends_on:
      - api
    networks:
      - app-network

  api:
    build: ./api
    expose:
      - "3000"
    environment:
      - NODE_ENV=production
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

```

**nginx.conf:**

```nginx
server {
    listen 80;
    server_name localhost;

    # Serve static frontend (Phục vụ frontend tĩnh)
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests (Chuyển tiếp API requests)
    location /api/ {
        proxy_pass http://api:3000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

```

---

### 9. Debugging and Logging (Debug và Xem logs) - 30 min

#### 9.1 Viewing Logs (Xem logs)

- Run the following commands (Chạy các lệnh sau):

```bash
# Docker
docker logs nginx
docker logs -f nginx

# Linux
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

```

#### 9.2 Custom Log Format (Định dạng log tùy chỉnh)

```nginx
http {
    log_format detailed '$remote_addr - $remote_user [$time_local] '
                        '"$request" $status $body_bytes_sent '
                        '"$http_referer" "$http_user_agent" '
                        '$request_time $upstream_response_time';
    
    access_log /var/log/nginx/access.log detailed;
}

```

#### 9.3 Debug Tips (Mẹo debug)

- Useful commands for debugging (Các lệnh hữu ích để debug):

```bash
# Test config syntax (Kiểm tra cú pháp config)
nginx -t

# Show full config (Hiển thị toàn bộ config)
nginx -T

# Reload config without downtime (Reload config không downtime)
nginx -s reload

# Docker commands (Lệnh Docker)
docker exec nginx nginx -t
docker exec nginx nginx -s reload

```

---

### 10. Security Best Practices (Bảo mật tốt nhất) - 30 min

```nginx
server {
    # Hide NGINX version (Ẩn version NGINX)
    server_tokens off;

    # Security headers (Headers bảo mật)
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Limit request size (Giới hạn kích thước request)
    client_max_body_size 10M;

    # Rate limiting (Giới hạn tốc độ)
    limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;
    
    location /api/ {
        limit_req zone=mylimit burst=20 nodelay;
        proxy_pass http://backend;
    }

    # Block common attacks (Chặn các tấn công phổ biến)
    location ~* \.(git|svn|htaccess)$ {
        deny all;
    }
}

```

---

> ✅ **Checkpoint - Before continuing, make sure you can answer:**
> *(Trước khi tiếp tục, hãy chắc bạn có thể trả lời:)*
>
> - [ ] What's the difference between a web server and a reverse proxy? *(Web server và reverse proxy khác nhau như thế nào?)*
> - [ ] How to configure NGINX to serve a static website? *(Làm sao cấu hình NGINX serve static website?)*
> - [ ] What does `proxy_pass` do? *(proxy_pass làm gì?)*
> - [ ] How to reload NGINX config without downtime? *(Làm sao reload config NGINX không downtime?)*
>
> *If you can't answer, please re-read the sections above!*

---

## 📝 Module Files (Các file trong Module)

| File | Description |
|------|-------------|
| [CHEATSHEET.md](./CHEATSHEET.md) | Quick reference (Tra cứu nhanh) |
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Exercises (Bài tập) |
| [PROJECT.md](./PROJECT.md) | Mini project (Dự án nhỏ) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Solutions (Đáp án) |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [1.5 Docker](../1.5_Docker_Fundamentals/) | **1.6 NGINX** | [1.7 CI/CD](../1.7_CICD_Basic/) |

---

**Master NGINX! 🌐**

*Thành thạo NGINX!*

</div>
