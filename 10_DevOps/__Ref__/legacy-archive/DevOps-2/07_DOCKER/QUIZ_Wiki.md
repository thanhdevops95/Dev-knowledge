# 📝 Quiz & Self-Test - Docker

Kiểm tra kiến thức Docker của bạn với 20 câu hỏi từ cơ bản đến nâng cao.

**Hướng dẫn:** Trả lời câu hỏi trước, sau đó xem đáp án bên dưới.

---

## 🟢 Cơ bản (1-7)

### Q1: Container vs Virtual Machine

Container khác VM như thế nào? Chọn TẤT CẢ câu đúng:

- [ ] A. Container share kernel với host OS
- [ ] B. VM nhẹ hơn Container
- [ ] C. Container khởi động nhanh hơn VM
- [ ] D. VM có isolation tốt hơn Container

<details>
<summary>💡 Đáp án</summary>

**A, C, D đúng**

- ✅ A: Container dùng chung kernel với host
- ❌ B: Sai, Container nhẹ hơn nhiều (MB vs GB)
- ✅ C: Container khởi động trong seconds, VM mất minutes
- ✅ D: VM có hardware-level isolation, Container là process-level

</details>

---

### Q2: Docker Image vs Container

Mối quan hệ giữa Image và Container là gì?

- [ ] A. Image là container đang chạy
- [ ] B. Container là instance của Image
- [ ] C. Image và Container là như nhau
- [ ] D. Container tạo ra Image

<details>
<summary>💡 Đáp án</summary>

**B đúng**

- Image = Template (read-only)
- Container = Instance đang chạy của Image
- Một Image có thể tạo nhiều Containers

```
Image (nginx:latest) → Container 1 (nginx-web-1)
                     → Container 2 (nginx-web-2)
                     → Container 3 (nginx-web-3)
```

</details>

---

### Q3: Dockerfile Commands

Lệnh nào trong Dockerfile chạy **khi build image**?

- [ ] A. CMD
- [ ] B. ENTRYPOINT
- [ ] C. RUN
- [ ] D. EXPOSE

<details>
<summary>💡 Đáp án</summary>

**C đúng**

- **RUN** - Chạy khi **build** image (tạo layer mới)
- **CMD** - Chạy khi **run** container
- **ENTRYPOINT** - Chạy khi **run** container
- **EXPOSE** - Chỉ là documentation, không chạy gì

```dockerfile
RUN apt-get update      # Chạy khi docker build
CMD ["nginx", "-g", "daemon off;"]  # Chạy khi docker run
```

</details>

---

### Q4: Docker Network

Khi 2 containers ở cùng network, chúng giao tiếp như thế nào?

- [ ] A. Bằng IP address của host
- [ ] B. Bằng container name
- [ ] C. Không thể giao tiếp
- [ ] D. Chỉ qua localhost

<details>
<summary>💡 Đáp án</summary>

**B đúng**

Trong Docker network, containers có thể dùng **container name** như hostname:

```bash
# Container app có thể gọi
curl http://db:5432  # db là tên container database
```

Docker DNS tự động resolve container names.

</details>

---

### Q5: Docker Volumes

Dữ liệu trong container sẽ như thế nào khi container bị xóa?

- [ ] A. Luôn được giữ lại
- [ ] B. Luôn bị mất
- [ ] C. Mất nếu không dùng Volume
- [ ] D. Tự động backup

<details>
<summary>💡 Đáp án</summary>

**C đúng**

- Dữ liệu **trong container filesystem** → Mất khi xóa container
- Dữ liệu **trong Volume** → Được giữ lại

```bash
# Không có volume - data mất
docker run postgres

# Có volume - data persist
docker run -v pgdata:/var/lib/postgresql/data postgres
```

</details>

---

### Q6: Layer Caching

Dockerfile nào tận dụng layer caching tốt hơn?

**Option A:**

```dockerfile
COPY . /app
RUN npm install
```

**Option B:**

```dockerfile
COPY package*.json /app/
RUN npm install
COPY . /app
```

<details>
<summary>💡 Đáp án</summary>

**Option B tốt hơn**

- A: Mỗi khi code thay đổi → invalidate cache → npm install lại
- B: package.json ít thay đổi → cache npm install → chỉ copy code mới

**Nguyên tắc:** Copy dependencies file trước, install, rồi mới copy code.

</details>

---

### Q7: Docker Compose

`depends_on` trong docker-compose có ý nghĩa gì?

- [ ] A. Đảm bảo service kia **healthy** trước khi start
- [ ] B. Chỉ đảm bảo service kia **started** trước
- [ ] C. Merge environment variables
- [ ] D. Share network namespace

<details>
<summary>💡 Đáp án</summary>

**B đúng**

`depends_on` chỉ đợi container **start**, không đợi **ready**:

```yaml
services:
  app:
    depends_on:
      - db  # Chỉ đợi db container start
  db:
    image: postgres
```

Để đợi healthy, dùng condition:

```yaml
depends_on:
  db:
    condition: service_healthy
```

</details>

---

## 🟡 Trung bình (8-14)

### Q8: Multi-stage Build

Multi-stage build giúp gì?

- [ ] A. Chạy nhiều containers cùng lúc
- [ ] B. Giảm kích thước final image
- [ ] C. Tăng tốc độ build
- [ ] D. Cho phép dùng nhiều base images

<details>
<summary>💡 Đáp án</summary>

**B và D đúng**

```dockerfile
# Stage 1: Build (có build tools)
FROM node:18 AS builder
WORKDIR /app
RUN npm ci && npm run build

# Stage 2: Production (chỉ có runtime)
FROM node:18-alpine
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

- Final image chỉ chứa production code
- Build tools không có trong final image
- Có thể dùng nhiều base images

</details>

---

### Q9: Container Exit Codes

Container exit với code 137. Nghĩa là gì?

- [ ] A. Application error
- [ ] B. Out of memory (OOM killed)
- [ ] C. Permission denied
- [ ] D. Network timeout

<details>
<summary>💡 Đáp án</summary>

**B đúng**

Exit codes phổ biến:

- **0**: Success
- **1**: General application error
- **126**: Permission problem
- **127**: Command not found
- **137**: OOM Killed (128 + 9 = SIGKILL)
- **143**: Graceful termination (128 + 15 = SIGTERM)

```bash
docker inspect container_id --format='{{.State.ExitCode}}'
# 137 = Container bị kill do hết memory
```

</details>

---

### Q10: Docker Security

Chạy container với `--privileged` có rủi ro gì?

- [ ] A. Container chậm hơn
- [ ] B. Container có full access đến host
- [ ] C. Không có rủi ro
- [ ] D. Container không thể dùng network

<details>
<summary>💡 Đáp án</summary>

**B đúng**

`--privileged` cho container:

- Full access đến host devices
- Có thể mount filesystems
- Có thể load kernel modules
- Gần như = root access trên host

**KHÔNG BAO GIỜ dùng privileged cho production** trừ khi absolutely cần thiết (như Docker-in-Docker).

</details>

---

### Q11: Docker Logging

Logs của container được lưu ở đâu (mặc định)?

- [ ] A. Trong container tại /var/log
- [ ] B. Trên Docker host tại /var/lib/docker/containers/
- [ ] C. Tự động gửi đến cloud
- [ ] D. Không lưu ở đâu

<details>
<summary>💡 Đáp án</summary>

**B đúng**

```bash
# Mặc định: json-file driver
docker inspect container_id | grep LogPath
# /var/lib/docker/containers/<container-id>/<container-id>-json.log

# Cấu hình log rotation
docker run --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  nginx
```

</details>

---

### Q12: Dockerfile COPY vs ADD

COPY và ADD khác nhau như thế nào?

- [ ] A. Giống nhau hoàn toàn
- [ ] B. ADD có thể download URL và extract tar
- [ ] C. COPY nhanh hơn ADD
- [ ] D. ADD deprecated

<details>
<summary>💡 Đáp án</summary>

**B đúng**

| COPY | ADD |
|------|-----|
| Copy files từ local | Copy + Download URL + Auto-extract tar |
| Predictable | Magic behavior |
| **Recommended** | Chỉ dùng khi cần extract |

```dockerfile
# ✅ Dùng COPY cho files thường
COPY app.py /app/

# ADD chỉ khi cần extract
ADD archive.tar.gz /app/
```

</details>

---

### Q13: Docker Registry

Khi `docker pull nginx`, Docker pull từ đâu?

- [ ] A. Docker Hub
- [ ] B. Local cache
- [ ] C. GitHub
- [ ] D. Google Container Registry

<details>
<summary>💡 Đáp án</summary>

**A đúng** (nếu không có local)

Pull order:

1. Check local cache
2. Nếu không có → Docker Hub (`docker.io`)

Full image name:

```
docker pull nginx
# = docker pull docker.io/library/nginx:latest

docker pull mycompany/myapp
# = docker pull docker.io/mycompany/myapp:latest

docker pull gcr.io/project/image
# Pull từ Google Container Registry
```

</details>

---

### Q14: Container Resource Limits

Điều gì xảy ra nếu container dùng hơn memory limit?

- [ ] A. Container tự động scale
- [ ] B. Container bị OOM kill
- [ ] C. Container swap sang disk
- [ ] D. Host bị slow

<details>
<summary>💡 Đáp án</summary>

**B đúng**

```bash
docker run --memory=256m nginx
# Nếu nginx dùng > 256MB → OOM Killed

