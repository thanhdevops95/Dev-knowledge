# 🎓 Network Tools — `ping`, `traceroute`, `ss`, `tcpdump`, `nmap` & friends

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [Ports, Sockets, Firewall](03_ports-sockets-firewall.md)

> 🎯 *Học 7 CLI tool debug mạng thật sự dùng: **ping**, **traceroute/tracepath**, **netstat/ss**, **tcpdump**, **nmap**, **nc (netcat)**, **iperf3**. Mỗi tool có 1 layer/khía cạnh riêng. Sau bài này bạn debug được 95% lỗi mạng.*

## 🎯 Sau bài này bạn sẽ

- [ ] `ping` test **layer 3** reachability + đo RTT + packet loss
- [ ] `traceroute` trace **đường đi** packet qua các hop
- [ ] `ss` / `netstat` xem **socket state** trên máy mình
- [ ] `nc` (netcat) test **port mở** + transfer data nhanh
- [ ] `tcpdump` **capture packet** real-time + đọc output
- [ ] `nmap` **scan port** + fingerprint dịch vụ
- [ ] `iperf3` đo **bandwidth thực** giữa 2 máy
- [ ] Biết khi nào dùng tool nào cho 1 case debug

---

## Tình huống — Bạn là người mới nhận on-call

Bạn làm devops on-call. 2 giờ sáng có alert: *"API latency p99 = 5s"*. Bạn mở terminal, ngơ:

- Dùng tool nào trước?
- Layer nào fail (network? app? DB)?
- Có phải DNS chậm không? TCP retransmit? Server load?

Senior chỉ:
- *"`ping` thử latency Internet."*
- *"`traceroute` xem đi đâu chậm."*
- *"`ss -tan | grep ESTAB | wc -l` xem connection active."*
- *"`tcpdump` capture vài giây trên port 443."*
- *"`htop` xem CPU/RAM."*

Bạn ngơ:
- Mỗi tool **dùng để làm gì**?
- Tại sao 5 tool khác nhau cho 1 vấn đề?
- Học theo thứ tự nào hợp lý?

→ Bài này dạy bạn **7 tool cốt lõi** + **5 case debug** + **cheat sheet đầy đủ**.

---

## 1️⃣ `ping` — test reachability + latency

**`ping`** gửi **ICMP echo request**, nhận **ICMP echo reply**. Test:
- ✅ Host có reachable không (L3)
- ✅ Latency (RTT)
- ✅ Packet loss

```bash
$ ping -c 4 google.com
PING google.com (142.250.190.46): 56 data bytes
64 bytes from 142.250.190.46: icmp_seq=0 ttl=117 time=23.456 ms
64 bytes from 142.250.190.46: icmp_seq=1 ttl=117 time=24.321 ms
64 bytes from 142.250.190.46: icmp_seq=2 ttl=117 time=22.987 ms
64 bytes from 142.250.190.46: icmp_seq=3 ttl=117 time=25.123 ms

--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss
round-trip min/avg/max/stddev = 22.987/23.972/25.123/0.834 ms
```

### Đọc output

Output `ping` có 4 thông tin chính cần hiểu — đặc biệt `RTT` (round-trip time) và `packet loss`. Nắm được sẽ chẩn đoán nhanh network: latency cao là chậm, loss cao là kém ổn định:

| Field | Ý nghĩa |
|---|---|
| `time=23.456 ms` | RTT của 1 packet |
| `ttl=117` | TTL còn lại (từ server) → đoán hop count = `64-117` (linux default 64) hoặc `255-117` |
| `0% packet loss` | Connectivity tốt |
| `min/avg/max/stddev` | Statistics |

### Options thường dùng

`ping` không chỉ là "lệnh test mạng" — 6 flag dưới đây mở ra nhiều use case khác (test MTU, flood test, custom interval). Bảng cheat sheet cho daily debugging:

```bash
ping -c 10 host           # Chỉ 10 packet rồi exit
ping -i 0.2 host          # Interval 200ms (root only nếu <0.2)
ping -s 1400 host         # Packet 1400 bytes (test MTU)
ping -W 2 host            # Timeout 2s per packet
ping -f host              # Flood (root only) — load test L3
ping -6 host              # IPv6
```

### ⚠️ `ping` không test app

Đây là nhầm lẫn rất phổ biến — "server `ping` được = app OK". Sai. `ping` chỉ test **Layer 3** (IP reachability), không nói gì về Layer 4 (port mở không) hay Layer 7 (app có chạy không). 2 trường hợp tiêu biểu gây bối rối:

```
ping OK   ≠ HTTP/SSH OK
ping FAIL ≠ Server down  (có thể chỉ ICMP bị firewall block)
```

→ `ping` test **L3 reachability**, **không** test L4 (port) hay L7 (app). Một số firewall block ICMP để giảm DDoS — server vẫn chạy.

---

## 2️⃣ `traceroute` / `tracepath` — đường đi packet

Cho biết packet đi qua **những hop nào** trước khi đến đích.

```bash
$ traceroute google.com
traceroute to google.com (142.250.190.46), 30 hops max
 1  192.168.1.1 (router nhà)            0.5ms
 2  10.0.0.1 (ISP gateway)              5.2ms
 3  113.171.1.1 (ISP backbone HN)       8.1ms
 4  213.248.94.18 (Singapore IX)        45.3ms
 5  74.125.243.6 (Google network)       46.1ms
 6  142.250.190.46 (google.com)         46.5ms
```

→ Mỗi dòng = 1 hop. Latency tăng dần là bình thường (mỗi hop xa hơn).

### Cách hoạt động (cũ — nhưng hay)

`traceroute` gửi UDP với **TTL=1, 2, 3, ...** Router decrement TTL, khi TTL=0 → trả ICMP "Time Exceeded" + IP của router. Kết quả: biết tên/IP từng hop.

### Khi nào hop "* * *"

Khi `traceroute` hiển thị `* * *` ở 1 hop, **không phải lỗi** — chỉ có nghĩa router đó **không trả lời ICMP** (admin disable để giảm DDoS). Skip hop đó và đọc tiếp:

```
 5  * * *
```

→ Router không trả ICMP (firewall block). Không phải lỗi — phổ biến. Skip.

### `mtr` — traceroute + ping liên tục

`mtr` là kết hợp `traceroute` + `ping` chạy liên tục — best tool để debug "đâu là bottleneck" trong đường đi. Chạy 30s đủ để thấy hop nào có packet loss hay latency spike:

```bash
$ mtr google.com
                            Packets       Pings
 Host                       Loss%  Snt   Last   Avg
 1. 192.168.1.1              0.0%   10    0.5    0.6
 2. 10.0.0.1                 0.0%   10    5.2    5.4
 3. 113.171.1.1              0.0%   10    8.1    8.5
 4. 213.248.94.18            10.0%  10   45.3   46.1
 5. 142.250.190.46           0.0%   10   46.5   46.8
```

→ Best tool debug "where latency comes from". Hop 4 mất 10% = bottleneck.

→ Mac/Linux: `brew install mtr` / `apt install mtr`.

### Windows tương đương

```cmd
tracert google.com
pathping google.com         (combine traceroute + ping)
```

---

## 3️⃣ `ss` / `netstat` — socket state local

**`ss`** (Socket Statistics) thay thế **`netstat`** trên Linux modern (nhanh hơn 10x).

```bash
$ ss -tlnp                          # TCP + Listening + Numeric + Process
State  Recv-Q  Send-Q  Local Address:Port  Peer Address:Port  Process
LISTEN 0       128     0.0.0.0:22           0.0.0.0:*           sshd
LISTEN 0       128     127.0.0.1:5432       0.0.0.0:*           postgres
LISTEN 0       128     0.0.0.0:443          0.0.0.0:*           nginx
```

### Flag

