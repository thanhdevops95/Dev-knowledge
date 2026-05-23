# 🔬 Labs: Docker Advanced

> **Hands-on Labs for Advanced Docker**
>
> *Bài thực hành Docker nâng cao.*

---

## 🔬 Lab 1: Multi-stage Builds

### Objective

Create optimized Docker image with multi-stage build.

*(Tạo optimized Docker image với multi-stage build.)*

### Steps

#### Step 1: Create Node.js App

```bash
mkdir docker-advanced-lab && cd docker-advanced-lab
npm init -y
```

```javascript
// server.js
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ status: 'ok', message: 'Docker Advanced Lab' }));
});

server.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

#### Step 2: Create Single-stage Dockerfile (for comparison)

*(Tạo Dockerfile đơn tầng - để so sánh)*

```dockerfile
# Dockerfile.single
FROM node:18

WORKDIR /app
COPY . .
RUN npm install

EXPOSE 3000
CMD ["node", "server.js"]
```

#### Step 3: Create Multi-stage Dockerfile

*(Tạo Dockerfile đa tầng)*

```dockerfile
# Dockerfile.multi
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:18-alpine
WORKDIR /app

# Create non-root user
RUN addgroup -S app && adduser -S app -G app

# Copy from builder
COPY --from=builder /app/node_modules ./node_modules
COPY --chown=app:app server.js ./

USER app
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

CMD ["node", "server.js"]
```

#### Step 4: Build and Compare

*(Build và so sánh)*

```bash
# Build both images
docker build -f Dockerfile.single -t app:single .
docker build -f Dockerfile.multi -t app:multi .

# Compare sizes
docker images | grep app
# app   single   ~950MB
# app   multi    ~180MB
```

#### Step 5: Test

*(Kiểm tra)*

```bash
docker run -d -p 3000:3000 --name test-app app:multi
curl http://localhost:3000
docker stop test-app && docker rm test-app
```

---

## 🔬 Lab 2: BuildKit Features

### Objective

Use BuildKit cache mounts and secret mounts.

*(Sử dụng tính năng cache và secret của BuildKit.)*

### Steps

#### Step 1: Enable BuildKit

*(Bật BuildKit)*

```bash
export DOCKER_BUILDKIT=1
```

#### Step 2: Create Dockerfile with Cache Mount

*(Tạo Dockerfile với Cache Mount)*

```dockerfile
# Dockerfile.buildkit
# syntax=docker/dockerfile:1.4

FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

# Cache npm packages
RUN --mount=type=cache,target=/root/.npm \
    npm ci

COPY . .

CMD ["node", "server.js"]
```

#### Step 3: Build with Cache

*(Build với Cache)*

```bash
# First build
docker build -f Dockerfile.buildkit -t app:cached .

# Modify package.json slightly
echo '{"version": "1.0.1"}' > package.json

# Second build - npm cache will be reused
docker build -f Dockerfile.buildkit -t app:cached .
```

#### Step 4: Secret Mount Example

*(Ví dụ Secret Mount)*

```dockerfile
# Dockerfile.secret
# syntax=docker/dockerfile:1.4

FROM node:18-alpine

WORKDIR /app

# Mount secret during build
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    echo "Secret mounted successfully"

COPY . .
CMD ["node", "server.js"]
```

```bash
# Create example npmrc
echo "//registry.npmjs.org/:_authToken=fake-token" > .npmrc

# Build with secret
docker build --secret id=npmrc,src=.npmrc -f Dockerfile.secret -t app:secret .

# Verify secret is not in image
docker history app:secret
```

---

## 🔬 Lab 3: Security Hardening

### Objective

Apply security best practices to Docker image.

*(Áp dụng các thực hành bảo mật tốt nhất cho Docker image.)*

### Steps

#### Step 1: Create Secure Dockerfile

*(Tạo Dockerfile bảo mật)*

```dockerfile
# Dockerfile.secure
FROM node:18-alpine

# Create non-root user
RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

WORKDIR /app

# Copy with proper ownership
COPY --chown=appuser:appgroup package*.json ./
RUN npm ci --only=production

COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Read-only filesystem friendly
ENV NODE_ENV=production

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

CMD ["node", "server.js"]
```

#### Step 2: Run with Security Options

*(Chạy với các tùy chọn bảo mật)*

```bash
# Build
docker build -f Dockerfile.secure -t app:secure .

