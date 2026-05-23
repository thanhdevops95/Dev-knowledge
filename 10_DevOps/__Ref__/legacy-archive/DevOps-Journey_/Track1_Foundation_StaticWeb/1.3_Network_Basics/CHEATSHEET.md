# 📋 Cheatsheet: Network Basics

> **Quick Reference for Networking Concepts & Commands**
>
> *Tra cứu nhanh khái niệm và lệnh mạng*

---

## 🌐 OSI Model

| Layer | Name | Protocol Examples | Devices |
|-------|------|------------------|---------|
| 7 | Application | HTTP, FTP, DNS, SSH | - |
| 6 | Presentation | SSL/TLS, JPEG, MPEG | - |
| 5 | Session | NetBIOS, RPC | - |
| 4 | Transport | TCP, UDP | Firewall |
| 3 | Network | IP, ICMP, ARP | Router |
| 2 | Data Link | Ethernet, MAC | Switch |
| 1 | Physical | Cables, Hubs | Hub, Cables |

---

## 📡 Common Ports

| Port | Service | Protocol |
|------|---------|----------|
| 20/21 | FTP | TCP |
| 22 | SSH | TCP |
| 23 | Telnet | TCP |
| 25 | SMTP | TCP |
| 53 | DNS | TCP/UDP |
| 67/68 | DHCP | UDP |
| 80 | HTTP | TCP |
| 110 | POP3 | TCP |
| 143 | IMAP | TCP |
| 443 | HTTPS | TCP |
| 3306 | MySQL | TCP |
| 5432 | PostgreSQL | TCP |
| 6379 | Redis | TCP |
| 27017 | MongoDB | TCP |

---

## 🔢 IP Addressing

### IPv4 Classes

| Class | Range | Default Mask | Private Range |
|-------|-------|--------------|---------------|
| A | 1-126 | 255.0.0.0 | 10.0.0.0/8 |
| B | 128-191 | 255.255.0.0 | 172.16.0.0/12 |
| C | 192-223 | 255.255.255.0 | 192.168.0.0/16 |

### CIDR Notation

| CIDR | Subnet Mask | Hosts |
|------|-------------|-------|
| /8 | 255.0.0.0 | 16,777,214 |
| /16 | 255.255.0.0 | 65,534 |
| /24 | 255.255.255.0 | 254 |
| /25 | 255.255.255.128 | 126 |
| /26 | 255.255.255.192 | 62 |
| /27 | 255.255.255.224 | 30 |
| /28 | 255.255.255.240 | 14 |
| /30 | 255.255.255.252 | 2 |
| /32 | 255.255.255.255 | 1 |

---

## 🔧 Linux Network Commands

### IP Configuration

```bash
# Show IP addresses
ip addr
ip a

# Show specific interface
ip addr show eth0

# Add IP address
sudo ip addr add 192.168.1.100/24 dev eth0

# Remove IP address
sudo ip addr del 192.168.1.100/24 dev eth0

# Bring interface up/down
sudo ip link set eth0 up
sudo ip link set eth0 down
```

### Routing

```bash
# Show routing table
ip route
route -n

# Add route
sudo ip route add 10.0.0.0/8 via 192.168.1.1

# Add default gateway
sudo ip route add default via 192.168.1.1

# Delete route
sudo ip route del 10.0.0.0/8
```

### DNS

```bash
# DNS lookup
nslookup google.com
dig google.com
host google.com

# Detailed DNS query
dig +trace google.com

# Check DNS servers
cat /etc/resolv.conf
```

### Connectivity Testing

```bash
# Ping
ping -c 4 google.com
ping -c 4 8.8.8.8

# Traceroute
traceroute google.com
tracepath google.com

# MTR (combines ping + traceroute)
mtr google.com
```

### Port & Connection

```bash
# Show listening ports
ss -tuln
netstat -tuln

# Show all connections
ss -ta
netstat -an

# Show connections with process
ss -tulnp
netstat -tulnp

# Check specific port
ss -tuln | grep :80
lsof -i :80

# Test port connectivity
nc -zv google.com 443
telnet google.com 80
```

