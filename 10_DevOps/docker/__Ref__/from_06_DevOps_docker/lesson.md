# 🐳 Docker — Tổng Quan và Khái Niệm Cốt Lõi

---

## 📋 Metadata

- **Parent Lesson:** N/A (Đây là bài mẹ)
- **Level:** `[BEGINNER]`
- **Estimated Time:** 30 phút (đọc), 2-3 giờ cho toàn bộ chủ đề
- **Prerequisites:** Hiểu cơ bản về terminal/command line

---

## 🎯 Mục Tiêu Bài Học

Sau khi đọc phần này, bạn sẽ hiểu được:

- ✅ Docker là gì và tại sao nó quan trọng
- ✅ Lịch sử và problem space Docker giải quyết
- ✅ Docker architecture cơ bản (Image, Container, Docker Engine)
- ✅ Khi nào nên dùng Docker và khi nào không
- ✅ Tổng quan về Docker ecosystem

---

## 📚 Nội Dung

### 1. Docker là gì?

**Định nghĩa chính thức (Official Definition):**

> Docker is a platform for developing, shipping, and running applications in containers.  
> — *Docker Official Documentation*

**Giải thích đơn giản:**

Docker cho phép bạn đóng gói **toàn bộ ứng dụng** (code, dependencies, libraries, configuration) vào một **container** — giống như một chiếc thùng container trong logistics. Container này có thể chạy **giống hệt** trên máy của bạn, máy của đồng nghiệp, staging server, hay production server.

```
Máy Dev A (macOS)     →     Docker Image     →     Máy Dev B (Windows)
    │                              │                              │
    └─[Python 3.11 + Flask]───────┼──────[Same Python 3.11 + Flask]─┘
                                   ↓
                            Production Server (Linux)
                                   ↓
                            Same behavior everywhere! ✅
```

---

### 2. Lịch sử ngắn & Tại sao cần Docker

#### Trước Docker: "It works on my machine!" era

**Vấn đề:**
- Mỗi developer có môi trường khác nhau (phiên bản Node.js, Python, libs)
- IT phải cài đặt thủ công trên mỗi server
- Khó khăn khi scaling và deploy
- Virtual Machines (VMs) nặng, chậm, tốn resource

**Virtual Machines vs Containers:**

| VMs | Containers (Docker) |
|-----|---------------------|
| Mỗi VM có full OS kernel | Chia sẻ host OS kernel |
| Heavy (GBs) | Light (MBs) |
| Slow boot (phút) | Fast boot (giây) |
| Isolation mạnh | Isolation tốt (nhưng không bằng VM) |
| Resource overhead cao | Resource overhead thấp |

#### Docker ra đời (2013)

Docker, dựa trên công nghệ container của Linux (cgroups, namespaces), đã đơn giản hóa việc sử dụng containers:

- Easy to use CLI
- Layered images (efficient storage)
- Docker Hub (public registry)
- Rich ecosystem

---

### 3. Docker Architecture Cơ Bản

```
┌──────────────────────────────────────────────────────────┐
│                    Docker Architecture                   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐       ┌──────────────────┐           │
│  │   You (CLI) │──────▶│ Docker Client    │           │
│  └─────────────┘       └──────────────────┘           │
│                                        │                │
│                                        ▼                │
│                              ┌──────────────────┐      │
│                              │  Docker Daemon   │      │
│                              │  (dockerd)       │      │
│                              └──────────────────┘      │
│                                        │                │
│          ┌─────────────────────────────┼────────────────┤
│          ▼                             ▼                │
│  ┌──────────────┐            ┌──────────────────┐     │
│  │   Images     │            │   Containers     │     │
│  │ (Read-only)  │            │  (Writable layer)│     │
│  └──────────────┘            └──────────────────┘     │
│                                        │                │
│                                        ▼                │
│                              ┌──────────────────┐      │
│                              │   Docker Hub     │      │
│                              │  (Registry)      │      │
│                              └──────────────────┘      │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Các thành phần chính:**

1. **Docker Client** — CLI tool bạn dùng (`docker run`, `docker build`,...)
2. **Docker Daemon (dockerd)** — Background service quản lý images, containers, networks, volumes
3. **Docker Images** — Read-only templates chứa application và dependencies
4. **Docker Containers** — Running instances của images (có writable layer)
5. **Docker Registry** — Nơi lưu trữ và phân phối images (Docker Hub, private registry)
6. **Dockerfile** — Text file chứa instructions để build image

---

### 4. Image vs Container — Sự Khác Biệt Quan Trọng

| Images | Containers |
|--------|------------|
| **Read-only** template (như class trong OOP) | **Writable** instance (như object) |
| Lưu trong `/var/lib/docker` | Từ image + writable layer |
| Dùng `docker build` để tạo | Dùng `docker run` để tạo từ image |
| Có thể có nhiều tags (latest, v1.0, prod) | Mỗi container là unique (có container ID) |

**Ví dụ:**

```bash
# Pull image từ Docker Hub
docker pull nginx:latest

