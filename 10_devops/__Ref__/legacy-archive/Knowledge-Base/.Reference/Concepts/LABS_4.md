# Module 05: Web Servers Labs

---

## 🎯 Mục tiêu

Sau labs này, bạn sẽ:

- Cài đặt và cấu hình Nginx
- Serve static website
- Setup reverse proxy
- Cấu hình HTTPS

---

## 🔧 Lab 1: Cài đặt Nginx

### Bước 1: Cài đặt

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx -y

# Kiểm tra version
nginx -v
```

### Bước 2: Start và kiểm tra

```bash
# Start nginx
sudo systemctl start nginx

# Enable auto-start
sudo systemctl enable nginx

# Check status
sudo systemctl status nginx
```

### Bước 3: Truy cập

Mở browser: `http://localhost` hoặc `http://your-ip`

Bạn sẽ thấy trang "Welcome to nginx!"

### Bước 4: Xem cấu trúc

```bash
ls -la /etc/nginx/
ls -la /var/www/html/
```

### ✅ Checkpoint Lab 1

- [ ] Nginx chạy OK
- [ ] Truy cập được trang default

---

## 📄 Lab 2: Static Website

### Bước 1: Tạo website

```bash
# Tạo thư mục
sudo mkdir -p /var/www/mysite

# Tạo HTML
sudo tee /var/www/mysite/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>My DevOps Site</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #1a1a2e; color: #eee; }
        h1 { color: #00ff88; }
        .container { max-width: 800px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Welcome to My DevOps Site!</h1>
        <p>Served by Nginx</p>
        <p>Time: <span id="time"></span></p>
    </div>
    <script>
        document.getElementById('time').textContent = new Date().toLocaleString();
    </script>
</body>
</html>
EOF

# Set permissions
sudo chown -R www-data:www-data /var/www/mysite
```

### Bước 2: Tạo Nginx config

```bash
sudo tee /etc/nginx/sites-available/mysite << 'EOF'
server {
    listen 80;
    server_name mysite.local;
    
    root /var/www/mysite;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Logs
    access_log /var/log/nginx/mysite.access.log;
    error_log /var/log/nginx/mysite.error.log;
}
EOF
```

### Bước 3: Enable site

```bash
# Create symlink
sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test config
sudo nginx -t

# Reload
sudo systemctl reload nginx
```

### Bước 4: Test

```bash
# Add to /etc/hosts (for local testing)
echo "127.0.0.1 mysite.local" | sudo tee -a /etc/hosts

# Test
curl http://mysite.local
```

### ✅ Checkpoint Lab 2

- [ ] Custom website hiển thị
- [ ] Hiểu cấu trúc config

---

## 🔄 Lab 3: Reverse Proxy

### Bước 1: Tạo simple backend app

```bash
# Tạo Python app
mkdir -p ~/backend-app
cd ~/backend-app

cat > app.py << 'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "message": "Hello from backend!",
            "port": 3000,
            "path": self.path
        }
        self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 3000), Handler)
    print("Backend running on port 3000")
    server.serve_forever()
EOF
```

### Bước 2: Chạy backend

```bash
# Mở terminal mới
cd ~/backend-app
python3 app.py &

# Test direct access
curl http://localhost:3000
```

### Bước 3: Config reverse proxy

```bash
sudo tee /etc/nginx/sites-available/api << 'EOF'
server {
    listen 80;
    server_name api.local;
    
    location / {
        proxy_pass http://127.0.0.1:3000;
        
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable
sudo ln -s /etc/nginx/sites-available/api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Add hosts entry
echo "127.0.0.1 api.local" | sudo tee -a /etc/hosts
```

### Bước 4: Test reverse proxy

```bash
curl http://api.local
# Response từ backend qua Nginx!
```

### ✅ Checkpoint Lab 3

- [ ] Backend chạy trên port 3000
- [ ] Nginx proxy requests từ port 80
- [ ] Headers được forward

---

## ⚖️ Lab 4: Load Balancing

### Bước 1: Tạo multiple backends

