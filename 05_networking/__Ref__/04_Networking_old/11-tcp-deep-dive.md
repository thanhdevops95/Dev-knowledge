# 🔧 TCP Deep Dive — Giao thức truyền tải tin cậy

> `[INTERMEDIATE → ADVANCED]` — Prerequisite: `03-osi-tcp-ip-fundamentals.md`
> Nội bộ TCP: handshake, congestion control, tuning, và troubleshooting.

---

## 1. Three-Way Handshake — Thiết lập kết nối

```
Client                          Server
  │                               │
  │ ──── SYN (seq=100) ────→     │  Step 1: Client gửi SYN
  │                               │
  │ ←── SYN+ACK (seq=200,       │  Step 2: Server gửi SYN+ACK  
  │      ack=101) ──────         │
  │                               │
  │ ──── ACK (ack=201) ────→    │  Step 3: Client gửi ACK
  │                               │
  │ ══ Connection Established ══  │
  │                               │
  │ ←─── Data transfer ───→     │
  │                               │

Tại sao 3-way?
  • Client → Server: "Tôi muốn kết nối" (SYN)
  • Server → Client: "OK, tôi cũng sẵn sàng" (SYN+ACK) 
  • Client → Server: "Nhận được, bắt đầu!" (ACK)
  → Cả 2 bên xác nhận khả năng gửi VÀ nhận
```

### Connection Termination — Four-Way Handshake

```
Client                          Server
  │                               │
  │ ──── FIN ──────────→         │  "Tôi xong rồi"
  │ ←─── ACK ──────────          │  "OK noted"
  │                               │
  │ ←─── FIN ──────────          │  "Tôi cũng xong"
  │ ──── ACK ──────────→         │  "OK bye"
  │                               │
  │   TIME_WAIT (2×MSL)          │  Client chờ trước khi đóng
  │                               │

Tại sao 4-way (không phải 3)?
  Vì mỗi bên cần đóng direction riêng (half-close).
  Server có thể vẫn gửi data sau khi client FIN.
```

---

## 2. TCP vs UDP — Tradeoffs chi tiết

| | TCP | UDP |
|---|---|---|
| **Connection** | Connection-oriented (handshake) | Connectionless |
| **Reliability** | Guaranteed delivery, ordering | Best-effort, no guarantee |
| **Flow control** | Sliding window | None |
| **Congestion control** | CUBIC/BBR | None |
| **Overhead** | 20+ bytes header | 8 bytes header |
| **Latency** | Higher (handshake, retransmit) | Lower |
| **Use case** | HTTP, SSH, email, file transfer | DNS, video streaming, gaming, VoIP |

```
TCP: "Bưu điện đảm bảo" — mọi thư đều đến, đúng thứ tự
UDP: "Ném giấy" — nhanh, nhưng có thể mất hoặc lộn xộn

Khi nào dùng UDP thay TCP?
  • Real-time: video call (mất 1 frame OK, delay KHÔNG OK)
  • Gaming: position update (current state > old state)
  • DNS: query đơn giản, 1 packet đủ
  • IoT: sensor readings, bandwidth limited
```

---

## 3. Congestion Control — Tránh nghẽn mạng

### CUBIC (Linux default)

```
CUBIC adjust gửi bao nhiêu data dựa trên packet loss:

Congestion Window (cwnd):
  1. Slow Start: cwnd doubles mỗi RTT (exponential)
     cwnd: 1 → 2 → 4 → 8 → 16 → ... 
     
  2. Khi loss detected → cwnd giảm mạnh (multiplicative decrease)
     cwnd: 64 → 32
     
  3. Congestion Avoidance: cwnd tăng chậm (cubic function)
     cwnd: 32 → 33 → 34.5 → ...

cwnd ↑
     |     ╱╲
     |    ╱  ╲     ╱╲
     |   ╱    ╲   ╱  ╲
     |  ╱      ╲ ╱    ╲
     | ╱        ╲      ╲
     |╱                  
     └──────────────────── time
          loss events ↓
```

### BBR (Google) — Bandwidth-based

