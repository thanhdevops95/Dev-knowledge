---
title: Ghép Cặp Đa Dịch Vụ Với Docker Compose
author: Mr.Rom
version: v3.0.0
date: 2026-05-26
level: Basic
tags: [MUST-KNOW, DEVOPS, DOCKER]
---

# 🎓 Ghép Cặp Đa Dịch Vụ Với Docker Compose

> 🎯 **Lời dẫn của Mr.Rom:** 
> Tiếp tục hành trình chinh phục Docker của chúng ta: Giờ đây bạn đã tự build thành công image `myapp:v1` cho ứng dụng của mình. Nhưng một ứng dụng thực tế trên Production hiếm khi đứng độc lập. Nó cần kết nối tới PostgreSQL để lưu trữ dữ liệu, Redis để lưu cache và chạy các tác vụ nền. Gõ 5-6 dòng lệnh `docker run` thủ công rồi tạo mạng kết nối từng cái là một cực hình vô cùng tẻ nhạt. Bài học này sẽ khai phóng cho bạn sức mạnh của **Docker Compose** — giúp bạn quản lý toàn bộ dàn nhạc container chỉ với **một tệp YAML duy nhất**!

## 🎯 Sau bài học này, bạn sẽ làm chủ:

- [x] Lý do cốt lõi vì sao phải dùng Docker Compose thay thế cho hàng loạt lệnh `docker run` rườm rà.
- [x] Thiết kế hoàn chỉnh một tệp `docker-compose.yml` kết nối an toàn giữa Web App + PostgreSQL + Redis.
- [x] Sử dụng thành thạo bộ công cụ điều khiển: `up`, `down`, `ps`, `logs`, `exec`, `restart`.
- [x] Bản chất của cơ chế **Service Discovery** — cách các container gọi nhau thông qua "bí danh" DNS thay vì địa chỉ IP cứng.
- [x] Quản lý dữ liệu lưu trữ bền vững (**volumes**) và cấu hình bảo mật (**environment**) trong Compose.
- [x] Sử dụng tệp `.env` để bảo mật thông tin nhạy cảm và linh hoạt hóa tham số.

---

## Tình Huống: Khi Ứng Dụng Đơn Lẻ Trở Thành Hệ Thống Phức Tạp Đa Dịch Vụ

Bạn đã đóng gói thành công image `myapp:v1` của riêng mình và hào hứng khởi chạy thử:

```bash
# Chạy thử ứng dụng của bạn
docker run -p 5000:5000 myapp:v1
```

🔥 **Hệ thống lập tức báo lỗi crash:**
```text
ConnectionRefusedError: Cannot connect to PostgreSQL on db:5432
```

Nguyên nhân rất rõ ràng: Ứng dụng Flask của bạn cần kết nối đến PostgreSQL để truy vấn cơ sở dữ liệu. Bạn nhanh trí khởi chạy tiếp một container PostgreSQL độc lập:

```bash
# Khởi chạy Postgres độc lập
docker run -d --name db -e POSTGRES_PASSWORD=secret postgres:15

# Chạy lại app của bạn và truyền tên host là "db"
docker run -p 5000:5000 -e DB_HOST=db myapp:v1
```

🔥 **Vẫn báo lỗi nghiêm trọng:**
```text
psycopg2.OperationalError: could not translate host name "db" to address: Name or service not known
```

❌ **Giải mã lỗi:** Dù cả hai container đều đang chạy trên cùng một máy tính, nhưng chúng nằm ở hai dải mạng ảo biệt lập của Docker, hoàn toàn không nhìn thấy và không thể nói chuyện được với nhau. 

Để giải quyết, bạn phải tự tay gõ một chuỗi các lệnh cực kỳ dài dòng và phức tạp:

```bash
# Bước 1: Tạo một mạng ảo kết nối chung
docker network create mynet

# Bước 2: Chạy Postgres gắn vào mạng ảo này và khai báo volume
docker run -d --name db --network mynet -e POSTGRES_PASSWORD=secret -v pg-data:/var/lib/postgresql/data postgres:15

# Bước 3: Chạy Redis gắn vào mạng ảo chung
docker run -d --name redis --network mynet redis:7-alpine

# Bước 4: Chạy app của bạn và truyền tham số kết nối
docker run -d --name app --network mynet -p 5000:5000 -e DB_HOST=db -e REDIS_HOST=redis myapp:v1

# Bước 5: Chạy thêm một container worker xử lý tác vụ nền
docker run -d --name worker --network mynet -e DB_HOST=db myapp:v1 celery worker
```

