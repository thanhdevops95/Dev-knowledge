# 🎓 BuildKit & Multi-stage Advanced — Build 1 phút thay 5 phút

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Intermediate\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~25 phút\
> **Prerequisites:** [00_intermediate-overview.md](00_intermediate-overview.md), Docker 23+ installed

> 🎯 *Bạn build image FastAPI mất 5 phút mỗi lần — `pip install` chạy lại từ đầu dù chỉ sửa 1 dòng code. Bài này dạy bạn dùng **BuildKit** (engine default 2026) đúng cách: cache mount, secret mount, parallelism, buildx, multi-platform, advanced multi-stage. Mục tiêu: build < 1 phút, image multi-arch.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **BuildKit** là gì, khác legacy builder thế nào
- [ ] Dùng **`RUN --mount=type=cache`** giữ pip/npm cache giữa các build
- [ ] Dùng **`RUN --mount=type=secret`** inject API key build-time **không leak** vào image
- [ ] Build **multi-platform** (amd64 + arm64) bằng `docker buildx`
- [ ] Viết **multi-stage Dockerfile** chuẩn cho Python/Node/Go
- [ ] Dùng **`docker buildx bake`** cho monorepo nhiều image
- [ ] Optimize **layer order** — code thay đổi không invalidate deps layer

---

## Tình huống — Build chậm 5 phút mỗi lần `git push`

Bạn có FastAPI app + Dockerfile basic:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
```

Build lần đầu **5 phút** — ok.

Sửa 1 dòng trong `app.py` (không động `requirements.txt`), `docker build`:

```
[+] Building 287.4s
 => [1/4] FROM python:3.12-slim                              0.5s (cached)
 => [2/4] WORKDIR /app                                       0.1s (cached)
 => [3/4] COPY . .                                           0.3s
 => [4/4] RUN pip install -r requirements.txt              285.0s ← lại 5 phút!
```

🔥 **Vấn đề**: `COPY . .` đứng trước `RUN pip install` → layer COPY thay đổi (vì có `app.py` mới) → cache layer phía sau **vỡ**, pip install chạy lại.

Bạn sửa thứ tự:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

→ Build 2: chỉ chạy lại COPY cuối, **15 giây**.

Nhưng sửa `requirements.txt` (thêm 1 package)? Lại 5 phút pip install từ đầu. **Vì sao?**

→ Vì pip không có **persistent cache** giữa builds. Mỗi build = pip download lại từ PyPI.

Sếp: *"Dùng BuildKit cache mount đi. `--mount=type=cache` giữ pip cache giữa các build. Build lần thứ 2 chỉ install package mới."*

→ Bài này dạy BuildKit features đầy đủ.

---

## 1️⃣ Vậy BuildKit là gì?

**BuildKit** = build engine thế hệ mới của Docker, viết bằng Go, replace legacy builder (cũ chạy bên trong Docker daemon).

| Aspect | Legacy builder | **BuildKit** (default 2023+) |
|---|---|---|
| Architecture | In-daemon | Standalone (containerd-based) |
| Parallelism | Sequential | **Parallel** (stage độc lập build cùng lúc) |
| Cache | Layer cache only | **Cache mount, secret mount, SSH mount** |
| Multi-platform | Khó | `docker buildx` native |
| Output formats | docker image | tar, OCI, registry, cache-only |
| Frontend | Dockerfile only | Dockerfile, custom (LLB) |

🪞 **Ẩn dụ**: *Legacy builder như **dây chuyền sản xuất tuần tự** — máy 1 xong mới máy 2. BuildKit như **dây chuyền song song nhiều line** — máy 1+2+3 chạy cùng lúc nếu không phụ thuộc nhau, có "kho vật liệu chung" (cache mount) tái dùng giữa các production run.*

### Verify BuildKit đang chạy

Docker 23+ (2023) đã enable BuildKit mặc định — nhưng đáng check trước khi dùng feature mới. 2 lệnh dưới confirm version + BuildKit availability:

```bash
docker buildx version
# github.com/docker/buildx v0.13.1 ...

# BuildKit default từ Docker 23+ (2023)
docker version | grep "Version"
# Server: Docker Engine - Community
#  Version: 25.0.3  ← 25+ là BuildKit default
```

Nếu muốn explicit:

```bash
DOCKER_BUILDKIT=1 docker build .
# (chỉ cần với Docker < 23)

