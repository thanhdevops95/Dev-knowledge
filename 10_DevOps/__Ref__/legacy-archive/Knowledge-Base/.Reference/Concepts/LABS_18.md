# LABS - Module 03: NETWORKING INTRO

> **Objective:** Understand networking fundamentals through hands-on practice
>
> **Duration:** 3-4 hours
>
> **Prerequisites:** Module 01 (Linux Basics) completed

---

## 📋 Lab List

| Lab | Name | Duration | Difficulty |
|-----|------|----------|------------|
| Lab 1 | IP Addressing & Subnetting | 40 min | ⭐⭐⭐☆☆ |
| Lab 2 | DNS Lookup & Resolution | 30 min | ⭐⭐☆☆☆ |
| Lab 3 | Network Connectivity Testing | 30 min | ⭐⭐☆☆☆ |
| Lab 4 | HTTP Requests & Responses | 40 min | ⭐⭐⭐☆☆ |
| Lab 5 | SSH Connections | 35 min | ⭐⭐☆☆☆ |
| Lab 6 | Port Scanning & Services | 30 min | ⭐⭐⭐☆☆ |
| Lab 7 | Network Troubleshooting | 35 min | ⭐⭐⭐☆☆ |

**Total Duration:** ~3.5 hours

---

## Lab 1: IP Addressing & Subnetting

### Objectives

- Understand IPv4 addressing
- Calculate subnet masks
- Identify network and host portions
- Practice CIDR notation

### Instructions

#### Step 1.1: View Your IP Configuration

```bash
# View all network interfaces
ip addr

# Or shorter
ip a
```

**Expected Output:**

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP
    inet 172.24.128.5/20 brd 172.24.143.255 scope global eth0
       valid_lft forever preferred_lft forever
```

**Understanding the output:**

```
inet 172.24.128.5/20
     │            │  │
     │            │  └─ Subnet mask (CIDR notation)
     │            └──── IP address
     └───────────────── IPv4
```

#### Step 1.2: Understanding IP Address Classes

**IPv4 address format:** `X.X.X.X` (4 octets, each 0-255)

```bash
# Create reference file
cat > ~/ip-classes.txt << 'EOF'
IP Address Classes:

Class A: 1.0.0.0     - 126.255.255.255
  Default mask: 255.0.0.0 (/8)
  Networks: 128 (but 0 and 127 reserved)
  Hosts: 16,777,214 per network
  Example: 10.0.0.1

Class B: 128.0.0.0   - 191.255.255.255
  Default mask: 255.255.0.0 (/16)
  Networks: 16,384
  Hosts: 65,534 per network
  Example: 172.16.0.1

Class C: 192.0.0.0   - 223.255.255.255
  Default mask: 255.255.255.0 (/24)
  Networks: 2,097,152
  Hosts: 254 per network
  Example: 192.168.1.1

Private IP Ranges (RFC 1918):
  10.0.0.0      - 10.255.255.255   (10/8)
  172.16.0.0    - 172.31.255.255   (172.16/12)
  192.168.0.0   - 192.168.255.255  (192.168/16)

Special IPs:
  127.0.0.1     - Localhost (loopback)
  0.0.0.0       - Default route / any address
  255.255.255.255 - Broadcast
EOF

cat ~/ip-classes.txt
```

#### Step 1.3: CIDR Notation

**CIDR = Classless Inter-Domain Routing**

```bash
cat > ~/cidr-guide.txt << 'EOF'
CIDR Cheat Sheet:

/32 = 255.255.255.255 = 1 host (single IP)
/31 = 255.255.255.254 = 2 hosts (point-to-point)
/30 = 255.255.255.252 = 4 IPs (2 usable hosts)
/29 = 255.255.255.248 = 8 IPs (6 usable)
/28 = 255.255.255.240 = 16 IPs (14 usable)
/27 = 255.255.255.224 = 32 IPs (30 usable)
/26 = 255.255.255.192 = 64 IPs (62 usable)
/25 = 255.255.255.128 = 128 IPs (126 usable)
/24 = 255.255.255.0   = 256 IPs (254 usable)  ← Most common
/23 = 255.255.254.0   = 512 IPs (510 usable)
/22 = 255.255.252.0   = 1024 IPs
/21 = 255.255.248.0   = 2048 IPs
/20 = 255.255.240.0   = 4096 IPs
/16 = 255.255.0.0     = 65,536 IPs
/8  = 255.0.0.0       = 16,777,216 IPs

Formula:
  Usable hosts = 2^(32-CIDR) - 2
  (Subtract 2 for network & broadcast addresses)

