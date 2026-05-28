# ⚖️ Load Balancing — Cân bằng tải

> `[INTERMEDIATE]` — Prerequisite: hiểu HTTP, TCP/IP cơ bản
> Kỹ thuật phân phối traffic giữa nhiều servers.

---

## Tại sao cần Load Balancing?

Hãy tưởng tượng quán phở chỉ có **1 đầu bếp**. 5 khách → OK. 500 khách → xếp hàng chờ hàng giờ. Giải pháp? Thêm đầu bếp + **1 người điều phối** (load balancer) phân khách đều cho từng bếp.

```
Không có LB:                    Có Load Balancer:
                                        ┌── Server 1 ←─┐
Users ──→ Single Server 💀     Users ──→ │  LB          │
          (overloaded)                   └── Server 2 ←─┤
                                         └── Server 3 ←─┘
```

**Load Balancer** giải quyết:
- **High Availability** — 1 server chết, traffic chuyển sang server khác
- **Scalability** — thêm server sau LB khi traffic tăng
- **Performance** — phân load đều, giảm response time

---

## 1. Layer 4 vs Layer 7 Load Balancing

| | L4 (Transport) | L7 (Application) |
|---|---|---|
| **Hoạt động tại** | TCP/UDP level | HTTP/HTTPS level |
| **Quyết định dựa trên** | IP, port, TCP connection | URL, headers, cookies, body |
| **Tốc độ** | Rất nhanh (ít overhead) | Chậm hơn (phải đọc HTTP) |
| **Tính năng** | Đơn giản, raw throughput | Routing thông minh, SSL termination |
| **Ví dụ** | AWS NLB, HAProxy TCP mode | AWS ALB, Nginx, HAProxy HTTP |

```
L4 Load Balancer:
Client ──TCP──→ LB ──TCP──→ Server
  • Chỉ nhìn IP:Port
  • Forward raw TCP packets
  • Không hiểu HTTP

L7 Load Balancer:
Client ──HTTPS──→ LB ──HTTP──→ Server
  • Đọc HTTP headers, URL path
  • SSL termination tại LB
  • Route /api → API servers, /static → CDN
```

---

## 2. Thuật toán Load Balancing

### Round Robin — Luân phiên

```
Request 1 → Server A
Request 2 → Server B
Request 3 → Server C
Request 4 → Server A  (quay lại)
Request 5 → Server B
...

✅ Đơn giản, công bằng
❌ Không biết server nào đang bận
```

### Weighted Round Robin

```
Server A (weight=3): nhận 3/6 = 50% requests
Server B (weight=2): nhận 2/6 = 33% requests
Server C (weight=1): nhận 1/6 = 17% requests

Sequence: A, A, A, B, B, C, A, A, A, B, B, C ...

✅ Cho phép servers mạnh nhận nhiều traffic hơn
```

### Least Connections

```
Server A: 15 active connections
Server B: 5 active connections   ← next request goes here
Server C: 10 active connections

✅ Phân tải dựa trên load thực tế
✅ Tốt cho long-lived connections (WebSocket, database)
❌ Connections không bằng nhau (1 conn có thể heavy hơn khác)
```

### IP Hash (Sticky Sessions)

```
hash(client_ip) % num_servers = target_server

Client 1 (IP: 10.0.0.1): hash → Server A (luôn luôn)
Client 2 (IP: 10.0.0.2): hash → Server C (luôn luôn)

✅ Session persistence — cùng client luôn đến cùng server
✅ Tốt cho stateful applications
❌ Uneven distribution nếu 1 IP gửi nhiều requests
```

### Consistent Hashing

```
Servers và requests được đặt trên vòng tròn hash:

         Server A
        /
  ─────●──────────●───── Server B
       |          |
  ─────●──────────●─────
        \        /
         Server C

Request hash → đi theo chiều kim đồng hồ → server gần nhất

Thêm/xóa server: chỉ ảnh hưởng requests ở vùng lân cận
(không cache miss toàn bộ như IP Hash!)

✅ Minimal disruption khi add/remove servers
✅ Dùng trong Redis Cluster, DynamoDB
❌ Phức tạp hơn để implement
```

---

## 3. Health Checks — Kiểm tra sức khỏe server

