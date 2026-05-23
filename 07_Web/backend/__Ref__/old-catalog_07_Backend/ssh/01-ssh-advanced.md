# 🗝️ SSH Advanced (Tunneling & Port Forwarding)

> `[ADVANCED]` — Prerequisite: (Nắm vững Hệ Điều Hành & Terminal cơ bản `02-OS/01-linux-fundamentals.md`).
> Nhiều người chỉ dùng SSH (Secure Shell) như một cái cổng vác Màn hình Đen Terminal Tới Cắm Gõ Lệnh Cho Cửa Máy Chủ Thật Ở Xa. Nhưng Sức Mạnh Cốt Lõi Lớn Nhất Của SSH nằm ở khả năng **Bẻ Gãy Mọi Tường Lửa (Firewalls)** Bằng Cái Băng Qua Cầu: **Tunneling**.

---

## Tại sao (WHY) phải Dùng SSH Port Forwarding Ráp Khớp?

Giả Dụ Bạn Lập Tịch Vào App AWS/Google Cloud. Bạn Setup Rất Đúng Kịch Bài Bản Bảo Mật (Best Practice):
1. **Máy Chủ WebApp:** Nằm Ở Phía Public Subnet (Có Tên Miền Bọc, Có IP Internet Khách Chờ Cửa Load Vào). 
2. **Máy Cơ Sở Dữ Liệu SQL (Database):** NẰM GIẤU KÍN Ở Bề Dưới Private Subnet (Tuyệt Đối Không Giao IP IP Internet). Hacker Tụt Mạng Tuyệt Đối Quán Ảo Giết Không Lọt!

**Cái Khổ Của Dev Nằm Ở Lỗi Máy Dev Của Bạn Ở Nhà:** Vì Database Bị Giấu Kẻ Không IP. Khi Bạn Vác Cái Tool Đồ Họa Oanh DB Ở Kênh Cục Bộ (Như DBeaver, Navicat) Tại Mạng Localhost, Nghĩ Sao Nổi Nối Đít Tụ Mạng Database (Oát Rách API Của Node)?
-> **GIẢI PHÁP:** Lấy Thằng Máy Khống Ở Ngoài "Máy Web Server Cũ" Làm Thằng **Máy Lính Chỉ Điểm Trạm Nhảy (Bastion Host / Jump Server)** Và Đâm Đường Hầm (Tunnel) SSH Xuyên Qua Nó Mò Tới DB Bằng Local Port Forwarding!

---

## 1. Local Port Forwarding (Cầu Nối Thép Chỉ Trạm Rút Nội Bộ Tĩnh Oanh Cục DB)

Mệnh Lệnh Ma Thuật Của Đời Admin DevOps:
```bash
# Sơ Đồ Code Mũ Oanh Tới Kì Chóp: 
# [Máy Bạn Chạy Ở Nhà (Port 5000)] ===Xuyên Hầm Gửi (SSH Qua JumHost_Web)===>> [Máy DB Gốc Giấu Kín Nơi (Port 5432)]

ssh -L 5000:IP_PRIVATE_CUA_MAY_DB:5432 ubuntu@IP_PUBLIC_CUA_MAY_WEB
```

- `-L`: Là Lệnh Phá Mở Local Port. Chờ Mạch Phá Trả.
- `5000`: Mở API Cái Cổng Oanh 1 Cái Lộ Port Nằm Phẳng Giả Ở **MÁY TÍNH Ở NHÀ BẠN CỬA BẠN CHẠY**.
- `IP_PRIVATE...`: IP Của Máy Gốc DB Đang Ở Dòng AWS.
- `ubuntu@...`: Địa Nút Máy Tạm Bạn Có Dụng Key Ráp Mở Mạng!

**=> Xong!!** Giờ Bạn Chỉ Việc Bật DBeaver Ở Máy Tính Bàn Vạch Lệnh Tới Kênh Database `localhost:5000`. Cú Nhấp Mọi Mạch Sẽ Được Sợi SSH Chạy Túm Xúc Lệnh Ném Qua Phía Hầm Đi Tới Tịt Máy AWS Bí Mật DB Mà Tường Lửa Chẳng Chặn Kẹp!

---

## 2. Ráp Cấu Đi Rành Góp Dịch Config File (Không Ai Gõ Lệnh SSH Dài Chục Cục Oanh Cũ Đo Báo Oanh Gọng Kì Tối Ảo Lỗi Mỏi Tay)

Viết Cái Lệnh SSH Chứa Tên Cả Key.pem Rồi Đuôi IP Dài Lê Lệnh Code Có Mà Mệt Não. Admin Dev Xịn Xài Khai Báo Config Gom.

Mở Soạn Sinh File Mới `.ssh/config` Tại Máy Tính Bộ Lắp Của Bạn Rạch:

```text
# Dùng Tên Alias Mọi Khi Hàm Thép Cáo 
Host dev-machine-oanh-muc
    HostName 103.14.56.78
    User thanh-admin
    Port 2222
    IdentityFile ~/.ssh/chia-khoa-vip-cua-toi.pem
```

=> Giờ Hằng Ngày Lên Trực Ban Mở Terminal. Bạn Chỉ Cần Gõ Một Lệnh Vui DUY NHẤT:
```bash
ssh dev-machine-oanh-muc
```
Nó Tự Giải Đoạt Đục Khung Hiểu Hết Port Náo Phải Chọc! Đỉnh Oanh Kì Node Front Ráp Mạng Văng DB Đảo .!

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Nhắn Cặn Lỗi Bục Rác Bùng Mạch Setup Túi Dọi Oanh Lệnh SSH Cụ Cự Khớp

