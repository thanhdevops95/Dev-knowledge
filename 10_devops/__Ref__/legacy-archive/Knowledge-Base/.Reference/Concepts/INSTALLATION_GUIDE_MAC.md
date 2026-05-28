# Hướng Dẫn Cài Đặt Môi Trường Phát Triển Trên macOS

Nếu máy Mac của bạn chưa có sẵn Python, Go hoặc Docker, hãy làm theo các bước dưới đây để cài đặt. Chúng ta sẽ sử dụng **Homebrew** - trình quản lý gói phổ biến nhất trên macOS để cài đặt mọi thứ dễ dàng.

## 1. Cài đặt Homebrew (Nếu chưa có)
Mở ứng dụng **Terminal**, gõ lệnh sau để kiểm tra xem đã có Homebrew chưa:
```bash
brew --version
```
Nếu máy báo `command not found`, hãy chạy lệnh sau để cài đặt:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Làm theo hướng dẫn trên màn hình (nhập password máy, nhấn Enter). Sau khi cài xong, có thể nó sẽ yêu cầu bạn chạy thêm vài lệnh để thêm `brew` vào PATH (nó sẽ hiện rõ trên màn hình, thường là `echo ... >> /Users/.../.zprofile`).

---

## 2. Cài đặt Python 3

Trên macOS hiện đại, `python3` thường đã có sẵn (cài theo Xcode Command Line Tools).
Kiểm tra:
```bash
python3 --version
```
*Lưu ý: Lệnh là `python3`, không phải `python`. Nếu bạn gõ `python` mà lỗi, hãy thử `python3`.*

Nếu chưa có hoặc muốn cài bản mới nhất qua Homebrew:
```bash
brew install python
```
Sau khi cài, hãy nhớ luôn dùng lệnh `python3` và `pip3` thay vì `python`/`pip`.

---

## 3. Cài đặt Go (Golang)

Kiểm tra:
```bash
go version
```

Nếu chưa có, cài đặt qua Homebrew:
```bash
brew install go
```

---

## 4. Cài đặt Docker

Để chạy container, bạn cần một Docker Runtime. Trên Mac có 2 lựa chọn phổ biến:

### Lựa chọn A: Docker Desktop (Phổ biến, giao diện đẹp)
- Tải về tại: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
- Kéo thả vào Applications như cài app bình thường.
- Mở app Docker lên, đợi icon cá voi trên thanh menu đứng yên là xong.

### Lựa chọn B: OrbStack (Nhẹ hơn, nhanh hơn - Khuyên dùng)
Nếu máy bạn cấu hình yếu hoặc muốn nhanh gọn:
```bash
brew install --cask orbstack
```
- Sau đó mở ứng dụng OrbStack lên để nó setup.
- OrbStack tương thích hoàn toàn với các lệnh `docker`.

### Kiểm tra cuối cùng
Sau khi cài xong, mở lại Terminal và gõ:
```bash
docker --version
```
Nếu thấy hiện version (ví dụ `Docker version 24.0...`) là thành công.