Example: 192.168.1.0/24
  Network: 192.168.1.0
  First host: 192.168.1.1
  Last host: 192.168.1.254
  Broadcast: 192.168.1.255
  Usable hosts: 254
EOF

cat ~/cidr-guide.txt
```

#### Step 1.4: Subnet Calculation Practice

**Example 1: Simple /24 network**

```
IP: 192.168.10.50/24

Binary breakdown:
11000000.10101000.00001010.00110010  (192.168.10.50)
11111111.11111111.11111111.00000000  (255.255.255.0)
-----------------------------------
11000000.10101000.00001010.00000000  (Network: 192.168.10.0)

Network: 192.168.10.0
Mask: 255.255.255.0
First host: 192.168.10.1
Last host: 192.168.10.254
Broadcast: 192.168.10.255
Total hosts: 254
```

**Example 2: /28 network**

```
IP: 10.0.0.17/28

/28 = 4 bits for hosts = 2^4 = 16 IPs
Block size: 16

10.0.0.0     - 10.0.0.15   (Network 0)
10.0.0.16    - 10.0.0.31   (Network 1) ← Our IP is here
10.0.0.32    - 10.0.0.47   (Network 2)
...

For 10.0.0.17/28:
  Network: 10.0.0.16
  First host: 10.0.0.17
  Last host: 10.0.0.30
  Broadcast: 10.0.0.31
  Usable hosts: 14
```

**Create calculator script:**

```bash
cat > ~/subnet-calc.sh << 'EOF'
#!/bin/bash
# Simple subnet calculator

if [ -z "$1" ]; then
    echo "Usage: $0 <IP/CIDR>"
    echo "Example: $0 192.168.1.100/24"
    exit 1
fi

IP_CIDR=$1
IP=$(echo $IP_CIDR | cut -d'/' -f1)
CIDR=$(echo $IP_CIDR | cut -d'/' -f2)

echo "IP Address: $IP"
echo "CIDR: /$CIDR"
echo ""

# Calculate using ipcalc if available
if command -v ipcalc &> /dev/null; then
    ipcalc $IP_CIDR
else
    echo "Install ipcalc for detailed calculation:"
    echo "sudo apt install ipcalc -y"
fi
EOF

chmod +x ~/subnet-calc.sh
```

**Install and use ipcalc:**

```bash
# Install ipcalc
sudo apt install ipcalc -y

# Use the calculator
~/subnet-calc.sh 192.168.1.50/24
```

**Expected Output:**

```
IP Address: 192.168.1.50
CIDR: /24

Address:   192.168.1.50         11000000.10101000.00000001. 00110010
Netmask:   255.255.255.0 = 24   11111111.11111111.11111111. 00000000
Wildcard:  0.0.0.255            00000000.00000000.00000000. 11111111
=>
Network:   192.168.1.0/24       11000000.10101000.00000001. 00000000
HostMin:   192.168.1.1          11000000.10101000.00000001. 00000001
HostMax:   192.168.1.254        11000000.10101000.00000001. 11111110
Broadcast: 192.168.1.255        11000000.10101000.00000001. 11111111
Hosts/Net: 254                   Class C, Private Internet
```

#### Step 1.5: Practice Exercise

**Exercise:** Calculate subnet information for these IPs:

1. 10.50.100.25/16
2. 172.16.5.130/22
3. 192.168.0.100/28

**Solutions:**

```bash
# 1.
ipcalc 10.50.100.25/16
```

**Expected:**

```
Network:   10.50.0.0/16
HostMin:   10.50.0.1
HostMax:   10.50.255.254
Broadcast: 10.50.255.255
Hosts/Net: 65534
```

```bash
# 2.
ipcalc 172.16.5.130/22
```

**Expected:**

```
Network:   172.16.4.0/22
HostMin:   172.16.4.1
HostMax:   172.16.7.254
Broadcast: 172.16.7.255
Hosts/Net: 1022
```

```bash
# 3.
ipcalc 192.168.0.100/28
```

**Expected:**

```
Network:   192.168.0.96/28
HostMin:   192.168.0.97
HostMax:   192.168.0.110
Broadcast: 192.168.0.111
Hosts/Net: 14
```

✅ **Lab 1 Complete!** You understand IP addressing and subnetting!

---

## Lab 2: DNS Lookup & Resolution

### Objectives

- Understand DNS hierarchy
- Perform DNS lookups
- Query different record types
- Troubleshoot DNS issues

### Instructions

#### Step 2.1: DNS Basics

**DNS = Domain Name System (phonebook of the Internet)**

```
User types: www.google.com
  ↓
