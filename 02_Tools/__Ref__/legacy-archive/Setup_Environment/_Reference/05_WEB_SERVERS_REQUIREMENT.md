# Module 05: WEB SERVERS (NGINX, APACHE)

> **"Web server là lễ tân của ứng dụng - điểm tiếp xúc đầu tiên với users"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu web server hoạt động như thế nào
- ✅ Cấu hình NGINX từ cơ bản đến nâng cao
- ✅ Setup Reverse Proxy
- ✅ Cấu hình Load Balancing
- ✅ SSL/TLS và HTTPS với Let's Encrypt
- ✅ Performance tuning
- ✅ Apache cơ bản
- ✅ HAProxy basics

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| Web Server | Web Server | Phần mềm phục vụ HTTP requests |
| NGINX | NGINX | Web server phổ biến, nhẹ |
| Apache | Apache HTTP Server | Web server lâu đời |
| Reverse Proxy | Reverse Proxy | Proxy đứng trước backend |
| Load Balancer | Load Balancer | Phân phối traffic |
| Upstream | Upstream | Backend servers |
| Virtual Host | Virtual Host | Nhiều sites trên 1 server |
| SSL | Secure Sockets Layer | Mã hóa kết nối |
| TLS | Transport Layer Security | SSL version mới |
| HTTPS | HTTP Secure | HTTP + SSL/TLS |
| Certificate | SSL Certificate | Chứng chỉ bảo mật |
| CA | Certificate Authority | Đơn vị cấp chứng chỉ |
| Let's Encrypt | Let's Encrypt | CA miễn phí |
| Certbot | Certbot | Tool tự động SSL |
| Round Robin | Round Robin | Thuật toán LB đơn giản |
| Least Connections | Least Connections | LB theo connections |
| Health Check | Health Check | Kiểm tra backend health |
| Caching | Caching | Lưu cache response |
| Gzip | Gzip Compression | Nén dữ liệu |

---

## ✅ Checklist Labs

### Labs NGINX cơ bản

- [ ] Lab 1: Cài đặt NGINX (apt, yum)
- [ ] Lab 2: NGINX directories và file structure
- [ ] Lab 3: Start, stop, reload NGINX
- [ ] Lab 4: Test configuration syntax
- [ ] Lab 5: Serve static files

### Labs NGINX Configuration

- [ ] Lab 6: Server blocks (virtual hosts)
- [ ] Lab 7: Location blocks và matching
- [ ] Lab 8: Root vs Alias
- [ ] Lab 9: Index và try_files
- [ ] Lab 10: Custom error pages
- [ ] Lab 11: Access logs và Error logs
- [ ] Lab 12: Log format customization

### Labs Reverse Proxy

- [ ] Lab 13: Basic reverse proxy setup
- [ ] Lab 14: Proxy headers (X-Forwarded-For, X-Real-IP)
- [ ] Lab 15: Proxy timeouts configuration
- [ ] Lab 16: WebSocket proxy
- [ ] Lab 17: Proxy buffering

### Labs Load Balancing

- [ ] Lab 18: Round-robin load balancing
- [ ] Lab 19: Least connections
- [ ] Lab 20: IP hash (session persistence)
- [ ] Lab 21: Weighted load balancing
- [ ] Lab 22: Health checks
- [ ] Lab 23: Backup servers

### Labs SSL/TLS

- [ ] Lab 24: Self-signed certificate creation
- [ ] Lab 25: Configure HTTPS với self-signed cert
- [ ] Lab 26: Let's Encrypt với Certbot
- [ ] Lab 27: Auto-renewal setup
- [ ] Lab 28: Certificate chain và intermediates
- [ ] Lab 29: SSL/TLS optimization (protocols, ciphers)
- [ ] Lab 30: HSTS và security headers
- [ ] Lab 31: HTTP to HTTPS redirect

### Labs Performance

- [ ] Lab 32: Gzip compression
- [ ] Lab 33: Static file caching (expires, cache-control)
- [ ] Lab 34: Browser caching headers
- [ ] Lab 35: Worker processes tuning
- [ ] Lab 36: Connection limits
- [ ] Lab 37: Rate limiting

### Labs Apache

- [ ] Lab 38: Apache installation
- [ ] Lab 39: Apache virtual hosts
- [ ] Lab 40: mod_proxy reverse proxy
- [ ] Lab 41: .htaccess và mod_rewrite

### Labs HAProxy

- [ ] Lab 42: HAProxy installation
- [ ] Lab 43: HAProxy frontend và backend
- [ ] Lab 44: HAProxy health checks
- [ ] Lab 45: HAProxy statistics page

---

## 🚨 Checklist Scenarios

### Scenarios về Configuration

- [ ] Scenario 1: NGINX không start - syntax error
- [ ] Scenario 2: Configuration reload không apply
- [ ] Scenario 3: Wrong server block được match
- [ ] Scenario 4: Location matching không như expected
- [ ] Scenario 5: 502 Bad Gateway sau deploy

### Scenarios về Reverse Proxy

- [ ] Scenario 6: Backend IP không đúng trong logs
- [ ] Scenario 7: Request timeout 504
- [ ] Scenario 8: Response bị cắt truncated
- [ ] Scenario 9: WebSocket connection drop
- [ ] Scenario 10: File upload fails với large files

### Scenarios về Load Balancing

- [ ] Scenario 11: Traffic không distribute đều
- [ ] Scenario 12: Session lost sau mỗi request
- [ ] Scenario 13: Một backend down mà traffic vẫn đến
- [ ] Scenario 14: Health check false positive

### Scenarios về SSL

- [ ] Scenario 15: SSL certificate expired
- [ ] Scenario 16: Certificate chain incomplete
- [ ] Scenario 17: Mixed content warnings
- [ ] Scenario 18: SSL handshake failed
- [ ] Scenario 19: Let's Encrypt renewal failed
- [ ] Scenario 20: Wrong certificate served

### Scenarios về Performance

- [ ] Scenario 21: High CPU usage trên NGINX
- [ ] Scenario 22: Slow response time
- [ ] Scenario 23: Too many open files error
- [ ] Scenario 24: Memory usage cao bất thường

---

## ⏱️ Thời lượng

**Ước tính:** 4-6 giờ

| Phần | Thời gian |
|------|-----------|
| NGINX basics (Labs 1-12) | 1.5 giờ |
| Reverse Proxy (Labs 13-17) | 1 giờ |
| Load Balancing (Labs 18-23) | 1 giờ |
| SSL/TLS (Labs 24-31) | 1.5 giờ |
| Performance + Apache/HAProxy | 1 giờ |
| Scenarios | 1 giờ |

---

## 🔗 Tài liệu tham khảo

- [NGINX Documentation](https://nginx.org/en/docs/)
- [NGINX Config Generator](https://www.digitalocean.com/community/tools/nginx)
- [SSL Labs Test](https://www.ssllabs.com/ssltest/)
- [Let's Encrypt](https://letsencrypt.org/)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