# Modern syntax:
docker buildx build .
```

---

## 2️⃣ Cache mount — pip/npm cache giữa các build

### Vấn đề

Mỗi build, pip download package từ PyPI → mất 1-5 phút cho project lớn.

### Giải pháp BuildKit

BuildKit feature **cache mount** giải quyết bằng 1 dòng — mount cache dir vào RUN, BuildKit persist cache giữa các build. Cấu hình tối thiểu cho Python:

```dockerfile
# syntax=docker/dockerfile:1.7
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
```

**Key changes**:
- `# syntax=docker/dockerfile:1.7` — directive bắt buộc ở dòng đầu để dùng BuildKit features (1.7 là version 2026).
- `RUN --mount=type=cache,target=/root/.cache/pip` — mount BuildKit cache vào `~/.cache/pip` khi RUN. Cache **persist giữa các build** trên cùng máy.

### Demo timing

Số liệu thực tế trên 1 Python project ~50 dependencies. Cache mount giúp build sau **nhanh 80-95%** so với cold build:

```bash
# Build 1 (cache trống):
docker buildx build -t myapp:v1 .
# RUN pip install ... 285s

# Build 2 (không sửa gì):
docker buildx build -t myapp:v2 .
# Toàn bộ cached, ~3s

# Build 3 (sửa requirements.txt, thêm 1 package "redis"):
docker buildx build -t myapp:v3 .
# RUN pip install ... ~15s (chỉ download redis, các package khác đã trong cache)
```

→ **85% build time saved** ở build 3 vs build 1.

### Cache mount cho Node/Go/Rust

Cache mount work cho mọi language có package manager — Node (npm/yarn), Go (build cache + module cache), Rust (cargo). Đây là pattern bắt buộc trong CI/CD modern:

```dockerfile
# Node.js
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Go
RUN --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=cache,target=/go/pkg/mod \
    go build -o /app .

# Rust
RUN --mount=type=cache,target=/root/.cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release
```

### Cache mount options

5 option chính của cache mount cho fine-tune — target path, ID để tách multiple cache, mode/uid cho non-root container. Hữu ích khi dùng image security-hardened:

| Option | Mô tả |
|---|---|
| `type=cache` | Loại mount |
| `target=<path>` | Path trong container |
| `id=<id>` | Cache ID — tách cache nếu nhiều RUN dùng cùng target |
| `mode=0755` | Permissions |
| `uid=1000,gid=1000` | Owner (cho non-root user) |
| `sharing=locked` | `private` (1 build độc quyền), `locked` (queue), `shared` (concurrent) |

> ⚠️ Cache mount **chỉ persist trên máy build** — không có trong image cuối. CI runner phải share cache giữa job (xem §6).

---

## 3️⃣ Secret mount — Inject API key không leak vào image

### Vấn đề

Bạn cần `PIP_INDEX_URL` private (PyPI nội bộ) cần token để pull package, hoặc cần SSH key clone private repo trong Dockerfile.

❌ **Cách sai**:

```dockerfile
# ❌ Build arg — leak vào image history!
ARG GITHUB_TOKEN
RUN git clone https://${GITHUB_TOKEN}@github.com/acme/private-lib

# Build:
docker build --build-arg GITHUB_TOKEN=ghp_xxx .

# Lộ ra:
docker history myapp:v1
# Thấy: ARG GITHUB_TOKEN=ghp_xxx
```

→ Bất kỳ ai pull image cũng `docker history` đọc được token.

### Giải pháp BuildKit secret mount

```dockerfile
# syntax=docker/dockerfile:1.7
FROM python:3.12-slim
WORKDIR /app

# ✅ Secret mount — KHÔNG ghi vào layer, KHÔNG ghi vào history
RUN --mount=type=secret,id=github_token \
    GITHUB_TOKEN=$(cat /run/secrets/github_token) && \
    pip install git+https://${GITHUB_TOKEN}@github.com/acme/private-lib.git

COPY . .
CMD ["python", "app.py"]
```

Build với secret:

