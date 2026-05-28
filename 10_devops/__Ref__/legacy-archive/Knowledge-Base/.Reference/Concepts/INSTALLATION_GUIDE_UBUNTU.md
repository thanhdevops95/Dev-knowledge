# Hướng Dẫn Cài Đặt Môi Trường Trên Ubuntu Server (Linux)

Tài liệu này hướng dẫn cài đặt các công cụ cần thiết (Docker, Go, Python) trên máy chủ Ubuntu (hoặc máy ảo OrbStack/WSL running Ubuntu).

---

## 1. Cập nhật hệ thống
Luôn bắt đầu bằng việc cập nhật danh sách gói phần mềm để đảm bảo bạn cài bản mới nhất.

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

---

## 2. Cài đặt Docker (Quan trọng nhất)
Trên môi trường server, Docker là thành phần cốt lõi để chạy ứng dụng đã đóng gói.

### Cách 1: Cài nhanh bằng script (Khuyên dùng cho Lab/Dev)
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Cách 2: Cài thủ công từ Repository
```bash
sudo apt-get install -y docker.io
```

### Cấu hình User (Tránh phải gõ sudo mỗi lần dùng docker)
Sau khi cài xong, thêm user hiện tại vào nhóm docker:
```bash
sudo usermod -aG docker $USER
```
*Lưu ý: Bạn cần thoát SSH và đăng nhập lại (Logout/Login) để thay đổi này có hiệu lực.*

Kiểm tra:
```bash
docker --version
```

---

## 3. Cài đặt Go (Golang)
Nếu bạn muốn build hoặc sửa code Go ngay trên server (thay vì chỉ chạy container), bạn cần cài Go.

Dùng `snap` (có sẵn trên Ubuntu) là cách dễ nhất để có bản Go mới:
```bash
sudo snap install go --classic
```

Kiểm tra:
```bash
go version
```
*Note: Nếu không dùng snap, bạn phải tải file tar.gz về và giải nén thủ công, phức tạp hơn.*

---

## 4. Cài đặt Python 3 & Pip
Ubuntu thường có sẵn Python 3, nhưng thường thiếu `pip` (trình quản lý thư viện) và `venv`.

Kiểm tra python:
```bash
python3 --version
```

Cài đặt pip và các công cụ hỗ trợ:
```bash
sudo apt-get install -y python3-pip python3-venv
```

Kiểm tra:
```bash
pip3 --version
```

---

## 5. Cài đặt các công cụ phụ trợ (Tùy chọn)
Để thuận tiện cho việc debug mạng hoặc tải file:
```bash
sudo apt-get install -y curl wget git net-tools
```
- `net-tools`: Cung cấp lệnh `ifconfig` để xem IP.
- `git`: Để clone code từ GitHub nếu cần.
