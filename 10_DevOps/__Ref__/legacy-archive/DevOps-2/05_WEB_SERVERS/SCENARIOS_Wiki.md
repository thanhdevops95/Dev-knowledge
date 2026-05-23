# Module 05: Web Servers Scenarios

---

## 🚨 Scenario 1: "Website báo 502 Bad Gateway"

### 📍 Bối cảnh

Users báo website không vào được, hiện:

```
502 Bad Gateway
nginx/1.18.0
```

### 🔍 Điều tra

**Bước 1: Check backend app**

```bash
# App có chạy không?
ps aux | grep python  # hoặc node, java...

# App có listen đúng port không?
ss -tuln | grep 3000
```

**Bước 2: Test direct connection**

```bash
curl http://localhost:3000
# Nếu fail → backend down
```

**Bước 3: Check nginx error log**

```bash
sudo tail -20 /var/log/nginx/error.log
```

**Output thường thấy:**

```
connect() failed (111: Connection refused) while connecting to upstream
```

### 💡 Giải quyết

```bash
# Restart backend
sudo systemctl restart myapp

# Hoặc chạy thủ công
cd /home/app && python app.py &
```

### 📚 Bài học

502 = Nginx OK, Backend NOT OK

---

## 🚨 Scenario 2: "SSL Certificate hết hạn"

### 📍 Bối cảnh

Browser cảnh báo "Your connection is not private"

### 🔍 Kiểm tra cert

```bash
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
```

**Output:**

```
notAfter=Dec 22 00:00:00 2023 GMT   ← Đã hết hạn!
```

### 💡 Giải quyết

**Let's Encrypt:**

```bash
sudo certbot renew
sudo systemctl reload nginx
```

**Setup auto-renewal:**

```bash
# Certbot timer
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Hoặc crontab
echo "0 3 * * * root certbot renew --quiet" | sudo tee /etc/cron.d/certbot
```

---

## 🚨 Scenario 3: "Nginx không start được"

### 📍 Bối cảnh

```bash
sudo systemctl start nginx
# Job for nginx.service failed
```

### 🔍 Điều tra

**Bước 1: Test config**

```bash
sudo nginx -t
```

**Output lỗi thường gặp:**

```
nginx: [emerg] unknown directive "proxy_passs" in /etc/nginx/sites-enabled/mysite:10
```

**Bước 2: Check port conflict**

```bash
sudo ss -tuln | grep :80
# Nếu có process khác dùng port 80
```

**Bước 3: Xem logs**

```bash
sudo journalctl -u nginx -n 50
```

### 💡 Giải quyết

**Config error:**

```bash
# Fix typo trong config
sudo nano /etc/nginx/sites-enabled/mysite
sudo nginx -t
sudo systemctl start nginx
```

**Port conflict:**

```bash
# Tìm process dùng port 80
sudo lsof -i :80

# Kill hoặc config nginx dùng port khác
```

---

## 🚨 Scenario 4: "Website chậm"

### 📍 Bối cảnh

Website load mất 10 giây thay vì 1 giây.

### 🔍 Điều tra

**Bước 1: Check response time**

```bash
curl -w "Total time: %{time_total}s\n" -o /dev/null -s https://example.com
```

**Bước 2: Analyze nginx logs**

```bash
# Nếu có log request time
cat /var/log/nginx/access.log | awk '{print $NF}' | sort -n | tail -20
```

**Bước 3: Check backend**

```bash
curl -w "Time: %{time_total}s\n" -o /dev/null -s http://localhost:3000
```

### 💡 Giải quyết

**Enable caching:**

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

**Enable gzip:**

```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
gzip_min_length 1000;
```

**Connection pooling:**

```nginx
upstream backend {
    server 127.0.0.1:3000;
    keepalive 32;
}
```

---

## 🚨 Scenario 5: "Một server trong pool bị chết"

### 📍 Bối cảnh

Load balancer có 3 servers, 1 server bị down. Users gặp lỗi intermittently.

### 💡 Giải quyết

**Health checks:**

```nginx
upstream backend {
    server 127.0.0.1:3000 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:3001 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:3002 max_fails=3 fail_timeout=30s;
}
```

**Giải thích:**

- `max_fails=3` - Nếu fail 3 lần
- `fail_timeout=30s` - Ngừng gửi traffic trong 30 giây

**Backup server:**

```nginx
upstream backend {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002 backup;  # Chỉ dùng khi các server khác down
}
```

---

## 📋 Nginx Troubleshooting Cheatsheet

| Vấn đề | Nguyên nhân | Giải pháp |
|--------|-------------|-----------|
| 502 Bad Gateway | Backend down | Restart backend |
| 503 Service Unavailable | All backends down | Check all servers |
| 504 Gateway Timeout | Backend quá chậm | Increase timeout |
| Config error | Typo trong config | `nginx -t` để debug |
| Port in use | Process khác dùng | Kill hoặc đổi port |
| SSL error | Cert expired | `certbot renew` |
| Slow response | No caching | Enable caching, gzip |

---

## ⏭️ Module tiếp theo

👉 **[Module 06: Databases](../06_DATABASES/README.md)**
