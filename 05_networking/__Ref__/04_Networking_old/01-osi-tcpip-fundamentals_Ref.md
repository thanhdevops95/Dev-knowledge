# 📶 Mô hình OSI & TCP/IP — Nền tảng Networking

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Hiểu cách dữ liệu truyền qua mạng

---

## Tại sao cần hiểu mô hình mạng?

Debug "trang web không mở được" — lỗi ở đâu?
- DNS? (Layer 7) → Không resolve được domain
- TCP? (Layer 4) → Connection refused, port bị chặn
- IP? (Layer 3) → Không route được, firewall block
- Vật lý? (Layer 1) → Cáp mạng đứt, WiFi mất

Hiểu layers = **debug nhanh**, **thiết kế mạng đúng**.

---

## 1. Mô hình OSI — 7 tầng

```
┌──────────────────────────────────────────────────────┐
│ Layer 7: APPLICATION    │ HTTP, HTTPS, FTP, SMTP,    │
│ (Ứng dụng)             │ DNS, SSH, WebSocket         │
│                         │ → Giao tiếp với user        │
├─────────────────────────┼────────────────────────────┤
│ Layer 6: PRESENTATION  │ SSL/TLS, Encryption,        │
│ (Trình bày)            │ Compression, JSON/XML       │
│                         │ → Mã hóa, format dữ liệu   │
├─────────────────────────┼────────────────────────────┤
│ Layer 5: SESSION        │ NetBIOS, RPC               │
│ (Phiên)                │ → Quản lý phiên kết nối     │
├─────────────────────────┼────────────────────────────┤
│ Layer 4: TRANSPORT      │ TCP, UDP                   │
│ (Vận chuyển)           │ → Đảm bảo giao hàng đúng   │
├─────────────────────────┼────────────────────────────┤
│ Layer 3: NETWORK        │ IP, ICMP, Routing          │
│ (Mạng)                 │ → Tìm đường đi (routing)    │
├─────────────────────────┼────────────────────────────┤
│ Layer 2: DATA LINK      │ Ethernet, WiFi, MAC        │
│ (Liên kết dữ liệu)    │ → Truyền trong mạng cục bộ  │
├─────────────────────────┼────────────────────────────┤
│ Layer 1: PHYSICAL       │ Cáp mạng, WiFi signal,     │
│ (Vật lý)               │ Fiber optic                 │
│                         │ → Tín hiệu điện/quang       │
└──────────────────────────────────────────────────────┘

Mẹo nhớ (từ dưới lên):
"Please Do Not Throw Sausage Pizza Away"
 Physical Data Network Transport Session Presentation Application
```

---

## 2. Mô hình TCP/IP — 4 tầng (thực tế)

```
OSI (lý thuyết)          TCP/IP (thực tế)
┌─────────────┐         ┌─────────────────┐
│ Application │         │                 │
├─────────────┤         │   Application   │  HTTP, DNS, FTP
│Presentation │         │                 │
├─────────────┤         │                 │
│   Session   │         └────────┬────────┘
├─────────────┤                  │
│  Transport  │         ┌────────┴────────┐
│             │         │    Transport    │  TCP, UDP
├─────────────┤         └────────┬────────┘
│   Network   │         ┌────────┴────────┐
│             │         │    Internet     │  IP, ICMP
├─────────────┤         └────────┬────────┘
│  Data Link  │         ┌────────┴────────┐
├─────────────┤         │ Network Access  │  Ethernet, WiFi
│  Physical   │         │                 │
└─────────────┘         └─────────────────┘
```

---

## 3. TCP vs UDP

### TCP — Tin cậy, có thứ tự

```
TCP 3-Way Handshake (bắt tay 3 bước):

Client ──► SYN ────────────► Server   "Tôi muốn kết nối"
Client ◄── SYN-ACK ◄──────── Server   "OK, tôi sẵn sàng"
Client ──► ACK ────────────► Server   "Bắt đầu truyền!"
           ═══ Connected ═══

Đặc điểm:
✅ Đảm bảo giao hàng (retransmission nếu mất)
✅ Đúng thứ tự (sequence numbers)
✅ Flow control (không gửi quá nhanh)
❌ Chậm hơn UDP (overhead handshake + ACK)

Dùng cho: HTTP, HTTPS, FTP, SSH, Email
```

### UDP — Nhanh, không đảm bảo

```
UDP: Gửi thẳng, không handshake, không ACK

Client ──► Data ──► Server     "Đây, nhận đi!"
Client ──► Data ──► Server     "Thêm nữa!"
Client ──► Data ──► (mất!)     "Mất thì mất, đi tiếp!"

Đặc điểm:
✅ Nhanh (không overhead)
✅ Real-time (không đợi retransmission)
❌ Có thể mất packet
❌ Không đảm bảo thứ tự

Dùng cho: Video call, game online, DNS lookup, live streaming
```

