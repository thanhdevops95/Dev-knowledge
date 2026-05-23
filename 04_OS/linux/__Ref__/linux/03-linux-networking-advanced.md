# 🌐 Linux Networking — Mạng trên Linux

> `[INTERMEDIATE → ADVANCED]` — Prerequisite: `01-linux-essentials-basics.md`, `04-Networking/`
> Cấu hình mạng, troubleshooting, và firewall trên Linux.

---

## 1. Network Interfaces & IP Config

```bash
# ── Xem IP & interfaces ──
ip addr show              # Tất cả interfaces (thay ifconfig)
ip addr show eth0         # Interface cụ thể
ip -br addr               # Brief format ⭐
ip link show              # Link layer info

# ── Cấu hình IP tạm thời ──
sudo ip addr add 192.168.1.100/24 dev eth0
sudo ip addr del 192.168.1.100/24 dev eth0
sudo ip link set eth0 up     # Enable interface
sudo ip link set eth0 down   # Disable interface

# ── Netplan (Ubuntu 18.04+) ──
# /etc/netplan/01-config.yaml
# network:
#   version: 2
#   ethernets:
#     eth0:
#       dhcp4: false
#       addresses:
#         - 192.168.1.100/24
#       routes:
#         - to: default
#           via: 192.168.1.1
#       nameservers:
#         addresses: [8.8.8.8, 8.8.4.4]

sudo netplan apply          # Apply config

# ── Routing ──
ip route show               # Routing table
ip route get 8.8.8.8        # How to reach IP
sudo ip route add 10.0.0.0/8 via 192.168.1.1 dev eth0
```

---

## 2. DNS

```bash
# ── DNS resolution ──
nslookup google.com
dig google.com              # Detailed DNS query
dig google.com +short       # Just the IP
dig -x 8.8.8.8              # Reverse DNS
host google.com             # Simple DNS lookup

# resolvectl — systemd-resolved
resolvectl status
resolvectl query google.com

# ── DNS config ──
cat /etc/resolv.conf        # DNS servers
# nameserver 8.8.8.8
# nameserver 8.8.4.4

# ── /etc/hosts — local DNS override ──
sudo vim /etc/hosts
# 127.0.0.1  myapp.local
# 192.168.1.50  db.internal
```

---

## 3. Sockets & Ports

```bash
# ── ss — Socket statistics (thay netstat) ──
ss -tuln                    # TCP/UDP listening ports ⭐
ss -tlnp                    # TCP listening + process name
ss -s                       # Socket summary
ss -t state established     # Established connections

# ── Tìm process dùng port ──
ss -tlnp | grep :8080
lsof -i :3000               # Process using port 3000
fuser 80/tcp                 # PID using port 80

# ── Check kết nối ──
nc -zv host 80              # Test TCP connection
nc -zv host 22              # Test SSH
telnet host 80              # Telnet test (deprecated)
```

---

## 4. Firewall — iptables & nftables

### iptables (classic)

```bash
# ── View rules ──
sudo iptables -L -v -n      # List all rules
sudo iptables -L -t nat     # NAT table

# ── Basic rules ──
# Allow SSH
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
# Allow HTTP/HTTPS
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
# Allow established connections
sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
# Allow loopback
sudo iptables -A INPUT -i lo -j ACCEPT
# Drop everything else
sudo iptables -A INPUT -j DROP

# ── Save & Restore ──
sudo iptables-save > /etc/iptables.rules
sudo iptables-restore < /etc/iptables.rules

# ── Delete rule ──
sudo iptables -D INPUT -p tcp --dport 8080 -j ACCEPT
sudo iptables -F                 # Flush all rules ⚠️
```

### nftables (modern replacement)

```bash
# /etc/nftables.conf
# table inet filter {
#     chain input {
#         type filter hook input priority 0;
#         ct state established,related accept
#         iif lo accept
#         tcp dport { 22, 80, 443 } accept
#         drop
#     }
# }

sudo nft list ruleset
sudo nft add rule inet filter input tcp dport 8080 accept
```

---

## 5. Troubleshooting Network Issues

### Diagnostic commands

