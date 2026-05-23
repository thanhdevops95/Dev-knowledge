# Solutions: Module 05 - DOCKER BASICS

> **Đáp Án Đầy Đủ Cho Exercises, Scenarios, và Quiz**

---

## 📋 EXERCISES SOLUTIONS

### Phần A: Trắc Nghiệm

1. **B** - Container chia sẻ kernel của host OS, VM có OS riêng
2. **D** - Cả A và B (create và run đều đúng)
3. **B** - Image là template, container là instance đang chạy
4. **C** - FROM
5. **B** - Chỉ containers đang chạy
6. **B** - `-d` (detached)
7. **B** - `-p 8080:80` (host:container)
8. **B** - Chạy background
9. **D** - Cả COPY và ADD đều hoạt động (COPY được khuyến nghị)
10. **B** - Loại files khỏi build context
11. **B** - `docker container prune`
12. **B** - Persist data ngoài container lifecycle
13. **A** - `COPY --from=stage`
14. **C** - alpine (~5MB vs 100MB+)
15. **B** - Restart khi Docker daemon start

### Phần B: Điền Vào Chỗ Trống

1. `docker ps -a`
2. `docker run -it ubuntu bash`
3. `docker build -t myapp:1.0 .`
4. `docker rm -f container_name`
5. `docker logs --tail 100 container_name`
6. `docker exec -it container_name bash`
7. `docker-compose up`
8. `docker volume create mydata`
9. `docker run -v mydata:/app/data myapp`
10. `docker stop $(docker ps -q)`

### Phần C: Viết Dockerfile

**Câu 36: Simple Python App:**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

**Câu 37: Multi-stage Node.js:**

```dockerfile
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm install --production
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

**Câu 38: Non-root User:**

```dockerfile
FROM nginx:alpine

RUN adduser -D appuser && \
    chown -R appuser:appuser /usr/share/nginx/html

USER appuser

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
```

**Câu 39: With Health Check:**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

**Câu 40: Optimized Layers:**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "app.py"]
```

**Câu 41: With Build Arguments:**

```dockerfile
ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION}-slim

ARG APP_VERSION=1.0
ENV VERSION=${APP_VERSION}

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

### Phần D: Debug Scenarios

**Câu 42: Container Won't Start:**

```bash
# Check logs
docker logs container_id

# Check exit code
docker inspect container_id | grep ExitCode

# Fix: Thêm CMD hoặc fix dependencies
```

**Câu 43: Network Connectivity:**

```bash
# Check network
docker network ls
docker network inspect bridge

# Fix: Đưa vào cùng network
docker network create mynet
docker run --network mynet --name db postgres
docker run --network mynet --name web nginx
```

**Câu 44: Volume Permissions:**

```bash
# Check ownership
ls -la ./data

# Fix trong Dockerfile:
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser
```

**Câu 45: Image Size Too Large:**

```bash
# Sử dụng multi-stage build
# Sử dụng alpine base
# Combine RUN commands
# Clean up trong cùng layer
```

**Câu 46: Port Not Accessible:**

```bash
# Check container running
docker ps

# Check port mapping
docker port container_name

# Test từ trong container
docker exec container curl localhost:80
```

**Câu 47: Compose Services Won't Communicate:**

```yaml
# Add network cho tất cả services
services:
  web:
    networks:
      - mynet
  database:
    networks:
      - mynet

networks:
  mynet:
```

**Câu 48: Slow Build Times:**

```dockerfile
# Copy dependencies trước
COPY package.json .
RUN npm install

# Copy source code sau
COPY . .
```

---

## 🎬 SCENARIOS - KEY LEARNINGS

**Scenario 1:** Luôn install dependencies trong Dockerfile  
**Scenario 2:** Define networks explicitly trong compose  
**Scenario 3:** Luôn dùng volumes cho persistent data  
**Scenario 4:** Set resource limits  
**Scenario 5:** Optimize Dockerfile layer order  
**Scenario 6:** Non-root user, không hardcode secrets  
**Scenario 7:** Blue-green cho zero-downtime  
**Scenario 8:** Production compose cần health checks  

---

## 📝 QUIZ SOLUTIONS

1. **B** - Container chia sẻ kernel, VM có full OS
2. **B** - `docker ps`
3. **B** - Detached mode (background)
4. **B** - `-p 8080:80` (host:container)
5. **B** - FROM
6. **A** - Set working directory cho instructions sau
7. **B** - Combine với && (ít layers hơn)
8. **C** - Stop, remove containers VÀ volumes
9. **C** - alpine:latest (~5MB)
10. **B** - Loại files khỏi build context
11. **B** - Dùng volumes
12. **B** - `COPY --from=stagename`
13. **B** - `--restart=unless-stopped`
14. **B** - `docker exec`
15. **B** - bridge
16. **B** - `docker container prune`
17. **B** - Document port app sử dụng
18. **C** - Dùng environment variables
19. **C** - Cả A và B đều đúng
20. **B** - `docker stats`
21. **A** - Set startup order
22. **B** - Command test container healthy
23. **C** - Specific version với slim variant
24. **B** - `docker logs container_name`
25. **B** - Image nhỏ hơn

---

## 📊 GRADING

**Exercises Total:** 200 điểm

- Phần A: 40/40
- Phần B: 30/30
- Phần C: 60/60
- Phần D: 70/70

**Quiz Total:** 25 điểm

**Đánh giá:**

- 200+ điểm: Docker Expert
- 160-199: Proficient
- 140-159: Competent
- <140: Cần review lại

---

**Review solutions để học từ mistakes! 📚**

**Docker mastery cần practice! 🐳💪**
