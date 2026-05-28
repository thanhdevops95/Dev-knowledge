# Networking Terms Dictionary -- Từ điển Thuật ngữ Mạng

> Networking terminology from English to Vietnamese -- Thuật ngữ mạng từ tiếng Anh sang tiếng Việt

## 📋 Table of Contents -- Mục lục

- [OSI Model](#osi-model) -- Mô hình OSI
- [IP & Addressing](#ip--addressing) -- IP và Địa chỉ
- [Protocols](#protocols) -- Giao thức
- [Network Devices](#network-devices) -- Thiết bị Mạng
- [DNS & Load Balancing](#dns--load-balancing) -- DNS và Cân bằng Tải

## OSI Model -- Mô hình OSI

### OSI (Open Systems Interconnection -- Kết nối Hệ thống Mở)
- **Definition -- Định nghĩa:** A conceptual model describing network communication in 7 layers. -- Mô hình mô tả giao tiếp mạng trong 7 tầng.
- **Layers -- Các tầng:**
  1. Physical -- Vật lý
  2. Data Link -- Liên kết dữ liệu
  3. Network -- Mạng
  4. Transport -- Vận chuyển
  5. Session -- Phiên
  6. Presentation -- Trình bày
  7. Application -- Ứng dụng

### Layer 4 (Transport Layer -- Tầng Vận chuyển)
- **Definition -- Định nghĩa:** Provides end-to-end communication. -- Cung cấp giao tiếp đầu cuối.
- **Protocols -- Giao thức:** TCP, UDP

### Layer 7 (Application Layer -- Tầng Ứng dụng)
- **Definition -- Định nghĩa:** Provides network services to applications. -- Cung cấp dịch vụ mạng cho ứng dụng.
- **Protocols -- Giao thức:** HTTP, HTTPS, FTP, SMTP, DNS

## IP & Addressing -- IP và Địa chỉ

### IP Address -- Địa chỉ IP
- **Definition -- Định nghĩa:** Unique identifier for a device on network. -- Định danh duy nhất cho thiết bị trên mạng.
- **Types -- Loại:** IPv4 (32-bit), IPv6 (128-bit)

### CIDR (Classless Inter-Domain Routing -- Định tuyến Liên miền Không phân lớp)
- **Definition -- Định nghĩa:** Method for IP address allocation. -- Phương pháp phân bổ địa chỉ IP.
- **Example -- Ví dụ:** 192.168.0.0/24

### Subnet -- Mạng con
- **Definition -- Định nghĩa:** Logical subdivision of an IP network. -- Phân chia logic của mạng IP.

### Private IP -- IP Riêng
- **Definition -- Định nghĩa:** IP addresses reserved for internal networks. -- Địa chỉ IP được dành riêng cho mạng nội bộ.
- **Ranges -- Dải:** 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16

### MAC Address -- Địa chỉ MAC
- **Definition -- Định nghĩa:** Unique hardware identifier for network interfaces. -- Định danh phần cứng duy nhất cho giao diện mạng.

## Protocols -- Giao thức

### TCP (Transmission Control Protocol -- Giao thức Điều khiển Truyền)
- **Definition -- Định nghĩa:** Connection-oriented, reliable data delivery. -- Hướng kết nối, truyền dữ liệu tin cậy.

### UDP (User Datagram Protocol -- Giao thức Datagram Người dùng)
- **Definition -- Định nghĩa:** Connectionless, fast transmission. -- Không kết nối, truyền nhanh.

### HTTP/HTTPS -- Giao thức Web
- **Definition -- Định nghĩa:** Protocol for transmitting web pages. -- Giao thức truyền trang web.
- **Ports -- Cổng:** 80 (HTTP), 443 (HTTPS)

### SSH (Secure Shell -- Shell Bảo mật)
- **Definition -- Định nghĩa:** Secure remote access protocol. -- Giao thức truy cập từ xa an toàn.
- **Port -- Cổng:** 22

### DHCP (Dynamic Host Configuration Protocol -- Giao thức Cấu hình Host Động)
- **Definition -- Định nghĩa:** Automatically assigns IP addresses. -- Tự động gán địa chỉ IP.

## Network Devices -- Thiết bị Mạng

### Router -- Bộ Định tuyến
- **Definition -- Định nghĩa:** Forwards packets between networks. -- Chuyển tiếp gói tin giữa các mạng.

### Switch -- Bộ Chuyển mạch
- **Definition -- Định nghĩa:** Connects devices within same network. -- Kết nối thiết bị trong cùng mạng.

### Firewall -- Tường lửa
- **Definition -- Định nghĩa:** Filters network traffic. -- Lọc traffic mạng.

### VPN (Virtual Private Network -- Mạng Riêng Ảo)
- **Definition -- Định nghĩa:** Encrypted tunnel for secure communication. -- Đường hầm mã hóa cho giao tiếp an toàn.

### NAT (Network Address Translation -- Chuyển đổi Địa chỉ Mạng)
- **Definition -- Định nghĩa:** Translates private to public IP. -- Chuyển đổi IP riêng thành IP công cộng.

## DNS & Load Balancing -- DNS và Cân bằng Tải

### DNS (Domain Name System -- Hệ thống Tên miền)
- **Definition -- Định nghĩa:** Translates domain names to IP addresses. -- Chuyển đổi tên miền thành địa chỉ IP.

### DNS Records -- Bản ghi DNS
- A, AAAA, CNAME, MX, TXT, NS

### Load Balancer -- Bộ Cân bằng Tải
- **Definition -- Định nghĩa:** Distributes traffic across servers. -- Phân phối traffic qua nhiều servers.
- **Types -- Loại:** L4 (Network), L7 (Application)

### Health Check -- Kiểm tra Sức khỏe
- **Definition -- Định nghĩa:** Ensures servers are functioning. -- Đảm bảo servers đang hoạt động.

---
