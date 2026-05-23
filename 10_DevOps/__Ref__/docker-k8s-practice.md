# 🐳☸️ Chuỗi đề thực hành Docker → Kubernetes (Liên kết xuyên suốt)

> **Nguyên tắc thiết kế:** Tất cả bài tập đều xoay quanh **một ứng dụng Python duy nhất** được tiến hóa dần. Mỗi bài kế thừa kết quả bài trước, giúp người học hiểu sâu và thấy được luồng phát triển thực tế.
>
> **App xuyên suốt:** `myapp` - bắt đầu là script Python in chuỗi, dần phát triển thành web API có database, cache, và cuối cùng deploy lên K8s.

---

## 📋 Mục lục

### Phần A: Docker (Bài 1-24)
- Docker cơ bản: Image, Tag, Inspect (Bài 1-8)
- Container vận hành: Run, Lifecycle, Debug (Bài 9-17)
- Docker nâng cao: Env, Volume, Network, Compose, Registry (Bài 18-24)

### Phần B: Kubernetes (Bài 25-41)
- K8s cơ bản: Pod, Deployment, Service (Bài 25-30)
- K8s nâng cao: Update, Config, Storage, Probes, HPA, Ingress (Bài 31-38)
- K8s production: StatefulSet, Helm, Dự án tổng hợp (Bài 39-41)

### Phần C: Chuyên sâu (Bài 42-50)
- Helm Template chuyên sâu (Bài 42-44)
- ArgoCD - GitOps (Bài 45-47)
- Service Mesh - Istio (Bài 48-50)

---

# 🐳 PHẦN A: DOCKER

## **Bài 01: Pull image đầu tiên**

**Mục tiêu:** Làm quen lệnh pull, hiểu khái niệm image từ registry.

**Yêu cầu:**
1. Pull image `hello-world` từ Docker Hub
2. Pull thêm image `python:3.11-slim` (sẽ dùng cho các bài sau)
3. Pull image `alpine:latest`

**Hướng dẫn:**
```bash
docker pull hello-world
docker pull python:3.11-slim
docker pull alpine:latest
```

**Câu hỏi suy ngẫm:**
- Khi pull, terminal hiển thị nhiều dòng "Pull complete" - đó là gì?
- Tại sao lần pull thứ 2 cùng image lại nhanh hơn?

---

## **Bài 02: Kiểm tra image đã có**

**Mục tiêu:** Liệt kê, lọc, xem thông tin image.

**Yêu cầu:**
1. Liệt kê tất cả image đang có
2. Liệt kê chỉ ID của image
3. Liệt kê cả image trung gian (dangling)
4. Lọc image có tên chứa "python"
5. Xem dung lượng từng image

**Hướng dẫn:**
```bash
docker images
docker images -q
docker images -a
docker images | grep python
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

**Câu hỏi:**
- `IMAGE ID` có ý nghĩa gì? Tại sao 2 image có thể cùng ID?
- Cột `CREATED` là thời gian image được build hay được pull?

---

## **Bài 03: Tạo app Python đầu tiên & Dockerfile cơ bản**

**Mục tiêu:** Viết Dockerfile đầu tiên, build image từ source code.

**Yêu cầu:**

1. Tạo thư mục `myapp/` chứa file `app.py`:
```python
# app.py
print("Hello from MyApp - Version 1.0")
print("Running inside Docker container")
```

2. Tạo `Dockerfile` đơn giản nhất:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

3. Build image với tên `myapp`:
```bash
docker build -t myapp .
```

4. Chạy image để kiểm tra output:
```bash
docker run myapp
```

**Câu hỏi:**
- Mỗi dòng trong Dockerfile có ý nghĩa gì?
- `WORKDIR` khác `cd` thế nào?
- Tại sao không cần install Python trong container?

---

## **Bài 04: Xóa image**

**Mục tiêu:** Quản lý dọn dẹp image không cần thiết.

**Yêu cầu:**
1. Xóa image `hello-world` đã pull ở Bài 01
2. Thử xóa image `python:3.11-slim` - sẽ báo lỗi nếu `myapp` đang dùng làm base. Hiểu lý do
3. Xóa image dangling (image không tag)
4. **KHÔNG xóa** `myapp` và `python:3.11-slim` vì cần cho các bài sau

**Hướng dẫn:**
```bash
docker rmi hello-world
docker rmi <image_id>           # Cách 2: xóa bằng ID
docker image prune              # Xóa dangling
docker images                   # Verify
```

**Câu hỏi:**
- Sự khác nhau giữa `docker rmi` và `docker image prune`?
- Khi nào dùng `-f` (force)?

---

## **Bài 05: Tag và Versioning**

**Mục tiêu:** Hiểu khái niệm tag, quản lý nhiều phiên bản image.

**Yêu cầu:**

1. Sửa `app.py` thành version 1.1:
```python
print("Hello from MyApp - Version 1.1")
print("Added: timestamp feature")
from datetime import datetime
print(f"Current time: {datetime.now()}")
```

2. Build với tag cụ thể:
```bash
docker build -t myapp:1.1 .
```

3. Sửa tiếp app thành version 1.2 (thêm dòng in tên hệ điều hành), build với tag `1.2`

4. Build thêm 1 lần nữa **không có tag** → tự động gắn `latest`

5. Liệt kê và quan sát:
```bash
docker images myapp
```

**Câu hỏi:**
- Có bao nhiêu image `myapp` hiện tại?
- Tag `latest` đang trỏ tới version nào?
- Image ID của các tag khác nhau giống hay khác nhau?

---

## **Bài 06: Đổi tag (Retag)**

**Mục tiêu:** Hiểu tag là "nhãn dán", không phải bản sao image.

**Tình huống:** Phiên bản `1.2` đã ổn định, muốn promote nó thành `latest` chính thức và tạo thêm tag `stable`.

**Yêu cầu:**
1. Tag lại image `myapp:1.2` thành `myapp:stable`
2. Tag lại thành `myapp:production`
3. Liệt kê và quan sát: cùng 1 IMAGE ID nhưng có nhiều tag
4. Xóa tag `myapp:production` (chỉ xóa tag, không xóa image)

**Hướng dẫn:**
```bash
docker tag myapp:1.2 myapp:stable
docker tag myapp:1.2 myapp:production
docker images myapp
docker rmi myapp:production
docker images myapp
```

**Câu hỏi:**
- Tag bản chất là gì? Tốn thêm dung lượng không?
- Khi xóa 1 tag, image có bị xóa không?

---

## **Bài 07: Xem lịch sử image (History)**

**Mục tiêu:** Hiểu cấu trúc layer của image.

**Yêu cầu:**
1. Xem lịch sử các layer của `myapp:1.2`:
```bash
docker history myapp:1.2
```

2. So sánh với image gốc:
```bash
docker history python:3.11-slim
```

3. Xem chi tiết không bị cắt:
```bash
docker history --no-trunc myapp:1.2
```

**Câu hỏi:**
- Mỗi lệnh trong Dockerfile tạo ra 1 layer phải không?
- Layer nào lớn nhất? Tại sao?
- Layer có `<missing>` ID nghĩa là gì?

---

## **Bài 08: Inspect image**

**Mục tiêu:** Đọc metadata chi tiết của image.

**Yêu cầu:**
1. Inspect image `myapp:1.2`:
```bash
docker inspect myapp:1.2
```

2. Lấy ra các thông tin cụ thể bằng format:
```bash
docker inspect --format='{{.Config.Cmd}}' myapp:1.2
docker inspect --format='{{.Config.WorkingDir}}' myapp:1.2
docker inspect --format='{{.Architecture}}' myapp:1.2
docker inspect --format='{{.Size}}' myapp:1.2
```

3. Lưu output ra file JSON:
```bash
docker inspect myapp:1.2 > myapp-info.json
```

**Câu hỏi:**
- Tìm trong output các trường: `Cmd`, `Env`, `Layers`, `RootFS`
- Có thể biết image build từ Dockerfile như thế nào qua inspect không?

---

## **Bài 09: Run container cơ bản (Foreground)**

**Mục tiêu:** Chạy container, hiểu vòng đời.

**Yêu cầu:**
1. Chạy `myapp:1.2` ở chế độ foreground:
```bash
docker run myapp:1.2
```

2. Chạy và đặt tên container:
```bash
docker run --name myapp-test myapp:1.2
```

3. Chạy lại với cùng tên → sẽ báo lỗi. Tại sao?

4. Xem container đã dừng:
```bash
docker ps -a
```

5. Chạy với `--rm` để tự xóa khi xong:
```bash
docker run --rm myapp:1.2
```

**Câu hỏi:**
- Tại sao container dừng ngay sau khi chạy?
- Sự khác nhau giữa `docker run` và `docker start`?

---

## **Bài 10: Nâng cấp app thành Web Server, Run background với Port Mapping**

**Mục tiêu:** Hiểu daemon mode, port mapping, network giữa host và container.

**Yêu cầu:**

1. Nâng cấp `app.py` thành web server đơn giản (dùng Flask):
```python
# app.py
from flask import Flask
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def home():
    return f"Hello from MyApp v2.0 - {datetime.now()}"