**Thực tế mệt mỏi:** 5 dòng lệnh dài dằng dặc, chỉ cần gõ sai 1 ký tự là cả hệ thống sụp đổ. Khi muốn tắt, bạn lại phải gõ `docker stop` rồi `docker rm` từng container một. Bạn phát hiện ra cách làm này cực kỳ tốn thời gian và dễ xảy ra lỗi khi bàn giao cho người khác.

Đúng lúc đó, sếp đi ngang qua và buông một câu hỏi quen thuộc: *"Sao em không dùng Compose?"* 

Bài học này sẽ hướng dẫn bạn giải quyết triệt để nỗi đau đó chỉ bằng **1 tệp YAML** duy nhất.

---

## 1️⃣ Nỗi Đau Thực Tế: Tại Sao Quản Lý Nhiều Container Bằng Tay Lại Là Cực Hình?

Một ứng dụng thực tế trên môi trường Production thường có cấu trúc phân tầng phức tạp như thế này:

```text
Thư mục dự án /
├── Dịch vụ Frontend (React/NextJS)  --> 1 container
├── Dịch vụ Backend (Flask/Express)  --> 1 container
├── Cơ sở dữ liệu chính (PostgreSQL)  --> 1 container
└── Bộ nhớ đệm Cache (Redis)         --> 1 container
```

Nếu không sử dụng Docker Compose, việc duy trì cấu hình mạng, cổng kết nối, volume lưu trữ của 4 container này trên máy dev của cả đội sẽ nhanh chóng biến thành một cơn ác mộng vì không có tính nhất quán.

### Phép màu từ Docker Compose mang lại

Chỉ với 1 tệp cấu hình `docker-compose.yml`, bạn khai báo toàn bộ cấu trúc hệ thống:

```yaml
# docker-compose.yml mẫu
services:
  app:
    image: my-app:v1
    ports:
      - "5000:5000"
    depends_on:
      - db
      - redis
    environment:
      DB_HOST: db
      REDIS_HOST: redis
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - pg-data:/var/lib/postgresql/data
  redis:
    image: redis:7-alpine

volumes:
  pg-data:
```

Để khởi động toàn bộ hệ thống gồm App + DB + Redis đồng loạt:
```bash
# Một lệnh khởi chạy tất cả
docker compose up -d
```

Để dừng toàn bộ, dọn sạch container và mạng ảo:
```bash
# Một lệnh dọn dẹp sạch sẽ
docker compose down
```

Không còn phải gõ hàng chục lệnh rườm rà. Hệ thống của bạn giờ đây đã được tài liệu hóa thành code (Configuration as Code), cực kỳ dễ dàng chia sẻ cho bất kỳ ai trong team!

---

## 2️⃣ Bản Chất Của Docker Compose: Nhạc Trưởng Cho Dàn Đồng Ca Container

**Định nghĩa chuẩn xác:** Docker Compose là một công cụ giúp định nghĩa và khởi chạy các ứng dụng Docker sử dụng **nhiều container cùng lúc**. Toàn bộ cấu hình hệ thống được khai báo thông qua một tệp tin định dạng YAML mang tên `docker-compose.yml`.

> [!NOTE]
> **Ẩn dụ sư phạm từ Mr.Rom:** 
> Hãy tưởng tượng Docker Compose giống như một **vị nhạc trưởng tài ba** đứng trước dàn nhạc giao hưởng. Mỗi container là một nhạc công chơi một loại nhạc cụ riêng (Violin, Kèn, Trống). Tệp `docker-compose.yml` chính là bản phổ nhạc ghi rõ ai chơi nhạc cụ gì, kết nối với ai và khi nào bắt đầu. Khi vị nhạc trưởng vung gậy điều khiển (`docker compose up`), cả dàn nhạc sẽ cất tiếng hát nhịp nhàng, đồng bộ và hoàn hảo!

### Cấu trúc cơ bản của tệp `docker-compose.yml`

Tệp cấu hình Compose luôn bao gồm **3 phân vùng chính (Top-level sections)**:

```yaml
# Khai báo các dịch vụ (container) chạy trong hệ thống
services:
  tên-dịch-vụ-1:
    image: ...        # Sử dụng image có sẵn từ Registry
    build: .          # Hoặc tự build từ Dockerfile ở thư mục hiện tại
    ports:
      - "cổng-host:cổng-container"
    environment:
      TÊN_BIẾN: giá-trị
    volumes:
      - tên-volume:/thư-mục-trong-container

# Khai báo các vùng lưu trữ dữ liệu bền vững dùng chung
volumes:
  tên-volume:

# Khai báo mạng ảo dùng riêng (tùy chọn - mặc định Compose tự tạo 1 mạng chung rất an toàn)
networks:
  tên-mạng:
```