| | TCP | UDP |
|---|---|---|
| **Kết nối** | Connection-oriented | Connectionless |
| **Tin cậy** | ✅ Guaranteed delivery | ❌ Best-effort |
| **Thứ tự** | ✅ Ordered | ❌ Unordered |
| **Tốc độ** | Chậm hơn | ⚡ Nhanh hơn |
| **Header** | 20-60 bytes | 8 bytes |
| **Use case** | Web, email, file transfer | Video, gaming, DNS |

---

## 4. IP Address — Địa chỉ mạng

```
IPv4: 192.168.1.100 (32 bit → ~4.3 tỷ addresses)
IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334 (128 bit → gần vô hạn)

Private IP (mạng nội bộ):
• 10.0.0.0 – 10.255.255.255
• 172.16.0.0 – 172.31.255.255
• 192.168.0.0 – 192.168.255.255

Public IP: Unique trên internet, do ISP cấp

NAT (Network Address Translation):
Nhiều devices (private IP) ──► Router (NAT) ──► Internet (1 public IP)
192.168.1.100 ─┐
192.168.1.101 ─┼──► 113.22.45.100 ──► Internet
192.168.1.102 ─┘
```

### Subnet & CIDR

```
192.168.1.0/24
       │        │
       │        └── /24 = 24 bit network, 8 bit host
       │             = 256 addresses (192.168.1.0 → 192.168.1.255)
       └── Network address

Common subnets:
/32 = 1 address   (single host)
/24 = 256         (small network)
/16 = 65,536      (medium network)
/8  = 16,777,216  (large network)
```

---

## 5. Ports — Cổng

```
IP address = địa chỉ nhà
Port       = số phòng

192.168.1.100:3000
     │           │
     IP          Port

Well-known ports:
  20/21  FTP
  22     SSH
  25     SMTP (email)
  53     DNS
  80     HTTP
  443    HTTPS
  3000   Node.js (dev)
  3306   MySQL
  5432   PostgreSQL
  6379   Redis
  27017  MongoDB
```

---

## 6. Dữ liệu đi qua các tầng

```
Gửi email "Xin chào":

Application:  HTTP Data: "Xin chào"
                    │
Transport:    │ TCP Header │ Data │         → Segment
                    │
Network:      │ IP Header │ TCP │ Data │    → Packet
                    │
Data Link:    │ Frame │ IP │ TCP │ Data │   → Frame
                    │
Physical:     0101001010110100...            → Bits/Signals

Mỗi tầng THÊM header → encapsulation
Bên nhận: BỎ header từng tầng → decapsulation
```

---

## Debug Networking — Tools

```bash
# Layer 1-2: Kết nối vật lý
ping 192.168.1.1               # Kiểm tra connectivity

# Layer 3: IP routing
traceroute google.com           # Xem đường đi packets
ip addr                         # Xem IP addresses
route -n                        # Xem routing table

# Layer 4: TCP/UDP
netstat -tlnp                   # Ports đang listen
ss -tlnp                        # Modern netstat
telnet google.com 80            # Test TCP connection
nc -zv google.com 443           # Test port open

# Layer 7: Application
curl -v https://google.com      # HTTP request chi tiết
dig google.com                  # DNS lookup
nslookup google.com             # DNS query
```

---

## Các lỗi thường gặp

```
❌ Sai: "Port 80 bị chiếm" → chạy 2 app cùng port
✅ Đúng: Mỗi app dùng port khác (3000, 3001) hoặc kill process cũ

❌ Sai: Expose private IP ra internet
✅ Đúng: Private IP chỉ trong mạng nội bộ, dùng NAT/VPN cho external

❌ Sai: Không hiểu TCP vs UDP → chọn sai protocol
✅ Đúng: Web/API = TCP, Video/Game real-time = UDP
```

---

## Bài tập thực hành

- [ ] Dùng Wireshark capture HTTP request → xem TCP 3-way handshake
- [ ] Dùng `traceroute` xem đường đi đến Google (bao nhiêu hops?)
- [ ] Tìm port nào đang mở trên máy bạn (`netstat -tlnp` hoặc `ss -tlnp`)
- [ ] Setup 2 VMs/containers giao tiếp qua private network

---

## Tài nguyên thêm

- [Computer Networking (Kurose & Ross)](https://gaia.cs.umass.edu/kurose_ross/online_lectures.htm) — Bài giảng free
- [Practical Networking](https://www.practicalnetworking.net/) — Networking cho beginners
- [Wireshark](https://www.wireshark.org/) — Capture & analyze network packets