@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

2. Tạo `requirements.txt`:
```
flask==3.0.0
```

3. Cập nhật `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

4. Build version mới:
```bash
docker build -t myapp:2.0 .
```

5. Chạy ở background với port mapping:
```bash
docker run -d -p 8080:5000 --name myapp-web myapp:2.0
```

6. Test:
```bash
curl http://localhost:8080
curl http://localhost:8080/health
```

**Câu hỏi:**
- `-d` làm gì? Khác `--rm` thế nào?
- Cú pháp `-p 8080:5000` nghĩa là gì? (host:container)
- `EXPOSE` trong Dockerfile có tác dụng gì? Có bắt buộc không?

---

## **Bài 11: Quản lý vòng đời container (start/stop/restart/pause/kill)**

**Mục tiêu:** Thành thạo các lệnh điều khiển container.

**Yêu cầu (làm tuần tự với container `myapp-web` từ Bài 10):**

1. **Stop** container:
```bash
docker stop myapp-web
docker ps              # không thấy
docker ps -a           # thấy với status Exited
```

2. **Start** lại:
```bash
docker start myapp-web
curl http://localhost:8080   # vẫn hoạt động
```

3. **Restart**:
```bash
docker restart myapp-web
```

4. **Pause** (tạm dừng process trong container):
```bash
docker pause myapp-web
curl http://localhost:8080   # treo - không phản hồi
```

5. **Unpause**:
```bash
docker unpause myapp-web
curl http://localhost:8080   # hoạt động lại
```

6. **Kill** (cưỡng chế dừng):
```bash
docker kill myapp-web
```

**Câu hỏi:**
- `stop` vs `kill` khác nhau ra sao? (SIGTERM vs SIGKILL)
- `pause` khác `stop` thế nào? Container ở trạng thái nào khi pause?
- Sau `stop` rồi `start`, dữ liệu trong container có còn không?

---

## **Bài 12: Exec vào container - Khám phá bên trong**

**Mục tiêu:** Vào container đang chạy để debug, quan sát filesystem.

**Yêu cầu:**

1. Khởi động lại container:
```bash
docker start myapp-web
```

2. Exec vào container với shell tương tác:
```bash
docker exec -it myapp-web /bin/bash
```

3. **Bên trong container, kiểm tra:**
```bash
pwd                    # Đang ở đâu?
ls -la                 # Có file gì?
cat app.py             # Xem code
ps aux                 # Process gì đang chạy?
env                    # Biến môi trường
whoami                 # User nào?
cat /etc/os-release    # OS gì?
which python           # Python ở đâu?
exit                   # Thoát
```

4. Chạy 1 lệnh nhanh không cần vào shell:
```bash
docker exec myapp-web ls /app
docker exec myapp-web python --version
```

**Câu hỏi:**
- Filesystem trong container khác máy host thế nào?
- Tại sao 1 số image không có `bash` mà chỉ có `sh`? (thử với alpine)
- Khi exit, container có dừng không?

---

## **Bài 13: Logs - Quan sát hoạt động**

**Mục tiêu:** Đọc log container để debug.

**Yêu cầu:**

1. Truy cập web app vài lần để tạo log:
```bash
curl http://localhost:8080
curl http://localhost:8080/health
curl http://localhost:8080/notexist
```

2. Xem toàn bộ log:
```bash
docker logs myapp-web
```

3. Theo dõi log realtime (mở terminal khác, gọi curl, xem log update):
```bash
docker logs -f myapp-web
```

4. Xem 10 dòng cuối:
```bash
docker logs --tail 10 myapp-web
```

5. Xem log kèm timestamp:
```bash
docker logs -t myapp-web
```

6. Xem log trong khoảng thời gian:
```bash
docker logs --since 5m myapp-web
```

**Câu hỏi:**
- Log của container đến từ đâu? (stdout/stderr)
- Nếu app ghi log vào file `/var/log/app.log`, `docker logs` có thấy không?

---

## **Bài 14: Copy file giữa host và container**

**Mục tiêu:** Trao đổi file với container.

**Yêu cầu:**

1. Copy file từ container ra host:
```bash
docker cp myapp-web:/app/app.py ./app-backup.py
ls -la app-backup.py
```

2. Tạo file mới ở host, copy vào container:
```bash
echo "test data" > test.txt
docker cp test.txt myapp-web:/app/test.txt
docker exec myapp-web ls /app
```

3. Copy cả thư mục:
```bash
mkdir static
echo "<h1>Test</h1>" > static/index.html
docker cp static myapp-web:/app/static
docker exec myapp-web ls /app/static
```

**Câu hỏi:**
- Khi container bị xóa, file đã copy vào có còn không?
- Nếu container đang dừng (stopped), có copy được không?

---

## **Bài 15: Commit - Tạo image từ container**

**Mục tiêu:** Lưu lại trạng thái container thành image mới.

**Yêu cầu:**

1. Vào container đang chạy và cài thêm tool:
```bash
docker exec -it myapp-web bash
# Bên trong container:
apt-get update && apt-get install -y curl vim
exit
```

2. Commit container thành image mới:
```bash
docker commit myapp-web myapp:2.0-with-tools
```

3. Kiểm tra image mới:
```bash
docker images myapp
docker run --rm myapp:2.0-with-tools curl --version
```

**Câu hỏi:**
- Commit khác Dockerfile build thế nào?
- Tại sao commit **không** phải cách tốt để tạo image production?

---

## **Bài 16: Diff - Xem thay đổi filesystem**

**Mục tiêu:** Phát hiện thay đổi trong container so với image gốc.

**Yêu cầu:**

1. Xem các thay đổi đã làm trong container `myapp-web`:
```bash
docker diff myapp-web
```

2. Quan sát ý nghĩa các ký hiệu:
   - `A` = Added (thêm mới)
   - `C` = Changed (thay đổi)
   - `D` = Deleted (xóa)

3. Thử tạo, sửa, xóa file rồi diff lại:
```bash
docker exec myapp-web touch /app/newfile.txt
docker exec myapp-web rm /app/test.txt
docker diff myapp-web
```

**Câu hỏi:**
- Tại sao có nhiều file `/var/cache/apt/...` xuất hiện sau khi `apt-get install`?

---

## **Bài 17: Stats, Top, Inspect Container**

**Mục tiêu:** Monitor tài nguyên và process.

**Yêu cầu:**

1. Xem tài nguyên realtime:
```bash
docker stats myapp-web
# Ctrl+C để thoát
```

2. Xem 1 lần không lặp:
```bash
docker stats --no-stream myapp-web
```

3. Xem process bên trong container:
```bash
docker top myapp-web
```

4. Inspect container (khác inspect image):
```bash
docker inspect myapp-web
docker inspect --format='{{.NetworkSettings.IPAddress}}' myapp-web
docker inspect --format='{{.State.Status}}' myapp-web
docker inspect --format='{{.HostConfig.PortBindings}}' myapp-web
```

---

## **Bài 18: Environment Variables**

**Mục tiêu:** Cấu hình app linh hoạt qua biến môi trường.

**Yêu cầu:**

1. Nâng cấp `app.py` để đọc env:
```python
from flask import Flask
import os
from datetime import datetime

