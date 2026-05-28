# Quiz: Module 05 - DOCKER BASICS

> **25 Câu Trắc Nghiệm Kiểm Tra Kiến Thức Docker**

**Thời gian:** 30 phút  
**Đạt:** 18/25 (72%)

---

## 📝 CÂU HỎI

**Câu 1:** Sự khác biệt chính giữa container và VM?

- A) Không khác
- B) Container chia sẻ OS kernel, VM có full OS riêng
- C) Container chậm hơn
- D) VM portable hơn

**Câu 2:** Lệnh nào hiển thị containers đang chạy?

- A) `docker ls`
- B) `docker ps`
- C) `docker list`
- D) `docker show`

**Câu 3:** Flag `-d` trong `docker run -d` có nghĩa gì?

- A) Debug mode
- B) Detached mode (background)
- C) Delete sau khi stop
- D) Development mode

**Câu 4:** Map port 8080 trên host sang port 80 trong container?

- A) `-p 80:8080`
- B) `-p 8080:80`
- C) `--port 8080-80`
- D) `-port 80->8080`

**Câu 5:** Dockerfile instruction nào set base image?

- A) BASE
- B) FROM
- C) IMAGE
- D) USING

**Câu 6:** Mục đích của WORKDIR trong Dockerfile?

- A) Set working directory cho các instructions sau
- B) Chỉ định nơi save image
- C) Define network directory
- D) Set log directory

**Câu 7:** Cách nào hiệu quả hơn trong Dockerfile?

- A) `RUN apt-get update` rồi `RUN apt-get install`
- B) `RUN apt-get update && apt-get install`
- C) Cả hai như nhau
- D) Dùng INSTALL command

**Câu 8:** `docker-compose down -v` làm gì?

- A) Chỉ stop services
- B) Stop và remove containers
- C) Stop, remove containers VÀ volumes
- D) Validate configuration

**Câu 9:** Base image nào nhỏ nhất?

- A) ubuntu:latest
- B) debian:latest
- C) alpine:latest
- D) centos:latest

**Câu 10:** Mục đích của .dockerignore?

- A) Ignore Docker errors
- B) Loại files khỏi build context
- C) Ignore container logs
- D) Skip layers trong build

**Câu 11:** Persist data trong Docker bằng cách nào?

- A) Đừng stop container
- B) Sử dụng volumes
- C) Backup container
- D) Dùng image lớn hơn

**Câu 12:** Multi-stage build, copy từ stage trước?

- A) `COPY --stage`
- B) `COPY --from=stagename`
- C) `COPY --previous`
- D) `GET FROM stage`

**Câu 13:** Restart policy nào restart container trừ khi manually stopped?

- A) `--restart=always`
- B) `--restart=unless-stopped`
- C) `--restart=on-failure`
- D) `--restart=no`

**Câu 14:** Chạy command trong running container?

- A) `docker run`
- B) `docker exec`
- C) `docker cmd`
- D) `docker execute`

**Câu 15:** Default Docker network driver?

- A) host
- B) bridge
- C) overlay
- D) macvlan

**Câu 16:** Xóa tất cả stopped containers?

- A) `docker rm -a`
- B) `docker container prune`
- C) `docker clean`
- D) `docker remove --all`

**Câu 17:** EXPOSE trong Dockerfile làm gì?

- A) Mở port trên host
- B) Document port app sử dụng
- C) Tạo firewall rule
- D) Map port tự động

**Câu 18:** Best practice cho secrets trong Docker?

- A) Hardcode trong Dockerfile
- B) Copy .env file
- C) Dùng environment variables
- D) Đặt trong image tags

**Câu 19:** Chạy container với non-root user:

- A) `RUN useradd` rồi `USER username`
- B) `--user` flag trong docker run
- C) Cả A và B
- D) Không thể trong Docker

**Câu 20:** Xem resource usage của containers?

- A) `docker usage`
- B) `docker stats`
- C) `docker resources`
- D) `docker monitor`

**Câu 21:** Trong docker-compose, `depends_on` làm gì?

- A) Set startup order
- B) Tạo dependencies
- C) Chia sẻ volumes
- D) Link networks

**Câu 22:** Healthcheck trong Dockerfile là gì?

- A) Check image valid
- B) Command test container healthy
- C) Scan malware
- D) Validate dependencies

**Câu 23:** Cái nào tốt hơn cho production?

- A) `python:latest`
- B) `python:3.9`
- C) `python:3.9.1-slim`
- D) `python`

**Câu 24:** Xem container logs:

- A) `docker log container_name`
- B) `docker logs container_name`
- C) `docker view-logs container_name`
- D) `docker cat container_name`

**Câu 25:** Multi-stage builds giúp gì?

- A) Build nhanh hơn
- B) Image nhỏ hơn
- C) Nhiều layers hơn
- D) Màu đẹp hơn

---

## 📊 ĐÁP ÁN

**Xem SOLUTIONS.md để có đáp án chi tiết!**

---

## 🎯 THANG ĐIỂM

- **23-25 (92%+):** Docker Expert! ⭐⭐⭐
- **20-22 (80-91%):** Docker Proficient ⭐⭐
- **18-19 (72-79%):** Docker Competent ⭐
- **<18 (<72%):** Cần review lại materials
