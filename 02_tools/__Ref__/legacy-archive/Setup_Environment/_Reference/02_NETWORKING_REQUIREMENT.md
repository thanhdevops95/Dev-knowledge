# Module 02: NETWORKING FUNDAMENTALS

> **"Không hiểu Network = Không debug được hệ thống phân tán"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu mô hình TCP/IP và OSI
- ✅ Làm việc với IP addresses, subnets, CIDR
- ✅ Hiểu DNS hoạt động từ A-Z
- ✅ Phân biệt TCP vs UDP và use cases
- ✅ Hiểu HTTP/HTTPS và SSL/TLS cơ bản
- ✅ Debug network với các công cụ CLI
- ✅ Cấu hình Firewall cơ bản
- ✅ Hiểu về Load Balancing và VPC

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| TCP | Transmission Control Protocol | Giao thức truyền tin cậy |
| UDP | User Datagram Protocol | Giao thức truyền nhanh, không tin cậy |
| IP | Internet Protocol | Giao thức định địa chỉ |
| DNS | Domain Name System | Hệ thống phân giải tên miền |
| DHCP | Dynamic Host Configuration Protocol | Cấp phát IP tự động |
| Port | Port Number | Số cổng dịch vụ |
| Subnet | Subnet | Mạng con |
| CIDR | Classless Inter-Domain Routing | Định dạng IP/prefix |
| Gateway | Default Gateway | Cổng ra mặc định |
| Firewall | Firewall | Tường lửa |
| NAT | Network Address Translation | Chuyển đổi địa chỉ |
| VPN | Virtual Private Network | Mạng riêng ảo |
| VPC | Virtual Private Cloud | Mạng riêng trên cloud |
| LB | Load Balancer | Bộ cân bằng tải |
| SSL | Secure Sockets Layer | Lớp bảo mật |
| TLS | Transport Layer Security | Bảo mật tầng vận chuyển |
| HTTPS | HTTP Secure | HTTP có mã hóa |
| Latency | Latency | Độ trễ mạng |
| Bandwidth | Bandwidth | Băng thông |
| Packet | Network Packet | Gói tin mạng |

---

## ✅ Checklist Labs

### Labs về IP & Subnetting

- [ ] Lab 1: Xem cấu hình network (ip addr, ifconfig)
- [ ] Lab 2: Tính toán subnet và CIDR
- [ ] Lab 3: Cấu hình static IP

### Labs về DNS

- [ ] Lab 4: DNS lookup với nslookup
- [ ] Lab 5: DNS lookup với dig
- [ ] Lab 6: Kiểm tra DNS records (A, AAAA, CNAME, MX, TXT)
- [ ] Lab 7: Cấu hình /etc/hosts và /etc/resolv.conf

### Labs về Connectivity Testing

- [ ] Lab 8: Kiểm tra kết nối với ping
- [ ] Lab 9: Trace route với traceroute/tracepath
- [ ] Lab 10: Kiểm tra ports với netstat/ss
- [ ] Lab 11: Kiểm tra ports từ xa với nc (netcat)
- [ ] Lab 12: Kiểm tra ports với telnet
- [ ] Lab 13: Capture packets với tcpdump

### Labs về HTTP

- [ ] Lab 14: HTTP requests với curl (GET, POST, PUT, DELETE)
- [ ] Lab 15: Phân tích HTTP headers
- [ ] Lab 16: Test API với curl
- [ ] Lab 17: Download files với wget/curl

### Labs về Firewall

- [ ] Lab 18: iptables cơ bản - list rules
- [ ] Lab 19: iptables - thêm/xóa rules
- [ ] Lab 20: UFW (Uncomplicated Firewall) trên Ubuntu
- [ ] Lab 21: Firewall-cmd trên CentOS/RHEL

### Labs về Advanced

- [ ] Lab 22: SSH tunneling (port forwarding)
- [ ] Lab 23: SCP và SFTP file transfer
- [ ] Lab 24: MTR (My Traceroute) - combined ping + traceroute

---

## 🚨 Checklist Scenarios

### Scenarios về DNS

- [ ] Scenario 1: Domain không resolve được
- [ ] Scenario 2: DNS propagation delay sau khi đổi record
- [ ] Scenario 3: DNS cache gây truy cập sai IP
- [ ] Scenario 4: nslookup works nhưng curl fails

### Scenarios về Connectivity

- [ ] Scenario 5: Ping works nhưng HTTP không vào được
- [ ] Scenario 6: Connection refused error
- [ ] Scenario 7: Connection timeout error
- [ ] Scenario 8: Intermittent connection drops
- [ ] Scenario 9: High latency giữa 2 servers

### Scenarios về Ports & Services

- [ ] Scenario 10: Port 80/443 không mở
- [ ] Scenario 11: Service listening on localhost only
- [ ] Scenario 12: Port conflict - Address already in use
- [ ] Scenario 13: Firewall block traffic trong security group

### Scenarios về SSL/TLS

- [ ] Scenario 14: SSL certificate expired
- [ ] Scenario 15: SSL certificate mismatch (wrong domain)
- [ ] Scenario 16: Mixed content warning (HTTP trong HTTPS)
- [ ] Scenario 17: SSL handshake failed

### Scenarios về Performance

- [ ] Scenario 18: Network bandwidth saturation
- [ ] Scenario 19: Packet loss gây slow response
- [ ] Scenario 20: MTU mismatch causing fragmentation

---

## ⏱️ Thời lượng

**Ước tính:** 4-6 giờ

| Phần | Thời gian |
|------|-----------|
| Lý thuyết TCP/IP, DNS | 1 giờ |
| Labs 1-7: IP & DNS | 1 giờ |
| Labs 8-17: Connectivity & HTTP | 1.5 giờ |
| Labs 18-24: Firewall & Advanced | 1 giờ |
| Scenarios | 1.5 giờ |

---

## 🔗 Tài liệu tham khảo

- [Computer Networking - Crash Course](https://www.youtube.com/watch?v=qiQR5rTSshw)
- [How DNS Works](https://howdns.works/)
- [High Performance Browser Networking](https://hpbn.co/)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
