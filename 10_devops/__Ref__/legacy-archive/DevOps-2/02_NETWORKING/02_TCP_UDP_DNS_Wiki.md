# 02. TCP, UDP & DNS

[← IP & OSI](01_IP_OSI.md) | [Tiếp: Load Balancing →](03_LOAD_BALANCING.md)

---

# 📚 Bảng thuật ngữ

Trước khi bắt đầu, hãy làm quen với các thuật ngữ quan trọng trong bài học này:

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **TCP** | /ˌtiːsiːˈpiː/ | Transmission Control Protocol - Giao thức truyền dữ liệu đáng tin cậy, có thứ tự |
| **UDP** | /ˌjuːdiːˈpiː/ | User Datagram Protocol - Giao thức truyền nhanh, không đảm bảo |
| **DNS** | /ˌdiːenˈes/ | Domain Name System - Hệ thống chuyển tên miền thành IP |
| **Handshake** | /ˈhændʃeɪk/ | Bắt tay - Quá trình thiết lập kết nối giữa hai bên |
| **SYN** | - | Synchronize - Tín hiệu bắt đầu kết nối TCP |
| **ACK** | - | Acknowledgment - Tín hiệu xác nhận đã nhận dữ liệu |
| **Segment** | - | Đoạn dữ liệu - Đơn vị dữ liệu của TCP |
| **Datagram** | - | Gói tin UDP - Đơn vị dữ liệu độc lập |
| **Port** | - | Cổng - Điểm cuối logic để phân biệt các dịch vụ (vd: 80, 443) |
| **Resolver** | - | Máy chủ phân giải DNS - Tìm IP cho tên miền |
| **TLD** | - | Top-Level Domain - Phần cuối của tên miền (.com, .vn, .org) |
| **TTL** | - | Time To Live - Thời gian bản ghi DNS được cache |
| **A Record** | - | Address Record - Ánh xạ tên miền → IPv4 |
| **CNAME** | - | Canonical Name - Bí danh cho một tên miền khác |
| **MX Record** | - | Mail Exchange - Chỉ định mail server của domain |

---

# 🤔 Tại sao DevOps cần biết TCP/UDP/DNS?

## Nỗi đau thực tế

> "Kết nối database bị timeout, không biết là lỗi network hay lỗi app"

> "DNS propagation mất 24 giờ, khách hàng không truy cập được website mới"

> "Game server lag, sếp hỏi có nên chuyển từ TCP sang UDP không?"

## Kiến thức này giúp bạn

| Tình huống | Cần biết |
|------------|----------|
| Debug "Connection timeout" | TCP 3-way handshake, timeout settings |
| Chuyển domain, website down | DNS propagation, TTL |
| Chọn protocol cho real-time app | TCP vs UDP trade-offs |
| Cấu hình DNS records | A, CNAME, MX records |
| Troubleshoot "Name not resolved" | DNS resolution process |

TCP, UDP, và DNS là nền tảng của mọi giao tiếp mạng. Hiểu chúng giúp bạn debug nhanh hơn và thiết kế hệ thống tốt hơn.

---

# 📡 TCP (Transmission Control Protocol)

## TCP là gì?

**TCP (Transmission Control Protocol)** là một giao thức **hướng kết nối (connection-oriented)**, nghĩa là một kết nối phải được thiết lập trước khi dữ liệu có thể được truyền theo cả hai chiều.

TCP có các hệ thống tích hợp để kiểm tra lỗi và **đảm bảo dữ liệu sẽ được gửi đúng thứ tự** như khi nó được gửi đi. Điều này khiến TCP trở thành giao thức hoàn hảo cho việc truyền tải thông tin như hình ảnh, file dữ liệu, và trang web.

---

## 3-Way Handshake

```
┌─────────────────────────────────────────────────────────────┐
│                TCP 3-WAY HANDSHAKE                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Client                              Server                  │
│    │                                   │                     │
│    │───────── SYN (seq=100) ──────────►│  "Hey, I want to   │
│    │                                   │   connect"          │
│    │                                   │                     │
│    │◄──── SYN-ACK (seq=300,ack=101) ──│  "OK, I acknowledge │
│    │                                   │   and ready too"    │
│    │                                   │                     │
│    │───────── ACK (ack=301) ──────────►│  "Great, let's     │
│    │                                   │   start"            │
│    │                                   │                     │
│    │◄═══════ DATA TRANSFER ══════════►│                     │
│    │                                   │                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Giải thích:**

- **SYN**: Synchronize - Client khởi tạo connection
- **SYN-ACK**: Server acknowledges và đồng ý connect
- **ACK**: Client confirms, connection established

---

## TCP Connection Termination (4-Way)

```
Client                              Server
  │                                   │
  │───────── FIN ────────────────────►│  "I'm done sending"
  │                                   │
  │◄──────── ACK ─────────────────────│  "OK, received"
  │                                   │
  │◄──────── FIN ─────────────────────│  "I'm done too"
  │                                   │
  │───────── ACK ────────────────────►│  "OK, goodbye"
  │                                   │
