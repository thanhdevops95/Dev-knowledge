# Networking Basics - Cheatsheet

> **Quick reference cho networking essentials**

---

## 🌐 IP ADDRESSES

```bash
# Find your public IP
curl ifconfig.me
curl icanhazip.com

# Find your private IP
ip addr show          # Linux
ifconfig              # macOS/older Linux

# Test connectivity
ping 8.8.8.8          # Test Internet
ping google.com       # Test DNS + Internet
```

**IP Ranges:**

```
Private (not routable on Internet):
10.0.0.0      - 10.255.255.255
172.16.0.0    - 172.31.255.255
192.168.0.0   - 192.168.255.255

Special:
127.0.0.1     Localhost (loopback)
0.0.0.0       All interfaces
```

---

## 🚪 PORTS

**Common Ports:**

```
20/21   FTP
22      SSH        ⭐
23      Telnet     (insecure, avoid)
25      SMTP
53      DNS
80      HTTP       ⭐
110     POP3
143     IMAP
443     HTTPS      ⭐
3306    MySQL
5432    PostgreSQL
6379    Redis
27017   MongoDB
3000    Node.js dev
5000    Flask
8080    Alt HTTP
8443    Alt HTTPS
```

**Check ports:**

```bash
# What's listening?
sudo netstat -tulpn
sudo ss -tulpn
sudo lsof -i :PORT

# Is port open?
nc -zv HOST PORT
telnet HOST PORT

# Examples
sudo lsof -i :80        # What's on port 80?
nc -zv google.com 443   # Can I reach Google HTTPS?
```

---

## 🌍 DNS

**Lookup commands:**

```bash
# Quick lookup
nslookup google.com

# Detailed info
dig google.com

# Specific record
dig google.com A        # IPv4
dig google.com AAAA     # IPv6
dig google.com MX       # Mail servers
dig google.com CNAME    # Canonical name

# Reverse lookup (IP → domain)
dig -x 8.8.8.8

# Query specific DNS server
dig @8.8.8.8 google.com
```

**DNS Record Types:**

```
A       Domain → IPv4
AAAA    Domain → IPv6
CNAME   Domain → Domain (alias)
MX      Mail server
TXT     Text (SPF, verification)
NS      Name servers
```

**Common DNS servers:**

```
Google:       8.8.8.8, 8.8.4.4
Cloudflare:   1.1.1.1, 1.0.0.1
Quad9:        9.9.9.9
OpenDNS:      208.67.222.222, 208.67.220.220
```

---

## 📡 HTTP/HTTPS

**HTTP Methods:**

```
GET     Retrieve data
POST    Create new
PUT     Update (full)
PATCH   Update (partial)
DELETE  Remove
HEAD    Get headers only
OPTIONS Check allowed methods
```

**Status Codes:**

```
2xx SUCCESS
200 OK
201 Created
204 No Content

3xx REDIRECTION
301 Moved Permanently
302 Found (temporary)
304 Not Modified

4xx CLIENT ERROR
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
429 Too Many Requests

5xx SERVER ERROR
500 Internal Server Error
502 Bad Gateway
503 Service Unavailable
504 Gateway Timeout
```

**Test HTTP:**

```bash
# Simple request
curl http://example.com

# With headers
curl -I http://example.com

# Verbose (debug)
curl -v https://example.com

# Follow redirects
curl -L http://example.com

# POST request
curl -X POST -d "key=value" http://api.com/endpoint

# Custom header
curl -H "Authorization: Bearer TOKEN" http://api.com
```

---

## 🔥 FIREWALL (UFW)

```bash
# Status
sudo ufw status
sudo ufw status numbered

# Enable/Disable
sudo ufw enable
sudo ufw disable

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow ports
sudo ufw allow 22        # SSH
sudo ufw allow 80        # HTTP
sudo ufw allow 443       # HTTPS
sudo ufw allow 3000      # Custom

# Allow from specific IP
sudo ufw allow from 192.168.1.100

# Allow port from specific IP
sudo ufw allow from 192.168.1.100 to any port 22

# Deny
sudo ufw deny 23         # Block telnet

# Delete rule
sudo ufw status numbered
sudo ufw delete 3        # Delete rule #3

# Reset (careful!)
sudo ufw reset
```

**Common setup:**

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22        # SSH (CRITICAL!)
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

---

## 🔍 TROUBLESHOOTING

**Test connectivity:**

