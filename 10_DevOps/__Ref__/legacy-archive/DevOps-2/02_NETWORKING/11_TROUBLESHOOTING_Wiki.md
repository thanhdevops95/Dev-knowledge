# 11. Network Troubleshooting

[← Architecture](10_ARCHITECTURE.md) | [Về README →](README.md)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **ping** | - | Công cụ kiểm tra kết nối mạng bằng ICMP |
| **traceroute** | - | Công cụ hiển thị đường đi của packet qua mạng |
| **nslookup** | - | Công cụ tra cứu DNS |
| **dig** | - | Công cụ DNS nâng cao hơn nslookup |
| **telnet** | - | Công cụ kiểm tra kết nối TCP đến port |
| **netcat (nc)** | - | Công cụ mạng đa năng, quét port |
| **curl** | - | Công cụ gửi HTTP request từ command line |
| **wget** | - | Công cụ tải file qua HTTP/FTP |
| **ss** | - | Công cụ xem các socket và port đang listen |
| **netstat** | - | Công cụ xem kết nối mạng (cũ hơn ss) |
| **TTL** | - | Time To Live - Số hop còn lại của packet |
| **ICMP** | - | Internet Control Message Protocol - Giao thức của ping |
| **Latency** | - | Độ trễ - Thời gian để packet đi từ A đến B |

---

# 🤔 Tại sao DevOps cần biết Network Troubleshooting?

## Nỗi đau thực tế

> "App không connect được database, không biết debug từ đâu"

> "Sếp hỏi: Tại sao website chậm? Mà không biết cách tìm nguyên nhân"

> "Container A không gọi được Container B, có phải lỗi network?"

## Kiến thức này giúp bạn

| Tình huống | Cần biết |
|------------|----------|
| Kiểm tra DNS | nslookup, dig |
| Kiểm tra kết nối mạng | ping, traceroute |
| Kiểm tra port có mở không | telnet, nc, ss |
| Debug HTTP/API | curl -v |
| Tìm bottleneck mạng | traceroute, latency analysis |

Troubleshooting là kỹ năng mà DevOps dùng hàng ngày. Khi có sự cố, bạn cần nhanh chóng xác định nguyên nhân nằm ở layer nào để tìm hướng xử lý.

---

# 🔧 Methodology: Check từng Layer

```
┌─────────────────────────────────────────────────────────────┐
│              NETWORK TROUBLESHOOTING LAYERS                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 7 (Application)  ← curl, wget                        │
│           ↑                                                  │
│  Layer 4 (Transport)    ← telnet, nc (port connectivity)   │
│           ↑                                                  │
│  Layer 3 (Network)      ← ping, traceroute, nslookup       │
│           ↑                                                  │
│  Layer 2/1 (Link/Phys)  ← cable, interface, ARP            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

# 🔹 Check Layer 3: Network Connectivity

## nslookup - DNS Resolution

```bash
# Check DNS resolution
nslookup google.com

# Output:
Server:         8.8.8.8
Address:        8.8.8.8#53

Non-authoritative answer:
Name:   google.com
Address: 142.250.190.14
```

## dig - Detailed DNS

```bash
# Basic query
dig google.com

# Query specific record type
dig google.com MX
dig google.com TXT

# Short answer only
dig +short google.com

# Trace full resolution path
dig +trace google.com
```

## Check DNS Resolver của máy

**Linux:**

```bash
cat /etc/resolv.conf

# Output:
nameserver 8.8.8.8
nameserver 8.8.4.4

# Hoặc với systemd-resolved
resolvectl status
```

**Windows:**

```powershell
Get-DnsClientServerAddress
# Hoặc
ipconfig /all | findstr "DNS"
```

**macOS:**

```bash
scutil --dns | grep nameserver
```

## ping - ICMP Connectivity

```bash
# Basic ping
ping google.com

# Output:
PING google.com (142.250.190.14): 56 data bytes
64 bytes from 142.250.190.14: icmp_seq=0 ttl=117 time=10.5 ms
64 bytes from 142.250.190.14: icmp_seq=1 ttl=117 time=11.2 ms

# ttl=117: Time To Live (hops còn lại)
# time=10.5 ms: Round-trip latency
```

```bash
# Ping với số lần cụ thể
ping -c 4 google.com
```

## traceroute - Path to Destination

```bash
traceroute google.com

# Output:
 1  192.168.1.1     1.123 ms    ← Router nhà
 2  10.0.0.1        5.456 ms    ← ISP gateway
 3  ...                          ← Internet backbone
14  142.250.190.14  15.789 ms   ← Destination
```

---

# 🔹 Check Layer 4: Port Connectivity

## telnet - TCP Port Check

```bash
# Check if port is open
telnet google.com 443

# Output (success):
Trying 142.250.190.14...
Connected to google.com.
Escape character is '^]'.

# Để thoát: Ctrl+] rồi gõ 'quit'

# Output (fail):
telnet: connect to address: Connection refused
```

## nc (netcat) - Port Testing

```bash
# Check single port
nc -zv google.com 443

# Output:
Connection to google.com 443 port [tcp/https] succeeded!

# Check port range
nc -zv localhost 20-25

# Listen on a port (for testing)
nc -l 8080
```

## ss / netstat - Local Ports

```bash
# Show listening ports
ss -tuln

# Output:
State    Local Address:Port   Peer Address:Port
LISTEN   0.0.0.0:22            0.0.0.0:*
LISTEN   0.0.0.0:80            0.0.0.0:*
LISTEN   127.0.0.1:6379        0.0.0.0:*

# Flags:
# -t: TCP
# -u: UDP
# -l: Listening only
# -n: Numeric (no DNS)
```

---

# 🔹 Check Layer 7: Application

## curl - HTTP/HTTPS Requests

```bash
# Simple GET
curl https://google.com

# Output (301 redirect):
<HTML><HEAD>
<TITLE>301 Moved</TITLE></HEAD><BODY>
The document has moved <A HREF="https://www.google.com/">here</A>.
</BODY></HTML>

# Follow redirects
curl -L https://google.com

# Show headers only
curl -I https://google.com

# Verbose mode (debug TLS, headers)
curl -v https://api.example.com

# POST request
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"name":"test"}' \
     https://api.example.com/users
```

## wget - Download Files

```bash
# Download file
wget https://example.com/file.zip

# Download với custom name
wget -O myfile.zip https://example.com/file.zip

# Test connectivity (không download)
wget --spider https://google.com
```

---

# 📋 Quick Reference

| Layer | Check | Tool | Command |
|-------|-------|------|---------|
| **L3** | DNS resolution | nslookup | `nslookup google.com` |
| **L3** | DNS details | dig | `dig google.com` |
| **L3** | Connectivity | ping | `ping google.com` |
| **L3** | Path | traceroute | `traceroute google.com` |
| **L4** | Port open | telnet | `telnet google.com 443` |
| **L4** | Port scan | nc | `nc -zv google.com 443` |
| **L4** | Local ports | ss | `ss -tuln` |
| **L7** | HTTP | curl | `curl https://google.com` |
| **L7** | Download | wget | `wget https://example.com/file` |

---

# 🔍 Common Issues

| Symptom | Check | Possible Cause |
|---------|-------|----------------|
| Can't resolve domain | nslookup fails | DNS misconfigured |
| Can't ping | ping fails | Firewall, no route |
| Port not accessible | telnet fails | Service not running, firewall |
| HTTP error | curl shows 4xx/5xx | Application issue |
| Slow response | high ping latency | Network congestion |

---

[← Architecture](10_ARCHITECTURE.md) | [Về README →](README.md)