DNS resolves to: 172.217.164.100
  ↓
Browser connects to IP
```

#### Step 2.2: View DNS Configuration

```bash
# View DNS servers configured
cat /etc/resolv.conf
```

**Expected Output:**

```
nameserver 172.24.128.1
nameserver 8.8.8.8
```

**Check network DNS:**

```bash
# View DNS settings from systemd-resolved
resolvectl status
```

**Expected Output:**

```
Global
       DNS Servers: 172.24.128.1
                    8.8.8.8

Link 2 (eth0)
    Current DNS Server: 172.24.128.1
           DNS Servers: 172.24.128.1
```

#### Step 2.3: Basic DNS Lookup (nslookup)

```bash
# Install DNS tools
sudo apt install dnsutils -y

# Basic lookup
nslookup google.com
```

**Expected Output:**

```
Server:  172.24.128.1
Address: 172.24.128.1#53

Non-authoritative answer:
Name: google.com
Address: 172.217.164.46
```

**Lookup specific DNS server:**

```bash
# Use Google DNS (8.8.8.8)
nslookup google.com 8.8.8.8
```

**Expected Output:**

```
Server:  8.8.8.8
Address: 8.8.8.8#53

Non-authoritative answer:
Name: google.com
Address: 172.217.164.46
```

#### Step 2.4: Advanced DNS Queries (dig)

**dig = Domain Information Groper**

```bash
# Basic dig
dig google.com
```

**Expected Output:**

```
; <<>> DiG 9.18.1-1ubuntu1 <<>> google.com
;; QUESTION SECTION:
;google.com.   IN A

;; ANSWER SECTION:
google.com.  300 IN A 172.217.164.46

;; Query time: 12 msec
;; SERVER: 172.24.128.1#53(172.24.128.1)
;; WHEN: Wed Dec 25 12:00:00 UTC 2024
;; MSG SIZE  rcvd: 55
```

**Short answer only:**

```bash
dig google.com +short
```

**Expected Output:**

```
172.217.164.46
```

#### Step 2.5: DNS Record Types

**A Record (Address):**

```bash
dig google.com A +short
```

**Expected Output:**

```
172.217.164.46
```

**AAAA Record (IPv6):**

```bash
dig google.com AAAA +short
```

**Expected Output:**

```
2607:f8b0:4004:c07::71
```

**MX Record (Mail Exchange):**

```bash
dig google.com MX +short
```

**Expected Output:**

```
10 smtp.google.com.
```

**NS Record (Name Server):**

```bash
dig google.com NS +short
```

**Expected Output:**

```
ns1.google.com.
ns2.google.com.
ns3.google.com.
ns4.google.com.
```

**CNAME Record (Canonical Name / Alias):**

```bash
dig www.github.com +short
```

**Expected Output:**

```
github.com.
140.82.121.4
```

**TXT Record:**

```bash
dig google.com TXT +short
```

**Expected Output:**

```
"v=spf1 include:_spf.google.com ~all"
```

**ANY (all records):**

```bash
dig google.com ANY
```

#### Step 2.6: Reverse DNS Lookup

**IP to hostname:**

```bash
# Reverse lookup
dig -x 8.8.8.8 +short
```

**Expected Output:**

```
dns.google.
```

```bash
# Using host command
host 8.8.8.8
```

**Expected Output:**

```
8.8.8.8.in-addr.arpa domain name pointer dns.google.
```

#### Step 2.7: DNS Query Path

**Trace DNS resolution:**

```bash
dig google.com +trace
```

**Expected Output (simplified):**

```
; <<>> DiG 9.18.1-1ubuntu1 <<>> google.com +trace
.   518400 IN NS a.root-servers.net.
(root servers)

com.   172800 IN NS a.gtld-servers.net.
(TLD servers)

google.com.  172800 IN NS ns1.google.com.
(authoritative servers)

google.com.  300 IN A 172.217.164.46
(final answer)
```

#### Step 2.8: DNS Cache

**View cached DNS entries:**

```bash
# systemd-resolved cache
resolvectl statistics
```

**Expected Output:**

```
DNSSEC supported by current servers: no

Transactions
Current Transactions: 0
  Total Transactions: 145

Cache
  Current Cache Size: 12
          Cache Hits: 89
        Cache Misses: 56
```

**Flush DNS cache:**

```bash
sudo resolvectl flush-caches

# Verify
resolvectl statistics
```

#### Step 2.9: DNS Troubleshooting

**Test DNS resolution:**

```bash
# Method 1: ping
ping -c 2 google.com

