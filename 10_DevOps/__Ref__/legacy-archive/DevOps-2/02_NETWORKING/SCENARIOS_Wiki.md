# Module 02: Networking Scenarios

---

## 🎯 Mục đích

Đây là những tình huống network **thực tế** bạn sẽ gặp. Mỗi scenario giúp bạn học cách suy nghĩ như một DevOps khi debug network issues.

---

## 🚨 Scenario 1: "Website không load được"

### 📍 Bối cảnh

Bạn nhận tin nhắn từ boss:

> "Website company không vào được, fix gấp!"

Bạn mở browser, gõ `https://mycompany.com` và thấy:

```
This site can't be reached
mycompany.com's server IP address could not be found.
```

### 🔍 Bước 1: Xác định vấn đề

**"IP address could not be found"** = DNS không resolve được

Kiểm tra:

```bash
nslookup mycompany.com
```

**Output xấu:**

```
** server can't find mycompany.com: NXDOMAIN
```

**NXDOMAIN** = Domain không tồn tại trong DNS

### 🔍 Bước 2: Kiểm tra DNS server

```bash
# DNS server có phản hồi không?
ping 8.8.8.8

# Thử DNS server khác
nslookup mycompany.com 1.1.1.1
```

**Nếu 8.8.8.8 OK nhưng nslookup vẫn fail:**
→ Vấn đề là DNS records của domain, không phải network

### 🔍 Bước 3: Kiểm tra với domain registrar

Có thể:

- Domain hết hạn
- DNS records bị xóa
- Nameserver config sai

### 💡 Giải quyết

**Nếu domain hết hạn:**
→ Renew với registrar (GoDaddy, Namecheap...)

**Nếu DNS records sai:**
→ Login vào DNS provider, kiểm tra A record

```
A record cần có:
Host: @
Value: <your-server-ip>
TTL: 300
```

### 📚 Bài học

1. **DNS là điểm fail đầu tiên** cần check
2. **Luôn có nhiều DNS servers** để test (8.8.8.8, 1.1.1.1)
3. **Monitor domain expiry** - set reminder trước 30 ngày

---

## 🚨 Scenario 2: "Connection Refused"

### 📍 Bối cảnh

Bạn deploy app lên server. Chạy thử:

```bash
curl http://192.168.1.100:3000
```

**Output:**

```
curl: (7) Failed to connect to 192.168.1.100 port 3000: Connection refused
```

### 🔍 Bước 1: App có đang chạy không?

SSH vào server:

```bash
ssh user@192.168.1.100
```

Kiểm tra process:

```bash
ps aux | grep node
```

**Output rỗng?** → App chưa chạy!

```bash
# Start the app
cd /home/app
npm start
```

### 🔍 Bước 2: App chạy nhưng vẫn refused?

Kiểm tra app đang listen ở đâu:

```bash
ss -tuln | grep 3000
```

**Output có thể là:**

```
LISTEN  127.0.0.1:3000
```

**Vấn đề:** App chỉ listen trên `127.0.0.1` (localhost), không phải `0.0.0.0` (all interfaces)

### 💡 Giải quyết

**Sửa app để listen trên 0.0.0.0:**

```javascript
// Node.js example
app.listen(3000, '0.0.0.0', () => {
  console.log('Server running on port 3000');
});
```

**Hoặc set environment variable:**

```bash
HOST=0.0.0.0 npm start
```

### 🔍 Bước 3: Vẫn refused? Check firewall

```bash
sudo ufw status
```

**Nếu port 3000 không được allow:**

```bash
sudo ufw allow 3000
```

### 📚 Bài học

**"Connection Refused" checklist:**

```
1. [ ] App có đang chạy không?
2. [ ] App listen trên 0.0.0.0 hay 127.0.0.1?
3. [ ] Firewall có allow port không?
4. [ ] Security group (cloud) có allow không?
```

---

## 🚨 Scenario 3: "Connection Timeout"

### 📍 Bối cảnh

Khác với "refused", lần này bạn gặp:

```bash
curl http://192.168.1.100:80
```

**Output:**

```
curl: (28) Connection timed out after 30000 milliseconds
```

### 🔍 Phân biệt Timeout vs Refused

| Connection Refused | Connection Timeout |
|--------------------|-------------------|
| Server nhận được request | Request không đến được server |
| Port không có ai listen | Firewall block hoặc network issue |
| Fail ngay lập tức | Đợi timeout rồi mới fail |

### 🔍 Bước 1: Ping được không?

```bash
ping 192.168.1.100
```

**Nếu không ping được:**
→ Network issue (server down, wrong IP, routing)

**Nếu ping OK:**
→ Firewall blocking specific port

### 🔍 Bước 2: Check firewall trên server

```bash
# SSH vào server (nếu được)
ssh user@192.168.1.100

# Xem firewall
sudo ufw status

# Xem có service listen không
ss -tuln | grep 80
```

### 🔍 Bước 3: Check cloud security group

Nếu dùng AWS/GCP:

1. Vào console → EC2 → Security Groups
2. Tìm security group của instance
3. Kiểm tra Inbound Rules có allow port 80 không

### 💡 Giải quyết

**Local firewall:**

```bash
sudo ufw allow 80
```