| Flag | Ý nghĩa |
|---|---|
| `-t` | TCP |
| `-u` | UDP |
| `-l` | Listening only |
| `-n` | Numeric (không resolve DNS) |
| `-p` | Process (cần sudo) |
| `-a` | All (listening + established) |
| `-4` / `-6` | IPv4 / IPv6 |
| `state <state>` | Filter state (`established`, `time-wait`, ...) |

### Thông dụng

```bash
ss -tlnp                       # Listening TCP ports + process
ss -tan                        # All TCP connections
ss -tan state established      # Chỉ ESTABLISHED
ss -tan state time-wait | wc -l # Count TIME-WAIT (debug high load)
ss -ltn4                       # Listening TCP IPv4 only
ss -tn dst :443                # Connection tới port 443
ss -tn src :80                 # Connection từ port 80
ss -i                          # Internal info (cwnd, rtt) — deep debug
```

### `netstat` cross-platform (Mac, Windows)

```bash
# Mac
netstat -an | grep LISTEN
netstat -anv | grep -i ESTABLISHED

# Windows
netstat -an
netstat -ano | findstr :443       (PID column)
netstat -e -s                      (stats by protocol)
```

### `lsof` — alternative

```bash
lsof -i -P -n                 # All open Internet sockets
lsof -i :443                   # Just port 443
lsof -i TCP:443 -sTCP:LISTEN   # Only listening on 443
```

→ Mac không có `ss`, dùng `lsof` thay.

---

## 4️⃣ `nc` (netcat) — Swiss army knife

**`nc`** (netcat) tạo TCP/UDP connection thủ công.

### Test port mở

```bash
nc -zv host port              # -z = scan, -v = verbose
nc -zv example.com 443         # Connection to example.com (203.0.113.10) port 443 [tcp/https] succeeded!
nc -zv example.com 5432        # Connection refused / timeout

nc -uzv example.com 53          # UDP check
```

### Listen & receive

```bash
# Terminal 1 (server)
nc -l 4242                     # Listen on port 4242

# Terminal 2 (client)
nc <server-ip> 4242            # Connect, chat
# Mỗi dòng gõ → bên kia nhận
```

### Transfer file (siêu nhanh, không SSH)

```bash
# Receiver
nc -l 4242 > received.zip

# Sender
nc receiver-ip 4242 < tobackup.zip
```

→ Lightning fast cho LAN. Không encrypt — chỉ dùng nội bộ.

### Banner grabbing — fingerprint dịch vụ

```bash
echo "" | nc example.com 22
# SSH-2.0-OpenSSH_8.9p1 Ubuntu-3
```

→ Server lộ version SSH → attacker scan vulnerable version. Tốt cho recon (và defense — biết server lộ gì).

### Port scan đơn giản

```bash
nc -zv host 20-25
# port 22 succeeded, 23 failed, ...
```

→ `nmap` mạnh hơn nhiều cho task này.

---

## 5️⃣ `tcpdump` — capture packet real-time

**`tcpdump`** capture mọi packet đi qua interface. Khi `ping`/`telnet`/`curl` không đủ debug, đi sâu hơn.

### Cơ bản

```bash
sudo tcpdump -i any                # All interfaces
sudo tcpdump -i eth0               # Interface cụ thể
sudo tcpdump -i any port 80        # Filter port
sudo tcpdump -i any host google.com  # Filter host
sudo tcpdump -i any port 443 and host 1.2.3.4  # Combine
```

### Đọc output

```
14:32:01.123456 IP 192.168.1.42.54321 > 142.250.190.46.443: Flags [S], seq 1234567, win 65535
14:32:01.148234 IP 142.250.190.46.443 > 192.168.1.42.54321: Flags [S.], seq 9876543, ack 1234568, win 65535
14:32:01.148567 IP 192.168.1.42.54321 > 142.250.190.46.443: Flags [.], ack 9876544, win 65535
```

→ Đọc thấy **3-way handshake** (SYN → SYN-ACK → ACK).

### Flags ý nghĩa

```
[S]   = SYN
[S.]  = SYN-ACK
[.]   = ACK
[P.]  = PSH-ACK (data)
[F.]  = FIN-ACK (close)
[R]   = RST
```

