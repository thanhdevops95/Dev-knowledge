# Exercises: Module 05 - DOCKER BASICS

> **Bài tập kiểm tra kiến thức Docker**

**Tổng điểm:** 200  
**Thời gian:** 90 phút  
**Đạt:** 140/200 (70%)

---

## PHẦN A: TRẮC NGHIỆM (40 điểm)

**Hướng dẫn:** Chọn đáp án đúng nhất. 2 điểm mỗi câu.

**Câu 1:** Docker container khác virtual machine như thế nào?

- A) Không khác gì
- B) Container chia sẻ kernel của host OS, VM có OS riêng
- C) Container chậm hơn VM
- D) VM portable hơn container

**Câu 2:** Lệnh nào tạo container mới?

- A) `docker create`
- B) `docker run`
- C) `docker start`
- D) Cả A và B đều đúng

**Câu 3:** Image và container khác nhau như thế nào?

- A) Không khác
- B) Image là template, container là instance đang chạy
- C) Container là template, image là instance
- D) Image chỉ cho Windows

**Câu 4:** Dockerfile instruction nào set base image?

- A) BASE
- B) IMAGE
- C) FROM
- D) TEMPLATE

**Câu 5:** `docker ps` hiển thị gì?

- A) Tất cả containers
- B) Chỉ containers đang chạy
- C) Docker images
- D) Docker volumes

**Câu 6:** Flag nào chạy container ở background?

- A) `-b`
- B) `-d`
- C) `--background`
- D) `-bg`

**Câu 7:** Expose port 8080 trên host tới port 80 trong container?

- A) `-p 80:8080`
- B) `-p 8080:80`
- C) `--port 8080:80`
- D) `-e 8080:80`

**Câu 8:** `docker-compose up -d` làm gì?

- A) Chạy foreground
- B) Chạy background (detached)
- C) Stop containers
- D) Remove containers

**Câu 9:** Dockerfile instruction copy files?

- A) `MOVE source dest`
- B) `COPY source dest`
- C) `ADD source dest`
- D) Cả B và C

**Câu 10:** Mục đích của `.dockerignore`?

- A) Ignore errors
- B) Loại files khỏi build context
- C) Ignore outdated images
- D) Skip validation

**Câu 11:** Xóa tất cả stopped containers?

- A) `docker rm -all`
- B) `docker container prune`
- C) `docker clean`
- D) `docker remove --stopped`

**Câu 12:** Volume dùng để làm gì?

- A) Tăng âm lượng
- B) Persist data ngoài container lifecycle
- C) Tăng size container
- D) Quản lý network

**Câu 13:** Multi-stage build, copy từ stage trước?

- A) `COPY --from=stage`
- B) `MOVE --stage`
- C) `GET --previous`
- D) `TRANSFER`

**Câu 14:** Base image nào nhỏ nhất?

- A) ubuntu
- B) debian
- C) alpine
- D) centos

**Câu 15:** `--restart=always` làm gì?

- A) Restart khi lỗi
- B) Restart khi Docker daemon start
- C) Không restart
- D) Restart mỗi ngày

**Câu 16-20:** [Thêm 5 câu về networking, compose, security...]

---

## PHẦN B: ĐIỀN VÀO CHỖ TRỐNG (30 điểm)

**Hướng dẫn:** Hoàn thành lệnh. 2 điểm mỗi câu.

**Câu 21:** List tất cả containers kể cả stopped:

```bash
docker ps ____
```

**Câu 22:** Chạy Ubuntu container interactive:

```bash
docker run ____ ubuntu bash
```

**Câu 23:** Build image tagged 'myapp:1.0':

```bash
docker build ____ myapp:1.0 .
```

**Câu 24:** Xóa container forcefully:

```bash
docker rm ____ container_name
```

**Câu 25:** Xem 100 dòng cuối logs:

```bash
docker logs ____ 100 container_name
```

**Câu 26:** Execute bash trong running container:

```bash
docker ____ -it container_name bash
```

**Câu 27:** Start tất cả services với compose:

```bash
docker-compose ____
```

**Câu 28:** Tạo Docker volume:

```bash
docker volume ____ mydata
```

**Câu 29:** Mount volume vào container:

```bash
docker run -v ____:/app/data myapp
```

**Câu 30:** Stop tất cả running containers:

```bash
docker stop ____(docker ps -q)
```

**Câu 31-35:** [Thêm 5 câu về pull, inspect, tag, push, network...]

---

## PHẦN C: VIẾT DOCKERFILE (60 điểm)

**Hướng dẫn:** Viết Dockerfile hoàn chỉnh. 10 điểm mỗi câu.

**Câu 36:** Simple Python App

- Base: python:3.9-slim
- Working directory: /app
- Copy requirements.txt và install
- Copy app.py
- Run: python app.py

**Câu 37:** Multi-stage Node.js Build

- Stage 1: Build với node:16
- Stage 2: Production với node:16-alpine
- Expose 3000

**Câu 38:** Non-root User

- Base nginx:alpine
- Tạo user 'appuser'
- Chạy với appuser

**Câu 39:** With Health Check

- Flask app
- Health check /health endpoint
- Interval 30s, timeout 3s

**Câu 40:** Optimized Layers

- Combine RUN commands
- No cache cho pip
- Minimal layers

**Câu 41:** With Build Arguments

- ARG cho version
- ENV cho runtime
- Default values

---

## PHẦN D: DEBUG SCENARIOS (70 điểm)

**Hướng dẫn:** Phân tích và sửa lỗi. 10 điểm mỗi câu.

**Câu 42:** Container Won't Start

```bash
docker run myapp
# Container exits immediately
```

**Tasks:** Check logs, exit code, fix issue

**Câu 43:** Network Connectivity

```bash
# Web container không connect được db
docker logs web
# Error: Can't connect to database
```

**Tasks:** Check network, verify names, fix

**Câu 44:** Volume Permissions

```bash
docker run -v ./data:/app/data myapp
# Permission denied
```

**Tasks:** Check ownership, fix permissions

**Câu 45:** Image Size Too Large

```bash
docker images myapp
# Size: 1.2GB (should be ~200MB)
```

**Tasks:** Identify bloat, optimize, multi-stage

**Câu 46:** Port Not Accessible

```bash
docker run -d -p 8080:80 nginx
curl http://localhost:8080
# Connection refused
```

**Tasks:** Check container, port mapping, firewall

**Câu 47:** Compose Services Won't Communicate

```yaml
services:
  web:
    build: .
  database:
    image: postgres
# Web can't connect to database
```

**Tasks:** Add network, fix service names

**Câu 48:** Slow Build Times

```bash
docker build -t myapp .
# Takes 10 minutes every time
```

**Tasks:** Identify cache-busting, reorder Dockerfile

---

## 📊 THANG ĐIỂM

- **180-200:** Expert ⭐⭐⭐
- **160-179:** Proficient ⭐⭐
- **140-159:** Competent ⭐
- **<140:** Cần review lại

**Xem SOLUTIONS.md để check đáp án!**
