# Module 05: DOCKER BASICS - Containerization Fundamentals

> **Thời gian học:** 2 tuần
>
> **Prerequisite:** Module 01 (Linux), Module 04 (HTML/CSS/JS)
>
> **Difficulty:** ⭐⭐⭐☆☆

---

## 📋 Mục lục

1. [Containerization là gì?](#1-containerization-là-gì)
2. [Docker Architecture](#2-docker-architecture)
3. [Images & Containers](#3-images--containers)
4. [Dockerfile - Build Images](#4-dockerfile---build-images)
5. [Docker Networking](#5-docker-networking)
6. [Docker Volumes](#6-docker-volumes)
7. [Docker Compose](#7-docker-compose)
8. [Best Practices](#8-best-practices)
9. [Troubleshooting](#9-troubleshooting)

---

## 🎯 Learning Objectives

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu **Containerization vs Virtualization** và tại sao containers phổ biến
- ✅ Nắm vững **Docker architecture** (daemon, CLI, registry)
- ✅ Phân biệt **image vs container**
- ✅ Viết **Dockerfile** để build custom images
- ✅ Áp dụng **multi-stage builds** để tối ưu image size
- ✅ Quản lý **networking** giữa containers
- ✅ Sử dụng **volumes** để persist data
- ✅ Orchestrate nhiều containers với **Docker Compose**
- ✅ Containerize landing page từ Module 04

---

## 1. Containerization là gì?

### 1.1. Vấn đề trước khi có Containers

**"It works on my machine" problem:**

```
Developer:
- Laptop: macOS, Python 3.9, Library version 1.2
- Code chạy perfect: ✅

Tester:
- Desktop: Windows, Python 3.7, Library version 1.0
- Code crash: ❌

Production Server:
- Linux, Python 3.8, Library version 1.3
- Lỗi khác: ❌
```

**Root causes (nguyên nhân gốc):**

- Môi trường khác nhau (OS, dependencies, versions)
- Thiếu dependencies (library chưa cài)
- Conflict giữa apps (2 apps cần 2 versions khác nhau của cùng library)
- Configuration khác nhau

**Traditional solution - Virtual Machines (VMs):**

```
Physical Server
├── Hypervisor (VMware, VirtualBox)
    ├── VM 1: Full Windows 10 (5 GB disk, 2 GB RAM)
    ├── VM 2: Full Ubuntu 20.04 (4 GB disk, 2 GB RAM)
    └── VM 3: Full CentOS (4 GB disk, 2 GB RAM)

Total overhead: 13 GB disk, 6 GB RAM chỉ cho OS!
```

**Problems với VMs:**

- ❌ Nặng: Mỗi VM cần full OS (GBs)
- ❌ Chậm: Boot time 30-60 giây
- ❌ Resource intensive: Cần nhiều RAM, CPU
- ❌ Portability limited: VM images rất lớn (10-20 GB)

### 1.2. Container Solution

**Container = Lightweight, portable, self-sufficient package chứa:**

- Application code
- Dependencies (libraries, runtimes)
- Configuration files
- Environment variables

**Key difference (sự khác biệt chính):**

```
Virtual Machine:
┌─────────────────────────────┐
│  App A     App B     App C  │
│  ────────────────────────   │
│  Bins/Libs  Bins/Libs       │
│  ────────────────────────   │
│  Guest OS   Guest OS  ...   │  ← Mỗi VM có full OS
│─────────────────────────────│
│      Hypervisor             │
│─────────────────────────────│
│      Host OS                │
│─────────────────────────────│
│      Hardware               │
└─────────────────────────────┘

Container:
┌─────────────────────────────┐
│  App A     App B     App C  │
│  ────────────────────────   │
│  Bins/Libs  Bins/Libs       │  ← Chỉ cần libs cần thiết
│─────────────────────────────│
│  Container Runtime (Docker) │
│─────────────────────────────│
│      Host OS (Linux kernel) │  ← Share chung kernel
│─────────────────────────────│
│      Hardware               │
└─────────────────────────────┘
```

**Container advantages:**

| Aspect | Virtual Machine | Container |
|--------|----------------|-----------|
| **Size** | GBs (5-20 GB) | MBs (50-500 MB) |
| **Startup** | Minutes | Seconds (< 1s) |
| **Performance** | Slower (overhead) | Near-native |
| **Isolation** | Complete (hardware-level) | Process-level |
| **Portability** | Limited | Excellent |
| **Density** | 10-20 VMs/host | 100+ containers/host |

**Example real numbers:**

```bash
# VM Ubuntu
Size: ~4 GB
Boot time: 45 seconds
Memory: 512 MB minimum

# Container Ubuntu (Alpine Linux base)
Size: ~5 MB
Start time: < 1 second  
Memory: ~10 MB
```

### 1.3. Use Cases

**Khi nào dùng Containers:**

- ✅ Microservices architecture (nhiều services nhỏ)
- ✅ CI/CD pipelines (build, test, deploy tự động)
- ✅ Development environments (đảm bảo consistency)
- ✅ Application portability (chạy ở đâu cũng giống nhau)
- ✅ Scaling (tăng/giảm số containers dễ dàng)

**Khi nào dùng VMs:**

- ✅ Cần full OS isolation (security-critical apps)
- ✅ Chạy different OS kernels (Windows app trên Linux host)
- ✅ Legacy applications (không thể containerize)
- ✅ Compliance requirements (yêu cầu isolated environments)

**Kết hợp cả hai:**

```
Physical Server
└── VM (Ubuntu)
    └── Docker Engine
        ├── Container 1 (NodeJS app)
        ├── Container 2 (Python app)
        └── Container 3 (Database)
```

---

## 2. Docker Architecture

### 2.1. Docker là gì?

**Docker:**

- Platform để build, ship, run containers
- Ra mắt năm 2013 bởi Solomon Hykes
- Open source, viết bằng Go
- De facto standard cho containerization

**Docker không phải:**

- ❌ Ngôn ngữ lập trình
- ❌ Cloud provider
- ❌ Virtual machine
- ❌ Chỉ cho Linux (có Docker Desktop cho Windows/macOS)

### 2.2. Docker Components

**Client-Server Architecture:**

```
┌──────────────────────────────────────────────────┐
│  Docker Client (CLI)                             │
│  $ docker run nginx                              │
│  $ docker build -t myapp .                       │
└──────────────┬───────────────────────────────────┘
               │ REST API
               ↓
┌──────────────────────────────────────────────────┐
│  Docker Daemon (dockerd)                         │
│  - Manages containers, images, networks, volumes│
│  - Listens on socket: /var/run/docker.sock      │
└──────────────┬───────────────────────────────────┘
               │
        ┌──────┴──────┬──────────────┐
        ↓             ↓              ↓
   Containers      Images         Networks
```

**1. Docker Client (CLI - Command Line Interface):**

- Interface để user tương tác với Docker
- Send commands to Docker daemon
- CLI hoặc GUI (Docker Desktop)

```bash
docker run nginx
docker ps
docker build -t myapp .
```

**2. Docker Daemon (dockerd):**

- Background service chạy trên host
- Quản lý: containers, images, networks, volumes
- Lắng nghe Docker API requests
- Build, run, distribute containers

**3. Docker Registry:**

- Repository lưu trữ Docker images
- Public: Docker Hub (hub.docker.com)
- Private: AWS ECR, Google GCR, Harbor, GitLab Registry

```bash
# Pull image từ Docker Hub
docker pull nginx:latest

# Push image lên Docker Hub
docker push username/myapp:v1.0
```

**4. Docker Images:**

- Read-only template để tạo containers
- Chứa: OS, application code, dependencies
- Layered filesystem (mỗi layer là 1 thay đổi)
- Immutable (không thay đổi được sau khi build)

**5. Docker Containers:**

- Running instance của image
- Isolated process với own filesystem, network, process tree
- Ephemeral (có thể xóa và tạo lại bất kỳ lúc nào)
- Multiple containers có thể chạy từ cùng 1 image

### 2.3. Installation

**Linux (Ubuntu):**

```bash
# Update packages
sudo apt update

# Install dependencies
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y

# Add Docker's GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io -y

# Add user to docker group (không cần sudo)
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker --version
docker run hello-world
```

**macOS / Windows:**

```
1. Download Docker Desktop from docker.com
2. Install
3. Launch Docker Desktop
4. Verify in terminal: docker --version
```

**Verify installation:**

```bash
# Check version
docker --version
# Output: Docker version 24.0.6, build ed223bc

# Run test container
docker run hello-world

# Output:
# Hello from Docker!
# This message shows that your installation appears to be working correctly.
```

---

## 3. Images & Containers

### 3.1. Docker Images

**Image = Snapshot của filesystem + metadata**

**Layered Architecture:**

```
Image: nginx:latest
├── Layer 5: nginx config      (2 MB)
├── Layer 4: nginx binary       (50 MB)
├── Layer 3: Dependencies       (30 MB)
├── Layer 2: Ubuntu packages    (70 MB)
└── Layer 1: Base Ubuntu        (100 MB)
                Total: ~250 MB
```

**Why layers (tại sao dùng layers):**

- ✅ Caching: Reuse unchanged layers khi rebuild
- ✅ Sharing: Multiple images share common base layers
- ✅ Efficient transfer: Chỉ pull layers chưa có

**Example - 2 images share layers:**

```
Image A (NodeJS app):
├── Layer 3: App code A    (10 MB)
├── Layer 2: Node modules  (150 MB)  ← Shared
└── Layer 1: Ubuntu base   (100 MB)  ← Shared

Image B (Python app):
├── Layer 3: App code B    (15 MB)
├── Layer 2: pip packages  (80 MB)
└── Layer 1: Ubuntu base   (100 MB)  ← Shared

Disk usage: 10 + 150 + 100 + 15 + 80 = 355 MB
(Not 260 + 195 = 455 MB, saved 100 MB do shared base layer)
```

### 3.2. Working with Images

**Pull images từ Docker Hub:**

```bash
# Latest version
docker pull nginx

# Specific version (tag)
docker pull nginx:1.25
docker pull nginx:alpine

# From specific registry
docker pull gcr.io/google-containers/nginx
```

**List local images:**

```bash
docker images

# Output:
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
nginx        latest    f9c14fe76d50   2 weeks ago    143MB
nginx        alpine    8e75cbc5b25c   2 weeks ago    41MB
ubuntu       22.04     08d22c0ceb15   1 month ago    77.8MB
```

**Inspect image:**

```bash
docker inspect nginx

# Specific info
docker inspect --format='{{.Config.Cmd}}' nginx
docker inspect --format='{{.Config.ExposedPorts}}' nginx
```

**Remove image:**

```bash
# Remove by name
docker rmi nginx:alpine

# Remove by ID
docker rmi f9c14fe76d50

# Remove unused images
docker image prune

# Remove all images (CAREFUL!)
docker rmi $(docker images -q)
```

### 3.3. Working with Containers

**Run container:**

```bash
# Basic run
docker run nginx

# Detached (background)
docker run -d nginx

# With name
docker run -d --name my-nginx nginx

# Port mapping (host:container)
docker run -d -p 8080:80 nginx
# Truy cập: http://localhost:8080

# Environment variables
docker run -d -e DB_HOST=localhost -e DB_PORT=5432 myapp

# Interactive terminal
docker run -it ubuntu bash
# -i: interactive
# -t: terminal
```

**List containers:**

```bash
# Running containers
docker ps

# All containers (cả đã dừng)
docker ps -a

# Output:
CONTAINER ID   IMAGE    COMMAND                  STATUS         PORTS                  NAMES
abc123def456   nginx    "/docker-entrypoint.…"   Up 5 minutes   0.0.0.0:8080->80/tcp   my-nginx
```

**Container lifecycle:**

```bash
# Start stopped container
docker start my-nginx

# Stop running container
docker stop my-nginx

# Restart container
docker restart my-nginx

# Pause (freeze process)
docker pause my-nginx

# Unpause
docker unpause my-nginx

# Kill (force stop)
docker kill my-nginx

# Remove container
docker rm my-nginx

# Remove running container (force)
docker rm -f my-nginx
```

**Execute commands trong running container:**

```bash
# Interactive shell
docker exec -it my-nginx bash

# Single command
docker exec my-nginx ls /usr/share/nginx/html

# As different user
docker exec -u root my-nginx whoami
```

**View logs:**

```bash
# All logs
docker logs my-nginx

# Follow (real-time)
docker logs -f my-nginx

# Last 100 lines
docker logs --tail 100 my-nginx

# Since timestamp
docker logs --since 2024-12-25T10:00:00 my-nginx
```

**Container stats:**

```bash
# Real-time stats
docker stats

# Specific container
docker stats my-nginx

# Output:
CONTAINER  CPU %   MEM USAGE / LIMIT   MEM %   NET I/O      BLOCK I/O
my-nginx   0.02%   3.5MiB / 7.77GiB    0.04%   1.2kB/648B   0B/8.19kB
```

**Cleanup:**

```bash
# Stop all running containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all: containers, images, networks, volumes (CAREFUL!)
docker system prune -a --volumes

# Check disk usage
docker system df
```

---

## 4. Dockerfile - Build Images

### 4.1. Dockerfile là gì?

**Dockerfile:**

- Text file chứa instructions để build image
- Mỗi instruction tạo 1 layer trong image
- Automated, reproducible, version-controlled

**Basic structure:**

```dockerfile
# Base image
FROM ubuntu:22.04

# Maintainer info
LABEL maintainer="your@email.com"

# Run commands
RUN apt-get update && apt-get install -y nginx

# Set working directory
WORKDIR /app

# Copy files from host to image
COPY index.html /usr/share/nginx/html/

# Environment variables
ENV PORT=80

# Expose port
EXPOSE 80

# Command to run khi container starts
CMD ["nginx", "-g", "daemon off;"]
```

### 4.2. Dockerfile Instructions

**FROM - Base image:**

```dockerfile
# Official base images
FROM ubuntu:22.04
FROM node:18-alpine
FROM python:3.11

# Scratch (empty base, for compiled binaries)
FROM scratch
```

**RUN - Execute commands khi build:**

```dockerfile
# Shell form
RUN apt-get update

# Exec form
RUN ["/bin/bash", "-c", "echo hello"]

# Multiple commands (chain with &&)
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*
```

**COPY - Copy files từ host vào image:**

```dockerfile
# Copy single file
COPY index.html /usr/share/nginx/html/

# Copy directory
COPY ./src /app/src

# Copy all
COPY . /app/

# Copy with different permissions
COPY --chown=node:node package*.json /app/
```

**ADD - Like COPY nhưng có extra features:**

```dockerfile
# Auto-extract tar files
ADD archive.tar.gz /app/

# Download from URL (không recommended, dùng RUN + curl thay vào)
ADD https://example.com/file.txt /app/
```

**Best practice:** Dùng COPY thay vì ADD (trừ khi cần auto-extract)

**WORKDIR - Set working directory:**

```dockerfile
WORKDIR /app

# All subsequent commands run trong /app
RUN npm install
COPY . .
```

**ENV - Set environment variables:**

```dockerfile
ENV NODE_ENV=production
ENV PORT=3000
ENV DB_HOST=localhost

# Multiple in one line
ENV NODE_ENV=production \
    PORT=3000 \
    DB_HOST=localhost
```

**EXPOSE - Document port (không publish ra host):**

```dockerfile
EXPOSE 80
EXPOSE 443
EXPOSE 3000
```

**CMD - Default command khi container start:**

```dockerfile
# Exec form (preferred)
CMD ["nginx", "-g", "daemon off;"]

# Shell form
CMD nginx -g "daemon off;"

# Chỉ có thể có 1 CMD, nếu nhiều thì chỉ CMD cuối được execute
```

**ENTRYPOINT - Command luôn chạy:**

```dockerfile
ENTRYPOINT ["nginx"]

# Combine với CMD
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]

# docker run myimage → nginx -g daemon off;
# docker run myimage -h → nginx -h
```

**USER - Set user cho subsequent commands:**

```dockerfile
# Run as non-root (security best practice)
RUN useradd -m appuser
USER appuser

# All commands sau này run as appuser
```

**VOLUME - Mount point cho data persistence:**

```dockerfile
VOLUME ["/data", "/var/log"]
```

**ARG - Build-time variables:**

```dockerfile
ARG VERSION=latest
FROM node:${VERSION}

ARG PORT=3000
ENV PORT=${PORT}
```

```bash
# Pass ARG khi build
docker build --build-arg VERSION=18-alpine -t myapp .
```

### 4.3. Build Image

**Simple Dockerfile example - Static website:**

```dockerfile
# Dockerfile
FROM nginx:alpine

# Copy HTML files
COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# NGINX alpine image đã có CMD sẵn, không cần thêm
```

**Build:**

```bash
# Build với tag
docker build -t my-website .

# Build với specific tag
docker build -t my-website:v1.0 .

# Build và xem build process
docker build --progress=plain -t my-website .

# Build without cache (force rebuild all layers)
docker build --no-cache -t my-website .
```

**Run:**

```bash
docker run -d -p 8080:80 --name website my-website

# Test
curl http://localhost:8080
```

### 4.4. Multi-Stage Builds

**Problem:** Build artifacts làm image size lớn

**Example - NodeJS app:**

```dockerfile
# ❌ BAD - Single stage (large image)
FROM node:18

WORKDIR /app
COPY package*.json ./
RUN npm install  # Includes devDependencies (lớn)
COPY . .

EXPOSE 3000
CMD ["node", "server.js"]

# Image size: ~1 GB
```

**Solution - Multi-stage:**

```dockerfile
# ✅ GOOD - Multi-stage build
# Stage 1: Build
FROM node:18 AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install  # Install all dependencies
COPY . .
RUN npm run build  # Build production files

# Stage 2: Production
FROM node:18-alpine

WORKDIR /app

# Copy only necessary files từ builder stage
COPY --from=builder /app/package*.json ./
RUN npm install --only=production  # Install chỉ production deps
COPY --from=builder /app/dist ./dist

EXPOSE 3000
CMD ["node", "dist/server.js"]

# Final image size: ~150 MB (saved ~850 MB!)
```

**How it works:**

1. Stage 1 (builder): Build app với full dependencies
2. Stage 2: Copy chỉ compiled files và production deps
3. Discard stage 1 (không lưu vào final image)

**Another example - Go app:**

```dockerfile
# Stage 1: Build
FROM golang:1.21 AS builder

WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o server .

# Stage 2: Production (tiny image!)
FROM alpine:latest

RUN apk --no-cache add ca-certificates
WORKDIR /root/

# Copy chỉ binary
COPY --from=builder /app/server .

EXPOSE 8080
CMD ["./server"]

# Final size: ~10 MB (vs ~800 MB nếu dùng golang base)
```

---

## 5. Docker Networking

### 5.1. Network Types

**Docker cung cấp 4 network drivers:**

**1. Bridge (default):**

```bash
# Containers trên cùng bridge network có thể communicate
docker network create my-network
docker run -d --network my-network --name app1 nginx
docker run -d --network my-network --name app2 nginx

# app1 có thể ping app2 by name:
docker exec app1 ping app2
```

**2. Host:**

```bash
# Container share host's network namespace
docker run -d --network host nginx
# Container bind trực tiếp lên host port 80 (no port mapping needed)
```

**3. None:**

```bash
# No networking
docker run -d --network none nginx
```

**4. Overlay (for Swarm/Kubernetes):**

- Multi-host networking
- Advanced, không cover trong module này

### 5.2. Network Commands

```bash
# List networks
docker network ls

# Create network
docker network create my-network

# Inspect network
docker network inspect my-network

# Connect container to network
docker network connect my-network container1

# Disconnect
docker network disconnect my-network container1

# Remove network
docker network rm my-network
```

### 5.3. Container Communication

**By container name (DNS resolution):**

```bash
docker network create app-network

# Database
docker run -d \
  --name postgres \
  --network app-network \
  -e POSTGRES_PASSWORD=secret \
  postgres:15

# Application (connect to db bởi hostname "postgres")
docker run -d \
  --name app \
  --network app-network \
  -e DB_HOST=postgres \
  -e DB_PORT=5432 \
  myapp
```

---

## 6. Docker Volumes

### 6.1. Data Persistence

**Problem:** Container data là ephemeral (mất khi container bị xóa)

```bash
docker run -d --name db postgres
# Write data to database
docker stop db
docker rm db
# → Data lost! ❌
```

**Solution:** Volumes

### 6.2. Volume Types

**1. Named Volumes (recommended):**

```bash
# Create volume
docker volume create db-data

# Use volume
docker run -d \
  --name postgres \
  -v db-data:/var/lib/postgresql/data \
  postgres:15

# Data persists ngay cả khi remove container!
docker rm -f postgres
docker run -d --name postgres-new -v db-data:/var/lib/postgresql/data postgres:15
# → Data still there! ✅
```

**2. Bind Mounts (mount host directory):**

```bash
# Mount current directory vào container
docker run -d \
  -v $(pwd)/html:/usr/share/nginx/html \
  nginx

# Changes on host → immediately reflected in container
```

**3. tmpfs (memory only, không persist to disk):**

```bash
docker run -d --tmpfs /app/temp myapp
```

### 6.3. Volume Commands

```bash
# List volumes
docker volume ls

# Create
docker volume create my-data

# Inspect
docker volume inspect my-data

# Remove volume
docker volume rm my-data

# Remove unused volumes
docker volume prune
```

---

## 7. Docker Compose

### 7.1. Compose là gì?

**Docker Compose:**

- Tool để define và run multi-container apps
- YAML file (`docker-compose.yml`)
- Single command để start/stop entire stack

**Use case:**

```
App cần 3 services:
├── Frontend (React)
├── Backend (NodeJS API)
└── Database (PostgreSQL)

Without Compose: 3 docker run commands, manual networking
With Compose: 1 command → all services start!
```

### 7.2. docker-compose.yml Syntax

**Basic example:**

```yaml
version: '3.8'

services:
  # Service 1: Web
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
    networks:
      - app-network

  # Service 2: Database
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  db-data:
```

**Compose commands:**

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Stop all
docker-compose down

# View logs
docker-compose logs -f

# List services
docker-compose ps

# Rebuild images
docker-compose build
```

### 7.3. Full Stack Example

**Project structure:**

```
my-app/
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   └── ... (React app)
└── backend/
    ├── Dockerfile
    └── ... (NodeJS app)
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:4000
    depends_on:
      - backend
    networks:
      - app-net

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "4000:4000"
    environment:
      - DB_HOST=database
      - DB_PORT=5432
      - DB_NAME=myapp
      - DB_USER=postgres
      - DB_PASSWORD=secret
    depends_on:
      - database
    networks:
      - app-net

  database:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-net

networks:
  app-net:
    driver: bridge

volumes:
  postgres-data:
```

**Usage:**

```bash
# Start entire stack
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend

# Restart service
docker-compose restart backend

# Stop everything và remove containers
docker-compose down

# Stop và remove volumes (DELETE DATA!)
docker-compose down -v
```

---

## 8. Best Practices

### 8.1. Image Optimization

**1. Use small base images:**

```dockerfile
# ❌ Large
FROM ubuntu:22.04  # ~77 MB

# ✅ Small
FROM alpine:latest  # ~5 MB
FROM node:18-alpine  # ~150 MB vs node:18 ~1 GB
```

**2. Multi-stage builds:**

```dockerfile
# Build stage: Large
FROM node:18 AS builder
# ... build app

# Production: Small
FROM node:18-alpine
COPY --from=builder /app/dist ./dist
```

**3. Minimize layers:**

```dockerfile
# ❌ BAD - 3 layers
RUN apt-get update
RUN apt-get install -y nginx
RUN rm -rf /var/lib/apt/lists/*

# ✅ GOOD - 1 layer
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*
```

**4. Order matters (cache optimization):**

```dockerfile
# ❌ BAD - Cache invalidated mỗi lần code thay đổi
COPY . /app
RUN npm install

# ✅ GOOD - npm install cached nếu package.json không đổi
COPY package*.json /app/
RUN npm install
COPY . /app
```

### 8.2. Security

**1. Run as non-root:**

```dockerfile
FROM node:18-alpine

# Create user
RUN addgroup -g 1001 appgroup && \
    adduser -D -u 1001 -G appgroup appuser

USER appuser

WORKDIR /app
```

**2. Scan images for vulnerabilities:**

```bash
# Docker Scout
docker scout cves nginx:latest

# Trivy
trivy image nginx:latest
```

**3. Không commit secrets vào image:**

```dockerfile
# ❌ BAD
ENV DB_PASSWORD=secret123

# ✅ GOOD - Pass as runtime env var
# docker run -e DB_PASSWORD=secret myapp
```

---

## 9. Troubleshooting

### 9.1. Common Issues

**Container exited immediately:**

```bash
# Check logs
docker logs container-name

# Thường do:
# - Entrypoint/CMD error
# - Missing dependencies
# - Port already in use
```

**Cannot connect to container:**

```bash
# Check port mapping
docker ps  # Xem PORTS column

# Check from inside container
docker exec -it container-name sh
wget localhost:80

# Check networking
docker network inspect bridge
```

**"No space left on device":**

```bash
# Check disk usage
docker system df

# Clean up
docker system prune -a
docker volume prune
```

---

## 📚 Tổng kết

### Key Takeaways

1. **Containers vs VMs** - Lighter, faster, more portable
2. **Images** - Read-only templates, layered filesystem
3. **Containers** - Running instances, ephemeral
4. **Dockerfile** - Automated image building
5. **Multi-stage** - Optimize image size
6. **Networking** - Container communication
7. **Volumes** - Data persistence
8. **Compose** - Multi-container orchestration

### Checklist

- [ ] Hiểu container vs VM differences
- [ ] Pull và run images từ Docker Hub
- [ ] Viết Dockerfile và build images
- [ ] Sử dụng multi-stage builds
- [ ] Manage networks và volumes
- [ ] Viết docker-compose.yml
- [ ] Container hóa landing page từ Module 04
- [ ] Push image lên Docker Hub

### Next: Module 06 - CI_BASICS

👉 Automate Docker  builds với CI/CD!

---

> **"Build once, run anywhere." - Docker Philosophy** 🐋
