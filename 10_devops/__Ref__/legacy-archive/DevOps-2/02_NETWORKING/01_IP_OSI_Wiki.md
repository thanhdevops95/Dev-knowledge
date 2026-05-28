# 01. IP Address & OSI Model

[← Về README](README.md) | [Tiếp: TCP/UDP/DNS →](02_TCP_UDP_DNS.md)

---

# 📚 Bảng thuật ngữ

Trước khi bắt đầu, hãy làm quen với các thuật ngữ quan trọng trong bài học này:

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **IP** | /ˌaɪˈpiː/ | Internet Protocol - Giao thức định địa chỉ và định tuyến trên mạng |
| **IPv4** | - | IP phiên bản 4 - Địa chỉ 32-bit, dạng số thập phân (192.168.1.1) |
| **IPv6** | - | IP phiên bản 6 - Địa chỉ 128-bit, dạng số hex (2001:db8::1) |
| **Octet** | /ɒkˈtet/ | Nhóm 8 bit - IPv4 có 4 octets |
| **Public IP** | - | Địa chỉ công khai - Có thể truy cập từ Internet |
| **Private IP** | - | Địa chỉ nội bộ - Chỉ dùng trong mạng LAN |
| **Static IP** | - | Địa chỉ tĩnh - Không thay đổi theo thời gian |
| **Dynamic IP** | - | Địa chỉ động - Được cấp tự động bởi DHCP |
| **DHCP** | /ˌdiːeɪtʃsiːˈpiː/ | Dynamic Host Configuration Protocol - Giao thức cấp IP tự động |
| **Subnet** | - | Mạng con - Phân chia mạng lớn thành các phần nhỏ hơn |
| **CIDR** | /ˈsaɪdər/ | Classless Inter-Domain Routing - Cách biểu diễn dải IP (vd: /24) |
| **NAT** | /næt/ | Network Address Translation - Chuyển đổi địa chỉ mạng |
| **OSI** | /ˌəʊ.esˈaɪ/ | Open Systems Interconnection - Mô hình 7 lớp mạng |
| **Layer** | - | Lớp - Mỗi tầng trong mô hình OSI có chức năng riêng |
| **MAC Address** | - | Media Access Control - Địa chỉ vật lý của thiết bị mạng |
| **Broadcast** | - | Gửi dữ liệu đến tất cả thiết bị trong mạng |
| **Routing** | - | Định tuyến - Xác định đường đi cho dữ liệu qua mạng |
| **Packet** | - | Gói tin - Đơn vị dữ liệu truyền trên mạng |

---

# 🤔 Tại sao DevOps cần biết về IP và OSI?

## Nỗi đau thực tế

> "Server không kết nối được, mà tao không biết debug từ đâu"

> "Sếp hỏi tại sao 2 container không nói chuyện được với nhau"

> "Khách hàng ở Việt Nam than chậm, nhưng server đặt ở US thì làm sao?"

## Kiến thức này giúp bạn

| Tình huống | Cần biết |
|------------|----------|
| Container không kết nối được | Hiểu IP addressing, networking modes |
| Thiết kế mạng nội bộ công ty | Subnetting, CIDR |
| Debug "Connection refused" | OSI Layer troubleshooting |
| Cấu hình firewall rules | Public/Private IP, Ports |
| Optimize network performance | Hiểu data flow qua các layers |

Hiểu IP và OSI Model giống như hiểu bản đồ trước khi đi du lịch - bạn sẽ biết mình đang ở đâu và cần đi đâu khi gặp vấn đề.

---

# 🔢 IP (Internet Protocol)

## IP là gì?

**IP (Internet Protocol)** là giao thức cơ bản của Internet, chịu trách nhiệm đánh địa chỉ và định tuyến các gói tin (packets) giữa các thiết bị trên mạng.

Mỗi thiết bị tham gia mạng cần một **IP address** duy nhất - giống như mỗi ngôi nhà cần một địa chỉ để bưu điện gửi thư đến đúng nơi.

---

## Versions

### IPv4

**IPv4 (Internet Protocol version 4)** là phiên bản IP được sử dụng rộng rãi nhất hiện nay.

**Cấu trúc:**

```
192.168.1.100
 │   │   │  │
 │   │   │  └── Octet 4 (0-255)
 │   │   └───── Octet 3 (0-255)
 │   └───────── Octet 2 (0-255)
 └───────────── Octet 1 (0-255)
```