```bash
# Từ file
echo "ghp_xxxxxx" > /tmp/token
docker buildx build --secret id=github_token,src=/tmp/token -t myapp:v1 .

# Hoặc từ env var
export GITHUB_TOKEN=ghp_xxxxxx
docker buildx build --secret id=github_token,env=GITHUB_TOKEN -t myapp:v1 .
```

Verify không leak:

```bash
docker history myapp:v1
# RUN --mount=type=secret,id=github_token ...  ← chỉ ghi reference, không value
docker inspect myapp:v1 | grep -i token
# (empty)
```

### SSH mount — Clone private repo

```dockerfile
# syntax=docker/dockerfile:1.7
FROM node:20-slim
RUN --mount=type=ssh \
    git clone git@github.com:acme/private-frontend.git
```

Build:

```bash
docker buildx build --ssh default -t myapp .
# 'default' = ~/.ssh/agent socket
```

---

## 4️⃣ Multi-stage build advanced

### Pattern 1: Build vs runtime separation (Python)

```dockerfile
# syntax=docker/dockerfile:1.7
# ===========================================
# Stage 1: builder — có compiler, dev tools
# ===========================================
FROM python:3.12 AS builder
WORKDIR /build

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

# ===========================================
# Stage 2: runtime — slim, chỉ runtime
# ===========================================
FROM python:3.12-slim AS runtime
WORKDIR /app

# Copy ONLY installed packages từ stage builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY app.py .
USER 1000:1000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
```

**Lợi ích**:
- Stage builder có gcc, dev headers (compile psycopg2, lxml) — nặng.
- Stage runtime chỉ chứa Python + installed packages — gọn.
- Image cuối ~150 MB thay 1.2 GB.

### Pattern 2: Build vs runtime (Node.js)

```dockerfile
# syntax=docker/dockerfile:1.7

# Stage 1: dependencies
FROM node:20 AS deps
WORKDIR /build
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Stage 2: build production bundle
FROM node:20 AS builder
WORKDIR /build
COPY --from=deps /build/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: runtime — chỉ chứa server.js + dist/
FROM node:20-slim AS runtime
WORKDIR /app
COPY --from=builder /build/dist ./dist
COPY --from=builder /build/server.js .
COPY --from=deps /build/node_modules ./node_modules

USER 1000:1000
EXPOSE 3000
CMD ["node", "server.js"]
```

### Pattern 3: Go binary (cực gọn)

```dockerfile
# syntax=docker/dockerfile:1.7

# Stage 1: build static binary
FROM golang:1.22 AS builder
WORKDIR /build
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download
COPY . .
RUN --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=cache,target=/go/pkg/mod \
    CGO_ENABLED=0 go build -ldflags="-w -s" -o /app/server .

# Stage 2: scratch (literally empty)
FROM scratch
COPY --from=builder /app/server /server
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
EXPOSE 8080
CMD ["/server"]
```

→ Image cuối ~10-30 MB cho Go binary. Không có shell, không có gì khác. (Trade-off: debug khó — xem bài 03 distroless).

### Target stage — Build chỉ 1 stage

Dockerfile nhiều stage, build stage cụ thể:

```bash
# Build chỉ stage "builder" — để debug
docker buildx build --target=builder -t myapp:debug .

# Build stage cuối (default)
docker buildx build -t myapp:prod .
```

→ Dùng khi cần image debug có shell + compiler.

---

## 5️⃣ Multi-platform — amd64 + arm64

### Vấn đề

- Bạn dùng MacBook M-series (arm64).
- Production server AWS EC2 t3 (amd64) hoặc Graviton (arm64).
- Build image trên Mac → image **chỉ arm64** → deploy AWS t3 = `exec format error`.

### Setup buildx

```bash
# Tạo builder hỗ trợ multi-platform
docker buildx create --name multi --use --platform linux/amd64,linux/arm64

# Verify
docker buildx ls
# NAME     DRIVER             PLATFORMS
# multi *  docker-container   linux/amd64, linux/arm64
```

### Build multi-platform

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t acme/myapp:v1 \
  --push \
  .
