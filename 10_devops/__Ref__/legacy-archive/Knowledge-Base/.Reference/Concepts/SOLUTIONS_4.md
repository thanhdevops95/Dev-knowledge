# Solutions: Module 03 - NETWORKING INTRO

> **Đáp Án Đầy Đủ Networking**

---

## EXERCISES SOLUTIONS

### Phần A: Trắc Nghiệm

1. **B** - 192.168.1.1 là private IP
2. **A** - Port 80 cho HTTP
3. **C** - DNS chuyển domain thành IP
4. **B** - netstat hiển thị open ports
5. **C** - ping test connectivity
6. **A** - UFW là firewall
7. **B** - Port 443 cho HTTPS
8. **C** - localhost = 127.0.0.1
9. **A** - nslookup cho DNS lookup
10. **B** - curl thực hiện HTTP requests

### Phần B: Điền Vào Chỗ Trống

1. `ping google.com` - Test connectivity
2. `netstat -tulpn` - Show listening ports
3. `sudo ufw allow 80` - Allow HTTP
4. `nslookup example.com` - DNS lookup
5. `curl https://api.example.com` - HTTP request
6. `traceroute 8.8.8.8` - Show network path
7. `sudo systemctl restart nginx` - Restart service
8. `dig example.com` - DNS query
9. `telnet localhost 80` - Test port
10. `sudo lsof -i :5000` - Check process on port

### Phần C: Thực Hành

**Port Checking:**

```bash
netstat -tulpn | grep LISTEN
ss -tulpn
```

**DNS Troubleshooting:**

```bash
nslookup domain.com
dig domain.com
cat /etc/resolv.conf
```

**Firewall Setup:**

```bash
sudo ufw enable
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
```

---

## SCENARIOS SOLUTIONS

**Scenario 1: Database Connection**

- Nguyên nhân: UFW block port 5432
- Fix: `sudo ufw allow 5432`

**Scenario 2: DNS Issues**  

- Nguyên nhân: DNS server sai
- Fix: Sửa /etc/resolv.conf

**Scenario 3: SSH Blocked**

- Nguyên nhân: Enable UFW mà không allow 22
- Fix: Console access, `sudo ufw allow 22`

**Scenario 4: API Slow**

- Nguyên nhân: Network latency
- Fix: Use CDN

**Scenario 5: SSL Expired**

- Nguyên nhân: Certificate hết hạn
- Fix: `sudo certbot renew`

---

## QUIZ SOLUTIONS

1-C, 2-B, 3-C, 4-A, 5-B, 6-A, 7-B, 8-C, 9-A, 10-B
11-C, 12-A, 13-B, 14-C, 15-A, 16-B, 17-C, 18-A, 19-B, 20-C

---

## KEY COMMANDS REFERENCE

| Command | Purpose |
|---------|---------|
| `ping` | Test connectivity |
| `netstat -tulpn` | Show ports |
| `nslookup` | DNS lookup |
| `dig` | DNS query |
| `curl` | HTTP request |
| `ufw` | Firewall |
| `traceroute` | Network path |
| `telnet` | Port test |

---

**Master these commands = Debug any network issue! 🌐**
