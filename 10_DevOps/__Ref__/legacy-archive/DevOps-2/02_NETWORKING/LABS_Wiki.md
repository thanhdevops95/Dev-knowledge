# Module 02: Networking Labs

---

## 🎯 Mục tiêu

Sau labs này, bạn sẽ:

- Debug network issues như một DevOps thực thụ
- Hiểu traffic đi từ đâu đến đâu
- Config firewall bảo vệ server
- Sử dụng thành thạo các công cụ network

---

## 🔧 Lab 1: Khám phá Network của máy bạn

### 🎬 Bối cảnh

Trước khi debug network của người khác, bạn cần hiểu network của chính máy mình.

### Bước 1: Xem IP addresses

```bash
# Linux/WSL
ip addr

# Hoặc ngắn gọn hơn
ip -4 addr show
```

**Output:**

```
1: lo: <LOOPBACK,UP,LOWER_UP>
    inet 127.0.0.1/8 scope host lo
    
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>
    inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0
```

**Giải thích:**

- `lo` = Loopback interface (localhost)
- `eth0` = Ethernet interface (mạng thật)
- `/24` = Subnet mask (255.255.255.0)
- `brd` = Broadcast address

### Bước 2: Xem routing table

```bash
ip route
```

**Output:**

```
default via 192.168.1.1 dev eth0
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100
```

**Giải thích:**

- `default via 192.168.1.1` = Gateway (router nhà)
- Traffic ra internet đều qua 192.168.1.1

### Bước 3: Xem DNS servers

```bash
cat /etc/resolv.conf
```

**Output:**

```
nameserver 8.8.8.8
nameserver 8.8.4.4
```

Đây là Google DNS servers.

### ✅ Checkpoint Lab 1

- [ ] Biết IP private của máy
- [ ] Biết default gateway
- [ ] Biết DNS server đang dùng

---

## 🔍 Lab 2: Tra cứu DNS

### 🎬 Bối cảnh

Website company không load. Bạn cần kiểm tra DNS có resolve đúng không.

### Bước 1: Tra cứu cơ bản

```bash
# Tra google.com
nslookup google.com
```

**Output:**

```
Server:         8.8.8.8
Address:        8.8.8.8#53

Non-authoritative answer:
Name:   google.com
Address: 142.250.190.14
```

### Bước 2: Dùng dig (chi tiết hơn)

```bash
dig google.com
```

**Output:**

```
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             300     IN      A       142.250.190.14

;; Query time: 15 msec
;; SERVER: 8.8.8.8#53
```

**Giải thích:**

- `IN A` = Internet Address record
- `300` = TTL (seconds to cache)
- `Query time` = Thời gian tra cứu

### Bước 3: Tra các loại records khác

```bash
# MX record (mail servers)
dig google.com MX

# TXT record
dig google.com TXT

# NS record (nameservers)
dig google.com NS

# Tất cả records
dig google.com ANY
```

### Bước 4: Trace DNS resolution

```bash
dig +trace google.com
```

**Output (rút gọn):**

```
.                       518400  IN      NS      a.root-servers.net.
com.                    172800  IN      NS      a.gtld-servers.net.
google.com.             172800  IN      NS      ns1.google.com.
google.com.             300     IN      A       142.250.190.14
```

**Giải thích luồng:**

1. Root servers (`.`)
2. → TLD servers (`com.`)
3. → Google's nameservers
4. → IP cuối cùng

### ✅ Checkpoint Lab 2

- [ ] Dùng được nslookup và dig
- [ ] Hiểu các loại DNS records
- [ ] Biết trace DNS resolution

---

## 🌐 Lab 3: HTTP Requests với curl

### 🎬 Bối cảnh

API trả về lỗi. Bạn cần kiểm tra xem request đang gửi gì và response như thế nào.

### Bước 1: GET request đơn giản

```bash
curl https://httpbin.org/get
```

**Output:**

```json
{
  "args": {}, 
  "headers": {
    "Accept": "*/*",
    "Host": "httpbin.org",
    "User-Agent": "curl/7.68.0"
  }, 
  "origin": "YOUR_PUBLIC_IP",
  "url": "https://httpbin.org/get"
}
```

### Bước 2: Xem response headers

```bash
curl -I https://google.com
```

**Output:**

```
HTTP/2 200 
content-type: text/html; charset=ISO-8859-1
date: Mon, 15 Jan 2024 10:00:00 GMT
expires: -1
cache-control: private, max-age=0
```

### Bước 3: POST request với data

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}' \
  https://httpbin.org/post
