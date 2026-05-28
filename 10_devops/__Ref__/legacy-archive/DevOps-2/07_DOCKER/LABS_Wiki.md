# Module 07: Docker Labs

---

## 🎯 Mục tiêu

Sau labs này, bạn sẽ:

- Chạy containers cơ bản
- Viết Dockerfile
- Sử dụng Docker Compose
- Dockerize Counter App

---

## 🔧 Lab 1: First Container

### Bước 1: Kiểm tra Docker

```bash
docker --version
docker run hello-world
```

### Bước 2: Chạy Nginx

```bash
# Pull và run
docker run -d -p 8080:80 --name my-nginx nginx

# Kiểm tra
docker ps

# Truy cập
curl http://localhost:8080
```

### Bước 3: Explore container

```bash
# Logs
docker logs my-nginx

# Exec into container
docker exec -it my-nginx bash

# Trong container:
ls /etc/nginx
cat /etc/nginx/nginx.conf
exit
```

### Bước 4: Cleanup

```bash
docker stop my-nginx
docker rm my-nginx
```

### ✅ Checkpoint Lab 1

- [ ] Container chạy OK
- [ ] Exec vào container được

---

## 📄 Lab 2: Build Docker Image

### Bước 1: Tạo simple app

```bash
mkdir ~/docker-lab
cd ~/docker-lab
```

```python
# app.py
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return f"Hello from Docker! Host: {os.environ.get('HOSTNAME', 'unknown')}"

@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

```bash
# requirements.txt
echo "flask==3.0.0" > requirements.txt
```

### Bước 2: Viết Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Bước 3: Build image

```bash
docker build -t my-flask-app:v1 .

# Xem image
docker images | grep my-flask-app
```

### Bước 4: Run container

```bash
docker run -d -p 5000:5000 --name flask-app my-flask-app:v1

# Test
curl http://localhost:5000
curl http://localhost:5000/health

# Cleanup
docker rm -f flask-app
```

### ✅ Checkpoint Lab 2

- [ ] Build image thành công
- [ ] App chạy trong container

---

## 🔄 Lab 3: Multi-stage Build

### Bước 1: Node.js app

```bash
mkdir ~/node-docker
cd ~/node-docker
```

```javascript
// server.js
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.json({ message: 'Hello from optimized Docker!', time: new Date() });
});

app.listen(3000, () => console.log('Server running on 3000'));
```

```json
// package.json
{
  "name": "node-docker",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  }
}
```

### Bước 2: Regular Dockerfile (để so sánh)

```dockerfile
# Dockerfile.regular
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
```

```bash
docker build -f Dockerfile.regular -t node-regular .
docker images | grep node-regular
# SIZE: ~900MB
```

### Bước 3: Optimized Dockerfile

```dockerfile
# Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY server.js .
EXPOSE 3000
CMD ["node", "server.js"]
```

```bash
docker build -t node-optimized .
docker images | grep node-optimized
# SIZE: ~120MB
```

### Size comparison

```bash
docker images | grep node
# node-regular     900MB
# node-optimized   120MB
# 7x smaller!
```

### ✅ Checkpoint Lab 3

- [ ] Hiểu multi-stage builds
- [ ] Image size giảm đáng kể

---

## 📦 Lab 4: Docker Compose

### Bước 1: Multi-service app

```bash
mkdir ~/compose-lab
cd ~/compose-lab
```

### Bước 2: Create docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

### Bước 3: App sử dụng Redis

```python
# app.py
from flask import Flask
import redis
import os

app = Flask(__name__)
r = redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'))

@app.route('/')
def counter():
    count = r.incr('hits')
    return f'This page has been viewed {count} times.'

@app.route('/reset')
def reset():
    r.set('hits', 0)
    return 'Counter reset!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

```bash
# requirements.txt
flask==3.0.0
redis==5.0.1
```

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

### Bước 4: Run với Compose

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Test
curl http://localhost:5000
curl http://localhost:5000
curl http://localhost:5000
# Count increases each time!

# Reset
curl http://localhost:5000/reset
```

### Bước 5: Manage services

```bash
# Stop
docker-compose stop

# Start
docker-compose start

# Restart single service
docker-compose restart web

# Rebuild
docker-compose up -d --build

# Down (stop + remove)
docker-compose down

# Down + remove volumes
docker-compose down -v
```

### ✅ Checkpoint Lab 4

- [ ] Multi-service với Compose
- [ ] Service communication
- [ ] Volume persistence

---

## 🌐 Lab 5: Networking

### Bước 1: Create custom network

```bash
docker network create myapp-network

docker network ls
```

### Bước 2: Run containers on network

```bash
# Redis on network
docker run -d --network myapp-network --name redis redis:7-alpine

# Check network
docker network inspect myapp-network
```

### Bước 3: App connecting to Redis

```bash
# Run app on same network
docker run -d \
  --network myapp-network \
  --name web \
  -p 5000:5000 \
  -e REDIS_HOST=redis \
  my-flask-app:v1

# Test
curl http://localhost:5000
```

### Bước 4: Verify connectivity

```bash
# From web container, ping redis
docker exec web ping -c 3 redis

# DNS resolution works!
docker exec web nslookup redis
```

### Bước 5: Cleanup

```bash
docker rm -f web redis
docker network rm myapp-network
```

### ✅ Checkpoint Lab 5

- [ ] Custom network created
- [ ] Container DNS resolution

---

## 💾 Lab 6: Volumes

### Bước 1: Named volume

```bash
# Create volume
docker volume create app-data

# Run with volume
docker run -d \
  --name postgres \
  -v app-data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=secret \
  postgres:15-alpine

# Add data
docker exec postgres psql -U postgres -c "CREATE DATABASE test;"

# Remove container
docker rm -f postgres

# Run new container with same volume
docker run -d \
  --name postgres-new \
  -v app-data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=secret \
  postgres:15-alpine

# Data persists!
docker exec postgres-new psql -U postgres -c "\l"
```

### Bước 2: Bind mount (development)

```bash
mkdir ~/app-code
echo "print('Hello from bind mount!')" > ~/app-code/app.py

# Mount folder into container
docker run --rm \
  -v ~/app-code:/app \
  python:3.11-slim \
  python /app/app.py

# Edit file on host
echo "print('Updated!')" > ~/app-code/app.py

# Run again - sees changes immediately
docker run --rm \
  -v ~/app-code:/app \
  python:3.11-slim \
  python /app/app.py
```

### ✅ Checkpoint Lab 6

- [ ] Named volumes persist data
- [ ] Bind mounts for development

---

## 🎓 Tổng kết Labs

| Lab | Skill | Output |
|-----|-------|--------|
| 1 | Run containers | Nginx running |
| 2 | Build images | Custom Flask app |
| 3 | Optimization | Smaller images |
| 4 | Docker Compose | Multi-service app |
| 5 | Networking | Container DNS |
| 6 | Volumes | Data persistence |

---

## ⏭️ Tiếp theo

👉 **[SCENARIOS.md - Tình huống Docker](SCENARIOS.md)**