# Run with security options
docker run -d \
  --name secure-app \
  --read-only \
  --tmpfs /tmp \
  --security-opt=no-new-privileges:true \
  --cap-drop=ALL \
  -p 3000:3000 \
  app:secure

# Verify user
docker exec secure-app whoami
# Output: appuser

# Test read-only
docker exec secure-app touch /test 2>&1 || echo "Read-only filesystem working"
```

#### Step 3: Scan for Vulnerabilities

*(Quét lỗ hổng bảo mật)*

```bash
# Using Docker Scout
docker scout cves app:secure

# Using Trivy (if installed)
trivy image app:secure
```

---

## 🔬 Lab 4: Resource Limits

### Objective

Set and test resource limits.

*(Thiết lập và kiểm tra giới hạn tài nguyên.)*

### Steps

#### Step 1: Create Memory-intensive Script

*(Tạo script ngốn RAM)*

```javascript
// memory-test.js
const array = [];
let count = 0;

setInterval(() => {
  // Allocate 10MB every second
  array.push(Buffer.alloc(10 * 1024 * 1024));
  count++;
  console.log(`Allocated ${count * 10}MB`);
}, 1000);
```

#### Step 2: Run with Memory Limit

*(Chạy với giới hạn RAM)*

```bash
# Build image
docker build -t memory-test .

# Run with 100MB limit
docker run --name mem-test -m 100m memory-test

# Watch it get OOM killed after ~10 seconds
docker logs -f mem-test
```

#### Step 3: CPU Limits

*(Giới hạn CPU)*

```bash
# Run with half CPU
docker run -d --name cpu-test --cpus=".5" myapp

# Monitor CPU usage
docker stats cpu-test
```

---

## 🔬 Lab 5: Debugging Containers

### Objective

Debug containers and troubleshoot issues.

*(Gỡ lỗi container và xử lý sự cố.)*

### Steps

#### Step 1: Create Buggy Application

*(Tạo ứng dụng lỗi)*

```javascript
// buggy.js
const http = require('http');

const server = http.createServer((req, res) => {
  if (req.url === '/crash') {
    throw new Error('Intentional crash!');
  }
  res.end('OK');
});

server.listen(3000);
console.log('Buggy server started');
```

#### Step 2: Debug Running Container

*(Debug container đang chạy)*

```bash
docker run -d --name buggy-app buggy-image

# View logs
docker logs buggy-app

# Exec into container
docker exec -it buggy-app sh

# View processes
docker top buggy-app

# Inspect container
docker inspect buggy-app | jq '.[0].State'
```

#### Step 3: Debug Crashed Container

*(Debug container bị crash)*

```bash
# Trigger crash
curl http://localhost:3000/crash

# Container will exit - check logs
docker logs buggy-app

# Create debug image from crashed container
docker commit buggy-app debug-image

# Run with shell
docker run -it --entrypoint sh debug-image

# Investigate
ls -la
cat /app/buggy.js
```

#### Step 4: Use Docker Events

*(Sử dụng Docker Events)*

```bash
# In terminal 1 - watch events
docker events

# In terminal 2 - perform actions
docker run --rm alpine echo "test"
docker run --rm alpine exit 1
```

---

## 🔬 Lab 6: Image Layer Analysis

### Objective

Analyze and optimize image layers.

*(Phân tích và tối ưu hóa các lớp Docker images.)*

### Steps

#### Step 1: View Image History

*(Xem lịch sử image)*

```bash
docker history myimage:tag

# With full commands
docker history --no-trunc myimage:tag
```

#### Step 2: Use Dive Tool

*(Sử dụng công cụ Dive)*

```bash
# Install dive
# macOS: brew install dive
# Linux: https://github.com/wagoodman/dive

# Analyze image
dive myimage:tag
```

#### Step 3: Optimize Layers

*(Tối ưu hóa các lớp)*

```dockerfile
# Before: 5 layers for apt
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y wget
RUN apt-get install -y git
RUN apt-get clean

# After: 1 layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl wget git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

---

## ✅ Lab Completion Checklist

- [ ] Lab 1: Multi-stage Builds
- [ ] Lab 2: BuildKit Features
- [ ] Lab 3: Security Hardening
- [ ] Lab 4: Resource Limits
- [ ] Lab 5: Debugging Containers
- [ ] Lab 6: Image Layer Analysis

---

**[← Back to README](./README.md)** | **[Go to Quiz →](./QUIZ.md)**
