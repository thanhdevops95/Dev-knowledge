# 🐳 Docker — Images & Containers — Bài Tập Thực Hành

---

## 📋 Metadata

- **Parent Lesson:** [../lesson.md](../lesson.md)
- **Type:** `[Exercise]`
- **Difficulty:** `[Easy-Medium]`
- **Estimated Time:** 45 phút
- **Prerequisites:** [Lesson 01](../01-Installation-Setup/lesson.md)

---

## 🎯 Mục Tiêu

Luyện tập làm việc với Docker images và containers một cách thành thạo.

---

## 📝 Bài Tập

### Bài 1: Image Operations

**Tasks:**
1. Pull image `alpine:3.18` (specify version)
   ```bash
   docker pull alpine:3.18
   ```
2. List images: `docker images`. Ghi ra:
   - alpine:3.18 — REPOSITORY: ___, TAG: ___, IMAGE ID: ___, SIZE: ___
3. Pull `ubuntu:22.04` và `node:18-alpine`
4. Tìm image `alpine` có size nhỏ nhất trong list của bạn: _______

---

### Bài 2: Container Lifecycle

**Tasks:**
1. Run container `alpine:3.18` với command `sleep 3600` (background):
   ```bash
   docker run -d --name sleeper alpine:3.18 sleep 3600
   ```
2. List running containers: `docker ps`. Container ID của `sleeper`: ___
3. Exec vào container và kiểm tra:
   ```bash
   docker exec -it sleeper /bin/sh
   # Trong container:
   ps aux
   exit
   ```
4. Stop container: `docker stop sleeper`
5. Start lại: `docker start sleeper`
6. Check logs: `docker logs sleeper` (không có output vì sleep không log)
7. Remove container: `docker rm -f sleeper` (`-f` force nếu đang chạy)

---

### Bài 3: Port Mapping & Access

**Tasks:**
1. Run Nginx container:
   ```bash
   docker run -d --name web-nginx -p 8081:80 nginx:latest
   ```
2. Verify running: `docker ps`. Port mapping: ____
3. Test: Mở browser → `http://localhost:8081`. Bạn thấy gì? ____
4. Xem logs: `docker logs web-nginx`. Có access log không? ____
5. Stop và remove container

---

### Bài 4: Inspect & Stats

**Tasks:**
1. Run PostgreSQL:
   ```bash
   docker run -d --name db-postgres \
     -e POSTGRES_PASSWORD=test123 \
     -p 5432:5432 \
     postgres:15-alpine
   ```
2. Inspect:
   ```bash
   docker inspect db-postgres | grep -A 5 "Ports"
   ```
   Ghi port mapping: ____
3. Stats:
   ```bash
   docker stats db-postgres
   ```
   Ghi CPU % và MEM usage: ____
4. Stop & remove

---

## 💡 Hints

- Dùng `docker ps -q` để lấy container IDs (cho scripts)
- Dùng `docker rm -f <name>` để force remove container đang chạy
- Port mapping: `-p <host_port>:<container_port>`

---

## ✅ Self-Evaluation

- [ ] Hoàn thành Bài 1 (Image operations)
- [ ] Hoàn thành Bài 2 (Container lifecycle)
- [ ] Hoàn thành Bài 3 (Port mapping)
- [ ] Hoàn thành Bài 4 (Inspect & stats)

**Success Criteria:**
- ✅ Biết cách pull, list, remove images
- ✅ Biết cách run, stop, start, remove containers
- ✅ Biết cách exec vào container
- ✅ Biết cách xem logs và stats
- ✅ Hiểu port mapping

---

→ Nếu pass, chuyển sang [Quiz](quiz.md) rồi sang [Lesson 03](../03-Dockerfile-Basics/lesson.md)

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