```bash
# Layer 3 (IP)
ping 8.8.8.8            # Internet reachable?
ping 192.168.1.1        # Gateway reachable?

# Layer 4 (TCP/UDP)
nc -zv HOST PORT        # Port open?
telnet HOST PORT        # Interactive test

# Layer 7 (HTTP)
curl http://example.com # Website working?
curl -I http://example.com  # Just headers

# DNS
nslookup domain.com     # Resolves?
dig domain.com          # Detailed info

# Trace route
traceroute google.com   # Path to destination
mtr google.com          # Continuous trace
```

**Debug checklist:**

```
1. ✅ Server running?
   systemctl status SERVICE

2. ✅ Process listening?
   sudo netstat -tulpn | grep PORT

3. ✅ Firewall allows?
   sudo ufw status

4. ✅ Can connect locally?
   curl http://localhost:PORT

5. ✅ DNS resolves?
   nslookup DOMAIN

6. ✅ Can reach from outside?
   curl http://PUBLIC_IP:PORT
```

---

## 📊 NETWORK INFO

```bash
# Network interfaces
ip addr show            # Linux
ifconfig                # macOS/old Linux

# Routing table
ip route show
route -n

# Active connections
netstat -an             # All connections
ss -an                  # Faster alternative

# Bandwidth usage
iftop                   # Real-time
nethogs                 # Per-process

# Network stats
netstat -s              # Statistics
ss -s                   # Summary
```

---

## 🔐 SSL/TLS

**Check certificate:**

```bash
# View certificate
openssl s_client -connect example.com:443

# Check expiry
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# Test SSL
curl -vI https://example.com 2>&1 | grep -i ssl
```

**Let's Encrypt (free SSL):**

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d example.com -d www.example.com

# Auto-renew test
sudo certbot renew --dry-run

# List certificates
sudo certbot certificates
```

---

## 🌐 LOAD BALANCING CONCEPTS

**Algorithms:**

```
Round Robin:
Request 1 → Server 1
Request 2 → Server 2
Request 3 → Server 3
Request 4 → Server 1

Least Connections:
Send to server with fewest active connections

IP Hash:
Same client → Same server
```

**Health Checks:**

```
Active: Load balancer pings servers regularly
Passive: Remove servers that fail requests

Common checks:
- HTTP 200 from /health endpoint
- TCP connection successful
- Response time < threshold
```

---

## 💡 COMMON SCENARIOS

**Scenario 1: Website unreachable**

```bash
# From server
curl http://localhost:80  # Works locally?
sudo netstat -tulpn | grep 80  # Something listening?
sudo ufw status  # Firewall blocking?

# From client
ping SERVER_IP  # Server reachable?
nc -zv SERVER_IP 80  # Port accessible?
curl http://SERVER_IP  # HTTP response?
```

**Scenario 2: DNS not working**

```bash
nslookup example.com  # Resolves?
dig example.com       # Correct IP?

# Try different DNS
dig @8.8.8.8 example.com  # Google DNS
dig @1.1.1.1 example.com  # Cloudflare DNS

# Check local DNS config
cat /etc/resolv.conf
```

**Scenario 3: Slow website**

```bash
# Measure latency
ping example.com

# Trace route
traceroute example.com
mtr example.com

# Check DNS
time nslookup example.com

# Test bandwidth
curl -w "@curl-format.txt" -o /dev/null -s http://example.com
```

---

## 🚨 SECURITY BEST PRACTICES

```bash
# Minimum ports open
sudo ufw default deny incoming  # Block all by default
sudo ufw allow 22               # SSH only
sudo ufw allow 80               # HTTP
sudo ufw allow 443              # HTTPS

# Change SSH port (security through obscurity)
# Edit /etc/ssh/sshd_config
Port 2222                       # Not 22
sudo ufw allow 2222
sudo systemctl restart sshd

# Fail2ban (auto-block attackers)
sudo apt install fail2ban
sudo systemctl enable fail2ban
```

---

## 📝 QUICK TESTS

```bash
# Is port open?
nc -zv example.com 80

# HTTP response code
curl -I -s example.com | head -1

# Response time
curl -w "@-" -o /dev/null -s http://example.com <<< "time_total: %{time_total}s"

# Download speed
curl -o /dev/null http://speedtest.example.com/file.bin

# Multiple requests (load test)
for i in {1..100}; do curl -s http://example.com > /dev/null; done
```

---

<div align="center">

**Network knowledge = DevOps superpower! 🌐💪**

**Bookmark for daily use! 🔖**

</div>