```

**Output:**

```json
{
  "data": "{\"name\": \"John\", \"email\": \"john@example.com\"}",
  "headers": {
    "Content-Type": "application/json"
  },
  "json": {
    "email": "john@example.com",
    "name": "John"
  }
}
```

### Bước 4: Debug với verbose mode

```bash
curl -v https://google.com 2>&1 | head -30
```

**Output:**

```
*   Trying 142.250.190.14:443...
* Connected to google.com (142.250.190.14) port 443 (#0)
* TLS handshake...
> GET / HTTP/2
> Host: google.com
> User-Agent: curl/7.68.0
> Accept: */*
>
< HTTP/2 200
< date: Mon, 15 Jan 2024 10:00:00 GMT
< content-type: text/html; charset=ISO-8859-1
```

**Giải thích:**

- `*` = curl info
- `>` = Request gửi đi
- `<` = Response nhận về

### Bước 5: Test các status codes

```bash
# 200 OK
curl -s -o /dev/null -w "%{http_code}" https://httpbin.org/status/200
# Output: 200

# 404 Not Found
curl -s -o /dev/null -w "%{http_code}" https://httpbin.org/status/404
# Output: 404

# 500 Server Error
curl -s -o /dev/null -w "%{http_code}" https://httpbin.org/status/500
# Output: 500
```

### ✅ Checkpoint Lab 3

- [ ] GET request với curl
- [ ] POST request với data
- [ ] Xem headers với -I
- [ ] Debug với -v

---

## 🚪 Lab 4: Kiểm tra Ports

### 🎬 Bối cảnh

App không connect được database. Bạn cần kiểm tra port có mở không.

### Bước 1: Xem ports đang mở trên máy

```bash
ss -tuln
```

**Output:**

```
State  Recv-Q Send-Q Local Address:Port Peer Address:Port
LISTEN 0      128    0.0.0.0:22          0.0.0.0:*
LISTEN 0      511    0.0.0.0:80          0.0.0.0:*
LISTEN 0      511    127.0.0.1:3306      0.0.0.0:*
```

**Giải thích:**

- `0.0.0.0:22` = SSH lắng nghe trên tất cả interfaces
- `127.0.0.1:3306` = MySQL chỉ local

### Bước 2: Xem process nào đang dùng port

```bash
sudo ss -tulnp
```

**Output:**

```
State  Local Address:Port Process
LISTEN 0.0.0.0:22        users:(("sshd",pid=1234,fd=3))
LISTEN 0.0.0.0:80        users:(("nginx",pid=5678,fd=6))
```

### Bước 3: Test connection đến port cụ thể

```bash
# Dùng netcat
nc -zv localhost 22

# Output thành công:
Connection to localhost 22 port [tcp/ssh] succeeded!

# Output thất bại:
nc -zv localhost 3000
nc: connect to localhost port 3000 (tcp) failed: Connection refused
```

### Bước 4: Test remote port

```bash
# Kiểm tra Google HTTP
nc -zv google.com 80
# Connection to google.com 80 port [tcp/http] succeeded!

# Kiểm tra port bị block
nc -zv -w 3 google.com 25
# nc: connect to google.com port 25 (tcp) failed: Connection timed out
```

**`-w 3`** = Timeout sau 3 giây

### ✅ Checkpoint Lab 4

- [ ] Xem ports đang listen với ss
- [ ] Test connection với nc
- [ ] Phân biệt "refused" vs "timeout"

---

## 🛤️ Lab 5: Trace đường đi Packets

### 🎬 Bối cảnh

Kết nối đến server bị chậm. Bạn cần biết đoạn nào gây lag.

### Bước 1: Ping cơ bản

```bash
ping -c 5 google.com
```

**Output:**

```
PING google.com (142.250.190.14) 56(84) bytes of data.
64 bytes from 142.250.190.14: icmp_seq=1 ttl=117 time=10.5 ms
64 bytes from 142.250.190.14: icmp_seq=2 ttl=117 time=11.2 ms
64 bytes from 142.250.190.14: icmp_seq=3 ttl=117 time=10.8 ms
64 bytes from 142.250.190.14: icmp_seq=4 ttl=117 time=15.3 ms
64 bytes from 142.250.190.14: icmp_seq=5 ttl=117 time=10.1 ms

--- google.com ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4006ms
rtt min/avg/max/mdev = 10.1/11.5/15.3/1.9 ms
```

**Phân tích:**

- `0% packet loss` = Network ổn định
- `avg 11.5 ms` = Latency trung bình
- `mdev 1.9 ms` = Độ biến thiên thấp (ổn định)

### Bước 2: Traceroute

```bash
traceroute google.com
```

**Output:**

```
 1  192.168.1.1 (192.168.1.1)  1.234 ms  1.100 ms  1.050 ms
 2  10.0.0.1 (10.0.0.1)  5.678 ms  5.500 ms  5.400 ms
 3  * * *
 4  103.15.200.1 (103.15.200.1)  8.123 ms  8.000 ms  7.900 ms
...
14 142.250.190.14 (142.250.190.14) 12.345 ms  12.200 ms  12.100 ms
```

**Giải thích:**

- Hop 1: Router nhà (fast)
- Hop 2: ISP gateway
- Hop 3: `* * *` = Router không respond (bình thường)
- Hop 14: Destination

### Bước 3: MTR (Better traceroute)

```bash
# Cài đặt nếu chưa có
sudo apt install mtr -y

# Chạy
mtr google.com
```

**MTR là combination của ping + traceroute, chạy liên tục.**

### ✅ Checkpoint Lab 5

- [ ] Phân tích ping output
- [ ] Đọc traceroute output
- [ ] Hiểu `* * *` là gì

---

## 🔥 Lab 6: Firewall với UFW

### 🎬 Bối cảnh

Server mới cài, cần bảo vệ bằng firewall.

### Bước 1: Xem status hiện tại

```bash
sudo ufw status
```

**Output:**

```
Status: inactive
```

### Bước 2: Cấu hình rules TRƯỚC KHI bật

⚠️ **QUAN TRỌNG:** Luôn allow SSH trước khi enable firewall!

```bash
# Cho phép SSH (port 22)
sudo ufw allow 22

# Hoặc
sudo ufw allow ssh
```

### Bước 3: Thêm các rules khác

```bash
# HTTP
sudo ufw allow 80

# HTTPS
sudo ufw allow 443

# Port custom (ví dụ app chạy 3000)
sudo ufw allow 3000

# Từ chối một IP cụ thể
sudo ufw deny from 192.168.1.50
```

### Bước 4: Bật firewall

```bash
sudo ufw enable
```

**Warning:**

```
Command may disrupt existing ssh connections. Proceed with operation (y|n)?
```

Nhấn `y` (vì bạn đã allow SSH ở bước 2)

### Bước 5: Kiểm tra rules

```bash
sudo ufw status verbose
```

**Output:**

```
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22                         ALLOW       Anywhere
80                         ALLOW       Anywhere
443                        ALLOW       Anywhere
```

### Bước 6: Xóa rule

```bash
# Xem rules với số thứ tự
sudo ufw status numbered

# Xóa rule số 3
sudo ufw delete 3
```

### ✅ Checkpoint Lab 6

- [ ] Allow SSH TRƯỚC KHI enable
- [ ] Cấu hình các rules cơ bản
- [ ] Xem và xóa rules

---

## 📝 Lab 7: Edit /etc/hosts

### 🎬 Bối cảnh

Bạn muốn test website với domain trước khi đổi DNS public.

### Bước 1: Xem nội dung hiện tại

```bash
cat /etc/hosts
```

**Output:**

```
127.0.0.1       localhost
127.0.1.1       your-hostname
```

### Bước 2: Thêm custom entry

```bash
sudo nano /etc/hosts
```

Thêm dòng:

```
192.168.1.100   myserver.local
192.168.1.100   api.myserver.local
```

Save và thoát.

### Bước 3: Test

```bash
ping myserver.local
```

**Output:**

```
PING myserver.local (192.168.1.100) 56(84) bytes of data.
64 bytes from 192.168.1.100: icmp_seq=1 ttl=64 time=0.5 ms
```

### Bước 4: Test với curl

```bash
# Nếu có web server chạy ở 192.168.1.100
curl http://myserver.local
```

### ✅ Checkpoint Lab 7

- [ ] Edit /etc/hosts
- [ ] Test custom domain
- [ ] Hiểu use case của /etc/hosts

---

## 🎓 Tổng kết Labs

| Lab | Kỹ năng | Commands |
|-----|---------|----------|
| 1 | Xem network config | `ip addr`, `ip route` |
| 2 | DNS tra cứu | `nslookup`, `dig` |
| 3 | HTTP requests | `curl` |
| 4 | Port checking | `ss`, `nc` |
| 5 | Path tracing | `ping`, `traceroute`, `mtr` |
| 6 | Firewall | `ufw` |
| 7 | Local DNS | `/etc/hosts` |

---

## ⏭️ Tiếp theo

👉 **[SCENARIOS.md - Tình huống thực chiến](SCENARIOS.md)**