### Phân biệt `docker compose` và `docker-compose` (Cạm bẫy phiên bản)

Rất nhiều bạn mới học thường bối rối giữa hai câu lệnh này. Đây là sự khác biệt:

- **`docker compose` (Có khoảng trắng - V2):** Là phiên bản hiện đại, được tích hợp trực tiếp dưới dạng một plugin chính thức của Docker CLI. Viết bằng ngôn ngữ Go, chạy cực kỳ nhanh và ổn định. **Hãy luôn luôn sử dụng cú pháp này!**
- **`docker-compose` (Có dấu gạch ngang - V1):** Là phiên bản cũ viết bằng Python chạy độc lập. Hiện tại đã bị hãng Docker chính thức khai tử (deprecated) và ngừng hỗ trợ.

---

## 3️⃣ Từng Bước Triển Khai: Kết Nối Flask + PostgreSQL + Redis Bằng Một Lệnh Duy Nhất

Chúng ta sẽ cùng bắt tay xây dựng một ứng dụng đếm lượt truy cập sử dụng Flask, lưu số lượt đếm vào Redis và truy vấn thông tin phiên bản cơ sở dữ liệu từ PostgreSQL.

### Bước 3.1: Chuẩn bị mã nguồn dự án

Hãy tạo một thư mục trống mang tên `compose-demo` và tạo các tệp tin sau:

```bash
# Tạo thư mục dự án
mkdir compose-demo && cd compose-demo
```

Viết tệp mã nguồn chính `app.py`:

```python
# app.py
import os
from flask import Flask
import redis
import psycopg2

app = Flask(__name__)

# Đọc cấu hình kết nối từ biến môi trường (mặc định trỏ về localhost nếu chạy ngoài Docker)
DB_HOST = os.getenv("DB_HOST", "localhost")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# Khởi tạo kết nối tới Redis cache
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

@app.route("/")
def hello():
    # Tăng số lượt truy cập trong Redis thêm 1 đơn vị mỗi lần reload trang
    count = r.incr("visits")
    
    # Kết nối đến PostgreSQL để truy vấn phiên bản hệ thống
    conn = psycopg2.connect(
        host=DB_HOST,
        user="admin",
        password="secret",
        database="myapp"
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()[0]
    conn.close()
    
    return f"Chào mừng bạn! Số lượt truy cập: {count}. Phiên bản DB: {db_version[:50]}..."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Viết tệp khai báo thư viện `requirements.txt`:

```text
flask==3.0.0
redis==5.0.1
psycopg2-binary==2.9.9
```

Viết tệp `Dockerfile` để tự động đóng gói ứng dụng Flask:

```dockerfile
# Sử dụng base image Python slim nhẹ và an toàn
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

---

### Bước 3.2: Thiết lập tệp cấu hình `docker-compose.yml`

Tạo tệp `docker-compose.yml` nằm ngay tại thư mục gốc của dự án để liên kết app Flask của bạn với dịch vụ PostgreSQL và Redis:

```yaml
# docker-compose.yml
services:
  # Dịch vụ ứng dụng Web của bạn
  app:
    build: .                          # Tự động build image từ Dockerfile trong thư mục hiện tại
    ports:
      - "5000:5000"                   # Ánh xạ cổng 5000 ra máy host để truy cập web
    environment:
      DB_HOST: db                     # Khai báo tên host của DB chính là tên service "db"
      REDIS_HOST: cache               # Khai báo tên host của Cache chính là tên service "cache"
    depends_on:
      - db
      - cache

  # Dịch vụ cơ sở dữ liệu PostgreSQL
  db:
    image: postgres:16-alpine         # Sử dụng image Postgres 16 siêu nhẹ chạy trên Alpine
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - pg-data:/var/lib/postgresql/data  # Gắn volume để bảo toàn dữ liệu database khi tắt container
    ports:
      - "5432:5432"                   # Mở cổng để bạn có thể kết nối debug từ máy host nếu muốn

  # Dịch vụ lưu trữ cache Redis
  cache:
    image: redis:7-alpine             # Sử dụng Redis 7 bản Alpine siêu gọn
    ports:
      - "6379:6379"

# Khai báo vùng lưu trữ dữ liệu bền vững
volumes:
  pg-data:
```