```bash
cd ~/backend-app

# App on port 3001
cat > app3001.py << 'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"message": "Hello from backend!", "port": 3001}
        self.wfile.write(json.dumps(response).encode())

server = HTTPServer(('0.0.0.0', 3001), Handler)
print("Backend running on port 3001")
server.serve_forever()
EOF

# App on port 3002
cat > app3002.py << 'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"message": "Hello from backend!", "port": 3002}
        self.wfile.write(json.dumps(response).encode())

server = HTTPServer(('0.0.0.0', 3002), Handler)
print("Backend running on port 3002")
server.serve_forever()
EOF

# Start all backends
python3 app.py &
python3 app3001.py &
python3 app3002.py &
```

### Bước 2: Config load balancer

```bash
sudo tee /etc/nginx/sites-available/loadbalancer << 'EOF'
upstream backend_servers {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
}

server {
    listen 80;
    server_name lb.local;
    
    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# Enable
sudo ln -s /etc/nginx/sites-available/loadbalancer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

echo "127.0.0.1 lb.local" | sudo tee -a /etc/hosts
```

### Bước 3: Test load balancing

```bash
# Gọi nhiều lần, xem port thay đổi (round-robin)
for i in {1..6}; do
    echo "Request $i:"
    curl -s http://lb.local | jq .port
done
```

### ✅ Checkpoint Lab 4

- [ ] 3 backends chạy
- [ ] Nginx phân phối requests

---

## 🔐 Lab 5: Self-signed SSL (Development)

### Bước 1: Tạo self-signed certificate

```bash
# Tạo thư mục cho certs
sudo mkdir -p /etc/nginx/ssl

# Generate self-signed cert
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/nginx.key \
    -out /etc/nginx/ssl/nginx.crt \
    -subj "/C=VN/ST=HCM/L=HCM/O=DevOps/CN=secure.local"
```

### Bước 2: Config HTTPS

```bash
sudo tee /etc/nginx/sites-available/secure << 'EOF'
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name secure.local;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl;
    server_name secure.local;
    
    ssl_certificate /etc/nginx/ssl/nginx.crt;
    ssl_certificate_key /etc/nginx/ssl/nginx.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    
    root /var/www/mysite;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
EOF

# Enable
sudo ln -s /etc/nginx/sites-available/secure /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

echo "127.0.0.1 secure.local" | sudo tee -a /etc/hosts
```

### Bước 3: Test

```bash
# HTTP redirects to HTTPS
curl -I http://secure.local

# HTTPS (skip cert verification for self-signed)
curl -k https://secure.local
```

### ✅ Checkpoint Lab 5

- [ ] HTTP redirects to HTTPS
- [ ] HTTPS works (with warning for self-signed)

---

## 📊 Lab 6: Logging và Monitoring

### Bước 1: Custom log format

```bash
sudo tee /etc/nginx/conf.d/logging.conf << 'EOF'
log_format detailed '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" '
                    'rt=$request_time uct=$upstream_connect_time '
                    'uht=$upstream_header_time urt=$upstream_response_time';
EOF
```

### Bước 2: Xem logs real-time

```bash
# Access log
sudo tail -f /var/log/nginx/access.log

# Error log
sudo tail -f /var/log/nginx/error.log

# Filter errors
sudo tail -f /var/log/nginx/error.log | grep -i error
```

### Bước 3: Analyze logs

```bash
# Top IPs
cat /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head

# Status codes
cat /var/log/nginx/access.log | awk '{print $9}' | sort | uniq -c | sort -rn

# Top URLs
cat /var/log/nginx/access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head
```

### ✅ Checkpoint Lab 6

- [ ] Xem được logs
- [ ] Phân tích traffic

---

## 🎓 Tổng kết Labs

| Lab | Skill | Output |
|-----|-------|--------|
| 1 | Installation | Nginx running |
| 2 | Static site | Custom website |
| 3 | Reverse proxy | Backend behind Nginx |
| 4 | Load balancing | Multiple backends |
| 5 | HTTPS | SSL encryption |
| 6 | Logging | Traffic analysis |

---

## ⏭️ Tiếp theo

👉 **[SCENARIOS.md - Tình huống Nginx](SCENARIOS.md)**
