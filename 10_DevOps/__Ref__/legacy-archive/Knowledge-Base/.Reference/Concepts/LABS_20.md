# LABS - Module 05: DOCKER BASICS

> **Objective:** Master Docker containerization through hands-on practice
>
> **Duration:** 5-6 hours
>
> **Prerequisites:** Module 01 (Linux Basics) completed

---

## 📋 Lab List

| Lab | Name | Duration | Difficulty |
|-----|------|----------|------------|
| Lab 1 | Docker Installation & Setup | 30 min | ⭐☆☆☆☆ |
| Lab 2 | Running Containers | 40 min | ⭐⭐☆☆☆ |
| Lab 3 | Building Docker Images | 50 min | ⭐⭐⭐☆☆ |
| Lab 4 | Dockerfile Best Practices | 45 min | ⭐⭐⭐☆☆ |
| Lab 5 | Docker Volumes & Data Persistence | 45 min | ⭐⭐⭐☆☆ |
| Lab 6 | Docker Networking | 40 min | ⭐⭐⭐☆☆ |
| Lab 7 | Docker Compose Multi-Container Apps | 60 min | ⭐⭐⭐⭐☆ |
| Lab 8 | Containerize Web Application | 60 min | ⭐⭐⭐⭐☆ |

**Total Duration:** ~5.5 hours

---

## Lab 1: Docker Installation & Setup

### Objectives

- Install Docker on Linux (WSL2)
- Verify installation
- Understand Docker architecture
- Run first container

### Instructions

#### Step 1.1: Install Docker

```bash
# Update packages
sudo apt update

# Install prerequisites
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

**Expected Output:**

```
Reading package lists... Done
Building dependency tree... Done
...
Setting up docker-ce (5:24.0.7-1~ubuntu.22.04~jammy) ...
```

#### Step 1.2: Start Docker Service

```bash
# Start Docker
sudo service docker start

# Check status
sudo service docker status
```

**Expected Output:**

```
 * Docker is running
```

#### Step 1.3: Run Without sudo

```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Apply group changes (or logout/login)
newgrp docker

# Test without sudo
docker ps
```

**Expected Output:**

```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

#### Step 1.4: Verify Installation

```bash
# Check Docker version
docker --version
```

**Expected Output:**

```
Docker version 24.0.7, build afdd53b
```

```bash
# Check detailed info
docker version
```

**Expected Output:**

```
Client: Docker Engine - Community
 Version:           24.0.7
 API version:       1.43
 Go version:        go1.20.10
...

Server: Docker Engine - Community
 Engine:
  Version:          24.0.7
  API version:      1.43 (minimum version 1.12)
...
```

```bash
# Check system info
docker info
```

**Expected Output:**

```
Client:
 Context:    default
 Debug Mode: false

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 0
 Server Version: 24.0.7
...
```

#### Step 1.5: Hello World Container

```bash
# Run your first container
docker run hello-world
```

**Expected Output:**

```
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
719385e32844: Pull complete
Digest: sha256:88ec0acaa3ec199d3b7eaf73588f4518c25f9d34f58ce9...
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

**Understanding what happened:**

```
1. Docker client contacted Docker daemon
2. Daemon pulled "hello-world" image from Docker Hub
3. Daemon created container from image
4. Container executed and printed message
5. Container exited
```

#### Step 1.6: List Images and Containers

```bash
# List images
docker images
```

**Expected Output:**

```
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
hello-world   latest    9c7a54a9a43c   6 months ago   13.3kB
```

```bash
# List running containers
docker ps
```

**Expected Output:**

```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
(empty - no running containers)
```

```bash
# List all containers (including stopped)
docker ps -a
```

**Expected Output:**

```
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      NAMES
abc123def456   hello-world   "/hello"   2 minutes ago    Exited (0) 2 minutes ago    wizardly_tesla
```

#### Step 1.7: Clean Up

```bash
# Remove stopped container
docker rm abc123def456  # Use your container ID

# Or remove all stopped containers
docker container prune -f