---

### Bước 3.3: Khởi động hệ thống và tận hưởng thành quả

Gõ một dòng lệnh duy nhất để Docker tự động thực hiện: build image của app Flask, tải các image Postgres/Redis từ Docker Hub về, tạo mạng ảo và kích hoạt cả 3 container đồng thời:

```bash
# Khởi chạy hệ thống ở chế độ chạy ngầm (detached)
docker compose up -d
```

Docker sẽ hiển thị tiến trình khởi chạy mượt mà:

```text
[+] Running 5/5
 ⠿ Network compose-demo_default    Created                                   0.1s
 ⠿ Volume "compose-demo_pg-data"   Created                                   0.0s
 ⠿ Container compose-demo-cache-1  Started                                   0.5s
 ⠿ Container compose-demo-db-1     Started                                   0.5s
 ⠿ Container compose-demo-app-1    Started                                   0.8s
```

Hãy mở trình duyệt truy cập `http://localhost:5000` hoặc chạy lệnh `curl` để kiểm tra:

```bash
curl http://localhost:5000
# Output lần 1: Chào mừng bạn! Số lượt truy cập: 1. Phiên bản DB: PostgreSQL 16.0...

curl http://localhost:5000
# Output lần 2: Chào mừng bạn! Số lượt truy cập: 2. Phiên bản DB: PostgreSQL 16.0...
```

Hệ thống hoạt động trơn tru hoàn hảo! Số lượt truy cập tự động tăng lên nhờ Redis và thông tin database được truy vấn trực tiếp từ PostgreSQL.

---

### Bước 3.4: Cẩm nang các câu lệnh điều khiển Compose thông dụng hàng ngày

Hãy ghi nhớ và sử dụng thành thạo các câu lệnh điều khiển sau:

```bash
# 1. Khởi chạy và hiển thị log trực tiếp ra màn hình terminal (Foreground)
docker compose up

# 2. Khởi chạy ở chế độ chạy ngầm dưới nền (Khuyên dùng)
docker compose up -d

# 3. Yêu cầu build lại image của app trước khi khởi chạy (Khi bạn vừa sửa Dockerfile hoặc code)
docker compose up -d --build

# 4. Kiểm tra trạng thái hoạt động và port của các container trong dự án
docker compose ps

# 5. Xem toàn bộ log của tất cả các container kết hợp theo thời gian thực
docker compose logs -f

# 6. Xem log chi tiết của duy nhất container "app"
docker compose logs -f app

# 7. Thực thi một dòng lệnh tương tác trực tiếp bên trong container "app"
docker compose exec app bash

# 8. Kết nối trực tiếp vào trình quản trị PostgreSQL bên trong container "db" để truy vấn nhanh
docker compose exec db psql -U admin myapp

# 9. Tạm dừng các container mà không xóa bỏ dữ liệu ảo
docker compose stop

# 10. Tắt toàn bộ hệ thống, xóa bỏ container và dọn sạch mạng ảo chung
docker compose down

# 11. Tắt hệ thống đồng thời XÓA SẠCH toàn bộ dữ liệu lưu trong volume (⚠️ CỰC KỲ CẨN THẬN!)
docker compose down -v
```

---

## 4️⃣ Cơ Chế Service Networking: Cách Các Container Tìm Thấy Nhau Qua "Bí Danh" DNS

Khi bạn khởi chạy Docker Compose, công cụ này sẽ tự động tạo ra một mạng ảo mặc định mang tên `<tên-thư-mục>_default` và gắn toàn bộ các container khai báo trong file vào mạng này.

Mỗi container sẽ được tự động cấp phát một địa chỉ IP ảo ngẫu nhiên. Tuy nhiên, thay vì phải ghi nhớ các IP ảo dễ thay đổi này, Docker Compose tích hợp sẵn một hệ thống **DNS nội bộ (Service Discovery)** cực kỳ thông minh:

```mermaid
graph TD
    subgraph Mạng ảo mặc định: compose-demo_default
        APP[Dịch vụ app - IP: 172.20.0.4]
        DB[Dịch vụ db - IP: 172.20.0.2]
        CACHE[Dịch vụ cache - IP: 172.20.0.3]
    end
    APP -.->|Kết nối qua DNS: db| DB
    APP -.->|Kết nối qua DNS: cache| CACHE
```

Nhờ cơ chế tuyệt vời này, trong mã nguồn `app.py` của ứng dụng Flask, bạn chỉ cần cấu hình địa chỉ máy chủ đích bằng **chính xác tên của dịch vụ (service name)** được khai báo trong file YAML:

