# ❓ Quiz: Docker Advanced

> **Knowledge Check for Advanced Docker (20 Questions)**
>
> *Kiểm tra kiến thức Docker nâng cao (20 câu hỏi).*

---

### Q1: Multi-stage Build

What does multi-stage build help with?

*(Multi-stage build giúp gì?)*

- a) Faster build *(Tăng tốc build)*
- b) Smaller final image *(Giảm kích thước final image)*
- c) Better security *(Tăng security)*
- d) Both b and c *(Cả b và c)*

---

### Q2: COPY --from

What does `COPY --from=builder` do?

*(`COPY --from=builder` làm gì?)*

- a) Copy from host *(Copy từ host)*
- b) Copy from previous stage *(Copy từ stage trước)*
- c) Copy from remote *(Copy từ remote)*
- d) Copy from volume *(Copy từ volume)*

---

### Q3: Base Image Size

Which image is the smallest?

*(Image nào nhỏ nhất?)*

- a) node:18
- b) node:18-slim
- c) node:18-alpine
- d) node:18-buster

---

### Q4: Non-root User

Why should containers run with non-root user?

*(Tại sao nên chạy container với non-root user?)*

- a) Better performance *(Tăng performance)*
- b) Reduce attack surface *(Giảm attack surface)*
- c) Save memory *(Tiết kiệm memory)*
- d) Faster build *(Tăng tốc build)*

---

### Q5: BuildKit

How to enable BuildKit?

*(Cách enable BuildKit?)*

- a) `DOCKER_BUILDKIT=1`
- b) `--buildkit`
- c) `--enable-buildkit`
- d) No need to enable *(Không cần enable)*

---

### Q6: Cache Mount

What is `RUN --mount=type=cache` used for?

*(`RUN --mount=type=cache` dùng để?)*

- a) Mount volume *(Mount volume)*
- b) Cache build dependencies *(Cache build dependencies)*
- c) Mount secrets *(Mount secrets)*
- d) Mount SSH keys *(Mount SSH keys)*

---

### Q7: Secret Mount

What happens with secret mount in BuildKit?

*(Secret mount trong BuildKit?)*

- a) Store secret in image *(Lưu secret trong image)*
- b) Mount secret only during build *(Chỉ mount secret khi build)*
- c) Environment variable *(Biến môi trường)*
- d) ARG instruction

---

### Q8: .dockerignore

What does .dockerignore help with?

*(.dockerignore giúp gì?)*

- a) Ignore containers *(Bỏ qua containers)*
- b) Reduce build context size *(Giảm kích thước build context)*
- c) Ignore images *(Bỏ qua images)*
- d) Ignore volumes *(Bỏ qua volumes)*

---

### Q9: Health Check

What is the default `HEALTHCHECK` interval?

*(`HEALTHCHECK` interval default?)*

- a) 10s
- b) 30s
- c) 60s
- d) No default *(Không có default)*

---

### Q10: Resource Limit

Which flag limits memory?

*(Flag giới hạn memory?)*

- a) `--mem`
- b) `-m`
- c) `--memory`
- d) Both b and c *(b và c đều đúng)*

---

### Q11: Read-only Filesystem

What does the `--read-only` flag do?

*(`--read-only` flag làm gì?)*

- a) Read-only volume *(Volume chỉ đọc)*
- b) Container filesystem read-only *(Filesystem container chỉ đọc)*
- c) Image read-only *(Image chỉ đọc)*
- d) Host read-only *(Host chỉ đọc)*

---

### Q12: Layer Caching

Which layer should come first in Dockerfile?

*(Layer nào nên đặt trước trong Dockerfile?)*

- a) Frequently changing *(Thay đổi thường xuyên)*
- b) Rarely changing *(Thay đổi ít)*
- c) Doesn't matter *(Không quan trọng)*
- d) Depends on image *(Tùy vào image)*

---

### Q13: Distroless

What is a distroless image?

*(Distroless image là gì?)*

- a) No Linux distribution *(Không có bản phân phối Linux)*
- b) Minimal image without package manager *(Image tối thiểu không có trình quản lý gói)*
- c) Empty image *(Image rỗng)*
- d) Alpine variant *(Biến thể Alpine)*

---

### Q14: Scratch Image

When to use `FROM scratch`?

*(`FROM scratch` dùng khi nào?)*

- a) All applications *(Mọi application)*
- b) Statically compiled binaries *(Binary được biên dịch tĩnh)*
- c) Node.js apps *(Ứng dụng Node.js)*
- d) Python apps *(Ứng dụng Python)*

---

### Q15: Container Debug

Command to exec into running container?

*(Lệnh exec vào running container?)*

- a) `docker enter`
- b) `docker exec -it`
- c) `docker attach`
- d) `docker shell`

---

### Q16: OOM Killer

When does a container get OOM killed?

*(Container bị OOM killed khi?)*

- a) CPU limit exceeded *(Vượt giới hạn CPU)*
- b) Memory limit exceeded *(Vượt giới hạn memory)*
- c) Disk limit exceeded *(Vượt giới hạn disk)*
- d) Network limit exceeded *(Vượt giới hạn network)*

---

### Q17: Layer Optimization

Best way to reduce layers?

*(Cách tốt nhất để giảm layers?)*

- a) Combine RUN commands *(Kết hợp lệnh RUN)*
- b) Use multistage *(Dùng multistage)*
- c) Remove with separate RUN *(Xóa bằng RUN riêng)*
- d) Use ADD instead of COPY *(Dùng ADD thay COPY)*

---

### Q18: Security Scanning

Which tool scans Docker vulnerabilities?

*(Tool nào scan Docker vulnerabilities?)*

- a) Trivy
- b) Docker Scout
- c) Snyk
- d) All of the above *(Tất cả)*

---

### Q19: Docker Stats

What does `docker stats` display?

*(`docker stats` hiển thị gì?)*

- a) Image info *(Thông tin image)*
- b) Container resource usage *(Mức sử dụng tài nguyên container)*
- c) Network stats *(Thống kê mạng)*
- d) Disk usage *(Sử dụng disk)*

---

### Q20: Build Target

What is `docker build --target` used for?

*(`docker build --target` dùng để?)*

- a) Build specific stage *(Build stage cụ thể)*
- b) Set target platform *(Đặt platform đích)*
- c) Set output target *(Đặt output đích)*
- d) Set registry *(Đặt registry)*

---

## 📝 Answers

<details>
<summary>Click to view answers / Nhấn để xem đáp án</summary>

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | d | Multi-stage reduces size and improves security |
| 2 | b | Copy files from previous stage |
| 3 | c | Alpine ~120MB, slim ~200MB, full ~900MB |
| 4 | b | Non-root reduces attack surface |
| 5 | a | DOCKER_BUILDKIT=1 environment variable |
| 6 | b | Cache dependencies between builds |
| 7 | b | Secret only available during build |
| 8 | b | Reduces build context size |
| 9 | b | Default interval is 30s |
| 10 | d | Both -m and --memory are valid |
| 11 | b | Container filesystem becomes read-only |
| 12 | b | Rarely changing first to leverage cache |
| 13 | b | Minimal image without package manager |
| 14 | b | For static binaries (Go, Rust) |
| 15 | b | docker exec -it container sh |
| 16 | b | Out Of Memory when memory limit exceeded |
| 17 | a | Combine with && in one RUN |
| 18 | d | All are vulnerability scanners |
| 19 | b | CPU, memory, network I/O of containers |
| 20 | a | Build specific stage in multi-stage |

</details>

---

**[← Back to README](./README.md)** | **[Go to Exercises →](./EXERCISES.md)**