```

> ⚠️ `--push` bắt buộc cho multi-platform — local Docker daemon không lưu được manifest list multi-arch. Phải push lên registry.

Verify manifest:

```bash
docker buildx imagetools inspect acme/myapp:v1
# Manifests:
#   linux/amd64  sha256:abc...
#   linux/arm64  sha256:def...
```

### Cross-platform build tip

Khi build amd64 trên M-series Mac, BuildKit dùng **QEMU emulation** — chậm. Tăng tốc bằng:
- **Native builder** trên server amd64 (GitHub Actions runner ubuntu-latest = amd64).
- **`--cache-to`/`--cache-from`** lưu cache vào registry để CI tái dùng.

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --cache-to=type=registry,ref=acme/myapp:buildcache,mode=max \
  --cache-from=type=registry,ref=acme/myapp:buildcache \
  -t acme/myapp:v1 \
  --push \
  .
```

---

## 6️⃣ BuildKit cache trong CI/CD (GitHub Actions)

```yaml
name: Build
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ghcr.io/acme/myapp:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          secrets: |
            github_token=${{ secrets.GITHUB_TOKEN }}
```

**Highlights**:
- `cache-from: type=gha` + `cache-to: type=gha` — BuildKit lưu cache lên **GitHub Actions cache** (10GB free per repo). Build sau pull cache → 70-90% faster.
- `secrets:` — inject secret vào BuildKit secret mount.
- `platforms: linux/amd64,linux/arm64` — build multi-arch trong 1 job.

→ **2026 default**: GitHub Actions = `cache-from/to: type=gha`. GitLab CI = `type=registry`. AWS CodeBuild = `type=s3`.

---

## 7️⃣ `docker buildx bake` — Build monorepo nhiều image

### Vấn đề monorepo

Bạn có monorepo:
```
acme/
├── backend/Dockerfile
├── frontend/Dockerfile
├── worker/Dockerfile
└── migrations/Dockerfile
```

Build 4 image cần 4 lệnh, không tái dùng cache cross-image.

### Giải pháp bake

`docker-bake.hcl`:

```hcl
variable "TAG" {
  default = "latest"
}

variable "REGISTRY" {
  default = "ghcr.io/acme"
}

group "default" {
  targets = ["backend", "frontend", "worker", "migrations"]
}

target "_base" {
  platforms = ["linux/amd64", "linux/arm64"]
  cache-from = ["type=gha"]
  cache-to = ["type=gha,mode=max"]
}

target "backend" {
  inherits = ["_base"]
  context = "./backend"
  tags = ["${REGISTRY}/backend:${TAG}"]
}

target "frontend" {
  inherits = ["_base"]
  context = "./frontend"
  tags = ["${REGISTRY}/frontend:${TAG}"]
}

target "worker" {
  inherits = ["_base"]
  context = "./worker"
  tags = ["${REGISTRY}/worker:${TAG}"]
}

target "migrations" {
  inherits = ["_base"]
  context = "./migrations"
  tags = ["${REGISTRY}/migrations:${TAG}"]
}
```

Build tất cả:

```bash
TAG=v1.2.3 docker buildx bake --push
```

→ 1 lệnh, 4 image, parallel, multi-arch, cache shared.

---

## 8️⃣ Hands-on: Setup pipeline build < 1 phút

### Step 1: Optimize Dockerfile cho FastAPI

```dockerfile
# Dockerfile
# syntax=docker/dockerfile:1.7

FROM python:3.12 AS builder
WORKDIR /build

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user -r requirements.txt

# Runtime stage
FROM python:3.12-slim AS runtime
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

COPY app/ ./app/

USER 1000:1000
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: GitHub Actions workflow

`.github/workflows/build.yml`:

```yaml
name: Build & Push

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha,format=long

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Step 3: Verify build times

| Run | Build time | Cache state |
|---|---|---|
| Run 1 (first ever) | ~4 phút | Cold (pull base + pip install) |
| Run 2 (no changes) | ~30s | Full cache hit |
| Run 3 (sửa app code) | ~45s | Pip cached, chỉ rebuild code layer |
| Run 4 (sửa requirements.txt) | ~1 phút | Pip download new package, others cached |

→ **75-90% build time saved**.

---

## 💡 Pitfall & Best practice

### ❌ Pitfall: Quên `# syntax=docker/dockerfile:1.7`

```dockerfile
# ❌ Thiếu syntax directive — BuildKit features fail
FROM python:3.12
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
```