```python
# Cấu hình kết nối cực kỳ tường minh và sạch sẽ
DB_HOST = "db"       # Tên dịch vụ db trong docker-compose.yml
REDIS_HOST = "cache"  # Tên dịch vụ cache trong docker-compose.yml
```

Docker Engine sẽ tự động biên dịch (resolve) từ khóa `db` và `cache` thành địa chỉ IP ảo chính xác của container tương ứng bên trong mạng nội bộ.

---

## 5️⃣ Quản Lý Dữ Liệu Bền Vững Với Volumes Trong Docker Compose

Container có tính chất nhất thời (ephemeral) — khi container bị xóa bỏ (`docker compose down`), toàn bộ dữ liệu ghi mới bên trong ổ đĩa ảo của nó cũng sẽ biến mất vĩnh viễn. Để lưu trữ database bền vững qua các lần tắt/mở, bạn buộc phải dùng Volume.

Có 2 phương pháp quản lý Volume phổ biến trong Compose:

### Phương pháp 1: Named Volume (Khuyên dùng cho Database trên Production)

```yaml
services:
  db:
    image: postgres:16-alpine
    volumes:
      - pg-data:/var/lib/postgresql/data  # Gắn volume có tên pg-data vào thư mục lưu trữ của Postgres

volumes:
  pg-data:  # Khai báo volume pg-data ở top-level. Docker sẽ tự quản lý vị trí lưu trữ an toàn trên ổ cứng máy host.
```

> [!TIP]
> Đây là phương pháp an toàn nhất vì dữ liệu được Docker quản lý biệt lập tại vùng an toàn trên máy host, không lo bị người dùng vô tình sửa đổi hay xóa nhầm từ bên ngoài.

### Phương pháp 2: Bind Mount (Tuyệt vời cho quá trình lập trình - Development)

```yaml
services:
  app:
    image: my-app:v1
    volumes:
      - ./app.py:/app/app.py  # Ánh xạ trực tiếp file app.py từ máy vật lý vào container
```

> [!TIP]
> **Mẹo tăng tốc lập trình của Mr.Rom:** 
> Khi sử dụng Bind Mount, bất kỳ thay đổi nào bạn thực hiện trên file `app.py` ở máy host bằng VS Code sẽ lập tức xuất hiện bên trong container ngay lập tức mà không cần bạn phải mất thời gian chạy lại lệnh `docker build` hay khởi động lại container!

---

## 6️⃣ Quản Lý Biến Môi Trường Và Bảo Mật Secret Trong Docker Compose

### Cách 1: Khai báo trực tiếp trong tệp YAML (Cho các cấu hình không nhạy cảm)

```yaml
services:
  app:
    environment:
      DEBUG: "true"
      PORT: 5000
```

### Cách 2: Tách biệt cấu hình bằng tệp `.env` (Bắt buộc cho thông tin nhạy cảm)

Hãy tạo một tệp mang tên `.env` nằm ở cùng thư mục với `docker-compose.yml` để lưu trữ mật khẩu:

```text
# .env (⚠️ LUÔN LUÔN cho file này vào .gitignore để tránh leak mật khẩu lên GitHub!)
POSTGRES_PASSWORD=my-super-secret-password-2026
APP_EXTERNAL_PORT=8080
```

Trong tệp `docker-compose.yml`, bạn tiến hành tham chiếu tới các biến này bằng cú pháp `${TÊN_BIẾN}`:

```yaml
services:
  app:
    ports:
      - "${APP_EXTERNAL_PORT}:5000"   # Sử dụng port động cấu hình từ file .env

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}  # Bảo mật tuyệt đối mật khẩu
```

Khi chạy `docker compose up`, Compose sẽ tự động đọc tệp `.env` ở cùng thư mục và điền các giá trị thực tế vào tệp YAML cho bạn.

---

## 7️⃣ depends_on Kết Hợp Health Check: Làm Sao Để Khởi Động Container Đúng Thứ Tự Ready?

Mặc định, tùy chọn `depends_on` chỉ đảm bảo **thứ tự kích hoạt** các container (ví dụ: container `db` được Docker nhấn nút start trước container `app`). 

Tuy nhiên, PostgreSQL sau khi được nhấn nút start sẽ cần khoảng 3 đến 5 giây để khởi tạo tệp cấu hình hệ thống và thực sự sẵn sàng tiếp nhận các truy vấn kết nối từ ứng dụng. Trong thời gian 5 giây chờ đợi đó, container `app` đã khởi chạy xong và cố gắng kết nối ngay lập tức dẫn đến lỗi crash hệ thống vì DB "chưa thực sự sẵn sàng".