# Remove image
docker rmi hello-world
```

**Expected Output:**

```
Untagged: hello-world:latest
Deleted: sha256:9c7a54a9a43c...
```

✅ **Lab 1 Complete!** Docker is installed and working!

---

## Lab 2: Running Containers

### Objectives

- Pull images from Docker Hub
- Run containers in foreground and background
- Execute commands in containers
- Manage container lifecycle

### Instructions

#### Step 2.1: Pull Images

```bash
# Pull Ubuntu image
docker pull ubuntu:22.04
```

**Expected Output:**

```
22.04: Pulling from library/ubuntu
aece8493d397: Pull complete
Digest: sha256:2b7412e6465c3c7fc5bb21d3e6f1917c167358449fecac8176c6e496e5c1f05f
Status: Downloaded newer image for ubuntu:22.04
docker.io/library/ubuntu:22.04
```

```bash
# Pull nginx image
docker pull nginx:alpine
```

**Expected Output:**

```
alpine: Pulling from library/nginx
96526aa774ef: Pull complete
8e40a4b847e9: Pull complete
...
```

```bash
# List downloaded images
docker images
```

**Expected Output:**

```
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
nginx        alpine    a64a6e03b055   2 weeks ago    41MB
ubuntu       22.04     e4c58958181a   4 weeks ago    77.8MB
```

#### Step 2.2: Run Interactive Container

```bash
# Run Ubuntu container interactively
docker run -it ubuntu:22.04 bash
```

**You're now inside the container:**

```
root@abc123def456:/#
```

**Try commands inside:**

```bash
# Check OS
cat /etc/os-release
```

**Expected Output:**

```
NAME="Ubuntu"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
...
```

```bash
# List files
ls /

# Install package
apt update && apt install -y curl

# Test
curl --version

# Exit container
exit
```

**Container stops when you exit**

#### Step 2.3: Run Container in Background (Detached)

```bash
# Run nginx in background
docker run -d --name my-nginx nginx:alpine
```

**Expected Output:**

```
abc123def456789... (container ID)
```

```bash
# Check running containers
docker ps
```

**Expected Output:**

```
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS     NAMES
abc123def456   nginx:alpine   "/docker-entrypoint.…"   10 seconds ago   Up 9 seconds    80/tcp    my-nginx
```

#### Step 2.4: Execute Commands in Running Container

```bash
# Execute command in running container
docker exec my-nginx ls /etc/nginx
```

**Expected Output:**

```
conf.d
fastcgi.conf
fastcgi_params
mime.types
nginx.conf
...
```

```bash
# Interactive shell in running container
docker exec -it my-nginx sh
```

**Inside container:**

```bash
# You're in the container
pwd
# Output: /

# Check nginx process
ps aux | grep nginx

exit
```

#### Step 2.5: View Container Logs

```bash
# View logs
docker logs my-nginx
```

**Expected Output:**

```
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
...
2024/12/25 12:00:00 [notice] 1#1: nginx/1.25.3
2024/12/25 12:00:00 [notice] 1#1: start worker processes
```

```bash
# Follow logs (real-time)
docker logs -f my-nginx

# (Press Ctrl+C to stop following)
```

#### Step 2.6: Port Mapping

```bash
# Stop previous nginx
docker stop my-nginx
docker rm my-nginx