**Lỗi**:
```
error: failed to solve: failed to compute cache key: --mount feature requires syntax directive
```

→ **Fix**: Dòng ĐẦU TIÊN của Dockerfile phải là `# syntax=docker/dockerfile:1.7` (hoặc version cao hơn).

### ❌ Pitfall: Cache mount path sai

```dockerfile
# ❌ Mount sai path
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt
```

→ pip dùng `~/.cache/pip` (sub-path). Cache mount ở `/root/.cache` không cover đúng → cache không hit.

→ **Fix**: Mount đúng sub-path tool dùng: `/root/.cache/pip` cho pip, `/root/.npm` cho npm.

### ❌ Pitfall: Secret in `ARG` hoặc `ENV`

```dockerfile
# ❌ ARG leak vào history
ARG NPM_TOKEN
RUN npm config set //registry.npmjs.org/:_authToken=$NPM_TOKEN
```

→ **Fix**: Dùng `--mount=type=secret`:

```dockerfile
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) && \
    npm config set //registry.npmjs.org/:_authToken=$NPM_TOKEN && \
    npm ci
```

### ❌ Pitfall: Multi-platform không `--push`

```bash
# ❌ Không có --push
docker buildx build --platform linux/amd64,linux/arm64 -t myapp .
```

**Lỗi**:
```
ERROR: Multi-platform build is not supported for the docker driver.
Switch to a different driver, or use --push or --output flag.
```

→ **Fix**: `--push` (lên registry) hoặc `--output type=oci,dest=image.tar` (local OCI tarball).

### ❌ Pitfall: COPY thừa làm vỡ cache

```dockerfile
# ❌ COPY toàn bộ trước install
COPY . .
RUN pip install -r requirements.txt
```

→ Mỗi lần sửa code → invalidate cache → pip install lại.

→ **Fix**: COPY chỉ dependency file trước, install, rồi COPY còn lại:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### ✅ Best practice: Pin base image bằng digest

```dockerfile
# ❌ Tag mutable — base image có thể đổi
FROM python:3.12-slim

# ✅ Pin bằng digest — immutable
FROM python:3.12-slim@sha256:abc123def456...
```

→ Build reproducible 100%. Khi muốn upgrade base, đổi digest explicit.

### ✅ Best practice: `.dockerignore` aggressive

```dockerignore
# .dockerignore
.git
.github
.vscode
.idea
__pycache__
*.pyc
.pytest_cache
.venv
venv/
node_modules/
*.log
.DS_Store
.env*
README.md
docs/
tests/
```

→ Giảm build context size → build start nhanh hơn → tránh COPY nhầm file nhạy cảm.

### ✅ Best practice: Image label metadata

```dockerfile
LABEL org.opencontainers.image.source="https://github.com/acme/myapp"
LABEL org.opencontainers.image.revision="${GIT_SHA}"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
```

→ OCI standard labels — registry UI hiển thị, audit dễ.

---

## 🧠 Self-check

**Q1.** Vì sao `RUN --mount=type=cache` nhanh hơn dùng `COPY requirements.txt + RUN pip install` thuần?

<details>
<summary>💡 Đáp án</summary>

`COPY requirements.txt + RUN pip install` chỉ tận dụng **layer cache** — nếu `requirements.txt` không đổi, layer pip install được cache, OK. Nhưng khi `requirements.txt` đổi (thêm 1 package), layer cache vỡ → `pip install` chạy lại **từ đầu** — download lại TẤT CẢ package.

`RUN --mount=type=cache,target=/root/.cache/pip` là **persistent cache mount**, không phải layer cache. Khi `requirements.txt` đổi, `pip install` vẫn chạy lại, nhưng pip dùng cache trong `~/.cache/pip` — package đã download trước đó không phải tải lại từ PyPI. **Chỉ package MỚI mới download**.

→ Layer cache = all-or-nothing per layer. Cache mount = persistent storage shared across layer rebuilds.
</details>

**Q2.** Tại sao multi-platform build BẮT BUỘC `--push`?

<details>
<summary>💡 Đáp án</summary>

Local Docker daemon dùng `containerd image store` chỉ hỗ trợ **một platform per image tag** (cho version cũ). Multi-platform image cần **manifest list** (OCI Image Index v1) reference nhiều image (1 per platform) — concept này không có trong local docker.

