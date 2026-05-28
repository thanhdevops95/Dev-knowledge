# 🧪 MODULE 02: LABS - Thực hành Docker & Git

## LAB 1: Cơ bản Docker

### LAB 1.1: Cài đặt và Verify

```bash
# Verify Docker installation
docker --version
docker-compose --version

# Test Docker
docker run hello-world
```

**Expected Output:** "Hello from Docker!"

---

### LAB 1.2: Pull và Run Image

```bash
# Pull official Redis image
docker pull redis:7-alpine

# Run Redis container
docker run -d --name my-redis -p 6379:6379 redis:7-alpine

# Verify running
docker ps

# Test connection
docker exec -it my-redis redis-cli ping
# Output: PONG
```

---

## LAB 2: Build Counter App

### LAB 2.1: Tạo Dockerfile

Tạo `Dockerfile`:

```dockerfile
FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

---

### LAB 2.2: Build Image

```bash
# Build image
docker build -t counter-app:v1.0 .

# Verify
docker images | grep counter

# Run container
docker run -d -p 5000:5000 \
  -e REDIS_HOST=host.docker.internal \
  --name counter-web counter-app:v1.0

# Test
curl http://localhost:5000
```

---

## LAB 3: Docker Compose

### LAB 3.1: Tạo docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      REDIS_HOST: redis
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

---

### LAB 3.2: Run Multi-Container

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f web

# Test app
curl http://localhost:5000

# Stop all
docker-compose down
```

---

## LAB 4: Phân nhánh Git

### LAB 4.1: Gitflow Workflow

```bash
# Create develop branch
git checkout -b develop

# Create feature branch
git checkout -b feature/docker-setup

# Make changes
git add Dockerfile docker-compose.yml
git commit -m "Add Docker configuration"

# Merge to develop
git checkout develop
git merge feature/docker-setup

# Tag release
git tag -a v1.0.0 -m "First containerized version"
```

---

## ✅ Checklist

- [ ] Docker Desktop installed
- [ ] Built Counter App image
- [ ] docker-compose.yml working
- [ ] Gitflow applied to project
