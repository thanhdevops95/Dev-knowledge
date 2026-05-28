# ❓ Quiz: Docker Advanced

> **Knowledge Check for Advanced Docker (20 Questions)**
>
> *Kiểm tra kiến thức Docker nâng cao (20 câu hỏi).*

---

### Q1: Multi-stage Build

Multi-stage build giúp gì?

- a) Tăng tốc build
- b) Giảm kích thước final image
- c) Tăng security
- d) Cả b và c  

---

### Q2: COPY --from

`COPY --from=builder` làm gì?

- a) Copy từ host
- b) Copy từ stage trước
- c) Copy từ remote
- d) Copy từ volume  

---

### Q3: Base Image Size

Image nào nhỏ nhất?

- a) node:18
- b) node:18-slim
- c) node:18-alpine
- d) node:18-buster  

---

### Q4: Non-root User

Tại sao nên chạy container với non-root user?

- a) Tăng performance
- b) Giảm attack surface
- c) Tiết kiệm memory
- d) Tăng tốc build  

---

### Q5: BuildKit

Cách enable BuildKit?

- a) `DOCKER_BUILDKIT=1`
- b) `--buildkit`
- c) `--enable-buildkit`
- d) Không cần enable  

---

### Q6: Cache Mount

`RUN --mount=type=cache` dùng để?

- a) Mount volume
- b) Cache build dependencies
- c) Mount secrets
- d) Mount SSH keys  

---

### Q7: Secret Mount

Secret mount trong BuildKit?

- a) Store secret in image (Lưu secret trong image)
- b) Mount secret only during build (Chỉ mount secret khi build)
- c) Environment variable
- d) ARG instruction  

---

### Q8: .dockerignore

.dockerignore giúp gì?

- a) Ignore containers
- b) Reduce build context size (Giảm kích thước build context)
- c) Ignore images
- d) Ignore volumes  

---

### Q9: Health Check

`HEALTHCHECK` interval default?

- a) 10s
- b) 30s
- c) 60s
- d) No default  

---

### Q10: Resource Limit

Flag giới hạn memory?

- a) `--mem`
- b) `-m`
- c) `--memory`
- d) b và c đều đúng  

---

### Q11: Read-only Filesystem

`--read-only` flag làm gì?

- a) Read-only volume
- b) Container filesystem read-only
- c) Image read-only
- d) host read-only  

---

### Q12: Layer Caching

Layer nào nên đặt trước trong Dockerfile?

- a) Thay đổi thường xuyên
- b) Thay đổi ít
- c) Không quan trọng
- d) Tùy vào image  

---

### Q13: Distroless

Distroless image là gì?

- a) No Linux distribution (Không có bản phân phối Linux)
- b) Minimal image without package manager (Image tối thiểu không có trình quản lý gói)
- c) Empty image
- d) Alpine variant  

---

### Q14: Scratch Image

`FROM scratch` dùng khi nào?

- a) Mọi application
- b) Statically compiled binaries
- c) Node.js apps
- d) Python apps  

---

### Q15: Container Debug

Lệnh exec vào running container?

- a) `docker enter`
- b) `docker exec -it`
- c) `docker attach`
- d) `docker shell`  

---

### Q16: OOM Killer

Container bị OOM killed khi?

- a) CPU limit exceeded
- b) Memory limit exceeded
- c) Disk limit exceeded
- d) Network limit exceeded  

---

### Q17: Layer Optimization

Cách tốt nhất để giảm layers?

- a) Combine RUN commands (Kết hợp lệnh RUN)
- b) Use multistage
- c) Remove with separate RUN
- d) Use ADD instead of COPY  

---

### Q18: Security Scanning

Tool nào scan Docker vulnerabilities?

- a) Trivy
- b) Docker Scout
- c) Snyk
- d) Tất cả  

---

### Q19: Docker Stats

`docker stats` hiển thị gì?

- a) Image info
- b) Container resource usage (Mức sử dụng tài nguyên container)
- c) Network stats
- d) Disk usage  

---

### Q20: Build Target

`docker build --target` dùng để?

- a) Build specific stage (Build stage cụ thể)
- b) Set target platform
- c) Set output target
- d) Set registry  

---

## 📝 Answers

<details>
<summary>Click để xem đáp án</summary>

| Q | A | Explanation |
|---|---|-------------|
| 1 | d | Multi-stage giảm size và tăng security |
| 2 | b | Copy files từ stage trước |
| 3 | c | Alpine ~120MB, slim ~200MB, full ~900MB |
| 4 | b | Non-root giảm attack surface |
| 5 | a | DOCKER_BUILDKIT=1 environment variable |
| 6 | b | Cache dependencies giữa builds |
| 7 | b | Secret chỉ available during build |
| 8 | b | Giảm build context size |
| 9 | b | Default interval là 30s |
| 10 | d | -m và --memory đều valid |
| 11 | b | Container filesystem read-only |
| 12 | b | Ít thay đổi trước để tận dụng cache |
| 13 | b | Minimal image không có package manager |
| 14 | b | Dành cho static binaries (Go, Rust) |
| 15 | b | docker exec -it container sh |
| 16 | b | Out Of Memory khi exceed memory limit |
| 17 | a | Combine với && trong một RUN |
| 18 | d | Tất cả đều là vulnerability scanners |
| 19 | b | CPU, memory, network I/O của containers |
| 20 | a | Build specific stage trong multi-stage |

</details>

---

**[← Back to README](./README.md)** | **[Go to Exercises →](./EXERCISES.md)**
