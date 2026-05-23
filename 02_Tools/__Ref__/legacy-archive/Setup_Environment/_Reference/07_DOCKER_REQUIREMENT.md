# Module 07: DOCKER & CONTAINERS

> **"Ship code như ship hộp container - đóng gói một lần, chạy mọi nơi"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu container vs VM
- ✅ Docker architecture và components
- ✅ Build custom Docker images
- ✅ Dockerfile best practices
- ✅ Multi-stage builds
- ✅ Docker Compose cho multi-container apps
- ✅ Docker networking
- ✅ Docker volumes và persistence
- ✅ Container security basics
- ✅ Container Registry (Docker Hub, ECR)

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| Container | Container | Môi trường cô lập chạy app |
| Image | Docker Image | Template để tạo container |
| Dockerfile | Dockerfile | File hướng dẫn build image |
| Layer | Image Layer | Lớp trong image |
| Registry | Container Registry | Kho chứa images |
| Repository | Repository | Tập hợp versions của image |
| Tag | Image Tag | Version của image |
| Volume | Docker Volume | Lưu trữ persistent |
| Bind Mount | Bind Mount | Mount folder host → container |
| Network | Docker Network | Mạng container |
| Bridge | Bridge Network | Mạng mặc định |
| Host | Host Network | Dùng chung network với host |
| Overlay | Overlay Network | Mạng multi-host |
| Compose | Docker Compose | Tool chạy multi-container |
| Service | Compose Service | Container trong Compose |
| Build Context | Build Context | Folder gửi cho Docker build |
| Entrypoint | Entrypoint | Lệnh chính của container |
| CMD | CMD | Arguments cho Entrypoint |
| Port Mapping | Port Mapping | Map port container → host |
| Health Check | Container Health Check | Kiểm tra container health |

---

## ✅ Checklist Labs

### Labs Docker basics

- [ ] Lab 1: Docker installation verification
- [ ] Lab 2: docker version, info, system df
- [ ] Lab 3: docker run hello-world
- [ ] Lab 4: docker run interactive (-it)
- [ ] Lab 5: docker run detached (-d)
- [ ] Lab 6: docker ps, logs, exec
- [ ] Lab 7: docker stop, kill, rm
- [ ] Lab 8: docker inspect

### Labs Docker Images

- [ ] Lab 9: docker images, pull, push
- [ ] Lab 10: docker tag
- [ ] Lab 11: docker history
- [ ] Lab 12: docker save, load, export, import
- [ ] Lab 13: Docker Hub public và private repos
- [ ] Lab 14: Clean up images (prune)

### Labs Dockerfile

- [ ] Lab 15: First Dockerfile - FROM, RUN, CMD
- [ ] Lab 16: COPY và ADD
- [ ] Lab 17: WORKDIR
- [ ] Lab 18: ENV và ARG
- [ ] Lab 19: EXPOSE
- [ ] Lab 20: USER (non-root)
- [ ] Lab 21: ENTRYPOINT vs CMD
- [ ] Lab 22: HEALTHCHECK
- [ ] Lab 23: LABEL metadata
- [ ] Lab 24: .dockerignore

### Labs Dockerfile Best Practices

- [ ] Lab 25: Layer caching optimization
- [ ] Lab 26: Multi-stage builds
- [ ] Lab 27: Minimize image size (alpine, slim)
- [ ] Lab 28: Combine RUN commands
- [ ] Lab 29: Avoid running as root
- [ ] Lab 30: Use specific tags (not latest)

### Labs Docker Networking

- [ ] Lab 31: docker network ls, create, inspect
- [ ] Lab 32: Bridge network
- [ ] Lab 33: Container-to-container communication
- [ ] Lab 34: Host network
- [ ] Lab 35: None network
- [ ] Lab 36: Port mapping (-p)
- [ ] Lab 37: DNS resolution trong Docker network

### Labs Docker Volumes