# Check container bị OOM
docker inspect container_id --format='{{.State.OOMKilled}}'
# true
```

Best practice: Set limits = 125-150% của expected usage.

</details>

---

## 🔴 Nâng cao (15-20)

### Q15: Docker Build Context

`.dockerignore` quan trọng vì sao?

<details>
<summary>💡 Đáp án</summary>

`.dockerignore` giúp:

1. **Giảm build context size** → Nhanh hơn
2. **Không copy secrets** vào image
3. **Không copy files không cần thiết**

```dockerignore
.git
node_modules
*.md
.env
secrets/
```

Không có `.dockerignore`:

```bash
docker build .
# Sending build context to Docker daemon  2.5GB  ← Chậm!
```

Có `.dockerignore`:

```bash
docker build .
# Sending build context to Docker daemon  10MB  ← Nhanh!
```

</details>

---

### Q16: Docker Healthcheck

Healthcheck fail 3 lần liên tiếp, container status là gì?

- [ ] A. Exited
- [ ] B. Unhealthy
- [ ] C. Restarting
- [ ] D. Dead

<details>
<summary>💡 Đáp án</summary>

**B đúng**

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
```

Container status progression:

1. **Starting** → Health not run yet
2. **Healthy** → Health check passed
3. **Unhealthy** → Health check failed (retries lần)

Container **vẫn running** khi unhealthy, nhưng orchestrators (K8s, Swarm) có thể restart.

</details>

---

### Q17: Docker Networking Modes

Container với `--network=host` có gì đặc biệt?

<details>
<summary>💡 Đáp án</summary>

`--network=host`:

- Container share network namespace với host
- Không có network isolation
- Container ports = Host ports directly
- Performance better (no NAT)

```bash
docker run --network=host nginx
# nginx listen on host's port 80 directly
# Không cần -p 80:80
```

**Use cases:** High-performance networking, monitoring host network.

**Risk:** Giảm isolation.

</details>

---

### Q18: Docker Layer Cache Invalidation

Thay đổi nào invalidate **tất cả** layer phía sau?

<details>
<summary>💡 Đáp án</summary>

Bất kỳ thay đổi nào trong Dockerfile đều invalidate cache của **tất cả layers phía sau**:

```dockerfile
FROM ubuntu
RUN apt-get update        # Layer 1
RUN apt-get install -y curl  # Layer 2 - nếu thay đổi
COPY . /app               # Layer 3 - INVALIDATED!
RUN npm install           # Layer 4 - INVALIDATED!
```

**Nguyên tắc:**

- Đặt commands ít thay đổi ở trên
- Đặt COPY code ở cuối

</details>

---

### Q19: Docker Secrets

Cách nào là **SAFE** để pass secrets vào container?

- [ ] A. ENV trong Dockerfile
- [ ] B. Build args
- [ ] C. docker run -e
- [ ] D. Docker secrets / external vault

<details>
<summary>💡 Đáp án</summary>

**D là safe nhất**

| Method | Safe? | Why |
|--------|-------|-----|
| ENV in Dockerfile | ❌ | Secrets trong image history |
| Build args | ❌ | Có trong docker history |
| docker run -e | ⚠️ | OK nhưng visible trong ps |
| Docker secrets | ✅ | Encrypted, mounted as file |
| External vault | ✅ | Secret không ở Docker |

```bash
# Docker secrets (Swarm)
echo "password" | docker secret create db_pass -
docker service create --secret db_pass myapp

# External vault
docker run -e VAULT_ADDR=... myapp
# App đọc secret từ Vault lúc runtime
```

</details>

---

### Q20: Docker Rootless Mode

Docker rootless mode là gì và khi nào nên dùng?

<details>
<summary>💡 Đáp án</summary>

**Docker Rootless** = Chạy Docker daemon và containers **không cần root privileges**.

**Lợi ích:**

- Nếu container bị compromise → Không có root access trên host
- Better security isolation
- Required trong nhiều secure environments

**Trade-offs:**

- Một số features không khả dụng (như port < 1024)
- Setup phức tạp hơn

**Khi nào dùng:**

- Multi-tenant environments
- Security-sensitive systems
- CI/CD runners

```bash
# Install rootless Docker
dockerd-rootless-setuptool.sh install
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
```

</details>

---

## 📊 Đánh giá

| Score | Level |
|-------|-------|
| 0-7 | 🟢 Beginner - Cần học thêm basics |
| 8-14 | 🟡 Intermediate - Đang tiến bộ |
| 15-18 | 🔴 Advanced - Hiểu sâu |
| 19-20 | ⭐ Expert - Sẵn sàng interview |

---

[← Về README](README.md) | [LABS.md →](LABS.md) | [SCENARIOS.md →](SCENARIOS.md)