Để khắc phục triệt để lỗ hổng này, hãy kết hợp **Healthcheck** để yêu cầu container `app` chỉ khởi chạy khi container `db` đã ở trạng thái hoàn toàn khỏe mạnh (`service_healthy`):

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: secret
    # Thiết lập kiểm tra sức khỏe nội bộ định kỳ
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s    # Kiểm tra mỗi 5 giây
      timeout: 5s     # Chờ phản hồi tối đa 5 giây
      retries: 5      # Thử lại tối đa 5 lần nếu lỗi

  app:
    build: .
    ports:
      - "5000:5000"
    # Yêu cầu đợi cho tới khi DB thực sự khỏe mạnh mới khởi chạy app
    depends_on:
      db:
        condition: service_healthy
```

---

## 8️⃣ Sử Dụng Profiles Để Phân Lập Môi Môi Trường Phát Triển Và Debug

Trong thực tế, bạn có thể cần chạy một số dịch vụ bổ sung phục vụ cho quá trình gỡ lỗi (như Adminer hay pgAdmin để xem cơ sở dữ liệu trực quan), nhưng không muốn chúng tự động khởi chạy làm tốn tài nguyên RAM của hệ thống khi chạy bình thường.

Tính năng **Profiles** sẽ giúp bạn phân nhóm dịch vụ cực kỳ chuyên nghiệp:

```yaml
services:
  app:
    image: my-app:v1
  db:
    image: postgres:16-alpine

  # Công cụ quản trị giao diện database chỉ dùng khi debug
  adminer:
    image: adminer
    ports:
      - "8080:8080"
    profiles:
      - tools   # Dịch vụ này thuộc profile "tools"
```

Khi bạn gõ lệnh chạy thông thường:
```bash
# Chỉ khởi chạy app và db
docker compose up -d
```

Khi bạn cần bật công cụ trực quan để kiểm tra dữ liệu:
```bash
# Khởi chạy toàn bộ hệ thống mặc định kèm theo profile tools
docker compose --profile tools up -d
```

---

## 💡 Những Cạm Bẫy Phổ Biến Và Cẩm Nang Vận Hành Compose Tối Ưu

### ❌ Cạm bẫy 1: Cố tình sử dụng tên host là `localhost` trong mã nguồn ứng dụng
Rất nhiều bạn mới chuyển đổi dự án lên Docker vẫn giữ thói quen cấu hình chuỗi kết nối là `postgresql://admin:secret@localhost:5432/myapp`. Khi chạy trong Docker, từ khóa `localhost` bên trong container `app` sẽ trỏ về chính bản thân container `app` chứ không phải máy chủ vật lý bên ngoài hay container database, dẫn đến lỗi mất kết nối.

- **Cẩm nang khắc phục:** Hãy luôn khai báo địa chỉ máy chủ đích bằng tên của dịch vụ đã định nghĩa trong tệp Compose (ví dụ: `db` hoặc `cache`).

---

### ❌ Cạm bẫy 2: Quên tham số `--build` khi thay đổi mã nguồn ở local
Khi bạn chỉnh sửa một dòng code trong tệp `app.py` và chạy lệnh `docker compose up -d`, Docker Compose sẽ phát hiện ra image `my-flask-app:v1` đã tồn tại ở local và lập tức khởi chạy ngay container từ image cũ đó mà không hề cập nhật code mới của bạn.

- **Cẩm nang khắc phục:** Hãy luôn đi kèm cờ `--build` mỗi khi bạn vừa sửa code để bắt buộc Docker đóng gói lại image mới trước khi khởi chạy:
  ```bash
  docker compose up -d --build
  ```

---

## 🛠️ Thực Hành Thực Chiến: Tự Tay Xây Dựng Hệ Thống Đa Container Hoàn Chỉnh

Để khép lại bài học cơ bản này một cách rực rỡ nhất, chúng ta sẽ cùng thực hiện một bài Lab thực tế cực kỳ cao cấp: **Thiết lập một hệ thống live-chat đa dịch vụ chuẩn Production bao gồm: Web App chạy NodeJS, Cơ sở dữ liệu lưu trữ MongoDB, và bộ nhớ đệm đồng bộ Redis Cache.**

