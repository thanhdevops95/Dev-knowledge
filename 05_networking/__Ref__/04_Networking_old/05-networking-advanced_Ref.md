# 🌐 Networking nâng cao — Firewall, VPN, Load Balancer

> `[INTERMEDIATE]` — Bảo mật & tối ưu mạng cho production

---

## 1. Firewall — Tường lửa

```
Internet ──► Firewall ──► DMZ ──► Internal Network

Firewall = bộ lọc traffic dựa trên rules

Types:
• Packet filtering:  Lọc theo IP, port, protocol
• Stateful:          Theo dõi connection state (TCP handshake)
• Application-level: Kiểm tra HTTP content (WAF)
• Next-gen (NGFW):   DPI + IDS/IPS + antivirus + VPN
```

```bash
# iptables (Linux firewall)
# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Drop everything else
iptables -A INPUT -j DROP

# AWS Security Group (cloud firewall)
# Inbound:  Allow 80, 443 from 0.0.0.0/0
# Inbound:  Allow 22 from 10.0.0.0/8 (internal only!)
# Outbound: Allow all
```

---

## 2. VPN — Virtual Private Network

```
Không VPN:
You ──[plain text]──► ISP ──► Internet ──► Server
         ↑ ISP thấy mọi thứ bạn truy cập!

Với VPN:
You ──[encrypted tunnel]──► VPN Server ──[plain text]──► Internet
         ↑ ISP chỉ thấy bạn connect VPN, không biết nội dung

Types:
• Remote Access VPN:  Nhân viên → Company network (OpenVPN, WireGuard)
• Site-to-Site VPN:   Office A ↔ Office B (IPSec)
• Cloud VPN:          VPC peering, AWS VPN Gateway
```

```
WireGuard (modern, nhanh, đơn giản):
# Server config
[Interface]
PrivateKey = server_private_key
Address = 10.0.0.1/24
ListenPort = 51820

[Peer]
PublicKey = client_public_key
AllowedIPs = 10.0.0.2/32

# Client config
[Interface]
PrivateKey = client_private_key
Address = 10.0.0.2/32
DNS = 1.1.1.1

[Peer]
PublicKey = server_public_key
AllowedIPs = 0.0.0.0/0
Endpoint = server.example.com:51820
```

---

## 3. Load Balancing — Chi tiết

```
          ┌──────────────────┐
Users ───►│  Load Balancer   │
          │  (HAProxy/Nginx) │
          └────────┬─────────┘
          ┌────────┼─────────┐
          ▼        ▼         ▼
       ┌─────┐ ┌─────┐ ┌─────┐
       │ S1  │ │ S2  │ │ S3  │
       │ OK  │ │ OK  │ │ ❌  │ ← Health check fail → remove
       └─────┘ └─────┘ └─────┘
```

### Nginx Load Balancer Config

```nginx
upstream backend {
    # Round Robin (default)
    server backend1.example.com:3000;
    server backend2.example.com:3000;
    server backend3.example.com:3000 backup;  # Chỉ dùng khi khác fail

    # Least connections
    # least_conn;

    # IP Hash (sticky sessions)
    # ip_hash;

    # Weighted
    # server backend1.example.com:3000 weight=3;
    # server backend2.example.com:3000 weight=1;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### L4 vs L7 Load Balancing

```
L4 (Transport Layer):
  Quyết định dựa trên: IP, Port, Protocol
  Nhanh hơn, không đọc content
  Ví dụ: AWS NLB, HAProxy TCP mode

L7 (Application Layer):
  Quyết định dựa trên: URL path, headers, cookies
  Linh hoạt hơn, có thể route theo content
  Ví dụ: AWS ALB, Nginx, HAProxy HTTP mode

  /api/users  → User Service
  /api/orders → Order Service
  /static/*   → CDN / S3
```

---

## 4. CDN — Content Delivery Network

```
Không CDN:
  User (Việt Nam) ──► Server (US) = ~200ms latency

Với CDN:
  User (Việt Nam) ──► CDN Edge (Singapore) = ~20ms latency
                      Cache hit → trả ngay!
                      Cache miss → fetch từ Origin → cache → trả

CDN caches:
  ✅ Static files: images, CSS, JS, fonts
  ✅ API responses (Cache-Control: public)
  ❌ Dynamic/personalized content (unless Edge Computing)

Providers:
  • Cloudflare (free tier tốt)
  • AWS CloudFront
  • Fastly (rất nhanh)
  • Vercel Edge Network
```

---

## 5. Reverse Proxy vs Forward Proxy

```
Forward Proxy (cho client):
  Client ──► Proxy ──► Internet
  • Hide client IP
  • Filter content (corporate)
  • Cache

Reverse Proxy (cho server):
  Internet ──► Reverse Proxy ──► Servers
  • Load balancing
  • SSL termination
  • Caching
  • Security (WAF)
  • Compression

Most common: Nginx, Caddy, Traefik
```

---

## 6. SSL/TLS — Certificates

```bash
# Let's Encrypt — free SSL
# Certbot auto
sudo certbot --nginx -d example.com -d www.example.com
# Auto-renew: certbot renew (cron job)

# Self-signed (dev only!)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

```
SSL/TLS Certificate Chain:
Root CA → Intermediate CA → Server Certificate

Types:
• DV (Domain Validation):     Verify domain ownership → minutes
• OV (Organization):          Verify org → days
• EV (Extended Validation):   Full verification → weeks
• Wildcard:                   *.example.com
```

---

## 7. Network Debugging

```bash
# DNS
dig example.com +trace           # Full resolution path
nslookup example.com 8.8.8.8    # Query specific DNS

# TCP
telnet server.com 443            # Test connection
nc -zv server.com 80-443         # Scan ports

# HTTP
curl -I https://example.com      # Headers only
curl -w "DNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" -o /dev/null -s https://example.com

# Network path
traceroute example.com           # Linux/macOS
tracert example.com              # Windows
mtr example.com                  # Continuous traceroute

# Packet capture
tcpdump -i eth0 port 80          # Capture HTTP traffic
tcpdump -i eth0 host 1.2.3.4    # Capture from specific IP

# Performance
iperf3 -s                        # Server mode
iperf3 -c server.com             # Bandwidth test
```

---

## Các lỗi thường gặp

```
❌ Sai: Expose database port (3306, 5432) ra internet
✅ Đúng: Database trong private subnet, access qua VPN/bastion

❌ Sai: Self-signed SSL cho production
✅ Đúng: Let's Encrypt (free) hoặc commercial cert

❌ Sai: Không có health check → LB gửi traffic đến dead server
✅ Đúng: Health check endpoint + auto-remove unhealthy
```

---

## Bài tập thực hành

- [ ] Setup Nginx reverse proxy: SSL + proxy_pass đến Node.js
- [ ] Cấu hình iptables: chỉ allow 22, 80, 443
- [ ] Setup WireGuard VPN giữa 2 máy
- [ ] Debug latency bằng curl timing + traceroute

---

## Tài nguyên thêm

- [Nginx Docs](https://nginx.org/en/docs/) — Official
- [Cloudflare Learning](https://www.cloudflare.com/learning/) — Networking concepts
- [High Performance Browser Networking](https://hpbn.co/) — Free book