```
LB liên tục kiểm tra servers:

Active Health Check:
  LB gửi HTTP GET /health mỗi 5 giây
  200 OK → server healthy
  500/timeout → server unhealthy → remove khỏi pool

Passive Health Check:
  LB theo dõi responses từ real traffic
  Nhiều 5xx errors → đánh dấu unhealthy

Health endpoint:
  GET /health → {"status": "ok", "db": "connected", "cache": "connected"}
```

```nginx
# Nginx health check
upstream backend {
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080 backup;  # Chỉ dùng khi others down
}

server {
    location / {
        proxy_pass http://backend;
        proxy_next_upstream error timeout;  # Retry on failure
    }
}
```

---

## 4. Connection Draining — Graceful Shutdown

```
Khi cần tắt server (deploy, maintenance):

❌ Hard shutdown: drop tất cả connections → users thấy error

✅ Connection Draining:
  1. LB ngừng gửi NEW requests đến server
  2. Server xử lý hết EXISTING requests (timeout: 30-300s)
  3. Khi không còn active connections → tắt server an toàn

Timeline:
  t=0:  Bắt đầu drain
  t=0+: New requests → other servers
  t=30s: Remaining requests finish
  t=30s: Server shuts down cleanly
```

---

## 5. SSL/TLS Termination

```
Option 1: SSL Termination at LB (phổ biến nhất)
  Client ──HTTPS──→ LB ──HTTP──→ Backend servers
  • LB xử lý SSL, backend nhận HTTP
  • Giảm CPU load cho backend
  • Dễ quản lý certificates

Option 2: SSL Passthrough
  Client ──HTTPS──→ LB ──HTTPS──→ Backend servers
  • LB forward TCP packets, không decrypt
  • End-to-end encryption
  • Backend tự xử lý SSL

Option 3: SSL Re-encryption
  Client ──HTTPS──→ LB ──HTTPS──→ Backend servers
  • LB decrypt → inspect → re-encrypt
  • Vừa inspect traffic, vừa encrypt to backend
  • Most overhead
```

---

## 6. Nginx Config Ví dụ

```nginx
# /etc/nginx/nginx.conf
upstream api_servers {
    least_conn;                    # Thuật toán
    
    server 10.0.0.1:8080 weight=3;
    server 10.0.0.2:8080 weight=2;
    server 10.0.0.3:8080 weight=1;
    server 10.0.0.4:8080 backup;   # Fallback server
    
    keepalive 64;                  # Connection pooling
}

server {
    listen 443 ssl http2;
    server_name api.example.com;
    
    ssl_certificate /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;
    
    location /api/ {
        proxy_pass http://api_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 5s;
        proxy_read_timeout 60s;
        proxy_next_upstream error timeout http_502 http_503;
    }
    
    location /static/ {
        root /var/www;
        expires 30d;
    }
}
```

---

## 7. Cloud Load Balancers

| Cloud | L4 | L7 | Global |
|---|---|---|---|
| **AWS** | NLB (Network LB) | ALB (Application LB) | Global Accelerator |
| **GCP** | Network LB | HTTP(S) LB | Cloud CDN + LB |
| **Azure** | Azure LB | Application Gateway | Front Door |

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | LB là single point of failure | Deploy LB dạng HA (active-passive hoặc active-active) | LB chết → toàn bộ hệ thống down |
| 2 | Round Robin cho stateful app | Dùng sticky sessions hoặc externalize state (Redis) | Session mất khi chuyển server |
| 3 | Không health check | Luôn config health check | Requests gửi đến dead server |
| 4 | SSL termination không set `X-Forwarded-Proto` | Set header để backend biết original protocol | Backend cần biết client dùng HTTP hay HTTPS |

---

## Bài tập thực hành

- [ ] **Bài 1 (Trung bình):** Setup Nginx reverse proxy + upstream với 2 backend servers
- [ ] **Bài 2 (Trung bình):** Config health check + weighted load balancing trên Nginx
- [ ] **Bài 3 (Khó):** So sánh Round Robin vs Least Connections bằng load test (k6/wrk)
- [ ] **Bài 4 (Khó):** Setup AWS ALB với target groups, health checks, và auto scaling

---

## Tài nguyên thêm

- [Nginx Load Balancing Guide](https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/) — Official docs
- [HAProxy Configuration Manual](https://www.haproxy.org/download/2.8/doc/configuration.txt) — Advanced LB
- [AWS Elastic Load Balancing](https://aws.amazon.com/elasticloadbalancing/) — Cloud LB
- [System Design — Load Balancer (ByteByteGo)](https://www.youtube.com/c/ByteByteGo) — Video giải thích
