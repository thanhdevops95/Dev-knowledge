# 🐳 Docker — Tài Nguyên Bổ Sung

---

## 📚 Official Documentation

| Resource | Link |
|----------|------|
| Docker Docs (Main) | https://docs.docker.com/ |
| Dockerfile Reference | https://docs.docker.com/engine/reference/builder/ |
| Docker CLI Reference | https://docs.docker.com/engine/reference/commandline/cli/ |
| Docker Compose | https://docs.docker.com/compose/ |
| Docker Hub | https://hub.docker.com/ |
| Best Practices | https://docs.docker.com/develop/develop-images/dockerfile_best-practices/ |

---

## 📖 Articles & Tutorials

| Title | Link | Level |
|-------|------|-------|
| Docker — From Zero to Hero | https://docker-curriculum.com/ | Beginner |
| Play with Docker (Interactive Labs) | https://labs.play-with-docker.com/ | All |
| Dockerfile Best Practices | https://docs.docker.com/develop/develop-images/dockerfile_best-practices/ | Intermediate |
| Multi-stage builds deep dive | https://docs.docker.com/build/building/multi-stage/ | Intermediate |
| Docker Security Best Practices | https://docs.docker.com/engine/security/security/ | Advanced |

---

## 🎥 Video Tutorials

| Title | Channel | Link |
|-------|---------|------|
| Docker Tutorial for Beginners | TechWorld with Nana | YouTube |
| Docker & Kubernetes — Full Course | freeCodeCamp | YouTube |
| Docker Compose Crash Course | NetworkChuck | YouTube |

---

## 📚 Books

- "The Docker Book" by James Turnbull & Jez Humble
- "Docker Deep Dive" by Nigel Poulton
- "Docker in Action" by Jeff Nickoloff & Stephen Kuenzli

---

## 🛠️ Tools & Utilities

| Tool | Purpose |
|------|---------|
| **Dive** | Analyze Docker image layers, size optimization |
| **Hadolint** | Dockerfile linter (best practices checker) |
| **Docker Slim** | Minify and secure Docker images |
| **Trivy** | Vulnerability scanner for containers |

---

## 💡 Cheatsheet

### Docker Commands Quick Reference

```bash
# Images
docker images                    # List images
docker pull <image>              # Pull image
docker build -t name .           # Build image
docker tag <src> <dest>          # Tag image
docker push <image>              # Push to registry
docker rmi <image>               # Remove image

# Containers
docker ps                        # List running
docker ps -a                     # List all
docker run <image>               # Create & start
docker run -d -p 8080:80 <image> # Run detached with port
docker exec -it <c> /bin/bash    # Exec into container
docker logs <c>                  # View logs
docker logs -f <c>               # Follow logs
docker stop <c>                  # Stop container
docker start <c>                 # Start stopped
docker rm <c>                    # Remove container
docker rm -f <c>                 # Force remove (if running)

# System
docker info                      # System info
docker system df                 # Disk usage
docker system prune -a           # Clean unused
```

---

## 🏷️ Docker Image Tags Explained

| Tag | Meaning | Use Case |
|-----|---------|----------|
| `latest` | Latest stable release (unreliable) | Development only |
| `alpine` | Alpine Linux base (small) | Production (if compatible) |
| `slim` | Debian-based, smaller than default | Production |
| `-buster` / `-bullseye` | Debian version | Production (specific OS) |
| `-vX.Y.Z` | Exact version | Production (reproducible) |
| `-dev` / `-testing` | Development builds | Testing only |

**Rule of thumb:** Never use `latest` in production. Pin to specific version.

---

## 🔒 Security Checklist

- [ ] Use non-root user (`USER` directive)
- [ ] Scan images for vulnerabilities (`trivy image <image>`)
- [ ] Keep base images updated
- [ ] Use multi-stage builds to exclude build tools
- [ ] Set resource limits (`--memory`, `--cpus`)
- [ ] Avoid storing secrets in images (use Docker secrets or env at runtime)
- [ ] Use `.dockerignore` to exclude sensitive files
- [ ] Read-only filesystem (`--read-only` flag) if possible
- [ ] Drop capabilities (`--cap-drop ALL`) nếu không cần
- [ ] Regular security updates

---

## 🐛 Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "port already allocated" | Port in use | `lsof -i :PORT` → kill process or use different port |
| "no space left on device" | Disk full | `docker system prune -a` |
| "permission denied" (Linux) | Not in docker group | `sudo usermod -aG docker $USER` + logout |
| Container exits immediately | Process ended | Check `docker logs`, use `docker run -it` for debugging |
| Slow builds | Poor Dockerfile order | Optimize layer caching (COPY deps first) |
| Large image size | Not using multi-stage | Implement multi-stage build |

---

## 🔄 Docker vs Alternatives

| Tool | Type | Pros | Cons |
|------|------|------|------|
| **Docker** | Container runtime | Mature, rich ecosystem, easy to use | Linux-only kernel, daemon runs as root |
| **Podman** | Daemonless container engine | Rootless by default, Docker-compatible | Younger ecosystem |
| **Buildah** | Image builder | Part of Podman ecosystem, flexible | CLI different from Docker |
| **Kaniko** | Build images in Kubernetes | No Docker daemon needed | Slower, specific to K8s |

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