**Đặc điểm:**

- **32-bit** address space
- **4 octets** phân cách bởi dấu chấm
- Mỗi octet có giá trị từ **0 đến 255**
- Tổng cộng **~4.3 tỷ** địa chỉ duy nhất
- Đang **cạn kiệt** do số lượng thiết bị tăng nhanh

**Ví dụ IPv4:**

```
192.168.1.1     # Private IP (home network)
10.0.0.1        # Private IP (corporate)
8.8.8.8         # Google DNS (public)
172.217.14.206  # Google.com (public)
```

### IPv6

**IPv6 (Internet Protocol version 6)** được thiết kế để thay thế IPv4 với không gian địa chỉ lớn hơn nhiều.

**Cấu trúc:**

```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
 │    │    │    │    │    │    │    │
 └────┴────┴────┴────┴────┴────┴────┴── 8 groups of 4 hex digits
```

**Đặc điểm:**

- **128-bit** address space
- **8 groups** of 4 hexadecimal digits
- Phân cách bởi dấu **hai chấm (:)**
- Tổng cộng **~340 undecillion** (3.4×10^38) địa chỉ
- Loại bỏ nhu cầu **NAT** trong hầu hết trường hợp

**Rút gọn IPv6:**

```
Full:     2001:0db8:0000:0000:0000:0000:0000:0001
Compact:  2001:db8::1   (bỏ leading zeros và thay :: cho consecutive zeros)
```

### So sánh IPv4 vs IPv6

| Feature | IPv4 | IPv6 |
|---------|------|------|
| Address Size | 32-bit | 128-bit |
| Format | Decimal (192.168.1.1) | Hexadecimal (2001:db8::1) |
| Total Addresses | ~4.3 billion | ~340 undecillion |
| Header Size | 20-60 bytes | 40 bytes (fixed) |
| Checksum | Yes | No (relies on link layer) |
| NAT Required | Common | Rarely needed |
| IPSec | Optional | Built-in |
| Broadcast | Yes | No (uses multicast) |

---

## Types of IP Addresses

### Public IP

**Public IP** là địa chỉ có thể truy cập trực tiếp từ Internet.

**Đặc điểm:**

- Globally unique - không có 2 thiết bị có cùng public IP
- Được cấp bởi **ISP (Internet Service Provider)**
- Cần thiết để host websites, servers, services
- Có thể là **static** (cố định) hoặc **dynamic** (thay đổi)

**Ví dụ:**

```
Google DNS:     8.8.8.8
Cloudflare:     1.1.1.1
Your ISP:       103.15.200.50
```

### Private IP

**Private IP** là địa chỉ dùng trong mạng nội bộ, không thể truy cập trực tiếp từ Internet.

**Private IP Ranges (RFC 1918):**

| Class | Range | CIDR | Addresses |
|-------|-------|------|-----------|
| A | 10.0.0.0 - 10.255.255.255 | 10.0.0.0/8 | 16,777,216 |
| B | 172.16.0.0 - 172.31.255.255 | 172.16.0.0/12 | 1,048,576 |
| C | 192.168.0.0 - 192.168.255.255 | 192.168.0.0/16 | 65,536 |

**Đặc điểm:**

- Có thể **reused** trong các mạng khác nhau
- Không routing trực tiếp trên Internet
- Cần **NAT** để truy cập Internet
- Miễn phí, không cần đăng ký

### Static IP

**Static IP** là địa chỉ được cấu hình thủ công và không thay đổi theo thời gian.

**Use cases:**

- Web servers, mail servers
- DNS servers
- Printers, network devices
- VPN endpoints

### Dynamic IP

**Dynamic IP** là địa chỉ được cấp tự động bởi **DHCP server** và có thể thay đổi.

**DHCP Process:**

```
┌────────────┐                    ┌─────────────┐
│   Client   │                    │ DHCP Server │
└─────┬──────┘                    └──────┬──────┘
      │                                  │
      │──── DHCPDISCOVER (broadcast) ───►│
      │                                  │
      │◄──── DHCPOFFER (IP available) ───│
      │                                  │
      │──── DHCPREQUEST (accept IP) ────►│
      │                                  │
      │◄──── DHCPACK (confirmed) ────────│
      │                                  │
```

### Special IP Addresses