- [ ] Lab 38: docker volume create, ls, inspect
- [ ] Lab 39: Named volumes
- [ ] Lab 40: Bind mounts
- [ ] Lab 41: tmpfs mounts
- [ ] Lab 42: Volume drivers
- [ ] Lab 43: Backup volumes

### Labs Docker Compose

- [ ] Lab 44: docker-compose.yml basics
- [ ] Lab 45: docker compose up, down, ps, logs
- [ ] Lab 46: Build trong Compose
- [ ] Lab 47: Networks trong Compose
- [ ] Lab 48: Volumes trong Compose
- [ ] Lab 49: Environment variables
- [ ] Lab 50: depends_on và healthcheck
- [ ] Lab 51: Docker Compose profiles
- [ ] Lab 52: Docker Compose override files

### Labs Counter App

- [ ] Lab 53: Build Counter App image
- [ ] Lab 54: Run Counter App với Docker Compose
- [ ] Lab 55: Multi-stage build cho Counter App
- [ ] Lab 56: Push Counter App to Docker Hub

### Labs Security

- [ ] Lab 57: Scan images với docker scout
- [ ] Lab 58: Scan với Trivy
- [ ] Lab 59: Non-root container
- [ ] Lab 60: Read-only filesystem
- [ ] Lab 61: Resource limits (CPU, Memory)
- [ ] Lab 62: Capabilities management

---

## 🚨 Checklist Scenarios

### Scenarios về Container

- [ ] Scenario 1: Container exits immediately
- [ ] Scenario 2: Container runs but app không accessible
- [ ] Scenario 3: Container OOM killed
- [ ] Scenario 4: Container filesystem full
- [ ] Scenario 5: Cannot remove running container

### Scenarios về Images

- [ ] Scenario 6: docker build fails at layer
- [ ] Scenario 7: Image size quá lớn
- [ ] Scenario 8: Cache không work như expected
- [ ] Scenario 9: Cannot pull private image
- [ ] Scenario 10: Tag latest gây confusion

### Scenarios về Networking

- [ ] Scenario 11: Container không connect được internet
- [ ] Scenario 12: Container A không ping được Container B
- [ ] Scenario 13: Port already allocated
- [ ] Scenario 14: DNS resolution fails trong container
- [ ] Scenario 15: localhost trong container không là host

### Scenarios về Volumes

- [ ] Scenario 16: Data lost sau container restart
- [ ] Scenario 17: Permission denied khi write volume
- [ ] Scenario 18: Bind mount không sync
- [ ] Scenario 19: Volume orphaned sau container remove

### Scenarios về Compose

- [ ] Scenario 20: Service depends_on không work
- [ ] Scenario 21: Environment variable không load
- [ ] Scenario 22: Network conflict
- [ ] Scenario 23: Build context quá lớn, chậm

### Scenarios về Security

- [ ] Scenario 24: Root user trong container
- [ ] Scenario 25: Secrets exposed trong image layers
- [ ] Scenario 26: Vulnerable base image
- [ ] Scenario 27: Container escape attempt detected

### Scenarios về Performance

- [ ] Scenario 28: Container CPU throttling
- [ ] Scenario 29: Build cache không work
- [ ] Scenario 30: Container slow startup

---

## ⏱️ Thời lượng

**Ước tính:** 8-10 giờ

| Phần | Thời gian |
|------|-----------|
| Docker basics (Labs 1-14) | 1.5 giờ |
| Dockerfile (Labs 15-30) | 2.5 giờ |
| Networking (Labs 31-37) | 1 giờ |
| Volumes (Labs 38-43) | 1 giờ |
| Compose (Labs 44-52) | 2 giờ |
| Counter App + Security | 1.5 giờ |
| Scenarios | 1.5 giờ |

---

## 🔗 Tài liệu tham khảo

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)
- [Play with Docker](https://labs.play-with-docker.com/)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
