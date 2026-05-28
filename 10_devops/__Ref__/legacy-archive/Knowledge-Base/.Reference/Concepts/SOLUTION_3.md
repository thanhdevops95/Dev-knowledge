# Lời giải - Bài 4: Nhập môn Mạng máy tính

Đây là lời giải cho các câu hỏi và bài tập thực hành trong bài học 04.

---

### Câu 1: Lý thuyết TCP/IP và DNS

**1. Trình bày vai trò của DNS trong một yêu cầu truy cập web, ví dụ `https://google.com`.**

DNS (Domain Name System) đóng vai trò như "danh bạ của Internet". Con người nhớ tên miền (`google.com`) nhưng máy tính cần địa chỉ IP (`172.217.22.14`) để kết nối. Quá trình này diễn ra **trước khi** trình duyệt có thể tải trang web.

Luồng đi của yêu cầu như sau:
1.  **Browser Cache:** Trình duyệt kiểm tra xem nó đã lưu địa chỉ IP của `google.com` trong bộ nhớ đệm từ lần truy cập gần đây chưa. Nếu có, nó dùng ngay địa chỉ IP này.
2.  **OS Cache / `hosts` file:** Nếu trình duyệt không có, nó sẽ hỏi hệ điều hành. Hệ điều hành kiểm tra file `hosts` cục bộ và bộ nhớ đệm của nó.
3.  **DNS Resolver:** Nếu không có trong cache, máy tính sẽ gửi yêu cầu đến một máy chủ DNS được cấu hình sẵn (thường là của nhà cung cấp dịch vụ Internet - ISP). Máy chủ này được gọi là DNS Resolver.
4.  **Recursive Query:** DNS Resolver bắt đầu một cuộc truy vấn đệ quy:
    *   Nó hỏi một trong các **Root DNS Server** ("."). Root Server không biết IP của `google.com`, nhưng nó biết ai quản lý đuôi `.com`, và chỉ Resolver đến **TLD (Top-Level Domain) Server** của `.com`.
    *   Resolver hỏi TLD Server của `.com`. Server này không biết IP của `google.com`, nhưng nó biết máy chủ DNS nào chịu trách nhiệm cho tên miền `google.com`. Nó chỉ Resolver đến **Authoritative Name Server** của Google.
    *   Resolver hỏi Authoritative Name Server của Google. Server này biết chính xác địa chỉ IP nào đang được gán cho `google.com` và trả về kết quả (ví dụ: `172.217.22.14`).
5.  **Hoàn tất:** DNS Resolver nhận được địa chỉ IP, lưu nó vào bộ nhớ đệm của mình để dùng cho các yêu cầu sau, và trả kết quả về cho hệ điều hành/trình duyệt của bạn.

Bây giờ, trình duyệt đã có địa chỉ IP và có thể bắt đầu một kết nối TCP đến `172.217.22.14` trên cổng 443 (HTTPS).

**2. TCP và UDP khác nhau ở điểm nào là cơ bản nhất?**

Sự khác biệt cơ bản nhất là: **TCP (Transmission Control Protocol)** là giao thức **hướng kết nối (connection-oriented)** và **đáng tin cậy (reliable)**, trong khi **UDP (User Datagram Protocol)** là giao thức **không kết nối (connectionless)** và **không đáng tin cậy (unreliable)**.

-   **TCP:**
    -   **Cơ chế:** Trước khi gửi dữ liệu, TCP thiết lập một kết nối ổn định thông qua quy trình "bắt tay ba bước" (three-way handshake). Nó đánh số thứ tự các gói tin, yêu cầu bên nhận phải gửi lại xác nhận (acknowledgement) khi nhận được gói tin, và sẽ gửi lại nếu có gói tin bị mất.
    -   **Đặc điểm:** Đảm bảo dữ liệu đến đúng thứ tự, đầy đủ, và không bị lỗi. Tuy nhiên, nó chậm hơn do các cơ chế xác nhận này.
    -   **Ứng dụng:** Tải file (HTTP/FTP), gửi email (SMTP), giao dịch ngân hàng. Đây là những dịch vụ không thể chấp nhận mất mát dù chỉ một chút dữ liệu.

-   **UDP:**
    -   **Cơ chế:** UDP chỉ đơn giản là gửi các gói tin đi mà không cần thiết lập kết nối trước và không cần biết bên nhận có nhận được hay không. Nó được ví như "gửi và quên" (fire and forget).
    -   **Đặc điểm:** Rất nhanh và có độ trễ thấp vì không có các bước xác nhận phức tạp. Tuy nhiên, gói tin có thể bị mất, đến sai thứ tự, hoặc bị lặp lại.
    -   **Ứng dụng:** Game online, gọi video/audio (VoIP), streaming. Các ứng dụng này ưu tiên tốc độ hơn là sự hoàn hảo. Mất một vài khung hình hay một chút âm thanh không quá nghiêm trọng bằng việc bị giật, lag do phải chờ gói tin gửi lại.

---

### Bài 2: Sử dụng Công cụ Dòng lệnh (Thực hành)

**1. Chạy lệnh `ping 8.8.8.8`**