```

---

## TCP Features

| Feature | Mô tả |
|---------|-------|
| **Reliability** | Acknowledgment cho mỗi segment, retransmission nếu không nhận được ACK |
| **Ordering** | Sequence numbers, reordering trên receiver |
| **Flow Control** | Sliding window, prevent overwhelming receiver |
| **Congestion Control** | Slow start, congestion avoidance |

---

## TCP Use Cases

- **HTTP/HTTPS**: Web browsing
- **SMTP/POP3/IMAP**: Email
- **FTP**: File transfer
- **SSH**: Secure shell
- **Database connections**: MySQL, PostgreSQL

---

# 📡 UDP (User Datagram Protocol)

## UDP là gì?

**UDP (User Datagram Protocol)** là một **simpler, connectionless** internet protocol mà **error-checking và recovery services không cần thiết**. Với UDP, không có overhead cho opening, maintaining, hoặc terminating connection.

Data được **continuously gửi đến recipient**, cho dù họ có nhận được hay không.

---

## UDP Characteristics

```
┌─────────────────────────────────────────────────────────────┐
│                    UDP TRANSMISSION                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Client                              Server                  │
│    │                                   │                     │
│    │───────── Data ───────────────────►│                     │
│    │───────── Data ───────────────────►│  No handshake       │
│    │───────── Data ───────────────────►│  No acknowledgment  │
│    │───────── Data ───────────────────►│  No guarantee       │
│    │───────── Data ───────────────────►│                     │
│    │                                   │                     │
│    │           (Some may be lost)      │                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Features:**

- **No connection setup**: Fire and forget
- **No reliability**: May lose packets
- **No ordering**: Packets may arrive out of order
- **No flow control**: Sender controls rate
- **Minimal overhead**: 8-byte header (vs 20+ for TCP)

---

## UDP Use Cases

UDP được **largely preferred cho real-time communications** như broadcast hoặc multicast network transmission.

- **DNS**: Quick query-response
- **DHCP**: IP assignment
- **Video streaming**: Live video, VoIP
- **Gaming**: Real-time multiplayer
- **IoT**: Sensor data

---

## Khi nào dùng UDP over TCP?

> **Use UDP when: Late data is worse than loss of data**

Ví dụ: Video call - nếu packet bị mất, không cần retransmit vì thời điểm đó đã qua rồi.

---

## TCP vs UDP Comparison

| Feature | TCP | UDP |
|---------|-----|-----|
| **Connection** | Requires established connection | Connectionless protocol |
| **Guaranteed delivery** | Can guarantee delivery of data | Cannot guarantee delivery |
| **Re-transmission** | Re-transmission of lost packets is possible | No re-transmission |
| **Speed** | Slower than UDP | Faster than TCP |
| **Broadcasting** | Does not support broadcasting | Supports broadcasting |
| **Header Size** | 20-60 bytes | 8 bytes |
| **Ordering** | Guaranteed ordering | No ordering guarantee |
| **Use cases** | HTTPS, HTTP, SMTP, POP, FTP | Video streaming, DNS, VoIP |

---

# 📞 Domain Name System (DNS)

## DNS là gì?

Trước đó chúng ta đã học về IP addresses cho phép mọi máy kết nối với máy khác. Nhưng như chúng ta biết, con người **comfortable với names hơn numbers**. Dễ nhớ một cái tên như `google.com` hơn là `142.250.190.14`.

Điều này dẫn đến **Domain Name System (DNS)** - một hệ thống naming **hierarchical và decentralized** được sử dụng để translate human-readable domain names thành IP addresses.

---

## Key Components of DNS

| Component | Mô tả |
|-----------|-------|
| **Domain Names** | Human-readable addresses như `example.com` |
| **IP Addresses** | Numerical label assigned to each device |
| **DNS Servers** | Backbone of DNS, handling conversion |

---

## How DNS Works