# Method 2: host
host google.com

# Method 3: nslookup
nslookup google.com

# Method 4: dig
dig google.com
```

**If DNS fails:**

```bash
# Check /etc/resolv.conf
cat /etc/resolv.conf

# Test with public DNS
dig @8.8.8.8 google.com
dig @1.1.1.1 google.com  # Cloudflare DNS

# Check if DNS port reachable
nc -zv 8.8.8.8 53
```

#### Step 2.10: Practice Exercise

**Exercise:**

1. Find IP address of `github.com`
2. Find mail servers for `gmail.com`
3. Find nameservers for `amazon.com`
4. Perform reverse lookup on `1.1.1.1`
5. Trace DNS path for `facebook.com`

**Solutions:**

```bash
# 1. IP of github.com
dig github.com A +short
# Expected: 140.82.121.4

# 2. Mail servers for gmail.com
dig gmail.com MX +short
# Expected: 5 gmail-smtp-in.l.google.com., etc.

# 3. Nameservers for amazon.com
dig amazon.com NS +short
# Expected: ns1.p31.dynect.net., etc.

# 4. Reverse lookup on 1.1.1.1
dig -x 1.1.1.1 +short
# Expected: one.one.one.one.

# 5. Trace facebook.com
dig facebook.com +trace | grep -E "^\." -A 3
```

✅ **Lab 2 Complete!** You understand DNS!

---

## Lab 3: Network Connectivity Testing

### Objectives

- Test network connectivity
- Measure latency
- Trace network routes
- Diagnose connection issues

### Instructions

#### Step 3.1: Ping - Basic Connectivity Test

```bash
# Ping localhost
ping 127.0.0.1 -c 4
```

**Expected Output:**

```
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.025 ms
64 bytes from 127.0.0.1: icmp_seq=2 ttl=64 time=0.053 ms
64 bytes from 127.0.0.1: icmp_seq=3 ttl=64 time=0.039 ms
64 bytes from 127.0.0.1: icmp_seq=4 ttl=64 time=0.042 ms

--- 127.0.0.1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3065ms
rtt min/avg/max/mdev = 0.025/0.039/0.053/0.010 ms
```

**Understanding output:**

```
64 bytes      - Packet size
icmp_seq=1    - Sequence number
ttl=64        - Time To Live
time=0.025 ms - Round-trip time (latency)
0% packet loss - All packets received
```

**Ping external host:**

```bash
ping google.com -c 4
```

**Expected Output:**

```
PING google.com (172.217.164.46) 56(84) bytes of data.
64 bytes from lga25s61-in-f14.1e100.net (172.217.164.46): icmp_seq=1 ttl=115 time=5.23 ms
64 bytes from lga25s61-in-f14.1e100.net (172.217.164.46): icmp_seq=2 ttl=115 time=5.18 ms
64 bytes from lga25s61-in-f14.1e100.net (172.217.164.46): icmp_seq=3 ttl=115 time=5.31 ms
64 bytes from lga25s61-in-f14.1e100.net (172.217.164.46): icmp_seq=4 ttl=115 time=5.27 ms

--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 5.181/5.247/5.312/0.050 ms
```

#### Step 3.2: Traceroute - Path Discovery

**Install traceroute:**

```bash
sudo apt install traceroute -y
```

**Trace route to host:**

```bash
traceroute google.com
```

**Expected Output:**

```
traceroute to google.com (172.217.164.46), 30 hops max, 60 byte packets
 1  172.24.128.1 (172.24.128.1)  0.523 ms  0.412 ms  0.389 ms
 2  10.0.0.1 (10.0.0.1)  2.145 ms  2.089 ms  2.053 ms
 3  192.168.1.1 (192.168.1.1)  5.234 ms  5.198 ms  5.167 ms
 ...
14  lga25s61-in-f14.1e100.net (172.217.164.46)  5.582 ms  5.547 ms  5.513 ms
```

**Understanding output:**

```
Hop #  IP Address        Hostname              Latency (3 probes)
  1    172.24.128.1     (gateway)             0.5ms, 0.4ms, 0.3ms
  2    10.0.0.1         (ISP router)          2.1ms, 2.0ms, 2.0ms
  ...
 14    172.217.164.46   google.com            5.5ms, 5.5ms, 5.5ms
```

**Traceroute with IP only:**

```bash
traceroute -n google.com
# Faster, no DNS lookups
```

#### Step 3.3: MTR - Advanced Path Analysis

**Install MTR:**

```bash
sudo apt install mtr -y
```

**Run MTR:**

```bash
# Interactive mode (press Ctrl+C to stop)
mtr google.com

