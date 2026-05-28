# 🐳 Module 2.1: Docker Advanced

[![Duration](https://img.shields.io/badge/Duration-1%20week-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Intermediate-orange?style=flat-square)](.)

> **Advanced Docker Skills** - Multi-stage builds, optimization, and security best practices.
>
> *Nâng cao kỹ năng Docker - Multi-stage builds, tối ưu hóa, và bảo mật.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Master multi-stage builds (Thành thạo multi-stage builds)
- ✅ Optimize Docker images - size, layers, caching (Tối ưu Docker images)
- ✅ Implement Docker security best practices (Áp dụng bảo mật Docker)
- ✅ Use BuildKit advanced features (Sử dụng tính năng BuildKit)
- ✅ Debug and troubleshoot containers (Debug và xử lý sự cố)
- ✅ Understand Docker internals (Hiểu cơ chế bên trong Docker)

---

## 📋 Prerequisites (Điều kiện tiên quyết)

- Complete Track 1, especially module 1.5 Docker Fundamentals (Hoàn thành Track 1)
- Docker Desktop installed (Đã cài Docker Desktop)
- Understand Dockerfile basics (Hiểu Dockerfile cơ bản)

---

## 📚 Content (Nội dung)

### 1. Multi-stage Builds

#### Why Multi-stage Builds? (Tại sao cần Multi-stage Builds?)

In reality, an application needs many dependencies to **build** (e.g., compiler, build tools), but doesn't need them to **run**. Multi-stage builds allow you to:

*Trong thực tế, một ứng dụng cần nhiều dependencies để **build** (ví dụ: compiler, build tools), nhưng không cần chúng để **chạy**. Multi-stage builds cho phép bạn:*

| Problem | Multi-stage Solution |
|---------|---------------------|
| Image too large due to build tools | Only copy needed artifacts to final image *(Chỉ copy artifacts cần thiết sang image cuối)* |
| Poor security due to source code | Production image doesn't contain source code *(Image production không chứa source code)* |
| Complex build process | Split into clear stages *(Chia thành các stages rõ ràng)* |

#### Basic Multi-stage

Below is an example of a Dockerfile with 2 stages. The first stage builds the application, the second stage only contains the build output.

*Dưới đây là ví dụ một Dockerfile với 2 stages. Stage đầu tiên build ứng dụng, stage thứ hai chỉ chứa kết quả build.*

```dockerfile
# Stage 1: Build (Giai đoạn build)
# Sử dụng image đầy đủ với npm, node để build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production (Giai đoạn production)
# Sử dụng image Alpine siêu nhẹ, chỉ copy kết quả build
FROM node:18-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/server.js"]
```

**Giải thích (Explanation):**

- `FROM node:18 AS builder`: Tạo stage tên "builder" với Node.js đầy đủ.
- `COPY --from=builder`: Copy files từ stage "builder" sang stage hiện tại. Đây là "bí quyết" của multi-stage.
- `node:18-alpine`: Image production chỉ ~50MB thay vì ~900MB của image đầy đủ.

#### Advanced Multi-stage with Multiple Targets (Multi-stage nâng cao với nhiều targets)

In real projects, you need different images for different environments. Multi-stage builds let you create multiple "target" outputs from one Dockerfile.

*Trong dự án thực tế, bạn cần images khác nhau cho các môi trường khác nhau. Multi-stage builds cho phép tạo nhiều "target" từ một Dockerfile.*

```dockerfile
# Base stage
FROM node:18-alpine AS base
WORKDIR /app
COPY package*.json ./

# Development stage
FROM base AS development
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]

# Build stage
FROM base AS build
RUN npm ci
COPY . .
RUN npm run build

# Test stage
FROM build AS test
RUN npm test

# Production stage
FROM node:18-alpine AS production
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
USER node
CMD ["node", "dist/server.js"]
```

```bash
# Build specific target
docker build --target development -t myapp:dev .
docker build --target production -t myapp:prod .
```

---

### 2. Image Optimization (Tối ưu hóa Image)

Smaller images = faster deployment, less storage, smaller attack surface. Here are key optimization techniques.

*Image nhỏ hơn = deploy nhanh hơn, ít tốn storage, ít lỗ hổng hơn. Dưới đây là các kỹ thuật tối ưu chính.*

#### Layer Optimization (Tối ưu hóa Layers)

Each `RUN`, `COPY`, `ADD` creates a layer. Combine them to reduce image size.

*Mỗi lệnh `RUN`, `COPY`, `ADD` tạo một layer. Gộp chúng lại để giảm kích thước image.*

```dockerfile
# ❌ Bad - Creates unnecessary layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get clean

# ✅ Good - Single layer, clean in same layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

#### Leverage Build Cache (Tận dụng Build Cache)

Docker caches layers. Order your Dockerfile so rarely-changing files come first.

*Docker cache các layers. Sắp xếp Dockerfile sao cho file ít thay đổi được copy trước.*

```dockerfile
# ✅ Copy dependency files first
COPY package*.json ./
RUN npm ci

# Then copy source (changes more frequently)
COPY . .
```

#### Use .dockerignore (Sử dụng .dockerignore)

Like `.gitignore`, this file tells Docker what NOT to copy into the build context. This speeds up builds and keeps secrets out.

*Giống `.gitignore`, file này cho Docker biết KHÔNG copy gì vào build context. Giúp build nhanh hơn và không lộ secrets.*

```dockerignore
# .dockerignore
node_modules
npm-debug.log
Dockerfile
.dockerignore
.git
.gitignore
README.md
.env
coverage
tests
*.md
```

#### Choose Right Base Image (Chọn Base Image phù hợp)

The base image dramatically affects your final image size. Choose the smallest that works.

*Base image ảnh hưởng lớn đến kích thước cuối cùng. Chọn image nhỏ nhất có thể hoạt động.*

```dockerfile
# Size comparison:
# node:18          ~900MB
# node:18-slim     ~200MB
# node:18-alpine   ~120MB

# For production, prefer alpine or distroless
FROM node:18-alpine
# or
FROM gcr.io/distroless/nodejs18-debian11
```

---

### 3. BuildKit Features (Tính năng BuildKit)

BuildKit is Docker's next-generation build engine. It's faster, more efficient, and has better caching.

*BuildKit là engine build thế hệ mới của Docker. Nhanh hơn, hiệu quả hơn, và cache tốt hơn.*

#### Enable BuildKit (Bật BuildKit)

```bash
# Environment variable
export DOCKER_BUILDKIT=1
docker build .

# Or in daemon.json
{
  "features": {
    "buildkit": true
  }
}
```

#### Cache Mounts (Mount Cache)

Persist cache between builds to speed up repeated builds significantly.

*Lưu cache giữa các lần build để tăng tốc build đáng kể.*

```dockerfile
# Cache npm packages
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Cache apt packages
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y git
```

#### Secret Mounts (Mount Secrets)

Mount secrets during build without storing them in the final image. Essential for private npm packages.

*Mount secrets khi build mà không lưu vào image cuối. Cần thiết cho npm packages riêng.*

```dockerfile
# Mount secrets during build (not stored in image)
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci
```

```bash
docker build --secret id=npmrc,src=$HOME/.npmrc .
```

#### SSH Mounts (Mount SSH Keys)

Use SSH keys to clone private repositories during build.

*Sử dụng SSH keys để clone private repos khi build.*

```dockerfile
# Clone private repos
RUN --mount=type=ssh \
    git clone git@github.com:private/repo.git
```

```bash
docker build --ssh default .
```

---

### 4. Security Best Practices (Thực hành bảo mật tốt nhất)

Secure images are critical in production. Here are essential practices.

*Images bảo mật rất quan trọng trong production. Dưới đây là các thực hành cần thiết.*

#### Run as Non-root User (Chạy với user không phải root)

Running as root inside containers is a security risk. Always create and use a non-root user.

*Chạy với quyền root trong container là rủi ro bảo mật. Luôn tạo và dùng user không phải root.*

```dockerfile
# Create user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Change ownership
COPY --chown=appuser:appgroup . .

# Switch user
USER appuser

CMD ["node", "server.js"]
```

#### Use Read-only Filesystem (Sử dụng Filesystem chỉ đọc)

Mount the container filesystem as read-only to prevent attackers from modifying files.

*Mount filesystem của container ở chế độ chỉ đọc để ngăn attacker sửa đổi files.*

```bash
docker run --read-only \
  --tmpfs /tmp \
  --tmpfs /var/run \
  myapp
```

#### Scan for Vulnerabilities (Quét lỗ hổng bảo mật)

Regularly scan images for known vulnerabilities before deploying.

*Thường xuyên quét images để tìm lỗ hổng trước khi deploy.*

```bash
# Docker Scout (built-in)
docker scout cves myimage:tag

# Trivy
trivy image myimage:tag

# Snyk
snyk container test myimage:tag
```

#### Minimal Base Images (Base Images tối giản)

Fewer packages = fewer vulnerabilities. Distroless and scratch images have minimal attack surface.

*Ít packages = ít lỗ hổng. Images distroless và scratch có bề mặt tấn công tối thiểu.*

```dockerfile
# Use distroless for minimal attack surface
FROM gcr.io/distroless/static-debian11

# Or scratch for Go binaries
FROM scratch
COPY myapp /myapp
CMD ["/myapp"]
```

#### Don't Store Secrets in Images (Không lưu Secrets trong Images)

Never hardcode secrets in Dockerfiles. Inject them at runtime instead.

*Không bao giờ hardcode secrets trong Dockerfile. Inject chúng khi chạy.*

```dockerfile
# ❌ Bad
ENV API_KEY=secret123

# ✅ Good - Use runtime injection
# docker run -e API_KEY=secret123 myapp
```

---

### 5. Health Checks (Kiểm tra sức khỏe)

Health checks tell Docker whether your container is working properly. Essential for orchestrators like Kubernetes.

*Health checks cho Docker biết container có hoạt động đúng không. Cần thiết cho orchestrators như Kubernetes.*

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Or with wget (for alpine)
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/health || exit 1
```

---

### 6. Resource Limits (Giới hạn tài nguyên)

Limit container resources to prevent one container from consuming all host resources.

*Giới hạn tài nguyên container để ngăn một container tiêu thụ hết tài nguyên host.*

```bash
# Memory limit
docker run -m 512m myapp

# CPU limit
docker run --cpus=".5" myapp

# Combined
docker run -m 512m --cpus="1" myapp
```

```yaml
# docker-compose.yml
services:
  app:
    image: myapp
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

---

### 7. Debugging Containers

```bash
# Execute into running container
docker exec -it container_name sh

# View logs
docker logs -f container_name

# Inspect container
docker inspect container_name

# View processes
docker top container_name

# View resource usage
docker stats container_name

# Copy files from container
docker cp container_name:/path/to/file ./local/path

# View filesystem changes
docker diff container_name
```

#### Debug Crashed Container

```bash
# Run with shell to debug
docker run -it --entrypoint sh myimage

# Start stopped container for debugging
docker commit crashed_container debug_image
docker run -it debug_image sh
```

---

### 8. Docker Internals

#### Namespaces

- **PID**: Process isolation
- **NET**: Network isolation
- **MNT**: Filesystem isolation
- **UTS**: Hostname isolation
- **IPC**: Inter-process communication
- **USER**: User isolation

#### Control Groups (cgroups)

- Resource limiting (CPU, memory)
- Prioritization
- Accounting
- Control

#### Union Filesystem

- Layered filesystem
- Copy-on-write
- Image layers are read-only
- Container layer is writable

---

## 🛠️ Best Practices Summary (Tóm tắt thực hành tốt nhất)

| Practice (Thực hành) | Description (Mô tả) |
|----------------------|---------------------|
| Multi-stage builds | Separate build and runtime (Tách biệt build và runtime) |
| Alpine/Distroless | Minimal base images (Image nền tối giản) |
| Non-root user | Security (Bảo mật) |
| .dockerignore | Smaller build context (Context build nhỏ hơn) |
| Layer ordering | Better cache utilization (Tận dụng cache tốt hơn) |
| Health checks | Container health monitoring (Giám sát sức khỏe container) |
| Resource limits | Prevent resource exhaustion (Ngăn chặn cạn kiệt tài nguyên) |
| Image scanning | Security vulnerabilities (Lỗ hổng bảo mật) |

---

## 📖 Resources

- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [BuildKit Documentation](https://docs.docker.com/build/buildkit/)
- [Docker Security](https://docs.docker.com/engine/security/)

---

## 📝 Module Files (Các file trong Module)

| File | Description (Mô tả) |
|------|---------------------|
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Practice exercises (Bài tập) |
| [PROJECT.md](./PROJECT.md) | Mini project (Dự án nhỏ) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Solutions (Đáp án) |
| [CHEATSHEET.md](./CHEATSHEET.md) | Quick reference (Tra cứu nhanh) |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [Track 1 Capstone](../../Track1_Foundation_StaticWeb/1.8_Capstone_Project/) | **2.1 Docker Advanced** | [2.2 Docker Compose](../2.2_Docker_Compose/) |

---

**Level up your Docker skills! 🐳**

*Nâng cấp kỹ năng Docker của bạn!*

</div>