Registry (Docker Hub, GHCR, ECR) hỗ trợ manifest list — đó là nơi multi-platform image sống. Vì vậy buildx **bắt buộc `--push`** hoặc `--output type=oci` để xuất ra registry/tarball.

(Note: Docker Desktop 2024+ có experimental `containerd image store` hỗ trợ local multi-platform, nhưng chưa stable.)
</details>

**Q3.** Khác biệt `--mount=type=cache` vs `--mount=type=secret` về **persistence**?

<details>
<summary>💡 Đáp án</summary>

- **Cache mount**: persist **trên máy build** (Docker daemon's BuildKit cache). Giữa các `docker build` consecutive, cache mount giữ lại data. Trong CI, share cache giữa job dùng `cache-from/to: type=gha|registry|s3`.

- **Secret mount**: **ephemeral** — chỉ tồn tại trong thời gian RUN instruction. Sau RUN xong, secret file biến mất, không vào layer cuối, không vào history.

→ Cache: chậm-thì-lưu. Secret: đụng-vào-rồi-xoá.
</details>

**Q4.** Bạn có Dockerfile multi-stage 5 stage (A → B → C → D → final, B+C độc lập với A). Build thế nào nhanh nhất với BuildKit?

<details>
<summary>💡 Đáp án</summary>

BuildKit **tự động phát hiện parallelism** dựa trên DAG dependency. Nếu B và C không depend trên nhau (chỉ depend A xong), BuildKit build B và C **parallel** sau khi A xong.

Bạn không cần làm gì đặc biệt — chỉ cần Dockerfile chuẩn. BuildKit phân tích `COPY --from=X` để xây DAG → schedule parallel.

Verify bằng output build log:
```
[+] Building 23.5s (15/15) FINISHED
 => [stage-A 1/3] FROM ...      4.2s
 => [stage-B 1/2] ...            3.1s ┐
 => [stage-C 1/2] ...            3.5s ┘ ← parallel!
 => [stage-D 1/3] ...            5.0s
 => [final 1/4] ...              2.0s
```

Time bars cho thấy B và C overlap.
</details>

**Q5.** GitHub Actions cache `type=gha` size limit là bao nhiêu? Khi nào không đủ?

<details>
<summary>💡 Đáp án</summary>

GitHub Actions cache:
- **10 GB total per repository** (2026)
- Eviction LRU (least recently used) khi đầy
- Per-branch (mỗi branch cache riêng, tự share với base branch fork)

**Khi không đủ**:
- Monorepo build 20+ image — cache mỗi image vài GB → đầy nhanh.
- Image base lớn (Java + JDK + Maven cache) 5+ GB/image.
- Many concurrent branches — mỗi branch nuốt cache.

**Workarounds**:
- `cache-to: type=registry,ref=...:buildcache` — lưu cache trực tiếp lên registry (size limit chỉ là registry quota).
- `cache-to: type=s3,region=...,bucket=...` — lưu lên S3 (pay-per-use, unlimited).
- Self-hosted runner với volume mounted — full control.
</details>

---

## ⚡ Cheatsheet

```bash
# === BuildKit basics ===
docker buildx version
docker buildx ls

# Build single platform với cache mount (Dockerfile có syntax directive)
docker buildx build -t myapp:v1 .

# Build với secret
docker buildx build --secret id=token,src=/tmp/token -t myapp:v1 .
docker buildx build --secret id=token,env=TOKEN -t myapp:v1 .

# === Multi-platform ===
docker buildx create --name multi --use --platform linux/amd64,linux/arm64
docker buildx build --platform linux/amd64,linux/arm64 -t acme/app:v1 --push .

# === Inspect ===
docker buildx imagetools inspect acme/app:v1   # manifest list
docker buildx du                                # cache size
docker buildx prune                             # clear cache

# === Bake ===
docker buildx bake                  # default group
docker buildx bake --print          # show resolved config
docker buildx bake backend frontend  # specific targets
TAG=v1.2.3 docker buildx bake --push

# === Cache strategies trong CI ===
# GitHub Actions
--cache-from=type=gha
--cache-to=type=gha,mode=max

# Registry (any CI)
--cache-from=type=registry,ref=acme/app:buildcache
--cache-to=type=registry,ref=acme/app:buildcache,mode=max

# Inline (small projects)
--cache-from=type=registry,ref=acme/app:latest
--cache-to=type=inline
```

```dockerfile
# === Dockerfile patterns ===

# Cache mount per language:
RUN --mount=type=cache,target=/root/.cache/pip pip install ...           # Python
RUN --mount=type=cache,target=/root/.npm npm ci                          # Node
RUN --mount=type=cache,target=/go/pkg/mod go build ...                   # Go
RUN --mount=type=cache,target=/root/.cargo/registry cargo build          # Rust
RUN --mount=type=cache,target=/var/cache/apt apt-get update              # APT

# Secret mount:
RUN --mount=type=secret,id=NAME TOKEN=$(cat /run/secrets/NAME) && ...

# SSH mount:
RUN --mount=type=ssh git clone git@github.com:org/private-repo.git

# Multi-stage target:
FROM python:3.12 AS builder    # ← `docker buildx build --target=builder`
FROM python:3.12-slim AS final
```

---

## 📚 Glossary

| Term | Vietnamese / Explanation |
|---|---|
| **BuildKit** | Build engine mới của Docker (default 2023+), parallel + cache mount + secret mount |
| **LLB** | Low-Level Build — BuildKit's intermediate representation (như IR của compiler) |
| **Frontend** | Parser convert Dockerfile/custom DSL → LLB |
| **Cache mount** | Persistent storage mount khi RUN, share giữa build runs (`--mount=type=cache`) |
| **Secret mount** | Ephemeral secret inject vào RUN, không ghi vào layer (`--mount=type=secret`) |
| **SSH mount** | Forward SSH agent socket vào build (`--mount=type=ssh`) |
| **Multi-stage build** | Dockerfile có nhiều `FROM ... AS <name>` — copy artifact giữa stages |
| **Target stage** | Build chỉ 1 stage cụ thể (`--target=builder`) |
| **buildx** | CLI plugin extend `docker build` với BuildKit features |
| **bake** | `docker buildx bake` — build multiple images theo HCL config |
| **Manifest list** | OCI Image Index — 1 tag reference nhiều platform images |
| **QEMU emulation** | Cross-platform build khi host ≠ target arch (chậm) |
| **OCI** | Open Container Initiative — chuẩn image format + distribution |
| **Provenance** | Build metadata (SLSA): builder ID, source URL, build params (xem bài 02) |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [00_intermediate-overview.md](00_intermediate-overview.md)
- → Tiếp: [02_image-security-supply-chain.md](02_image-security-supply-chain.md) *(sắp viết)*
- ↑ Cluster: [Docker README](../../README.md)

### Cross-reference
- 🔁 [CI/CD GitHub Actions](../../../ci-cd/lessons/01_basic/01_github-actions.md) — workflow integration
- 🔁 [CI/CD Pipeline patterns](../../../ci-cd/lessons/01_basic/03_pipeline-patterns.md) — monorepo selective build
- ☸️ [K8s images](../../../kubernetes/lessons/01_basic/01_pods-and-deployments.md) — imagePullPolicy

### Tài nguyên ngoài
- 📖 [BuildKit docs](https://docs.docker.com/build/buildkit/)
- 📖 [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) — syntax + RUN --mount
- 📖 [buildx docs](https://docs.docker.com/buildx/)
- 📖 [Bake reference](https://docs.docker.com/build/bake/)
- 📖 [docker/build-push-action](https://github.com/docker/build-push-action) — GitHub Action
- 📖 [Multi-platform images](https://docs.docker.com/build/building/multi-platform/)
- 📖 [BuildKit cache exporters](https://docs.docker.com/build/cache/backends/)

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in trước Verify BuildKit + Cache mount giải pháp + Demo timing + Cache cho Node/Go/Rust + Cache mount options.

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Lesson 01 của intermediate cluster. Tập trung BuildKit cache/secret/SSH mount, multi-stage 3 pattern (Python/Node/Go), multi-platform amd64+arm64, buildx bake monorepo, CI integration (GitHub Actions với `type=gha` cache). 5 pitfall + 3 best practice + 5 self-check + cheatsheet command/Dockerfile.