**AWS Security Group:**

- Add Inbound Rule
- Type: HTTP
- Source: 0.0.0.0/0 (hoặc restrict theo IP)

### 📚 Bài học

**Timeout = Request không đến được destination**

```
Checklist:
1. [ ] Ping được không?
2. [ ] Local firewall (ufw/iptables)
3. [ ] Cloud security group/firewall
4. [ ] Network ACL (VPC level)
5. [ ] ISP blocking?
```

---

## 🚨 Scenario 4: "502 Bad Gateway"

### 📍 Bối cảnh

Website hoạt động bình thường, đột nhiên hiện:

```
502 Bad Gateway
nginx/1.18.0
```

### 🔍 Bước 1: Hiểu 502 là gì

```
User → Nginx (reverse proxy) → App
                    ↑
                    └── Nginx không connect được App
                    → Trả về 502
```

**502 có nghĩa:** Nginx (gateway) không nhận được response từ backend.

### 🔍 Bước 2: Check app backend

```bash
# App có chạy không?
ps aux | grep python  # hoặc node, java...

# App có respond không?
curl localhost:8000
```

**Nếu app crash:**

```bash
# Xem logs
journalctl -u myapp -n 50

# Hoặc
tail -100 /var/log/myapp/error.log
```

### 🔍 Bước 3: Check nginx config

```bash
# Test config syntax
sudo nginx -t

# Xem upstream config
cat /etc/nginx/sites-enabled/myapp
```

**Config ví dụ:**

```nginx
upstream backend {
    server 127.0.0.1:8000;  ← App phải chạy ở đây
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
    }
}
```

### 💡 Giải quyết

**Nếu app crash:**

```bash
sudo systemctl restart myapp
```

**Nếu port sai:**

- Sửa nginx config hoặc app config để match

**Nếu app quá chậm (timeout):**

```nginx
# Tăng timeout trong nginx
proxy_connect_timeout 60s;
proxy_read_timeout 60s;
```

### 📚 Bài học

**502 = Backend problem**

```
Checklist:
1. [ ] Backend app có chạy không?
2. [ ] Backend đang listen đúng port?
3. [ ] Nginx config đúng upstream?
4. [ ] Backend có overloaded không?
```

---

## 🚨 Scenario 5: "SSL Certificate Error"

### 📍 Bối cảnh

Users báo browser cảnh báo:

```
Your connection is not private
NET::ERR_CERT_DATE_INVALID
```

### 🔍 Bước 1: Kiểm tra certificate

```bash
# Xem cert info
echo | openssl s_client -connect mycompany.com:443 2>/dev/null | openssl x509 -noout -dates
```

**Output:**

```
notBefore=Jan  1 00:00:00 2023 GMT
notAfter=Jan  1 00:00:00 2024 GMT   ← Hết hạn!
```

### 🔍 Bước 2: Xác định loại cert

```bash
# Xem cert details
echo | openssl s_client -connect mycompany.com:443 2>/dev/null | openssl x509 -noout -text | grep -A1 "Issuer"
```

**Output:**

```
Issuer: C = US, O = Let's Encrypt, CN = R3
```

→ Let's Encrypt cert

### 💡 Giải quyết

**Let's Encrypt (certbot):**

```bash
# Renew tất cả certs
sudo certbot renew

# Renew specific domain
sudo certbot certonly --nginx -d mycompany.com

# Reload nginx
sudo systemctl reload nginx
```

**Paid cert (DigiCert, Comodo...):**

1. Login vào provider
2. Download renewed cert
3. Replace files trên server
4. Reload nginx

### 🔍 Bước 3: Setup auto-renewal

```bash
# Kiểm tra certbot timer
systemctl status certbot.timer

# Nếu không có, thêm cron job
sudo crontab -e
# Thêm dòng:
0 3 * * * certbot renew --quiet
```

### 📚 Bài học

```
SSL cert problems:
1. [ ] Cert hết hạn → Renew
2. [ ] Cert sai domain → Reissue
3. [ ] Chain không đầy đủ → Check intermediate certs
4. [ ] Luôn setup auto-renewal!
```

---

## 🎓 Tổng kết Scenarios

| Scenario | Triệu chứng | Nguyên nhân thường gặp |
|----------|-------------|------------------------|
| 1 | DNS not found | Domain expired, DNS misconfigured |
| 2 | Connection refused | App not running, wrong bind address |
| 3 | Connection timeout | Firewall, security groups |
| 4 | 502 Bad Gateway | Backend down, misconfigured proxy |
| 5 | SSL error | Certificate expired |

### Quick Debug Flow

```
Website không load?
        │
        ├── DNS resolve được không?
        │   ├── Không → Check DNS
        │   └── Được ↓
        │
        ├── Ping được server không?
        │   ├── Không → Network/firewall
        │   └── Được ↓
        │
        ├── Port có mở không?
        │   ├── Refused → App not running
        │   ├── Timeout → Firewall
        │   └── Open ↓
        │
        └── HTTP status?
            ├── 502/503 → Backend issue
            ├── 500 → App error
            └── 200 → OK!
```

---

## ⏭️ Module tiếp theo

👉 **[Module 03: Scripting](../03_SCRIPTING/README.md)**