app = Flask(__name__)
APP_NAME = os.getenv('APP_NAME', 'MyApp')
APP_ENV = os.getenv('APP_ENV', 'development')
APP_VERSION = os.getenv('APP_VERSION', '3.0')

@app.route('/')
def home():
    return f"Hello from {APP_NAME} [{APP_ENV}] v{APP_VERSION} - {datetime.now()}"

@app.route('/config')
def config():
    return {
        "name": APP_NAME,
        "env": APP_ENV,
        "version": APP_VERSION
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

2. Build version mới:
```bash
docker build -t myapp:3.0 .
```

3. Chạy với env truyền inline:
```bash
docker stop myapp-web && docker rm myapp-web
docker run -d -p 8080:5000 \
  -e APP_NAME="Production App" \
  -e APP_ENV="production" \
  --name myapp-web myapp:3.0

curl http://localhost:8080/config
```

4. Chạy với file `.env`:
```bash
cat > app.env <<EOF
APP_NAME=Staging App
APP_ENV=staging
APP_VERSION=3.0-rc1
EOF

docker stop myapp-web && docker rm myapp-web
docker run -d -p 8080:5000 --env-file app.env --name myapp-web myapp:3.0
curl http://localhost:8080/config
```

5. Set ENV trong Dockerfile (làm thêm bài tập):
```dockerfile
ENV APP_NAME=DefaultApp
ENV APP_ENV=development
```

**Câu hỏi:**
- Thứ tự ưu tiên: ENV trong Dockerfile vs `-e` lúc run?
- Tại sao không nên hardcode password vào Dockerfile mà nên dùng env?

---

## **Bài 19: Volume - Lưu trữ dữ liệu bền vững**

**Mục tiêu:** Hiểu Bind Mount, Named Volume, Anonymous Volume.

**Yêu cầu:**

### Phần A: Bind Mount (mount thư mục host)

1. Nâng cấp app ghi log ra file:
```python
# app.py - thêm
import logging
logging.basicConfig(
    filename='/app/logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

@app.route('/')
def home():
    logging.info(f"Home page accessed")
    return f"Hello from {APP_NAME} ..."
```

2. Build và chạy với bind mount:
```bash
docker build -t myapp:4.0 .
mkdir -p ./logs

docker stop myapp-web && docker rm myapp-web
docker run -d -p 8080:5000 \
  -v $(pwd)/logs:/app/logs \
  --name myapp-web myapp:4.0

curl http://localhost:8080
cat ./logs/app.log    # Log xuất hiện ngay trên host!
```

### Phần B: Named Volume

3. Tạo named volume:
```bash
docker volume create myapp-data
docker volume ls
docker volume inspect myapp-data
```

4. Chạy container dùng named volume:
```bash
docker run -d -p 8081:5000 \
  -v myapp-data:/app/logs \
  --name myapp-web2 myapp:4.0

curl http://localhost:8081
```

5. Test tính bền vững:
```bash
docker rm -f myapp-web2
docker run -d -p 8081:5000 -v myapp-data:/app/logs --name myapp-web2 myapp:4.0
docker exec myapp-web2 cat /app/logs/app.log   # Log cũ vẫn còn!
```

**Câu hỏi:**
- Bind mount vs Named volume: khi nào dùng cái nào?
- Volume có bị xóa khi container bị xóa không?
- Làm sao xóa volume?

---

## **Bài 20: Wait - Chờ container kết thúc**

**Mục tiêu:** Hiểu exit code và đồng bộ hóa.

**Yêu cầu:**

1. Tạo script Python kết thúc với exit code khác nhau:
```python
# exit_test.py
import sys
import time
print("Working...")
time.sleep(5)
print("Done!")
sys.exit(0)  # Đổi thành 1 để test
```

2. Tạo `Dockerfile.exit`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY exit_test.py .
CMD ["python", "exit_test.py"]
```

3. Build và chạy, dùng wait:
```bash
docker build -t exit-test -f Dockerfile.exit .
docker run -d --name waiter exit-test
docker wait waiter
echo "Exit code: $?"
```

**Câu hỏi:**
- Lệnh `wait` block đến khi nào?
- Exit code dùng để làm gì trong CI/CD?

---

## **Bài 21: Network - Giao tiếp giữa các container**

**Mục tiêu:** Cho phép container "nói chuyện" với nhau.

**Yêu cầu:**

### Phần A: Default bridge network

1. Liệt kê network:
```bash
docker network ls
docker network inspect bridge
```

### Phần B: Custom network

2. Tạo network riêng:
```bash
docker network create myapp-net
```

3. Chạy Redis trong network này:
```bash
docker run -d --name redis --network myapp-net redis:alpine
```

4. Nâng cấp app để sử dụng Redis (đếm số lượt truy cập):
```python
# app.py
from flask import Flask
import redis
import os

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/')
def home():
    count = r.incr('visit_count')
    return f"Hello! You are visitor #{count}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

5. Cập nhật `requirements.txt`:
```
flask==3.0.0
redis==5.0.1
```

6. Build và chạy trong cùng network:
```bash
docker build -t myapp:5.0 .
docker run -d -p 8080:5000 --name myapp-web --network myapp-net myapp:5.0

curl http://localhost:8080     # Visitor #1
curl http://localhost:8080     # Visitor #2
```

7. Test DNS giữa container:
```bash
docker exec myapp-web ping -c 2 redis
```

**Câu hỏi:**
- Tại sao trong code dùng `host='redis'` mà không phải IP?
- Container ở 2 network khác nhau có thấy nhau không?

---

## **Bài 22: Multi-stage Build - Tối ưu image**

**Mục tiêu:** Giảm dung lượng image production.

**Yêu cầu:**

1. Viết `Dockerfile.multi`:
```dockerfile
# Stage 1: Builder
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
CMD ["python", "app.py"]
```

2. Build và so sánh:
```bash
docker build -t myapp:5.0-slim -f Dockerfile.multi .
docker images myapp
```

**Câu hỏi:**
- Image multi-stage nhỏ hơn bao nhiêu %?
- Khi nào nên dùng multi-stage?

---

## **Bài 23: Docker Compose - Orchestrate Multi-Container**

**Mục tiêu:** Quản lý nhiều container bằng 1 file YAML.

**Yêu cầu:**

1. Tạo `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build: .
    image: myapp:6.0
    ports:
      - "8080:5000"
    environment:
      - APP_NAME=Compose App
      - APP_ENV=production
    depends_on:
      - redis
      - db
    networks:
      - myapp-net
    volumes:
      - ./logs:/app/logs

  redis:
    image: redis:alpine
    networks:
      - myapp-net

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myappdb
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret123
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - myapp-net

networks:
  myapp-net:

volumes:
  db-data:
```

2. Khởi động:
```bash
docker-compose up -d
docker-compose ps
docker-compose logs -f web
```

3. Scale service:
```bash
docker-compose up -d --scale web=3
```

4. Dừng:
```bash
docker-compose down
docker-compose down -v   # xóa cả volume
```

**Câu hỏi:**
- `depends_on` đảm bảo gì? (thứ tự khởi động, không phải sẵn sàng)
- So với chạy `docker run` từng container, compose có ưu điểm gì?

---

## **Bài 24: Push lên Registry**

**Mục tiêu:** Chuẩn bị image để deploy.

**Yêu cầu:**

1. Đăng nhập Docker Hub:
```bash
docker login
```

2. Tag image theo format `username/imagename:tag`:
```bash
docker tag myapp:6.0 <your-username>/myapp:6.0
docker tag myapp:6.0 <your-username>/myapp:latest
```

3. Push:
```bash
docker push <your-username>/myapp:6.0
docker push <your-username>/myapp:latest
```

4. Verify trên Docker Hub web UI

5. Test pull về máy khác (hoặc xóa local rồi pull lại):
```bash
docker rmi <your-username>/myapp:6.0
docker pull <your-username>/myapp:6.0
```

---

# ☸️ PHẦN B: KUBERNETES

> **Lưu ý:** Tiếp tục dùng image `myapp:6.0` đã push ở Bài 24. Tất cả bài K8s dưới đây đều xoay quanh app này.

## **Bài 25: Cài đặt K8s và kiểm tra**

**Mục tiêu:** Có cluster để thực hành.

**Yêu cầu:**

1. Chọn 1 trong các option:
   - **Minikube:** `minikube start --driver=docker`
   - **Kind:** `kind create cluster --name myapp-cluster`
   - **Docker Desktop:** Enable Kubernetes trong Settings

2. Kiểm tra:
```bash
kubectl version
kubectl cluster-info
kubectl get nodes
kubectl get pods -A    # Xem system pods
```

3. Cài autocomplete (bash):
```bash
source <(kubectl completion bash)
echo 'alias k=kubectl' >> ~/.bashrc
```

---

## **Bài 26: Namespace - Tổ chức tài nguyên**

**Mục tiêu:** Cô lập môi trường dev/staging/prod.

**Yêu cầu:**

1. Tạo 3 namespace:
```bash
kubectl create namespace dev
kubectl create namespace staging
kubectl create namespace prod
kubectl get ns
```

2. Tạo bằng YAML (cách khuyến khích):
```yaml
# namespaces.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: myapp-dev
---
apiVersion: v1
kind: Namespace
metadata:
  name: myapp-prod
```

```bash
kubectl apply -f namespaces.yaml
```

3. Set default namespace:
```bash
kubectl config set-context --current --namespace=myapp-dev
kubectl config view --minify | grep namespace
```

---

## **Bài 27: Pod đầu tiên - Chạy myapp trên K8s**

**Mục tiêu:** Tạo pod chạy chính app đã build ở Docker.

**Yêu cầu:**

1. Tạo `pod.yaml`:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  namespace: myapp-dev
  labels:
    app: myapp
    version: "6.0"
spec:
  containers:
    - name: myapp
      image: <your-username>/myapp:6.0
      ports:
        - containerPort: 5000
      env:
        - name: APP_NAME
          value: "K8s App"
        - name: APP_ENV
          value: "kubernetes"
```

2. Apply và kiểm tra:
```bash
kubectl apply -f pod.yaml
kubectl get pods
kubectl get pods -o wide
kubectl describe pod myapp-pod
```

3. Test app qua port-forward:
```bash
kubectl port-forward pod/myapp-pod 8080:5000
# Mở terminal khác:
curl http://localhost:8080
```

**Câu hỏi:**
- Pod khác Container thế nào?
- Tại sao app chưa kết nối được Redis? (vì chưa có redis trong cluster)

---

## **Bài 28: Pod Logs, Exec, Describe (Tương tự Docker)**

**Mục tiêu:** Debug pod như đã làm với container.

**Yêu cầu:**

```bash
# Xem log (giống docker logs)
kubectl logs myapp-pod
kubectl logs -f myapp-pod
kubectl logs --tail=20 myapp-pod

# Exec vào pod (giống docker exec)
kubectl exec -it myapp-pod -- /bin/bash

# Describe - rất quan trọng để debug
kubectl describe pod myapp-pod

# Copy file (giống docker cp)
kubectl cp myapp-pod:/app/app.py ./pod-app.py
```

**So sánh:**

| Docker | Kubernetes |
|--------|-----------|
| `docker logs` | `kubectl logs` |
| `docker exec` | `kubectl exec` |
| `docker inspect` | `kubectl describe` |
| `docker cp` | `kubectl cp` |
| `docker ps` | `kubectl get pods` |

---

## **Bài 29: Deployment - Quản lý nhiều pod**

**Mục tiêu:** Tự động tạo, scale, update pod.

**Yêu cầu:**

1. Xóa pod cũ:
```bash
kubectl delete pod myapp-pod
```

2. Tạo `deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  namespace: myapp-dev
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: <your-username>/myapp:6.0
          ports:
            - containerPort: 5000
          env:
            - name: APP_ENV
              value: "kubernetes"
          resources:
            requests:
              memory: "64Mi"
              cpu: "100m"
            limits:
              memory: "128Mi"
              cpu: "200m"
```

3. Apply và quan sát:
```bash
kubectl apply -f deployment.yaml
kubectl get deployments
kubectl get replicasets
kubectl get pods    # Có 3 pod
```

4. Test self-healing - xóa 1 pod:
```bash
kubectl delete pod <pod-name>
kubectl get pods    # Pod mới tự được tạo!
```

5. Scale:
```bash
kubectl scale deployment myapp-deployment --replicas=5
kubectl get pods
```

---

## **Bài 30: Service - Expose Deployment**

**Mục tiêu:** Cho phép truy cập app từ ngoài và load balance giữa các pod.

**Yêu cầu:**

1. Tạo `service.yaml`:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: myapp-dev
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 5000
      nodePort: 30080
```

2. Apply:
```bash
kubectl apply -f service.yaml
kubectl get services
```

3. Truy cập:
```bash
# Với Minikube:
minikube service myapp-service -n myapp-dev --url
# Hoặc port-forward:
kubectl port-forward service/myapp-service 8080:80
curl http://localhost:8080
```

4. Test load balancing - gọi nhiều lần, kết hợp với log:
```bash
for i in {1..10}; do curl http://localhost:8080; echo; done
kubectl logs -l app=myapp --tail=20
```

**Câu hỏi:**
- Sự khác nhau: ClusterIP, NodePort, LoadBalancer?
- `selector` trong Service hoạt động thế nào với `labels` của Pod?

---

## **Bài 31: Rolling Update & Rollback**

**Mục tiêu:** Cập nhật app không downtime.

**Yêu cầu:**

1. Sửa code app thành version 7.0, build và push image mới:
```bash
docker build -t <your-username>/myapp:7.0 .
docker push <your-username>/myapp:7.0
```

2. Update deployment:
```bash
kubectl set image deployment/myapp-deployment myapp=<your-username>/myapp:7.0
```

3. Quan sát rolling update:
```bash
kubectl rollout status deployment/myapp-deployment
kubectl get pods -w
```

4. Xem lịch sử:
```bash
kubectl rollout history deployment/myapp-deployment
```

5. Rollback:
```bash
kubectl rollout undo deployment/myapp-deployment
kubectl rollout undo deployment/myapp-deployment --to-revision=1
```

---

## **Bài 32: ConfigMap - Cấu hình bên ngoài**

**Mục tiêu:** Tách config khỏi image (giống env trong Docker nhưng quản lý tập trung).

**Yêu cầu:**

1. Tạo `configmap.yaml`:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
  namespace: myapp-dev
data:
  APP_NAME: "MyApp on K8s"
  APP_ENV: "production"
  APP_VERSION: "7.0"
  LOG_LEVEL: "INFO"
```

2. Apply:
```bash
kubectl apply -f configmap.yaml
kubectl get configmaps
kubectl describe configmap myapp-config
```

3. Cập nhật Deployment dùng ConfigMap:
```yaml
# Trong deployment.yaml, thay phần env:
        env:
          - name: APP_NAME
            valueFrom:
              configMapKeyRef:
                name: myapp-config
                key: APP_NAME
          - name: APP_ENV
            valueFrom:
              configMapKeyRef:
                name: myapp-config
                key: APP_ENV

# HOẶC load toàn bộ:
        envFrom:
          - configMapRef:
              name: myapp-config
```

4. Apply lại deployment và verify:
```bash
kubectl apply -f deployment.yaml
kubectl rollout restart deployment/myapp-deployment
kubectl exec -it <pod-name> -- env | grep APP_
```

---

## **Bài 33: Secret - Lưu trữ thông tin nhạy cảm**

**Mục tiêu:** Quản lý password, API key an toàn.

**Yêu cầu:**

1. Tạo secret bằng lệnh:
```bash
kubectl create secret generic myapp-secret \
  --from-literal=DB_PASSWORD=supersecret123 \
  --from-literal=API_KEY=abc-xyz-789
```

2. Hoặc bằng YAML (base64 encoded):
```bash
echo -n "supersecret123" | base64
# c3VwZXJzZWNyZXQxMjM=
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
data:
  DB_PASSWORD: c3VwZXJzZWNyZXQxMjM=
  API_KEY: YWJjLXh5ei03ODk=
```

3. Sử dụng trong Deployment:
```yaml
        env:
          - name: DB_PASSWORD
            valueFrom:
              secretKeyRef:
                name: myapp-secret
                key: DB_PASSWORD
```

4. Verify:
```bash
kubectl get secrets
kubectl describe secret myapp-secret
kubectl get secret myapp-secret -o yaml
```

---

## **Bài 34: PersistentVolume & PersistentVolumeClaim**

**Mục tiêu:** Lưu trữ dữ liệu bền vững (giống Volume trong Docker).

**Yêu cầu:**

1. Tạo PV:
```yaml
# pv.yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: myapp-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /tmp/myapp-data
```

2. Tạo PVC:
```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myapp-pvc
  namespace: myapp-dev
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
```

3. Mount vào pod (sửa deployment):
```yaml
      containers:
        - name: myapp
          # ...
          volumeMounts:
            - name: logs
              mountPath: /app/logs
      volumes:
        - name: logs
          persistentVolumeClaim:
            claimName: myapp-pvc
```

4. Test:
```bash
kubectl apply -f pv.yaml -f pvc.yaml
kubectl apply -f deployment.yaml
kubectl get pv,pvc
```

---

## **Bài 35: Redis trong K8s + App kết nối**

**Mục tiêu:** Hoàn thiện multi-tier app trên K8s (giống Bài 21 nhưng trên K8s).

**Yêu cầu:**

1. Tạo Redis deployment + service:
```yaml
# redis.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: myapp-dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
        - name: redis
          image: redis:alpine
          ports:
            - containerPort: 6379
---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: myapp-dev
spec:
  selector:
    app: redis
  ports:
    - port: 6379
      targetPort: 6379
```

2. App tự động kết nối Redis qua DNS `redis.myapp-dev.svc.cluster.local` (hoặc gọn `redis`)

3. Apply và test:
```bash
kubectl apply -f redis.yaml
kubectl port-forward service/myapp-service 8080:80
for i in {1..5}; do curl http://localhost:8080; echo; done
```

---

## **Bài 36: Liveness & Readiness Probes**

**Mục tiêu:** Đảm bảo K8s biết khi nào pod khỏe/sẵn sàng.

**Yêu cầu:**

1. Thêm vào deployment:
```yaml
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
```

2. Test bằng cách làm app trả lỗi tạm thời, quan sát K8s tự restart pod.

**Câu hỏi:**
- Liveness probe khác Readiness probe ra sao?
- Khi liveness fail, K8s làm gì? Khi readiness fail thì sao?

---

## **Bài 37: HPA - Auto Scaling**

**Mục tiêu:** Pod tự scale theo CPU/RAM.

**Yêu cầu:**

1. Cài metrics-server (nếu chưa có):
```bash
# Minikube:
minikube addons enable metrics-server
```

2. Tạo HPA:
```bash
kubectl autoscale deployment myapp-deployment \
  --cpu-percent=50 --min=2 --max=10
```

3. Tạo tải bằng tool:
```bash
kubectl run load-gen --image=busybox -it --rm -- /bin/sh
# Trong shell:
while true; do wget -q -O- http://myapp-service.myapp-dev; done
```

4. Quan sát:
```bash
kubectl get hpa -w
kubectl get pods
```

---

## **Bài 38: Ingress - Routing HTTP từ ngoài**

**Mục tiêu:** Cấu hình URL/host routing.

**Yêu cầu:**

1. Enable Ingress controller:
```bash
minikube addons enable ingress
```

2. Tạo Ingress:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  namespace: myapp-dev
spec:
  rules:
    - host: myapp.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-service
                port:
                  number: 80
```

3. Thêm vào `/etc/hosts`:
```
<minikube-ip> myapp.local
```

4. Test:
```bash
curl http://myapp.local
```

---

## **Bài 39: StatefulSet - Database Cluster**

**Mục tiêu:** Triển khai database với identity ổn định.

**Yêu cầu:**

1. Tạo Headless Service:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis-headless
  namespace: myapp-dev
spec:
  clusterIP: None
  selector:
    app: redis-cluster
  ports:
    - port: 6379
```

2. Tạo StatefulSet:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis-cluster
  namespace: myapp-dev
spec:
  serviceName: redis-headless
  replicas: 3
  selector:
    matchLabels:
      app: redis-cluster
  template:
    metadata:
      labels:
        app: redis-cluster
    spec:
      containers:
        - name: redis
          image: redis:alpine
          ports:
            - containerPort: 6379
          volumeMounts:
            - name: data
              mountPath: /data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 100Mi
```

3. Apply và verify:
```bash
kubectl apply -f redis-statefulset.yaml
kubectl get statefulsets
kubectl get pods   # Tên có thứ tự: redis-cluster-0, -1, -2
kubectl get pvc    # Mỗi pod có PVC riêng
```

**Câu hỏi:**
- StatefulSet khác Deployment ở điểm nào?
- Tại sao cần Headless Service?

---

## **Bài 40: Helm - Đóng gói toàn bộ app**

**Mục tiêu:** Quản lý ứng dụng K8s như package.

**Yêu cầu:**

1. Cài Helm:
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

2. Tạo chart cho myapp:
```bash
helm create myapp-chart
```

3. Tùy chỉnh `values.yaml`:
```yaml
replicaCount: 3
image:
  repository: <your-username>/myapp
  tag: "7.0"
service:
  type: NodePort
  port: 80
ingress:
  enabled: true
  host: myapp.local
```

4. Install/Upgrade/Rollback:
```bash
helm install myapp ./myapp-chart -n myapp-dev
helm upgrade myapp ./myapp-chart -n myapp-dev --set replicaCount=5
helm rollback myapp 1 -n myapp-dev
helm uninstall myapp -n myapp-dev
```

---

## **Bài 41: Dự án tổng hợp - Triển khai Full Stack**

**Mục tiêu:** Tổng hợp tất cả kiến thức.

**Đề bài:** Triển khai hoàn chỉnh hệ thống `myapp` lên K8s với:

✅ **Yêu cầu bắt buộc:**
1. Frontend: nginx serve static (1 deployment, 2 replica)
2. Backend API: `myapp:7.0` (1 deployment, 3 replica, HPA)
3. Redis cache (StatefulSet)
4. PostgreSQL (StatefulSet với PVC)
5. ConfigMap cho config chung
6. Secret cho passwords
7. Ingress với 2 path: `/` → frontend, `/api` → backend
8. Liveness/Readiness probes đầy đủ
9. Resource requests/limits
10. Đóng gói thành Helm chart

✅ **Yêu cầu nâng cao:**
- NetworkPolicy hạn chế giao tiếp
- ServiceAccount + RBAC riêng
- Monitoring với Prometheus + Grafana
- CI/CD: GitHub Actions tự build image và update Helm chart

**Tiêu chí đánh giá:**
- Tính sẵn sàng cao (high availability)
- Khả năng scale
- Bảo mật
- Khả năng quan sát (observability)
- Tự động hóa

---

# 🎯 PHẦN C: CHUYÊN SÂU

## 🎁 C.1. HELM TEMPLATE CHUYÊN SÂU (Bài 42-44)

> **Bối cảnh:** Sau khi đã làm quen Helm cơ bản ở Bài 40, giờ ta sẽ đi sâu vào templating engine của Helm - bí quyết để tạo chart linh hoạt cho nhiều môi trường.

---

## **Bài 42: Helm Template Functions & Pipelines**

**Mục tiêu:** Hiểu sâu cú pháp Go template trong Helm.

**Yêu cầu:**

### Phần A: Built-in Objects

1. Tạo chart mới `myapp-advanced`:
```bash
helm create myapp-advanced
cd myapp-advanced
```

2. Khám phá các built-in object trong template:
```yaml
# templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-info
  namespace: {{ .Release.Namespace }}
data:
  release-name: {{ .Release.Name }}
  release-namespace: {{ .Release.Namespace }}
  release-revision: {{ .Release.Revision | quote }}
  release-service: {{ .Release.Service }}
  chart-name: {{ .Chart.Name }}
  chart-version: {{ .Chart.Version }}
  app-version: {{ .Chart.AppVersion }}
  k8s-version: {{ .Capabilities.KubeVersion.Version }}
```

### Phần B: Template Functions

3. Sử dụng các function phổ biến trong `templates/deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name | lower }}-app
  labels:
    app: {{ .Chart.Name | upper }}
    version: {{ .Chart.Version | replace "." "-" }}
spec:
  replicas: {{ .Values.replicaCount | default 1 }}
  template:
    metadata:
      annotations:
        # checksum để rolling update khi config thay đổi
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        # Timestamp
        deployed-at: {{ now | date "2006-01-02T15:04:05Z" | quote }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          env:
            - name: APP_NAME
              value: {{ .Values.appName | quote }}
            - name: ENVIRONMENT
              value: {{ .Values.environment | upper | quote }}
            - name: FULL_NAME
              value: {{ printf "%s-%s" .Release.Name .Values.environment | quote }}
```

### Phần C: Pipelines

4. Kết hợp nhiều function với pipeline:
```yaml
# Ví dụ
{{ .Values.message | trim | upper | quote }}
{{ .Values.list | join ", " | quote }}
{{ .Values.password | b64enc | quote }}
{{ .Values.config | toYaml | indent 4 }}
```

5. Render thử và xem kết quả:
```bash
helm template myapp-advanced . --debug
helm install --dry-run --debug myapp ./myapp-advanced
```

**Bài tập:**
- Viết template sinh ra Secret từ password trong values.yaml, dùng `b64enc`
- Dùng `randAlphaNum 16` để sinh password ngẫu nhiên nếu chưa được set

---

## **Bài 43: Conditionals, Loops & Named Templates**

**Mục tiêu:** Viết template logic phức tạp.

**Yêu cầu:**

### Phần A: If/Else

1. Tạo template có điều kiện:
```yaml
# templates/ingress.yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ .Release.Name }}-ingress
  {{- if .Values.ingress.annotations }}
  annotations:
    {{- toYaml .Values.ingress.annotations | nindent 4 }}
  {{- end }}
spec:
  {{- if .Values.ingress.tls }}
  tls:
    - hosts:
        - {{ .Values.ingress.host }}
      secretName: {{ .Release.Name }}-tls
  {{- end }}
  rules:
    - host: {{ .Values.ingress.host }}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {{ .Release.Name }}-service
                port:
                  number: {{ .Values.service.port }}
{{- end }}
```

### Phần B: Range (Loop)

2. Tạo nhiều resource từ array:
```yaml
# values.yaml
environments:
  - name: dev
    replicas: 1
    cpu: "100m"
  - name: staging
    replicas: 2
    cpu: "200m"
  - name: prod
    replicas: 5
    cpu: "500m"
```

```yaml
# templates/multi-env.yaml
{{- range .Values.environments }}
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ $.Release.Name }}-{{ .name }}-config
data:
  ENV_NAME: {{ .name | quote }}
  REPLICAS: {{ .replicas | quote }}
  CPU_LIMIT: {{ .cpu | quote }}
{{- end }}
```

3. Loop trên map:
```yaml
# values.yaml
labels:
  app: myapp
  tier: backend
  team: platform
```

```yaml
metadata:
  labels:
    {{- range $key, $value := .Values.labels }}
    {{ $key }}: {{ $value | quote }}
    {{- end }}
```

### Phần C: Named Templates (_helpers.tpl)

4. Định nghĩa template tái sử dụng:
```yaml
# templates/_helpers.tpl
{{/*
Common labels
*/}}
{{- define "myapp.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "myapp.selectorLabels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Full name with truncation (K8s name limit 63 chars)
*/}}
{{- define "myapp.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
```

5. Sử dụng:
```yaml
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
```

---

## **Bài 44: Subchart, Dependencies & Hooks**

**Mục tiêu:** Tổ chức chart phức tạp với dependencies, lifecycle hooks.

**Yêu cầu:**

### Phần A: Dependencies

1. Khai báo dependency trong `Chart.yaml`:
```yaml
apiVersion: v2
name: myapp-fullstack
version: 1.0.0
dependencies:
  - name: redis
    version: "18.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: redis.enabled
  - name: postgresql
    version: "13.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

2. Pull dependencies:
```bash
helm dependency update
helm dependency list
```

3. Override values cho subchart trong `values.yaml`:
```yaml
redis:
  enabled: true
  auth:
    password: "myredispass"
  master:
    persistence:
      size: 1Gi

postgresql:
  enabled: true
  auth:
    username: myapp
    password: mypass
    database: myappdb
```

### Phần B: Hooks

4. Tạo hook chạy migration database trước khi install:
```yaml
# templates/migration-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ .Release.Name }}-migration
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-weight": "1"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migration
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          command: ["python", "migrate.py"]
          env:
            - name: DB_HOST
              value: "{{ .Release.Name }}-postgresql"
```

5. Hook test sau khi install:
```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: {{ .Release.Name }}-test-connection
  annotations:
    "helm.sh/hook": test
spec:
  restartPolicy: Never
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['{{ .Release.Name }}-service:80']
```

6. Test:
```bash
helm install myapp ./myapp-fullstack
helm test myapp
```

### Phần C: Multi-environment với 1 chart

7. Tạo file values riêng cho từng môi trường:
```bash
# values-dev.yaml
replicaCount: 1
image:
  tag: "dev-latest"
ingress:
  host: myapp.dev.local

# values-staging.yaml
replicaCount: 2
image:
  tag: "staging-v1.2"
ingress:
  host: myapp.staging.local

# values-prod.yaml
replicaCount: 5
image:
  tag: "v1.0"
ingress:
  host: myapp.production.com
  tls: true
```

8. Deploy:
```bash
helm install myapp-dev ./myapp-fullstack -f values-dev.yaml -n dev
helm install myapp-staging ./myapp-fullstack -f values-staging.yaml -n staging
helm install myapp-prod ./myapp-fullstack -f values-prod.yaml -n prod
```

---

## 🚀 C.2. ARGOCD - GITOPS (Bài 45-47)

> **Bối cảnh:** Thay vì `kubectl apply` thủ công hoặc CI/CD push-based, GitOps dùng Git làm nguồn chân lý duy nhất. ArgoCD tự động đồng bộ trạng thái cluster với Git.

---

## **Bài 45: Cài đặt ArgoCD và Application đầu tiên**

**Mục tiêu:** Setup ArgoCD và deploy `myapp` qua GitOps.

**Yêu cầu:**

### Phần A: Cài đặt

1. Cài ArgoCD vào cluster:
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

2. Đợi pod ready:
```bash
kubectl get pods -n argocd -w
```

3. Cài ArgoCD CLI:
```bash
# Linux
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
```

4. Truy cập UI:
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Mở https://localhost:8080
```

5. Lấy password admin:
```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

6. Đăng nhập CLI:
```bash
argocd login localhost:8080 --username admin --password <password>
```

### Phần B: Tạo Git Repository

7. Tạo repo Git (GitHub) với cấu trúc:
```
myapp-gitops/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── environments/
    ├── dev/
    │   └── kustomization.yaml
    └── prod/
        └── kustomization.yaml
```

8. Push các manifest từ Bài 29-33 vào `base/`

### Phần C: Tạo Application

9. Tạo Application qua YAML:
```yaml
# argocd-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-dev
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/<your-username>/myapp-gitops
    targetRevision: main
    path: environments/dev
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp-dev
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

10. Apply:
```bash
kubectl apply -f argocd-app.yaml
```

11. Quan sát trên UI - thấy app được sync tự động

**Câu hỏi:**
- `prune: true` làm gì?
- `selfHeal: true` xử lý tình huống nào?

---

## **Bài 46: GitOps Workflow - Deploy qua Git**

**Mục tiêu:** Trải nghiệm luồng deploy hoàn toàn qua Git.

**Yêu cầu:**

### Kịch bản: Update image version

1. Trên máy local, sửa file `environments/dev/kustomization.yaml`:
```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
images:
  - name: <your-username>/myapp
    newTag: "8.0"   # Đổi từ 7.0 thành 8.0
```

2. Commit và push:
```bash
git add .
git commit -m "Update myapp to v8.0 in dev"
git push origin main
```

3. Quan sát ArgoCD UI - tự động phát hiện thay đổi và sync (mặc định polling mỗi 3 phút)

4. Force sync nếu muốn nhanh:
```bash
argocd app sync myapp-dev
```

### Kịch bản: Tự self-heal khi có drift

5. Cố ý thay đổi thủ công bằng kubectl:
```bash
kubectl scale deployment myapp-deployment --replicas=10 -n myapp-dev
```

6. Quan sát: ArgoCD phát hiện drift và **tự revert** về trạng thái trong Git

### Kịch bản: Rollback

7. Xem lịch sử trong UI hoặc CLI:
```bash
argocd app history myapp-dev
```

8. Rollback về version trước:
```bash
argocd app rollback myapp-dev <revision-id>
```

**Lưu ý:** Trong GitOps thuần, rollback đúng đắn là **revert commit trong Git** rồi để ArgoCD sync.

---

## **Bài 47: Multi-environment với ApplicationSet**

**Mục tiêu:** Quản lý nhiều môi trường (dev/staging/prod) tự động.

**Yêu cầu:**

### Phần A: ApplicationSet với List Generator

1. Tạo ApplicationSet quản lý 3 môi trường:
```yaml
# applicationset.yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: myapp-environments
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - env: dev
            namespace: myapp-dev
            branch: develop
          - env: staging
            namespace: myapp-staging
            branch: staging
          - env: prod
            namespace: myapp-prod
            branch: main
  template:
    metadata:
      name: 'myapp-{{env}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/<your-username>/myapp-gitops
        targetRevision: '{{branch}}'
        path: 'environments/{{env}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

2. Apply:
```bash
kubectl apply -f applicationset.yaml
```

3. Quan sát: 3 Application được tự động tạo ra.

### Phần B: ArgoCD với Helm

4. Application dùng Helm chart:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-helm-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/<your-username>/myapp-helm
    targetRevision: main
    path: charts/myapp
    helm:
      valueFiles:
        - values-prod.yaml
      parameters:
        - name: image.tag
          value: "v1.0"
        - name: replicaCount
          value: "5"
  destination:
    server: https://kubernetes.default.svc
    namespace: myapp-prod
  syncPolicy:
    automated:
      prune: true
```

### Phần C: Image Updater (Bonus)

5. Cài ArgoCD Image Updater để tự động update image khi có version mới:
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj-labs/argocd-image-updater/stable/manifests/install.yaml
```

6. Annotate Application:
```yaml
metadata:
  annotations:
    argocd-image-updater.argoproj.io/image-list: myapp=<your-username>/myapp
    argocd-image-updater.argoproj.io/myapp.update-strategy: semver
```

**Bài tập:**
- Push image mới với tag `v1.0.1`, quan sát Image Updater tự update
- Cấu hình Slack notification khi sync thành công/thất bại

---

## 🕸️ C.3. SERVICE MESH - ISTIO (Bài 48-50)

> **Bối cảnh:** Khi có nhiều microservice, việc quản lý traffic, security, observability trở nên phức tạp. Service Mesh inject sidecar proxy (Envoy) vào mỗi pod để xử lý các tác vụ này mà không cần sửa code app.

---

## **Bài 48: Cài Istio và Sidecar Injection**

**Mục tiêu:** Setup Istio, hiểu cách sidecar hoạt động.

**Yêu cầu:**

### Phần A: Cài đặt

1. Download và cài Istio:
```bash
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y
```

2. Cài addon (Kiali, Jaeger, Grafana, Prometheus):
```bash
kubectl apply -f samples/addons/
kubectl rollout status deployment/kiali -n istio-system
```

3. Enable automatic sidecar injection cho namespace:
```bash
kubectl label namespace myapp-dev istio-injection=enabled
```

### Phần B: Redeploy và quan sát sidecar

4. Restart deployment để inject sidecar:
```bash
kubectl rollout restart deployment/myapp-deployment -n myapp-dev
```

5. Kiểm tra: mỗi pod giờ có **2 container** (app + istio-proxy):
```bash
kubectl get pods -n myapp-dev
# READY: 2/2 (thay vì 1/1 trước đây)

kubectl describe pod <pod-name> -n myapp-dev
# Có thêm container 'istio-proxy'
```

6. Mở Kiali Dashboard để xem topology:
```bash
istioctl dashboard kiali
```

### Phần C: Truy cập app qua Istio Gateway

7. Tạo Gateway (thay cho Ingress):
```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: myapp-gateway
  namespace: myapp-dev
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - "myapp.local"
---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp-vs
  namespace: myapp-dev
spec:
  hosts:
    - "myapp.local"
  gateways:
    - myapp-gateway
  http:
    - route:
        - destination:
            host: myapp-service
            port:
              number: 80
```

8. Apply và test:
```bash
kubectl apply -f gateway.yaml
# Lấy IP của istio-ingressgateway
kubectl get svc istio-ingressgateway -n istio-system
```

**Câu hỏi:**
- Sidecar proxy là gì? Tại sao gọi là "service mesh"?
- Mô hình data plane vs control plane trong Istio?

---

## **Bài 49: Traffic Management - Canary, A/B Testing**

**Mục tiêu:** Triển khai chiến lược release nâng cao.

**Yêu cầu:**

### Phần A: Canary Deployment

1. Deploy 2 version của myapp:
```yaml
# myapp v1
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: v1
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      containers:
        - name: myapp
          image: <your-username>/myapp:7.0
---
# myapp v2
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-v2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
      version: v2
  template:
    metadata:
      labels:
        app: myapp
        version: v2
    spec:
      containers:
        - name: myapp
          image: <your-username>/myapp:8.0
```

2. Tạo DestinationRule định nghĩa subset:
```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp-destination
spec:
  host: myapp-service
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
```

3. VirtualService với traffic splitting 90/10:
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp-canary
spec:
  hosts:
    - myapp-service
  http:
    - route:
        - destination:
            host: myapp-service
            subset: v1
          weight: 90
        - destination:
            host: myapp-service
            subset: v2
          weight: 10
```

4. Test bằng cách gọi nhiều lần:
```bash
for i in {1..100}; do
  curl -s http://myapp.local/config | grep version
done | sort | uniq -c
# Sẽ thấy ~90% v1, ~10% v2
```

5. Tăng dần traffic về v2: 50/50, rồi 0/100.

### Phần B: A/B Testing theo Header

6. Route theo HTTP header:
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp-ab-test
spec:
  hosts:
    - myapp-service
  http:
    - match:
        - headers:
            user-type:
              exact: beta-tester
      route:
        - destination:
            host: myapp-service
            subset: v2
    - route:
        - destination:
            host: myapp-service
            subset: v1
```

7. Test:
```bash
# User thường → v1
curl http://myapp.local

# Beta tester → v2
curl -H "user-type: beta-tester" http://myapp.local
```

### Phần C: Fault Injection

8. Inject lỗi để test resilience:
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp-fault
spec:
  hosts:
    - myapp-service
  http:
    - fault:
        delay:
          percentage:
            value: 50
          fixedDelay: 5s
        abort:
          percentage:
            value: 10
          httpStatus: 500
      route:
        - destination:
            host: myapp-service
            subset: v1
```

9. Test - 50% request bị delay 5s, 10% bị lỗi 500.

---

## **Bài 50: Security & Observability với Istio (Dự án cuối)**

**Mục tiêu:** Hoàn thiện hệ thống với mTLS, RBAC, distributed tracing.

**Yêu cầu:**

### Phần A: Mutual TLS (mTLS) tự động

1. Enable strict mTLS toàn cluster:
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

2. Verify mTLS hoạt động:
```bash
istioctl authn tls-check myapp-pod.myapp-dev
```

3. Capture traffic giữa các pod - thấy được encrypt.

### Phần B: Authorization Policy (RBAC tầng L7)

4. Chỉ cho phép service nhất định gọi myapp:
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: myapp-authz
  namespace: myapp-dev
spec:
  selector:
    matchLabels:
      app: myapp
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/myapp-dev/sa/frontend-sa"]
      to:
        - operation:
            methods: ["GET"]
            paths: ["/", "/health"]
    - from:
        - source:
            namespaces: ["myapp-dev"]
      to:
        - operation:
            methods: ["GET", "POST"]
```

5. Test: pod ngoài namespace gọi → bị từ chối.

### Phần C: Distributed Tracing với Jaeger

6. Tạo tải:
```bash
for i in {1..100}; do curl http://myapp.local; done
```

7. Mở Jaeger:
```bash
istioctl dashboard jaeger
```

8. Quan sát:
- Request flow qua các service
- Latency từng span
- Tìm bottleneck

### Phần D: Metrics với Prometheus + Grafana

9. Mở Grafana:
```bash
istioctl dashboard grafana
```

10. Xem các dashboard có sẵn:
- Istio Mesh Dashboard
- Istio Service Dashboard
- Istio Workload Dashboard

11. Quan sát: P50, P95, P99 latency, error rate, request rate (RED metrics).

### 🎓 DỰ ÁN CUỐI KHÓA - HỆ THỐNG HOÀN CHỈNH

**Đề bài:** Triển khai hệ thống microservices `myapp` hoàn chỉnh với:

✅ **Bắt buộc:**
1. **Code & Docker:**
   - 3 microservice: frontend (React), backend API (Python), worker (Python)
   - Multi-stage Dockerfile, image nhỏ gọn
   - Push lên registry với tag semver

2. **Kubernetes:**
   - Deployment + Service + Ingress
   - ConfigMap + Secret
   - StatefulSet cho database
   - PVC cho persistent data
   - HPA cho frontend và API
   - Liveness/Readiness probes
   - Resource limits

3. **Helm:**
   - Đóng gói toàn bộ thành 1 chart
   - Subchart cho Redis, PostgreSQL
   - Values riêng cho dev/staging/prod
   - Hook chạy migration

4. **GitOps với ArgoCD:**
   - ApplicationSet cho 3 môi trường
   - Auto-sync và self-heal
   - Image Updater tự động cập nhật version

5. **Service Mesh với Istio:**
   - Sidecar injection
   - Gateway thay Ingress
   - Canary deployment khi release
   - mTLS strict
   - Authorization Policy hạn chế truy cập

6. **Observability:**
   - Distributed tracing với Jaeger
   - Metrics với Prometheus + Grafana
   - Logging tập trung với Loki hoặc EFK

✅ **Bonus:**
- CI/CD pipeline tự động build và update Helm chart
- Chaos testing với Chaos Mesh
- Backup & Restore strategy cho database
- Cost optimization (right-sizing resources)

**Tiêu chí đánh giá:**

| Tiêu chí | Trọng số |
|----------|----------|
| Tính sẵn sàng cao (HA) | 20% |
| Bảo mật (mTLS, RBAC, Secret management) | 20% |
| Khả năng quan sát (Logs, Metrics, Traces) | 20% |
| Tự động hóa (GitOps, CI/CD) | 20% |
| Documentation & hướng dẫn deploy | 10% |
| Khả năng mở rộng | 10% |

---

## 📚 Tổng kết lộ trình

| Giai đoạn | Bài | Trọng tâm | Thời lượng đề xuất |
|-----------|-----|-----------|---------------------|
| **Docker cơ bản** | 1-8 | Image, Tag, Inspect | 1 tuần |
| **Container vận hành** | 9-17 | Run, lifecycle, debug | 1 tuần |
| **Docker nâng cao** | 18-24 | Env, Volume, Network, Compose, Registry | 1 tuần |
| **K8s cơ bản** | 25-30 | Pod, Deployment, Service | 1 tuần |
| **K8s nâng cao** | 31-38 | Update, Config, Storage, Probes, HPA, Ingress | 2 tuần |
| **K8s production** | 39-41 | StatefulSet, Helm, Dự án | 1 tuần |
| **Helm chuyên sâu** | 42-44 | Template, Hooks, Dependencies | 1 tuần |
| **GitOps - ArgoCD** | 45-47 | Application, ApplicationSet | 1 tuần |
| **Service Mesh** | 48-50 | Istio, Traffic, Security, Observability | 2 tuần |

**Tổng cộng:** ~11 tuần học bài bản từ zero đến production-ready.

---

## 🛠️ Tools & Tài nguyên tham khảo

### Local Development
- Docker Desktop / Podman
- Minikube / Kind / k3d
- kubectl, helm, argocd CLI
- istioctl, kustomize

### CI/CD
- GitHub Actions / GitLab CI / Jenkins
- ArgoCD / Flux

### Monitoring
- Prometheus + Grafana
- Jaeger / Tempo
- Loki / ELK Stack

### Cloud Providers (để thực hành thực tế)
- AWS EKS
- GCP GKE
- Azure AKS
- DigitalOcean Kubernetes

### Học tập tham khảo
- [Kubernetes Official Docs](https://kubernetes.io/docs/)
- [Helm Docs](https://helm.sh/docs/)
- [ArgoCD Docs](https://argo-cd.readthedocs.io/)
- [Istio Docs](https://istio.io/latest/docs/)

---

> **Lời khuyên:** Đừng vội vàng - mỗi bài cần thực hành tay, gặp lỗi, sửa lỗi mới hiểu sâu. Sau mỗi giai đoạn, tự tạo project nhỏ áp dụng kiến thức để củng cố.

**Chúc bạn học tập hiệu quả! 🚀**
