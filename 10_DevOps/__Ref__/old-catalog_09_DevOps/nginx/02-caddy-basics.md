# 🔥 Caddy Server Basics — Máy Chủ Web Tự Động SSL

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Một sự lựa chọn thay thế cực kỳ hiện đại cho Nginx với tiêu chí tự động cấp phát bảo mật chứng chỉ.
> **Prerequisite:** `09-DevOps/nginx/01-nginx-basics.md`

---

## Tại sao chọn Caddy thay cho Nginx?

Để sử dụng chứng chỉ mã hóa dữ liệu (HTTPS/SSL) trên Nginx, bạn phải tự tải công cụ Let's Encrypt, tự viết câu lệnh mã tạo bảo mật, chỉnh sửa file `nginx.conf`, và tạo mã đếm ngày gia hạn (Cronjob) mỗi 90 ngày. Việc này tốn rất nhiều thời gian và gây lỗi gián đoạn nếu chứng chỉ hết hạn mà bạn quên gia hạn.

**Caddy Server** là công cụ thế hệ mới được viết bằng ngôn ngữ Golang. Triết lý của nó là "Mặc định sử dụng HTTPS". Nó sẽ tự động liên hệ với cơ quan cấp chứng chỉ (Let's Encrypt), tự tải khóa SSL, tự động cài đặt vào cấu hình, tự động chạy chuyển hướng cổng HTTP sang HTTPS và tự gia hạn chứng chỉ 100% trong chế độ ngầm định.

---

## 1. Cấu Trúc Tập Tin Cấu Hình Siêu Cấp Ngắn (Caddyfile)

Tập tin thiết lập của Caddy có tên mặc định là `Caddyfile`. Cú pháp thiết lập rút ngắn có thể chỉ bằng một phần mười so với tập tin cấu hình của Nginx.

```caddyfile
# Ví dụ 1: Phục vụ File Tĩnh HTML
congty.com {
    # Tự động HTTPS cho tên miền trên
    root * /var/www/ungdung
    file_server # Bật tính năng trả file vật lí tĩnh
}

# Ví dụ 2: Dùng làm Reverse Proxy Đẩy cổng qua ứng dụng Node.js
api.congty.com {
    reverse_proxy 127.0.0.1:3000
}

# Ví dụ 3: Cân Bằng Tải hai Hệ Thống Máy Chủ
app.congty.com {
    reverse_proxy 10.0.0.1:8080 10.0.0.2:8080 {
        # Cấu hình gỡ máy chủ lỗi tự động
        health_uri /ping
    }
}
```

Với cùng mục đích trên, Nginx cần tầm 40 dòng lệnh. Caddy chỉ thực thi cấu hình trong 10 khối ký tự.

---

## 2. Các Lệnh Điều Khiển Trong Thiết Bị Linux (Terminal CLI)

Ngoài việc cấu hình bằng tập tin, điểm mạnh của ứng dụng phát triển bằng Golang là bạn có thể gọi thẳng câu lệnh từ thiết bị cuối (Terminal) mà không cần cấu hình bằng tệp.

```bash
# Khởi chạy một trang web bảo mật chia sẻ thư mục làm việc hiện tại nhanh chóng.
# Tự thiết lập HTTPS và phát lên mạng ngay tức thì. Chỉ nên dùng khi Test.
caddy file-server --domain trangtest.com

# Trực tiếp mở cổng Reverse Proxy qua câu lệnh không cần file.
# Chỉ nên phục vụ cho môi trường thiết lập máy trạm thử nghiệm nội bộ.
caddy reverse-proxy --from apitest.com --to 127.0.0.1:5000

# Áp dụng thay đổi từ Caddyfile mà không làm đứt kết nối mạng cũ (Zero-downtime)
caddy reload --config /etc/caddy/Caddyfile
```

---

## Gotchas — Những lỗi thiết quản mạng thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cố tình thiết lập chạy Caddy để xin cấp quyền chứng chỉ SSL với tên miền (Domain) là địa chỉ IP tĩnh như `192.168.1.1` hoặc gõ `localhost`. | Cung cấp tên miền đầy đủ đã được gắn với máy chủ IP thực tế, ví dụ `tencongty.com`. | Let's Encrypt và các cơ quan cấp ủy quyền SSL không bao giờ cấp chứng chỉ cho bộ số IP công cộng hoặc máy trạm cục bộ. Chứng chỉ mã hóa chỉ đi kèm với Domain Name. |
| 2 | Chạy công cụ thử nghiệm máy trạm Caddy bằng quyền tài khoản người dùng bình thường ở Linux rồi báo lỗi không truy cập được cổng mạng. | Phải sử dụng quyền quản trị ưu tiên Root bằng thao tác lệnh cấp `sudo` khi chạy ứng dụng máy phát Web. | Tiêu chuẩn hệ điều hành Linux bảo mật, mọi ứng dụng máy nào muốn sử dụng thiết bị đón lõng luồng mạng ở cổng giao thức có số mốc dưới 1024 (Ví dụ cổng HTTP 80 và HTTPS 443) bắt buộc phải có giấy phép hệ điều hành ở quyền cao nhất. |

---

## Bài tập thực hành

- [ ] **Bài 1:** Cài đặt ứng dụng nền tảng Caddy. Tạo tập tệp `Caddyfile` ở mạng máy cục bộ Localhost và viết 2 dòng lệnh mở chức năng chia sẻ nội dung văn bản thư mục hiện tại phân định cổng dịch vụ `8080`.
- [ ] **Bài 2:** Thiết lập kỹ năng làm cổng chuyển chuyển tiếp (Reverse Proxy) thay thế cho công cụ Nginx. Mở ứng dụng Python hoặc Express.js đang sử dụng cổng 3000. Dùng tệp `Caddyfile` điều hướng mạng 80 vào mạng nội tại 3000 và test lại tải trọng mạng.

---

## Tài nguyên thêm
- [Caddy The Docs Official Caddyfile Tutorial](https://caddyserver.com/docs/caddyfile/tutorial) — Tệp sách cấu hình giải nghĩa tài liệu cú pháp gõ rút ngắn mạng dành riêng bộ tạo Caddyfile.
- [Automatic HTTPS Documentation Caddy](https://caddyserver.com/docs/automatic-https) — Định tuyến giải thích tài liệu cốt lõi nguyên lý cấp máy trạm SSL tự kích hoạt của nhà máy.