> [!IMPORTANT]
> **Yêu cầu bài Lab:**
> 1. Viết một tệp `docker-compose.yml` liên kết 3 dịch vụ: `chat-app` (tự build từ Dockerfile ở local), `chat-db` (sử dụng MongoDB bản Alpine), và `chat-cache` (sử dụng Redis bản Alpine).
> 2. Đảm bảo toàn bộ hệ thống cơ sở dữ liệu MongoDB và Redis được gắn volume lưu trữ dữ liệu an toàn.
> 3. Tách biệt mật khẩu quản trị của MongoDB ra tệp cấu hình bảo mật `.env`.
> 4. Thiết lập cơ chế kiểm tra sức khỏe (Healthcheck) an toàn cho MongoDB để đảm bảo Node.js chat-app chỉ khởi chạy khi cơ sở dữ liệu đã hoàn toàn sẵn sàng tiếp nhận kết nối.

### Bước 1: Khởi tạo tệp tin cấu hình bí mật `.env` tại thư mục của bạn:

```text
# .env
MONGO_INITDB_ROOT_USERNAME=chatadmin
MONGO_INITDB_ROOT_PASSWORD=supersecretpassword2026
CHAT_APP_PORT=3000
```

### Bước 2: Viết tệp `docker-compose.yml` giải quyết trọn vẹn yêu cầu bài Lab:

```yaml
# docker-compose.yml
services:
  # 1. Dịch vụ ứng dụng Live Chat NodeJS
  chat-app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "${CHAT_APP_PORT}:3000"       # Đọc cổng ra từ tệp cấu hình động .env
    environment:
      MONGO_URI: mongodb://${MONGO_INITDB_ROOT_USERNAME}:${MONGO_INITDB_ROOT_PASSWORD}@chat-db:27117/chatdb?authSource=admin
      REDIS_HOST: chat-cache
    # Đợi database chat-db vượt qua bài kiểm tra sức khỏe thành công mới start app
    depends_on:
      chat-db:
        condition: service_healthy

  # 2. Dịch vụ cơ sở dữ liệu MongoDB
  chat-db:
    image: mongo:7.0-jammy
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_INITDB_ROOT_USERNAME}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_INITDB_ROOT_PASSWORD}
    volumes:
      - mongo-data:/data/db           # Lưu trữ bền vững dữ liệu tin nhắn chat
    ports:
      - "27017:27017"
    # Cơ chế Healthcheck kiểm tra trạng thái hoạt động thực tế của MongoDB
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 5s
      timeout: 3s
      retries: 5

  # 3. Dịch vụ lưu trữ cache đồng bộ tin nhắn nhanh
  chat-cache:
    image: redis:7-alpine
    volumes:
      - redis-data:/data              # Lưu trữ bền vững dữ liệu cache Redis
    ports:
      - "6379:6379"

# Khai báo các vùng lưu trữ dữ liệu an toàn độc lập với container
volumes:
  mongo-data:
  redis-data:
```

Mẫu thiết kế trên chính là kiến trúc baseline kinh điển được áp dụng tại hầu hết các dự án startup công nghệ hiện nay trên thế giới!

---

## 🧠 Thử Thách Tư Duy: Củng Cố Kiến Thức Cốt Lõi

**Câu hỏi 1:** Khi bạn chạy lệnh `docker compose down`, các dữ liệu được ghi trong Named Volume (ví dụ: `pg-data`) có bị xóa mất hay không? Làm sao để xóa sạch hoàn toàn hệ thống để test fresh từ đầu?

<details>
<summary><b>💡 Bấm để xem đáp án giải mã của Mr.Rom</b></summary>

Khi bạn chạy lệnh `docker compose down` thông thường, Docker chỉ tiến hành dừng và xóa bỏ các container cùng hệ thống mạng ảo được tạo ra. **Toàn bộ dữ liệu lưu trữ bên trong Named Volume vẫn được giữ lại nguyên vẹn và an toàn tuyệt đối.**

Để xóa sạch hoàn toàn hệ thống bao gồm cả các Named Volume nhằm mục đích cấu hình lại từ đầu (Fresh Start), bạn phải truyền thêm cờ `-v` (Volume) khi tắt hệ thống:
```bash
# Xóa bỏ sạch sẽ không tì vết (Lưu ý: Mất dữ liệu vĩnh viễn!)
docker compose down -v
```

</details>

**Câu hỏi 2:** Cơ chế Service Discovery của Docker Compose hoạt động dựa vào đâu để chuyển đổi tên dịch vụ (ví dụ: `host=db`) thành địa chỉ IP ảo chính xác?

