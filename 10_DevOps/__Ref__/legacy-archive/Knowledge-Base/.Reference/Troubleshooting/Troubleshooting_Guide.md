# 🔧 TROUBLESHOOTING GUIDE - XỬ LÝ LỖI THƯỜNG GẶP

## 📌 MỤC ĐÍCH
File này tổng hợp các lỗi phổ biến nhất khi học DevOps và cách xử lý. Hãy Ctrl+F tìm thông báo lỗi của bạn.

---

## 🐍 PYTHON ERRORS

### ❌ Lỗi 1: `python: command not found`

**Nguyên nhân:** Python chưa được cài hoặc chưa có trong PATH.

**Giải pháp:**

**Windows:**
1. Gỡ và cài lại Python từ python.org
2. **QUAN TRỌNG:** Tích vào ô "Add Python to PATH"
3. Hoặc thêm thủ công:
   - Win + Pause → Advanced system settings
   - Environment Variables → Path → Edit
   - Thêm: `C:\Users\[TênMáy]\AppData\Local\Programs\Python\Python311`

**macOS/Linux:**
```bash
# Thử dùng python3 thay vì python
python3 --version

# Nếu vẫn không có, cài lại
# macOS:
brew install python

# Linux:
sudo apt install python3 python3-pip
```

---

### ❌ Lỗi 2: `ModuleNotFoundError: No module named 'flask'`

**Nguyên nhân:** Chưa cài thư viện Flask.

**Giải pháp:**
```bash
# Đảm bảo đang ở thư mục python-service/
pip install -r requirements.txt

# Hoặc cài riêng
pip install Flask flask-cors requests
```

**Nếu vẫn lỗi (dùng nhiều Python version):**
```bash
# Dùng pip3 thay vì pip
pip3 install -r requirements.txt

# Hoặc chỉ định rõ Python version
python3 -m pip install -r requirements.txt
```

---

## 🔷 GO ERRORS

### ❌ Lỗi 3: `go: command not found`

**Nguyên nhân:** Go chưa cài hoặc chưa có trong PATH.

**Giải pháp:**

**Kiểm tra Go đã cài chưa:**
```bash
# Windows
where go

# macOS/Linux
which go
```

**Nếu chưa có, cài lại theo Stage01_Setup.md**

**Nếu đã cài nhưng vẫn lỗi (PATH issue):**
```bash
# macOS/Linux - Thêm vào ~/.zshrc hoặc ~/.bashrc
export PATH=$PATH:/usr/local/go/bin
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

# Reload
source ~/.zshrc
```

---

### ❌ Lỗi 4: `cannot find package "github.com/gin-gonic/gin"`

**Nguyên nhân:** Chưa tải thư viện.

**Giải pháp:**
```bash
cd go-service

# Tải tất cả dependencies
go mod tidy

# Hoặc tải riêng
go get github.com/gin-gonic/gin
go get github.com/google/uuid
```

---

## 🐳 DOCKER ERRORS

### ❌ Lỗi 5: `Cannot connect to the Docker daemon`

**Nguyên nhân:** Docker Desktop chưa chạy.

**Giải pháp:**
1. Mở Docker Desktop
2. Đợi icon cá voi trên thanh menu/taskbar đứng yên (không còn animation)
3. Chạy lại lệnh

**Nếu vẫn lỗi (Linux):**
```bash
# Khởi động Docker service
sudo systemctl start docker

# Cho phép user hiện tại dùng Docker không cần sudo
sudo usermod -aG docker $USER

# Log out và log in lại để áp dụng
```

---

### ❌ Lỗi 6: `port is already allocated` hoặc `address already in use`

**Nguyên nhân:** Port đã bị process khác chiếm.

**Giải pháp:**

**Windows:**
```bash
# Tìm process đang dùng port 8080
netstat -ano | findstr :8080

# Kill process (PID là số ở cột cuối)
taskkill /PID [số_PID] /F
```

