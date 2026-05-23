# 🐳 Module 2.2: Docker Compose

[![Duration](https://img.shields.io/badge/Duration-1%20week-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Intermediate-orange?style=flat-square)](.)

> **Multi-container Orchestration** - Manage applications with Docker Compose.
>
> *Điều phối đa container - Quản lý ứng dụng với Docker Compose.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Write docker-compose.yml files (Viết docker-compose.yml)
- ✅ Manage multi-container applications (Quản lý ứng dụng đa container)
- ✅ Configure networks and volumes (Cấu hình mạng và volumes)
- ✅ Use environment variables and secrets (Sử dụng biến môi trường và secrets)
- ✅ Implement development workflows (Triển khai quy trình phát triển)
- ✅ Deploy with Compose in production (Deploy với Compose trong production)

---

## 📚 Content (Nội dung)

### 1. What is Docker Compose? (Docker Compose là gì?)

**Docker Compose** is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application's services.

*Docker Compose là công cụ để định nghĩa và chạy các ứng dụng Docker đa container. Với Compose, bạn sử dụng file YAML để cấu hình các dịch vụ của ứng dụng.*

#### Why Docker Compose? (Tại sao cần Docker Compose?)

**Problem:** A real application usually has multiple containers (web, api, database, cache...). Starting each container with `docker run` is complex:

*Vấn đề: Một ứng dụng thực tế thường có nhiều containers (web, api, database, cache...). Khởi động từng container bằng `docker run` rất phức tạp:*

```bash
# Without Compose - many complex commands:
# Không dùng Compose - phải chạy nhiều lệnh phức tạp:
docker network create myapp
docker run -d --network myapp --name db -e POSTGRES_PASSWORD=secret postgres:15
docker run -d --network myapp --name api --link db -p 3000:3000 myapi:latest
docker run -d --network myapp --name web --link api -p 80:80 nginx:alpine
```

**Solution:** Docker Compose - 1 config file, 1 single command.

*Giải pháp: Docker Compose - 1 file cấu hình, 1 lệnh duy nhất.*

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCKER COMPOSE                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   docker-compose.yml                                         │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  services:                                           │   │
│   │    web: ...                                          │   │
│   │    api: ...      ──────► docker compose up ─┐       │   │
│   │    db: ...                                    │       │   │
│   │    redis: ...                                 │       │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                    │         │
│                                                    ▼         │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│   │   Web    │  │   API    │  │   DB     │  │  Redis   │   │
│   │ (nginx)  │──│ (node)   │──│(postgres)│──│ (cache)  │   │
│   └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│   Tất cả trong 1 isolated network (All in isolated network) │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Key benefits (Lợi ích chính):**

| Benefit (Lợi ích) | Description (Mô tả) |
|-------------------|---------------------|
| **Single configuration** | Define app stack in one `docker-compose.yml` *(Định nghĩa app trong 1 file)* |
| **One command** | `docker compose up` starts everything *(1 lệnh khởi động tất cả)* |
| **Isolated environments** | Creates isolated networks for each project *(Tạo mạng cách ly cho mỗi project)* |
| **Reproducible** | Anyone can run the same with the same file *(Ai cũng có thể chạy giống nhau)* |
| **Environment parity** | Dev/Staging/Production use same config *(Dev/Staging/Prod dùng cùng config)* |

---

### 2. Docker Compose Basics (Cơ bản Docker Compose)

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    
  api:
    build: ./api
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    depends_on:
      - db
    
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

### Commands (Các lệnh quan trọng)

These are the essential commands you'll use daily with Docker Compose.

*Đây là các lệnh cần thiết bạn sẽ dùng hàng ngày với Docker Compose.*

```bash
docker compose up -d          # Start all services (Khởi động tất cả)
docker compose down           # Stop and remove (Dừng và xóa)
docker compose ps             # List services (Liệt kê services)
docker compose logs -f        # View logs (Xem logs)
docker compose exec api sh    # Exec into service (Vào service)
docker compose build          # Build images (Build images)
```

---

### 3. Service Configuration (Cấu hình Service)

Each service in `docker-compose.yml` has many configuration options. Here are the most common ones.

*Mỗi service trong `docker-compose.yml` có nhiều tùy chọn cấu hình. Dưới đây là các tùy chọn phổ biến nhất.*

```yaml
services:
  app:
    # Build from Dockerfile (Build từ Dockerfile)
    build:
      context: ./app
      dockerfile: Dockerfile
      args:
        - NODE_ENV=production
    
    # Or use image (Hoặc sử dụng image)
    image: myapp:latest
    
    # Container name (Tên container)
    container_name: myapp-container
    
    # Restart policy (Chính sách khởi động lại)
    restart: unless-stopped
    
    # Port mapping (Ánh xạ cổng)
    ports:
      - "3000:3000"
      - "3001:3001"
    
    # Environment (Biến môi trường)
    environment:
      - NODE_ENV=production
      - DB_HOST=db
    
    # Or from file (Hoặc từ file)
    env_file:
      - .env
      - .env.production
    
    # Dependencies (Phụ thuộc)
    depends_on:
      - db
      - cache
    
    # Health check (Kiểm tra sức khỏe)
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

### 4. Networking (Mạng)

```yaml
version: '3.8'

services:
  frontend:
    networks:
      - frontend-network
  
  api:
    networks:
      - frontend-network
      - backend-network
  
  db:
    networks:
      - backend-network

networks:
  frontend-network:
    driver: bridge
  
  backend-network:
    driver: bridge
    internal: true  # No external access (Không truy cập từ bên ngoài)
```

---

### 5. Volumes

```yaml
services:
  db:
    volumes:
      # Named volume (Volume có tên)
      - db-data:/var/lib/postgresql/data
      
      # Bind mount (Mount trực tiếp)
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
      
      # Read-only bind mount (Mount chỉ đọc)
      - ./config:/etc/config:ro

volumes:
  db-data:
    driver: local
  
  # External volume - pre-created (Volume ngoài - tạo sẵn)
  logs:
    external: true
```

---

### 6. Environment Management (Quản lý môi trường)

```yaml
# .env file
POSTGRES_PASSWORD=mysecret
API_KEY=abc123

# docker-compose.yml
services:
  api:
    environment:
      - DB_PASSWORD=${POSTGRES_PASSWORD}
      - API_KEY=${API_KEY}
```

### Secrets (Swarm mode)

```yaml
services:
  api:
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

---

### 7. Multiple Compose Files (Nhiều file Compose)

```yaml
# docker-compose.yml (base - cơ bản)
services:
  api:
    build: ./api
    ports:
      - "3000:3000"

# docker-compose.override.yml (development - phát triển)
services:
  api:
    volumes:
      - ./api:/app
    environment:
      - DEBUG=true

# docker-compose.prod.yml (production - sản xuất)
services:
  api:
    image: myregistry/api:latest
    deploy:
      replicas: 3
```

```bash
# Development - uses override automatically (Dev - tự động dùng override)
docker compose up

# Production (Sản xuất)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

---

### 8. Resource Limits (Giới hạn tài nguyên)

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

---

### 9. Logging (Ghi log)

```yaml
services:
  api:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 📝 Module Files (Các file trong Module)

| File | Description |
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
| [2.1 Docker Advanced](../2.1_Docker_Advanced/) | **2.2 Docker Compose** | [2.3 Jenkins](../2.3_Jenkins/) |

---

**Master container orchestration! 🐳**

*Thành thạo điều phối container!*

</div>
