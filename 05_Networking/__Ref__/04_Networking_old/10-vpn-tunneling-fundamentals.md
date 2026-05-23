# 🔒 VPN & Tunneling — Kết nối an toàn qua mạng công cộng

> `[INTERMEDIATE]` — Prerequisite: hiểu networking cơ bản, TCP/IP
> Bảo vệ traffic, truy cập remote resources, bypass restrictions.

---

## 1. VPN là gì?

**VPN (Virtual Private Network)** tạo "đường hầm" mã hóa giữa thiết bị của bạn và VPN server. Toàn bộ traffic đi qua tunnel → ISP/hackers không đọc được.

```
Không có VPN:
  You ──[plain text]──→ ISP ──→ Internet ──→ Server
  ISP thấy: "User truy cập facebook.com, xem video X"

Có VPN:
  You ──[encrypted tunnel]──→ VPN Server ──→ Internet ──→ Server
  ISP thấy: "User kết nối đến IP 1.2.3.4 (VPN), nội dung: 🔒"
```

---

## 2. VPN Protocols

### WireGuard — Modern (Recommended ⭐)

```bash
# Simple, fast, secure — chỉ ~4000 dòng code
# Performance: ~1Gbps throughput, ~0.2ms overhead

# Server setup
sudo apt install wireguard
wg genkey | tee server_private.key | wg pubkey > server_public.key

# /etc/wireguard/wg0.conf (Server)
[Interface]
PrivateKey = <server_private_key>
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = <client_public_key>
AllowedIPs = 10.0.0.2/32

# Client setup
[Interface]
PrivateKey = <client_private_key>
Address = 10.0.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = <server_public_key>
Endpoint = server_ip:51820
AllowedIPs = 0.0.0.0/0    # Route ALL traffic through VPN
PersistentKeepalive = 25

# Start/Stop
sudo wg-quick up wg0
sudo wg-quick down wg0
sudo wg show               # Status
```

### OpenVPN — Battle-tested

```
OpenVPN: proven, widely supported, nhưng chậm hơn WireGuard
- Uses OpenSSL for encryption
- TCP (reliable, slower) hoặc UDP (faster, default)
- ~100x more code than WireGuard
```

### IPSec — Enterprise standard

```
IPSec: phức tạp nhưng là enterprise standard
- IKEv2/IPSec: tốt cho mobile (fast reconnect)
- L2TP/IPSec: legacy, vẫn dùng
- Tích hợp sẵn trong Windows, macOS, iOS, Android
```

### So sánh

| | WireGuard | OpenVPN | IKEv2/IPSec |
|---|---|---|---|
| **Speed** | ⚡ Fastest | Moderate | Fast |
| **Simplicity** | 4K lines | 100K+ lines | Complex |
| **Mobile** | Good | Good | ⭐ Best (reconnect) |
| **Maturity** | Newer (2020+) | Proven (2001+) | Enterprise standard |
| **Port** | UDP 51820 | UDP 1194 / TCP 443 | UDP 500/4500 |

---

## 3. SSH Tunneling — Quick & Dirty VPN

### Local Port Forwarding

```bash
# Access remote service through SSH tunnel
# Scenario: Database on remote server, only accessible locally
ssh -L 5432:localhost:5432 user@server

# Now connect to localhost:5432 → forwards to server:5432
psql -h localhost -p 5432 -U myuser

# Diagram:
# Laptop:5432 ──[SSH tunnel]──→ Server ──→ localhost:5432 (PostgreSQL)
```

### Remote Port Forwarding

```bash
# Expose local service to internet through SSH
ssh -R 8080:localhost:3000 user@public-server

# Anyone accessing public-server:8080 → forwards to your localhost:3000
# Useful for demos, webhooks testing

# Diagram:
# Internet ──→ public-server:8080 ──[SSH tunnel]──→ Laptop:3000
```

### Dynamic Port Forwarding (SOCKS Proxy)

```bash
# Turn SSH into SOCKS5 proxy — route ANY traffic
ssh -D 1080 user@server

# Configure browser: SOCKS proxy → localhost:1080
# ALL browser traffic → encrypted through SSH to server → internet
```

---

## 4. Site-to-Site vs Client VPN

```
Site-to-Site VPN:
  Office A ──[VPN]──→ AWS VPC
  • Kết nối 2 networks permanently
  • Hardware VPN gateway hoặc software
  • Dùng cho hybrid cloud, multi-site

Client VPN:
  Employee laptop ──[VPN]──→ Company network
  • Individual devices connect remotely
  • WireGuard/OpenVPN client  
  • Dùng cho remote work
```

---

## 5. Split Tunneling

```
Full Tunnel (default):
  ALL traffic → VPN → Internet
  ✅ Complete privacy
  ❌ Slow (everything goes through VPN)

Split Tunnel:
  Company traffic → VPN → Company network
  Other traffic  → Direct → Internet
  ✅ Faster for general browsing
  ❌ Less private for non-VPN traffic

WireGuard split tunnel:
[Peer]
AllowedIPs = 10.0.0.0/8, 172.16.0.0/12   # Only company IPs through VPN
# AllowedIPs = 0.0.0.0/0                  # Full tunnel
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | VPN = anonymous | VPN chỉ encrypt tunnel, VPN server vẫn thấy traffic | Dùng Tor cho anonymity |
| 2 | Quên DNS leak | Config DNS qua VPN (`DNS = 1.1.1.1` trong WireGuard) | ISP DNS resolve → leak visited sites |
| 3 | SSH tunnel cho production | Dùng proper VPN cho production | SSH tunnel = quick hack, không scalable |
| 4 | Expose WireGuard port không firewall | UFW allow chỉ WireGuard port | Limit exposure |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** Setup SSH local port forwarding để access remote database
- [ ] **Bài 2 (Trung bình):** Setup WireGuard VPN giữa 2 VPS
- [ ] **Bài 3 (Khó):** Config split tunneling — company traffic qua VPN, rest direct

---

## Tài nguyên thêm

- [WireGuard Quick Start](https://www.wireguard.com/quickstart/) — Official docs
- [SSH Tunneling Explained](https://www.ssh.com/academy/ssh/tunneling) — SSH Academy
- [OpenVPN Community](https://openvpn.net/community/) — OpenVPN docs
