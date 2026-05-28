# OSI Model & TCP/IP

> **Tags:** `networking` `osi` `tcp` `udp` `ip` `subnetting` `protocols`
> **Level:** Intermediate | **Prerequisite:** `01-http-networking.md`

---

## 1. OSI Model — 7 Layers

```
Layer 7 — Application    HTTP, HTTPS, DNS, FTP, SMTP, WebSocket
Layer 6 — Presentation   TLS/SSL, encoding (ASCII/UTF-8), compression
Layer 5 — Session        Session management, token, RPC
Layer 4 — Transport      TCP, UDP — ports, segmentation, reliability
Layer 3 — Network        IP, ICMP, routing, ARP
Layer 2 — Data Link      Ethernet, MAC addresses, switches, VLANs
Layer 1 — Physical       Cables, fiber, radio waves, bits
```

### Mnemonic
- **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing
- (Application, Presentation, Session, Transport, Network, Data Link, Physical)

### Encapsulation khi gửi dữ liệu
```
App: HTTP Request "GET /index.html"
  └─▶ L7: HTTP message
        └─▶ L4: TCP segment [SRC_PORT | DST_PORT | SEQ | DATA]
              └─▶ L3: IP packet [SRC_IP | DST_IP | TTL | SEGMENT]
                    └─▶ L2: Ethernet frame [SRC_MAC | DST_MAC | PACKET | FCS]
                          └─▶ L1: Bits on wire
```

---

## 2. TCP vs UDP

### TCP (Transmission Control Protocol)
- **Connection-oriented**: 3-way handshake trước khi gửi data
- **Reliable**: đảm bảo delivery, ordering, no duplicates
- **Flow control**: sliding window, receiver advertises buffer size
- **Congestion control**: slow start, AIMD

```
3-Way Handshake:
Client                    Server
  │── SYN (seq=100) ──────▶│
  │◀─ SYN-ACK (seq=200, ack=101) ─│
  │── ACK (ack=201) ───────▶│
  │   [Connection established]   │
  │── GET /index.html ──────▶│
  │◀─ 200 OK + body ─────────│
  │── FIN ─────────────────▶│  (4-way teardown)
  │◀─ ACK ───────────────────│
  │◀─ FIN ───────────────────│
  │── ACK ─────────────────▶│
```

### UDP (User Datagram Protocol)
- **Connectionless**: không handshake
- **Unreliable**: không đảm bảo delivery hay ordering
- **Fast**: không có overhead của TCP
- **Use cases**: DNS, DHCP, video streaming, gaming, WebRTC, QUIC

```python
# UDP server in Python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 9999))

while True:
    data, addr = server.recvfrom(1024)
    print(f"From {addr}: {data}")
    server.sendto(b"ACK", addr)  # Optional — UDP doesn't require this
```

### So sánh

| | TCP | UDP |
|---|---|---|
| Connection | 3-way handshake | None |
| Reliability | Guaranteed | Best-effort |
| Ordering | Yes | No |
| Speed | Slower | Faster |
| Overhead | High (20-60B header) | Low (8B header) |
| Flow control | Yes | No |
| Use cases | HTTP, SSH, FTP, email | DNS, gaming, streaming, VoIP |

---

## 3. TCP Deep Dive — Congestion Control

### Slow Start
```
Khi bắt đầu kết nối hoặc sau packet loss:
  cwnd (congestion window) = 1 MSS
  mỗi ACK: cwnd += 1 MSS  → exponential growth
  khi cwnd >= ssthresh: chuyển sang Congestion Avoidance
```

### Congestion Avoidance (AIMD)
```
  mỗi RTT: cwnd += 1 MSS  → linear growth
  khi detect packet loss (timeout hoặc 3 duplicate ACKs):
    ssthresh = cwnd / 2
    cwnd = 1 (timeout) hoặc cwnd = ssthresh (3 dup ACKs + Fast Recovery)
```

### Nagle's Algorithm
- Gom nhỏ nhiều sends thành 1 TCP segment để giảm overhead
- Vấn đề: gây latency tăng (200-500ms) cho interactive apps
- Tắt bằng: `TCP_NODELAY`