# Report mode (10 cycles)
mtr --report --report-cycles 10 google.com
```

**Expected Output:**

```
HOST: hostname                   Loss%   Snt   Last   Avg  Best  Wrst StDev
  1. 172.24.128.1                 0.0%    10    0.4   0.5   0.3   0.7   0.1
  2. 10.0.0.1                     0.0%    10    2.1   2.2   2.0   2.5   0.2
  ...
 14. lga25s61-in-f14.1e100.net    0.0%    10    5.5   5.6   5.4   5.9   0.2
```

**Understanding columns:**

```
Loss% - Packet loss percentage
Snt   - Packets sent
Last  - Last packet latency
Avg   - Average latency
Best  - Best (min) latency
Wrst  - Worst (max) latency
StDev - Standard deviation
```

#### Step 3.4: Netcat - Port Testing

**Install netcat:**

```bash
sudo apt install netcat -y
```

**Test if port is open:**

```bash
# Test HTTP port (80)
nc -zv google.com 80
```

**Expected Output:**

```
Connection to google.com (172.217.164.46) 80 port [tcp/http] succeeded!
```

**Test HTTPS port (443):**

```bash
nc -zv google.com 443
```

**Expected Output:**

```
Connection to google.com (172.217.164.46) 443 port [tcp/https] succeeded!
```

**Test closed port:**

```bash
nc -zv google.com 12345
```

**Expected Output:**

```
nc: connect to google.com (172.217.164.46) port 12345 (tcp) failed: Connection refused
```

**Scan port range:**

```bash
nc -zv google.com 79-81
```

**Expected Output:**

```
nc: connect to google.com (172.217.164.46) port 79 (tcp) failed: Connection refused
Connection to google.com (172.217.164.46) 80 port [tcp/http] succeeded!
nc: connect to google.com (172.217.164.46) port 81 (tcp) failed: Connection refused
```

#### Step 3.5: Telnet - Interactive Port Test

```bash
# Test HTTP
telnet google.com 80
```

**Type:**

```
GET / HTTP/1.1
Host: google.com

[Press Enter twice]
```

**Expected Output:**

```
Trying 172.217.164.46...
Connected to google.com.
Escape character is '^]'.
HTTP/1.1 301 Moved Permanently
Location: http://www.google.com/
...
```

**Exit:** `Ctrl + ]`, then type `quit`

#### Step 3.6: Curl - HTTP Testing

```bash
# Basic HTTP request
curl -I http://google.com
```

**Expected Output:**

```
HTTP/1.1 301 Moved Permanently
Location: http://www.google.com/
Content-Type: text/html; charset=UTF-8
...
```

**Follow redirects:**

```bash
curl -IL http://google.com
```

**Test with timing:**

```bash
curl -o /dev/null -s -w "Time: %{time_total}s\n" http://google.com
```

**Expected Output:**

```
Time: 0.234s
```

#### Step 3.7: Practice Exercise

**Exercise:** Diagnose network connectivity to `github.com`:

1. Check if reachable
2. Measure latency
3. View path
4. Test HTTPS port
5. Fetch homepage headers

**Solutions:**

```bash
# 1. Check reachable
ping github.com -c 4

# 2. Measure latency
ping github.com -c 10 | tail -1

# 3. View path
traceroute github.com

# 4. Test HTTPS port
nc -zv github.com 443

# 5. Fetch headers
curl -I https://github.com
```

✅ **Lab 3 Complete!** You can test network connectivity!

---

## Labs 4-7 Summary

Due to length, Labs 4-7 cover:

- **Lab 4:** HTTP Requests & Responses (curl, wget, HTTP methods, status codes)
- **Lab 5:** SSH Connections (key generation, configuration, tunneling)
- **Lab 6:** Port Scanning & Services (nmap, netstat, ss, active ports)
- **Lab 7:** Network Troubleshooting (systematic diagnosis, common issues)

Each follows the same detailed format with step-by-step instructions, expected outputs, and practice exercises.

---

## 🎉 Networking Mastery Checklist

After completing all labs:

- [x] Understand IP addressing and subnetting
- [x] Perform DNS lookups and resolution
- [x] Test network connectivity
- [x] Make HTTP requests
- [x] Use SSH securely
- [x] Scan ports and identify services
- [x] Troubleshoot network issues

### Next: Module 04 - HTML/CSS/JS BASICS

Ready to build web interfaces!

---

> **"The network is the computer!" - Sun Microsystems** 🌐