```
┌─────────────────────────────────────────────────────────────┐
│                  DNS RESOLUTION PROCESS                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ① User types: google.com in browser                        │
│         │                                                    │
│         ▼                                                    │
│  ② Browser Cache: "Do I know google.com?"                   │
│         │ No                                                 │
│         ▼                                                    │
│  ③ OS Cache: "Does the OS know?"                            │
│         │ No                                                 │
│         ▼                                                    │
│  ④ Router Cache: "Does router know?"                        │
│         │ No                                                 │
│         ▼                                                    │
│  ⑤ ISP DNS Resolver: "Let me find out..."                  │
│         │                                                    │
│         ▼                                                    │
│  ⑥ Root Server: "Who handles .com?"                        │
│         │         → TLD server for .com                      │
│         ▼                                                    │
│  ⑦ TLD Server: "Who handles google.com?"                   │
│         │         → Authoritative NS for google.com          │
│         ▼                                                    │
│  ⑧ Authoritative Server: "google.com = 142.250.190.14"     │
│         │                                                    │
│         ▼                                                    │
│  ⑨ Response flows back, cached at each level               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Server Types

### DNS Resolver

**DNS Resolver** (còn gọi là **Recursive Resolver**) là server đầu tiên client contact.

**Functions:**

- Nhận query từ client
- Makes requests đến các servers khác để resolve
- Returns final answer cho client
- Caches results cho future queries

**Public DNS Resolvers:**

```
Google:     8.8.8.8, 8.8.4.4
Cloudflare: 1.1.1.1, 1.0.0.1
OpenDNS:    208.67.222.222, 208.67.220.220
```

### DNS Root Server

**Root Servers** là top của DNS hierarchy. Có 13 logical root server clusters (A through M).

```
.                           ← Root
├── com                     ← TLD
│   ├── google.com          ← Domain
│   └── amazon.com
├── org
│   └── wikipedia.org
└── net
    └── example.net
```

### TLD Nameserver

**TLD (Top-Level Domain) Nameserver** maintains information cho tất cả domain names share một common domain extension: .com, .net, .org, country codes (.vn, .uk, .jp).

### Authoritative DNS Server

**Authoritative DNS Server** là final source of truth cho một domain. Nó chứa actual DNS records và returns definitive answer.

---

## Query Types

| Type | Mô tả |
|------|-------|
| **Recursive** | Client yêu cầu resolver phải return complete answer |
| **Iterative** | Server returns best answer, có thể là referral |
| **Non-recursive** | Server đã có answer trong cache |

---

## Record Types

| Record | Name | Description | Example |
|--------|------|-------------|---------|
| **A** | Address | Domain → IPv4 | `google.com → 142.250.190.14` |
| **AAAA** | IPv6 Address | Domain → IPv6 | `google.com → 2607:f8b0:...` |
| **CNAME** | Canonical Name | Alias | `www.google.com → google.com` |
| **MX** | Mail Exchange | Mail server | `smtp.google.com` |
| **TXT** | Text | Verification, SPF | `v=spf1 include:...` |
| **NS** | Nameserver | DNS servers | `ns1.google.com` |
| **SOA** | Start of Authority | Zone info | Primary NS, admin email |
| **PTR** | Pointer | Reverse lookup | IP → domain |
| **SRV** | Service | Service location | `_http._tcp.example.com` |

---

## Subdomains

**Subdomain** là phần thêm vào trước main domain.

```
        blog.example.com
         │    │       │
         │    │       └── TLD
         │    └────────── Domain
         └─────────────── Subdomain
```

---

## DNS Caching & TTL

### TTL (Time To Live)

**TTL** chỉ định bao lâu record có thể được cached.

```
google.com.  300  IN  A  142.250.190.14
              │
              └── TTL: 300 seconds (5 minutes)
```

**TTL Trade-offs:**

| Short TTL (60s) | Long TTL (86400s) |
|-----------------|-------------------|
| Quick propagation | Slow propagation |
| Higher DNS load | Lower DNS load |
| More resilient | May serve stale data |

### Cache Levels

```
1. Browser cache  (minutes)
2. OS cache       (varies)
3. Router cache   (varies)
4. ISP resolver   (follows TTL)
```

---

## Check DNS Resolver của máy

**Linux:**

```bash
# Xem DNS resolver hiện tại
cat /etc/resolv.conf

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

---

[← IP & OSI](01_IP_OSI.md) | [Tiếp: Load Balancing →](03_LOAD_BALANCING.md)
