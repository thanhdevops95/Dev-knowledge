# SOLUTIONS - Foundation Track

Complete solutions for all exercises across modules 00-09.

---

## 📌 How to Use This File

1. **Try exercises first** - Don't look at solutions immediately
2. **Compare approaches** - Your solution might be different but equally valid
3. **Learn alternatives** - Solutions often show multiple approaches
4. **Practice variations** - Modify exercises and solve again

---

## Module 00: SETUP - Exercise Solutions

### Exercise 1: WSL2 Configuration Check

```bash
# Check WSL version
wsl --version
# Output: WSL version: 2.0.9.0...

# List distributions
wsl --list --verbose
# Output shows VERSION = 2 for Ubuntu

# Check kernel
uname -r  
# Should contain: microsoft-standard-WSL2

# Check OS
cat /etc/os-release
# NAME="Ubuntu" VERSION="22.04..."
```

### Exercise 3: SSH Key Generation

```bash
# Generate key
ssh-keygen -t ed25519 -C "your-email@example.com"
# Press Enter to accept default location
# Enter passphrase (optional but recommended)

# Start agent
eval "$(ssh-agent -s)"

# Add key
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub | clip.exe  # WSL
# Or manually cat and copy

# Test GitHub connection
ssh -T git@github.com
# Success: "Hi username! You've successfully authenticated"
```

### Exercise 6: Environment Health Check Script

```bash
#!/bin/bash
# health-check.sh

echo "=== Environment Health Check ==="
echo ""

# Check Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    GIT_NAME=$(git config user.name)
    GIT_EMAIL=$(git config user.email)
    
    echo "✓ Git: $GIT_VERSION"
    [ -n "$GIT_NAME" ] && echo "  Name: $GIT_NAME" || echo "  ✗ Name not set"
    [ -n "$GIT_EMAIL" ] && echo "  Email: $GIT_EMAIL" || echo "  ✗ Email not set"
else
    echo "✗ Git not found"
fi

echo ""

# Check SSH
if [ -f ~/.ssh/id_ed25519 ]; then
    echo "✓ SSH key exists"
    ssh -T git@github.com 2>&1 | grep -q "successfully authenticated" && \
        echo "  ✓ GitHub connection works" || \
        echo "  ✗ GitHub connection failed"
else
    echo "✗ SSH key not found"
fi

echo ""

# Check Node.js
if command -v node &> /dev/null; then
    echo "✓ Node.js: $(node --version)"
    echo "✓ NPM: $(npm --version)"
else
    echo "✗ Node.js not found"
fi

echo ""

# Check Zsh
if command -v zsh &> /dev/null; then
    echo "✓ Zsh: $(zsh --version)"
    [ -d ~/.oh-my-zsh ] && echo "  ✓ Oh My Zsh installed" || echo "  - Oh My Zsh not installed"
else
    echo "✗ Zsh not found"
fi

echo ""
echo "Health check complete!"
```

---

## Module 01: LINUX BASICS - Exercise Solutions

### Exercise 11: Extract Emails from File

```bash
# Method 1: Using grep with regex
grep -Eo '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' file.txt | sort -u

# Method 2: Using sed
sed -n 's/.*\([a-zA-Z0-9._%+-]\+@[a-zA-Z0-9.-]\+\.[a-zA-Z]\{2,\}\).*/\1/p' file.txt | sort -u

# Method 3: Using awk
awk '{for(i=1;i<=NF;i++){if($i~/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/){print $i}}}' file.txt | sort -u
```

### Exercise 12: Count Unique IPs in Access Log

```bash
# Extract IP addresses (assuming standard format)
awk '{print $1}' access.log | sort | uniq -c | sort -rn

# Total unique IPs
awk '{print $1}' access.log | sort -u | wc -l

# Top 10 IPs
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10

# With percentage
awk '{print $1}' access.log | \
  sort | uniq -c | sort -rn | \
  awk -v total=$(wc -l < access.log) '{printf "%s\t%s\t%.2f%%\n", $1, $2, ($1/total)*100}'
```

### Exercise 26: Backup Script with Rotation

```bash
#!/bin/bash
# backup-rotation.sh

# Configuration
SOURCE_DIR="/var/www"
BACKUP_DIR="/backup"
RETENTION_DAYS=7
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_$DATE.tar.gz"

# Create backup
echo "Creating backup..."
tar -czf "$BACKUP_DIR/$BACKUP_FILE" "$SOURCE_DIR"

if [ $? -eq 0 ]; then
    echo "✓ Backup created: $BACKUP_FILE"
    SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
    echo "  Size: $SIZE"
else
    echo "✗ Backup failed!"
    exit 1
fi

# Rotate old backups
echo "Removing backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete

# List current backups
echo ""
echo "Current backups:"
ls -lh "$BACKUP_DIR"/backup_*.tar.gz | awk '{print $9, $5, $6, $7, $8}'

echo ""
echo "Backup rotation complete!"
```