**macOS/Linux:**
```bash
# Tìm process
lsof -i :8080

# Kill process
kill -9 [PID]

# Hoặc dùng Docker
docker ps  # Xem container nào đang chạy
docker rm -f [container_name]  # Xóa container đó
```

**Hoặc đổi port trong code/docker-compose:**
```yaml
ports:
  - "5001:8080"  # Đổi 5000 thành 5001
```

---

### ❌ Lỗi 7: `no such file or directory` khi build Docker

**Nguyên nhân:** Dockerfile đang ở sai thư mục hoặc đường dẫn sai.

**Giải pháp:**
```bash
# Đảm bảo bạn đang ở đúng thư mục
pwd  # Kiểm tra thư mục hiện tại

# Build từ thư mục gốc
cd Todo-App-DevOps
docker build -t todo-go:v1 ./go-service

# Kiểm tra Dockerfile có tồn tại không
ls go-service/Dockerfile
```

---

### ❌ Lỗi 8: Container chạy nhưng không truy cập được

**Nguyên nhân:** Chưa map port hoặc sai network.

**Giải pháp:**

**Kiểm tra container có chạy không:**
```bash
docker ps
# Nếu không thấy, xem log
docker logs [container_name]
```

**Kiểm tra port mapping:**
```bash
docker ps
# Cột PORTS phải có: 0.0.0.0:5000->8080/tcp
```

**Nếu thiếu port mapping, chạy lại với -p:**
```bash
docker run -d -p 5000:8080 --name python-app todo-python:v1
```

---

## 🕸️ NETWORK ERRORS

### ❌ Lỗi 9: `Connection refused` giữa các container

**Nguyên nhân:** 
1. Containers không cùng network
2. Gọi sai hostname

**Giải pháp:**

**Kiểm tra network:**
```bash
# Xem container nào trong network nào
docker network inspect todo-net

# Nếu thiếu, thêm container vào network
docker network connect todo-net [container_name]
```

**Kiểm tra hostname:**
```python
# SAI: Trong container Python gọi
GO_SERVICE_URL = "http://localhost:8081"  # localhost là chính nó!

# ĐÚNG: Gọi bằng tên container
GO_SERVICE_URL = "http://go-app:8081"  # go-app là tên container Go
```

---

### ❌ Lỗi 10: `CORS policy` error trên browser

**Nguyên nhân:** Backend chưa cho phép frontend gọi API (khác domain/port).

**Giải pháp:**

**Python (Flask):**
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Cho phép tất cả origins (dev mode)
```

**Go (Gin):**
```go
import "github.com/gin-contrib/cors"

router.Use(cors.Default())  // Cho phép tất cả
```

---

## 🗄️ DATABASE ERRORS

### ❌ Lỗi 11: `Can't connect to MySQL server`

**Nguyên nhân:**
1. MySQL container chưa chạy
2. Sai host/port
3. MySQL chưa sẵn sàng (đang khởi động)

**Giải pháp:**

**Kiểm tra MySQL container:**
```bash
docker ps | grep mysql
# Nếu không thấy, chạy lại docker-compose up
```

**Kiểm tra connection string:**
```go
// SAI (nếu chạy trong Docker)
dsn := "root:secret@tcp(localhost:3306)/todo_db"

// ĐÚNG (gọi bằng tên service)
dsn := "root:secret@tcp(db:3306)/todo_db"
```

**Đợi MySQL sẵn sàng:**
```go
// Thêm retry logic trong code Go
for i := 0; i < 10; i++ {
    db, err = sql.Open("mysql", dsn)
    if err == nil {
        err = db.Ping()
        if err == nil {
            break  // Kết nối thành công
        }
    }
    time.Sleep(2 * time.Second)
}
```

---

## ☸️ KUBERNETES ERRORS

### ❌ Lỗi 12: `ImagePullBackOff`

**Nguyên nhân:** K8s không tải được Docker Image.

**Giải pháp:**

**Kiểm tra tên image:**
```bash
kubectl describe pod [pod_name]
# Xem phần Events để biết lỗi cụ thể
```