### Save to file (analyze offline với Wireshark)

```bash
sudo tcpdump -i any -w capture.pcap port 443
# Stop Ctrl+C → file capture.pcap
# Mở bằng Wireshark GUI — đẹp + chi tiết hơn nhiều
```

### Print details

```bash
sudo tcpdump -i any -nn -v port 443       # Verbose
sudo tcpdump -i any -X port 80             # Show payload (hex + ASCII)
sudo tcpdump -i any -c 100 port 443        # Stop sau 100 packet
```

### ⚠️ Sensitive data trong tcpdump

HTTPS bị encrypt → tcpdump thấy header TCP/IP nhưng KHÔNG đọc được HTTP content. HTTP cleartext = LỘ HẾT (cookie, password). Cẩn thận khi share capture.

---

## 6️⃣ `nmap` — port scanner + service fingerprint

**`nmap`** scan port + nhận diện dịch vụ + OS guess.

### Basic scan

```bash
nmap host                          # Top 1000 port phổ biến
nmap -p 22 host                    # Chỉ port 22
nmap -p 1-1000 host                # Range
nmap -p- host                      # ALL 65535 port (chậm)
```

### Output

```
$ nmap example.com
Starting Nmap 7.94 ( https://nmap.org )
PORT     STATE    SERVICE
22/tcp   open     ssh
80/tcp   open     http
443/tcp  open     https
3306/tcp filtered mysql       ← firewall drop, không refused
```

| State | Ý nghĩa |
|---|---|
| `open` | Có app listen, nhận connect |
| `closed` | Reachable nhưng không có app (RST) |
| `filtered` | Bị firewall drop (timeout) |
| `unfiltered` | Reachable nhưng không xác định open/closed |

### Service fingerprint

```bash
nmap -sV host                      # Version detection
nmap -A host                        # Aggressive: OS + service + script
nmap -O host                        # OS guess
nmap -sC -sV host                   # Default scripts + version
```

### Scan stealth

```bash
nmap -sS host                       # SYN scan (half-open) — quick
nmap -sU host                       # UDP scan (chậm)
nmap -T0 host                       # Paranoid (slow, avoid IDS)
nmap -T4 host                       # Aggressive (fast)
```

### ⚠️ Sử dụng nmap

→ **Chỉ scan máy bạn sở hữu** hoặc có phép. Scan người khác = illegal nhiều nước.

→ Cloud (AWS) cho phép scan EC2 của bạn không cần thông báo (từ 2023).

---

## 7️⃣ `iperf3` — đo bandwidth thực

**`iperf3`** test bandwidth giữa 2 máy (TCP/UDP).

```bash
# Server
iperf3 -s                          # Listen port 5201

# Client
iperf3 -c <server-ip>              # Test 10s mặc định
iperf3 -c <server-ip> -t 60        # Test 60s
iperf3 -c <server-ip> -u -b 100M   # UDP 100Mbps
iperf3 -c <server-ip> -P 4         # 4 parallel streams
iperf3 -c <server-ip> -R           # Reverse (server gửi)
```

### Output

```
[ID] Interval         Transfer    Bitrate
[5]  0.00-10.00 sec   1.10 GBytes  945 Mbits/sec
```

→ Đo **bandwidth thực** giữa 2 máy. Hữu ích test VPN, fiber, intra-cloud.

→ Khác `speedtest.net` test public Internet, `iperf3` test 2 đầu nội bộ.

---

## 8️⃣ Bonus — Các tool khác hay dùng

| Tool | Mục đích |
|---|---|
| **`curl -v`** | HTTP request + verbose headers |
| **`httpie`** / `xh` | HTTP CLI đẹp |
| **`dig`** | DNS lookup ([bài DNS 03](../../../dns/lessons/01_basic/03_dns-tools.md)) |
| **`openssl s_client`** | TLS connect + cert info |
| **`telnet`** | Test TCP port (legacy nhưng còn dùng) |
| **`ip route`** | Routing table Linux |
| **`arp -a`** | ARP table (MAC ↔ IP) |
| **`ifconfig`** / `ip a` | Interface info |
| **`tshark`** | tcpdump CLI nhưng output Wireshark-style |
| **`Wireshark`** | GUI packet analyzer — bible cho serious debug |

