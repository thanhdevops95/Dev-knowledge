# 🔀 Proxies — Forward & Reverse Proxy

> `[BEGINNER → INTERMEDIATE]` — Prerequisite: hiểu HTTP, DNS cơ bản
> Trung gian giữa client và server — bảo mật, performance, routing.

---

## Tại sao cần Proxy?

**Proxy** là trung gian đứng giữa client và server. Tùy vào vị trí, có 2 loại:

```
Forward Proxy (Client-side):
  Client → [Proxy] → Internet → Server
  • Client biết proxy, server không biết client
  • Ví dụ: VPN, corporate proxy, Tor

Reverse Proxy (Server-side):
  Client → Internet → [Proxy] → Server(s)
  • Client không biết server thật, chỉ biết proxy
  • Ví dụ: Nginx, Cloudflare, API Gateway
```

---

## 1. Forward Proxy

### Cách hoạt động

```
Client (10.0.0.5) ──→ Forward Proxy (10.0.0.1) ──→ google.com
                      ↑
                      • Thay đổi source IP (ẩn danh)
                      • Cache responses
                      • Filter/block websites
                      • Log access
```

### Use cases

| Use case | Mô tả |
|---|---|
| **Corporate proxy** | Công ty kiểm soát internet access, block websites |
| **Caching** | Cache thường xuyên truy cập → giảm bandwidth |
| **Anonymity** | Ẩn IP thật của client |
| **Geo-unblocking** | Bypass geo-restrictions (VPN chính là forward proxy) |
| **Content filtering** | Block malware, ads, NSFW |

### SOCKS5 Proxy

```bash
# SSH SOCKS5 proxy — tunnel mọi traffic qua SSH
ssh -D 1080 user@server
# Browser config: SOCKS proxy localhost:1080

# Curl qua SOCKS5
curl --socks5 localhost:1080 https://api.example.com
```

---

## 2. Reverse Proxy

### Cách hoạt động

```
Client ──→ Reverse Proxy (nginx/cloudflare) ──→ Backend servers
           ↑
           • SSL termination
           • Load balancing
           • Caching
           • Rate limiting  
           • Security (hide backend)
           • Compression
```

### Nginx Reverse Proxy Config

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    ssl_certificate /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;
    
    # API → backend servers
    location /api/ {
        proxy_pass http://127.0.0.1:3000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_read_timeout 60s;
        proxy_send_timeout 60s;
        
        # Buffer settings
        proxy_buffering on;
        proxy_buffer_size 16k;
    }
    
    # Static files served by Nginx directly
    location /static/ {
        root /var/www;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    location /api/auth/ {
        limit_req zone=api burst=20;
        proxy_pass http://127.0.0.1:3000/auth/;
    }
}
```

---

## 3. API Gateway — Reverse Proxy cho Microservices

```
Client ──→ API Gateway ──→ User Service    (/api/users)
                       ──→ Order Service   (/api/orders)
                       ──→ Product Service (/api/products)

API Gateway handles:
  • Routing (URL path → service)
  • Authentication (validate JWT)
  • Rate limiting (100 req/min/user)
  • Request/Response transformation
  • Circuit breaking
  • Logging & monitoring
```

### Popular API Gateways

| Gateway | Type | Best for |
|---|---|---|
| **Kong** | Open source | General purpose, plugin ecosystem |
| **AWS API Gateway** | Managed | AWS Lambda integration |
| **Traefik** | Open source | Docker/K8s native |
| **Nginx** | Open source | Simple reverse proxy + gateway |
| **Envoy** | Open source | Service mesh sidecar |

---

## 4. So sánh Forward vs Reverse

| | Forward Proxy | Reverse Proxy |
|---|---|---|
| **Vị trí** | Client-side | Server-side |
| **Client biết?** | Biết proxy | Không biết backend servers |
| **Server biết?** | Không biết client | Biết proxy |
| **Bảo vệ** | Client (ẩn danh) | Server (hide topology) |
| **Ví dụ** | VPN, Squid, Tor | Nginx, HAProxy, CDN |

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Quên `X-Forwarded-For` header | Proxy phải forward client IP | Backend log proxy IP thay vì client IP |
| 2 | `proxy_pass http://backend` (không trailing slash) | Cẩn thận trailing slash behavior | `/api` vs `/api/` → Nginx behaves differently |
| 3 | Timeout quá ngắn cho long requests | Set timeout phù hợp (60s cho API, 300s cho uploads) | Large file uploads timeout |
| 4 | Forward POST body bị mất | Đảm bảo `proxy_pass_request_body on` | Default on, nhưng check nếu custom config |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** Setup Nginx reverse proxy cho Node.js/Python app
- [ ] **Bài 2 (Trung bình):** Config SSL termination + static file serving tại Nginx
- [ ] **Bài 3 (Trung bình):** Setup SSH SOCKS5 proxy, duyệt web qua tunnel
- [ ] **Bài 4 (Khó):** Config API Gateway (Nginx/Traefik) cho 3 microservices với rate limiting

---

## Tài nguyên thêm

- [Nginx Reverse Proxy Guide](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/) — Official docs
- [Traefik Documentation](https://doc.traefik.io/traefik/) — Docker/K8s proxy
- [Cloudflare — What is a Proxy?](https://www.cloudflare.com/learning/cdn/glossary/reverse-proxy/) — Visual explanation
