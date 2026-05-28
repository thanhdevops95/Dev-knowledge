# Docker Basics - Cheatsheet

> **Essential Docker commands & patterns for daily DevOps work**

---

## 🐳 DOCKER BASICS

### Installation Check

```bash
# Version
docker --version
docker version

# System info
docker info

# Test installation
docker run hello-world
```

---

## 📦 IMAGES

### Pull Images

```bash
# Pull from Docker Hub
docker pull ubuntu
docker pull ubuntu:20.04
docker pull python:3.9
docker pull nginx:alpine

# Search images
docker search nginx
```

### List & Remove Images

```bash
# List images
docker images
docker image ls

# Remove image
docker rmi image_id
docker rmi ubuntu:20.04

# Remove unused images
docker image prune

# Remove all images (CAREFUL!)
docker rmi $(docker images -q)
```

### Build Images

```bash
# Build from Dockerfile
docker build -t myapp .
docker build -t myapp:1.0 .
docker build -t myapp:latest .

# Build with different Dockerfile
docker build -f Dockerfile.prod -t myapp:prod .

# Build with no cache
docker build --no-cache -t myapp .

# Build with build args
docker build --build-arg VERSION=1.0 -t myapp .
```

### Tag & Push

```bash
# Tag image
docker tag myapp:latest username/myapp:latest
docker tag myapp:1.0 username/myapp:1.0

# Login to Docker Hub
docker login

# Push to Docker Hub
docker push username/myapp:latest
docker push username/myapp:1.0

# Logout
docker logout
```

---

## 🚀 CONTAINERS

### Run Containers

```bash
# Basic run
docker run ubuntu
docker run -it ubuntu bash          # Interactive with terminal

# Run in background (detached)
docker run -d nginx

# Run with name
docker run --name mycontainer nginx

# Run with port mapping
docker run -p 8080:80 nginx         # Host:Container
docker run -p 80:80 -p 443:443 nginx

# Run with environment variables
docker run -e DB_PASSWORD=secret myapp
docker run -e DB_HOST=localhost -e DB_PORT=5432 myapp

# Run with volume
docker run -v /host/path:/container/path myapp
docker run -v mydata:/app/data myapp

# Run with restart policy
docker run --restart=always nginx
docker run --restart=unless-stopped nginx

# Run with resource limits
docker run -m 512m --cpus=1 myapp   # 512MB RAM, 1 CPU

# Remove after exit
docker run --rm ubuntu echo "Hello"
```

### List Containers

```bash
# Running containers
docker ps

# All containers (including stopped)
docker ps -a

# Latest container
docker ps -l

# Container IDs only
docker ps -q

# Container sizes
docker ps -s
```

### Container Lifecycle

```bash
# Start stopped container
docker start container_id
docker start mycontainer

# Stop running container
docker stop container_id
docker stop mycontainer

# Restart container
docker restart container_id

# Pause container
docker pause container_id

# Unpause container
docker unpause container_id

# Kill container (force stop)
docker kill container_id

# Remove container
docker rm container_id
docker rm -f container_id           # Force remove running

# Remove all stopped containers
docker container prune

# Remove all containers (CAREFUL!)
docker rm -f $(docker ps -aq)
```

### Container Interaction

```bash
# View logs
docker logs container_id
docker logs -f container_id         # Follow logs
docker logs --tail 100 container_id # Last 100 lines
docker logs --since 1h container_id # Last hour

# Execute command in running container
docker exec container_id ls /app
docker exec -it container_id bash   # Interactive shell
docker exec -it container_id sh     # For Alpine

# Copy files to/from container
docker cp file.txt container_id:/app/
docker cp container_id:/app/output.txt .

# Inspect container
docker inspect container_id
docker inspect --format='{{.NetworkSettings.IPAddress}}' container_id

# Stats (resource usage)
docker stats
docker stats container_id

# Top (processes in container)
docker top container_id
```

---

## 📝 DOCKERFILE

### Common Instructions

```dockerfile
# Base image
FROM ubuntu:20.04
FROM python:3.9-slim
FROM node:16-alpine

# Metadata
LABEL maintainer="you@example.com"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY . /app
COPY --chown=user:group file.txt /app/

# Add (can extract tar & fetch URLs)
ADD https://example.com/file.tar.gz /app/
ADD archive.tar.gz /app/

# Run commands
RUN apt-get update && apt-get install -y curl
RUN pip install -r requirements.txt
RUN npm install

# Environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV PATH="/app/bin:${PATH}"

# Expose port (documentation only)
EXPOSE 80
EXPOSE 3000 8080

# Volume (mount point)
VOLUME /app/data

# User
USER node
USER 1000

# Default command
CMD ["python", "app.py"]
CMD ["npm", "start"]

# Entrypoint (can't be easily overridden)
ENTRYPOINT ["python"]
CMD ["app.py"]              # Arguments to ENTRYPOINT

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
```