```
BBR (Bottleneck Bandwidth and RTT):
  • Không dùng packet loss làm signal
  • Đo bandwidth + RTT thực tế
  • Tối ưu throughput & latency đồng thời

BBR vs CUBIC:
  CUBIC: "Gửi nhanh hơn cho đến khi mất packet"
  BBR:   "Gửi đúng tốc độ bottleneck bandwidth"

Enable BBR (Linux):
  echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
  echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
  sysctl -p
```

---

## 4. Nagle's Algorithm & TCP_NODELAY

```
Nagle's Algorithm:
  Buffer small writes → combine into larger segments
  → Giảm số lượng small packets trên network
  → Tăng latency vì phải chờ buffer đầy hoặc ACK

Vấn đề: interactive apps (SSH, gaming, mouse movement)
  Gõ 1 ký tự → Nagle buffer → delay 200ms → hiển thị

Giải pháp: TCP_NODELAY
  Disable Nagle → gửi data ngay lập tức
```

```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Disable Nagle
```

---

## 5. TIME_WAIT — Tại sao exist?

```
Sau connection close → port ở trạng thái TIME_WAIT 60-120 giây

Tại sao?
  1. Đảm bảo ACK cuối cùng đến server
     (nếu mất → server resend FIN → client retransmit ACK)
  2. Tránh old duplicate packets ảnh hưởng new connection
     trên cùng port

Vấn đề: High-traffic server → hàng nghìn TIME_WAIT → hết port!

Fix:
  # Linux tuning
  echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse        # Reuse TIME_WAIT ports
  echo 30 > /proc/sys/net/ipv4/tcp_fin_timeout     # Giảm FIN timeout
```

---

## 6. TCP Tuning cho High Performance

```bash
# /etc/sysctl.conf — Linux TCP tuning

# Buffer sizes (tăng cho high bandwidth-delay product)
net.core.rmem_max = 16777216          # Max receive buffer
net.core.wmem_max = 16777216          # Max send buffer
net.ipv4.tcp_rmem = 4096 87380 16777216   # Min/Default/Max
net.ipv4.tcp_wmem = 4096 65536 16777216

# Connection handling
net.core.somaxconn = 65535            # Max backlog queue
net.ipv4.tcp_max_syn_backlog = 65535  # Max SYN queue
net.core.netdev_max_backlog = 5000   # Network device backlog

# Keepalive (detect dead connections)
net.ipv4.tcp_keepalive_time = 600     # Start probing after 600s idle
net.ipv4.tcp_keepalive_probes = 5     # 5 probes before killing
net.ipv4.tcp_keepalive_intvl = 15     # 15s between probes

# Apply
sysctl -p
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Disable Nagle cho mọi thứ | Chỉ disable cho interactive/realtime | Bulk transfer cần Nagle giảm overhead |
| 2 | Panic khi thấy TIME_WAIT | TIME_WAIT là BÌNH THƯỜNG | Chỉ fix khi hết port (quá nhiều) |
| 3 | BBR cho mọi server | BBR tốt cho WAN, CUBIC có thể tốt hơn cho LAN | Test cả 2, đo throughput thực tế |
| 4 | `tcp_tw_recycle` (Linux < 4.12) | Bỏ — gây lỗi với NAT | Đã bị remove khỏi kernel |

---

## Bài tập thực hành

- [ ] **Bài 1 (Trung bình):** Dùng Wireshark capture TCP 3-way handshake và FIN
- [ ] **Bài 2 (Trung bình):** So sánh throughput TCP_NODELAY on vs off bằng iperf3
- [ ] **Bài 3 (Khó):** Enable BBR trên Linux, benchmark so với CUBIC
- [ ] **Bài 4 (Khó):** Tune TCP parameters cho web server xử lý 10K concurrent connections

---

## Tài nguyên thêm

- [TCP/IP Illustrated Vol.1 (Stevens)](https://www.amazon.com/TCP-Illustrated-Vol-Addison-Wesley-Professional/dp/0201633469) — Gold standard book
- [High Performance Browser Networking (Ilya Grigorik)](https://hpbn.co/) — Free online book ⭐
- [BBR Paper (Google)](https://research.google/pubs/pub45646/) — Congestion control research
- [Linux Kernel Networking](https://www.kernel.org/doc/Documentation/networking/) — Kernel docs
