# 🛠️ GIAI ĐOẠN 1: CHUẨN BỊ MÔI TRƯỜNG (SETUP)

## 📌 MỤC TIÊU PHẦN NÀY
Trước khi bắt đầu code Giai đoạn 1 (Bare-metal), bạn cần chuẩn bị đầy đủ "đồ nghề". File này hướng dẫn cài đặt các công cụ cốt lõi để chạy ứng dụng trực tiếp trên máy (chưa dùng Docker).

Sau khi làm xong, bạn sẽ có:
✅ Python 3.9+  
✅ Go 1.21+  
✅ Git  
✅ cURL & Postman  
✅ VS Code (IDE)

---

## 1. CÀI ĐẶT PYTHON 3 (BACKEND API GATEWAY)

Python được dùng để viết Flash API Gateway - cổng đón nhận request từ người dùng.

### 🔹 Kiểm tra (nếu đã cài)
Mở Terminal/Command Prompt và gõ:
```bash
python3 --version
# Hoặc
python --version
```
> Yêu cầu: Phiên bản >= 3.9

### 🔹 Cài đặt mới
#### 🪟 Windows
1. Truy cập: [python.org/downloads](https://www.python.org/downloads/)
2. Tải bản mới nhất (VD: 3.11.x).
3. Chạy file cài đặt. **QUAN TRỌNG:** Tích vào ô **"Add Python to PATH"** ở màn hình đầu tiên.
4. Bấm "Install Now".

#### 🍎 macOS
```bash
# Cài qua Homebrew
brew install python
```

#### 🐧 Linux (Ubuntu)
```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

---

## 2. CÀI ĐẶT GO (GOLANG - BACKEND SERVICE)

Go được dùng để xử lý logic chính (Todo CRUD) vì hiệu năng cao.

### 🔹 Kiểm tra
```bash
go version
```
> Yêu cầu: Phiên bản >= 1.21

### 🔹 Cài đặt mới
#### 🪟 Windows
1. Truy cập: [go.dev/dl](https://go.dev/dl/)
2. Tải file `.msi`.
3. Chạy cài đặt (Next > Next > Install).

#### 🍎 macOS
```bash
brew install go
# Setup GOPATH (thêm vào ~/.zshrc)
echo 'export GOPATH=$HOME/go' >> ~/.zshrc
echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.zshrc
source ~/.zshrc
```

#### 🐧 Linux
```bash
# Tải và cài đặt (check link version mới nhất trên go.dev)
wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
# Thêm vào path
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc
```

---

## 3. CÀI ĐẶT CÔNG CỤ QUẢN LÝ SOURCE CODE (GIT)

### 🔹 Kiểm tra
```bash
git --version
```

### 🔹 Cài đặt
- **Windows**: Tải [Git for Windows](https://git-scm.com/download/win).
- **macOS**: `brew install git`
- **Linux**: `sudo apt install git -y`

---

## 4. CÔNG CỤ TEST API (CURL & POSTMAN)

Chúng ta cần công cụ để gửi request (GET, POST) vào server kiểm tra xem nó có hoạt động không.

### 🔹 cURL (Thường có sẵn)
Kiểm tra: `curl --version`. Nếu chưa có (Windows cũ), tải từ [curl.se](https://curl.se/windows/).

### 🔹 Postman (Giao diện trực quan)
1. Truy cập: [postman.com/downloads](https://www.postman.com/downloads/)
2. Tải và cài đặt bản Free.
3. (Tùy chọn) Đăng ký tài khoản để lưu lịch sử.

---

## 5. IDE Code Editor (VS Code)

### 🔹 Cài đặt
Tải tại: [code.visualstudio.com](https://code.visualstudio.com/)

### 🔹 Extensions Khuyên Dùng (Cài đặt trong VS Code)
Bấm `Ctrl+Shift+X` (hoặc icon 4 ô vuông bên trái), tìm và cài:
1. **Python** (Microsoft)
2. **Go** (Go Team at Google)
3. **Thunder Client** (Optional - nếu không muốn dùng Postman riêng)

---

## ✅ CHECKLIST HOÀN THÀNH
Hãy chạy lần lượt các lệnh sau trong Terminal để chắc chắn bạn đã sẵn sàng:

```bash
python --version   # Ra 3.x
pip --version      # Không báo lỗi
go version         # Ra go1.21+
git --version      # Ra git version...
curl --version     # Ra curl...
```

Nếu tất cả đều hiển thị version, bạn đã sẵn sàng sang **Giai đoạn 1**!