```bash
# ── Connectivity ──
ping -c 4 8.8.8.8           # Test internet
ping -c 4 192.168.1.1       # Test gateway
traceroute google.com        # Trace hops
mtr google.com               # Continuous traceroute ⭐

# ── Bandwidth & Performance ──
iperf3 -s                    # Start server
iperf3 -c server-ip          # Test bandwidth to server
speedtest-cli                # Internet speed test

# ── Packet capture ──
sudo tcpdump -i eth0 port 80                    # Capture HTTP
sudo tcpdump -i eth0 -w capture.pcap            # Save to file
sudo tcpdump -i eth0 host 192.168.1.100         # Specific host
sudo tcpdump -i eth0 'tcp port 443 and host google.com'  # Complex filter

# Analyze in Wireshark
wireshark capture.pcap       # GUI analysis
tshark -r capture.pcap       # CLI analysis
```

### Troubleshooting Flowchart

```
Can't reach server?
│
├─ ping localhost → FAIL? → Network stack broken
│
├─ ping gateway (192.168.1.1) → FAIL? → Local network issue
│
├─ ping 8.8.8.8 → FAIL? → Internet/routing issue
│
├─ ping google.com → FAIL? → DNS issue
│   └─ Check /etc/resolv.conf
│
├─ curl http://server:80 → FAIL? → Firewall or service issue
│   ├─ ss -tlnp | grep :80 → Service listening?
│   └─ iptables -L → Firewall blocking?
│
└─ curl https://server:443 → FAIL? → SSL/TLS issue
    └─ openssl s_client -connect server:443
```

---

## 6. VPN & Tunneling

```bash
# ── SSH Tunnel ──
# Local port forwarding: access remote:5432 via localhost:5432
ssh -L 5432:localhost:5432 user@server

# Remote port forwarding: expose local:3000 on server:8080
ssh -R 8080:localhost:3000 user@server

# SOCKS proxy
ssh -D 1080 user@server
# Browser settings: SOCKS proxy localhost:1080

# ── WireGuard VPN ──
sudo apt install wireguard
# /etc/wireguard/wg0.conf
# [Interface]
# PrivateKey = <private_key>
# Address = 10.0.0.1/24
# ListenPort = 51820
# 
# [Peer]
# PublicKey = <peer_public_key>
# AllowedIPs = 10.0.0.2/32
# Endpoint = peer_ip:51820

sudo wg-quick up wg0
sudo wg show                # Status
sudo wg-quick down wg0
```

---

## 7. Network Namespaces — Container Networking Basics

```bash
# Container networking = Linux network namespaces

# Create namespace
sudo ip netns add my-ns

# List namespaces
ip netns list

# Run command in namespace
sudo ip netns exec my-ns ip addr show

# Connect namespaces with veth pair
sudo ip link add veth0 type veth peer name veth1
sudo ip link set veth1 netns my-ns
sudo ip addr add 10.0.0.1/24 dev veth0
sudo ip netns exec my-ns ip addr add 10.0.0.2/24 dev veth1
sudo ip link set veth0 up
sudo ip netns exec my-ns ip link set veth1 up

# Test connectivity
sudo ip netns exec my-ns ping 10.0.0.1
# → Đây chính là cách Docker network hoạt động!
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | `iptables -F` khi SSH | Đảm bảo rule SSH ACCEPT trước khi flush | Flush xong → lock yourself out |
| 2 | Dùng `ifconfig` | Dùng `ip addr` | ifconfig deprecated, ip là standard |
| 3 | Hard-code DNS trong app | Dùng `/etc/hosts` hoặc DNS service | Config centralized |
| 4 | Quên persistent firewall rules | Save iptables rules hoặc dùng ufw | Reboot → rules mất |

---

## Bài tập thực hành

- [ ] **Bài 1 (Trung bình):** Configure static IP bằng Netplan
- [ ] **Bài 2 (Trung bình):** Setup iptables: allow SSH + HTTP, deny all else
- [ ] **Bài 3 (Khó):** Capture packets với tcpdump, analyze trong Wireshark
- [ ] **Bài 4 (Khó):** Create network namespaces + veth pair (simulate Docker networking)

---

## Tài nguyên thêm

- [Linux Network Administrator's Guide](https://tldp.org/LDP/nag2/index.html) — Comprehensive reference
- [DigitalOcean — Linux Networking](https://www.digitalocean.com/community/tutorials?q=linux+networking) — Practical guides
- [Container Networking (Michael Kerrisk)](https://lwn.net/Articles/580893/) — Network namespaces deep dive
- [nftables Wiki](https://wiki.nftables.org/) — Modern firewall reference