# Tạo container từ image nginx
docker run -d -p 8080:80 --name my-webserver nginx:latest

# Khoảng này:
# - nginx:latest là IMAGE (read-only)
# - my-webserver là CONTAINER (writable, chạy ngay)
```

---

### 5. Docker Use Cases

**Khi nào nên dùng Docker?**

✅ **Microservices** — Mỗi service chạy trong container riêng  
✅ **CI/CD pipelines** — Consistent build environment  
✅ **Development environments** — "Works on my machine" problem solved  
✅ **Legacy app modernization** — Wrap old app trong container  
✅ **Testing** — Spin up isolated test environments nhanh  

**Khi nào KHÔNG nên dùng Docker?**

❌ **High-performance computing** — Bare metal tốt hơn  
❌ **Graphics-intensive apps** — GPU pass-through phức tạp  
❌ **Stateful monolithic apps** (đã có VM sẵn)  
❌ **Windows-only apps** (không chạy trên Linux kernel)

---

### 6. Docker Ecosystem

Docker không chỉ là `docker run`:

| Tool | Mục đích |
|------|----------|
| **Docker Desktop** | GUI + CLI cho Mac/Windows (dễ cài đặt) |
| **Docker Engine** | Core engine cho Linux (chỉ CLI) |
| **Docker Compose** | Define và run multi-container apps |
| **Docker Swarm** | Native container orchestration (ít dùng hơn K8s) |
| **Docker Hub** | Public registry (pull/push images) |
| **Docker Scout** | Security scanning |
| **BuildKit** | Advanced builder với caching, parallelism |

**Trong chủ đề này, chúng ta tập trung vào:**
- Docker Desktop / Docker Engine
- Docker CLI
- Dockerfile
- Docker Compose (cơ bản)

---

## 💻 Hands-On Demo (Optional)

Nếu bạn đã cài Docker, thử các commands sau:

```bash
# Kiểm tra Docker version
docker --version

# Pull một image công khai (hello-world)
docker pull hello-world

# Chạy container từ image
docker run hello-world

# List tất cả images đã pull
docker images

# List containers đang chạy
docker ps

# List tất cả containers (kể cả stopped)
docker ps -a
```

---

## ✅ Kiểm Tra & Đánh Giá

### Self-Check Questions

1. **Sự khác biệt chính giữa Image và Container là gì?**
   - A. Image là writable, Container là read-only
   - B. Image là read-only template, Container là writable instance
   - C. Không có khác biệt
   
   **Đáp án:** B

2. **Docker sử dụng isolation techniques nào của Linux?**
   - A. Virtualization
   - B. Cgroups và Namespaces
   - C. Chroot only
   
   **Đáp án:** B

3. **Command nào dùng để build image từ Dockerfile?**
   - A. `docker create`
   - B. `docker build`
   - C. `docker make`
   
   **Đáp án:** B

---

### Mini Exercise

**Bài tập:** Mô tả bằng lời của bạn (không cần code):

Giải thích sự khác biệt giữa Docker và Virtual Machine. Khi nào nên dùng Docker thay vì VM?

**Gợi ý:** Think về resource usage, boot time, isolation level

**Kỳ vọng:** Bạn có thể nêu được ít nhất 3 điểm khác biệt và 1 scenario rõ ràng cho mỗi approach.

---

## 🔗 Liên Kết

### Navigation

- ← [Quay lại index bài mẹ](index.md)
- → [Bài tiếp theo: Installation & Setup](_sub-lessons/01-Installation-Setup/lesson.md)

### Further Reading

- [Docker Get Started Guide](https://docs.docker.com/get-started/)
- [Docker Architecture Overview](https://docs.docker.com/engine/docker-overview/)
- [Docker vs VM — Detailed Comparison](https://www.docker.com/resources/what-container/)

---

## 📝 Ghi Chú & Lưu Ý

> **Lưu ý quan trọng:** Docker Desktop trên Mac/Windows chạy Docker trong một lightweight VM. Trên Linux, Docker chạy trực tiếp trên kernel.

> **Common misconception:** Docker không phải là virtualization tool — nó là containerization. Không có hypervisor, chỉ dùng Linux kernel features.

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