---

## Module 02: GIT & GITHUB - Exercise Solutions

### Exercise 7: Merge Conflict Resolution

```bash
# Create scenario
git checkout main
echo "Line 1 from main" > conflict.txt
git add conflict.txt
git commit -m "Add line from main"

git checkout -b feature
echo "Line 1 from feature" > conflict.txt
git add conflict.txt
git commit -m "Add line from feature"

# Merge will create conflict
git checkout main
git merge feature

# Conflict appears:
# <<<<<<< HEAD
# Line 1 from main
# =======
# Line 1 from feature
# >>>>>>> feature

# Resolve by editing file
cat > conflict.txt << 'EOF'
Line 1 - merged version combining both
EOF

# Complete merge
git add conflict.txt
git commit -m "Resolve conflict between main and feature"
```

### Exercise 16: Interactive Rebase to Squash

```bash
# Create multiple commits
echo "v1" > file.txt; git add file.txt; git commit -m "Version 1"
echo "v2" > file.txt; git add file.txt; git commit -m "Version 2"
echo "v3" > file.txt; git add file.txt; git commit -m "Version 3"
echo "v4" > file.txt; git add file.txt; git commit -m "Version 4"
echo "v5" > file.txt; git add file.txt; git commit -m "Version 5"

# Interactive rebase last 5 commits
git rebase -i HEAD~5

# In editor, change all but first "pick" to "squash" or "s":
# pick abc1234 Version 1
# squash def5678 Version 2
# squash ghi9012 Version 3
# squash jkl3456 Version 4
# squash mno7890 Version 5

# Save and close editor
# Next editor opens for combined commit message
# Write: "Implement feature X with versions 1-5"
# Save and close

# Result: 5 commits squashed into 1
git log --oneline -1
# Shows single commit with combined message
```

---

## Module 05: DOCKER - Exercise Solutions

### Exercise 20: Complete MERN Stack Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  # MongoDB Database
  mongodb:
    image: mongo:6
    container_name: mern_mongodb
    restart: unless-stopped
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=secret123
      - MONGO_INITDB_DATABASE=mernapp
    volumes:
      - mongodb_data:/data/db
    ports:
      - "27017:27017"
    networks:
      - mern_network

  # Express Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: mern_backend
    restart: unless-stopped
    environment:
      - NODE_ENV=development
      - PORT=5000
      - MONGODB_URI=mongodb://admin:secret123@mongodb:27017/mernapp?authSource=admin
    ports:
      - "5000:5000"
    depends_on:
      - mongodb
    networks:
      - mern_network
    volumes:
      - ./backend:/app
      - /app/node_modules

  # React Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: mern_frontend
    restart: unless-stopped
    environment:
      - REACT_APP_API_URL=http://localhost:5000/api
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - mern_network
    volumes:
      - ./frontend:/app
      - /app/node_modules

  # NGINX Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: mern_nginx
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend
    networks:
      - mern_network

networks:
  mern_network:
    driver: bridge

volumes:
  mongodb_data:
```

```nginx
# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }

    upstream backend {
        server backend:5000;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://frontend;
        }

        location /api {
            proxy_pass http://backend;
        }
    }
}
```

---

## Module 06: CI/CD - Exercise Solutions

### Exercise 15: Complete CI/CD Pipeline

```yaml
# .github/workflows/complete-pipeline.yml
name: Complete CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
      - run: npm run test:coverage
      - uses: codecov/codecov-action@v3

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/myapp:latest
            ${{ secrets.DOCKER_USERNAME }}/myapp:${{ github.sha }}

  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - name: Deploy to staging
        run: |
          # SSH to staging server and deploy
          echo "Deploying to staging..."
          
  deploy-production:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com
    steps:
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
```

---

## 🎯 General Problem-Solving Approach

For any exercise:

1. **Understand the problem** - Read carefully
2. **Plan your approach** - Think before coding
3. **Start simple** - Get basic version working
4. **Test incrementally** - Don't wait until the end
5. **Handle errors** - Consider edge cases
6. **Document** - Add comments and README
7. **Refactor** - Improve after it works
8. **Learn alternatives** - Compare with solutions

---

> **These solutions are guides, not gospel. Your approach may be equally valid!** 💡