```python
import socket
sock = socket.socket()
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Disable Nagle
```

### TIME_WAIT
- Sau khi kết nối đóng, bên initiate close ở trạng thái TIME_WAIT **2 * MSL** (thường 60-120 giây)
- Mục đích: đảm bảo delayed packets của kết nối cũ không ảnh hưởng kết nối mới
- Vấn đề: High-throughput servers có thể cạn kiệt ports

```bash
# Xem TIME_WAIT connections
ss -natp | grep TIME_WAIT | wc -l

# Giảm TIME_WAIT timeout
sysctl -w net.ipv4.tcp_fin_timeout=15
sysctl -w net.ipv4.tcp_tw_reuse=1    # Tái sử dụng TIME_WAIT sockets
```

---

## 4. IP Addressing

### IPv4
```
32-bit, dotted-decimal notation
192.168.1.100

Binary:
11000000.10101000.00000001.01100100
```

### CIDR Notation (Classless Inter-Domain Routing)
```
192.168.1.0/24

/24 = subnet mask 255.255.255.0
    = 24 bits cho network, 8 bits cho host
    = 2^8 = 256 addresses (254 usable, -1 network, -1 broadcast)

Ví dụ phổ biến:
/8  = 10.0.0.0/8        = 16,777,216 hosts (class A private)
/16 = 172.16.0.0/16     = 65,536 hosts (class B private)
/24 = 192.168.0.0/24    = 256 hosts (class C private)
/32 = 192.168.1.1/32    = 1 host (dùng trong routing, security groups)
```

### Subnetting Example
```
Given: 192.168.1.0/24, divide into 4 subnets

/26 = 64 addresses per subnet (62 usable)

Subnet 1: 192.168.1.0/26   → 192.168.1.0  - 192.168.1.63
Subnet 2: 192.168.1.64/26  → 192.168.1.64 - 192.168.1.127
Subnet 3: 192.168.1.128/26 → 192.168.1.128 - 192.168.1.191
Subnet 4: 192.168.1.192/26 → 192.168.1.192 - 192.168.1.255

For each subnet:
  First IP = Network address (không dùng được)
  Last IP  = Broadcast address (không dùng được)
  Rest     = Usable host addresses
```

### Private IP Ranges (RFC 1918)
```
10.0.0.0/8         → 10.0.0.0 - 10.255.255.255    (16M hosts)
172.16.0.0/12      → 172.16.0.0 - 172.31.255.255  (1M hosts)
192.168.0.0/16     → 192.168.0.0 - 192.168.255.255 (65K hosts)
127.0.0.0/8        → Loopback (127.0.0.1)
169.254.0.0/16     → Link-local (APIPA khi DHCP fails)
```

### IPv6
```
128-bit, hexadecimal, separated by colons
2001:0db8:85a3:0000:0000:8a2e:0370:7334

Compressed (leading zeros omitted, :: = consecutive zeroes):
2001:db8:85a3::8a2e:370:7334

Special:
::1            = Loopback (IPv6 equivalent of 127.0.0.1)
::             = Unspecified
fe80::/10      = Link-local
fd00::/8       = Unique local (private)
2000::/3       = Global unicast (public internet)
```

---

## 5. ARP (Address Resolution Protocol)

ARP map **IP address → MAC address** trong local network:

```
Host A (192.168.1.1) muốn gửi đến Host B (192.168.1.2):

1. A gửi ARP Request (broadcast):
   "Who has 192.168.1.2? Tell 192.168.1.1"
   Destination MAC: FF:FF:FF:FF:FF:FF (broadcast)

2. B nhận broadcast, reply unicast:
   "192.168.1.2 is at AA:BB:CC:DD:EE:FF"

3. A lưu vào ARP cache, gửi frame đến MAC của B
```

```bash
# Xem ARP cache
arp -n
ip neigh show

# Flush ARP cache
ip neigh flush all
```

### ARP Spoofing
Attacker gửi fake ARP replies để redirect traffic qua mình (man-in-the-middle):
- Protection: **Dynamic ARP Inspection** (DAI) trên managed switches, **arpwatch**

---

## 6. ICMP & Network Diagnostics