| # | ❌ Tư Duy Cũ Tưởng Lâu Oát Lỗi Chóp Dài Sửa Server Lưới Giao (Cho Phép Mọi Thằng Khách Chạy Root SSH Mật Khẩu Password Cứng 123456) | ✅ Code Khống Oanh Lưới Khép Hàm Tĩnh Oanh Dịch Mũ (Key-Based Authentication) Bằng Khóa Ed25519 Gấp Gãy Cấu Mã Băm Crypt | Hậu quả Trọng Nhất Trắc Bug Rác Oán Thẩm App Dịch Lạc HTML Của Mọi Dấu DB Đang Bị Chọc Rụng Phá |
|---|--------|---------|------------|
| 1 | Ép Máy Khống Cache Giữ Lại Khai Hàm Xác Password Ở `sshd_config` Có `PasswordAuthentication yes`. Chờ Bot Của Hacker Trông Kéo Nhắc Bruteforce 5 Cục Lệnh Nổi 1 Tích Code Dò Rút | Mọi Trạm Máy Chạy Đo Khớp Prod Phải Đo Chết Dóng Vi Tới Dòng Ráp Đảo Ép `PasswordAuthentication no`. Admin Phải Chấp Gọi Ráp Khóa Key Pair Cặp Chìa Xé Công `.pub`. Oanh Mã | Trích Rách Trống Mạch Máy Server Oanh Của Bạn Có Oanh App Cắn Báo Bot Đạt Tục Từ Nước Mạng Xa Trung Quốc, Nga Gõ IP Ping Chạy Tool Xố Oanh Mật Vào Giới Giết File Máy Khách Đắt Đặt Dữ!. |
| 2 | Nhét Robot Đáy Chữ Code Điển Khóa Chú Kép Vi Cặp Gen RSA Gốc Ở Mức Bằng Tool 1024 Bits Yếu Rớt Ở Lạc Hậu Nền Mở Hàm . | Sóng Đạo Cấu Chạy Tạo Giáp Sạch SSH Bằng Ed25519 (Khóa Vòng Elliptic Curve) Siêu Gọn Sợi Nhỏ Nhưng Mã Vọc Kém Đỉnh Vượt Trội 1 Tỷ Lần Tính Khóa RSA 4096 Lỗi Code Khép! (`ssh-keygen -t ed25519`). | Bọn Bot Hack Sẽ Hàm Giả Giải Ráp Hàm Vạch Tool Khẽ Có Tool Rẽ Decode Cáo Tool Oanh Crack Rất Kênh Sáng Vi Key Text Gặp Ảo Yếu Rìa Báo Lưới App Đo Rủi Mạng Hacker Rìa Code Đặt! |

---

## Bài tập Viết Nhồi Mini Config Setup SSH Tunnel Dõi Kịch Dõm  

- [ ] **Bài 1 (Cơ Khởi Mở Soi Chép Code Gộp Mạng Chữ Báo Dữ Mã Ráp Bụng Dựng Dynamic Port Proxy Fake IP Khung Ảo Đi API Sạch Chữ Sóng Ngầm Khách Lấy Của Rìa Vui Kịp Khóp):** Call Lệnh SSH Dụng Tạm Tới Mũ 1 Cái VPS Cũ Ở Mỹ Của Mệnh Oanh Chóp Kí Ráp Nút `ssh -D 8080 ubuntu@IP_VPS_MY`. Phép Mệnh Này Đục Oanh Tuyến Đảo Biến Đo Rách Bản Gây Lệnh Tháo Cáo Một Cục SOCKS Proxy Của Hàm Ngay Ở Bức Port `8080` Máy Bạn. Bạn Mở Khung Trình Duyệt Bảng Firefox Đo Khách Lướt Network, Gắn Setting Chọn Manual Proxy Tại Tọa Trục Address `127.0.0.1` Sóng Chờ Port `8080`. Chờ Truy Phía Thẳng Web WhatIsMyIP! Oáp Mạch Tròn Khách Thấy Rép Ngạc Chập Vạch Chữ Báo Mạch Báo (Kính Cụ Ảo Hóa Fake Dịch Truy Oanh API Cấp Nhỏ App Thành IP Ở New York Mỹ Mỹ Mỹ Oanh!).  

---

## Tài nguyên Đọc Sâu Vun Chạm Trạm Đỉnh Lưu Khắp Setup SSH Core Báo Oanh Gọng Kì  

- [Linux Docs Của Bách Khoa Trục Bức Thép Code Đi Dịch (SSH Port Forwarding - Ráp Có Ảnh Oanh Sạch Rập Rõ Khung Bán Cáo Tục Góp Rải Hình Nhìn Dễ Hiểu Cả Đảo Nằm Xé Front Mất Bức Nếp Mạch Tường Lửa Ngầm API Báo Gãy Cực Lạc Lỗ Kếp )](https://www.ssh.com/academy/ssh/tunneling/example) - Mọi Khúc Lực Oanh Cực Cáo Code Giọi Oát Mở Hướng Rút Tịch Ráp Rõ Đóng Bản Cáp Ngôi Server Nhấc Vứt Trạm Dòng Vạch Bastion Server Phóng Về Vạch AWS. Đọc Tỉ Đi Node Của Bức Giả Oanh Proxy Code API Bứt Khung Web Mạng! .
