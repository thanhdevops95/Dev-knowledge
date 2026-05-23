# ✅ Solutions: Docker Fundamentals

> **Solutions for Exercises. Try to solve it yourself first!**
>
> *Đáp án cho Exercises. Hãy thử tự giải trước!*

---

## Exercise 1: Container Basics

```bash
# 1. Run with custom name
docker run -d --name my-nginx nginx

# 2. Exec and check version
docker exec -it my-nginx nginx -v

# 3. Copy file from container
docker cp my-nginx:/etc/nginx/nginx.conf ./nginx.conf

# 4. View logs
docker logs my-nginx
docker logs -f my-nginx  # follow

# 5. Stop, start, restart
docker stop my-nginx
docker start my-nginx
docker restart my-nginx

# 6. Remove
docker stop my-nginx
docker rm my-nginx
```

---

## Exercise 2: Dockerfile

```dockerfile
# Dockerfile
FROM node:18-alpine

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copy package files first (cache layer)
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

EXPOSE 3000

CMD ["node", "server.js"]
```

```bash
docker build -t my-node-app .
docker run -d -p 3000:3000 my-node-app
```

---

## Exercise 3: Multi-stage Build

```dockerfile
# Stage 1: Build
FROM node:18 AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Serve
FROM nginx:alpine

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built files
COPY --from=builder /app/build /usr/share/nginx/html

# Non-root user
RUN chown -R nginx:nginx /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

```bash
docker build -t react-app .
docker images react-app  # Should be ~25-30MB
```

---

## Exercise 4: Volumes

```bash
# 1. Create volume
docker volume create mydata

# 2. Run MySQL with volume
docker run -d \
  --name mydb \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=testdb \
  -v mydata:/var/lib/mysql \
  mysql:8

# 3. Insert data
docker exec -it mydb mysql -uroot -psecret -e \
  "USE testdb; CREATE TABLE users (id INT, name VARCHAR(50)); INSERT INTO users VALUES (1, 'John');"

# 4. Stop and remove
docker stop mydb
docker rm mydb

# 5. New container with same volume
docker run -d \
  --name mydb2 \
  -e MYSQL_ROOT_PASSWORD=secret \
  -v mydata:/var/lib/mysql \
  mysql:8

# 6. Verify data
docker exec -it mydb2 mysql -uroot -psecret -e "USE testdb; SELECT * FROM users;"
# Output: 1, John (data persisted!)
```

---

## Exercise 5: Networking

```bash
# 1. Create network
docker network create myapp-network

# 2. Run database
docker run -d \
  --name db \
  --network myapp-network \
  -e POSTGRES_PASSWORD=secret \
  postgres:15

# 3. Run backend
docker run -d \
  --name api \
  --network myapp-network \
  -e DATABASE_URL=postgres://postgres:secret@db:5432/postgres \
  my-backend

# 4. Run frontend
docker run -d \
  --name web \
  --network myapp-network \
  -p 80:80 \
  my-frontend

# 5. Verify communication
docker exec api ping -c 2 db
docker exec web curl http://api:3000/health

# 6. Inspect network
docker network inspect myapp-network
```

---

## Exercise 6: Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - app-network

  backend:
    build: ./backend
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://postgres:secret@db:5432/appdb
    depends_on:
      - db
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: appdb
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

```bash
docker compose up -d
docker compose ps
docker compose logs -f
docker compose down
```

---

## Exercise 7: Image Optimization

### Before (Unoptimized)

```dockerfile
FROM node:18

WORKDIR /app
COPY . .
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]
```

### After (Optimized)

```dockerfile
# Use alpine for smaller size
FROM node:18-alpine AS builder

WORKDIR /app

# Copy only package files first
COPY package*.json ./

# Install with production only
RUN npm ci --only=production

# Production stage
FROM node:18-alpine

# Non-root user
RUN addgroup -S app && adduser -S app -G app

WORKDIR /app

# Copy from builder
COPY --from=builder /app/node_modules ./node_modules
COPY --chown=app:app . .

USER app

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/health || exit 1

EXPOSE 3000

CMD ["node", "server.js"]
```

### .dockerignore

```
node_modules
npm-debug.log
Dockerfile
.git
.gitignore
.env
*.md
tests
coverage
```

### Comparison

```bash
# Build both versions
docker build -f Dockerfile.old -t app:old .
docker build -f Dockerfile.new -t app:new .

# Compare sizes
docker images | grep app
# app   old   ~950MB
# app   new   ~150MB
```

---

**[← Back to Exercises](./EXERCISES.md)** | **[Back to README →](./README.md)**