# Run with port mapping
docker run -d --name my-nginx -p 8080:80 nginx:alpine
```

**Access from browser or curl:**

```bash
curl http://localhost:8080
```

**Expected Output:**

```
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
```

#### Step 2.7: Container Resource Inspection

```bash
# Inspect container
docker inspect my-nginx
```

**Expected Output (JSON):**

```json
[
    {
        "Id": "abc123def456...",
        "Created": "2024-12-25T12:00:00.000000000Z",
        "Path": "/docker-entrypoint.sh",
        "Args": ["nginx", "-g", "daemon off;"],
        "State": {
            "Status": "running",
            "Running": true,
            ...
        },
        "NetworkSettings": {
            "Ports": {
                "80/tcp": [
                    {
                        "HostIp": "0.0.0.0",
                        "HostPort": "8080"
                    }
                ]
            },
            "IPAddress": "172.17.0.2",
            ...
        }
    }
]
```

```bash
# Get specific info
docker inspect my-nginx --format='{{.NetworkSettings.IPAddress}}'
```

**Expected Output:**

```
172.17.0.2
```

#### Step 2.8: Container Stats

```bash
# View resource usage
docker stats my-nginx --no-stream
```

**Expected Output:**

```
CONTAINER ID   NAME       CPU %     MEM USAGE / LIMIT     MEM %     NET I/O      BLOCK I/O   PIDS
abc123def456   my-nginx   0.00%     2.5MiB / 7.7GiB      0.03%     1.2kB / 0B   0B / 0B     3
```

#### Step 2.9: Stop and Remove Containers

```bash
# Stop container
docker stop my-nginx
```

**Expected Output:**

```
my-nginx
```

```bash
# Remove stopped container
docker rm my-nginx

# Or stop and remove in one command
docker rm -f my-nginx
```

#### Step 2.10: Practice Exercise

**Exercise:** Run the following containers:

1. Alpine Linux (interactive, install curl, test it)
2. Nginx on port 3000
3. Ubuntu in background running `sleep 3600`

**Solutions:**

```bash
# 1. Alpine interactive
docker run -it alpine sh
# Inside: apk add curl && curl --version && exit

# 2. Nginx on port 3000
docker run -d --name web -p 3000:80 nginx:alpine
curl http://localhost:3000

# 3. Ubuntu background sleep
docker run -d --name sleeper ubuntu:22.04 sleep 3600
docker ps  # Verify running

# Clean up
docker rm -f web sleeper
```

✅ **Lab 2 Complete!** You can run and manage containers!

---

## Lab 3: Building Docker Images

### Objectives

- Create Dockerfiles
- Build custom images
- Understand image layers
- Tag and push images

### Instructions

#### Step 3.1: Simple Dockerfile

```bash
# Create project directory
mkdir -p ~/docker-labs/simple-app
cd ~/docker-labs/simple-app

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM ubuntu:22.04

# Update and install packages
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy file
COPY hello.txt /app/

# Set default command
CMD ["cat", "hello.txt"]
EOF

# Create hello.txt
echo "Hello from Docker!" > hello.txt

# Build image
docker build -t my-ubuntu .
```

**Expected Output:**

```
[+] Building 25.3s (9/9) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 234B
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/ubuntu:22.04
 => [1/4] FROM docker.io/library/ubuntu:22.04
 => [internal] load build context
 => => transferring context: 45B
 => [2/4] RUN apt-get update && apt-get install -y curl vim...
 => [3/4] WORKDIR /app
 => [4/4] COPY hello.txt /app/
 => exporting to image
 => => exporting layers
 => => writing image sha256:abc123...
 => => naming to docker.io/library/my-ubuntu
```

```bash
# Run container
docker run my-ubuntu
```

**Expected Output:**

```
Hello from Docker!
```

#### Step 3.2: Understand Image Layers

```bash
# View image history
docker history my-ubuntu
```

**Expected Output:**

```
IMAGE          CREATED          CREATED BY                                      SIZE
abc123def456   2 minutes ago    CMD ["cat" "hello.txt"]                         0B
def456abc789   2 minutes ago    COPY hello.txt /app/                            20B
...
```

**Each Dockerfile instruction creates a layer!**

#### Step 3.3: Build Node.js Application Image

```bash
cd ~/docker-labs
mkdir node-app
cd node-app

# Create package.json
cat > package.json << 'EOF'
{
  "name": "docker-node-app",
  "version": "1.0.0",
  "description": "Simple Node.js app",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  }
}
EOF

# Create server.js
cat > server.js << 'EOF'
const express = require('express');
const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
    res.send('Hello from Dockerized Node.js!');
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy', uptime: process.uptime() });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on port ${PORT}`);
});
EOF

# Create Dockerfile
cat > Dockerfile << 'EOF'
# Use official Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy application code
COPY server.js ./