**Nếu image là private (Docker Hub):**
```bash
# Tạo secret
kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=YOUR_USERNAME \
  --docker-password=YOUR_PASSWORD

# Thêm vào deployment.yaml
spec:
  imagePullSecrets:
  - name: regcred
```

**Nếu dùng Minikube (local image):**
```bash
# Build image vào Minikube
eval $(minikube docker-env)
docker build -t todo-go:v1 ./go-service

# Trong deployment.yaml, set imagePullPolicy
spec:
  containers:
  - name: backend
    image: todo-go:v1
    imagePullPolicy: Never  # Không pull từ registry
```

---

### ❌ Lỗi 13: `CrashLoopBackOff`

**Nguyên nhân:** Container khởi động rồi chết liên tục.

**Giải pháp:**

**Xem log:**
```bash
kubectl logs [pod_name]
# Nếu pod restart nhiều lần, xem log lần trước
kubectl logs [pod_name] --previous
```

**Nguyên nhân thường gặp:**
1. App lỗi code → Sửa code
2. Thiếu biến môi trường → Thêm vào deployment
3. Không kết nối được DB → Kiểm tra service name

---

## 🔐 PERMISSION ERRORS

### ❌ Lỗi 14: `Permission denied` (Linux/macOS)

**Nguyên nhân:** Không có quyền ghi file/folder.

**Giải pháp:**

**Cho phép ghi vào folder data:**
```bash
chmod 777 data/
```

**Hoặc chạy Docker với user hiện tại:**
```yaml
# docker-compose.yaml
services:
  backend:
    user: "${UID}:${GID}"
```

---

## 🚨 GITLAB CI/CD ERRORS

### ❌ Lỗi 15: `This job is stuck because you don't have any active runners`

**Nguyên nhân:** Không có GitLab Runner.

**Giải pháp:**
- Dùng Shared Runners của GitLab.com (Settings → CI/CD → Runners → Enable shared runners)
- Hoặc cài GitLab Runner riêng (nâng cao)

---

### ❌ Lỗi 16: `docker: command not found` trong CI

**Nguyên nhân:** Job không dùng Docker image hoặc thiếu Docker-in-Docker.

**Giải pháp:**
```yaml
build-job:
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind  # Docker-in-Docker
  script:
    - docker build ...
```

---

## 📞 CÁCH DEBUG HIỆU QUẢ

### 1. Đọc kỹ thông báo lỗi
Thông báo lỗi thường chỉ rõ vấn đề. Đừng bỏ qua!

### 2. Xem log
```bash
# Docker
docker logs [container_name]

# Kubernetes
kubectl logs [pod_name]

# GitLab CI
Vào Pipeline → Click vào job bị lỗi
```

### 3. Kiểm tra từng bước
- Service có chạy không? `docker ps` / `kubectl get pods`
- Port có đúng không?
- Network có thông không? `ping`, `curl`

### 4. Google lỗi
Copy thông báo lỗi chính xác, search Google. Thường có người gặp lỗi tương tự.

### 5. Hỏi cộng đồng
- Stack Overflow
- DevOps Vietnam Facebook Group
- Kubernetes Vietnam

---

## 🎯 CHECKLIST KHI GẶP LỖI

- [ ] Đã đọc kỹ thông báo lỗi?
- [ ] Đã xem log?
- [ ] Đã kiểm tra service/container có chạy không?
- [ ] Đã kiểm tra port mapping?
- [ ] Đã kiểm tra network?
- [ ] Đã Google lỗi?
- [ ] Đã thử restart Docker/Service?
- [ ] Đã đọc lại hướng dẫn?

---

**Nếu vẫn không giải quyết được, hãy tạo issue mới với đầy đủ thông tin:**
1. Hệ điều hành (Windows/macOS/Linux)
2. Giai đoạn đang làm
3. Lệnh đã chạy
4. Thông báo lỗi đầy đủ
5. Log (nếu có)