---

## 9️⃣ 5 case debug thực tế

### Case 1 — "Site không vào được"

```bash
1. ping site.com               → fail = DNS hoặc L3
   ↳ dig site.com               (DNS đúng?)
   ↳ ping IP-trực-tiếp           (L3 reach?)
2. nc -zv site.com 443         → port 443 mở?
3. curl -v https://site.com    → HTTP response gì?
```

### Case 2 — "Latency cao đột nhiên"

```bash
1. ping site.com               → RTT trung bình
2. mtr site.com                → hop nào loss/spike
3. ss -tan | grep ESTAB | wc -l → connection pool đầy?
4. tcpdump -i any -nn port 443 → packet retransmit?
```

### Case 3 — "Server crash, port 443 không mở"

```bash
1. systemctl status nginx       → service running?
2. ss -tlnp | grep :443         → đang listen không?
3. tail /var/log/nginx/error.log → log lỗi
4. journalctl -u nginx -n 50    → systemd log
5. ufw status                    → firewall block?
```

### Case 4 — "DNS sai"

```bash
1. dig domain                   → resolver default trả gì?
2. dig @1.1.1.1 domain          → Cloudflare trả gì?
3. dig +trace domain            → root → TLD → auth flow
4. sudo dscacheutil -flushcache  → flush local OS cache
```

### Case 5 — "Network slow giữa 2 VM"

```bash
1. ping vm2-ip                  → RTT
2. iperf3 -c vm2-ip             → bandwidth thực
3. mtr vm2-ip                    → route giữa 2 VM
4. ip route get vm2-ip           → route VM1 đi qua đâu
```

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **`ping` fail → tưởng server down** → ICMP có thể bị firewall block, server vẫn chạy. Thử `telnet host 22` hoặc `curl host`.
2. **`tcpdump` mà filter sai** → `tcpdump port 443` = TCP **hoặc** UDP port 443. Cần `tcp port 443`.
3. **`netstat` slow + deprecated** → Trên Linux đã chậm 10x so `ss`. Dùng `ss` thay.
4. **`nmap` mạnh tay scan production** → DDoS được, hoặc trigger alert. Slow scan + permission.
5. **Quên `sudo`** → `tcpdump`, `nmap -sS`, `ss -p` cần root. Quên = output thiếu / error vague.

---

## 🧠 Tự kiểm tra (Self-check)

1. Test "host A có reachable không" — tool nào? Test "port 5432 mở không" — tool nào khác?
2. Sao `mtr` hữu ích hơn `traceroute`?
3. `ss -tlnp` vs `ss -tan` — khác sao?
4. Khi `tcpdump`, bạn thấy flags `[S]` rồi `[S.]` rồi `[.]` — đang quan sát gì?
5. `nmap -p 443 host` trả `filtered` nghĩa là gì?

<details>
<summary>Gợi ý đáp án</summary>

1. **Reachable (L3)**: `ping host`. **Port mở (L4)**: `nc -zv host port` hoặc `telnet host port` hoặc `nmap -p port host`.

2. `traceroute` chỉ chạy 1 lần — packet loss tạm thời không thấy. `mtr` chạy liên tục — show loss% mỗi hop → bottleneck rõ hơn.

3. `-l` = chỉ listening sockets (server bind đợi connection). `-a` = all (cả listening + ESTABLISHED + TIME-WAIT). Cần xem app listen chưa = `-tlnp`. Xem connection hiện tại = `-tan`.

4. **3-way handshake TCP**: SYN → SYN-ACK → ACK. Đang mở 1 TCP connection mới.

5. **`filtered`**: nmap gửi packet, **không nhận response** trong timeout. Thường do **firewall drop packet** (silent). Khác `closed` (server reply RST) và `open` (server reply SYN-ACK).
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### 1-liner thường dùng