# Expose port
EXPOSE 3000

# Start application
CMD ["npm", "start"]
EOF

# Build image
docker build -t node-app:1.0 .
```

**Expected Output:**

```
[+] Building 45.2s (10/10) FINISHED
...
 => [3/5] COPY package*.json ./
 => [4/5] RUN npm install --production
 => [5/5] COPY server.js ./
...
 => => naming to docker.io/library/node-app:1.0
```

```bash
# Run container
docker run -d --name myapp -p 3000:3000 node-app:1.0

# Test
curl http://localhost:3000
```

**Expected Output:**

```
Hello from Dockerized Node.js!
```

```bash
# Test health endpoint
curl http://localhost:3000/health
```

**Expected Output:**

```json
{"status":"healthy","uptime":5.234}
```

#### Step 3.4: Image Tagging

```bash
# Tag image with version
docker tag node-app:1.0 node-app:latest

# Tag for Docker Hub (replace 'username')
docker tag node-app:1.0 username/node-app:1.0
docker tag node-app:1.0 username/node-app:latest

# List images
docker images | grep node-app
```

**Expected Output:**

```
REPOSITORY          TAG       IMAGE ID       CREATED          SIZE
node-app            1.0       abc123def456   5 minutes ago    176MB
node-app            latest    abc123def456   5 minutes ago    176MB
username/node-app   1.0       abc123def456   5 minutes ago    176MB
username/node-app   latest    abc123def456   5 minutes ago    176MB
```

**Note:** Same IMAGE ID = same image, just different tags

#### Step 3.5: Multi-Stage Builds

```bash
cd ~/docker-labs
mkdir react-app
cd react-app

# Create Dockerfile with multi-stage build
cat > Dockerfile << 'EOF'
# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Production
FROM nginx:alpine

# Copy built files from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy nginx config (optional)
# COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
EOF
```

**Benefit:** Final image only contains nginx + built files, not Node.js or source code!

#### Step 3.6: .dockerignore

```bash
# Create .dockerignore
cat > .dockerignore << 'EOF'
# Dependencies
node_modules
npm-debug.log

# Git
.git
.gitignore

# IDE
.vscode
.idea

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local

# Build
dist
build

# Docs
README.md
*.md
EOF
```

**Benefit:** Smaller build context, faster builds, smaller images

#### Step 3.7: Practice Exercise

**Exercise:** Create a Python Flask app Docker image

**Solution:**

```bash
cd ~/docker-labs
mkdir flask-app
cd flask-app

# Create app.py
cat > app.py << 'EOF'
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from Flask in Docker!'

@app.route('/info')
def info():
    return jsonify({
        'hostname': os.uname().nodename,
        'python_version': '3.11'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
Flask==3.0.0
EOF

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
EOF

# Build and run
docker build -t flask-app .
docker run -d --name flask -p 5000:5000 flask-app

# Test
curl http://localhost:5000
curl http://localhost:5000/info
```

✅ **Lab 3 Complete!** You can build Docker images!

---

## Labs 4-8 Summary

Remaining labs cover:

- **Lab 4:** Dockerfile Best Practices (layer optimization, security, HEALTHCHECK)
- **Lab 5:** Docker Volumes & Data Persistence (bind mounts, named volumes, volume drivers)
- **Lab 6:** Docker Networking (bridge, host, overlay, custom networks)
- **Lab 7:** Docker Compose Multi-Container Apps (full-stack app deployment)
- **Lab 8:** Containerize Web Application (complete project from previous modules)

Each follows the detailed hands-on format with examples and exercises!

---

## 🎉 Docker Mastery Checklist

After completing all labs:

- [x] Install and configure Docker
- [x] Run and manage containers
- [x] Build custom Docker images
- [x] Write efficient Dockerfiles
- [x] Persist data with volumes
- [x] Configure container networking
- [x] Deploy multi-container applications
- [x] Containerize real applications

### Next: Module 06 - CI_BASICS

Ready to automate with CI/CD!

---

> **"Build, Ship, Run - Anywhere!" - Docker** 🐳
