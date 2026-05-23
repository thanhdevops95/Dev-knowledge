# Hướng Dẫn 1: Thực Hành Trực Tiếp Trên Máy Mac (Local Host)

File này hướng dẫn bạn đóng vai trò là Developer phát triển và chạy thử nghiệm hệ thống ngay trên máy cá nhân (Mac) của mình.

## Mục lục
1. [Chuẩn bị môi trường](#1-chuan-bi-moi-truong)
2. [Bước 1: Viết Code (Coding)](#2-buoc-1-viet-code)
3. [Bước 2: Chạy thử dạng tiến trình (Manual Run)](#3-buoc-2-chay-thu-dang-tien-trinh)
4. [Bước 3: Đóng gói Docker (Dockerize)](#4-buoc-3-dong-goi-docker)
5. [Bước 4: Chạy Docker Containers & Network](#5-buoc-4-chay-docker-containers)
6. [Bước 5: Xử lý lưu trữ dữ liệu (Docker Volumes)](#6-buoc-5-xu-ly-luu-tru-du-lieu)

---

## 1. Chuẩn bị môi trường
Đảm bảo máy Mac của bạn đã cài:
- **Python 3**: Kiểm tra `python3 --version`.
- **Go**: Kiểm tra `go version`.
- **Docker Desktop**: Kiểm tra `docker --version`.

---

## 2. Bước 1: Viết Code

Chúng ta sẽ tạo thư mục dự án và code cho 2 service.

### 2.1 Cấu trúc thư mục
Mở Terminal, chạy lệnh sau để tạo thư mục:
```bash
# mkdir: make directory (tạo thư mục)
# -p: parents (tạo cả thư mục cha nếu chưa có)
mkdir -p ~/TwoAppSystem/python-app
mkdir -p ~/TwoAppSystem/go-app
```

### 2.2 App 2: Go Backend (Xử lý & Lưu trữ)
Tạo file `~/TwoAppSystem/go-app/main.go`.
*Mục đích:* App này nghe ở cổng 8080, nhận request đếm số lần ping và lưu vào file để test tính năng Volume của Docker.

```go
// File: go-app/main.go
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"sync"
)

// Data struct để lưu trữ dữ liệu
type Data struct {
	Pings int `json:"pings"`
}

var (
	data      = Data{Pings: 0}
	dataMutex sync.Mutex
	// Đường dẫn file db, nơi dữ liệu được ghi xuống đĩa
	dbPath = "/data/db.json"
)

// Hàm load dữ liệu từ file khi khởi động
func loadData() {
	file, err := ioutil.ReadFile(dbPath)
	if err == nil {
		json.Unmarshal(file, &data)
		fmt.Println("Loaded data from file:", data.Pings)
	} else {
		fmt.Println("No existing data file found, starting fresh.")
	}
}

// Hàm lưu dữ liệu xuống file
func saveData() {
	file, _ := json.MarshalIndent(data, "", " ")
	// 0644 là quyền ghi file permission
	_ = ioutil.WriteFile(dbPath, file, 0644)
	fmt.Println("Saved data to file:", data.Pings)
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	dataMutex.Lock()
	defer dataMutex.Unlock()

	data.Pings++
	saveData() // Ghi ngay xuống đĩa mỗi khi có ping

	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "Pong! Total pings: %d", data.Pings)
}

func statsHandler(w http.ResponseWriter, r *http.Request) {
	dataMutex.Lock()
	defer dataMutex.Unlock()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(data)
}

func main() {
    // Tạo thư mục chứa data nếu chưa có
    os.MkdirAll("/data", 0755) 
    
	loadData()

	http.HandleFunc("/ping", pingHandler)
	http.HandleFunc("/stats", statsHandler)

	fmt.Println("Go App running on port 8080...")
	http.ListenAndServe(":8080", nil)
}
```
**Giải thích code Go:**
- `http.HandleFunc`: Định nghĩa router, khi ai đó gọi vào `/ping` thì chạy hàm `pingHandler`.
- `ioutil.WriteFile`: Ghi file xuống đĩa cứng. Đây là mấu chốt để test Docker Volume sau này.
- `8080`: Cổng mà ứng dụng sẽ mở ra để nghe.

### 2.3 App 1: Python Frontend (Gateway)
Tạo file `~/TwoAppSystem/python-app/app.py`.
*Mục đích:* App này dùng thư viện `Flask` để tạo web server ở cổng 5000. Code sẽ gọi sang Go App.

```python
# File: python-app/app.py
import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Lấy địa chỉ của Go App từ biến môi trường (Environment Variable)
# Nếu không có (chạy local), mặc định là localhost:8080
GO_APP_URL = os.environ.get('GO_APP_URL', 'http://localhost:8080')

@app.route('/')
def home():
    return "Hello! Call /do-ping to ping the backend."

@app.route('/do-ping')
def do_ping():
    try:
        # Gửi request sang Go App
        response = requests.get(f"{GO_APP_URL}/ping")
        return jsonify({
            "message": "Ping successful",
            "backend_response": response.text,
            "backend_url": GO_APP_URL
        })
    except Exception as e:
        return jsonify({"error": str(e), "url": GO_APP_URL}), 500

if __name__ == '__main__':
    # Chạy Flask ở port 5001 binding mọi IP (0.0.0.0)
    # Port 5000 thường bị chiếm bởi AirPlay trên Mac
    app.run(host='0.0.0.0', port=5001)
```
**Giải thích code Python:**
- `os.environ.get`: Giúp code linh hoạt. Khi chạy Docker ta sẽ truyền IP của container Go vào đây.
- `requests.get`: Thực hiện HTTP call giống như người dùng gõ trình duyệt.

---

## 3. Bước 2: Chạy thử dạng tiến trình (Manual Run)

Trước khi đóng gói Docker, ta chạy thử "trần" (bare-metal) để đảm bảo code logic đúng.

**Cửa sổ Terminal 1 (Chạy Go):**
```bash
cd ~/TwoAppSystem/go-app
# Tạo thư mục data giả lập vì code Go yêu cầu /data/db.json
# Vì chạy trên Mac, ta cần quyền sudo để tạo thư mục ở root /data hoặc sửa code.
# Để đơn giản cho bài lab này, ta chỉ cần tạo thư mục local:
mkdir -p /tmp/data 
# Lưu ý: Code Go trên đang trỏ fix cứng vào /data. 
# Bạn có thể sửa code thành "./data" để dễ chạy local, 
# hoặc chạy với sudo để nó ghi vào /data thật của Mac.
# Ở đây ta giả định chạy:
go run main.go
# (Nếu lỗi permission tạo folder /data, hãy sửa code Go thành "./db.json" tạm thời hoặc chạy sudo)
```

**Cửa sổ Terminal 2 (Chạy Python):**
```bash
cd ~/TwoAppSystem/python-app
# Cài thư diện
pip3 install flask requests
# Chạy app
python3 app.py
```

**Kiểm tra kết quả:**
Mở trình duyệt truy cập: `http://localhost:5001/do-ping`.
- Nếu thấy JSON trả về "Ping successful" và "Pong!...", bạn đã thành công phase 1.

### Dừng ứng dụng
Sau khi test xong, hãy nhấn `Ctrl+C` ở cả 2 cửa sổ Terminal để dừng Go và Python, chuẩn bị cho bước đóng gói Docker.

---

## 4. Bước 3: Đóng gói Docker (Dockerize)

Bây giờ ta sẽ viết "bản hướng dẫn" (Dockerfile) để Docker biết cách đóng gói ứng dụng.

### 4.1 Dockerfile cho Go
Tạo `~/TwoAppSystem/go-app/Dockerfile`:
```dockerfile
# Start from a base Golang image (phiên bản alpine cho nhẹ)
FROM golang:1.20-alpine

# Tạo thư mục làm việc bên trong container
WORKDIR /app

# Copy các file go mod (nếu có) và code main.go vào container
COPY main.go .

# Build ứng dụng thành file thực thi tên là "backend"
RUN go build -o backend main.go

# Tạo thư mục /data để app ghi file
RUN mkdir /data

# Mở cổng 8080 (chỉ mang tính document)
EXPOSE 8080

# Lệnh chạy khi container start
CMD ["./backend"]
```

### 4.2 Dockerfile cho Python
Tạo `~/TwoAppSystem/python-app/Dockerfile`:
```dockerfile
# Dùng python slim cho nhẹ
FROM python:3.9-slim

WORKDIR /app

# Cài đặt thư viện dependencies ngay
RUN pip install flask requests

# Copy code vào
COPY app.py .

EXPOSE 5001

# Chạy ứng dụng
CMD ["python", "app.py"]
```

### 4.3 Build Images
Tại Terminal, chạy lệnh Build. 
- `-t`: Tag (đặt tên cho image).
- `.`: Build context (thư mục hiện tại).

```bash
# Build Go App
cd ~/TwoAppSystem/go-app
docker build -t my-go-backend:v1 .

# Build Python App
cd ~/TwoAppSystem/python-app
docker build -t my-py-frontend:v1 .
```
**Kết quả:** Chạy `docker images` sẽ thấy 2 image vừa tạo.

---

## 5. Bước 4: Chạy Docker Containers

### 5.1 Tạo Network
Docker container mặc định cô lập. Ta cần 1 mạng chung.
```bash
docker network create my-net
```

### 5.2 Chạy Go Container
```bash
docker run -d \
  --name go-container \
  --network my-net \
  my-go-backend:v1
```
- `-d`: Detached (chạy ngầm).
- `--name`: Đặt tên dễ nhớ là `go-container`. Python app sẽ gọi tên này.
- `--network`: Cắm vào mạng `my-net`.

### 5.3 Chạy Python Container
```bash
docker run -d \
  --name py-container \
  --network my-net \
  -p 5001:5001 \
  -e GO_APP_URL="http://go-container:8080" \
  my-py-frontend:v1
```
- `-p 5001:5001`: Mở cổng 5001 của container ra cổng 5001 của máy Mac (Host).
- `-e ...`: Truyền biến môi trường. Lưu ý URL là `http://go-container:8080`. Docker DNS tự giải phân giải tên `go-container` thành IP nội bộ.

**Kiểm tra:** Truy cập `http://localhost:5001/do-ping`. Web chạy OK là thành công.

---

## 6. Bước 5: Xử lý lưu trữ dữ liệu (Docker Volume)

### Vấn đề
Hiện tại, code Go ghi file vào `/data/db.json` **bên trong** container.
Nếu ta xóa container Go:
```bash
docker rm -f go-container
```
Sau đó chạy lại container mới, số đếm Ping sẽ về 0. Dữ liệu mất!

### Giải pháp: Volume
Ta sẽ "mount" (gắn) một thư mục trên máy Mac vào thư mục `/data` của container.

**Lệnh chạy lại Go với Volume:**
```bash
# Tạo thư mục trên Mac để chứa data (Ví dụ ở Desktop cho dễ thấy)
mkdir -p ~/Desktop/my-docker-data

# Chạy Go container có gắn volume (-v)
docker run -d \
  --name go-container-v2 \
  --network my-net \
  -v ~/Desktop/my-docker-data:/data \
  my-go-backend:v1
```
- `-v ~/Desktop/my-docker-data:/data`: Mọi thứ app ghi vào `/data` trong container sẽ thực chất được ghi vào `~/Desktop/my-docker-data` trên Mac.

**Kiểm thử:**
1. Ping vài lần qua Web Python (lúc này cần chạy lại Python container trỏ vào `go-container-v2` hoặc đổi tên Go container).
2. Kiểm tra `~/Desktop/my-docker-data`, bạn sẽ thấy file `db.json` xuất hiện.
3. `docker rm -f go-container-v2`.
4. Chạy lại container mới (image mới cũng được).
5. Nó sẽ đọc file `db.json` cũ lên. Số đếm ping được bảo toàn!