| IP Address | Mục đích | Giải thích |
|------------|----------|------------|
| `127.0.0.1` | Localhost | Loopback - gửi traffic về chính máy |
| `0.0.0.0` | All interfaces | Bind to all available interfaces |
| `255.255.255.255` | Broadcast | Gửi đến tất cả devices trong network |
| `169.254.x.x` | Link-local | APIPA - khi DHCP fail |

---

## Subnetting

### Subnet là gì?

**Subnet (subnetwork)** là việc chia một network lớn thành các networks nhỏ hơn để:

- Cải thiện **performance** (giảm broadcast domain)
- Tăng **security** (isolate networks)
- Sử dụng IP hiệu quả hơn

### CIDR Notation

**CIDR (Classless Inter-Domain Routing)** là cách biểu diễn IP range.

```
192.168.1.0/24
     │        │
     │        └── Prefix length (số bit cho network)
     └────────── Network address
```

**Common CIDR Blocks:**

| CIDR | Subnet Mask | Addresses | Usable |
|------|-------------|-----------|--------|
| /8 | 255.0.0.0 | 16,777,216 | 16,777,214 |
| /16 | 255.255.0.0 | 65,536 | 65,534 |
| /24 | 255.255.255.0 | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 126 |
| /26 | 255.255.255.192 | 64 | 62 |
| /27 | 255.255.255.224 | 32 | 30 |
| /28 | 255.255.255.240 | 16 | 14 |
| /30 | 255.255.255.252 | 4 | 2 |
| /32 | 255.255.255.255 | 1 | 1 |

### Ví dụ Subnetting thực tế

**Yêu cầu:** Thiết kế network cho công ty với:

- 50 developers
- 30 marketing
- 10 executives
- 20 servers

**Solution:**

```
Company Network: 10.0.0.0/16

├── Developers:  10.0.1.0/26   (64 IPs, 62 usable)
├── Marketing:   10.0.2.0/26   (64 IPs, 62 usable)
├── Executives:  10.0.3.0/28   (16 IPs, 14 usable)
└── Servers:     10.0.10.0/27  (32 IPs, 30 usable)
```

---

## NAT (Network Address Translation)

### NAT là gì?

**NAT** cho phép nhiều devices dùng chung một Public IP.