### Best Practices

```dockerfile
# Multi-stage build
FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/server.js"]

# Combine RUN commands (fewer layers)
RUN apt-get update && \
    apt-get install -y curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Use .dockerignore
# Create .dockerignore file:
# node_modules
# .git
# *.log
```

---

## 🔧 DOCKER COMPOSE

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    image: myapp:latest
    container_name: web_app
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379
    env_file:
      - .env
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app
      - static-data:/app/static
    networks:
      - mynetwork
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - mynetwork

  redis:
    image: redis:6-alpine
    networks:
      - mynetwork

volumes:
  db-data:
  static-data:

networks:
  mynetwork:
```

### Commands

```bash
# Start services
docker-compose up
docker-compose up -d              # Detached

# Stop services
docker-compose down
docker-compose down -v            # Remove volumes too

# Build/rebuild
docker-compose build
docker-compose up --build         # Build + start

# View services
docker-compose ps

# View logs
docker-compose logs
docker-compose logs -f            # Follow
docker-compose logs web           # Specific service

# Execute command
docker-compose exec web bash
docker-compose exec db psql -U user

# Scale service
docker-compose up -d --scale web=3

# Restart service
docker-compose restart web

# Pull images
docker-compose pull

# Use different compose file
docker-compose -f docker-compose.prod.yml up -d
```

---

## 💾 VOLUMES

```bash
# Create volume
docker volume create mydata

# List volumes
docker volume ls

# Inspect volume
docker volume inspect mydata

# Remove volume
docker volume rm mydata

# Remove unused volumes
docker volume prune

# Use volume in container
docker run -v mydata:/app/data myapp

# Bind mount (host directory)
docker run -v $(pwd):/app myapp
docker run -v /host/path:/container/path myapp
```

---

## 🌐 NETWORKS

```bash
# Create network
docker network create mynetwork
docker network create --driver bridge mynetwork

# List networks
docker network ls

# Inspect network
docker network inspect mynetwork

# Connect container to network
docker network connect mynetwork container_id

# Disconnect
docker network disconnect mynetwork container_id

# Remove network
docker network rm mynetwork

# Create container on network
docker run --network mynetwork myapp
```

---

## 🧹 CLEANUP

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune
docker image prune -a             # All unused

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Remove everything (CAREFUL!)
docker system prune
docker system prune -a            # Include images
docker system prune -a --volumes  # Include volumes

# Show disk usage
docker system df
```

---

## 🐛 DEBUGGING

```bash
# View container logs
docker logs -f container_id

# Execute shell in running container
docker exec -it container_id /bin/bash
docker exec -it container_id /bin/sh    # Alpine

# Inspect container details
docker inspect container_id

# Port mappings
docker port container_id

# Process list
docker top container_id

# Resource usage
docker stats container_id

# Events (real-time)
docker events

# Check if container is healthy
docker inspect --format='{{.State.Health.Status}}' container_id
```

---

## 📊 COMMON PATTERNS

### Development Workflow

```bash
# Local development
docker-compose up -d
docker-compose logs -f

# Code changes (with volume mount)
# Changes reflect immediately, no rebuild

# Rebuild after dependency changes
docker-compose up --build

# Stop everything
docker-compose down
```

### Production Deployment

```bash
# Build production image
docker build -t myapp:1.0.0 .

# Tag for registry
docker tag myapp:1.0.0 username/myapp:1.0.0
docker tag myapp:1.0.0 username/myapp:latest

# Push to registry
docker push username/myapp:1.0.0
docker push username/myapp:latest

# On production server
docker pull username/myapp:1.0.0
docker run -d -p 80:80 --restart=always username/myapp:1.0.0
```

### Health Check Pattern

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1
```

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' container_id
```

---

## 🔐 SECURITY

```bash
# Run as non-root user
# In Dockerfile:
USER node
USER 1000

# Don't expose unnecessary ports
EXPOSE 5000              # Only what's needed

# Use secrets (not environment variables)
docker secret create db_password password.txt
docker service create --secret db_password myapp

# Scan images
docker scan myapp:latest

# Use trusted base images
FROM python:3.9-slim     # Official images
```

---

<div align="center">

**Docker = DevOps foundation! 🐳**

**Master these commands for daily DevOps work! 💪**

</div>
