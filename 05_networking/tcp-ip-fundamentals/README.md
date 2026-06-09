# tcp-ip-fundamentals

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Cập nhật:** 25/05/2026\
> **Status:** ✅ Có bài — cụm `01_basic` đã hoàn chỉnh (5 bài)

## 🎯 Chủ đề này có gì

TCP/IP — bộ giao thức nền của Internet. Cụm bài cơ bản đi từ "TCP/IP là gì" → IP addressing → TCP vs UDP → ports/sockets/firewall → network tools debug.

## 📖 Lessons — 01_basic

| # | Bài | Nội dung |
|---|---|---|
| 00 | [TCP/IP là gì](lessons/01_basic/00_what-is-tcp-ip.md) | 4 layer model, OSI 7 layer, encapsulation |
| 01 | [IP Addressing](lessons/01_basic/01_ip-addressing.md) | IPv4/IPv6, subnet mask, CIDR, NAT |
| 02 | [TCP vs UDP](lessons/01_basic/02_tcp-vs-udp.md) | 3-way handshake, flow/congestion control, QUIC |
| 03 | [Ports, Sockets, Firewall](lessons/01_basic/03_ports-sockets-firewall.md) | Well-known ports, socket tuple, ufw/iptables/SG |
| 04 | [Network Tools](lessons/01_basic/04_network-tools.md) | `ping`, `traceroute`, `ss`, `tcpdump`, `nmap`, `nc`, `iperf3` |

## 🚀 Đọc folder này thế nào

| Nhu cầu | Đọc gì |
|---|---|
| Mới bắt đầu | `lessons/01_basic/00_what-is-tcp-ip.md` rồi đi tuần tự 00 → 04 |
| Tra nhanh port / tool | `lessons/01_basic/03_ports-sockets-firewall.md`, `lessons/01_basic/04_network-tools.md` (có cheatsheet cuối bài) |
| Debug lỗi mạng | `lessons/01_basic/04_network-tools.md` (5 case debug + decision tree) |
| Theo nghề | Xem [`../00_roadmaps/career/`](../../00_roadmaps/career/) chọn career path đi qua networking |

## 📂 Cấu trúc

```
tcp-ip-fundamentals/
├── README.md                ← (file này) index + lộ trình đọc
├── lessons/01_basic/        ← 5 bài cơ bản (đã có)
├── exercises/               ← bài tập (chưa có)
├── recipes/                 ← công thức / troubleshooting (chưa có)
└── setup/                   ← cài đặt + cấu hình (chưa có)
```