```
┌─────────────────────────────────────────────────────────────┐
│                         NAT FLOW                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Device A (192.168.1.10) ─┐                                  │
│                           │      ┌────────┐                  │
│  Device B (192.168.1.20) ─┼─────►│  NAT   │────► Internet    │
│                           │      │ Router │   (103.15.1.50)  │
│  Device C (192.168.1.30) ─┘      └────────┘                  │
│                                                              │
│  Internal IPs ─────────────────► Single Public IP            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### NAT Types

| Type | Mô tả | Use case |
|------|-------|----------|
| **SNAT** | Source NAT - đổi source IP | Outbound traffic |
| **DNAT** | Destination NAT - đổi dest IP | Inbound (port forwarding) |
| **PAT** | Port Address Translation | Multiple devices share 1 IP |

---

# 🏗️ OSI Model

## OSI Model là gì?

**OSI (Open Systems Interconnection) Model** là một mô hình khái niệm mô tả cách dữ liệu di chuyển qua mạng. Model này chia network communication thành **7 layers**, mỗi layer có responsibility riêng.

OSI Model được xem như **universal language** cho computer networking. Nó dựa trên concept chia một hệ thống communication thành 7 abstract layers, mỗi layer được xây dựng trên layer bên dưới.

## Tại sao OSI Model quan trọng?

**1. Troubleshooting có hệ thống:**

```
"Website không load được"
├── Layer 7: HTTP status code?
├── Layer 4: Port có open?
├── Layer 3: Ping được không?
├── Layer 2: MAC address đúng?
└── Layer 1: Cable có kết nối?
```

**2. Abstraction:** Mỗi layer chỉ cần biết interface với layer liền kề.

**3. Interoperability:** Thiết bị từ các vendors khác nhau có thể communicate.

---

## 7 Layers chi tiết

### Layer 7: Application Layer

**Định nghĩa:**

Application Layer là layer **duy nhất tương tác trực tiếp với data từ user**. Software applications như web browsers và email clients dựa vào application layer để khởi tạo communication.

Tuy nhiên, cần hiểu rằng **client software applications KHÔNG phải là một phần của application layer**. Application layer chịu trách nhiệm cho **protocols và data manipulation** mà software dựa vào để present meaningful data cho user.

**Protocols phổ biến:**

| Protocol | Port | Mô tả |
|----------|------|-------|
| HTTP | 80 | Web traffic (unencrypted) |
| HTTPS | 443 | Web traffic (encrypted) |
| FTP | 21 | File transfer |
| SMTP | 25 | Email sending |
| POP3 | 110 | Email retrieval |
| IMAP | 143 | Email access |
| DNS | 53 | Domain name resolution |
| SSH | 22 | Secure shell |

---

### Layer 6: Presentation Layer

**Định nghĩa:**

Presentation Layer còn được gọi là **Translation Layer**. Data từ application layer được extract và manipulate theo format cần thiết để truyền qua network.

**Functions:**

| Function | Mô tả |
|----------|-------|
| **Translation** | Convert data formats (EBCDIC ↔ ASCII), character encoding |
| **Encryption/Decryption** | SSL/TLS encryption, data security |
| **Compression** | Reduce data size (gzip, deflate) |

---

### Layer 5: Session Layer

**Định nghĩa:**

Session Layer chịu trách nhiệm **opening và closing communication** giữa hai devices. Thời gian giữa khi communication được open và closed được gọi là **session**.

**Functions:**

| Function | Mô tả |
|----------|-------|
| **Session Establishment** | Authentication, Authorization |
| **Session Maintenance** | Keep-alive, reconnection |
| **Synchronization** | Checkpoints, recovery from failures |

---

### Layer 4: Transport Layer

**Định nghĩa:**

Transport Layer chịu trách nhiệm **end-to-end communication** giữa hai devices.

**Functions:**

| Function | Mô tả |
|----------|-------|
| **Segmentation** | Chia data thành segments |
| **Flow Control** | Prevent sender overwhelming receiver |
| **Error Control** | Detect lost segments, retransmission |

**Protocols:** TCP, UDP

---

### Layer 3: Network Layer

**Định nghĩa:**

Network Layer chịu trách nhiệm **facilitating data transfer giữa hai networks khác nhau**. Nếu hai devices đang communicate ở cùng một network, thì network layer không cần thiết.

**Functions:**

| Function | Mô tả |
|----------|-------|
| **Logical Addressing** | IP addresses |
| **Routing** | Find best path |
| **Packet Forwarding** | Move packets between networks |

**Devices:** Routers, Layer 3 switches

---

### Layer 2: Data Link Layer

**Định nghĩa:**

Data Link Layer **facilitates data transfer giữa hai devices trên CÙNG một network**. Layer này lấy packets và chia thành **frames**.

**Sub-layers:**

| Sub-layer | Function |
|-----------|----------|
| **LLC** | Flow control, error detection, interface with Network layer |
| **MAC** | Physical addressing (MAC address), access control |

**MAC Address:**

```
00:1A:2B:3C:4D:5E
└──────┼──────┘
 First 3: Manufacturer (OUI)
 Last 3:  Device ID
```

**Devices:** Switches, NICs, Bridges

---

### Layer 1: Physical Layer

**Định nghĩa:**

Physical Layer bao gồm **physical equipment** involved trong data transfer. Đây là layer nơi data được convert thành **bit stream** (1s và 0s).

**Components:**

| Type | Examples |
|------|----------|
| Cables | Ethernet (Cat5e, Cat6), Fiber optic |
| Connectors | RJ-45, LC, SC |
| Signals | Electrical, Light, Radio waves |

---

## OSI vs TCP/IP Model

```
┌─────────────────────┬─────────────────────┐
│      OSI Model      │    TCP/IP Model     │
├─────────────────────┼─────────────────────┤
│ 7. Application      │                     │
├─────────────────────┤  4. Application     │
│ 6. Presentation     │                     │
├─────────────────────┤                     │
│ 5. Session          │                     │
├─────────────────────┼─────────────────────┤
│ 4. Transport        │  3. Transport       │
├─────────────────────┼─────────────────────┤
│ 3. Network          │  2. Internet        │
├─────────────────────┼─────────────────────┤
│ 2. Data Link        │                     │
├─────────────────────┤  1. Network Access  │
│ 1. Physical         │                     │
└─────────────────────┴─────────────────────┘
```

---

[← Về README](README.md) | [Tiếp: TCP/UDP/DNS →](02_TCP_UDP_DNS.md)