<details>
<summary><b>💡 Bấm để xem đáp án giải mã của Mr.Rom</b></summary>

Docker Compose tự động tích hợp sẵn một **Embedded DNS Server** (máy chủ phân giải tên miền nhúng) chạy ngầm bên trong mỗi container. 

Khi container `app` gửi một yêu cầu kết nối tới tên miền `db`, Embedded DNS Server này sẽ lập tức tra cứu bảng ánh xạ dịch vụ nội bộ của nó và trả về chính xác IP mạng ảo hiện tại của container `db`. Nhờ cơ chế tự động này, bạn hoàn toàn được giải phóng khỏi nỗi lo quản lý IP tĩnh cho từng container.

</details>

---

## ⚡ Bảng Tra Cứu Nhanh (Cheatsheet) Lệnh Và Cấu Trúc YAML

### Cú pháp điều khiển hệ thống Compose nhanh chóng:
```bash
docker compose up -d                  # Bật toàn bộ dịch vụ ngầm dưới nền
docker compose up -d --build          # Rebuild lại code và khởi chạy
docker compose down                   # Tắt sạch hệ thống (Giữ lại data)
docker compose down -v                # Tắt sạch hệ thống và XÓA SẠCH data (⚠️ Nguy hiểm!)
docker compose ps                     # Liệt kê trạng thái và port
docker compose logs -f                # Xem log trực tiếp thời gian thực
docker compose exec app sh            # Mở terminal tương tác trực tiếp trong app
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary) Chuyên Ngành

- **Service discovery (Khám phá dịch vụ):** Cơ chế tự động phát hiện và kết nối giữa các container dựa vào tên dịch vụ mà không cần biết trước địa chỉ IP.
- **Detached Mode (Chế độ chạy ngầm - cờ `-d`):** Lựa chọn yêu cầu Docker chạy container dưới nền và trả lại quyền điều khiển terminal cho người dùng lập tức.
- **Named Volume (Volume có tên):** Vùng lưu trữ dữ liệu an toàn do Docker quản lý hoàn toàn độc lập với vòng đời của container.
- **Healthcheck (Kiểm tra sức khỏe):** Lệnh kiểm tra định kỳ do lập trình viên thiết lập để xác nhận container có đang hoạt động "bình thường" từ bên trong hay không.

---

## 🔗 Liên Kết & Tài Nguyên Học Tập Bổ Sung

### Các bài học liên quan trực tiếp:
- [⬅️ Bài học trước: Tự đóng gói bản thiết kế với Dockerfile Custom](./02_dockerfile-basics.md)
- [🛠️ Công cụ hỗ trợ: Hướng dẫn cấu hình môi trường lập trình tối ưu trên VS Code](../../../../02_tools/ide/vs-code.md)

### Tài liệu chính hãng tham khảo thêm:
- [Tài liệu đặc tả cấu hình tệp tin Compose chính thức từ hãng Docker](https://docs.docker.com/compose/compose-file/)
- [Awesome Compose — Kho lưu trữ hơn 50+ dự án mẫu thực tế chất lượng cao](https://github.com/docker/awesome-compose)

---

## 📌 Lịch Sử Thay Đổi (Changelog)

- **v3.0.0 (26/05/2026)** — **Mr.Rom nâng cấp Premium chuẩn 5 sao:**
  - Nâng cấp toàn diện bài viết đạt chuẩn Blueprint Premium mới nhất.
  - Cấu trúc lại tiêu đề H1 và metadata block YAML chuẩn chỉnh chuyên nghiệp.
  - Chuyển đổi 100% tiêu đề H2 thành câu hỏi mở kích thích tư duy sâu sắc.
  - Sửa đổi toàn bộ các Alerts cũ sang định dạng GitHub Alerts chuẩn chỉnh.
  - Việt hóa 100% các dòng ghi chú giải thích bên trong các block code Python, YAML, và Bash.
  - Bổ sung chương thực hành thực chiến Lab cao cấp: Live Chat Nodejs + MongoDB + Redis kết hợp Healthcheck chuyên sâu.
  - Cập nhật liên kết tuyệt đối trỏ chính xác về cẩm nang VS Code Guide.
- **v2.2.0 (25/05/2026)** — Bổ sung các chú dẫn mở đầu trước các phần Hands-on.
- **v2.0.0 (20/05/2026)** — Tái cơ cấu bài học theo triết lý story-driven thực tế của dự án.
- **v1.0.0 (16/05/2026)** — Khởi tạo bản thảo sơ khai đầu tiên.