```bash
# Reachability + latency
ping -c 4 host
mtr host

# Port test
nc -zv host port
telnet host port

# Listening ports + process
ss -tlnp                       # Linux
lsof -i -P -n | grep LISTEN    # Mac

# Active connections
ss -tan state established
netstat -an | grep ESTABLISHED

# DNS
dig +short host
dig @1.1.1.1 host

# HTTP
curl -v https://host
curl -I https://host           # HEAD only

# Capture packet
sudo tcpdump -i any -nn port 443 -c 20

# Port scan
nmap -p 22,80,443 host

# Bandwidth test (2 máy)
iperf3 -s                       # server
iperf3 -c server-ip             # client
```

### Layer ↔ Tool

| Bạn debug Layer | Tool |
|---|---|
| L3 (IP) | `ping`, `traceroute`, `mtr`, `ip route` |
| L4 (TCP/UDP) | `nc`, `telnet`, `ss`, `nmap`, `tcpdump` |
| L7 (HTTP) | `curl -v`, `httpie`, Chrome DevTools |
| DNS | `dig`, `nslookup`, `host` |

### Quick decision tree

```
Site không vào được?
├─ ping host           → fail = DNS / L3
│   ├─ dig host         → DNS đúng?
│   └─ ping IP          → L3 reach?
├─ nc -zv host 443     → port mở?
└─ curl -v https://host  → HTTP/TLS issue
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **`ping`** | ICMP echo — test L3 reachability + RTT |
| **`traceroute` / `mtr`** | Trace hop path |
| **`ss` / `netstat`** | Socket statistics |
| **`nc` / netcat** | Read/write TCP/UDP — Swiss army knife |
| **`tcpdump`** | Capture packet real-time |
| **`nmap`** | Port scanner + fingerprint |
| **`iperf3`** | Bandwidth test |
| **`Wireshark`** | GUI packet analyzer (đọc pcap) |
| **PCAP file** | Packet capture file (`.pcap`) |
| **ICMP** | Internet Control Message Protocol — `ping`, error |
| **TTL** | Time To Live — số hop tối đa |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [Ports, Sockets & Firewall — Layer 4 access control](03_ports-sockets-firewall.md)
- ↑ **Về cụm:** [tcp-ip-fundamentals README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [DNS Tools](../../../dns/lessons/01_basic/03_dns-tools.md) — `dig`/`nslookup`/`host`/`whois` cho DNS debug

### 🌐 Tài nguyên tham khảo khác
- 📖 [Wireshark User Guide](https://www.wireshark.org/docs/wsug_html_chunked/)
- 📖 [Julia Evans: Networking zines](https://wizardzines.com/zines/networking/)
- 📖 [Brendan Gregg: Network observability tools](https://www.brendangregg.com/Perf/linux_observability_tools.png) — bản đồ tool kinh điển
- 📖 [tcpdump cheat sheet — Daniel Miessler](https://danielmiessler.com/blog/the-tcpdump-network-tool/)
- 📖 [nmap docs](https://nmap.org/docs.html) — book + tutorial

---

> 🎯 *Cluster TCP/IP fundamentals basic 5/5 đóng. Bạn giờ debug được mọi vấn đề mạng từ L3 → L7. Bài kế tiếp có thể vào `02_intermediate/` (BGP, OSPF, routing nâng cao) hoặc nhảy sang cluster khác (load-balancing, proxy).*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `tcp-ip-fundamentals/` lesson 5/5. Cover: 6 network tools daily debug (ping L3 reachability, traceroute hop visualization, mtr live monitoring, ss/netstat socket inspection, tcpdump packet capture, nmap port scan, dig DNS query) + flowchart decision "tool nào dùng khi nào".
- **v1.1.0 (25/05/2026)** — Bổ sung lead-in trước các bảng/ví dụ ở §1 (ping "Đọc output", "Options", "ping không test app") và §2 (traceroute "Khi nào hop `* * *`", `mtr` intro). Thêm Changelog section.