**ICMP** (Internet Control Message Protocol) = Layer 3, dùng cho network diagnostics:

```bash
# ping — ICMP Echo Request/Reply
ping -c 5 google.com
ping -s 1400 google.com    # Specific packet size
ping6 ::1                   # IPv6

# traceroute — tìm path qua network
# Mỗi hop: gửi UDP/ICMP với TTL tăng dần
# Khi TTL=0, router gửi ICMP Time Exceeded
traceroute google.com
traceroute -T google.com    # TCP-based (qua firewalls tốt hơn)
mtr google.com              # Kết hợp ping + traceroute, real-time

# Xem ICMP errors trong socket
# ICMP Port Unreachable → ECONNREFUSED
# ICMP Network Unreachable → ENETUNREACH
# ICMP Time Exceeded → EHOSTUNREACH (TTL expired)
```

---

## 7. Common Ports

| Port | Protocol | Service |
|---|---|---|
| 21 | TCP | FTP |
| 22 | TCP | SSH |
| 25 | TCP | SMTP |
| 53 | TCP/UDP | DNS |
| 80 | TCP | HTTP |
| 443 | TCP | HTTPS |
| 587 | TCP | SMTP (submission) |
| 3306 | TCP | MySQL |
| 5432 | TCP | PostgreSQL |
| 6379 | TCP | Redis |
| 27017 | TCP | MongoDB |
| 8080 | TCP | HTTP alternative |
| 8443 | TCP | HTTPS alternative |
| 9200 | TCP | Elasticsearch |
| 2181 | TCP | ZooKeeper |
| 9092 | TCP | Kafka |

---

## 8. Networking Commands Cheatsheet

```bash
# IP và interfaces
ip addr show                    # Xem IPs
ip addr add 192.168.1.100/24 dev eth0
ip link show                    # Xem interfaces
ip link set eth0 up/down        # Enable/disable interface

# Routing
ip route show                   # Xem routing table
ip route add default via 192.168.1.1   # Add default gateway
ip route add 10.0.0.0/8 via 192.168.1.1

# Connections
ss -tuln                        # Listening ports (TCP+UDP)
ss -tunp                        # Connections + process
ss -s                           # Summary stats
netstat -tuln                   # Older alternative to ss

# DNS
dig google.com                  # DNS query
dig google.com @8.8.8.8         # Query specific DNS server
dig -x 8.8.8.8                  # Reverse lookup
nslookup google.com             # Interactive DNS
host google.com                 # Simple lookup

# Traffic capture
tcpdump -i eth0 port 80         # Capture HTTP on eth0
tcpdump -i any -w capture.pcap  # Write to file for Wireshark
tcpdump 'tcp port 443'          # Filter HTTPS

# Bandwidth
iperf3 -s                       # Start server
iperf3 -c server_ip             # Test bandwidth to server
```

---

## 9. Network Layers trong Docker & Kubernetes

```
Docker bridge network:
  Container A (172.17.0.2)
  Container B (172.17.0.3)
       └──── docker0 bridge (172.17.0.1) ──────▶ Host (eth0) ──▶ Internet

Kubernetes pod network:
  Pod A (10.244.1.5/24)   ← eth0 veth pair với node
  Pod B (10.244.1.6/24)
       └──── cni0 bridge (10.244.1.1/24) ──── flannel/calico/cilium
              └──────────────────────────────▶ Node 2 pods
```

---

## 10. Bài tập

1. **Subnetting practice**: Cho mạng 10.0.0.0/16, chia thành 8 subnets. Mỗi subnet có bao nhiêu hosts? Đặt tên các subnets.
2. **Wireshark**: Capture traffic khi browse một website. Quan sát TCP handshake, TLS handshake, HTTP requests.
3. **Socket programming**: Viết TCP echo server + client bằng Python thuần (không dùng frameworks).
4. **ARP investigation**: Chạy `arp -n` và `ip neigh`. Giải thích từng cột.
5. **Traceroute analysis**: Chạy `mtr google.com` và giải thích mỗi hop là gì.

---

*Tài liệu liên quan: `networking/04-tls-ssl.md` | `networking/05-dns.md` | `networking/11-tcp-deep-dive.md`*