```bash
$ ping -c 4 8.8.8.8

PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=113 time=44.062 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=113 time=43.947 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=113 time=44.548 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=113 time=47.475 ms

--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 43.947/45.008/47.475/1.442 ms
```
-   **Thông tin nhận được:** Lệnh này cho thấy kết nối mạng từ máy của bạn đến máy chủ DNS của Google (`8.8.8.8`) đang hoạt động tốt.
    -   `0.0% packet loss`: Không có gói tin nào bị mất trên đường đi.
    -   `time=45.008 ms` (trung bình): Độ trễ (latency) của kết nối là khoảng 45 mili giây. Đây là thời gian để một gói tin đi từ máy bạn đến máy chủ và quay trở lại.

**2. Dùng lệnh `nslookup github.com`**

```bash
$ nslookup github.com

Server:		192.168.1.1
Address:	192.168.1.1#53

Non-authoritative answer:
Name:	github.com
Address: 20.205.243.166
```
-   **Thông tin nhận được:** Lệnh này đã hỏi máy chủ DNS `192.168.1.1` (máy chủ DNS cục bộ) và nhận được câu trả lời "không chính thức" (non-authoritative answer) rằng tên miền `github.com` tương ứng với địa chỉ IP là `20.205.243.166`.

**3. Chạy lệnh `curl -I https://www.vietnamnet.vn`**

```bash
$ curl -I https://www.vietnamnet.vn

HTTP/2 301 
server: nginx
date: Sun, 07 Dec 2025 08:11:28 GMT
content-type: text/html
content-length: 162
location: https://vietnamnet.vn/
last-modified: Sunday, 07-Dec-2025 08:11:28 GMT
cache-control: no-store, no-cache
```
-   **Thông tin nhận được:** Có, trong phần header trả về, dòng `server: nginx` cho thấy máy chủ web của Vietnamnet đang sử dụng là **Nginx**. Dòng `HTTP/2 301` cũng cho thấy một sự chuyển hướng (redirect) đang diễn ra.

**4. Chạy lệnh `netstat -anp tcp | grep LISTEN` (trên macOS)**

```bash
$ netstat -anp tcp | grep LISTEN

tcp46      0      0  *.54233                *.*                    LISTEN     
tcp4       0      0  *.8080                 *.*                    LISTEN     
tcp4       0      0  *.59869                *.*                    LISTEN
```
-   **Thông tin nhận được:** Lệnh này liệt kê các cổng TCP đang ở trạng thái `LISTEN` (lắng nghe kết nối) trên máy. Ví dụ `*.8080` có nghĩa là có một dịch vụ nào đó đang lắng nghe kết nối đến trên cổng 8080 từ bất kỳ địa chỉ IP nào. Đây có thể là một server web cho môi trường phát triển đang chạy trên máy.

---

### Câu 3: Firewall và Ports

**Quy tắc Firewall (diễn giải bằng lời) cho Database Server:**

> **Cho phép** các kết nối **đến (inbound)** theo giao thức **TCP** trên **cổng 5432** (cổng mặc định của PostgreSQL) chỉ từ **địa chỉ IP của Application Server**. **Từ chối (Deny)** tất cả các kết nối khác đến cổng này.

Quy tắc này đảm bảo rằng chỉ có máy chủ ứng dụng của chúng ta mới có thể "nói chuyện" với cơ sở dữ liệu, ngăn chặn các truy cập trái phép từ bên ngoài.

---

### Câu 4: Load Balancer (Scale-up vs. Scale-out)

Việc chỉ tăng cấu hình cho một máy chủ duy nhất ("scale-up") không phải lúc nào cũng tốt bằng việc thêm nhiều máy chủ và dùng Load Balancer ("scale-out") vì những lý do sau:

1.  **Tồn tại Điểm lỗi duy nhất (Single Point of Failure):** Dù máy chủ có mạnh đến đâu, nếu nó gặp sự cố (phần cứng, hệ điều hành, mất kết nối mạng), toàn bộ hệ thống sẽ sập.
2.  **Giới hạn vật lý và chi phí:** Có một giới hạn vật lý cho việc bạn có thể thêm bao nhiêu CPU/RAM vào một máy chủ. Vượt qua một ngưỡng nào đó, chi phí để nâng cấp sẽ tăng theo cấp số nhân và không còn hiệu quả.
3.  **Khó khăn trong bảo trì:** Bạn không thể nâng cấp hay sửa chữa máy chủ duy nhất đó mà không gây gián đoạn dịch vụ (downtime).

**Hai lợi ích của việc scale-out (thêm nhiều máy chủ và dùng Load Balancer):**

1.  **Độ tin cậy cao (High Availability):** Load Balancer có thể kiểm tra "sức khỏe" của các máy chủ. Nếu một máy chủ bị lỗi, nó sẽ tự động ngừng gửi traffic đến máy chủ đó và phân phối cho các máy chủ còn lại. Người dùng cuối không hề cảm nhận được sự gián đoạn.
2.  **Khả năng mở rộng linh hoạt (Scalability & Elasticity):** Khi traffic tăng đột biến (ví dụ: đợt khuyến mãi), bạn có thể dễ dàng thêm các máy chủ mới vào "trang trại" (server farm) để xử lý tải. Khi traffic giảm, bạn có thể loại bỏ chúng để tiết kiệm chi phí. Khả năng co giãn này hiệu quả hơn nhiều so với việc mua một máy chủ khổng lồ và để lãng phí tài nguyên trong phần lớn thời gian.