# 📋 Docker Compose - Cheatsheet

> **Quick Reference for Docker Compose**
>
> *Tra cứu nhanh Docker Compose*

---

## 🔧 Basic Commands (Lệnh cơ bản)

```bash
docker compose up -d        # Start services (Khởi động services)
docker compose down         # Stop and remove (Dừng và xóa)
docker compose ps           # List services (Liệt kê services)
docker compose logs -f      # Follow logs (Theo dõi logs)
docker compose build        # Build images (Build images)
docker compose pull         # Pull images (Tải images)
docker compose restart      # Restart services (Khởi động lại)
docker compose exec web sh  # Enter container (Vào container)
```

---

## 📝 Basic docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

---

## 🌐 Networks (Mạng)

```yaml
services:
  web:
    networks:
      - frontend
      - backend
  
  db:
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true  # No external access (Không truy cập bên ngoài)
```

---

## 💾 Volumes

```yaml
services:
  app:
    volumes:
      - ./src:/app/src          # Bind mount
      - data:/app/data          # Named volume
      - /etc/config:/config:ro  # Read-only

volumes:
  data:
    driver: local
```

---

## 🔐 Environment Variables (Biến môi trường)

```yaml
services:
  app:
    environment:
      - DB_HOST=db
      - DB_PORT=5432
    env_file:
      - .env
      - .env.local
```

---

## 🏥 Health Checks

```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

---

## 📊 Resource Limits (Giới hạn tài nguyên)

```yaml
services:
  app:
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

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
