# Module 03: NETWORKING INTRO - Hiểu cách máy tính giao tiếp

> **Thời gian học:** 1 tuần
>
> **Prerequisite:** Module 01 (Linux Basics)
>
> **Difficulty:** ⭐⭐☆☆☆

---

## 📋 Mục lục

1. [Networking Fundamentals](#1-networking-fundamentals)
2. [OSI Model & TCP/IP](#2-osi-model--tcpip)
3. [IP Addresses & Subnetting](#3-ip-addresses--subnetting)
4. [Ports & Sockets](#4-ports--sockets)
5. [DNS - Domain Name System](#5-dns---domain-name-system)
6. [HTTP/HTTPS](#6-httphttps)
7. [SSH - Secure Shell](#7-ssh---secure-shell)
8. [Network Troubleshooting](#8-network-troubleshooting)

---

## 🎯 Learning Objectives

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu **OSI model** và **TCP/IP stack**
- ✅ Phân biệt **IPv4 vs IPv6**
- ✅ Tính toán **subnets** và **CIDR notation**
- ✅ Hiểu **ports** và cách applications communicate
- ✅ Giải thích **DNS resolution** từ domain → IP
- ✅ Phân biệt **HTTP vs HTTPS**, hiểu TLS/SSL
- ✅ Sử dụng **SSH** để remote access
- ✅ Troubleshoot network issues với **ping, traceroute, netstat**

---

## 1. Networking Fundamentals

### 1.1. Tại sao cần Networks?

**Without networks:**

- Máy tính hoạt động isolated
- Không share resources
- Không communicate

**With networks:**

- ✅ Share files, printers
- ✅ Internet access
- ✅ Email, messaging
- ✅ Cloud services
- ✅ Distributed systems (DevOps!)

### 1.2. Types of Networks

**By scale:**

| Type | Coverage | Example |
|------|----------|---------|
| **PAN** (Personal Area Network) | ~10m | Bluetooth devices |
| **LAN** (Local Area Network) | Building/Campus | Office network |
| **MAN** (Metropolitan Area Network) | City | City-wide fiber |
| **WAN** (Wide Area Network) | Country/Global | Internet |

**DevOps context:**

```
Developer laptop (PAN)
    ↓
Office LAN
    ↓
Internet (WAN)
    ↓
Cloud data center (LAN)
    ↓
Your application servers
```

### 1.3. Network Topologies

**Star (en phổ biến):**

```
     Switch
    /  |  \
   A   B   C
```

- Pro: Failure of one device doesn't affect others
- Con: If switch fails, entire network down

**Mesh (cloud networks):**

```
A---B
|\ /|
| X |
|/ \|
C---D
```

- Pro: Redundancy, multiple paths
- Con: Complex, expensive

---

## 2. OSI Model & TCP/IP

### 2.1. OSI Model (7 Layers)

**Open Systems Interconnection:**

```
7. Application    ← HTTP, FTP, SSH, DNS
6. Presentation   ← Encryption, compression
5. Session        ← Connection management
4. Transport      ← TCP, UDP (ports)
3. Network        ← IP addresses, routing
2. Data Link      ← MAC addresses, Ethernet
1. Physical       ← Cables, WiFi, signals
```

**Mnemonic:** "All People Seem To Need Data Processing"

**Example: Web request**

```
Layer 7 (App):    GET /index.html HTTP/1.1
Layer 4 (Trans):  TCP port 80
Layer 3 (Net):    IP: 192.168.1.100 → 93.184.216.34
Layer 2 (Link):   MAC: aa:bb:cc:dd:ee:ff
Layer 1 (Phys):   Electrical signals over Ethernet cable
```

### 2.2. TCP/IP Model (4 Layers)

**Practical model used in reality:**

```
4. Application    ← HTTP, SSH, FTP, DNS (OSI 5-7)
3. Transport      ← TCP, UDP (OSI 4)
2. Internet       ← IP, ICMP (OSI 3)
1. Link           ← Ethernet, WiFi (OSI 1-2)
```

**DevOps cares mostly about:**

- **Application:** HTTP/HTTPS, SSH, DNS
- **Transport:** TCP (reliable) vs UDP (fast)
- **Internet:** IP addresses, routing

### 2.3. TCP vs UDP

**TCP (Transmission Control Protocol):**

```
✅ Reliable (guaranteed delivery)
✅ Ordered packets
✅ Error checking
✅ Connection-oriented (handshake)
❌ Slower

Use cases: HTTP, SSH, FTP, email
```

**TCP 3-way handshake:**

```
Client          Server
  |---SYN------->|
  |<--SYN-ACK----|
  |---ACK------->|
  [Connected]
```

**UDP (User Datagram Protocol):**

```
✅ Fast
✅ Low overhead
❌ No guarantee delivery
❌ No ordering
❌ Connectionless

Use cases: DNS, video streaming, gaming, VoIP
```

**Analogy:**

```
TCP = Registered mail (guaranteed, tracked)
UDP = Postcard (fire and forget)
```

---

## 3. IP Addresses & Subnetting

### 3.1. IPv4 Addresses

**Format:** 4 octets, mỗi octet 0-255

```
192.168.1.100

192      .168      .1        .100
binary:
11000000.10101000.00000001.01100100

Total: 32 bits
```

**Classes (old system, mostly historical):**

| Class | Range | Default Subnet | Use |
|-------|-------|----------------|-----|
| A | 1-126 | /8 (255.0.0.0) | Large networks |
| B | 128-191 | /16 (255.255.0.0) | Medium |
| C | 192-223 | /24 (255.255.255.0) | Small |

**Private IP ranges (not routable on Internet):**

```
10.0.0.0    - 10.255.255.255     (10/8)
172.16.0.0  - 172.31.255.255     (172.16/12)
192.168.0.0 - 192.168.255.255    (192.168/16)

Your home router likely uses: 192.168.1.1
```

**Special addresses:**

```
127.0.0.1       localhost (loopback)
0.0.0.0         Default route / "any"
255.255.255.255 Broadcast
```

### 3.2. Subnet Masks & CIDR

**Subnet mask defines network vs host portions:**

```
IP:      192.168.1.100
Mask:    255.255.255.0

Binary mask:    11111111.11111111.11111111.00000000
                ↑ Network part ↑ ↑ Host part ↑

Network:  192.168.1.0
Hosts:    192.168.1.1 - 192.168.1.254
Broadcast: 192.168.1.255
```

**CIDR (Classless Inter-Domain Routing) notation:**

```
192.168.1.0/24

/24 means first 24 bits are network
= Subnet mask 255.255.255.0

Common CIDR:
/32 = 255.255.255.255  (single host)
/24 = 255.255.255.0    (256 IPs)
/16 = 255.255.0.0      (65,536 IPs)
/8  = 255.0.0.0        (16 million IPs)
```

**Calculate usable IPs:**

```
/24 network:
Total IPs: 2^(32-24) = 2^8 = 256
Usable:    256 - 2 = 254
           (minus network address & broadcast)

First usable: 192.168.1.1
Last usable:  192.168.1.254
```

### 3.3. IPv6

**128 bits (vs IPv4's 32 bits):**

```
2001:0db8:85a3:0000:0000:8a2e:0370:7334

Shortened:
2001:db8:85a3::8a2e:370:7334

Format: 8 groups of 4 hex digits
```

**Why IPv6?**

- IPv4: 4.3 billion addresses (running out)
- IPv6: 340 undecillion addresses (3.4 × 10^38)

**DevOps note:**

- Most apps still use IPv4
- Cloud providers support IPv6
- Dual-stack (IPv4 + IPv6) common

---

## 4. Ports & Sockets

### 4.1. Port Numbers

**Port = Endpoint for communication (0-65535)**

```
Computer IP: 192.168.1.100
Service on port: 80 (HTTP web server)

Full address: 192.168.1.100:80
```

**Port ranges:**

```
0-1023      Well-known ports (system)
1024-49151  Registered ports (applications)
49152-65535 Dynamic/private ports (temporary)
```

### 4.2. Common Ports

**Must know for DevOps:**

| Port | Service | Description |
|------|---------|-------------|
| 20/21 | FTP | File Transfer (control/data) |
| 22 | SSH | Secure Shell |
| 23 | Telnet | Unencrypted shell (avoid!) |
| 25 | SMTP | Email sending |
| 53 | DNS | Domain name resolution |
| 80 | HTTP | Web traffic |
| 110 | POP3 | Email retrieval |
| 143 | IMAP | Email retrieval |
| 443 | HTTPS | Secure web traffic |
| 3306 | MySQL | Database |
| 5432 | PostgreSQL | Database |
| 6379 | Redis | Cache |
| 8080 | HTTP alt | Development web server |
| 27017 | MongoDB | Database |

**Check listening ports:**

```bash
# Linux
sudo netstat -tulpn

# Or
sudo ss -tulpn

# macOS
lsof -i -P -n | grep LISTEN
```

### 4.3. Sockets

**Socket = IP + Port + Protocol**

```
192.168.1.100:80 TCP

Client socket:   192.168.1.50:52341
Server socket:   192.168.1.100:80
Connection:      192.168.1.50:52341 ↔ 192.168.1.100:80
```

**View active connections:**

```bash
netstat -an

# Output:
Proto Local Address      Foreign Address    State
TCP   0.0.0.0:80         0.0.0.0:0          LISTEN
TCP   127.0.0.1:3306     0.0.0.0:0          LISTEN
TCP   192.168.1.100:443  52.1.2.3:41234     ESTABLISHED
```

---

## 5. DNS - Domain Name System

### 5.1. Tại sao cần DNS?

**Problem:**

```
Computers understand: 93.184.216.34
Humans remember:      example.com
```

**DNS = Phone book of Internet:**

```
example.com → 93.184.216.34
```

### 5.2. DNS Resolution Process

**Step-by-step:**

```
1. You type: https://www.google.com

2. Browser checks cache
   - Browser cache
   - OS cache
   
3. If not cached, query DNS resolver
   (usually your ISP's DNS server or 8.8.8.8)

4. Resolver queries root servers
   "Where is .com?"
   → Points to .com TLD servers

5. Query .com TLD servers
   "Where is google.com?"
   → Points to Google's nameservers

6. Query Google's nameservers
   "Where is www.google.com?"
   → Returns: 142.250.185.196

7. Browser connects to 142.250.185.196:443
```

**Visual:**

```
Browser
  ↓
OS DNS cache (check)
  ↓
DNS Resolver (8.8.8.8)
  ↓
Root servers (.)
  ↓
TLD servers (.com)
  ↓
Authoritative nameserver (google.com)
  ↓
IP: 142.250.185.196
```

### 5.3. DNS Record Types

**Common records:**

| Type | Purpose | Example |
|------|---------|---------|
| **A** | Domain → IPv4 | example.com → 93.184.216.34 |
| **AAAA** | Domain → IPv6 | example.com → 2606:2800:220:1:... |
| **CNAME** | Alias | <www.example.com> → example.com |
| **MX** | Mail server | example.com → mail.example.com |
| **TXT** | Text data | SPF, DKIM, verification |
| **NS** | Nameserver | example.com → ns1.provider.com |

**Query DNS records:**

```bash
# A record
dig example.com A
nslookup example.com

# All records
dig example.com ANY

# Specific nameserver
dig @8.8.8.8 example.com

# Reverse lookup (IP → domain)
dig -x 93.184.216.34
```

### 5.4. /etc/hosts Override

**Local DNS override:**

```bash
# Edit /etc/hosts
sudo nano /etc/hosts

# Add:
127.0.0.1   myapp.local
192.168.1.100   dev-server

# Now:
ping myapp.local
# → pings 127.0.0.1
```

**Use case:**

- Local development
- Override DNS for testing
- Block ads (point ad domains to 127.0.0.1)

---

## 6. HTTP/HTTPS

### 6.1. HTTP Basics

**HyperText Transfer Protocol:**

**Request-Response model:**

```
Client                  Server
  |---HTTP Request------>|
  |<--HTTP Response------|
```

**HTTP Request:**

```http
GET /index.html HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: text/html
```

**HTTP Response:**

```http
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1234

<html>...</html>
```

### 6.2. HTTP Methods

| Method | Purpose | Safe | Idempotent |
|--------|---------|------|------------|
| **GET** | Retrieve data | ✅ | ✅ |
| **POST** | Create resource | ❌ | ❌ |
| **PUT** | Update/replace | ❌ | ✅ |
| **PATCH** | Partial update | ❌ | ❌ |
| **DELETE** | Remove resource | ❌ | ✅ |
| **HEAD** | Get headers only | ✅ | ✅ |
| **OPTIONS** | Check methods | ✅ | ✅ |

**Safe:** Doesn't modify data
**Idempotent:** Same result if repeated

### 6.3. HTTP Status Codes

**Categories:**

```
1xx: Informational (100 Continue)
2xx: Success (200 OK, 201 Created)
3xx: Redirection (301 Moved, 302 Found)
4xx: Client error (400 Bad Request, 404 Not Found)
5xx: Server error (500 Internal Error, 502 Bad Gateway)
```

**Common codes:**

```
200 OK                    Everything worked
201 Created               Resource created
204 No Content            Success, no body
301 Moved Permanently     Redirect forever
302 Found                 Temporary redirect
304 Not Modified          Use cached version
400 Bad Request           Invalid request
401 Unauthorized          Need authentication
403 Forbidden             Not allowed
404 Not Found             Resource doesn't exist
500 Internal Server Error Server crashed
502 Bad Gateway           Proxy error
503 Service Unavailable   Server overloaded/down
```

### 6.4. HTTPS = HTTP + TLS/SSL

**Why HTTPS?**

```
HTTP (unencrypted):
Browser → ISP can see:
        GET /login?username=alice&password=secret123

HTTPS (encrypted):
Browser → ISP sees:
        [encrypted gibberish]
```

**TLS/SSL handshake:**

```
1. Client: "Hello, I speak TLS 1.3"
2. Server: "Hello, here's my certificate"
3. Client verifies certificate (CA trust chain)
4. Exchange encryption keys
5. Encrypted communication begins
```

**Certificate:**

```
Issued to: example.com
Issued by: Let's Encrypt (Certificate Authority)
Valid from: 2024-01-01
Valid until: 2024-04-01
Public key: [RSA 2048-bit]
```

**Check cert:**

```bash
# Via browser: Click padlock icon
# Via command:
openssl s_client -connect example.com:443

# Check cert expiry
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
```

---

## 7. SSH - Secure Shell

### 7.1. SSH Basics

**Remote shell access:**

```bash
# Connect to server
ssh user@192.168.1.100

# Or with domain
ssh user@example.com

# Specific port
ssh -p 2222 user@server

# Run single command
ssh user@server 'ls -la'
```

**How it works:**

```
1. Client connects to server:22
2. Server sends public key
3. Client verifies (known_hosts)
4. Authenticate:
   - Password
   - SSH key (better)
5. Encrypted shell session
```

### 7.2. SSH Key Authentication

**Better than passwords:**

```bash
# Generate key pair (if not done)
ssh-keygen -t ed25519 -C "your@email.com"

# Files created:
~/.ssh/id_ed25519      (private key - NEVER share)
~/.ssh/id_ed25519.pub  (public key - can share)

# Copy public key to server
ssh-copy-id user@server

# Or manual:
cat ~/.ssh/id_ed25519.pub | ssh user@server 'cat >> ~/.ssh/authorized_keys'

# Now login without password:
ssh user@server
```

### 7.3. SSH Config

**Simplify connections:**

```bash
# Edit ~/.ssh/config
nano ~/.ssh/config

# Add:
Host dev
    HostName dev-server.example.com
    User admin
    Port 22
    IdentityFile ~/.ssh/id_ed25519

Host prod
    HostName 52.1.2.3
    User deploy
    Port 2222

# Now simply:
ssh dev
ssh prod
```

### 7.4. SCP & SFTP

**Copy files over SSH:**

```bash
# SCP (Secure Copy)
# Upload
scp file.txt user@server:/path/to/destination/

# Download
scp user@server:/path/to/file.txt ./

# Copy directory
scp -r folder/ user@server:/path/

# SFTP (interactive)
sftp user@server
# sftp> put file.txt
# sftp> get remote-file.txt
# sftp> ls
# sftp> quit
```

---

## 8. Network Troubleshooting

### 8.1. `ping` - Test Connectivity

```bash
# Test if host reachable
ping google.com

# Output:
PING google.com (142.250.185.196): 56 data bytes
64 bytes from 142.250.185.196: icmp_seq=0 ttl=117 time=12.3 ms
64 bytes from 142.250.185.196: icmp_seq=1 ttl=117 time=11.8 ms

# Ping 4 times then stop
ping -c 4 google.com

# Ping specific IP
ping 8.8.8.8
```

**What it tells:**

- ✅ Host reachable
- ✅ Latency (time=12.3 ms)
- ❌ If timeout: network issue or firewall blocks ICMP

### 8.2. `traceroute` / `tracert` - Trace Route

```bash
# Linux/macOS
traceroute google.com

# Windows
tracert google.com

# Output shows hops:
 1  192.168.1.1 (1.2 ms)        # Your router
 2  10.0.0.1 (5.3 ms)           # ISP gateway
 3  52.93.1.2 (12.5 ms)         # ISP backbone
 ...
12  142.250.185.196 (15.2 ms)   # Google server
```

**Use case:**

- Where is packet delay?
- Which hop failing?

### 8.3. `netstat` / `ss` - Network Statistics

```bash
# Show listening ports
netstat -tulpn

# Newer (faster):
ss -tulpn

# Output:
Proto Local Address      State     PID/Program
tcp   0.0.0.0:22         LISTEN    1234/sshd
tcp   0.0.0.0:80         LISTEN    5678/nginx

# Show active connections
netstat -an

# Count connections per state
netstat -an | awk '{print $6}' | sort | uniq -c
```

### 8.4. `curl` / `wget` - HTTP Clients

```bash
# curl - Make HTTP request
curl https://example.com

# See headers
curl -I https://example.com

# Follow redirects
curl -L https://bit.ly/short-url

# POST data
curl -X POST -d "key=value" https://api.example.com

# Download file
curl -O https://example.com/file.zip

# wget - Download file
wget https://example.com/file.zip

# Resume download
wget -c https://example.com/large-file.zip
```

### 8.5. `nslookup` / `dig` - DNS Lookup

```bash
# nslookup
nslookup google.com

# Output:
Server:    8.8.8.8
Address:   8.8.8.8#53

Non-authoritative answer:
Name:   google.com
Address: 142.250.185.196

# dig (more details)
dig google.com

# Short answer
dig +short google.com
# 142.250.185.196

# Trace DNS resolution
dig +trace google.com
```

### 8.6. Common Issues & Solutions

**Issue: Cannot ping google.com**

```bash
# 1. Check local network
ping 127.0.0.1  # Loopback OK?
ping 192.168.1.1  # Router OK?

# 2. Check DNS
ping 8.8.8.8  # If this works, DNS issue
nslookup google.com  # DNS resolving?

# 3. Check route
ip route  # Default gateway correct?
```

**Issue: Website not loading**

```bash
# 1. Can resolve domain?
nslookup example.com

# 2. Can reach server?
ping example.com

# 3. Port 80/443 open?
telnet example.com 80
# Or
curl -I http://example.com

# 4. Check from server side
# SSH to server
netstat -tulpn | grep :80  # Web server running?
```

**Issue: SSH connection refused**

```bash
# 1. Port open?
telnet server 22

# 2. SSH service running?
# On server:
sudo systemctl status sshd

# 3. Firewall blocking?
# On server:
sudo ufw status

# 4. Correct IP/hostname?
ping server
```

---

## 📚 Tổng kết

### Key Takeaways

1. **OSI/TCP-IP models** - Foundation of networking
2. **IP addresses** - IPv4 (192.168.1.1), IPv6 (2001:db8::1)
3. **Subnetting** - CIDR notation (/24), subnet masks
4. **Ports** - 80 (HTTP), 443 (HTTPS), 22 (SSH)
5. **DNS** - Translates domains to IPs
6. **HTTP/HTTPS** - Request-response, status codes, TLS encryption
7. **SSH** - Secure remote access, key-based auth
8. **Tools** - ping, traceroute, netstat, curl, dig

### Checklist

- [ ] Explain OSI 7 layers and TCP/IP 4 layers
- [ ] Calculate subnet sizes from CIDR notation
- [ ] Identify common port numbers
- [ ] Perform DNS lookup with dig/nslookup
- [ ] Understand HTTP methods and status codes
- [ ] Explain HTTPS/TLS handshake
- [ ] Connect to servers via SSH with keys
- [ ] Troubleshoot connectivity with ping/traceroute
- [ ] Check listening ports with netstat/ss

### Next: Module 04 - HTML_CSS_JS_BASICS

👉 Time to build simple web apps to deploy!

---

> **The network is the computer.** - Sun Microsystems 🌐