### Network Statistics

```bash
# Interface statistics
ip -s link

# Connection statistics
ss -s

# Network traffic (if installed)
iftop
nethogs
```

---

## 🌐 HTTP Methods

| Method | Description | Idempotent |
|--------|-------------|------------|
| GET | Retrieve resource | Yes |
| POST | Create resource | No |
| PUT | Update/Replace resource | Yes |
| PATCH | Partial update | No |
| DELETE | Delete resource | Yes |
| HEAD | GET without body | Yes |
| OPTIONS | Get allowed methods | Yes |

---

## 📊 HTTP Status Codes

| Code | Category | Common Examples |
|------|----------|-----------------|
| 1xx | Informational | 100 Continue |
| 2xx | Success | 200 OK, 201 Created, 204 No Content |
| 3xx | Redirection | 301 Moved, 302 Found, 304 Not Modified |
| 4xx | Client Error | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| 5xx | Server Error | 500 Internal Error, 502 Bad Gateway, 503 Service Unavailable |

---

## 🔒 SSL/TLS

### Check SSL Certificate

```bash
# View certificate
openssl s_client -connect google.com:443 </dev/null

# View certificate details
openssl s_client -connect google.com:443 </dev/null 2>/dev/null | \
  openssl x509 -text -noout

# Check expiration
echo | openssl s_client -connect google.com:443 2>/dev/null | \
  openssl x509 -noout -dates
```

### Generate Self-signed Certificate

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout server.key -out server.crt
```

---

## 🔥 Firewall (iptables)

```bash
# List rules
sudo iptables -L -n -v

# Allow incoming SSH
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow incoming HTTP/HTTPS
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Block IP
sudo iptables -A INPUT -s 192.168.1.100 -j DROP

# Allow established connections
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Default policy
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT ACCEPT

# Save rules
sudo iptables-save > /etc/iptables.rules
```

---

## 🔥 Firewall (UFW - Simplified)

```bash
# Enable/disable
sudo ufw enable
sudo ufw disable

# Status
sudo ufw status verbose

# Allow/deny
sudo ufw allow 22
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw deny 23

# Allow from specific IP
sudo ufw allow from 192.168.1.0/24

# Delete rule
sudo ufw delete allow 80

# Reset
sudo ufw reset
```

---

## 📡 cURL Commands

```bash
# Basic GET
curl https://api.example.com

# With headers
curl -H "Authorization: Bearer token" https://api.example.com

# POST with JSON
curl -X POST -H "Content-Type: application/json" \
  -d '{"name":"test"}' https://api.example.com

# Download file
curl -O https://example.com/file.zip

# Follow redirects
curl -L https://example.com

# Show headers
curl -I https://example.com

# Verbose
curl -v https://example.com

# With timeout
curl --connect-timeout 5 --max-time 10 https://example.com
```

---

## 📋 /etc/hosts

```bash
# Format
# IP_ADDRESS  HOSTNAME  ALIAS

127.0.0.1       localhost
192.168.1.10    web-server  web
192.168.1.20    db-server   db
```

---

## 🔧 Network Configuration Files

### Ubuntu/Debian (Netplan)

```yaml
# /etc/netplan/01-config.yaml
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 192.168.1.100/24
      gateway4: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
```

```bash
sudo netplan apply
```

### CentOS/RHEL

```bash
# /etc/sysconfig/network-scripts/ifcfg-eth0
TYPE=Ethernet
BOOTPROTO=static
NAME=eth0
DEVICE=eth0
ONBOOT=yes
IPADDR=192.168.1.100
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS1=8.8.8.8
```

---

## 🧪 Troubleshooting Flow

```
1. Check local config
   ip addr, ip route

2. Check DNS
   nslookup, dig

3. Test connectivity
   ping gateway
   ping external IP (8.8.8.8)
   ping hostname (google.com)

4. Check ports
   ss -tuln
   telnet/nc to port

5. Check firewall
   iptables -L / ufw status

6. Check logs
   /var/log/syslog
   journalctl
```

---

**[← Back to README](./README.md)**
